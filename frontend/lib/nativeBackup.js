// Narrow main-window bridge. Only a verified, user-selected destination may return
// to this window for display; paths never enter diagnostics or generic JS writes.
const COMMANDS = new Set([
  "create_curis_backup", "preflight_curis_restore", "commit_curis_restore",
  "cancel_curis_restore", "read_curis_recovery_status",
]);

export function recoveryError(error) {
  const message = typeof error === "string" ? error : error instanceof Error ? error.message : "";
  const code = /not allowed by ACL/i.test(message) ? "ACL_DENIED"
    : /invalid args|deserialize|missing required key/i.test(message) ? "ARGUMENT_INVALID"
    : "NATIVE_FAILURE";
  return { status: "FAILED", code, message: "本机数据操作未完成；请保留当前数据并查看恢复状态。" };
}

export async function nativeRecovery(command, args = {}, bridge = globalThis.window?.__TAURI_INTERNALS__) {
  if (!COMMANDS.has(command)) throw new TypeError("unsupported recovery command");
  if (!bridge?.invoke) return { status: "UNSUPPORTED", code: "NATIVE_UNAVAILABLE" };
  if (command !== "commit_curis_restore" && Object.keys(args).length) throw new TypeError("unexpected recovery arguments");
  if (command === "commit_curis_restore" &&
    (Object.keys(args).length !== 1 || !/^[0-9a-f]{64}$/.test(args.confirmationId || ""))) {
    throw new TypeError("invalid recovery confirmation");
  }
  try {
    const result = await bridge.invoke(command, args);
    const valid = new Set(["BACKUP_VERIFIED", "PREFLIGHT_OK", "RESTORED", "RECOVERY_HOLD", "RECOVERY_REQUIRED", "CANCELLED", "READY", "NO_PENDING_RECOVERY", "ROLLED_BACK", "UNKNOWN"]);
    return result && typeof result === "object" && valid.has(result.status) ? result
      : { status: "FAILED", code: "NATIVE_RESULT_INVALID", message: "本机回证尚未核验。" };
  } catch (error) {
    return recoveryError(error);
  }
}
