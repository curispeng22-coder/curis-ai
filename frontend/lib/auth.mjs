const DEFAULT_RETURN_PATH = "/ceo-office";
const CONTROL_OR_BACKSLASH = /[\u0000-\u001f\u007f\\]/;

export function safeReturnPath(value, origin) {
  const candidate = String(value || "").trim();
  if (
    !candidate.startsWith("/")
    || candidate.startsWith("//")
    || candidate.length > 2048
    || CONTROL_OR_BACKSLASH.test(candidate)
  ) {
    return DEFAULT_RETURN_PATH;
  }
  try {
    const base = new URL(origin);
    const resolved = new URL(candidate, base);
    if (resolved.origin !== base.origin) return DEFAULT_RETURN_PATH;
    return `${resolved.pathname}${resolved.search}${resolved.hash}`;
  } catch {
    return DEFAULT_RETURN_PATH;
  }
}
