// Pure mapping for object search results: group labels, icons, and href rules.
// No React, no fetch — this module is unit-testable and the single source of
// truth for how a search item navigates.

export const OBJECT_GROUPS = [
  { type: "business", label: "业务", icon: "i-business" },
  { type: "workspace", label: "工作台", icon: "i-view_in_ar" },
  { type: "employee", label: "员工", icon: "i-person" },
  { type: "business_object", label: "业务对象", icon: "i-category" },
  { type: "knowledge", label: "资料", icon: "i-auto_stories" },
  { type: "meeting", label: "会议", icon: "i-event" },
  { type: "decision", label: "决策", icon: "i-published_with_changes" },
  { type: "task", label: "任务", icon: "i-checklist" },
  { type: "result", label: "结果", icon: "i-description" },
];

const GROUP_BY_TYPE = Object.fromEntries(OBJECT_GROUPS.map((g) => [g.type, g]));

export function groupMeta(type) {
  return GROUP_BY_TYPE[type] || { type, label: type, icon: "i-help" };
}

// Build the navigation href for a search item. Each route is verified against
// an existing frontend page; unknown types fall back to the company home.
export function objectHref(item) {
  const { type, id } = item;
  switch (type) {
    case "business":
      return "/ceo-office/business";
    case "workspace":
      return `/ceo-office/workspace/installed/${encodeURIComponent(id)}`;
    case "employee":
      return `/ceo-office/organization/employees/${encodeURIComponent(id)}`;
    case "knowledge":
      return `/ceo-office/knowledge/entries/${encodeURIComponent(id)}`;
    case "meeting":
      return `/ceo-office/meeting?meeting=${encodeURIComponent(id)}`;
    case "decision":
      return "/ceo-office/decisions";
    case "task":
      return `/ceo-office/execution/tasks/${encodeURIComponent(id)}`;
    case "result": {
      const workspaceId = item.workspace_id || "";
      const base = `/ceo-office/workspace?workspace_id=${encodeURIComponent(workspaceId)}`;
      return `${base}&result_workspace=${encodeURIComponent(workspaceId)}&result_ref=${encodeURIComponent(id)}`;
    }
    case "business_object":
      // Business objects live inside a workspace; fall back to the workspace
      // list when no owning workspace is known.
      return item.workspace_id
        ? `/ceo-office/workspace/installed/${encodeURIComponent(item.workspace_id)}`
        : "/ceo-office/workspace";
    default:
      return "/ceo-office";
  }
}
