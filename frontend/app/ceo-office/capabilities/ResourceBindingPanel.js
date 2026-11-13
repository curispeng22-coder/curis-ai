"use client";

import { useState } from "react";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import { TerraButton, TerraTag } from "../../../components/terra/TerraPrimitives.js";
import TerraResourcePicker from "../../../components/terra/TerraResourcePicker.js";

/**
 * ResourceBindingPanel — 能力绑定面板（复用 TerraResourcePicker）。
 *
 * 用于能力中心页面中的资源绑定操作。
 * 选择结果显示作用范围。
 *
 * @param {Object} props
 * @param {boolean} props.open
 * @param {string} [props.targetName] - 绑定目标名称（如员工名/项目名）
 * @param {Array} [props.resources=[]] - 可选资源列表
 * @param {Function} props.onClose
 * @param {Function} props.onBind - (selectedResource) => void
 */

export default function ResourceBindingPanel({ open, targetName = "", resources = [], onClose, onBind }) {
  const [selectedScope, setSelectedScope] = useState(null);

  if (!open) return null;

  function handleSelect(item) {
    setSelectedScope(item);
    onBind?.(item);
  }

  return (
    <>
      <TerraResourcePicker
        open={open}
        resources={resources}
        onSelect={handleSelect}
        onClose={onClose}
      />

      {/* 选择后的作用范围展示 */}
      {selectedScope && open && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-[1001] bg-ui-surface border border-ui-line rounded-ui-lg shadow-ui-3 px-4 py-3 flex items-center gap-3 max-w-lg">
          <TerraIcon name="i-check_circle" className="w-5 h-5 text-ui-green" />
          <div className="text-sm">
            <span className="font-medium text-ui-txt">已选择：</span>
            <span className="text-ui-primary font-semibold">{selectedScope.name || selectedScope.id}</span>
            {targetName && (
              <span className="text-ui-txt-3 ml-2">→ 应用于「{targetName}」</span>
            )}
          </div>
          <TerraTag color="green">已绑定</TerraTag>
          <button
            type="button"
            onClick={() => setSelectedScope(null)}
            className="ml-auto p-1 rounded hover:bg-ui-surface-2 transition-colors"
          >
            <svg className="w-4 h-4 fill-current text-ui-txt-3" viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
          </button>
        </div>
      )}
    </>
  );
}
