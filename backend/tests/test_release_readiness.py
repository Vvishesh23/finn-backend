"""CP11: restart/lease/cache persistence using fresh processes and no credential."""
import json,subprocess,sys,os,sqlite3
from fastapi.testclient import TestClient
from backend.app.main import app

def worker(path,code):
    # Literal environment only, never inherited real deployment credentials.
    result=subprocess.run([sys.executable,'-c',code],env={'PATH':'/usr/bin:/bin','FINN_DB':str(path),'AI_ENABLED':'false','REASONING_PROVIDER':'disabled','MAX_AI_REQUESTS_PER_DAY':'1'},capture_output=True,text=True,timeout=15)
    assert result.returncode==0,'Isolated restart worker failed'
    return json.loads(result.stdout)

def test_restart_preserves_budget_cache_and_session_identity(tmp_path):
    db=tmp_path/'restart.sqlite3'
    first=worker(db,"""import json
from backend.app import reasoning,store,client_privacy
from backend.app.inference_limits import acquire,release
_,lease=acquire(reasoning.configuration(),100,'client');release(lease)
store.cache_put('session-a',{'answer':'public fixture'})
print(json.dumps({'calls':reasoning.usage()['callsAttempted'],'identity':client_privacy.digest('synthetic-session')}))
""")
    second=worker(db,"""import json
from backend.app import reasoning,store,client_privacy
from backend.app.inference_limits import acquire,Denied
try:acquire(reasoning.configuration(),100,'client');reason='WRONG_ALLOW'
except Denied as e:reason=e.reason
print(json.dumps({'calls':reasoning.usage()['callsAttempted'],'reason':reason,'cache':store.cache_get('session-a'),'otherCache':store.cache_get('session-b'),'identity':client_privacy.digest('synthetic-session')}))
""")
    assert first['calls']==second['calls']==1
    assert first['identity']==second['identity']
    assert second['reason']=='daily_budget_exhausted'
    assert second['cache']=={'answer':'public fixture'} and second['otherCache'] is None

def test_crashed_process_lease_is_not_immediately_forgotten(tmp_path):
    db=tmp_path/'lease.sqlite3'
    worker(db,"""import json
from backend.app import reasoning
from backend.app.inference_limits import acquire
cfg=reasoning.configuration();cfg['concurrent']=1;cfg['max_calls']=3
acquire(cfg,10,'client')
print('{}')
""")
    result=worker(db,"""import json
from backend.app import reasoning
from backend.app.inference_limits import acquire,Denied
cfg=reasoning.configuration();cfg['concurrent']=1;cfg['max_calls']=3
try:acquire(cfg,10,'other');reason='WRONG_ALLOW'
except Denied as e:reason=e.reason
print(json.dumps({'reason':reason}))
""")
    assert result['reason']=='concurrency_limit'
    # Synthetic clock expiry; do not sleep or modify a real deployment database.
    with sqlite3.connect(db) as connection:
        connection.execute('UPDATE ai_leases SET expires=0')
    result=worker(db,"""import json
from backend.app import reasoning
from backend.app.inference_limits import acquire,release
cfg=reasoning.configuration();cfg['max_calls']=3
_,lease=acquire(cfg,10,'other');release(lease)
print(json.dumps({'calls':reasoning.usage()['callsAttempted']}))
""")
    assert result['calls']==2

def test_latest_import_cutoff_is_explicit_and_alerts_match():
    with TestClient(app) as c:
        health=c.get('/health').json();cutoff=health['latestFilingAt']
        brief=c.get('/api/brief',params={'end':cutoff}).json()
        alerts=c.get('/api/alerts',params={'filing_end':cutoff}).json()
        assert brief['count']>0 and alerts['filingAlerts']
        assert alerts['filingWindowEnd']==brief['asOf']
        assert alerts['priceAsOf']==health['asOf']
        assert c.get('/api/alerts',params={'filing_end':'2099-01-01T00:00:00Z'}).status_code==422

def test_release_smoke_checks_against_actual_app_without_network():
    from scripts.smoke_url import verify
    from backend.app.main import requests
    requests.clear()
    with TestClient(app,base_url='https://testserver') as client:
        result=verify(client,'https://testserver')
    assert result['result']=='HTTP_SMOKE_PASS'
    assert result['liveGemini']=='NOT_TESTED_BY_THIS_SCRIPT'
