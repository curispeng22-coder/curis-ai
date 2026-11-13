"use client";

import { useState } from "react";
import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import {
  TerraCard,
  TerraCardHeader,
  TerraTag,
  TerraEmpty,
  TerraBackLink,
  TerraPageHead,
} from "../../../components/terra/TerraPrimitives.js";
import {
  TerraEmptyState,
  TerraLoadingSkeleton,
  DATA_COPY,
  TerraSampleBadge,
} from "../../../components/terra/TerraState.js";

/** 示例汇报数据 */
const SAMPLE_REPORTS = {
  pending: [
    { id: "r1", title: "Q2 产品交付总结报告", author: "张伟", date: "2026-07-20 10:00", status: "pending" },
    { id: "r2", title: "AI 智能客服 POC 验收报告", author: "王芳", date: "2026-07-22 19:30", status: "pending" },
    { id: "r3", title: "移动端性能优化阶段性报告", author: "李明", date: "2026-07-23 09:15", status: "pending" },
    { id: "r4", title: "供应链数据迁移风险评估", author: "陈琳", date: "2026-07-24 16:00", status: "pending" },
    { id: "r5", title: "官网品牌升级最终验收", author: "刘洋", date: "2026-07-25 14:20", status: "reviewed" },
    { id: "r6", title: "Q2 财务审计报告", author: "赵敏", date: "2026-07-25 16:00", status: "archived" },
    { id: "r7", title: "Q2 财务审计报告", author: "赵敏", date: "2026-07-25 16:00", status: "archived" },
  ],
};

/** 当前选中的汇报详情 */
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

const TABS = [
  { key: "all", label: "全部" },
  { key: "pending", label: "待处理" },
  { key: "reviewed", label: "已审阅" },
  { key: "archived", label: "归档" },
];

export default function ReportsPage() {
  const [activeTab, setActiveTab] = useState("all");
  const [selectedReport, setSelectedReport] = useState(SAMPLE_DETAIL);

  const filteredReports = (SAMPLE_REPORTS.pending || []).filter((r) =>
    activeTab === "all" ? true : r.status === activeTab
  );

  const counts = {
    all: SAMPLE_REPORTS.pending.length,
    pending: SAMPLE_REPORTS.pending.filter((r) => r.status === "pending").length,
    reviewed: SAMPLE_REPORTS.pending.filter((r) => r.status === "reviewed").length,
    archived: SAMPLE_REPORTS.pending.filter((r) => r.status === "archived").length,
  };

  return (
    <TerraShell topCrumb="重要汇报">
      <TerraBackLink href="/ceo-office">返回总裁办公室</TerraBackLink>

      <TerraPageHead
        title="重要汇报"
        subtitle="接收与审阅各部门提交的关键汇报材料"
        facts={[
          { value: counts.pending, label: "待审阅" },
          { value: counts.reviewed, label: "已审阅" },
          { value: DATA_COPY.noData, label: "本周" },
        ]}
      />

      <TerraSampleBadge className="mb-4" />

      <div className="grid grid-cols-12 gap-3.5">
        {/* 汇报收件箱 */}
        <TerraCard className="col-span-5">
          <div className="flex items-center justify-between mb-3">
            <TerraCardHeader icon="i-mail" iconClass="primary" title="汇报收件箱" />
          </div>

          {/* Tab 切换 */}
          <div className="flex gap-1.5 mb-3">
            {TABS.map((tab) => (
              <button
                key={tab.key}
                type="button"
                onClick={() => setActiveTab(tab.key)}
                className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                  activeTab === tab.key
                    ? "bg-ui-primary text-ui-primary-fg"
                    : "bg-ui-surface-2 text-ui-txt-2 hover:bg-ui-surface-3"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* 汇报列表 */}
          <div className="space-y-1.5 max-h-[480px] overflow-y-auto">
            {filteredReports.length === 0 ? (
              <TerraEmpty icon="i-inbox">暂无{activeTab === "all" ? "" : TABS.find((t) => t.key === activeTab)?.label}汇报</TerraEmpty>
            ) : (
              filteredReports.map((report) => (
                <button
                  key={report.id}
                  type="button"
                  onClick={() => setSelectedReport({ ...SAMPLE_DETAIL, title: report.title, author: report.author })}
                  className={`w-full text-left px-3 py-2.5 rounded-ui-sm border transition-colors group ${
                    selectedReport?.title === report.title
                      ? "border-ui-primary bg-ui-primary-soft/30"
                      : "border-transparent hover:bg-ui-surface-2"
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <span className={`w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0 ${
                      report.status === "pending" ? "bg-ui-amber" :
                      report.status === "reviewed" ? "bg-ui-green" : "bg-ui-txt-3"
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="font-semibold text-sm text-ui-txt truncate group-hover:text-ui-primary transition-colors">{report.title}</div>
                      <div className="text-ui-1 text-ui-txt-3 mt-0.5">
                        {report.author} · {report.date}
                      </div>
                    </div>
                    <TerraTag color={
                      report.status === "pending" ? "amber" :
                      report.status === "reviewed" ? "green" : "grey"
                    }>
                      {report.status === "pending" ? "待审阅" :
                       report.status === "reviewed" ? "已审阅" : "归档"}
                    </TerraTag>
                  </div>
                </button>
              ))
            )}
          </div>
        </TerraCard>

        {/* 汇报正文 */}
        <TerraCard className="col-span-7">
          <TerraCardHeader icon="i-description" iconClass="cyan" title="汇报正文" />

          {selectedReport ? (
            <div className="mt-3 space-y-4">
              {/* 标题与元信息 */}
              <div>
                <h3 className="font-ui-sans font-semibold text-lg text-ui-txt">{selectedReport.title}</h3>
                <div className="flex items-center gap-3 mt-1 text-xs text-ui-txt-3">
                  <span>作者：{selectedReport.author}</span>
                  <span>·</span>
                  <span>{selectedReport.role}</span>
                  <span>·</span>
                  <span>{selectedReport.date}</span>
                </div>
              </div>

              {/* 正文内容 */}
              <p className="text-sm text-ui-txt-2 leading-relaxed">{selectedReport.content}</p>

              {/* 关键指标 */}
              <div className="grid grid-cols-3 gap-3">
                {(selectedReport.metrics || []).map((m, i) => (
                  <div key={i} className="bg-ui-surface-2 rounded-ui-md px-3 py-2.5 text-center">
                    <div className="font-ui-sans font-bold text-xl text-ui-primary">{m.value}</div>
                    <div className="text-ui-1 text-ui-txt-3 mt-0.5">{m.label}</div>
                  </div>
                ))}
              </div>

              {/* 审阅状态 */}
              <div className="flex items-center gap-2 bg-ui-green-soft border border-ui-green/20 rounded-ui-sm px-3 py-2 text-xs font-medium text-ui-green">
                <TerraIcon name="i-check_circle" className="w-4 h-4" />
                CEO 审阅状态：{selectedReport.reviewStatus}
              </div>

              <div className="text-right text-ui-1 text-ui-txt-3">{selectedReport.lastReview}</div>
            </div>
          ) : (
            <TerraEmptyState
              icon="i-description"
              title="选择一份汇报"
              description="从左侧列表中选择一份汇报以阅读详细内容。"
            />
          )}
        </TerraCard>
      </div>
    </TerraShell>
  );
}
