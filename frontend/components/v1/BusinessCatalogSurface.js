"use client";

import Link from "next/link";
import { workspaceOfficeHref } from "../../lib/runtimeApi.js";
import { MUSIC_PACKAGE } from "../../lib/musicState.mjs";
import Image from "next/image";
import { useEffect, useMemo, useState } from "react";
import { TerraPaneContent } from "../terra/TerraShell.js";
import { TerraIcon } from "../terra/TerraIcons.js";
import growthImage from "../../public/assets/business/global-business-growth.png";
import writingImage from "../../public/assets/business/global-business-writing.png";
import musicImage from "../../public/assets/business/global-business-music.png";
import styles from "./BusinessCatalogSurface.module.css";

export const BUSINESS_DIRECTIONS = Object.freeze([
  { id: "growth", packageId: "com.curis.local.content-growth", name: "内容增长", icon: "i-analytics", subtitle: "让内容创造更多可能", description: "围绕平台与账号，规划内容方向、创作与持续经营。", objects: "平台、账号与内容", boundary: "账号授权、发布与平台表现以实际接入和回执为准。" },
  { id: "writing", packageId: "com.curis.local.writing-authoring", name: "写作", icon: "i-description", subtitle: "用更好的工具表达思想", description: "围绕作品与章节，整理创作资料、维护正文与作者确认的版本。", objects: "作品、章节与创作资料", boundary: "本地编辑与作者确认不等于公开发表或出版。" },
  { id: "music", packageId: "com.curis.local.music", name: "音乐", icon: "i-music_note", subtitle: "用音乐连接更多真实的人", description: "围绕歌曲与创作方向，整理歌词、制作依据与选版。", objects: "歌曲、歌词与制作版本", boundary: "创作候选、选版、成品确认与发行分别核验。" },
]);

export function businessCatalogHref(companyId, selection = {}) {
  const query = new URLSearchParams({ company_id: companyId });
  if (selection.businessId) query.set("business_id", selection.businessId);
  if (BUSINESS_DIRECTIONS.some((item) => item.id === selection.definitionId)) query.set("definition", selection.definitionId);
  if (selection.create) query.set("new", "1");
  if (selection.sourceDefinition) query.set("source_definition", selection.sourceDefinition);
  return "/ceo-office/business?" + query;
}

export function businessCatalogSelection(params, companyId, businesses) {
  if (params.has("company_id") && (params.getAll("company_id").length !== 1 || params.get("company_id") !== companyId)) return { kind: "invalid" };
  if (["business_id", "definition", "new", "source_definition"].some((key) => params.getAll(key).length > 1)) return { kind: "invalid" };
  const businessId = params.get("business_id"), definitionId = params.get("definition");
  if (["business_id", "definition", "new"].filter((key) => params.has(key)).length > 1) return { kind: "invalid" };
  const sourceDefinition = params.get("source_definition");
  if (params.has("source_definition") && (params.get("new") !== "1" || !BUSINESS_DIRECTIONS.some((item) => item.id === sourceDefinition))) return { kind: "invalid" };
  if (params.get("new") === "1") return sourceDefinition ? { kind: "create", sourceDefinition } : { kind: "create" };
  if (businessId) {
    const business = businesses.find((item) => item.business_id === businessId && item.company_id === companyId);
    return business ? { kind: "business", business } : { kind: "invalid" };
  }
  if (definitionId) return BUSINESS_DIRECTIONS.some((item) => item.id === definitionId) ? { kind: "definition", definitionId } : { kind: "invalid" };
  return { kind: "directory" };
}

export function creationDirectionDefinition(sourceDefinition, payload) {
  const direction = BUSINESS_DIRECTIONS.find((item) => item.id === sourceDefinition);
  if (!direction) return null;
  const matches = (payload?.definitions || (payload?.available ? [payload.definition] : []))
    .filter((item) => item?.package_id === direction.packageId && item.published !== false && item.version && item.digest
      && (item.package_id !== MUSIC_PACKAGE.id || item.published === true && item.version === MUSIC_PACKAGE.version && item.digest === MUSIC_PACKAGE.digest));
  if (matches.length !== 1) return null;
  return directionCreationReady({ ...direction, definition: matches[0] }, "ready") ? matches[0] : null;
}

export function directionCreationReady(direction, status) {
  const definition = direction.definition, contract = definition?.initial_team_contract;
  return status === "ready" && Boolean(contract?.sha256 && contract.packageId === direction.packageId
    && contract.packageVersion === definition.version && contract.packageDigest === definition.digest
    && (direction.id === "writing" || definition.published === true));
}

export function businessCatalogProjection(companyId, businesses = [], organization = null, definitions = null) {
  const scoped = businesses.filter((item) => item.company_id === companyId);
  const organizationMatches = organization?.company?.company_id === companyId;
  const pending = (organizationMatches ? organization.pending_business_proposals || [] : [])
    .filter((item) => item.company_id === companyId && item.lifecycle_status === "PROPOSED"
      && typeof item.founding_run_id === "string" && item.founding_run_id.trim()
      && typeof item.business_name === "string" && item.business_name.trim());
  const pendingCounts = new Map();
  for (const item of pending) pendingCounts.set(item.founding_run_id, (pendingCounts.get(item.founding_run_id) || 0) + 1);
  const supportIds = new Set((organizationMatches ? organization.departmentAssignments || [] : [])
    .filter((item) => item.company_id === companyId && /^(space\.engineering|data\.analytics)\./.test(item.data?.responsibilityKey || ""))
    .map((item) => item.data.scopeRef));
  return {
    businesses: scoped,
    pendingProposals: pending.filter((item) => pendingCounts.get(item.founding_run_id) === 1).slice(0, 20),
    departments: (organizationMatches ? organization.departments || [] : []).filter((item) => item.company_id === companyId && supportIds.has(item.id)),
    organizationReadable: organizationMatches,
    directions: BUSINESS_DIRECTIONS.map((item) => ({ ...item,
      definition: definitions ? (definitions.definitions || (definitions.definition ? [definitions.definition] : []))
        .find((entry) => entry.package_id === item.packageId && entry.published !== false) || null : null,
      availabilityKnown: Boolean(definitions),
    })),
  };
}

export function businessWorkspaceTargets(business) {
  const rows = Array.isArray(business?.workspaces) ? business.workspaces : [];
  return rows.filter((row) => row && typeof row.workspace_id === "string" && row.workspace_id.trim() === row.workspace_id && row.workspace_id
    && ["PACKAGE", "GENERIC"].includes(row.business_type)
    && rows.filter((other) => other?.workspace_id === row.workspace_id).length === 1);
}

export const businessPaneId = (companyId, kind, id = "") => JSON.stringify([companyId, kind, id]);

export function BusinessCatalogPaneContent({ company, businesses, organization, definitions, definitionStatus, selection }) {
  const [request, setRequest] = useState({ target: "", key: 0 });
  const target = selection.kind === "definition" ? businessPaneId(company.company_id, "definition", selection.definitionId)
    : selection.kind === "business" ? businessPaneId(company.company_id, "business", selection.business.business_id) : "";
  useEffect(() => { if (target) setRequest((value) => ({ target, key: value.key + 1 })); }, [target]);
  const panes = useMemo(() => {
    const view = businessCatalogProjection(company.company_id, businesses, organization, definitions);
    const reopenSelected = (event, id) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || id !== target) return;
      setRequest((value) => ({ target: id, key: value.key + 1 }));
    };
    const tabs = [{ id: businessPaneId(company.company_id, "company"), title: "当前公司", content: <section><h2 className="text-lg font-semibold">{company.name}</h2><p className="mt-3 text-sm text-ui-txt-2">{view.businesses.length} 项已读取业务</p><p className="mt-2 text-sm text-ui-txt-2">团队依据当前责任分配读取；员工执行另需配置与授权。</p><Link className="mt-4 block text-ui-primary" href={businessCatalogHref(company.company_id)}>返回业务目录</Link></section> }];
    for (const item of view.directions) tabs.push({ id: businessPaneId(company.company_id, "definition", item.id), title: item.name + " · 范围", content: <section><h2 className="text-lg font-semibold">{item.name}</h2><p className="mt-3 text-sm text-ui-txt-2" role="status">{["idle", "loading"].includes(definitionStatus) ? "正在读取可用范围…" : item.definition ? item.definition.name : item.availabilityKnown ? "当前尚不可启用" : "可用范围暂时无法读取"}</p><p className="mt-3 text-sm text-ui-txt-2">{item.boundary}</p><h3 className="mt-5 font-semibold">启用准备</h3><p className="mt-2 text-sm text-ui-txt-2">{directionCreationReady(item, definitionStatus) ? `创建时将配备${item.definition.initial_team_contract.displayName}，兼业务负责人；执行另需配置与授权。` : "当前未提供可创建的业务定义或初始团队合同。"}</p>{directionCreationReady(item, definitionStatus) ? <Link className="mt-3 block text-ui-primary" href={businessCatalogHref(company.company_id, { create: true, sourceDefinition: item.id })}>新建业务 →</Link> : <button type="button" disabled className="mt-3 rounded border border-ui-line p-2 text-sm">暂不可启用</button>}</section> });
    for (const item of view.businesses) tabs.push({ id: businessPaneId(company.company_id, "business", item.business_id), title: item.name || "业务信息", content: <section><h2 className="text-lg font-semibold">{item.name || "未命名业务"}</h2><dl className="mt-4 space-y-3 text-sm"><div><dt className="text-ui-txt-2">所属公司</dt><dd>{company.name}</dd></div><div><dt className="text-ui-txt-2">所属部门</dt><dd>{item.parentPath?.department?.name || "所属部门尚未读取"}</dd></div><div><dt className="text-ui-txt-2">已读取工作空间</dt><dd>{Array.isArray(item.workspaces) ? item.workspaces.length : "尚未读取"}</dd></div></dl><Link className="mt-4 block text-ui-primary" href={businessCatalogHref(company.company_id, { businessId: item.business_id })}>查看业务现场 →</Link></section> });
    const context = <nav aria-label="业务导航" className={`${styles.contextNavigation} space-y-5`}><section><h2 className="text-sm font-semibold">当前业务</h2>{view.businesses.length ? view.businesses.map((item) => <Link key={item.business_id} className="mt-3 block text-sm text-ui-primary" href={businessCatalogHref(company.company_id, { businessId: item.business_id })} onClick={(event) => reopenSelected(event, businessPaneId(company.company_id, "business", item.business_id))}>{item.name || "未命名业务"}</Link>) : <p className="mt-2 text-sm text-ui-txt-2">还没有经营中的业务</p>}</section><section><h2 className="text-sm font-semibold">方向介绍</h2>{view.directions.map((item) => <Link key={item.id} className="mt-3 block text-sm text-ui-primary" href={businessCatalogHref(company.company_id, { definitionId: item.id })} onClick={(event) => reopenSelected(event, businessPaneId(company.company_id, "definition", item.id))}>{item.name}</Link>)}</section><Link className="block text-sm text-ui-primary" href={businessCatalogHref(company.company_id)}>返回业务目录</Link></nav>;
    return { context, tabs };
  }, [company, businesses, organization, definitions, definitionStatus, target]);
  return <TerraPaneContent contextPane={panes.context} utilityTabs={panes.tabs} contextLabel="业务导航" utilityLabel="对象信息" initialContextOpen initialUtilityOpen={false} utilityRequestKey={selection.kind === "business" && target && request.target === target ? request.key : 0} utilityRequestTabId={target} />;
}

export default function BusinessCatalogSurface({ company, businesses, organization, definitions, definitionId, definitionStatus = definitions ? "ready" : "error" }) {
  const view = businessCatalogProjection(company.company_id, businesses, organization, definitions);
  const direction = view.directions.find((item) => item.id === definitionId);
  const images = { growth: growthImage, writing: writingImage, music: musicImage };
  const directoryHref = businessCatalogHref(company.company_id);
  if (direction) return <main className={styles.page}>
    <Link className={styles.back} href={directoryHref}>← 返回业务目录</Link>
    <header className={styles.header}><div><h1>{direction.name} · 能力与边界</h1><p>{direction.subtitle}</p></div><span className={styles.badge}>业务方向</span></header>
    <div><section><Image className={styles.detailPhoto} src={images[direction.id]} alt={`${direction.name}工作参考`} sizes="(max-width: 900px) 100vw, 65vw" />
      <h2>经营什么</h2><p>{direction.description}</p><dl className={styles.facts}><dt>经营对象</dt><dd>{direction.objects}</dd><dt>当前可用范围</dt><dd role="status">{["idle", "loading"].includes(definitionStatus) ? "正在读取可用范围…" : direction.definition ? direction.definition.name : direction.availabilityKnown ? "当前尚不可启用" : "可用范围暂时无法读取"}</dd></dl>
      <h2>使用边界</h2><p>{direction.boundary}</p><p>模型、外部账号与电脑访问仍须各自的实际授权。</p><h2>初始团队</h2><p>{directionCreationReady(direction, definitionStatus) ? `创建时将配备${direction.definition.initial_team_contract.displayName}，兼业务负责人；创作、自检、交付与复盘责任已包含，自检不等于独立审核。` : "当前未提供可创建的业务定义或初始团队合同。"}</p>{directionCreationReady(direction, definitionStatus) && <Link className={styles.action} href={businessCatalogHref(company.company_id, { create: true, sourceDefinition: direction.id })}>新建业务 →</Link>}
    </section></div>
  </main>;
  return <main className={styles.page}>
    <header className={styles.header}><div><h1>业务空间</h1><p>进入业务现场，开展专注的工作。</p></div><Link className={styles.primary} href={businessCatalogHref(company.company_id, { create: true })}><TerraIcon name="i-add" />新建业务</Link></header>
    <section><div className={styles.sectionHeading}><h2>内容增长 · 写作 · 音乐</h2><span className={styles.meta}>已有工作空间直接进入；新建前明确确认</span></div><div className={styles.directionGrid}>{view.directions.map((item) => <article className={styles.direction} key={item.id}><div className={styles.directionTitle}><span className={styles.glyph}><TerraIcon name={item.icon} /></span><div><h3>{item.name}</h3><p>{item.subtitle}</p></div></div><Image className={styles.photo} src={images[item.id]} alt={`${item.name}工作参考`} sizes="(max-width: 900px) 100vw, 33vw" /><p>{item.description}</p><div className={styles.directionWorkspaces} aria-label={`${item.name}已有工作空间`}>{view.businesses.flatMap((business) => businessWorkspaceTargets(business).filter((workspace) => workspace.business_type === "PACKAGE" && workspace.package_id === item.packageId && typeof workspace.package_version === "string" && workspace.package_version.trim()).map((workspace) => <Link key={`${business.business_id}:${workspace.workspace_id}`} className={`${styles.link} ${styles.workspaceEntry}`} title={`${business.name || "未命名业务"} · ${workspace.name || "工作空间"}`} href={workspaceOfficeHref(workspace)}><span>进入 {business.name || "未命名业务"}</span><span className={styles.workspaceName}>{workspace.name || "工作空间"} →</span></Link>))}</div>{directionCreationReady(item, definitionStatus) && <Link className={styles.action} href={businessCatalogHref(company.company_id, { create: true, sourceDefinition: item.id })}>新建{item.name}业务 →</Link>}<Link className={styles.secondary} href={businessCatalogHref(company.company_id, { definitionId: item.id })}>了解能力与边界 →</Link></article>)}</div></section>
    {view.pendingProposals.length > 0 && <div aria-label="已保存的待确认提案">
      <p className={styles.meta}>已保存、尚未确认的提案</p>
      <ul>{view.pendingProposals.map((proposal) => <li key={proposal.founding_run_id}>
        <Link className={styles.link} href={`${businessCatalogHref(company.company_id, { create: true })}&${new URLSearchParams({ founding_run_id: proposal.founding_run_id })}`}>继续创建：{proposal.business_name}</Link>
      </li>)}</ul>
    </div>}
    <section><div className={styles.sectionHeading}><h2>当前业务</h2><span className={styles.meta}>{company.name}</span></div>
      {view.businesses.length ? <ul className={styles.businessList}>{view.businesses.map((business) => <li key={business.business_id}><div><h3>{business.name || "未命名业务"}</h3><p>{business.definition?.goal || business.definition?.positioning || "经营目标尚未提供"}</p></div><span className={styles.meta}>{Array.isArray(business.workspaces) ? `${business.workspaces.length} 个工作空间` : "工作空间尚未提供"}</span><div className={styles.workspaceActions}>{businessWorkspaceTargets(business).map((workspace) => <Link key={workspace.workspace_id} className={styles.link} href={workspaceOfficeHref(workspace)}>打开{workspace.name || "工作空间"} →</Link>)}<Link className={styles.secondary} href={businessCatalogHref(company.company_id, { businessId: business.business_id })}>查看业务</Link></div></li>)}</ul>
        : <div className={styles.empty}><h3>还没有经营中的业务</h3><p>可以从上方专业方向开始，或描述你想开展的业务。</p></div>}
    </section>

    <section className={styles.support}><div className={styles.sectionHeading}><h2>公司支持部门</h2><span className={styles.badge}>支持部门 · 非业务</span></div><p>跨业务的支持与协作，来自当前公司的组织安排。</p>
      {view.departments.length ? <div className={styles.supportGrid}>{view.departments.map((department) => <article className={styles.department} key={department.id}><span className={styles.glyph}><TerraIcon name="i-apartment" /></span><div><h3>{department.name || "未命名部门"}</h3><p>{department.mission || "支持公司内的工作与协作。"}</p></div><Link className={styles.link} href="/ceo-office/organization">查看部门 →</Link></article>)}</div>
        : <p className={styles.empty}>{view.organizationReadable ? "当前没有可读取的支持部门安排。" : "支持部门暂时无法读取。已有业务仍可直接进入。"}</p>}
    </section>
    <p className={styles.footnote}>方向介绍与当前业务分别展示；创建团队不等于员工执行已可用，未提供可用定义的方向暂不可启用。</p>
  </main>;
}
