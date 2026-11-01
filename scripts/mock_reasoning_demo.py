"""Run only through run_isolated_tests.py --demo; never uses real credentials."""
import os,json,sys,socket
from pathlib import Path
if os.environ.get('FINN_ISOLATED_TESTS')!='true':raise RuntimeError('Use isolated runner')
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
os.environ['AI_ENABLED']='true';os.environ['REASONING_PROVIDER']='mock'
def deny(*args,**kwargs):raise AssertionError('Network forbidden in mock demonstration')
socket.socket.connect=deny;socket.create_connection=deny
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app import reasoning
cases=[('HINDUNILVR','Explain FY25 consolidated revenue caveats'),('WIPRO','FY25 revenue and profit'),('HINDUNILVR','FY25 consolidated PAT margin'),('INFY','Did management deliver on FY25 guidance?'),('ZENSARTECH','Explain FY25 risks')]
results=[]
with TestClient(app,base_url='https://testserver') as client:
    for symbol,question in cases:
        response=client.post('/api/research/query',json={'symbol':symbol,'question':question})
        results.append({'symbol':symbol,'question':question,'httpStatus':response.status_code,'result':response.json()})
    cached=client.post('/api/research/query',json={'symbol':cases[0][0],'question':cases[0][1]}).json()
    assert cached['cacheHit'] and cached['modelCalls']==0
    assert client.get('/api/coverage').json()['factCount']==71
    assert client.get('/api/coverage').json()['financialIssuerCount']==11
print(json.dumps({'mode':'MOCK_ONLY_NO_REAL_CREDENTIAL_OR_NETWORK','results':results,'repeatCacheHit':cached['cacheHit'],'usage':reasoning.usage()},indent=2))
