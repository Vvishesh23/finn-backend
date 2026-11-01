"""Synthetic packaging safety tests. No real secrets, accounts or provider calls."""
from pathlib import Path
import pytest
from scripts import build_frontend,check_publish_safety,prepare_desktop

def test_static_build_contains_only_public_assets_and_no_api_access(tmp_path):
    output=tmp_path/'public'
    files=build_frontend.build(output)
    assert set(files)=={'index.html','assets/app.js','assets/style.css','assets/preview.js','.nojekyll'}
    html=(output/'index.html').read_text()
    assert 'src="assets/preview.js' in html and 'src="/assets/' not in html
    assert html.index('assets/preview.js')<html.index('assets/app.js')
    assert "connect-src 'none'" in html and 'Frontend preview' in html
    # Real backend continues to load its normal index without the preview switch.
    assert 'preview.js' not in (build_frontend.ROOT/'frontend/index.html').read_text()
    with pytest.raises(ValueError,match='already exists'):build_frontend.build(output)

def test_prohibited_material_is_rejected_before_opening():
    for name in ['.env','.env.production','demo/private.sqlite3','key.pem','credentials.json','report.pdf','.ssh/id_rsa','../outside','/absolute/key','a.sqlite3-wal']:
        assert check_publish_safety.forbidden(name)
    assert not check_publish_safety.forbidden('.env.example')
    assert not check_publish_safety.forbidden('backend/app/main.py')
    # Deliberately constructed synthetic credential, never used for authentication.
    fake=('AI'+'za'+'X'*35).encode()
    findings=check_publish_safety.violations('synthetic.txt',fake)
    assert findings==[{'path':'synthetic.txt','rule':'google_api_key'}]
    assert fake.decode() not in str(findings)

def test_desktop_export_never_overwrites_existing_work(tmp_path,monkeypatch):
    destination=tmp_path/'existing';destination.mkdir();(destination/'keep').write_text('previous work')
    def forbidden_selection():raise AssertionError('Must reject before reading source')
    monkeypatch.setattr(prepare_desktop.package_review,'selected',forbidden_selection)
    with pytest.raises(ValueError,match='refusing to overwrite'):prepare_desktop.prepare(destination)
    assert (destination/'keep').read_text()=='previous work'

def test_desktop_export_rejects_symlink_without_reading_target(tmp_path,monkeypatch):
    root=tmp_path/'source';root.mkdir();target=root/'README.md'
    target.symlink_to(tmp_path/'never-opened-secret')
    monkeypatch.setattr(prepare_desktop.package_review,'ROOT',root)
    monkeypatch.setattr(prepare_desktop.package_review,'selected',lambda:[target])
    with pytest.raises(ValueError,match='Unsafe source path'):prepare_desktop.prepare(tmp_path/'destination')
    assert not (tmp_path/'destination').exists()
