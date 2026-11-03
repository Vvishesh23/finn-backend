from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import math,hashlib,json

def change(current, prior):
    if prior is None or current is None or Decimal(str(prior)) == 0:return None
    return float(((Decimal(str(current))-Decimal(str(prior)))/abs(Decimal(str(prior)))*100).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))

def compare(a,b):
    for key in ('basis','currency','period_type','metric'):
        if a.get(key)!=b.get(key):return {'status':'NOT_COMPARABLE','reason':f'{key} mismatch'}
    if a.get('scale') not in ('rupee','crore','million') or b.get('scale') not in ('rupee','crore','million'):return {'status':'NOT_COMPARABLE','reason':'unknown scale'}
    scales={'rupee':1,'crore':10000000,'million':1000000}
    if not a.get('value') is None and not b.get('value') is None:
        v=change(Decimal(str(a['value']))*scales[a['scale']],Decimal(str(b['value']))*scales[b['scale']])
        return {'status':'DERIVED' if v is not None else 'MISSING','pct':v}
    return {'status':'MISSING','pct':None}

def anomalies(bars,price_pct,volume_multiple):
    valid=sorted([b for b in bars if b['finalized']],key=lambda b:b['date'])
    if len(valid)<21:return {'status':'INSUFFICIENT_HISTORY','alerts':[]}
    current=valid[-1]; prior=valid[-21:-1]
    if any(b['basis']!=current['basis'] or b['provider']!=current['provider'] for b in prior):return {'status':'NOT_COMPARABLE','alerts':[]}
    if any(not math.isfinite(b['close']) or b['close']<=0 or not math.isfinite(b['volume']) or b['volume']<0 for b in [*prior,current]):return {'status':'BAD_DATA','alerts':[]}
    if any(b.get('price_review_required') for b in [*prior,current]):return {'status':'SOURCE_CORRECTION_REVIEW','alerts':[]}
    if current.get('corporate_action') or any(b.get('corporate_action') for b in prior):return {'status':'CORPORATE_ACTION_REVIEW','alerts':[]}
    pct=change(current['close'],prior[-1]['close']);avg=sum(b['volume'] for b in prior)/20
    ratio=current['volume']/avg if avg else None
    items=[]
    for kind,hit in [('price',abs(pct)>=price_pct),('volume',ratio is not None and ratio>volume_multiple)]:
        if hit:items.append({'id':hashlib.sha256(json.dumps([current,kind],sort_keys=True).encode()).hexdigest()[:20],'symbol':current['symbol'],'kind':kind,'date':current['date'],'price_pct':pct,'volume_multiple':round(ratio,2) if ratio else None,'source_url':current['source_url']})
    return {'status':'DERIVED','alerts':items,'price_pct':pct,'volume_multiple':round(ratio,2) if ratio else None,'baseline_sessions':20,'asOf':current['date']}

CATEGORIES=['results','M&A','fund_raise','management_change','litigation','insider_trading','earnings_call','investor_meetings','credit_rating','dividend','bonus_split','capex','press_release','postal_ballot','agm_egm','pledging','unclassified']
def category(f):
    s=(f['raw_category']+' '+f['subject']).lower()
    rules=[
        (['resignation','appointment of chief','chief financial officer','change in director','change in management'],'management_change',85),
        (['acquisition','merger','demerger','joint venture'],'M&A',85),
        (['financial statement','financial result','auditor report','auditors on financial','outcome of board'],'results',90),
        (['litigation','penalty','fine imposed','regulatory order','insolvency'],'litigation',80),
        (['credit rating','credit-rating'],'credit_rating',65),
        (['pledge','pledging'],'pledging',70),
        (['fund rais','rights issue','qualified institution','buyback','commercial paper'],'fund_raise',75),
        (['bonus','stock split','sub-division'],'bonus_split',65),
        (['capex','capacity expansion','capital expenditure'],'capex',75),
        (['record date','dividend'],'dividend',60),
        (['transcript','earnings call','conference call','audio recording'],'earnings_call',55),
        (['insider trading','disclosure under regulation 7'],'insider_trading',50),
        (['postal ballot'],'postal_ballot',20),
        (['annual general meeting','extraordinary general meeting','agm','egm'],'agm_egm',20),
        (['newspaper','meeting','conference'],'investor_meetings',15),
        (['press release','order win','partnership','launch','collaboration'],'press_release',40),
    ]
    for words,c,score in rules:
        if any(w in s for w in words):return c,score
    return 'unclassified',10

def group_filings(raw):
    revisions={}
    for f in raw:
        key=(f['source_exchange'],f['symbol'],f.get('original_id',f['id']))
        previous=revisions.get(key)
        if previous is None or f.get('available_at',f['source_published_at'])>previous.get('available_at',previous['source_published_at']):revisions[key]=f
    groups={}
    for f in revisions.values():
        key=(f['symbol'],f.get('attachment_hash') or f['url'])
        if key not in groups:
            c,score=category(f)
            groups[key]={'id':f['id'],'symbol':f['symbol'],'headline':f['subject'],'category':c,'raw_category':f['raw_category'],'score':score,'reason_codes':[f'{c}: baseline relevance {score}','Exact attachment grouping; ranking does not predict returns'],'evidenceRefs':[],'sources':[],'source_published_at':f['source_published_at'],'record_date':f.get('record_date'),'payment_date':f.get('payment_date'),'event_effective_at':f.get('event_effective_at'),'revised_at':f.get('revised_at')}
        event=groups[key];event['evidenceRefs'].append(f['id']);event['sources'].append(f)
        event['source_published_at']=min(event['source_published_at'],f['source_published_at'])
    return sorted(groups.values(),key=lambda e:(e['score'],e['source_published_at']),reverse=True)

def digest(raw,start,end,cat=None,symbol=None):
    # Filter before grouping: no future duplicate source can leak into an as-of view.
    known=[f for f in raw if start<=datetime.fromisoformat(f['source_published_at'])<=end and datetime.fromisoformat(f.get('available_at',f['source_published_at']))<=end]
    return [e for e in group_filings(known) if (not cat or e['category']==cat) and (not symbol or e['symbol']==symbol)]

def guidance_outcome(low,high,actual,explicit=True,comparable=True):
    if not explicit:return {'status':'INCONCLUSIVE','reason':'Qualitative aspiration is not numeric guidance'}
    if not comparable:return {'status':'NOT_COMPARABLE'}
    if actual is None:return {'status':'INCONCLUSIVE'}
    a,l,h=map(lambda v:Decimal(str(v)),(actual,low,high))
    return {'status':'EXCEEDED' if a>h else 'MISSED' if a<l else 'MET','gap_pp':float(a-h if a>h else a-l if a<l else Decimal(0))}
