"""Public HTTPS smoke checks. Only deterministic research; never requests inference."""
import argparse,json
from urllib.parse import urlsplit
import httpx

def verify(client,url):
    checks=[]
    def get(path,**kwargs):
        r=client.get(url+path,**kwargs);r.raise_for_status();checks.append({'path':path,'httpStatus':r.status_code});return r.json()
    health=get('/health');watch=get('/api/watchlist');get('/api/categories');coverage=get('/api/coverage')
    assert len(watch['companies'])==18
    assert coverage['financialIssuerCount']==11 and coverage['factCount']==71
    digest=get('/api/brief',params={'end':health['latestFilingAt']})
    assert digest['count']>0
    filtered=get('/api/brief',params={'end':health['latestFilingAt'],'symbol':'LT'})
    assert filtered['events'] and all(e['symbol']=='LT' for e in filtered['events'])
    replay=get('/api/brief',params={'start':'2025-04-17T00:00:00+05:30','end':'2025-04-23T23:59:59+05:30'})
    assert replay['events'] and all(e['source_published_at'].startswith('2025-04') for e in replay['events'])
    alerts=get('/api/alerts',params={'price_pct':.1,'volume_multiple':.1,'filing_end':health['latestFilingAt']})
    assert alerts['alerts'] and alerts['filingAlerts']
    for symbol,question,expected in [('WIPRO','FY25 revenue','89,088.40'),('HINDUNILVR','FY25 consolidated revenue','63,121'),('UNINDEXED','FY25 revenue','source unavailable')]:
        r=client.post(url+'/api/research/query',json={'symbol':symbol,'question':question});r.raise_for_status();body=r.json()
        assert expected in body['answer'] and body['modelCalls']==0
        checks.append({'symbol':symbol,'httpStatus':r.status_code,'status':body['status'],'modelCalls':body['modelCalls']})
    return {'url':url,'checks':checks,'result':'HTTP_SMOKE_PASS','publicBrowserQA':'STILL_REQUIRED','liveGemini':'NOT_TESTED_BY_THIS_SCRIPT','originalPublisherAccess':'BROWSER_CHECK_REQUIRED'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--url',required=True);a=p.parse_args();url=a.url.rstrip('/');u=urlsplit(url)
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.query or u.fragment or u.path or u.hostname.endswith('.invalid'):
        p.error('Provide the actual HTTPS origin without credentials/path/query, not a placeholder')
    with httpx.Client(timeout=60,follow_redirects=False,trust_env=False) as client:report=verify(client,url)
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
