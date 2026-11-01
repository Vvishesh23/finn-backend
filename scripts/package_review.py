"""Explicit source-only review export. Never opens secret files, DBs or .git content.
This is a working-tree snapshot, not GitHub publication or an AI conversation export.
"""
import argparse,json,hashlib,re,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def selected():
    roots={'backend/app':{'.py'},'backend/tests':{'.py'},'frontend':{'.js','.css','.html','.cjs'},'scripts':{'.py'},'demo':{'.json'},'deploy':{'.yaml'},'docs':{'.md','.txt','.json','.jpg','.png'}}
    files=[ROOT/name for name in ['README.md','CODEX_HANDOFF.md','GPT_REVIEW.md','DEPLOYMENT_README.md','GITHUB_RENDER_STEPS.md','Dockerfile','start.sh','pytest.ini','.gitignore','.dockerignore','.env.example','render.yaml','backend/requirements.txt','backend/requirements.lock','backend/requirements-pdf.txt']]
    for directory,extensions in roots.items():
        for path in (ROOT/directory).rglob('*'):
            if path.is_symlink():raise ValueError('Symlink not permitted in export')
            if path.is_file() and path.suffix in extensions and not any(p.startswith('.') or p=='__pycache__' for p in path.relative_to(ROOT).parts):files.append(path)
    return sorted(set(files))
def export(output):
    manifest=[];google_key=re.compile(rb'AIza[0-9A-Za-z_-]{35}')
    files=selected()
    for path in files:
        if path.is_symlink() or not path.is_file():raise ValueError('Missing/unsafe allowlisted file')
        raw=path.read_bytes()
        if google_key.search(raw):raise ValueError('Potential credential pattern in selected export; contents suppressed')
        manifest.append({'path':str(path.relative_to(ROOT)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED) as archive:
        for row in manifest:archive.write(ROOT/row['path'],'finn/'+row['path'])
        archive.writestr('finn/RELEASE_FILE_MANIFEST.json',json.dumps({'kind':'UNCOMMITTED_WORKTREE_REVIEW_EXPORT','files':manifest,'excluded':'Secrets, SQLite, .git, venvs, original PDFs, old HDD inputs; not a guarantee about unknown files/history.'},indent=2))
    with zipfile.ZipFile(output) as archive:
        assert archive.testzip() is None
        assert all(not n.endswith(('.pdf','.sqlite3','.key','.pem')) and '/.env' not in n.replace('/.env.example','/allowed-example') for n in archive.namelist())
    return {'files':len(files),'archive':str(output),'sha256':hashlib.sha256(Path(output).read_bytes()).hexdigest(),'credentialPatternMatchesInSelectedFiles':0}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args();print(json.dumps(export(args.output),indent=2))
