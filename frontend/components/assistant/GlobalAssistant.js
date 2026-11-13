"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useReducer,
  useRef,
  useState,
} from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import {
  INITIAL_ASSISTANT_STATE,
  assistantReducer,
  normalizeAssistantContext,
} from "../../lib/assistantState.mjs";
import { workspaceEntryHref } from "../../lib/runtimeApi.js";
import { TerraIcon } from "../terra/TerraIcons.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import { getCompanyAttention, getCEOAssistantConversation, sendCEOAssistantMessage, conversationError } from "../../lib/v1FrontendApi.js";
import SharedConversation from "../v1/SharedConversation.js";

export function clampAssistantPosition(position, width, height, viewportWidth, viewportHeight) {
  return { left: Math.max(8, Math.min(Math.max(8, viewportWidth - width - 8), position.left)),
    top: Math.max(8, Math.min(Math.max(8, viewportHeight - height - 8), position.top)) };
}


const AssistantContext = createContext(null);
const WORKSPACE_PREFIXES = [
  "/ceo-office",
  "/projects",
  "/employees",
  "/capabilities",
  "/org-center",
];

function isWorkspacePath(pathname) {
  return WORKSPACE_PREFIXES.some(
    (prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`)
  );
}

function canonicalAssistantIdentity(snapshot) {
  const assistant = snapshot?.assistant;
  const data = assistant?.data || assistant || {};
  return {
    name: data.name || data.display_name || "CEO 助理",
    avatar: data.avatar || "AI",
    role: data.role || "公司级协调与经营跟进",
    canonical_ref: assistant?.entity_id || assistant?.assistant_id || null,
  };
}

function runtimeAssistantSnapshot(runtime, attention) {
  const snapshot = runtime.snapshot;
  const workspaces = snapshot?.workspaces || [];
  const employees = snapshot?.organization?.employees || [];
  const activeEmployees = employees.filter((employee) => employee.lifecycle_status !== "PROPOSED");
  const proposedEmployees = employees.length - activeEmployees.length;
  const workforceCount = activeEmployees.length + (snapshot?.assistant ? 1 : 0);
  const pending = (attention.items || []).map((item) => ({
    id: item.source_ref || item.reference_id || item.id,
    title: item.summary,
    status: "请在 CEO 工作台查看原事项",
  }));
  const watching = workspaces.map((workspace) => ({
    id: workspace.workspace_id,
    title: workspace.name,
    status: "查看工作空间",
    href: workspaceEntryHref(workspace.workspace_id),
  }));
  return {
    identity: canonicalAssistantIdentity(snapshot),
    brief: {
      summary: snapshot?.company
        ? `${snapshot.company.name} 当前有 ${workspaces.length} 个工作空间、${workforceCount} 位 AI 员工${proposedEmployees ? `，另有 ${proposedEmployees} 位候选方案待审查` : ""}。`
        : "公司尚未建立，先完成创办引导。",
      counts: {
        workspaces: workspaces.length,
        employees: workforceCount,
        proposedEmployees,
        attention: pending.length,
      },
    },
    pending,
    watching,
  };
}

export function GlobalAssistantProvider({ children }) {
  const pathname = usePathname();
  const runtime = useRuntime();
  const [state, dispatch] = useReducer(assistantReducer, INITIAL_ASSISTANT_STATE);

  // Compatibility callback only: opening this panel cannot acknowledge a Result or Decision.
  const markRead = useCallback(() => {}, []);

  const refresh = useCallback(async () => {
    if (!isWorkspacePath(pathname)) return;
    dispatch({ type: "loading" });
    try {
      const attention = runtime.companyId ? await getCompanyAttention(runtime.companyId) : { items: [] };
      dispatch({
        type: "loaded",
        snapshot: runtimeAssistantSnapshot(runtime, attention),
        notifications: [],
        unreadCount: attention.items.length,
      });
    } catch (error) {
      dispatch({
        type: "error",
        value: "暂时无法读取关注事项，请稍后重新打开。",
      });
    }
  }, [pathname, runtime]);

  useEffect(() => {
    refresh();
    if (!isWorkspacePath(pathname)) return undefined;
    const timer = window.setInterval(refresh, 30000);
    return () => window.clearInterval(timer);
  }, [pathname, refresh]);

  useEffect(() => {
    if (state.open && state.notifications.length) {
      markRead(state.notifications);
    }
  }, [markRead, state.notifications, state.open]);

  const openAssistant = useCallback(() => {
    dispatch({ type: "open" });
  }, []);
  const closeAssistant = useCallback(() => {
    dispatch({ type: "close" });
  }, []);
  const minimizeAssistant = useCallback(() => {
    dispatch({ type: "minimize" });
  }, []);
  const setPageContext = useCallback((value) => {
    dispatch({ type: "context", value });
  }, []);
  const value = useMemo(() => ({
    ...state,
    openAssistant,
    closeAssistant,
    minimizeAssistant,
    setPageContext,
    refresh,
    markRead,
  }), [
    closeAssistant,
    markRead,
    minimizeAssistant,
    openAssistant,
    refresh,
    setPageContext,
    state,
  ]);

  return (
    <AssistantContext.Provider value={value}>
      {children}
      <GlobalAssistantHost />
    </AssistantContext.Provider>
  );
}

export function useGlobalAssistant() {
  const value = useContext(AssistantContext);
  if (!value) {
    throw new Error("useGlobalAssistant requires GlobalAssistantProvider");
  }
  return value;
}

export function useAssistantPageContext(value) {
  const { setPageContext } = useGlobalAssistant();
  const contextKey = JSON.stringify(normalizeAssistantContext(value));
  useEffect(() => {
    setPageContext(JSON.parse(contextKey));
  }, [contextKey, setPageContext]);
}

function GlobalAssistantHost() {
  const pathname = usePathname();
  const assistant = useGlobalAssistant();
  const runtime = useRuntime();
  const closeAssistant = assistant.closeAssistant;
  const minimizeAssistant = assistant.minimizeAssistant;
  const panel = useRef(null);
  const trigger = useRef(null);
  const [triggerPosition, setTriggerPosition] = useState({ left: 16, bottom: 16 });
  const drag = useRef(null);
  const sending = useRef(false);
  const currentCompany = useRef(runtime.companyId);
  const [position, setPosition] = useState(null);
  const [conversation, setConversation] = useState(null);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  useEffect(() => { currentCompany.current = runtime.companyId; setConversation(null); setInput(""); setError(""); }, [runtime.companyId]);
  useEffect(() => {
    if (!assistant.open || !runtime.companyId) return undefined;
    let active = true;
    getCEOAssistantConversation(runtime.companyId).then((value) => {
      if (active) { setConversation(value); setError(""); }
    }).catch(() => { if (active) setError("暂时无法读取对话，请收起后重新打开。"); });
    return () => { active = false; };
  }, [assistant.open, runtime.companyId, pathname]);
  const send = async (event, model) => {
    event.preventDefault();
    if (sending.current || !input.trim() || !runtime.companyId) return;
    const company = runtime.companyId;
    sending.current = true; setBusy(true); setError("");
    try {
      const response = await sendCEOAssistantMessage(company, {
        message: input.trim(), model_key: model?.capability_id || model?.model_key || "", references: [],
      });
      if (currentCompany.current === company) {
        setConversation((value) => ({ ...value, messages: response.messages })); setInput("");
      }
    } catch (caught) {
      if (currentCompany.current === company) setError(conversationError(caught, "助理暂时无法回复，输入已保留，请稍后重试。"));
    } finally { sending.current = false; setBusy(false); }
  };
  const collapse = (action) => {
    action(); window.requestAnimationFrame(() => trigger.current?.focus());
  };
  useEffect(() => { closeAssistant(); setPosition(null); }, [runtime.companyId, closeAssistant]);
  useEffect(() => {
    const locate = () => {
      const anchor = [...document.querySelectorAll("[data-d0-assistant-anchor]")].find((node) => node.getClientRects().length);
      const rect = anchor?.getBoundingClientRect();
      const next = rect ? { left: rect.left, top: rect.top } : { left: 16, top: window.innerHeight - 48 };
      setTriggerPosition((value) => value.left === next.left && value.top === next.top ? value : next);
    };
    locate();
    const observer = new MutationObserver(locate); observer.observe(document.body, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden", "style", "class"] });
    window.addEventListener("resize", locate);
    return () => { observer.disconnect(); window.removeEventListener("resize", locate); };
  }, [pathname]);
  useEffect(() => {
    if (!assistant.open) return undefined;
    const clamp = () => {
      const rect = panel.current?.getBoundingClientRect(); if (!rect) return;
      setPosition((value) => {
        const next = clampAssistantPosition(value || { left: 205, top: window.innerHeight - rect.height - 88 }, rect.width, rect.height, window.innerWidth, window.innerHeight);
        return value?.left === next.left && value?.top === next.top ? value : next;
      });
    };
    const escape = (event) => {
      if (event.key === "Escape" && !event.defaultPrevented && !document.querySelector('dialog[open][aria-modal="true"]')) {
        minimizeAssistant(); window.requestAnimationFrame(() => trigger.current?.focus());
      }
    };
    clamp(); const observer = new ResizeObserver(clamp); if (panel.current) observer.observe(panel.current);
    window.addEventListener("resize", clamp); window.addEventListener("keydown", escape);
    return () => { observer.disconnect(); window.removeEventListener("resize", clamp); window.removeEventListener("keydown", escape); };
  }, [assistant.open, minimizeAssistant]);
  const beginDrag = (event) => {
    if (event.button !== 0 || event.target.closest("button")) return;
    const rect = panel.current.getBoundingClientRect();
    drag.current = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    event.currentTarget.setPointerCapture(event.pointerId);
  };
  const moveDrag = (event) => {
    if (!drag.current) return;
    const rect = panel.current.getBoundingClientRect();
    setPosition(clampAssistantPosition({ left: event.clientX - drag.current.x, top: event.clientY - drag.current.y }, rect.width, rect.height, window.innerWidth, window.innerHeight));
  };

  if (!isWorkspacePath(pathname)) return null;

  const canonicalRef = canonicalAssistantIdentity(runtime.snapshot).canonical_ref;
  const verified = Boolean(canonicalRef && conversation?.assistant?.assistant_id === canonicalRef);
  const displayName = verified ? conversation.assistant.name || "CEO 助理" : "CEO 助理";
  const displayRole = verified ? conversation.assistant.role || "公司级协调与经营跟进" : "正在核验当前公司身份";

  return (
    <>
      {!assistant.open && (
        <button
          ref={trigger}
          type="button"
          style={triggerPosition}
          aria-expanded={assistant.open}
          onClick={assistant.openAssistant}
          aria-label="打开 Assistant"
          className="fixed z-40 grid h-8 w-8 place-items-center rounded-md border border-ui-line bg-ui-surface text-ui-primary hover:bg-ui-primary-soft"
        >
          <TerraIcon name="i-auto_awesome" className="h-5 w-5" />
          {assistant.unreadCount > 0 && (
            <span className="absolute -right-1 -top-1 min-w-5 rounded-full bg-ui-red px-1 text-ui-1 font-bold leading-5 text-ui-primary-fg">
              {Math.min(assistant.unreadCount, 99)}
            </span>
          )}
        </button>
      )}

      {assistant.open && (
        <section
          ref={panel}
          role="dialog"
          aria-label="Global Assistant"
          data-assistant-id={verified ? canonicalRef : ""}
          style={position || { bottom: 88, left: 205 }}
          className="fixed z-50 flex max-h-[65vh] w-[min(390px,calc(100vw-24px))] flex-col overflow-hidden rounded-ui-lg border border-ui-line bg-ui-surface"
        >
          <header onPointerDown={beginDrag} onPointerMove={moveDrag} onPointerUp={() => { drag.current = null; }} onPointerCancel={() => { drag.current = null; }}
            title="拖动移动助理" className="flex touch-none cursor-move select-none items-start gap-3 border-b border-ui-line px-4 py-3">
            <div className="grid h-9 w-9 flex-shrink-0 place-items-center rounded-full bg-ui-primary-soft text-sm font-bold text-ui-primary">
              {verified && assistant.identity.canonical_ref === canonicalRef ? assistant.identity.avatar : <TerraIcon name="i-auto_awesome" className="h-4 w-4" />}
            </div>
            <div className="min-w-0 flex-1">
              <h2 className="truncate font-ui-sans text-sm font-semibold text-ui-txt">
                {displayName}
              </h2>
              <p className="truncate text-ui-1 text-ui-txt-3">{displayRole}</p>
            </div>
            <button
              type="button"
              onClick={() => collapse(assistant.minimizeAssistant)}
              className="rounded p-1 text-ui-txt-3 hover:bg-ui-surface-2"
              aria-label="最小化 Assistant"
            >
              <span aria-hidden="true">—</span>
            </button>
            <button
              type="button"
              onClick={() => collapse(assistant.closeAssistant)}
              className="rounded p-1 text-ui-txt-3 hover:bg-ui-surface-2"
              aria-label="关闭 Assistant"
            >
              <TerraIcon name="i-close" className="h-4 w-4" />
            </button>
          </header>

          <div className="flex-1 space-y-3 overflow-y-auto p-4">
            {verified ? <SharedConversation
              scopeKey={`${runtime.companyId}:${conversation?.assistant?.assistant_id || ""}`}
              employee={{ ...conversation?.assistant, name: conversation?.assistant?.name || displayName, role: displayRole }}
              messages={conversation?.messages || []} value={input} onChange={setInput} onSubmit={send} busy={busy}
              placeholder="向 CEO 助理说说你想推进什么…"
            /> : <p role="status" className="text-sm text-ui-txt-2">{runtime.companyId ? "当前公司助理身份尚未核验，输入暂不可用。" : "建立公司后，助理会在这里陪你继续工作。"}</p>}
            {error ? <p role="alert" className="text-sm text-ui-red">{error}</p> : null}
            {verified && assistant.identity.canonical_ref === canonicalRef && <details>
              <summary className="cursor-pointer text-xs text-ui-txt-2">当前公司概况</summary>
                <AssistantSection title="今日简报">
                  <p className="text-xs leading-relaxed text-ui-txt-2">
                    {assistant.snapshot?.brief?.summary || "正在读取当前 Workspace 状态。"}
                  </p>
                  {assistant.snapshot?.brief?.counts && (
                    <div className="mt-2 grid grid-cols-3 gap-2">
                      <AssistantFact
                        value={assistant.snapshot.brief.counts.workspaces}
                        label="工作空间"
                      />
                      <AssistantFact
                        value={assistant.snapshot.brief.counts.employees}
                        label="AI 员工"
                      />
                      <AssistantFact
                        value={assistant.snapshot.brief.counts.attention}
                        label="需要关注"
                      />
                    </div>
                  )}
                </AssistantSection>

                <AssistantSection
                  title="待处理"
                  count={assistant.snapshot?.pending?.length || 0}
                >
                  <AssistantItems
                    items={assistant.snapshot?.pending || []}
                    empty="当前没有等待 CEO 的运行事项。"
                  />
                </AssistantSection>

                <AssistantSection title="我正在关注" count={assistant.snapshot?.watching?.length || 0}>
                  <AssistantLinks
                    items={assistant.snapshot?.watching || []}
                    empty="当前没有已配置的工作空间。"
                  />
                </AssistantSection>

              </details>}
            {assistant.error && (
              <div role="alert" className="rounded-ui-sm bg-ui-red-soft px-3 py-2 text-xs text-ui-red">
                {assistant.error}
              </div>
            )}
          </div>

          <footer className="border-t border-ui-line p-3 text-xs leading-relaxed text-ui-txt-3">
            <Link href="/ceo-office" className="text-ui-primary">查看 CEO 工作台关注事项 →</Link>
          </footer>
        </section>
      )}
    </>
  );
}

function AssistantSection({ title, count, children }) {
  return (
    <section className="rounded-ui-sm border border-ui-line bg-ui-bg p-3">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="text-xs font-bold text-ui-txt">{title}</h3>
        {typeof count === "number" && (
          <span className="rounded-full bg-ui-surface-2 px-2 py-0.5 text-ui-1 text-ui-txt-3">
            {count}
          </span>
        )}
      </div>
      {children}
    </section>
  );
}

function AssistantFact({ value, label }) {
  return (
    <div className="rounded-ui-sm bg-ui-surface px-2 py-1.5 text-center">
      <div className="font-ui-sans text-sm font-bold text-ui-primary">{value}</div>
      <div className="text-ui-1 text-ui-txt-3">{label}</div>
    </div>
  );
}

function AssistantItems({ items, empty }) {
  if (!items.length) {
    return <p className="text-ui-1 text-ui-txt-3">{empty}</p>;
  }
  return (
    <div className="max-h-32 space-y-1.5 overflow-y-auto">
      {items.map((item) => (
        <div
          key={item.notification_id || item.id}
          className="rounded-ui-sm bg-ui-surface px-2.5 py-2"
        >
          <div className="text-ui-1 font-semibold text-ui-txt">
            {item.title}
          </div>
          {(item.status || item.event_type) && (
            <div className="mt-0.5 text-ui-1 text-ui-txt-3">
              {item.status || item.event_type}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function AssistantLinks({ items, empty }) {
  if (!items.length) return <p className="text-ui-1 text-ui-txt-3">{empty}</p>;
  return (
    <div className="space-y-1.5">
      {items.map((item) => (
        <Link
          key={item.id}
          href={item.href || "/ceo-office/workspace"}
          className="flex items-center justify-between gap-2 rounded-ui-sm bg-ui-surface px-2.5 py-2 text-ui-1 no-underline"
        >
          <span className="truncate font-semibold text-ui-txt">{item.title}</span>
          <span className="flex-shrink-0 text-ui-txt-3">{item.status}</span>
        </Link>
      ))}
    </div>
  );
}
