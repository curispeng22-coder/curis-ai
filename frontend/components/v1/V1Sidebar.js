"use client";
import { avatarPreset } from "../../lib/avatarPresets.mjs";

import { useEffect, useRef, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import { TerraIcon } from "../terra/TerraIcons.js";
import { getV1Presentation } from "../../lib/v1FrontendApi.js";
import ConversationQuickAccess from "./ConversationQuickAccess.js";
import { captureSettingsHref, PRESENTATION_CHANGED, THEME_CHANGED, applySettingsTheme, themeValue } from "../../lib/settingsEntryState.mjs";
import styles from "../workspace/WorkspacePaneShell.module.css";

const NAV = [
  ["CEO 工作台", "i-home", "/ceo-office"],
  ["业务空间", "i-widgets", "/ceo-office/business"],
  ["组织中心", "i-groups", "/ceo-office/organization"],
  ["人才与能力", "i-star", "/ceo-office/talent-market"],
  ["经营洞察", "i-analytics", "/ceo-office/analytics"],
  ["资料库", "i-auto_stories", "/ceo-office/knowledge"],
  ["会议", "i-meeting_room", "/ceo-office/meeting"],
];
function Avatar({ presentation }) {
  const source = presentation.avatar_ref || "";
  const preset = avatarPreset(source);
  if (source.startsWith("data:image/")) {
    // User-selected local data URLs never go to an image optimizer.
    // eslint-disable-next-line @next/next/no-img-element
    return <img src={source} alt="CEO 头像" className="h-8 w-8 rounded-full object-cover" />;
  }
  return <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-ui-primary-soft text-xs font-bold text-ui-primary" style={preset ? { backgroundColor: preset[2], color: preset[3] } : undefined}>{preset?.[1] || (presentation.display_name || "CEO").slice(0, 1)}</span>;
}
export default function V1Sidebar({ open, onClose, embedded = false, brandActions }) {
  const pathname = usePathname();
  const router = useRouter();
  const [presentation, setPresentation] = useState({ display_name: "", avatar_ref: "" });
  const [profileOpen, setProfileOpen] = useState(false), [theme, setTheme] = useState("system");
  const profile = useRef(null), trigger = useRef(null);
  useEffect(() => {
    let active = true, generation = 0;
    const refresh = () => { const request = ++generation; getV1Presentation().then((value) => { if (active && request === generation) setPresentation(value); }).catch(() => {}); };
    refresh(); setProfileOpen(false); window.addEventListener(PRESENTATION_CHANGED, refresh);
    return () => { active = false; window.removeEventListener(PRESENTATION_CHANGED, refresh); };
  }, [pathname]);
  useEffect(() => {
    const refresh = () => { try { setTheme(themeValue(window.localStorage.getItem("curis.theme"))); } catch {} };
    refresh(); window.addEventListener(THEME_CHANGED, refresh); return () => window.removeEventListener(THEME_CHANGED, refresh);
  }, []);
  useEffect(() => {
    if (!profileOpen) return undefined;
    profile.current?.querySelector("a")?.focus();
    const close = (event) => {
      if (event.key === "Escape") { setProfileOpen(false); trigger.current?.focus(); }
      else if (event.type === "pointerdown" && !profile.current?.contains(event.target) && !trigger.current?.contains(event.target)) setProfileOpen(false);
    };
    document.addEventListener("keydown", close); document.addEventListener("pointerdown", close);
    return () => { document.removeEventListener("keydown", close); document.removeEventListener("pointerdown", close); };
  }, [profileOpen]);
  const changeTheme = (value) => {
    setTheme(applySettingsTheme(value));
  };
  const drawer = typeof open === "boolean";
  return <>
    {drawer && open && <button aria-label="关闭导航" className="fixed inset-0 z-40 bg-black/25 lg:hidden" onClick={onClose} />}
    <aside className={styles.sidebar + (!embedded ? " w-[190px] border-r border-ui-line bg-ui-surface" : "") + (drawer ? " fixed inset-y-0 left-0 z-50" : "")} hidden={drawer && !open}>
      <div className={styles.brandRow}><Link href="/ceo-office" className={styles.sidebarBrand}>Curis</Link>{brandActions}</div>
      <p className={styles.brandDescription}>让创意变成持续的影响力</p>
      <div className={styles.navItems}><nav aria-label="主导航" className={styles.primaryNav}>
        {NAV.map(([label, icon, href]) => {
          const active = pathname === href || (href !== "/ceo-office" && pathname.startsWith(href + "/")) || (href === "/ceo-office/business" && (pathname === "/ceo-office/workspace" || pathname.startsWith("/ceo-office/workspace/")));
          return <Link key={href} href={href} aria-current={active ? "page" : undefined} className={styles.navLink}><TerraIcon name={icon} className="h-[17px] w-[17px] shrink-0" />{label}</Link>;
        })}
      </nav><ConversationQuickAccess /></div>
      <div className={styles.userFooter}>
        <button ref={trigger} type="button" className={styles.profileTrigger} aria-label="用户中心" aria-expanded={profileOpen} onClick={() => setProfileOpen((value) => !value)}>
          <Avatar presentation={presentation} /><span><strong>{presentation.display_name || "CEO"}</strong><small>个人设置</small></span>
        </button><span data-d0-assistant-anchor className={styles.assistantAnchor} aria-hidden />
        {profileOpen && <div ref={profile} role="dialog" aria-label="用户中心菜单" className={styles.userMenu}>
          <div className={styles.menuIdentity}>{presentation.display_name || "CEO"}</div>
          <Link href="/ceo-office/settings" onClick={(event) => {
            if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
            event.preventDefault(); setProfileOpen(false);
            router.push(captureSettingsHref(window.location.pathname, window.location.search));
          }}>设置</Link><Link href="/ceo-office/analytics">查看用量</Link>
          <label>主题<select aria-label="界面主题" value={theme} onChange={(event) => changeTheme(event.target.value)}><option value="system">跟随系统</option><option value="light">浅色</option><option value="dark">深色</option></select></label>
          <Link href="/ceo-office/help" onClick={() => setProfileOpen(false)}>本地使用帮助</Link><button type="button" disabled title="反馈入口尚未接入">反馈 · 尚未接入</button>
        </div>}
      </div>
    </aside>
  </>;
}
