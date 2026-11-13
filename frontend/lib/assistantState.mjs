export const EMPTY_ASSISTANT_IDENTITY = {
  name: "",
  avatar: "",
  role: "",
  tone: "",
  personality: "",
  updated_at: null,
};
const IDENTITY_KEYS = ["name", "avatar", "role", "tone", "personality"];

export function normalizeAssistantIdentity(value = {}) {
  return Object.fromEntries(
    IDENTITY_KEYS.map((key) => [key, String(value?.[key] || "")])
  );
}

export const INITIAL_ASSISTANT_STATE = {
  open: false,
  minimized: false,
  pageContext: { page: "workspace" },
  input: "",
  intent: "auto",
  unreadCount: 0,
  snapshot: null,
  notifications: [],
  identity: EMPTY_ASSISTANT_IDENTITY,
  loading: false,
  error: "",
  lastResult: null,
};

const CONTEXT_KEYS = [
  "page",
  "company_id",
  "workspace_id",
  "business_type",
  "cycle_id",
  "content_id",
  "department_id",
  "project_id",
  "task_id",
  "employee_id",
];
const PAGE_CONTEXTS = new Set(["workspace", "ceo-office", "project", "task"]);

export function normalizeAssistantContext(value = {}) {
  const result = {};
  for (const key of CONTEXT_KEYS) {
    const next = String(value?.[key] || "").trim();
    if (next) result[key] = next;
  }
  result.page = PAGE_CONTEXTS.has(result.page) ? result.page : "workspace";
  return result;
}

export function assistantReducer(state, action) {
  switch (action.type) {
    case "open":
      return { ...state, open: true, minimized: false };
    case "close":
      return { ...state, open: false };
    case "minimize":
      return { ...state, open: false, minimized: true };
    case "context":
      return {
        ...state,
        pageContext: normalizeAssistantContext(action.value),
      };
    case "input":
      return { ...state, input: action.value };
    case "intent":
      return { ...state, intent: action.value };
    case "loading":
      return { ...state, loading: true, error: "" };
    case "loaded":
      return {
        ...state,
        loading: false,
        error: "",
        snapshot: action.snapshot,
        identity: action.snapshot?.identity || state.identity,
        notifications: action.notifications || [],
        unreadCount: action.unreadCount || 0,
      };
    case "identity":
      return { ...state, identity: action.value };
    case "result":
      return {
        ...state,
        loading: false,
        error: "",
        lastResult: action.value,
        input: "",
      };
    case "error":
      return { ...state, loading: false, error: action.value };
    case "read":
      return { ...state, unreadCount: 0 };
    default:
      return state;
  }
}
