# Research Journal

Authority Class: EVIDENCE
Status: Review
Date: 2026-09-15 Asia/Shanghai

1. 读取本轮完整请求，承接上一轮G1–G6，先登记Required Capability。
2. 查Curis当前相关源码及历史研究，排除旧Admin-only/凭证占位结论。
3. 11个独立OSS候选，G3/G4共用三个；G6原有工具足够，不扩大搜索。
4. GitHub公开API登记维护/版本；公开raw文件记录hash。MCP初次连接重置，raw重试成功但未伪造release。APScheduler README.md路径404，改读取稳定tag的README.rst/LICENSE.txt；FFmpeg改读LICENSE.md。无安装、无外部项目运行。
5. 针对性读取BrowserContext、Router、model schema、DBOS步骤和SQLite选择、CronTrigger、DocumentConverter、TessBaseAPI。Apple页面web解析失败，使用其官方Markdown获取正文。
6. 发现DBOS README强调Postgres但源码保留SQLite；选型理由改为已有Runtime映射成本，而非不存在SQLite。LiteLLM历史Issue仅作制品验证门槛，不宣称当前发行安全/受影响。
7. 生成16节主报告、11候选×16问、6套实施验证门槛；结论B，提交CEO Review。
8. 26个上轮证据源hash复核一致；16节/候选字段/引用文件检查通过。未执行数据库或业务代码。源码静态检查不等于实现验收。

Unresolved: CEO接受；G1-V至G6-V实施验证；MCP精确release、LiteLLM采用制品验证、解析权重与FFmpeg构建许可。Current Pointer不变，V2不变。
