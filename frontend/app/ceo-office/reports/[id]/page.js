"use client";

import { useParams } from "next/navigation";
import TerraShell from "../../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../../components/terra/TerraIcons.js";
import {
  TerraCard,
  TerraCardHeader,
  TerraTag,
  TerraBackLink,
  TerraPageHead,
} from "../../../../components/terra/TerraPrimitives.js";
import {
  DATA_COPY,
  TerraSampleBadge,
} from "../../../../components/terra/TerraState.js";

/** 示例汇报详情（与 reports 列表快照一致） */
const SAMPLE_DETAIL = {
  title: "Q2 产品交付总结报告",
  author: "张伟",
  role: "PM",
  date: "2026-07-20",
  content: "Q2 共完成 3 个核心项目交付，其中客户管理系统 v2.0 进入执行阶段（进度 65%），移动端性能优化完成核心改造，官网品牌升级已验收通过。整体目标达成率 82%。",
  metrics: [
    { label: "任务完成率", value: "82%" },
    { label: "延期率", value: "12%" },
    { label: "客户满意度", value: "4.2" },
  ],
  reviewStatus: "已审阅 · 通过",
  lastReview: "上次审阅：3 小时前",
};

export default function ReportDetailPage() {
  const params = useParams();
  const id = params?.id || "";
  const r = SAMPLE_DETAIL;

  return (
    <TerraShell topCrumb="重要汇报 / 汇报正文">
      <TerraBackLink href="/ceo-office/reports">返回重要汇报</TerraBackLink>
      <TerraPageHead
        title={r.title}
        subtitle={`汇报 ID：${id || DATA_COPY.noData}`}
        pill={{ text: "已审阅", icon: "i-check_circle" }}
        facts={[
          { value: r.author, label: "作者" },
          { value: r.date, label: "提交日期" },
        ]}
      />

      <TerraSampleBadge className="mb-4" />

      <div className="grid grid-cols-12 gap-3.5">
        <TerraCard className="col-span-8">
          <TerraCardHeader icon="i-description" iconClass="cyan" title="汇报正文" />
          <div className="mt-3 space-y-4">
            <div>
              <h3 className="font-ui-sans font-semibold text-lg text-ui-txt">{r.title}</h3>
              <div className="flex items-center gap-3 mt-1 text-xs text-ui-txt-3">
                <span>作者：{r.author}</span>
                <span>·</span>
                <span>{r.role}</span>
                <span>·</span>
                <span>{r.date}</span>
              </div>
            </div>

            <p className="text-sm text-ui-txt-2 leading-relaxed">{r.content}</p>

            <div className="grid grid-cols-3 gap-3">
              {(r.metrics || []).map((m, i) => (
                <div key={i} className="bg-ui-surface-2 rounded-ui-md px-3 py-2.5 text-center">
                  <div className="font-ui-sans font-bold text-xl text-ui-primary">{m.value}</div>
                  <div className="text-ui-1 text-ui-txt-3 mt-0.5">{m.label}</div>
                </div>
              ))}
            </div>

            <div className="flex items-center gap-2 bg-ui-green-soft border border-ui-green/20 rounded-ui-sm px-3 py-2 text-xs font-medium text-ui-green">
              <TerraIcon name="i-check_circle" className="w-4 h-4" />
              CEO 审阅状态：{r.reviewStatus}
            </div>
            <div className="text-right text-ui-1 text-ui-txt-3">{r.lastReview}</div>
          </div>
        </TerraCard>

        <TerraCard className="col-span-4">
          <TerraCardHeader icon="i-info" iconClass="primary" title="汇报元信息" />
          <div className="space-y-2 mt-1">
            {[
              { label: "汇报类型", value: "季度总结" },
              { label: "提交人", value: r.author },
              { label: "关联部门", value: DATA_COPY.unassigned },
              { label: "审阅人", value: "CEO" },
            ].map((row) => (
              <div key={row.label} className="flex justify-between gap-3 bg-ui-surface-2 rounded-ui-sm px-3 py-2">
                <span className="text-xs text-ui-txt-3 flex-shrink-0">{row.label}</span>
                <span className="text-xs text-ui-txt font-medium text-right truncate">{row.value}</span>
              </div>
            ))}
          </div>
        </TerraCard>

        <div className="col-span-12">
          <div className="flex items-center gap-2 bg-ui-accent-light border border-ui-line rounded-ui-sm px-3 py-2 text-ui-1 text-ui-accent">
            <TerraIcon name="i-verified" className="w-4 h-4 text-ui-accent" />
            汇报详情为示例快照（未接入真实数据）；审阅状态仅作展示，未写入后端。
          </div>
        </div>
      </div>
    </TerraShell>
  );
}
