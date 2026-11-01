"""Typed source/fact repository, independent of the watchlist and issuer names."""
import hashlib,json
from datetime import date,datetime,timezone,timedelta
from decimal import Decimal
from .models import SourceEvidence,FinancialFact,GuidanceRecord
from . import store

class EvidenceRepository:
    def __init__(self,evidence,facts,guidance=()):
        self.evidence={e['id']:SourceEvidence.model_validate(e) for e in evidence}
        self.facts=[FinancialFact.model_validate(f) for f in facts]
        self.guidance=[GuidanceRecord.model_validate(g) for g in guidance]
        if len(self.evidence)!=len(evidence):raise ValueError('Duplicate evidence ID')
        if len({f.id for f in self.facts})!=len(self.facts):raise ValueError('Duplicate fact ID')
        for f in self.facts:
            e=self.evidence.get(f.evidence_id)
            if not e or e.symbol!=f.symbol:raise ValueError('Fact/evidence issuer mismatch or missing evidence')
            if f.verification=='pdf_reviewed' and e.evidence_method!='pdf_extracted_reviewed':raise ValueError('PDF fact lacks reviewed PDF evidence')
        self.version=hashlib.sha256(json.dumps([evidence,facts,list(guidance)],sort_keys=True).encode()).hexdigest()
    def sources(self,symbol,as_of=None):
        rows=[e for e in self.evidence.values() if e.symbol==symbol]
        if as_of is not None:
            rows=[e for e in rows if e.published_at and e.published_at<=as_of]
        return rows
    def select(self,symbol,year,quarter=None,basis=None,as_of=None):
        allowed={e.id for e in self.sources(symbol,as_of)}
        return [f for f in self.facts if self.evidence[f.evidence_id].evidence_method!='pdf_extracted_unverified' and f.symbol==symbol and f.fiscal_year==year and f.quarter==quarter and f.evidence_id in allowed and f.verification!='unverified' and (basis is None or f.basis==basis)]
    def coverage(self):
        """Describe verified corpus dimensions, never listing or live-data certification."""
        result=[]
        for symbol in sorted({e.symbol for e in self.evidence.values()}):
            sources=[e for e in self.sources(symbol) if e.evidence_method!='pdf_extracted_unverified']
            ids={e.id for e in sources}
            facts=[f for f in self.facts if f.symbol==symbol and f.evidence_id in ids and f.verification!='unverified']
            periods=sorted({(f.fiscal_year,f.quarter) for f in facts},key=lambda p:(p[0],p[1] or 0),reverse=True)
            result.append({'symbol':symbol,'sourceCount':len(sources),'factCount':len(facts),
                'periods':[{'fiscalYear':y,'quarter':q,'label':f'Q{q} FY{str(y)[-2:]}' if q else f'FY{str(y)[-2:]} annual'} for y,q in periods],
                'metrics':sorted({f.metric for f in facts}),'bases':sorted({f.basis for f in facts}),
                'methods':sorted({e.evidence_method for e in sources}),
                'unknownPublicationDates':sum(e.published_at is None for e in sources)})
        return {'issuers':result,'financialIssuerCount':sum(bool(r['factCount']) for r in result),
                'sourceCount':sum(r['sourceCount'] for r in result),'factCount':sum(r['factCount'] for r in result),
                'scope':'Reviewed historical corpus; coverage is not comprehensive and does not certify current listing status.'}

    def citations(self,ids):
        return [citation(self.evidence[i]) for i in dict.fromkeys(ids) if i in self.evidence]

SCALES={'rupee':Decimal(1),'thousand':Decimal(1000),'crore':Decimal(10000000),'million':Decimal(1000000),'billion':Decimal(1000000000),'percent':Decimal(1)}
def compare_facts(current,prior,kind):
    for key in ('symbol','metric','currency','basis','accounting_standard','definition','period_type'):
        if getattr(current,key)!=getattr(prior,key):return {'status':'NOT_COMPARABLE','reason':key+' mismatch','pct':None}
    if kind=='qoq' and (current.period_type!='quarter' or prior.period_end+timedelta(days=1)!=current.period_start):return {'status':'NOT_COMPARABLE','reason':'Non-adjacent quarters','pct':None}
    if kind=='yoy' and not (prior.fiscal_year==current.fiscal_year-1 and prior.quarter==current.quarter and (prior.period_end.month,prior.period_end.day)==(current.period_end.month,current.period_end.day) and (prior.period_start.month,prior.period_start.day)==(current.period_start.month,current.period_start.day)):
        return {'status':'NOT_COMPARABLE','reason':'Not matching prior-year period','pct':None}
    from .analytics import change
    return {'status':'DERIVED' if prior.value else 'MISSING','pct':change(current.value*SCALES[current.scale],prior.value*SCALES[prior.scale])}

def citation(e):
    d=e.model_dump(mode='json')
    return {**d,'kind':e.kind,'date':d['report_date'],'source_published_at':d['published_at'],'hash':e.content_hash,'method':e.evidence_method,'is_paraphrase':True,'status':'REVIEWED' if e.evidence_method!='pdf_extracted_unverified' else 'UNVERIFIED'}

def load_repository():
    return EvidenceRepository(store.load('evidence'),store.load('facts'),store.load('guidance'))
REPOSITORY=load_repository()
