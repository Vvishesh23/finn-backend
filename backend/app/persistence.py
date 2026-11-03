"""Explicit SQLite/local or PostgreSQL/hosted persistence. Never loads .env files.
Only PostgreSQL startup reads DATABASE_URL. Public metadata never includes it.
All callers serialize access with store.LOCK; budgets also lock in the database.
"""
import os,sqlite3
from urllib.parse import urlsplit,parse_qsl

class StorageUnavailable(Exception):
    def __init__(self):super().__init__('Persistent storage unavailable. Check backend database configuration.')

class SQLiteDB:
    kind='sqlite'
    def __init__(self,path):
        try:self.connection=sqlite3.connect(path,check_same_thread=False,timeout=10)
        except sqlite3.Error:raise StorageUnavailable() from None
    def __getattr__(self,name):return getattr(self.connection,name)
    def begin(self,lock_key=None):self.connection.execute('BEGIN IMMEDIATE')

class Rows:
    def __init__(self,rows):self.rows=rows
    def fetchone(self):return self.rows.pop(0) if self.rows else None
    def fetchall(self):rows=self.rows;self.rows=[];return rows
    def __iter__(self):return iter(self.rows)

class PostgresDB:
    kind='postgres'
    def __init__(self,dsn,*,local_test=False,connector=None):
        # Never interpolate an exception/URL into logs or client errors.
        try:
            url=urlsplit(dsn)
            if url.scheme not in ('postgres','postgresql') or not url.hostname or not url.path.strip('/'):
                raise ValueError()
            self._local_test=local_test and url.hostname in ('127.0.0.1','localhost') and url.path.startswith('/finn_test_')
            if local_test and not self._local_test:raise ValueError()
            if not self._local_test and (not url.username or not url.password):raise ValueError()
            if url.fragment or any(k not in {'sslmode','channel_binding','connect_timeout'} for k,v in parse_qsl(url.query)):
                raise ValueError()
        except Exception:raise StorageUnavailable() from None
        self._dsn=dsn;self._connection=None;self._in_transaction=False;self._connector=connector

    def _connect(self):
        if self._connection is None or self._connection.closed:
            try:
                import psycopg,certifi
                if any(name in os.environ for name in ('PGSERVICE','PGSERVICEFILE','PGSYSCONFDIR','PGPASSFILE','PGSSLCERT','PGSSLKEY','PGSSLROOTCERT','PGHOSTADDR')):
                    raise ValueError('Implicit libpq configuration is not permitted')
                connect=self._connector or psycopg.connect
                # Ignore ambient PG* variables: URI must define host/user/db itself;
                # no password files/services, client certificates or local key files.
                self._connection=connect(self._dsn,autocommit=True,connect_timeout=10,
                    sslmode='disable' if self._local_test else 'verify-full',
                    sslrootcert=certifi.where(),sslcert='',sslkey='',passfile='/dev/null',
                    options='-c statement_timeout=10000 -c lock_timeout=5000 -c idle_in_transaction_session_timeout=15000',
                    prepare_threshold=None)
            except Exception:
                self._connection=None;raise StorageUnavailable() from None
        return self._connection

    def _drop(self):
        if self._connection is not None:
            try:self._connection.close()
            except Exception:pass
        self._connection=None;self._in_transaction=False

    def execute(self,sql,parameters=()):
        try:
            with self._connect().cursor() as cursor:
                # Only static application SQL reaches this adapter. Values stay bound.
                cursor.execute(sql.replace('?','%s'),parameters or None)
                return Rows(cursor.fetchall() if cursor.description else [])
        except Exception:
            # No automatic write/transaction replay after uncertain commit outcomes.
            self._drop();raise StorageUnavailable() from None

    def executemany(self,sql,parameters):
        try:
            with self._connect().cursor() as cursor:cursor.executemany(sql.replace('?','%s'),parameters)
        except Exception:self._drop();raise StorageUnavailable() from None

    def begin(self,lock_key=None):
        self.execute('BEGIN');self._in_transaction=True
        if lock_key is not None:self.execute('SELECT pg_advisory_xact_lock(?)',(lock_key,))

    def commit(self):
        try:self._connect().commit();self._in_transaction=False
        except Exception:self._drop();raise StorageUnavailable() from None

    def rollback(self):
        # After a dropped connection the server rolls back; never reconnect just to roll back.
        if self._connection is not None:
            try:self._connection.rollback()
            except Exception:self._drop()
        self._in_transaction=False

    def close(self):self._drop()

def open_database(default_path):
    kind=os.environ.get('FINN_STORAGE_BACKEND','sqlite')
    if kind=='sqlite':return SQLiteDB(os.environ.get('FINN_DB',str(default_path)))
    if kind!='postgres':raise StorageUnavailable()
    # Runtime secret boundary: called only after explicit PostgreSQL selection.
    dsn=os.environ.get('DATABASE_URL','')
    return PostgresDB(dsn,local_test=os.environ.get('FINN_ISOLATED_POSTGRES_TESTS')=='true')
