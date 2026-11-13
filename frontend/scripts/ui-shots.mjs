#!/usr/bin/env node
/*
 * Curis Frontend UI Shots — 断点视觉抽样
 * ---------------------------------------------------------------------------
 * 审计脚本只查「数值红线」，查不出「看起来对不对」。这个脚本补上人眼验收：
 * 在 Frozen 的三个关键断点各截一张，确认骨架没有塌、导航形态没有串档。
 *
 *   1440 → xl：220px 侧栏，一级导航「图标 + 文字」横排
 *   1100 → lg：76px 图标轨，一级导航「图标在上、文字隐藏」竖排
 *    900 → 移动：侧栏隐藏，走顶栏汉堡抽屉
 *
 * 用法：node scripts/ui-shots.mjs [--base-url=…] [--theme=dark|light] [--out=…]
 */

import { mkdirSync } from "node:fs";
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
const OUT_DIR = resolve(__dirname, args.out || "../.cache/ui-shots");

const BREAKPOINTS = [
  { name: "xl-1440", width: 1440, height: 900 },
  { name: "lg-1100", width: 1100, height: 860 },
  { name: "sm-900", width: 900, height: 860 },
];

const ROUTES = [
  ["/ceo-office", "ceo-office"],
  ["/ceo-office/capabilities", "capabilities"],
  ["/ceo-office/company-runtime", "company-runtime"],
];

async function main() {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: "new",
    args: ["--no-proxy-server", "--no-sandbox"],
  });
  mkdirSync(OUT_DIR, { recursive: true });

  for (const bp of BREAKPOINTS) {
    for (const [route, slug] of ROUTES) {
      // 移动断点只截首页，其余页面骨架一致，无需重复
      if (bp.name !== "xl-1440" && slug !== "ceo-office") continue;

      const page = await browser.newPage();
      await page.setViewport({ width: bp.width, height: bp.height });
      await page.evaluateOnNewDocument((theme) => {
        try { localStorage.setItem("curis-theme", theme); } catch { /* 忽略 */ }
        const apply = () => {
          if (document.documentElement) {
            document.documentElement.setAttribute("data-theme", theme);
          }
        };
        apply();
        document.addEventListener("DOMContentLoaded", apply);
      }, THEME);
      await page.goto(BASE + route, { waitUntil: "networkidle2", timeout: 30000 });
      await new Promise((r) => setTimeout(r, 700));

      const file = resolve(OUT_DIR, `${bp.name}-${slug}-${THEME}.png`);
      await page.screenshot({ path: file });
      console.log(`✓ ${file}`);
      await page.close();
    }
  }

  await browser.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
