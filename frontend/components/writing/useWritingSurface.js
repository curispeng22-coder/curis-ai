"use client";
import { useCallback, useLayoutEffect, useRef } from "react";
import { TENANT_ID } from "../../lib/api.js";
import { WRITING_PACKAGE, writingRequest } from "../../lib/writingState.mjs";

export function validateWritingSurfaceRecord(record, company, workspace) {
  if (!record || record.tenant_id !== TENANT_ID || record.company_id !== company || record.workspace_id !== workspace || !record.entity_id) {
    throw new Error("所选记录不属于当前工作空间。");
  }
  return record;
}

export function validateWritingSurfacePayload(payload, company, workspace, instance = null) {
  const scope = payload?.entry?.scope || payload?.scope;
  if (!scope || scope.tenant_id !== TENANT_ID || scope.company_id !== company || scope.workspace_id !== workspace
    || !scope.instance_id || instance && scope.instance_id !== instance
    || scope.package_id !== WRITING_PACKAGE.id || scope.package_version !== WRITING_PACKAGE.version || scope.package_digest !== WRITING_PACKAGE.digest) {
    throw new Error("当前记录来源已变化，请从原工作空间重新读取。");
  }
  if (payload.record) validateWritingSurfaceRecord(payload.record, company, workspace);
  for (const record of payload.records || []) validateWritingSurfaceRecord(record, company, workspace);
  return scope;
}

export default function useWritingSurface(company, workspace, object = "") {
  const key = JSON.stringify([company, workspace, object]);
  const owner = useRef({ key, generation: 0, mounted: true });
  const read = useRef(0); const pending = useRef(new Map());
  useLayoutEffect(() => {
    owner.current = { key, generation: owner.current.generation + 1, mounted: true };
    read.current += 1; pending.current.clear();
    return () => { owner.current.mounted = false; owner.current.generation += 1; };
  }, [key]);
  const capture = useCallback(() => {
    if (!owner.current.mounted || owner.current.key !== key) throw new Error("工作空间已切换，没有提交原表单。");
    return { key, generation: owner.current.generation };
  }, [key]);
  const live = useCallback((token) => Boolean(token && owner.current.mounted && token.key === key
    && owner.current.key === key && token.generation === owner.current.generation
    && (token.read === undefined || token.read === read.current)), [key]);
  const beginRead = useCallback(() => ({ ...capture(), read: ++read.current }), [capture]);
  const request = useCallback(async (action, base, data) => {
    const token = capture();
    const value = await writingRequest(pending.current.get(action), action, base || "", data, () => crypto.randomUUID());
    if (!live(token)) throw new Error("工作空间已切换，没有提交原表单。");
    pending.current.set(action, value); return { token, request_id: value.request_id };
  }, [capture, live]);
  const complete = useCallback((action, token) => { if (live(token)) pending.current.delete(action); }, [live]);
  return { key, capture, live, beginRead, request, complete };
}
