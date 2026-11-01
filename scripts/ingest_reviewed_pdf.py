"""Reproducible local PDF -> small reviewed evidence/fact bundle.
No network, model, arbitrary code or automatic table guessing. Manifest pins publisher
file hash, identity, selected pages, extraction regex and expected manually-reviewed values.
"""
import argparse,hashlib,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.app.models import SourceEvidence,FinancialFact

def extract_bundle(pdf,manifest):
    import pymupdf
    raw=Path(pdf).read_bytes()
    if len(raw)>40000000 or not raw.startswith(b'%PDF'):raise ValueError('Invalid/oversize PDF')
    sha=hashlib.sha256(raw).hexdigest()
    if sha!=manifest['document_hash']:raise ValueError('Document hash mismatch; source changed')
    evidence=[];facts=[]
    with pymupdf.open(stream=raw,filetype='pdf') as doc:
        for entry in manifest['pages']:
            page=int(entry['page']);text=doc[page-1].get_text()
            if any(token.lower() not in text.lower() for token in entry['identity_checks']):raise ValueError('Page identity/basis checks failed')
            positions=[];items=[]
            for row in entry.get('facts',[]):
                matches=list(re.finditer(row['pattern'],text,re.I))
                if len(matches)!=1:raise ValueError('Extraction match is not unique: '+row['id'])
                match=matches[0];value=match['value'].replace(',','').replace(' ','')
                if value!=str(row['expected_value']):raise ValueError('Reviewed value mismatch: '+row['id'])
                positions.append(match.span())
                f={k:v for k,v in row.items() if k not in ('pattern','expected_value')}
                f.update(symbol=manifest['symbol'],value=value,evidence_id=entry['id'],verification='pdf_reviewed')
                facts.append(FinancialFact.model_validate(f).model_dump(mode='json'))
                items.append(f"{row['metric']} {row['fiscal_year']}: {value} {row['currency']} {row['scale']}")
            if entry.get('passage_pattern'):
                matches=list(re.finditer(entry['passage_pattern'],text,re.S))
                if len(matches)!=1:raise ValueError('Passage anchor is not unique')
                positions.append(matches[0].span())
            if not positions:raise ValueError('Evidence requires a matched source span')
            # Persist minimal derived financial records, not whole copyrighted PDF pages.
            summary=entry['summary']+(' Derived table facts: '+'; '.join(items)+'.' if items else '')
            e=dict(id=entry['id'],symbol=manifest['symbol'],title=manifest['title'],publisher=manifest['publisher'],url=manifest['url'],kind=manifest.get('kind','annual_report'),report_date=manifest['report_date'],published_at=manifest.get('published_at'),ingested_at=manifest['ingested_at'],page=page,section=entry['section'],text=summary,evidence_method='pdf_extracted_reviewed',content_hash=hashlib.sha256(summary.encode()).hexdigest(),document_hash=sha,offsets=[min(a for a,b in positions),max(b for a,b in positions)])
            evidence.append(SourceEvidence.model_validate(e).model_dump(mode='json'))
    return {'evidence':evidence,'facts':facts,'guidance':[],'review':'Manifest values and reporting dimensions manually reviewed against original PDF pages; extraction must match exactly.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--pdf',required=True);p.add_argument('--manifest',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();bundle=extract_bundle(a.pdf,json.loads(Path(a.manifest).read_text()))
    with Path(a.output).open('x') as f:json.dump(bundle,f,indent=2)
    print(json.dumps({'evidence':len(bundle['evidence']),'facts':len(bundle['facts']),'output':a.output}))
if __name__=='__main__':main()
