"""Atomic budgets/leases: shared SQLite file, or shared PostgreSQL transactions.
PostgreSQL budget reservations share a transaction-scoped advisory lock.
"""
import time,secrets
from datetime import datetime,timezone
from . import store

class Denied(Exception):
    def __init__(self,reason,status=429):self.reason=reason;self.status=status;super().__init__(reason)

with store.LOCK:
    store.DB.execute('CREATE TABLE IF NOT EXISTS ai_clients(day TEXT,client TEXT,calls INTEGER,PRIMARY KEY(day,client))')
    store.DB.execute('CREATE TABLE IF NOT EXISTS ai_minutes(bucket INTEGER,client TEXT,calls INTEGER,PRIMARY KEY(bucket,client))')
    store.DB.execute('CREATE TABLE IF NOT EXISTS ai_leases(id TEXT PRIMARY KEY,expires DOUBLE PRECISION)')
    store.DB.commit()

def acquire(cfg,amount,client):
    lease=secrets.token_hex(16)
    with store.LOCK:
        try:
            store.DB.begin(2026110103)
            now=time.time();day=datetime.now(timezone.utc).date().isoformat();bucket=int(now//60)
            store.DB.execute('DELETE FROM ai_leases WHERE expires<=?',(now,))
            store.DB.execute('DELETE FROM ai_minutes WHERE bucket<?',(bucket-2,))
            store.DB.execute('DELETE FROM ai_clients WHERE day<?',(day,))
            active=store.DB.execute('SELECT count(*) FROM ai_leases').fetchone()[0]
            if active>=cfg['concurrent']:raise Denied('concurrency_limit',503)
            store.DB.execute('INSERT INTO ai_usage VALUES (?,0,0,0,0) ON CONFLICT DO NOTHING',(day,))
            calls,reserved=store.DB.execute('SELECT calls,reserved FROM ai_usage WHERE day=?',(day,)).fetchone()
            if calls>=cfg['max_calls'] or reserved+amount>cfg['max_tokens']:raise Denied('daily_budget_exhausted')
            daily=store.DB.execute('SELECT calls FROM ai_clients WHERE day=? AND client=?',(day,client)).fetchone()
            minute=store.DB.execute('SELECT calls FROM ai_minutes WHERE bucket=? AND client=?',(bucket,client)).fetchone()
            global_minute=store.DB.execute('SELECT calls FROM ai_minutes WHERE bucket=? AND client=?',(bucket,'_global')).fetchone()
            if global_minute and global_minute[0]>=cfg['global_minute']:raise Denied('global_rate_limit')
            if daily and daily[0]>=cfg['client_daily']:raise Denied('client_daily_limit')
            if minute and minute[0]>=cfg['client_minute']:raise Denied('client_rate_limit')
            store.DB.execute('INSERT INTO ai_clients VALUES (?,?,1) ON CONFLICT(day,client) DO UPDATE SET calls=ai_clients.calls+1',(day,client))
            store.DB.execute('INSERT INTO ai_minutes VALUES (?,?,1) ON CONFLICT(bucket,client) DO UPDATE SET calls=ai_minutes.calls+1',(bucket,client))
            store.DB.execute('INSERT INTO ai_minutes VALUES (?,?,1) ON CONFLICT(bucket,client) DO UPDATE SET calls=ai_minutes.calls+1',(bucket,'_global'))
            store.DB.execute('UPDATE ai_usage SET calls=calls+1,reserved=reserved+? WHERE day=?',(amount,day))
            # Lease outlives the bounded total SDK timeout and configured backoff window.
            store.DB.execute('INSERT INTO ai_leases VALUES (?,?)',(lease,time.time()+cfg['timeout']+30))
            store.DB.commit();return day,lease
        except Exception:store.DB.rollback();raise

def release(lease):
    with store.LOCK:store.DB.execute('DELETE FROM ai_leases WHERE id=?',(lease,));store.DB.commit()
