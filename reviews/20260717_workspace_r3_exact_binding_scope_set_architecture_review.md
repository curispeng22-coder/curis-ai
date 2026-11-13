# R3 固定 Role → Binding 集合兼容契约 Review

Issue：`issues/20260717_workspace_r3_exact_binding_scope_set_l2_gate.md`  
结论：`PASS`（仅配置/边界契约；不授权实施、不出网）。

## 唯一配置

服务端只接受固定、显式、无通配符的 role→binding 映射：

```json
{
  "tech_lead": "bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d",
  "product_manager": "bind-6d5b31e1-1b69-49a6-bd80-d2be741d6530",
  "architect": "bind-b476f200-6bfc-4d8e-b1d7-c2c6e4e5f938",
  "frontend_engineer": "bind-7275893a-7588-4f71-b780-ab55bef7db1d",
  "backend_engineer": "bind-e2cbbcb3-b940-4bbd-bd09-1225b86a0eb3",
  "qa_engineer": "bind-c04accdf-4567-4715-b9a3-46adf0eea40f"
}
```

该集合是服务端批准配置，不从客户端、请求 payload 或运行时“发现全部 binding”生成。当前 Step 的 role 是唯一选择键：先查映射得到一个 binding，再执行既有 tenant/company/department/project/employee/capability/workflow 全量校验，最后才允许执行。

## Fail-closed

以下任一情况立即拒绝且不得出网：配置缺失、空集合、未知 role、重复 role、重复 binding、binding ID 拼写/格式错误、role 与 binding 实际 employee role 不一致、集合外 binding、客户端覆盖 role/binding、binding inactive/撤销、scope 任一不匹配、同一 role 出现多个候选。不得通配符、随机选择、默认 binding 或 Tech Lead 冒充其他角色。

每条 binding 必须匹配当前固定 Run 的 tenant、company、研发 Department、project、workflow、employee、approved model capability 和对应 Step role。累计预算允许六个集合成员在不同 Step 合法使用；这不放宽单 Workflow 的 Step 顺序、一次/Step 调用、总调用次数、Token、成本、0 重试和无 Fallback 规则。

## 历史单值兼容

旧单值配置 `CURIS_R3_APPROVED_CAPABILITY_BINDING_ID` 仅兼容解释为 `tech_lead` 的历史首步 binding，且只有值等于 `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` 时通过。它不能授权 Step 2–6，不能与新集合同时产生覆盖优先级；新集合存在但不完整时拒绝，不回退旧单值。

首步历史 UsageEvent 继续以 Tech Lead binding 校验；后续 Step 必须按当前 role 取集合对应 binding。集合外、角色错配或同角色多 binding 均拒绝。

回滚只能恢复上一版同样 fail-closed 的单值兼容配置：允许历史 Tech Lead 首步，拒绝其余角色，不得恢复客户端选择、默认值、自动发现或跨角色复用。若回滚后无法证明首步 binding 与历史审计一致，则保持阻塞。

## 最少实施文件

后续实现只需：

- `backend/app/main.py`：把 R3 approved binding 校验从单值改为固定服务端映射，并按当前 Step role 选择；
- `backend/app` 中现有 R3 scope 校验入口：复用既有全量资源/能力校验，不新增授权入口；
- `deploy/curis/workspace.env.example` 或现有非秘密配置模板：仅声明集合配置形状，不写凭据；
- 直接相关 focused tests；不改 Workflow、Provider、Model、Gateway、成本规则、数据库或部署网络。

## Focused 验收

不出网覆盖：六个 role 各自解析唯一正确 binding；历史 Tech Lead UsageEvent 通过；集合外 binding、role 错配、重复/未知/缺失/空集合、错误 ID、客户端覆盖、scope 不一致均在 Adapter 前拒绝；Tech Lead 不被其他 Step 复用；累计预算只接受集合内合法 Step；旧单值仅能通过首步；日志不泄露凭据或完整 subject。

Handoff: sent to 安全边界席复核，并回传产品规划席；实现与真实执行仍等待安全 PASS 和总负责人批准。
