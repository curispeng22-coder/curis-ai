# Company Package → 可执行 Workflow 来源追溯 L2 Review

Issue：`issues/shared/20260718_workspace_admin_company_package_workflow_provenance_l2.md`  
裁决建议：选择 **B：Shared 显式 Package → 可执行 Workflow 桥接关系 / 只读 API**。  
范围：只读评审；未修改资产、代码、数据库或历史数据。

## 选择 B 的理由

当前 `ccp_ai_software_company` 只有 `workflow_refs_json`，实例化写入 `workflow_instances` 时只保留 Workflow/template 来源，不能证明实例来自哪个 Package 版本；现有 Package 引用的 6 个 Workflow Template 又全部为 `design_only`，唯一 `structured_executable` 的 `official.workflow.software_rnd_sop` 不在 Package 内。

A 仅修订 Admin Package 并加入可执行 Workflow，仍不能自动给实例保留“Package ID + Package version + Workflow template version”的不可变来源；若把现有 `design_only` 改成可执行则违反能力态边界，若另挂可执行模板又仍需一层明确关联。因此 A 不能同时闭合两项事实，除非额外承担 Shared 运行态来源落点，越过题目限定。

B 直接建立明确关联：Package 的版本化来源与批准的可执行 Workflow 版本分开记录，实例化时固化来源快照，Workspace 只读消费并在运行链路中校验，不把 `design_only` 当作可执行。

## B 的最小数据边界

新增一个 Shared additive 桥接关系，逻辑字段最少为：

- `company_package_id`、`package_version`；
- `workflow_template_id`、`workflow_template_version`；
- `workflow_capability_status`，只能为 `structured_executable`；
- `tenant_id`/来源作用域、`status`、`created_at`、`revoked_at`；
- 唯一键：`(company_package_id, package_version, workflow_template_id, workflow_template_version)`。

实例化后的 `workflow_instances` 必须固化 `source_company_package_id`、`source_package_version`、`source_workflow_template_id`、`source_workflow_template_version`；这些是来源快照，不随目录后续版本漂移。现有 `company.instantiated` 事件继续保留，并补充 package version 与桥接版本引用；历史实例不猜测回填，保持不可证明状态。

桥接记录只能指向已存在、active、`structured_executable` 的官方 Workflow；`design_only`、disabled、revoked、版本缺失或 Package/template 不匹配均拒绝实例化。桥接不改 Provider、Model、Gateway、Token、成本或 Workflow 执行语义。

## 最小只读 API

Shared 只增加一个只读查询面（名称可沿现有 Workspace catalog 命名）：

`GET /api/catalog/company-packages/{package_id}/workflows?version=<package_version>`

响应必须逐项返回 package/version、workflow template/version、capability status、tenant/source、bridge status；不得返回 secret 或可写字段。Workspace 实例/Run 详情同时返回固化的 source package/template 版本引用。不存在、跨租户、版本不一致、design_only 或 revoked 均 fail-closed，不返回“可执行”假象。

## 版本、回滚与审计

- Package、Workflow、Bridge 三者均为不可变版本；修订生成新版本，不覆盖已消费版本。
- 新 Bridge 先校验目标 Workflow 为 `structured_executable`，再允许新隔离实例消费；不修改历史 `company-a`。
- 撤销只影响尚未实例化/尚未启用的 Bridge；已创建实例继续使用其固化快照，但后续运行必须再次校验 instance status、binding 和安全边界。
- 回滚为将新 Bridge 置 revoked/disabled 并恢复上一批准 Bridge 版本；不能把旧 `design_only` 当可执行，也不能删除或重写历史来源事件。
- 冲突、重复 active Bridge、缺版本、来源字段缺失或历史实例没有来源时停止并报告，不猜测回填。

## 最小允许范围

- Admin：提供版本化 Package/Workflow 资产证据，确保被桥接 Workflow 明确为 `structured_executable`；不修改历史包或历史实例。
- Shared：新增桥接关系及实例来源快照、只读 API、实例化前校验和 focused tests。
- Quality：独立验证 Package version → Bridge → executable Workflow version → Company/Department/Employee/Binding/Run/Usage 链路。

禁止前端、Provider、模型、Gateway、完整 RBAC、通用成果平台、历史数据猜测回填及真实模型执行扩展。

## 裁决结论

建议总控决策席批准 **B**。它是唯一能在不伪造 `design_only` 能力的前提下，同时补齐“精确 Package 来源”和“可执行 Workflow 来源”的最小方案。批准前维持 `BLOCKED_L2`，不启动模型执行。

Handoff: sent to 总控决策席。
