"use client";

import { useEffect, useState } from "react";
import TerraShell from "../../../components/terra/TerraShell.js";
import {
  TerraPageHead,
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraDrawer,
  TerraEmpty,
  TerraTag,
} from "../../../components/terra/TerraPrimitives.js";
import { TerraIcon } from "../../../components/terra/TerraIcons.js";
import TaskLauncher from "../../../components/terra/TaskLauncher.js";
import { getStrategyMeetings, createStrategyMeeting } from "../../../lib/api.js";

/**
 * AI 会议室 / 战略会议室（总裁办公室二级，GlobalAssistant「AI 会议室」入口）。
 *
 * 左：战略会议空间（会议列表 + 新建）；右：选中会议的上下文 + 一键启动 AI 战略简报。
 * 会议持久化走真实后端 /api/workspace/strategy-meetings（租户隔离，无密钥列）；
 * AI 简报复用 TaskLauncher → POST /api/task + /run，真实执行、不伪造结果。
 */

const STATUS_LABEL = {
  scheduled: { label: "待开始", color: "grey" },
  active: { label: "进行中", color: "amber" },
  closed: { label: "已结束", color: "green" },
};

function MeetingCard({ m, selected, onSelect }) {
  const status = STATUS_LABEL[m.status] || STATUS_LABEL.scheduled;
  return (
    <button
      type="button"
      onClick={() => onSelect(m)}
      className={`mb-3 block w-full rounded-ui-sm border bg-ui-surface px-4 py-3 text-left transition ${
        selected ? "border-ui-primary ring-1 ring-ui-primary/40" : "border-ui-line hover:border-ui-primary/50"
      }`}
    >
      <div className="flex items-center justify-between gap-2">
        <span className="text-sm font-semibold text-ui-txt">{m.title}</span>
        <TerraTag color={status.color}>{status.label}</TerraTag>
      </div>
      {m.agenda ? (
        <p className="mt-1 line-clamp-2 text-xs leading-relaxed text-ui-txt-2">{m.agenda}</p>
      ) : null}
      <div className="mt-2 flex flex-wrap items-center gap-1.5">
        {(m.participants || []).map((p, i) => (
          <span
            key={i}
            className="rounded-full bg-ui-surface-2 px-2 py-0.5 text-[11px] text-ui-txt-3"
          >
            {p}
          </span>
        ))}
        <span className="ml-auto text-[11px] text-ui-txt-3">{m.created_at?.slice(0, 10)}</span>
      </div>
    </button>
  );
}

export default function StrategyRoomPage() {
  const [meetings, setMeetings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedId, setSelectedId] = useState("");
  const [composerOpen, setComposerOpen] = useState(false);
  const [form, setForm] = useState({ title: "", agenda: "", participants: "" });
  const [creating, setCreating] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const data = await getStrategyMeetings();
      const list = data?.meetings || [];
      setMeetings(list);
      setSelectedId((prev) => prev || list[0]?.meeting_id || "");
    } catch (err) {
      setError(err?.message || "会议列表加载失败");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const selected = meetings.find((m) => m.meeting_id === selectedId) || null;

  async function submitComposer(event) {
    event.preventDefault();
    if (!form.title.trim() || creating) return;
    setCreating(true);
    setError("");
    try {
      const created = await createStrategyMeeting({
        title: form.title.trim(),
        agenda: form.agenda.trim(),
        participants: form.participants
          .split(/[,，]/)
          .map((s) => s.trim())
          .filter(Boolean),
      });
      setComposerOpen(false);
      setForm({ title: "", agenda: "", participants: "" });
      await load();
      setSelectedId(created?.meeting_id || "");
    } catch (err) {
      setError(err?.message || "会议创建失败");
    } finally {
      setCreating(false);
    }
  }

  return (
    <TerraShell topCrumb="总裁办公室 · Curis">
      <TerraPageHead
        title="AI 会议室"
        subtitle="组织与管理公司战略级别会议"
        pill={{ icon: "i-spark", text: "CEO 专属战略空间" }}
        actions={
          <TerraButton variant="primary" onClick={() => setComposerOpen(true)}>
            <TerraIcon name="i-add" className="mr-1" /> 新建战略会议
          </TerraButton>
        }
      />

      <div className="grid grid-cols-12 gap-4">
        {/* 左：战略会议空间 */}
        <div className="col-span-8">
          <h3 className="mb-3 text-ui-3 font-semibold text-ui-txt">战略会议空间</h3>
          {loading ? (
            <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-2 text-xs text-ui-txt-3">
              正在加载会议…
            </div>
          ) : error && meetings.length === 0 ? (
            <p className="text-xs text-ui-red">{error}</p>
          ) : meetings.length === 0 ? (
            <TerraEmpty icon="i-spark">
              <p className="text-sm font-semibold text-ui-txt">还没有战略会议</p>
              <p className="mt-1 text-xs leading-relaxed">
                新建一场战略会议，组织议题与参与方；可在右侧为会议启动 AI 战略简报。
              </p>
              <div className="mt-3">
                <TerraButton variant="primary" onClick={() => setComposerOpen(true)}>
                  新建战略会议
                </TerraButton>
              </div>
            </TerraEmpty>
          ) : (
            meetings.map((m) => (
              <MeetingCard
                key={m.meeting_id}
                m={m}
                selected={m.meeting_id === selectedId}
                onSelect={(x) => setSelectedId(x.meeting_id)}
              />
            ))
          )}
        </div>

        {/* 右：当前会议上下文 */}
        <div className="col-span-4">
          <h3 className="mb-3 text-ui-3 font-semibold text-ui-txt">当前会议上下文</h3>
          {selected ? (
            <TerraCard>
              <TerraCardHeader icon="i-spark" iconClass="primary" title={selected.title} />
              <div className="space-y-3 text-xs leading-relaxed text-ui-txt-2">
                <div>
                  <span className="text-ui-txt-3">状态：</span>
                  <TerraTag color={(STATUS_LABEL[selected.status] || STATUS_LABEL.scheduled).color}>
                    {(STATUS_LABEL[selected.status] || STATUS_LABEL.scheduled).label}
                  </TerraTag>
                </div>
                <div>
                  <span className="text-ui-txt-3">议题：</span>
                  <p className="mt-1 whitespace-pre-wrap">{selected.agenda || "（未填写）"}</p>
                </div>
                <div>
                  <span className="text-ui-txt-3">参与方：</span>
                  <div className="mt-1 flex flex-wrap gap-1.5">
                    {(selected.participants || []).map((p, i) => (
                      <span key={i} className="rounded-full bg-ui-surface-2 px-2 py-0.5 text-[11px] text-ui-txt-3">
                        {p}
                      </span>
                    ))}
                    {(selected.participants || []).length === 0 && <span>—</span>}
                  </div>
                </div>
              </div>
              <div className="mt-4 border-t border-ui-line pt-4">
                <TaskLauncher
                  title={`为《${selected.title}》启动 AI 战略简报`}
                  defaultContent={`为战略会议《${selected.title}》生成战略简报：现状研判、关键决策点、可执行建议与风险。`}
                />
              </div>
            </TerraCard>
          ) : (
            <div className="rounded-ui-sm border border-ui-line bg-ui-surface-2 px-3 py-6 text-center text-xs text-ui-txt-3">
              选择左侧会议查看上下文，或新建一场战略会议。
            </div>
          )}
        </div>
      </div>

      <TerraDrawer
        open={composerOpen}
        title="新建战略会议"
        description="记录会议主题、议题与参与方；创建后可在右侧启动 AI 战略简报。"
        onClose={() => setComposerOpen(false)}
      >
        <form onSubmit={submitComposer} className="space-y-4">
          <div>
            <label className="mb-1.5 block text-xs font-bold text-ui-txt-2">会议标题</label>
            <input
              value={form.title}
              onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
              placeholder="例如：Q3 市场进入战略"
              className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none focus:border-ui-primary"
            />
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-bold text-ui-txt-2">议题</label>
            <textarea
              value={form.agenda}
              onChange={(e) => setForm((f) => ({ ...f, agenda: e.target.value }))}
              placeholder="本次战略会议要讨论的核心议题"
              rows={3}
              className="w-full resize-none rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none focus:border-ui-primary"
            />
          </div>
          <div>
            <label className="mb-1.5 block text-xs font-bold text-ui-txt-2">参与方</label>
            <input
              value={form.participants}
              onChange={(e) => setForm((f) => ({ ...f, participants: e.target.value }))}
              placeholder="逗号分隔，例如：研发部, 市场部, 运营部"
              className="w-full rounded-ui-sm border border-ui-line bg-ui-surface px-3 py-2 text-sm text-ui-txt outline-none focus:border-ui-primary"
            />
          </div>
          {error && <p className="text-xs text-ui-red">{error}</p>}
          <div className="flex justify-end gap-3">
            <TerraButton type="button" variant="ghost" onClick={() => setComposerOpen(false)}>
              取消
            </TerraButton>
            <TerraButton type="submit" variant="primary" disabled={!form.title.trim() || creating}>
              {creating ? "创建中…" : "创建会议"}
            </TerraButton>
          </div>
        </form>
      </TerraDrawer>
    </TerraShell>
  );
}
