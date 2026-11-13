import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import { uploadEmployeeAvatar } from "../lib/talentMarket.js";


test("avatar upload uses the canonical Employee endpoint and keeps bytes out of JSON", async () => {
  const originalFetch = globalThis.fetch;
  const file = new Blob([new Uint8Array([0x89, 0x50, 0x4e, 0x47])], { type: "image/png" });
  let observed;
  globalThis.fetch = async (url, options) => {
    observed = { url: String(url), options };
    return new Response(JSON.stringify({ id: "employee-1", avatar_ref: "asset:abc.png" }), {
      status: 200,
      headers: { "Content-Type": "application/json" },
    });
  };
  try {
    await uploadEmployeeAvatar("employee-1", file);
    assert.match(observed.url, /\/api\/workspace\/employees\/employee-1\/avatar$/);
    assert.equal(observed.options.method, "PUT");
    assert.equal(observed.options.headers["Content-Type"], "image/png");
    assert.equal(observed.options.body, file);
  } finally {
    globalThis.fetch = originalFetch;
  }
});


test("recruitment exposes upload preset and fallback without adding another identity store", async () => {
  const page = await readFile(
    new URL("../app/ceo-office/talent-market/page.js", import.meta.url), "utf8"
  );
  const avatar = await readFile(
    new URL("../components/v1/EmployeeAvatar.js", import.meta.url), "utf8"
  );
  const projection = await readFile(
    new URL("../lib/organizationProjection.js", import.meta.url), "utf8"
  );
  assert.match(page, /上传图片/);
  assert.match(page, /暂不设置/);
  assert.match(page, /EMPLOYEE_AVATAR_PRESETS/);
  assert.match(page, /重新上传头像并完成/);
  assert.match(avatar, /employee\?\.avatar_ref/);
  assert.match(avatar, /data-avatar-ref=.*fallback/);
  assert.match(projection, /avatarRef: text\(employee\?\.avatar_ref\)/);
  assert.doesNotMatch(page, /readAsDataURL|data:image/);
});


test("Curis ships eight local preset assets", async () => {
  const ids = ["iris", "sage", "coral", "amber", "sky", "plum", "mint", "slate"];
  for (const id of ids) {
    const asset = await readFile(
      new URL(`../public/avatars/curis-employee/${id}.svg`, import.meta.url), "utf8"
    );
    assert.match(asset, /^<svg/);
    assert.doesNotMatch(asset, /(?:href|src)=["']https?:\/\//);
  }
});

async function editDrawer(employee, bindings = [], capabilities = [], bindingError = null) {
  const { createRequire } = await import('node:module');
  const vm = await import('node:vm');
  const require = createRequire(import.meta.url), React = require('react'), swc = require('next/dist/build/swc');
  await swc.loadBindings();
  const source = await readFile(new URL('../app/ceo-office/organization/employees/[id]/EmployeeEditDrawer.js', import.meta.url), 'utf8');
  const { code } = await swc.transform(source, { filename: 'EmployeeEditDrawer.js', isModule: true, jsc: { parser: { syntax: 'ecmascript', jsx: true }, transform: { react: { runtime: 'automatic' } } }, module: { type: 'commonjs' } });
  const states = [], effects = [], calls = [], successes = []; let i = 0;
  const hooks = { ...React, useState: (initial) => { const n = i++; if (!(n in states)) states[n] = initial; return [states[n], value => { states[n] = typeof value === 'function' ? value(states[n]) : value; }]; }, useEffect: fn => effects.push(fn) };
  const loaded = { exports: {} };
  vm.runInNewContext(code, { module: loaded, exports: loaded.exports, require: name => {
    if (name === 'react') return hooks;
    if (name === 'react/jsx-runtime') return require(name);
    if (name.endsWith('api.js')) return { updateEmployee: async (id, payload) => { calls.push({ method: 'PATCH', id, payload }); return { ...employee, ...payload }; }, setEmployeeCapabilities: async (id, payload) => { calls.push({ method: 'PUT', id, payload }); if (bindingError) throw bindingError; return { bindings: payload }; } };
    return { TerraDrawer: 'drawer', TerraInput: 'input', TerraButton: 'button' };
  } });
  const render = () => { i = 0; effects.length = 0; return loaded.exports.default({ open: true, employee, bindings, capabilities, onSuccess: (...args) => successes.push(args) }); };
  render(); effects[0]();
  const find = (node, match) => !node ? null : Array.isArray(node) ? node.map(n => find(n, match)).find(Boolean) : match(node) ? node : find(node.props?.children, match);
  return { calls, successes, tree: render, change: (match, value) => find(render(), match).props.onChange({ target: { value } }), toggle: () => find(render(), n => n.props?.type === 'checkbox').props.onChange(), submit: () => find(render(), n => n.type === 'form').props.onSubmit({ preventDefault() {} }) };
}

const employeeFixture = { id: 'employee-test', name: '章节作者', instructions_override: '', status: 'disabled', enabled: false, avatar_ref: 'existing-avatar' };
const hiddenBindings = [{ capability_source: 'local', capability_type: 'model', capability_id: 'unavailable-existing', enabled: false, priority: 73 }];

test('actual Drawer name-only with empty instructions PATCHes only name and preserves hidden bindings', async () => {
  const h = await editDrawer(employeeFixture, hiddenBindings);
  h.change(n => n.props?.label === '员工名称', '章节作者·验收一'); await h.submit();
  assert.deepEqual(JSON.parse(JSON.stringify(h.calls)), [{ method: 'PATCH', id: employeeFixture.id, payload: { name: '章节作者·验收一' } }]);
  assert.equal(h.successes.length, 1); assert.equal(h.successes[0][1].bindings, hiddenBindings);
  assert.equal(h.successes[0][0].enabled, false); assert.equal(h.successes[0][0].avatar_ref, 'existing-avatar');
});

test('actual Drawer unchanged values issue no writes, including unedited whitespace instructions', async () => {
  const h = await editDrawer({ ...employeeFixture, instructions_override: ' 原说明 ' }, hiddenBindings);
  await h.submit(); assert.equal(h.calls.length, 0); assert.equal(h.successes[0][1].bindings, hiddenBindings);
});

test('actual Drawer explicit clear and status edit send only the edited fields', async () => {
  const h = await editDrawer({ ...employeeFixture, instructions_override: '原说明' });
  h.change(n => n.props?.id === 'employee-edit-responsibility', ''); await h.submit();
  assert.deepEqual(JSON.parse(JSON.stringify(h.calls[0].payload)), { instructions_override: '' });
  const status = await editDrawer(employeeFixture);
  status.change(n => n.props?.id === 'employee-edit-status', 'idle'); await status.submit();
  assert.deepEqual(JSON.parse(JSON.stringify(status.calls[0].payload)), { status: 'idle' });
});

test('actual Drawer blank name refuses all writes', async () => {
  const h = await editDrawer(employeeFixture); h.change(n => n.props?.label === '员工名称', ' '); await h.submit();
  assert.equal(h.calls.length, 0); assert.ok(JSON.stringify(h.tree()).includes('请输入员工名称'));
});

test('actual Drawer explicit capability edit retains PUT and real authorization refusal', async () => {
  const cap = { source: 'local', capability_type: 'model', capability_id: 'chosen', label: '模型' };
  const h = await editDrawer(employeeFixture, [], [cap], new Error('not authorized'));
  h.toggle(); await h.submit();
  assert.deepEqual(JSON.parse(JSON.stringify(h.calls)), [{ method: 'PUT', id: employeeFixture.id, payload: [{ capability_source: 'local', capability_type: 'model', capability_id: 'chosen', priority: 10, enabled: true }] }]);
  assert.equal(h.successes.length, 0); assert.ok(JSON.stringify(h.tree()).includes('部分能力超出该岗位授权范围'));
});
