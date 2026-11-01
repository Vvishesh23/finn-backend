"""Fresh, source-only portable project copy. No secrets, DB, history or venv read.
Original repository is preserved. Output must not already exist.
"""
import argparse,hashlib,json,re
from pathlib import Path
try:from . import package_review,check_publish_safety,build_frontend
except ImportError:import package_review,check_publish_safety,build_frontend

def prepare(output):
    output=Path(output)
    if output.exists():raise ValueError('Destination exists; refusing to overwrite existing work')
    files=package_review.selected();rows=[];payloads=[]
    for path in files:
        relative=path.relative_to(package_review.ROOT)
        if path.is_symlink() or not path.is_file() or check_publish_safety.forbidden(relative):raise ValueError('Unsafe source path; contents not opened')
        raw=path.read_bytes()
        if check_publish_safety.violations(relative,raw):raise ValueError('Potential credential in selected source; contents suppressed')
        if relative.parts[0]=='docs' or str(relative) in {'CODEX_HANDOFF.md','GPT_REVIEW.md'}:
            if path.suffix not in {'.jpg','.png'}:
                # Portability/privacy change in docs only; application code stays identical.
                raw=re.sub(r'/Users/[^/\s)<>\"\']+','~',raw.decode()).encode()
        payloads.append((relative,raw));rows.append({'path':str(relative),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    output.mkdir(parents=True)
    for relative,raw in payloads:
        target=output/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
    manifest={'kind':'PORTABLE_SOURCE_COPY_NOT_GIT_HISTORY','files':rows,
        'excluded':['Actual .env/credentials','SQLite/caches','virtual environments','original PDFs','Git metadata/history','old HDD project'],
        'docTransformation':'Local /Users/name prefixes replaced with ~ in text documentation only. Historical test results remain historical; see new copy verification.'}
    (output/'RELEASE_FILE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
    report={'status':'PASS','checkedSourceFiles':len(rows),'credentialPatternFindings':0,
        'limits':'Known patterns only, not a universal secret-free guarantee or history/licence audit. No excluded secret file was opened.',
        'runtime':'Docker build context allows only app, static assets, required public JSON fixtures and dependency lock. No docs/tests/tools/.env/DB.'}
    (output/'PUBLISH_SAFETY_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    build_frontend.build(output/'frontend-publish')
    (output/'frontend-publish'/'.gitignore').write_text('.DS_Store\n.env\n.env.*\n*.key\n*.pem\n')
    return {'output':str(output),'sourceFiles':len(rows),'frontend':'frontend-publish','status':'CREATED'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();print(json.dumps(prepare(a.output),indent=2))
