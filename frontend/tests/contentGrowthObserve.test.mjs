import test from 'node:test';
import assert from 'node:assert/strict';
import { cgEntry, contentHref } from '../lib/contentGrowthState.mjs';
import { createContentGrowthApi } from '../lib/contentGrowthApi.js';

test('cg_view=observe is whitelisted and encoded; unknown views still fail closed', () => {
  const params = (q) => new URLSearchParams(q);
  assert.equal(cgEntry(params('cg_view=observe')).view, 'observe');
  assert.ok(cgEntry(params('cg_view=Observe')).error, 'case-sensitive whitelist');
  assert.ok(cgEntry(params('cg_view=analytics')).error, 'no analytics wording in routes');
  const href = contentHref('workspace', { view: 'observe' });
  assert.ok(href.includes('cg_view=observe'), href);
  assert.equal(cgEntry(new URL(href, 'https://x.invalid').searchParams).view, 'observe');
  assert.equal(cgEntry(params('cg_view=observe&cg_version=v')).error !== undefined, true);
});

test('receipt and observation api wrappers: routes, methods and payloads', async () => {
  const calls = [];
  const request = async (url, options) => { calls.push({ url, options }); return { ok: true }; };
  const api = createContentGrowthApi(request);
  await api.receipts('c1', 'w1', 'cg-verify-a');
  await api.receiptCreate('c1', 'w1', 'cg-verify-a', 'req-1', { published_at: '', platform_post_url: 'https://x/p', note: '' });
  await api.receipt('c1', 'w1', 'cg-receipt-a');
  await api.observations('c1', 'w1');
  await api.observationCreate('c1', 'w1', 'req-2', { title: '首周', body: '正文', scope_ref: 'cg-account-a', period: '第一周' });
  await api.observation('c1', 'w1', 'cg-obs-a');
  const base = '/api/workspace/v1/companies/c1/content-growth/w1';
  assert.deepEqual(calls.map((c) => c.url), [
    `${base}/verifications/cg-verify-a/receipts`,
    `${base}/verifications/cg-verify-a/receipts`,
    `${base}/receipts/cg-receipt-a`,
    `${base}/observations`,
    `${base}/observations`,
    `${base}/observations/cg-obs-a`,
  ]);
  assert.deepEqual(calls.map((c) => c.options?.method || 'GET'), ['GET', 'POST', 'GET', 'GET', 'POST', 'GET']);
  const receiptBody = JSON.parse(calls[1].options.body);
  assert.equal(receiptBody.request_id, 'req-1');
  assert.equal(receiptBody.data.platform_post_url, 'https://x/p');
  const obsBody = JSON.parse(calls[4].options.body);
  assert.equal(obsBody.request_id, 'req-2');
  assert.equal(obsBody.data.scope_ref, 'cg-account-a');
  assert.equal(obsBody.data.period, '第一周');
});

test('receipt/observation route ids are percent-encoded', async () => {
  const calls = [];
  const api = createContentGrowthApi(async (url) => { calls.push(url); return {}; });
  await api.receipts('c', 'w', 'cg verify');
  await api.receipt('c', 'w', 'cg-receipt/..');
  await api.observation('c', 'w', 'cg-obs/..');
  assert.equal(calls[0], '/api/workspace/v1/companies/c/content-growth/w/verifications/cg%20verify/receipts');
  assert.equal(calls[1], '/api/workspace/v1/companies/c/content-growth/w/receipts/cg-receipt%2F..');
  assert.equal(calls[2], '/api/workspace/v1/companies/c/content-growth/w/observations/cg-obs%2F..');
});

test('analysis face does not widen observable actions into real platform analytics', () => {
  assert.equal(cgEntry(new URLSearchParams('cg_view=analysis')).view, 'analysis');
  assert.ok(cgEntry(new URLSearchParams('cg_view=live-analytics')).error);
});
