import sqlite3,os,json,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
LOCK=threading.RLock()
DB=sqlite3.connect(os.getenv('FINN_DB',str(ROOT/'finn.sqlite3')),check_same_thread=False)
DB.execute('CREATE TABLE IF NOT EXISTS answers (key TEXT PRIMARY KEY, payload TEXT NOT NULL)')
DB.execute('CREATE TABLE IF NOT EXISTS alerts (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
DB.execute('CREATE TABLE IF NOT EXISTS raw_filings (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
DB.execute('CREATE TABLE IF NOT EXISTS private_answers_v2 (key TEXT PRIMARY KEY,payload TEXT NOT NULL,created REAL NOT NULL)')
def load(name):return json.loads((ROOT/'demo'/f'{name}.json').read_text())
COMPANIES=load('companies');BARS=load('bars');DOCS=load('documents')
with LOCK:
    for f in load('filings'):DB.execute('INSERT OR IGNORE INTO raw_filings VALUES (?,?)',(f['id'],json.dumps(f)))
    DB.commit()
def filings():
    with LOCK:return [json.loads(r[0]) for r in DB.execute('SELECT payload FROM raw_filings')]
def cache_get(key):
    with LOCK:
        row=DB.execute('SELECT payload FROM private_answers_v2 WHERE key=? AND created>?',(key,time.time()-86400)).fetchone()
        return json.loads(row[0]) if row else None
def cache_put(key,payload):
    with LOCK:
        DB.execute('DELETE FROM private_answers_v2 WHERE created<?',(time.time()-86400,))
        DB.execute('INSERT OR REPLACE INTO private_answers_v2 VALUES (?,?,?)',(key,json.dumps(payload),time.time()))
        DB.execute('DELETE FROM private_answers_v2 WHERE key IN (SELECT key FROM private_answers_v2 ORDER BY created DESC LIMIT -1 OFFSET 1000)')
        DB.commit()
def save_alert(a):
    with LOCK:
        DB.execute('INSERT OR IGNORE INTO alerts VALUES (?,?)',(a['id'],json.dumps(a)));DB.commit()
