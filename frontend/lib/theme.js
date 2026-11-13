// Curis v1 Desktop — Frozen 视觉常量（2026-08-05 总控裁定）
// 旧 Terra 暖奶油 + 森林绿浅色主题已作废；本文件仅作为「JS 内联样式」通道，
// 所有值一律引用 Frozen --ui-* 令牌（定义见 app/globals.css / Curis_UI_Frozen_Spec_2026-08-04.md）。
// 禁止在此写死 hex / px；新增值必须落在 Frozen 档位内。
// 导出签名保持不变（COLORS / STYLE / statusLabel / roleLabel / deptTypeLabel …）。

export const COLORS = {
  bg: "var(--ui-bg)",
  surface: "var(--ui-surface)",
  surface2: "var(--ui-surface-2)",
  surface3: "var(--ui-surface-2)",
  primary: "var(--ui-action-primary-bg)",
  primaryDark: "var(--ui-action-primary-hover)",
  primaryLight: "var(--ui-surface-2)",
  primarySoft: "var(--ui-surface-2)",
  accent: "var(--ui-accent)",
  accentLight: "var(--ui-surface-2)",
  text: "var(--ui-text)",
  text2: "var(--ui-text-2)",
  text3: "var(--ui-text-3)",
  line: "var(--ui-line)",
  line2: "var(--ui-line)",
  green: "var(--ui-success)",
  greenSoft: "var(--ui-surface-2)",
  amber: "var(--ui-warning)",
  amberSoft: "var(--ui-surface-2)",
  red: "var(--ui-danger)",
  redSoft: "var(--ui-surface-2)",
};

// 抽屉 / 卡片 / 表单共用内联样式（全部走 Frozen 令牌）
export const STYLE = {
  overlay: {
    position: "fixed", inset: 0, zIndex: "var(--ui-z-modal)",
    background: "rgba(0,0,0,0.55)", display: "flex",
    alignItems: "center", justifyContent: "center",
    padding: "5vw",
  },
  drawer: {
    background: "var(--ui-surface)", border: "1px solid var(--ui-line)",
    borderRadius: "var(--ui-r-lg)", minWidth: 400, maxWidth: 560, width: "100%",
    maxHeight: "90vh", overflow: "auto", padding: "var(--ui-sp-7)",
    boxShadow: "var(--ui-shadow-3)",
  },
  formLabel: {
    display: "block", marginBottom: "var(--ui-sp-5)", color: "var(--ui-text-2)",
    fontSize: "var(--ui-fs-1)", fontWeight: 700, letterSpacing: "0.05em",
  },
  input: {
    display: "block", width: "100%", marginTop: "var(--ui-sp-1)",
    padding: "var(--ui-sp-2) var(--ui-sp-3)", background: "var(--ui-surface-2)",
    border: "1px solid var(--ui-line)", borderRadius: "var(--ui-r-sm)",
    color: "var(--ui-text)", fontSize: "var(--ui-fs-3)", outline: "none",
    minHeight: "var(--ui-ctl-h)",
  },
  textarea: {
    display: "block", width: "100%", marginTop: "var(--ui-sp-1)",
    padding: "var(--ui-sp-2) var(--ui-sp-3)", background: "var(--ui-surface-2)",
    border: "1px solid var(--ui-line)", borderRadius: "var(--ui-r-sm)",
    color: "var(--ui-text)", fontSize: "var(--ui-fs-3)", outline: "none",
    resize: "vertical", fontFamily: "inherit",
  },
  select: {
    display: "block", width: "100%", marginTop: "var(--ui-sp-1)",
    padding: "var(--ui-sp-2) var(--ui-sp-3)", background: "var(--ui-surface-2)",
    border: "solid", borderColor: "var(--ui-line)", borderRadius: "var(--ui-r-sm)",
    color: "var(--ui-text)", fontSize: "var(--ui-fs-3)", outline: "none",
    minHeight: "var(--ui-ctl-h)",
  },
  checkboxWrap: {
    display: "flex", alignItems: "center", gap: "var(--ui-sp-2)",
    marginBottom: "var(--ui-sp-5)",
    color: "var(--ui-text-2)", fontSize: "var(--ui-fs-1)", fontWeight: 700,
    letterSpacing: "0.05em", cursor: "pointer", minHeight: "var(--ui-tap-min)",
  },
  card: {
    background: "var(--ui-surface)", border: "1px solid var(--ui-line)",
    borderRadius: "var(--ui-r-md)", padding: "var(--ui-sp-3) var(--ui-sp-4)",
  },
  cardActions: {
    display: "flex", gap: "var(--ui-sp-2)", marginTop: "var(--ui-sp-3)", flexWrap: "wrap",
  },
  btnSmall: {
    padding: "var(--ui-sp-1) var(--ui-sp-3)", fontSize: "var(--ui-fs-1)",
    minHeight: "var(--ui-ctl-h-sm)",
  },
  btnDanger: {
    borderColor: "var(--ui-danger)", color: "var(--ui-danger)",
    background: "transparent",
  },
  btnDangerPrimary: {
    borderColor: "var(--ui-danger)", background: "var(--ui-danger)",
    color: "var(--ui-action-primary-fg)",
  },
  deptHeader: {
    display: "flex", alignItems: "center", gap: "var(--ui-sp-3)",
    padding: "var(--ui-sp-4) 0 var(--ui-sp-3)", flexWrap: "wrap",
  },
  empCount: {
    color: "var(--ui-text-3)", fontSize: "var(--ui-fs-1)", letterSpacing: "0.05em",
  },
  empMeta: {
    color: "var(--ui-text-3)", fontSize: "var(--ui-fs-1)",
  },
  empRow: {
    display: "flex", alignItems: "center", justifyContent: "space-between",
    gap: "var(--ui-sp-3)", flexWrap: "wrap",
  },
  empTag: {
    padding: "2px var(--ui-sp-1)", borderRadius: "var(--ui-r-xs)",
    fontSize: "var(--ui-fs-1)", fontWeight: 700, letterSpacing: "0.08em",
  },
  btnPrimary: {
    borderColor: "var(--ui-action-primary-bg)", background: "var(--ui-action-primary-bg)",
    color: "var(--ui-action-primary-fg)",
  },
};

export function COLORS_HELPER() {
  return COLORS;
}

export function statusClass(status) {
  if (!status) return "other";
  if (status === "active" || status === "completed") return "active";
  if (status === "blocked" || status === "failed" || status === "disabled") return "risk";
  if (status === "planned" || status === "draft" || status === "idle") return "waiting";
  return "other";
}

export function statusLabel(status) {
  if (!status) return "未知";
  const labels = {
    active: "已启用", inactive: "已停用", disabled: "已停用",
    idle: "空闲中", assigned: "已分配",
    draft: "草稿", planned: "计划中", completed: "已完成",
    archived: "已归档", blocked: "已阻塞",
  };
  return labels[status] || String(status).toUpperCase();
}

export const ROLE_LABELS = {
  architect: "架构师",
  backend_engineer: "后端工程师",
  brand_manager: "品牌经理",
  community_manager: "社群运营",
  content_auditor: "审核员",
  content_operator: "运营专员",
  content_planner: "策划",
  content_researcher: "研究员",
  data_analyst: "数据分析师",
  devops_engineer: "运维工程师",
  distribution_operator: "分发运营",
  frontend_engineer: "前端工程师",
  live_host: "主播",
  product_manager: "产品经理",
  qa_engineer: "测试工程师",
  script_writer: "脚本撰写",
  seo_specialist: "SEO 专员",
  tech_lead: "技术负责人",
  video_producer: "视频制作",
  "backend-engineer": "后端工程师",
  "frontend-engineer": "前端工程师",
  "product-manager": "产品经理",
  "qa-engineer": "测试工程师",
  "tech-lead": "技术负责人",
  "brand-manager": "品牌经理",
  "community-manager": "社群运营",
  "data-analyst": "数据分析师",
  "live-host": "主播",
  "script-writer": "脚本撰写",
  "video-producer": "视频制作",
  backend: "后端工程师", devops: "运维工程师", pm: "产品经理", qa: "测试工程师",
  auditor: "审核员", distribution: "分发运营", operator: "运营专员",
  planner: "策划", researcher: "研究员", seo: "SEO 专员",
};

export const DEPT_TYPE_LABELS = {
  "tech.rd": "研发", "content.growth": "内容增长",
  "software_rnd": "研发", "ai.rd": "AI 研发",
};

export function roleLabel(role) {
  return ROLE_LABELS[role] || role || "未指定";
}

export function deptTypeLabel(type) {
  return DEPT_TYPE_LABELS[type] || type || "未分类";
}
