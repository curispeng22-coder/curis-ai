#!/usr/bin/env bash
set -euo pipefail

python3 - "$PWD/envoy.yaml.template" "$PWD/.generated/envoy.yaml" <<'PY'
import os
from pathlib import Path
import sys
from urllib.parse import urlparse

required = {name: os.environ.get(name, "").strip() for name in ("OIDC_ISSUER", "OIDC_AUDIENCE", "OIDC_JWKS_URI")}
missing = [name for name, value in required.items() if not value]
if missing:
    raise SystemExit("missing: " + ", ".join(missing))
uri = urlparse(required["OIDC_JWKS_URI"])
if uri.scheme not in {"http", "https"} or not uri.hostname:
    raise SystemExit("OIDC_JWKS_URI must be an absolute http(s) URL")
values = {
    **required,
    "JWKS_HOST": uri.hostname,
    "JWKS_PORT": str(uri.port or (443 if uri.scheme == "https" else 80)),
    "JWKS_TLS": "      transport_socket:\n        name: envoy.transport_sockets.tls\n        typed_config:\n          \"@type\": type.googleapis.com/envoy.extensions.transport_sockets.tls.v3.UpstreamTlsContext\n          sni: \"%s\"" % uri.hostname if uri.scheme == "https" else "",
}
text = Path(sys.argv[1]).read_text()
for name, value in values.items():
    if name != "JWKS_TLS" and any(ch in value for ch in "\n\r\""):
        raise SystemExit(f"unsafe value for {name}")
    text = text.replace("{{" + name + "}}", value)
output = Path(sys.argv[2])
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(text)
PY
