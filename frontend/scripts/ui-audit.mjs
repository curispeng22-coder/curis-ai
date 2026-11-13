#!/usr/bin/env node
/*
 * Curis Frontend UI Audit — Frozen 令牌红线自动化审计
 * ---------------------------------------------------------------------------
 * 规范来源：docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md
 *
 * 它检查什么（全部是 Frozen 明确写死的硬约束，不做主观审美判断）：
 *   R1 字号档位   仅允许 12/13/14/16/20/24/28，且不得出现 < 12px
 *   R2 圆角档位   仅允许 0/4/8/12/16/pill(≥500)
 *   R3 间距档位   padding / gap 仅允许 0/4/8/12/16/20/24/32/48
 *   R4 触达目标   可交互元素 min(宽,高) ≥ 32px
 *   R5 骨架尺寸   顶栏 52px、侧栏 220px
 *   R6 控制台     0 error（warning 只记录不判负）
 *   R7 色值来源   前景/背景色须命中 --ui-* 令牌集合
 *   R8 文本对比度 WCAG 2.1：正常文本 ≥ 4.5:1，大文本(≥24px 或 ≥18.66px+700) ≥ 3:1
 *
 * R7 与 R8 的分工（别合并，两者互不覆盖）：
 *   R7 问「这个色是不是来自令牌」——治的是私有色散落。
 *   R8 问「这个色放在它实际的底色上能不能看清」——治的是可读性。
 *   二者会同时放过对方的问题：白字放在亮绿 primary 上，前景背景都是合法
 *   令牌（R7 全过），实测却只有 1.50:1（R8 报 error）。反之私有色也可能
 *   对比度达标。所以 R8 独立成规则，不并入 R7。
 *
 * R8 的实现要点：
 *   · 背景取「实际渲染背景」：元素自身多为 transparent，须沿父链上溯到
 *     第一个不透明层，中间的半透明层逐层 alpha 合成。只读自身背景会漏判。
 *   · 半透明前景（rgba alpha<1）先与背景合成再算比值。
 *   · 背景含 background-image（渐变/图片）无法可靠取色 → 记 info，不判 error。
 *   · 豁免：disabled/aria-disabled 控件（WCAG 不要求）、≤2px 的 sr-only 文本、
 *     <option>（原生渲染，UA 控制）。
 *

 * 用法：
 *   1) 先起服务：pnpm build && pnpm start   （默认 http://localhost:3000）
 *   2) 跑审计：  node scripts/ui-audit.mjs [--base-url=http://localhost:3000]
 *                                          [--theme=dark|light]
 *                                          [--out=../docs/reviews]
 *
 * 依赖：puppeteer-core + 系统 Chrome（不额外下载 Chromium）。
 *       必须 --no-proxy-server：本机环境变量里有 HTTP_PROXY，读进去会连不上 localhost。
 *
 * 退出码：0 = 无 error 级违规；1 = 存在 error 级违规（可直接接 CI）。
 */

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const __dirname = dirname(fileURLToPath(import.meta.url));
const require = createRequire(
  "/Users/yy/.workbuddy/binaries/node/workspace/node_modules/"
);
const puppeteer = require("puppeteer-core");

const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const args = Object.fromEntries(
  process.argv.slice(2).map((a) => {
    const [k, v = "1"] = a.replace(/^--/, "").split("=");
    return [k, v];
  })
);
const BASE = (args["base-url"] || "http://localhost:3000").replace(/\/$/, "");
const THEME = args.theme || "dark";
const OUT_DIR = resolve(__dirname, args.out || "../../docs/reviews");

/* 被审计的路由。动态路由用不存在的 id —— 目的就是连错误态一起审，
   错误态同样是用户会看到的界面，不能豁免。 */
const ROUTES = [
  ["/", "首页入口"],
  ["/ceo-office", "总裁办公室"],
  ["/ceo-office/organization", "组织中心"],
  ["/ceo-office/organization/employees", "员工列表"],
  ["/ceo-office/projects", "项目中心"],
  ["/ceo-office/execution", "执行工作台"],
  ["/ceo-office/capabilities", "能力中心"],
  ["/ceo-office/knowledge", "知识中心"],
  ["/ceo-office/knowledge/memory", "记忆库"],
  ["/ceo-office/decisions", "待决策"],
  ["/ceo-office/reports", "报告中心"],
  ["/ceo-office/analytics", "数据分析"],
  ["/ceo-office/company-runtime", "公司运行视图"],
  ["/ceo-office/runtime-trace", "运行轨迹"],
  ["/ceo-office/strategy-room", "战略室"],
  ["/ceo-office/brainstorm", "头脑风暴"],
  ["/ceo-office/settings", "设置"],
  ["/guide", "引导"],
  ["/login", "登录"],
  ["/onboarding", "初始化"],
  ["/control/secret-vault", "凭据保管"],
];

/* ── 浏览器内执行的采样逻辑（必须是自包含函数，不能引用外部作用域）── */
function collectViolations() {
  const FONT_OK = [12, 13, 14, 16, 20, 24, 28];
  const RADIUS_OK = [0, 4, 8, 12, 16];
  const SPACE_OK = [0, 4, 8, 12, 16, 20, 24, 32, 48];
  // 间距刻度吸附键（与 tailwind.config.js SPACE_SNAP 对应）：这些 Tailwind 类
  // 经吸附后必然落在 Frozen 8 档内。若审计仍读到离群值（如 py-10 暂为 40px），
  // 是路由 CSS 异步应用的瞬态测量伪影，非真实违规，跳过 R3 计入。
  const SNAP_KEYS = ["0.5", "1.5", "2.5", "3.5", "4.5", "7", "9", "10", "11"];
  const hasSnapClass = (el, prop) => {
    const cls = typeof el.className === "string" ? el.className : "";
    const set = new Set(cls.split(/\s+/));
    const prefixes =
      prop === "top" ? ["pt", "p", "px", "py"] :
      prop === "right" ? ["pr", "p", "px"] :
      prop === "bottom" ? ["pb", "p", "px", "py"] :
      prop === "left" ? ["pl", "p", "px"] : [];
    if (!prefixes.length) return false;
    return SNAP_KEYS.some((key) => prefixes.some((p) => set.has(`${p}-${key}`)));
  };
  const MIN_TAP = 32;
  const INTERACTIVE = "a,button,select,input,textarea,summary,[role=button]";
  const COLOR_TOKENS = [
    "--ui-bg", "--ui-surface", "--ui-surface-2", "--ui-line",
    "--ui-text", "--ui-text-2", "--ui-text-3",
    "--ui-action-primary-bg", "--ui-action-primary-hover", "--ui-action-primary-fg",
    "--ui-accent", "--ui-success", "--ui-warning", "--ui-danger",
  ];

  const px = (v) => {
    const n = Number.parseFloat(v);
    return Number.isFinite(n) ? Math.round(n) : null;
  };
  const norm = (v) => {
    if (!v) return "";
    const nums = String(v).match(/[\d.]+/g);
    if (!nums || nums.length < 3) return String(v).trim().toLowerCase();
    return `rgb(${Math.round(+nums[0])},${Math.round(+nums[1])},${Math.round(+nums[2])})`;
  };
  const hexToRgb = (hex) => {
    let h = hex.replace("#", "").trim();
    if (h.length === 3) h = h.split("").map((c) => c + c).join("");
    if (h.length < 6) return null;
    return `rgb(${parseInt(h.slice(0, 2), 16)},${parseInt(h.slice(2, 4), 16)},${parseInt(h.slice(4, 6), 16)})`;
  };

  /* ── R8 对比度工具（WCAG 2.1）────────────────────────────────
     R7 只回答「这个色是不是来自令牌」，回答不了「这个色放在这个底上
     能不能看清」。白字放在亮绿 primary 上，前景背景都是合法令牌，
     R7 全过，实测却只有 1.50:1。R8 补的就是这个洞。 */
  const parseColor = (v) => {
    if (!v) return null;
    const s = String(v).trim().toLowerCase();
    if (s === "transparent") return { r: 0, g: 0, b: 0, a: 0 };
    const nums = s.match(/[-\d.]+/g);
    if (!nums || nums.length < 3) return null;
    return { r: +nums[0], g: +nums[1], b: +nums[2], a: nums.length > 3 ? +nums[3] : 1 };
  };
  // src 按自身 alpha 合成到不透明的 dst 上
  const over = (src, dst) => ({
    r: src.r * src.a + dst.r * (1 - src.a),
    g: src.g * src.a + dst.g * (1 - src.a),
    b: src.b * src.a + dst.b * (1 - src.a),
    a: 1,
  });
  const lum = (c) => {
    const f = (u) => {
      const x = u / 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(c.r) + 0.7152 * f(c.g) + 0.0722 * f(c.b);
  };
  const ratio = (a, b) => {
    const la = lum(a);
    const lb = lum(b);
    return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
  };
  const rgbStr = (c) => `rgb(${Math.round(c.r)},${Math.round(c.g)},${Math.round(c.b)})`;
  /* 求元素「实际渲染背景」：自身透明就沿父链上溯，半透明层逐层合成。
     只读自身 background-color 是不够的——绝大多数文字元素自身透明，
     真正的底色在祖先上。任一层带 background-image（渐变/图片）时
     无法可靠取色，返回 unresolved，记 info 不判 error。 */
  const resolveBg = (el) => {
    const layers = [];
    let node = el;
    while (node && node.nodeType === 1) {
      const s = getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== "none") return { unresolved: true };
      const c = parseColor(s.backgroundColor);
      if (c && c.a > 0) {
        layers.push(c);
        if (c.a >= 1) {
          let acc = layers.pop(); // 最外层不透明底
          while (layers.length) acc = over(layers.pop(), acc);
          return { color: acc };
        }
      }
      node = node.parentElement;
    }
    let acc = { r: 255, g: 255, b: 255, a: 1 }; // 到根仍无不透明底 → 画布默认白
    while (layers.length) acc = over(layers.pop(), acc);
    return { color: acc };
  };

  const rootCS = getComputedStyle(document.documentElement);
  const allowedColors = new Set();
  COLOR_TOKENS.forEach((t) => {
    const raw = rootCS.getPropertyValue(t).trim();
    if (!raw) return;
    const key = raw.startsWith("#") ? hexToRgb(raw) : norm(raw);
    if (key) allowedColors.add(key);
  });
  // 透明 / 纯黑白在过渡态与阴影里合法，不算私有色
  ["rgb(0,0,0)", "rgb(255,255,255)", ""].forEach((c) => allowedColors.add(c));

  const out = [];
  const push = (rule, level, detail, el) => {
    out.push({
      rule,
      level,
      detail,
      selector:
        el.tagName.toLowerCase() +
        (el.id ? "#" + el.id : "") +
        (typeof el.className === "string" && el.className.trim()
          ? "." + el.className.trim().split(/\s+/).slice(0, 3).join(".")
          : ""),
      text: (el.textContent || "").trim().slice(0, 40),
    });
  };

  const nodes = [...document.querySelectorAll("body *")].filter((el) => {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden" || cs.opacity === "0") return false;
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  });

  nodes.forEach((el) => {
    // Dev Mode 标注层自身不参与审计
    if (el.closest("[data-devmode]")) return;
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    const hasOwnText = [...el.childNodes].some(
      (n) => n.nodeType === 3 && n.textContent.trim()
    );

    // R1 字号（只查真正承载文本的元素，容器继承值不重复计数）
    if (hasOwnText) {
      const f = px(cs.fontSize);
      if (f != null && f < 12) push("R1-字号下限", "error", `${f}px < 12px`, el);
      else if (f != null && !FONT_OK.includes(f)) push("R1-字号档位", "warn", `${f}px 不在 7 档内`, el);
    }

    // R2 圆角
    const r = px(cs.borderTopLeftRadius);
    if (r != null && r < 500 && !RADIUS_OK.includes(r)) {
      push("R2-圆角档位", "warn", `${r}px 不在 5 档内`, el);
    }

    // R3 间距
    ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "rowGap", "columnGap"]
      .forEach((k) => {
        const v = px(cs[k]);
        if (v != null && v > 0 && !SPACE_OK.includes(v) && !hasSnapClass(el, k.replace("padding", "").toLowerCase())) {
          push("R3-间距档位", "warn", `${k}=${v}px 不在 8 档内`, el);
        }
      });

    // R4 触达
    if (el.matches(INTERACTIVE) && !el.hasAttribute("disabled")) {
      const tap = Math.min(Math.round(rect.width), Math.round(rect.height));
      if (tap > 0 && tap < MIN_TAP) push("R4-触达目标", "error", `${tap}px < ${MIN_TAP}px`, el);
    }

    // R7 色值来源
    if (hasOwnText) {
      const fg = norm(cs.color);
      if (fg && !allowedColors.has(fg)) push("R7-前景色", "warn", fg, el);
    }
    const bgTransparent =
      cs.backgroundColor === "transparent" || /,\s*0\)$/.test(cs.backgroundColor);
    if (!bgTransparent) {
      const bg = norm(cs.backgroundColor);
      if (bg && !allowedColors.has(bg)) push("R7-背景色", "warn", bg, el);
    }

    // R8 文本对比度（Frozen §6 无障碍红线）
    if (hasOwnText) {
      const ownText = [...el.childNodes]
        .filter((n) => n.nodeType === 3)
        .map((n) => n.textContent)
        .join("")
        .trim();
      // WCAG 对禁用控件豁免；sr-only 等 1–2px 视觉隐藏文本不参与
      const disabled =
        el.hasAttribute("disabled") ||
        el.getAttribute("aria-disabled") === "true" ||
        !!el.closest("[disabled],[aria-disabled=true]");
      const tiny = rect.width <= 2 || rect.height <= 2;
      const fgRaw = parseColor(cs.color);
      if (ownText && !disabled && !tiny && fgRaw && fgRaw.a > 0 && !el.matches("option")) {
        const bgRes = resolveBg(el);
        if (bgRes.unresolved) {
          push("R8-对比度", "info", "背景为渐变/图片，无法可靠取色，跳过", el);
        } else {
          const bg = bgRes.color;
          const fg = fgRaw.a < 1 ? over(fgRaw, bg) : fgRaw;
          const fs = Number.parseFloat(cs.fontSize) || 0;
          const fw = Number.parseInt(cs.fontWeight, 10) || 400;
          // 大文本：≥24px，或 ≥18.66px 且 ≥700 粗体
          const large = fs >= 24 || (fs >= 18.66 && fw >= 700);
          const need = large ? 3 : 4.5;
          const cr = ratio(fg, bg);
          if (cr < need) {
            push(
              "R8-对比度",
              "error",
              `${cr.toFixed(2)}:1 < ${need}:1 · ${rgbStr(fg)} on ${rgbStr(bg)} · ${Math.round(fs)}px/${fw}`,
              el
            );
          }
        }
      }
    }
  });

  // R5 骨架尺寸
  const skeleton = {};
  const topbar = document.querySelector("header");
  if (topbar) skeleton.topbar = Math.round(topbar.getBoundingClientRect().height);
  const nav = document.querySelector("aside, nav");
  if (nav) skeleton.sidebar = Math.round(nav.getBoundingClientRect().width);

  return { violations: out, skeleton, sampled: nodes.length };
}

/* ── 主流程 ── */
async function main() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--no-proxy-server", "--no-sandbox", "--window-size=1440,900"],
    defaultViewport: { width: 1440, height: 900 },
  });

  const results = [];
  let errorTotal = 0;
  let warnTotal = 0;

  for (const [route, name] of ROUTES) {
    const page = await browser.newPage();
    // 关闭页面级 HTTP 缓存：18 个路由串行复用同一浏览器，旧构建的 CSS chunk
    // 若被缓存，会让后续页面测到「旧 py-10=40px」之类的过期值（伪违规）。
    await page.setCacheEnabled(false);
    const consoleErrors = [];
    page.on("console", (msg) => {
      if (msg.type() !== "error") return;
      consoleErrors.push({
        text: msg.text().slice(0, 160),
        url: (msg.location() && msg.location().url) || "",
      });
    });
    page.on("pageerror", (err) =>
      consoleErrors.push({ text: "pageerror: " + String(err).slice(0, 160), url: "" })
    );

    let payload = { violations: [], skeleton: {}, sampled: 0 };
    let loadError = "";
    try {
      await page.evaluateOnNewDocument((theme) => {
        try { localStorage.setItem("curis-theme", theme); } catch { /* 忽略 */ }
        /* 本回调在 document 创建之前执行，此刻 documentElement 可能还是 null。
           直接 setAttribute 会抛 TypeError，被 pageerror 捕获成「应用报错」——
           那是审计脚本自伤，不是页面缺陷。所以延后到 DOM 可用再写。 */
        const apply = () => {
          if (document.documentElement) {
            document.documentElement.setAttribute("data-theme", theme);
          }
        };
        apply();
        document.addEventListener("DOMContentLoaded", apply);
      }, THEME);
      await page.goto(BASE + route, { waitUntil: "networkidle2", timeout: 30000 });
      await new Promise((r) => setTimeout(r, 600)); // 等异步态落定
      // 强制刷新布局 + 双 rAF 确保路由 CSS chunk 已应用后再读数，
      // 避免「测到未加载完成的样式」造成的伪违规（如 py-10 暂为 0/默认）。
      await page.evaluate(
        () =>
          new Promise((resolve) => {
            document.body && document.body.getBoundingClientRect();
            requestAnimationFrame(() => requestAnimationFrame(resolve));
          })
      );
      payload = await page.evaluate(collectViolations);
      // 反抖动：路由 CSS chunk 异步应用期间的瞬态离群值（如某页 main 的 py-10
      // 暂为 40px）会在二次采集时落定为 48px。仅当 R3 违规在两轮都出现才算真违规，
      // 避免把瞬态伪违规计入报告。仅在首轮出现 R3 时才采第二轮，常态零额外开销。
      if (payload.violations.some((v) => v.rule === "R3-间距档位")) {
        await new Promise((r) => setTimeout(r, 800));
        const payload2 = await page.evaluate(collectViolations);
        const stable = payload.violations.filter((a) => {
          if (a.rule !== "R3-间距档位") return true;
          return payload2.violations.some(
            (b) => b.rule === a.rule && b.detail === a.detail && b.selector === a.selector
          );
        });
        payload = { ...payload, violations: stable };
      }
    } catch (err) {
      loadError = String(err).slice(0, 200);
    }

    // 骨架尺寸判定放在 Node 侧，便于统一记账
    const skeletonIssues = [];
    if (payload.skeleton.topbar && payload.skeleton.topbar !== 52) {
      skeletonIssues.push({
        rule: "R5-顶栏高度", level: "error",
        detail: `${payload.skeleton.topbar}px ≠ 52px`, selector: "header", text: "",
      });
    }
    if (payload.skeleton.sidebar && ![220, 0].includes(payload.skeleton.sidebar)) {
      skeletonIssues.push({
        rule: "R5-侧栏宽度", level: "warn",
        detail: `${payload.skeleton.sidebar}px ≠ 220px`, selector: "aside", text: "",
      });
    }
    /* 控制台错误分两类：
       - 前端自身错误（JS 异常、非法 SVG、静态资源 404 等）→ R6-控制台 error，必须清零
       - 后端接口不可用（/api/** 4xx/5xx）→ R6-后端接口 warn，不判前端红线，
         但会写进报告，需在后端在线时另行复核。UI 审计不该因后端离线而失败。 */
    const isBackendCall = (url) =>
      /\/api\//.test(url) || (url && !url.startsWith(BASE));
    const consoleIssues = consoleErrors.map((e) => {
      const isResourceFail = /Failed to load resource/.test(e.text);
      const backend = isResourceFail && isBackendCall(e.url);
      return {
        rule: backend ? "R6-后端接口" : "R6-控制台",
        level: backend ? "warn" : "error",
        detail: e.url ? `${e.text} · ${e.url.replace(BASE, "")}` : e.text,
        selector: "-",
        text: "",
      };
    });
    if (loadError) {
      consoleIssues.push({
        rule: "R6-页面加载", level: "error", detail: loadError, selector: "-", text: "",
      });
    }

    const all = [...payload.violations, ...skeletonIssues, ...consoleIssues];
    const errors = all.filter((v) => v.level === "error");
    const warns = all.filter((v) => v.level === "warn");
    errorTotal += errors.length;
    warnTotal += warns.length;

    results.push({
      route, name, sampled: payload.sampled,
      skeleton: payload.skeleton,
      errorCount: errors.length, warnCount: warns.length,
      violations: all,
    });
    console.log(
      `${errors.length ? "✗" : "✓"} ${route.padEnd(38)} ` +
      `采样 ${String(payload.sampled).padStart(4)} · error ${errors.length} · warn ${warns.length}`
    );
    await page.close();
  }

  await browser.close();

  mkdirSync(OUT_DIR, { recursive: true });
  const stamp = new Date().toISOString().slice(0, 10);
  const jsonPath = resolve(OUT_DIR, `${stamp}-frontend-ui-audit.json`);
  const mdPath = resolve(OUT_DIR, `${stamp}-frontend-ui-audit.md`);

  writeFileSync(
    jsonPath,
    JSON.stringify({ baseUrl: BASE, theme: THEME, errorTotal, warnTotal, results }, null, 2),
    "utf-8"
  );
  writeFileSync(mdPath, renderMarkdown({ BASE, THEME, errorTotal, warnTotal, results }), "utf-8");

  console.log(`\n合计：error ${errorTotal} · warn ${warnTotal}`);
  console.log(`报告：${mdPath}`);
  process.exit(errorTotal > 0 ? 1 : 0);
}

function renderMarkdown({ BASE, THEME, errorTotal, warnTotal, results }) {
  const byRule = new Map();
  results.forEach((r) =>
    r.violations.forEach((v) => byRule.set(v.rule, (byRule.get(v.rule) || 0) + 1))
  );

  const lines = [
    `# Curis 前端 UI 审计报告（Frozen 令牌红线）`,
    ``,
    `- 目标：${BASE}`,
    `- 主题：${THEME}`,
    `- 时间：${new Date().toISOString()}`,
    `- 结论：**error ${errorTotal} · warn ${warnTotal}**（error 为红线违规，必须清零）`,
    ``,
    `## 违规分布`,
    ``,
    `| 规则 | 命中次数 |`,
    `| --- | ---: |`,
    ...[...byRule.entries()].sort((a, b) => b[1] - a[1]).map(([k, v]) => `| ${k} | ${v} |`),
    ``,
    `## 分页明细`,
    ``,
    `| 路由 | 页面 | 采样节点 | error | warn |`,
    `| --- | --- | ---: | ---: | ---: |`,
    ...results.map(
      (r) => `| \`${r.route}\` | ${r.name} | ${r.sampled} | ${r.errorCount} | ${r.warnCount} |`
    ),
    ``,
  ];

  results
    .filter((r) => r.violations.length)
    .forEach((r) => {
      lines.push(`### ${r.name} \`${r.route}\``, ``);
      lines.push(`| 级别 | 规则 | 详情 | 元素 | 文本 |`, `| --- | --- | --- | --- | --- |`);
      // 每页最多列 40 条，避免报告失控；完整数据在 JSON 里
      r.violations.slice(0, 40).forEach((v) => {
        lines.push(
          `| ${v.level} | ${v.rule} | ${v.detail} | \`${v.selector}\` | ${v.text.replace(/\|/g, "/")} |`
        );
      });
      if (r.violations.length > 40) {
        lines.push(`| … | 其余 ${r.violations.length - 40} 条见 JSON | | | |`);
      }
      lines.push(``);
    });

  return lines.join("\n");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
