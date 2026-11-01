"""Tests must be launched through the environment-isolating runner.
Network is forbidden for every application test, including SDK tests.
"""
import os,socket,pytest
if os.environ.get('FINN_ISOLATED_TESTS')!='true':
    raise RuntimeError('Use python3 scripts/run_isolated_tests.py; ambient credentials must not enter tests.')
@pytest.fixture(autouse=True)
def deny_external_network(monkeypatch):
    def deny(*args,**kwargs):raise AssertionError('Real network forbidden in FINN tests')
    monkeypatch.setattr(socket.socket,'connect',deny)
    monkeypatch.setattr(socket,'create_connection',deny)
