"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import TerraShell from "../../../../../components/terra/TerraShell.js";
import {
  TerraBackLink,
  TerraBoundary,
  TerraButton,
  TerraCard,
  TerraCardHeader,
  TerraPageHead,
  TerraTag,
} from "../../../../../components/terra/TerraPrimitives.js";
import {
  TerraErrorState,
  TerraLoadingSkeleton,
} from "../../../../../components/terra/TerraState.js";
import {
  getCapability,
  getModelGatewaySummary,
  updateCapabilityStatus,
} from "../../../../../lib/capabilities.js";

const TYPE_LABEL = {
  model: "模型",
  agent: "Agent",
  skill: "技能",
  tool: "工具",
  workflow: "工作流",
  connector: "连接器",
};

function costText(facts) {
  const rows = facts?.cost_by_currency;
  if (!rows?.length) return facts == null ? "尚未读取" : "未记录";
  return rows.map(row => {
    const known = row.known_cost;
    const label = row.currency === "UNKNOWN" ? "币种未知" : row.currency;
    const amount = known == null ? "" : `${Number(known).toFixed(4)} ${label}`;
    return row.unknown_cost_count > 0
      ? `${amount ? `已知部分 ${amount}；` : ""}${row.unknown_cost_count} 次费用未知`
      : amount || "费用未知";
  }).join("；");
}

export default function CapabilityDetailPage() {
  const params = useParams();
  const id = Array.isArray(params?.id) ? params.id[0] : params?.id;
  const [capability, setCapability] = useState(null);
  const [gateway, setGateway] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [error, setError] = useState("");

  const loadCapability = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError("");
    try {
      const item = await getCapability(id);
      setCapability(item);
      setGateway(item.type === "model" ? await getModelGatewaySummary() : null);
    } catch (err) {
      setError(err?.message || "能力详情读取失败");
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => { loadCapability(); }, [loadCapability]);

  async function changeStatus() {
    setUpdating(true);
    setError("");
    try {
      setCapability(await updateCapabilityStatus(
        capability.capability_key,
        capability.status === "active" ? "disable" : "enable"
      ));
    } catch (err) {
      setError(err?.message || "能力状态更新失败");
    } finally {
      setUpdating(false);
    }
  }

  if (loading) {
    return (
      <TerraShell topCrumb="能力中心 / 详情">
        <TerraLoadingSkeleton variant="page" />
      </TerraShell>
    );
  }
  if (!capability) {
    return (
      <TerraShell topCrumb="能力中心 / 详情">
        <TerraErrorState message={error || "能力不存在"} onRetry={loadCapability} />
      </TerraShell>
    );
  }

  const migratedDraft = capability.migration_status === "draft_candidate";
  const inputSchema = capability.io_schema?.input;
  const outputSchema = capability.io_schema?.output;
  const provider = gateway?.providers?.find(
    (item) => item.gateway_id === capability.gateway_ref
  );
  const modelUsage = gateway?.usage?.by_model?.find(
    (item) => item.model_gateway_id === capability.gateway_ref
      && item.model_name === capability.model_name
  );

  return (
    <TerraShell topCrumb={`能力中心 / ${TYPE_LABEL[capability.type] || capability.type}详情`}>
      <TerraBackLink href={`/ceo-office/capabilities?type=${capability.type}`}>
        返回能力中心
      </TerraBackLink>
      <TerraPageHead
        title={capability.name}
        subtitle={`能力 ID：${capability.capability_key} · 类型：${TYPE_LABEL[capability.type] || capability.type}`}
        pill={{
          text: capability.status === "active" ? "已启用" : "已停用",
          icon: "i-auto_awesome",
        }}
        facts={[
          { value: capability.provider_id || capability.source || "未记录", label: "来源" },
          { value: capability.version || "未记录", label: "版本" },
          { value: capability.live_status || "unknown", label: "运行状态" },
          ...(capability.type === "model"
            ? [{ value: capability.model_name || "未记录", label: "调用模型" }]
            : []),
        ]}
        actions={(
          <TerraButton
            variant={capability.status === "active" ? "ghost" : "primary"}
            onClick={changeStatus}
            disabled={updating}
          >
            {updating ? "更新中…" : capability.status === "active" ? "停用能力" : "启用能力"}
          </TerraButton>
        )}
      />

      {error && <p className="mb-3 text-xs text-ui-red">{error}</p>}
      {migratedDraft && (
        <TerraBoundary className="mb-4">
          历史 Skill 许可为 {capability.license || "NOASSERTION"}，不允许商用；许可复核前不可启用。
        </TerraBoundary>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-3.5">
        <TerraCard className="lg:col-span-8">
          <TerraCardHeader icon="i-info" iconClass="primary" title="能力说明" />
          <p className="text-sm text-ui-txt-2 leading-relaxed mt-1">
            {capability.description || "未记录能力说明"}
          </p>
        </TerraCard>

        <TerraCard className="lg:col-span-4">
          <TerraCardHeader icon="i-dataset" iconClass="violet" title="登记信息" />
          <dl className="space-y-2 text-xs">
            <div><dt className="text-ui-txt-3">状态</dt><dd className="mt-0.5"><TerraTag color={capability.status === "active" ? "green" : "grey"}>{capability.status === "active" ? "已启用" : "已停用"}</TerraTag></dd></div>
            <div><dt className="text-ui-txt-3">登记来源</dt><dd className="text-ui-txt mt-0.5 break-all">{capability.source || "未记录"}</dd></div>
            <div><dt className="text-ui-txt-3">提供方</dt><dd className="text-ui-txt mt-0.5 break-all">{capability.provider_id || "未记录"}</dd></div>
            {capability.type === "model" && <div><dt className="text-ui-txt-3">Provider 状态</dt><dd className="text-ui-txt mt-0.5 break-all">{provider?.status === "active" ? "已连接" : provider ? "已停用" : "未配置"}</dd></div>}
            {capability.source_template_id && <div><dt className="text-ui-txt-3">原 Skill ID</dt><dd className="text-ui-txt mt-0.5 break-all">{capability.source_template_id}</dd></div>}
          </dl>
        </TerraCard>

        {capability.type === "model" && (
          <TerraCard className="lg:col-span-12">
            <TerraCardHeader icon="i-memory" iconClass="green" title="Model Gateway 使用事实" />
            <dl className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
              <div><dt className="text-ui-txt-3">Provider</dt><dd className="text-ui-txt mt-0.5">{provider?.name || capability.gateway_ref || "未记录"}</dd></div>
              <div><dt className="text-ui-txt-3">调用次数</dt><dd className="text-ui-txt mt-0.5">{modelUsage?.usage_event_count ?? 0}</dd></div>
              <div><dt className="text-ui-txt-3">Token</dt><dd className="text-ui-txt mt-0.5">{modelUsage?.total_tokens ?? "未记录"}</dd></div>
              <div><dt className="text-ui-txt-3">成本</dt><dd className="text-ui-txt mt-0.5">{costText(modelUsage || (gateway ? { cost_by_currency: [] } : null))}</dd></div>
            </dl>
            <p className="text-ui-1 text-ui-txt-3 mt-3">
              明确选择的模型失败时不会自动改投其他供应商；金额未知不代表免费，记录成本不等于实际账单。
            </p>
          </TerraCard>
        )}

        <TerraCard className="lg:col-span-12">
          <TerraCardHeader icon="i-terminal" iconClass="cyan" title="接口契约" />
          {inputSchema || outputSchema ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <pre className="overflow-x-auto rounded-ui-sm bg-ui-surface-2 p-3 text-xs text-ui-txt">{JSON.stringify(inputSchema || {}, null, 2)}</pre>
              <pre className="overflow-x-auto rounded-ui-sm bg-ui-surface-2 p-3 text-xs text-ui-txt">{JSON.stringify(outputSchema || {}, null, 2)}</pre>
            </div>
          ) : (
            <p className="text-sm text-ui-txt-3">未记录输入与输出契约。</p>
          )}
        </TerraCard>
      </div>
    </TerraShell>
  );
}
