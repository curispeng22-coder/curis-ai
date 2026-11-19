// T-017 / W03-A 前端组件测试：配置前被拦、配置后回到任务、输入保留、
// 待连接能力、未就绪加载态。沿用 frontend/tests 的 node --test + SWC/vm 渲染写法。
// 纯逻辑直接 import lib；组件通过 SWC 编译后用真实 react/jsx-runtime 渲染并驱动事件。

import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";
import path from "node:path";
import vm from "node:vm";

import * as logic from "../lib/firstTaskSetup.mjs";

const require = createRequire(import.meta.url);
const React = require("react");
const jsxRuntime = require("react/jsx-runtime");
const swc = require("next/dist/build/swc");
await swc.loadBindings();

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const COMP_CODE = (await swc.transform(
  readFileSync(path.join(ROOT, "components/v1/FirstTaskModelSetup.js"), "utf8"),
  { filename: "FirstTaskModelSetup.js", isModule: true,
    jsc: { parser: { syntax: "ecmascript", jsx: true }, transform: { react: { runtime: "automatic" } } },
    module: { type: "commonjs" } },
)).code;

// ---- helpers ----
function text(n) {
  if (n == null || typeof n === "boolean") return "";
  if (typeof n !== "object") return String(n);
  if (Array.isArray(n)) return n.map(text).join("");
  return text(n.props?.children);
}
function nodes(n, pred) {
  const out = [];
  const visit = (v) => {
    if (!v || typeof v !== "object") return;
    if (Array.isArray(v)) { v.forEach(visit); return; }
    if (pred(v)) out.push(v);
    visit(v.props?.children);
  };
  visit(n);
  return out;
}
function deep(n) {
  if (!n || typeof n !== "object") return n;
  if (Array.isArray(n)) return n.map(deep);
  if (typeof n.type === "function") return deep(n.type(n.props || {}));
  return { ...n, props: { ...n.props, children: deep(n.props?.children) } };
}

// 后端 read_draft 真实形状（first_launch_service.read_draft）。
const readDraft = (next_action) => ({
  work: { entity_id: "work-1", lifecycle_status: "PLANNED" },
  draft: { text: "写一篇关于秋日的文稿", revision: 1 },
  execution: { status: next_action === "CONTINUE_TASK" ? "AVAILABLE" : "UNAVAILABLE" },
  next_action,
  return_to: { company_id: "C", workspace_id: "W", work_id: "work-1" },
});

// 交互式渲染器：自定义 useReducer/useEffect（状态存在 slots；effect 按 deps 变化记录、
// flushEffects 手动驱动），真实 jsx-runtime，deep() 解析子组件后返回可断言的元素树。
function harness(api, opts = {}) {
  let cursor = 0;
  let effectCursor = 0;
  const slots = [];
  const effects = [];
  const depsEqual = (a, b) => Array.isArray(a) && Array.isArray(b)
    && a.length === b.length && a.every((value, index) => Object.is(value, b[index]));
  const hooks = {
    useReducer(reducer, initialArg, init) {
      const i = cursor++;
      if (!(i in slots)) slots[i] = { value: init ? init(initialArg) : initialArg };
      const dispatch = (action) => { slots[i].value = reducer(slots[i].value, action); };
      return [slots[i].value, dispatch];
    },
    useEffect(fn, deps) {
      const i = effectCursor++;
      const prior = effects[i];
      if (!prior || !depsEqual(prior.deps, deps)) effects[i] = { fn, deps, ran: false };
    },
  };
  const mod = { exports: {} };
  vm.runInNewContext(COMP_CODE, {
    module: mod, exports: mod.exports, console,
    require: (p) => p === "react" ? hooks
      : p === "react/jsx-runtime" ? jsxRuntime
        : p.includes("firstTaskSetup.mjs") ? logic
          : p.includes("firstTaskApi.js") ? { __esModule: true }
            : {},
  });
  const Component = mod.exports.default;
  const props = {
    api, runtimeStatus: opts.runtimeStatus || "ready", teams: opts.teams || [],
    companyId: opts.companyId ?? "C", writingWorkspaceId: opts.writingWorkspaceId ?? "W",
    storage: opts.storage, initialInput: opts.initialInput || "",
  };
  return {
    render: () => { cursor = 0; effectCursor = 0; return deep(Component(props)); },
    flushEffects: async () => { for (const entry of effects) if (entry && !entry.ran) { entry.ran = true; await entry.fn(); } },
  };
}

// sessionStorage 替身：只存 workId（业务 id），符合 lib 的读写防护。
function fakeStorage(init = new Map()) {
  return {
    getItem: (key) => (init.has(key) ? init.get(key) : null),
    setItem: (key, value) => { init.set(String(key), String(value)); },
  };
}

function buttonByText(tree, label) {
  return nodes(tree, (n) => n.type === "button" && text(n).includes(label))[0];
}

// ============================================================
// 1) 纯状态机 / 选择器
// ============================================================

test("配置前被拦：next_action=CONFIGURE_MODEL 打开配置弹窗、不执行任务、输入保留", () => {
  let s = logic.defaultFirstTaskState();
  s = logic.firstTaskReducer(s, { type: "INPUT", input: "写一篇关于秋日的文稿" });
  s = logic.firstTaskReducer(s, { type: "EXECUTE_RESULT", result: readDraft(logic.CONFIGURE_MODEL) });
  assert.equal(s.phase, logic.PHASE.SETUP, "应停在模型配置弹窗");
  assert.equal(s.executed, false, "配置前不应执行任务");
  assert.equal(s.configured, false);
  assert.equal(s.input, "写一篇关于秋日的文稿", "输入不丢");
  assert.equal(s.workId, "work-1", "保存草稿后记录 return_to.work_id");
  assert.equal(s.revision, 1);
  assert.equal(logic.shouldOpenModelSetup(logic.CONFIGURE_MODEL), true);
  assert.equal(logic.shouldOpenModelSetup(logic.CONTINUE_TASK), false);
});

test("配置后回到任务：重读草稿 CONTINUE_TASK 回到原任务、输入保留", () => {
  let s = logic.defaultFirstTaskState();
  s = logic.firstTaskReducer(s, { type: "INPUT", input: "写一篇关于秋日的文稿" });
  s = logic.firstTaskReducer(s, { type: "EXECUTE_RESULT", result: readDraft(logic.CONFIGURE_MODEL) });
  s = logic.firstTaskReducer(s, { type: "CONFIGURE_RESULT", result: readDraft(logic.CONTINUE_TASK) });
  assert.equal(s.phase, logic.PHASE.RESUMED, "配置成功后回到原任务");
  assert.equal(s.configured, true);
  assert.equal(s.input, "写一篇关于秋日的文稿", "回到原任务后输入不丢");
  assert.match(s.message, /回到原任务/);
});

test("输入保留：配置前 / 配置完成 / 取消配置 / 配置未完成 都不丢输入", () => {
  const INPUT = "写一篇关于秋日的文稿";
  const visit = (s, at) => assert.equal(s.input, INPUT, `${at} 输入应保留`);
  let s = logic.firstTaskReducer(logic.defaultFirstTaskState(), { type: "INPUT", input: INPUT });
  s = logic.firstTaskReducer(s, { type: "EXECUTE_RESULT", result: readDraft(logic.CONFIGURE_MODEL) });
  visit(s, "配置前被拦");
  const cancelled = logic.firstTaskReducer(s, { type: "CANCEL_SETUP" });
  assert.equal(cancelled.phase, logic.PHASE.EDITING, "取消后回到编辑态");
  visit(cancelled, "取消配置");
  const notReady = logic.firstTaskReducer(s, { type: "CONFIGURE_RESULT", result: readDraft(logic.CONFIGURE_MODEL) });
  assert.equal(notReady.phase, logic.PHASE.SETUP, "重读仍未配置时诚实停留在弹窗");
  visit(notReady, "配置未完成");
  const resumed = logic.firstTaskReducer(s, { type: "CONFIGURE_RESULT", result: readDraft(logic.CONTINUE_TASK) });
  visit(resumed, "配置完成");
});

test("待连接能力：未配置团队显示「待连接能力」，已配置显示「就绪」", () => {
  assert.equal(logic.capabilityLabel({ status_label: "待连接能力" }), "待连接能力");
  assert.equal(logic.needsCapability({ status_label: "待连接能力" }), true);
  assert.equal(logic.capabilityLabel({ execution: { status: "UNAVAILABLE" } }), "待连接能力");
  assert.equal(logic.capabilityLabel({ status_label: "就绪", execution: { status: "AVAILABLE" } }), "就绪");
  assert.equal(logic.needsCapability({ status_label: "就绪" }), false);
  assert.equal(logic.PENDING_CAPABILITY, "待连接能力");
});

test("未就绪加载态：idle/loading 显示加载态，ready/empty 不显示", () => {
  assert.equal(logic.isRuntimeNotReady("idle"), true);
  assert.equal(logic.isRuntimeNotReady("loading"), true);
  assert.equal(logic.isRuntimeNotReady("ready"), false);
  assert.equal(logic.isRuntimeNotReady("empty"), false);
});

// ============================================================
// 2) 组件渲染 + 交互（真实组件 / 真实 jsx-runtime / 注入 api）
// ============================================================

const teams = [
  { kind: "content_growth", name: "内容增长", workspace_id: "W1", status_label: "待连接能力", execution: { status: "UNAVAILABLE" } },
  { kind: "writing", name: "写作", workspace_id: "W2", status_label: "待连接能力", execution: { status: "UNAVAILABLE" } },
  { kind: "music", name: "音乐创作", workspace_id: "W3", status_label: "待连接能力" },
];

test("组件·未就绪加载态：runtime loading 只显示加载态，不闪「还没有公司」、不出现执行入口", () => {
  const tree = harness({ saveWritingTaskDraft: async () => readDraft(logic.CONFIGURE_MODEL) }, { runtimeStatus: "loading", teams }).render();
  const body = text(tree);
  assert.match(body, /正在打开 Curis 工作台/);
  assert.ok(nodes(tree, (n) => n.props?.role === "status").length >= 1, "加载态应有 role=status");
  assert.doesNotMatch(body, /这里还没有公司/);
  assert.doesNotMatch(body, /执行任务/);
  assert.doesNotMatch(body, /role="dialog"/);
});

test("组件·待连接能力：未配置团队显示「待连接能力」标签", () => {
  const tree = harness({}, { runtimeStatus: "ready", teams }).render();
  assert.equal(nodes(tree, (n) => n.props?.["data-capability"] === "待连接能力").length, 3);
  assert.match(text(tree), /团队与能力/);
  assert.match(text(tree), /待连接能力/);
});

test("组件·首启不走向导：ready 且未执行时不弹配置弹窗，主路径为任务输入", () => {
  const tree = harness({}, { runtimeStatus: "ready", teams }).render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 0, "首启/未执行时不应弹窗");
  assert.ok(buttonByText(tree, "执行任务"), "应有执行任务按钮");
  assert.doesNotMatch(text(tree), /前往模型设置/);
});

test("组件·配置前被拦：点执行任务（CONFIGURE_MODEL）弹出模型配置弹窗，输入保留", async () => {
  let saved = null;
  const api = { saveWritingTaskDraft: async (...args) => { saved = args; return readDraft(logic.CONFIGURE_MODEL); } };
  const h = harness(api, { runtimeStatus: "ready", teams, initialInput: "写一篇关于秋日的文稿" });
  let tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 0, "点击前无弹窗");
  const exec = buttonByText(tree, "执行任务");
  assert.ok(exec, "应能找到执行任务按钮");
  await exec.props.onClick();
  tree = h.render();
  assert.equal(saved[0], "C");
  assert.equal(saved[1], "W");
  assert.equal(saved[2].text, "写一篇关于秋日的文稿", "草稿保存应携带输入");
  assert.equal(saved[2].expectedRevision, 0, "首次执行 expected_revision=0");
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 1, "配置前应弹出模型配置弹窗");
  assert.match(text(tree), /先连接模型，才能开始执行/);
  assert.equal(nodes(tree, (n) => n.props?.["data-preserved-input"]).length, 1);
  assert.equal(text(nodes(tree, (n) => n.props?.["data-preserved-input"])[0]), "写一篇关于秋日的文稿", "弹窗内输入保留");
  assert.ok(buttonByText(tree, "配置完成，回到原任务"));
  assert.ok(buttonByText(tree, "取消配置"));
});

test("组件·配置后回到任务：配置完成（CONTINUE_TASK）关弹窗、回原任务、输入不丢", async () => {
  const api = {
    saveWritingTaskDraft: async () => readDraft(logic.CONFIGURE_MODEL),
    readWritingTaskDraft: async () => readDraft(logic.CONTINUE_TASK),
  };
  const h = harness(api, { runtimeStatus: "ready", teams, initialInput: "写一篇关于秋日的文稿" });
  let tree = h.render();
  await buttonByText(tree, "执行任务").props.onClick();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 1, "配置前弹窗打开");
  await buttonByText(tree, "配置完成，回到原任务").props.onClick();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 0, "配置完成后弹窗关闭");
  assert.match(text(tree), /已回到原任务/);
  const ta = nodes(tree, (n) => n.type === "textarea")[0];
  assert.equal(ta.props.value, "写一篇关于秋日的文稿", "回到原任务后输入仍在");
});

test("组件·取消配置不丢输入：取消后关弹窗、回到编辑态、输入仍在", async () => {
  const api = { saveWritingTaskDraft: async () => readDraft(logic.CONFIGURE_MODEL) };
  const h = harness(api, { runtimeStatus: "ready", teams, initialInput: "写一篇关于秋日的文稿" });
  let tree = h.render();
  await buttonByText(tree, "执行任务").props.onClick();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 1);
  await buttonByText(tree, "取消配置").props.onClick();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 0, "取消后弹窗关闭");
  assert.match(text(tree), /已取消配置/);
  const ta = nodes(tree, (n) => n.type === "textarea")[0];
  assert.equal(ta.props.value, "写一篇关于秋日的文稿", "取消配置后输入保留");
});

// ============================================================
// 3) 回归：前往设置不离开原页（新标签）+ 重挂载读回服务端草稿
//    （不限于直接注入 CONTINUE_TASK 的假 API 测试：覆盖真实 UI 的
//     「从原任务打开设置 → 配置完回原任务 / 取消 / 刷新后退」路径）
// ============================================================

test("纯逻辑·workId 持久化：合法 id 可读写，非法值拒写拒读", () => {
  const store = fakeStorage();
  const key = logic.firstTaskWorkKey("C", "W");
  assert.equal(logic.readStoredWorkId(store, key), "", "空存储读出为空");
  logic.writeStoredWorkId(store, key, "work-1");
  assert.equal(logic.readStoredWorkId(store, key), "work-1", "写入后可读回");
  logic.writeStoredWorkId(store, "bad", "含空格的 id");
  assert.equal(store.getItem("bad"), null, "非法 id 不写入");
  logic.writeStoredWorkId(store, "long", "x".repeat(129));
  assert.equal(store.getItem("long"), null, "超长 id 不写入");
  assert.equal(logic.readStoredWorkId(null, key), "", "无 storage 安全返回空");
});

test("纯逻辑·重挂载读回：输入为空时采纳服务端草稿，模型未配置回弹窗、已配置回任务；有输入不覆盖", () => {
  let s = logic.firstTaskReducer(logic.defaultFirstTaskState(), { type: "RESTORE_RESULT", result: readDraft(logic.CONFIGURE_MODEL) });
  assert.equal(s.phase, logic.PHASE.SETUP, "仍未配置时重新打开配置弹窗");
  assert.equal(s.input, "写一篇关于秋日的文稿", "输入从服务端草稿恢复");
  assert.equal(s.workId, "work-1");
  assert.equal(s.revision, 1);
  assert.equal(s.executed, false);
  assert.match(s.message, /已读回/);

  s = logic.firstTaskReducer(logic.defaultFirstTaskState(), { type: "RESTORE_RESULT", result: readDraft(logic.CONTINUE_TASK) });
  assert.equal(s.phase, logic.PHASE.RESUMED, "模型已配置时回到原任务");
  assert.equal(s.input, "写一篇关于秋日的文稿");
  assert.match(s.message, /模型已就绪/);

  s = logic.firstTaskReducer({ ...logic.defaultFirstTaskState(), input: "用户新输入" },
    { type: "RESTORE_RESULT", result: readDraft(logic.CONFIGURE_MODEL) });
  assert.equal(s.input, "用户新输入", "读回绝不覆盖用户已输入的内容");

  s = logic.firstTaskReducer(logic.defaultFirstTaskState(), { type: "RESTORE_RESULT", result: { next_action: logic.CONFIGURE_MODEL, draft: { text: "" } } });
  assert.equal(s.input, "", "空草稿不产生恢复");
});

test("组件·执行后 workId 写入存储：保存草稿成功即持久化，供重挂载读回", async () => {
  const store = fakeStorage();
  const api = { saveWritingTaskDraft: async () => readDraft(logic.CONFIGURE_MODEL) };
  const h = harness(api, { runtimeStatus: "ready", teams, storage: store, initialInput: "写一篇关于秋日的文稿" });
  const tree = h.render();
  await buttonByText(tree, "执行任务").props.onClick();
  assert.equal(store.getItem(logic.firstTaskWorkKey("C", "W")), "work-1", "保存后 workId 已写入 storage");
});

test("组件·前往设置不离开原页（回归）：设置链接新标签打开，弹窗与输入保留可核对", async () => {
  const api = { saveWritingTaskDraft: async () => readDraft(logic.CONFIGURE_MODEL) };
  const h = harness(api, { runtimeStatus: "ready", teams, initialInput: "写一篇关于秋日的文稿" });
  let tree = h.render();
  await buttonByText(tree, "执行任务").props.onClick();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 1, "弹窗打开");
  const link = nodes(tree, (n) => n.type === "a" && text(n).includes("模型设置"))[0];
  assert.ok(link, "应有模型设置链接");
  assert.equal(link.props.href, "/ceo-office/settings?tab=models");
  assert.equal(link.props.target, "_blank", "设置链接必须新标签打开（保留本页）");
  assert.match(link.props.rel, /noreferrer/);
  assert.match(text(link), /在新标签打开模型设置/, "文案说明是新标签打开");
  assert.match(text(tree), /回到本页/, "文案说明配置完成后回到本页核对");
  assert.equal(nodes(tree, (n) => n.props?.["data-preserved-input"]).length, 1, "弹窗内输入保留");
  assert.equal(text(nodes(tree, (n) => n.props?.["data-preserved-input"])[0]), "写一篇关于秋日的文稿");
});

test("组件·重挂载读回草稿（回归，未配置）：刷新/后退后弹窗重开、输入从服务端草稿恢复", async () => {
  const store = fakeStorage(new Map([[logic.firstTaskWorkKey("C", "W"), "work-1"]]));
  const reads = [];
  const api = {
    readWritingTaskDraft: async (...args) => { reads.push(args); return readDraft(logic.CONFIGURE_MODEL); },
  };
  const h = harness(api, { runtimeStatus: "ready", teams, storage: store, initialInput: "" });
  let tree = h.render();
  await h.flushEffects();
  assert.equal(reads.length, 1, "挂载后按存储的 workId 读服务端草稿");
  assert.deepEqual(reads[0], ["C", "W", "work-1"]);
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 1, "重挂载后配置弹窗重新打开");
  assert.match(text(tree), /已读回上次保留的任务草稿/, "提示已读回草稿");
  const ta = nodes(tree, (n) => n.type === "textarea")[0];
  assert.equal(ta.props.value, "写一篇关于秋日的文稿", "输入从服务端草稿恢复，不丢");
  assert.equal(text(nodes(tree, (n) => n.props?.["data-preserved-input"])[0]), "写一篇关于秋日的文稿");
  // 取消仍不丢输入
  await buttonByText(tree, "取消配置").props.onClick();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 0);
  assert.equal(nodes(tree, (n) => n.type === "textarea")[0].props.value, "写一篇关于秋日的文稿", "取消后输入仍在");
});

test("组件·重挂载读回草稿（回归，已配置）：模型就绪时回到编辑态、输入恢复、可继续执行", async () => {
  const store = fakeStorage(new Map([[logic.firstTaskWorkKey("C", "W"), "work-1"]]));
  const api = { readWritingTaskDraft: async () => readDraft(logic.CONTINUE_TASK) };
  const h = harness(api, { runtimeStatus: "ready", teams, storage: store, initialInput: "" });
  let tree = h.render();
  await h.flushEffects();
  tree = h.render();
  assert.equal(nodes(tree, (n) => n.props?.role === "dialog").length, 0, "已配置：不再弹配置弹窗");
  const ta = nodes(tree, (n) => n.type === "textarea")[0];
  assert.equal(ta.props.value, "写一篇关于秋日的文稿", "输入从服务端草稿恢复");
  assert.match(text(tree), /模型已就绪/);
  const exec = buttonByText(tree, "执行任务");
  assert.ok(exec, "回到原任务后可再次执行");
  assert.equal(exec.props.disabled, false);
});
