import sqlite3,os,json,threading,time
from pathlib import Path
from .persistence import open_database,StorageUnavailable
ROOT=Path(__file__).resolve().parents[2]
LOCK=threading.RLock()
DB=open_database(ROOT/'finn.sqlite3')
def load(name):return json.loads((ROOT/'demo'/f'{name}.json').read_text())
COMPANIES=load('companies');BARS=load('bars');DOCS=load('documents');BUNDLED_FILINGS=load('filings')
with LOCK:
    DB.begin(2026110101)
    try:
        for sql in (
            'CREATE TABLE IF NOT EXISTS answers (key TEXT PRIMARY KEY,payload TEXT NOT NULL)',
            'CREATE TABLE IF NOT EXISTS alerts (id TEXT PRIMARY KEY,payload TEXT NOT NULL)',
            'CREATE TABLE IF NOT EXISTS raw_filings (id TEXT PRIMARY KEY,payload TEXT NOT NULL)',
            'CREATE TABLE IF NOT EXISTS private_answers_v2 (key TEXT PRIMARY KEY,payload TEXT NOT NULL,created DOUBLE PRECISION NOT NULL)',
            'CREATE TABLE IF NOT EXISTS ai_usage(day TEXT PRIMARY KEY,calls INTEGER NOT NULL,reserved INTEGER NOT NULL,reported INTEGER NOT NULL,failures INTEGER NOT NULL)',
            'CREATE TABLE IF NOT EXISTS ai_clients(day TEXT,client TEXT,calls INTEGER,PRIMARY KEY(day,client))',
            'CREATE TABLE IF NOT EXISTS ai_minutes(bucket BIGINT,client TEXT,calls INTEGER,PRIMARY KEY(bucket,client))',
            'CREATE TABLE IF NOT EXISTS ai_leases(id TEXT PRIMARY KEY,expires DOUBLE PRECISION)',
            'CREATE TABLE IF NOT EXISTS security_meta(name TEXT PRIMARY KEY,value TEXT NOT NULL)'):
            DB.execute(sql)
        DB.executemany('INSERT INTO raw_filings VALUES (?,?) ON CONFLICT DO NOTHING',[(f['id'],json.dumps(f)) for f in BUNDLED_FILINGS])
        DB.commit()
    except Exception:DB.rollback();raise
def filings(allow_snapshot_fallback=False):
    with LOCK:
        try:return [json.loads(r[0]) for r in DB.execute('SELECT payload FROM raw_filings')]
        except StorageUnavailable:
            # Primary document research can still retrieve bundled evidence, without
            # replacing quota storage or claiming that the remote DB is healthy.
            if allow_snapshot_fallback:return BUNDLED_FILINGS
            raise
def cache_get(key):
    with LOCK:
        try:row=DB.execute('SELECT payload FROM private_answers_v2 WHERE key=? AND created>?',(key,time.time()-86400)).fetchone()
        except StorageUnavailable:return None
        return json.loads(row[0]) if row else None
def cache_put(key,payload):
    with LOCK:
        try:
            DB.begin(2026110102)
            DB.execute('DELETE FROM private_answers_v2 WHERE created<?',(time.time()-86400,))
            DB.execute('INSERT INTO private_answers_v2 VALUES (?,?,?) ON CONFLICT(key) DO UPDATE SET payload=excluded.payload,created=excluded.created',(key,json.dumps(payload),time.time()))
            DB.execute('DELETE FROM private_answers_v2 WHERE key IN (SELECT key FROM private_answers_v2 ORDER BY created DESC LIMIT 1000000000 OFFSET 1000)')
            DB.commit()
        except StorageUnavailable:DB.rollback()
def save_alert(a):
    with LOCK:
        DB.execute('INSERT INTO alerts VALUES (?,?) ON CONFLICT DO NOTHING',(a['id'],json.dumps(a)));DB.commit()
