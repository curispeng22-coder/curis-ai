"use client";

import { useEffect, useState } from "react";
import { safeReturnPath } from "../../lib/auth.mjs";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "/gateway";

export default function LoginPage() {
  const [message, setMessage] = useState("正在检查本地 Owner…");
  const [initialized, setInitialized] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [nextPath, setNextPath] = useState("/ceo-office");

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    const next = safeReturnPath(query.get("next"), window.location.origin);
    setNextPath(next);
    fetch(`${API_BASE}/api/auth/local/status`, {
      cache: "no-store",
      credentials: "include",
    })
      .then(async (response) => {
        if (!response.ok) throw new Error("status unavailable");
        return response.json();
      })
      .then((status) => {
        if (status.authenticated) {
          window.location.replace(next);
          return;
        }
        setInitialized(Boolean(status.initialized));
        setMessage(
          status.initialized
            ? "本地 Owner 已创建，进入你的个人 AI Workspace。"
            : "首次启动只需创建本地 Owner，无需 Google 账号或外部网络。"
        );
      })
      .catch(() => {
        setInitialized(null);
        setMessage("认证服务暂时不可用，请确认 Curis 已完整启动。");
      });
  }, []);

  async function enterWorkspace() {
    setSubmitting(true);
    setMessage(initialized ? "正在进入 Workspace…" : "正在创建本地 Owner…");
    try {
      const action = initialized ? "session" : "initialize";
      const response = await fetch(
        `${API_BASE}/api/auth/local/${action}?${new URLSearchParams({ next: nextPath })}`,
        { method: "POST", credentials: "include" }
      );
      const payload = await response.json();
      if (!response.ok) throw new Error(payload?.detail || "本地 Owner 初始化失败");
      window.location.replace(safeReturnPath(payload.next, window.location.origin));
    } catch (error) {
      setMessage(error?.message || "本地 Owner 初始化失败");
      setSubmitting(false);
    }
  }

  return (
    <main
      className="flex min-h-[100dvh] items-center justify-center bg-ui-bg px-5 text-ui-txt"
      style={{ display: "flex", minHeight: "100dvh", alignItems: "center", justifyContent: "center", padding: "20px" }}
    >
      <section
        className="w-full max-w-md rounded-xl border border-ui-line bg-ui-surface p-8 shadow-ui-3"
        style={{ width: "min(28rem, calc(100vw - 40px))", boxSizing: "border-box" }}
      >
        <p className="text-xs font-black uppercase tracking-[0.2em] text-ui-txt-2">Curis Local Desktop</p>
        <h1 className="mt-3 text-3xl font-black tracking-tight">登录 Curis</h1>
        <p className="mt-4 text-sm leading-6 text-ui-txt-2">{message}</p>
        <button
          type="button"
          disabled={initialized === null || submitting}
          onClick={enterWorkspace}
          className="mt-7 inline-flex w-full justify-center rounded-lg bg-ui-primary px-5 py-3 text-sm font-black text-ui-primary-fg hover:bg-ui-primary-dark disabled:cursor-not-allowed disabled:opacity-50"
        >
          {submitting ? "处理中…" : initialized ? "进入 Curis" : "创建本地 Owner"}
        </button>
        <p className="mt-4 text-xs leading-5 text-ui-txt-3">
          身份仅保存在这台 Mac 的本地 Curis 数据库和当前 HttpOnly Session 中。
        </p>
      </section>
    </main>
  );
}
