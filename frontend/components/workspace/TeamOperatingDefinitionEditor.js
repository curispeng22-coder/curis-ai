"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { getTeamOperatingDefinition, publishTeamOperatingDefinition } from "../../lib/runtimeApi.js";

function fromSnapshot(item) {
  return {
    assignment_ref: item.assignmentRef || null,
    role_ref: item.roleRef || null,
    responsibility_key: item.responsibilityKey,
    role_name: item.roleName || item.responsibilityKey,
    employee_ref: item.employeeRef,
    responsibility: item.responsibility || "",
    input: item.inputContract?.description || "",
    output: item.outputContract?.description || "",
    is_leader: Boolean(item.isLeader),
  };
}

function moveRole(items, sourceKey, targetKey) {
  if (!sourceKey || sourceKey === targetKey) return items;
  const source = items.findIndex((item) => item.responsibility_key === sourceKey);
  const target = items.findIndex((item) => item.responsibility_key === targetKey);
  if (source < 0 || target < 0 || items[source].is_leader || items[target].is_leader) return items;
  const next = [...items];
  const [moved] = next.splice(source, 1);
  next.splice(target, 0, moved);
  return next;
}

const musicWorkflowKey = "music-market-research";
const marketResearchRole = "MUSIC_MARKET_RESEARCH";

export function musicResearchPublishRequest(companyId, businessRef, definition, researcher) {
  const leader = definition?.leader;
  if (definition?.company_id !== companyId || definition?.scope?.type !== "BUSINESS"
      || definition.scope.ref !== businessRef || definition.scope.workspace_id !== null
      || definition.workflow_key !== musicWorkflowKey || definition.published || definition.can_publish !== true
      || !leader?.isLeader || !leader.assignmentRef || !leader.employeeRef || leader.employeeRef === researcher
      || !Number.isInteger(leader.assignmentRevision) || leader.assignmentRevision < 1
      || !definition.available_employees?.some(employee => employee.employee_ref === researcher)) {
    throw new Error("请重新核对音乐业务、负责人和研究员。");
  }
  return {
    company_id: companyId, scope_type: "BUSINESS", scope_ref: businessRef, workflow_key: musicWorkflowKey,
    default_flow: [marketResearchRole],
    music_research: { leader_revision: leader.assignmentRevision, confirm: true },
    roles: [
      { responsibility_key: leader.responsibilityKey, role_name: leader.roleName,
        employee_ref: leader.employeeRef, responsibility: leader.responsibility,
        assignment_ref: leader.assignmentRef, role_ref: leader.roleRef, is_leader: true },
      { responsibility_key: marketResearchRole, role_name: "市场研究", employee_ref: researcher,
        responsibility: "核对公开市场来源、数据口径和限制。", is_leader: false },
    ],
  };
}

function MusicResearchArrangement({ companyId, businessRef, onPublished }) {
  const [definition, setDefinition] = useState(null);
  const [researcher, setResearcher] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [reread, setReread] = useState(0);
  const pending = useRef(false);
  const mounted = useRef(false);

  const checkScope = useCallback((data) => {
    if (data?.company_id !== companyId || data?.scope?.type !== "BUSINESS" || data.scope.ref !== businessRef
        || data.scope.workspace_id !== null || data.workflow_key !== musicWorkflowKey) {
      throw new Error("研究流程的业务范围无法核对。");
    }
    return data;
  }, [companyId, businessRef]);

  useEffect(() => {
    let active = true;
    mounted.current = true;
    setBusy(true);
    setDefinition(null);
    setResearcher("");
    setConfirmed(false);
    setError("");
    getTeamOperatingDefinition({ companyId, scopeType: "BUSINESS", scopeRef: businessRef, workflowKey: musicWorkflowKey })
      .then(checkScope)
      .then(data => { if (active) setDefinition(data); })
      .catch(reason => { if (active) setError(reason.message || "暂时无法读取市场研究安排。"); })
      .finally(() => { if (active) setBusy(false); });
    return () => { active = false; mounted.current = false; };
  }, [companyId, businessRef, checkScope, reread]);

  async function publish(event) {
    event.preventDefault();
    if (pending.current || busy || !confirmed || error) return;
    pending.current = true;
    setBusy(true);
    try {
      const body = musicResearchPublishRequest(companyId, businessRef, definition, researcher);
      const data = checkScope(await publishTeamOperatingDefinition(body));
      const roles = data.published?.roles;
      if (!data.published?.workflow_ref || !(data.published.version >= 1) || roles?.length !== 2
          || roles[0].assignmentRef !== definition.leader.assignmentRef
          || roles[0].assignmentRevision !== definition.leader.assignmentRevision
          || roles[1].employeeRef !== researcher || roles[1].outputContract?.resultType !== "market-summary") {
        throw new Error("发布回执无法核对。");
      }
      if (mounted.current) {
        setDefinition(data);
        onPublished?.();
      }
    } catch (reason) {
      if (mounted.current) setError((reason.message || "发布状态待核对。") + " 请先重新读取安排。");
    } finally {
      pending.current = false;
      if (mounted.current) setBusy(false);
    }
  }

  return <section className="rounded-ui-md border border-ui-line bg-ui-surface p-4" aria-label="安排市场研究">
    <h2 className="text-ui-3 font-semibold">安排市场研究</h2>
    {busy && !definition && <p role="status">正在读取研究安排…</p>}
    {definition && <p className="mt-2 text-ui-2">业务负责人：{definition.leader.employeeName}</p>}
    {definition?.published && <p role="status" className="mt-2 text-ui-2">市场研究负责人：{definition.published.roles[1].employeeName}。流程已发布 · 版本 {definition.published.version}</p>}
    {definition?.can_publish && !error && !definition.available_employees.length && <p role="status">当前没有可安排的其他员工。</p>}
    {definition?.can_publish && !error && definition.available_employees.length > 0 && <form onSubmit={publish} className="mt-3 grid gap-2">
      <label className="grid gap-1">研究员<select required value={researcher} disabled={busy}
        className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2"
        onChange={event => { setResearcher(event.target.value); setConfirmed(false); }}>
        <option value="">请选择员工</option>
        {definition.available_employees.map(person => <option key={person.employee_ref} value={person.employee_ref}>
          {person.name}{person.role && person.name !== person.role ? ` · ${person.role}` : ""}
        </option>)}
      </select></label>
      <label className="flex gap-2"><input type="checkbox" checked={confirmed} disabled={!researcher || busy}
        onChange={event => setConfirmed(event.target.checked)} />确认以上研究员，发布本业务的市场研究流程</label>
      <button type="submit" disabled={!researcher || !confirmed || busy}
        className="rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-action-primary-fg disabled:opacity-50">
        {busy ? "正在发布…" : "发布市场研究流程"}
      </button>
    </form>}
    {error && <><p role="alert" className="mt-2 text-ui-danger">{error}</p>
      <button type="button" disabled={busy} onClick={() => setReread(value => value + 1)}
        className="mt-2 text-ui-primary">重新读取安排</button></>}
  </section>;
}

export default function TeamOperatingDefinitionEditor({ musicBusinessRef, ...props }) {
  return musicBusinessRef
    ? <MusicResearchArrangement key={JSON.stringify([props.companyId, musicBusinessRef])}
        companyId={props.companyId} businessRef={musicBusinessRef} onPublished={props.onPublished} />
    : <WorkspaceDefinitionEditor {...props} />;
}

function WorkspaceDefinitionEditor({ companyId, workspaceId, workflowKey = "content-growth" }) {
  const [state, setState] = useState({ status: "loading", data: null, error: "" });
  const [editing, setEditing] = useState(false);
  const [roles, setRoles] = useState([]);
  const draggedRef = useRef("");
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    if (!companyId || !workspaceId) return;
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      const data = await getTeamOperatingDefinition({
        companyId, workspaceId, scopeType: "WORKSPACE", scopeRef: workspaceId, workflowKey,
      });
      setState({ status: "ready", data, error: "" });
      setRoles((data.published?.roles || []).map(fromSnapshot));
    } catch (error) {
      setState({ status: "error", data: null, error: error.message || "暂时无法读取团队运转设置" });
    }
  }, [companyId, workspaceId, workflowKey]);

  useEffect(() => { load(); }, [load]);

  const employees = state.data?.available_employees || [];
  const employeeName = useMemo(
    () => Object.fromEntries(employees.map((item) => [item.employee_ref, item.name])),
    [employees],
  );
  const flow = roles.filter((item) => !item.is_leader);

  function update(key, field, value) {
    setRoles((current) => current.map((item) => item.responsibility_key === key ? { ...item, [field]: value } : item));
  }

  function moveBy(key, offset) {
    setRoles((current) => {
      const flowItems = current.filter((item) => !item.is_leader);
      const index = flowItems.findIndex((item) => item.responsibility_key === key);
      const target = flowItems[index + offset];
      return target ? moveRole(current, key, target.responsibility_key) : current;
    });
  }

  function addRole() {
    const key = `role-${Date.now()}`;
    setRoles((current) => [...current, {
      assignment_ref: null, role_ref: null, responsibility_key: key, role_name: "新岗位",
      employee_ref: employees[0]?.employee_ref || "", responsibility: "", input: "", output: "", is_leader: false,
    }]);
  }

  function startReorder(key) {
    draggedRef.current = key;
  }

  function stopReorder() {
    draggedRef.current = "";
  }

  async function save() {
    setSaving(true);
    setState((current) => ({ ...current, error: "" }));
    try {
      const data = await publishTeamOperatingDefinition({
        company_id: companyId,
        workspace_id: workspaceId,
        scope_type: "WORKSPACE",
        scope_ref: workspaceId,
        workflow_key: workflowKey,
        default_flow: flow.map((item) => item.responsibility_key),
        roles: roles.map((item) => ({
          assignment_ref: item.assignment_ref,
          role_ref: item.role_ref,
          responsibility_key: item.responsibility_key,
          role_name: item.role_name,
          employee_ref: item.employee_ref,
          responsibility: item.responsibility,
          input_contract: item.input ? { description: item.input } : {},
          output_contract: { ...(item.output ? { description: item.output } : {}), requiresResult: true },
          is_leader: item.is_leader,
        })),
      });
      setState({ status: "ready", data, error: "" });
      setRoles((data.published?.roles || []).map(fromSnapshot));
      setEditing(false);
    } catch (error) {
      setState((current) => ({ ...current, error: error.message || "保存失败，请检查岗位和员工" }));
    } finally {
      setSaving(false);
    }
  }

  return <section className="rounded-ui-md border border-ui-line bg-ui-surface p-4">
    <div className="flex flex-wrap items-start justify-between gap-3">
      <div><p className="text-ui-1 text-ui-txt-3">团队运转</p><h2 className="mt-1 text-ui-3 font-semibold">默认流程</h2><p className="mt-1 text-ui-1 text-ui-txt-2">正常情况下按责任顺序流转；遇到问题时，员工仍可咨询、退回或交接。</p></div>
      <button type="button" onClick={() => setEditing((value) => !value)} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt">{editing ? "收起" : "编辑"}</button>
    </div>
    {state.status === "loading" ? <p className="mt-4 text-ui-2 text-ui-txt-3">正在读取团队安排…</p> : flow.length ? <div className="mt-4 flex flex-wrap items-center gap-2">{flow.map((item, index) => <span key={item.responsibility_key} className="contents"><span className="rounded-ui-sm bg-ui-surface-2 px-3 py-2 text-ui-2 font-medium">{item.role_name || item.responsibility_key} · {employeeName[item.employee_ref] || "待安排员工"}</span>{index < flow.length - 1 && <span className="text-ui-txt-3">→</span>}</span>)}</div> : <p className="mt-4 text-ui-2 text-ui-txt-2">还没有默认流程。可以先安排岗位；不会因此自动开始工作。</p>}
    {state.data?.published && <p className="mt-3 text-ui-1 text-ui-txt-3">当前版本 v{state.data.published.version} · 修改只影响新工作{state.data.running_work?.length ? ` · ${state.data.running_work.length} 项既有工作继续原版本` : ""}</p>}
    {editing && <div className="mt-4 grid gap-3 border-t border-ui-line pt-4">
      {roles.map((item) => <article
        key={item.responsibility_key}
        data-role-key={item.responsibility_key}
        draggable={!item.is_leader}
        onDragStart={() => startReorder(item.responsibility_key)}
        onDragOver={(event) => { event.preventDefault(); if (!item.is_leader) setRoles((current) => moveRole(current, draggedRef.current, item.responsibility_key)); }}
        onDragEnd={stopReorder}
        onMouseUp={() => { if (draggedRef.current && !item.is_leader) setRoles((current) => moveRole(current, draggedRef.current, item.responsibility_key)); stopReorder(); }}
        className="grid gap-3 rounded-ui-sm bg-ui-surface-2 p-3 lg:grid-cols-2"
      >
        <div
          className={`lg:col-span-2 flex items-center justify-between gap-3 ${item.is_leader ? "" : "cursor-grab"}`}
        ><p onMouseDown={() => { if (!item.is_leader) startReorder(item.responsibility_key); }} className="select-none text-ui-2 font-semibold">{item.is_leader ? "协作负责人" : "拖动调整顺序"}</p>{!item.is_leader && <div className="flex gap-2"><button type="button" onClick={() => moveBy(item.responsibility_key, -1)} className="text-ui-1 text-ui-txt-2">上移</button><button type="button" onClick={() => moveBy(item.responsibility_key, 1)} className="text-ui-1 text-ui-txt-2">下移</button><button type="button" onClick={() => setRoles((current) => current.filter((role) => role.responsibility_key !== item.responsibility_key))} className="text-ui-1 text-ui-danger">删除岗位</button></div>}</div>
        <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">岗位名称<input readOnly={Boolean(item.role_ref)} value={item.role_name} onChange={(event) => update(item.responsibility_key, "role_name", event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt read-only:text-ui-txt-3" /></label>
        <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">安排员工<select value={item.employee_ref} onChange={(event) => update(item.responsibility_key, "employee_ref", event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt"><option value="">请选择员工</option>{employees.map((employee) => <option key={employee.employee_ref} value={employee.employee_ref}>{employee.name}</option>)}</select></label>
        <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2 lg:col-span-2">负责什么<textarea value={item.responsibility} onChange={(event) => update(item.responsibility_key, "responsibility", event.target.value)} rows={2} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label>
        <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">需要的输入<input value={item.input} onChange={(event) => update(item.responsibility_key, "input", event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label>
        <label className="grid gap-1 text-ui-1 font-medium text-ui-txt-2">交付结果<input value={item.output} onChange={(event) => update(item.responsibility_key, "output", event.target.value)} className="rounded-ui-sm border border-ui-line bg-ui-bg px-3 py-2 text-ui-2 text-ui-txt" /></label>
      </article>)}
      <div className="flex flex-wrap gap-2"><button type="button" onClick={addRole} className="rounded-ui-sm border border-ui-line px-3 py-2 text-ui-1 font-semibold text-ui-txt">添加岗位</button><button type="button" disabled={saving || !roles.length || roles.some((item) => !item.employee_ref || !item.responsibility.trim())} onClick={save} className="rounded-ui-sm bg-ui-action-primary-bg px-3 py-2 text-ui-1 font-semibold text-ui-action-primary-fg disabled:opacity-50">{saving ? "正在保存…" : "保存新版本"}</button></div>
    </div>}
    {state.error && <p role="alert" className="mt-3 text-ui-1 text-ui-danger">{state.error}</p>}
  </section>;
}

export { moveRole };
