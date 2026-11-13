"""issue_pipeline 模块单元测试。

覆盖：
- NLParser（无网关兜底 + JSON 解析 + 模型输出解析）
- IssueQueue（入队/出队/更新/列表/排序/并发安全）
- ResultReviewer（通过/失败/返工/升级）
- PipelineDispatcher（dispatch + 审查 + 返工循环）
- submit_natural_language 便利函数
- issue_pipeline_api 端点

运行：``cd backend && python -m pytest tests/test_issue_pipeline.py -v``
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from datetime import datetime, timezone
from typing import Any
from unittest import mock

from app.issue_pipeline import (
    NLParser,
    IssueQueue,
    PipelineDispatcher,
    PipelineTask,
    ResultReviewer,
    submit_natural_language,
)
from app.issue_pipeline_api import pipeline_router
from fastapi.testclient import TestClient
from fastapi import FastAPI


# ---------------------------------------------------------------------------
# 测试辅助
# ---------------------------------------------------------------------------


def _make_task(**overrides: Any) -> PipelineTask:
    defaults = {
        "id": "test-task-1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "natural_language": "把 target_a.py 的 BETA 改成 3",
        "issue_spec": {
            "issue_id": "test-task-1",
            "target_file": "tools/real_rd_fixture/target_a.py",
            "issue": "把 target_a.py 的 BETA 改成 3",
            "expected_test": "backend/tests/test_real_rd_fixture_a.py",
            "max_rounds": 3,
        },
        "status": "pending",
    }
    defaults.update(overrides)
    return PipelineTask(**defaults)


def _make_queue(db_path: str | None = None) -> IssueQueue:
    if db_path is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        tmp.close()
        db_path = tmp.name
    return IssueQueue(db_path=db_path)


def _cleanup_queue(queue: IssueQueue) -> None:
    try:
        if os.path.exists(queue._db_path):
            os.unlink(queue._db_path)
    except Exception:
        pass


# ===========================================================================
# NLParser 测试
# ===========================================================================


class TestNLParser(unittest.TestCase):
    """NLParser 单元测试。"""

    def test_default_spec_without_gateway(self) -> None:
        """无模型网关时应返回默认 spec。"""
        parser = NLParser(model_gateway=None)
        spec = parser.parse("把 BETA 改成 3")
        self.assertEqual(spec["target_file"], "tools/real_rd_fixture/target_a.py")
        self.assertEqual(spec["expected_test"], "backend/tests/test_real_rd_fixture_a.py")
        self.assertIn("BETA", spec["issue"])
        self.assertIn("task-", spec["issue_id"])
        self.assertEqual(spec["max_rounds"], 3)

    def test_parse_json_output_json_block(self) -> None:
        """解析 ```json ... ``` 围栏内的 JSON。"""
        text = '```json\n{"issue_id": "task-abc", "target_file": "x.py"}\n```'
        result = NLParser._parse_json_output(text)
        self.assertEqual(result["issue_id"], "task-abc")
        self.assertEqual(result["target_file"], "x.py")

    def test_parse_json_output_raw_json(self) -> None:
        """解析裸 JSON 文本。"""
        text = '{"issue_id": "task-xyz", "target_file": "y.py"}'
        result = NLParser._parse_json_output(text)
        self.assertEqual(result["issue_id"], "task-xyz")
        self.assertEqual(result["target_file"], "y.py")

    def test_parse_json_output_brace_fallback(self) -> None:
        """找首个 { 并尝试解析。"""
        text = "some random text\n{\"a\": 1}\nmore text"
        result = NLParser._parse_json_output(text)
        self.assertEqual(result["a"], 1)

    def test_parse_json_output_empty(self) -> None:
        """空字符串返回空 dict。"""
        result = NLParser._parse_json_output("no json here")
        self.assertEqual(result, {})

    def test_parse_json_output_plain_code_block(self) -> None:
        """解析 ``` ... ``` 围栏（非 json 标记）。"""
        text = '```\n{"key": "value"}\n```'
        result = NLParser._parse_json_output(text)
        self.assertEqual(result["key"], "value")

    def test_parse_with_gateway(self) -> None:
        """通过 mock 模型网关解析。"""
        mock_gw = mock.MagicMock()
        mock_gw.execute.return_value = {
            "output": '{"issue_id": "task-custom", "target_file": "src/test.py"}',
        }
        parser = NLParser(model_gateway=mock_gw)
        spec = parser.parse("fix the bug")
        self.assertEqual(spec["issue_id"], "task-custom")
        self.assertEqual(spec["target_file"], "src/test.py")

    def test_parse_with_gateway_fallback_on_error(self) -> None:
        """模型网关报错时降级为默认 spec。"""
        mock_gw = mock.MagicMock()
        mock_gw.execute.side_effect = RuntimeError("gateway down")
        parser = NLParser(model_gateway=mock_gw)
        spec = parser.parse("fix this")
        self.assertEqual(spec["target_file"], "tools/real_rd_fixture/target_a.py")


# ===========================================================================
# IssueQueue 测试
# ===========================================================================


class TestIssueQueue(unittest.TestCase):
    """IssueQueue 单元测试。"""

    def setUp(self) -> None:
        self.queue = _make_queue()

    def tearDown(self) -> None:
        _cleanup_queue(self.queue)

    def test_enqueue_and_get(self) -> None:
        """入队后能通过 get 取出。"""
        task = _make_task()
        self.queue.enqueue(task)
        retrieved = self.queue.get(task.id)
        self.assertIsNotNone(retrieved)
        assert retrieved is not None
        self.assertEqual(retrieved.id, task.id)
        self.assertEqual(retrieved.natural_language, task.natural_language)
        self.assertEqual(retrieved.status, "pending")
        self.assertEqual(retrieved.issue_spec, task.issue_spec)

    def test_get_nonexistent(self) -> None:
        """不存在的 id 返回 None。"""
        self.assertIsNone(self.queue.get("nonexistent"))

    def test_dequeue_returns_pending(self) -> None:
        """dequeue 返回 pending 任务并标记为 queued。"""
        task = _make_task()
        self.queue.enqueue(task)
        dequeued = self.queue.dequeue()
        self.assertIsNotNone(dequeued)
        assert dequeued is not None
        self.assertEqual(dequeued.id, task.id)
        self.assertEqual(dequeued.status, "queued")
        self.assertIsNotNone(dequeued.queued_at)
        # 第二次 dequeue 应为 None
        self.assertIsNone(self.queue.dequeue())

    def test_dequeue_order(self) -> None:
        """dequeue 按 created_at ASC 排序。"""
        t1 = _make_task(id="task-1", natural_language="first")
        t2 = _make_task(id="task-2", natural_language="second")
        self.queue.enqueue(t1)
        self.queue.enqueue(t2)
        first = self.queue.dequeue()
        self.assertIsNotNone(first)
        assert first is not None
        self.assertEqual(first.id, "task-1")

    def test_update_status(self) -> None:
        """update_status 更新指定字段。"""
        task = _make_task()
        self.queue.enqueue(task)
        self.queue.update_status(
            task.id,
            status="running",
            started_at="2025-01-01T00:00:00Z",
        )
        retrieved = self.queue.get(task.id)
        assert retrieved is not None
        self.assertEqual(retrieved.status, "running")
        self.assertEqual(retrieved.started_at, "2025-01-01T00:00:00Z")

    def test_update_status_executor_result(self) -> None:
        """update_status 更新 executor_result（JSON 序列化）。"""
        task = _make_task()
        self.queue.enqueue(task)
        result = {
            "status": "succeeded",
            "rounds": 1,
            "diff_text": "--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-old\n+new\n",
            "test_exit_code": 0,
        }
        self.queue.update_status(task.id, executor_result=result)
        retrieved = self.queue.get(task.id)
        assert retrieved is not None
        self.assertEqual(retrieved.executor_result, result)

    def test_update_status_rework_feedback(self) -> None:
        """update_status 更新 rework_feedback（JSON 列表）。"""
        task = _make_task()
        self.queue.enqueue(task)
        feedback = ["测试失败（exit_code=1）"]
        self.queue.update_status(task.id, rework_feedback=feedback, rework_count=1)
        retrieved = self.queue.get(task.id)
        assert retrieved is not None
        self.assertEqual(retrieved.rework_feedback, feedback)
        self.assertEqual(retrieved.rework_count, 1)

    def test_list_all(self) -> None:
        """list_all 返回所有任务。"""
        self.queue.enqueue(_make_task(id="t1"))
        self.queue.enqueue(_make_task(id="t2"))
        tasks = self.queue.list_all()
        self.assertEqual(len(tasks), 2)
        # 按 created_at DESC 排序
        self.assertIn(tasks[0].id, ("t1", "t2"))

    def test_list_pending(self) -> None:
        """list_pending 仅返回 pending/queued 状态的任务。"""
        self.queue.enqueue(_make_task(id="t1"))
        t2 = _make_task(id="t2")
        self.queue.enqueue(t2)
        self.queue.update_status("t2", status="running")
        pending = self.queue.list_pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].id, "t1")

    def test_enqueue_with_none_fields(self) -> None:
        """issue_spec/executor_result 为 None 时正常入队。"""
        task = PipelineTask(
            id="test-minimal",
            created_at=datetime.now(timezone.utc).isoformat(),
            natural_language="minimal test",
        )
        self.queue.enqueue(task)
        retrieved = self.queue.get(task.id)
        assert retrieved is not None
        self.assertIsNone(retrieved.issue_spec)
        self.assertIsNone(retrieved.executor_result)

    def test_sqlite_lock_concurrent(self) -> None:
        """多个操作不应死锁。"""
        for i in range(5):
            t = _make_task(id=f"concurrent-{i}")
            self.queue.enqueue(t)
        tasks = self.queue.list_all()
        self.assertEqual(len(tasks), 5)


# ===========================================================================
# ResultReviewer 测试
# ===========================================================================


class TestResultReviewer(unittest.TestCase):
    """ResultReviewer 单元测试。"""

    def setUp(self) -> None:
        self.reviewer = ResultReviewer()
        self.good_diff = (
            "--- a/tools/real_rd_fixture/target_a.py\n"
            "+++ b/tools/real_rd_fixture/target_a.py\n"
            "@@ -1,5 +1,5 @@\n"
            " ALPHA = 1\n"
            "-BETA = 2\n"
            "+BETA = 3\n"
        )

    def test_passes_with_good_result(self) -> None:
        """test_exit_code=0 + 有效 diff → passes=True。"""
        task = _make_task(
            executor_result={
                "status": "succeeded",
                "rounds": 1,
                "diff_text": self.good_diff,
                "test_exit_code": 0,
            },
        )
        result = self.reviewer.review(task)
        self.assertTrue(result["passes"])
        self.assertFalse(result["needs_rework"])
        self.assertFalse(result["escalated"])
        self.assertEqual(result["feedback"], [])

    def test_needs_rework_on_test_failure(self) -> None:
        """test_exit_code=1 → needs_rework=True。"""
        task = _make_task(
            executor_result={
                "status": "failed",
                "rounds": 3,
                "diff_text": "",
                "test_exit_code": 1,
            },
        )
        result = self.reviewer.review(task)
        self.assertFalse(result["passes"])
        self.assertTrue(result["needs_rework"])
        self.assertIn("exit_code=1", result["feedback"][0])

    def test_needs_rework_on_no_diff(self) -> None:
        """无有效 diff → needs_rework=True。"""
        task = _make_task(
            executor_result={
                "status": "failed",
                "rounds": 1,
                "diff_text": "",
                "test_exit_code": 0,
            },
        )
        result = self.reviewer.review(task)
        self.assertFalse(result["passes"])
        self.assertIn("有效 diff", result["feedback"][0])

    def test_needs_rework_on_no_test_exit(self) -> None:
        """test_exit_code=None → needs_rework=True。"""
        task = _make_task(
            executor_result={
                "status": "error",
                "rounds": 0,
                "diff_text": "",
                "test_exit_code": None,
            },
        )
        result = self.reviewer.review(task)
        self.assertFalse(result["passes"])
        self.assertIn("未执行", result["feedback"][0])

    def test_escalated_after_two_reworks(self) -> None:
        """rework_count >= 2 → escalated=True。"""
        task = _make_task(
            rework_count=2,
            executor_result={
                "status": "failed",
                "rounds": 3,
                "diff_text": "",
                "test_exit_code": 1,
            },
        )
        result = self.reviewer.review(task)
        self.assertTrue(result["escalated"])

    def test_escalated_after_three_reworks(self) -> None:
        """rework_count > 2 也 escalated。"""
        task = _make_task(
            rework_count=5,
            executor_result={
                "status": "failed",
                "rounds": 3,
                "diff_text": "",
                "test_exit_code": 1,
            },
        )
        result = self.reviewer.review(task)
        self.assertTrue(result["escalated"])


# ===========================================================================
# PipelineDispatcher 测试
# ===========================================================================


class TestPipelineDispatcher(unittest.TestCase):
    """PipelineDispatcher 单元测试。"""

    def test_dispatch_nonexistent_raises(self) -> None:
        """不存在的 task_id → ValueError。"""
        dispatcher = PipelineDispatcher()
        with self.assertRaises(ValueError):
            dispatcher.dispatch_one("nonexistent")

    def test_dispatch_success_to_review(self) -> None:
        """执行成功 → status 变成 review。"""
        queue = _make_queue()
        try:
            task = _make_task()
            queue.enqueue(task)
            dispatcher = PipelineDispatcher(queue=queue)

            with mock.patch.object(dispatcher, "_make_executor") as mock_maker:
                fake_executor = mock.MagicMock()
                fake_executor.run.return_value = {
                    "issue_id": "test-task-1",
                    "status": "succeeded",
                    "rounds": 1,
                    "diff_text": "--- a/x.py\n+++ b/x.py\n@@ -1 +1 @@\n-old\n+new\n",
                    "test_exit_code": 0,
                    "files": [],
                    "total_tokens": 0,
                    "estimated_cost": 0.0,
                    "audit_event_count": 0,
                    "model_gateway_id": "mock",
                    "model_name": "mock",
                }
                mock_maker.return_value = fake_executor
                updated = dispatcher.dispatch_one(task.id)

            self.assertEqual(updated.status, "review")
            self.assertIsNotNone(updated.executor_result)
            assert updated.executor_result is not None
            self.assertEqual(updated.executor_result["test_exit_code"], 0)
        finally:
            _cleanup_queue(queue)

    def test_dispatch_failure_triggers_rework(self) -> None:
        """执行失败（test_exit_code=1）→ 触发返工（status=pending, rework_count=1）。"""
        queue = _make_queue()
        try:
            task = _make_task()
            queue.enqueue(task)
            dispatcher = PipelineDispatcher(queue=queue)

            with mock.patch.object(dispatcher, "_make_executor") as mock_maker:
                fake_executor = mock.MagicMock()
                fake_executor.run.return_value = {
                    "issue_id": "test-task-1",
                    "status": "failed",
                    "rounds": 3,
                    "diff_text": "",
                    "test_exit_code": 1,
                    "files": [],
                    "total_tokens": 0,
                    "estimated_cost": 0.0,
                    "audit_event_count": 0,
                    "model_gateway_id": "mock",
                    "model_name": "mock",
                }
                mock_maker.return_value = fake_executor
                updated = dispatcher.dispatch_one(task.id)

            self.assertEqual(updated.status, "pending")  # 重新排队
            self.assertEqual(updated.rework_count, 1)
            self.assertTrue(len(updated.rework_feedback) > 0)
        finally:
            _cleanup_queue(queue)

    def test_dispatch_exception_handling(self) -> None:
        """executor.run 抛异常 → 优雅降级。"""
        queue = _make_queue()
        try:
            task = _make_task()
            queue.enqueue(task)
            dispatcher = PipelineDispatcher(queue=queue)

            with mock.patch.object(dispatcher, "_make_executor") as mock_maker:
                fake_executor = mock.MagicMock()
                fake_executor.run.side_effect = RuntimeError("execution failed")
                mock_maker.return_value = fake_executor
                updated = dispatcher.dispatch_one(task.id)

            # 异常应被捕获，status 变为 pending（返工）
            self.assertIn(updated.status, ("pending", "failed"))
        finally:
            _cleanup_queue(queue)

    def test_dispatch_triggers_escalation(self) -> None:
        """rework_count >= 2 时触发升级（status=failed）。"""
        queue = _make_queue()
        try:
            task = _make_task(
                rework_count=2,
                rework_feedback=["之前失败"],
            )
            queue.enqueue(task)
            dispatcher = PipelineDispatcher(queue=queue)

            with mock.patch.object(dispatcher, "_make_executor") as mock_maker:
                fake_executor = mock.MagicMock()
                fake_executor.run.return_value = {
                    "issue_id": "test-task-1",
                    "status": "failed",
                    "rounds": 1,
                    "diff_text": "",
                    "test_exit_code": 1,
                    "files": [],
                    "total_tokens": 0,
                    "estimated_cost": 0.0,
                    "audit_event_count": 0,
                    "model_gateway_id": "mock",
                    "model_name": "mock",
                }
                mock_maker.return_value = fake_executor
                updated = dispatcher.dispatch_one(task.id)

            self.assertEqual(updated.status, "failed")
        finally:
            _cleanup_queue(queue)

    def test_to_executor_spec_defaults(self) -> None:
        """_to_executor_spec 生成正确的 executor 格式。"""
        dispatcher = PipelineDispatcher()
        spec = dispatcher._to_executor_spec({
            "issue_id": "test-123",
            "target_file": "tools/real_rd_fixture/target_a.py",
            "issue": "modify BETA",
            "expected_test": "backend/tests/test_real_rd_fixture_a.py",
            "max_rounds": 5,
        })
        self.assertEqual(spec["issue_id"], "test-123")
        self.assertEqual(spec["target_files"], ["tools/real_rd_fixture/target_a.py"])
        self.assertEqual(spec["test_command_id"], "rd_verify")
        self.assertEqual(spec["test_command_argv"], ["pytest", "backend/tests/test_real_rd_fixture_a.py"])
        self.assertEqual(spec["instructions"], "modify BETA")
        self.assertEqual(spec["max_rounds"], 5)


# ===========================================================================
# submit_natural_language 测试
# ===========================================================================


class TestSubmitNaturalLanguage(unittest.TestCase):
    """submit_natural_language 便利函数测试。"""

    def test_submit_creates_pending_task(self) -> None:
        """提交后获得 pending 状态任务。"""
        queue = _make_queue()
        try:
            parser = NLParser(model_gateway=None)
            task = submit_natural_language(
                "把 BETA 改成 3",
                queue=queue,
                parser=parser,
            )
            self.assertEqual(task.status, "pending")
            self.assertEqual(task.natural_language, "把 BETA 改成 3")

            retrieved = queue.get(task.id)
            self.assertIsNotNone(retrieved)
            assert retrieved is not None
            self.assertEqual(retrieved.status, "pending")
        finally:
            _cleanup_queue(queue)


# ===========================================================================
# issue_pipeline_api 端点集成测试
# ===========================================================================


class TestPipelineAPI(unittest.TestCase):
    """issue_pipeline_api FastAPI 端点集成测试。"""

    def setUp(self) -> None:
        app = FastAPI()
        app.include_router(pipeline_router)
        self.client = TestClient(app)

    def test_submit_endpoint(self) -> None:
        """POST /api/pipeline/submit → 返回 {id, status}。"""
        resp = self.client.post("/api/pipeline/submit", json={"natural_language": "测试任务"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["status"], "pending")

    def test_submit_missing_field(self) -> None:
        """POST /api/pipeline/submit 缺少字段 → 422。"""
        resp = self.client.post("/api/pipeline/submit", json={})
        self.assertEqual(resp.status_code, 422)

    def test_list_endpoint(self) -> None:
        """GET /api/pipeline/list → 返回列表。"""
        self.client.post("/api/pipeline/submit", json={"natural_language": "任务1"})
        self.client.post("/api/pipeline/submit", json={"natural_language": "任务2"})
        resp = self.client.get("/api/pipeline/list")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

    def test_get_endpoint(self) -> None:
        """GET /api/pipeline/{id} → 返回任务详情。"""
        submit_resp = self.client.post(
            "/api/pipeline/submit", json={"natural_language": "测试详情"}
        )
        task_id = submit_resp.json()["id"]
        resp = self.client.get(f"/api/pipeline/{task_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["id"], task_id)
        self.assertIn("natural_language", data)

    def test_get_endpoint_not_found(self) -> None:
        """GET /api/pipeline/{id} 不存在 → 404。"""
        resp = self.client.get("/api/pipeline/nonexistent")
        self.assertEqual(resp.status_code, 404)

    def test_dispatch_endpoint_not_pending(self) -> None:
        """POST /api/pipeline/{id}/dispatch 对不存在任务 → 404。"""
        resp = self.client.post("/api/pipeline/nonexistent/dispatch")
        self.assertEqual(resp.status_code, 404)

    def test_approve_endpoint(self) -> None:
        """POST /api/pipeline/{id}/approve → 对非 review 状态报错。"""
        submit_resp = self.client.post(
            "/api/pipeline/submit", json={"natural_language": "测试审批"}
        )
        task_id = submit_resp.json()["id"]
        resp = self.client.post(f"/api/pipeline/{task_id}/approve")
        self.assertEqual(resp.status_code, 400)  # 非 review 状态不能审批

    def test_reject_endpoint(self) -> None:
        """POST /api/pipeline/{id}/reject → 对非 review 状态报错。"""
        submit_resp = self.client.post(
            "/api/pipeline/submit", json={"natural_language": "测试打回"}
        )
        task_id = submit_resp.json()["id"]
        resp = self.client.post(
            f"/api/pipeline/{task_id}/reject", json={"note": "需要修改"}
        )
        self.assertEqual(resp.status_code, 400)

    def test_rework_endpoint(self) -> None:
        """POST /api/pipeline/{id}/rework → 触发返工排队。"""
        submit_resp = self.client.post(
            "/api/pipeline/submit", json={"natural_language": "测试返工"}
        )
        task_id = submit_resp.json()["id"]
        resp = self.client.post(f"/api/pipeline/{task_id}/rework")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "pending")


if __name__ == "__main__":
    unittest.main()
