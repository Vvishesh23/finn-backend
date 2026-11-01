"""Append a validated reviewed bundle. Existing IDs cannot change or disappear."""
import argparse,json,sys,os,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.app.evidence import EvidenceRepository

def promote(bundle,root):
    collections={}
    for key in ('evidence','facts','guidance'):
        path=Path(root)/(key+'.json');old=json.loads(path.read_text());incoming=bundle.get(key,[])
        indexed={r['id']:r for r in old}
        for row in incoming:
            if row['id'] in indexed and indexed[row['id']]!=row:raise ValueError('Existing immutable ID differs: '+row['id'])
            indexed[row['id']]=row
        collections[key]=list(indexed.values())
    EvidenceRepository(collections['evidence'],collections['facts'],collections['guidance'])
    # Offline CLI only: no running writers. Validation precedes all replacements.
    for key,rows in collections.items():
        path=Path(root)/(key+'.json')
        fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.'+key)
        with os.fdopen(fd,'w') as f:json.dump(rows,f,indent=2)
        os.replace(tmp,path)
    return {k:len(v) for k,v in collections.items()}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('bundle');p.add_argument('--directory',default=str(Path(__file__).resolve().parents[1]/'demo'));a=p.parse_args()
    print(json.dumps(promote(json.loads(Path(a.bundle).read_text()),a.directory)))
