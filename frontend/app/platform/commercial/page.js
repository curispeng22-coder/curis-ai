"use client";

// DEPRECATED: 商业运营面板，L2 冻结，v1 自用不渲染

import Link from "next/link";
import { useCallback, useState } from "react";
import CommercialConsolePanel from "./CommercialConsolePanel";

// 商业运营控制台独立路由页（Phase-9A Console MVP）。
// 自含最小管理员令牌输入与 apiFetch（与 platform/page.js 同构的少量复制），
// 仅调用 /api/platform/*，绝不 mutation、绝不触碰 /api/workspace/*。

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000";
const DEFAULT_ADMIN_TOKEN = "platform-admin-dev";

export default function CommercialConsolePage() {
  const [token, setToken] = useState(DEFAULT_ADMIN_TOKEN);
  const [message, setMessage] = useState("");

  const apiFetch = useCallback(
    async (path, options = {}) => {
      const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...(options.headers || {}),
      };
      const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
      if (response.status === 401) {
        throw new Error("鉴权失败：管理员令牌无效（请在顶部填写正确令牌）");
      }
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(payload.detail || `请求失败：${path}`);
      }
      return payload;
    },
    [token],
  );

  return (
    <main className="min-h-screen bg-zinc-100 px-4 py-8 text-zinc-950">
      <section className="mx-auto max-w-6xl">
        <header className="border-b border-zinc-300 pb-4">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <h1 className="text-2xl font-black">Commercial Operation Console</h1>
            <Link
              href="/"
              className="rounded-md border border-zinc-300 px-3 py-2 text-xs font-bold text-zinc-700"
            >
              ← 返回工作台
            </Link>
          </div>
          <p className="mt-2 max-w-4xl text-sm text-zinc-600">
            Phase-9A Console MVP：商业运营只读聚合控制台。仅调用 /api/platform/*，绝不 mutation，
            绝不触碰 /api/workspace/*。所有商业配置修改仍在 /platform 各 TAB 完成。
          </p>
        </header>

        <div className="mt-4 flex flex-wrap items-center gap-3 rounded-md border border-zinc-200 bg-white p-3 shadow-sm">
          <label className="text-xs font-bold text-zinc-500" htmlFor="commercial-token">
            管理员令牌
          </label>
          <input
            id="commercial-token"
            className="min-w-[16rem] flex-1 rounded-md border border-zinc-300 px-3 py-2 font-mono text-xs"
            value={token}
            onChange={(event) => setToken(event.target.value)}
          />
        </div>

        {message ? (
          <div className="mt-4 rounded-md bg-white p-3 text-sm font-bold text-zinc-700 shadow-sm">
            {message}
          </div>
        ) : null}

        <div className="mt-5">
          <CommercialConsolePanel apiFetch={apiFetch} onMessage={setMessage} />
        </div>
      </section>
    </main>
  );
}
