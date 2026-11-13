"use client";

/*
 * DevMode — Frozen 令牌合规的实时标注层（前端等价物）
 * ---------------------------------------------------------------------------
 * 规范来源：Curis UI Frozen Spec §6「Dev Mode 与验收」
 *   原型版（curis-ui-prototype/_system/devmode.js）靠手写 data-spec 标注组件规格；
 *   真实前端组件量大、data-spec 维护成本高，改为**从 computed style 反查令牌**：
 *   不需要任何页面侧埋点，任意元素悬停即出结论，且能直接判红线违规。
 *
 * 开关（三选一，零成本：未开启时组件返回 null，不注册任何监听）：
 *   · URL 加 ?dev=1
 *   · 页面内按 Shift + D 开 / Esc 关
 *   · localStorage['curis-devmode'] = '1'（跨刷新保持）
 *
 * 悬停面板给出四类信息：
 *   尺寸    宽 × 高，触达目标 < 32px 标红（Frozen 红线）
 *   排版    字号 / 行高，命中字阶档位显令牌名，未命中或 < 12px 标红
 *   形状    圆角 / 内边距，未命中 5 档圆角或 8 档间距标黄（可疑，非硬红线）
 *   颜色    前景 / 背景，命中令牌显名称，未命中显字面值并标黄
 *
 * 实现约束：
 *   · 只读，不改动任何被测元素的样式（覆盖框是独立的 fixed 层）
 *   · z-index 取 --ui-z-devmode(9000)，永远压在业务 UI 之上
 *   · pointer-events:none，不劫持任何点击
 */

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

const STORAGE_KEY = "curis-devmode";

/* Frozen 档位（与 globals.css 的 --ui-* 一一对应，改一处必须同步改另一处） */
const FONT_SCALE = { 12: "--ui-fs-1", 13: "--ui-fs-2", 14: "--ui-fs-3", 16: "--ui-fs-4", 20: "--ui-fs-5", 24: "--ui-fs-6", 28: "--ui-fs-7" };
const SPACE_SCALE = { 0: "0", 4: "--ui-sp-1", 8: "--ui-sp-2", 12: "--ui-sp-3", 16: "--ui-sp-4", 20: "--ui-sp-5", 24: "--ui-sp-6", 32: "--ui-sp-7", 48: "--ui-sp-8" };
const RADIUS_SCALE = { 0: "0", 4: "--ui-r-xs", 8: "--ui-r-sm", 12: "--ui-r-md", 16: "--ui-r-lg", 999: "--ui-r-pill" };

const COLOR_TOKENS = [
  "--ui-bg", "--ui-surface", "--ui-surface-2", "--ui-line",
  "--ui-text", "--ui-text-2", "--ui-text-3",
  "--ui-action-primary-bg", "--ui-action-primary-hover", "--ui-action-primary-fg",
  "--ui-accent", "--ui-success", "--ui-warning", "--ui-danger",
];

const MIN_FONT = 12;   // 红线：正文字号下限
const MIN_TAP = 32;    // 红线：交互元素触达下限
const INTERACTIVE = "a,button,select,input,textarea,summary,[role=button],[tabindex]";

const OK = "ok";
const WARN = "warn";
const BAD = "bad";

function toPx(value) {
  const n = Number.parseFloat(value);
  return Number.isFinite(n) ? Math.round(n) : null;
}

function normalizeColor(value) {
  if (!value) return "";
  const nums = value.match(/[\d.]+/g);
  if (!nums || nums.length < 3) return value.trim().toLowerCase();
  const [r, g, b] = nums;
  return `rgb(${Math.round(+r)},${Math.round(+g)},${Math.round(+b)})`;
}

function hexToRgb(hex) {
  let h = hex.replace("#", "").trim();
  if (h.length === 3) h = h.split("").map((c) => c + c).join("");
  if (h.length < 6) return null;
  return `rgb(${parseInt(h.slice(0, 2), 16)},${parseInt(h.slice(2, 4), 16)},${parseInt(h.slice(4, 6), 16)})`;
}

/** 建立「计算色值 → 令牌名」反查表（主题切换后需重建，故每次开启时重算） */
function buildColorIndex() {
  const cs = getComputedStyle(document.documentElement);
  const index = new Map();
  COLOR_TOKENS.forEach((token) => {
    const raw = cs.getPropertyValue(token).trim();
    if (!raw) return;
    const key = raw.startsWith("#") ? hexToRgb(raw) : normalizeColor(raw);
    if (key && !index.has(key)) index.set(key, token);
  });
  return index;
}

export default function DevMode() {
  const [enabled, setEnabled] = useState(false);
  const [info, setInfo] = useState(null);
  const colorIndex = useRef(null);

  /* 开关：URL / localStorage 初始化 + Shift+D 快捷键 */
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    let on = params.get("dev") === "1";
    if (!on) {
      try { on = window.localStorage.getItem(STORAGE_KEY) === "1"; } catch { /* 隐私模式：忽略 */ }
    }
    setEnabled(on);

    const onKey = (event) => {
      if (event.shiftKey && (event.key === "D" || event.key === "d")) {
        setEnabled((prev) => {
          const next = !prev;
          try { window.localStorage.setItem(STORAGE_KEY, next ? "1" : "0"); } catch { /* 忽略 */ }
          return next;
        });
      } else if (event.key === "Escape") {
        setEnabled((prev) => {
          if (!prev) return prev;
          try { window.localStorage.setItem(STORAGE_KEY, "0"); } catch { /* 忽略 */ }
          return false;
        });
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const inspect = useCallback((el) => {
    if (!el || !(el instanceof Element)) return null;
    if (!colorIndex.current) colorIndex.current = buildColorIndex();
    const idx = colorIndex.current;
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();

    const fontPx = toPx(cs.fontSize);
    const fontToken = FONT_SCALE[fontPx];
    const fontLevel = fontPx == null ? WARN : fontPx < MIN_FONT ? BAD : fontToken ? OK : WARN;

    const radiusPx = toPx(cs.borderTopLeftRadius);
    const radiusToken = radiusPx != null && radiusPx >= 500 ? RADIUS_SCALE[999] : RADIUS_SCALE[radiusPx];
    const radiusLevel = radiusPx === 0 || radiusToken ? OK : WARN;

    const pads = ["paddingTop", "paddingRight", "paddingBottom", "paddingLeft"].map((k) => toPx(cs[k]) ?? 0);
    const padOff = pads.filter((v) => !(v in SPACE_SCALE));
    const padLevel = padOff.length ? WARN : OK;

    const isInteractive = el.matches(INTERACTIVE);
    const tapPx = Math.min(Math.round(rect.width), Math.round(rect.height));
    const tapLevel = !isInteractive ? OK : tapPx >= MIN_TAP ? OK : BAD;

    const fg = normalizeColor(cs.color);
    const bgRaw = normalizeColor(cs.backgroundColor);
    const transparent = /rgba?\([^)]*,\s*0\)$/.test(cs.backgroundColor) || cs.backgroundColor === "transparent";

    return {
      tag: el.tagName.toLowerCase() + (el.className && typeof el.className === "string"
        ? "." + el.className.trim().split(/\s+/).slice(0, 2).join(".")
        : ""),
      rect,
      size: `${Math.round(rect.width)} × ${Math.round(rect.height)}`,
      font: { text: `${fontPx}px / ${cs.lineHeight}`, token: fontToken, level: fontLevel },
      radius: { text: radiusPx != null ? `${radiusPx}px` : "—", token: radiusToken, level: radiusLevel },
      padding: { text: pads.join(" / "), token: padOff.length ? null : "全部命中间距档", level: padLevel },
      tap: { text: isInteractive ? `${tapPx}px` : "非交互元素", level: tapLevel },
      fg: { text: fg, token: idx.get(fg), level: idx.get(fg) ? OK : WARN },
      bg: {
        text: transparent ? "transparent" : bgRaw,
        token: transparent ? "继承父级" : idx.get(bgRaw),
        level: transparent || idx.get(bgRaw) ? OK : WARN,
      },
    };
  }, []);

  /* 悬停采样：mouseover 冒泡一次绑定，无需逐元素监听 */
  useEffect(() => {
    if (!enabled) {
      setInfo(null);
      colorIndex.current = null;
      return undefined;
    }
    colorIndex.current = buildColorIndex();
    const onOver = (event) => setInfo(inspect(event.target));
    const onLeave = () => setInfo(null);
    document.addEventListener("mouseover", onOver, true);
    document.addEventListener("mouseleave", onLeave);
    return () => {
      document.removeEventListener("mouseover", onOver, true);
      document.removeEventListener("mouseleave", onLeave);
    };
  }, [enabled, inspect]);

  const panelPos = useMemo(() => {
    if (!info) return null;
    const { rect } = info;
    const below = rect.bottom + 8;
    const top = below + 220 > window.innerHeight ? Math.max(8, rect.top - 228) : below;
    const left = Math.min(Math.max(8, rect.left), window.innerWidth - 300);
    return { top, left };
  }, [info]);

  if (!enabled) return null;

  return (
    <div
      data-devmode=""
      aria-hidden="true"
      style={{
        position: "fixed",
        inset: 0,
        zIndex: "var(--ui-z-devmode)",
        pointerEvents: "none",
        fontFamily: "var(--ui-mono)",
      }}
    >
      {/* 常驻角标：提示当前处于标注模式，避免误以为是产品 UI */}
      <div style={{
        position: "absolute", right: 12, bottom: 12,
        background: "var(--ui-accent)", color: "var(--ui-action-primary-fg)",
        fontSize: "var(--ui-fs-1)", lineHeight: 1, fontWeight: 700,
        padding: "var(--ui-sp-2) var(--ui-sp-3)", borderRadius: "var(--ui-r-pill)",
      }}>
        DEV MODE · Shift+D 切换
      </div>

      {info && (
        <>
          {/* 元素轮廓 */}
          <div style={{
            position: "absolute",
            top: info.rect.top, left: info.rect.left,
            width: info.rect.width, height: info.rect.height,
            outline: "1px solid var(--ui-accent)",
            background: "rgba(50,240,140,0.07)",
          }} />
          {/* 信息面板 */}
          <div style={{
            position: "absolute", top: panelPos.top, left: panelPos.left, width: 288,
            background: "var(--ui-surface)", border: "1px solid var(--ui-line)",
            borderRadius: "var(--ui-r-md)", boxShadow: "var(--ui-shadow-3)",
            padding: "var(--ui-sp-3)", color: "var(--ui-text)",
            fontSize: "var(--ui-fs-1)", lineHeight: 1.6,
          }}>
            <div style={{
              color: "var(--ui-accent)", fontWeight: 700, marginBottom: "var(--ui-sp-2)",
              overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
            }}>
              {info.tag}
            </div>
            <Row label="尺寸" value={info.size} />
            <Row label="触达" value={info.tap.text} level={info.tap.level} />
            <Row label="字号" value={info.font.text} token={info.font.token} level={info.font.level} />
            <Row label="圆角" value={info.radius.text} token={info.radius.token} level={info.radius.level} />
            <Row label="内距" value={info.padding.text} token={info.padding.token} level={info.padding.level} />
            <Row label="前景" value={info.fg.text} token={info.fg.token} level={info.fg.level} />
            <Row label="背景" value={info.bg.text} token={info.bg.token} level={info.bg.level} />
          </div>
        </>
      )}
    </div>
  );
}

function Row({ label, value, token, level = OK }) {
  const color = level === BAD ? "var(--ui-danger)" : level === WARN ? "var(--ui-warning)" : "var(--ui-text-2)";
  return (
    <div style={{ display: "flex", gap: "var(--ui-sp-2)", alignItems: "baseline" }}>
      <span style={{ width: 32, flexShrink: 0, color: "var(--ui-text-3)" }}>{label}</span>
      <span style={{ color, wordBreak: "break-all" }}>
        {value}
        {token && <span style={{ color: "var(--ui-success)" }}>{"  " + token}</span>}
      </span>
    </div>
  );
}
