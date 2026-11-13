#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SmokeConfig:
    base_url: str
    task_content: str
    timeout: float


def main() -> int:
    config = _parse_args()

    try:
        health = _request_json("GET", f"{config.base_url}/health", timeout=config.timeout)
        _require(health.get("status") == "ok", "health response must include status=ok")

        created = _request_json(
            "POST",
            f"{config.base_url}/api/task",
            payload={"content": config.task_content},
            timeout=config.timeout,
        )
        task_id = created.get("task_id")
        _require(isinstance(task_id, str) and bool(task_id), "task creation response must include task_id")
        _require(created.get("status") == "created", "task creation response must include status=created")

        tasks = _request_json("GET", f"{config.base_url}/api/tasks", timeout=config.timeout)
        _require(isinstance(tasks, list), "task history response must be a list")
        _require(any(task.get("task_id") == task_id for task in tasks if isinstance(task, dict)), "created task must appear in task history")
    except SmokeFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print("PASS: local/demo API smoke completed")
    print(json.dumps({"base_url": config.base_url, "task_id": task_id, "checks": ["health", "task_create", "task_history"]}, ensure_ascii=False))
    return 0


def _parse_args() -> SmokeConfig:
    parser = argparse.ArgumentParser(description="Run local/demo smoke checks against the existing Curis API.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Local Curis API base URL.")
    parser.add_argument("--task-content", default="本地演示验证任务", help="Task content for the smoke-created task.")
    parser.add_argument("--timeout", type=float, default=5.0, help="HTTP timeout in seconds.")
    args = parser.parse_args()

    return SmokeConfig(
        base_url=args.base_url.rstrip("/"),
        task_content=args.task_content,
        timeout=args.timeout,
    )


def _request_json(method: str, url: str, *, payload: dict[str, Any] | None = None, timeout: float) -> Any:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            if not 200 <= response.status < 300:
                raise SmokeFailure(f"{method} {url} returned HTTP {response.status}")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise SmokeFailure(f"{method} {url} returned HTTP {error.code}: {body}") from error
    except urllib.error.URLError as error:
        raise SmokeFailure(f"{method} {url} failed: {error.reason}") from error
    except TimeoutError as error:
        raise SmokeFailure(f"{method} {url} timed out") from error

    try:
        return json.loads(body)
    except json.JSONDecodeError as error:
        raise SmokeFailure(f"{method} {url} did not return JSON: {body}") from error


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SmokeFailure(message)


class SmokeFailure(RuntimeError):
    pass


if __name__ == "__main__":
    raise SystemExit(main())
