import { businessReturnInput } from "./businessReturnApi.js";

export const SETTINGS_CATEGORIES = Object.freeze([
  ["personal", "个人与外观", "i-person"], ["company", "公司默认值", "i-business"],
  ["models", "模型与 AI 提供方", "i-auto_awesome"], ["security", "权限与安全", "i-verified"],
  ["data", "应用与数据", "i-widgets"], ["help", "账户与帮助", "i-info"],
]);
export const PRESENTATION_CHANGED = "curis.presentation.changed";
export const THEME_CHANGED = "curis.theme.changed";
const ROOTS = new Set(["/ceo-office", "/ceo-office/business", "/ceo-office/organization", "/ceo-office/talent-market", "/ceo-office/analytics", "/ceo-office/knowledge", "/ceo-office/meeting"]);
export const settingsCategory = (value) => SETTINGS_CATEGORIES.some(([key]) => key === value) ? value : "personal";
export const themeValue = (value) => ["system", "light", "dark"].includes(value) ? value : "system";

export function applySettingsTheme(value, host = window) {
  const next = themeValue(value);
  host.document.documentElement.dataset.theme = next;
  try { host.localStorage.setItem("curis.theme", next); } catch { /* The active choice still applies. */ }
  host.dispatchEvent(new Event(THEME_CHANGED));
  return next;
}

function localArea(value) {
  if (typeof value !== "string" || value.length > 8192 || /[\x00-\x20\\#]/u.test(value)) return null;
  const path = value.split("?")[0];
  return ROOTS.has(path) ? value : null;
}

export function settingsReturn(params) {
  const business = businessReturnInput(params);
  const areas = params.getAll("settings_from");
  if (areas.length > 1 || business && areas.length || areas.length && !localArea(areas[0])) throw new Error("无法确认原页面，请从业务入口重新进入。");
  return business ? { business } : areas.length ? { href: areas[0], label: "返回原页面" } : null;
}

// Route metadata only locates the original work; the page must still authorize it.
export function captureSettingsHref(pathname, search = "") {
  const href = pathname + (search ? search.startsWith("?") ? search : "?" + search : "");
  const result = new URLSearchParams();
  if (localArea(href)) result.set("settings_from", href);
  else if (pathname.startsWith("/ceo-office/workspace/installed/")) {
    for (const kind of ["cg", "music", "writing"]) {
      const candidate = new URLSearchParams({ return_kind: kind, return_to: href });
      try { businessReturnInput(candidate); result.set("return_kind", kind); result.set("return_to", href); break; } catch { /* Try the next bounded domain parser. */ }
    }
  }
  return "/ceo-office/settings" + (result.size ? "?" + result : "");
}

export function settingsModelHref(params, { returning = false } = {}) {
  const result = new URLSearchParams({ settings_entry: "models" });
  if (returning) result.set("tab", "models");
  const target = settingsReturn(params);
  if (target?.business) { result.set("return_kind", target.business.kind); result.set("return_to", target.business.value); }
  if (target?.href) result.set("settings_from", target.href);
  return (returning ? "/ceo-office/settings" : "/ceo-office/capabilities") + "?" + result;
}

export function settingsEntryIdentity(params) {
  const target = settingsReturn(params);
  return JSON.stringify(target?.business || target?.href || "direct");
}

export function presentationSubmission(saved, draft) {
  if (typeof saved?.welcome_dismissed !== "boolean" || typeof saved?.avatar_ref !== "string"
    || typeof draft?.display_name !== "string" || typeof draft?.avatar_ref !== "string") throw new Error("个人资料尚未完整读取，请重新读取后保存。");
  const name = draft.display_name.trim(), avatar = draft.avatar_ref;
  if (name.length > 80 || /[\x00-\x1f\x7f]/u.test(name)) throw new Error("显示名称不能超过 80 个字符或包含控制字符。");
  if (avatar.length > 260000 || avatar && !avatar.startsWith("preset:") && !/^data:image\/(png|jpeg|webp);base64,/u.test(avatar)) throw new Error("请选择本地头像或已有头像。");
  return { welcome_dismissed: saved.welcome_dismissed, display_name: name, avatar_ref: avatar };
}

export const samePresentationDraft = (a, b) => a?.display_name === b?.display_name && a?.avatar_ref === b?.avatar_ref;
export const savedPresentationDraft = (current, submittedDraft, saved) => samePresentationDraft(current, submittedDraft) ? saved : current;
export const settingsDraftKey = (tenant, actor, company, entry) => "curis.settings.draft." + JSON.stringify([tenant, actor, company || "PRE_COMPANY", entry]);
export function readSettingsDraft(storage, key) {
  try {
    const raw = storage.getItem(key);
    if (!raw || raw.length > 270000) return null;
    const draft = JSON.parse(raw);
    presentationSubmission({ welcome_dismissed: false, avatar_ref: "" }, draft);
    return { display_name: draft.display_name, avatar_ref: draft.avatar_ref };
  } catch { return null; }
}

export async function readSettingsModels({ readProviders, readPreference, isCurrent }) {
  try {
    const [providers, preference] = await Promise.all([readProviders(), readPreference()]);
    if (!isCurrent()) return null;
    if (!Array.isArray(providers?.providers)) throw new Error("invalid provider metadata");
    return { status: "ready", configured: providers.providers.filter((item) => item.configured === true).length,
      defaultName: typeof preference?.preference?.model_name === "string" ? preference.preference.model_name : "" };
  } catch { return isCurrent() ? { status: "error" } : null; }
}
