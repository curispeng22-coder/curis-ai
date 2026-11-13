"use client";

// 我的凭证（Self-use v1 · Wave 2 V1 单账号 Vault + cookie）
// 创始人单页：粘贴平台 cookie + 自有 AI key → 存 Vault（local-dev 单用户，
// 明文不落库，仅存摘要）。引用格式统一 <scheme>://tenant/selfuse/credential/<id>。
// 与后端 /api/credential/* 对接（复用 CredentialVaultService）。

import { useCallback, useEffect, useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const TENANT_ID = process.env.NEXT_PUBLIC_CURIS_TENANT_ID || "selfuse";

const PLATFORM_OPTIONS = [
  { value: "social_platform_douyin", label: "抖音 cookie" },
  { value: "social_platform_xhs", label: "小红书 cookie" },
  { value: "social_platform_video_account", label: "视频号 cookie" },
  { value: "social_platform_bilibili", label: "B站 cookie" },
  { value: "social_platform_kuaishou", label: "快手 cookie" },
  { value: "social_platform_tiktok", label: "TikTok cookie" },
  { value: "social_platform_youtube", label: "YouTube cookie" },
  { value: "model_gateway", label: "自有 AI key" },
];

function maskRef(ref) {
  if (!ref) return "";
  const i = ref.lastIndexOf("/");
  return ref.slice(0, i + 1) + "••••";
}

export default function SecretVaultPage() {
  const [credentials, setCredentials] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "",
    provider: "social_platform_douyin",
    credential_type: "cookie",
    secret: "",
  });
  const [busy, setBusy] = useState(false);
  const [toast, setToast] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API_BASE}/api/credential`, {
        headers: { "X-Tenant-Id": TENANT_ID },
        cache: "no-store",
      });
      const payload = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(payload.detail || "读取失败");
      setCredentials(payload.credentials || []);
    } catch (err) {
      setError(err.message || "凭证读取失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const onProviderChange = (provider) => {
    const isKey = provider === "model_gateway";
    setForm((f) => ({
      ...f,
      provider,
      credential_type: isKey ? "api_key" : "cookie",
      name: isKey ? "自有 AI key" : f.name,
    }));
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!form.secret.trim()) {
      setError("请粘贴凭证内容（cookie 或 AI key）");
      return;
    }
    setBusy(true);
    setError("");
    setToast("");
    try {
      const res = await fetch(`${API_BASE}/api/credential`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-Tenant-Id": TENANT_ID },
        body: JSON.stringify(form),
      });
      const payload = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(payload.detail || "保存失败");
      setToast(`已存入 Vault：${maskRef(payload.credential_ref)}（明文不落库）`);
      setForm((f) => ({ ...f, secret: "" }));
      await load();
    } catch (err) {
      setError(err.message || "保存失败");
    } finally {
      setBusy(false);
    }
  };

  const onTest = async (id) => {
    try {
      const res = await fetch(`${API_BASE}/api/credential/${id}/test`, {
        method: "POST",
        headers: { "X-Tenant-Id": TENANT_ID },
      });
      const payload = await res.json().catch(() => ({}));
      setToast(`测试 ${id}：${payload.status || "unknown"}`);
    } catch (err) {
      setError(err.message || "测试失败");
    }
  };

  return (
    <main style={{ maxWidth: 980, margin: "0 auto", padding: "var(--ui-sp-8) var(--ui-sp-6)", color: "var(--ui-text)" }}>
      <h1 style={{ fontSize: "var(--ui-fs-7)", marginBottom: "var(--ui-sp-1)" }}>我的凭证</h1>
      <p style={{ color: "var(--ui-text-2)", marginBottom: "var(--ui-sp-6)" }}>
        单账号 Vault（local-dev）。粘贴平台 cookie 或自有 AI key；明文仅驻留进程内存，
        库内只存摘要与引用。引用格式：<code>local-dev://tenant/selfuse/credential/&lt;id&gt;</code>。
      </p>

      {toast ? (
        <div style={{ background: "var(--ui-surface-2)", color: "var(--ui-success)", padding: "var(--ui-sp-2) var(--ui-sp-3)", borderRadius: "var(--ui-r-sm)", marginBottom: "var(--ui-sp-4)", border: "1px solid var(--ui-line)" }}>
          {toast}
        </div>
      ) : null}
      {error ? (
        <div style={{ background: "var(--ui-surface-2)", color: "var(--ui-danger)", padding: "var(--ui-sp-2) var(--ui-sp-3)", borderRadius: "var(--ui-r-sm)", marginBottom: "var(--ui-sp-4)", border: "1px solid var(--ui-line)" }}>
          {error}
        </div>
      ) : null}

      <section style={{ border: "1px solid var(--ui-line)", borderRadius: "var(--ui-r-md)", padding: "var(--ui-sp-5)", marginBottom: "var(--ui-sp-7)", background: "var(--ui-surface)" }}>
        <h2 style={{ fontSize: "var(--ui-fs-5)", marginBottom: "var(--ui-sp-4)" }}>新增凭证</h2>
        <form onSubmit={onSubmit} style={{ display: "grid", gap: "var(--ui-sp-3)" }}>
          <label style={{ display: "grid", gap: "var(--ui-sp-1)" }}>
            <span>类型</span>
            <select
              value={form.provider}
              onChange={(e) => onProviderChange(e.target.value)}
              style={FIELD}
            >
              {PLATFORM_OPTIONS.map((o) => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </label>
          <label style={{ display: "grid", gap: "var(--ui-sp-1)" }}>
            <span>名称（可选）</span>
            <input
              value={form.name}
              onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
              placeholder="如：抖音主号 cookie"
              style={FIELD}
            />
          </label>
          <label style={{ display: "grid", gap: "var(--ui-sp-1)" }}>
            <span>凭证内容（cookie / api_key，单值）</span>
            <textarea
              value={form.secret}
              onChange={(e) => setForm((f) => ({ ...f, secret: e.target.value }))}
              rows={5}
              placeholder="粘贴平台 cookie 字符串或 AI key"
              style={{ ...FIELD, fontFamily: "var(--ui-mono)" }}
            />
          </label>
          <button
            type="submit"
            disabled={busy}
            style={{ justifySelf: "start", padding: "var(--ui-sp-2) var(--ui-sp-5)", minHeight: "var(--ui-ctl-h)", borderRadius: "var(--ui-r-sm)", border: "none", background: "var(--ui-action-primary-bg)", color: "var(--ui-action-primary-fg)", fontSize: "var(--ui-fs-3)", fontWeight: 600, cursor: "pointer" }}
          >
            {busy ? "保存中…" : "存入 Vault"}
          </button>
        </form>
      </section>

      <section>
        <h2 style={{ fontSize: "var(--ui-fs-5)", marginBottom: "var(--ui-sp-3)" }}>已存凭证</h2>
        {loading ? (
          <p style={{ color: "var(--ui-text-2)" }}>读取中…</p>
        ) : credentials.length === 0 ? (
          <p style={{ color: "var(--ui-text-2)" }}>暂无凭证。上方添加第一条。</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse", background: "var(--ui-surface)", borderRadius: "var(--ui-r-md)", overflow: "hidden", border: "1px solid var(--ui-line)" }}>
            <thead>
              <tr style={{ background: "var(--ui-surface-2)", textAlign: "left" }}>
                <th style={th}>名称</th>
                <th style={th}>provider</th>
                <th style={th}>类型</th>
                <th style={th}>引用（脱敏）</th>
                <th style={th}>状态</th>
                <th style={th}></th>
              </tr>
            </thead>
            <tbody>
              {credentials.map((c) => (
                <tr key={c.credential_id} style={{ borderTop: "1px solid var(--ui-line)" }}>
                  <td style={td}>{c.name}</td>
                  <td style={td}>{c.provider}</td>
                  <td style={td}>{c.credential_type}</td>
                  <td style={{ ...td, fontFamily: "var(--ui-mono)", fontSize: "var(--ui-fs-1)" }}>{maskRef(c.credential_ref)}</td>
                  <td style={td}>{c.status}</td>
                  <td style={td}>
                    <button onClick={() => onTest(c.credential_id)} style={linkBtn}>测试</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </main>
  );
}

// Frozen 令牌（2026-08-05 总控裁定：视觉一律走 --ui-*，禁止写死 hex/px）
const FIELD = {
  padding: "var(--ui-sp-2) var(--ui-sp-3)", minHeight: "var(--ui-ctl-h)",
  borderRadius: "var(--ui-r-sm)", border: "1px solid var(--ui-line)",
  background: "var(--ui-surface-2)", color: "var(--ui-text)",
  fontSize: "var(--ui-fs-3)", outline: "none",
};
const th = { padding: "var(--ui-sp-2) var(--ui-sp-3)", fontSize: "var(--ui-fs-2)", color: "var(--ui-text-2)" };
const td = { padding: "var(--ui-sp-2) var(--ui-sp-3)", fontSize: "var(--ui-fs-2)", color: "var(--ui-text)" };
const linkBtn = {
  padding: "var(--ui-sp-1) var(--ui-sp-3)", minHeight: "var(--ui-ctl-h-sm)",
  borderRadius: "var(--ui-r-sm)", border: "1px solid var(--ui-line)",
  background: "var(--ui-surface-2)", color: "var(--ui-text)",
  cursor: "pointer", fontSize: "var(--ui-fs-1)",
};
