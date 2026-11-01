"""Bounded public acquisition CLI; extracted documents require human verification."""
import argparse,json,urllib.request,ssl,datetime,pathlib,hashlib,re
from urllib.parse import quote,urlsplit
p=argparse.ArgumentParser();p.add_argument('kind',choices=['prices','nse','document']);p.add_argument('--symbol',default='INFY');p.add_argument('--file');p.add_argument('--url');p.add_argument('--title');p.add_argument('--published');a=p.parse_args()
symbol=a.symbol.upper().removesuffix('.NS')
if not re.fullmatch(r'[A-Z0-9][A-Z0-9&-]{0,19}',symbol):p.error('Invalid ticker')
root=pathlib.Path(__file__).resolve().parents[1];out=root/'demo'/'imports';out.mkdir(exist_ok=True);now=datetime.datetime.now(datetime.timezone.utc).isoformat()
if a.kind=='document':
    if not a.file or not a.url or not a.title:p.error('Requires --file --url --title')
    u=urlsplit(a.url)
    if u.scheme!='https' or not u.hostname or u.username or u.password:p.error('HTTPS citation required')
    path=pathlib.Path(a.file)
    if path.stat().st_size>15000000:p.error('Maximum 15 MB')
    import pymupdf
    doc=pymupdf.open(path);pages=[{'page':i+1,'text':page.get_text()} for i,page in enumerate(doc)]
    h=hashlib.sha256(path.read_bytes()).hexdigest();dest=out/(symbol+'-'+h[:12]+'.json')
    data={'symbol':symbol,'title':a.title,'url':a.url,'published':a.published,'ingested_at':now,'file_hash':h,'pages':pages,'status':'EXTRACTED_UNVERIFIED'}
else:
    url=('https://query1.finance.yahoo.com/v8/finance/chart/'+quote(symbol)+'.NS?range=3mo&interval=1d') if a.kind=='prices' else ('https://www.nseindia.com/api/corporate-announcements?index=equities&symbol='+quote(symbol))
    try:
        ca='/etc/ssl/cert.pem' if pathlib.Path('/etc/ssl/cert.pem').exists() else None
        with urllib.request.urlopen(url,timeout=20,context=ssl.create_default_context(cafile=ca)) as r:raw=r.read(12000001)
        if len(raw)>12000000:raise ValueError('Source exceeds size limit')
        data={'url':url,'ingested_at':now,'data':json.loads(raw)};dest=out/(symbol+'-'+a.kind+'.json')
    except Exception as e:raise SystemExit(f'SOURCE_UNAVAILABLE: {type(e).__name__}. Snapshot unchanged.')
dest.write_text(json.dumps(data,indent=2));print(dest);print('Raw import only: review provenance, rights, financial values and normalization before promoting to verified replay. Not automatically indexed.')
