import test from "node:test";
import assert from "node:assert/strict";
import { nativeRecovery, recoveryError } from "../lib/nativeBackup.js";

test("only the five narrow commands reach the native bridge and no path argument crosses IPC", async () => {
  const calls = [];
  const bridge = { invoke: async (command, args) => { calls.push({ command, args }); return { status: "PREFLIGHT_OK", archiveSha256: "a".repeat(64), confirmationId: "b".repeat(64) }; } };
  const result = await nativeRecovery("preflight_curis_restore", {}, bridge);
  assert.equal(result.status, "PREFLIGHT_OK");
  assert.deepEqual(calls, [{ command: "preflight_curis_restore", args: {} }]);
  await assert.rejects(nativeRecovery("preflight_curis_restore", { path: "/tmp/private" }, bridge), TypeError);
  await assert.rejects(nativeRecovery("restore_everything", {}, bridge), TypeError);
  assert.equal(calls.length, 1);
});

test("verified destination and bounded preflight facts return only as current-user result data", async () => {
  const destination = "/private/tmp/selected-by-user.curis.zip";
  const backup = await nativeRecovery("create_curis_backup", {}, {
    invoke: async () => ({ status: "BACKUP_VERIFIED", localDestination: destination, archiveSha256: "a".repeat(64) }),
  });
  assert.equal(backup.localDestination, destination);
  const preview = await nativeRecovery("preflight_curis_restore", {}, {
    invoke: async () => ({ status: "PREFLIGHT_OK", identity: [{ company_id: "company-1" }],
      targetIdentity: [{ company_id: "company-1" }], createdAt: "2026-10-15T00:00:00+00:00",
      appVersion: "0.1.0", schemaVersion: 7, backupProtocol: 2,
      compatibility: { sameRoot: "MATCHED", company: "MATCHED", appVersion: "MATCHED", schema: "MATCHED" } }),
  });
  assert.equal(preview.identity[0].company_id, "company-1");
  assert.equal(preview.compatibility.schema, "MATCHED");
  assert.equal(preview.createdAt, "2026-10-15T00:00:00+00:00");
});

test("commit accepts only a fixed-size confirmation and native failure never reveals paths or secrets", async () => {
  const calls = [];
  const bridge = { invoke: async (command, args) => { calls.push([command, args]); throw new Error("/private/root token=secret original error"); } };
  const id = "c".repeat(64);
  const result = await nativeRecovery("commit_curis_restore", { confirmationId: id }, bridge);
  assert.equal(result.status, "FAILED");
  assert.equal(result.code, "NATIVE_FAILURE");
  assert.doesNotMatch(JSON.stringify(result), /private|secret/);
  assert.deepEqual(calls, [["commit_curis_restore", { confirmationId: id }]]);
  await assert.rejects(nativeRecovery("commit_curis_restore", { confirmationId: id, archive: "x" }, bridge), TypeError);
  assert.equal(recoveryError("Command commit_curis_restore not allowed by ACL").code, "ACL_DENIED");
});

test("browser-only environment is honestly unsupported", async () => {
  assert.deepEqual(await nativeRecovery("create_curis_backup", {}, null), { status: "UNSUPPORTED", code: "NATIVE_UNAVAILABLE" });
});

test("recovery hold remains visible without exposing a local file path", async () => {
  const result = await nativeRecovery("read_curis_recovery_status", {}, {
    invoke: async () => ({ status: "RECOVERY_HOLD", nextAction: "VERIFY_PENDING_EFFECTS" }),
  });
  assert.deepEqual(result, { status: "RECOVERY_HOLD", nextAction: "VERIFY_PENDING_EFFECTS" });
});

test("a known damaged local root keeps the native backup chooser available", async () => {
  const result = await nativeRecovery("read_curis_recovery_status", {}, {
    invoke: async () => ({ status: "RECOVERY_REQUIRED", currentMode: "DAMAGED_DB", nextAction: "CHOOSE_VERIFIED_BACKUP" }),
  });
  assert.equal(result.status, "RECOVERY_REQUIRED");
  assert.equal(result.nextAction, "CHOOSE_VERIFIED_BACKUP");
});
