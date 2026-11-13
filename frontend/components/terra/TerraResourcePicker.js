"use client";

import { useState } from "react";
import { TerraIcon } from "./TerraIcons.js";

/**
 * TerraResourcePicker — 资源选择器对话框（model/skill/tool 共用目录）。
 *
 * 选择结果显示作用范围（scope），供项目详情对话框 / 员工头像复用。
 *
 * @param {Object} props
 * @param {boolean} props.open - 是否显示
 * @param {Array<{id:string,name:string,type:string,description?:string}>} [props.resources=[]] - 可选资源列表
 * @param {string} [props.type="model"] - 默认筛选类型: model | skill | tool | agent | workflow
 * @param {Function} props.onSelect - 选择回调 (selectedItem) => void
 * @param {Function} props.onClose - 关闭回调
 */
export default function TerraResourcePicker({
  open,
  resources = [],
  type = "model",
  onSelect,
  onClose,
}) {
  const [filter, setFilter] = useState("");
  const [activeType, setActiveType] = useState(type);

  if (!open) return null;

  const TYPES = [
    { key: "agent", label: "Agent", icon: "i-smart_toy" },
    { key: "model", label: "模型 Model", icon: "i-memory" },
    { key: "skill", label: "技能 Skill", icon: "i-auto_awesome" },
    { key: "tool", label: "工具 Tool", icon: "i-construction" },
    { key: "workflow", label: "工作流 Workflow", icon: "i-account_tree" },
  ];

  const filtered = resources.filter((r) => {
    const matchType = !activeType || r.type === activeType || r.type === activeType.replace(" ", "");
    const matchSearch = !filter ||
      (r.name || "").toLowerCase().includes(filter.toLowerCase()) ||
      (r.id || "").toLowerCase().includes(filter.toLowerCase());
    return matchType && matchSearch;
  });

  return (
    <div
      className="fixed inset-0 z-[1000] flex items-center justify-center p-4 md:p-5"
      role="dialog"
      aria-modal="true"
      aria-label="选择资源"
    >
      {/* 遮罩 */}
      <div className="absolute inset-0 bg-black/[0.35]" onClick={onClose} aria-hidden="true" />

      {/* 对话框主体 */}
      <div
        className="relative bg-ui-surface border border-ui-line rounded-ui-lg shadow-ui-3 w-full max-w-[600px] max-h-[80vh] overflow-hidden flex flex-col outline-none"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 头部 */}
        <div className="px-6 py-4 border-b border-ui-line">
          <h3 className="font-ui-sans font-semibold text-ui-4 text-ui-txt">选择资源</h3>
          <p className="text-xs text-ui-txt-3 mt-0.5">选择后将在对应作用范围内生效</p>
        </div>

        {/* 类型标签 */}
        <div className="px-6 pt-3 pb-0 flex gap-2 flex-wrap border-b border-ui-line">
          {TYPES.map((t) => (
            <button
              key={t.key}
              type="button"
              onClick={() => setActiveType(t.key)}
              className={`inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-medium transition-colors ${
                activeType === t.key
                  ? "bg-ui-primary text-ui-primary-fg"
                  : "bg-ui-surface-2 text-ui-txt-2 hover:bg-ui-surface-3"
              }`}
            >
              <TerraIcon name={t.icon} className="w-3.5 h-3.5" />
              {t.label}
            </button>
          ))}
        </div>

        {/* 搜索框 */}
        <div className="px-6 pt-3">
          <div className="flex items-center gap-1.5 bg-ui-surface ring-1 ring-inset ring-ui-line-2 rounded-full px-3 h-[var(--ui-ctl-h-sm)]">
            <TerraIcon name="i-search" className="w-4 h-4 text-ui-txt-3" />
            <input
              type="text"
              placeholder={`搜索${TYPES.find((t) => t.key === activeType)?.label || "资源"}…`}
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="border-0 outline-0 bg-transparent text-ui-2 w-full h-full text-ui-txt placeholder:text-ui-txt-3"
            />
          </div>
        </div>

        {/* 资源列表 */}
        <div className="flex-1 overflow-y-auto px-6 py-3 min-h-[120px]">
          {filtered.length === 0 ? (
            <div className="text-center py-8 text-sm text-ui-txt-3">
              <TerraIcon name="i-inbox" className="w-8 h-8 mx-auto mb-2 opacity-40" />
              无匹配资源
            </div>
          ) : (
            <div className="space-y-1.5">
              {filtered.map((item) => (
                <button
                  key={item.id || item.name}
                  type="button"
                  onClick={() => {
                    onSelect?.(item);
                    onClose();
                  }}
                  className="w-full text-left px-3 py-2.5 rounded-ui-sm border border-transparent hover:border-ui-line hover:bg-ui-surface-2 transition-colors group"
                >
                  <div className="flex items-center justify-between">
                    <div className="min-w-0">
                      <div className="font-semibold text-sm text-ui-txt truncate group-hover:text-ui-primary transition-colors">
                        {item.name || item.id || "未命名资源"}
                      </div>
                      <div className="text-ui-1 text-ui-txt-3 mt-0.5 truncate">
                        {item.type || ""} {item.id ? `· ${item.id}` : ""}
                      </div>
                      {item.description && (
                        <div className="text-xs text-ui-txt-3 mt-1 line-clamp-1">{item.description}</div>
                      )}
                    </div>
                    <TerraIcon name="i-arrow_forward" className="w-4 h-4 text-ui-txt-3 group-hover:text-ui-primary flex-shrink-0 ml-2 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>

        {/* 底部 */}
        <div className="px-6 py-3 border-t border-ui-line flex justify-end">
          <button
            type="button"
            onClick={onClose}
            className="px-4 py-2 rounded-ui-sm text-xs font-bold border border-ui-line-2 bg-ui-surface text-ui-txt-2 hover:border-ui-primary hover:text-ui-primary transition-colors"
          >
            取消
          </button>
        </div>
      </div>
    </div>
  );
}
