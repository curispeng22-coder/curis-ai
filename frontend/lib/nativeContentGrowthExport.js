// Dedicated S2/D4 bridge. The legacy payload has no company/tenant claims.
const TYPE = "curis.cg.local-verification-export/1";
const NOTICE = "本地核验导出，不构成发布；平台连接不存在。";
const FIELDS = ["verification_ref", "title", "body", "format", "platform", "account", "checks", "connection_status", "verification", "source"];
const equal = (a, b) => {
  if (a === b) return true;
  if (!a || !b || typeof a !== "object" || typeof b !== "object" || Array.isArray(a) !== Array.isArray(b)) return false;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every(key => Object.hasOwn(b, key) && equal(a[key], b[key]));
};
export function cgExportSelection(record, company, business) {
  const data = record?.data;
  if (!company || !business || record?.company_id !== company || data?.business_ref !== business
    || !record?.entity_id?.startsWith("cg-verify-") || record.entity_id.length > 256
    || data.objectType !== "PublishVerification" || data.verification !== "UNVERIFIED"
    || data.source !== "CEO_MANUAL" || data.connection_status !== "NOT_CONNECTED") {
    throw new Error("核验范围已变化，请重新选择原记录。");
  }
  return { verification_ref: record.entity_id, title: data.content_title, body: data.content_body,
    format: data.content_format, platform: { ref: data.platform_ref, name: data.platform_name },
    account: { ref: data.account_ref, name: data.account_name }, checks: structuredClone(data.checks),
    connection_status: data.connection_status, verification: data.verification, source: data.source };
}
export async function saveNativeContentGrowthExport(blob, selection, bridge = globalThis.window?.__TAURI_INTERNALS__, isCurrent = () => true) {
  const current = () => { if (!isCurrent()) throw new Error("核验记录已切换，请回到原记录核对保存结果。"); };
  const expected = structuredClone(selection);
  current();
  if (!bridge?.invoke) throw new Error("本机保存暂不可用，原核验记录已保留。");
  const buffer = await blob.arrayBuffer();
  current();
  if (!buffer.byteLength || buffer.byteLength > 2 * 1024 * 1024) throw new Error("核验导出文件为空或超过允许大小。");
  let payload;
  try { payload = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(buffer)); }
  catch { throw new Error("核验导出不是有效 JSON，原记录已保留。"); }
  if (!payload || Array.isArray(payload) || Object.keys(payload).length !== FIELDS.length + 3
    || !FIELDS.every(key => Object.hasOwn(payload, key) && equal(payload[key], expected[key]))
    || payload.package_type !== TYPE || payload.notice !== NOTICE
    || payload.verification !== "UNVERIFIED" || payload.source !== "CEO_MANUAL" || payload.connection_status !== "NOT_CONNECTED"
    || typeof payload.exported_at !== "string" || !payload.exported_at || payload.exported_at.length > 128) {
    throw new Error("导出内容与当前核验记录不一致，没有打开保存窗口。");
  }
  current();
  let outcome;
  try { outcome = await bridge.invoke("save_cg_local_verification", { bytes: Array.from(new Uint8Array(buffer)), selection: expected }); }
  catch (reason) {
    // Neither native strings nor arbitrary error objects are safe to display.
    const codes = ["NSV_ORIGIN", "NSV_PACKAGE", "NSV_BUSY", "NSV_UNSUPPORTED", "NSV_DISPATCH", "NSV_MAIN", "NSV_DIRECTORY", "NSV_PANEL", "NSV_SELECTION", "NSV_WRITE"];
    const code = codes.includes(reason?.code) ? reason.code : "NSV_UNKNOWN";
    throw new Error(`文件保存未完成，原核验记录已保留。支持码：${code}`);
  }
  current();
  if (outcome?.status === "CANCELLED" && outcome.verified === false && outcome.bytes === 0 && outcome.path === null) return outcome;
  if (outcome?.status !== "SAVED" || outcome.verified !== true || outcome.bytes !== buffer.byteLength
    || typeof outcome.path !== "string" || !outcome.path.startsWith("/")) {
    throw new Error("文件保存尚未核验完成，请核对原保存结果。");
  }
  return outcome;
}
