"""Credential access exists only in the explicitly selected production provider.
Development/tests inject MockReasoningProvider; no SDK client is created at import.
"""
import json,os,multiprocessing,logging
from typing import Protocol

class ProviderError(Exception):
    def __init__(self,status=503):
        self.status=status if isinstance(status,int) else 503
        super().__init__('provider_failure')

class ReasoningProvider(Protocol):
    def generate(self,model,payload,config): ...

class DisabledReasoningProvider:
    def generate(self,model,payload,config):raise ProviderError(503)

class MockReasoningProvider:
    """Explicit mock: fixed evidence-linked output; no network or credential access."""
    def __init__(self,handler=None):self.handler=handler;self.calls=0
    def generate(self,model,payload,config):
        self.calls+=1
        if self.handler:return self.handler(model,payload,config)
        data=json.loads(payload['contents'][0]['parts'][0]['text'])
        first=data['evidence'][0]
        parsed={'claims':[{'text':'The supplied issuer passage is the available evidence; this is a mock interpretation, not live Gemini analysis.','evidence_ids':[first['id']]}], 'limitations':'Mock provider; no live model quality validation.'}
        return {'candidates':[{'content':{'parts':[{'text':json.dumps(parsed)}]}}],'usageMetadata':{'totalTokenCount':0}}

class GeminiReasoningProvider:
    """Executed by deployment only. Never instantiate with ambient credentials in tests."""
    def __init__(self,client_factory=None,credential_loader=None):
        self.client_factory=client_factory
        self.credential_loader=credential_loader or (lambda:os.environ.get('GEMINI_API_KEY',''))
    def generate(self,model,payload,config):
        from google import genai
        from google.genai import types
        key=self.credential_loader().strip()
        if not key or any(x in key.lower() for x in ('placeholder','replace_me','your_key','example')):
            raise ProviderError(503)
        if self.client_factory is None:
            return isolated_generate(key,model,payload,config)
        factory=self.client_factory
        client=None
        try:
            # Explicit key prevents SDK ambient credential discovery; no SDK retries/tools.
            client=factory(api_key=key,vertexai=False,http_options=types.HttpOptions(
                base_url='https://generativelanguage.googleapis.com',api_version='v1beta',
                timeout=config['timeout']*1000,retry_options=types.HttpRetryOptions(attempts=1),
                client_args={'trust_env':False,'follow_redirects':False}))
            generation=types.GenerateContentConfig(
                system_instruction=payload['systemInstruction']['parts'][0]['text'],
                temperature=0,max_output_tokens=config['max_output'],response_mime_type='application/json',
                response_json_schema=payload['generationConfig']['responseJsonSchema'],
                thinking_config=(types.ThinkingConfig(**payload['generationConfig']['thinkingConfig'])
                    if 'thinkingConfig' in payload['generationConfig'] else None),
                tools=[],automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))
            response=client.models.generate_content(model=model,contents=payload['contents'],config=generation)
            # Accept only normal bounded text, never a function-call/tool result.
            raw=response.text or ''
            if len(raw.encode())>64000:raise ProviderError(503)
            tokens=getattr(getattr(response,'usage_metadata',None),'total_token_count',0) or 0
            candidates=getattr(response,'candidates',None) or []
            finish=getattr(candidates[0],'finish_reason',None) if candidates else None
            finish=getattr(finish,'value',finish)
            return {'candidates':[{'finishReason':finish,'content':{'parts':[{'text':raw}]}}],'usageMetadata':{'totalTokenCount':tokens}}
        except ProviderError:raise
        except Exception as exc:
            # No provider response body, headers, secret or exception string crosses boundary.
            raise ProviderError(getattr(exc,'code',503)) from None
        finally:
            if client is not None:
                try:client.close()
                except Exception:pass


def _sdk_worker(connection,key,model,payload,config):
    # Deployment child only: no inherited SDK logging of prompts/provider errors.
    logging.disable(logging.CRITICAL)
    try:
        from google import genai
        provider=GeminiReasoningProvider(client_factory=genai.Client,credential_loader=lambda:key)
        connection.send(('ok',provider.generate(model,payload,config)))
    except ProviderError as exc:connection.send(('error',exc.status))
    except Exception:connection.send(('error',503))
    finally:connection.close()

def isolated_generate(key,model,payload,config):
    """Hard wall deadline: terminate the SDK child before releasing its shared lease.
    The key crosses a local process boundary in memory, never command-line arguments.
    """
    context=multiprocessing.get_context('spawn')
    receiver,sender=context.Pipe(duplex=False)
    process=context.Process(target=_sdk_worker,args=(sender,key,model,payload,config),daemon=True)
    process.start();sender.close()
    try:
        if not receiver.poll(config['timeout']):raise ProviderError(504)
        status,body=receiver.recv()
        if status!='ok':raise ProviderError(body)
        return body
    except (EOFError,OSError):raise ProviderError(503) from None
    finally:
        if process.is_alive():process.terminate()
        process.join(timeout=2)
        if process.is_alive():process.kill();process.join(timeout=2)
        receiver.close()
