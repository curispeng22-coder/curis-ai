"use client";

import { useCallback, useState } from "react";

/**
 * useLocalDraft — 纯本地草稿状态 hook（绝不调用后端）。
 *
 * 所有写操作（创建 / 编辑 / 删除）在此仅生成本地草稿状态，
 * 不发起任何 fetch POST / PUT / DELETE，不伪造成功响应。
 * UI 文案统一使用：「草稿已生成（本地）」「本地草稿已更新（未接入后端）」。
 *
 * @param {Object} [initial={}] - 初始草稿对象
 * @returns {{
 *   draft: Object,
 *   isDraft: boolean,
 *   savedAt: string|null,
 *   createDraft: (data: Object) => void,
 *   updateDraft: (patch: Object) => void,
 *   reset: () => void,
 * }} 本地草稿状态与控制函数
 */
export function useLocalDraft(initial = {}) {
  const [draft, setDraft] = useState(initial);
  const [isDraft, setIsDraft] = useState(false);
  const [savedAt, setSavedAt] = useState(null);

  const createDraft = useCallback((data) => {
    setDraft({ ...initial, ...data });
    setIsDraft(true);
    setSavedAt(new Date().toLocaleString("zh-CN", { hour12: false }));
  }, [initial]);

  const updateDraft = useCallback((patch) => {
    setDraft((prev) => ({ ...prev, ...patch }));
    setIsDraft(true);
    setSavedAt(new Date().toLocaleString("zh-CN", { hour12: false }));
  }, []);

  const reset = useCallback(() => {
    setDraft(initial);
    setIsDraft(false);
    setSavedAt(null);
  }, [initial]);

  return { draft, isDraft, savedAt, createDraft, updateDraft, reset };
}

/** 演示用草稿生成提示（本地） */
export const DRAFT_CREATED_TEXT = "草稿已生成（本地）";

/** 演示用草稿更新提示（本地，未接入后端） */
export const DRAFT_UPDATED_TEXT = "本地草稿已更新（未接入后端）";
