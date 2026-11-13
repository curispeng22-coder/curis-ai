"use client";

import { useEffect, useState } from "react";
import {
  TerraButton,
  TerraDrawer,
  TerraInput,
} from "../../../components/terra/TerraPrimitives.js";
import { createCapability } from "../../../lib/capabilities.js";

// 后端 kind_map 规定：仅 cli → cli 适配器（本地命令执行）；tool/api/connector/webhook → http。
// 故「命令行执行」入口唯一落在 cli，其余统一走 HTTP 服务调用型字段。
const EXECUTION_TYPES = ["cli"];
const SERVICE_TYPES = ["tool", "api", "connector", "webhook"];
const PROTOCOL_TYPES = ["mcp"];

const EFFECT_CLASSES = [
  ["read", "只读（不改动外部状态）"],
  ["side-effect", "有副作用（读后写/触发动作）"],
  ["writing", "会写入/产生外部变更"],
];

// 与后端 auth_type 枚举对齐（none | oauth | apikey）；具体 Authorization 头在请求头 JSON 里填。
const AUTH_TYPES = [
  ["none", "无认证"],
  ["oauth", "OAuth"],
  ["apikey", "API Key"],
];

const HTTP_METHODS = ["POST", "GET", "PUT", "DELETE", "PATCH"];

const EMPTY = {
  capability_key: "",
  type: "model",
  name: "",
  provider_id: "",
  model_name: "",
  description: "",
  version: "1.0.0",
  endpoint: "",
  credential_ref: "",
  // 执行型（tool/cli）
  command: "",
  args: "",
  cwd: "",
  timeout: "30",
  effect_class: "read",
  // 服务型（api/connector/webhook）
  method: "POST",
  url: "",
  auth_type: "none",
  headers_json: "",
  body_json: "",
  // 协议型（mcp）
  transport: "stdio",
  mcp_target: "",
};

/** 解析多行文本为数组（支持 {{变量}} 占位）。空输入返回空数组。 */
function parseLines(text) {
  return (text || "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

/** 解析 JSON 文本，失败抛出带字段名的可读错误。 */
function parseJsonField(raw, fieldName) {
  const text = (raw || "").trim();
  if (!text) return undefined;
  try {
    return JSON.parse(text);
  } catch {
    throw new Error(`${fieldName} 不是合法 JSON`);
  }
}

export default function CapabilityFormDrawer({ open, initialType = "model", onClose, onSuccess }) {
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!open) return;
    setForm({ ...EMPTY, type: initialType });
    setError("");
    setSubmitting(false);
  }, [initialType, open]);

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function buildPayload() {
    const t = form.type;
    const payload = {
      capability_key: form.capability_key.trim(),
      type: t,
      name: form.name.trim(),
      provider_id: form.provider_id.trim(),
      description: form.description.trim(),
      version: form.version.trim() || "1.0.0",
      credential_ref: form.credential_ref.trim(),
    };

    // 执行型：命令直接进 adapter_config，运行时按 command/args 调用。
    if (EXECUTION_TYPES.includes(t)) {
      if (!form.command.trim()) throw new Error("请输入要执行的命令");
      const adapterConfig = {
        command: form.command.trim(),
        args: parseLines(form.args),
        effect_class: form.effect_class,
      };
      if (form.cwd.trim()) adapterConfig.cwd = form.cwd.trim();
      const timeout = Number(form.timeout);
      if (Number.isFinite(timeout) && timeout > 0) adapterConfig.timeout = timeout;
      payload.adapter_config = adapterConfig;
      return payload;
    }

    // 服务型：URL + 方法 + 认证 + 头/体模板，全部归位进 adapter_config。
    if (SERVICE_TYPES.includes(t)) {
      if (!form.url.trim()) throw new Error("请输入接口地址 URL");
      const adapterConfig = {
        url: form.url.trim(),
        method: form.method,
      };
      if (form.auth_type && form.auth_type !== "none") {
        payload.auth_type = form.auth_type;
      }
      const headers = parseJsonField(form.headers_json, "请求头");
      if (headers) adapterConfig.headers = headers;
      const body = parseJsonField(form.body_json, "请求体");
      if (body) adapterConfig.body = body;
      payload.adapter_config = adapterConfig;
      payload.endpoint = form.url.trim(); // 列表卡片展示用
      return payload;
    }

    // 协议型 MCP：stdio 用启动命令，sse 用 URL。
    if (PROTOCOL_TYPES.includes(t)) {
      if (!form.mcp_target.trim()) throw new Error("请输入 MCP 启动命令或 SSE 地址");
      const adapterConfig = { transport: form.transport };
      if (form.transport === "stdio") {
        adapterConfig.server_command = form.mcp_target.trim();
      } else {
        adapterConfig.url = form.mcp_target.trim();
      }
      payload.adapter_config = adapterConfig;
      return payload;
    }

    // 模型：base_url 走 endpoint，后端归位 runtime_meta.base_url + adapter_kind=model。
    if (t === "model") {
      if (!form.model_name.trim()) throw new Error("请输入 Provider 中的调用模型 ID");
      payload.model_name = form.model_name.trim();
      payload.endpoint = form.endpoint.trim();
      return payload;
    }

    // agent / skill / workflow：组合或逻辑型，元信息登记即可。
    // agent 已另有专属「注册自定义智能体」抽屉；skill/workflow 非端点型。
    payload.endpoint = form.endpoint.trim();
    return payload;
  }

  async function submit(event) {
    event.preventDefault();
    if (!form.capability_key.trim()) return setError("请输入稳定的能力标识");
    if (!form.name.trim()) return setError("请输入能力名称");
    setSubmitting(true);
    setError("");
    try {
      const payload = buildPayload();
      const capability = await createCapability(payload);
      onSuccess?.(capability);
    } catch (err) {
      setError(err?.message || "能力注册失败");
    } finally {
      setSubmitting(false);
    }
  }

  const t = form.type;

  return (
    <TerraDrawer
      open={open}
      title="注册能力"
      description="按类型填写接入信息。密钥不进表单：仅填凭证引用（env:VAR / vault:xxx / kms:xxx），明文放环境变量。"
      onClose={onClose}
    >
      <form onSubmit={submit} className="space-y-4">
        {/* 通用字段 */}
        <div>
          <label htmlFor="capability-type" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            能力类型 *
          </label>
          <select
            id="capability-type"
            value={form.type}
            onChange={(event) => update("type", event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
          >
            {[
              ["model", "模型 Model"],
              ["agent", "智能体 Agent"],
              ["skill", "技能 Skill"],
              ["tool", "工具 Tool"],
              ["workflow", "工作流 Workflow"],
              ["connector", "连接器 Connector"],
              ["cli", "命令行 CLI"],
              ["api", "接口调用 API"],
              ["webhook", "事件回调 Webhook"],
              ["mcp", "MCP 协议"],
            ].map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </div>
        <TerraInput
          label="能力标识"
          required
          value={form.capability_key}
          onChange={(event) => update("capability_key", event.target.value)}
          hint="小写字母、数字、点、短横线或下划线，例如 tool.web-search"
          autoFocus
        />
        <TerraInput
          label="能力名称"
          required
          value={form.name}
          onChange={(event) => update("name", event.target.value)}
        />
        <TerraInput
          label="提供方"
          value={form.provider_id}
          onChange={(event) => update("provider_id", event.target.value)}
          placeholder="未填写则显示未记录"
        />

        {/* 模型专属字段 */}
        {t === "model" && (
          <>
            <TerraInput
              label="调用模型 ID"
              required
              value={form.model_name}
              onChange={(event) => update("model_name", event.target.value)}
              hint="Provider 实际接收的模型名，例如 gpt-4.1-mini"
            />
            <TerraInput
              label="网关 base_url"
              value={form.endpoint}
              onChange={(event) => update("endpoint", event.target.value)}
              placeholder="https://api.deepseek.com"
              hint="OpenAI 兼容端点（可选）。也可用上方「注册自定义模型」专属抽屉。"
            />
          </>
        )}

        {/* 执行型：tool / cli */}
        {EXECUTION_TYPES.includes(t) && (
          <>
            <TerraInput
              label="执行命令"
              required
              value={form.command}
              onChange={(event) => update("command", event.target.value)}
              placeholder="tesseract 或 python /path/script.py"
              hint="仅 cli 类型是本地命令执行通道；HTTP 工具请选 tool / api 类型。运行时按此命令调用，参数见下一行"
            />
            <div>
              <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">
                参数（每行一个，可用 {"{{变量}}"} 占位）
              </label>
              <textarea
                rows={3}
                value={form.args}
                onChange={(event) => update("args", event.target.value)}
                placeholder={"--lang eng\n{{input}}"}
                className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
              />
            </div>
            <TerraInput
              label="工作目录（可选）"
              value={form.cwd}
              onChange={(event) => update("cwd", event.target.value)}
              placeholder="/Users/you/project"
            />
            <div className="grid grid-cols-2 gap-3">
              <TerraInput
                label="超时（秒）"
                value={form.timeout}
                onChange={(event) => update("timeout", event.target.value)}
              />
              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">副作用级别</label>
                <select
                  value={form.effect_class}
                  onChange={(event) => update("effect_class", event.target.value)}
                  className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
                >
                  {EFFECT_CLASSES.map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </div>
            </div>
          </>
        )}

        {/* 服务型：api / connector / webhook */}
        {SERVICE_TYPES.includes(t) && (
          <>
            <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
              HTTP 服务调用型：tool 是通用工具端点，api/connector/webhook 是外部服务。具体认证头（如 Authorization）在下方「请求头 JSON」里填写。
            </p>
            <TerraInput
              label="接口地址 URL"
              required
              value={form.url}
              onChange={(event) => update("url", event.target.value)}
              placeholder="https://api.example.com/run"
            />
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">方法</label>
                <select
                  value={form.method}
                  onChange={(event) => update("method", event.target.value)}
                  className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
                >
                  {HTTP_METHODS.map((m) => <option key={m} value={m}>{m}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">认证方式</label>
                <select
                  value={form.auth_type}
                  onChange={(event) => update("auth_type", event.target.value)}
                  className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
                >
                  {AUTH_TYPES.map(([value, label]) => (
                    <option key={value} value={value}>{label}</option>
                  ))}
                </select>
              </div>
            </div>
            <div>
              <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">
                请求头（JSON，可选）
              </label>
              <textarea
                rows={2}
                value={form.headers_json}
                onChange={(event) => update("headers_json", event.target.value)}
                placeholder={'{"Authorization": "Bearer {{token}}"}'}
                className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">
                请求体（JSON，可选）
              </label>
              <textarea
                rows={3}
                value={form.body_json}
                onChange={(event) => update("body_json", event.target.value)}
                placeholder={'{"input": "{{text}}"}'}
                className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
              />
            </div>
            {t === "connector" && (
              <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
                连接器可在「连接器运行模式」切换真实端点 / 本地同构；此处填真实服务地址即可。
              </p>
            )}
          </>
        )}

        {/* 协议型：mcp */}
        {PROTOCOL_TYPES.includes(t) && (
          <>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5">传输方式</label>
                <select
                  value={form.transport}
                  onChange={(event) => update("transport", event.target.value)}
                  className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
                >
                  <option value="stdio">stdio（本地启动）</option>
                  <option value="sse">sse（远程地址）</option>
                </select>
              </div>
            </div>
            <TerraInput
              label={form.transport === "stdio" ? "启动命令" : "SSE 地址"}
              required
              value={form.mcp_target}
              onChange={(event) => update("mcp_target", event.target.value)}
              placeholder={form.transport === "stdio" ? "npx -y @my/mcp-server" : "https://mcp.example.com/sse"}
            />
          </>
        )}

        {/* agent / skill / workflow 提示 */}
        {(t === "agent" || t === "skill" || t === "workflow") && (
          <p className="text-xs text-ui-txt-3 bg-ui-surface-2 rounded-ui-sm p-3">
            {t === "agent"
              ? "智能体建议用上方「注册自定义智能体」专属抽屉（字段更贴合 kind/endpoint）。此处仅作元信息登记。"
              : t === "skill"
                ? "技能 Skill 是逻辑 / 知识包，不是端点。在说明里写清触发条件与处理逻辑，运行时按描述调度，可用 {{变量}} 引用上下文。"
                : "工作流 Workflow 由已有能力节点组合编排，建议在运行现场 / 工作流编辑器组合。此处仅登记元信息。"}
          </p>
        )}

        {/* 通用尾部字段 */}
        <TerraInput
          label="版本"
          value={form.version}
          onChange={(event) => update("version", event.target.value)}
        />
        <div>
          <label htmlFor="capability-description" className="block text-xs font-bold text-ui-txt-2 mb-1.5">
            能力说明
          </label>
          <textarea
            id="capability-description"
            rows={4}
            value={form.description}
            onChange={(event) => update("description", event.target.value)}
            className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none resize-y focus:ring-2 focus:ring-ui-primary/30"
          />
        </div>
        <TerraInput
          label="凭证引用（不填明文）"
          value={form.credential_ref}
          onChange={(event) => update("credential_ref", event.target.value)}
          hint="仅填 scheme:reference，密钥放环境变量。格式 env:YOUR_ENV_VAR / vault:xxx / kms:xxx"
          placeholder="env:OPENAI_API_KEY"
        />
        {error && <p className="text-xs text-ui-red">{error}</p>}
        <div className="flex justify-end gap-3 pt-2">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton type="submit" disabled={submitting}>
            {submitting ? "注册中…" : "注册能力"}
          </TerraButton>
        </div>
      </form>
    </TerraDrawer>
  );
}
