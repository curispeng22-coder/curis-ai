import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

import {
  createInstalledWorkspaceObject,
  getInstalledWorkspace,
  getInstalledWorkspaceNavigation,
  operateInstalledWorkspaceObject,
  resolveInstalledWorkspaceCompanyIntegration,
} from "../lib/workspacePackageApi.js";


const read = (path) => readFile(new URL(path, import.meta.url), "utf8");

test("Package API stays generic and the existing Shell renders all declared panes", async () => {
  const calls = [];
  const request = async (path, options) => { calls.push({ path, options }); return { items: [] }; };
  await getInstalledWorkspaceNavigation("company/一", request);
  await getInstalledWorkspace("workspace/一", request);
  await createInstalledWorkspaceObject("workspace/一", "core.domain-object.create", { ceo_id: "ceo", object_type: "Feedback", data: {} }, request);
  await operateInstalledWorkspaceObject("workspace/一", "object/一", { ceo_id: "ceo", responsibility_type: "FEEDBACK_TRIAGE" }, request);
  await resolveInstalledWorkspaceCompanyIntegration("workspace/一", "object/一", request);
  assert.deepEqual(calls.map((item) => item.path), [
    "/api/workspace/packages/navigation?company_id=company%2F%E4%B8%80",
    "/api/workspace/packages/workspaces/workspace%2F%E4%B8%80",
    "/api/workspace/packages/workspaces/workspace%2F%E4%B8%80/actions/core.domain-object.create",
    "/api/workspace/packages/workspaces/workspace%2F%E4%B8%80/objects/object%2F%E4%B8%80/company-operate",
    "/api/workspace/packages/workspaces/workspace%2F%E4%B8%80/objects/object%2F%E4%B8%80/company-integration",
  ]);
  assert.equal(calls[2].options.method, "POST");
  assert.equal(calls[3].options.method, "POST");

  const [sidebar, renderer, route] = await Promise.all([
    read("../components/terra/TerraSidebar.js"),
    read("../components/workspace/InstalledWorkspaceRuntime.js"),
    read("../app/ceo-office/workspace/installed/[workspaceId]/page.js"),
  ]);
  assert.match(sidebar, /getInstalledWorkspaceNavigation/);
  assert.match(sidebar, /installedWorkspaces\.map/);
  assert.match(route, /InstalledWorkspaceRuntime/);
  assert.match(renderer, /WorkspacePaneShell/);
  for (const contract of ["object-list", "object-detail", "object-create-form", "contextPane", "utilityPane", "createInstalledWorkspaceObject"]) {
    assert.match(renderer, new RegExp(contract));
  }
  assert.match(renderer, /detail\?\.surfaces\?\.utility\?\.objectType/);
  assert.match(renderer, /Company OS Integration/);
  assert.match(renderer, /Core refs resolved/);
  for (const contract of [
    "curis.workspace-package/v2",
    "Workspace Domain Navigation",
    "Professional Surface",
    "workspace-work-list",
    "workspace-result-list",
    "workspace-evidence-list",
    "surfacePreferenceKey",
    "searchParams.get\\(\"surface\"\\)",
    "surfaceModel.defaultSurfaceRef",
    "surfaceModel.workspaceGap.key",
    "router.replace",
  ]) {
    assert.match(renderer, new RegExp(contract));
  }
  assert.match(renderer, /detail\.instance\.workspace_id/);
  assert.doesNotMatch(renderer, /surface.*workspaceId\s*=/i);
});

test("the real packaged v2 Core gap fails closed before default Surface initialization", async () => {
  const [renderer, responseText] = await Promise.all([
    read("../components/workspace/InstalledWorkspaceRuntime.js"),
    read("../../artifacts/workspace-engineering-multi-surface-package-001/packaged-workspace-api-response.json"),
  ]);
  const response = JSON.parse(responseText);
  const gap = response.surfaceModel.workspaceGap;

  assert.equal(response.package.schema_version, "curis.workspace-package/v2");
  assert.equal(gap.key, "__workspace_gap__");
  assert.equal(gap.eligible, true);
  assert.equal(gap.viewRefs, undefined);
  assert.equal(gap.projectionRefs, undefined);
  assert.match(renderer, /!Array\.isArray\(surface\?\.viewRefs\)/);
  assert.match(renderer, /!Array\.isArray\(surface\?\.projectionRefs\)/);
});
