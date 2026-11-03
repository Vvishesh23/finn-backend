"""Bounded public-source acquisition. No cookies, authentication or bypasses."""
import datetime,json,ssl,urllib.request,urllib.parse,math
from pathlib import Path
from zoneinfo import ZoneInfo
from .models import DailyBar,RawFiling
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
    if result['meta'].get('currency')!='INR':raise ValueError('Provider currency mismatch')
    q=result['indicators']['quote'][0];rows=[]
    action_days={datetime.datetime.fromtimestamp(e['date'],ZoneInfo('Asia/Kolkata')).date().isoformat()
        for events in result.get('events',{}).values() for e in events.values()}
    for i,ts in enumerate(result['timestamp']):
        day=datetime.datetime.fromtimestamp(ts,ZoneInfo('Asia/Kolkata')).date().isoformat()
        if day>=today:continue
        if any(q[k][i] is None for k in ('open','high','low','close','volume')):continue
        if any(not math.isfinite(q[k][i]) for k in ('open','high','low','close','volume')):raise ValueError('Nonfinite quote')
        if not 0<q['low'][i]<=min(q['open'][i],q['close'][i])<=max(q['open'][i],q['close'][i])<=q['high'][i]:raise ValueError('Invalid OHLC')
        row=dict(symbol=symbol,date=day,open=q['open'][i],high=q['high'][i],low=q['low'][i],close=q['close'][i],volume=q['volume'][i],basis='raw',provider='Yahoo Finance',currency='INR',source_url='https://finance.yahoo.com/quote/'+symbol+'.NS/history/',ingested_at=ingested_at,finalized=True)
        if day in action_days:row['corporate_action']=True
        DailyBar.model_validate(row);rows.append(row)
    return rows

def normalize_filings(symbol,payload,ingested_at,limit=25):
    if not isinstance(payload,list):raise ValueError('Expected announcement list')
    if any(f.get('symbol')!=symbol for f in payload):raise ValueError('Announcement issuer mismatch')
    def publication(f):
        field='exchdisstime' if f.get('exchdisstime') not in (None,'','-') else 'an_dt'
        return datetime.datetime.strptime(f[field],'%d-%b-%Y %H:%M:%S'),field
    payload=sorted(payload,key=lambda f:publication(f)[0],reverse=True)
    rows=[]
    for f in payload[:limit]:
        if f.get('symbol')!=symbol:raise ValueError('Announcement issuer mismatch')
        url=f.get('attchmntFile','');u=urllib.parse.urlsplit(url)
        if u.scheme!='https' or u.hostname not in ('nsearchives.nseindia.com','archives.nseindia.com','www.nseindia.com') or u.username or u.password:continue
        moment,field=publication(f)
        published=moment.replace(tzinfo=ZoneInfo('Asia/Kolkata')).astimezone(datetime.timezone.utc).isoformat()
        if published>ingested_at:raise ValueError('Future publication timestamp')
        row=dict(id=str(f['seq_id']),symbol=symbol,subject=f.get('attchmntText') or f['desc'],raw_category=f['desc'],url=url,source_published_at=published,ingested_at=ingested_at,source_exchange='NSE',source_timezone='Asia/Kolkata',record_date=None,payment_date=None,event_effective_at=None,revised_at=None)
        row['source_timestamp_field']=field
        RawFiling.model_validate(row);rows.append(row)
    return rows
