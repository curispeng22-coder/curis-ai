// T-017 / W03-A 前端：首次执行前配置模型的状态机（纯函数，无 DOM、无新依赖）。
// 字段严格对应后端 T-011 的实际实现，不臆造：
//   POST /api/workspace/v1/first-launch
//     -> { company_id, teams:[{ kind, name, workspace_id, organization_status,
//                              execution:{ status, ... }, status_label }], next_action:'OPEN_HOME' }
//        status_label = '就绪'（execution.status==='AVAILABLE'）否则 '待连接能力'
//   PUT  /api/workspace/v1/companies/{company_id}/writing/{workspace_id}/task-draft
//     body { draft_id, text, expected_revision }
//     -> read_draft: { work, draft:{ text, revision }, execution, next_action,
//                      return_to:{ company_id, workspace_id, work_id } }
//   GET  /api/workspace/v1/companies/{company_id}/writing/{workspace_id}/task-drafts/{work_id}
//     -> read_draft（同上）
//   next_action = 'CONFIGURE_MODEL'（模型/执行能力未配置）| 'CONTINUE_TASK'（可用）

export const CONFIGURE_MODEL = "CONFIGURE_MODEL";
export const CONTINUE_TASK = "CONTINUE_TASK";
export const PENDING_CAPABILITY = "待连接能力";
export const READY = "就绪";

export const PHASE = Object.freeze({
  EDITING: "editing",   // 工作台：可输入、可点「执行任务」
  SETUP: "setup",       // 模型配置弹窗打开（配置前被拦）
  RESUMED: "resumed",   // 配置完成，已回到原任务（输入仍保留）
});

// 团队是否具备执行能力：以后端 status_label 为主，execution.status 为辅。
export function teamHasCapability(team) {
  if (!team || typeof team !== "object") return false;
  if (typeof team.status_label === "string") return team.status_label === READY;
  return team.execution?.status === "AVAILABLE";
}

export function needsCapability(team) {
  return !teamHasCapability(team);
}

export function capabilityLabel(team) {
  return teamHasCapability(team) ? READY : PENDING_CAPABILITY;
}

// 是否要为这次执行弹出模型配置：只认后端 next_action，不臆造「已配置」标记。
export function shouldOpenModelSetup(nextAction) {
  return nextAction === CONFIGURE_MODEL;
}

// 首启 runtime 未就绪（idle/loading）时显示加载态，不先闪「还没有公司」。
export function isRuntimeNotReady(status) {
  return status === "idle" || status === "loading";
}

// 后端 read_draft 中的任务定位与版本（first_launch_service.read_draft 实际返回）。
export function draftWorkId(result) {
  return result?.return_to?.work_id || result?.work?.entity_id || "";
}

export function draftRevision(result, fallback) {
  return Number.isInteger(result?.draft?.revision) ? result.draft.revision : fallback;
}

// workId 持久化（sessionStorage，仅业务 id，非凭证）：重挂载（刷新/后退/重进）后
// 用它 GET 服务端草稿读回输入。真实后端 entity_id 形如 work-<uuid4>（workspace.py:152）。
const WORK_ID_PATTERN = /^[A-Za-z0-9_-]{1,128}$/;

export function firstTaskWorkKey(companyId, workspaceId) {
  return `curis.first-task.work.${companyId}__${workspaceId}`;
}

export function sessionDraftStorage() {
  try {
    if (typeof window === "undefined" || !window.sessionStorage) return null;
    return window.sessionStorage;
  } catch { return null; } // 隐私模式等场景 storage 访问可能被拒：降级为不持久化。
}

export function readStoredWorkId(storage, key) {
  try {
    const raw = storage?.getItem?.(key);
    return typeof raw === "string" && WORK_ID_PATTERN.test(raw) ? raw : "";
  } catch { return ""; }
}

export function writeStoredWorkId(storage, key, workId) {
  try {
    if (storage?.setItem && typeof workId === "string" && WORK_ID_PATTERN.test(workId)) storage.setItem(key, workId);
  } catch { /* 保留在内存即可；服务端草稿仍存在。 */ }
}

export function defaultFirstTaskState() {
  return {
    phase: PHASE.EDITING,
    input: "",
    workId: "",
    revision: 0,
    busy: false,
    configured: false,
    executed: false,
    message: "",
    error: "",
  };
}

// 全部转换都保留 state.input —— 配置前被拦 / 配置完成 / 取消配置都不丢输入。
export function firstTaskReducer(state, action) {
  switch (action.type) {
    case "INPUT":
      return { ...state, input: action.input };
    case "EXECUTE_START":
      return { ...state, busy: true, error: "", message: "" };
    case "EXECUTE_RESULT": {
      const result = action.result || {};
      const workId = draftWorkId(result) || state.workId;
      const revision = draftRevision(result, state.revision);
      if (shouldOpenModelSetup(result.next_action)) {
        // 配置前被拦：不执行任务，打开模型配置弹窗，输入保留。
        return {
          ...state, phase: PHASE.SETUP, busy: false, configured: false, executed: false,
          workId, revision, message: "第一次执行前需要连接模型；原任务输入已保留。", error: "",
        };
      }
      // CONTINUE_TASK：模型/执行能力可用，继续执行原任务。
      return {
        ...state, phase: PHASE.EDITING, busy: false, configured: true, executed: true,
        workId, revision, message: "模型已就绪，可继续执行任务。", error: "",
      };
    }
    case "CONFIGURE_START":
      return { ...state, busy: true, error: "" };
    case "CONFIGURE_RESULT": {
      const result = action.result || {};
      const revision = draftRevision(result, state.revision);
      if (result.next_action === CONTINUE_TASK) {
        // 配置成功，回到原任务；不自动执行，输入保留。
        return {
          ...state, phase: PHASE.RESUMED, busy: false, configured: true,
          revision, message: "配置完成，已回到原任务；你填写的内容仍然保留。", error: "",
        };
      }
      // 重读仍为 CONFIGURE_MODEL：诚实提示，不假装配置成功，输入保留。
      return {
        ...state, phase: PHASE.SETUP, busy: false,
        message: "模型仍未连接，请先在模型设置里完成配置。", error: "",
      };
    }
    case "RESTORE_RESULT": {
      // 重挂载读回：只在输入为空时采纳服务端草稿，绝不覆盖用户已输入的内容。
      const result = action.result || {};
      const input = typeof result.draft?.text === "string" ? result.draft.text : "";
      if (state.input || !input) return state;
      const workId = draftWorkId(result) || state.workId;
      const revision = draftRevision(result, state.revision);
      if (result.next_action === CONTINUE_TASK) {
        return {
          ...state, phase: PHASE.RESUMED, configured: true, workId, revision, input,
          message: "已读回上次保留的任务草稿；模型已就绪，可继续执行。", error: "",
        };
      }
      // 仍未配置：重新打开配置弹窗，输入从服务端草稿恢复（可继续核对/取消）。
      return {
        ...state, phase: PHASE.SETUP, configured: false, executed: false, workId, revision, input,
        message: "已读回上次保留的任务草稿；模型仍未连接，请完成配置。", error: "",
      };
    }
    case "CANCEL_SETUP":
      return {
        ...state, phase: PHASE.EDITING, busy: false,
        message: "已取消配置，可以稍后再执行；输入已保留。", error: "",
      };
    case "ERROR":
      return { ...state, busy: false, error: action.message || "操作暂时无法完成，输入已保留。" };
    case "RESET":
      return defaultFirstTaskState();
    default:
      return state;
  }
}
