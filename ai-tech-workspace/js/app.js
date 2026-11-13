/* ============================================================
   Curis AI Tech Workspace — Closure v2
   职责：
   - Theme：system / dark / light + persist
   - Shell pane toggles + persist
   - CEO Assistant drawer (global overlay)
   - Object → Utility mapping （核心修复）
       employee  → Employee Quick Panel
       research  → Research Detail
       content   → Content Detail
       handoff   → Handoff Detail
       result    → Result / Evidence Detail
   - Employee Quick Panel → Conversation / Current Work / Handoff / Workstation
   - Context restore（Utility 内的返回栈，跨页面 preserve 最近对象）
   - Station accordion
   - Calendar navigation + selection
   - Prototype controls 跳转（仍支持多页面入口，但对象上下文保留到下一页 hash）
   ============================================================ */
(function () {
  "use strict";

  const STORAGE_KEYS = {
    THEME: "curis.ai.theme",
    SHELL_STATE: "curis.ai.shell",
    UX_CONTEXT: "curis.ai.ux.ctx.v1", // {selectedEmployeeId, selectedObjectId, lastHash ...}
  };

  const PAGE_MAP = {
    overview: "overview.html",
    research: "research.html",
    content: "content.html",
    calendar: "calendar.html",
    growth: "growth.html",
    feedback: "feedback.html",
    commercial: "commercial.html",
    team: "team.html",
    handoff: "handoff.html",
    utility: "utility.html",
    assistant: "assistant.html",
    collapsed: "collapsed.html",
    "1280": "1280.html",
    rdcheck: "rdcheck.html",
  };

  /* =========================================================
     FIXTURES — 复用现有内容，不新增员工/研究/内容
     ========================================================= */
  // Frozen Shared Employee UI Status Projection（Shell Contract §3.1 Delta-X10）
  // 用户侧仅三态：空闲 / 工作中 · <desc> / 阻塞 · <cause>
  function projectEmployeeStatus(emp) {
    if (!emp) return { label: "空闲", tone: "idle", dot: "" };
    // 优先消费显式 frozenProjection（未来可从 Runtime Responsibility 真值生成）
    if (emp && emp.frozenProjection) return emp.frozenProjection;
    const w = emp.currentWork;
    if (w && /进行中|制作中|待发布|待确认/.test(w.tag || "")) {
      return {
        label: "工作中 · " + (w.title || emp.responsibility || "当前工作"),
        tone: "working",
        dot: "working",
      };
    }
    if (emp.blockedCause) {
      return { label: "阻塞 · " + emp.blockedCause, tone: "blocked", dot: "blocked" };
    }
    return { label: "空闲", tone: "idle", dot: "" };
  }
  function employeeStatusLabel(emp) { return projectEmployeeStatus(emp).label; }
  function employeeStatusDot(emp) { return projectEmployeeStatus(emp).dot; }
  function employeeStatusToneClass(emp) {
    const t = projectEmployeeStatus(emp).tone;
    if (t === "working") return "tag-working";
    if (t === "blocked") return "tag-needs";
    return "tag"; // idle
  }

  const PAGE_DISPLAY_NAME = {
    overview: "经营概览",
    research: "研究与洞察",
    content: "内容运营",
    calendar: "内容运营 · 日历",
    growth: "增长与评估",
    feedback: "用户反馈",
    commercial: "商业化",
    team: "团队",
    handoff: "交接关系",
  };

  const EMPLOYEES = {
    wy: {
      id: "wy", name: "王颖", role: "研究专家",
      avatar: "王", color: "var(--ui-accent)",
      // --- Minimal Identity Summary（回答“这个员工是谁？”，仅 Quick Panel/Profile 消费） ---
      org: "内容增长部 · AI 科技",
      coreResponsibility: "行业研究 / 趋势洞察",
      capabilities: ["行业研究", "竞品分析", "数据检索", "证据整理"],
      profile: {
        joined: "2025-03",
        level: "P6 · Senior",
        reportTo: "林薇（内容增长部负责人）",
        highlights: [
          "2026 Q1：3 份趋势报告支撑内容方向调整",
          "实测型笔记互动率 34% 提升归因研究",
        ],
      },
      // Frozen Projection（真实 Runtime / Responsibility 投影，不自创 IM 状态）
      frozenProjection: {
        label: "工作中 · OpenAI 新模型研究与证据整理",
        tone: "working",
        dot: "working",
      },
      responsibility: "AI 科技 · 研究与洞察：趋势跟踪、选题建议、证据整理",
      currentWork: {
        id: "r1", title: "OpenAI 新模型发布后的用户关注点", type: "研究对象",
        tag: "进行中", tagClass: "tag-working",
      },
      context: "AI 科技 / 研究与洞察 · 绑定研究对象：OpenAI 新模型发布后的用户关注点",
      handoff: {
        id: "h1",
        title: "交接至 内容运营：生成 3 个实测选题",
        status: "等待对方接收", statusCls: "tag",
        from: { empId: "wy", resp: "研究与洞察" },
        to: { empId: "cz", resp: "内容运营" },
        sourceResult: "OpenAI 新模型 → 实测型笔记互动率高于资讯型 34%",
        evidence: ["竞品选题周报.csv（近 7 天 120 条笔记）", "搜索词热度快照（8/12–8/19）"],
        nextWork: "陈真输出 3 个实测选题方向并提交评审",
      },
      results: [
        { title: "教程 / 实测型内容表现优于泛资讯内容", tag: "判断", tagClass: "tag-ctx", linkKind: "research", linkId: "r1" },
        { title: "OpenAI 新模型 → 实测型笔记互动率高于资讯型 34%", tag: "证据", tagClass: "tag-working", linkKind: "research", linkId: "r1" },
      ],
    },
    cz: {
      id: "cz", name: "陈真", role: "研究 & 内容创作者",
      avatar: "陈", color: "var(--ui-warning)",
      org: "内容增长部 · AI 科技",
      coreResponsibility: "选题落地 · 内容制作",
      capabilities: ["内容脚本", "提示词工程", "AI 绘画", "发布前检查"],
      profile: {
        joined: "2025-05",
        level: "P5 · Experienced",
        reportTo: "林薇（内容增长部负责人）",
        highlights: [
          "AI 绘画教程系列 2 期，收藏率均值 8.2%",
          "与王颖协作完成实测型选题闭环",
        ],
      },
      frozenProjection: {
        label: "工作中 · 制作小红书 AI 绘画教程 #3",
        tone: "working",
        dot: "working",
      },
      responsibility: "AI 科技 · 内容运营：选题落地、笔记制作、发布前检查",
      currentWork: {
        id: "c3", title: "小红书 AI 绘画教程 #3", type: "内容对象",
        tag: "制作中", tagClass: "tag-working",
      },
      context: "AI 科技 / 内容运营 · 绑定内容对象：小红书 AI 绘画教程 #3",
      handoff: {
        id: "h2",
        title: "交接至 李然：发布前检查（AI 绘画教程 #3）",
        status: "准备中", statusCls: "tag-working",
        from: { empId: "cz", resp: "内容运营 / 制作" },
        to: { empId: "lr", resp: "内容运营 / 发布排期" },
        sourceResult: "小红书 AI 绘画教程 #2 发布后收藏率 8.2%",
        evidence: ["教程 #2 原始素材", "提示词集合.md", "教程 #2 数据快照"],
        nextWork: "待陈真正在制作 #3 后，8/22 提交李然检查",
      },
      results: [
        { title: "AI 绘画教程系列持续增长，关注转化 6.4%", tag: "结果", tagClass: "tag-ctx", linkKind: "content", linkId: "c3" },
      ],
    },
    lr: {
      id: "lr", name: "李然", role: "内容策划 & 发布",
      avatar: "李", color: "var(--ui-text-2)",
      org: "内容增长部 · AI 科技",
      coreResponsibility: "内容排期 · 硬件测评发布",
      capabilities: ["内容策划", "发布排期", "硬件测评", "受众分层"],
      profile: {
        joined: "2024-11",
        level: "P6 · Senior",
        reportTo: "林薇（内容增长部负责人）",
        highlights: [
          "8 月内容日历 0 延误",
          "硬件测评系列评论互动率均值 11%",
        ],
      },
      frozenProjection: {
        label: "工作中 · 策划 9 月发布排期与硬件测评发布",
        tone: "working",
        dot: "working",
      },
      responsibility: "AI 科技 · 内容运营：策划、发布排期、硬件测评",
      currentWork: {
        id: "c2", title: "AI 硬件测评：谁更适合入门", type: "内容对象",
        tag: "待发布", tagClass: "tag",
      },
      context: "AI 科技 / 内容运营 · 绑定内容对象：AI 硬件测评：谁更适合入门",
      handoff: {
        id: "h4",
        title: "交接至 增长与评估：验证分层的关注转化",
        status: "已归档", statusCls: "tag",
        from: { empId: "lr", resp: "研究与洞察（协作）" },
        to: { empId: "lr", resp: "增长与评估" },
        sourceResult: "受众分层：入门偏教程 / 进阶偏工作流",
        evidence: ["问卷 200 份原始数据", "评论意图标注 JSON"],
        nextWork: "增长侧按分层在 9 月安排 A/B 选题节奏",
      },
      results: [
        { title: "硬件测评对比系列覆盖 5 款设备，评论互动率均值 11%", tag: "结果", tagClass: "tag-ctx", linkKind: "content", linkId: "c2" },
      ],
    },
    // U2 FIX：林薇 = 公司内独立员工（内容增长部负责人 / Workspace Leader），
    // 与 CEO Assistant 完全解耦；CEO Assistant 仅为匿名 Company-level 身份。
    lw: {
      id: "lw", name: "林薇", role: "内容增长部负责人",
      avatar: "林", color: "var(--ui-warning)",
      org: "内容增长部 · AI 科技",
      coreResponsibility: "部门目标对齐 · 决策评审 · 资源调配",
      capabilities: ["团队管理", "决策评审", "产品判断", "跨部门协作"],
      profile: {
        joined: "2023-09",
        level: "D1 · Director",
        reportTo: "CEO",
        highlights: [
          "建立内容增长部 XHS 专业工作面",
          "定义小红书业务空间的员工协作规范",
        ],
      },
      // 在 XHS Workspace 内林薇的责任以 Leader/Review 为主，未绑定具体业务执行 → 投影空闲
      frozenProjection: {
        label: "空闲",
        tone: "idle",
        dot: "",
      },
      responsibility: "内容增长部：目标对齐、决策评审、人才与能力",
      currentWork: { id: "d0", title: "小红书业务空间协作规范收口", type: "决策/评审", tag: "进行中", tagClass: "tag-working" },
      context: "CEO 工作台 / 业务空间 · 部门负责人",
      handoff: null,
      results: [
        { title: "员工速览面板交互规范 v2", tag: "交付", tagClass: "tag-ctx" },
        { title: "小红书业务空间体验路线确认（CEO 已批）", tag: "决策", tagClass: "tag-working" },
      ],
    },
  };

  const RESEARCH = {
    r1: {
      id: "r1", type: "研究对象",
      source: "趋势 · 8月18日",
      title: "OpenAI 新模型发布后的用户关注点",
      owner: "wy",
      status: "进行中", statusCls: "tag-working",
      claim: "小红书用户对“怎么用”的关注度高于“是什么”；实测型笔记的互动率高于资讯型 34%。",
      evidence: ["近 7 天 120 条相关笔记的评论抽样", "搜索词热度快照（8/12–8/19）"],
      handoff: "h1",
    },
    r2: {
      id: "r2", type: "研究对象",
      source: "竞品 · 8月19日",
      title: "同类账号选题结构对比",
      owner: "cz",
      status: "进行中", statusCls: "tag-working",
      claim: "头部账号在“教程 + 工具清单”组合上占据优势；评论区预埋问题可提升互动。",
      evidence: ["5 个对标账号近 30 天内容结构分析"],
      handoff: "h3",
    },
    r3: {
      id: "r3", type: "研究对象",
      source: "受众 · 8月15日",
      title: "AI 科技受众兴趣分层",
      owner: "lr",
      status: "已归档", statusCls: "tag",
      claim: "入门用户偏好“零基础教程”，进阶用户偏好“工具测评与工作流”。",
      evidence: ["问卷 200 份 + 评论区意图标注"],
      handoff: "h4",
    },
  };

  const CONTENT = {
    c1: {
      id: "c1", type: "内容对象",
      cover: "AI",
      title: "OpenAI 新模型对小红书选题的影响",
      meta: "8月18日 · 来自研究与洞察",
      owner: "cz",
      status: "制作中", statusCls: "tag-working",
      source: "r1",
      plan: "结构：判断 → 3 个实测示例 → 工具清单 → 下一步建议",
      publish: "预计 8/24 发布",
      metrics: null,
    },
    c2: {
      id: "c2", type: "内容对象",
      cover: "测评",
      title: "AI 硬件测评：谁更适合入门",
      meta: "8月20日 · 待发布",
      owner: "lr",
      status: "待发布", statusCls: "tag",
      source: null,
      plan: "5 款设备横向对比，输出“入门推荐 / 进阶推荐”结论",
      publish: "8/22 18:00",
      metrics: null,
    },
    c3: {
      id: "c3", type: "内容对象",
      cover: "绘画",
      title: "小红书 AI 绘画教程 #3",
      meta: "8月21日 · 制作中",
      owner: "cz",
      status: "制作中", statusCls: "tag-working",
      source: null,
      plan: "聚焦“零基础：提示词三步走”，附带 10 组可直接复制的提示词",
      publish: "预计 8/22 完成",
      metrics: null,
    },
    c4: {
      id: "c4", type: "内容对象",
      cover: "变现",
      title: "AIGC 变现路径盘点",
      meta: "8月25日 · 待确认方向",
      owner: "wy",
      status: "待确认", statusCls: "tag-needs",
      source: null,
      plan: "盘点 4 类可行路径，避免夸大收益；合规先行",
      publish: "方向确认后 5 天内",
      metrics: null,
    },
  };

  const HANDOFFS = {
    h1: {
      id: "h1",
      title: "交接至 内容运营：生成 3 个实测选题",
      from: { empId: "wy", resp: "研究与洞察" },
      to: { empId: "cz", resp: "内容运营" },
      sourceResult: "实测型笔记互动率高于资讯型 34%（OpenAI 新模型研究）",
      evidence: ["竞品选题周报.csv", "搜索词热度快照（8/12–8/19）"],
      status: "等待对方接收", statusCls: "tag",
      nextWork: "陈真输出 3 个可执行选题方向（预计 8/23 前）",
    },
    h2: {
      id: "h2",
      title: "交接至 李然：发布前检查（AI 绘画教程 #3）",
      from: { empId: "cz", resp: "内容运营 / 制作" },
      to: { empId: "lr", resp: "内容运营 / 发布排期" },
      sourceResult: "教程 #2 发布后收藏率 8.2%，超周期均值 3pt",
      evidence: ["教程 #3 素材包", "提示词集合.md", "发布文案草稿"],
      status: "准备中", statusCls: "tag-working",
      nextWork: "陈真制作完成 → 李然接手做发布前 Checklist",
    },
    h3: {
      id: "h3",
      title: "交接至 内容运营：调整内容结构模板",
      from: { empId: "cz", resp: "研究与洞察（协作）" },
      to: { empId: "cz", resp: "内容运营" },
      sourceResult: "头部账号“教程 + 工具清单”组合优势明显",
      evidence: ["5 个对标账号结构对比表"],
      status: "接收中", statusCls: "tag-working",
      nextWork: "内容结构模板 v2 调整完成后试点 2 条内容",
    },
    h4: {
      id: "h4",
      title: "交接至 增长与评估：验证分层的关注转化",
      from: { empId: "lr", resp: "研究与洞察（协作）" },
      to: { empId: "lr", resp: "增长与评估" },
      sourceResult: "受众分层：入门偏教程 / 进阶偏工作流",
      evidence: ["问卷 200 份原始数据", "评论意图标注 JSON"],
      status: "已归档", statusCls: "tag",
      nextWork: "增长侧按分层在 9 月安排 A/B 选题节奏",
    },
  };

  /* =========================================================
     THEME
     ========================================================= */
  function readTheme() {
    try { return localStorage.getItem(STORAGE_KEYS.THEME) || "system"; } catch (_) { return "system"; }
  }
  function writeTheme(t) { try { localStorage.setItem(STORAGE_KEYS.THEME, t); } catch (_) {} }
  function applyTheme(t) {
    const html = document.documentElement;
    html.setAttribute("data-theme", t);
    const mode = t === "system"
      ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light")
      : t;
    html.classList.remove("light", "dark");
    html.classList.add(mode);
    const btn = document.querySelector('[data-dom-id="theme-toggle"]');
    if (btn) {
      btn.textContent = t === "system" ? "🖥️" : (t === "dark" ? "🌙" : "🌞");
      btn.setAttribute("aria-label", "主题：" + t);
      btn.title = "主题：" + t + "（点击切换 system → dark → light）";
    }
  }
  function cycleTheme() {
    const order = ["system", "dark", "light"];
    const curr = readTheme();
    const next = order[(order.indexOf(curr) + 1) % order.length];
    writeTheme(next);
    applyTheme(next);
  }

  /* =========================================================
     SHELL STATE
     ========================================================= */
  function readShellState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEYS.SHELL_STATE);
      return raw ? JSON.parse(raw) : {};
    } catch (_) { return {}; }
  }
  function writeShellState(s) {
    try { localStorage.setItem(STORAGE_KEYS.SHELL_STATE, JSON.stringify(s)); } catch (_) {}
  }
  function applyShellState() {
    const state = readShellState();
    const shell = document.querySelector(".ms-shell");
    if (!shell) return;
    if (state.navCollapsed) shell.classList.add("nav-collapsed");
    if (state.contextCollapsed) {
      shell.classList.remove("with-context");
      shell.classList.add("context-collapsed");
    }
    if (state.utilityOpen) shell.classList.add("with-utility");
    if (state.assistantOpen) {
      shell.classList.add("assistant-open");
      const d = document.querySelector(".ms-assistant-drawer");
      if (d) d.classList.remove("collapsed");
    }
  }
  function updateShellFromDOM() {
    const shell = document.querySelector(".ms-shell");
    if (!shell) return;
    writeShellState({
      navCollapsed: shell.classList.contains("nav-collapsed"),
      contextCollapsed: shell.classList.contains("context-collapsed"),
      utilityOpen: shell.classList.contains("with-utility"),
      assistantOpen: shell.classList.contains("assistant-open"),
    });
  }
  function toggleNav() {
    const shell = document.querySelector(".ms-shell");
    if (!shell) return;
    shell.classList.toggle("nav-collapsed");
    updateShellFromDOM();
  }
  function toggleContext() {
    const shell = document.querySelector(".ms-shell");
    if (!shell) return;
    if (shell.classList.contains("context-collapsed") || !shell.classList.contains("with-context")) {
      shell.classList.add("with-context");
      shell.classList.remove("context-collapsed", "context-iconrail");
    } else {
      shell.classList.remove("with-context");
      shell.classList.add("context-collapsed");
    }
    updateShellFromDOM();
  }
  function toggleUtility(force) {
    const shell = document.querySelector(".ms-shell");
    if (!shell) return;
    if (typeof force === "boolean") shell.classList.toggle("with-utility", force);
    else shell.classList.toggle("with-utility");
    updateShellFromDOM();
  }
  function toggleAssistant() {
    const shell = document.querySelector(".ms-shell");
    const drawer = document.querySelector(".ms-assistant-drawer");
    if (!shell || !drawer) return;
    const open = drawer.classList.toggle("collapsed") === false;
    shell.classList.toggle("assistant-open", open);
    updateShellFromDOM();
  }
  function closeAssistant() {
    const shell = document.querySelector(".ms-shell");
    const drawer = document.querySelector(".ms-assistant-drawer");
    if (shell) shell.classList.remove("assistant-open");
    if (drawer) drawer.classList.add("collapsed");
    updateShellFromDOM();
  }

  /* =========================================================
     UX CONTEXT PERSISTENCE (employee / object restore)
     ========================================================= */
  function readUX() {
    try {
      const raw = localStorage.getItem(STORAGE_KEYS.UX_CONTEXT);
      return raw ? JSON.parse(raw) : {};
    } catch (_) { return {}; }
  }
  function writeUX(patch) {
    const cur = readUX();
    const next = Object.assign({}, cur, patch);
    try { localStorage.setItem(STORAGE_KEYS.UX_CONTEXT, JSON.stringify(next)); } catch (_) {}
  }

  /* =========================================================
     UTILITY RENDER
     ========================================================= */
  const utilStack = []; // simple back-stack within one page load

  function clearSelected() {
    document.querySelectorAll(".is-selected").forEach((el) => el.classList.remove("is-selected"));
  }
  function markSelected(anchor) {
    if (!anchor) return;
    const candidates = [".insight-card", ".content-row", ".surface-card", ".station-head", "tr"];
    for (const sel of candidates) {
      const p = anchor.closest(sel);
      if (p) { p.classList.add("is-selected"); return p; }
    }
  }

  function openUtility(html, anchor) {
    const shell = document.querySelector(".ms-shell");
    const utilContent = document.querySelector(".util-content");
    if (!utilContent) return;
    if (shell) shell.classList.add("with-utility");
    updateShellFromDOM();
    // push current snapshot to stack if any
    if (utilContent.dataset.viewKey) {
      utilStack.push({
        viewKey: utilContent.dataset.viewKey,
        viewPayload: utilContent.dataset.viewPayload || null,
      });
    }
    utilContent.innerHTML = html;
    clearSelected();
    markSelected(anchor);
    bindUtilityActions();
  }

  function setUtilityView(viewKey, payload, anchor, opts) {
    opts = opts || {};
    const utilTitle = document.querySelector(".ms-pane-util .pane-title");
    const utilContent = document.querySelector(".util-content");
    if (!utilContent) return;
    // CONFLICT C1/C2 FIX：Conversation / Workstation / Profile 永远不在 Utility，统一路由到 Main。
    if (viewKey === "conversation") { setMainView("conversation", payload); return; }
    if (viewKey === "workstation") { setMainView("workstation", payload); return; }
    if (viewKey === "profile") { setMainView("profile", payload); return; }

    let html = "";
    let titleText = "工具";
    switch (viewKey) {
      case "employee":
        titleText = "员工 · 详情"; // Utility 仅 Detail，不含 Conversation
        html = renderEmployeeQuickPanel(payload);
        break;
      case "handoff":
        titleText = "交接详情";
        html = renderHandoffDetail(payload);
        break;
      case "research":
        titleText = "研究详情";
        html = renderResearchDetail(payload);
        break;
      case "content":
        titleText = "内容详情";
        html = renderContentDetail(payload);
        break;
      case "work-detail":
        titleText = "当前工作详情";
        html = renderWorkDetail(payload);
        break;
      case "employee-handoff":
        titleText = "当前交接";
        html = renderHandoffDetail(payload.handoff, { fromEmployee: payload.empId });
        break;
      default:
        html = `<div class="preview-cover">选择对象查看详情</div><div class="preview-title">未选中对象</div><div class="preview-body">点击任意内容对象、洞察、反馈或员工，可在此处展开。</div>`;
    }
    if (utilTitle) utilTitle.textContent = titleText;
    utilContent.dataset.viewKey = viewKey;
    utilContent.dataset.viewPayload = JSON.stringify(payload || null);
    openUtility(html, anchor);
    // T3 位置：Utility 打开时，把 Main 的 T3 隐藏，Utility Header 内的 T3 显示（实现 Delta-X7：T3 随展开转移到 Utility Header 右侧）。
    reflectT3Placement();
  }

  // Shell Contract §1.5.2 / §1.5.3：T3 在 Utility 展开时转移到 Utility Header；折叠时回到 Main Header 右侧
  function reflectT3Placement() {
    const shell = document.querySelector(".ms-shell");
    const utilOpen = shell && shell.classList.contains("with-utility");
    const t3Main = document.querySelector(".ms-main-head [data-action='toggle-utility']");
    const t3Util = document.querySelector(".ms-util-head [data-action='toggle-utility']");
    if (t3Main) t3Main.style.display = utilOpen ? "none" : "";
    if (t3Util) t3Util.style.display = utilOpen ? "" : "none";
  }

  function renderUtilTrail(items) {
    if (!items || !items.length) return "";
    const parts = items.map((it, i) => {
      if (it.href) return `<a data-util-back="${it.href}">${it.label}</a>`;
      if (it.onclick) return `<a data-util-action="${it.onclick}">${it.label}</a>`;
      return `<span>${it.label}</span>`;
    });
    return `<div class="util-trail">${parts.join('<span class="sep">/</span>')}</div>`;
  }

  function employeeChipSmall(emp) {
    if (!emp) return "";
    return `<span class="identity" data-object="employee" data-id="${emp.id}"><span class="avatar" style="width:18px;height:18px;font-size:11px;background:${emp.color};color:var(--ui-action-primary-fg);">${emp.avatar}</span>${emp.name}</span>`;
  }

  /* ---------------- Employee Quick Panel（Utility Detail · 不含 Conversation · Frozen §3.14） ----------------
     Section 分层：
       I.  Identity（他是谁：姓名/岗位/组织归属/核心职责/核心能力）
       II. Current Work Summary（现在在做什么：状态/当前责任/工作/交接/最近结果）
     信息边界遵守：不展开完整 Capability/Assignment/History/Model/Skill
  */
  function renderEmployeeQuickPanel(empId) {
    const e = EMPLOYEES[empId];
    if (!e) return `<div class="preview-title">员工不存在</div>`;
    const trail = renderUtilTrail([{ label: "员工" }, { label: e.name }]);
    const curWork = e.currentWork;
    const curWorkEl = curWork
      ? `<div class="eqp-list-item" data-util-action="open-work" data-id="${curWork.id}"><span>${curWork.title}</span><span class="tag ${curWork.tagClass || "tag"}">${curWork.tag}</span></div>`
      : `<div class="eqp-section-body" style="color:var(--ui-text-3)">当前暂无绑定工作</div>`;
    const capsHtml = (e.capabilities || []).slice(0, 3).map((c) => `<span class="tag tag-ctx">${c}</span>`).join(" ");
    const resultsHtml = (e.results || []).slice(0, 3).map((r) => {
      const openAttr = (r.linkKind && r.linkId) ? ` style="cursor:pointer;color:var(--ui-accent);" data-object="${r.linkKind}" data-id="${r.linkId}"` : "";
      return `<div class="eqp-result"${openAttr}><span class="tag ${r.tagClass || "tag-ctx"}" style="margin-right:8px;">${r.tag}</span>${r.title}</div>`;
    }).join("");
    const handoffEl = e.handoff
      ? `<div class="eqp-list-item" data-util-action="open-employee-handoff" data-id="${e.handoff.id}"><span>${e.handoff.title}</span><span class="tag ${e.handoff.statusCls || "tag"}">${e.handoff.status}</span></div>`
      : "";
    return `
${trail}
<section class="eqp">
  <header class="eqp-head">
    <div class="eqp-avatar" style="background:${e.color};">${e.avatar}</div>
    <div class="eqp-id">
      <div class="eqp-name">${e.name}</div>
      <div class="eqp-role">${e.role} · ${e.org || ""}</div>
    </div>
  </header>

  <div class="eqp-section">
    <div class="eqp-section-title">核心职责</div>
    <div class="eqp-section-body">${e.coreResponsibility || e.responsibility || "—"}</div>
  </div>

  <div class="eqp-section">
    <div class="eqp-section-title">核心能力</div>
    <div class="eqp-section-body">${capsHtml || '<span class="tag tag-ctx">—</span>'}</div>
  </div>

  <div class="eqp-section">
    <div class="eqp-section-title">当前状态</div>
    <div class="eqp-section-body"><span class="eqp-status"><span class="dot ${employeeStatusDot(e) || ""}"></span>${employeeStatusLabel(e)}</span></div>
  </div>

  <div class="eqp-section">
    <div class="eqp-section-title">当前工作</div>
    ${curWorkEl}
  </div>

  <div class="eqp-section">
    <div class="eqp-section-title">最近成果</div>
    ${resultsHtml || `<div class="eqp-section-body" style="color:var(--ui-text-3)">暂未记录</div>`}
  </div>

  ${handoffEl ? `<div class="eqp-section low">
    <div class="eqp-section-title">交接</div>
    ${handoffEl}
  </div>` : ""}

  <footer class="eqp-actions">
    <button class="btn-primary btn-sm eqp-primary" data-util-action="open-conversation" data-id="${e.id}">直接对话</button>
    <div class="eqp-secondary">
      <button class="btn-ghost btn-sm" data-util-action="open-employee-profile" data-id="${e.id}">资料</button>
      <button class="btn-ghost btn-sm" data-util-action="open-workstation" data-id="${e.id}">工作站</button>
      ${handoffEl ? `<button class="btn-ghost btn-sm" data-util-action="open-employee-handoff" data-id="${e.handoff.id}">交接</button>` : ""}
    </div>
  </footer>
</section>`;
  }

  /* ---------------- Employee Profile（Main Focus View · ≠ Workstation） ----------------
     回答：“这个员工是谁？”  —— Identity / Role / Responsibility / Capability / Business & Workspace Relation / Results Highlights
     注意：不含 Composer / 不含 Deep Work grid。信息边界遵守 Quick Panel 中 profile 摘要的扩展。
  */
  function renderMainProfile(empId) {
    const e = EMPLOYEES[empId];
    if (!e) return ``;
    const p = e.profile || {};
    const capsHtml = (e.capabilities || []).map((c) => `<span class="tag tag-ctx">${c}</span>`).join(" ");
    const highHtml = (p.highlights || []).map((h) => `<li>${h}</li>`).join("");
    const resultsHtml = (e.results || []).slice(0, 5).map((r) => {
      const openAttr = (r.linkKind && r.linkId) ? ` style="cursor:pointer;color:var(--ui-accent);" data-object="${r.linkKind}" data-id="${r.linkId}"` : "";
      return `<div class="eqp-result"${openAttr}><span class="tag ${r.tagClass || "tag-ctx"}" style="margin-right:8px;">${r.tag}</span>${r.title}</div>`;
    }).join("");
    return `
  <div class="empprofile" data-emp-id="${e.id}" data-view="profile">
    <div class="empws-head">
      <div class="empws-id">
        <div class="empws-back" data-main-action="back-surface" title="返回">← 返回</div>
        <div class="empws-avatar" style="background:${e.color};">${e.avatar}</div>
        <div>
          <div class="empws-name">${e.name} <span class="empws-badge deep">员工资料</span></div>
          <div class="empws-role">${e.role} · 员工资料</div>
        </div>
      </div>
      <div class="empws-status">
        <span class="eqp-status"><span class="dot ${employeeStatusDot(e)}"></span>${employeeStatusLabel(e)}</span>
        <button class="btn-secondary btn-sm" data-main-action="to-conversation" data-id="${e.id}">直接对话 →</button>
        <button class="btn-secondary btn-sm" data-main-action="to-workstation" data-id="${e.id}">完整工作站 →</button>
      </div>
    </div>

    <div class="empws-ctx">这里只说明她是谁、能做什么；要推进具体工作请点「直接对话」。</div>

    <div class="empws-grid">
      <section class="empws-section">
        <div class="section-label">基本信息</div>
        <dl class="kv">
          <dt>组织归属</dt><dd>${e.org || "—"}</dd>
          <dt>岗位角色</dt><dd>${e.role || "—"}</dd>
          <dt>入职</dt><dd>${p.joined || "—"}</dd>
          <dt>层级</dt><dd>${p.level || "—"}</dd>
          <dt>汇报给</dt><dd>${p.reportTo || "—"}</dd>
        </dl>
      </section>

      <section class="empws-section">
        <div class="section-label">核心职责</div>
        <div class="paragraph">${e.coreResponsibility || e.responsibility || "—"}</div>
        <div style="margin-top:var(--ui-sp-3);">
          <div class="section-label">核心能力</div>
          <div style="display:flex; gap:var(--ui-sp-2); flex-wrap:wrap; margin-top:var(--ui-sp-2);">
            ${capsHtml || '<span class="tag tag-ctx">—</span>'}
          </div>
        </div>
      </section>

      <section class="empws-section">
        <div class="section-label">业务与团队关系</div>
        <div class="paragraph">${e.responsibility}</div>
        <div class="paragraph" style="margin-top:var(--ui-sp-2);">上下文：${e.context || "—"}</div>
      </section>

      <section class="empws-section">
        <div class="section-label">代表成果</div>
        <div class="ev-list">${resultsHtml || '<div class="eqp-section-body">暂未记录</div>'}</div>
      </section>

      <section class="empws-section" style="grid-column:1 / -1;">
        <div class="section-label">成长亮点</div>
        <ul style="margin:0; padding-left:1.2em; display:flex; flex-direction:column; gap:var(--ui-sp-2); font-size:var(--ui-fs-2); color:var(--ui-text-2); line-height:var(--ui-lh-loose);">
          ${highHtml || '<li>—</li>'}
        </ul>
      </section>
    </div>
  </div>`;
  }

  /* ---------------- Conversation & Workstation：永远在 Main（Frozen §3.12 / §3.14 / Delta-X9） ---------------- */
  function sharedComposerSlots(emp, opts) {
    // 内嵌式 Composer（原则 E）：所有操作置于输入框内部，无独立文字工具栏。
    // ＋ = 更多（添加资料 / 访问权限 / 工作模式）；目标▾ = 工作方向；Auto▾ = 执行方式（模型·智能体）。
    // 未真实连接的能力以 disabled + tooltip 说明，不伪造接通。
    opts = opts || {};
    const placeholder = opts.placeholder || `直接跟${emp.name}说话，她可以引用当前上下文...（原型：回车发送 / ⇧回车换行）`;
    const empContext = opts.context || "";
    return `
  <div class="composer-shell">
    <div class="composer-ctxline">${empContext}</div>
    <div class="composer-inline">
      <textarea class="composer-input" rows="1" placeholder="${placeholder}"></textarea>
      <div class="composer-inline-actions">
        <button class="composer-chip" title="更多操作（原型示意）">＋</button>
        <button class="composer-chip" title="目标 / 工作方向（由运行时真值决定）">目标 ▾</button>
        <button class="composer-chip" title="执行方式：模型 · 智能体 · Auto（默认由员工绑定能力决定）">Auto ▾</button>
        <button class="composer-chip icon" disabled title="语音：仅当 Provider 原生支持时显示">🎙</button>
        <button class="btn-primary composer-send">发送</button>
      </div>
    </div>
  </div>`;
  }

  // 返回员工的当前 assignment 上下文行（用于 Conversation / Workstation 顶栏）
  function employeeAssignmentContextLine(emp) {
    const curPage = document.body.dataset.page || "overview";
    const surfaceName = PAGE_DISPLAY_NAME[curPage] || curPage;
    const pieces = ["当前上下文：AI 科技 · " + surfaceName, "员工：" + emp.name + "（" + emp.role + "）"];
    if (emp.currentWork) pieces.push("工作对象：" + emp.currentWork.title);
    return pieces.join(" · ");
  }

  // Main Workstation：Conversation-first（C1 FIX · Shell Contract §3.1 Delta-S1 / §3.14）
  function renderMainConversation(empId) {
    const e = EMPLOYEES[empId];
    if (!e) return ``;
    const opener = `你好，我是${e.name}。我当前正在处理：${e.currentWork ? e.currentWork.title : "当前暂无绑定对象"}。需要我调整优先级、补充上下文或直接推进吗？`;
    const ctxLine = employeeAssignmentContextLine(e);
    const curWork = e.currentWork;
    const handoff = e.handoff ? HANDOFFS[e.handoff.id] : null;
    return `
  <div class="empws" data-emp-id="${e.id}" data-view="conversation">
    <div class="empws-head">
      <div class="empws-id">
        <div class="empws-back" data-main-action="back-surface" title="返回">← 返回</div>
        <div class="empws-avatar" style="background:${e.color};">${e.avatar}</div>
        <div>
          <div class="empws-name">${e.name} <span class="empws-badge">直接对话</span></div>
          <div class="empws-role">${e.role} · 直接对话</div>
        </div>
      </div>
      <div class="empws-status">
        <span class="eqp-status"><span class="dot ${employeeStatusDot(e)}"></span>${employeeStatusLabel(e)}</span>
        <button class="btn-secondary btn-sm" data-main-action="to-workstation" data-id="${e.id}">完整工作站 →</button>
      </div>
    </div>

    <div class="empws-ctx">${ctxLine}</div>

    <div class="empws-body">
      <div class="empws-msg them">${opener}</div>
      ${curWork ? `<div class="empws-msg them bounded">
        <div class="section-label">当前工作</div>
        <div class="row-compact"><span class="tag ${curWork.tagClass || "tag"}">${curWork.tag}</span> ${curWork.title}</div>
        <a class="link-inline" data-object="${curWork.type === "研究对象" ? "research" : "content"}" data-id="${curWork.id}">查看对象详情 →</a>
      </div>` : ""}
      ${handoff ? `<div class="empws-msg them bounded">
        <div class="section-label">当前交接</div>
        <div class="ho-flow">
          <span class="ho-node">${employeeChipSmall(EMPLOYEES[handoff.from.empId])} · ${handoff.from.resp}</span>
          <span class="ho-arrow">→</span>
          <span class="ho-node">${employeeChipSmall(EMPLOYEES[handoff.to.empId])} · ${handoff.to.resp}</span>
        </div>
        <div class="row-compact"><span class="tag ${handoff.statusCls || "tag"}">${handoff.status}</span> ${handoff.title}</div>
        <a class="link-inline" data-object="handoff" data-id="${handoff.id}">查看交接详情 →</a>
      </div>` : ""}
    </div>

    <div class="empws-foot">
      ${sharedComposerSlots(e, { placeholder: `直接跟${e.name}说话，她会结合当前上下文推进...`, context: ctxLine })}
    </div>
  </div>`;
  }

  // Main Workstation：Full Employee Workstation（C2 FIX · Deep Work Mode · Frozen Delta-X9 / Delta-S1）
  function renderMainWorkstation(empId) {
    const e = EMPLOYEES[empId];
    if (!e) return ``;
    const ctxLine = employeeAssignmentContextLine(e);
    const handoff = e.handoff ? HANDOFFS[e.handoff.id] : null;
    const curWork = e.currentWork;
    const opener = `你好，我是${e.name}。我现在正在做：${curWork ? curWork.title : "当前暂无绑定工作"}。可以直接告诉我要调整什么，或者让我把下一步做完。`;
    const worksHtml = [curWork].filter(Boolean).map((w) => {
      const kind = w.type === "研究对象" ? "research" : "content";
      return `<div class="eqp-list-item" data-object="${kind}" data-id="${w.id}"><span>${w.title} · ${w.type}</span><span class="tag ${w.tagClass || "tag"}">${w.tag}</span></div>`;
    }).join("");
    const resultsHtml = (e.results || []).map((r) => {
      const openAttr = (r.linkKind && r.linkId) ? ` style="cursor:pointer;color:var(--ui-accent);" data-object="${r.linkKind}" data-id="${r.linkId}"` : "";
      return `<div class="eqp-result"${openAttr}><span class="tag ${r.tagClass || "tag-ctx"}" style="margin-right:8px;">${r.tag}</span>${r.title}</div>`;
    }).join("");
    const handoffPanel = handoff ? `<section class="empws-section">
        <div class="section-label">待处理交接</div>
        <div class="ho-flow">
          <span class="ho-node">${employeeChipSmall(EMPLOYEES[handoff.from.empId])} · ${handoff.from.resp}</span>
          <span class="ho-arrow">→</span>
          <span class="ho-node">${employeeChipSmall(EMPLOYEES[handoff.to.empId])} · ${handoff.to.resp}</span>
        </div>
        <div class="row-compact"><span class="tag ${handoff.statusCls || "tag"}">${handoff.status}</span> ${handoff.title}</div>
        <a class="link-inline" data-object="handoff" data-id="${handoff.id}">查看交接详情 →</a>
      </section>` : "";
    // 原则 C：第一屏 = 员工 / 状态 / 对话 / 输入框。
    // 职责 · 工作 · 交接 · 结果 → 对话内轻引用 + 一条可展开的工作面板（Frozen 能力仍在，只是不永久占屏）。
    return `
  <div class="empws deep conv-first" data-emp-id="${e.id}" data-view="workstation">
    <div class="empws-head">
      <div class="empws-id">
        <div class="empws-back" data-main-action="back-surface" title="返回">← 返回</div>
        <div class="empws-avatar" style="background:${e.color};">${e.avatar}</div>
        <div>
          <div class="empws-name">${e.name} <span class="empws-badge deep">完整工作台</span></div>
          <div class="empws-role">${e.role} · ${e.org || ""}</div>
        </div>
      </div>
      <div class="empws-status">
        <span class="eqp-status"><span class="dot ${employeeStatusDot(e)}"></span>${employeeStatusLabel(e)}</span>
      </div>
    </div>

    <div class="empws-ctx">${ctxLine}</div>

    <div class="empws-body" data-conv-emp="${e.id}">
      <div class="empws-msg them">${opener}</div>
      ${curWork ? `<div class="empws-msg them bounded">
        <div class="section-label">正在做</div>
        <div class="row-compact"><span class="tag ${curWork.tagClass || "tag"}">${curWork.tag}</span> ${curWork.title}</div>
        <a class="link-inline" data-object="${curWork.type === "研究对象" ? "research" : "content"}" data-id="${curWork.id}">查看详情 →</a>
      </div>` : ""}
      ${handoff ? `<div class="empws-msg them bounded">
        <div class="section-label">需要交接</div>
        <div class="row-compact"><span class="tag ${handoff.statusCls || "tag"}">${handoff.status}</span> ${handoff.title}</div>
        <a class="link-inline" data-object="handoff" data-id="${handoff.id}">查看交接 →</a>
      </div>` : ""}
    </div>

    <details class="ws-panel">
      <summary class="ws-panel-summary">展开工作面板 · 职责 / 工作 / 交接 / 结果</summary>
      <div class="ws-panel-body">
        <section class="empws-section">
          <div class="section-label">当前职责</div>
          <div class="paragraph">${e.responsibility}</div>
        </section>
        <section class="empws-section">
          <div class="section-label">当前工作</div>
          ${worksHtml || '<div class="eqp-section-body">暂无明确工作对象</div>'}
        </section>
        ${handoffPanel}
        <section class="empws-section">
          <div class="section-label">最近成果</div>
          <div class="ev-list">${resultsHtml || '<div class="eqp-section-body">暂未记录</div>'}</div>
        </section>
      </div>
    </details>

    <div class="empws-foot">
      ${sharedComposerSlots(e, { placeholder: `直接跟${e.name}说话，她会结合当前工作推进...`, context: ctxLine })}
    </div>
  </div>`;
  }

  // Main Pane 视图切换
  // - 原 Surface 内容会被保存在 .ms-original-surface（仅首次），以便「返回」时恢复
  function setMainView(viewKey, payload) {
    const main = document.querySelector(".ms-pane-main");
    if (!main) return;
    const scroll = main.querySelector(":scope > .ms-scroll");
    if (!scroll) return;

    // 保存原始 Surface
    let stash = scroll.querySelector(":scope > .ms-original-surface");
    if (!stash) {
      const children = Array.prototype.slice.call(scroll.children);
      stash = document.createElement("div");
      stash.className = "ms-original-surface";
      stash.style.display = "none";
      children.forEach((c) => stash.appendChild(c));
      scroll.appendChild(stash);
    } else {
      // 移除已有 main workstation 视图（覆盖切换）
      const old = scroll.querySelector(":scope > .ms-workstation-view");
      if (old) old.remove();
    }

    const view = document.createElement("div");
    view.className = "ms-workstation-view";
    view.dataset.view = viewKey;
    if (viewKey === "conversation") view.innerHTML = renderMainConversation(payload);
    else if (viewKey === "workstation") view.innerHTML = renderMainWorkstation(payload);
    else if (viewKey === "profile") view.innerHTML = renderMainProfile(payload);
    scroll.appendChild(view);

    // 同步：Utility 可选择回 Employee Detail（保持 Quick Panel 可辅助查阅）；也可关闭 Utility。
    const empId = payload;
    if (empId && EMPLOYEES[empId]) {
      // 仅当当前 Utility 不是员工详情时才自动打开，避免覆盖用户正在看的 handoff / research detail
      const utilContent = document.querySelector(".util-content");
      const current = utilContent ? utilContent.dataset.viewKey : "";
      if (!current || current === "default") {
        setUtilityView("employee", empId, null, { silent: true });
      }
    }

    // 绑定 Main 内独有 actions + object clicks + composer
    bindMainWorkstation(view);

    // 滚动到顶部，聚焦当前工作站
    if (scroll.scrollTo) scroll.scrollTo({ top: 0, behavior: "smooth" });
  }

  function restoreOriginalSurface() {
    const main = document.querySelector(".ms-pane-main");
    if (!main) return;
    const scroll = main.querySelector(":scope > .ms-scroll");
    if (!scroll) return;
    const stash = scroll.querySelector(":scope > .ms-original-surface");
    const view = scroll.querySelector(":scope > .ms-workstation-view");
    if (!stash) return;
    if (view) view.remove();
    stash.style.display = "";
    // 还原：把 stash 的孩子放回到 scroll 下一级
    while (stash.firstChild) scroll.insertBefore(stash.firstChild, stash);
    stash.remove();
    if (scroll.scrollTo) scroll.scrollTo({ top: 0, behavior: "smooth" });
  }

  function bindMainWorkstation(viewEl) {
    viewEl.querySelectorAll("[data-main-action]").forEach((b) => {
      if (b.dataset.bound) return;
      b.dataset.bound = "1";
      b.addEventListener("click", (e) => {
        e.preventDefault();
        const act = b.getAttribute("data-main-action");
        const id = b.getAttribute("data-id");
        if (act === "back-surface") restoreOriginalSurface();
        if (act === "to-workstation" && id) setMainView("workstation", id);
        if (act === "to-conversation" && id) setMainView("conversation", id);
      });
    });

    viewEl.querySelectorAll("[data-object]").forEach((el) => {
      if (el.dataset.bound) return;
      el.dataset.bound = "1";
      el.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        const kind = el.getAttribute("data-object");
        const id = el.getAttribute("data-id");
        if (kind && id) setUtilityView(kind, id, el);
      });
    });

    // Composer 发送：找到最近的 messages 容器写入
    viewEl.querySelectorAll(".composer-shell").forEach((shell) => {
      if (shell.dataset.bound) return;
      shell.dataset.bound = "1";
      const ta = shell.querySelector(".composer-input");
      const sendBtn = shell.querySelector(".composer-send");
      const empws = shell.closest(".empws");
      const empId = empws ? empws.dataset.empId : null;
      const e = EMPLOYEES[empId || ""];
      const msgs = empws ? (empws.querySelector(".empws-body[data-conv-emp]") || empws.querySelector(":scope > .empws-body")) : null;
      if (!ta || !msgs || !e) return;

      function send() {
        const text = ta.value.trim(); if (!text) return;
        const me = document.createElement("div"); me.className = "empws-msg me"; me.textContent = text;
        msgs.appendChild(me); ta.value = "";
        setTimeout(() => {
          const them = document.createElement("div");
          them.className = "empws-msg them";
          them.textContent = "收到。我会结合当前上下文立即推进：" + (e.currentWork ? e.currentWork.title : "待明确工作对象") + "。";
          msgs.appendChild(them);
          msgs.scrollTop = msgs.scrollHeight;
        }, 360);
        msgs.scrollTop = msgs.scrollHeight;
      }
      if (sendBtn) sendBtn.addEventListener("click", send);
      ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); send(); }
      });
    });
  }

  /* ---------------- Research Detail ---------------- */
  function renderResearchDetail(id) {
    const r = RESEARCH[id];
    if (!r) return ``;
    const owner = EMPLOYEES[r.owner];
    const handoff = r.handoff ? HANDOFFS[r.handoff] : null;
    const trail = renderUtilTrail([
      { label: "研究对象" },
      { label: r.title },
    ]);
    const evHtml = r.evidence.map((e) => `<div class="ev-item"><span>${e}</span></div>`).join("");
    // 原则 D：先说人的判断和下一步，再降级放来源与依据。
    return `${trail}
<section class="detail">
  <div class="hero">
    <div class="hero-title">${r.title}</div>
    <div class="hero-meta">${employeeChipSmall(owner)} · ${owner.role} <span class="tag ${r.statusCls || "tag"}">${r.status}</span></div>
  </div>
  <div>
    <div class="section-label">${owner.name}的判断</div>
    <div class="paragraph lead">${r.claim}</div>
  </div>
  ${handoff ? `<div>
    <div class="section-label">下一步</div>
    <div class="paragraph">${handoff.nextWork}</div>
    <a class="link-inline" data-util-action="open-handoff" data-id="${handoff.id}">查看交接 →</a>
  </div>` : ""}
  <div class="action-row">
    <button class="btn-primary btn-sm" data-util-action="open-conversation" data-id="${r.owner}">直接对话</button>
  </div>
  <details class="obj-meta">
    <summary class="obj-meta-summary">依据与来源（${r.evidence.length}）</summary>
    <div class="ev-list">${evHtml}</div>
    <div class="obj-meta-line">来源：${r.source}</div>
  </details>
</section>`;
  }

  /* ---------------- Content Detail ---------------- */
  function renderContentDetail(id) {
    const c = CONTENT[id];
    if (!c) return ``;
    const owner = EMPLOYEES[c.owner];
    const trail = renderUtilTrail([{ label: "内容对象" }, { label: c.title }]);
    const srcLine = c.source
      ? `来自研究：<a class="identity" data-object="research" data-id="${c.source}">${RESEARCH[c.source]?.title || c.source}</a>`
      : `无关联研究`;
    // 原则 D：先说人怎么打算做、什么时候出，再降级放封面/日期/关联。
    return `${trail}
<section class="detail">
  <div class="hero">
    <div class="hero-title">${c.title}</div>
    <div class="hero-meta">${employeeChipSmall(owner)} · ${owner.role} <span class="tag ${c.statusCls || "tag"}">${c.status}</span></div>
  </div>
  <div>
    <div class="section-label">${owner.name}的打算</div>
    <div class="paragraph lead">${c.plan}</div>
  </div>
  <div>
    <div class="section-label">下一步</div>
    <div class="paragraph">${c.publish}</div>
  </div>
  <div class="action-row">
    <button class="btn-primary btn-sm" data-util-action="open-conversation" data-id="${c.owner}">直接对话</button>
  </div>
  <details class="obj-meta">
    <summary class="obj-meta-summary">更多信息</summary>
    <div class="obj-meta-line">${srcLine}</div>
    <div class="obj-meta-line">封面：${c.cover} · ${c.meta}</div>
  </details>
</section>`;
  }

  /* ---------------- Work detail (from Current Work) ---------------- */
  function renderWorkDetail(workId) {
    let r = RESEARCH[workId], c = CONTENT[workId];
    if (r) return renderResearchDetail(workId);
    if (c) return renderContentDetail(workId);
    return `<div class="preview-title">未匹配到工作对象详情</div><div class="preview-body">请先在页面上选择一个对象。</div>`;
  }

  /* ---------------- Handoff Detail ---------------- */
  function renderHandoffDetail(id, opts) {
    const h = HANDOFFS[id];
    if (!h) return ``;
    opts = opts || {};
    const from = EMPLOYEES[h.from.empId];
    const to = EMPLOYEES[h.to.empId];
    const trail = renderUtilTrail([
      opts.fromEmployee ? { onclick: "back-to-employee:" + opts.fromEmployee, label: EMPLOYEES[opts.fromEmployee]?.name || "员工" } : { label: "交接" },
      { label: "详情" },
    ]);
    const evHtml = h.evidence.map((e) => `<div class="ev-item"><span>${e}</span><span class="tag tag-ctx">证据</span></div>`).join("");
    return `${trail}
<section class="detail">
  <div class="hero">
    <div class="hero-meta"><span class="tag ${h.statusCls || "tag"}">${h.status}</span></div>
    <div class="hero-title">${h.title}</div>
  </div>

  <div>
    <div class="section-label">交接路径</div>
    <div class="ho-flow">
      <span class="ho-node">${employeeChipSmall(from)} · ${h.from.resp}</span>
      <span class="ho-arrow">→</span>
      <span class="ho-node">${employeeChipSmall(to)} · ${h.to.resp}</span>
    </div>
  </div>

  <div>
    <div class="section-label">来源结果</div>
    <div class="paragraph">${h.sourceResult}</div>
  </div>

  <div>
    <div class="section-label">证据</div>
    <div class="ev-list">${evHtml}</div>
  </div>

  <dl class="kv">
    <dt>下一步工作</dt><dd>${h.nextWork}</dd>
  </dl>

  <div class="action-row">
    <button class="btn-secondary btn-sm" data-util-action="open-employee" data-id="${h.from.empId}">联系 ${from.name}</button>
    <button class="btn-secondary btn-sm" data-util-action="open-employee" data-id="${h.to.empId}">联系 ${to.name}</button>
    <button class="btn-primary btn-sm" onclick="window.CurisApp.navigate('handoff');">进入相关员工工作站 →</button>
  </div>
</section>`;
  }

  /* =========================================================
     UTILITY ACTION BINDING (render后对新插入元素绑定)
     ========================================================= */
  function bindUtilityActions() {
    const util = document.querySelector(".util-content");
    if (!util) return;
    util.querySelectorAll('[data-util-action]').forEach((el) => {
      if (el.dataset.bound) return;
      el.dataset.bound = "1";
      el.addEventListener("click", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        const act = el.getAttribute("data-util-action");
        const id = el.getAttribute("data-id") || "";
        handleUtilityAction(act, id);
      });
    });
    util.querySelectorAll('[data-util-back]').forEach((el) => {
      if (el.dataset.bound) return;
      el.dataset.bound = "1";
      el.addEventListener("click", (ev) => {
        ev.preventDefault();
        const key = el.getAttribute("data-util-back");
        if (key.indexOf("back-to-employee:") === 0) {
          const empId = key.split(":")[1];
          setUtilityView("employee", empId, null);
        }
      });
    });
    // util 内再次出现 employee / research / handoff / content 链接，复用对象映射
    util.querySelectorAll('[data-object]').forEach((el) => {
      if (el.dataset.bound) return;
      el.dataset.bound = "1";
      el.addEventListener("click", (ev) => {
        ev.preventDefault();
        ev.stopPropagation();
        const kind = el.getAttribute("data-object");
        const id = el.getAttribute("data-id");
        openObject(kind, id, el);
      });
    });
    // conversation composer
    util.querySelectorAll(".conv-composer").forEach((wrap) => {
      if (wrap.dataset.bound) return;
      wrap.dataset.bound = "1";
      const ta = wrap.querySelector("textarea");
      const btn = wrap.querySelector("button");
      const section = wrap.closest(".conv");
      const empId = section ? section.dataset.empId : null;
      const msgs = section ? section.querySelector(".conv-msgs") : null;
      const e = EMPLOYEES[empId || ""];
      function send() {
        if (!ta || !msgs || !e) return;
        const text = ta.value.trim(); if (!text) return;
        const me = document.createElement("div");
        me.className = "conv-msg me"; me.textContent = text;
        msgs.appendChild(me);
        ta.value = "";
        setTimeout(() => {
          const them = document.createElement("div");
          them.className = "conv-msg them";
          them.textContent = "收到。我会结合当前上下文立即推进：" + (e.currentWork ? e.currentWork.title : "待明确工作对象") + "。";
          msgs.appendChild(them);
          msgs.scrollTop = msgs.scrollHeight;
        }, 350);
        msgs.scrollTop = msgs.scrollHeight;
      }
      if (btn) btn.addEventListener("click", (ev) => { ev.preventDefault(); send(); });
      if (ta) ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Enter" && !ev.shiftKey) { ev.preventDefault(); send(); }
      });
    });
  }

  function handleUtilityAction(act, id) {
    if (!act) return;
    if (act.indexOf("back-to-employee:") === 0) {
      const empId = act.split(":")[1];
      if (empId) setUtilityView("employee", empId);
      return;
    }
    switch (act) {
      case "open-employee":
        if (id) { writeUX({ lastEmployeeId: id }); setUtilityView("employee", id); }
        break;
      case "open-conversation":
        if (id) setUtilityView("conversation", id);
        break;
      case "open-workstation":
        if (id) setUtilityView("workstation", id);
        break;
      case "open-handoff":
        if (id) setUtilityView("handoff", id);
        break;
      case "open-employee-handoff": {
        if (!id) return;
        const h = HANDOFFS[id];
        // Try to find employee that owns this handoff context for back-link
        let empId = null;
        Object.values(EMPLOYEES).forEach((e) => { if (e.handoff && e.handoff.id === id) empId = e.id; });
        setUtilityView("employee-handoff", { handoff: id, empId: empId });
        break;
      }
      case "open-work":
        if (id) setUtilityView("work-detail", id);
        break;
      case "open-employee-profile":
        // Employee Profile（回答这个员工是谁）放在 Main，≠Workstation
        if (id) { writeUX({ lastEmployeeId: id }); setUtilityView("profile", id); }
        break;
    }
  }

  /* =========================================================
     OBJECT → UTILITY · DISPATCH
     ========================================================= */
  function resolveObjectFromClick(target) {
    // Priority: 员工 identity (王颖/陈真/李然/林薇) > research/content/handoff > 容器
    const empLink = target.closest('[data-object="employee"]') || target.closest(".presence-chip") || target.closest(".station-head") || target.closest(".avatar");
    const handoffLink = target.closest('[data-object="handoff"]') || target.closest(".handoff-link");
    const researchCard = target.closest('[data-object="research"]') || target.closest(".insight-card");
    const contentRow = target.closest('[data-object="content"]') || target.closest(".content-row");
    const surfaceCard = target.closest('[data-object="surface"]') || target.closest(".surface-card");

    // Preference: employee identity wins if explicitly requested (data-object=employee or user clicked avatar/chip/station-head).
    // Explicit handoff affordance (.handoff-link / [data-object=handoff]) ALWAYS wins,
    // even when nested inside an insight card foot (C7/C3.4: Handoff link → Handoff Detail, not Research).
    if (handoffLink && handoffLink !== researchCard && handoffLink !== contentRow) {
      const id = handoffLink.getAttribute("data-id") || resolveHandoffIdFromText(handoffLink);
      if (id) return { kind: "handoff", id, el: handoffLink };
    }

    if (empLink) {
      const explicitId = empLink.getAttribute("data-id");
      if (explicitId) return { kind: "employee", id: explicitId, el: empLink };
      const inferred = inferEmployeeIdFromEl(empLink);
      if (inferred) return { kind: "employee", id: inferred, el: empLink };
    }

    if (researchCard) {
      const id = researchCard.getAttribute("data-id") || resolveResearchIdFromText(researchCard);
      if (id) return { kind: "research", id, el: researchCard };
    }
    if (contentRow) {
      const id = contentRow.getAttribute("data-id") || resolveContentIdFromText(contentRow);
      if (id) return { kind: "content", id, el: contentRow };
    }
    if (surfaceCard) {
      const id = surfaceCard.getAttribute("data-id") || resolveSurfaceCardId(surfaceCard);
      if (id) return { kind: id.kind, id: id.id, el: surfaceCard };
    }

    // Team table employee cell
    const ttCell = target.closest(".tt-name") || target.closest(".tt-role");
    if (ttCell) {
      const tr = ttCell.closest("tr");
      if (tr) {
        const txt = (tr.innerText || tr.textContent || "");
        const e = findEmployeeByText(txt);
        if (e) return { kind: "employee", id: e.id, el: tr };
      }
    }
    return null;
  }

  function findEmployeeByText(text) {
    const names = Object.values(EMPLOYEES).map((e) => e.name);
    for (const e of Object.values(EMPLOYEES)) if (text.indexOf(e.name) >= 0) return e;
    return null;
  }
  function inferEmployeeIdFromEl(el) {
    const t = el.innerText || el.textContent || "";
    const e = findEmployeeByText(t);
    if (e) return e.id;
    // Fallback by avatar letter (王->wy 陈->cz 李->lr 林->lw)
    const ava = (el.querySelector(".pc-avatar, .avatar, .nav-user-ava") || el).textContent.trim().slice(0, 1);
    const map = { "王": "wy", "陈": "cz", "李": "lr", "林": "lw" };
    return map[ava] || null;
  }
  function resolveResearchIdFromText(el) {
    const t = el.innerText || el.textContent || "";
    for (const id of Object.keys(RESEARCH)) if (t.indexOf(RESEARCH[id].title) >= 0) return id;
    return null;
  }
  function resolveContentIdFromText(el) {
    const t = el.innerText || el.textContent || "";
    for (const id of Object.keys(CONTENT)) if (t.indexOf(CONTENT[id].title) >= 0) return id;
    return null;
  }
  function resolveHandoffIdFromText(el) {
    const t = el.innerText || el.textContent || "";
    for (const id of Object.keys(HANDOFFS)) if (t.indexOf(HANDOFFS[id].title) >= 0) return id;
    // fallback keyword
    if (/生成 ?3 ?个实测选题/.test(t)) return "h1";
    if (/发布前检查.*AI 绘画教程/.test(t)) return "h2";
    if (/调整内容结构模板/.test(t)) return "h3";
    if (/验证分层的关注转化/.test(t)) return "h4";
    return null;
  }
  function resolveSurfaceCardId(el) {
    const t = el.innerText || el.textContent || "";
    if (t.indexOf("AI 绘画系列") >= 0) return { kind: "content", id: "c3" };
    if (t.indexOf("AI 工具实测") >= 0) return { kind: "content", id: "c1" };
    if (t.indexOf("AIGC 变现观察") >= 0) return { kind: "content", id: "c4" };
    return null;
  }

  function openObject(kind, id, anchor) {
    switch (kind) {
      case "employee":
        writeUX({ lastEmployeeId: id });
        setUtilityView("employee", id, anchor);
        break;
      case "research":
        writeUX({ lastObjectId: id, lastObjectKind: kind });
        setUtilityView("research", id, anchor);
        break;
      case "content":
        writeUX({ lastObjectId: id, lastObjectKind: kind });
        setUtilityView("content", id, anchor);
        break;
      case "handoff":
        setUtilityView("handoff", id, anchor);
        break;
      case "result":
      case "evidence":
        setUtilityView("handoff", id, anchor);
        break;
      default:
        setUtilityView("default", null, anchor);
    }
  }

  function bindObjectClicks() {
    const main = document.querySelector(".ms-pane-main");
    const ctx = document.querySelector(".ms-pane-ctx");
    const util = document.querySelector(".ms-pane-util");
    [main, ctx, util].forEach((root) => {
      if (!root) return;
      if (root.dataset.objectBound) return;
      root.dataset.objectBound = "1";
      root.addEventListener("click", (ev) => {
        const target = ev.target;
        if (!target) return;
        // Honor explicit data-util-action in Main/Context panes（问X / 直接对话 / 头像→速览）
        const ua = target.closest("[data-util-action]");
        if (ua) {
          ev.preventDefault();
          handleUtilityAction(ua.getAttribute("data-util-action"), ua.getAttribute("data-id") || "");
          return;
        }
        // Don't swallow utility pane buttons already handled in bindUtilityActions
        if (target.closest(".util-content [data-util-action], .util-content [data-util-back]")) return;
        // Don't swallow surface/context navigation hrefs (let real links go)
        if (target.closest(".ctx-nav-item, .crumbs a, .nav-item")) return;
        // Don't swallow prototype controls / nav toggle
        if (target.closest(".prototype-controls, .ms-nav-head, .ms-ctx-head, .ms-main-head, .ms-util-head")) return;
        const obj = resolveObjectFromClick(target);
        if (!obj) return;
        ev.preventDefault();
        openObject(obj.kind, obj.id, obj.el);
      });
    });
  }

  /* =========================================================
     RESTORE LAST CONTEXT ON PAGE LOAD
     ========================================================= */
  function restoreContextOnLoad() {
    const ux = readUX();
    // hash can overwrite: #emp=wy · #emp=wy,conv · #obj=research:r1
    let empToOpen = null, objToOpen = null;
    const hash = (location.hash || "").replace(/^#/, "");
    if (hash) {
      const parts = hash.split(/[,&;]/);
      parts.forEach((p) => {
        const [k, v] = p.split("=");
        if (k === "emp") empToOpen = v;
        if (k === "obj") {
          const [kk, vv] = (v || "").split(":");
          if (kk && vv) objToOpen = { kind: kk, id: vv };
        }
      });
    }
    if (!empToOpen) empToOpen = ux.lastEmployeeId || null;
    if (!objToOpen && ux.lastObjectKind && ux.lastObjectId) objToOpen = { kind: ux.lastObjectKind, id: ux.lastObjectId };

    // Priority: current hash / selection overrides UX context.
    // If current page matches the object context type, auto-open:
    const page = document.body.dataset.page || "";
    if (objToOpen) {
      const pageToKind = { research: "research", content: "content", calendar: "content", growth: "result", feedback: "feedback", commercial: "result" };
      if (pageToKind[page] && pageToKind[page] === objToOpen.kind) {
        // find anchor in dom
        const anchor = findObjectAnchor(objToOpen);
        setTimeout(() => openObject(objToOpen.kind, objToOpen.id, anchor), 60);
        return;
      }
    }
    if (empToOpen && EMPLOYEES[empToOpen]) {
      setTimeout(() => openObject("employee", empToOpen, findEmployeeAnchor(empToOpen)), 60);
    }
  }
  function findObjectAnchor(obj) {
    const sel = obj.kind === "research" ? ".insight-card" : obj.kind === "content" ? ".content-row" : null;
    if (!sel) return null;
    const title = (RESEARCH[obj.id] || CONTENT[obj.id] || {}).title;
    if (!title) return null;
    const arr = document.querySelectorAll(sel);
    for (let i = 0; i < arr.length; i++) {
      if ((arr[i].innerText || arr[i].textContent || "").indexOf(title) >= 0) return arr[i];
    }
    return null;
  }
  function findEmployeeAnchor(empId) {
    const name = (EMPLOYEES[empId] || {}).name;
    if (!name) return null;
    const arr = document.querySelectorAll(".presence-chip, .station-head, .avatar, .tt-name");
    for (let i = 0; i < arr.length; i++) {
      if ((arr[i].innerText || arr[i].textContent || "").indexOf(name) >= 0) return arr[i];
    }
    return null;
  }

  /* =========================================================
     STATIONS, TABS, CALENDAR, PROTOTYPE CONTROLS
     ========================================================= */
  function bindStations() {
    document.querySelectorAll(".station-head").forEach((head) => {
      if (head.dataset.bound) return;
      head.dataset.bound = "1";
      head.addEventListener("click", (e) => {
        const tag = ((e.target.tagName || "") + "").toLowerCase();
        if (["button", "a", "select", "input", "textarea"].indexOf(tag) >= 0) return;
        if (e.target.closest("button, a")) return;
        const station = head.closest(".station");
        if (!station) return;
        station.classList.toggle("collapsed");
      });
    });
  }
  function bindTabs() {
    document.querySelectorAll(".surface-tabs").forEach((wrap) => {
      wrap.querySelectorAll(".surface-tab").forEach((tab) => {
        tab.addEventListener("click", (e) => {
          if (tab.getAttribute("href") && tab.getAttribute("href") !== "#") return;
          e.preventDefault();
          wrap.querySelectorAll(".surface-tab").forEach((t) => t.classList.remove("active"));
          tab.classList.add("active");
        });
      });
    });
    document.querySelectorAll(".view-switch").forEach((wrap) => {
      wrap.querySelectorAll("a, button").forEach((el) => {
        el.addEventListener("click", (e) => {
          if (el.tagName.toLowerCase() === "a" && el.getAttribute("href") && el.getAttribute("href") !== "#") return;
          e.preventDefault();
          wrap.querySelectorAll("a, button").forEach((t) => t.classList.remove("active"));
          el.classList.add("active");
        });
      });
    });
  }
  function bindCalendar() {
    const shell = document.querySelector(".calendar-shell");
    if (!shell) return;
    let cursor = shell.dataset.month ? new Date(shell.dataset.month) : new Date();
    cursor.setDate(1);
    function formatMonth(d) { return d.toLocaleDateString("zh-CN", { year: "numeric", month: "long" }); }
    function render() {
      const title = shell.querySelector(".cal-title");
      if (title) title.textContent = formatMonth(cursor);
      const grid = shell.querySelector(".cal-days");
      if (!grid) return;
      const today = new Date();
      const selected = shell.dataset.selectedDate ? new Date(shell.dataset.selectedDate) : null;
      const firstDay = new Date(cursor);
      const firstWeekday = firstDay.getDay();
      const daysInMonth = new Date(cursor.getFullYear(), cursor.getMonth() + 1, 0).getDate();
      const cells = [];
      for (let i = 0; i < firstWeekday; i++) cells.push('<div class="day-cell empty"></div>');
      for (let d = 1; d <= daysInMonth; d++) {
        const date = new Date(cursor.getFullYear(), cursor.getMonth(), d);
        const ymd = date.toISOString().slice(0, 10);
        const classes = ["day-cell"];
        if (today.getFullYear() === date.getFullYear() && today.getMonth() === date.getMonth() && today.getDate() === date.getDate()) classes.push("today");
        if (selected && selected.getFullYear() === date.getFullYear() && selected.getMonth() === date.getMonth() && selected.getDate() === date.getDate()) classes.push("selected");
        cells.push(`<div class="${classes.join(" ")}" data-date="${ymd}"><div class="day-number">${d}</div><div class="day-notes"></div></div>`);
      }
      grid.innerHTML = cells.join("");
      try {
        const notes = shell.dataset.notes ? JSON.parse(shell.dataset.notes) : {};
        Object.keys(notes).forEach((ymd) => {
          const cell = grid.querySelector(`.day-cell[data-date="${ymd}"] .day-notes`);
          if (!cell) return;
          notes[ymd].forEach((n) => {
            const a = document.createElement("a");
            a.className = "cal-note";
            a.href = n.href || "#";
            a.dataset.object = "content";
            a.dataset.id = n.contentId || "";
            a.innerHTML = `<div class="cn-cover">${n.cover || "📝"}</div><div class="cn-title">${n.title || ""}</div><div class="cn-meta"><span class="tag ${n.tagClass || "tag-working"}">${n.tag || ""}</span></div>`;
            cell.appendChild(a);
          });
        });
      } catch (_) { /* ignore */ }
      grid.querySelectorAll(".day-cell:not(.empty)").forEach((cell) => {
        cell.addEventListener("click", () => {
          shell.dataset.selectedDate = cell.dataset.date;
          render();
        });
      });
    }
    shell.querySelectorAll(".cal-nav [data-cal-nav]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      btn.addEventListener("click", () => {
        const dir = btn.getAttribute("data-cal-nav");
        if (dir === "prev") cursor.setMonth(cursor.getMonth() - 1);
        else if (dir === "next") cursor.setMonth(cursor.getMonth() + 1);
        else if (dir === "today") cursor = new Date();
        render();
      });
    });
    render();
  }

  function bindPrototypeControls(currentPageKey) {
    const controls = document.querySelector(".prototype-controls");
    if (!controls) return;
    controls.querySelectorAll("button[data-page]").forEach((btn) => {
      if (btn.dataset.bound) return;
      btn.dataset.bound = "1";
      const key = btn.getAttribute("data-page");
      if (key === currentPageKey) btn.classList.add("active");
      btn.addEventListener("click", () => navigate(key));
    });
    const themeBtn = controls.querySelector('[data-dom-id="theme-toggle"]');
    if (themeBtn && !themeBtn.dataset.bound) {
      themeBtn.dataset.bound = "1";
      themeBtn.addEventListener("click", cycleTheme);
    }
  }

  function navigate(pageKey) {
    const target = PAGE_MAP[pageKey];
    if (!target) return;
    // carry hash with current context so next page restores object
    const ux = readUX();
    const parts = [];
    if (ux.lastEmployeeId) parts.push("emp=" + ux.lastEmployeeId);
    if (ux.lastObjectKind && ux.lastObjectId) parts.push("obj=" + ux.lastObjectKind + ":" + ux.lastObjectId);
    const hash = parts.length ? "#" + parts.join(",") : "";
    location.href = target + hash;
  }

  /* =========================================================
     BOOT
     ========================================================= */
  function boot(pageKey) {
    applyTheme(readTheme());
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      if (readTheme() === "system") applyTheme("system");
    });
    applyShellState();

    const navToggle = document.querySelector('[data-dom-id="nav-toggle"]');
    const navRestore = document.querySelector('[data-dom-id="nav-restore"]');
    if (navToggle && !navToggle.dataset.bound) { navToggle.dataset.bound = "1"; navToggle.addEventListener("click", toggleNav); }
    if (navRestore && !navRestore.dataset.bound) { navRestore.dataset.bound = "1"; navRestore.addEventListener("click", toggleNav); }
    document.querySelectorAll('[data-action="toggle-context"]').forEach((b) => { if (!b.dataset.bound) { b.dataset.bound = "1"; b.addEventListener("click", toggleContext); } });
    document.querySelectorAll('[data-action="toggle-utility"]').forEach((b) => { if (!b.dataset.bound) { b.dataset.bound = "1"; b.addEventListener("click", () => toggleUtility()); } });
    document.querySelectorAll('[data-action="toggle-assistant"], [data-dom-id="assistant-toggle"]').forEach((b) => { if (!b.dataset.bound) { b.dataset.bound = "1"; b.addEventListener("click", toggleAssistant); } });
    document.querySelectorAll('[data-action="close-assistant"]').forEach((b) => { if (!b.dataset.bound) { b.dataset.bound = "1"; b.addEventListener("click", closeAssistant); } });

    bindStations();
    bindTabs();
    bindCalendar();
    bindPrototypeControls(pageKey);
    bindObjectClicks();

    // Breadcrumb/context internal navigation: mark visited for UX (already real hrefs).
    bindBreadcrumbBack();
    restoreContextOnLoad();
  }

  function bindBreadcrumbBack() {
    // Let users hit a "返回" button inside utility (back stack) — simple pop via utilStack or hash
    // (not requested explicitly; placeholder for future SPA mode)
  }

  // Public API
  window.CurisApp = {
    boot, cycleTheme, toggleNav, toggleContext, toggleUtility, toggleAssistant,
    openObject, navigate,
    EMPLOYEES, RESEARCH, CONTENT, HANDOFFS, PAGE_MAP,
  };

  document.addEventListener("DOMContentLoaded", () => {
    const pageKey = (window.__CURIS_PAGE__) || document.body.dataset.page || null;
    boot(pageKey);
    // §12 FINAL SIMPLIFICATION：开发控制条默认隐藏；?dev 或 Ctrl/Cmd+Shift+D 打开
    const devOn = new URLSearchParams(location.search).has("dev");
    const pcs = document.querySelectorAll(".prototype-controls");
    if (devOn) pcs.forEach((el) => el.classList.add("dev-open"));
    document.addEventListener("keydown", (e) => {
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === "D" || e.key === "d")) {
        e.preventDefault();
        pcs.forEach((el) => el.classList.toggle("dev-open"));
      }
    });
  });
})();
