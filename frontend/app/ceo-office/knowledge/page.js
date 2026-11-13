"use client";

import Link from "next/link";
import { Suspense, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";

import { useRuntime } from "../../../components/runtime/RuntimeProvider.js";
import { RuntimeEmpty, RuntimeError, RuntimeLoading } from "../../../components/runtime/RuntimeStates.js";
import TerraShell, { TerraPaneContent } from "../../../components/terra/TerraShell.js";
import {
  TerraButton,
  TerraDrawer,
  TerraPageHead,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import { getCanonicalBusinesses, runtimeErrorMessage } from "../../../lib/runtimeApi.js";
import {
  addWorkKnowledgeReferences,
  createKnowledgeEntry,
  getKnowledgeEntries,
  getLocalKnowledgeFiles,
  getLocalKnowledgeRoots,
  getWorkKnowledgeReferences,
  importLocalKnowledgeFile,
} from "../../../lib/knowledge.js";

const FILTER_KEY = "curis-knowledge-filters";
const RETURN_KEY = "curis-knowledge-return";
const EMPTY_FORM = { title: "", body: "", tags: "", target: "" };

function sourceLabel(value) {
  return value === "local_file" ? "本地文件" : "手工内容";
}

function stateLabel(entry) {
  if (entry.lifecycle_status === "ARCHIVED") return ["已归档", "grey"];
  if (entry.source_status === "UNAVAILABLE") return ["来源待恢复", "amber"];
  return ["可引用", "green"];
}

function formatDate(value) {
  if (!value) return "时间未知";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "时间未知" : date.toLocaleDateString("zh-CN");
}

function safeReturnPath(value) {
  return value?.startsWith("/ceo-office/") ? value : "/ceo-office/workspace";
}

function parseTarget(value, companyId) {
  const [targetType, ...rest] = String(value || `COMPANY:${companyId}`).split(":");
  return {
    company_id: companyId,
    target_type: targetType,
    target_ref: rest.join(":"),
  };
}

export function KnowledgeSurface() {
  const runtime = useRuntime();
  const searchParams = useSearchParams();
  const pickerWork = searchParams.get("pick_for") || "";
  const returnTo = safeReturnPath(searchParams.get("return_to") || "");
  const filterKey = `${FILTER_KEY}:${runtime.companyId}:${pickerWork}`;
  const alive = useRef(true), generation = useRef(0);
  const [filters, setFilters] = useState({ query: "", target: "ALL", source: "", sort: "updated" });
  const [state, setState] = useState({ status: "idle", entries: [], total: 0, hasMore: false, error: "" });
  const [businesses, setBusinesses] = useState([]);
  const [roots, setRoots] = useState([]);
  const [selected, setSelected] = useState([]);
  const [existing, setExisting] = useState([]);
  const [pickerContext, setPickerContext] = useState(null);
  const [savingRefs, setSavingRefs] = useState(false);
  const [manualOpen, setManualOpen] = useState(false);
  const [importOpen, setImportOpen] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [formError, setFormError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [rootId, setRootId] = useState("");
  const [files, setFiles] = useState([]);
  const [relativePath, setRelativePath] = useState("");
  const [sourceRequest, setSourceRequest] = useState(0);

  useEffect(() => {
    alive.current = true;
    return () => { alive.current = false; generation.current += 1; };
  }, []);

  useEffect(() => {
    try {
      const saved = JSON.parse(sessionStorage.getItem(filterKey) || "null");
      if (saved) setFilters(saved);
    } catch (_error) {
      sessionStorage.removeItem(filterKey);
    }
  }, [filterKey]);

  useEffect(() => {
    sessionStorage.setItem(filterKey, JSON.stringify(filters));
  }, [filterKey, filters]);

  const targetOptions = useMemo(() => {
    const company = runtime.snapshot?.company;
    const values = company ? [{ value: `COMPANY:${runtime.companyId}`, label: company.name }] : [];
    for (const business of businesses) {
      values.push({ value: `BUSINESS:${business.business_id}`, label: `业务 · ${business.name}` });
      for (const workspace of business.workspaces || []) {
        values.push({ value: `WORKSPACE:${workspace.workspace_id}`, label: `工作空间 · ${workspace.name}` });
      }
    }
    return values;
  }, [businesses, runtime.companyId, runtime.snapshot]);

  const requestOptions = useCallback((offset = 0) => {
    const [targetType, ...targetParts] = filters.target === "ALL" ? [""] : filters.target.split(":");
    return {
      query: filters.query,
      companyId: runtime.companyId,
      targetType,
      targetRef: targetParts.join(":"),
      sourceType: filters.source,
      sort: filters.sort,
      limit: 30,
      offset,
      workRef: pickerWork,
    };
  }, [filters, pickerWork, runtime.companyId]);

  const load = useCallback(async ({ append = false } = {}) => {
    if (runtime.status !== "ready" || !runtime.companyId) return;
    const ticket = ++generation.current;
    setState((current) => ({ ...current, status: "loading", error: "" }));
    try {
      const offset = append ? state.entries.length : 0;
      const [entryPayload, rootPayload, businessPayload] = await Promise.all([
        getKnowledgeEntries(requestOptions(offset)),
        getLocalKnowledgeRoots(),
        getCanonicalBusinesses(runtime.companyId),
      ]);
      if (!alive.current || ticket !== generation.current) return;
      const nextRoots = rootPayload?.roots || [];
      setRoots(nextRoots);
      setRootId((current) => current || nextRoots[0]?.root_id || "");
      setBusinesses(businessPayload?.businesses || []);
      setState((current) => ({
        status: "ready",
        entries: append ? [...current.entries, ...(entryPayload?.entries || [])] : entryPayload?.entries || [],
        total: entryPayload?.total || 0,
        hasMore: Boolean(entryPayload?.has_more),
        error: "",
      }));
    } catch (error) {
      if (!alive.current || ticket !== generation.current) return;
      setState((current) => ({ ...current, status: "error", error: runtimeErrorMessage(error) }));
    }
  }, [requestOptions, runtime.companyId, runtime.status, state.entries.length]);

  useEffect(() => { load(); }, [filters, pickerWork, runtime.companyId, runtime.status]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    if (!pickerWork || runtime.status !== "ready") return;
    let current = true;
    setSelected([]); setExisting([]); setPickerContext(null);
    getWorkKnowledgeReferences(pickerWork)
      .then((payload) => {
        if (!current) return;
        setExisting((payload?.references || []).map((item) => item.id));
        setPickerContext(payload?.work || null);
      })
      .catch((error) => { if (current) setState((state) => ({ ...state, status: "error", error: runtimeErrorMessage(error) })); });
    return () => { current = false; };
  }, [pickerWork, runtime.status]);

  useEffect(() => {
    if (state.status !== "ready") return;
    try {
      const saved = JSON.parse(sessionStorage.getItem(RETURN_KEY) || "null");
      if (saved?.path === `${location.pathname}${location.search}`) {
        requestAnimationFrame(() => scrollTo({ top: Number(saved.scrollY || 0), behavior: "instant" }));
        sessionStorage.removeItem(RETURN_KEY);
      }
    } catch (_error) {
      sessionStorage.removeItem(RETURN_KEY);
    }
  }, [state.status]);

  useEffect(() => {
    if (!importOpen || !rootId) return;
    let current = true;
    getLocalKnowledgeFiles(rootId)
      .then((payload) => {
        if (!current) return;
        const rows = payload?.files || [];
        setFiles(rows);
        setRelativePath((previous) => rows.some((item) => item.relative_path === previous) ? previous : rows[0]?.relative_path || "");
      })
      .catch((error) => { if (current) setFormError(error?.message || "无法读取本地资料"); });
    return () => { current = false; };
  }, [importOpen, rootId]);

  const detailReturn = `/ceo-office/knowledge?${new URLSearchParams({ view: "browse", ...(pickerWork ? { pick_for: pickerWork, return_to: returnTo } : {}) })}`;

  function rememberReturn() {
    sessionStorage.setItem(RETURN_KEY, JSON.stringify({ path: `${location.pathname}${location.search}`, scrollY }));
  }

  function openForm(kind) {
    setForm((current) => ({ ...current, target: targetOptions.some((item) => item.value === current.target) ? current.target : targetOptions[0]?.value || "" }));
    setFormError("");
    if (kind === "manual") setManualOpen(true);
    else setImportOpen(true);
  }

  async function submitManual(event) {
    event.preventDefault();
    if (!form.title.trim() || !form.body.trim() || !form.target) {
      setFormError("请填写标题、资料正文并选择使用范围");
      return;
    }
    setSubmitting(true);
    setFormError("");
    try {
      await createKnowledgeEntry({
        title: form.title.trim(),
        body: form.body.trim(),
        tags: form.tags.split(/[,，]/).map((item) => item.trim()).filter(Boolean),
        ...parseTarget(form.target, runtime.companyId),
      });
      if (!alive.current) return;
      setManualOpen(false);
      setForm(EMPTY_FORM);
      await load();
    } catch (error) {
      if (!alive.current) return;
      setFormError(error?.message || "资料保存失败");
    } finally {
      if (alive.current) setSubmitting(false);
    }
  }

  async function submitImport(event) {
    event.preventDefault();
    if (!rootId || !relativePath || !form.target) {
      setFormError("请选择资料根、相对路径和使用范围");
      return;
    }
    setSubmitting(true);
    setFormError("");
    try {
      await importLocalKnowledgeFile({
        root_id: rootId,
        relative_path: relativePath,
        title: form.title.trim(),
        tags: form.tags.split(/[,，]/).map((item) => item.trim()).filter(Boolean),
        ...parseTarget(form.target, runtime.companyId),
      });
      if (!alive.current) return;
      setImportOpen(false);
      setForm(EMPTY_FORM);
      await load();
    } catch (error) {
      if (!alive.current) return;
      setFormError(error?.message || "资料导入失败");
    } finally {
      if (alive.current) setSubmitting(false);
    }
  }

  async function addSelected() {
    setSavingRefs(true);
    setFormError("");
    try {
      await addWorkKnowledgeReferences(pickerWork, selected);
      if (!alive.current) return;
      location.assign(returnTo);
    } catch (error) {
      if (!alive.current) return;
      setFormError(error?.message || "资料引用失败");
      setSavingRefs(false);
    }
  }

  const context = <nav aria-label="资料范围与来源" className="grid gap-1 text-sm">
    <p className="px-3 pt-2 text-xs font-semibold text-ui-txt-3">使用范围</p>
    {[{ value: "ALL", label: "全部范围" }, ...targetOptions].map((option) => <button key={option.value} type="button"
      aria-current={filters.target === option.value ? "page" : undefined}
      onClick={() => setFilters((current) => ({ ...current, target: option.value }))}
      className={`rounded-ui-sm px-3 py-2 text-left hover:bg-ui-surface-2 ${filters.target === option.value ? "bg-ui-primary-light font-semibold text-ui-primary" : "text-ui-txt-2"}`}>{option.label}</button>)}
    <p className="mt-2 border-t border-ui-line px-3 pt-3 text-xs font-semibold text-ui-txt-3">来源筛选</p>
    {[["", "全部来源"], ["manual", "手工内容"], ["local_file", "本地文件"]].map(([value, label]) => <button key={value} type="button"
      aria-current={filters.source === value ? "page" : undefined}
      onClick={() => setFilters((current) => ({ ...current, source: value }))}
      className={`rounded-ui-sm px-3 py-2 text-left hover:bg-ui-surface-2 ${filters.source === value ? "bg-ui-primary-light font-semibold text-ui-primary" : "text-ui-txt-2"}`}>{label}</button>)}
  </nav>;
  const sourceTabId = JSON.stringify([runtime.companyId, "knowledge-sources"]);
  const sourceTabs = [{ id: sourceTabId, title: "来源与接入", content: <div className="space-y-6 p-5 text-ui-txt"><section><h2 className="font-semibold">本地资料</h2><p className="mt-2 text-sm leading-6 text-ui-txt-2">可导入已配置来源中的 Markdown 与纯文本文件，原始来源与使用范围一起保留。</p>{roots.length ? <ul className="mt-3 divide-y divide-ui-line">{roots.map((root) => <li key={root.root_id} className="py-3 text-sm">{root.label}</li>)}</ul> : <p className="mt-3 text-sm text-ui-txt-3">尚未配置本地文件来源，可先手工保存资料。</p>}</section><section className="border-t border-ui-line pt-5"><h2 className="font-semibold">外部知识库与定向搜集</h2><p className="mt-2 text-sm leading-6 text-ui-txt-2">尚未接入外部知识库或网页搜集。这里不会把接入显示成已导入，也不会自动扫描外部内容。</p><button disabled className="mt-3 rounded-ui-sm border border-ui-line px-3 py-2 text-sm text-ui-txt-3">暂不可连接或搜集</button></section></div> }];

  if (["idle", "loading"].includes(runtime.status)) return <RuntimeLoading label="正在打开资料库…" />;
  if (["error", "forbidden"].includes(runtime.status)) return <RuntimeError message={runtime.error} onRetry={runtime.refresh} forbidden={runtime.status === "forbidden"} />;
  if (!runtime.snapshot?.company) return <RuntimeEmpty title="公司尚未建立" description="建立公司后，资料才能获得明确的使用范围。" />;
  if (state.status === "error" && !state.entries.length) return <RuntimeError message={state.error} onRetry={() => load()} />;

  return <>
    <TerraPageHead
      title={pickerWork ? "为当前工作选择资料" : "资料库"}
      subtitle={pickerWork ? "为原来的工作挑选有来源的资料，选择后直接返回。" : "保存公司事实、业务方法和创作参考，让每次工作都有据可查。"}
      actions={pickerWork ? <TerraButton disabled={!selected.length || savingRefs} onClick={addSelected}>{savingRefs ? "正在添加…" : `添加 ${selected.length} 条并返回`}</TerraButton> : <div className="flex flex-wrap gap-2"><TerraButton variant="ghost" onClick={() => setSourceRequest((value) => value + 1)}>来源与接入</TerraButton><TerraButton variant="ghost" onClick={() => openForm("import")}>导入文件</TerraButton><TerraButton onClick={() => openForm("manual")}>新建资料</TerraButton></div>}
    />

    <TerraPaneContent contextPane={context} contextLabel="资料导航" initialContextOpen
      utilityTabs={sourceTabs} utilityLabel="资料来源" initialUtilityOpen
      utilityRequestTabId={sourceTabId} utilityRequestKey={sourceRequest} />

    {state.error && <div className="mb-4 rounded-ui-sm border border-ui-red bg-ui-red-soft px-4 py-3 text-ui-1 text-ui-red">{state.error}</div>}
    {formError && pickerWork && <div className="mb-4 rounded-ui-sm border border-ui-red bg-ui-red-soft px-4 py-3 text-ui-1 text-ui-red">{formError}</div>}

    <Browse
      entries={state.entries}
      filters={filters}
      setFilters={setFilters}
      targetOptions={targetOptions}
      pickerWork={pickerWork}
      pickerContext={pickerContext}
      selected={selected}
      existing={existing}
      onSelect={setSelected}
      hasMore={state.hasMore}
      loading={state.status === "loading"}
      loadMore={() => load({ append: true })}
      detailReturn={detailReturn}
      rememberReturn={rememberReturn}
    />

    <TerraDrawer open={manualOpen} title="新建资料" description="手工内容会保留来源与使用范围，不会写进 Memory。" onClose={() => setManualOpen(false)}>
      <KnowledgeForm form={form} setForm={setForm} targetOptions={targetOptions} error={formError} submitting={submitting} onSubmit={submitManual} showBody />
    </TerraDrawer>
    <TerraDrawer open={importOpen} title="导入文件" description="当前只支持已配置根目录中的 Markdown / Text。" onClose={() => setImportOpen(false)}>
      <form className="space-y-4" onSubmit={submitImport}>
        <Select label="资料根" value={rootId} onChange={(value) => { setRootId(value); setRelativePath(""); }} options={roots.map((item) => ({ value: item.root_id, label: item.label }))} empty="尚未配置本地来源" />
        <Select label="相对路径" value={relativePath} onChange={setRelativePath} options={files.map((item) => ({ value: item.relative_path, label: item.relative_path }))} empty="没有可导入的文件" />
        <KnowledgeFields form={form} setForm={setForm} targetOptions={targetOptions} />
        {formError && <p className="text-ui-1 text-ui-red">{formError}</p>}
        <TerraButton type="submit" disabled={submitting || !roots.length}>{submitting ? "导入中…" : "导入资料"}</TerraButton>
      </form>
    </TerraDrawer>
  </>;
}

function Browse({ entries, filters, setFilters, targetOptions, pickerWork, pickerContext, selected, existing, onSelect, hasMore, loading, loadMore, detailReturn, rememberReturn }) {
  const filtered = Boolean(filters.query || filters.target !== "ALL" || filters.source);
  return <section aria-label="资料集合">
    {pickerWork && <div className="mb-4 border-b border-ui-line pb-4"><p className="text-ui-1 font-semibold text-ui-primary">当前工作</p><h2 className="mt-1 text-ui-3 font-semibold">{pickerContext?.problem || "正在读取工作目标…"}</h2>{pickerContext?.expected_result && <p className="mt-1 text-ui-2 text-ui-txt-2">期望结果：{pickerContext.expected_result}</p>}<p className="mt-2 text-ui-1 text-ui-txt-3">已有引用保留；新选择只加入当前工作。</p></div>}
    <div className="mb-5 flex flex-wrap items-end gap-3 border-b border-ui-line pb-4">
      <label className="min-w-[180px] flex-1 text-ui-1 font-medium text-ui-txt-2" htmlFor="knowledge-search">搜索标题、正文或标签<input id="knowledge-search" value={filters.query} onChange={(event) => setFilters((current) => ({ ...current, query: event.target.value }))} placeholder="搜索资料…" className="mt-1.5 h-9 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-2 text-ui-txt outline-none focus:ring-2 focus:ring-ui-primary" /></label>
      <Select label="使用范围" value={filters.target} onChange={(target) => setFilters((current) => ({ ...current, target }))} options={[{ value: "ALL", label: "全部范围" }, ...targetOptions]} />
      <Select label="来源" value={filters.source} onChange={(source) => setFilters((current) => ({ ...current, source }))} options={[{ value: "", label: "全部来源" }, { value: "manual", label: "手工内容" }, { value: "local_file", label: "本地文件" }]} />
      <Select label="排序" value={filters.sort} onChange={(sort) => setFilters((current) => ({ ...current, sort }))} options={[{ value: "updated", label: "最近更新" }, { value: "recent_used", label: "最近使用" }]} />
      {filtered && <button type="button" onClick={() => setFilters({ query: "", target: "ALL", source: "", sort: "updated" })} className="h-9 text-ui-1 font-semibold text-ui-primary">清除筛选</button>}
    </div>
    <div className="mb-3 flex items-center justify-between text-ui-1 text-ui-txt-3"><span>{loading ? "正在读取资料…" : `${entries.length} 条已加载资料`}</span>{pickerWork && <span>已选择 {selected.length} 条 · 原有 {existing.length} 条</span>}</div>
    {!entries.length && !loading ? <RuntimeEmpty title={filtered ? "没有符合条件的资料" : "资料库还是空的"} description={filtered ? "调整或清除筛选，查看其他资料。" : "导入一份本地文档，或新建一条公司资料。"} /> : <div className="grid max-w-[1100px] grid-cols-[repeat(auto-fit,minmax(min(100%,280px),1fr))] gap-4">
      {entries.map((entry) => {
        const [label, color] = stateLabel(entry), checked = selected.includes(entry.id) || existing.includes(entry.id);
        return <article key={entry.id} className="flex min-w-0 flex-col rounded-ui-md border border-ui-line bg-ui-surface p-4 transition-colors hover:border-ui-primary">
          <div className="flex items-center justify-between gap-3"><span className="text-ui-1 font-medium text-ui-txt-3">{sourceLabel(entry.source_type)}</span>{pickerWork && <input type="checkbox" aria-label={`选择 ${entry.title}`} checked={checked} disabled={existing.includes(entry.id)} onChange={(event) => onSelect((current) => event.target.checked ? [...current, entry.id] : current.filter((id) => id !== entry.id))} className="h-4 w-4 accent-ui-primary" />}</div>
          <Link href={`/ceo-office/knowledge/entries/${encodeURIComponent(entry.id)}?return_to=${encodeURIComponent(detailReturn)}`} onClick={rememberReturn} className="mt-4 block break-words text-ui-4 font-semibold leading-6 text-ui-txt no-underline hover:text-ui-primary focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-primary">{entry.title}</Link>
          <p className="mt-2 line-clamp-3 text-ui-2 leading-6 text-ui-txt-2">{entry.excerpt || entry.summary || "打开资料阅读原文"}</p>
          {!!entry.tags?.length && <div className="mt-3 flex flex-wrap gap-1.5">{entry.tags.slice(0, 3).map((tag) => <TerraTag key={tag} color="grey">{tag}</TerraTag>)}</div>}
          <div className="mt-auto flex flex-wrap items-center gap-2 border-t border-ui-line pt-3 mt-4"><TerraTag color={color}>{existing.includes(entry.id) ? "已引用" : label}</TerraTag><span className="text-ui-1 text-ui-txt-3">{entry.scope_name}</span></div>
          <p className="mt-2 text-ui-1 text-ui-txt-3">{formatDate(entry.updated_at)} · 被 {entry.used_count || 0} 项工作引用</p>
        </article>;
      })}
    </div>}
    {hasMore && <div className="mt-6 flex justify-center"><TerraButton variant="ghost" disabled={loading} onClick={loadMore}>{loading ? "正在加载…" : "加载更多"}</TerraButton></div>}
  </section>;
}

function Select({ label, value, onChange, options, empty = "暂无选项" }) {
  return <label className="block text-ui-1 font-bold text-ui-txt-2">{label}<select value={value} onChange={(event) => onChange(event.target.value)} className="mt-1.5 h-9 w-full max-w-[240px] rounded-ui-sm border border-ui-line bg-ui-surface px-3 text-ui-2 font-normal text-ui-txt outline-none focus:ring-2 focus:ring-ui-primary">{!options.length && <option value="">{empty}</option>}{options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}</select></label>;
}

function KnowledgeFields({ form, setForm, targetOptions }) {
  return <>
    <label className="block text-ui-1 font-bold text-ui-txt-2">标题<input value={form.title} onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))} className="mt-1.5 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2.5 text-ui-2 font-normal text-ui-txt" /></label>
    <Select label="使用范围" value={form.target} onChange={(target) => setForm((current) => ({ ...current, target }))} options={targetOptions} empty="公司归属尚未建立" />
    <label className="block text-ui-1 font-bold text-ui-txt-2">标签<input value={form.tags} onChange={(event) => setForm((current) => ({ ...current, tags: event.target.value }))} placeholder="用逗号分隔" className="mt-1.5 w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2.5 text-ui-2 font-normal text-ui-txt" /></label>
  </>;
}

function KnowledgeForm({ form, setForm, targetOptions, error, submitting, onSubmit, showBody }) {
  return <form className="space-y-4" onSubmit={onSubmit}><KnowledgeFields form={form} setForm={setForm} targetOptions={targetOptions} />{showBody && <label className="block text-ui-1 font-bold text-ui-txt-2">资料正文<textarea rows={10} value={form.body} onChange={(event) => setForm((current) => ({ ...current, body: event.target.value }))} className="mt-1.5 w-full resize-y rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2.5 text-ui-2 font-normal text-ui-txt" /></label>}{error && <p className="text-ui-1 text-ui-red">{error}</p>}<TerraButton type="submit" disabled={submitting}>{submitting ? "保存中…" : "保存资料"}</TerraButton></form>;
}

function KnowledgeRoute() {
  const runtime = useRuntime(), params = useSearchParams();
  return <KnowledgeSurface key={JSON.stringify([runtime.companyId, params.get("pick_for"), params.get("return_to")])} />;
}

export default function KnowledgePage() {
  return <TerraShell topCrumb="资料库" assistantContext={{ page: "knowledge" }}><Suspense fallback={<RuntimeLoading label="正在打开资料库…" />}><KnowledgeRoute /></Suspense></TerraShell>;
}
