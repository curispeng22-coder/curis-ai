"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import { TerraIcon, TerraIconSprite } from "./TerraIcons.js";
import GROUPS, { PERSISTENT_LABELS, findActiveNav } from "./TerraNavData.js";
import { getInstalledWorkspaceNavigation } from "../../lib/workspacePackageApi.js";

/**
 * TerraSidebar — 分组响应式导航组件（Frozen 视觉：浅色表面 + 激活态 3px 强调线）
 *
 * IA 结构（2026-08-05 · T0 对齐 Frozen 原型 canonical-nav.js P2-2）：
 * - 常驻区：仅 4 个公司级核心入口（CEO 工作台/经营/业务版图/工作空间，无分组 label）
 * - 「更多」按钮（初始收起，aria-expanded 控制）：展开折叠面板，内含
 *   AI 团队（单组无 label）+「经营工具」组 +「公司资源」组（组 label 12px/600）
 * - 折叠页默认态：常驻区与「更多」之间内联「当前栏目」单条（3px 高亮 + aria-current，
 *   WCAG 2.4.3）；折叠面板内同名项 suppressActive 不重复高亮（原型 suppressHref）
 * - 底部固定区渲染「底部」组：设置 / 帮助与反馈（原型 nav-footer 语义）
 * - 办公室（动态分组）v1 未落地，由「AI 团队」承接部门空间；
 *   工作空间与 AI 团队同路由（/ceo-office/organization），激活命中 AI 团队，工作空间不高亮
 *
 * Desktop (≥1280): 220px 固定侧栏，一级 14px/600 + 二级 12px/500 缩进 35px
 * Tablet (1024–1279): 76px 图标态，隐藏标签/二级/分组 label
 * Mobile (<1024): 隐藏；通过 open prop 控制为 286px 抽屉 + 半透明遮罩
 *
 * 交互：
 * - 一级点击 <a> 跳转路由
 * - chevron 点击仅展开/收起二级（不改变路由）
 * - 「更多」点击展开/收起折叠面板（默认收起）
 * - 当前组默认展开；当前二级左侧 3px 指示条 + 浅底
 * - hover 右移 1px；focus 主色 ring
 * - Drawer 点击遮罩关闭
 */

const FOOTER_GROUP = "底部";
const MORE_GROUP_LABELS = ["经营工具", "公司资源", "兼容入口"];

export default function TerraSidebar({ open, onClose }) {
  const pathname = usePathname();
  const { activeTop, activeSub } = findActiveNav(pathname);
  const [installedWorkspaces, setInstalledWorkspaces] = useState([]);
  const [expanded, setExpanded] = useState(() => {
    const initial = {};
    GROUPS.forEach((group) => {
      group.items.forEach((item) => {
        initial[item.label] = item.label === activeTop || false;
      });
    });
    return initial;
  });
  /* P2-2：折叠面板（「更多」抽屉）默认收起，aria-expanded 控制展开/收起 */
  const [moreOpen, setMoreOpen] = useState(false);

  useEffect(() => {
    let active = true;
    getInstalledWorkspaceNavigation()
      .then((payload) => active && setInstalledWorkspaces(Array.isArray(payload?.items) ? payload.items : []))
      .catch(() => active && setInstalledWorkspaces([]));
    return () => { active = false; };
  }, [pathname]);

  const toggle = (e, label) => {
    e.preventDefault();
    e.stopPropagation();
    setExpanded((prev) => ({ ...prev, [label]: !prev[label] }));
  };

  /* 判断是否在移动端抽屉模式 */
  const isDrawer = typeof open === "boolean";

  /* 基础侧栏类（Frozen：浅色表面 + 右分割线） */
  const sidebarBase = isDrawer
    ? "fixed inset-y-0 left-0 z-50 w-[286px] bg-ui-surface text-ui-txt-2 border-r border-ui-line flex flex-col py-3.5 px-2.5 overflow-hidden transform transition-transform duration-200"
    : "w-[220px] lg:w-[76px] xl:w-[220px] flex-shrink-0 bg-ui-surface text-ui-txt-2 border-r border-ui-line flex flex-col py-3.5 px-2.5 overflow-hidden lg:flex hidden";

  const sidebarVisible = isDrawer ? (open ? "translate-x-0" : "-translate-x-full") : "";

  /* P2-2 分区：常驻 4 项（公司组内按 PERSISTENT_LABELS 过滤，保持原型顺序）；
     折叠面板 = AI 团队（单组无 label）+ 经营工具组 + 公司资源组；底部固定组独立 */
  const companyGroup = GROUPS.find((group) => group.group === "公司") || { group: "公司", items: [] };
  const persistentItems = companyGroup.items
    .filter((item) => PERSISTENT_LABELS.includes(item.label))
    .map((item) => item.label === "工作空间" ? {
      ...item,
      subs: installedWorkspaces.map((workspace) => ({ label: workspace.label, href: workspace.href })),
    } : item);
  const aiTeamItem = companyGroup.items.find((item) => item.label === "AI 团队") || null;
  const foldedGroups = GROUPS.filter((group) => MORE_GROUP_LABELS.includes(group.group));
  const footerGroup = GROUPS.find((group) => group.group === FOOTER_GROUP) || { group: FOOTER_GROUP, items: [] };

  /* 当前栏目（原型 canonical-nav.js currentFolded）：当前页若在折叠区内，
     在「更多」上方内联渲染单条高亮 + aria-current（WCAG 2.4.3 当前位置可见）。
     工作空间与 AI 团队同路由，activeTop 已命中 AI 团队，故此处只会内联 AI 团队。 */
  const foldedItemLabels = [aiTeamItem?.label, ...foldedGroups.flatMap((group) => group.items.map((item) => item.label))].filter(Boolean);
  const currentFolded = foldedItemLabels.includes(activeTop)
    ? [aiTeamItem, ...foldedGroups.flatMap((group) => group.items)].find((item) => item && item.label === activeTop) || null
    : null;

  /* 渲染单个一级导航项（可含二级）；showSubs=false 用于底部固定区（扁平项）；
     current=true 给内联「当前栏目」项声明 aria-current="page"（WCAG 2.4.3）；
     suppressActive=true 用于折叠面板内与「当前栏目」同名的项，避免一屏双高亮 */
  const renderNavItem = (item, { showSubs = true, current = false, suppressActive = false } = {}) => {
    const isOpen = expanded[item.label];
    const isActiveTop = !suppressActive && item.label === activeTop;
    const hasSubs = showSubs && item.subs && item.subs.length > 0;

    return (
      <div key={item.label}>
        {/* 一级导航项 */}
        <a
          href={item.href}
          aria-current={current ? "page" : undefined}
          className={`relative flex items-center gap-2 px-2 py-2 lg:flex-col lg:items-center lg:justify-center lg:px-0 lg:py-2.5 xl:flex-row xl:justify-start xl:px-2 xl:py-2 rounded-ui-sm text-ui-3 font-semibold mb-0.5 transition-all duration-100 ${
            isActiveTop
              ? "bg-ui-surface-2 text-ui-txt"
              : "text-ui-txt-2 hover:bg-ui-surface-2 hover:translate-x-[1px]"
          } focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ui-accent focus-visible:ring-offset-2 focus-visible:ring-offset-ui-surface`}
        >
          {isActiveTop && (
            <span className="absolute left-0 top-1.5 bottom-1.5 w-[3px] rounded-full bg-ui-accent" aria-hidden="true" />
          )}
          <span className="w-5 text-center flex-shrink-0">
            <TerraIcon name={item.icon} className="w-5 h-5" />
          </span>
          <span className={`flex-1 whitespace-nowrap overflow-hidden text-ellipsis ${isDrawer ? "block" : "hidden xl:block"}`}>{item.label}</span>
          {/* 展开箭头：固定 32×32 命中区（Frozen 触达 ≥32px），
              不靠 padding 撑高，避免影响一级导航项行高 */}
          {hasSubs && (
            <span
              onClick={(e) => toggle(e, item.label)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") toggle(e, item.label);
              }}
              className={`text-ui-5 opacity-70 cursor-pointer w-8 h-8 flex-shrink-0 -mr-1 place-items-center ${isDrawer ? "grid" : "hidden xl:grid"}`}
              role="button"
              tabIndex={0}
              aria-label={isOpen ? "收起" : "展开"}
            >
              <TerraIcon name="i-expand_less" className={`w-4 h-4 transition-transform ${isOpen ? "" : "rotate-180"}`} />
            </span>
          )}
        </a>

        {/* 二级导航 */}
        {hasSubs && isOpen && (
          <div className={`ml-[35px] mb-1 ${isDrawer ? "block" : "hidden xl:block"}`}>
            {item.subs.map((sub) => {
              const isActiveSubItem = sub.label === activeSub || pathname === sub.href;
              return (
                <a
                  key={sub.label}
                  href={sub.href}
                  className={`relative flex items-center min-h-[32px] px-2 py-2 rounded-ui-sm text-ui-1 font-medium no-underline transition-colors ${
                    isActiveSubItem
                      ? "text-ui-txt font-semibold bg-ui-surface-2"
                      : "text-ui-txt-3 hover:bg-ui-surface-2 hover:text-ui-txt"
                  }`}
                >
                  {/* 当前二级指示条（Frozen：3px 强调线） */}
                  {isActiveSubItem && (
                    <span className="absolute left-0 top-1 bottom-1 w-[3px] rounded-full bg-ui-accent" aria-hidden="true" />
                  )}
                  {sub.label}
                </a>
              );
            })}
          </div>
        )}
      </div>
    );
  };

  return (
    <>
      {/* 移动端遮罩 */}
      {isDrawer && open && (
        <div
          className="fixed inset-0 z-40 bg-black/30 lg:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={`${sidebarBase} ${sidebarVisible}`}
        aria-hidden={isDrawer && !open ? "true" : undefined}
        inert={isDrawer && !open ? true : undefined}
      >
        <TerraIconSprite />

        {/* Logo 区域（品牌文案：Curis，对齐原型 brand） */}
        <div className={`${isDrawer ? "flex" : "hidden xl:flex"} items-center gap-2 px-1.5 pb-3.5 font-ui-sans font-bold text-ui-4 text-ui-txt`}>
          <span className="w-[26px] h-[26px] rounded-ui-sm bg-ui-accent text-ui-surface grid place-items-center text-ui-4">C</span>
          Curis
        </div>

        {/* P2-2 常驻区：4 项（CEO 工作台/经营/业务版图/工作空间），无分组 label */}
        <nav className="overflow-y-auto flex-1" aria-label="主导航">
          {persistentItems.map((item) => renderNavItem(item))}

          {/* 当前栏目（原型 curis-here-nav）：折叠页默认态内联单条，3px 高亮 + aria-current */}
          {currentFolded && (
            <div key="curis-here-nav">
              <p className={`${isDrawer ? "block" : "hidden xl:block"} mt-3 px-2 py-1 text-ui-1 font-semibold text-ui-txt-2`}>
                当前栏目
              </p>
              {renderNavItem(currentFolded, { current: true })}
            </div>
          )}

          {/* 「更多」切换（原型 nav-more-toggle）：默认收起，aria-expanded 控制 */}
          <button
            type="button"
            aria-expanded={moreOpen}
            aria-controls="curis-nav-more-panel"
            aria-label={moreOpen ? "收起次要导航" : "展开次要导航"}
            onClick={() => setMoreOpen((prev) => !prev)}
            className={`flex items-center justify-between gap-2 min-h-[32px] w-full mt-2 mb-1 px-2 py-2 lg:flex-col lg:items-center lg:justify-center lg:px-0 lg:py-2.5 xl:flex-row xl:justify-between xl:px-2 xl:py-2 rounded-ui-sm text-ui-1 font-semibold text-ui-txt-2 bg-transparent border-0 cursor-pointer transition-colors duration-100 hover:bg-ui-surface-2 hover:text-ui-txt focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ui-accent focus-visible:ring-offset-2 focus-visible:ring-offset-ui-surface`}
          >
            <span className={`whitespace-nowrap ${isDrawer ? "block" : "hidden xl:block"}`}>更多</span>
            <TerraIcon name="i-expand_less" className={`w-4 h-4 transition-transform ${moreOpen ? "" : "rotate-180"}`} />
          </button>

          {/* 折叠面板：AI 团队（单组无 label）+ 经营工具 + 公司资源 */}
          {moreOpen && (
            <div id="curis-nav-more-panel" className={`${isDrawer ? "block" : "hidden xl:block"}`}>
              {/* AI 团队：原型 curis-ai-nav，单组无 label（v1 与工作空间同路由合并，激活命中此项） */}
              {aiTeamItem && renderNavItem(aiTeamItem, { suppressActive: currentFolded?.label === aiTeamItem.label })}

              {foldedGroups.map((group) => (
                <div key={group.group}>
                  {/* 分组 label（原型 nav-label：12px/600，Frozen --ui-* 令牌） */}
                  <p className={`${isDrawer ? "block" : "hidden xl:block"} mt-3 px-2 py-1 text-ui-1 font-semibold text-ui-txt-2`}>
                    {group.group}
                  </p>
                  {group.items.map((item) => renderNavItem(item, { suppressActive: currentFolded?.label === item.label }))}
                </div>
              ))}
            </div>
          )}
        </nav>

        {/* 底部固定：设置 / 帮助与反馈（原型 nav-footer 语义） */}
        <div className={`mt-auto pt-2.5 border-t border-ui-line ${isDrawer ? "block" : "hidden xl:block"}`}>
          {footerGroup.items.map((item) => renderNavItem(item, { showSubs: false }))}

          {/* 底部用户信息 */}
          <div className={`flex items-center gap-2 mt-2 text-ui-1 text-ui-txt-3 ${isDrawer ? "flex" : "hidden xl:flex"}`}>
            <span className="w-6 h-6 rounded-full bg-ui-accent text-ui-surface grid place-items-center text-ui-1 font-bold">齐</span>
            齐活林 · Admin
          </div>
        </div>
      </aside>
    </>
  );
}
