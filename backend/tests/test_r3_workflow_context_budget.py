from __future__ import annotations

import copy
import hashlib

import pytest

from app.model_gateway import R3_WORKFLOW_CONTEXT_MAX_BYTES
from app.workflow_runtime import WorkflowRuntime


class TaskStore:
    def __init__(self, content: str = "Build the approved R3 delivery") -> None:
        self.content = content

    def get_task(self, task_id: str) -> dict[str, str]:
        return {"task_id": task_id, "content": self.content}


def runtime(content: str = "Build the approved R3 delivery") -> WorkflowRuntime:
    instance = object.__new__(WorkflowRuntime)
    instance.store = TaskStore(content)
    return instance


def step(order: int, *, status: str = "succeeded") -> dict[str, object]:
    return {
        "workflow_step_id": f"step-{order}",
        "step_order": order,
        "step_type": f"type_{order}",
        "step_name": f"Step {order}",
        "employee_role": f"role_{order}",
        "status": status,
    }


def result(order: int, value: object) -> dict[str, object]:
    return {
        "step_result_id": f"result-{order}",
        "workflow_step_id": f"step-{order}",
        "result": value,
        "status": "succeeded",
    }


def run_with_history(values: list[object]) -> tuple[dict[str, object], dict[str, object]]:
    steps = [step(order) for order in range(1, len(values) + 1)]
    current = step(len(values) + 1, status="pending")
    steps.append(current)
    run = {
        "workflow_run_id": "run-approved",
        "task_id": "task-approved",
        "steps": steps,
        "step_results": [result(order, value) for order, value in enumerate(values, 1)],
    }
    return run, current


def test_step_six_context_is_deterministic_bounded_traceable_and_immutable():
    values = [f"BODY-{order}-" + ("研发结果" * 2_000) for order in range(1, 6)]
    run, current = run_with_history(values)
    original = copy.deepcopy(run)
    builder = runtime("目标" * 2_000)

    first = builder._build_step_input(run, current)
    second = builder._build_step_input(run, current)

    assert first == second
    assert len(first.encode("utf-8")) <= R3_WORKFLOW_CONTEXT_MAX_BYTES
    assert first.encode("utf-8").decode("utf-8") == first
    assert "[TRUNCATED:current_requirement]" in first
    for order, value in enumerate(values, 1):
        assert f"step_result_id=result-{order}" in first
        assert f"order={order}" in first
        assert f"step_type=type_{order}" in first
        assert "status=succeeded" in first
        assert hashlib.sha256(value.encode("utf-8")).hexdigest() in first
        assert f"ref=step_results/result-{order}" in first
    assert first.index("[step_result:result-5]") < first.index("[step_result:result-4]")
    assert "BODY-5-" in first
    assert "BODY-4-" in first
    assert "[TRUNCATED:step_result:" in first
    assert run == original


def test_context_handles_empty_and_multibyte_content():
    values = ["", "测", "界" * 4_000]
    run, current = run_with_history(values)
    builder = runtime()

    prompt = builder._build_step_input(run, current)

    assert "[EMPTY_RESULT]" in prompt
    assert "测" in prompt
    assert len(prompt.encode("utf-8")) <= R3_WORKFLOW_CONTEXT_MAX_BYTES
    assert prompt.encode("utf-8").decode("utf-8") == prompt


@pytest.mark.parametrize("body", [{"result": "dict"}, ["list"]])
def test_non_text_result_body_fails_before_recorder(body):
    run, current = run_with_history([body])
    recorded_prompts = []

    with pytest.raises(ValueError, match="result body must be text"):
        prompt = runtime()._build_step_input(run, current)
        recorded_prompts.append(prompt)

    assert recorded_prompts == []


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (lambda run, current: run["step_results"].append(copy.deepcopy(run["step_results"][0])), "invalid"),
        (
            lambda run, current: run["step_results"].append(
                {**copy.deepcopy(run["step_results"][0]), "step_result_id": "another-result"}
            ),
            "invalid",
        ),
        (lambda run, current: run["step_results"][0].pop("step_result_id"), "invalid"),
        (lambda run, current: run["step_results"][0].update(status="failed"), "invalid"),
        (lambda run, current: run["steps"][0].update(status="pending"), "non-succeeded"),
        (lambda run, current: run["step_results"].clear(), "missing"),
        (lambda run, current: run["step_results"][0].update(result=42), "must be text"),
        (lambda run, current: run["step_results"][0].update(result=True), "must be text"),
        (lambda run, current: run["step_results"][0].update(result=None), "must be text"),
        (lambda run, current: run["step_results"][0].update(result=b"not-text"), "must be text"),
        (lambda run, current: run["step_results"][0].update(result="bad\ud800text"), "UTF-8"),
        (lambda run, current: current.update(step_name="x" * 600), "step instruction"),
        (
            lambda run, current: run["step_results"][0].update(step_result_id="x" * 2_100),
            "metadata",
        ),
    ],
)
def test_invalid_history_fails_closed_before_prompt_use(mutate, message):
    run, current = run_with_history(["prior result"])
    mutate(run, current)

    with pytest.raises(ValueError, match=message):
        runtime()._build_step_input(run, current)
