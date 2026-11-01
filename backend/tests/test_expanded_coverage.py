"""Real corpus regressions; synthetic mutations are explicitly labelled."""
import copy
from decimal import Decimal
from datetime import datetime,timezone
import pytest
from fastapi.testclient import TestClient
from backend.app import evidence,research,store
from backend.app.main import app
from backend.app.models import Query
client=TestClient(app)

@pytest.mark.parametrize('symbol,metric,value',[
 ('RELIANCE','revenue',980136),('LT','pbt',23578.79),
 ('DRREDDY','revenue',32643.9),('WIPRO','pat',13218),
 ('BAJFINANCE','pat',16779.48),('ICICIBANK','pat',54569.3756),
 ('NTPC','revenue',188138.06),('POWERGRID','pat',15521.44)])
def test_real_reviewed_issuer_amount_and_source(symbol,metric,value):
    result=research.answer(Query(symbol=symbol,question='FY25 '+metric))
    assert result['status']=='VERIFIED_DERIVED'
    fs=result['financials'];assert fs['unit']=='INR crore'
    row=next(m for m in fs['metrics'] if m['key']==metric)
    assert row['current']==pytest.approx(value)
    assert row['previous'] is None and row['qoq'] is None
    assert row['yoy'] is not None
    assert result['modelCalls']==0
    assert all(c['document_hash'] and c['page'] and c['evidence_method']=='pdf_extracted_reviewed' for c in result['citations'])

@pytest.mark.parametrize('symbol',['RELIANCE','LT','DRREDDY','WIPRO','BAJFINANCE','ICICIBANK','NTPC','POWERGRID'])
def test_new_reports_unknown_publication_fail_closed(symbol):
    result=research.answer(Query(symbol=symbol,question='FY25 PAT',as_of=datetime(2026,10,28,tzinfo=timezone.utc)))
    assert result['status']=='MISSING'
    assert not result['citations']

def test_coverage_comes_from_repository_and_exposes_dimensions():
    result=client.get('/api/coverage').json()
    assert result['financialIssuerCount']==11
    assert result['factCount']==71
    rows={r['symbol']:r for r in result['issuers']}
    assert rows['WIPRO']['bases']==['consolidated']
    assert rows['ASIANPAINT']['bases']==['standalone']
    assert rows['ICICIBANK']['metrics']==['pat']
    assert rows['NTPC']['metrics']==['pat','revenue']
    assert rows['INFY']['methods']==['legacy_curated_note']

def test_powergrid_quarters_are_not_annual_or_ytd():
    result=research.answer(Query(symbol='POWERGRID',question='Q4 FY25 revenue and PAT'))
    rows={r['key']:r for r in result['financials']['metrics']}
    assert rows['revenue']['current']==12275.35
    assert rows['revenue']['previous']==11233.03
    assert rows['revenue']['year_ago']==11978.11
    assert rows['revenue']['qoq']==9.28
    assert rows['pat']['current']==4142.87
    assert rows['pbt']['status']=='MISSING'
    assert rows['ebitda']['status']=='MISSING'

def test_bank_metrics_not_substituted():
    result=research.answer(Query(symbol='ICICIBANK',question='FY25 revenue and EBITDA'))
    assert result['status']=='MISSING'
    assert 'Not verified' in result['answer']
    assert not result['citations']

def test_synthetic_mixed_currency_statement_rejected(monkeypatch):
    facts=copy.deepcopy(store.load('facts'))
    for f in facts:
        if f['symbol']=='LT' and f['fiscal_year']==2025 and f['metric']=='pbt':f['currency']='USD'
    monkeypatch.setattr(evidence,'REPOSITORY',evidence.EvidenceRepository(store.load('evidence'),facts,store.load('guidance')))
    assert research.financials('LT',2025,None)['status']=='MISSING'

def test_synthetic_mixed_scale_statement_normalized(monkeypatch):
    facts=copy.deepcopy(store.load('facts'))
    for f in facts:
        if f['symbol']=='LT' and f['metric']=='pbt':
            f['value']=str(Decimal(f['value'])*10);f['scale']='million'
    monkeypatch.setattr(evidence,'REPOSITORY',evidence.EvidenceRepository(store.load('evidence'),facts,store.load('guidance')))
    result=research.financials('LT',2025,None)
    pbt=next(m for m in result['metrics'] if m['key']=='pbt')
    assert pbt['current']==23578.79 and pbt['year_ago']==20517.11
    assert result['unit']=='INR crore'


def test_revalidation_headers_and_asset_version():
    response=client.get('/')
    assert response.headers['cache-control']=='no-cache'
    assert '/assets/app.js?v=cp11' in response.text
    assert client.get('/api/coverage').headers['cache-control']=='no-cache'
