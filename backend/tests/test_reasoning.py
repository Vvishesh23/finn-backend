"""Provider behavior is mocked. These tests make zero real Gemini calls."""
import json,threading
from concurrent.futures import ThreadPoolExecutor
import httpx,pytest
from backend.app import reasoning,research,evidence,store
from backend.app.models import Query
from backend.app.providers import MockReasoningProvider,ProviderError
from backend.app.inference_limits import acquire,release

@pytest.fixture
def configured(monkeypatch):
    monkeypatch.setenv('AI_ENABLED','true');monkeypatch.setenv('REASONING_PROVIDER','mock')
    monkeypatch.setenv('MAX_AI_REQUESTS_PER_DAY','20');monkeypatch.setenv('AI_GLOBAL_BUDGET_TOKENS_PER_DAY','100000')
    with store.LOCK:
        for table in ('ai_usage','ai_clients','ai_minutes','ai_leases','private_answers_v2'):store.DB.execute('DELETE FROM '+table)
        store.DB.commit()
    return evidence.REPOSITORY.citations(['hul-ar25-consolidated-p186'])

def mocked(monkeypatch,handler):
    def generate(model,payload,config):
        # Synthetic request preserves existing response/error regression cases.
        request=httpx.Request('POST','https://mock.invalid',headers={'x-goog-api-key':'unit-test-secret-do-not-log'},json=payload)
        try:response=handler(request)
        except httpx.TimeoutException:raise ProviderError(503) from None
        if response.status_code!=200:raise ProviderError(response.status_code)
        return response.json()
    provider=MockReasoningProvider(generate)
    monkeypatch.setattr(reasoning,'provider_factory',lambda cfg:provider)

def good(ids=None,text='The available statement reports annual consolidated figures.'):
    return httpx.Response(200,json={'candidates':[{'content':{'parts':[{'text':json.dumps({'claims':[{'text':text,'evidence_ids':ids or ['hul-ar25-consolidated-p186']}],'limitations':'Only the selected evidence was reviewed.'})}]}}],'usageMetadata':{'totalTokenCount':123}})

def test_disabled_and_placeholder_make_no_request(monkeypatch):
    monkeypatch.setenv('AI_ENABLED','true');monkeypatch.setenv('GEMINI_API_KEY','REPLACE_ME_SERVER_SECRET')
    monkeypatch.setattr(reasoning.httpx,'Client',lambda **kw:pytest.fail('No network allowed'))
    assert reasoning.interpret('question','HINDUNILVR',[])['calls']==0

def test_bounded_structured_call(configured,monkeypatch):
    def handler(request):
        data=json.loads(request.content)
        assert 'tools' not in data
        assert 'UNTRUSTED DATA' in data['systemInstruction']['parts'][0]['text']
        assert request.headers['x-goog-api-key']=='unit-test-secret-do-not-log'
        assert 'unit-test-secret' not in str(request.url)
        return good()
    mocked(monkeypatch,handler)
    result=reasoning.interpret('What are the reporting caveats?','HINDUNILVR',configured)
    assert result['status']=='answered';assert result['tokens']==123
    assert reasoning.usage()['callsAttempted']==1
    assert reasoning.usage()['providerReportedTokens']==123

def test_direct_financial_query_never_calls_model(configured,monkeypatch):
    monkeypatch.setattr(reasoning.httpx,'Client',lambda **kw:pytest.fail('Direct fact must not use model'))
    result=research.answer(Query(symbol='HINDUNILVR',question='FY25 consolidated revenue'))
    assert result['modelCalls']==0

def test_missing_evidence_no_call(configured,monkeypatch):
    monkeypatch.setattr(reasoning.httpx,'Client',lambda **kw:pytest.fail('Missing evidence must not call'))
    result=research.answer(Query(symbol='UNINDEXED',question='What are the risks?'))
    assert result['modelCalls']==0;assert result['status']=='MISSING'

@pytest.mark.parametrize('status',[400,401,403,429,500])
def test_provider_errors_redacted(configured,monkeypatch,status):
    mocked(monkeypatch,lambda request:httpx.Response(status,text='unit-test-secret-do-not-log'))
    r=reasoning.interpret('Interpret annual statement','HINDUNILVR',configured)
    assert r['status']=='unavailable';assert 'unit-test-secret' not in json.dumps(r)
    assert reasoning.usage()['failures']==1

def test_timeout_no_retry(configured,monkeypatch):
    calls=[]
    def handler(request):calls.append(1);raise httpx.ReadTimeout('unit-test-secret-do-not-log')
    mocked(monkeypatch,handler)
    result=reasoning.interpret('Interpret annual statement','HINDUNILVR',configured)
    assert result['status']=='unavailable';assert len(calls)==1
    assert 'unit-test-secret' not in json.dumps(result)

@pytest.mark.parametrize('ids,text,reason',[(['invented-id'],'Supported text','invalid_citation'),(['hul-ar25-consolidated-p186'],'Revenue grew 99.99%','unsupported_numeric_claim')])
def test_invalid_citation_or_numeric_claim_rejected(configured,monkeypatch,ids,text,reason):
    mocked(monkeypatch,lambda request:good(ids,text))
    r=reasoning.interpret('Interpret annual statement','HINDUNILVR',configured)
    assert r['status']=='unavailable';assert r['reason']==reason

def test_daily_budget_enforced_atomically(configured,monkeypatch):
    monkeypatch.setenv('MAX_AI_REQUESTS_PER_DAY','1');calls=[]
    mocked(monkeypatch,lambda request:(calls.append(1) or good()))
    first=reasoning.interpret('Interpret annual statement','HINDUNILVR',configured)
    second=reasoning.interpret('Interpret again','HINDUNILVR',configured)
    assert first['calls']==1;assert second['calls']==0
    assert second['reason']=='daily_budget_exhausted';assert len(calls)==1

def test_token_budget_prevents_call(configured,monkeypatch):
    monkeypatch.setenv('AI_GLOBAL_BUDGET_TOKENS_PER_DAY','1000')
    monkeypatch.setattr(reasoning.httpx,'Client',lambda **kw:pytest.fail('Budget should block call'))
    r=reasoning.interpret('Interpret annual statement','HINDUNILVR',configured)
    assert r['reason']=='daily_budget_exhausted';assert r['calls']==0

def test_singleflight_cache_avoids_duplicate_calls(configured,monkeypatch):
    calls=[];entered=threading.Event();release=threading.Event()
    def handler(request):
        calls.append(1);entered.set();assert release.wait(3);return good()
    mocked(monkeypatch,handler)
    # Include a query variant to avoid any pre-existing fixture cache key.
    q=Query(symbol='HINDUNILVR',question='Explain the annual consolidated figures with caution')
    with ThreadPoolExecutor(max_workers=2) as pool:
        first=pool.submit(research.answer,q);assert entered.wait(3)
        second=pool.submit(research.answer,q);release.set()
        rows=[first.result(),second.result()]
    assert len(calls)==1;assert sum(r['modelCalls'] for r in rows)==1
    assert sorted(r['cacheHit'] for r in rows)==[False,True]
    assert all(r['status']=='MODEL_INTERPRETATION' for r in rows)

def test_concurrency_limit_returns_without_call(configured,monkeypatch):
    cfg=reasoning.configuration();leases=[acquire(cfg,1,'held-'+str(i))[1] for i in range(2)]
    try:
        r=reasoning.interpret('Interpret statement','HINDUNILVR',configured)
        assert r['reason']=='concurrency_limit';assert r['calls']==0
    finally:
        for lease in leases:release(lease)

def test_malformed_json_rejected(configured,monkeypatch):
    mocked(monkeypatch,lambda request:httpx.Response(200,json={'candidates':[{'content':{'parts':[{'text':'not json'}]}}]}))
    r=reasoning.interpret('Interpret statement','HINDUNILVR',configured)
    assert r['status']=='unavailable'

def test_interpretive_financial_question_uses_bounded_reasoning(configured,monkeypatch):
    calls=[]
    mocked(monkeypatch,lambda request:(calls.append(1) or good()))
    q=Query(symbol='HINDUNILVR',question='Explain FY25 consolidated revenue reporting caveats')
    result=research.answer(q)
    assert result['plan']['intent']=='financial_trajectory'
    assert result['route']=='mock_grounded_interpretation';assert len(calls)==1
    assert research.answer(q)['modelCalls']==0

def test_future_period_narrative_does_not_use_old_sources(configured,monkeypatch):
    monkeypatch.setattr(reasoning.httpx,'Client',lambda **kw:pytest.fail('No matching period evidence'))
    result=research.answer(Query(symbol='HINDUNILVR',question='Explain FY2026 revenue risks'))
    assert result['status']=='MISSING';assert result['modelCalls']==0
