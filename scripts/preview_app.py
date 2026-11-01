"""Local QA harness only; production starts backend.app.main:app directly."""
import os
from backend.app.main import app
from backend.app import reasoning
from backend.app.providers import MockReasoningProvider,ProviderError
fault=os.environ.get('FINN_PREVIEW_FAULT','')
if fault:
    def failure(*args):raise ProviderError(429 if fault=='quota' else 503)
    reasoning.provider_factory=lambda cfg:MockReasoningProvider(failure)
