# Curis Development Specification

# 27 Connector与外部系统连接规范（Connector Integration Specification）

版本：v1.0-draft

---

# 1. 系统定位

Connector系统负责连接：

Curis之外的业务系统、数据源和工具。

目标：

让Curis能够进入用户真实工作环境。

---

# 2. 核心理念

Curis不是重新建设所有业务系统。

而是：

连接已有系统。

---

关系：

```
外部系统

↓

Connector

↓

Knowledge / Capability

↓

Project

↓

AI员工执行
```

---

# 3. Connector类型

支持：

## 数据型Connector

负责读取数据。

例如：

- GitHub；
- Notion；
- Obsidian；
- 网盘；
- 数据库。

---

## 工具型Connector

负责执行操作。

例如：

- Git提交；
- 文件操作；
- API调用。

---

## 业务型Connector

连接业务平台。

例如：

- 小红书；
- 抖音；
- 电商平台；
- 邮件系统。

---

## 通信型Connector

连接消息系统。

例如：

- 企业微信；
- Slack；
- Discord。

---

# 4. Connector统一模型

所有Connector统一抽象：

```
Connector

├── 名称

├── 类型

├── Provider

├── 连接方式

├── 权限

├── 数据能力

├── 操作能力

└── 状态
```

---

# 5. Connector能力声明

每个Connector需要定义：

---

## 可以读取什么

例如：

GitHub：

读取：

- Repository；
- Issue；
- Commit。

---

## 可以执行什么

例如：

GitHub：

执行：

- 创建Issue；
- 提交代码。

---

## 需要什么权限

例如：

读取仓库。

写入仓库。

---

# 6. 本地Connector

通过：

Local Bridge。

---

连接：

## 文件系统

例如：

项目目录。

资料目录。

---

## 本地AI应用

例如：

- Codex；
- Claude Code；
- Trae；
- WorkBuddy。

---

## 本地工具

例如：

- Git；
- Terminal；
- IDE。

---

# 7. Obsidian Connector

重点支持。

---

连接：

用户知识库。

---

能力：

读取：

Markdown。

标签。

链接。

目录结构。

---

输出：

Knowledge。

---

流程：

```
Obsidian Vault

↓

Connector

↓

Knowledge Index

↓

AI员工调用
```

---

# 8. GitHub Connector

研发项目核心连接。

---

支持：

读取：

- 代码；
- Commit；
- Issue；
- PR。

---

执行：

- 创建Branch；
- 提交代码；
- 创建PR。

---

绑定：

研发项目。

---

# 9. 内容平台Connector

用于：

内容增长项目。

---

例如：

小红书。

抖音。

头条。

---

支持：

## 自动连接（平台允许时）

读取：

- 数据；
- 内容状态；
- 评论。

---

## 半自动模式

平台限制时：

用户输入数据。

---

例如：

小红书：

手动填写：

- 浏览量；
- 收藏；
- 评论；
- 粉丝变化。

---

进入：

经营分析。

---

# 10. Connector权限模型

每个连接需要：

授权。

---

包括：

## 数据权限

读取哪些数据。

---

## 操作权限

允许执行什么。

---

## 项目权限

绑定哪些项目。

---

例如：

GitHub：

允许：

研发项目。

---

不允许：

私人仓库。

---

# 11. Connector状态管理

状态：

```
未连接

↓

授权中

↓

已连接

↓

同步中

↓

异常

↓

暂停
```

---

展示：

连接时间。

权限。

错误原因。

---

# 12. Connector与Knowledge

数据型Connector：

进入知识系统。

---

例如：

GitHub。

↓

代码知识。

↓

研发员工Memory。

---

Notion。

↓

产品知识。

↓

项目Context。

---

# 13. Connector与Capability

Connector本身也是能力。

---

例如：

GitHub Connector：

属于：

Tool Capability。

---

可以被：

Workflow。

Agent。

调用。

---

# 14. Connector与Workflow

Workflow可以调用Connector。

---

例如：

内容复盘：

```
定时触发

↓

读取平台数据

↓

分析

↓

生成报告
```

---

# 15. Connector与智能调度

调度中心选择：

需要什么Connector。

---

例如：

用户：

“分析代码问题。”

系统：

选择：

GitHub Connector。

---

用户：

“分析账号增长。”

系统：

选择：

内容平台Connector。

---

# 16. Connector市场（未来）

未来支持：

第三方Connector。

---

例如：

开发者创建：

电商Connector。

CRM Connector。

---

进入：

Capability Marketplace。

---

# 17. Connector安全

重点：

外部系统权限。

---

要求：

- 明确授权；
- 最小权限；
- 可撤销；
- 可审计。

---

# 18. Connector操作记录

记录：

```
Connector

↓

调用者

↓

项目

↓

操作

↓

结果
```

---

例如：

```
研发Agent

调用GitHub

提交代码

成功
```

---

# 19. API设计

## 获取Connector

```
GET /connectors
```

---

## 添加Connector

```
POST /connectors
```

---

## 授权Connector

```
POST /connectors/{id}/authorize
```

---

## 测试连接

```
POST /connectors/{id}/test
```

---

## 执行操作

```
POST /connectors/{id}/execute
```

---

# 20. 验收标准

Connector系统完成后：

用户可以：

连接已有工具。

连接知识来源。

连接业务平台。

让AI员工进入真实工作环境。

---

检查：

## 开放性

支持未来扩展。

---

## 安全性

权限可控。

---

## 可用性

用户无需重复搬运数据。

---

# 本章冻结内容

本章定义Connector系统。

核心：

Curis不是替代用户已有工具。

而是成为连接和调度这些工具的AI工作操作系统。

---

下一章：

# 28 Curis本地运行架构规范（Desktop Runtime Architecture）