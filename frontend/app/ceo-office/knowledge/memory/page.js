"use client";

import { Suspense, useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import TerraShell from "../../../../components/terra/TerraShell.js";
import {
  TerraButton,
  TerraCard,
  TerraDrawer,
  TerraPageHead,
  TerraSearch,
  TerraTag,
} from "../../../../components/terra/TerraPrimitives.js";
import {
  TerraEmptyState,
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../../components/terra/TerraState.js";
import { getEmployees, getProjects } from "../../../../lib/api.js";
import {
  createMemoryEntry,
  getMemoryEntries,
  updateMemoryEntry,
} from "../../../../lib/memory.js";

const TYPES = [
  { key: "all", label: "全部 Memory" },
  { key: "user", label: "用户 Memory" },
  { key: "project", label: "项目 Memory" },
  { key: "employee", label: "员工 Memory" },
];

const EMPTY_FORM = {
  memory_type: "user",
  target_id: "",
  title: "",
  content: "",
  tags: "",
  confidence: "1",
};

const TYPE_LABELS = {
  user: "用户 Memory",
  project: "项目 Memory",
  employee: "员工 Memory",
};

function tagsFrom(value) {
  return value.split(/[,，]/).map((item) => item.trim()).filter(Boolean);
}

function MemoryInner() {
  const searchParams = useSearchParams();
  const scope = searchParams.get("scope") || "all";
  const [entries, setEntries] = useState([]);
  const [projects, setProjects] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [editingId, setEditingId] = useState("");
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const memoryPayload = await getMemoryEntries({ query, scope });
      const projectPayload = await getProjects();
      const employeePayload = await getEmployees();
      setEntries(memoryPayload?.entries || []);
      setProjects(projectPayload?.projects || []);
      setEmployees(employeePayload?.employees || []);
    } catch (err) {
      setError(err?.message || "Memory 读取失败");
    } finally {
      setLoading(false);
    }
  }, [query, scope]);

  useEffect(() => { load(); }, [load]);

  const targets = useMemo(() => {
    if (form.memory_type === "project") {
      return projects.map((item) => ({ id: item.project_id, name: item.name }));
    }
    if (form.memory_type === "employee") {
      return employees.map((item) => ({ id: item.id, name: item.name }));
    }
    return [];
  }, [employees, form.memory_type, projects]);

  function openCreate() {
    setEditingId("");
    setForm(EMPTY_FORM);
    setFormError("");
    setDrawerOpen(true);
  }

  function openEdit(entry) {
    setEditingId(entry.id);
    setForm({
      memory_type: entry.memory_type,
      target_id: entry.project_id || entry.employee_id || "",
      title: entry.title,
      content: entry.content,
      tags: (entry.tags || []).join(","),
      confidence: String(entry.confidence),
    });
    setFormError("");
    setDrawerOpen(true);
  }

  function setType(memoryType) {
    const options = memoryType === "project" ? projects : memoryType === "employee" ? employees : [];
    const targetId = options[0]?.project_id || options[0]?.id || "";
    setForm((current) => ({ ...current, memory_type: memoryType, target_id: targetId }));
  }

  async function submit(event) {
    event.preventDefault();
    setFormError("");
    if (!form.title.trim() || !form.content.trim()) {
      setFormError("请填写 Memory 标题和内容");
      return;
    }
    if (form.memory_type !== "user" && !form.target_id) {
      setFormError("请选择 Memory 归属");
      return;
    }
    setSubmitting(true);
    const values = {
      title: form.title.trim(),
      content: form.content.trim(),
      tags: tagsFrom(form.tags),
      confidence: Number(form.confidence),
    };
    try {
      if (editingId) {
        await updateMemoryEntry(editingId, values);
      } else {
        await createMemoryEntry({
          ...values,
          memory_type: form.memory_type,
          project_id: form.memory_type === "project" ? form.target_id : null,
          employee_id: form.memory_type === "employee" ? form.target_id : null,
        });
      }
      setDrawerOpen(false);
      await load();
    } catch (err) {
      setFormError(err?.message || "Memory 保存失败");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading && entries.length === 0) {
    return (
      <TerraShell topCrumb="知识中心 / 记忆管理">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (error && entries.length === 0) {
    return (
      <TerraShell topCrumb="知识中心 / 记忆管理">
        <TerraErrorState message={error} onRetry={load} />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="知识中心 / 记忆管理"
      topbarExtra={(
        <TerraSearch
          placeholder="搜索经验、规则或标签…"
          value={query}
          onChange={setQuery}
        />
      )}
    >
      <TerraPageHead
        title="记忆管理"
        subtitle="保存经用户确认、未来仍有价值的工作经验。Memory 不等于资料或执行日志。"
        pill={{ text: `${entries.length} 条 Memory`, icon: "i-memory" }}
        actions={<TerraButton onClick={openCreate}>新建 Memory</TerraButton>}
      />

      <div className="mb-4 flex items-center gap-2 overflow-x-auto pb-1 no-h-scroll">
        {TYPES.map((item) => (
          <a
            key={item.key}
            href={`/ceo-office/knowledge/memory${item.key === "all" ? "" : `?scope=${item.key}`}`}
            className={`inline-flex items-center whitespace-nowrap rounded-full px-3 py-1.5 text-xs font-medium no-underline ${
              scope === item.key
                ? "bg-ui-primary text-ui-primary-fg"
                : "bg-ui-surface-2 text-ui-txt-2"
            }`}
          >
            {item.label}
          </a>
        ))}
      </div>

      {error && <p className="mb-3 text-xs text-ui-red">{error}</p>}
      {entries.length === 0 ? (
        <TerraCard>
          <TerraEmptyState
            icon="i-memory"
            title="暂无已确认 Memory"
            description="完成任务后确认沉淀经验，或手工保存第一条长期规则。"
          />
        </TerraCard>
      ) : (
        <div className="grid grid-cols-1 gap-3.5 md:grid-cols-2">
          {entries.map((entry) => (
            <TerraCard key={entry.id}>
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <h3 className="font-ui-sans text-ui-4 font-semibold text-ui-txt">
                    {entry.title}
                  </h3>
                  <p className="mt-2 whitespace-pre-wrap text-xs leading-relaxed text-ui-txt-2">
                    {entry.content}
                  </p>
                </div>
                <TerraTag color={entry.memory_type === "project" ? "green" : "violet"}>
                  {TYPE_LABELS[entry.memory_type] || entry.memory_type}
                </TerraTag>
              </div>
              <div className="mt-3 flex flex-wrap gap-1.5">
                <TerraTag color="grey">{entry.memory_level}</TerraTag>
                <TerraTag color="grey">{entry.scope_name || "未记录"}</TerraTag>
                {(entry.tags || []).map((tag) => (
                  <TerraTag key={tag} color="violet">{tag}</TerraTag>
                ))}
              </div>
              <dl className="mt-3 grid grid-cols-2 gap-2 text-ui-1 text-ui-txt-3">
                <div>
                  <dt>来源</dt>
                  <dd className="mt-0.5 text-ui-txt-2">
                    {entry.source_type === "task" ? entry.source_task_title || "Task" : "手工确认"}
                  </dd>
                </div>
                <div>
                  <dt>可信度</dt>
                  <dd className="mt-0.5 text-ui-txt-2">{Math.round(entry.confidence * 100)}%</dd>
                </div>
                <div>
                  <dt>使用次数</dt>
                  <dd className="mt-0.5 text-ui-txt-2">{entry.use_count}</dd>
                </div>
                <div>
                  <dt>最后使用</dt>
                  <dd className="mt-0.5 text-ui-txt-2">{entry.last_used_at || "未使用"}</dd>
                </div>
              </dl>
              <div className="mt-3 flex items-center justify-between gap-3">
                <span className="text-ui-1 text-ui-txt-3">
                  更新于 {entry.updated_at || "未记录"}
                </span>
                <TerraButton variant="ghost" onClick={() => openEdit(entry)}>编辑</TerraButton>
              </div>
            </TerraCard>
          ))}
        </div>
      )}

      <TerraDrawer
        open={drawerOpen}
        title={editingId ? "编辑 Memory" : "新建 Memory"}
        description="只保存长期有效的偏好、决策、方法或问题解决经验。"
        onClose={() => setDrawerOpen(false)}
      >
        <form onSubmit={submit} className="space-y-4">
          {!editingId && (
            <SelectField
              id="memory-type"
              label="Memory 类型"
              value={form.memory_type}
              onChange={setType}
              options={[
                { id: "user", name: "用户 Memory" },
                { id: "project", name: "项目 Memory" },
                { id: "employee", name: "员工 Memory" },
              ]}
            />
          )}
          {!editingId && form.memory_type !== "user" && (
            <SelectField
              id="memory-target"
              label={form.memory_type === "project" ? "项目" : "员工"}
              value={form.target_id}
              onChange={(value) => setForm((current) => ({ ...current, target_id: value }))}
              options={targets}
              emptyLabel={form.memory_type === "project" ? "暂无可用项目" : "暂无可用员工"}
            />
          )}
          <TextField
            id="memory-title"
            label="标题"
            value={form.title}
            onChange={(value) => setForm((current) => ({ ...current, title: value }))}
            placeholder="例如：发布验收原则"
          />
          <div>
            <label htmlFor="memory-content" className="mb-1.5 block text-xs font-bold text-ui-txt-2">
              Memory 内容 *
            </label>
            <textarea
              id="memory-content"
              rows={8}
              value={form.content}
              onChange={(event) => setForm((current) => ({ ...current, content: event.target.value }))}
              placeholder="记录未来仍有价值的经验，不要粘贴执行日志"
              className="w-full resize-y rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
            />
          </div>
          <TextField
            id="memory-tags"
            label="标签"
            value={form.tags}
            onChange={(value) => setForm((current) => ({ ...current, tags: value }))}
            placeholder="用逗号分隔，最多 10 个"
            required={false}
          />
          <SelectField
            id="memory-confidence"
            label="可信度"
            value={form.confidence}
            onChange={(value) => setForm((current) => ({ ...current, confidence: value }))}
            options={[
              { id: "1", name: "100% · 已确认" },
              { id: "0.8", name: "80% · 较可信" },
              { id: "0.6", name: "60% · 待验证" },
            ]}
          />
          {formError && <p className="text-xs text-ui-red">{formError}</p>}
          <div className="flex justify-end gap-3 pt-2">
            <TerraButton type="button" variant="ghost" onClick={() => setDrawerOpen(false)}>
              取消
            </TerraButton>
            <TerraButton type="submit" disabled={submitting}>
              {submitting ? "保存中…" : "保存 Memory"}
            </TerraButton>
          </div>
        </form>
      </TerraDrawer>
    </TerraShell>
  );
}

function SelectField({ id, label, value, onChange, options, emptyLabel }) {
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-xs font-bold text-ui-txt-2">
        {label} *
      </label>
      <select
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
      >
        {options.length === 0 && <option value="">{emptyLabel}</option>}
        {options.map((item) => (
          <option key={item.id} value={item.id}>{item.name}</option>
        ))}
      </select>
    </div>
  );
}

function TextField({ id, label, value, onChange, placeholder, required = true }) {
  return (
    <div>
      <label htmlFor={id} className="mb-1.5 block text-xs font-bold text-ui-txt-2">
        {label}{required ? " *" : ""}
      </label>
      <input
        id={id}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none"
      />
    </div>
  );
}

export default function MemoryPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-ui-bg" />}>
      <MemoryInner />
    </Suspense>
  );
}
