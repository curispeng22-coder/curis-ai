"""A5 统一响应契约测试。

验证：信封形状、分页计算、业务错误经由 handler 转成信封、未捕获异常转 500 信封。
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api import (
    ApiResponse,
    BusinessError,
    ConflictError,
    ErrorCode,
    NotFoundError,
    Page,
    fail,
    ok,
    paginate,
    register_exception_handlers,
)


def test_envelope_ok_shape() -> None:
    r = ok({"id": "1"}, message="done")
    assert isinstance(r, ApiResponse)
    assert r.code == 0
    assert r.message == "done"
    assert r.data == {"id": "1"}
    assert r.trace_id
    assert r.timestamp


def test_fail_envelope() -> None:
    r = fail(ErrorCode.NOT_FOUND, "没找到")
    assert r.code == ErrorCode.NOT_FOUND
    assert r.message == "没找到"
    assert r.data is None


def test_paginate_calculates_pages() -> None:
    p = paginate(items=[1, 2], total=25, page=2, page_size=10)
    assert isinstance(p, Page)
    assert p.total == 25
    assert p.page == 2
    assert p.page_size == 10
    assert p.pages == 3  # ceil(25/10)


def _build_app() -> FastAPI:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/ok")
    def _ok():
        return ok({"hello": "world"})

    @app.get("/notfound")
    def _nf():
        raise NotFoundError("资源不存在")

    @app.get("/conflict")
    def _cf():
        raise ConflictError("状态冲突")

    @app.get("/boom")
    def _boom():
        raise RuntimeError("意外")

    return app


def test_business_error_becomes_envelope() -> None:
    client = TestClient(_build_app())
    resp = client.get("/notfound")
    assert resp.status_code == 404
    body = resp.json()
    assert body["code"] == ErrorCode.NOT_FOUND
    assert body["message"] == "资源不存在"
    assert "trace_id" in body


def test_conflict_error_status_and_code() -> None:
    client = TestClient(_build_app())
    resp = client.get("/conflict")
    assert resp.status_code == 409
    assert resp.json()["code"] == ErrorCode.CONFLICT


def test_unexpected_exception_becomes_500_envelope() -> None:
    # raise_server_exceptions=False 才会把未捕获异常转成 500 信封，而不是在测试里重抛。
    client = TestClient(_build_app(), raise_server_exceptions=False)
    resp = client.get("/boom")
    assert resp.status_code == 500
    body = resp.json()
    assert body["code"] == ErrorCode.INTERNAL
    assert body["message"] == "服务器内部错误"


def test_ok_endpoint_returns_envelope() -> None:
    client = TestClient(_build_app())
    resp = client.get("/ok")
    assert resp.status_code == 200
    assert resp.json() == {
        "code": 0,
        "message": "ok",
        "data": {"hello": "world"},
        "trace_id": resp.json()["trace_id"],
        "timestamp": resp.json()["timestamp"],
    }
