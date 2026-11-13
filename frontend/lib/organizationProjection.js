const STATUS_COPY = {
  ACTIVE: "经营中",
  RUNNING: "进行中",
  DRAFT: "准备中",
  PLANNED: "准备中",
  PAUSED: "已暂停",
  ARCHIVED: "已归档",
  DISABLED: "已停用",
  AVAILABLE: "可参与工作",
  IDLE: "当前空闲",
  ASSIGNED: "当前有责任",
  BLOCKED: "暂时受阻",
  FAILED: "需要处理",
};

const upper = (value) => String(value || "").trim().toUpperCase();
const list = (value) => (Array.isArray(value) ? value : []);
const text = (value) => String(value || "").trim();

export function organizationStatusLabel(value) {
  return STATUS_COPY[upper(value)] || "状态待确认";
}

function assignmentView(item, employeeById) {
  const data = item?.data || {};
  const employeeRef = text(data.companyEmployeeRef);
  const employee = employeeById.get(employeeRef) || null;
  return {
    assignmentRef: text(item?.entity_id),
    employeeRef,
    employee,
    roleRef: text(data.roleRef),
    roleName: text(data.roleName || data.responsibility) || "岗位未命名",
    responsibility: text(data.responsibility),
    isLeader: Boolean(data.isLeader),
    identityStatus: text(data.employeeIdentityStatus) || "UNRESOLVED",
    scopeType: text(data.scopeType),
    scopeRef: text(data.scopeRef),
    workspaceId: text(item?.workspace_id),
    enabled: Boolean(employee && data.employeeEnabled !== false && employee.enabled !== false && employee.enabled !== 0 && !["DISABLED", "DELETED"].includes(upper(employee.status)) && (!data.roleStatus || ["ASSIGNED", "OPERATING"].includes(upper(data.roleStatus)))),
  };
}

function businessView(item, employeeById) {
  const assignments = list(item?.team).filter((assignment) => !assignment.lifecycle_status || upper(assignment.lifecycle_status) === "ACTIVE").map((assignment) => assignmentView(assignment, employeeById));
  const employeeRefs = new Set(assignments.map((assignment) => assignment.employeeRef).filter(Boolean));
  const roleRefs = new Set(
    assignments.map((assignment) => assignment.roleRef || assignment.roleName).filter(Boolean)
  );
  const leaderAssignment = assignments.find((assignment) => assignment.isLeader && (!assignment.scopeType || assignment.scopeType === "BUSINESS")) || null;
  const attentionCount = Number(item?.operatingSummary?.needsAttentionCount || 0);
  return {
    id: text(item?.business_id),
    name: text(item?.name) || "未命名业务",
    status: organizationStatusLabel(item?.lifecycle_status),
    statusRaw: upper(item?.lifecycle_status),
    departmentId: text(item?.department_id || item?.parentPath?.department?.id),
    departmentName: text(item?.parentPath?.department?.name),
    goal: text(item?.definition?.goal || item?.goal),
    positioning: text(item?.definition?.positioning || item?.positioning),
    assignments,
    leader: leaderAssignment?.employee || null,
    leaderAssignment,
    roleCount: roleRefs.size,
    staffingCount: employeeRefs.size,
    vacancyCount: 0,
    attentionCount,
    workspaceCount: Number(item?.operatingSummary?.workspaceCount ?? list(item?.workspaces).length),
    workspaces: list(item?.workspaces).map((workspace) => ({
      id: text(workspace?.workspace_id),
      name: text(workspace?.name) || "未命名工作空间",
      status: organizationStatusLabel(workspace?.status),
    })),
  };
}

export function buildOrganizationProjection({ company, departments, businesses, employees, departmentAssignments = [] }) {
  const companyId = text(company?.company_id);
  const companyDepartments = list(departments).filter(
    (department) => !companyId || text(department?.company_id) === companyId
  );
  const companyEmployees = list(employees).filter(
    (employee) => !companyId || text(employee?.company_id) === companyId
  );
  const employeeById = new Map(companyEmployees.map((employee) => [text(employee?.id), employee]));
  const businessViews = list(businesses)
    .filter((business) => !companyId || text(business?.company_id) === companyId)
    .map((business) => businessView(business, employeeById));

  const businessById = new Map(businessViews.map((business) => [business.id, business]));
  const assignmentsByEmployee = new Map();
  for (const item of list(departmentAssignments)) {
    if (text(item.company_id) !== companyId) continue;
    const assignment = assignmentView(item, employeeById);
    const department = companyDepartments.find((entry) => entry.id === item.data?.scopeRef);
    if (!assignment.employee || !department) continue;
    const current = assignmentsByEmployee.get(assignment.employeeRef) || [];
    current.push({ ...assignment, departmentId: department.id, departmentName: department.name,
      businessName: "", scopeName: department.name });
    assignmentsByEmployee.set(assignment.employeeRef, current);
  }
  for (const business of businessViews) {
    for (const assignment of business.assignments) {
      if (!assignment.employeeRef || !assignment.employee) continue;
      const current = assignmentsByEmployee.get(assignment.employeeRef) || [];
      current.push({
        businessId: business.id,
        businessName: business.name,
        departmentId: business.departmentId,
        departmentName: business.departmentName,
        roleRef: assignment.roleRef,
        roleName: assignment.roleName,
        responsibility: assignment.responsibility,
        isLeader: assignment.isLeader,
      });
      assignmentsByEmployee.set(assignment.employeeRef, current);
    }
  }

  const departmentViews = companyDepartments.map((department) => {
    const id = text(department?.id);
    const members = companyEmployees.filter((employee) => text(employee?.department_id) === id);
    const scopedBusinesses = businessViews.filter((business) => business.departmentId === id);
    return {
      id,
      name: text(department?.name) || "未命名部门",
      description: text(department?.mission || department?.description),
      leader: employeeById.get(text(department?.manager_employee_id)) || null,
      businesses: scopedBusinesses,
      businessCount: scopedBusinesses.length,
      employeeCount: members.length,
      members,
      assignments: list(departmentAssignments).filter((item) => item.company_id === companyId && item.data?.scopeRef === id)
        .map((item) => assignmentView(item, employeeById)),
      vacancyCount: scopedBusinesses.reduce((sum, business) => sum + business.vacancyCount, 0),
      attentionCount: scopedBusinesses.reduce((sum, business) => sum + business.attentionCount, 0),
    };
  });

  const knownDepartmentIds = new Set(departmentViews.map((department) => department.id));
  const unresolvedBusinesses = businessViews.filter(
    (business) => !business.departmentId || !knownDepartmentIds.has(business.departmentId)
  );

  const directEmployees = companyEmployees.filter(
    (employee) => !text(employee?.department_id) || !knownDepartmentIds.has(text(employee?.department_id))
  );
  const employeeViews = companyEmployees.map((employee) => ({
    id: text(employee?.id),
    name: text(employee?.name) || "未命名员工",
    role: text(employee?.role) || "岗位待确认",
    avatarRef: text(employee?.avatar_ref),
    departmentId: text(employee?.department_id),
    departmentName:
      departmentViews.find((department) => department.id === text(employee?.department_id))?.name || "直属公司",
    status: employee?.enabled === false || employee?.enabled === 0 ? "已停用" : organizationStatusLabel(employee?.status || "AVAILABLE"),
    enabled: employee?.enabled !== false && employee?.enabled !== 0,
    assignments: assignmentsByEmployee.get(text(employee?.id)) || [],
  }));

  return {
    company: company
      ? { id: companyId, name: text(company?.name) || "未命名公司", status: organizationStatusLabel(company?.status) }
      : null,
    departments: departmentViews,
    businesses: businessViews,
    businessById,
    employees: employeeViews,
    directEmployeeCount: directEmployees.length,
    unresolvedBusinesses,
    totals: {
      departments: departmentViews.length,
      businesses: businessViews.length,
      employees: employeeViews.length,
      vacancies: departmentViews.reduce((sum, department) => sum + department.vacancyCount, 0),
      attention: departmentViews.reduce((sum, department) => sum + department.attentionCount, 0),
    },
  };
}

export function organizationBusinessMatches(business, query) {
  const needle = text(query).toLocaleLowerCase("zh-CN");
  if (!needle) return true;
  return [
    business.name,
    business.goal,
    business.positioning,
    business.leader?.name,
    ...business.assignments.flatMap((assignment) => [assignment.roleName, assignment.responsibility]),
  ].some((value) => text(value).toLocaleLowerCase("zh-CN").includes(needle));
}

export function organizationEmployeeMatches(employee, query) {
  const needle = text(query).toLocaleLowerCase("zh-CN");
  if (!needle) return true;
  return [
    employee.name,
    employee.role,
    employee.departmentName,
    ...employee.assignments.flatMap((assignment) => [
      assignment.businessName,
      assignment.roleName,
      assignment.responsibility,
    ]),
  ].some((value) => text(value).toLocaleLowerCase("zh-CN").includes(needle));
}
