import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("S12 exposes one recoverable Terra loading and error experience", async () => {
  const [errorPage, loadingPage] = await Promise.all([
    read("../app/error.js"),
    read("../app/loading.js"),
  ]);

  assert.match(errorPage, /TerraErrorState/);
  assert.match(errorPage, /onRetry=\{reset\}/);
  assert.doesNotMatch(errorPage, /error\\.message/);
  assert.match(loadingPage, /TerraLoadingSkeleton/);
  assert.match(loadingPage, /页面加载中/);
});

test("task identity remains usable when optional execution facts fail", async () => {
  const page = await read("../app/ceo-office/execution/tasks/[id]/page.js");

  assert.match(page, /const taskPayload = await getTask\(id\)/);
  assert.match(page, /Promise\.allSettled/);
  assert.match(page, /部分执行事实暂时无法读取/);
});

test("project remains visible when optional organization facts fail", async () => {
  const page = await read("../app/ceo-office/projects/[id]/page.js");

  assert.match(page, /const projectPayload = await getProject\(id\)/);
  assert.match(page, /Promise\.allSettled/);
  assert.match(page, /if \(taskResult\.status === "rejected"\) throw taskResult\.reason/);
});
