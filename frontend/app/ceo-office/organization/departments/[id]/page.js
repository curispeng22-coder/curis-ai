"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import {
  TerraBackLink,
  TerraCard,
  TerraCardHeader,
  TerraEmpty,
  TerraPageHead,
  TerraTag,
} from "../../../../../components/terra/TerraPrimitives.js";
import {
  DATA_COPY,
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../../../components/terra/TerraState.js";
import {
  getDepartment,
  getEmployees,
  getProjects,
} from "../../../../../lib/api.js";

const STATUS_LABEL = {
  active: "运行中",
  draft: "草稿",
  disabled: "已暂停",
  archived: "已归档",
};

export default function DepartmentDetailPage() {
  const params = useParams();
  const id = typeof params?.id === "string" ? params.id : "";
  const [department, setDepartment] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const loadVersion = useRef(0);

  const load = useCallback(async () => {
    if (!id) return;
    const version = ++loadVersion.current;
    setLoading(true);
    setError("");
    try {
      const departmentData = await getDepartment(id);
      const employeeData = await getEmployees();
      const projectData = await getProjects();
      if (version !== loadVersion.current) return;
      setDepartment(departmentData);
      setEmployees((employeeData?.employees || []).filter((item) => item.department_id === id));
      setProjects((projectData?.projects || []).filter((item) => item.department_id === id));
    } catch (err) {
      if (version === loadVersion.current) {
        setError(err?.message || "业务部门数据读取失败");
      }
    } finally {
      if (version === loadVersion.current) setLoading(false);
    }
  }, [id]);

  useEffect(() => { load(); }, [load]);

  if (loading) {
    return (
      <TerraShell topCrumb="组织中心 / 业务部门">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }

  if (error || !department) {
    return (
      <TerraShell topCrumb="组织中心 / 业务部门">
        <TerraErrorState message={error || "业务部门不存在"} onRetry={load} />
      </TerraShell>
    );
  }

  const manager = employees.find((item) => item.id === department.manager_employee_id);

  return (
    <TerraShell topCrumb={`组织中心 / ${department.name}`}>
      <TerraBackLink href="/ceo-office/organization">返回组织中心</TerraBackLink>
      <TerraPageHead
        title={department.name}
        subtitle={department.mission || "未记录价值目标"}
        pill={{ text: STATUS_LABEL[department.status] || department.status, icon: "i-apartment" }}
        facts={[
          { value: employees.length, label: "员工" },
          { value: projects.length, label: "项目" },
        ]}
      />

      <div className="grid grid-cols-12 gap-3.5">
        <TerraCard className="col-span-12 lg:col-span-7">
          <TerraCardHeader icon="i-info" iconClass="primary" title="业务部门概览" />
          <dl className="grid gap-3 sm:grid-cols-2">
            {[
              { label: "负责人", value: manager?.name || DATA_COPY.noOwner },
              { label: "业务部门模板", value: department.template_id || DATA_COPY.noData },
              { label: "创建时间", value: department.created_at || DATA_COPY.noData },
              { label: "运行状态", value: STATUS_LABEL[department.status] || department.status },
            ].map((item) => (
              <div key={item.label} className="rounded-ui-sm bg-ui-surface-2 px-3 py-2">
                <dt className="text-ui-1 text-ui-txt-3">{item.label}</dt>
                <dd className="text-sm font-medium text-ui-txt mt-0.5">{item.value}</dd>
              </div>
            ))}
          </dl>
        </TerraCard>

        <TerraCard className="col-span-12 lg:col-span-5">
          <TerraCardHeader icon="i-groups" iconClass="cyan" title="直属员工" />
          {employees.length === 0 ? (
            <TerraEmpty icon="i-person_off">暂无成员</TerraEmpty>
          ) : (
            <div className="space-y-2">
              {employees.map((employee) => (
                <Link
                  key={employee.id}
                  href={`/ceo-office/organization/employees/${employee.id}`}
                  className="flex items-center gap-2 rounded-ui-sm bg-ui-surface-2 px-3 py-2 no-underline"
                >
                  <span className="w-8 h-8 rounded-full bg-ui-primary text-ui-primary-fg grid place-items-center text-xs font-bold">
                    {(employee.name || "?").slice(0, 1)}
                  </span>
                  <span className="min-w-0 flex-1">
                    <span className="block text-xs font-semibold text-ui-txt truncate">{employee.name}</span>
                    <span className="block text-ui-1 text-ui-txt-3 truncate">{employee.role || DATA_COPY.unassigned}</span>
                  </span>
                  <TerraTag color={employee.enabled ? "green" : "grey"}>
                    {employee.enabled ? "在岗" : "停用"}
                  </TerraTag>
                </Link>
              ))}
            </div>
          )}
        </TerraCard>

        <TerraCard className="col-span-12">
          <TerraCardHeader icon="i-folder_open" iconClass="green" title="直属项目" />
          {projects.length === 0 ? (
            <TerraEmpty icon="i-folder_off">暂无项目</TerraEmpty>
          ) : (
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
              {projects.map((project) => (
                <Link
                  key={project.project_id}
                  href={`/ceo-office/projects/${project.project_id}`}
                  className="rounded-ui-sm border border-ui-line p-3 no-underline hover:border-ui-primary-light"
                >
                  <div className="font-semibold text-sm text-ui-txt">{project.name}</div>
                  <div className="text-ui-1 text-ui-txt-3 mt-1 line-clamp-2">{project.goal}</div>
                  <TerraTag color={project.status === "active" ? "green" : "grey"}>{project.status}</TerraTag>
                </Link>
              ))}
            </div>
          )}
        </TerraCard>
      </div>
    </TerraShell>
  );
}
