"""Curis Business Runtime —— 事件总线（A3）与异步化契约（A4）。

A3 事件总线：状态流转与关键业务节点发出领域事件，订阅方（CEO 桌面通知、
经营账更新、归因采集）解耦消费，不回写状态机。

A4 异步化契约：运行执行不在 HTTP 请求链路内发生。调度器在后台 worker 线程
跑 ``run_once()``；API 层只做「落库节奏 / 人工处置」这类快操作，执行由 worker
异步完成。本模块只定义事件与总线；调度器在 ``scheduler.py`` 中发布事件。
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class BusinessEvent:
    type: str
    entity_type: str
    entity_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    at: str = ""


class EventBus:
    """极简进程内发布/订阅总线（A3）。

    订阅按事件 ``type`` 精确匹配；``"*"`` 订阅全部。handler 同步执行。
    跨进程 / 持久化分发是后续阶段职责——A3 只求进程内解耦，让「通知」与
    「状态机」脱钩。
    """

    def __init__(self) -> None:
        self._subs: dict[str, list[Callable[[BusinessEvent], None]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, event_type: str, handler: Callable[[BusinessEvent], None]) -> None:
        with self._lock:
            self._subs.setdefault(event_type, []).append(handler)

    def publish(self, event: BusinessEvent) -> None:
        with self._lock:
            handlers = list(self._subs.get(event.type, [])) + list(self._subs.get("*", []))
        for handler in handlers:
            handler(event)
