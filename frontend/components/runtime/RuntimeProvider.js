"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
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
    error: "",
  });

  const refresh = useCallback(async () => {
    if (!usesRuntime(pathname)) return;
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      const result = await getRuntimeBootstrap();
      setState({
        status: result.snapshot ? "ready" : "empty",
        companyId: result.companyId,
        snapshot: result.snapshot,
        simulations: result.simulations,
        error: "",
      });
    } catch (error) {
      setState({
        status: error?.status === 403 || error?.status === 404 ? "forbidden" : "error",
        companyId: "",
        snapshot: null,
        simulations: [],
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
