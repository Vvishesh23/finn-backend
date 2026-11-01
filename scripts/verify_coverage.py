"""Offline corpus acceptance check. Genuine stored sources; no model/provider calls."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.app import evidence,research
from backend.app.models import Query

def verify(minimum):
    coverage=evidence.REPOSITORY.coverage()
    if coverage['financialIssuerCount']<minimum:raise ValueError('Insufficient verified issuer coverage')
    answers=[]
    for issuer in coverage['issuers']:
        if not issuer['factCount']:continue
        annual=next((p for p in issuer['periods'] if p['quarter'] is None),None)
        if not annual:continue
        metric='pat' if 'pat' in issuer['metrics'] else issuer['metrics'][0]
        question=f"FY{annual['fiscalYear']} {metric}"
        result=research.answer(Query(symbol=issuer['symbol'],question=question))
        if result['status']!='VERIFIED_DERIVED' or not result['citations'] or result['modelCalls']!=0:
            raise ValueError('Research acceptance failed: '+issuer['symbol'])
        answers.append({'symbol':issuer['symbol'],'question':question,'result':result})
    return {'coverage':coverage,'answers':answers,'modelCalls':0,'mode':'OFFLINE_STORED_PRIMARY_EVIDENCE'}
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--min-issuers',type=int,default=10);parser.add_argument('--output')
    args=parser.parse_args();report=verify(args.min_issuers)
    if args.output:
        with Path(args.output).open('x') as f:json.dump(report,f,indent=2)
    print(json.dumps({'financialIssuers':report['coverage']['financialIssuerCount'],'facts':report['coverage']['factCount'],'testedIssuerAnswers':len(report['answers']),'modelCalls':0}))
