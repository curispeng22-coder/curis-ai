"use client";

import { useEffect, useId, useLayoutEffect, useRef, useState } from "react";
import { usePathname } from "next/navigation";
import { TerraIcon, TerraIconSprite } from "../terra/TerraIcons.js";
import V1Sidebar from "../v1/V1Sidebar.js";
import { useRuntime } from "../runtime/RuntimeProvider.js";
import { searchCompanyObjects } from "../../lib/v1FrontendApi.js";
import { OBJECT_GROUPS, groupMeta, objectHref } from "../../lib/objectSearchState.mjs";
import styles from "./WorkspacePaneShell.module.css";

const DEFAULTS = { context: false, utility: false, contextWidth: 210, utilityWidth: 340 };
export function paneScopeKey(companyId, workspaceId, surfaceId) {
  return "curis.d0.panes." + JSON.stringify([companyId || "unselected", workspaceId || "", surfaceId || ""]);
}
export function paneWidth(kind, width) {
  const min = kind === "context" ? 170 : 280, max = kind === "context" ? 320 : 480;
  return Math.max(min, Math.min(max, Number.isFinite(width) ? width : DEFAULTS[kind + "Width"]));
}
export function paneGeometry(width, navigation, context, utility, contextWidth, utilityWidth, lastOpened) {
  const navWidth = navigation ? (width <= 1100 ? 158 : 190) : 0;
  const room = Math.max(0, width - navWidth);
  let overlay = null, suppress = null;
  if (room - (context ? contextWidth : 0) - (utility ? utilityWidth : 0) < 600) {
    overlay = context && utility ? lastOpened : utility ? "utility" : context ? "context" : null;
    const other = overlay === "context" ? "utility" : "context";
    if (overlay && room - (other === "context" && context ? contextWidth : other === "utility" && utility ? utilityWidth : 0) < 600) suppress = other;
  }
  return { navWidth, overlay, suppress };
}
export function sanitizePanePreferences(value = {}) {
  return { context: value.context === true, utility: value.utility === true,
    contextWidth: paneWidth("context", value.contextWidth), utilityWidth: paneWidth("utility", value.utilityWidth) };
}
export function initialPanePreferences(saved, initial = {}, legacy = {}) {
  return sanitizePanePreferences(saved && typeof saved === "object" ? saved : { ...initial, contextWidth: legacy.contextWidth, utilityWidth: legacy.utilityWidth });
}
function readPreferences(key, workspaceId, initial = DEFAULTS) {
  if (typeof window === "undefined") return initialPanePreferences(null, initial);
  try {
    const current = window.sessionStorage.getItem(key);
    // Read legacy width preferences only; new instances start with Nav + Main.
    const legacy = current ? {} : JSON.parse(window.localStorage.getItem("curis.workspace-pane." + (workspaceId || "unselected")) || "{}");
    return initialPanePreferences(current ? JSON.parse(current) : null, initial, legacy);
  } catch { return initialPanePreferences(null, initial); }
}
function readNavigation(key) {
  try { return window.sessionStorage.getItem(key) !== "false"; } catch { return true; }
}
export function utilityTabState(state, action, available) {
  const blank = (id) => /^new:\d+-\d+$/.test(id);
  const ids = [...new Set((state?.ids || []).filter((id) => available.includes(id) || blank(id)))];
  if (action.type === "select" && available.includes(action.id)) {
    const index = ids.indexOf(state?.active);
    if (index >= 0 && blank(state.active)) ids.splice(index, 1);
  }
  if ((action.type === "open" || action.type === "select" || action.type === "new") && (available.includes(action.id) || action.type === "new" && blank(action.id)) && !ids.includes(action.id)) ids.push(action.id);
  if (action.type === "close") ids.splice(ids.indexOf(action.id), ids.includes(action.id) ? 1 : 0);
  const active = ["open", "select", "new"].includes(action.type) && ids.includes(action.id) ? action.id : ids.includes(state?.active) ? state.active : ids.at(-1) || "";
  return { ids, active };
}
function IconButton({ label, icon, onClick, expanded, buttonRef, disabled = false, title }) {
  return <button ref={buttonRef} type="button" disabled={disabled} title={title} className={styles.iconButton} aria-label={label} aria-expanded={expanded} onClick={onClick}><TerraIcon name={icon} className="h-4 w-4" /></button>;
}
function PanelControl({ side = "left", label, expanded, onClick, navigation = false }) {
  return <button type="button" className={styles.paneControl} title={label} aria-label={label} aria-expanded={expanded}
    data-navigation-toggle={navigation || undefined} data-pane-toggle={navigation ? undefined : side === "left" ? "context" : "utility"} onClick={onClick}>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true">
      <rect x="3" y="4" width="18" height="16" rx="2" /><path d={side === "left" ? "M9 4v16" : "M15 4v16"} />
    </svg>
  </button>;
}
function Resizer({ kind, width, onWidth }) {
  const drag = useRef(null);
  const min = kind === "context" ? 170 : 280, max = kind === "context" ? 320 : 480;
  return <div role="separator" tabIndex={0} aria-label={kind === "context" ? "调整目录宽度" : "调整详情宽度"} aria-orientation="vertical" aria-valuemin={min} aria-valuemax={max} aria-valuenow={width}
    className={styles.resizer + " " + (kind === "context" ? styles.contextResizer : styles.utilityResizer)}
    onPointerDown={(event) => { if (event.button !== 0) return; event.preventDefault(); event.currentTarget.focus(); drag.current = { x: event.clientX, width }; event.currentTarget.setPointerCapture(event.pointerId); }}
    onPointerMove={(event) => { if (drag.current) onWidth(paneWidth(kind, drag.current.width + (event.clientX - drag.current.x) * (kind === "context" ? 1 : -1))); }}
    onPointerUp={() => { drag.current = null; }} onPointerCancel={() => { drag.current = null; }}
    onKeyDown={(event) => { if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return; event.preventDefault(); onWidth(event.key === "Home" ? min : event.key === "End" ? max : paneWidth(kind, width + (event.key === "ArrowRight" ? 20 : -20) * (kind === "context" ? 1 : -1))); }} />;
}

export default function WorkspacePaneShell({
  workspaceId, surfaceId, breadcrumb, headerExtra, contextPane, utilityPane, utilityTabs,
  contextAvailable = false, utilityAvailable = false,
  contextLabel = "当前工作", utilityLabel = "详情", utilityRequestKey = 0,
  utilityRequestTabId = "", initialContextOpen = false, initialUtilityOpen = false,
  navigationSlot, onUtilityClose, children,
}) {
  const { companyId } = useRuntime();
  const pathname = usePathname();
  const scope = paneScopeKey(companyId, workspaceId, surfaceId || pathname);
  const navigationKey = "curis.d0.navigation." + JSON.stringify(companyId || "unselected");
  const [entry, setEntry] = useState({ key: "", value: DEFAULTS });
  const [navEntry, setNavEntry] = useState({ key: "", value: true });
  const [width, setWidth] = useState(1440);
  const [searchCompanyId, setSearchCompanyId] = useState("");
  const searchOpen = Boolean(companyId && searchCompanyId === companyId);
  const currentCompany = useRef(companyId);
  useLayoutEffect(() => { currentCompany.current = companyId; }, [companyId]);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchState, setSearchState] = useState({ status: "idle", groups: [], error: "" });
  const [searchCursor, setSearchCursor] = useState(-1);
  const searchInputRef = useRef(null);
  const searchTimerRef = useRef(null);
  const searchSeqRef = useRef(0);
  const [maxScope, setMaxScope] = useState(null);
  const [lastOpened, setLastOpened] = useState("utility");
  const [tabsEntry, setTabsEntry] = useState({ key: "", ids: [], active: "" });
  const tabSequence = useRef(0);
  const tabListRef = useRef(null);
  const tabPrefix = useId();
  const root = useRef(null), maximizeTrigger = useRef(null), searchTrigger = useRef(null), requestSeen = useRef(null);
  const initialPreferences = { ...DEFAULTS, context: initialContextOpen, utility: initialUtilityOpen };
  const preferences = entry.key === scope ? entry.value : initialPreferences;
  const navigation = navEntry.key === navigationKey ? navEntry.value : true;
  const contextOpen = Boolean(contextAvailable && contextPane && preferences.context);
  const tabs = utilityTabs || (utilityPane ? [{ id: "current", title: utilityLabel, content: utilityPane }] : []);
  const tabIds = tabs.map((tab) => tab.id);
  const tabIdsKey = JSON.stringify(tabIds);
  const tabState = utilityTabState(tabsEntry.key === scope ? tabsEntry : { ids: tabIds.slice(0, 1), active: tabIds[0] }, { type: "read" }, tabIds);
  const changeTab = (action) => {
    const next = utilityTabState(tabState, action, tabIds);
    setTabsEntry({ key: scope, ...next });
    try { window.sessionStorage.setItem(scope + ".tabs", JSON.stringify(next)); } catch {}
    if (action.type === "close" && !next.ids.length && onUtilityClose) onUtilityClose();
  };
  const newTab = () => {
    let id;
    do { id = `new:0-${++tabSequence.current}`; } while (tabState.ids.includes(id));
    changeTab({ type: "new", id });
  };
  const openTabs = tabState.ids.map((id) => tabs.find((tab) => tab.id === id) || { id, title: "新标签页", content: <section className={styles.tabPicker} aria-label="选择标签内容"><h3>打开内容</h3>{tabs.map((tab) => <button type="button" key={tab.id} onClick={() => changeTab({ type: "select", id: tab.id })}>{tab.title}{tabState.ids.includes(tab.id) ? " · 已打开" : ""}</button>)}</section> });
  const utilityOpen = Boolean(utilityAvailable && tabs.length && preferences.utility);
  const openTabIdsKey = JSON.stringify(tabState.ids);
  const maximized = maxScope === scope && utilityOpen;
  const geometry = paneGeometry(width, navigation, contextOpen, maximized ? false : utilityOpen, preferences.contextWidth, preferences.utilityWidth, lastOpened);
  const update = (patch) => {
    const next = sanitizePanePreferences({ ...preferences, ...patch });
    setEntry({ key: scope, value: next });
    try { window.sessionStorage.setItem(scope, JSON.stringify(next)); } catch {}
  };
  const focusToggle = (kind) => window.requestAnimationFrame(() => root.current?.querySelector('[data-pane-toggle="' + kind + '"]')?.focus());
  const setPane = (kind, open) => {
    update({ [kind]: open });
    if (open) setLastOpened(kind);
    if (!open && kind === "utility") {
      setMaxScope(null);
      focusToggle(kind);
    } else if (!open) focusToggle(kind);
  };
  const toggleNavigation = () => {
    const next = !navigation; setNavEntry({ key: navigationKey, value: next });
    try { window.sessionStorage.setItem(navigationKey, String(next)); } catch {}
    window.requestAnimationFrame(() => [...(root.current?.querySelectorAll("[data-navigation-toggle]") || [])].find((node) => node.getClientRects().length)?.focus());
  };
  const exitMaximize = () => { setMaxScope(null); };
  const openSearch = () => {
    if (companyId && currentCompany.current === companyId) setSearchCompanyId(companyId);
  };
  const closeSearch = () => {
    ++searchSeqRef.current;
    setSearchCompanyId("");
    setSearchQuery("");
    setSearchState({ status: "idle", groups: [], error: "" });
    setSearchCursor(-1);
    if (searchTimerRef.current) window.clearTimeout(searchTimerRef.current);
    window.requestAnimationFrame(() => searchTrigger.current?.focus());
  };

  useEffect(() => {
    setEntry({ key: scope, value: readPreferences(scope, workspaceId, initialPreferences) });
    try { const saved = JSON.parse(window.sessionStorage.getItem(scope + ".tabs") || "null"); setTabsEntry({ key: scope, ...(saved || { ids: tabIds.slice(0, 1), active: tabIds[0] || "" }) }); } catch { setTabsEntry({ key: scope, ids: tabIds.slice(0, 1), active: tabIds[0] || "" }); }
    setSearchCompanyId(""); setSearchQuery(""); setMaxScope(null);
  // Restore only on scope changes; live descriptors are validated every render.
  }, [scope, workspaceId, initialContextOpen, initialUtilityOpen]); // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => { setNavEntry({ key: navigationKey, value: readNavigation(navigationKey) }); }, [navigationKey]);
  useEffect(() => {
    const strip = tabListRef.current;
    const selected = strip?.querySelector('[role="tab"][aria-selected="true"]');
    if (!utilityOpen || !selected || !strip.clientWidth) return;
    const item = selected.parentElement.getBoundingClientRect();
    const left = strip.getBoundingClientRect().left + strip.clientLeft;
    const right = left + strip.clientWidth;
    if (item.left < left || item.width > strip.clientWidth) strip.scrollLeft += item.left - left;
    else if (item.right > right) strip.scrollLeft += item.right - right;
  }, [scope, tabState.active, openTabIdsKey, utilityOpen, width, preferences.utilityWidth, maximized]);
  useEffect(() => {
    const observer = new ResizeObserver((entries) => setWidth(entries[0].contentRect.width));
    observer.observe(root.current); return () => observer.disconnect();
  }, []);
  useEffect(() => {
    const ids = JSON.parse(tabIdsKey);
    if (utilityRequestTabId && !ids.includes(utilityRequestTabId)) return;
    const previous = requestSeen.current;
    if (Number.isInteger(utilityRequestKey) && utilityRequestKey > 0 && utilityAvailable && (previous?.scope !== scope || utilityRequestKey > previous.key)) {
      requestSeen.current = { scope, key: utilityRequestKey };
      const base = readPreferences(scope, workspaceId, { ...DEFAULTS, context: initialContextOpen, utility: initialUtilityOpen }), next = { ...base, utility: true };
      setEntry({ key: scope, value: next }); setLastOpened("utility");
      if (utilityRequestTabId) setTabsEntry((current) => {
        const selected = utilityTabState(current.key === scope ? current : { ids: ids.slice(0, 1), active: ids[0] }, { type: "select", id: utilityRequestTabId }, ids);
        try { window.sessionStorage.setItem(scope + ".tabs", JSON.stringify(selected)); } catch {}
        return { key: scope, ...selected };
      });
      try { window.sessionStorage.setItem(scope, JSON.stringify(next)); } catch {}
    }
  }, [scope, workspaceId, utilityRequestKey, utilityRequestTabId, utilityAvailable, tabIdsKey, initialContextOpen, initialUtilityOpen]);
  useEffect(() => {
    const escape = (event) => {
      if (event.key !== "Escape") return;
      if (searchOpen) closeSearch();
      else if (maximized) { setMaxScope(null); window.requestAnimationFrame(() => maximizeTrigger.current?.focus()); }
    };
    window.addEventListener("keydown", escape); return () => window.removeEventListener("keydown", escape);
  }, [searchOpen, maximized]);

  // Autofocus the search input when the surface opens.
  useEffect(() => {
    if (searchOpen) window.requestAnimationFrame(() => searchInputRef.current?.focus());
  }, [searchOpen]);

  // Debounced search against the read-only object-search endpoint.
  useEffect(() => {
    const seq = ++searchSeqRef.current;
    if (searchTimerRef.current) window.clearTimeout(searchTimerRef.current);
    const q = searchQuery.trim();
    if (!companyId || !searchOpen || !q) {
      setSearchState({ status: "idle", groups: [], error: "" });
      setSearchCursor(-1);
      return;
    }
    setSearchState((prev) => ({ ...prev, status: "loading" }));
    searchTimerRef.current = window.setTimeout(() => {
      if (seq !== searchSeqRef.current || currentCompany.current !== companyId) return;
      searchCompanyObjects(companyId, q).then((data) => {
        if (seq !== searchSeqRef.current || currentCompany.current !== companyId) return;
        const groups = Array.isArray(data?.groups) ? data.groups : [];
        setSearchState({
          status: groups.length ? "ready" : "empty",
          groups,
          error: "",
        });
        setSearchCursor(groups.length ? 0 : -1);
      }).catch(() => {
        if (seq !== searchSeqRef.current || currentCompany.current !== companyId) return;
        setSearchState({ status: "error", groups: [], error: "搜索暂时不可用，请稍后重试。" });
        setSearchCursor(-1);
      });
    }, 180);
    return () => { ++searchSeqRef.current; if (searchTimerRef.current) window.clearTimeout(searchTimerRef.current); };
  }, [searchOpen, searchQuery, companyId]);

  // Flatten grouped items for keyboard navigation.
  const searchItems = searchState.groups.flatMap((g) =>
    (g.items || []).map((item) => ({ ...item, type: g.type }))
  );
  const openSearchItem = (item) => {
    if (!companyId || currentCompany.current !== companyId || !item) return;
    closeSearch();
    window.location.href = objectHref(item);
  };
  const onSearchKeyDown = (event) => {
    if (!companyId || currentCompany.current !== companyId) { event.preventDefault(); return; }
    if (event.key === "ArrowDown") {
      event.preventDefault();
      setSearchCursor((c) => Math.min(c + 1, searchItems.length - 1));
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      setSearchCursor((c) => Math.max(c - 1, 0));
    } else if (event.key === "Enter") {
      event.preventDefault();
      if (searchCursor >= 0 && searchItems[searchCursor]) openSearchItem(searchItems[searchCursor]);
    }
  };

  // Stable tracks let folding interpolate without moving a pane into another column.
  const columns = [navigation ? geometry.navWidth + "px" : "0px",
    contextOpen && geometry.overlay !== "context" && geometry.suppress !== "context" ? preferences.contextWidth + "px" : "0px",
    maximized ? "0px" : "minmax(0, 1fr)",
    maximized ? "minmax(0, 1fr)" : utilityOpen && geometry.overlay !== "utility" && geometry.suppress !== "utility" ? preferences.utilityWidth + "px" : "0px"].join(" ");

  return <div ref={root} className={styles.shell} data-d0-shell data-pane-overlay={geometry.overlay || "none"} style={{ gridTemplateColumns: columns, "--d0-navigation-width": geometry.navWidth + "px" }}>
    <TerraIconSprite />
    <a href="#curis-main" className={styles.skipLink}>跳到主区域</a>
    <aside hidden={!navigation} className={styles.navigation} aria-label="公司导航栏">
      <header data-tauri-drag-region className={styles.header}><span className={styles.brand} aria-hidden data-tauri-drag-region />
        <PanelControl navigation label="收起导航" expanded={navigation} onClick={toggleNavigation} />
      </header>
      {navigationSlot || <V1Sidebar embedded brandActions={<IconButton label="搜索公司对象" icon="i-search" buttonRef={searchTrigger} disabled={!companyId} title={!companyId ? "建立公司后可搜索公司对象" : undefined} onClick={openSearch} />} />}
    </aside>
    {contextAvailable && contextPane && <aside hidden={!contextOpen || geometry.suppress === "context"} className={styles.pane + " " + (geometry.overlay === "context" ? styles.contextOverlay : "")} style={{ width: preferences.contextWidth }} aria-label={contextLabel}>
      <header data-tauri-drag-region className={styles.header}><span className={styles.brand} aria-hidden data-tauri-drag-region /><PanelControl label={"收起" + contextLabel} expanded={contextOpen} onClick={() => setPane("context", false)} /></header><div className={styles.paneBody}>{contextPane}</div>
      <Resizer kind="context" width={preferences.contextWidth} onWidth={(value) => update({ contextWidth: value })} />
    </aside>}
    <main id="curis-main" hidden={maximized} tabIndex={-1} aria-label="当前工作页面" className={styles.main} data-d0-main>
      <header data-tauri-drag-region className={styles.header + (!navigation ? " " + styles.windowControlsSpace : "")}>
        {!navigation && <><IconButton label="搜索公司对象" icon="i-search" buttonRef={searchTrigger} disabled={!companyId} title={!companyId ? "建立公司后可搜索公司对象" : undefined} onClick={openSearch} /><PanelControl navigation label="展开导航" expanded={navigation} onClick={toggleNavigation} /></>}
        {contextAvailable && contextPane && (!contextOpen || geometry.suppress === "context") && <PanelControl label={"展开" + contextLabel} expanded={false} onClick={() => setPane("context", true)} />}
        <p data-tauri-drag-region className={styles.breadcrumb}>{breadcrumb}</p>{headerExtra}
        {utilityAvailable && tabs.length > 0 && (!utilityOpen || geometry.suppress === "utility") && <PanelControl side="right" label={"展开" + utilityLabel} expanded={false} onClick={() => setPane("utility", true)} />}
      </header><div className={styles.mainBody}>{children}</div>
    </main>
    {geometry.overlay && !maximized && <button className={styles.shade} aria-label="返回主工作面" onClick={() => setPane(geometry.overlay, false)} />}
    {utilityAvailable && tabs.length > 0 && <section hidden={!utilityOpen || (!maximized && geometry.suppress === "utility")}
      aria-label={utilityLabel}
      className={styles.pane + " " + styles.utility + (maximized ? " " + styles.expandedUtility : geometry.overlay === "utility" ? " " + styles.utilityOverlay : "")}
      style={{ width: preferences.utilityWidth }}>
      <header className={styles.header + " " + styles.utilityHeader + (!navigation && maximized ? " " + styles.windowControlsSpace : "")} data-tauri-drag-region>
        {!navigation && maximized && <PanelControl navigation label="展开导航" expanded={false} onClick={toggleNavigation} />}
        <div ref={tabListRef} role="tablist" aria-label="已打开的辅助内容" className={styles.tabList}>{openTabs.map((tab) => <div key={tab.id} className={styles.tabItem}><button role="tab" type="button" id={tabPrefix + tab.id} aria-controls={tabPrefix + tab.id + "-panel"} aria-selected={tabState.active === tab.id} onClick={() => changeTab({ type: "open", id: tab.id })}>{tab.title}</button><button type="button" aria-label={"关闭标签 · " + tab.title} onClick={() => changeTab({ type: "close", id: tab.id })}>×</button></div>)}</div>
        <button type="button" className={styles.iconButton} aria-label="新建标签页" onClick={newTab}>+</button>
        <button type="button" className={styles.iconButton} ref={maximizeTrigger} aria-label={maximized ? "恢复标签页大小" : "放大当前标签页"} aria-pressed={maximized} onClick={() => maximized ? exitMaximize() : setMaxScope(scope)}><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" aria-hidden="true"><path d={maximized ? "M3 9h6V3M21 9h-6V3M3 15h6v6M21 15h-6v6" : "M9 3H3v6M15 3h6v6M3 15v6h6M21 15v6h-6"} /></svg></button>
        <PanelControl side="right" label={"收起" + utilityLabel} expanded onClick={() => setPane("utility", false)} />
      </header>
      <div className={styles.tabPanels}>{openTabs.map((tab) => <section key={tab.id} role="tabpanel" id={tabPrefix + tab.id + "-panel"} aria-labelledby={tabPrefix + tab.id} hidden={tabState.active !== tab.id} className={styles.paneBody}>{tab.content}</section>)}{!tabState.ids.length && <p className={styles.paneBody}>点击上方 + 新建标签页。</p>}</div>
      {!maximized && <Resizer kind="utility" width={preferences.utilityWidth} onWidth={(value) => update({ utilityWidth: value })} />}
    </section>}
    {searchOpen && <div className={styles.searchShade} onMouseDown={closeSearch}><section role="dialog" aria-modal="true" aria-label="搜索公司对象" className={styles.searchDialog} onMouseDown={(event) => event.stopPropagation()}>
      <header className={styles.header}><h2>搜索公司对象</h2><IconButton label="关闭搜索" icon="i-close" onClick={closeSearch} /></header>
      <div className={styles.searchBody}>
        <input
          ref={searchInputRef}
          className={styles.searchInput}
          type="text"
          value={searchQuery}
          placeholder="输入关键词以搜索公司对象"
          aria-label="搜索关键词"
          autoComplete="off"
          spellCheck={false}
          onChange={(event) => { setSearchQuery(event.target.value); setSearchCursor(-1); }}
          onKeyDown={onSearchKeyDown}
        />
        <div className={styles.searchResults} role="listbox" aria-label="搜索结果">
          {searchState.status === "idle" && <p className={styles.searchHint}>输入关键词以搜索公司对象</p>}
          {searchState.status === "loading" && <p className={styles.searchHint}>正在搜索…</p>}
          {searchState.status === "empty" && <p className={styles.searchHint}>未找到匹配对象</p>}
          {searchState.status === "error" && <p className={styles.searchError}>{searchState.error}</p>}
          {searchState.status === "ready" && searchState.groups.map((group) => {
            const meta = groupMeta(group.type);
            return (
              <div key={group.type} className={styles.searchGroup}>
                <div className={styles.searchGroupLabel}><TerraIcon name={meta.icon} className="h-3.5 w-3.5" /><span>{meta.label}</span></div>
                {(group.items || []).map((item) => {
                  const flatIndex = searchItems.findIndex((i) => i.id === item.id && i.type === group.type);
                  const selected = flatIndex === searchCursor;
                  return (
                    <button
                      key={item.id}
                      type="button"
                      role="option"
                      aria-selected={selected}
                      className={styles.searchItem + (selected ? " " + styles.searchItemActive : "")}
                      onMouseEnter={() => setSearchCursor(flatIndex)}
                      onClick={() => openSearchItem({ ...item, type: group.type })}
                    >
                      <span className={styles.searchItemTitle}>{item.title}</span>
                      {item.context && <span className={styles.searchItemContext}>{item.context}</span>}
                    </button>
                  );
                })}
              </div>
            );
          })}
        </div>
        <footer className={styles.searchFooter}>↵ 进入对象 · Esc 关闭 · 仅对象搜索 v1</footer>
      </div>
    </section></div>}
  </div>;
}
