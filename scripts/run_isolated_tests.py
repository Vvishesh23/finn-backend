"""Run tests without forwarding any ambient environment or reading secret files.
Only a literal allowlist is passed. Tests use a new temporary SQLite DB and no real key.
"""
import subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='finn-mock-tests-') as directory:
    environment={'PATH':'/usr/bin:/bin','LANG':'en_US.UTF-8','FINN_DB':directory+'/test.sqlite3',
        'AI_ENABLED':'false','REASONING_PROVIDER':'disabled','FINN_ISOLATED_TESTS':'true',
        'PYTHONDONTWRITEBYTECODE':'1'}
    arguments=sys.argv[1:]
    command=[str(ROOT/'.venv/bin/python'),'-m','pytest',*arguments]
    if arguments[:1]==['--demo']:
        command=[str(ROOT/'.venv/bin/python'),str(ROOT/'scripts/mock_reasoning_demo.py')]
    result=subprocess.run(command,cwd=ROOT,env=environment)
    sys.exit(result.returncode)
