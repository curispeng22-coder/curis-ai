"""social-auto-upload 发布桥接服务（Wave 2 · D2）。

把 Curis Connector（backend/app/connectors/social_auto_upload.py）的 HTTP 契约
`POST /api/publish {platform, account, cookie, package}` 翻译为 social-auto-upload
（github.com/dreammis/social-auto-upload，MIT，patchright）的 CLI 调用。

设计边界：
- 创始人 cookie 来自 Curis Vault，仅经本服务内存/临时文件使用，不落盘、不进提交。
- 不注册任何平台原生 OAuth App（cookie 登录即最小感知路径）。
- 本服务仅对内网暴露（docker compose 绑定 127.0.0.1:8090）。

启动：SAU_REPO=/app/social-auto-upload python publish_server.py
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


SAU_REPO = os.getenv("SAU_REPO", "/app/social-auto-upload")
# 发布命令模板（占位符：{platform} {account} {cookie_file} {package_file}）。
# 默认适配 dreammis/social-auto-upload 的 `python main.py <platform> ...` 形态；
# 若上游参数不同，改 SAU_PUBLISH_CMD 即可，无需改 Curis 侧代码。
SAU_PUBLISH_CMD = os.getenv(
    "SAU_PUBLISH_CMD",
    "python {repo}/main.py {platform} --account {account} --cookie {cookie_file} "
    "--publish {package_file}",
)


def _run(platform: str, account: str, cookie: str, package: dict) -> dict:
    """调用 social-auto-upload CLI；返回与 connector 契约一致的回执。"""
    with tempfile.NamedTemporaryFile("w", suffix=".ck", delete=False) as cf:
        cf.write(cookie or "")
        cookie_file = cf.name
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as pf:
        json.dump(package, pf, ensure_ascii=False)
        package_file = pf.name
    try:
        cmd = SAU_PUBLISH_CMD.format(
            repo=SAU_REPO, platform=platform, account=account,
            cookie_file=cookie_file, package_file=package_file,
        )
        proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
        ok = proc.returncode == 0
        return {
            "status": "published" if ok else "failed",
            "platform": platform,
            "post_id": "" if not ok else f"{platform}-{abs(hash(package.get('package_id','')) % 10**8)}",
            "message": (proc.stdout or proc.stderr or "")[:500],
        }
    except Exception as error:  # noqa: BLE001
        return {"status": "failed", "platform": platform, "post_id": "", "message": str(error)[:500}
    finally:
        for f in (cookie_file, package_file):
            try:
                os.unlink(f)
            except OSError:
                pass


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok"})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        if self.path != "/api/publish":
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._send(422, {"error": "invalid json"})
            return
        platform = data.get("platform", "")
        account = data.get("account", "founder")
        cookie = data.get("cookie", "")
        package = data.get("package", {})
        if not platform:
            self._send(422, {"error": "platform required"})
            return
        self._send(200, _run(platform, account, cookie, package))

    def log_message(self, *args):  # 静默访问日志
        return


def main() -> None:
    port = int(os.getenv("SAU_PORT", "8090"))
    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"[social-auto-upload bridge] listening on :{port} (repo={SAU_REPO})")
    server.serve_forever()


if __name__ == "__main__":
    main()
