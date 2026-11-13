from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator


_current_ceo: ContextVar[str | None] = ContextVar("curis_ceo", default=None)


class CeoContext:
    @staticmethod
    def current_ceo_id() -> str | None:
        return _current_ceo.get()

    @staticmethod
    @contextmanager
    def scope(ceo_id: str | None) -> Iterator[None]:
        token = _current_ceo.set(ceo_id or None)
        try:
            yield
        finally:
            _current_ceo.reset(token)

    @staticmethod
    def parse_ceo_from_request(request) -> str | None:
        headers = getattr(request, "headers", None)
        if headers is None:
            return None
        ceo_id = headers.get("X-Ceo-Id")
        return ceo_id or None
