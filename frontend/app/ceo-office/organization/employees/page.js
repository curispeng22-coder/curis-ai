"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import TerraShell from "../../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../../components/terra/TerraIcons.js";
import {
  TerraButton,
  TerraCard,
  TerraEmpty,
  TerraBoundary,
  TerraPageHead,
  TerraSearch,
  TerraBackLink,
  EmployeeCard,
} from "../../../../components/terra/TerraPrimitives.js";
import { TerraErrorState, TerraLoadingSkeleton } from "../../../../components/terra/TerraState.js";
import {
  deleteEmployee,
  getCapabilitySelector,
  getDepartments,
  getEmployeeCapabilities,
  getEmployees,
  getEmployeeTemplates,
} from "../../../../lib/api.js";
import EmployeeFormDrawer from "./EmployeeFormDrawer.js";
import TerraConfirmDialog from "../../../../components/terra/TerraConfirm.js";

const FILTER_TABS = [
  { key: "all", label: "全部" },
  { key: "idle", label: "空闲" },
  { key: "assigned", label: "工作中" },
  { key: "completed", label: "已完成" },
  { key: "error", label: "异常" },
  { key: "disabled", label: "已暂停" },
];

function selectorKey(item) {
  return `${item.source}:${item.capability_type}:${item.capability_id}`;
}

function uniqueCapabilities(items = []) {
  const result = [];
  const seen = new Set();
  for (const item of items) {
    if (!item?.enabled || !["model", "tool", "connector"].includes(item.capability_type)) continue;
    const key = selectorKey(item);
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(item);
  }
  return result;
}

export default function EmployeesPage() {
  const [employees, setEmployees] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [capabilities, setCapabilities] = useState([]);
  const [profiles, setProfiles] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [filterTab, setFilterTab] = useState("all");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const loadAll = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const employeePayload = await getEmployees();
      const departmentPayload = await getDepartments();
      const templatePayload = await getEmployeeTemplates();
      const capabilityPayload = await getCapabilitySelector();
      const employeeRows = employeePayload?.employees || [];
      const nextProfiles = {};
      for (const employee of employeeRows) {
        try {
          const profile = await getEmployeeCapabilities(employee.id);
          nextProfiles[employee.id] = profile?.bindings || [];
        } catch (_error) {
          nextProfiles[employee.id] = [];
        }
      }
      setEmployees(employeeRows);
      setDepartments(departmentPayload?.departments || []);
      setTemplates(templatePayload?.employee_templates || []);
      setCapabilities(uniqueCapabilities(capabilityPayload?.capabilities));
      setProfiles(nextProfiles);
    } catch (err) {
      setError(err?.message || "员工数据读取失败");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadAll(); }, [loadAll]);

  const departmentNames = useMemo(
    () => Object.fromEntries(departments.map((item) => [item.id, item.name])),
    [departments]
  );
  const roleNames = useMemo(
    () => Object.fromEntries(templates.map((item) => [item.role, item.name])),
    [templates]
  );
  const capabilityNames = useMemo(
    () => Object.fromEntries(capabilities.map((item) => [selectorKey(item), item.label])),
    [capabilities]
  );

  const filteredEmployees = useMemo(() => {
    let list = employees;
    if (filterTab !== "all") list = list.filter((item) => item.status === filterTab);
    if (!searchQuery.trim()) return list;
    const query = searchQuery.trim().toLowerCase();
    return list.filter((item) =>
      (item.name || "").toLowerCase().includes(query)
      || (roleNames[item.role] || item.role || "").toLowerCase().includes(query)
      || (departmentNames[item.department_id] || "").toLowerCase().includes(query)
    );
  }, [departmentNames, employees, filterTab, roleNames, searchQuery]);

  async function confirmDelete() {
    if (!deleteTarget) return;
    setDeleting(true);
    setError("");
    try {
      await deleteEmployee(deleteTarget.id);
      setNotice(`已移除员工「${deleteTarget.name}」`);
      setDeleteTarget(null);
      await loadAll();
    } catch (err) {
      setError(err?.message || "员工移除失败");
      setDeleteTarget(null);
    } finally {
      setDeleting(false);
    }
  }

  if (loading) {
    return (
      <TerraShell topCrumb="组织中心 / 员工管理">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }

  if (error && employees.length === 0) {
    return (
      <TerraShell topCrumb="组织中心 / 员工管理">
        <TerraErrorState message={error} onRetry={loadAll} />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="组织中心 / 员工管理"
      topbarExtra={(
        <TerraSearch
          placeholder="搜索员工…"
          value={searchQuery}
          onChange={setSearchQuery}
          className="hidden sm:flex"
        />
      )}
    >
      <div>
        <TerraBackLink href="/ceo-office/organization">返回组织中心</TerraBackLink>

        <TerraPageHead
          title="AI 员工"
          subtitle="按业务部门管理员工职责、能力配置档案与当前状态。"
          pill={{ text: `共 ${employees.length} 名员工`, icon: "i-person" }}
          facts={[
            { value: employees.filter((item) => item.status !== "disabled").length, label: "可用员工" },
            { value: employees.filter((item) => item.status === "assigned").length, label: "工作中" },
          ]}
          actions={(
            <TerraButton icon="i-add" onClick={() => setDrawerOpen(true)}>
              创建员工
            </TerraButton>
          )}
        />

        {notice && (
          <div className="mb-3 flex items-center gap-2 bg-ui-green-soft border border-ui-green/20 rounded-ui-sm px-4 py-2.5 text-xs font-medium text-ui-green">
            <TerraIcon name="i-check_circle" className="w-4 h-4" />
            {notice}
          </div>
        )}
        {error && (
          <div className="mb-3 flex items-center gap-2 bg-ui-red-soft border border-ui-red/20 rounded-ui-sm px-4 py-2.5 text-xs font-medium text-ui-red">
            <TerraIcon name="i-error" className="w-4 h-4" />
            {error}
          </div>
        )}

        <TerraSearch
          placeholder="搜索员工…"
          value={searchQuery}
          onChange={setSearchQuery}
          className="sm:hidden w-full mb-3"
        />

        <div className="flex flex-wrap gap-1.5 mb-4" aria-label="员工状态筛选">
          {FILTER_TABS.map((tab) => (
            <button
              key={tab.key}
              type="button"
              onClick={() => setFilterTab(tab.key)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                filterTab === tab.key
                ? "bg-ui-primary text-ui-primary-fg"
                : "bg-ui-surface-2 text-ui-txt-2 hover:bg-ui-surface-3"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        <div className="grid grid-cols-12 gap-3.5">
          <TerraCard className="col-span-12">
            {filteredEmployees.length === 0 ? (
              <TerraEmpty icon="i-person_off">
                {searchQuery || filterTab !== "all"
                  ? "没有符合当前条件的员工"
                  : "暂无员工。创建第一个 AI 员工后会显示在这里。"}
              </TerraEmpty>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {filteredEmployees.map((employee) => {
                  const profile = profiles[employee.id] || [];
                  const profileLabels = profile.map((binding) =>
                    capabilityNames[
                      `${binding.capability_source}:${binding.capability_type}:${binding.capability_id}`
                    ] || binding.capability_id
                  );
                  return (
                    <EmployeeCard
                      key={employee.id}
                      employee={{
                        ...employee,
                        role: roleNames[employee.role] || employee.role,
                        capabilityProfile: profileLabels.join("、"),
                      }}
                      department={departmentNames[employee.department_id]}
                      project={null}
                      actions={(
                        <>
                          <a
                            href={`/ceo-office/organization/employees/${employee.id}`}
                            className="px-2.5 py-1 rounded-ui-sm text-ui-1 font-bold border border-ui-line-2 bg-ui-surface text-ui-txt-2 hover:border-ui-primary hover:text-ui-primary transition-colors no-underline"
                          >
                            详情
                          </a>
                          <button
                            type="button"
                            className="px-2.5 py-1 rounded-ui-sm text-ui-1 font-bold border border-ui-red/30 text-ui-red hover:bg-ui-red-soft transition-colors"
                            onClick={() => setDeleteTarget({ id: employee.id, name: employee.name })}
                          >
                            移除
                          </button>
                        </>
                      )}
                    />
                  );
                })}
              </div>
            )}
          </TerraCard>

          <div className="col-span-12">
            <TerraBoundary>
              员工主归属业务部门；职责与能力配置档案可按员工调整。
            </TerraBoundary>
          </div>
        </div>

        <EmployeeFormDrawer
          open={drawerOpen}
          departments={departments}
          templates={templates}
          capabilities={capabilities}
          onClose={() => setDrawerOpen(false)}
          onSuccess={async (employee) => {
            setNotice(`已创建员工「${employee.name}」`);
            setDrawerOpen(false);
            await loadAll();
          }}
        />

        <TerraConfirmDialog
          open={!!deleteTarget}
          title={`确定移除「${deleteTarget?.name || ""}」？`}
          description="员工将被软删除；如果员工是部门负责人，系统会要求先调整负责人。"
          dangerText={deleting ? "移除中…" : "确认移除"}
          onConfirm={confirmDelete}
          onClose={() => !deleting && setDeleteTarget(null)}
        />
      </div>
    </TerraShell>
  );
}
