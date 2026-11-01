"""Local-only QA preview. Literal clean environment; no ambient secret forwarding."""
import subprocess,tempfile,argparse
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8010);p.add_argument('--mode',choices=['mock','disabled','unavailable','quota'],default='mock');args=p.parse_args()
if not 1024<=args.port<=65535:p.error('Use a local unprivileged port')
with tempfile.TemporaryDirectory(prefix='finn-qa-preview-') as directory:
    environment={'PATH':'/usr/bin:/bin','LANG':'en_US.UTF-8','FINN_DB':directory+'/preview.sqlite3','AI_ENABLED':'false' if args.mode=='disabled' else 'true','REASONING_PROVIDER':'disabled' if args.mode=='disabled' else 'mock','MAX_AI_REQUESTS_PER_DAY':'20'}
    if args.mode in ('unavailable','quota'):environment['FINN_PREVIEW_FAULT']=args.mode
    subprocess.run([str(root/'.venv/bin/python'),'-m','uvicorn','scripts.preview_app:app','--host','127.0.0.1','--port',str(args.port),'--no-proxy-headers','--no-access-log'],cwd=root,env=environment)
