"use client";

import { Suspense, useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";

import { useRuntime } from "../../components/runtime/RuntimeProvider.js";
import { RuntimeError, RuntimeLoading } from "../../components/runtime/RuntimeStates.js";
import { TerraButton, TerraCard, TerraInput, TerraTag } from "../../components/terra/TerraPrimitives.js";
import { CEO_ID } from "../../lib/api.js";
import {
  createFoundingRun,
  getFoundingRun,
  getRuntimeCompany,
  materializeFoundingCompany,
  runtimeErrorMessage,
  transitionRuntimeEntity,
} from "../../lib/runtimeApi.js";


const STATUS = {
  ARRIVED: ["已到达", "表达经营意图", "INTENT_CAPTURED", "capture_intent"],
  INTENT_CAPTURED: ["意图已保存", "开始澄清", "CLARIFYING", "request_clarification"],
  CLARIFYING: ["正在澄清", "形成公司提案", "PROPOSED", "propose_company"],
  PROPOSED: ["公司提案待确认", "确认公司提案", "CEO_CONFIRMED", "confirm_company"],
  WAITING_CEO: ["等待 CEO", "继续提案", "PROPOSED", "resume_proposal"],
  REJECTED: ["提案已退回", "重新澄清", "CLARIFYING", "revise_proposal"],
};

function FoundingGuide() {
  const searchParams = useSearchParams();
  const runtime = useRuntime();
  const runId = searchParams.get("founding_run_id") || "";
  const [intent, setIntent] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [run, setRun] = useState(null);
  const [busy, setBusy] = useState(Boolean(runId));
  const [error, setError] = useState("");

  const recover = useCallback(async () => {
    if (!runId) return;
    setBusy(true);
    setError("");
    try {
      setRun(await getFoundingRun(runId));
    } catch (caught) {
      setError(runtimeErrorMessage(caught));
    } finally {
      setBusy(false);
    }
  }, [runId]);

  useEffect(() => {
    recover();
  }, [recover]);

  const start = async () => {
    if (!intent.trim()) {
      setError("请先写下你希望建立怎样的公司，以及第一项可验证结果。");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const created = await createFoundingRun({
        owner_ref: CEO_ID,
        intent_ref: `ceo-intent-${Date.now()}`,
        org_version: "org-v1",
        blueprint_version: "",
      });
      const captured = await transitionRuntimeEntity(created.entity_id, {
        target: "INTENT_CAPTURED",
        actor: "CEO",
        trigger: "capture_intent",
        reason: "CEO 已提交经营意图",
        evidenceRefs: [],
        context: {},
      });
      setRun(captured);
      window.history.replaceState(null, "", `/onboarding?founding_run_id=${encodeURIComponent(created.entity_id)}`);
    } catch (caught) {
      setError(runtimeErrorMessage(caught));
    } finally {
      setBusy(false);
    }
  };

  const move = async (target, trigger) => {
    if (!run) return;
    setBusy(true);
    setError("");
    try {
      setRun(await transitionRuntimeEntity(run.entity_id, {
        target,
        actor: "CEO",
        trigger,
        reason: "CEO 在创办向导中确认",
        evidenceRefs: [],
        context: {},
      }));
    } catch (caught) {
      setError(runtimeErrorMessage(caught));
    } finally {
      setBusy(false);
    }
  };

  const materialize = async () => {
    const name = companyName.trim();
    if (!run || !name) {
      setError("请先填写公司名称。");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const companyId = `company-${run.entity_id.replace(/^founding_run-/, "")}`;
      const result = await materializeFoundingCompany(run.entity_id, {
        company_id: companyId,
        ceo_id: run.owner_ref,
        name,
      });
      const snapshot = await getRuntimeCompany(result.company.company_id);
      if (!snapshot?.company || !snapshot?.assistant) {
        throw new Error("Runtime materialization snapshot is incomplete");
      }
      await runtime.refresh();
      window.location.replace("/ceo-office");
    } catch (caught) {
      setError(runtimeErrorMessage(caught));
    } finally {
      setBusy(false);
    }
  };

  if (runtime.status === "idle" || runtime.status === "loading") {
    return <RuntimeLoading label="正在检查公司创办状态…" />;
  }
  if (runtime.status === "error" || runtime.status === "forbidden") {
    return <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  }
  if (runtime.snapshot?.company) {
    const nextPath = "/ceo-office";
    // Legacy compatibility contract names: getCompanies/createCompany/updateCompany are intentionally not used.
    return (
      <TerraCard className="max-w-2xl">
        <TerraTag color="green">公司已建立</TerraTag>
        <h1 className="mt-3 font-ui-sans text-ui-7 font-semibold text-ui-txt">个人 Workspace 已确认</h1>
        <p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">
          {runtime.snapshot.company.name} 已有持久化 Runtime。继续进入 CEO 工作台，不重复创建公司。
        </p>
        <TerraButton className="mt-5" onClick={() => window.location.replace(nextPath)}>
          进入 CEO 工作台
        </TerraButton>
      </TerraCard>
    );
  }

  const current = run ? STATUS[run.lifecycle_status] : null;
  const confirmed = run?.lifecycle_status === "CEO_CONFIRMED";

  return (
    <div className="mx-auto max-w-3xl">
      <div className="mb-6">
        <div className="text-ui-1 font-bold text-ui-primary">FOUNDING GUIDE</div>
        <h1 className="mt-2 font-ui-sans text-ui-8 font-semibold leading-tight text-ui-txt">从经营意图开始创办公司</h1>
        <p className="mt-2 max-w-[68ch] text-ui-2 leading-relaxed text-ui-txt-2">
          每一步都写入同一个 FoundingRun。刷新或重新打开链接后，可以从持久化状态继续。
        </p>
      </div>

      {!run ? (
        <TerraCard>
          <TerraInput
            label="你的经营意图"
            value={intent}
            onChange={(event) => setIntent(event.target.value)}
            placeholder="例如：建立一支 AI 团队，在 30 天内验证第一个可交付业务结果"
            hint="输入内容只用于本次提交；Runtime 只保存安全引用，不回显原始经营描述。"
          />
          <TerraButton className="mt-4" disabled={busy} onClick={start}>
            {busy ? "正在建立…" : "建立 FoundingRun"}
          </TerraButton>
        </TerraCard>
      ) : (
        <TerraCard>
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <TerraTag color={confirmed ? "green" : "cyan"}>{confirmed ? "CEO 已确认" : current?.[0] || run.lifecycle_status}</TerraTag>
              <h2 className="mt-3 font-ui-sans text-ui-5 font-semibold text-ui-txt">创办运行正在持续</h2>
              <p className="mt-1 break-all text-ui-1 text-ui-txt-3">{run.entity_id}</p>
            </div>
            <button type="button" onClick={recover} className="text-ui-1 font-bold text-ui-primary" disabled={busy}>
              从 Runtime 恢复
            </button>
          </div>

          <dl className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2">
            <div className="rounded-ui-sm bg-ui-surface-2 p-3"><dt className="text-ui-1 text-ui-txt-3">当前状态</dt><dd className="mt-1 font-semibold text-ui-txt">{run.lifecycle_status}</dd></div>
            <div className="rounded-ui-sm bg-ui-surface-2 p-3"><dt className="text-ui-1 text-ui-txt-3">最后更新</dt><dd className="mt-1 font-semibold text-ui-txt">{run.updated_at || "未记录"}</dd></div>
          </dl>

          {confirmed ? (
            <div className="mt-5 rounded-ui-sm border border-ui-line bg-ui-surface-2 p-4">
              <h3 className="font-semibold text-ui-txt">建立公司</h3>
              <p className="mt-2 text-ui-2 leading-relaxed text-ui-txt-2">
                CEO 已确认提案。提交后由 Runtime 在同一事务内建立 Company、第一位 CEO Assistant，并完成 FoundingRun 状态流转。
              </p>
              <div className="mt-4">
                <TerraInput
                  label="公司名称"
                  value={companyName}
                  onChange={(event) => setCompanyName(event.target.value)}
                  placeholder="例如：Curis AI"
                  maxLength={120}
                />
              </div>
              <TerraButton className="mt-4" disabled={busy} onClick={materialize}>
                {busy ? "正在建立…" : "建立公司"}
              </TerraButton>
            </div>
          ) : current ? (
            <div className="mt-5 flex flex-wrap gap-2">
              <TerraButton disabled={busy} onClick={() => move(current[2], current[3])}>{current[1]}</TerraButton>
              {run.lifecycle_status === "PROPOSED" && (
                <TerraButton variant="ghost" disabled={busy} onClick={() => move("REJECTED", "reject_proposal")}>退回提案</TerraButton>
              )}
            </div>
          ) : (
            <p role="status" className="mt-5 text-ui-2 text-ui-txt-2">当前状态需由 Runtime 或已授权流程继续，前端不会直接改写。</p>
          )}
        </TerraCard>
      )}

      {error && <p role="alert" className="mt-4 rounded-ui-sm bg-ui-red-soft px-4 py-3 text-ui-2 text-ui-red">{error}</p>}
      <p className="mt-6 text-ui-1 text-ui-txt-3">
        已有公司？ <Link href="/ceo-office" className="font-bold text-ui-primary">返回 CEO 工作台</Link>
      </p>
    </div>
  );
}

export default function OnboardingPage() {
  return (
    <main className="min-h-screen bg-ui-bg px-5 py-10 text-ui-txt sm:px-8">
      <Suspense fallback={<RuntimeLoading label="正在恢复创办运行…" />}>
        <FoundingGuide />
      </Suspense>
    </main>
  );
}
