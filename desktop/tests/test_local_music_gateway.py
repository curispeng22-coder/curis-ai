"""Actual gateway method probes; no sockets/server/Workspace or old Root."""
import io
from email.message import Message
import pytest
from desktop.runtime.gateway import GatewayHandler


def probe(origin, requested):
    h=object.__new__(GatewayHandler);h.headers=Message();h.headers['Origin']=origin;h.headers['Access-Control-Request-Headers']=requested
    h.wfile=io.BytesIO();result={'headers':{}}
    h.send_response=lambda status,*args:result.update(status=status)
    h.send_header=lambda k,v:result['headers'].update({k:v})
    h.end_headers=lambda:None
    h._preflight()
    return result,h.wfile.getvalue()

@pytest.mark.parametrize('origin',['http://127.0.0.1:3010','http://localhost:3010'])
@pytest.mark.parametrize('import_header',['X-Music-Import','X-CG-Import'])
def test_normal_media_metadata_identity_preflight_exact_allowlist(origin, import_header):
    result,raw=probe(origin,f'Content-Type, X-Tenant-Id, X-Ceo-Id, {import_header}')
    assert result['status']==204 and raw==b''
    assert result['headers']['Access-Control-Allow-Origin']==origin
    assert result['headers']['Access-Control-Allow-Credentials']=='true'
    assert set(result['headers']['Access-Control-Allow-Headers'].split(', '))=={'content-type','x-tenant-id','x-ceo-id',import_header.lower()}
    assert '*' not in str(result)

@pytest.mark.parametrize('origin,requested',[('https://foreign.invalid','x-music-import'),('http://127.0.0.1:3010','x-music-import,x-unknown'),('http://127.0.0.1:9999','content-type'),('https://foreign.invalid','x-cg-import'),('http://127.0.0.1:3010','x-cg-import,x-unknown'),('http://localhost:3010','x-cg-import,x-unknown')])
def test_foreign_origin_or_unknown_header_remains_denied(origin,requested):
    result,raw=probe(origin,requested)
    assert result['status']==403
    assert 'Access-Control-Allow-Origin' not in result['headers']
    assert raw
