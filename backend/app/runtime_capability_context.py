from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator


_current_capability: ContextVar[dict[str, Any] | None] = ContextVar(
    "curis_runtime_capability", default=None
)


class RuntimeCapabilityContext:
    @staticmethod
    def current() -> dict[str, Any] | None:
        value = _current_capability.get()
        return dict(value) if value else None

    @staticmethod
    @contextmanager
    def scope(capability: dict[str, Any] | None) -> Iterator[None]:
        token = _current_capability.set(dict(capability) if capability else None)
        try:
            yield
        finally:
            _current_capability.reset(token)
