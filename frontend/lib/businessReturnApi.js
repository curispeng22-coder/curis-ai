import { TENANT_ID, workspaceFetch } from "./api.js";
import { getInstalledWorkspace } from "./workspacePackageApi.js";
import { cgReturnTarget, isContentGrowthPackage } from "./contentGrowthState.mjs";
import { musicReturnTarget, isMusicPackage } from "./musicState.mjs";
import { isWritingPackage } from "./writingState.mjs";
import { createContentGrowthApi, validateContentGrowthReturn } from "./contentGrowthApi.js";
import { createMusicApi, validateMusicReturn } from "./musicApi.js";
import { writingReturnTarget, validateWritingReturn } from "./writingApi.js";

const parsers = { cg: cgReturnTarget, music: musicReturnTarget, writing: writingReturnTarget };
const packages = { cg: isContentGrowthPackage, music: isMusicPackage, writing: isWritingPackage };
const invalid = () => { throw new Error("无法确认原工作台，请从业务入口重新进入。"); };

export function businessReturnInput(params, { allowConversation = false } = {}) {
  const values = params.getAll("return_to"), kinds = params.getAll("return_kind");
  if (!values.length && !kinds.length) return null;
  if (values.length !== 1 || kinds.length > 1) invalid();
  const kind = kinds.length ? kinds[0] : "writing";
  if (!Object.hasOwn(parsers, kind) || params.has("company") || params.has("company_id")) invalid();
  if (allowConversation && !kinds.length && values[0].startsWith("/ceo-office/conversation?conversation_id=")) return null;
  parsers[kind](values[0]);
  return { kind, value: values[0] };
}

export async function validateBusinessReturn(kind, value, { employeeCompany, request = workspaceFetch } = {}) {
  if (!Object.hasOwn(parsers, kind)) invalid();
  const target = parsers[kind](value);
  // This metadata locates the source. It does not authorize its Company.
  const detail = await getInstalledWorkspace(target.workspace, request), instance = detail?.instance;
  if (!instance?.company_id || !instance.instance_id || instance.workspace_id !== target.workspace
    || instance.status !== "ACTIVE" || detail.package?.status !== "ACTIVE" || detail.read_only !== false || !packages[kind](detail)
    || employeeCompany !== undefined && (!employeeCompany || employeeCompany !== instance.company_id)) invalid();
  const company = instance.company_id;
  const domain = { cg: "content-growth", music: "music", writing: "writing" }[kind];
  const root = `/api/workspace/v1/companies/${encodeURIComponent(company)}/${domain}/${encodeURIComponent(target.workspace)}`;
  let authorizedScope = null;
  const checkedRequest = async (path, options) => {
    // Keep the existing authenticated request: no headers/identity/scope override.
    const result = await request(path, options);
    if (path === root) {
      const scope = kind === "writing" ? result?.scope : result?.entry?.scope;
      const definition = kind === "writing"
        ? { package_id: scope?.package_id, version: scope?.package_version, digest: scope?.package_digest }
        : result?.entry?.definition;
      if (!scope?.tenant_id || scope.tenant_id !== TENANT_ID || scope.company_id !== company || scope.workspace_id !== target.workspace
        || definition?.package_id !== instance.package_id || definition.version !== instance.package_version || definition.digest !== instance.package_digest
        || kind === "writing" && scope.instance_id !== instance.instance_id
        || kind !== "writing" && (typeof result?.entry?.actor !== "string" || !result.entry.actor.trim()
          || scope.scope_type !== "WORKSPACE" || scope.scope_ref !== target.workspace)) invalid();
      authorizedScope = scope;
    } else {
      const holder = result?.content || result?.song || result?.record;
      if (holder && (!authorizedScope || holder.tenant_id !== authorizedScope.tenant_id
        || holder.company_id !== company || holder.workspace_id !== target.workspace)) invalid();
    }
    return result;
  };
  const verified = kind === "cg"
    ? await validateContentGrowthReturn(value, company, createContentGrowthApi(checkedRequest))
    : kind === "music"
      ? await validateMusicReturn(value, company, createMusicApi(checkedRequest))
      : await validateWritingReturn(value, company, checkedRequest);
  if (!authorizedScope || verified.company !== company || verified.workspace !== instance.workspace_id) invalid();
  return verified;
}
