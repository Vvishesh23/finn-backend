import copy,json
from datetime import datetime,timezone
from decimal import Decimal
import pytest
from backend.app import evidence,research,store
from backend.app.models import Query,FinancialFact,SourceEvidence
from fastapi.testclient import TestClient
from backend.app.main import app,requests
client=TestClient(app)

def test_real_pdf_issuer_answers_differ_and_resolve():
    for symbol,question,amount,basis in [('HINDUNILVR','FY25 consolidated revenue','63,121','consolidated'),('ASIANPAINT','FY25 standalone PBT and PAT','4,897.18','standalone')]:
        requests.clear()
        r=client.post('/api/research/query',json={'symbol':symbol,'question':question}).json()
        assert amount in r['answer'];assert basis in r['answer'].lower()
        assert r['citations'][0]['method']=='pdf_extracted_reviewed'
        assert r['citations'][0]['document_hash'];assert r['citations'][0]['page']
        assert client.get('/api/source/'+r['citations'][0]['id']).status_code==200
        assert '40,925' not in r['answer']

def test_new_real_ticker_not_in_mock_portfolio():
    assert 'ASIANPAINT' not in {c['symbol'] for c in store.COMPANIES}
    r=research.answer(Query(symbol='ASIANPAINT',question='FY25 standalone PAT'))
    assert '3,584.88' in r['answer'];assert r['modelCalls']==0

def test_standalone_not_silently_consolidated():
    r=research.answer(Query(symbol='ASIANPAINT',question='FY25 consolidated PAT'))
    assert r['status']=='MISSING';assert not r['citations']

def test_no_quarter_from_annual():
    r=research.answer(Query(symbol='HINDUNILVR',question='Q4 FY25 revenue'))
    assert r['status']=='MISSING'

def test_pdf_annual_yoy_deterministic():
    fs=research.financials('HINDUNILVR',2025,None)
    rev=next(m for m in fs['metrics'] if m['key']=='revenue')
    assert rev['current']==63121;assert rev['year_ago']==61896
    assert rev['yoy']==1.98;assert rev['qoq'] is None
    r=research.answer(Query(symbol='ASIANPAINT',question='FY25 EBITDA'))
    assert 'other income' in r['citations'][0]['text']

def test_explicit_asof_excludes_unknown_publication():
    r=research.answer(Query(symbol='HINDUNILVR',question='FY25 revenue',as_of=datetime(2026,1,1,tzinfo=timezone.utc)))
    assert r['status']=='MISSING';assert not r['citations']
    r=research.answer(Query(symbol='INFY',question='FY25 guidance',as_of=datetime(2025,4,20,tzinfo=timezone.utc)))
    assert r['status']=='MISSING' # Transcript published April 22, not call day April 17.

def test_fact_evidence_must_match_issuer():
    ev=store.load('evidence');facts=store.load('facts');bad=copy.deepcopy(facts)
    bad[0]['symbol']='OTHER'
    with pytest.raises(ValueError):evidence.EvidenceRepository(ev,bad)

def test_same_issuer_new_fact_no_code_branch(monkeypatch):
    ev=copy.deepcopy(store.load('evidence')[4]);ev.update(id='synthetic-third-party',symbol='SYNTHETIC',title='Synthetic unit test, not genuine issuer')
    f=copy.deepcopy(store.load('facts')[15]);f.update(id='synthetic-fact',symbol='SYNTHETIC',evidence_id=ev['id'],value='123')
    repo=evidence.EvidenceRepository([ev],[f]);monkeypatch.setattr(evidence,'REPOSITORY',repo)
    result=research.answer(Query(symbol='SYNTHETIC',question='FY25 consolidated revenue'))
    assert '123.00' in result['answer'];assert '63,121' not in result['answer']

@pytest.mark.parametrize('field,value',[('period_start','2025-04-02'),('quarter',4),('value','NaN')])
def test_bad_fact_contract_rejected(field,value):
    f=copy.deepcopy(store.load('facts')[15]);f[field]=value
    with pytest.raises(ValueError):FinancialFact.model_validate(f)

def test_financial_comparison_rejects_entity_definition_and_period():
    fact=evidence.REPOSITORY.facts[0]
    prior=next(f for f in evidence.REPOSITORY.facts if f.symbol==fact.symbol and f.metric==fact.metric and f.quarter==4 and f.fiscal_year==2024)
    for update in [{'symbol':'OTHER'},{'basis':'standalone'},{'definition':'different revenue'},{'period_type':'annual'}]:
        bad=prior.model_copy(update=update)
        assert evidence.compare_facts(fact,bad,'yoy')['status']=='NOT_COMPARABLE'
    assert evidence.compare_facts(fact,prior,'qoq')['status']=='NOT_COMPARABLE'

def test_unverified_fact_not_promoted_to_answer(monkeypatch):
    ev=store.load('evidence');facts=copy.deepcopy(store.load('facts'))
    for f in facts:
        if f['symbol']=='HINDUNILVR':f['verification']='unverified'
    monkeypatch.setattr(evidence,'REPOSITORY',evidence.EvidenceRepository(ev,facts))
    assert research.answer(Query(symbol='HINDUNILVR',question='FY25 revenue'))['status']=='MISSING'

def test_fact_version_invalidates_cache(monkeypatch):
    q=Query(symbol='HINDUNILVR',question='FY25 revenue');research.answer(q)
    assert research.answer(q)['cacheHit']
    facts=copy.deepcopy(store.load('facts'));facts[15]['value']='63122'
    monkeypatch.setattr(evidence,'REPOSITORY',evidence.EvidenceRepository(store.load('evidence'),facts,store.load('guidance')))
    result=research.answer(q);assert not result['cacheHit'];assert '63,122' in result['answer']

def test_document_only_new_ticker_coverage_status():
    result=client.get('/api/company/ASIANPAINT').json()
    assert result['sourceStatus']=='PRIMARY_DOCUMENTS_ONLY'
    assert result['documents']

def test_real_business_passages_not_model_background():
    for symbol,word in [('HINDUNILVR','FMCG'),('ASIANPAINT','paints')]:
        r=research.answer(Query(symbol=symbol,question='Business overview'))
        assert r['route']=='retrieval_only'
        assert any(word in c['text'] for c in r['citations'])
        assert any('business' in c['id'] for c in r['citations'])

@pytest.mark.parametrize('publication',[None,'2025-05-01T00:00:00+00:00'])
def test_guidance_needs_contemporaneous_public_evidence(monkeypatch,publication):
    entries=copy.deepcopy(store.load('evidence'))
    for row in entries:
        if row['id']=='infy-call-fy24':row['published_at']=publication
    monkeypatch.setattr(evidence,'REPOSITORY',evidence.EvidenceRepository(entries,store.load('facts'),store.load('guidance')))
    assert not research.guidance('INFY')['items']


@pytest.mark.parametrize('symbol,period',[('INFY','Q4 FY25'),('HINDUNILVR','FY25 annual'),('ASIANPAINT','FY25 annual')])
def test_company_financial_endpoints_agree(symbol,period):
    detail=client.get('/api/company/'+symbol).json()['financials']
    standalone=client.get('/api/company/'+symbol+'/financials').json()
    assert detail==standalone
    assert standalone['periods'][0]==period
    assert any(m['current'] is not None for m in standalone['metrics'])

def test_company_financial_unknown_does_not_borrow_issuer_data():
    result=client.get('/api/company/ZENSARTECH/financials').json()
    assert result['status']=='MISSING'
    assert result['metrics']==[]

def test_company_default_period_is_data_driven(monkeypatch):
    # Synthetic earlier-only corpus checks selection rather than hardcoded FY25.
    facts=[f for f in store.load('facts') if f['symbol']=='HINDUNILVR' and f['fiscal_year']==2024]
    monkeypatch.setattr(evidence,'REPOSITORY',evidence.EvidenceRepository(store.load('evidence'),facts))
    result=research.company_financials('HINDUNILVR')
    assert result['periods'][0]=='FY24 annual'
    assert next(m for m in result['metrics'] if m['key']=='revenue')['current']==61896
