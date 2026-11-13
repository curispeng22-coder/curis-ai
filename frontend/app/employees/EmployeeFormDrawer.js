"use client";

// 员工新增/编辑抽屉（从 employees/page.js 抽出并增强）。
// 支持「多归属选择器」：多行「部门 + 项目」组合；提交时由父组件分两步
// 写 employees 与 employee-affiliations（replace-all）。复用 ceo-office 抽屉样式。

import { useMemo, useState } from "react";
import { STYLE, ROLE_LABELS, DEPT_TYPE_LABELS } from "../../lib/theme.js";

function uniqueTemplates(templates) {
  const seen = new Set();
  return (templates || []).filter((t) => {
    if (seen.has(t.slug)) return false;
    seen.add(t.slug);
    return true;
  });
}

export default function EmployeeFormDrawer({
  mode,
  employee,
  departments = [],
  employeeTemplates = [],
  projects = [],
  affiliations = [],
  submitting = false,
  onSave,
  onClose,
}) {
  const isEdit = mode === "edit";

  const [form, setForm] = useState({
    department_id: employee?.department_id || "",
    template_id: employee?.template_id || "",
    name: employee?.name || "",
    status: employee?.status || "idle",
    enabled: employee?.enabled ?? true,
    instructions_override: employee?.instructions_override || "",
  });

  // 多归属行：{ department_id, project_id }
  const [rows, setRows] = useState(() => {
    const initial = (affiliations || []).map((a) => ({
      department_id: a.department_id || "",
      project_id: a.project_id || "",
    }));
    return initial.length ? initial : [{ department_id: "", project_id: "" }];
  });

  const templates = useMemo(() => uniqueTemplates(employeeTemplates), [employeeTemplates]);

  function update(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function updateRow(index, field, value) {
    setRows((prev) => prev.map((r, i) => (i === index ? { ...r, [field]: value } : r)));
  }

  function addRow() {
    setRows((prev) => [...prev, { department_id: "", project_id: "" }]);
  }

  function removeRow(index) {
    setRows((prev) => (prev.length > 1 ? prev.filter((_, i) => i !== index) : prev));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.name.trim()) {
      alert("请输入员工姓名");
      return;
    }
    if (!isEdit && !form.department_id) {
      alert("请选择部门");
      return;
    }
    if (!isEdit && !form.template_id) {
      alert("请选择员工模板");
      return;
    }

    const base = {};
    if (!isEdit) {
      base.department_id = form.department_id;
      base.template_id = form.template_id;
      base.name = form.name.trim();
      base.status = form.status;
      base.enabled = form.enabled;
      base.instructions_override = form.instructions_override || "";
    } else {
      if (form.name.trim() !== undefined && form.name.trim() !== (employee?.name || ""))
        base.name = form.name.trim();
      if ((form.instructions_override || "") !== (employee?.instructions_override || ""))
        base.instructions_override = form.instructions_override;
      if (form.status !== employee?.status) base.status = form.status;
      if (form.enabled !== employee?.enabled) base.enabled = form.enabled;
    }

    // 构建多归属（去重）：创建时含主部门；编辑时含员工主部门，保证一致。
    const affSet = new Map();
    const addAff = (d, p) => {
      const dept = (d || "").trim();
      const proj = (p || "").trim();
      if (!dept && !proj) return;
      affSet.set(`${dept}::${proj}`, { department_id: dept, project_id: proj });
    };
    if (!isEdit && form.department_id) addAff(form.department_id, "");
    if (isEdit && employee?.department_id) addAff(employee.department_id, "");
    for (const row of rows) addAff(row.department_id, row.project_id);
    const builtAffiliations = Array.from(affSet.values());

    if (!isEdit && builtAffiliations.length === 0) {
      alert("请至少选择一个归属部门");
      return;
    }

    await onSave({ base, affiliations: builtAffiliations });
  }

  return (
    <div style={STYLE.overlay} onClick={onClose}>
      <div style={STYLE.drawer} onClick={(e) => e.stopPropagation()}>
        <div style={{ marginBottom: "var(--ui-sp-6)" }}>
          <p className="ceo-kicker">{isEdit ? "编辑员工" : "新增员工"}</p>
          <h3 style={{ color: "var(--ui-text)", margin: 0, fontSize: "var(--ui-fs-5)" }}>
            {isEdit ? `编辑 · ${employee?.name || ""}` : "创建新员工"}
          </h3>
        </div>

        <form onSubmit={handleSubmit}>
          {!isEdit && (
            <>
              <label style={STYLE.formLabel}>
                部门（主部门） *
                <select
                  value={form.department_id}
                  onChange={(e) => update("department_id", e.target.value)}
                  style={STYLE.select}
                  required
                >
                  <option value="">请选择部门</option>
                  {departments.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name}（{DEPT_TYPE_LABELS[d.department_type] || d.department_type}）
                    </option>
                  ))}
                </select>
              </label>

              <label style={STYLE.formLabel}>
                员工模板 *
                <select
                  value={form.template_id}
                  onChange={(e) => update("template_id", e.target.value)}
                  style={STYLE.select}
                  required
                >
                  <option value="">请选择模板</option>
                  {templates.map((t) => (
                    <option key={t.id} value={t.id}>
                      {ROLE_LABELS[t.slug] || t.name}（{t.department_type || ""}）
                    </option>
                  ))}
                </select>
              </label>
            </>
          )}

          <label style={STYLE.formLabel}>
            姓名 *
            <input
              type="text"
              value={form.name}
              onChange={(e) => update("name", e.target.value)}
              style={STYLE.input}
              placeholder={isEdit ? "" : "例如：晓研"}
              required
            />
          </label>

          <label style={STYLE.formLabel}>
            状态
            <select value={form.status} onChange={(e) => update("status", e.target.value)} style={STYLE.select}>
              <option value="idle">空闲</option>
              <option value="assigned">已分配</option>
              <option value="disabled">已停用</option>
            </select>
          </label>

          <label style={STYLE.checkboxWrap}>
            <input
              type="checkbox"
              checked={form.enabled}
              onChange={(e) => update("enabled", e.target.checked)}
            />
            启用
          </label>

          <label style={STYLE.formLabel}>
            指令覆盖
            <textarea
              value={form.instructions_override}
              onChange={(e) => update("instructions_override", e.target.value)}
              style={STYLE.textarea}
              rows={4}
              placeholder="覆盖官方模板默认指令（可选）"
            />
          </label>

          {/* 多归属选择器 */}
          <div style={{ marginTop: 8, borderTop: "1px solid rgba(117,217,230,0.12)", paddingTop: 16 }}>
            <p style={STYLE.formLabel}>多归属（部门 / 项目，可多行）</p>
            {rows.map((row, index) => (
              <div
                key={index}
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr auto",
                  gap: 8,
                  marginBottom: 10,
                  alignItems: "center",
                }}
              >
                <select
                  value={row.department_id}
                  onChange={(e) => updateRow(index, "department_id", e.target.value)}
                  style={STYLE.select}
                >
                  <option value="">部门（可选）</option>
                  {departments.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name}
                    </option>
                  ))}
                </select>
                <select
                  value={row.project_id}
                  onChange={(e) => updateRow(index, "project_id", e.target.value)}
                  style={STYLE.select}
                >
                  <option value="">项目（可选）</option>
                  {projects.map((p) => (
                    <option key={p.project_id} value={p.project_id}>
                      {p.name}
                    </option>
                  ))}
                </select>
                <button
                  type="button"
                  onClick={() => removeRow(index)}
                  disabled={rows.length <= 1}
                  style={{
                    ...STYLE.btnSmall,
                    border: "1px solid var(--ui-danger)",
                    color: "var(--ui-danger)",
                    background: "transparent",
                    cursor: rows.length <= 1 ? "not-allowed" : "pointer",
                  }}
                >
                  删
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={addRow}
              style={{
                ...STYLE.btnSmall,
                border: "1px solid var(--ui-accent)",
                color: "var(--ui-accent)",
                background: "transparent",
              }}
            >
              + 添加归属
            </button>
          </div>

          {isEdit && (
            <p className="ceo-empty-copy" style={{ fontSize: "var(--ui-fs-1)", margin: "var(--ui-sp-3) 0 0" }}>
              编辑仅支持修改姓名、指令覆盖、状态和启用开关；归属可在此多归属区增删。修改部门请删除后重建。
            </p>
          )}

          <div style={{ display: "flex", gap: 12, justifyContent: "flex-end", marginTop: 24 }}>
            <button type="button" className="ceo-secondary-action" onClick={onClose} disabled={submitting}>
              取消
            </button>
            <button type="submit" className="ceo-primary-action" disabled={submitting}>
              {submitting ? "保存中…" : "保存"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
