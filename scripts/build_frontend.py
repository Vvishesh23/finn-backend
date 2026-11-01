"""Build only explicitly public frontend assets. No env, DB, docs or backend reads."""
import argparse
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def build(output):
    output=Path(output)
    if output.exists():raise ValueError('Output already exists; choose a new folder to preserve existing work')
    sources=[ROOT/'frontend'/name for name in ('index.html','app.js','style.css','preview.js')]
    if any(p.is_symlink() or not p.is_file() for p in sources):raise ValueError('Unsafe frontend source')
    output.mkdir(parents=True)
    (output/'assets').mkdir()
    html=sources[0].read_text().replace('href="/assets/','href="assets/').replace('src="/assets/','src="assets/')
    html=html.replace('<script src="assets/app.js', '<script src="assets/preview.js?v=1" defer></script><script src="assets/app.js')
    html=html.replace('Snapshot mode','Frontend preview').replace('Loading source evidence…','Loading frontend preview…')
    html=html.replace('</head>','<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; script-src \'self\'; style-src \'self\'; img-src \'self\' data:; connect-src \'none\'; base-uri \'none\'; form-action \'none\'"><meta name="referrer" content="strict-origin-when-cross-origin"></head>')
    (output/'index.html').write_text(html)
    for path in sources[1:]:(output/'assets'/path.name).write_bytes(path.read_bytes())
    (output/'.nojekyll').write_text('')
    return sorted(str(p.relative_to(output)) for p in output.rglob('*') if p.is_file())

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='dist');a=p.parse_args()
    print('Frontend-only preview built:',', '.join(build(a.output)))
