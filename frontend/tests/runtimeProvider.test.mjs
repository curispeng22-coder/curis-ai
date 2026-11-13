import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";


const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("CEO Desk presents the Runtime-backed AI workforce relationship", async () => {
  const [desk, business, workspace, onboarding] = await Promise.all([
    read("../app/ceo-office/page.js"),
    read("../app/ceo-office/business/page.js"),
    read("../app/ceo-office/workspace/page.js"),
    read("../app/onboarding/page.js"),
  ]);

  for (const source of [desk, business, workspace]) {
    assert.match(source, /useRuntime/);
    assert.doesNotMatch(source, /getProjects|getTasks|getHomeSummary|getOperatingDay|project_type/);
  }
  assert.match(desk, /AI 团队运行图/);
  assert.match(desk, /CEO Assistant/);
  assert.match(desk, /汇报对象/);
  assert.match(desk, /能力引用/);
  assert.match(desk, /专业 AI 员工/);
  assert.match(onboarding, /createFoundingRun/);
  assert.match(onboarding, /getFoundingRun/);
  assert.match(onboarding, /transitionRuntimeEntity/);
  assert.doesNotMatch(onboarding, /localStorage|createCompany\(/);
});

test("Runtime provider exposes stable loading empty forbidden and error states", async () => {
  const [provider, states] = await Promise.all([
    read("../components/runtime/RuntimeProvider.js"),
    read("../components/runtime/RuntimeStates.js"),
  ]);

  assert.match(provider, /status: result\.snapshot \? "ready" : "empty"/);
  assert.match(provider, /"forbidden"/);
  assert.match(states, /RuntimeLoading/);
  assert.match(states, /RuntimeError/);
  assert.match(states, /RuntimeEmpty/);
  assert.doesNotMatch(states, /error\.message|stack/);
});

test("Global Assistant is one Runtime-backed overlay with user identity and no task command bypass", async () => {
  const assistant = await read("../components/assistant/GlobalAssistant.js");

  assert.match(assistant, /useRuntime/);
  assert.match(assistant, /getAssistantIdentity/);
  assert.match(assistant, /assistant\.open &&/);
  assert.match(assistant, /position|fixed/);
  assert.match(assistant, /closeAssistant/);
  assert.match(assistant, /minimizeAssistant/);
  assert.match(assistant, /我正在关注/);
  assert.match(assistant, /workspaceEntryHref/);
  assert.match(assistant, /告诉我你正在关注的经营问题/);
  assert.doesNotMatch(assistant, /getAssistantSnapshot|getAssistantNotifications|submitAssistantCommand/);
  assert.doesNotMatch(assistant, /createTask|<aside|xl:grid-cols-3/);
});

test("navigation keeps Company OS primary entries and moves old execution routes to compatibility", async () => {
  const nav = await read("../components/terra/TerraNavData.js");

  assert.match(nav, /label: "业务版图"[\s\S]*href: "\/ceo-office\/business"/);
  assert.match(nav, /label: "工作空间"[\s\S]*href: "\/ceo-office\/workspace"[\s\S]*subs: \[\]/);
  assert.match(nav, /group: "兼容入口"/);
  assert.match(nav, /href: "\/ceo-office\/projects"/);
  assert.match(nav, /href: "\/ceo-office\/execution"/);
  assert.match(nav, /href: "\/ceo-office\/execution\/pipeline"/);
  assert.match(nav, /PERSISTENT_LABELS = \["CEO 工作台", "经营", "业务版图", "工作空间"\]/);
});

test("layout and shell preserve one provider chain, three themes and frozen dimensions", async () => {
  const [layout, shell, css] = await Promise.all([
    read("../app/layout.js"),
    read("../components/terra/TerraShell.js"),
    read("../app/globals.css"),
  ]);

  assert.match(layout, /<RuntimeProvider>[\s\S]*<GlobalAssistantProvider>/);
  assert.match(shell, /w-\[220px\]|TerraSidebar/);
  assert.match(shell, /h-\[52px\]/);
  assert.match(shell, /跟随系统/);
  assert.match(shell, /浅色/);
  assert.match(shell, /深色/);
  assert.match(css, /data-theme="system"/);
  assert.match(css, /data-theme="light"/);
  assert.match(css, /data-theme="dark"/);
});
