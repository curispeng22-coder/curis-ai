"use client";

// T-017 / W03-A 前端：首次「执行任务」前的模型配置门。
// 行为：模型未配置（后端 next_action==='CONFIGURE_MODEL'）时，第一次执行才弹配置弹窗；
// 「在新标签打开模型设置」不离开本页，配好（重读草稿得到 CONTINUE_TASK）回到原任务，输入不丢；
// 取消配置也不丢输入；刷新/后退后按 sessionStorage 里的 workId 从服务端读回草稿，输入仍不丢；
// 未配置能力的团队显示「待连接能力」；runtime 未就绪显示加载态。
// 组件为 props 驱动（runtime/teams/api/storage 可注入），便于组件测试与直接渲染截图。

import { useEffect, useReducer } from "react";
import * as realApi from "../../lib/firstTaskApi.js";
import {
  PHASE, firstTaskReducer, defaultFirstTaskState,
  needsCapability, capabilityLabel, isRuntimeNotReady, PENDING_CAPABILITY,
  draftWorkId, firstTaskWorkKey, readStoredWorkId, writeStoredWorkId, sessionDraftStorage,
} from "../../lib/firstTaskSetup.mjs";

const DRAFT_ID = "t017-first-task";
const MODEL_SETTINGS_HREF = "/ceo-office/settings?tab=models";

// 首启 runtime 未就绪的加载态（不再先闪「这里还没有公司」再跳首页）。
export function FirstTaskLoading({ label = "正在打开 Curis 工作台…" }) {
  return <main role="status" aria-live="polite" className="grid min-h-screen place-items-center bg-ui-bg px-6 text-ui-txt">
    <section className="w-full max-w-md rounded-2xl border border-ui-line bg-ui-surface p-8 text-center shadow-ui">
      <div className="mx-auto h-10 w-10 animate-pulse rounded-full bg-ui-primary-soft" />
      <p className="mt-4 text-sm font-semibold text-ui-txt">{label}</p>
      <p className="mt-2 text-xs text-ui-txt-3">正在读取公司与团队状态，请稍候。</p>
    </section>
  </main>;
}

// 团队能力展示：未配置能力显示「待连接能力」，不假装可用。
export function TeamCapabilityList({ teams = [] }) {
  const list = Array.isArray(teams) ? teams : [];
  return <section aria-label="团队能力" className="rounded-2xl border border-ui-line bg-ui-surface p-5">
    <h2 className="text-sm font-semibold text-ui-txt">团队与能力</h2>
    <p className="mt-1 text-xs text-ui-txt-3">组织与员工已就绪；执行能力需连接模型后才可用。</p>
    {list.length === 0 ? <p role="status" className="mt-3 text-sm text-ui-txt-2">团队状态正在读取…</p> :
      <ul className="mt-3 divide-y divide-ui-line">
        {list.map((team, index) => {
          const pending = needsCapability(team);
          const label = capabilityLabel(team);
          return <li key={team.workspace_id || team.kind || index} className="flex items-center justify-between gap-3 py-3">
            <span className="text-sm text-ui-txt">{team.name || "团队"}</span>
            <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${pending ? "bg-ui-amber-soft text-ui-amber" : "bg-ui-green-soft text-ui-green"}`}
              data-capability={label}>{label}</span>
          </li>;
        })}
      </ul>}
  </section>;
}

// 首次执行前弹出的模型配置弹窗（少而清楚，沿用现有样式）。
export function ModelSetupDialog({ input = "", busy = false, message = "", error = "", onConfirm, onCancel, modelSettingsHref = MODEL_SETTINGS_HREF }) {
  return <div role="presentation" className="fixed inset-0 z-50 grid place-items-center bg-ui-bg/70 px-4">
    <section role="dialog" aria-modal="true" aria-label="首次执行前配置模型" className="w-full max-w-[520px] rounded-2xl border border-ui-line bg-ui-surface p-7 shadow-ui-3">
      <span className="text-xs font-semibold text-ui-primary-text">首次执行 · 模型配置</span>
      <h2 className="mt-2 text-xl font-semibold text-ui-txt">先连接模型，才能开始执行</h2>
      <p className="mt-2 text-sm leading-6 text-ui-txt-2">当前团队显示「{PENDING_CAPABILITY}」。下面的链接会在<b>新标签</b>打开模型设置，不离开本页；请在其中的「模型管理」里连接并验证一个可用模型。本页与你的输入会一直保留，配置完成后回到本页点「配置完成，回到原任务」核对即可。</p>
      <div className="mt-4 rounded-xl border border-ui-line bg-ui-surface-2 p-3">
        <p className="text-xs font-semibold text-ui-txt-3">你的任务输入（已保留）</p>
        <p className="mt-1 whitespace-pre-wrap break-words text-sm text-ui-txt" data-preserved-input>{input || "（尚未填写）"}</p>
      </div>
      <a href={modelSettingsHref} target="_blank" rel="noreferrer" className="mt-4 inline-block text-sm font-semibold text-ui-primary">在新标签打开模型设置 →</a>
      {message ? <p role="status" className="mt-3 text-sm text-ui-amber">{message}</p> : null}
      {error ? <p role="alert" className="mt-3 text-sm text-ui-danger">{error}</p> : null}
      <div className="mt-5 flex flex-wrap gap-3">
        <button type="button" disabled={busy} onClick={onConfirm} className="rounded-xl bg-ui-primary px-5 py-3 text-sm font-semibold text-ui-primary-fg disabled:opacity-50">{busy ? "正在核对…" : "配置完成，回到原任务"}</button>
        <button type="button" disabled={busy} onClick={onCancel} className="rounded-xl border border-ui-line bg-ui-surface px-5 py-3 text-sm font-semibold text-ui-txt-2 disabled:opacity-50">取消配置</button>
      </div>
      <p className="mt-3 text-xs text-ui-txt-3">取消也会保留你已填写的内容，可稍后再执行。</p>
    </section>
  </div>;
}

export default function FirstTaskModelSetup({
  runtimeStatus = "ready",
  teams = [],
  companyId = "",
  writingWorkspaceId = "",
  api,
  storage,
  initialInput = "",
  initialState,
  modelSettingsHref = MODEL_SETTINGS_HREF,
}) {
  const actions = api || realApi;
  const draftStore = storage || sessionDraftStorage();
  const seed = initialState || { ...defaultFirstTaskState(), input: initialInput };
  const [state, dispatch] = useReducer(firstTaskReducer, seed);

  // 重挂载（刷新/后退/直接重进）读回：workId 存于 sessionStorage（仅业务 id，非凭证），
  // 据此 GET 服务端草稿恢复输入与配置弹窗；读回失败保持当前状态，不覆盖用户已输入的内容。
  useEffect(() => {
    if (!companyId || !writingWorkspaceId) return;
    const workId = readStoredWorkId(draftStore, firstTaskWorkKey(companyId, writingWorkspaceId));
    if (!workId) return;
    let alive = true;
    actions.readWritingTaskDraft(companyId, writingWorkspaceId, workId)
      .then((result) => { if (alive) dispatch({ type: "RESTORE_RESULT", result }); })
      .catch(() => { /* 草稿仍在服务端，保持当前状态即可。 */ });
    return () => { alive = false; };
  }, [actions, draftStore, companyId, writingWorkspaceId]);

  const execute = async () => {
    if (state.busy || !state.input.trim() || !companyId || !writingWorkspaceId) return;
    dispatch({ type: "EXECUTE_START" });
    try {
      const result = await actions.saveWritingTaskDraft(companyId, writingWorkspaceId, {
        draftId: DRAFT_ID, text: state.input, expectedRevision: state.revision,
      });
      writeStoredWorkId(draftStore, firstTaskWorkKey(companyId, writingWorkspaceId), draftWorkId(result));
      dispatch({ type: "EXECUTE_RESULT", result });
    } catch {
      dispatch({ type: "ERROR", message: "暂时无法保存任务，请稍后重试；输入已保留。" });
    }
  };

  const confirmConfigured = async () => {
    if (state.busy || !state.workId) return;
    dispatch({ type: "CONFIGURE_START" });
    try {
      const result = await actions.readWritingTaskDraft(companyId, writingWorkspaceId, state.workId);
      dispatch({ type: "CONFIGURE_RESULT", result });
    } catch {
      dispatch({ type: "ERROR", message: "暂时无法核对模型配置，请稍后重试；输入已保留。" });
    }
  };

  const cancel = () => dispatch({ type: "CANCEL_SETUP" });

  if (isRuntimeNotReady(runtimeStatus)) return <FirstTaskLoading />;

  const pendingTeams = (Array.isArray(teams) ? teams : []).filter(needsCapability).length;

  return <main className="mx-auto max-w-[880px] space-y-5 p-6 text-ui-txt">
    <header>
      <span className="text-xs font-semibold text-ui-primary-text">W03-A · 首次执行</span>
      <h1 className="mt-1 text-2xl font-semibold tracking-[-0.02em]">写下你的第一个任务</h1>
      <p className="mt-1 text-sm text-ui-txt-2">输入会先保存为草稿；模型未配置时，只有点「执行任务」才会弹出配置。</p>
    </header>

    <TeamCapabilityList teams={teams} />

    <section aria-label="任务输入" className="rounded-2xl border border-ui-line bg-ui-surface p-5">
      <label className="block text-sm font-semibold" htmlFor="first-task-input">文稿任务</label>
      <textarea id="first-task-input" aria-label="任务输入" value={state.input}
        onChange={(event) => dispatch({ type: "INPUT", input: event.target.value })}
        rows={4} placeholder="例如：写一篇关于……的文稿"
        className="mt-2 w-full resize-none rounded-xl border border-ui-line bg-ui-surface px-3 py-2 text-sm outline-none focus:border-ui-primary" />
      {state.message ? <p role="status" className="mt-2 text-sm text-ui-amber">{state.message}</p> : null}
      {state.error ? <p role="alert" className="mt-2 text-sm text-ui-danger">{state.error}</p> : null}
      <div className="mt-3 flex flex-wrap items-center gap-3">
        <button type="button" onClick={execute} disabled={state.busy || !state.input.trim() || !companyId || !writingWorkspaceId}
          className="rounded-xl bg-ui-primary px-5 py-3 text-sm font-semibold text-ui-primary-fg disabled:opacity-50">{state.busy ? "处理中…" : "执行任务"}</button>
        {pendingTeams > 0 ? <span className="text-xs text-ui-txt-3">还有 {pendingTeams} 支团队「{PENDING_CAPABILITY}」</span> : null}
      </div>
    </section>

    {state.phase === PHASE.SETUP ? <ModelSetupDialog
      input={state.input} busy={state.busy} message={state.message} error={state.error}
      onConfirm={confirmConfigured} onCancel={cancel} modelSettingsHref={modelSettingsHref} /> : null}
  </main>;
}
