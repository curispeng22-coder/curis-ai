// 起任务封装（T4 / 工作台）。
// 仅创建 workflow 实例并展示返回状态，不轮询、不声称真实执行完成（RealRD 工具多为 mock）。
// 统一经 workspaceFetch（自动注入租户头），不调用 /api/platform/*，不自造 fetch。

import { workspaceFetch } from "./api.js";

const DEFAULT_TEMPLATE_ID = "official.workflow.software_rnd_sop";

/**
 * 启动一个 workflow 实例（Workspace 写入口 /api/workspace/workflows）。
 * 默认模板 official.workflow.software_rnd_sop；payload 携带员工 / 项目上下文。
 * 仅创建并返回一个实例对象（含 workflow_instance_id / status 等），调用方不得假设其已执行完成。
 *
 * @param {Object} [payload]
 * @param {string} [payload.empId] 关联员工 id
 * @param {string} [payload.projectId] 关联项目 id
 * @param {string} [payload.projectName] 关联项目名
 * @param {string} [payload.templateId] 覆盖默认模板
 * @param {Object} [payload.context] 额外业务上下文
 * @returns {Promise<any>}
 */
export async function startWorkflow({
  empId,
  projectId,
  projectName,
  templateId = DEFAULT_TEMPLATE_ID,
  context = {},
  ...rest
} = {}) {
  try {
    const body = {
      template_id: templateId,
      ...(empId ? { employee_id: empId } : {}),
      ...(projectId ? { project_id: projectId } : {}),
      ...(projectName ? { project_name: projectName } : {}),
      ...(context && Object.keys(context).length ? { context } : {}),
      ...rest,
    };
    return await workspaceFetch("/api/workspace/workflows", {
      method: "POST",
      body: JSON.stringify(body),
    });
  } catch (err) {
    // 优雅处理模板不存在等异常：归一化错误信息，交由 UI 显示而非崩溃。
    const normalized = new Error(
      err && err.message ? err.message : "启动工作流失败"
    );
    normalized.cause = err;
    throw normalized;
  }
}

export { DEFAULT_TEMPLATE_ID };
