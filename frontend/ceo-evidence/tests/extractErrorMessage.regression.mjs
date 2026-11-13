/**
 * Regression test for the FastAPI error-message handling fix.
 *
 * This test extracts the REAL `extractErrorMessage` and `fetchJson` functions
 * from `src/api/index.ts` (so it stays a genuine regression test of the
 * production source, not a re-implementation) by transpiling the slice with
 * esbuild (already available via Vite) and importing it as an ES module.
 *
 * Run with:  node tests/extractErrorMessage.regression.mjs
 *
 * Covers the original bug: FastAPI 422 validation errors were rendered as
 * "[object Object],[object Object]" in the Dashboard Alert. The fix must
 * produce human-readable text for every FastAPI error shape:
 *   - string detail                    -> { "detail": "not found" }
 *   - array of validation errors       -> { "detail": [ { loc, msg }, ... ] }
 *   - nested object detail             -> { "detail": { "message": "..." } }
 *   - HTTP status fallback             -> non-JSON / unreadable body
 */

import { transformSync } from 'esbuild'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const indexPath = join(__dirname, '..', 'src', 'api', 'index.ts')
const source = readFileSync(indexPath, 'utf8')

// Extract the slice from `function extractErrorMessage` up to the next top-level
// section comment (which follows `fetchJson`). This slice contains both functions.
const start = source.indexOf('function extractErrorMessage')
const end = source.indexOf('// ── Existing CEO Evidence Types')
if (start === -1) throw new Error('Could not locate extractErrorMessage in src/api/index.ts')
if (end === -1) throw new Error('Could not locate end boundary in src/api/index.ts')
const slice = source.slice(start, end)

const { code } = transformSync(slice, { loader: 'ts', format: 'esm' })
// esbuild's `transform` strips TypeScript but does NOT auto-export declarations,
// so we append an explicit export of the two functions we want to exercise.
const exportTail = '\nexport { extractErrorMessage, fetchJson };\n'
const moduleUrl = 'data:text/javascript;base64,' + Buffer.from(code + exportTail).toString('base64')
const mod = await import(moduleUrl)
const { extractErrorMessage, fetchJson } = mod

// ── Tiny test harness ──
let passed = 0
let failed = 0
const failures = []

function assert(cond, name, detail) {
  if (cond) {
    passed++
    console.log(`  ✓ ${name}`)
  } else {
    failed++
    failures.push(`${name} — ${detail}`)
    console.log(`  ✗ ${name}\n      ${detail}`)
  }
}

function noObjectObject(text) {
  return typeof text === 'string' && !text.includes('[object Object]')
}

function isHumanReadable(text) {
  return typeof text === 'string' && text.trim().length > 0
}

console.log('\n# extractErrorMessage — unit regression\n')

// 1. Plain string detail is returned verbatim.
{
  const out = extractErrorMessage('Resource not found')
  assert(out === 'Resource not found' && noObjectObject(out) && isHumanReadable(out),
    'string detail returned verbatim', `got: ${JSON.stringify(out)}`)
}

// 2. CORE BUG: FastAPI 422 validation array -> readable "field: msg; field: msg".
{
  const detail = [
    { loc: ['body', 'company_id'], msg: 'field required' },
    { loc: ['body', 'goal'], msg: 'field required' },
  ]
  const out = extractErrorMessage(detail)
  const ok = out === 'company_id: field required; goal: field required'
  assert(ok && noObjectObject(out) && isHumanReadable(out),
    '422 validation array -> "company_id: field required; goal: field required"',
    `got: ${JSON.stringify(out)}`)
}

// 3. Nested loc path is joined with dots, body/query/path prefixes dropped.
{
  const detail = [{ loc: ['body', 'items', '0', 'name'], msg: 'field required' }]
  const out = extractErrorMessage(detail)
  assert(out === 'items.0.name: field required' && noObjectObject(out),
    'nested loc path joined with dots', `got: ${JSON.stringify(out)}`)
}

// 4. Array items that are bare strings are joined directly.
{
  const detail = ['first error', 'second error']
  const out = extractErrorMessage(detail)
  assert(out === 'first error; second error' && noObjectObject(out),
    'string array items joined', `got: ${JSON.stringify(out)}`)
}

// 5. Nested object with `message` field.
{
  const out = extractErrorMessage({ message: 'Validation pipeline broke' })
  assert(out === 'Validation pipeline broke' && noObjectObject(out),
    'nested object with message', `got: ${JSON.stringify(out)}`)
}

// 6. Nested object with `error` field.
{
  const out = extractErrorMessage({ error: 'boom' })
  assert(out === 'boom' && noObjectObject(out),
    'nested object with error', `got: ${JSON.stringify(out)}`)
}

// 7. Nested object whose `detail` is itself a validation array -> recurses.
{
  const out = extractErrorMessage({ detail: [{ loc: ['body', 'goal'], msg: 'field required' }] })
  assert(out === 'goal: field required' && noObjectObject(out),
    'nested object detail array recurses', `got: ${JSON.stringify(out)}`)
}

// 8. Plain nested object without message/error/detail -> JSON.stringify fallback.
{
  const out = extractErrorMessage({ code: 42, reason: 'weird' })
  assert(out === '{"code":42,"reason":"weird"}' && noObjectObject(out) && isHumanReadable(out),
    'unknown object -> JSON.stringify fallback', `got: ${JSON.stringify(out)}`)
}

// 9. null -> empty string (signals fetchJson to keep its HTTP status fallback).
assert(extractErrorMessage(null) === '', 'null -> empty string',
  `got: ${JSON.stringify(extractErrorMessage(null))}`)

// 10. undefined -> empty string.
assert(extractErrorMessage(undefined) === '', 'undefined -> empty string',
  `got: ${JSON.stringify(extractErrorMessage(undefined))}`)

console.log('\n# fetchJson — integration regression (mocked fetch)\n')

// Helper: install a mock global fetch returning a Response-like object.
function withMockFetch(handler, fn) {
  const original = globalThis.fetch
  globalThis.fetch = handler
  return fn().finally(() => { globalThis.fetch = original })
}

// 11. 422 validation array body -> Error message is readable (no [object Object]).
await withMockFetch(
  async () => ({
    ok: false,
    status: 422,
    statusText: 'Unprocessable Entity',
    json: async () => ([
      { loc: ['body', 'company_id'], msg: 'field required' },
      { loc: ['body', 'goal'], msg: 'field required' },
    ]),
  }),
  async () => {
    let msg = '(no throw)'
    try { await fetchJson('/api/workspace/projects', { method: 'POST', body: '{}' }) }
    catch (e) { msg = e.message }
    assert(msg === 'company_id: field required; goal: field required' && noObjectObject(msg),
      'fetchJson 422 validation array -> readable Error', `got: ${JSON.stringify(msg)}`)
  },
)

// 12. 500 with non-JSON body -> HTTP status fallback text.
await withMockFetch(
  async () => ({
    ok: false,
    status: 500,
    statusText: 'Internal Server Error',
    json: async () => { throw new Error('not json') },
  }),
  async () => {
    let msg = '(no throw)'
    try { await fetchJson('/api/x') }
    catch (e) { msg = e.message }
    assert(msg === 'HTTP 500: Internal Server Error' && noObjectObject(msg) && isHumanReadable(msg),
      'fetchJson 500 non-JSON body -> HTTP status fallback', `got: ${JSON.stringify(msg)}`)
  },
)

// 13. 200 OK -> returns parsed JSON (no throw).
await withMockFetch(
  async () => ({ ok: true, status: 200, statusText: 'OK', json: async () => ({ ok: true }) }),
  async () => {
    let result = null
    let threw = false
    try { result = await fetchJson('/api/x') } catch { threw = true }
    assert(!threw && result && result.ok === true,
      'fetchJson 200 OK -> returns parsed body', `threw=${threw} result=${JSON.stringify(result)}`)
  },
)

// 14. 422 nested object { message } -> readable Error.
await withMockFetch(
  async () => ({
    ok: false,
    status: 422,
    statusText: 'Unprocessable Entity',
    json: async () => ({ message: 'Project goal must not be empty' }),
  }),
  async () => {
    let msg = '(no throw)'
    try { await fetchJson('/api/workspace/projects', { method: 'POST', body: '{}' }) }
    catch (e) { msg = e.message }
    assert(msg === 'Project goal must not be empty' && noObjectObject(msg),
      'fetchJson 422 nested message -> readable Error', `got: ${JSON.stringify(msg)}`)
  },
)

// ── Summary ──
console.log(`\n# Result: ${passed} passed, ${failed} failed\n`)
if (failed > 0) {
  console.log('Failures:')
  for (const f of failures) console.log('  - ' + f)
  process.exit(1)
}
console.log('All regression tests passed ✓')
process.exit(0)
