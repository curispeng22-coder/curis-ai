# Google OIDC Owner Pre-Authorization

## Parent

`issues/20260722_google_oidc_project_runtime_vertical_slice.md`

## Objective

通过现有受控部署密钥设施创建一条一次性、服务端 Owner 绑定授权记录，使 Google OIDC 验证后的 `issuer + sub` 能原子完成首次 active owner membership 绑定。

## Fixed Flow

1. Owner 在部署侧执行一次精确操作，注入一次性预授权材料；不提供 Google subject、token、email 或客户端 Header。
2. 服务端从受控密钥设施读取材料，创建精确锁定 tenant/company/owner membership 的一次性绑定授权记录。
3. 浏览器只持有不透明 handle；Google OIDC 验证成功后，服务端以 `issuer + sub` 原子消费记录并建立绑定。
4. 重复、过期、已消费、主体不一致或映射缺失一律拒绝；固定提示：`Owner activation is not pre-authorized.`

## Boundaries

- 禁止首账号自动 Owner、浏览器自建预授权、email/Header/default/Admin token/token 替代。
- 不记录或回传 Google subject、token、code、Cookie、Secret。
- 不另建产品线；本 Issue 仅为同一 Google OIDC → Project Runtime 动线的 bootstrap 实施单。

## Before Implementation

系统交付与安全席必须先给出 Owner 的唯一部署侧操作：精确配置名、写入位置、是否需要生成随机值、预期成功标志和失败回传方式。未给出前不得实施。

## Route

系统交付席只读确认现有部署密钥设施与精确操作 → 安全边界席确认 → Owner 一次性部署操作 → 系统交付席最小实现 → 质量运行席浏览器验收。
