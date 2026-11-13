# ADR-0035: Desktop First

Status: Frozen

Baseline: `main @ c0e1855f`

Updated: 2026-07-30

Module: Product Delivery

## Decision

Curis 当前采用 Desktop First 产品策略。

```text
Current:
Local Desktop Owner
→ Trusted Local Gateway
→ Single Workspace Runtime
→ Local SQLite

Future:
Web deployment
→ Mobile extension
```

## Reason

- 当前核心用户是本机 Owner/CEO
- 本地文件、受控工具和真实执行需要明确设备边界
- Desktop 能先完成完整产品闭环和安全边界
- Web/Mobile 扩展需要独立身份、部署、同步和数据治理

## Consequences

- 当前验收优先 Desktop 主流程
- 响应式 Web 页面是当前实现能力，但不等于已经完成 Web 商业部署
- Mobile 当前只要求响应式可用，不声明独立移动产品
- Web/Mobile 扩展必须通过新的产品、架构和安全 Decision
