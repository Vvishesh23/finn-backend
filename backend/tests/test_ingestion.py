import json,copy,importlib.util
from pathlib import Path
import pytest
from backend.app import store
from backend.app.models import SourceEvidence,FinancialFact
ROOT=Path(__file__).resolve().parents[2]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/(name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
refresh=module('refresh_portfolio')

def test_same_id_correction_is_reported_not_overwritten():
    old=store.BARS[0];new={**old,'close':old['close']+1}
    rows,conflicts=refresh.append_rows([old],[new],'bars')
    assert rows==[old];assert len(conflicts)==1

def test_repeat_source_import_is_idempotent():
    raw=store.filings()[0]
    rows,conflicts=refresh.append_rows([raw],[copy.deepcopy(raw)],'filings')
    assert len(rows)==1;assert not conflicts

def test_price_symbol_mismatch_rejected():
    with pytest.raises(ValueError):refresh.normalize_prices('TEST',{'chart':{'result':[{'meta':{'symbol':'OTHER.NS'}}]}},'2026-10-27T00:00:00+00:00','2026-10-27')

def test_acquisition_day_price_is_not_finalized():
    payload={'chart':{'result':[{'meta':{'symbol':'TEST.NS'},'timestamp':[1793072700],'indicators':{'quote':[dict(open=[1],high=[1],low=[1],close=[1],volume=[1])]}}]}}
    assert not refresh.normalize_prices('TEST',payload,'2026-10-27T12:00:00+00:00','2026-10-27')

def test_wrong_issuer_filings_not_imported():
    assert not refresh.normalize_filings('TEST',[{'symbol':'OTHER'}],'2026-10-27T12:00:00+00:00')

def test_fact_promotion_rejects_conflicting_existing_id(tmp_path):
    promote=module('promote_evidence')
    for name in ('evidence','facts','guidance'):(tmp_path/(name+'.json')).write_text((ROOT/'demo'/(name+'.json')).read_text())
    original=(tmp_path/'facts.json').read_text();row=copy.deepcopy(store.load('facts')[0]);row['value']='999'
    with pytest.raises(ValueError):promote.promote({'facts':[row]},tmp_path)
    assert (tmp_path/'facts.json').read_text()==original

def test_reviewer_pdf_hash_check_runs_before_parsing(tmp_path):
    m=module('ingest_reviewed_pdf')
    # Stub optional parser import; no real PDF claim for this synthetic tamper check.
    import sys,types
    sys.modules.setdefault('pymupdf',types.SimpleNamespace())
    p=tmp_path/'synthetic.pdf';p.write_bytes(b'%PDF-synthetic')
    with pytest.raises(ValueError,match='hash mismatch'):m.extract_bundle(p,{'document_hash':'wrong'})

def test_real_expanded_snapshot_covers_sectors():
    bars=store.BARS;filings=store.filings()
    assert len({b['symbol'] for b in bars})==17
    assert len({f['symbol'] for f in filings})==17
    assert {'SUNPHARMA','LT','NTPC','HINDUNILVR','HDFCBANK'}<={b['symbol'] for b in bars}
    assert not any(b['symbol']=='TATAMOTORS' for b in bars)
    assert all(b['date']<'2026-10-27' for b in bars)

def test_configurable_filing_alerts_and_validation():
    from fastapi.testclient import TestClient
    from backend.app.main import app
    c=TestClient(app)
    assert c.get('/api/alerts?categories=madeup').status_code==422
    assert c.get('/api/alerts?categories=').json()['filingAlerts']==[]
    # Use an explicit synthetic event at the current clock to test actual rule application.
    from datetime import datetime,timezone
    from unittest.mock import patch
    f={**store.filings()[0],'id':'synthetic-material-filing','symbol':'INFY','subject':'Acquisition of a company','raw_category':'Acquisition','source_published_at':datetime.now(timezone.utc).isoformat()}
    with patch.object(store,'filings',return_value=[f]):
        selected=c.get('/api/alerts?categories=M%26A').json()
        assert len(selected['filingAlerts'])==1
        assert not c.get('/api/alerts?categories=dividend').json()['filingAlerts']
