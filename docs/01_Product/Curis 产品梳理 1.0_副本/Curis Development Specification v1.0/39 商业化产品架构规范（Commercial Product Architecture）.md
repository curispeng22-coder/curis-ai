# Curis Development Specification

# 39 商业化产品架构规范（Commercial Product Architecture）

版本：v1.0-draft

---

# 1. 系统定位

商业化产品架构定义 Curis 从：

个人AI工作台。

发展为：

面向个人、团队、企业的AI组织平台。

---

# 2. 产品演进路径

```
Curis Desktop

↓

Curis Workspace

↓

Curis Platform

↓

Curis Ecosystem
```

---

# 3. 产品形态

未来商业产品：

```
Curis Platform

├── Workspace

├── Admin

├── Capability Marketplace

├── Template Marketplace

└── Developer Platform
```

---

# 4. Workspace产品

定位：

AI公司的工作空间。

---

用户使用：

- AI员工；
- 项目；
- 任务；
- Workflow；
- 知识；
- 成果。

---

适用：

个人。

团队。

企业部门。

---

# 5. Admin产品

定位：

AI组织管理平台。

---

负责：

- 用户管理；
- 权限管理；
- 能力管理；
- 模板管理；
- 成本管理；
- 安全治理。

---

# 6. Capability Marketplace

定位：

AI能力生态。

---

提供：

- Model；
- Agent；
- Skill；
- Tool；
- Workflow；
- MCP；
- Connector。

---

用户可以：

发现。

安装。

配置。

使用。

---

# 7. Template Marketplace

定位：

业务能力生态。

---

提供：

Business Template。

---

例如：

## 软件研发模板

包含：

- 产品负责人；
- 开发员工；
- 测试员工；
- 发布流程。

---

## 内容增长模板

包含：

- 内容负责人；
- 策划员工；
- 数据分析员工。

---

# 8. Developer Platform

定位：

开放第三方开发能力。

---

开发者可以创建：

- Agent；
- Skill；
- Tool；
- Connector；
- Workflow；
- Business Template。

---

# 9. 用户体系

商业版本支持：

---

## 个人用户

场景：

个人AI助手。

---

## 专业用户

场景：

开发者。

创作者。

顾问。

---

## 团队用户

场景：

小团队协作。

---

## 企业用户

场景：

组织级AI管理。

---

# 10. 商业套餐设计方向

未来可以支持：

## Personal

个人Workspace。

---

## Team

团队Workspace。

---

## Enterprise

企业Workspace + Admin。

---

# 11. 商业价值模型

Curis价值来源：

---

## AI员工效率

减少重复工作。

---

## 能力整合

减少工具切换。

---

## 知识沉淀

形成企业资产。

---

## 自动执行

提升业务效率。

---

# 12. 企业部署模式

支持：

## SaaS模式

云端Workspace。

---

## 私有部署

企业服务器。

---

## 混合模式

云端管理。

本地执行。

---

# 13. 数据架构

商业版本：

```
Platform Data

↓

Tenant Data

↓

Workspace Data

↓

Local Data
```

---

# 14. 多租户设计

企业之间隔离：

- 用户；
- 项目；
- 知识；
- Memory；
- 能力。

---

结构：

```
Tenant A

×

Tenant B
```

---

# 15. 企业AI治理

支持：

## 能力治理

哪些模型可以使用。

---

## 成本治理

预算限制。

---

## 数据治理

资料访问规则。

---

## 安全治理

执行审批。

---

# 16. 企业知识资产

企业长期使用后：

形成：

```
企业知识

↓

部门经验

↓

员工Memory

↓

业务优化
```

---

成为企业AI资产。

---

# 17. 商业生态闭环

完整生态：

```
开发者

↓

能力/模板

↓

Marketplace

↓

企业用户

↓

业务数据

↓

优化反馈

↓

生态增长
```

---

# 18. Curis核心竞争壁垒

不是：

模型。

---

不是：

聊天入口。

---

而是：

## AI组织模型

管理AI员工。

---

## 能力调度

组合所有AI资源。

---

## 长期记忆

让AI持续成长。

---

## 业务模板

快速复制业务能力。

---

# 19. 商业化阶段目标

## 第一阶段

个人验证。

---

## 第二阶段

团队使用。

---

## 第三阶段

企业部署。

---

## 第四阶段

生态平台。

---

# 20. 当前开发影响

当前Desktop版本：

需要预留：

- Workspace边界；
- Admin边界；
- Capability边界；
- Template边界。

---

但不提前实现：

复杂商业系统。

---

# 21. 验收标准

商业架构完成后：

Curis可以：

从个人工具。

平滑升级。

成为企业AI平台。

---

检查：

## 产品

定位清晰。

---

## 技术

支持扩展。

---

## 商业

具备生态空间。

---

# 本章冻结内容

本章定义Curis商业化产品架构。

核心：

当前做个人AI工作台。

未来发展为：

连接AI能力、AI员工和业务流程的企业级AI组织平台。

---

下一章：

# 40 开发验证与MVP验收规范（MVP Validation Specification）