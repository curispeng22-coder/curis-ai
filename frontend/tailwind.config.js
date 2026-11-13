/** @type {import('tailwindcss').Config} */

/* ── 间距刻度吸附表 ─────────────────────────────────────────────
   Frozen 间距只有 8 档：4 / 8 / 12 / 16 / 20 / 24 / 32 / 48 px。
   Tailwind 默认刻度里的「半档」（0.5=2px、1.5=6px、2.5=10px、3.5=14px）
   以及 7=28 / 9=36 / 11=44 全部不在档内，是审计 R3 的唯一来源。
   这里把它们就近吸附到 Frozen 档，从源头消灭 2/6/10/14px，
   存量类名（py-1.5 等）无需逐个改写即可自动合规。

   注意：只吸附 padding / margin / gap / space —— 也就是「间距语义」。
   theme.spacing 本体保持默认，w-3.5(14px 图标) / h-1.5(6px 圆点) /
   top-1.5 这类「尺寸与定位」不受影响，避免误伤图形细节。 */
const SPACE_SNAP = {
  "0.5": "4px", //  2 → 4
  "1.5": "8px", //  6 → 8
  "2.5": "12px", // 10 → 12
  "3.5": "16px", // 14 → 16
  "4.5": "16px", // 18 → 16
  7: "24px", // 28 → 24
  9: "32px", // 36 → 32
  10: "48px", // 40 → 48（整页级留白，就近取 Frozen 最大档）
  11: "48px", // 44 → 48
};

module.exports = {
  content: ["./app/**/*.{js,jsx}", "./components/**/*.{js,jsx}"],
  theme: {
    padding: ({ theme }) => ({ ...theme("spacing"), ...SPACE_SNAP }),
    margin: ({ theme }) => ({ auto: "auto", ...theme("spacing"), ...SPACE_SNAP }),
    gap: ({ theme }) => ({ ...theme("spacing"), ...SPACE_SNAP }),
    space: ({ theme }) => ({ ...theme("spacing"), ...SPACE_SNAP }),
    extend: {
      // Frozen --ui-* 映射（类名命名空间与 Frozen 令牌同名，值全部指向 Frozen 令牌）
      // 详见 docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md
      colors: {
        ui: {
          bg: "var(--ui-bg)",
          surface: "var(--ui-surface)",
          "surface-2": "var(--ui-surface-2)",
          "surface-3": "var(--ui-surface-2)",
          line: "var(--ui-line)",
          "line-2": "var(--ui-line)",
          txt: "var(--ui-text)",
          "txt-2": "var(--ui-text-2)",
          "txt-3": "var(--ui-text-3)",
          primary: "var(--ui-action-primary-bg)",
          "primary-dark": "var(--ui-action-primary-hover)",
          // B1 红线：Primary 按钮前景必须是 --ui-action-primary-fg。
          // dark 主题下 primary 背景是 #32f08c（亮绿），写 text-white 只有 1.75:1，
          // 直接违反 Frozen §6（≥4.5:1）。此别名让页面能正确表达该配对。
          "primary-fg": "var(--ui-action-primary-fg)",
          // 2026-10-05 双主题：文字型主行动（链接/文本按钮）用深紫 #5B469E（dark 为绿）。
          "primary-text": "var(--ui-action-primary-text)",
          "primary-light": "var(--ui-surface-2)",
          "primary-soft": "var(--ui-primary-soft)",
          accent: "var(--ui-accent)",
          "accent-light": "var(--ui-surface-2)",
          green: "var(--ui-success)",
          "green-soft": "var(--ui-surface-2)",
          cyan: "var(--ui-accent)",
          "cyan-soft": "var(--ui-surface-2)",
          amber: "var(--ui-warning)",
          "amber-soft": "var(--ui-surface-2)",
          red: "var(--ui-danger)",
          "red-soft": "var(--ui-surface-2)",
          violet: "var(--ui-accent)",
          "violet-soft": "var(--ui-surface-2)",
        },
        // 保留旧 curis 别名（不引入新私有调色板）
        curis: {
          ink: "#172126",
          panel: "#ffffff",
          teal: "#0f766e",
          line: "#dce4e7",
        },
      },
      fontFamily: {
        // D3：废弃 serif 展示字体，统一 Frozen 字体栈
        "ui-serif": ["var(--ui-font)"],
        "ui-sans": ["var(--ui-font)"],
      },
      boxShadow: {
        ui: "var(--ui-shadow)",
        "ui-2": "var(--ui-shadow-2)",
        "ui-3": "var(--ui-shadow-3)",
      },
    },
    // ── 刻度吸附（override，非 extend）─────────────────────────
    // Frozen 红线：字号仅 7 档、圆角仅 5 档。覆盖 Tailwind 默认刻度，
    // 使 text-lg / rounded-md 等旧类名自动落到最近的 Frozen 档位，
    // 从源头杜绝再次引入 18px / 6px 这类非档位值。
    fontSize: {
      // Frozen 7 档（12/13/14/16/20/24/28）—— 推荐直接用 text-ui-*
      "ui-1": ["var(--ui-fs-1)", { lineHeight: "1.5" }],
      "ui-2": ["var(--ui-fs-2)", { lineHeight: "1.5" }],
      "ui-3": ["var(--ui-fs-3)", { lineHeight: "1.5" }],
      "ui-4": ["var(--ui-fs-4)", { lineHeight: "1.25" }],
      "ui-5": ["var(--ui-fs-5)", { lineHeight: "1.25" }],
      "ui-6": ["var(--ui-fs-6)", { lineHeight: "1.1" }],
      "ui-7": ["var(--ui-fs-7)", { lineHeight: "1.1" }],
      // Tailwind 默认名 → 最近 Frozen 档（兼容存量类名）
      xs: ["var(--ui-fs-1)", { lineHeight: "1.5" }], // 12 → 12
      sm: ["var(--ui-fs-3)", { lineHeight: "1.5" }], // 14 → 14
      base: ["var(--ui-fs-4)", { lineHeight: "1.5" }], // 16 → 16
      lg: ["var(--ui-fs-5)", { lineHeight: "1.25" }], // 18 → 20
      xl: ["var(--ui-fs-5)", { lineHeight: "1.25" }], // 20 → 20
      "2xl": ["var(--ui-fs-6)", { lineHeight: "1.1" }], // 24 → 24
      "3xl": ["var(--ui-fs-7)", { lineHeight: "1.1" }], // 30 → 28
      "4xl": ["var(--ui-fs-7)", { lineHeight: "1.1" }], // 36 → 28
      "5xl": ["var(--ui-fs-7)", { lineHeight: "1.1" }],
      "6xl": ["var(--ui-fs-7)", { lineHeight: "1.1" }],
      // 语义字号别名（已收敛到 Frozen 档位）
      "ui-title": ["var(--ui-fs-6)", { lineHeight: "1.1", fontWeight: "700" }],
      "ui-card": ["var(--ui-fs-3)", { lineHeight: "1.3", fontWeight: "600" }],
      "ui-helper": ["var(--ui-fs-1)", { lineHeight: "1.5", fontWeight: "400" }],
    },
    borderRadius: {
      none: "0px",
      // Frozen 5 档（4 / 8 / 12 / 16 / 999）
      "ui-xs": "var(--ui-r-xs)",
      "ui-sm": "var(--ui-r-sm)",
      "ui-md": "var(--ui-r-md)",
      "ui-lg": "var(--ui-r-lg)",
      "ui-pill": "var(--ui-r-pill)",
      // Tailwind 默认名 → 最近 Frozen 档
      sm: "var(--ui-r-xs)", // 2 → 4
      DEFAULT: "var(--ui-r-xs)", // 4 → 4
      md: "var(--ui-r-sm)", // 6 → 8
      lg: "var(--ui-r-sm)", // 8 → 8
      xl: "var(--ui-r-md)", // 12 → 12
      "2xl": "var(--ui-r-lg)", // 16 → 16
      "3xl": "var(--ui-r-lg)", // 24 → 16
      full: "var(--ui-r-pill)",
    },
  },
  plugins: [],
};
