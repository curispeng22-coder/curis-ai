import os
import sys
import traceback

if len(sys.argv) > 1 and sys.argv[1] == "--curis-browser-supervisor":
    if len(sys.argv) != 2:
        raise SystemExit(2)
    if not getattr(sys, "frozen", False):
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from backend.app.agent_browser_runtime import run_browser_supervisor
    raise SystemExit(run_browser_supervisor())

if len(sys.argv) > 1 and sys.argv[1] == "--curis-agent-supervisor":
    if not getattr(sys, "frozen", False):
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from backend.app.agent_adapter import run_agent_supervisor
    raise SystemExit(run_agent_supervisor())

if len(sys.argv) > 1 and sys.argv[1] == "--curis-runtime-self-check":
    if len(sys.argv) != 2:
        raise SystemExit(2)
    # Fixed offline packaging diagnostic; never import the product or open its DB.
    import ctypes
    import json
    from pathlib import Path
    import ssl
    import sqlite3
    import _ssl
    import _sqlite3
    root = Path(sys._MEIPASS).resolve()
    assert getattr(sys, "frozen", False)
    assert all(Path(module.__file__).resolve().is_relative_to(root) for module in (_ssl, _sqlite3))
    with sqlite3.connect(":memory:") as connection:
        assert connection.execute("select 1").fetchone() == (1,)
    connection.close()
    library = ctypes.CDLL("/usr/lib/libSystem.B.dylib")
    class DlInfo(ctypes.Structure):
        _fields_ = [("filename", ctypes.c_char_p), ("base", ctypes.c_void_p),
                    ("symbol", ctypes.c_char_p), ("address", ctypes.c_void_p)]
    library.dladdr.argtypes = [ctypes.c_void_p, ctypes.POINTER(DlInfo)]
    library.dladdr.restype = ctypes.c_int
    loaded = {}
    for module, symbol, expected in [(_ssl, "SSL_version", "libssl.3.dylib"),
            (_ssl, "OpenSSL_version", "libcrypto.3.dylib"),
            (_sqlite3, "sqlite3_libversion", "libsqlite3.dylib")]:
        handle = ctypes.CDLL(module.__file__)
        address = ctypes.cast(getattr(handle, symbol), ctypes.c_void_p)
        info = DlInfo()
        assert library.dladdr(address, ctypes.byref(info)) and info.filename
        path = Path(os.fsdecode(info.filename)).resolve()
        assert path.name == expected and path.is_relative_to(root)
        loaded[expected] = str(path)
    import asyncio
    import threading
    import secrets
    import httpx
    import anyio
    import uvicorn
    from fastapi import FastAPI
    from anyio._core._eventloop import get_async_backend
    async def asgi_probe():
        fixture = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
        nonce = secrets.token_hex(16)
        event_loop_thread = threading.get_ident()
        observed = {"middleware": 0, "sync_worker": False}
        @fixture.middleware("http")
        async def probe_middleware(request, call_next):
            observed["middleware"] += 1
            response = await call_next(request)
            response.headers["X-Curis-Selfcheck"] = "isolated-asgi"
            return response
        @fixture.get("/packaging-probe")
        def probe_route():
            observed["sync_worker"] = threading.get_ident() != event_loop_thread
            return {"nonce": nonce, "scope": "synthetic-only"}
        transport = httpx.ASGITransport(app=fixture, raise_app_exceptions=True)
        async with httpx.AsyncClient(transport=transport, base_url="http://asgi-selfcheck.invalid", trust_env=False) as client:
            response = await client.get("/packaging-probe")
        assert response.status_code == 200
        assert response.json() == {"nonce": nonce, "scope": "synthetic-only"}
        assert response.headers["X-Curis-Selfcheck"] == "isolated-asgi"
        assert observed == {"middleware": 1, "sync_worker": True}
        backend = get_async_backend()
        assert backend.__module__ == "anyio._backends._asyncio"
        module = sys.modules[backend.__module__]
        assert Path(module.__file__).resolve().is_relative_to(root)
        assert "backend.app.main" not in sys.modules
        return {"status": 200, "response_verified": True, "middleware_taskgroup": True,
            "sync_route_worker_thread": True, "anyio_backend": backend.__module__,
            "backend_module": module.__file__, "uvicorn_version": uvicorn.__version__,
            "transport": "HTTPX ASGITransport, no network socket", "business_app_imported": False}
    asgi = asyncio.run(asgi_probe())
    print(json.dumps({"status": "PASS", "frozen": True, "ssl_version": ssl.OPENSSL_VERSION,
        "sqlite_version": sqlite3.sqlite_version, "native_modules": {"_ssl": _ssl.__file__, "_sqlite3": _sqlite3.__file__},
        "bundled_libraries": loaded, "database": ":memory:", "product_imported": False,
        "provider_invoked": False, "asgi": asgi}, sort_keys=True))
    raise SystemExit(0)

try:
    import uvicorn
    from backend.app.main import app
except Exception:
    traceback.print_exc()
    raise


uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("CURIS_WORKSPACE_PORT", "8002")))
