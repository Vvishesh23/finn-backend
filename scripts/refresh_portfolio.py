"""Bounded public snapshot acquisition. No bypasses, private sessions or full PDFs.
One sequential request per provider per selected ticker; append new observations and
filing IDs, report conflicting same-ID corrections for review instead of overwriting.
"""
import argparse,datetime,json,ssl,sys,time,urllib.request,urllib.parse,hashlib,os,tempfile
from pathlib import Path
from zoneinfo import ZoneInfo
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.app.models import DailyBar,RawFiling
ROOT=Path(__file__).resolve().parents[1]

def request_json(url):
    context=ssl.create_default_context(cafile='/etc/ssl/cert.pem' if Path('/etc/ssl/cert.pem').exists() else None)
    req=urllib.request.Request(url,headers={'User-Agent':'FINN-public-research-prototype/0.2'})
    with urllib.request.urlopen(req,context=context,timeout=15) as response:
        if response.headers.get_content_type()!='application/json':raise ValueError('Not JSON')
        raw=response.read(12000001)
        if len(raw)>12000000:raise ValueError('Response too large')
    return json.loads(raw)

def normalize_prices(symbol,payload,ingested_at,today):
    result=payload['chart']['result'][0]
    if result['meta']['symbol']!=symbol+'.NS':raise ValueError('Provider symbol mismatch')
    q=result['indicators']['quote'][0];rows=[]
    for i,ts in enumerate(result['timestamp']):
        day=datetime.datetime.fromtimestamp(ts,ZoneInfo('Asia/Kolkata')).date().isoformat()
        if day>=today:continue
        if any(q[k][i] is None for k in ('open','high','low','close','volume')):continue
        row=dict(symbol=symbol,date=day,open=q['open'][i],high=q['high'][i],low=q['low'][i],close=q['close'][i],volume=q['volume'][i],basis='raw',provider='Yahoo Finance',currency='INR',source_url='https://finance.yahoo.com/quote/'+symbol+'.NS/history/',ingested_at=ingested_at,finalized=True)
        DailyBar.model_validate(row);rows.append(row)
    return rows

def normalize_filings(symbol,payload,ingested_at,limit=25):
    if not isinstance(payload,list):raise ValueError('Expected announcement list')
    rows=[]
    for f in payload[:limit]:
        if f.get('symbol')!=symbol:continue
        url=f.get('attchmntFile','');u=urllib.parse.urlsplit(url)
        if u.scheme!='https' or not u.hostname or u.username or u.password:continue
        published=datetime.datetime.strptime(f.get('exchdisstime') or f['an_dt'],'%d-%b-%Y %H:%M:%S').replace(tzinfo=ZoneInfo('Asia/Kolkata')).astimezone(datetime.timezone.utc).isoformat()
        row=dict(id=str(f['seq_id']),symbol=symbol,subject=f.get('attchmntText') or f['desc'],raw_category=f['desc'],url=url,source_published_at=published,ingested_at=ingested_at,source_exchange='NSE',source_timezone='Asia/Kolkata',record_date=None,payment_date=None,event_effective_at=None,revised_at=None)
        RawFiling.model_validate(row);rows.append(row)
    return rows

def append_rows(old,new,kind):
    key=(lambda r:(r['symbol'],r['date'],r['provider'],r['basis'])) if kind=='bars' else (lambda r:r['id'])
    indexed={key(r):r for r in old};conflicts=[]
    for row in new:
        identity=key(row)
        if identity in indexed:
            fields=('close','volume','open','high','low') if kind=='bars' else ('symbol','url','subject','source_published_at')
            if any(indexed[identity].get(f)!=row.get(f) for f in fields):conflicts.append(str(identity))
        else:indexed[identity]=row
    return list(indexed.values()),conflicts

def atomic_json(path,value):
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.'+path.stem)
    with os.fdopen(fd,'w') as f:json.dump(value,f,indent=2)
    os.replace(tmp,path)

def main():
    p=argparse.ArgumentParser();p.add_argument('--symbol',action='append');p.add_argument('--report',required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
    companies=json.loads((ROOT/'demo/companies.json').read_text());symbols=a.symbol or [c['symbol'] for c in companies]
    if len(symbols)>20 or any(not __import__('re').fullmatch(r'[A-Z0-9][A-Z0-9&-]{0,19}',s) for s in symbols):p.error('At most 20 valid ticker symbols')
    now=datetime.datetime.now(datetime.timezone.utc).isoformat();today=datetime.datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat()
    acquired={'bars':[],'filings':[]};log=[]
    for symbol in symbols:
        for kind,url in [('bars','https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(symbol)+'.NS?range=3mo&interval=1d'),('filings','https://www.nseindia.com/api/corporate-announcements?index=equities&symbol='+urllib.parse.quote(symbol))]:
            row={'symbol':symbol,'kind':kind,'url':url,'attempted_at':now}
            try:
                raw=request_json(url)
                data=normalize_prices(symbol,raw,now,today) if kind=='bars' else normalize_filings(symbol,raw,now)
                acquired[kind].extend(data);row.update(status='ACQUIRED' if data else 'EMPTY',rows=len(data),latest=max((r.get('date') or r['source_published_at'] for r in data),default=None))
            except Exception as exc:row.update(status='SOURCE_UNAVAILABLE',reason=type(exc).__name__)
            log.append(row);print(json.dumps(row),flush=True);time.sleep(.25)
    result={'acquired_at':now,'mode':'PUBLIC_SNAPSHOT_NOT_LIVE','attempts':log,'applied':a.apply,'conflicts':{}}
    for kind,new in acquired.items():
        path=ROOT/'demo'/(kind+'.json');old=json.loads(path.read_text());merged,conflicts=append_rows(old,new,kind);result['conflicts'][kind]=conflicts
        result[kind]={'before':len(old),'acquired':len(new),'after':len(merged)}
        if a.apply:atomic_json(path,merged)
    report=Path(a.report)
    with report.open('x') as f:json.dump(result,f,indent=2)
    print('Report',report)
if __name__=='__main__':main()
