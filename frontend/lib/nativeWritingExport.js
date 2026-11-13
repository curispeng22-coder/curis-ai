// Narrow bridge for the pinned Tauri desktop runtime; never a generic file writer.
const NATIVE_CODES = new Set(["NSV_ORIGIN", "NSV_PACKAGE", "NSV_BUSY", "NSV_UNSUPPORTED", "NSV_DISPATCH", "NSV_MAIN", "NSV_DIRECTORY", "NSV_PANEL", "NSV_SELECTION", "NSV_WRITE", "NSV_READBACK", "NSV_RESULT"]);
const STAGES = new Set(["FETCH_BEGIN", "BYTES_RECEIVED", "READ_BYTES", "PACKAGE_VERIFIED", "INVOKE_BEGIN", "IPC_REJECTED", "COMMAND_ENTRY", "ORIGIN", "PACKAGE", "LOCK", "DISPATCH", "MAIN_ENTER", "DIRECTORY", "PANEL_CONFIGURED", "PANEL_PRESENT", "PANEL_RETURN", "SELECTION", "WRITE", "READBACK", "RESULT"]);

export function writingSaveDiagnostic(reason, stage = "IPC_REJECTED") {
  const errorType = reason instanceof Error ? "Error" : typeof reason;
  const message = typeof reason === "string" ? reason : reason instanceof Error ? reason.message : "";
  let code = "NSV_UNKNOWN", errorClass = "UNKNOWN";
  if (message.includes("Command save_writing_local_package not allowed by ACL")) { code = "NSV_IPC_ACL"; errorClass = "ACL_DENIED"; }
  else if (/invalid args|invalid type|missing required key|deserialize/i.test(message)) { code = "NSV_IPC_ARGUMENT"; errorClass = "ARGUMENT_INVALID"; }
  else if (reason && typeof reason === "object" && NATIVE_CODES.has(reason.code)) {
    code = reason.code; stage = STAGES.has(reason.stage) ? reason.stage : stage;
    errorClass = code.slice(4);
  } else if (stage === "READ_BYTES" || stage === "PACKAGE_VERIFIED" || stage === "PACKAGE") { code = "NSV_PACKAGE"; errorClass = "PACKAGE_VALIDATION"; }
  return { version: 1, stage: STAGES.has(stage) ? stage : "IPC_REJECTED", code, errorType,
    errorClass, sanitizedSummary: code === "NSV_IPC_ACL" ? "单一保存命令未获IPC许可" : code === "NSV_IPC_ARGUMENT" ? "保存参数无法解析" : "保存未完成；原内容与路径未记录" };
}

export function writingSaveFailureMessage(reason, stage = "IPC_REJECTED") {
  const candidate = reason?.diagnostic;
  const diagnostic = candidate && /^(NSV_[A-Z_]+)$/.test(candidate.code) && ["NSV_UNKNOWN", "NSV_IPC_ACL", "NSV_IPC_ARGUMENT", ...NATIVE_CODES].includes(candidate.code) ? candidate : writingSaveDiagnostic(reason, stage);
  return `文件保存未完成，请保留原包。支持码：${diagnostic.code}`;
}

export async function saveNativeWritingPackage(blob, prepared, scope, bridge = globalThis.window?.__TAURI_INTERNALS__, isCurrent = () => true) {
  if (!bridge?.invoke) return { status: "UNSUPPORTED", verified: false };
  let stage = "READ_BYTES";
  try {
  if (!isCurrent()) throw new Error("原发布包已切换，没有开始保存。");
  const buffer = await blob.arrayBuffer();
  if (!buffer.byteLength || buffer.byteLength > 2 * 1024 * 1024) throw new Error("发布包文件为空或超过允许大小。");
  stage = "PACKAGE";
  const digest = Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256", buffer)), value => value.toString(16).padStart(2, "0")).join("");
  if (digest !== prepared.content_sha256) throw new Error("下载的发布包摘要与原记录不一致。");
  const payload = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(buffer));
  const actual = payload.scope;
  const fields = ["tenant_id", "company_id", "workspace_id", "instance_id", "book_ref", "chapter_ref", "package_id", "package_version", "package_digest"];
  if (payload.schema_version !== "writing.local-package/v1" || payload.metadata?.target !== "LOCAL_DOWNLOAD"
    || payload.package_ref !== prepared.ref || payload.formal_ref !== prepared.formal_ref
    || payload.external_publication !== "NOT_PUBLISHED" || fields.some(field => !scope[field] || actual?.[field] !== scope[field])) {
    throw new Error("发布包与当前作品、章节或正式稿来源不一致。");
  }
  if (!isCurrent()) throw new Error("原发布包已切换，没有打开保存窗口。");
  stage = "PACKAGE_VERIFIED";
  console.info("WRITING_SAVE_DIAGNOSTIC", JSON.stringify({version:1,stage,code:"NSV_STAGE",errorType:"none",errorClass:"STAGE",sanitizedSummary:"下载包校验已到达"}));
  stage = "INVOKE_BEGIN";
  console.info("WRITING_SAVE_DIAGNOSTIC", JSON.stringify({version:1,stage,code:"NSV_STAGE",errorType:"none",errorClass:"STAGE",sanitizedSummary:"已提交单一保存调用"}));
  const outcome = await bridge.invoke("save_writing_local_package", { bytes: Array.from(new Uint8Array(buffer)), scope: actual, packageRef: prepared.ref, formalRef: prepared.formal_ref });
  if (outcome?.status === "CANCELLED") return outcome;
  if (outcome?.status !== "SAVED" || outcome.verified !== true || outcome.bytes !== buffer.byteLength || !outcome.path) {
    throw new Error("文件保存尚未核验完成，请核对原保存结果。");
  }
  return { ...outcome, sha256: digest };
  } catch (reason) {
    const diagnostic = writingSaveDiagnostic(reason, stage);
    // Only the whitelist is retained; rejected strings/objects can contain private paths or payloads.
    console.warn("WRITING_SAVE_DIAGNOSTIC", JSON.stringify(diagnostic));
    const error = new Error(writingSaveFailureMessage({ diagnostic }));
    error.name = "WritingSaveError"; error.diagnostic = diagnostic; throw error;
  }
}
