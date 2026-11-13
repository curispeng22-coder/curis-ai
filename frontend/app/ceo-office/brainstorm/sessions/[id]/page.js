"use client";

import { useParams } from "next/navigation";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import { TerraIcon } from "../../../../../components/terra/TerraIcons.js";
import {
  TerraCard,
  TerraCardHeader,
  TerraTag,
  TerraBackLink,
  TerraPageHead,
} from "../../../../../components/terra/TerraPrimitives.js";
import {
  DATA_COPY,
  TerraSampleBadge,
} from "../../../../../components/terra/TerraState.js";

/** 示例快照：头脑风暴会话详情（未接入真实数据） */
const SAMPLE_SESSION = {
  topic: "小红书增长策略重构",
  participants: "内容增长部 · 5 人",
  status: "active",
  updatedAt: DATA_COPY.noData,
  background: "当前小红书渠道获客成本上升，需重构选题与脚本生产链路，提升单位内容转化。",
  ideas: [
    { author: "王芳", text: "建立选题热度榜，按周滚动淘汰低互动选题。", votes: 8 },
    { author: "李明", text: "引入 A/B 脚本模板，前 3 秒钩子标准化。", votes: 6 },
    { author: "陈琳", text: "把评论区高频问题沉淀为二次内容选题。", votes: 5 },
  ],
  conclusion: DATA_COPY.unassigned,
  decisions: DATA_COPY.unassigned,
};

export default function BrainstormSessionPage() {
  const params = useParams();
  const id = params?.id || "";
  const s = SAMPLE_SESSION;

  return (
    <TerraShell topCrumb="头脑风暴室 / 会话详情">
      <TerraBackLink href="/ceo-office/brainstorm">返回头脑风暴室</TerraBackLink>
      <TerraPageHead
        title={s.topic}
        subtitle={`会话 ID：${id || DATA_COPY.noData}`}
        pill={{ text: s.status === "active" ? "进行中" : "已沉淀", icon: "i-lightbulb" }}
        facts={[
          { value: s.participants, label: "参与方" },
          { value: s.updatedAt, label: "更新" },
        ]}
      />

      <TerraSampleBadge className="mb-4" />

      <div className="grid grid-cols-12 gap-3.5">
        <TerraCard className="col-span-8">
          <TerraCardHeader icon="i-lightbulb" iconClass="amber" title="风暴背景" />
          <p className="text-sm text-ui-txt-2 leading-relaxed mt-1">{s.background}</p>

          <div className="text-ui-1 text-ui-txt-2 font-bold mt-4 mb-2">创意池</div>
          <div className="space-y-2">
            {(s.ideas || []).map((idea, i) => (
              <div key={i} className="flex items-start gap-3 px-3 py-2.5 rounded-ui-md bg-ui-surface border border-ui-line">
                <span className="w-7 h-7 rounded-full bg-ui-primary-light text-ui-primary grid place-items-center text-ui-1 font-bold flex-shrink-0">
                  {(idea.author || "?")[0]}
                </span>
                <div className="flex-1 min-w-0">
                  <div className="text-xs text-ui-txt-3 mb-0.5">{idea.author}</div>
                  <div className="text-sm text-ui-txt leading-relaxed">{idea.text}</div>
                </div>
                <div className="flex items-center gap-1 text-ui-1 font-bold text-ui-primary flex-shrink-0">
                  <TerraIcon name="i-emoji_events" className="w-3.5 h-3.5" />
                  {idea.votes}
                </div>
              </div>
            ))}
          </div>
        </TerraCard>

        <TerraCard className="col-span-4">
          <TerraCardHeader icon="i-emoji_events" iconClass="green" title="沉淀结论" />
          <div className="space-y-2 mt-1">
            <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
              <div className="text-ui-1 text-ui-txt-3">结论</div>
              <div className="text-sm text-ui-txt font-medium mt-0.5">{s.conclusion}</div>
            </div>
            <div className="bg-ui-surface-2 rounded-ui-sm px-3 py-2">
              <div className="text-ui-1 text-ui-txt-3">决策</div>
              <div className="text-sm text-ui-txt font-medium mt-0.5">{s.decisions}</div>
            </div>
          </div>
          <div className="mt-3">
            <TerraTag color={s.status === "active" ? "amber" : "green"}>
              {s.status === "active" ? "进行中" : "已沉淀"}
            </TerraTag>
          </div>
        </TerraCard>

        <div className="col-span-12">
          <div className="flex items-center gap-2 bg-ui-accent-light border border-ui-line rounded-ui-sm px-3 py-2 text-ui-1 text-ui-accent">
            <TerraIcon name="i-verified" className="w-4 h-4 text-ui-accent" />
            会话详情为示例快照（未接入真实数据）；投票与结论仅作展示。
          </div>
        </div>
      </div>
    </TerraShell>
  );
}
