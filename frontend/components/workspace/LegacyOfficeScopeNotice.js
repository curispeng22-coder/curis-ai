// Honest out-of-scope marker for frozen legacy business-type office pages
// (RD / 小红书 XHS / 抖音 TTK). The pages and their components are preserved per the
// Product Freeze "do not delete historical work", but these businesses are outside the
// CURIS V1 contract (Content Growth / Writing / Music). The pages are reachable only by
// direct URL and must carry this notice; V1 entry surfaces never link to them.
// See CURIS-V1-LEGACY-RD-XHS-TTK-FREEZE-20261007 (CEO decision 2026-10-07).

export default function LegacyOfficeScopeNotice({ label = "该业务类型" }) {
  return (
    <div
      role="note"
      data-legacy-office-notice="true"
      className="mb-4 rounded-ui-md border border-ui-line bg-ui-surface-2 px-4 py-3"
    >
      <p className="text-ui-2 font-bold text-ui-txt">
        {label}不在 CURIS V1 范围内 · 专业工作面已冻结
      </p>
      <p className="mt-1 text-ui-1 leading-relaxed text-ui-txt-3">
        V1 仅包含内容增长、写作、音乐三类业务。此页面为历史工作数据的只读保留，不会从
        V1 导航或工作空间入口进入，执行链也不再接通新能力。小红书 / 抖音等平台在
        「内容增长」业务内继续提供现行经营能力。
      </p>
    </div>
  );
}
