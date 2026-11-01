from datetime import datetime,timedelta,timezone
from pathlib import Path
from collections import defaultdict,deque
import time,threading
from fastapi import FastAPI,HTTPException,Request,Query as Param
from fastapi.responses import JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from . import store,research,evidence,reasoning,client_privacy
from .models import Query,Company,DailyBar,SourceDocument,RawFiling
from .analytics import anomalies,digest,group_filings,CATEGORIES
app=FastAPI(title='FINN',version='0.1.0')
for c in store.COMPANIES:Company.model_validate(c)
for b in store.BARS:DailyBar.model_validate(b)
for d in store.DOCS:SourceDocument.model_validate(d)
for f in store.filings():RawFiling.model_validate(f)
requests=defaultdict(deque);rate_lock=threading.Lock()
@app.middleware('http')
async def guard(request:Request,call_next):
    if request.method=='POST':
        try:size=int(request.headers.get('content-length','0'))
        except ValueError:return JSONResponse({'error':'INVALID_LENGTH'},400)
        if size>reasoning.integer('MAX_REQUEST_BODY_BYTES',8192,1024,16384):return JSONResponse({'error':'BODY_TOO_LARGE'},413)
        # Bound actual body too, including chunked requests.
        chunks=[];total=0
        async for chunk in request.stream():
            total+=len(chunk)
            if total>reasoning.integer('MAX_REQUEST_BODY_BYTES',8192,1024,16384):return JSONResponse({'error':'BODY_TOO_LARGE'},413)
            chunks.append(chunk)
        request._body=b''.join(chunks)
        now=time.monotonic();client=client_privacy.digest('request:'+client_privacy.peer_address(request))
        with rate_lock:
            for key,limit in [(client,reasoning.integer('MAX_REQUESTS_PER_CLIENT_MINUTE',30,1,120)),('_global',300)]:
                queue=requests[key]
                while queue and queue[0]<now-60:queue.popleft()
                if len(queue)>=limit:return JSONResponse({'error':'RATE_LIMIT','message':'Please retry in a minute.'},429,headers={'Retry-After':'60'})
            requests[client].append(now);requests['_global'].append(now)
    response=await call_next(request)
    if 'Cache-Control' not in response.headers:response.headers['Cache-Control']='no-cache'
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'"
    return response
@app.exception_handler(HTTPException)
async def errors(request,exc):return JSONResponse({'error':'REQUEST_ERROR','message':exc.detail},status_code=exc.status_code)
@app.get('/health')
def health():return {'status':'ok','mode':'AUTHENTIC_HISTORICAL_REPLAY','modelEnabled':reasoning.configuration()['enabled'],'reasoningProvider':reasoning.configuration()['provider'],'latestFilingAt':max(f['source_published_at'] for f in store.filings()),'asOf':max(b['date'] for b in store.BARS),'refresh':'On-demand imported snapshot; no background polling'}
def symbol_ok(s):
    try:return Query(symbol=s,question='overview').symbol
    except Exception:raise HTTPException(422,'Invalid ticker')
def company_data(c):
    bars=[b for b in store.BARS if b['symbol']==c['symbol']]
    a=anomalies(bars,3,2)
    return {**c,'bar':bars[-1] if bars else None,'observation':a,'sourceStatus':'HISTORICAL_SNAPSHOT' if bars else 'MISSING','replayMode':True}
@app.get('/api/watchlist')
def watchlist():return {'companies':[company_data(c) for c in store.COMPANIES],'mock':True,'listingStatus':'Example labels; not a certified current listings master'}
@app.get('/api/brief')
def brief(start:datetime|None=None,end:datetime|None=None,hours:int=Param(default=24,ge=1,le=87600),category:str|None=None,symbol:str|None=None):
    end=end or datetime.now(timezone.utc);start=start or end-timedelta(hours=hours)
    if start.tzinfo is None or end.tzinfo is None:raise HTTPException(422,'Use timestamps with timezone')
    if start>end:raise HTTPException(422,'Start must be before end')
    items=digest(store.filings(),start,end,category,symbol_ok(symbol) if symbol else None)
    return {'events':items,'asOf':end.isoformat(),'from':start.isoformat(),'replayMode':True,'sourceStatus':'IMPORTED_SNAPSHOT','count':len(items)}
@app.get('/api/company/{symbol}')
def company(symbol:str):
    s=symbol_ok(symbol);c=next((c for c in store.COMPANIES if c['symbol']==s),None)
    return {**(company_data(c) if c else {'symbol':s,'sourceStatus':'PRIMARY_DOCUMENTS_ONLY' if evidence.REPOSITORY.sources(s) else 'MISSING','reason':'Primary documents indexed; not a watchlist price series.' if evidence.REPOSITORY.sources(s) else 'Ticker syntax accepted; listing status and sources not verified.'}),'documents':evidence.REPOSITORY.citations(e.id for e in evidence.REPOSITORY.sources(s)),'filings':group_filings([f for f in store.filings() if f['symbol']==s]),'financials':research.company_financials(s),'guidance':research.guidance(s)}
@app.get('/api/company/{symbol}/financials')
def financials(symbol:str):return research.company_financials(symbol_ok(symbol))
@app.get('/api/company/{symbol}/guidance')
def guidance(symbol:str):return research.guidance(symbol_ok(symbol))
@app.get('/api/company/{symbol}/filings')
def filings(symbol:str):return {'events':group_filings([f for f in store.filings() if f['symbol']==symbol_ok(symbol)])}
@app.get('/api/coverage')
def coverage():return evidence.REPOSITORY.coverage()
@app.get('/api/categories')
def categories():return {'categories':CATEGORIES}

@app.get('/api/alerts')
def alerts(price_pct:float=Param(default=3,ge=.1,le=50),volume_multiple:float=Param(default=2,ge=.1,le=20),categories:str='results,M&A,management_change',filing_end:datetime|None=None):
    selected=[c for c in categories.split(',') if c]
    if len(selected)>len(CATEGORIES) or any(c not in CATEGORIES for c in selected):raise HTTPException(422,'Unknown filing alert category')
    now=filing_end or datetime.now(timezone.utc)
    if now.tzinfo is None or now>datetime.now(timezone.utc):raise HTTPException(422,'Use a non-future filing cutoff with timezone')
    events=digest(store.filings(),now-timedelta(hours=24),now)
    watched={c['symbol'] for c in store.COMPANIES}
    filing_alerts=[{'id':'filing-'+e['id'],'event':e,'kind':'filing','symbol':e['symbol']} for e in events if e['category'] in selected and e['symbol'] in watched]
    for alert in filing_alerts:store.save_alert(alert)
    observations={c['symbol']:anomalies([b for b in store.BARS if b['symbol']==c['symbol']],price_pct,volume_multiple) for c in store.COMPANIES}
    active=[a for o in observations.values() for a in o['alerts']]
    for a in active:store.save_alert(a)
    return {'alerts':active,'filingAlerts':filing_alerts,'observations':observations,'replayMode':True,'rule':{'price_pct':price_pct,'volume_multiple':volume_multiple,'categories':selected},'filingWindowEnd':now.isoformat(),'priceAsOf':max(b['date'] for b in store.BARS),'cadence':'Imported EOD snapshot; manual checks only'}
@app.post('/api/research/query')
def query(q:Query,request:Request):
    if len(q.question)>reasoning.integer('MAX_QUERY_CHARS',2000,100,2000):
        return JSONResponse({'error':'QUERY_TOO_LONG'},status_code=422)
    client,scope,cookie=client_privacy.context(request)
    result=research.answer(q,client_id=client,cache_scope=scope)
    response=JSONResponse(result,status_code=result.get('httpStatus',200))
    response.set_cookie('finn_session',cookie,httponly=True,secure=True,samesite='strict',max_age=86400)
    response.headers['Cache-Control']='private, no-store'
    if response.status_code==429:response.headers['Retry-After']='60'
    return response
@app.get('/api/source/{id}')
def source(id:str):
    found=next(iter(evidence.REPOSITORY.citations([id])),None) or next((f for f in store.filings() if f['id']==id),None)
    if not found:raise HTTPException(404,'Evidence not found')
    return found
@app.get('/api/usage')
def usage():return {**research.STATS,'modelEnabled':reasoning.configuration()['enabled'],'scope':'Single local process; counters reset on restart','runtimeCost':'Provider account-specific; see aiUsage','aiUsage':reasoning.usage()}
FRONT=store.ROOT/'frontend'
app.mount('/assets',StaticFiles(directory=FRONT),name='assets')
@app.get('/')
def index():return FileResponse(FRONT/'index.html')
