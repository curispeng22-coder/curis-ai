// Read-only ADR-0046 truth mapping for the Shared Composer access slot.
// The slot never offers a choice: Requested != Configured != Effective, and
// only a verified Adapter snapshot may claim that access is in effect.

export const COMPUTER_ACCESS_MODEL_VIEW = {
  label: "访问权限 · 模型不适用",
  title: "当前对话由模型执行，不涉及本机电脑访问。接入可验证的本地 Agent 后，这里才会出现真实权限设置；当前版本不提供选择。",
};

const VERIFIED_EFFECTIVE = {
  GRANTED: "已验证生效",
  DENIED: "已验证未授予",
  REVOKED: "已验证已撤回",
  NONE: "已验证无访问",
};

export function computerAccessView(access, { modelBacked = false, agentBacked = false } = {}) {
  if (access?.state === "MODEL_EXECUTOR_NOT_APPLICABLE") return COMPUTER_ACCESS_MODEL_VIEW;
  if (access?.state === "NO_EXECUTION_BRIDGE") {
    return {
      label: "访问权限 · 无法确认",
      title: "无法确认是否已生效：这位员工尚无可用的执行能力桥接，也没有可验证的本地 Agent 接入证据。",
    };
  }
  if (access?.verification_state === "VERIFIED"
      && access.effective_state && access.effective_state !== "UNKNOWN") {
    const effective = VERIFIED_EFFECTIVE[access.effective_state] || "已验证";
    return {
      label: `访问权限 · ${effective}`,
      title: `电脑访问已经过 Adapter 验证（当前状态：${access.effective_state}）。恢复会话后需要重新验证；如需扩大访问范围仍会先询问。`,
    };
  }
  if (access?.configured_state === "CONFIGURED") {
    return {
      label: "访问权限 · 已配置 · 待验证",
      title: "Agent 已按允许范围配置；实际生效权限尚未验证，无法确认是否已生效。",
    };
  }
  if (modelBacked && !agentBacked) return COMPUTER_ACCESS_MODEL_VIEW;
  return {
    label: "访问权限 · 无法确认",
    title: "无法确认是否已生效：当前没有可验证的本地 Agent 访问证据。",
  };
}
