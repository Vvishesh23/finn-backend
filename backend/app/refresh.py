"""Owner-operated bounded refresh. No public write endpoint and no Gemini access.
Dry run by default; --apply writes only to the explicitly configured store.
"""
import argparse,datetime,hashlib,json,time,uuid,sys
from urllib.parse import quote
from zoneinfo import ZoneInfo
from . import store
from .acquisition import request_json,normalize_prices,normalize_filings

UTC=datetime.timezone.utc
def stamp():return datetime.datetime.now(UTC).isoformat()
def fingerprint(row,kind):
    fields=('symbol','date','provider','basis','open','high','low','close','volume','corporate_action') if kind=='bars' else ('symbol','subject','raw_category','url','source_published_at')
    return hashlib.sha256(json.dumps({k:row.get(k) for k in fields},sort_keys=True).encode()).hexdigest()

def apply_batch(symbol,kind,rows,attempt):
    """Serialize imports; preserve first ingestion time, quarantine corrections.
    Filings corrections get an immutable revision and cannot appear before discovery.
    Price corrections require review, never overwrite a previously validated bar.
    """
    from .models import DailyBar,RawFiling
    watched={c['symbol'] for c in store.COMPANIES}
    if symbol not in watched or kind not in ('bars','filings'):raise ValueError('Outside watchlist')
    for row in rows:
        (DailyBar if kind=='bars' else RawFiling).model_validate(row)
        if row['symbol']!=symbol:raise ValueError('Issuer mismatch')
        for field in ('ingested_at',)+ (('source_published_at',) if kind=='filings' else ()):
            if datetime.datetime.fromisoformat(row[field]).tzinfo is None:raise ValueError('Timezone missing')
    added=duplicates=corrections=0
    with store.LOCK:
        store.DB.begin(2026110301)
        try:
            old=store.bars() if kind=='bars' else store.filings()
            for row in rows:
                if kind=='filings' and any(r['id']==row['id'] and (r['symbol']!=symbol or r['source_exchange']!=row['source_exchange']) for r in old):raise ValueError('Source identity collision')
                digest=fingerprint(row,kind)
                identity=(lambda r:(r['symbol'],r['date'],r['provider'],r['basis'])) if kind=='bars' else (lambda r:r.get('original_id',r['id']))
                same=[r for r in old if identity(r)==identity(row)]
                if any(fingerprint(r,kind)==digest for r in same):duplicates+=1;continue
                value=dict(row)
                if same:
                    corrections+=1
                    revision_id=kind+':'+digest
                    store.DB.execute('INSERT INTO feed_revisions VALUES (?,?) ON CONFLICT DO NOTHING',(revision_id,json.dumps({'kind':kind,'observed_at':attempt['attempted_at'],'candidate':value,'previousFingerprints':[fingerprint(r,kind) for r in same],'status':'REVIEW_REQUIRED' if kind=='bars' else 'SOURCE_REVISION'})))
                    if kind=='bars':continue
                    value.update(original_id=row['id'],id=row['id']+'@'+digest[:16],available_at=attempt['attempted_at'],revised_at=attempt['attempted_at'])
                table='imported_bars' if kind=='bars' else 'raw_filings'
                record_id=digest if kind=='bars' else value['id']
                store.DB.execute('INSERT INTO '+table+' VALUES (?,?) ON CONFLICT DO NOTHING',(record_id,json.dumps(value)))
                old.append(value);added+=1
            result={**attempt,'added':added,'duplicates':duplicates,'corrections':corrections,'rows':len(rows),'latest':max((r.get('date') or r.get('source_published_at') for r in rows),default=None)}
            store.DB.execute('INSERT INTO feed_refreshes VALUES (?,?)',(uuid.uuid4().hex,json.dumps(result)))
            store.DB.commit()
        except Exception:store.DB.rollback();raise
    return result

def record_failure(attempt):
    with store.LOCK:
        store.DB.execute('INSERT INTO feed_refreshes VALUES (?,?)',(uuid.uuid4().hex,json.dumps(attempt)));store.DB.commit()

def freshness(now=None):
    now=now or datetime.datetime.now(UTC)
    with store.LOCK:history=[json.loads(r[0]) for r in store.DB.execute('SELECT payload FROM feed_refreshes')]
    latest={};success={}
    for r in sorted(history,key=lambda r:r['attempted_at']):
        if r['status'] not in ('SUCCESS','FAILED'):continue
        key=(r['symbol'],r['kind']);latest[key]=r
        if r['status']=='SUCCESS':success[key]=r
    failed=[{'symbol':s,'kind':k,'reason':r.get('reason','Source unavailable')} for (s,k),r in latest.items() if r['status']!='SUCCESS']
    expected={(c['symbol'],k) for c in store.COMPANIES for k in ('filings','bars')}
    recent=all(key in success and (now-datetime.datetime.fromisoformat(success[key]['attempted_at'])).total_seconds()<36*3600 for key in expected)
    bars=store.bars();filings=store.filings()
    latest_filing=max((f['source_published_at'] for f in filings),default=None)
    latest_eod=max((b['date'] for b in bars),default=None)
    # This is an age warning, not an exchange trading-calendar certification.
    old_data=not latest_eod or (now.date()-datetime.date.fromisoformat(latest_eod)).days>4
    return {'state':'REFRESH_FAILED' if failed else 'RECENT_CHECK' if recent and not old_data else 'STALE',
        'lastAttemptAt':max((r['attempted_at'] for r in history),default=None),
        'lastSuccessfulRefreshAt':max((r['attempted_at'] for r in success.values()),default=None),
        'successfulSources':len(success),'expectedSources':len(expected),'failures':failed,
        'latestFilingAt':latest_filing,'latestEodDate':latest_eod,
        'method':'Owner CLI / optional external workflow; no Render background scheduler',
        'note':'A successful check is not proof of complete source coverage or a new event. EOD excludes the in-progress IST day. Old research corpus remains separate.'}

def run(symbols,apply=False,fetch=request_json,progress=None):
    today=datetime.datetime.now(ZoneInfo('Asia/Kolkata')).date().isoformat();results=[]
    for symbol in symbols:
        if symbol not in {c['symbol'] for c in store.COMPANIES}:raise ValueError('Outside watchlist')
        for kind,url in [('filings','https://www.nseindia.com/api/corporate-announcements?index=equities&symbol='+quote(symbol)),('bars','https://query1.finance.yahoo.com/v8/finance/chart/'+quote(symbol)+'.NS?range=3mo&interval=1d&events=div%2Csplits')]:
            attempt={'symbol':symbol,'kind':kind,'attempted_at':stamp(),'status':'SUCCESS'}
            if progress:progress({**attempt,'status':'CHECKING'})
            try:
                data=fetch(url)
                rows=normalize_filings(symbol,data,attempt['attempted_at'],limit=250) if kind=='filings' else normalize_prices(symbol,data,attempt['attempted_at'],today)
                if kind=='bars' and not rows:raise ValueError('No completed EOD observations')
                result=apply_batch(symbol,kind,rows,attempt) if apply else {**attempt,'rows':len(rows),'latest':max((r.get('date') or r.get('source_published_at') for r in rows),default=None)}
            except Exception as exc:
                # Exception type only: never URLs, credentials or provider bodies.
                result={**attempt,'status':'FAILED','reason':type(exc).__name__}
                if apply:record_failure(result)
            results.append(result)
            if progress:progress(result)
            time.sleep(.25)
    return {'applied':apply,'attempts':results,'allSucceeded':all(r['status']=='SUCCESS' for r in results)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--symbol',action='append');a=p.parse_args()
    def progress(row):
        print(row['symbol']+' '+row['kind']+': '+row['status']+' (added '+str(row.get('added','—'))+', duplicates '+str(row.get('duplicates','—'))+')',file=sys.stderr,flush=True)
    result=run(a.symbol or [c['symbol'] for c in store.COMPANIES],a.apply,progress=progress)
    print(json.dumps(result,indent=2));return 0 if result['allSucceeded'] else 1
if __name__=='__main__':raise SystemExit(main())
