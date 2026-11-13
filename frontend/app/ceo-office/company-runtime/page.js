"use client";

import { useState } from "react";
import Link from "next/link";
import TerraShell from "../../../components/terra/TerraShell.js";
import RuntimeCapabilitySwitcher from "../../../components/terra/RuntimeCapabilitySwitcher.js";
import {
  TerraBoundary,
  TerraCard,
  TerraCardHeader,
  TerraPageHead,
} from "../../../components/terra/TerraPrimitives.js";
import {
  TerraEmptyState,
  TerraLoadingSkeleton,
  noRuntimeFact,
} from "../../../components/terra/TerraState.js";

/** 成果库（原公司运行视图 · T0 归公司资源组）：运行事实统一「未读取事实」，不填假数字（handoff §4.6 / §10.5） */
const ASSET_METRICS = [
  { key: "verified", label: "已验证成果", note: "过去 30 天" },
  { key: "workflows", label: "可复用工作流", note: "跨工作空间" },
  { key: "sources", label: "已连接来源", note: "API / Connector" },
  { key: "pending", label: "待补证据", note: "需要 CEO 处理" },
];

export default function CompanyRuntimePage() {
  const [loading] = useState(false);

  if (loading) {
    return (
      <TerraShell topCrumb="公司资源 / 成果库">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }

  return (
    <TerraShell
      topCrumb="公司资源 / 成果库"
      topbarExtra={<RuntimeCapabilitySwitcher />}
    >
      <p className="mb-1 text-ui-1 font-semibold tracking-widest text-ui-txt-3">
        公司知识与产出
      </p>

      <TerraPageHead
        title="成果库"
        subtitle="每一份交付、外部结果和复盘都留下版本与证据。成果不是附件，而是下一次经营可以直接复用的公司资产。"
        pill={{ text: "运行事实未读取", icon: "i-monitoring" }}
      />

      {/* 汇总指标 — 对齐原型 assets.html summary 四宫格；运行事实未读取统一「未读取事实」 */}
      <div className="mb-4 grid grid-cols-2 gap-3.5 lg:grid-cols-4">
        {ASSET_METRICS.map((item) => (
          <div key={item.key} className="rounded-ui-sm border border-ui-line bg-ui-surface p-3">
            <div className="text-ui-1 text-ui-txt-3">{item.label}</div>
            <div className="mt-1 font-ui-sans font-semibold text-ui-5 text-ui-txt-3">{noRuntimeFact}</div>
            <div className="mt-1 text-ui-1 text-ui-txt-3">{item.note}</div>
          </div>
        ))}
      </div>

      {/* 所有成果 — 对齐原型 assets 主卡；无真实成果数据时展示空态 */}
      <TerraCard>
        <TerraCardHeader icon="i-description" iconClass="primary" title="所有成果" />
        <p className="mb-3 text-ui-1 text-ui-txt-3 leading-relaxed">
          按业务筛选，打开后可以查看输入、负责人、证据、版本和下一步复用位置。
        </p>
        <TerraEmptyState
          icon="i-description"
          title="成果库还没有内容"
          description="Agent 完成交付、CEO 验收或外部结果回传后，成果会带着来源和版本出现在这里。当前运行事实未读取，暂不填假数字。"
          action={
            <Link
              href="/ceo-office/settings"
              className="inline-flex items-center justify-center h-[var(--ui-ctl-h-lg)] rounded-ui-sm bg-ui-primary px-4 text-ui-2 font-bold text-ui-primary-fg no-underline transition-colors hover:bg-ui-primary-dark"
            >
              前往设置接入运行端点
            </Link>
          }
        />
      </TerraCard>

      {/* 使用方式 — 对齐原型 callout */}
      <div className="mt-4 rounded-ui-sm border border-ui-line bg-ui-surface-2 px-4 py-3 text-ui-1 text-ui-txt-2 leading-relaxed">
        <strong className="text-ui-txt">成果如何进入公司：</strong>
        AI 员工在每个阶段提交带来源的产出；CEO 验收或外部数据确认后，它才会变成“已验证”。你可以把已验证成果直接放入新的工作空间，保留原始上下文和版本关系。
      </div>

      <div className="mt-3.5">
        <TerraBoundary>
          成果库运行事实当前未读取时统一显示「未读取事实」，不填假数字；未新增独立运行端点。
        </TerraBoundary>
      </div>
    </TerraShell>
  );
}
