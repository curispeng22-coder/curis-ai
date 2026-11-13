// TerraNavData — 全站唯一导航分组数据源（Company OS IA + 旧链兼容入口）。
// route 统一 /ceo-office/* 命名空间。
// 所有页面与组件必须从此读取，禁止内联 NAV 数组。
//
// IA 对齐（2026-08-06 · v2 强制对齐 canonical-nav.js 唯一真源）：
//   公司     ：CEO 工作台 / 经营 / 业务版图 / AI 团队 / 工作空间
//   经营工具 ：会议工作台 / 决策室
//   公司资源 ：成果库 / 知识库 / 财务 / 日历
//   兼容入口 ：旧项目 / 旧执行 / 旧任务流水线
//   底部固定 ：设置 / 帮助与反馈
//
// 对齐纪律：本文件只承载 canonical-nav.js NAV_MODEL 列出的项；
// 任何不在原型里的历史自创栏目（如原 v1 的 CEO 协调型子项、头脑风暴室、
// 执行工作台、能力中心等）一律不进入导航，保持与原型 100% 一致。
//
// Workspace 入口由 Runtime API 动态生成，不在导航中静态映射业务类型。

const GROUPS = [
  {
    group: "公司",
    items: [
      {
        label: "CEO 工作台",
        icon: "i-home",
        href: "/ceo-office",
        subs: [],
      },
      {
        label: "经营",
        icon: "i-analytics",
        href: "/ceo-office/analytics",
        subs: [],
      },
      {
        label: "业务版图",
        icon: "i-folder_open",
        href: "/ceo-office/business",
        subs: [],
      },
        {
          label: "AI 团队",
          icon: "i-groups",
          href: "/ceo-office/organization",
          subs: [],
        },
        {
          label: "人才市场",
          icon: "i-search",
          href: "/ceo-office/talent-market",
          subs: [],
        },
        {
        label: "工作空间",
        icon: "i-widgets",
        href: "/ceo-office/workspace",
        subs: [],
      },
    ],
  },
  {
    group: "经营工具",
    items: [
      {
        label: "会议工作台",
        icon: "i-meeting_room",
        href: "/ceo-office/meeting",
        subs: [],
      },
      {
        label: "决策室",
        icon: "i-gavel",
        href: "/ceo-office/decisions",
        subs: [],
      },
    ],
  },
  {
    group: "兼容入口",
    items: [
      { label: "旧项目", icon: "i-folder_open", href: "/ceo-office/projects", subs: [] },
      { label: "旧执行", icon: "i-play_circle", href: "/ceo-office/execution", subs: [] },
      { label: "旧任务流水线", icon: "i-polyline", href: "/ceo-office/execution/pipeline", subs: [] },
    ],
  },
  {
    group: "公司资源",
    items: [
      {
        label: "成果库",
        icon: "i-monitoring",
        href: "/ceo-office/company-runtime",
        subs: [],
      },
      {
        label: "知识库",
        icon: "i-auto_stories",
        href: "/ceo-office/knowledge",
        subs: [],
      },
      {
        label: "财务",
        icon: "i-pie_chart",
        href: "/ceo-office/finance",
        subs: [], // v1 暂不建设（Blueprint §16），占位页标「规划中」
      },
      {
        label: "日历",
        icon: "i-clock",
        href: "/ceo-office/calendar",
        subs: [], // v1 暂不建设，占位
      },
    ],
  },
  {
    group: "底部",
    items: [
      {
        label: "设置",
        icon: "i-settings",
        href: "/ceo-office/settings",
        subs: [],
      },
      {
        label: "帮助与反馈",
        icon: "i-chat",
        href: "/ceo-office/help",
        subs: [],
      },
    ],
  },
];

export default GROUPS;

/**
 * 导航分组固定顺序常量（保证渲染与激活匹配稳定）。
 * 与 GROUPS 一一对应：group 为分组名，items 为该组一级项 label 顺序。
 * @type {{ group: string, items: string[] }[]}
 */
export const ORDER = [
  { group: "公司", items: ["CEO 工作台", "经营", "业务版图", "AI 团队", "人才市场", "工作空间"] },
  { group: "经营工具", items: ["会议工作台", "决策室"] },
  { group: "公司资源", items: ["成果库", "知识库", "财务", "日历"] },
  { group: "兼容入口", items: ["旧项目", "旧执行", "旧任务流水线"] },
  { group: "底部", items: ["设置", "帮助与反馈"] },
];

/**
 * P2-2 常驻区（对齐原型 canonical-nav.js PERSISTENT_HREFS）：
 * 侧栏默认只渲染这 4 个公司级核心入口（无分组 label）；
 * 其余一级项（AI 团队 + 经营工具 + 公司资源）折叠进「更多」抽屉。
 * @type {string[]}
 */
export const PERSISTENT_LABELS = ["CEO 工作台", "经营", "业务版图", "人才市场", "工作空间"];

/**
 * 根据当前 pathname 匹配一级和二级激活项。
 *
 * 采用两轮匹配以消除前缀误吞问题：
 * - 第一轮：先尝试用一级 href 精确匹配（含带 query 的一级默认页）。
 *   由于「CEO 工作台」href 为 "/ceo-office" 且带 subs，若仅用 startsWith 前缀判断，
 *   会误吞所有 /ceo-office/* 子路由。故第一轮只做精确匹配。
 * - 第二轮：仅当第一轮未命中任意一级时，再按 subs 匹配。此时路径必然是某一级的
 *   孙级或二级页（如 /ceo-office/workspace/software），按 subs 的 path + query
 *   精确/前缀匹配，不会被 CEO 工作台前缀误吞。
 *
 * @param {string} pathname
 * @returns {{ activeTop: string|null, activeSub: string|null }}
 */
export function findActiveNav(pathname) {
  const allItems = GROUPS.flatMap((group) => group.items);
  let activeTop = null;
  let activeSub = null;

  // 第一轮：精确匹配一级（仅做精确匹配，禁止前缀/query 误吞）。
  for (const item of allItems) {
    const [itemPath] = item.href.split("?");
    if (pathname === item.href || pathname === itemPath || pathname === itemPath + "/") {
      activeTop = item.label;
      break;
    }
  }

  // 第二轮：未命中一级时，按 subs 匹配（避免被前缀项误吞）
  if (!activeTop) {
    for (const item of allItems) {
      if (!item.subs || item.subs.length === 0) continue;
      const pathBase = pathname.includes("?") ? pathname.split("?")[0] : pathname;
      const pathQuery = pathname.includes("?") ? pathname.split("?")[1] : null;
      for (const sub of item.subs) {
        const [subPath] = sub.href.split("?");
        const subQuery = sub.href.includes("?") ? sub.href.split("?")[1] : null;
        const samePath = pathBase === subPath || pathBase.startsWith(subPath + "/");
        const sameQuery = !subQuery || subQuery === pathQuery;
        if (samePath && sameQuery) {
          activeTop = item.label;
          activeSub = sub.label;
          break;
        }
      }
      if (activeTop) break;
    }
  }

  if (!activeTop) {
    const parent = allItems
      .filter((item) => item.href !== "/ceo-office" && pathname.startsWith(`${item.href}/`))
      .sort((left, right) => right.href.length - left.href.length)[0];
    activeTop = parent?.label || null;
  }

  return { activeTop, activeSub };
}
