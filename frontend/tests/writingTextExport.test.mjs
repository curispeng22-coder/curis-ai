import test from "node:test";
import assert from "node:assert/strict";
import { formalMarkdownFilename, formalSnapshotText, formalVersionNumber } from "../lib/writingTextExport.mjs";

const FIRST = "第一稿开头。\n\n凌晨的雾笼罩灯塔😀，号角未响。\n  尾部空格保留  ";
const SECOND = "第二稿开头。\n\n正文延续前稿，作者确认后的快照。\n引号“—”与😀符号逐字保留。";

test("formal snapshot text is returned verbatim, never trimmed or reformatted", () => {
  assert.equal(formalSnapshotText({ snapshot: { text: FIRST } }), FIRST);
  assert.equal(formalSnapshotText({ snapshot: { text: "" } }), "");
  assert.throws(() => formalSnapshotText({}), /缺少正文快照/);
  assert.throws(() => formalSnapshotText({ snapshot: { text: 123 } }), /缺少正文快照/);
  assert.throws(() => formalSnapshotText(null), /缺少正文快照/);
});

test("formal version number counts only formal.confirmed events and rejects foreign refs", () => {
  const events = [
    { action: "draft.saved", ref: "d1" },
    { action: "formal.confirmed", ref: "F1" },
    { action: "candidate.recorded", ref: "C1" },
    { action: "package.prepared", ref: "P1", formal_ref: "F1" },
    { action: "formal.confirmed", ref: "F2" },
  ];
  assert.equal(formalVersionNumber(events, "F1"), 1);
  assert.equal(formalVersionNumber(events, "F2"), 2);
  assert.throws(() => formalVersionNumber(events, "C1"), /不在当前章节版本记录/);
  assert.throws(() => formalVersionNumber(events, "missing"), /不在当前章节版本记录/);
  assert.throws(() => formalVersionNumber(events, ""), /请先选择/);
  assert.throws(() => formalVersionNumber(null, "F1"), /不在当前章节版本记录/);
});

test("markdown filename keeps title and version, sanitizes illegal characters, preserves Chinese", () => {
  assert.equal(formalMarkdownFilename("雾色灯塔·第一章", 2), "雾色灯塔·第一章-正式稿2.md");
  assert.equal(formalMarkdownFilename("a/b\\c:d*e?f\"g<h>i|j", 1), "a b c d e f g h i j-正式稿1.md");
  assert.equal(formalMarkdownFilename("序章：转折", 3), "序章：转折-正式稿3.md");
  assert.equal(formalMarkdownFilename("  \n第一章\t\t二号 ", 5), "第一章 二号-正式稿5.md");
  assert.equal(formalMarkdownFilename("", 1), "未命名章节-正式稿1.md");
  assert.equal(formalMarkdownFilename(undefined, 1), "未命名章节-正式稿1.md");
  assert.equal(formalMarkdownFilename("尾声", 12), "尾声-正式稿12.md");
  assert.ok(formalMarkdownFilename("雾色灯塔", 2).endsWith(".md"));
});

test("long CJK titles are capped by code points without splitting surrogate pairs", () => {
  const mixed = "字".repeat(59) + "😀" + "雾".repeat(20);
  assert.equal(formalMarkdownFilename(mixed, 1), "字".repeat(59) + "😀-正式稿1.md");
  assert.equal(formalMarkdownFilename("章".repeat(80), 1), "章".repeat(60) + "-正式稿1.md");
});

test("exported markdown blob is UTF-8 typed and round-trips Chinese and emoji byte-exactly", async () => {
  const blob = new Blob([formalSnapshotText({ snapshot: { text: SECOND } })], { type: "text/markdown;charset=utf-8" });
  assert.equal(blob.type, "text/markdown;charset=utf-8");
  assert.equal(await blob.text(), SECOND);
  assert.equal(new TextDecoder("utf-8").decode(await blob.arrayBuffer()), SECOND);
});

async function writingComponent(path, props, api = {}) {
  const { readFileSync } = await import("node:fs"); const { createRequire } = await import("node:module"); const vm = await import("node:vm");
  const require = createRequire(import.meta.url), React = require("react"), swc = require("next/dist/build/swc"); await swc.loadBindings();
  const states = [], refs = [], effects = []; let si = 0, ri = 0, ei = 0; const storage = api.__storage || new Map(), routes = [], writes = [];
  const hooks = { ...React, useState: initial => { const n = si++; if (!(n in states)) states[n] = initial; return [states[n], value => { states[n] = typeof value === "function" ? value(states[n]) : value; }]; }, useRef: initial => refs[ri++] ||= { current: initial }, useCallback: fn => fn, useMemo: fn => fn(), useEffect: (fn, deps) => { const n = ei++, old = effects[n]; if (!old || !deps || deps.some((v, i) => !Object.is(v, old.deps[i]))) effects[n] = { fn, deps, pending: true, cleanup: old?.cleanup }; } };
  hooks.useLayoutEffect = hooks.useEffect;
  const originalApi = await import("../lib/writingApi.js"), originalState = await import("../lib/writingState.mjs"), originalBookState = await import("../lib/writingBookState.mjs"), textExport = await import("../lib/writingTextExport.mjs");
  const fx = api.__fx || { copied: [], blobs: [], urls: [], clicks: [], revoked: [], timers: [] };
  let urlCount = 0;
  const modules = new Map();
  const sandbox = { URLSearchParams, crypto: globalThis.crypto, localStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value) }, sessionStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value) },
    document: { querySelector: () => null, createElement: tag => ({ tag, href: "", download: "", click() { fx.clicks.push({ tag, href: this.href, download: this.download }); } }) },
    Blob, URL: { createObjectURL: blob => { fx.blobs.push(blob); const url = `blob:writing-fixture-${++urlCount}`; fx.urls.push(url); return url; }, revokeObjectURL: url => fx.revoked.push(url) },
    setTimeout: (fn, ms) => fx.timers.push({ fn, ms }),
    navigator: api.__noClipboard ? {} : { clipboard: { writeText: async value => { fx.copied.push(value); } } },
    require: name => {
      if (name === "react") return hooks; if (name === "react/jsx-runtime") return require(name);
      if (name === "next/link") return { __esModule: true, default: props => React.createElement("a", props, props.children) };
      if (name === "next/navigation") return { useRouter: () => ({ push: href => routes.push(href) }), useSearchParams: () => new URLSearchParams(api.__query || "") };
      if (name.endsWith("writingTextExport.mjs")) return textExport;
      if (name.endsWith("writingBookState.mjs")) return originalBookState;
      if (name.endsWith("writingApi.js")) return { ...originalApi, writingApi: api };
      if (name.endsWith("writingState.mjs")) return originalState;
      if (name.endsWith("useWritingSurface.js")) return modules.get("useWritingSurface.js");
      if (name.endsWith("v1FrontendApi.js")) return api.__workApi || {};
      if (name.endsWith("api.js")) return { TENANT_ID: "t", CEO_ID: "ceo" };
      if (name.endsWith("workspacePackageApi.js")) return { createInstalledWorkspaceObject: async (...args) => { writes.push(args); return { object_id: args[2].object_type === "WritingBook" ? "new-book" : "new-chapter" }; } };
      if (name.endsWith("SharedConversation.js")) return { ConversationComposer: "composer", useConversationModel: () => api.__model || ({ models: [], selected: null }) };
      if (name.endsWith("EmployeeAvatar.js")) return { EmployeeAvatar: "avatar" };
      if (name.endsWith(".module.css")) return { __esModule: true, default: new Proxy({}, { get: (_target, key) => String(key) }) };
      return { __esModule: true, default: props => React.createElement("div", props) };
    } };
  async function load(name) {
    const source = readFileSync(new URL("../components/writing/" + name, import.meta.url), "utf8");
    const { code } = await swc.transform(source, { filename: name, isModule: true, jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } }, module: { type: "commonjs" } });
    const m = { exports: {} };
    vm.runInNewContext(code, { ...sandbox, module: m, exports: m.exports, require: sandbox.require });
    modules.set(name, m.exports); return m.exports;
  }
  await load("useWritingSurface.js");
  const Component = (await load(path)).default;
  let currentProps = props;
  const render = () => { si = 0; ri = 0; ei = 0; return Component(currentProps); };
  const first = (node, pred) => !node ? null : Array.isArray(node) ? node.map(v => first(v, pred)).find(Boolean) || null : pred(node) ? node : first(node.props?.children, pred) || null;
  const all = (node, pred) => !node || typeof node !== "object" ? [] : Array.isArray(node) ? node.flatMap(v => all(v, pred)) : [...(pred(node) ? [node] : []), ...all(node.props?.children, pred)];
  return { fx, routes, writes, render, find: pred => first(render(), pred), all, setProps: value => { currentProps = value; },
    async flush() { render(); for (const e of effects) if (e.pending) { e.cleanup?.(); e.pending = false; e.cleanup = e.fn(); } await new Promise(resolve => setTimeout(resolve, 0)); return render(); } };
}

const SCOPE = { tenant_id: "t", company_id: "co", workspace_id: "w", instance_id: "i", book_ref: "book", chapter_ref: "chapter" };
const FORMALS = [
  { action: "formal.confirmed", ref: "F1", created_at: "2026-11-13 09:00:00", snapshot: { ref: "draft-1", sha256: "h1", text: FIRST } },
  { action: "candidate.recorded", ref: "C1", created_at: "2026-11-13 10:00:00", draft_ref: "draft-2", selection: { excerpt: "凌晨的雾" }, replacement: "候选替换文字" },
  { action: "formal.confirmed", ref: "F2", created_at: "2026-11-13 11:00:00", snapshot: { ref: "draft-2", sha256: "h2", text: SECOND } },
];
const publishingState = () => ({ scope: SCOPE, read_only: false, draft: { ref: "draft-2", sha256: "h2", text: SECOND, knowledge: [] }, events: [ ...FORMALS, { action: "package.prepared", ref: "P1", formal_ref: "F1", created_at: "2026-11-13 12:00:00", package: { metadata: { introduction: "介绍", credits: "作者" } } } ], responsibility: { employee_name: "章节作者", status: "UNAVAILABLE", reason: "无模型" } });
const publishingProps = formal => ({ state: publishingState(), entry: { mode: "package", book: "book", chapter: "chapter", formal, package: "" }, workspaceId: "w", chapterTitle: "雾色灯塔·第一章", command: async () => ({ ref: "x" }), busy: false, onNavigate() {} });
const findButton = (h, label) => h.find(n => n.type === "button" && n.props?.children === label);

test("publishing formal area shows copy and export actions only for the selected formal version", async () => {
  const h = await writingComponent("WritingPublishingMain.js", publishingProps("F2"));
  await h.flush();
  const section = h.find(n => n.props?.className === "formalSnapshot");
  assert.ok(section, "formal snapshot section is rendered");
  assert.equal(h.all(section, n => n.type === "button" && n.props?.children === "复制正文").length, 1);
  assert.equal(h.all(section, n => n.type === "button" && n.props?.children === "导出 Markdown").length, 1);
});

test("copying the formal version puts the verbatim snapshot text on the clipboard", async () => {
  const h = await writingComponent("WritingPublishingMain.js", publishingProps("F2"));
  await h.flush();
  await findButton(h, "复制正文").props.onClick();
  assert.deepEqual(h.fx.copied, [SECOND]);
  assert.ok(JSON.stringify(h.render()).includes("已复制所选正式稿正文"));
  assert.equal(h.fx.blobs.length, 0, "copy must not touch the export path");
});

test("exporting markdown downloads a UTF-8 blob of the verbatim snapshot with title and version in the name", async () => {
  const h = await writingComponent("WritingPublishingMain.js", publishingProps("F2"));
  await h.flush();
  findButton(h, "导出 Markdown").props.onClick();
  assert.equal(h.fx.blobs.length, 1);
  assert.equal(h.fx.blobs[0].type, "text/markdown;charset=utf-8");
  assert.equal(await h.fx.blobs[0].text(), SECOND, "exported bytes decode to the exact snapshot text");
  assert.equal(h.fx.clicks.length, 1);
  assert.equal(h.fx.clicks[0].download, "雾色灯塔·第一章-正式稿2.md");
  assert.equal(h.fx.clicks[0].href, h.fx.urls[0]);
  assert.equal(h.fx.copied.length, 0, "export must not touch the clipboard");
  assert.ok(JSON.stringify(h.render()).includes("雾色灯塔·第一章-正式稿2.md"));
  assert.equal(h.fx.timers.length, 1);
  h.fx.timers[0].fn();
  assert.deepEqual(h.fx.revoked, h.fx.urls, "object URL is released after the download");
});

test("switching the selected formal version switches the copied and exported snapshot verbatim", async () => {
  const fx = { copied: [], blobs: [], urls: [], clicks: [], revoked: [], timers: [] };
  const h = await writingComponent("WritingPublishingMain.js", publishingProps("F2"), { __fx: fx });
  await h.flush();
  await findButton(h, "复制正文").props.onClick();
  findButton(h, "导出 Markdown").props.onClick();
  h.setProps({ ...publishingProps("F2"), entry: { mode: "package", book: "book", chapter: "chapter", formal: "F1", package: "" } });
  await h.flush();
  await findButton(h, "复制正文").props.onClick();
  findButton(h, "导出 Markdown").props.onClick();
  assert.deepEqual(fx.copied, [SECOND, FIRST]);
  assert.equal(await fx.blobs[1].text(), FIRST);
  assert.equal(fx.clicks[1].download, "雾色灯塔·第一章-正式稿1.md");
});

test("without an explicitly selected formal version the two actions never render", async () => {
  const h = await writingComponent("WritingPublishingMain.js", publishingProps(""));
  await h.flush();
  assert.equal(findButton(h, "复制正文"), null);
  assert.equal(findButton(h, "导出 Markdown"), null);
  assert.ok(JSON.stringify(h.render()).includes("请选择已确认的正式稿"));
});

test("when the clipboard is unavailable no text is written and the notice stays honest", async () => {
  const h = await writingComponent("WritingPublishingMain.js", publishingProps("F2"), { __noClipboard: true });
  await h.flush();
  await findButton(h, "复制正文").props.onClick();
  assert.deepEqual(h.fx.copied, []);
  assert.ok(JSON.stringify(h.render()).includes("不支持一键复制"));
});

test("chapter candidate content never exposes the formal copy or export actions", async () => {
  const state = { scope: SCOPE, read_only: false, draft: { ref: "draft-2", sha256: "h2", text: SECOND, knowledge: [] },
    events: FORMALS, responsibility: { employee_name: "章节作者", status: "UNAVAILABLE", reason: "无模型" } };
  const props = { state, entry: { mode: "chapter", book: "book", chapter: "chapter" }, workspaceId: "w", company: "co", entryMetadata: { company_employee_ref: "employee", employee_name: "章节作者", models: [] }, command: async () => ({}), onNavigate() {}, onRefresh() {}, onExecutionLock() {}, onDetails() {} };
  const h = await writingComponent("WritingChapterMain.js", props);
  await h.flush();
  assert.ok(JSON.stringify(h.render()).includes("候选替换文字"), "candidate content is rendered");
  assert.equal(findButton(h, "复制正文"), null);
  assert.equal(findButton(h, "导出 Markdown"), null);
});
