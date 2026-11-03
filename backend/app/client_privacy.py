"""Pseudonymous rate identity; signed session cache isolation; no raw IP storage."""
import hashlib,hmac,secrets,ipaddress,os
from . import store
with store.LOCK:
    store.DB.execute('CREATE TABLE IF NOT EXISTS security_meta(name TEXT PRIMARY KEY,value TEXT NOT NULL)')
    store.DB.execute('INSERT INTO security_meta VALUES (?,?) ON CONFLICT DO NOTHING',('session_signer',secrets.token_hex(32)))
    SIGNER=bytes.fromhex(store.DB.execute('SELECT value FROM security_meta WHERE name=?',('session_signer',)).fetchone()[0])
    store.DB.commit()
def digest(text):return hmac.new(SIGNER,text.encode(),hashlib.sha256).hexdigest()
def peer_address(request):
    peer=request.client.host if request.client else 'unknown'
    try:
        networks=[ipaddress.ip_network(n.strip()) for n in os.environ.get('TRUSTED_PROXY_CIDRS','').split(',') if n.strip()]
        address=ipaddress.ip_address(peer)
        if not any(address in n for n in networks):return peer
        chain=request.headers.get('x-forwarded-for','').split(',')
        if len(chain)>16:return peer
        for raw in reversed(chain):
            address=ipaddress.ip_address(raw.strip())
            if not any(address in n for n in networks):return str(address)
    except ValueError:pass
    return peer

def context(request):
    cookie=request.cookies.get('finn_session','');parts=cookie.split('.')
    valid=len(parts)==2 and len(parts[0])==32 and all(c in '0123456789abcdef' for c in parts[0]) and hmac.compare_digest(parts[1],digest('session:'+parts[0]))
    if not valid:
        token=secrets.token_hex(16);cookie=token+'.'+digest('session:'+token)
    peer=peer_address(request)
    return digest('rate:'+peer),digest('cache:'+peer+':'+cookie),cookie
