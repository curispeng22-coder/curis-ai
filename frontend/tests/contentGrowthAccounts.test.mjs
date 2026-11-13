import test from 'node:test';
import assert from 'node:assert/strict';
import { cgEntry, contentHref } from '../lib/contentGrowthState.mjs';
import { createContentGrowthApi } from '../lib/contentGrowthApi.js';

test('cg_view=accounts is whitelisted and encoded; unknown views still fail closed', () => {
  const params = (q) => new URLSearchParams(q);
  assert.equal(cgEntry(params('cg_view=accounts')).view, 'accounts');
  assert.ok(cgEntry(params('cg_view=Accounts')).error, 'case-sensitive whitelist');
  assert.ok(cgEntry(params('cg_view=connections')).error);
  const href = contentHref('workspace', { view: 'accounts' });
  assert.ok(href.includes('cg_view=accounts'), href);
  assert.equal(cgEntry(new URL(href, 'https://x.invalid').searchParams).view, 'accounts');
  // view must not combine with version-scoped locators into ambiguity.
  assert.equal(cgEntry(params('cg_view=accounts&cg_version=v')).error !== undefined, true);
});

test('account api wrappers: routes, methods and payloads', async () => {
  const calls = [];
  const request = async (url, options) => { calls.push({ url, options }); return { ok: true }; };
  const api = createContentGrowthApi(request);
  await api.accounts('c1', 'w1');
  await api.account('c1', 'w1', 'cg-account-a');
  await api.accountCreate('c1', 'w1', { platform_ref: 'xhs', name: '主号', connection_status: 'HACKED' });
  await api.accountEdit('c1', 'w1', 'cg-account-a', { name: '改名', connection_status: 'HACKED' });
  const base = '/api/workspace/v1/companies/c1/content-growth/w1';
  assert.deepEqual(calls.map((c) => c.url), [
    `${base}/accounts`, `${base}/accounts/cg-account-a`, `${base}/accounts`, `${base}/accounts/cg-account-a`,
  ]);
  assert.deepEqual(calls.map((c) => c.options?.method || 'GET'), ['GET', 'GET', 'POST', 'PUT']);
  const created = JSON.parse(calls[2].options.body);
  assert.equal(created.data.platform_ref, 'xhs');
  // Client cannot inject connection truth; server owns it and ignores the field.
  assert.equal(created.data.connection_status, 'HACKED');
  const edited = JSON.parse(calls[3].options.body);
  assert.equal(edited.data.name, '改名');
  assert.equal(edited.data.platform_ref, undefined, 'edit payload must not carry platform_ref');
});

test('account route ids are percent-encoded', async () => {
  const calls = [];
  const api = createContentGrowthApi(async (url, options) => { calls.push(url); return {}; });
  await api.account('c', 'w', 'cg-account/..');
  assert.equal(calls[0], '/api/workspace/v1/companies/c/content-growth/w/accounts/cg-account%2F..');
});

test('account view remains available beside the new production/operating faces without implicit connection', () => {
  for (const view of ['accounts', 'production', 'operating']) assert.equal(cgEntry(new URL(contentHref('w', {view}), 'https://x.invalid').searchParams).view, view);
});
