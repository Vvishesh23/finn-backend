"""Limited-pattern publication check. Never opens prohibited secret/DB/PDF paths.
Not an exhaustive secret scanner, image OCR, licence review or history audit.
"""
import argparse,json,re,subprocess
from pathlib import Path
try:from . import package_review
except ImportError:import package_review

ROOT=Path(__file__).resolve().parents[1]
PATTERNS={
    'google_api_key':rb'AIza[0-9A-Za-z_-]{35}',
    'github_token':rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})',
    'aws_access_id':rb'(?:AKIA|ASIA)[A-Z0-9]{16}',
    'private_key_block':rb'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----',
    'openai_style_key':rb'sk-(?:proj-)?[A-Za-z0-9_-]{40,}',
    'slack_token':rb'xox[baprs]-[A-Za-z0-9-]{20,}',
    'credential_in_url':rb'https?://[^\s/:]+:[^\s/@]+@',
}
def forbidden(path):
    p=Path(path);parts=p.parts;n=p.name.lower()
    return (p.is_absolute() or '..' in parts or any(x in {'.git','.venv','.aws','.ssh','secrets','private','node_modules','__pycache__'} for x in parts)
        or (n.startswith('.env') and str(p)!='.env.example') or n=='.ds_store'
        or any(n.endswith(x) for x in ('.pdf','.sqlite3','.sqlite','.db','.pem','.key','.p12','.pfx','.crt','.zip','.log'))
        or bool(re.search(r'\.(?:sqlite3|sqlite|db)-',n))
        or n.startswith('credentials') or 'service-account' in n)

def violations(path,raw):
    return [{'path':str(path),'rule':name} for name,pattern in PATTERNS.items() if re.search(pattern,raw)]

def scan(staged=False,frontend=False):
    findings=[];checked=0
    git_env={'PATH':'/usr/bin:/bin','LANG':'C','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null'}
    if frontend:
        base=ROOT/'frontend-publish'
        files=sorted(p for p in base.rglob('*') if p.is_file() or p.is_symlink())
        if not files:raise ValueError('Build frontend-publish first')
    elif staged:
        base=ROOT
        result=subprocess.run(['git','ls-files','--cached','-z'],cwd=ROOT,env=git_env,check=True,capture_output=True)
        files=[ROOT/p.decode() for p in result.stdout.split(b'\0') if p]
        if not files:raise ValueError('No staged files to check')
    else:
        base=ROOT;files=package_review.selected()
        files += [ROOT/n for n in ('RELEASE_FILE_MANIFEST.json','PUBLISH_SAFETY_REPORT.json') if (ROOT/n).is_file()]
    for path in files:
        relative=path.relative_to(base)
        if forbidden(relative) or path.is_symlink():
            findings.append({'path':str(relative),'rule':'prohibited_path_not_opened'});continue
        if staged:
            # Read reviewed index bytes rather than possibly different worktree bytes.
            result=subprocess.run(['git','show',':'+str(relative)],cwd=ROOT,env=git_env,check=True,capture_output=True)
            raw=result.stdout
        else:raw=path.read_bytes()
        checked+=1;findings.extend(violations(relative,raw))
    return {'status':'PASS' if not findings else 'FAIL','checkedFiles':checked,'findings':findings,
        'scope':'Limited known credential patterns and prohibited paths only; no secret files opened, no history audit or image OCR. Review before publishing.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();g=parser.add_mutually_exclusive_group();g.add_argument('--staged',action='store_true');g.add_argument('--frontend',action='store_true');a=parser.parse_args()
    result=scan(a.staged,a.frontend);print(json.dumps(result,indent=2));raise SystemExit(0 if result['status']=='PASS' else 1)
