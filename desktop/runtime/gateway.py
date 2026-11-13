"""Loopback-only Trusted Gateway for the packaged local Desktop.

The Desktop build deliberately keeps this tiny and explicit: the gateway has one
fixed upstream (the packaged Workspace Runtime on 127.0.0.1:8002), preserves
the local owner / tenant headers and cookies, and never accepts a user-supplied
upstream URL.
"""

from __future__ import annotations

import http.client
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


UPSTREAM_HOST = "127.0.0.1"
UPSTREAM_PORT = int(os.environ.get("CURIS_WORKSPACE_PORT", "8002"))
GATEWAY_PORT = int(os.environ.get("CURIS_GATEWAY_PORT", "8080"))
UPSTREAM_TIMEOUT_SECONDS = int(os.environ.get("CURIS_GATEWAY_UPSTREAM_TIMEOUT_SECONDS", "135"))
HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}


class GatewayHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _cors_headers(self) -> dict[str, str]:
        origin = self.headers.get("Origin", "")
        allowed_origins = {"http://127.0.0.1:3010", "http://localhost:3010"}
        if origin not in allowed_origins:
            return {}
        requested = self.headers.get("Access-Control-Request-Headers", "")
        allowed_headers = {
            "content-type",
            "x-tenant-id",
            "x-ceo-id",
            "x-curis-gateway",
            "x-music-import",
            "x-cg-import",
        }
        requested_headers = {
            item.strip().lower()
            for item in requested.split(",")
            if item.strip()
        }
        if not requested_headers.issubset(allowed_headers):
            return {}
        return {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": ", ".join(sorted(requested_headers or allowed_headers)),
            "Access-Control-Allow-Methods": "GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS",
            "Vary": "Origin, Access-Control-Request-Headers",
        }

    def _send_cors_headers(self) -> None:
        for key, value in self._cors_headers().items():
            self.send_header(key, value)

    def _error(self, status: int, detail: str) -> None:
        payload = json.dumps({"detail": detail}, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    def _preflight(self) -> None:
        if not self._cors_headers():
            self._error(403, "不允许的 Desktop 请求来源")
            return
        self.send_response(204)
        self.send_header("Content-Length", "0")
        self.send_header("Cache-Control", "no-store")
        self._send_cors_headers()
        self.end_headers()

    def _proxy(self) -> None:
        if self.path == "/health":
            self._health()
            return

        body = b""
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length:
            body = self.rfile.read(length)

        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in HOP_BY_HOP and key.lower() != "host"
        }
        headers["Host"] = f"{UPSTREAM_HOST}:{UPSTREAM_PORT}"
        headers["X-Curis-Gateway"] = "local-desktop"

        try:
            connection = http.client.HTTPConnection(
                UPSTREAM_HOST, UPSTREAM_PORT, timeout=UPSTREAM_TIMEOUT_SECONDS
            )
            connection.request(self.command, self.path, body=body, headers=headers)
            response = connection.getresponse()
            payload = response.read()
        except OSError:
            self._error(503, "Workspace Runtime 不可用")
            return
        finally:
            try:
                connection.close()
            except (UnboundLocalError, AttributeError):
                pass

        self.send_response(response.status, response.reason)
        for key, value in response.getheaders():
            lowered = key.lower()
            if (
                lowered not in HOP_BY_HOP
                and lowered != "content-length"
                and not lowered.startswith("access-control-")
                and lowered != "vary"
            ):
                self.send_header(key, value)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self._send_cors_headers()
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def _health(self) -> None:
        try:
            connection = http.client.HTTPConnection(UPSTREAM_HOST, UPSTREAM_PORT, timeout=2)
            connection.request("GET", "/health")
            response = connection.getresponse()
            payload = response.read()
            connection.close()
            if response.status >= 500:
                self._error(503, "Workspace Runtime 健康检查失败")
                return
        except OSError:
            self._error(503, "Workspace Runtime 未就绪")
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(payload)

    do_GET = _proxy
    do_HEAD = _proxy
    do_OPTIONS = _preflight
    do_POST = _proxy
    do_PUT = _proxy
    do_PATCH = _proxy
    do_DELETE = _proxy

    def log_message(self, _format: str, *_args: object) -> None:
        return


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", GATEWAY_PORT), GatewayHandler)
    server.daemon_threads = True
    server.serve_forever()


if __name__ == "__main__":
    main()
