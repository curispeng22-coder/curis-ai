"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { workspaceFetch } from "../../lib/api.js";
import { usePathname } from "next/navigation";

import { getRuntimeBootstrap, runtimeErrorMessage } from "../../lib/runtimeApi.js";


const RuntimeContext = createContext(null);

function usesRuntime(pathname) {
  return pathname === "/welcome" || pathname === "/onboarding" || pathname?.startsWith("/ceo-office");
}

export function RuntimeProvider({ children }) {
  const pathname = usePathname();
  const [state, setState] = useState({
    status: "idle",
    companyId: "",
    snapshot: null,
    simulations: [],
    teams: [],
    error: "",
  });

  const refresh = useCallback(async () => {
    if (!usesRuntime(pathname)) return;
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      // T-011 首启接口返回 teams（含 status_label「待连接能力」/「就绪」），
      // 供前端团队能力展示使用；不臆造字段。
      const launch = await workspaceFetch("/api/workspace/v1/first-launch", { method: "POST" });
      const result = await getRuntimeBootstrap();
      setState({
        status: result.snapshot ? "ready" : "empty",
        companyId: result.companyId,
        snapshot: result.snapshot,
        simulations: result.simulations,
        teams: Array.isArray(launch?.teams) ? launch.teams : [],
        error: "",
      });
    } catch (error) {
      setState({
        status: error?.status === 403 || error?.status === 404 ? "forbidden" : "error",
        companyId: "",
        snapshot: null,
        simulations: [],
        teams: [],
        error: runtimeErrorMessage(error),
      });
    }
  }, [pathname]);

  useEffect(() => {
    // Let the server-rendered loading tree hydrate before an immediate API error
    // swaps it out; this also keeps soft navigation and full reload consistent.
    const timer = window.setTimeout(refresh, 250);
    return () => window.clearTimeout(timer);
  }, [refresh]);

  const value = useMemo(() => ({ ...state, refresh }), [refresh, state]);
  return <RuntimeContext.Provider value={value}>{children}</RuntimeContext.Provider>;
}

export function useRuntime() {
  const value = useContext(RuntimeContext);
  if (!value) throw new Error("useRuntime requires RuntimeProvider");
  return value;
}
