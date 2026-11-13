"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import Link from "next/link";
import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import {
  TerraBoundary,
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraEmpty,
  TerraPageHead,
  TerraTable,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import {
  DATA_COPY,
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../components/terra/TerraState.js";
import TerraConfirmDialog from "../../../components/terra/TerraConfirm.js";
import {
  deleteDepartment,
  getCompanies,
  getDepartmentTemplates,
  getDepartments,
  getEmployees,
  getProjects,
} from "../../../lib/api.js";
import {
  getPrivateCapabilities,
  getPrivateModels,
} from "../../../lib/capabilities.js";
import CompanyFormDrawer from "./CompanyFormDrawer.js";
import DepartmentFormDrawer from "./DepartmentFormDrawer.js";
import OrganizationCenter from "./OrganizationCenter.js";

const STATUS_LABEL = {
  active: "运行中",
  draft: "草稿",
  disabled: "已暂停",
  archived: "已归档",
};

/**
 * OrgLevel — AI Workforce Map 的一层（公司 / 业务部门 / AI 员工）。
 * 左列固定层级标签，右侧节点流式排布，对齐原型 org-level 的信息层级。
 */
function OrgLevel({ label, children }) {
  return (
    <div className="flex flex-col gap-2 sm:flex-row sm:gap-4">
      <div className="sm:w-24 sm:flex-shrink-0 sm:pt-2">
        <span className="text-ui-1 font-bold text-ui-txt-3 tracking-wide">{label}</span>
      </div>
      <div className="flex flex-1 flex-wrap gap-3">{children}</div>
    </div>
  );
}

/**
 * OrgNode — 单个团队节点卡片（头像 + 名称 + 角色 + 状态/补充信息），
 * 形态对齐原型 org-node；只渲染真实记录，缺省字段显示「未记录/未分配」。
 */
function OrgNode({ avatar, name, role, status, extra }) {
  return (
    <article className="w-full max-w-[280px] rounded-ui-md border border-ui-line bg-ui-surface-2 p-3 sm:w-auto sm:min-w-[200px]">
      <div className="flex items-center gap-2.5">
        <span className="w-9 h-9 rounded-full bg-ui-primary text-ui-primary-fg grid place-items-center text-ui-3 font-bold flex-shrink-0">
          {String(avatar || "?").slice(0, 1)}
        </span>
        <div className="min-w-0 flex-1">
          <div className="text-ui-3 font-semibold text-ui-txt truncate">{name}</div>
          <div className="text-ui-1 text-ui-txt-3 line-clamp-2">{role}</div>
        </div>
      </div>
      {(status || extra) && (
        <div className="mt-2.5 flex flex-wrap items-center gap-1.5">
          {status}
          {extra}
        </div>
      )}
    </article>
  );
}

/**
 * CapacityItem — 能力与容量卡内的单项（标签 + 值 + 说明）。
 * 只展示真实计数；容量百分比等未接入端点的事实不填假数字。
 */
function CapacityItem({ label, value, note }) {
  return (
    <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 p-3">
      <div className="flex items-center justify-between gap-2">
        <span className="text-ui-1 font-semibold text-ui-txt-3">{label}</span>
        <span className="font-ui-sans font-bold text-ui-4 text-ui-txt">{value}</span>
      </div>
      <div className="text-ui-1 text-ui-txt-3 mt-1.5">{note}</div>
    </div>
  );
}

export function LegacyOrganizationPage() {
  const [companies, setCompanies] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [projects, setProjects] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState("");
  const [companyForm, setCompanyForm] = useState(undefined);
  const [departmentForm, setDepartmentForm] = useState(undefined);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  // 能力资产库（对齐原型 ai-organization.html §能力资产库）：只读概览，
  // 真实私有能力来自后端，写操作统一交给能力中心页，避免两套表单实现漂移。
  const [capAssets, setCapAssets] = useState([]);
  const [capLoading, setCapLoading] = useState(true);

  const loadAll = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const companyData = await getCompanies();
      const departmentData = await getDepartments();
      const employeeData = await getEmployees();
      const projectData = await getProjects();
      const templateData = await getDepartmentTemplates();
      const nextCompanies = companyData?.companies || [];
      setCompanies(nextCompanies);
      setDepartments(departmentData?.departments || []);
      setEmployees(employeeData?.employees || []);
      setProjects(projectData?.projects || []);
      setTemplates(templateData?.department_templates || []);
      setSelectedCompanyId((current) => {
        if (nextCompanies.some((item) => item.company_id === current)) return current;
        return nextCompanies.find((item) => item.is_default)?.company_id || nextCompanies[0]?.company_id || "";
      });
    } catch (err) {
      setError(err?.message || "组织中心数据读取失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadAll(); }, [loadAll]);

  /**
   * 读取租户私有能力，归一成统一形状供「能力资产库」卡展示。
   * 失败不阻塞组织数据（能力是增量信息，不是组织页主干）。
   */
  const loadCapAssets = useCallback(async () => {
    setCapLoading(true);
    try {
      const [models, agents] = await Promise.all([
        getPrivateModels(),
        getPrivateCapabilities("agent"),
      ]);
      const modelItems = (models?.models || []).map((m) => ({
        key: `model:${m.name}`,
        name: m.name,
        typeLabel: "模型",
        typeColor: "primary",
        meta: [m.provider_type, m.model_name].filter(Boolean).join(" · ") || DATA_COPY.noData,
        credential: m.credential_ref || "",
        enabled: m.enabled !== false,
      }));
      const agentItems = (agents?.capabilities || []).map((a) => ({
        key: `agent:${a.capability_id}`,
        name: a.display_name || a.capability_id,
        typeLabel: "AI 员工",
        typeColor: "violet",
        meta: [a.metadata?.kind, a.metadata?.endpoint].filter(Boolean).join(" · ") || DATA_COPY.noData,
        credential: a.metadata?.credential_ref || "",
        enabled: (a.status || "inactive") === "active",
      }));
      setCapAssets([...modelItems, ...agentItems]);
    } catch (err) {
      setCapAssets([]);
    } finally {
      setCapLoading(false);
    }
  }, []);

  useEffect(() => { loadCapAssets(); }, [loadCapAssets]);

  const company = useMemo(
    () => companies.find((item) => item.company_id === selectedCompanyId) || null,
    [companies, selectedCompanyId]
  );
  const companyDepartments = departments.filter((item) => item.company_id === selectedCompanyId);
  const companyEmployees = employees.filter((item) => item.company_id === selectedCompanyId);
  const companyProjects = projects.filter((item) => item.company_id === selectedCompanyId);
  const activeEmployeeCount = companyEmployees.filter((item) => item.enabled).length;

  function departmentFacts(department) {
    return {
      employeeCount: companyEmployees.filter((item) => item.department_id === department.id).length,
      projectCount: companyProjects.filter((item) => item.department_id === department.id).length,
      manager: companyEmployees.find((item) => item.id === department.manager_employee_id),
    };
  }

  // 责任矩阵行：业务部门 + 其真实事实（负责人/员工/项目计数）
  const matrixRows = useMemo(
    () => companyDepartments.map((department) => ({ department, ...departmentFacts(department) })),
    [companyDepartments, companyEmployees, companyProjects]
  );

  async function removeDepartment() {
    if (!deleteTarget) return;
    setError("");
    try {
      await deleteDepartment(deleteTarget.id);
      setDeleteTarget(null);
      setNotice(`已删除业务部门「${deleteTarget.name}」`);
      await loadAll();
    } catch (err) {
      setDeleteTarget(null);
      setError(err?.message || "业务部门删除失败");
    }
  }

  if (loading) {
    return (
      <TerraShell topCrumb="AI 团队办公室">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }

  if (error && companies.length === 0) {
    return (
      <TerraShell topCrumb="AI 团队办公室">
        <TerraErrorState message={error} onRetry={loadAll} />
      </TerraShell>
    );
  }

  return (
    <TerraShell topCrumb="AI 团队办公室">
      <TerraPageHead
        title="AI 团队办公室"
        subtitle="在这里看到谁正在工作、谁在等待交接，以及哪间办公室需要 CEO 介入。"
        pill={{ text: company ? "本地 Workspace" : "尚未初始化", icon: "i-groups" }}
        facts={[
          { value: companyDepartments.length, label: "业务部门" },
          { value: companyEmployees.length, label: "员工" },
          { value: companyProjects.length, label: "项目" },
        ]}
        actions={
          <TerraButton
            icon="i-add"
            onClick={() => company ? setDepartmentForm(null) : setCompanyForm(null)}
          >
            {company ? "创建业务部门" : "初始化 Workspace"}
          </TerraButton>
        }
      />

      {(notice || error) && (
        <div className={`mb-3 flex items-center gap-2 rounded-ui-sm px-4 py-2.5 text-xs font-medium ${
          error ? "bg-ui-red-soft text-ui-red" : "bg-ui-green-soft text-ui-green"
        }`}>
          <TerraIcon name={error ? "i-warning" : "i-check_circle"} className="w-4 h-4" />
          {error || notice}
        </div>
      )}

      {/* AI Workforce Map — 对齐原型 ai-organization 的团队结构层级 */}
      <TerraCard className="mb-3.5">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <TerraCardHeader icon="i-account_tree" iconClass="primary" title="AI Workforce Map" />
          <span className="text-ui-1 text-ui-txt-3">部门与员工来自当前 Workspace 真实记录</span>
        </div>
        {company ? (
          <div className="mt-1 space-y-4">
            <OrgLevel label="公司">
              <OrgNode
                avatar={company.name}
                name={company.name}
                role={company.description || DATA_COPY.noData}
                status={
                  <TerraTag color={company.status === "active" ? "green" : "grey"}>
                    {STATUS_LABEL[company.status] || company.status}
                  </TerraTag>
                }
                extra={
                  <>
                    {company.is_default && <TerraTag color="primary">主公司</TerraTag>}
                    <TerraButton size="sm" variant="ghost" icon="i-edit" onClick={() => setCompanyForm(company)}>
                      编辑公司
                    </TerraButton>
                  </>
                }
              />
            </OrgLevel>

            <OrgLevel label="业务部门">
              {companyDepartments.length === 0 ? (
                <TerraEmpty icon="i-apartment" className="w-full">尚未创建业务部门</TerraEmpty>
              ) : (
                companyDepartments.map((department) => {
                  const facts = departmentFacts(department);
                  return (
                    <OrgNode
                      key={department.id}
                      avatar={department.name}
                      name={
                        <Link
                          href={`/ceo-office/organization/departments/${department.id}`}
                          className="inline-flex items-center min-h-[32px] min-w-[32px] font-ui-sans font-semibold text-ui-txt no-underline hover:text-ui-primary"
                        >
                          {department.name}
                        </Link>
                      }
                      role={department.mission || DATA_COPY.noData}
                      status={
                        <TerraTag color={department.status === "active" ? "green" : "grey"}>
                          {STATUS_LABEL[department.status] || department.status}
                        </TerraTag>
                      }
                      extra={
                        <span className="text-ui-1 text-ui-txt-3">
                          员工 {facts.employeeCount} · 项目 {facts.projectCount}
                        </span>
                      }
                    />
                  );
                })
              )}
            </OrgLevel>

            <OrgLevel label="AI 员工">
              {companyEmployees.length === 0 ? (
                <TerraEmpty icon="i-person_off" className="w-full">当前公司暂无员工</TerraEmpty>
              ) : (
                <>
                  {companyEmployees.slice(0, 8).map((employee) => (
                    <OrgNode
                      key={employee.id}
                      avatar={employee.name}
                      name={employee.name}
                      role={employee.role || DATA_COPY.unassigned}
                      status={
                        <TerraTag color={employee.enabled ? "green" : "grey"}>
                          {employee.enabled ? "在岗" : "停用"}
                        </TerraTag>
                      }
                    />
                  ))}
                  {companyEmployees.length > 8 && (
                    <Link
                      href="/ceo-office/organization/employees"
                      className="inline-flex items-center self-center min-h-[32px] px-3 text-xs font-bold text-ui-primary no-underline hover:opacity-80"
                    >
                      查看全部 {companyEmployees.length} 名员工 →
                    </Link>
                  )}
                </>
              )}
            </OrgLevel>
          </div>
        ) : (
          <TerraEmpty icon="i-domain">尚未创建公司 · 点击右上角创建</TerraEmpty>
        )}
      </TerraCard>

      {/* 责任矩阵 + 升级队列/组织异常 — 对齐原型 grid-2 双栏 */}
      <div className="grid grid-cols-12 gap-3.5">
        <TerraCard className="col-span-12 lg:col-span-8">
          <div className="flex items-start justify-between gap-2">
            <TerraCardHeader icon="i-groups" iconClass="primary" title="责任矩阵" />
            <TerraButton
              icon="i-add"
              variant="ghost"
              onClick={() => setDepartmentForm(null)}
              disabled={!company}
            >
              创建业务部门
            </TerraButton>
          </div>
          <TerraTable
            caption="业务部门责任矩阵"
            columns={[
              {
                key: "department",
                label: "岗位",
                render: (row) => (
                  <div className="min-w-[160px]">
                    <Link
                      href={`/ceo-office/organization/departments/${row.department.id}`}
                      className="inline-flex items-center min-h-[32px] min-w-[32px] font-semibold text-ui-txt no-underline hover:text-ui-primary"
                    >
                      {row.department.name}
                    </Link>
                    <div className="text-ui-1 text-ui-txt-3 line-clamp-2">
                      {row.department.mission || DATA_COPY.noData}
                    </div>
                  </div>
                ),
              },
              {
                key: "manager",
                label: "结果责任",
                render: (row) => row.manager?.name || DATA_COPY.noOwner,
              },
              { key: "employeeCount", label: "员工" },
              { key: "projectCount", label: "项目" },
              {
                key: "status",
                label: "状态",
                render: (row) => (
                  <TerraTag color={row.department.status === "active" ? "green" : "grey"}>
                    {STATUS_LABEL[row.department.status] || row.department.status}
                  </TerraTag>
                ),
              },
              {
                key: "actions",
                label: "操作",
                render: (row) => (
                  <div className="flex gap-1 whitespace-nowrap">
                    <TerraButton size="sm" variant="ghost" onClick={() => setDepartmentForm(row.department)}>
                      编辑
                    </TerraButton>
                    <TerraButton size="sm" variant="ghost" onClick={() => setDeleteTarget({ ...row.department, ...row })}>
                      删除
                    </TerraButton>
                  </div>
                ),
              },
            ]}
            rows={matrixRows}
            rowKey={(row) => row.department.id}
            empty="尚未创建业务部门"
          />
        </TerraCard>

        <div className="col-span-12 flex flex-col gap-3.5 lg:col-span-4">
          <TerraCard>
            <div className="flex items-start justify-between gap-2">
              <TerraCardHeader icon="i-flag" iconClass="amber" title="升级队列" />
              <TerraTag color="grey" className="mt-1">{DATA_COPY.unsynced}</TerraTag>
            </div>
            <TerraEmpty icon="i-flag">
              升级队列尚未同步 · 接入运行端点后显示待 CEO 处理事项
            </TerraEmpty>
          </TerraCard>

          <TerraCard>
            <div className="flex items-start justify-between gap-2">
              <TerraCardHeader icon="i-warning" iconClass="red" title="组织异常" />
              <span className="mt-1 text-ui-1 text-ui-txt-3">需 CEO 关注或决策</span>
            </div>
            <TerraEmpty icon="i-warning">
              组织异常未读取 · 当前无异常判定事实
            </TerraEmpty>
          </TerraCard>
        </div>
      </div>

      {/* 能力与容量 — 对齐原型 capacity 卡；只展示真实计数，不填假百分比 */}
      <TerraCard className="mt-3.5">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <TerraCardHeader icon="i-activity_zone" iconClass="cyan" title="能力与容量" />
          <span className="text-ui-1 text-ui-txt-3">容量百分比未接入运行端点 · 显示未读取事实</span>
        </div>
        <div className="grid grid-cols-1 gap-3.5 md:grid-cols-3">
          <CapacityItem
            label="AI 团队在岗"
            value={company ? `${activeEmployeeCount} / ${companyEmployees.length}` : DATA_COPY.noData}
            note="来自员工记录 · enabled 在岗"
          />
          <CapacityItem
            label="业务部门"
            value={company ? companyDepartments.length : DATA_COPY.noData}
            note="当前 Workspace 业务部门"
          />
          <CapacityItem
            label="项目"
            value={company ? companyProjects.length : DATA_COPY.noData}
            note="当前 Workspace 项目"
          />
        </div>
      </TerraCard>

      {/* 能力资产库 — 对齐原型 ai-organization.html §能力资产库。
          原型把能力管理落在 AI 团队页（而非独立导航栏目），此卡是能力中心的正式入口。 */}
      <TerraCard className="mt-3.5">
        <div className="flex flex-wrap items-start justify-between gap-2">
          <TerraCardHeader icon="i-dataset" iconClass="violet" title="能力资产库" />
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-ui-1 text-ui-txt-3">
              本地配置 · 模型 / AI 员工 / 技能 / 工具 / 连接器
            </span>
            <Link
              href="/ceo-office/capabilities"
              className="inline-flex items-center justify-center gap-1.5 rounded-ui-sm text-ui-1 font-bold leading-none transition-colors bg-ui-primary text-ui-primary-fg hover:bg-ui-primary-dark px-3 py-2 no-underline"
            >
              <TerraIcon name="i-add" className="w-4 h-4" />
              添加能力
            </Link>
          </div>
        </div>

        {capLoading ? (
          <TerraEmpty icon="i-dataset">能力资产读取中…</TerraEmpty>
        ) : capAssets.length === 0 ? (
          <TerraEmpty icon="i-dataset">
            还没有接入能力。去「能力中心」把模型 / AI 员工 / 技能 / 工具 / 连接器 加进来，再绑定到 AI 员工。
          </TerraEmpty>
        ) : (
          <div className="grid grid-cols-1 gap-2.5 md:grid-cols-2">
            {capAssets.map((item) => (
              <div
                key={item.key}
                className="flex items-start justify-between gap-3 rounded-ui-md border border-ui-line-2 bg-ui-surface-2 px-3.5 py-3"
              >
                <div className="min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-ui-sans font-semibold text-ui-3 text-ui-txt truncate">
                      {item.name}
                    </span>
                    <TerraTag color={item.typeColor}>{item.typeLabel}</TerraTag>
                  </div>
                  <p className="text-ui-1 text-ui-txt-3 mt-1 truncate">{item.meta}</p>
                  <p className="text-ui-1 text-ui-txt-3 mt-0.5 truncate">
                    凭证：{item.credential || "未设置"}
                  </p>
                </div>
                <TerraTag color={item.enabled ? "green" : "grey"}>
                  {item.enabled ? "已启用" : "已停用"}
                </TerraTag>
              </div>
            ))}
          </div>
        )}
      </TerraCard>

      <div className="mt-3.5">
        <TerraBoundary>所有组织卡片均来自当前 Workspace 的真实业务部门、员工与项目记录。</TerraBoundary>
      </div>

      <CompanyFormDrawer
        open={companyForm !== undefined}
        company={companyForm || null}
        onClose={() => setCompanyForm(undefined)}
        onSuccess={(saved) => {
          setCompanyForm(undefined);
          setSelectedCompanyId(saved.company_id);
          setNotice(`公司「${saved.name}」已保存`);
          loadAll();
        }}
      />
      <DepartmentFormDrawer
        open={departmentForm !== undefined}
        department={departmentForm || null}
        companyId={selectedCompanyId}
        templates={templates}
        existingDepts={companyDepartments}
        onClose={() => setDepartmentForm(undefined)}
        onSuccess={(saved) => {
          setDepartmentForm(undefined);
          setNotice(`业务部门「${saved.name}」已保存`);
          loadAll();
        }}
      />
      <TerraConfirmDialog
        open={!!deleteTarget}
        title={`删除「${deleteTarget?.name || ""}」？`}
        description="删除前必须先转移该业务部门的员工和项目。"
        disabledReason={
          deleteTarget && (deleteTarget.employeeCount || deleteTarget.projectCount)
            ? `当前仍有 ${deleteTarget.employeeCount} 名员工、${deleteTarget.projectCount} 个项目`
            : undefined
        }
        onConfirm={removeDepartment}
        onClose={() => setDeleteTarget(null)}
      />
    </TerraShell>
  );
}

export default OrganizationCenter;
