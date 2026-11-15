"""Shared public-only target, DNS and TLS proxy policy for Reader."""
from __future__ import annotations

import base64
import hashlib
import http.client
import ipaddress
import json
import os
import re
import secrets
import select
import socket
import socketserver
import ssl
import stat
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path
from urllib.parse import parse_qsl, quote, urljoin, urlsplit

import certifi

from .agent_work_resources import safe_directory

SENSITIVE_HEADERS = {"authorization", "proxy-authorization", "cookie", "set-cookie",
                     "set-cookie2", "connection", "proxy-connection", "transfer-encoding", "content-length", "referer"}
PUBLIC_REQUEST_HEADERS = {"accept", "accept-language", "accept-encoding", "user-agent", "range",
                          "if-none-match", "if-modified-since", "sec-fetch-dest", "sec-fetch-mode", "sec-fetch-site"}
BENCHMARK_NETWORK = ipaddress.ip_network("198.18.0.0/15")

def host_name(value):
    if not isinstance(value, str) or not value or any(ord(c) <= 32 for c in value):
        raise ValueError("请输入明确的公开网站域名。")
    host = value.lower().encode("idna").decode("ascii")
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", host) or ".." in host or "." not in host:
        raise ValueError("网站域名不合法。")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("本次只允许明确的网站域名。")
    if host.endswith((".local", ".localhost", ".internal", ".invalid", ".test")):
        raise ValueError("不能连接本机或内部网站。")
    return host


def _doh_exchange(host):
    """Fixed public DNS bootstrap, without system DNS, proxy settings or credentials."""
    connections = []
    def close():
        for connection in list(connections):
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            connection.close()
    timer = threading.Timer(8, close)
    timer.daemon = True
    timer.start()
    try:
        raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connections.append(raw)
        raw.settimeout(5)
        raw.connect(("1.1.1.1", 443))
        context = ssl.create_default_context(cafile=certifi.where())
        if not context.check_hostname or context.verify_mode != ssl.CERT_REQUIRED:
            raise ValueError("公开 DNS 的证书核验不可关闭。")
        secure = context.wrap_socket(raw, server_hostname="cloudflare-dns.com", do_handshake_on_connect=False)
        connections.append(secure)
        secure.settimeout(5)
        secure.do_handshake()
        path = "/dns-query?name=" + quote(host, safe="") + "&type=A"
        secure.sendall(("GET " + path + " HTTP/1.1\r\nHost: cloudflare-dns.com\r\n"
            "Accept: application/dns-json\r\nConnection: close\r\n\r\n").encode("ascii"))
        response = http.client.HTTPResponse(secure)
        response.begin()
        return response.status, response.read(65537)
    finally:
        timer.cancel()
        close()


def pinned_public_dns(host, *, exchange=None):
    host = host_name(host)
    try:
        status, raw = (exchange or _doh_exchange)(host)
        if status != 200 or not isinstance(raw, bytes) or len(raw) > 65536:
            raise ValueError("公开 DNS 响应不完整或超出范围。")
        result = json.loads(raw)
        if not isinstance(result, dict) or type(result.get("Status")) is not int or result["Status"] != 0:
            raise ValueError("公开 DNS 未确认该域名。")
        questions = result.get("Question")
        if (not isinstance(questions, list) or len(questions) != 1
                or type(questions[0].get("type")) is not int or questions[0]["type"] != 1
                or questions[0].get("name", "").removesuffix(".").lower() != host):
            raise ValueError("公开 DNS 回执不属于已批准域名。")
        answers = result.get("Answer")
        if not isinstance(answers, list) or not 1 <= len(answers) <= 32:
            raise ValueError("公开 DNS 没有可核验地址。")
        addresses = []
        for answer in answers:
            if (not isinstance(answer, dict) or type(answer.get("type")) is not int
                    or answer["type"] not in {1, 5} or not isinstance(answer.get("data"), str)):
                raise ValueError("公开 DNS 包含未请求的地址类型。")
            host_name(answer.get("name", "").removesuffix("."))
            if answer["type"] == 5:
                host_name(answer.get("data", "").removesuffix("."))
                continue
            address = ipaddress.ip_address(answer.get("data", ""))
            if (not isinstance(address, ipaddress.IPv4Address) or not address.is_global
                    or address.is_multicast or address.is_reserved):
                raise ValueError("公开 DNS 包含非公开地址。")
            addresses.append((socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "", (str(address), 443)))
        if not addresses:
            raise ValueError("公开 DNS 没有 A 地址。")
        return addresses
    except (OSError, ValueError, TypeError, AttributeError, http.client.HTTPException) as error:
        raise ValueError("无法核验公开网站地址；没有放行私网或本机地址。") from error


class PublicTargets:
    def __init__(self, hosts, *, resolver=socket.getaddrinfo, bootstrap=pinned_public_dns):
        if not isinstance(hosts, (list, tuple)) or not 1 <= len(hosts) <= 8:
            raise ValueError("每次明确选择 1 至 8 个公开网站域名。")
        self.hosts = frozenset(host_name(h) for h in hosts)
        self.resolver = resolver
        self.bootstrap = bootstrap
        self.dns_evidence = {}
        self.dns_lock = threading.Lock()

    def url(self, value):
        if not isinstance(value, str) or len(value) > 4096 or "\\" in value or any(ord(c) <= 32 for c in value):
            raise ValueError("网页地址不合法。")
        parsed = urlsplit(value)
        if (parsed.scheme != "https" or parsed.username or parsed.password or parsed.port not in {None, 443}
                or host_name(parsed.hostname or "") not in self.hosts):
            raise ValueError("网页不在本次已确认的 HTTPS 网站范围。")
        if any(key.lower() in {"token", "access_token", "auth", "session", "sid", "api_key", "password", "code"}
               for key, _ in parse_qsl(parsed.query) + parse_qsl(parsed.fragment)):
            raise ValueError("不能通过网页地址携带账号凭据。")
        return host_name(parsed.hostname)

    def resolve(self, host):
        host = host_name(host)
        if host not in self.hosts:
            raise ValueError("域名没有授权。")
        addresses = self.resolver(host, 443, type=socket.SOCK_STREAM)
        if not addresses or len(addresses) > 32:
            raise ValueError("公开网站解析无法核验。")
        benchmark_only = all(family == socket.AF_INET and kind == socket.SOCK_STREAM
            and ipaddress.ip_address(address[0]) in BENCHMARK_NETWORK
            for family, kind, _protocol, _name, address in addresses)
        method = "SYSTEM_PUBLIC"
        if benchmark_only:
            addresses = self.bootstrap(host)
            method = "PINNED_DOH_BENCHMARK_BOOTSTRAP"
            if not addresses or len(addresses) > 32:
                raise ValueError("公开 DNS 无法核验。")
        for family, kind, _protocol, _name, address in addresses:
            ip = ipaddress.ip_address(address[0])
            if (family not in {socket.AF_INET, socket.AF_INET6} or kind != socket.SOCK_STREAM
                    or address[1] != 443 or not ip.is_global or ip.is_multicast or ip.is_reserved
                    or (family == socket.AF_INET) != (ip.version == 4)):
                raise ValueError("解析包含本机、内部或保留地址。")
            if isinstance(ip, ipaddress.IPv6Address) and (ip.ipv4_mapped or ip.sixtofour or ip.teredo
                    or ip in ipaddress.ip_network("64:ff9b::/96") or ip in ipaddress.ip_network("64:ff9b:1::/48")
                    or "%" in address[0] or address[3] != 0):
                raise ValueError("不能通过转换地址或接口范围访问目标。")
        with self.dns_lock:
            self.dns_evidence[host] = {"host": host, "method": method, "addresses": sorted({row[4][0] for row in addresses}),
                "resolver": "cloudflare-dns.com" if benchmark_only else "system",
                "bootstrap_ip": "1.1.1.1" if benchmark_only else None}
        return addresses

    def dns_snapshot(self):
        with self.dns_lock:
            return [dict(self.dns_evidence[host]) for host in sorted(self.dns_evidence)]

    def request(self, host, method, path, headers):
        if method not in {"GET", "HEAD"}:
            raise ValueError("本次浏览只允许读取。")
        if not path.startswith("/") or path.startswith("//") or len(path) > 4096:
            raise ValueError("网页请求路径不合法。")
        self.url("https://" + host + path)
        if headers.get("Host", "").lower() not in {host, host + ":443"} or headers.get("Upgrade") or headers.get("Transfer-Encoding"):
            raise ValueError("网页请求目标或协议改变。")
        length = int(headers.get("Content-Length", "0"))
        if length != 0:
            raise ValueError("网页请求正文超出允许范围。")
        if any("\r" in k + v or "\n" in k + v for k, v in headers.items()):
            raise ValueError("请求头不能包含换行。")
        return {k: v for k, v in headers.items() if k.lower() in PUBLIC_REQUEST_HEADERS}, length


def tls_certificate(directory, hosts):
    """Use the OS crypto utility locally; its process cannot read home or use network."""
    safe_directory(directory.parent)
    directory.mkdir(mode=0o700)  # A fresh nonce directory, never an existing key destination.
    config, key, cert = (directory / name for name in ("request.cnf", "key.pem", "cert.pem"))
    config.write_text("[req]\nprompt=no\ndistinguished_name=dn\nx509_extensions=extensions\n"
        "[dn]\nCN=Curis public read proxy\n[extensions]\nsubjectAltName=" +
        ",".join("DNS:" + host_name(host) for host in sorted(hosts)) + "\n")
    profile = directory / "crypto.sb"
    profile.write_text("(version 1)\n(allow default)\n(deny network*)\n(deny file-read-data)\n"
        "(allow file-read-data (literal \"/\") (subpath \"/System\") (subpath \"/usr\") (literal \"/dev/urandom\")"
        " (literal \"/dev/random\") (literal \"/dev/null\") (subpath " + json.dumps(str(directory)) + "))\n"
        "(deny file-write*)\n(allow file-write* (subpath " + json.dumps(str(directory)) + ") (literal \"/dev/null\"))\n")
    command = ["/usr/bin/sandbox-exec", "-f", str(profile), "/usr/bin/openssl"]
    # LibreSSL loads its default configuration before processing the -config option.
    # Pin every command to this fresh owned config without opening system or user settings.
    environment = {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8", "OPENSSL_CONF": str(config)}
    try:
        subprocess.run([*command, "req", "-new", "-newkey", "rsa:2048", "-nodes", "-x509", "-days", "1",
            "-config", str(config), "-keyout", str(key), "-out", str(cert)], stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, cwd=directory, env=environment, check=True, timeout=10)
        key.chmod(0o600)
        public = subprocess.run([*command, "x509", "-in", str(cert), "-pubkey", "-noout"],
            capture_output=True, env=environment, cwd=directory, check=True, timeout=3).stdout
        der = subprocess.run([*command, "pkey", "-pubin", "-outform", "DER"], input=public,
            capture_output=True, env=environment, cwd=directory, check=True, timeout=3).stdout
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert, key)
        context.set_alpn_protocols(["http/1.1"])
        return context, base64.b64encode(hashlib.sha256(der).digest()).decode()
    except (subprocess.SubprocessError, OSError) as error:
        raise ValueError("无法创建独立浏览器的本地安全连接，浏览器尚未启动。请重试；若仍失败，请检查应用安装。") from error
    finally:
        key.unlink(missing_ok=True)  # Exact fresh task key, including failed initialization.



class PublicReadProxy:
    def __init__(self, directory, policy, *, alive=lambda: True, seconds=90, source_url=None):
        context, spki = tls_certificate(directory, policy.hosts)
        self._initialize(policy, alive, seconds, context, spki, ("127.0.0.1", 0), None, source_url=source_url)

    @classmethod
    def for_managed_runtime(cls, identity, nonce, policy, *, seconds=90):
        """Private candidate entry; only the fixed trusted owner can grant a listener.

        Owner must authenticate this proxy's actual network namespace/interface,
        the original browser peer, firewall and Work lifetime, not supplied JSON.
        The production owner factory remains closed. No caller-selected address,
        TLS material, callback or host wildcard is accepted by this entrypoint.
        """
        from .reader_vm_host import _open_verified_vm_owner
        required = {"tenant_id", "company_id", "work_ref", "task_id", "employee_id", "binding_ref"}
        if (type(identity) is not dict or set(identity) != required
                or any(type(v) is not str or not v for v in identity.values())
                or type(nonce) is not str or not re.fullmatch(r"[0-9a-f]{48}", nonce)):
            raise PermissionError("Proxy Work binding is invalid")
        fixed = identity.copy()
        owner = _open_verified_vm_owner(fixed.copy())
        def snapshot():
            raw = owner.verified_proxy_binding(fixed.copy(), nonce)
            keys = {"identity", "nonce", "boot_id", "container_id", "image_digest", "network_id",
                    "proxy_ip", "browser_ip", "port", "verified", "active"}
            if (type(raw) is not dict or set(raw) != keys or raw["identity"] != fixed or raw["nonce"] != nonce
                    or raw["verified"] is not True or raw["active"] is not True
                    or raw["proxy_ip"] != "172.30.253.2" or raw["browser_ip"] != "172.30.253.3"
                    or type(raw["port"]) is not int or raw["port"] != 8443
                    or any(type(raw[k]) is not str or not raw[k] for k in ("boot_id", "container_id", "image_digest", "network_id"))):
                raise PermissionError("Proxy private interface is not owner-verified")
            return {**raw, "identity": dict(raw["identity"])}
        bound = snapshot()
        def alive():
            return snapshot() == bound
        context, spki = owner.proxy_tls(fixed.copy(), nonce, dict(bound))
        if (not isinstance(context, ssl.SSLContext) or context.protocol != ssl.PROTOCOL_TLS_SERVER
                or type(spki) is not str or not re.fullmatch(r"[A-Za-z0-9+/]{43}=", spki) or not alive()):
            raise PermissionError("Proxy TLS or lifetime is not verified")
        result = cls.__new__(cls)
        result._initialize(policy, alive, seconds, context, spki, (bound["proxy_ip"], bound["port"]), bound["browser_ip"])
        try:
            result.check()
        except BaseException:
            result.close()
            raise
        return result

    def _initialize(self, policy, alive, seconds, context, spki, address, browser_ip, *, source_url=None):
        self.policy, self.alive = policy, alive
        self.deadline = time.monotonic() + min(seconds, 90)
        self.source_url = source_url
        if source_url is not None:
            policy.url(source_url)
        self.source_responses = []
        self.context, self.spki = context, spki
        self.sockets, self.lock, self.total_bytes = set(), threading.Lock(), 0
        self.permits = threading.BoundedSemaphore(8)
        owner = self
        class Handler(socketserver.BaseRequestHandler):
            def handle(self):
                if browser_ip is not None and self.client_address[0] != browser_ip:
                    return
                if not owner.permits.acquire(blocking=False):
                    return
                try:
                    owner.serve(self.request)
                except (ValueError, OSError, ssl.SSLError, http.client.HTTPException):
                    pass
                finally:
                    owner.permits.release()
        class Server(socketserver.ThreadingTCPServer):
            daemon_threads = True
            allow_reuse_address = False
        self.check()
        self.server = Server(address, Handler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.timer = threading.Timer(max(0, self.deadline - time.monotonic()), self.close)
        self.timer.daemon = True
        self.timer.start()

    def check(self):
        if time.monotonic() >= self.deadline or not self.alive():
            raise ValueError("原浏览器工作已停止。")

    def track(self, sock):
        with self.lock:
            self.sockets.add(sock)
        sock.settimeout(3)
        return sock

    @staticmethod
    def headers(stream):
        lines = []
        total = 0
        while True:
            line = stream.readline(8193)
            total += len(line)
            if not line or len(line) > 8192 or total > 32768:
                raise ValueError("请求头超出限制。")
            lines.append(line)
            if line == b"\r\n":
                break
        import io
        headers = http.client.parse_headers(io.BytesIO(b"".join(lines)))
        if len(headers.get_all("Host", [])) != 1 or len(headers.get_all("Content-Length", [])) > 1:
            raise ValueError("请求头目标不唯一。")
        return headers

    def serve(self, raw):
        self.track(raw)
        client = upstream = None
        try:
            self.check()
            stream = raw.makefile("rb", buffering=0)
            line = stream.readline(8193).decode("ascii").strip().split(" ")
            if len(line) != 3 or line[0] != "CONNECT" or line[2] != "HTTP/1.1":
                raise ValueError("只允许 TLS 连接。")
            host = self.policy.url("https://" + line[1] + "/")
            self.headers(stream)
            stream.close()
            raw.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
            client = self.track(self.context.wrap_socket(raw, server_side=True))
            stream = client.makefile("rb", buffering=0)
            request_line = stream.readline(8193).decode("ascii").strip().split(" ")
            if len(request_line) != 3 or request_line[2] != "HTTP/1.1":
                raise ValueError("只允许有界 HTTP/1.1 请求。")
            method, path, _ = request_line
            headers, length = self.policy.request(host, method, path, self.headers(stream))
            body = stream.read(length) if length else b""
            if len(body) != length:
                raise ValueError("请求正文不完整。")
            addresses = self.policy.resolve(host)
            self.check()
            family, kind, protocol, _, address = addresses[0]
            upstream = self.track(socket.socket(family, kind, protocol))
            upstream.connect(address)  # Connect the validated literal IP; never resolve it again.
            upstream = self.track(ssl.create_default_context(cafile=certifi.where()).wrap_socket(upstream, server_hostname=host))
            headers.update({"Host": host, "Connection": "close", "Content-Length": str(len(body)), "Cache-Control": "no-cache"})
            upstream.sendall((f"{method} {path} HTTP/1.1\r\n" + "".join(f"{k}: {v}\r\n" for k, v in headers.items()) + "\r\n").encode("latin1") + body)
            response = http.client.HTTPResponse(upstream, method=method)
            response.begin()
            if response.status in {401, 407}:
                raise ValueError("本次不进入需要账号验证的网站。")
            if response.getheader("Location"):
                self.policy.url(urljoin("https://" + host + path, response.getheader("Location")))
            payload = bytearray()
            while True:
                self.check()
                chunk = response.read(65536)
                if not chunk:
                    break
                payload.extend(chunk)
                with self.lock:
                    self.total_bytes += len(chunk)
                    if len(payload) > 8 * 1024 * 1024 or self.total_bytes > 32 * 1024 * 1024:
                        raise ValueError("网页数据超出本次上限。")
            fields = {k: v for k, v in response.getheaders() if k.lower() not in SENSITIVE_HEADERS | {"cache-control"}}
            fields.update({"Content-Length": str(len(payload)), "Connection": "close", "Cache-Control": "no-store"})
            self.check()
            client.sendall((f"HTTP/1.1 {response.status} {response.reason}\r\n" +
                "".join(f"{k}: {v}\r\n" for k, v in fields.items()) + "\r\n").encode("latin1") + payload)
            if "https://" + host + path == getattr(self, "source_url", None):
                with self.lock:
                    self.source_responses.append({"url": self.source_url, "host": host, "method": method,
                        "status": response.status, "bytes": len(payload), "body_sha256": hashlib.sha256(payload).hexdigest(),
                        "peer_ip": address[0], "validated_addresses": sorted({row[4][0] for row in addresses}),
                        "dns": self.policy.dns_snapshot(), "received_at_unix": time.time()})
        finally:
            for sock in (upstream, client, raw):
                if sock:
                    with self.lock:
                        self.sockets.discard(sock)
                    sock.close()

    def source_snapshot(self):
        with self.lock:
            return json.loads(json.dumps(self.source_responses))

    def close(self):
        if hasattr(self, "timer"):
            self.timer.cancel()
        self.deadline = 0
        with self.lock:
            connections = list(self.sockets)
        for connection in connections:
            try:
                connection.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            connection.close()
        if hasattr(self, "server"):
            self.server.shutdown()
            self.server.server_close()


