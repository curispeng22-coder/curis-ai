import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { safeReturnPath } from "../lib/auth.mjs";

const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("shared Workspace API redirects a browser 401 to login with its return path", async () => {
  const api = await read("../lib/api.js");

  assert.match(api, /response\.status === 401/);
  assert.ok(api.includes("window.location.replace(`/login?next="));
  assert.match(api, /credentials: "include"/);
});

test("return paths cannot escape the Curis origin", () => {
  const origin = "http://127.0.0.1:3001";

  assert.equal(
    safeReturnPath("/ceo-office/projects?view=active#tasks", origin),
    "/ceo-office/projects?view=active#tasks"
  );
  for (const unsafe of [
    "https://evil.example/path",
    "//evil.example/path",
    "/\t/evil.example",
    "/\r\nLocation:https://evil.example",
    String.raw`/\evil.example`,
  ]) {
    assert.equal(safeReturnPath(unsafe, origin), "/ceo-office");
  }
});

test("local frontend proxies API traffic through the trusted gateway", async () => {
  const [config, startup, gateway] = await Promise.all([
    read("../next.config.js"),
    read("../../deploy/curis/start-local.sh"),
    read("../../deploy/curis/gateway/envoy.yaml.template"),
  ]);

  assert.match(config, /source: "\/gateway\/:path\*"/);
  assert.match(config, /destination: "http:\/\/127\.0\.0\.1:8080\/:path\*"/);
  assert.match(startup, /NEXT_PUBLIC_API_BASE=\/gateway/);
  assert.match(startup, /CURIS_LOCAL_OWNER_ENABLED=1/);
  assert.match(startup, /CURIS_LOCAL_GOOGLE_OIDC_ENABLED=0/);
  assert.match(gateway, /prefix: "\/api\/auth\/local\/"/);
});

test("login and onboarding preserve the safe user journey", async () => {
  const [login, onboarding] = await Promise.all([
    read("../app/login/page.js"),
    read("../app/onboarding/page.js"),
  ]);

  assert.match(login, /api\/auth\/local\/status/);
  assert.match(login, /api\/auth\/local\/\$\{action\}/);
  assert.match(login, /创建本地 Owner/);
  assert.doesNotMatch(login, /auth\/google|使用 Google 登录/);
  assert.match(login, /登录 Curis/);
  assert.match(onboarding, /个人 Workspace 已确认/);
  assert.match(onboarding, /getCompanies/);
  assert.match(onboarding, /createCompany/);
  assert.match(onboarding, /updateCompany/);
  assert.match(onboarding, /window\.location\.replace\(nextPath\)/);
});
