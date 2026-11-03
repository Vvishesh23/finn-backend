"""Generic deterministic facts and bounded source retrieval. No issuer-specific answers."""
import re,hashlib,json
from datetime import datetime
from decimal import Decimal
from .models import QueryPlan
from .analytics import guidance_outcome
from . import store,evidence,reasoning
STATS={'model_calls':0,'tokens':0,'cache_hits':0,'queries':0}
LABELS={'revenue':'Revenue','pbt':'PBT','pat':'PAT (total profit)','ebitda':'EBITDA','free_cash_flow':'Free cash flow','operating_margin':'Operating margin','revenue_growth_cc':'Constant-currency revenue growth'}

def parse_period(question,intent):
    text=question.lower();years=[]
    if re.search(r'\b(latest|today|current|last|next|previous|ytd|ttm|calendar)\b',text):return None,None,'UNSUPPORTED_OR_AMBIGUOUS'
    def fiscal(m):
        start=int(m[1]);start=start+2000 if start<100 else start
        end=int(m[2]) if m[2] else None
        if end is not None and end<100:end=start//100*100+end
        years.append(end if end==start+1 else -1 if end is not None else start)
        return ' '
    remaining=re.sub(r'\bfy\s*(\d{4}|\d{2})(?:\s*[-/–]\s*(\d{4}|\d{2}))?\b',fiscal,text)
    years.extend(int(y) for y in re.findall(r'\b(20\d{2})\b',remaining))
    if len(set(years))>1 or -1 in years:return None,None,'UNSUPPORTED_OR_AMBIGUOUS'
    qs=[int(x) for x in re.findall(r'\bq\s*([1-4])\b',text)]
    for name,number in [('first',1),('second',2),('third',3),('fourth',4)]:
        if re.search(r'\b'+name+r'\s+quarter\b',text):qs.append(number)
    quarterly=bool(qs) or bool(re.search(r'\b(quarter|quarterly)\b',text))
    annual=bool(re.search(r'\b(annual|full[ -]year)\b',text))
    if len(set(qs))>1 or (quarterly and (annual or not qs)) or (quarterly and intent=='guidance_vs_actuals'):
        return None,None,'UNSUPPORTED_OR_AMBIGUOUS'
    # No silent latest period: retain a visible historical default for the existing demo.
    year=years[0] if years else 2025
    q=qs[0] if qs else None if years or annual or intent!='financial_snapshot' else 4
    return year,q,f'Q{q} FY{str(year)[-2:]}' if q else f'FY{str(year)[-2:]} annual'

def resolve_period(question,intent):return parse_period(question,intent)[2]

def plan(q):
    s=q.question.lower()
    if re.search(r'\b(why|explain|interpret|assess|risks|drivers|bull|bear|synthesi[sz]e)\b',s):intent='financial_trajectory'
    elif re.search(r'\b(guidance|promise|deliver|target)\b',s):intent='guidance_vs_actuals'
    elif re.search(r'\b(why|explain|interpret|assess|risks|drivers|bull|bear)\b',s):intent='financial_trajectory'
    elif re.search(r'\b(revenue|pat|pbt|ebitda|profit|financial|ratio|margin)\b',s):intent='financial_snapshot'
    elif re.search(r'\b(cash|conversion)\b',s):intent='cash_conversion'
    elif re.search(r'\b(business|overview|services|company do)\b',s):intent='business_overview'
    else:intent='unknown'
    metrics=[m for m in ('revenue','pat','pbt','ebitda') if re.search(r'\b'+m+r'\b',s)]
    if 'profit' in s and not any(m in metrics for m in ('pat','pbt')):metrics+=['pbt','pat']
    ratio='pat_margin' if re.search(r'\b(?:pat|net profit|profit|net)\s+margin\b',s) else None
    if ratio:metrics=['pat','revenue']
    year,quarter,period=parse_period(s,intent)
    basis='standalone' if 'standalone' in s else 'consolidated' if 'consolidated' in s else None
    return QueryPlan(intent=intent,symbol=q.symbol,ratio=ratio,metric=metrics[0] if len(metrics)==1 else None,metrics=metrics,period=period,fiscal_year=year,quarter=quarter,basis=basis,operations=['retrieve','compare'] if intent in ('financial_snapshot','guidance_vs_actuals') else ['retrieve'])

def period_facts(symbol,year,quarter,basis=None,as_of=None):
    rows=evidence.REPOSITORY.select(symbol,year,quarter,basis,as_of)
    rows=[f for f in rows if f.metric in ('revenue','pbt','pat','ebitda','free_cash_flow')]
    bases={f.basis for f in rows if f.metric in ('revenue','pbt','pat','ebitda')}
    if basis is None and len(bases)>1:return [],'Reporting basis is ambiguous; specify consolidated or standalone.'
    if len({f.metric for f in rows})!=len(rows):return [],'Conflicting verified facts require review.'
    return rows,None

def company_financials(symbol):
    """Use the most recent verified period; prefer a quarter at the same end date.

    Explicit research periods continue to use financials() without fallback.
    """
    repo=evidence.REPOSITORY
    allowed={e.id for e in repo.sources(symbol) if e.evidence_method!='pdf_extracted_unverified'}
    rows=[f for f in repo.facts if f.symbol==symbol and f.evidence_id in allowed
          and f.verification!='unverified' and f.metric in ('revenue','pbt','pat','ebitda')]
    if not rows:
        return {'status':'MISSING','metrics':[],'reason':'No verified primary financial facts imported for this ticker.'}
    latest=max(rows,key=lambda f:(f.period_end,f.quarter is not None))
    return financials(symbol,latest.fiscal_year,latest.quarter)

def financials(symbol,year=2025,quarter=4,basis=None,as_of=None):
    rows,reason=period_facts(symbol,year,quarter,basis,as_of)
    if not rows:return {'status':'MISSING','metrics':[],'reason':reason or 'No verified primary financial facts imported for this ticker and period.'}
    rows=[f for f in rows if f.metric in ('revenue','pbt','pat','ebitda')]
    if not rows:return {'status':'MISSING','metrics':[],'reason':'No verified income statement metrics for this period.'}
    currencies={f.currency for f in rows}
    standards={f.accounting_standard for f in rows}
    if len(currencies)!=1 or len(standards)!=1:
        return {'status':'MISSING','metrics':[],'reason':'Conflicting currency or accounting standards require review.'}
    currency=rows[0].currency
    scale='crore' if currency=='INR' else 'million'
    def displayed(f):return float(f.value*evidence.SCALES[f.scale]/evidence.SCALES[scale])
    metrics=[]
    for key in ('revenue','pbt','pat','ebitda'):
        f=next((r for r in rows if r.metric==key),None)
        row={'metric':LABELS[key],'key':key,'current':displayed(f) if f else None,'previous':None,'year_ago':None,'qoq':None,'yoy':None,'status':'VERIFIED_DERIVED' if f else 'MISSING','reason':None if f else 'Not verified in this source; not substituted with another metric.','evidenceRefs':[f.evidence_id] if f else []}
        if f:
            previous_year,previous_q=(year-1,4) if quarter==1 else (year,quarter-1) if quarter else (None,None)
            for kind,y,q,col in [('qoq',previous_year,previous_q,'previous'),('yoy',year-1,quarter,'year_ago')]:
                if y is None:continue
                candidates=evidence.REPOSITORY.select(symbol,y,q,f.basis,as_of)
                candidates=[r for r in candidates if r.metric==key]
                if len(candidates)==1:
                    other=candidates[0];comparison=evidence.compare_facts(f,other,kind)
                    row[kind]=comparison['pct'];row[kind+'Status']=comparison['status']
                    if comparison['status']!='NOT_COMPARABLE':
                        row[col]=displayed(other);row['evidenceRefs'].append(other.evidence_id)
        row['definition']=f.definition if f else None
        metrics.append(row)
    sample=rows[0]
    return {'status':evidence_status(metrics),'basis':f'{sample.basis.title()} {sample.accounting_standard}; {currency} {scale}; '+('discrete quarters' if quarter else 'annual periods'), 'periods':[f'Q{quarter} FY{str(year)[-2:]}' if quarter else f'FY{str(year)[-2:]} annual','Previous quarter' if quarter else 'Not applicable',f'FY{str(year-1)[-2:]}'+(f' Q{quarter}' if quarter else ' annual')], 'currency':currency,'scale':scale,'unit':currency+' '+scale,'metrics':metrics,'evidenceRefs':list(dict.fromkeys(i for m in metrics for i in m['evidenceRefs'])),'asOf':str(sample.period_end),'replayMode':True}

def guidance(symbol,year=2025,as_of=None):
    repo=evidence.REPOSITORY;items=[]
    sources={e.id:e for e in repo.sources(symbol,as_of)}
    for g in repo.guidance:
        if g.symbol!=symbol or g.target_end.year!=year or g.evidence_id not in sources:continue
        actual=next((f for f in repo.facts if f.id==g.actual_fact_id and f.evidence_id in sources and f.verification!='unverified'),None)
        original=sources[g.evidence_id]
        comparable=actual is not None and actual.symbol==g.symbol and actual.metric==g.metric and (g.target_start,g.target_end,g.basis,g.scale,g.definition)==(actual.period_start,actual.period_end,actual.basis,actual.scale,actual.definition)
        known_date=original.report_date
        if not comparable or not known_date or not original.published_at or original.published_at.date()>=actual.period_end or known_date>=actual.period_end:continue
        items.append({'metric':f'FY{str(year)[-2:]} '+LABELS.get(actual.metric,actual.metric),'target':f'{g.low}–{g.high}%','actual':float(actual.value),'unit':'%','statement_date':str(original.report_date),'actual_date':str(sources[actual.evidence_id].report_date),'basis':actual.definition,'evidenceRefs':[g.evidence_id,actual.evidence_id],**guidance_outcome(g.low,g.high,actual.value)})
    return {'status':'VERIFIED_DERIVED' if items else 'INCONCLUSIVE','caveat':'Initial guidance comparison only. Subsequent revisions and a rolling four-quarter promise history are not indexed. Not an assessment of management quality.','reason':None if items else 'No comparable explicit guidance imported.','items':items}

def evidence_status(rows):
    known=sum(r['current'] is not None for r in rows)
    return 'MISSING' if not known else 'VERIFIED_DERIVED' if known==len(rows) else 'PARTIAL'

def answer(q,client_id="internal",cache_scope="internal"):
    p=plan(q);repo=evidence.REPOSITORY;STATS['queries']+=1
    sources=repo.sources(q.symbol,q.as_of)
    # Full evidence/fact/guidance version, including raw revisions, prevents stale fact answers.
    version=[reasoning.configuration(),reasoning.PROMPT_VERSION,repo.version,[(d['id'],d.get('hash')) for d in store.DOCS],store.filings(allow_snapshot_fallback=True)]
    key=hashlib.sha256(json.dumps([cache_scope,q.model_dump(mode='json'),p.model_dump(),version,'private-research-v4'],sort_keys=True).encode()).hexdigest()
    with reasoning.single_flight(key):
        return _answer(q,p,repo,sources,key,client_id)

def _answer(q,p,repo,sources,key,client_id):
    cached=store.cache_get(key)
    if cached:STATS['cache_hits']+=1;return {**cached,'cacheHit':True,'originalModelCalls':cached.get('modelCalls',0),'modelCalls':0}
    result={'plan':p.model_dump(),'cacheHit':False,'modelCalls':0,'replayMode':True,'asOf':q.as_of.isoformat() if q.as_of else None,'citations':[],'status':'MISSING','route':'deterministic'}
    if p.period=='UNSUPPORTED_OR_AMBIGUOUS':
        result['answer']='The requested period is ambiguous or not supported. Specify a fiscal year and discrete quarter or annual period; no period was substituted.'
    elif not sources:
        result['answer']=f'{q.symbol}: source unavailable in this local corpus or as-of cutoff. Ticker syntax is valid; exchange listing status is unverified.'
    elif p.intent=='financial_snapshot' and p.ratio is None and re.search(r'\b(ratio|margin)\b',q.question,re.I):
        result['answer']='This requested ratio is not implemented. No model calculation or substitute figure was used.'
    elif p.intent=='financial_snapshot':
        fs=financials(q.symbol,p.fiscal_year,p.quarter,p.basis,q.as_of)
        wanted=[m for m in fs['metrics'] if not p.metrics or m['key'] in p.metrics]
        if not wanted:result['answer']=fs.get('reason','No verified facts for the requested period.')
        else:
            lines=[]
            for m in wanted:
                if m['current'] is None:lines.append(m['metric']+': Not verified in this source.');continue
                dims=next(f for f in repo.facts if f.symbol==q.symbol and f.evidence_id in m['evidenceRefs'] and f.metric==m['key'] and f.fiscal_year==p.fiscal_year and f.quarter==p.quarter)
                line=f"{m['metric']}: {fs['currency']} {m['current']:,.2f} {fs['scale']}."
                line+=f" Definition: {dims.definition}."
                if m['qoq'] is not None:line+=f" QoQ {m['qoq']:+.2f}%."
                if m['yoy'] is not None:line+=f" YoY {m['yoy']:+.2f}%."
                lines.append(line)
            result.update(status=evidence_status(wanted),answer=f'{q.symbol} · {p.period} · {fs["basis"]}. '+' '.join(lines),financials=fs,citations=repo.citations(i for m in wanted for i in m['evidenceRefs']))
        if p.ratio:
            rows,_=period_facts(q.symbol,p.fiscal_year,p.quarter,p.basis,q.as_of)
            dims={f.metric:f for f in rows if f.metric in ('pat','revenue')}
            if fs['status']!='MISSING' and len(dims)==2 and dims['revenue'].value>0:
                profit=dims['pat'];sales=dims['revenue']
                value=(profit.value*evidence.SCALES[profit.scale]/(sales.value*evidence.SCALES[sales.scale])*100).quantize(Decimal('0.01'))
                result.update(status='VERIFIED_DERIVED',answer=f'{q.symbol} · {p.period}: total-PAT/revenue margin {value}%. Deterministic calculation; PAT and revenue retain their cited definitions.',derivedRatio={'key':'total_pat_to_revenue','value':float(value),'unit':'percent'},citations=repo.citations([profit.evidence_id,sales.evidence_id]))
            else:result.update(status='MISSING',answer='Comparable positive revenue and total PAT are required for this margin. No ratio was calculated.')
    elif p.intent=='guidance_vs_actuals':
        g=guidance(q.symbol,p.fiscal_year,q.as_of)
        result.update(status=g['status'] if g['items'] else 'MISSING',guidance=g,answer=' '.join(f"{i['metric']}: original {i['target']}, actual {i['actual']}%; {i['status'].lower()}, gap beyond band {i['gap_pp']} percentage points." for i in g['items'])+' '+g['caveat'] if g['items'] else g['reason'],citations=repo.citations(i for item in g['items'] for i in item['evidenceRefs']))
    else:
        terms=set(re.findall(r'[a-z]{4,}',q.question.lower()))-{'business','overview','financial','research','what','does','company','annual'}
        period_ids={f.evidence_id for f in repo.facts if f.symbol==q.symbol and f.verification!='unverified' and f.fiscal_year==p.fiscal_year and (p.quarter is None or f.quarter==p.quarter) and (p.basis is None or f.basis==p.basis)}
        narrative_sources=[e for e in sources if e.id in period_ids or (p.basis is None and p.quarter is None and (str(p.fiscal_year) in e.title or 'FY'+str(p.fiscal_year)[-2:] in e.title or any(f'{p.fiscal_year-1}{sep}{str(p.fiscal_year)[-2:]}' in e.title for sep in ('-','–','/'))))]
        ranked=sorted(narrative_sources,key=lambda e:len(terms & set(re.findall(r'[a-z]{4,}',e.text.lower()))),reverse=True)
        if p.intent=='cash_conversion':
            rows=repo.select(q.symbol,p.fiscal_year,None,as_of=q.as_of)
            cash=[f for f in rows if f.metric=='free_cash_flow']
            if cash:
                f=cash[0];result.update(status='PARTIAL',answer=f'Company-reported free cash flow: {f.currency} {f.value} {f.scale}. Comparable cash-conversion quality has not been verified.',citations=repo.citations([f.evidence_id]),route='verified_source_summary')
            else:result['answer']='No verified cash-flow fact for this issuer and fiscal year. No cash-quality conclusion can be drawn.'
        else:
            selected=[e for e in ranked if e.evidence_method!='pdf_extracted_unverified' and (not terms or terms & set(re.findall(r'[a-z]{4,}',e.text.lower())))][:p.max_passages]
            result.update(status='PARTIAL' if selected else 'MISSING',answer='Reasoning is unavailable: no runtime model is configured. Retrieved issuer evidence is shown below; it is not a synthesized answer.' if selected else 'No relevant verified primary-source passages found.',route='retrieval_only',citations=repo.citations(e.id for e in selected))
    if result['route']=='retrieval_only' and result['citations']:
        model=reasoning.interpret(q.question,q.symbol,result['citations'],client_id=client_id)
        result['reasoningStatus']=model['status'];result['modelCalls']=model['calls']
        STATS['model_calls']+=model['calls'];STATS['tokens']+=model.get('tokens',0)
        if model['status']=='answered':
            result.update(status='MODEL_INTERPRETATION',route='mock_grounded_interpretation' if model.get('provider')=='mock' else 'gemini_grounded_interpretation',answer=' '.join(c['text'] for c in model['claims']),claims=model['claims'],limitations=model['limitations'],model=model['model'])
            ids=[i for c in model['claims'] for i in c['evidence_ids']]
            result['citations']=repo.citations(ids)
        else:
            result['httpStatus']=model.get('httpStatus',200)
            result['reasoningUnavailableReason']=model.get('reason',model.get('limitations','insufficient_evidence'))
            if model['status']=='unavailable' and model.get('reason')!='not_configured':
                result['answer']='Reasoning temporarily unavailable. Retrieved source notes are shown without an interpretive conclusion.'
            if model['status']=='insufficient_evidence':result.update(status='MISSING',answer='The available evidence does not support an answer. '+model.get('limitations',''))
        # Provider failures are not durable answers; retain deterministic/retrieval fallback but retry later.
        if model['status']=='unavailable' and model.get('reason')!='not_configured':return result
    store.cache_put(key,result);return result
