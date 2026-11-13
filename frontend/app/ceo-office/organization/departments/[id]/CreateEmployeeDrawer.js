"use client";

import { useEffect, useState } from "react";
import { useLocalDraft, DRAFT_CREATED_TEXT } from "../../../../../lib/useLocalDraft.js";
import { TerraIcon } from "../../../../../components/terra/TerraIcons.js";
import { TerraButton } from "../../../../../components/terra/TerraPrimitives.js";

/**
 * CreateEmployeeDrawer — 在部门内新建员工抽屉（本地草稿模式）。
 *
 * 初始归属锁定为所传部门（deptName）。
 * 不调用 createEmployee POST；提交后仅生成本地草稿。
 *
 * @param {Object} props
 * @param {boolean} props.open
 * @param {string} [props.deptName=""] - 锁定归属部门名
 * @param {string} [props.deptId=""] - 锁定归属部门 ID
 * @param {Function} props.onClose
 * @param {Function} props.onSuccess - (draftName) => void
 */

const EMPTY_FORM = {
  name: "",
  role: "",
  project: "",
};

export default function CreateEmployeeDrawer({ open, deptName = "", deptId = "", onClose, onSuccess }) {
  const { draft, createDraft, reset } = useLocalDraft({ ...EMPTY_FORM, department: deptName, departmentId: deptId });
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  useEffect(() => {
    if (open) {
      reset();
      setErrors({});
      setSubmitted(false);
      setSubmitting(false);
    }
  }, [open, reset]);

  if (!open) return null;

  function validate() {
    const e = {};
    if (!draft.name?.trim()) e.name = "请输入员工名称";
    if (!draft.role?.trim()) e.role = "请选择或输入岗位职责";
    setErrors(e);
    return Object.keys(e).length === 0;
  }

  async function handleSubmit() {
    if (!validate()) return;
    setSubmitting(true);
    await new Promise((resolve) => setTimeout(resolve, 600));
    setSubmitting(false);
    setSubmitted(true);
    onSuccess?.(draft.name);
    setTimeout(() => { setSubmitted(false); onClose(); }, 1800);
  }

  function handleCancel() {
    reset();
    setErrors({});
    setSubmitted(false);
    onClose();
  }

  return (
    <div className="fixed inset-0 z-[1000] flex items-center justify-center p-4 md:p-5" role="dialog" aria-modal="true">
      <div className="absolute inset-0 bg-black/[0.35]" onClick={handleCancel} aria-hidden="true" />

      <div
        className="relative bg-ui-surface border border-ui-line rounded-ui-lg shadow-ui-3 w-full max-w-[520px] max-h-[90vh] overflow-auto outline-none"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="px-6 py-4 border-b border-ui-line flex items-center justify-between">
          <h3 className="font-ui-sans font-semibold text-ui-4 text-ui-txt">在部门内新建员工（本地草稿）</h3>
          <button type="button" onClick={handleCancel} className="p-1 rounded hover:bg-ui-surface-2 transition-colors" aria-label="关闭">
            <svg className="w-5 h-5 fill-current text-ui-txt-3" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>

        {submitted ? (
          <div className="p-8 text-center">
            <div className="w-14 h-14 rounded-full bg-ui-green-soft grid place-items-center mx-auto mb-3">
              <TerraIcon name="i-check_circle" className="w-7 h-7 text-ui-green" />
            </div>
            <h3 className="font-ui-sans font-semibold text-lg text-ui-txt mb-1">{DRAFT_CREATED_TEXT}</h3>
            <p className="text-sm text-ui-txt-3 leading-relaxed">
              「{draft.name}」已保存为本地草稿，初始归属 {deptName || "该部门"}。未接入后端写入。
            </p>
          </div>
        ) : (
          <>
            <div className="px-6 py-5 space-y-4">
              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5 tracking-wide">员工名称 *</label>
                <input
                  type="text"
                  value={draft.name || ""}
                  onChange={(e) => createDraft({ ...draft, name: e.target.value })}
                  placeholder="例如：张三"
                  className={`w-full px-3 py-2 rounded-ui-sm border text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30 ${
                    errors.name ? "border-ui-red" : "border-ui-line"
                  }`}
                />
                {errors.name && <p className="text-ui-1 text-ui-red mt-1">{errors.name}</p>}
              </div>

              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5 tracking-wide">岗位职责 *</label>
                <select
                  value={draft.role || ""}
                  onChange={(e) => createDraft({ ...draft, role: e.target.value })}
                  className={`w-full px-3 py-2 rounded-ui-sm border text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30 ${
                    errors.role ? "border-ui-red" : "border-ui-line"
                  }`}
                >
                  <option value="">选择角色…</option>
                  <option value="frontend_engineer">前端工程师</option>
                  <option value="backend_engineer">后端工程师</option>
                  <option value="product_manager">产品经理</option>
                  <option value="qa_engineer">测试工程师</option>
                  <option value="data_analyst">数据分析师</option>
                  <option value="content_operator">运营专员</option>
                  <option value="researcher">研究员</option>
                </select>
                {errors.role && <p className="text-ui-1 text-ui-red mt-1">{errors.role}</p>}
              </div>

              <div className="bg-ui-primary-soft border border-ui-primary/20 rounded-ui-sm px-3 py-2 text-xs text-ui-primary flex items-center gap-2">
                <TerraIcon name="i-verified" className="w-4 h-4" />
                <span><strong>初始归属：</strong>{deptName || "该部门"}（系统锁定）</span>
              </div>

              <div>
                <label className="block text-xs font-bold text-ui-txt-2 mb-1.5 tracking-wide">关联项目（可选）</label>
                <input
                  type="text"
                  value={draft.project || ""}
                  onChange={(e) => createDraft({ ...draft, project: e.target.value })}
                  placeholder="例如：客户管理系统 v2.0"
                  className="w-full px-3 py-2 rounded-ui-sm border border-ui-line text-sm text-ui-txt bg-ui-surface outline-none focus:ring-2 focus:ring-ui-primary/30"
                />
              </div>
            </div>

            <div className="px-6 py-4 border-t border-ui-line flex justify-end gap-3">
              <button type="button" onClick={handleCancel} className="px-4 py-2 rounded-ui-sm text-xs font-bold border border-ui-line-2 bg-ui-surface text-ui-txt-2 hover:border-ui-primary hover:text-ui-primary transition-colors">
                取消
              </button>
              <TerraButton onClick={handleSubmit} disabled={submitting}>
                {submitting ? "提交中…" : "生成本地草稿"}
              </TerraButton>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
