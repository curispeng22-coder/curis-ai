"use client";

import { TerraIcon } from "./TerraIcons.js";
import { TerraButton, TerraModal } from "./TerraPrimitives.js";

/**
 * TerraConfirmDialog — 删除二次确认 overlay。
 *
 * 沿用既有 422 错误透出模式：
 * - disabledReason 存在时禁用确认按钮并展示原因
 * - 危险操作使用红色主按钮
 * - 点击遮罩或取消关闭
 *
 * @param {Object} props
 * @param {boolean} props.open - 是否显示
 * @param {string} props.title - 标题
 * @param {string} [props.description] - 描述文字
 * @param {string} [props.dangerText] - 危险按钮文案（默认 "确认删除"）
 * @param {string} [props.disabledReason] - 禁用原因（存在时禁用确认）
 * @param {Function} props.onConfirm - 确认回调
 * @param {Function} props.onClose - 关闭回调
 */
export default function TerraConfirmDialog({
  open,
  title,
  description,
  dangerText = "确认删除",
  disabledReason,
  onConfirm,
  onClose,
}) {
  const isDisabled = !!disabledReason;

  return (
    <TerraModal
      open={open}
      title={title}
      description={description}
      onClose={onClose}
      footer={(
        <div className="flex justify-end gap-3">
          <TerraButton type="button" variant="ghost" onClick={onClose}>取消</TerraButton>
          <TerraButton
            type="button"
            variant="danger"
            onClick={() => !isDisabled && onConfirm?.()}
            disabled={isDisabled}
          >
            {dangerText}
          </TerraButton>
        </div>
      )}
    >
      {isDisabled && (
        <div className="flex items-start gap-2 bg-ui-amber-soft border border-ui-amber/20 rounded-ui-sm px-3 py-2 text-xs text-ui-amber">
          <TerraIcon name="i-warning" className="w-4 h-4 flex-shrink-0 mt-0.5" />
          <span>{disabledReason}</span>
        </div>
      )}
    </TerraModal>
  );
}
