# CURIS V1 — KNOWLEDGE CANONICAL SCOPE + TYPED WORK REFERENCE CONTRACT

Status: Review
Authority Class: REVIEW / ARCHITECTURE CANDIDATE
Date: 2026-09-01
Disposition: BLOCKER CONTRACT PROPOSED / ACCEPTED CANDIDATE FOR CEO / ARCHITECTURE REVIEW
Implementation: NOT AUTHORIZED

## 1. Purpose and decision boundary

本文件只定义资料库产品化所需的最小 scope 与 Work → Knowledge reference 合同。它是技术/参考合同候选，不是 Product Blueprint、Runtime Schema 或实现授权。

本合同只解决：

1. Knowledge 如何引用 canonical Company / Business / Workspace；
2. Work 如何持久化并消费一个 typed Knowledge reference；
3. 如何从同一关系反查 Used By Work，并沿 Work → Execution / Result / Evidence / Artifact 投影；
4. 如何保持 Context isolation、历史引用和 legacy 数据诚实。

本轮不建立 KnowledgeScopeV2、CitationDB、LibraryUsage、KnowledgeWorkLink、ReferenceStoreV2 或第二套 provenance graph；不处理 Employee、Department、Meeting、Result、Artifact 作为 Knowledge scope target，也不顺带定义 semantic search、Vector、ACL、External Connector、完整 Citation、Retention 或 Conflict Engine。

## 2. Authority and current evidence

### 2.1 Accepted product boundary

- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_ACCEPTANCE.md`：用户语言为“资料库”，内部心智为 Company Reference Space；scope 为 Company → Business → Workspace；Work ↔ Library ↔ Result 只共享引用，不复制正文。
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_UI_ACCEPTANCE.md`：Figma `187:2 / 187:276 / 187:550 / 187:824` 为当前 UI 基线；Work Picker 是 compact reference picker。
- `docs/01_Product/Curis_Product_Context.md` 与 `docs/03_Design/Curis_Company_OS_Shared_Authority.md`：Company → Department → Business → Workspace、责任/上下文隔离、Work/Result/Evidence 使用既有 Company OS truth。

### 2.2 Implementation evidence and blocker

`docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCTIZATION_REVIEW.md` 与 `issues/CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001.md` 已记录：

- `knowledge_entries` 当前只有隐含 Company（tenant）及 legacy `project_id` / `department_id`，没有 canonical Business / Workspace 关系；
- Work `inputRefs` 可保存字符串，但当前 resolver 不识别、校验或经 Context hydrate Knowledge；
- `context_packages.relevant_knowledge_json` 是 Context 快照，不是用户选中关系的写入 authority；
- `runtime_links` 要求两端都是合法、可解析的 Runtime entity，不能把 Knowledge 或 canonical Business/Workspace 直接塞入；
- 因此当前实现仍停在 `BLOCKED AT PRECISE CANONICAL PROJECTION GATE`。

本合同消费这些事实，不把它们改写成已实现能力。

## 3. Canonical Knowledge scope contract

### 3.1 Scope vocabulary

| Scope | canonical target_type | canonical target_ref | 必须验证 | 用户语言 |
|---|---|---|---|---|
| Company | `COMPANY` | 当前 Company 的稳定 `company_id` | tenant、Company 存在且属于当前身份 | 全公司资料 |
| Business | `BUSINESS` | 当前 Business 的稳定 `business_id` | tenant、Company、Business 存在；Business 属于当前 Company | 业务资料 |
| Workspace | `WORKSPACE` | 当前 Workspace 的稳定 `workspace_id` | tenant、Company、Workspace 存在；Workspace 属于 canonical Business，且该 Business 属于当前 Company | 工作空间资料 |

Company scope 必须有显式 `company_id`；不能用无 target、`owner_ref`、title、path 或 tenant alone 代替。`owner_ref` 是责任/所有者语义，不是资料适用范围。

`target_type + target_ref` 是本合同的语义要求；具体是现有行字段、既有 relation 结构还是受限扩展，必须由 Architecture Review 决定，不能在实现中静默发明字段或新表。

### 3.2 Scope invariants

- scope 不是正文复制。同一 Knowledge identity 可被多个合法范围引用；实现应复用同一 body 与 stable identity，不创建三份 Knowledge。
- Business / Workspace scope 必须沿 canonical parent chain 解析为 `Workspace → Business → Department → Company`（Department 关系由 Company Truth 验证）。
- 所有写入和读取必须限定当前 tenant 与 Company；Business/Workspace target 必须是当前 Company 的后代。
- target 不存在、已脱离当前 Company、类型不符、状态不允许或父关系无法解析时 fail-closed。
- 本轮不扩展 Employee、Department、Meeting、Result、Artifact 为 Knowledge target。Department 仅是 Business 的组织归属，不替代 Business scope。

## 4. Legacy Project / Department

现有 `project_id`、`department_id` 只允许作为：

- `LEGACY ONLY`；
- `MIGRATION INPUT`；
- `COMPATIBILITY READ`（在明确标示 legacy 的历史读取中）。

禁止 `project_id = business_id`、把 department 当 Business、通过 tags/JSON 猜 scope，或把 legacy 行自动挂到默认 Business / Workspace。

没有 canonical target 的旧行保持 `UNMAPPED / LEGACY`，可继续以兼容方式读取，但不能出现在 canonical Business/Workspace 筛选、Work reference 或 Used By projection 中，除非完成显式映射并留下可追溯记录。

## 5. Typed Work → Knowledge reference

### 5.1 Minimum relation

| 要素 | 合同 |
|---|---|
| Source | 一个真实 Work（现有 Work / Task identity） |
| Relation | 语义名 `USES_REFERENCE`，Knowledge 专用读取别名可为 `uses_knowledge`；最终名称沿用现有 reference vocabulary，由实现前 Review 定稿 |
| Target | Knowledge 的 stable canonical `knowledge_id` |
| Canonical ref form | `knowledge:<knowledge_id>` 作为 Work `inputRefs` 的 typed 表达候选；不得用 title/path/hash 作为 identity |
| Scope | Work 与 Knowledge 必须在同一 tenant / Company；Business / Workspace scope 必须与 Work 的当前 scope 兼容 |
| Idempotency | 同一 Work + relation + Knowledge 只保留一条有效关系；重复添加不得复制正文或产生重复事实 |

`knowledge:<id>` 是对现有 `inputRefs` opaque string 的最小 typed 语义约束，不是新 Runtime enum。实际保存位置可以复用现有 Work reference seam；不得把 `runtime_links` 当作自动获准的写入表。

### 5.3 Reference vocabulary extensibility

Work 是当前第一个消费方，但该语义不锁死为 Work 专属关系或 `work_knowledge_links` 表。长期兼容形态是可扩展的 typed reference vocabulary：每条关系保持 source type / source ref / relation / target type / target ref 的分离；本轮只启用 `Work → USES_REFERENCE → Knowledge`。未来 Meeting、Decision、Result、Artifact 等若获 Authority 批准，可复用同一 vocabulary 增加关系类型，不改变 Knowledge identity 或 scope contract。

未来可在同一关系上增加可选的 source-version、locator/anchor、provenance metadata，但这些不是本轮字段或 UI；不得把版本、段落、权限或来源信息塞进 `target_ref` 字符串。

### 5.2 Work Picker write

在“从工作选择资料”点击“添加所选资料”时，UI 的 pending selection 必须提交为上述 canonical Work → Knowledge relation；仅留在浏览器 local state 不算成功。提交后仍返回原 Work，并从同一关系重读已选资料。

允许添加关系的 actor 必须复用现有 Work write authority：CEO 或有权限的 Leader 可显式添加；Assigned Employee 只有在既有 Work authority 允许其编辑当前 Work 时才可添加；System 只能在 approved proposal / continuation 已携带明确 refs 时写入。禁止新增 Library-specific role/permission model。若 Work Authority 对具体 actor 没有最终列举，实施前必须补一条适用 Authority Review，不得自行放宽。

## 6. Reverse Used-by

“Knowledge 被哪些 Work 使用”必须由同一 canonical Work → Knowledge relation 反向查询，不新增 reverse table 或 `LibraryUsage` truth。

查询返回至少：Work id、Work scope、标题/摘要、状态、创建/更新时间及可解析的 Employee/Assignment context；所有结果按当前 tenant / Company / Business / Workspace 过滤。跨 Company 或无权 Business/Workspace 的 Work 必须不返回，而不是返回后再由 UI 隐藏。

同一关系可支持：

```text
Knowledge → Work → Execution / Result / Evidence / Artifact
```

反向视图不得把 Context 快照、标题或复制的正文当作关系 authority。

## 7. Result / Evidence projection

本轮不新增 Knowledge → Result 关系。资料详情的“相关结果 / Evidence”通过既有链路投影：

```text
Knowledge
  → canonical Work reference
  → existing Execution / Result / Evidence / Artifact refs
```

只有 Work/Execution/Result/Evidence 的真实可解析关系才可显示；没有真实来源时显示 Unknown / 暂无数据，不推断结果质量或外部业务结果。

## 8. Context Service behavior

Context Service 继续复用现有 bounded assembly，不创建 Context V2：

1. 先读取当前 Work 的显式 typed Knowledge refs；
2. 对每个 ref 验证 tenant、Company、Business、Workspace scope 与 Knowledge 状态；无效、过期或越权 ref fail-closed，并保留可解释原因；
3. 显式 refs 优先进入 Context，保持用户选择，不因自动检索而静默丢失；
4. 在剩余预算内合并现有 bounded automatic retrieval，自动候选必须只来自 Work 当前合法 scope；
5. 去重后生成现有 `context_packages.relevant_knowledge_json` 快照，记录 stable ref/source metadata，不把全库或全文历史注入 Employee；
6. 现有 `MAX_KNOWLEDGE=3` 或等价上限继续作为实现级 bounded rule；如需调整，单独以证据驱动，不在本合同新建产品指标。

因此，Context 快照是一次执行的 derived projection；Work → Knowledge relation 才是用户选中资料的持久化 authority。

## 9. Reference lifecycle

- **Update**：同一 Knowledge identity 原地更新时，已有 Work ref 仍指向同一 id；Context 读取当前可用版本/更新时间，并显示 freshness/provenance。若未来引入版本化，必须追加 version ref，不在本轮创建 Version system。
- **Historical version compatibility**：未来若需要回答“该 Work 当时使用的版本”，应在同一 Knowledge identity 下追加经批准的 immutable source-version reference；现有 Work relation 不得因正文更新而失去历史可解释性。
- **Locator compatibility**：未来 section / paragraph / line / quote anchor 作为可选 locator 附着于 typed relation 或版本引用，不改变 relation target，也不把 locator 当作 Knowledge identity。
- **Source unavailable**：来源文件失效或暂时不可读时，历史 Work ref 不静默消失；显示 `待连接 / 数据较旧 / 需要核实 / 未记录` 等真实状态，并保留 stable ref。
- **Archive**：归档不删除历史关系；Used By 与历史 Work 仍可解析为 archived/unavailable。
- **Delete**：已被 Work 引用的 Knowledge 禁止 hard delete。采用 archive/tombstone 或等价保留策略；完整 retention policy 不在本轮定义。

## 10. Read / write authority and isolation

### Write

- Knowledge scope 写入必须经过现有 KnowledgeService/native canonical identity validation；不从 title/path/project/department 猜 Business/Workspace。
- Work ref 写入必须经过现有 Work write authority 和同一 scope validator；不直接 SQL 插入 `runtime_links`。

### Read

- Knowledge by scope、Work references、Knowledge Used By Work、Result/Evidence projection 均只读当前合法 tenant/Company/Business/Workspace。
- Employee 通过 Assignment 服务多个 Workspace 不代表自动获得全部 Company Knowledge；每次执行仍按 Responsibility → current Workspace / Object → relevant refs 组装 Context。

## 11. Migration and compatibility

迁移采取 non-destructive、no-guess policy：

1. 先审计现有 Knowledge rows 的 project/department provenance；
2. 无法确定 canonical Business/Workspace 的行保持 `LEGACY / UNMAPPED`；
3. 只有 CEO/授权 Owner 的明确映射，或经批准的 deterministic migration plan，才可写入 canonical target；
4. 不重写正文、不复制 body、不覆盖历史 source path/hash/timestamps；
5. 旧 API/UI 可继续读 legacy rows，但必须标示 legacy，不得把它们当 canonical scoped records；
6. 任何迁移必须先有单独 Issue、dry-run/回滚策略、隔离 DB 证据与明确 acceptance，不由本合同授权执行。

## 12. Schema impact

**BOUNDED SCHEMA EXTENSION — REVIEW REQUIRED (NOT AUTHORIZED)**

现有字段无法同时表达 canonical Company/Business/Workspace scope 与 typed Work reference，因此不能诚实选择 `NO SCHEMA CHANGE`。但当前证据也不支持 `NEW PRIMITIVE REQUIRED`：优先扩展现有 `knowledge_entries` truth 与现有 Work reference/Context seam；只有 Architecture Review 证明现有 seam 无法承载时，才另行提出新 primitive。

候选扩展边界：

- `knowledge_entries` 的 canonical scope representation（或等价的既有 relation mechanism）；
- 现有 Work `inputRefs` 的 Knowledge typed validation / persistence / read path；
- reverse projection 使用同一 relation，禁止第二张关系表。

本节不是 schema 设计，也不授权 migration。

## 13. Developer implementation contract (after approval)

实现前必须由 Architecture / Main Development 重新确认 exact files/hunks。获准后，开发应能逐项证明：

- **Write**：Company/Business/Workspace scope 与 Work → Knowledge relation 写入 canonical authority；Work Picker 不是 local-only。
- **Read**：按 scope 查询 Knowledge、按 Work 读取 refs、按 Knowledge 反查 Used By Work。
- **Validate**：tenant、Company parent、Business parent、Workspace parent、lifecycle/status、权限与 typed target type。
- **Context**：显式 refs first，bounded automatic retrieval merge/dedupe，snapshot 非关系 authority。
- **Preserve**：manual / `.md/.txt` source truth、legacy rows、stable identity、source provenance、unknown/unavailable 状态、restart continuity。
- **Do not**：Project masquerade、free-form IDs、direct `runtime_links` bypass、第二套 Store、整库 hydration、fake reverse/result facts。

## 14. Test contract (future, not run in this review)

至少需要以下真实隔离测试；本轮不执行：

1. Company-scoped Knowledge 可创建/读取；
2. Business-scoped Knowledge 可创建/读取；
3. Workspace-scoped Knowledge 可创建/读取；
4. cross-tenant ref 拒绝；
5. invalid/missing target 拒绝；
6. Work Picker 添加并持久化 typed Knowledge ref；
7. Work 重新读取 refs；
8. Knowledge 反查 Used By Work；
9. Result/Evidence 通过 Work 链回查；
10. restart 后 scope/ref/reverse projection 保留；
11. legacy unmapped 行不被解释成 Business/Workspace；
12. Context isolation：越权、跨 Business、无合法 scope 的 ref fail-closed；
13. explicit refs 与 bounded automatic retrieval 合并且不丢失用户选择；
14. duplicate add 幂等且不复制 Knowledge body。

验收必须使用外部隔离 SQLite、真实 canonical identity、Browser/packaged Desktop 与 restart evidence；不能以静态页面、fixture、单个 API 200 或现有旧测试替代。

## 15. Blocker status and next gate

**BLOCKER STATUS: STILL BLOCKED**

本文件将当前门禁收敛为一个最小候选合同，但不覆盖 Frozen Authority、不批准 Schema/Runtime/DB/UI 实现，也不关闭 `CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001`。

### Required decision

CEO / Architecture 需要明确接受或退回：

1. Company/Business/Workspace 显式 canonical `target_type + target_ref`；
2. Work `inputRefs` 采用 `knowledge:<id>` 的 typed 语义并由现有 Work/Context seam 验证消费；
3. reverse Used By 与 Result/Evidence 继续从同一 Work relation 投影，而不建第二套 relation store；
4. Schema impact 允许以 bounded extension 方式评审，不提前授权 migration。

批准后，先回到原 Issue，补写 exact Allowed Files / hunks、migration/test plan 与 stop gates，再恢复 `CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001`。在此之前，Current implementation 仍是 blocked。

**KNOWLEDGE CANONICAL SCOPE + TYPED WORK REFERENCE CONTRACT READY**
**STOP FOR CEO / CHATGPT ARCHITECTURE REVIEW**
