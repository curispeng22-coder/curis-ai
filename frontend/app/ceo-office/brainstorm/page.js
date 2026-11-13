"use client";

import { Suspense, useState } from "react";
import { useSearchParams } from "next/navigation";
import TerraShell from "../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import {
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraTag,
  TerraPageHead,
  TerraSearch,
} from "../../../components/terra/TerraPrimitives.js";
import {
  TerraEmptyState,
  TerraLoadingSkeleton,
  DATA_COPY,
  TerraSampleBadge,
} from "../../../components/terra/TerraState.js";

const VIEWS = [
  { key: "active", label: "进行中的风暴", icon: "i-lightbulb" },
  { key: "results", label: "已沉淀成果", icon: "i-emoji_events" },
];

/** 示例快照：头脑风暴会话（未接入真实数据） */
const SAMPLE_ACTIVE = [
  { id: "bs-1", topic: "小红书增长策略重构", participants: "内容增长部 · 5 人", status: "active", updatedAt: DATA_COPY.noData },
  { id: "bs-2", topic: "微信小程序拉新方案", participants: "研发部 · 3 人", status: "active", updatedAt: DATA_COPY.noData },
];
const SAMPLE_RESULTS = [
  { id: "bsr-1", topic: "AI 客服话术库", conclusion: "沉淀 42 条高转化话术", decisions: "采纳 A 方案", updatedAt: DATA_COPY.noData },
  { id: "bsr-2", topic: "季度内容选题矩阵", conclusion: "形成 6 大选题方向", decisions: "已归档", updatedAt: DATA_COPY.noData },
];

function BrainstormInner() {
  const searchParams = useSearchParams();
  const view = searchParams.get("view") || "active";
  const [searchQuery, setSearchQuery] = useState("");
  const [loading] = useState(false);

  const list = view === "results" ? SAMPLE_RESULTS : SAMPLE_ACTIVE;
  const filtered = list.filter((s) =>
    !searchQuery.trim() || s.topic.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (loading) {
    return (
      <TerraShell topCrumb="头脑风暴室">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }

  return (
    <TerraShell topCrumb="头脑风暴室" topbarExtra={<TerraSearch placeholder="搜索风暴…" value={searchQuery} onChange={setSearchQuery} />}>
      <TerraPageHead
        title="头脑风暴室"
        subtitle="发起并沉淀公司级创意风暴"
        pill={{ text: "CEO 专属创意空间", icon: "i-lightbulb" }}
      />

      {/* 视图 Tab（query param 接线） */}
      <div className="flex items-center gap-2 mb-4 overflow-x-auto pb-1 no-h-scroll">
        {VIEWS.map((v) => (
          <a
            key={v.key}
            href={`/ceo-office/brainstorm?view=${v.key}`}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-colors no-underline ${
              view === v.key
                ? "bg-ui-primary text-ui-primary-fg"
                : "bg-ui-surface-2 text-ui-txt-2 hover:bg-ui-surface-3"
            }`}
          >
            <TerraIcon name={v.icon} className="w-3.5 h-3.5" />
            {v.label}
          </a>
        ))}
      </div>

      <TerraSampleBadge className="mb-4" />

      {filtered.length === 0 ? (
        <TerraCard>
          <TerraEmptyState
            icon="i-lightbulb"
            title={view === "results" ? "暂无沉淀成果" : "暂无进行中的风暴"}
            description="未接入头脑风暴会话数据。上方为示例快照结构，便于理解信息层级。"
          />
        </TerraCard>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          {filtered.map((s) => (
            <a
              key={s.id}
              href={`/ceo-office/brainstorm/sessions/${s.id}`}
              className="no-underline"
            >
              <TerraCard hover>
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className="w-9 h-9 rounded-lg bg-ui-primary-light text-ui-primary grid place-items-center text-sm font-bold flex-shrink-0">
                      <TerraIcon name="i-lightbulb" className="w-5 h-5" />
                    </span>
                    <div className="min-w-0">
                      <div className="font-ui-sans font-semibold text-ui-4 text-ui-txt truncate">{s.topic}</div>
                      <div className="text-ui-1 text-ui-txt-3 mt-0.5 truncate">{s.participants}</div>
                    </div>
                  </div>
                  <TerraTag color={view === "results" ? "green" : "amber"}>
                    {view === "results" ? "已沉淀" : "进行中"}
                  </TerraTag>
                </div>
                {view === "results" ? (
                  <div className="text-xs text-ui-txt-2 leading-relaxed">
                    <span className="text-ui-txt-3">结论：</span>{s.conclusion}
                    <div className="mt-1 text-ui-txt-3">决策：{s.decisions}</div>
                  </div>
                ) : (
                  <div className="text-xs text-ui-txt-3 mt-1">更新时间：{s.updatedAt}</div>
                )}
              </TerraCard>
            </a>
          ))}
        </div>
      )}

      <div className="mt-4">
        <div className="flex items-center gap-2 bg-ui-accent-light border border-ui-line rounded-ui-sm px-3 py-2 text-ui-1 text-ui-accent">
          <TerraIcon name="i-verified" className="w-4 h-4 text-ui-accent" />
          头脑风暴会话为示例快照（未接入真实数据）；点击卡片进入会话详情草稿视图。
        </div>
      </div>
    </TerraShell>
  );
}

export default function BrainstormPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-ui-bg" />}>
      <BrainstormInner />
    </Suspense>
  );
}
