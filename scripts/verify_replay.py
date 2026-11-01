import sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from backend.app import store
from backend.app.models import Company,DailyBar,SourceDocument,RawFiling
for name,model in [('companies',Company),('bars',DailyBar),('documents',SourceDocument),('filings',RawFiling)]:
    rows=store.load(name)
    for row in rows:model.model_validate(row)
    print(name,len(rows),'validated')
print('Price range:',min(b['date'] for b in store.BARS),'to',max(b['date'] for b in store.BARS))

from backend.app.evidence import REPOSITORY
print('Typed evidence:',len(REPOSITORY.evidence),'Financial facts:',len(REPOSITORY.facts),'Guidance records:',len(REPOSITORY.guidance))
