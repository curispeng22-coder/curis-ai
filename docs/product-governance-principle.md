# 产品级治理原则（B 层运行时 · 小白用户"拍板闸"）

> 定位：Curis Workspace 运行时（B 层）的产品级治理原则，约束"终端用户的 AI 公司"在自治运行时的边界呈现方式。
> 关联：`docs/architecture/b-layer-runtime-governance.md`（详细设计）、`docs/architecture/paperclip-curis-mapping-report.md`（外部参照）、运营协定 v2（席位链 / 默认自主推进）。
> 生效：2026-07-20 总控决策席拍板。

## 0. 一句话原则

**终端用户是技术小白**：系统替他做**所有技术决断**；只有当某个动作跨越高影响业务边界（钱 / 数据 / 对外声誉 / 不可逆 / 外部）时，才弹一次"拍板闸"。这个闸**不是技术审批闸**，而是**业务风险 / 效果对比闸**。

## 1. 最高约束（不可妥协）

- 系统自主做**全部技术决断**，绝不需要用户做技术裁决。
- 闸只对用户呈现二选一：
  - (a) 用大白话告诉他**可能的业务危险**；或
  - (b) 给出**几种方案各自产生的不一样效果**，让他基于业务后果选。
- **绝不让用户判断技术细节**（如"要不要改 schema""用哪个 API""是否绕过沙箱"）。
- **文案禁词红线**：sandbox / schema / API / token / diff / 回滚 / 部署 / 端点 / 进程 / 权限位 等术语一律禁止出现在给用户的闸里；生成含禁词即**回退"先模拟(B)+取消(C)"二元安全闸**。
- 标准选项工厂：**A 继续 / B 先模拟看看 / C 取消 /（可选）D 换个做法**。

## 2. 默认 fail-closed 动作（G1–G8）

见 `docs/architecture/b-layer-runtime-governance.md` §1。八类动作（真实部署 / 对外发消息·调外部接口 / 删覆盖数据 / 超预算 token / 改计费配置 / 开 Marketplace / 改权限边界 / 改新核心资产体系）默认全部弹闸；用户可在配置里显式关掉某类或加免确认白名单。横切"不可逆"强制弹闸。

## 3. 已拍板的默认阈值（总控 2026-07-20 确认）

| 配置项 | 默认值 |
|---|---|
| `token_hard_limit` | 200000 |
| `protected_collections` | `["customers","orders","employees"]` |
| `default_decision_policy` | `ask` |
| 标准选项 | A 继续 / B 先模拟看看 / C 取消 /（可选）D 换个做法 |

## 4. 与 A 层纪律的关系（不冲突）

- **A 层**（开发 workspace 平台的我们）：用 L2 Gate 七项 + `LOCKED_ACTIONS`(auto_modify_code / lift_human_approval_gate) + 安全边界席，保护**在建平台**。
- **B 层**（终端用户的 AI 公司）：用本原则保护**用户业务**，闸是业务风险 / 效果对比闸。
- 两层目的、主体、对象均不同；**B 层配置无权解除 A 层 `auto_modify_code` / `lift_human_approval_gate` 锁定**。
- 由此把"不采用自主执行"从 A 层纪律精确收敛为：B 层产品本就是"用户目标 → team lead 自治循环"；系统定技术、用户定高影响业务。

## 5. 自治白名单（不弹闸）

正常 operational loop（拆解 → 改文件 → 跑测试 → commit → 汇报）全自治不弹闸。仅当不满足以下全部 6 条件时才进高影响评估：sandbox 内 + 不跨外部网络 + 不删数据 + 预算内 + 不碰 L2 + 可逆。

## 6. 落地

详细设计与 4 个接线点（RealRDExecutor.run 前 / LocalRDToolset 出站前 / content_workflow_runtime 发布前 / governance 写 L2 前）见 `docs/architecture/b-layer-runtime-governance.md` §6。本原则本身**不触 L2**（仅定义边界呈现与配置）。
