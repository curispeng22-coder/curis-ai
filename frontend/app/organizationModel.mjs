export function nextOrganizationAction(data) {
  if (!data.company) return { label: "创建本地 Workspace", href: "/ceo-office/organization" };
  if (data.departments.length === 0) {
    return { label: "创建首个业务部门", href: "/ceo-office/organization" };
  }
  if (data.employees.length === 0) {
    return { label: "创建首位 AI 员工", href: "/ceo-office/organization/employees" };
  }
  if (data.projects.length === 0) {
    return { label: "创建首个项目", href: "/ceo-office/projects" };
  }
  return {
    label: "继续重点项目",
    href: `/ceo-office/projects/${data.projects[0].project_id}`,
  };
}
