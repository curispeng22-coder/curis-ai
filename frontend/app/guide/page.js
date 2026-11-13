"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import TerraShell from "../../components/terra/TerraShell.js";
import {
  TerraBoundary,
  TerraButton,
  TerraCard,
  TerraPageHead,
  TerraTag,
} from "../../components/terra/TerraPrimitives.js";
import {
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../components/terra/TerraState.js";
import {
  abandonGuideSession,
  answerGuideSession,
  confirmGuideSession,
  listGuides,
  startGuideSession,
} from "../../lib/api.js";

/**
 * 业务工作台引导（Workbench Guide）向导页。
 * 流程：选模板 → 对话描述业务（AI 追问/出蓝图）→ 确认蓝图 → 落地生成工作台。
 * 交互形态：创建入口向导（接近引导表单填写），流程定义全在后端（数据驱动模板）。
 */
export default function GuidePage() {
  const [phase, setPhase] = useState("idle"); // idle | collecting | confirming | done
  const [guides, setGuides] = useState([]);
  const [session, setSession] = useState(null);
  const [step, setStep] = useState(1);
  const [prompt, setPrompt] = useState("");
  const [answer, setAnswer] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [blueprint, setBlueprint] = useState(null);
  const [manualFields, setManualFields] = useState([]);
  const [workbench, setWorkbench] = useState(null);
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    listGuides()
      .then((payload) => setGuides(payload?.guides || []))
      .catch((err) => setError(err?.message || "引导模板读取失败"))
      .finally(() => setLoading(false));
  }, []);

  async function start(guideId) {
    setBusy(true);
    setError("");
    try {
      const sessionData = await startGuideSession(guideId);
      setSession(sessionData);
      setStep(sessionData.current_step);
      setPrompt(sessionData.step?.prompt || "");
      setPhase("collecting");
    } catch (err) {
      setError(err?.message || "引导会话启动失败");
    } finally {
      setBusy(false);
    }
  }

  async function submitAnswer() {
    if (!answer.trim()) return;
    setBusy(true);
    setError("");
    try {
      const payload = await answerGuideSession(session.session_id, step, answer);
      setAnswer("");
      if (payload.mode === "follow_up") {
        setFollowUp(payload.question || "请补充说明");
      } else if (payload.mode === "blueprint") {
        setBlueprint(payload.blueprint || {});
        setPhase("confirming");
      } else if (payload.mode === "manual_fallback") {
        setManualFields(payload.fields || []);
        setFollowUp(payload.message || "请直接填写以下字段");
        // manual_fallback 时用字段表单收集，仍停留在 collecting；这里提示用户填写后点「生成方案」。
      }
    } catch (err) {
      setError(err?.message || "提交回答失败");
    } finally {
      setBusy(false);
    }
  }

  async function submitManual() {
    // manual_fallback 兜底：用已收集的 answer 重新尝试出蓝图（简化：提示重试或直接出空蓝图）。
    setBusy(true);
    setError("");
    try {
      const payload = await answerGuideSession(session.session_id, step, answer);
      if (payload.mode === "blueprint") {
        setBlueprint(payload.blueprint || {});
        setPhase("confirming");
      } else {
        setFollowUp("AI 暂时无法生成方案，请稍后重试或直接填写下方字段确认。");
      }
    } catch (err) {
      setError(err?.message || "重试失败");
    } finally {
      setBusy(false);
    }
  }

  function updateBlueprint(path, value) {
    setBlueprint((prev) => {
      const next = { ...(prev || {}) };
      if (path === "project_name" || path === "goal" || path === "description") {
        next[path] = value;
      }
      return next;
    });
  }

  async function submitConfirm() {
    if (!blueprint?.project_name?.trim() || !blueprint?.goal?.trim()) {
      setError("项目名称与目标必填");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const payload = await confirmGuideSession(session.session_id, blueprint);
      setWorkbench(payload.workbench || {});
      setPhase("done");
    } catch (err) {
      setError(err?.message || "工作台生成失败");
    } finally {
      setBusy(false);
    }
  }

  function abandon() {
    if (session?.session_id) {
      abandonGuideSession(session.session_id).catch(() => {});
    }
    setSession(null);
    setPhase("idle");
    setFollowUp("");
    setBlueprint(null);
  }

  if (loading) {
    return (
      <TerraShell activeKey="guide">
        <TerraLoadingSkeleton label="加载引导模板…" />
      </TerraShell>
    );
  }
  if (error && phase === "idle") {
    return (
      <TerraShell activeKey="guide">
        <TerraErrorState title="无法加载引导" message={error} onRetry={() => window.location.reload()} />
      </TerraShell>
    );
  }

  return (
    <TerraShell activeKey="guide">
      <TerraPageHead
        title="创建业务工作台"
        description="告诉我你想做的业务，我帮你生成项目、岗位与员工"
      />

      {phase === "idle" && (
        <div className="g-stack" style={{ gap: 12, marginTop: 24 }}>
          {guides.map((guide) => (
            <TerraCard key={guide.guide_id} title={guide.name} style={{ padding: 20 }}>
              <p className="g-muted">{guide.steps?.map((s) => s.title).join(" → ") || "引导流程"}</p>
              <TerraButton
                label="开始引导"
                variant="primary"
                onClick={() => start(guide.guide_id)}
                disabled={busy}
              />
            </TerraCard>
          ))}
        </div>
      )}

      {phase === "collecting" && (
        <TerraCard title={`第 ${step} 步`} style={{ padding: 20, marginTop: 24 }}>
          {prompt && <p className="g-body">{prompt}</p>}
          {followUp && (
            <p className="g-note" style={{ marginTop: 12 }}>
              {followUp}
            </p>
          )}
          {manualFields.length > 0 ? (
            <div className="g-stack" style={{ gap: 8, marginTop: 16 }}>
              <p className="g-muted">AI 暂不可用，请直接填写字段后确认：</p>
              {manualFields.map((field) => (
                <input
                  key={field}
                  className="g-input"
                  placeholder={field}
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                />
              ))}
            </div>
          ) : (
            <textarea
              className="g-textarea"
              rows={4}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              placeholder="描述你的业务：目标、面向谁、预期产出…"
            />
          )}
          <div className="g-row" style={{ gap: 8, marginTop: 16 }}>
            <TerraButton
              label={manualFields.length > 0 ? "确认填写" : "提交回答"}
              variant="primary"
              onClick={manualFields.length > 0 ? submitManual : submitAnswer}
              disabled={busy || !answer.trim()}
            />
            <TerraButton label="放弃" variant="ghost" onClick={abandon} />
          </div>
        </TerraCard>
      )}

      {phase === "confirming" && blueprint && (
        <TerraCard title="确认工作台方案" style={{ padding: 20, marginTop: 24 }}>
          <p className="g-muted">确认或修改以下方案，确认后将生成你的工作台：</p>
          <div className="g-stack" style={{ gap: 10, marginTop: 12 }}>
            <label className="g-label">
              项目名称
              <input
                className="g-input"
                value={blueprint.project_name || ""}
                onChange={(e) => updateBlueprint("project_name", e.target.value)}
              />
            </label>
            <label className="g-label">
              业务目标
              <textarea
                className="g-textarea"
                rows={2}
                value={blueprint.goal || ""}
                onChange={(e) => updateBlueprint("goal", e.target.value)}
              />
            </label>
            {(blueprint.departments || []).map((dept, index) => (
              <div key={index} className="g-card-mini">
                <span className="g-muted">
                  {dept.name || dept.template_id}（{dept.employees?.length || 0} 个岗位）
                </span>
                {(dept.employees || []).map((emp, empIndex) => (
                  <span key={empIndex} className="g-tag-wrap">
                    <TerraTag label={emp.name || emp.template_id} />
                    {emp.allowed_effect_classes?.length > 0 && (
                      <span className="g-authz" title="岗位允许的能力类型">
                        {emp.allowed_effect_classes.join(" · ")}
                      </span>
                    )}
                  </span>
                ))}
              </div>
            ))}
          </div>
          <div className="g-row" style={{ gap: 8, marginTop: 16 }}>
            <TerraButton label="生成工作台" variant="primary" onClick={submitConfirm} disabled={busy} />
            <TerraButton label="返回修改" variant="ghost" onClick={() => setPhase("collecting")} />
          </div>
        </TerraCard>
      )}

      {phase === "done" && workbench && (
        <TerraCard title="工作台已生成" style={{ padding: 20, marginTop: 24 }}>
          <p className="g-body">
            <strong>{workbench.project_name}</strong> 已创建：{workbench.department_ids?.length || 0} 个部门、
            {workbench.employee_ids?.length || 0} 个岗位。
          </p>
          <p className="g-note">项目 ID：{workbench.project_id}</p>
          <div className="g-row" style={{ gap: 8, marginTop: 16 }}>
            <Link href="/ceo-office">
              <TerraButton label="进入 CEO Office" variant="primary" />
            </Link>
            <TerraButton label="再建一个业务" variant="ghost" onClick={abandon} />
          </div>
        </TerraCard>
      )}

      {error && phase !== "idle" && (
        <TerraBoundary>
          <TerraErrorState title="操作失败" message={error} onRetry={() => setError("")} />
        </TerraBoundary>
      )}

      <style jsx>{`
        .g-stack { display: flex; flex-direction: column; }
        .g-row { display: flex; align-items: center; }
        .g-muted { color: var(--ui-text-2); font-size: var(--ui-fs-2); }
        .g-note { color: var(--ui-accent); font-size: var(--ui-fs-2); }
        .g-body { font-size: var(--ui-fs-3); line-height: var(--ui-lh-loose); }
        .g-input, .g-textarea {
          width: 100%; padding: var(--ui-sp-2) var(--ui-sp-3);
          min-height: var(--ui-ctl-h);
          border-radius: var(--ui-r-sm); font-size: var(--ui-fs-3);
          color: var(--ui-text);
          background: var(--ui-surface-2);
          border: 1px solid var(--ui-line);
        }
        .g-label { display: flex; flex-direction: column; gap: var(--ui-sp-1); font-size: var(--ui-fs-2); color: var(--ui-text-2); }
        .g-card-mini {
          padding: var(--ui-sp-2) var(--ui-sp-3); border-radius: var(--ui-r-sm);
          background: var(--ui-surface-2);
          border: 1px solid var(--ui-line);
          display: flex; flex-wrap: wrap; gap: var(--ui-sp-1); align-items: center;
        }
        .g-tag-wrap { display: inline-flex; }
        .g-authz {
          margin-left: var(--ui-sp-1); font-size: var(--ui-fs-1); color: var(--ui-accent);
          border: 1px solid var(--ui-line); border-radius: var(--ui-r-pill);
          padding: 2px var(--ui-sp-2);
        }
      `}</style>
    </TerraShell>
  );
}
