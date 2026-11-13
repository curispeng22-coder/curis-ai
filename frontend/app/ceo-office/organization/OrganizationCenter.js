"use client";

import Link from "next/link";
import { roleLabel } from "../../../lib/theme.js";
import { Suspense, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";

import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../components/runtime/RuntimeStates.js";
import TerraShell, { TerraPaneContent } from "../../../components/terra/TerraShell.js";
import { EmployeeAvatar } from "../../../components/v1/EmployeeAvatar.js";
import { getOrganizationProjection, runtimeErrorMessage } from "../../../lib/runtimeApi.js";
import {
  buildOrganizationProjection,
  organizationBusinessMatches,
  organizationEmployeeMatches,
} from "../../../lib/organizationProjection.js";
import styles from "./organizationCenter.module.css";

const tabHref = (tab) => `/ceo-office/organization${tab === "employees" ? "?tab=employees" : ""}`;
const mapHref = (businessId = "") =>
  `/ceo-office/organization${businessId ? `?business_id=${encodeURIComponent(businessId)}` : ""}`;
const departmentHref = (departmentId) =>
  `/ceo-office/organization?department_id=${encodeURIComponent(departmentId)}`;
const paneId = (companyId, kind, id = "") => JSON.stringify([companyId, kind, id]);
const businessHref = (businessId) => `/ceo-office/business?business_id=${encodeURIComponent(businessId)}`;
const workspaceHref = (workspaceId) => `/ceo-office/workspace?workspace_id=${encodeURIComponent(workspaceId)}`;

function initials(name) {
  return String(name || "?").trim().slice(0, 1).toUpperCase();
}

function StatusDot({ status }) {
  const tone = status === "经营中" || status === "进行中" || status === "可参与工作"
    ? styles.good
    : status === "需要处理" || status === "暂时受阻"
      ? styles.warn
      : styles.neutral;
  return <span className={`${styles.status} ${tone}`}><i aria-hidden="true" />{status}</span>;
}

function LocalHeader({ projection, tab }) {
  return (
    <div className={styles.localHeader}>
      <div className={styles.titleRow}>
        <h1>组织中心</h1>
        <p>
          {projection.company?.name || "公司尚未建立"}
          {projection.company ? ` · ${projection.totals.departments} 部门 · ${projection.totals.businesses} 业务 · ${projection.totals.employees} 员工` : ""}
          {projection.totals.vacancies > 0 ? ` · ${projection.totals.vacancies} 个空缺` : ""}
        </p>
      </div>
      <nav className={styles.tabs} aria-label="组织中心视图">
        <Link href={tabHref("map")} aria-current={tab === "map" ? "page" : undefined}>公司版图</Link>
        <Link href={tabHref("employees")} aria-current={tab === "employees" ? "page" : undefined}>员工目录</Link>
      </nav>
    </div>
  );
}

function CompanyMap({ projection, query, setQuery }) {
  const departments = useMemo(() => projection.departments.map((department) => ({ ...department, visibleBusinesses: department.businesses.filter((business) => organizationBusinessMatches(business, query)) })).filter((department) => !query || department.visibleBusinesses.length), [projection.departments, query]);
  return <section aria-labelledby="company-map-title">
    <div className={styles.toolbar}><p id="company-map-title">部门、业务、工作空间与真实责任</p><div className={styles.tools}><label><span className="sr-only">搜索公司版图</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索业务、岗位或负责人" /></label></div></div>
    {projection.unresolvedBusinesses.length > 0 && <div className={styles.inlineWarning} role="status">{projection.unresolvedBusinesses.length} 项业务的所属部门尚未确认，暂不展示。请先确认业务归属。</div>}
    {!departments.length ? <div className={styles.empty}><h2>{query ? "没有匹配的业务" : "公司版图还是空的"}</h2><p>{query ? "换一个业务、岗位或负责人名称试试。" : "当前没有可读取的部门与业务。"}</p></div> : <div className={styles.structure}>
      <div className={styles.structureHead} aria-hidden="true"><span>部门 / 业务 / 工作空间</span><span>当前状态</span><span>职责与人员</span><span>负责人</span></div>
      {departments.map((department) => <details key={department.id} className={styles.structureDepartment} open>
        <summary><strong>{department.name}</strong><span>{department.businessCount} 个业务</span><Link href={departmentHref(department.id)} onClick={(event) => event.stopPropagation()}>查看部门资料 →</Link></summary>
        {department.visibleBusinesses.map((business) => <div key={business.id} className={styles.structureBusiness}>
          <div className={styles.structureRow}><div><Link href={mapHref(business.id)}><strong>{business.name}</strong></Link><p>{business.goal || "业务目标尚未设置"}</p></div><StatusDot status={business.status} /><span>{business.roleCount} 项职责 · {business.staffingCount} 名员工</span><span>{business.leader?.name || "负责人尚未设置"}</span></div>
          <details className={styles.structureChildren} open={query ? true : undefined}><summary>{business.workspaceCount} 个工作空间 · 查看职责</summary>
            {business.workspaces.map((workspace) => <div className={styles.workspaceRow} key={workspace.id}><Link href={workspaceHref(workspace.id)}>{workspace.name}</Link><StatusDot status={workspace.status} /></div>)}
            {business.assignments.map((assignment) => <div className={styles.assignmentRow} key={assignment.assignmentRef}><div><strong>{assignment.roleName}</strong><p>{assignment.responsibility || "责任说明未提供"}</p></div>{assignment.employee ? <Link href={`/ceo-office/organization/employees/${encodeURIComponent(assignment.employeeRef)}`}>{assignment.employee.name}</Link> : <span>员工尚未确认</span>}</div>)}
          </details>
        </div>)}
        {!department.visibleBusinesses.length && <div className={styles.departmentEmpty}>{department.assignments.length ? department.assignments.map((assignment) => <div className={styles.assignmentRow} key={assignment.assignmentRef}><span>{assignment.roleName}</span><Link href={`/ceo-office/organization/employees/${encodeURIComponent(assignment.employeeRef)}`}>{assignment.employee?.name}</Link></div>) : <p>这个部门尚未建立业务。</p>}</div>}
      </details>)}
    </div>}
  </section>;
}

function BusinessFocus({ business, projection }) {
  const department = projection.departments.find((item) => item.id === business.departmentId) || null;
  return (
    <section className={styles.focus} aria-labelledby="business-focus-title">
      <div className={styles.focusCrumb}>
        <Link href={mapHref()}>公司版图</Link>
        <span>/</span><span>{department?.name || "所属部门未知"}</span><span>/</span><strong>{business.name}</strong>
      </div>
      <div className={styles.focusLayout}>
        <div className={styles.focusMain}>
          <div className={styles.focusIntro}>
            <div>
              <StatusDot status={business.status} />
              <h2 id="business-focus-title">{business.name}</h2>
              <p>业务聚焦 · 目标、岗位与人员配置</p>
            </div>
            <Link className={styles.exitFocus} href={mapHref()}>退出聚焦 · 返回公司版图</Link>
          </div>

          <div className={styles.goalBlock}>
            <span>目标与经营方式</span>
            <strong>{business.goal || "业务目标尚未设置"}</strong>
            {business.positioning && <p>{business.positioning}</p>}
            <div className={styles.ownerLine}>
              {business.leader ? <EmployeeAvatar employee={business.leader} className={styles.avatar} /> : <span className={styles.avatar}>{initials("")}</span>}
              <span>{business.leader?.name ? `${business.leader.name} · 负责人` : "负责人尚未设置"}</span>
            </div>
            <div className={styles.tags}>
              <span>{business.roleCount} 个岗位</span>
              <span>{business.staffingCount} 名员工</span>
              {business.vacancyCount > 0 && <span className={styles.attention}>{business.vacancyCount} 个空缺</span>}
              <span>{business.workspaceCount} 个工作空间</span>
            </div>
          </div>

          <div className={styles.focusSection}>
            <div className={styles.sectionTitle}><h3>岗位结构</h3><span>来自真实责任分配</span></div>
            {business.assignments.length ? (
              <ul className={styles.roleList}>
                {business.assignments.map((assignment) => (
                  <li key={assignment.assignmentRef || `${assignment.roleRef}-${assignment.employeeRef}`}>
                    <div><strong>{assignment.roleName}</strong><p>{assignment.responsibility || "责任说明尚未记录"}</p></div>
                    <span>{assignment.employee?.name || "员工身份待确认"}</span>
                  </li>
                ))}
              </ul>
            ) : <p className={styles.sectionEmpty}>这项业务尚未设置岗位责任。</p>}
          </div>

          <div className={styles.focusSection}>
            <div className={styles.sectionTitle}><h3>工作空间 · 次级入口</h3><span>{business.workspaceCount} 个</span></div>
            {business.workspaces.length ? (
              <ul className={styles.workspaceList}>
                {business.workspaces.map((workspace) => (
                  <li key={workspace.id}><div><strong>{workspace.name}</strong><p>{workspace.status}</p></div><Link href={workspaceHref(workspace.id)}>查看 →</Link></li>
                ))}
              </ul>
            ) : <p className={styles.sectionEmpty}>尚未建立工作空间。</p>}
          </div>
        </div>

      </div>
    </section>
  );
}

function BusinessSummary({ business, projection }) {
  const department = projection.departments.find((item) => item.id === business.departmentId);
  return <section className={styles.paneDetail} aria-label="当前业务摘要"><h2>{business.name}</h2><dl>
    <div><dt>所属部门</dt><dd>{department?.name || "未知"}</dd></div>
    <div><dt>业务负责人</dt><dd>{business.leader?.name || "未设置"}</dd></div>
    <div><dt>当前状态</dt><dd>{business.status}</dd></div>
    <div><dt>岗位职责</dt><dd>{business.roleCount ? `${business.roleCount} 项` : "尚无岗位事实"}</dd></div>
    <div><dt>员工</dt><dd>{business.staffingCount} 名</dd></div>
    <div><dt>工作空间</dt><dd>{business.workspaceCount} 个</dd></div>
  </dl><Link className={styles.primaryAction} href={businessHref(business.id)}>进入业务详情</Link>
    {business.workspaces.map((workspace) => <Link key={workspace.id} className={styles.secondaryAction} href={workspaceHref(workspace.id)}>{workspace.name} →</Link>)}</section>;
}

function EmployeeSummary({ employee }) {
  return <section className={styles.selectedEmployee} aria-label="所选员工"><EmployeeAvatar employee={{ ...employee, avatar_ref: employee.avatarRef }} className={styles.avatar} /><h2>{employee.name}</h2><p>{roleLabel(employee.role)}</p><StatusDot status={employee.status} /><h3>当前职责与范围</h3>{employee.assignments.length ? employee.assignments.map((assignment, index) => <div key={index}><strong>{assignment.businessName || assignment.scopeName} · {assignment.roleName}</strong><p>{assignment.responsibility || "责任说明尚未提供"}</p></div>) : <p>当前尚未分配业务责任</p>}<p>所属部门：{employee.departmentName}</p><Link href={`/ceo-office/organization/employees/${encodeURIComponent(employee.id)}`}>打开员工档案与对话 →</Link></section>;
}

function EmployeeDirectory({ projection, query, setQuery, selected, onSelect }) {
  const employees = projection.employees.filter((employee) => organizationEmployeeMatches(employee, query));
  const groups = projection.departments.map((department) => ({
    id: department.id,
    name: department.name,
    employees: employees.filter((employee) => employee.departmentId === department.id),
  })).filter((group) => group.employees.length);
  const direct = employees.filter((employee) => !projection.departments.some((department) => department.id === employee.departmentId));
  if (direct.length) groups.push({ id: "company", name: "直属公司", employees: direct });

  return (
    <section aria-labelledby="employee-directory-title">
      <div className={styles.toolbar}>
        <p id="employee-directory-title">按人员反查岗位、所属业务与所属部门</p>
        <div className={styles.tools}>
          <label><span className="sr-only">搜索员工目录</span><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索员工、岗位或业务" /></label>
        </div>
      </div>
      {groups.length === 0 ? (
        <div className={styles.empty}><h2>{query ? "没有匹配的员工" : "员工目录还是空的"}</h2><p>{query ? "换一个员工、岗位或业务名称试试。" : "这里只显示已经属于当前公司的真实员工。"}</p></div>
      ) : (
        <div className={styles.employeeGroups}>
          {groups.map((group) => (
            <section key={group.id} className={styles.employeeGroup} aria-labelledby={`employee-group-${group.id}`}>
              <header><h2 id={`employee-group-${group.id}`}>{group.name}</h2><span>{group.employees.length} 名员工</span></header>
              <div className={styles.employeeGrid}>
                {group.employees.map((employee) => (
                  <article key={employee.id} className={`${styles.employeeRow} ${selected?.id === employee.id ? styles.employeeSelected : ""}`}>
                    <EmployeeAvatar employee={{ ...employee, avatar_ref: employee.avatarRef }} className={styles.avatar} />
                    <div className={styles.employeeCopy}>
                      <strong>{employee.name} · {roleLabel(employee.role)}</strong>
                      <p>所属部门：{employee.departmentName}</p>
                      {employee.assignments.length ? (
                        <p>{employee.assignments.map((assignment) => `${assignment.businessName || assignment.scopeName} · ${assignment.roleName}`).join("；")}</p>
                      ) : <p>尚未分配业务责任</p>}
                      <StatusDot status={employee.status} />
                    </div>
                    <button type="button" aria-label={`查看${employee.name}的资料`} aria-pressed={selected?.id === employee.id} onClick={() => onSelect(employee.id)}>查看资料 →</button>
                  </article>
                ))}
              </div>
            </section>
          ))}
          {projection.totals.vacancies > 0 && (
            <div className={styles.hiringNotice}>
              <div><strong>{projection.totals.vacancies} 个岗位空缺 · 待招聘</strong><p>这些岗位尚未安排员工。</p></div>
              <Link href="/ceo-office/talent-market?source=organization">去人才与能力 →</Link>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

export function OrganizationReady({ projection, tab, selectedBusinessId, selectedDepartmentId }) {
  const [query, setQuery] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [request, setRequest] = useState(0);
  const selectedBusiness = tab === "map" && projection.departments.some((department) =>
    department.businesses.some((business) => business.id === selectedBusinessId))
    ? projection.businessById.get(selectedBusinessId) : null;
  const selectedDepartment = tab === "map" && !selectedBusiness
    ? projection.departments.find((item) => item.id === selectedDepartmentId) : null;
  const selectedEmployee = tab === "employees" ? projection.employees.find((item) => item.id === employeeId) : null;
  const selectedId = selectedEmployee ? paneId(projection.company.id, "employee", selectedEmployee.id)
    : selectedBusiness ? paneId(projection.company.id, "business", selectedBusiness.id)
      : selectedDepartment ? paneId(projection.company.id, "department", selectedDepartment.id) : "";
  useEffect(() => { if (selectedBusiness || selectedDepartment) setRequest((value) => value + 1); }, [selectedBusiness, selectedDepartment]);
  const context = useMemo(() => <nav className={styles.domainNav} aria-label="组织导航">
    <Link href={tabHref("map")} aria-current={tab === "map" && !selectedBusiness && !selectedDepartment ? "page" : undefined}>公司版图</Link>
    <Link href={tabHref("employees")} aria-current={tab === "employees" ? "page" : undefined}>员工目录</Link>
    {projection.departments.map((department) => <section key={department.id}>
      <Link href={departmentHref(department.id)} aria-current={selectedDepartment?.id === department.id ? "page" : undefined}>{department.name}</Link>
      {department.businesses.map((business) => <Link key={business.id} className={styles.domainChild} href={mapHref(business.id)} aria-current={selectedBusiness?.id === business.id ? "page" : undefined}>{business.name}</Link>)}
    </section>)}
  </nav>, [projection, tab, selectedBusiness, selectedDepartment]);
  const tabs = useMemo(() => {
    const company = projection.company;
    const available = [{ id: paneId(company.id, "company"), title: "当前公司", content: <section className={styles.paneDetail}><h2>{company.name}</h2><dl>
      <div><dt>部门</dt><dd>{projection.totals.departments}</dd></div><div><dt>业务</dt><dd>{projection.totals.businesses}</dd></div><div><dt>员工</dt><dd>{projection.totals.employees}</dd></div><div><dt>待配置岗位</dt><dd>{projection.totals.vacancies}</dd></div>
    </dl></section> }];
    if (selectedDepartment) available.push({ id: paneId(company.id, "department", selectedDepartment.id), title: selectedDepartment.name, content: <section className={styles.paneDetail}><h2>{selectedDepartment.name}</h2><p>{selectedDepartment.description || "部门职责尚未记录"}</p><dl>
      <div><dt>业务</dt><dd>{selectedDepartment.businessCount}</dd></div><div><dt>员工</dt><dd>{selectedDepartment.employeeCount}</dd></div><div><dt>负责人</dt><dd>{selectedDepartment.leader?.name || "尚未设置"}</dd></div>
    </dl></section> });
    if (selectedBusiness) available.push({ id: paneId(company.id, "business", selectedBusiness.id), title: selectedBusiness.name, content: <BusinessSummary business={selectedBusiness} projection={projection} /> });
    if (selectedEmployee) available.push({ id: paneId(company.id, "employee", selectedEmployee.id), title: selectedEmployee.name, content: <EmployeeSummary employee={selectedEmployee} /> });
    return available;
  }, [projection, selectedDepartment, selectedBusiness, selectedEmployee]);
  return <div className={styles.page}>
    <TerraPaneContent contextPane={context} contextLabel="组织导航" utilityTabs={tabs} utilityLabel="组织资料"
      initialContextOpen initialUtilityOpen utilityRequestKey={request} utilityRequestTabId={selectedId} />
    <LocalHeader projection={projection} tab={tab} />
    {tab === "employees"
      ? <EmployeeDirectory projection={projection} query={query} setQuery={setQuery} selected={selectedEmployee} onSelect={(id) => { setEmployeeId(id); setRequest((value) => value + 1); }} />
      : selectedBusiness
        ? <BusinessFocus business={selectedBusiness} projection={projection} />
        : <CompanyMap projection={projection} query={query} setQuery={setQuery} />}
  </div>;
}

function OrganizationSurface() {
  const runtime = useRuntime();
  const searchParams = useSearchParams();
  const tab = searchParams.get("tab") === "employees" ? "employees" : "map";
  const selectedBusinessId = searchParams.get("business_id") || "";
  const selectedDepartmentId = searchParams.get("department_id") || "";
  const [state, setState] = useState({ status: "idle", projection: null, error: "" });

  useEffect(() => {
    let active = true;
    if (runtime.status !== "ready" || !runtime.companyId || !runtime.snapshot?.company) return () => { active = false; };
    setState({ status: "loading", projection: null, error: "" });
    getOrganizationProjection(runtime.companyId)
      .then((payload) => {
        if (!active) return;
        setState({
          status: "ready",
          projection: buildOrganizationProjection({
            company: payload?.company || runtime.snapshot.company,
            departments: payload?.departments || [],
            employees: payload?.employees || [],
            businesses: payload?.businesses || [],
            departmentAssignments: payload?.departmentAssignments || [],
          }),
          error: "",
        });
      })
      .catch((error) => active && setState({ status: "error", projection: null, error: runtimeErrorMessage(error) }));
    return () => { active = false; };
  }, [runtime.companyId, runtime.snapshot?.company, runtime.status]);

  if (["idle", "loading"].includes(runtime.status) || ["idle", "loading"].includes(state.status)) return <RuntimeLoading label="正在读取组织信息…" />;
  if (["error", "forbidden"].includes(runtime.status)) return <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  if (state.status === "error") return <RuntimeError message={state.error || "无法加载组织信息"} />;
  if (!runtime.snapshot?.company) return <RuntimeEmpty title="公司尚未建立" description="先完成公司创办，再查看公司版图。" action={<Link href="/onboarding">开始创办公司</Link>} />;

  return <OrganizationReady key={state.projection.company.id} projection={state.projection} tab={tab}
    selectedBusinessId={selectedBusinessId} selectedDepartmentId={selectedDepartmentId} />;
}

export default function OrganizationCenter() {
  return (
    <TerraShell topCrumb="组织中心" assistantContext={{ page: "organization" }}>
      <Suspense fallback={<RuntimeLoading label="正在打开组织中心…" />}>
        <OrganizationSurface />
      </Suspense>
    </TerraShell>
  );
}
