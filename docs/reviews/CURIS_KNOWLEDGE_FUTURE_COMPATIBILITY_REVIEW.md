# CURIS — KNOWLEDGE FUTURE COMPATIBILITY REVIEW

Status: Review
Authority Class: REVIEW
Date: 2026-09-01
Disposition: COMPATIBILITY REVIEW COMPLETE — CANDIDATE CONTRACT READY FOR CEO / ARCHITECTURE REVIEW
Implementation: NOT AUTHORIZED

## A. Executive conclusion

现有 `CURIS_KNOWLEDGE_CANONICAL_SCOPE_TYPED_WORK_REFERENCE_CONTRACT.md` 能兼容未来 Knowledge 能力，但需要一项窄幅澄清：Work 是当前第一个消费方，不是关系模型的永久边界。typed reference 必须保持 source / relation / target 分离，未来可在同一 vocabulary 上增加 Meeting、Decision、Result、Artifact 等经批准的关系。

没有发现需要新 Product Surface、第二套 Knowledge Truth、Graph DB、Vector Truth 或新的 Runtime Primitive 的硬需求。当前资料库产品化门禁可在合同层解除；Schema/Runtime 实施仍需 CEO / Architecture 明确批准并回到原 Issue 重新开放 Allowed Files。

## B. Review inputs and authority boundary

- `docs/reviews/CURIS_KNOWLEDGE_CANONICAL_SCOPE_TYPED_WORK_REFERENCE_CONTRACT.md`（本轮唯一基础合同候选）
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_ACCEPTANCE.md`
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_RESEARCH.md`
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCTIZATION_REVIEW.md`
- `backend/app/knowledge_service.py`、`backend/app/context_service.py`、`backend/app/database.py`
- `backend/app/runtime/models.py`、`backend/app/runtime/foundation.py`
- 现有 Work / Execution / Result / Evidence / Artifact / Company OS Shared Authority

Research 只用于兼容性判断；不覆盖 Current Product Truth。当前实现仍是 manual + `.md/.txt`、legacy Project/Department scope、opaque Work refs 与 bounded Context snapshot。

## C. Compatibility matrix

| Capability | Product Definition Ready? | New UX Required? | New Authority Required? | Current Contract Compatible? | Foundation Change Needed Now? | Implement Now? | Deferred reason |
|---|---|---|---|---|---|---|---|
| Source Version / historical version | 部分；“Work 当时使用哪个版本”需后续产品确认 | 完整版本浏览/切换需要新 UX | 版本采用与保留规则需 Authority | YES | 仅保留 stable identity + version-ref extension seam | NO；当前产品化先保留 stable ref | 完整版本历史、比较与回溯尚未定产品合同 |
| Citation Anchor / locator | 资料级 reference 已就绪；段落/行/quote 未定 | YES，需阅读/引用交互 | 需确定 anchor provenance 规则 | YES | 仅保留 optional locator extension seam | NO | 完整 Citation UX 不是当前门禁 |
| Semantic / Vector Search | 检索目标可定义，但 V1 只要求有限搜索 | 可能需要搜索解释与排序 UX | 若只作派生索引无需新 Authority | YES | 无；稳定 id/scope/source 足够 | NO | 当前规模与成本未证明需要；Vector 只能是 DERIVED INDEX |
| External Connectors | Source Provider 语义明确，具体 Provider 未定 | YES，连接/授权/Health UX | 复用 Connector / Capability Authority | YES | 保持 source identity/type/scope seam | NO | 需要真实 Provider、授权与 Health 验证 |
| ACL / Access Control | scope 与 permission 必须分离 | YES | YES，影响 Company OS 权限 | YES（因未把 scope 当 ACL） | 不新增字段 | NO | 完整 ACL 是 Company OS/员工访问决策 |
| Knowledge Graph | 关系可由 typed vocabulary 扩展 | 图 UI 非必要 | 若成为产品图谱则需新 Authority | YES | 窄幅澄清 vocabulary 可扩展 | NO | 不需要 Graph DB、Graph UI 或 traversal platform |
| Result / Report Promotion | 只能在明确批准后成为 Knowledge | YES，需确认/来源/范围 | YES：谁批准、何时生效、未验证如何处理 | YES | 保留 Artifact/Result → explicit promotion seam | NO | 涉及 Truth ownership、scope、approval 与 provenance |
| Conflict Handling | Unknown / needs review 已存在 | 可能需要冲突阅读 UX | YES，若引入正式 Conflict state | YES | 无 | NO | 当前不建 Conflict Engine；来源不一致沿既有 Unknown/Review-needed |
| Archive / Tombstone | 已引用资料不可 hard delete 已明确 | 低；可先表达 archived/unavailable | 完整 retention policy 需 Authority | YES | **建议在本次产品化实现中加入最小删除保护** | **YES（bounded engineering）** | 它直接保护当前 Work reference 历史真相，不扩大产品面 |
| Scale / reverse index | 查询关系语义已明确 | NO | NO | YES | **建议随实现补现有 relation 的 source/target 索引** | **YES（bounded engineering）** | 低成本避免 Used By 在规模增长时退化；不建新表 |
| Multi-source / Dedup | source identity/type 已有；自动去重规则未定 | 可能需要来源比较 UX | 可能需要来源合并 Authority | YES | 无复杂预留 | NO | 先保留 source identity/content hash；不自动合并 |
| Offline / unavailable source | 当前状态语言已支持 | 低；详情显示 unavailable/last-known 即可 | 完整离线保留策略需 Authority | YES | **建议沿现有 lifecycle 保留 archived/unavailable 标记** | **YES（bounded engineering）** | 已引用历史必须可解释；不设计离线平台 |

`IMPLEMENT NOW` 仅指在原 Knowledge Productization Issue 获准后，一起完成当前门禁所需的 canonical scope、typed Work reference、reverse projection，以及 archive/delete guard 与必要 source/target index；本 Review 不执行这些改动。

## D. Source version / citation compatibility

当前合同已将 `knowledge_id` 与 title/path/hash 分离，因此正文更新不会无故改变 Knowledge identity。未来需要历史版本时，可在同一 identity 下挂 immutable source-version reference；未来需要 section/paragraph/line/quote 时，可把 optional locator 附着在 typed relation 或版本引用上。两者均不改变 relation 主模型，也不授权本轮创建 Version/Citation UI。

结论：`FOUNDATION COMPATIBLE / IMPLEMENTATION LATER`。

## E. Search / connector / ACL compatibility

- Search index（包括未来 vector）只能是派生索引，Knowledge identity、scope、source provenance 仍是 canonical truth；当前有限关键词搜索足够，暂无实现理由。
- Drive、Notion、GitHub、Web 等未来来源可作为 Source Provider，复用 `source_type + source identity + canonical scope + reference`；授权与健康状态继续归 Connector / Capability Authority，不创建 Library Connector 系统。
- `scope` 仅表示适用范围，不是 permission。未来 ACL 可引用同一 Company/Business/Workspace identity，但不得把权限塞入 `target_type` 或 target ref。

结论：`CURRENT CONTRACT COMPATIBLE; DEFER FULL IMPLEMENTATION`。

## F. Graph and typed reference breadth

本轮对原合同做了最小修订：Work 是第一消费者，但 typed reference 是可扩展词汇，不是 `work_knowledge_links` 专属结构。当前启用 `Work → USES_REFERENCE → Knowledge`；未来 Meeting、Decision、Result、Artifact 关系若获 Authority 批准，可复用同一 source/relation/target 形态。不要建立 Graph DB、Graph UI 或第二套关系存储。

结论：`TYPED REFERENCE CONTRACT ACCEPT WITH NARROW REVISION`。

## G. Result / Report promotion

`Artifact / Result → explicit promotion → Knowledge` 在结构上兼容，但不是当前自动动作。只有明确的批准人、effective time、scope、未验证状态和 provenance 后，才能成为长期公司依据；未验证 Result 不得静默晋升。当前仅保留 extension seam，等待独立 Product / Authority 决策。

## H. Archive, tombstone and scale

Archive/tombstone 是当前引用生命周期的直接完整性要求，不是新产品能力：已被 Work 引用的 Knowledge 不可 hard delete，历史 ref 必须仍能显示 archived/unavailable。实现时可在现有 truth 上加最小 guard；不定义完整 retention system。

Used By 反查继续使用同一关系。若当前关系落点需要索引，只增加既有 relation source/target 的 bounded index；不新建 reverse table。该建议不会改变产品语义。

## I. Multi-source and offline behavior

`source_type`、source identity、content hash 与 stable Knowledge identity 已为未来多来源提供区分基础，但不应自动 dedupe 或合并不同来源。Source 不可用时，保留 last-known reference/status；不要以 0、删除或新 Knowledge body 掩盖缺失。

## J. IMPLEMENT NOW

仅限在 CEO / Architecture 批准原合同后，由原 `CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001` 一次完成：

1. canonical Company / Business / Workspace scope；
2. typed Work → Knowledge relation、校验、幂等和 reverse Used By；
3. explicit refs first + bounded automatic Context merge；
4. archive/tombstone 或等价 hard-delete guard；
5. 已存在 relation 的必要 source/target 索引。

这些是当前产品化门禁的工程实现，不是新产品面；本 Review 未执行。

## K. FOUNDATION NOW

只保留兼容性边界，不新增 speculative 字段：

- stable Knowledge identity 与 canonical scope 分离；
- generic typed-reference vocabulary，不锁死 Work-only table；
- optional future version / locator / provenance extension seam；
- scope ≠ permission；
- Search/Vector 为 derived index；
- Result/Report promotion 必须 explicit、approved、provenance-preserving。

## L. DEFER

完整版本浏览、Citation UI、Semantic/Vector Search、External Connector、ACL、Knowledge Graph、Result/Report Promotion、Conflict Engine、自动 Dedup、完整 Offline/Retention policy 均需要后续独立 Product / UX / Authority Gate，当前只保证兼容。

## M. Contract verdict

- **KNOWLEDGE SCOPE CONTRACT: ACCEPT**（显式 Company / Business / Workspace target contract；legacy 不猜迁移）
- **TYPED REFERENCE CONTRACT: ACCEPT WITH NARROW REVISION**（generic vocabulary；Work 是当前消费者）
- **SCHEMA EXTENSION: REVISE / BOUNDED EXTENSION — REVIEW REQUIRED**（可作为后续 Issue 的受限实现范围，不是本轮授权）
- **FUTURE COMPATIBILITY: PASS**

### Blocker

**COMPATIBILITY BLOCKER: RESOLVED FOR IMPLEMENTATION PREPARATION**
**AUTHORITY / IMPLEMENTATION AUTHORIZATION: STILL OPEN**

当前可以把原 Productization Issue 作为下一实施候选，但在 CEO / Architecture 明确批准合同、补写 exact Allowed Files / hunks、migration 与测试门禁前，不得修改 Schema、Runtime、DB 或 Frontend。

## N. Next

Resume candidate after explicit approval:

`CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001`

必须先将本 Review 与修订后的 scope/reference 合同纳入该 Issue，再启动实现；本轮没有变更代码、Schema、DB、Migration、Connector、Vector、Graph 或 UI。

**KNOWLEDGE FUTURE COMPATIBILITY REVIEW COMPLETE**
**STOP FOR CEO / CHATGPT ARCHITECTURE REVIEW**
