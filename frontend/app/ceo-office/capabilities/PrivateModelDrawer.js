"use client";

import { useEffect, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../components/terra/TerraPrimitives.js";
import { createPrivateModel } from "../../../lib/capabilities.js";

// 与后端 catalog_constants.GATEWAY_TYPE 对齐的 OpenAI 兼容方言（仅作 UI 选项，
// 后端不强制校验 provider_type；新增方言改这里即可）。
const PROVIDER_TYPES = [
  ["openai_compatible", "OpenAI 兼容（自建/通用）"],
  ["openai", "OpenAI 官方"],
  ["newapi", "New API 聚合网关"],
  ["oneapi", "One API 聚合网关"],
  ["openrouter", "OpenRouter"],
  ["deepseek", "DeepSeek"],
  ["moonshot", "Moonshot"],
  ["ollama", "Ollama 本地"],
  ["vllm", "vLLM 自托管"],
];

const EMPTY = {
  name: "",
  provider_type: "openai_compatible",
  base_url: "",
  model_name: "",
  credential_ref: "",
  enabled: true,
};

export default function PrivateModelDrawer({ open, onClose, onSuccess }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setForm(EMPTY);
    setError("");
    setSubmitting(false);
  }, [open]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function submit(event) {
    event.preventDefault();
    if (!form.name.trim()) return setError("请输入模型名称（作为标识）");
    if (!form.base_url.trim()) return setError("请输入网关 base_url");
    if (!form.model_name.trim()) return setError("请输入 Provider 接收的模型 ID");
    setSubmitting(true);
    setError("");
    try {
      const created = await createPrivateModel({
        name: form.name.trim(),
        provider_type: form.provider_type,
        base_url: form.base_url.trim().replace(/\/+$/, ""),
        model_name: form.model_name.trim(),
        credential_ref: form.credential_ref.trim(),
        enabled: Boolean(form.enabled),
      });
      onSuccess?.(created);
    } catch (err) {
      setError(err?.message || "自定义模型保存失败");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <TerraDrawer
      open={open}
      title="注册自定义模型"
      description="为当前租户接入一个私有 OpenAI 兼容模型网关。密钥不进表单：仅填凭证引用（env:VAR），明文放环境变量。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        <TerraInput
          label="模型名称（标识）"
          required
          value={form.name}
          onChange={(event) => update("name", event.target.value)}
          hint="作为该私有模型的稳定标识，例如 My DeepSeek"
          autoFocus
        />
        <div>
          <label htmlFor="pm-provider" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            协议方言
          </label>
          <select
            id="pm-provider"
            value={form.provider_type}
            onChange={(event) => update("provider_type", event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {PROVIDER_TYPES.map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </div>
        <TerraInput
          label="网关 base_url"
          required
          value={form.base_url}
          onChange={(event) => update("base_url", event.target.value)}
          placeholder="https://api.deepseek.com"
          hint="OpenAI 兼容端点；调用时自动拼接 /v1/chat/completions"
        />
        <TerraInput
          label="调用模型 ID"
          required
          value={form.model_name}
          onChange={(event) => update("model_name", event.target.value)}
          placeholder="deepseek-chat"
          hint="Provider 实际接收的模型名"
        />
        <TerraInput
          label="凭证引用（不填明文）"
          value={form.credential_ref}
          onChange={(event) => update("credential_ref", event.target.value)}
          hint="仅填 scheme:reference，密钥放环境变量。格式 env:YOUR_ENV_VAR / vault:xxx / kms:xxx"
          placeholder="env:DEEPSEEK_API_KEY"
        />
        <label className="flex items-center gap-2 text-sm text-ui-txt">
          <input
            type="checkbox"
            checked={form.enabled}
            onChange={(event) => update("enabled", event.target.checked)}
            className="rounded border-ui-line"
          />
          注册后立即可用
        </label>
        <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
          本条目保存在「租户私有能力」中，与官方目录隔离；未来商业化时即终端用户自助接入的入口。
        </p>
        {error && <p className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting}>
            {submitting ? "保存中…" : "保存自定义模型"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
