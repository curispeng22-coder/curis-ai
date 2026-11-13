# CEO Review 截图索引 — Writing Business HTML Exploration

全部截图来自**真实 Chrome 无头浏览器点击操作**（viewport 1512×982），由 `node _selftest.js` 自动生成，非手工拼图。
对应自测报告：`_evidence/SELFTEST_REPORT.md`（**140 项断言全部通过，Console Error 0**）。
本次运行共 **55 张**；修订前的 32 张旧截图已移入 `../_backup_pre_revision_2026-09-21/evidence/`（保留可查，未删除）。
逐条能力→入口映射与修订前后状态见 `../REVISION_NOTE.md`。

---

## A. 六区主要状态

| 截图 | 区 / 合同项 | 评审看点 |
|---|---|---|
| `23-p5-operate-home.png` | 经营 · 业务首页 | 作品组合、真实待决、无人负责的职责缺口如何显示 |
| `24-p5-operate-plan.png` | 经营 · 经营计划与决定 | 批准 / 保持 / 暂缓三选项与依据并列 |
| `01-p1-market-observations.png` | 市场与方向 · 市场观察 | 是「可判断的观察」而不是热度结论 |
| `02-p1-market-references.png` | 市场与方向 · 参考与拆解 | 外部参考与自有作品分开 |
| `03-p1-market-direction.png` | 市场与方向 · 创作方向 | 已接受方向同时展示风险 / 未确认 / 落到何处 |
| `05-p1-book-library.png` | 作品 · 作品库 | 本地作品与「接入已有平台作品」区分 |
| `06-p2-book-overview.png` | 作品 · 作品概览 | 库存按可发布 / 已排期 / 草稿三类 |
| `10-p2-story-state.png` | 作品 · 故事状态 | 伏笔 / 设定可追溯，区分已兑现与计划中 |
| `11-p2-canon-conflict.png` | 作品 · 正文与候选 | Canon 冲突被显式标出并给出处理入口 |
| `12-p3-publish-queue.png` | 连载发布 · 发布队列 | 未知 / 已上线 / 退回 / 已排期分色；未知不显示为失败 |
| `13-p3-receipts.png` | 连载发布 · 提交与回执 | 提交版本 ≠ 线上版本，回执证据可核验 |
| `14-p3-accounts.png` | 连载发布 · 账号与映射 | 跨平台映射阻塞被显式暴露 |
| `15-p4-performance.png` | 读者与收益 · 表现总览 | 口径 / 覆盖 / 来源声明；**章节收益显式标注「无此字段」** |
| `16-p4-entry.png` | 读者与收益 · 数据补录 | 导入冲突与手工订正待处理 |
| `17-p4-comments.png` | 读者与收益 · 评论洞察 | 主题簇 + 样本量 + 可回跳正文锚点 |
| `21-p4-learning-library.png` | 写作经验 · 经验库 | 范围 / 反例 / 应用次数与验证次数分离 |
| `22-p4-learning-detail.png` | 写作经验 · 经验详情 | 「用过」≠「验证过」；反例随行 |

## B. Candidate 部分采纳 → 正式版本（核心路径）

| 截图 | 看什么 |
|---|---|
| `07-p2-manuscript-candidate.png` | 正文为视觉中心；右侧候选栏逐条列「采纳 / 拒绝」；正文可点段选区；章节栏可切换 |
| `08-p2-candidate-adopted-one.png` | **部分采纳**：只采纳其中一条，正式稿版本不动；「已采纳」与「已生效」分离 |
| `09-p2-manuscript-applied.png` | **生成正式 v3**；线上仍是 v2（正式 ≠ 已发布） |
| `04-p1-direction-accepted-new-book.png` | 接受未定方向 → **派生新的 Book 身份**，并说明已更新到何处 |

## C. 发布等待 / 回执 → 未知消解

| 截图 | 看什么 |
|---|---|
| `12-p3-publish-queue.png` | 第 40 章为「外部状态未知」；不重发 |
| `13-p3-receipts.png` | 核验清单路径：未知可被核验，核验后 `unknown → live` 并回写章节发布事实 |

## D. 内容归因 → Learning 回流

| 截图 | 看什么 |
|---|---|
| `18-p4-attribution.png` | **五层归因完整**：观察 / 证据 / 假设（含替代解释与反证）/ 经验候选 / 建议；含证据缺口与表述边界 |
| `19-p4-evidence-drawer.png` | 「完整证据」抽屉：不离开当前上下文，返回保留原筛选与版本 |
| `20-p4-attribution-to-learning.png` | 沉淀为经验前**强制声明适用范围与尚未排除项**，反例与来源随行 |
| `21-p4-learning-library.png` / `22-p4-learning-detail.png` | 经验回到创作：可用于下一章、可回访、可停用 |

## E. 日常维护与恢复

| 截图 | 看什么 |
|---|---|
| `25-p5-decision-applied.png` | 决定已裁决并显示「已接受 ≠ 已应用」 |
| `26-p5-watches-recover.png` | 关注点失败 / 暂停后如何恢复 |
| `27-p5-disconnect-guard.png` | 断连前弹影响确认；断开不删历史 |
| `28-p5-book-switch.png` | 切换作品改变「当前作品」范围 |
| `29-p5-new-book-empty.png` | **新作品不串稿**：正文工作面不显示其他作品的章节 |
| `30-p5-first-chapter.png` | 空书可开写第一章；新章为草稿，不计入可发布库存 |
| `31-f-reset-restored.png` | 重置演示数据后回到初始样例（改动只写入本机 localStorage） |
| `55-single-file-build.png` | 单文件构建物真机校验通过（零外部引用、Console Error 0） |

## F. 创作内核定向修订 — 7 条新增验收路径（超出第 43 章样例）

### F-1 新书路径（含「空态必须真实」反证）

| 截图 | 看什么 |
|---|---|
| `32-i1-book-library.png` | 作品库有「新建作品」真实入口 |
| `33-i1-new-book-overview.png` | 新书创作内核为**真空**：背景 / 人物 / 大纲 / 场景 = 0 |
| `34-i1-story-empty-real.png` | **复现缺陷反证**：新空书故事状态显示真实空，**不出现**他作人物（林砚 / 顾晚 / 夜行灯） |
| `35-i1-positioning-form.png` | 定位把**「读者分区」与「题材」作为两个维度**同时呈现，且可编辑 |
| `36-i1-craft-world-characters.png` | 背景条目 + 人物（认知域：角色 / 作者 / 读者 / 未揭露四分） |
| `37-i1-manuscript-handwritten.png` | 手写正文两段保存为**草稿**（≠ 正式稿 ≠ 已发布） |
| `38-i1-scene-to-candidate.png` | 按场景计划生成候选，**绑定本书本章**（`C-1G` / `ch-B-03-1`） |
| `39-i1-candidate-applied.png` | 逐项采纳 → 确认闸 → 生成正式版本，**线上版本不变** |

### F-2 先写后规划 / 旧稿导入

| 截图 | 看什么 |
|---|---|
| `40-i2-extract-outline-candidate.png` | 「从正文提取章纲」产出**待确认候选**，不自动成为章纲 |
| `41-i2-write-then-plan.png` | 写后可补大纲（计划 ≠ 事实，不覆盖已写正文） |
| `42-i3-import-classify.png` | 导入解析出分类行（含理由与置信度），**分类可逐行修改** |
| `43-i3-import-confirmed.png` | 确认写入**只产草稿**，既有正式稿数量不变，导入记录登记 |
| `44-i3-import-extract-candidates.png` | 从已导入正文抽取设定候选（AI 推断，待确认，不自动进 Canon） |

### F-3 知识变更影响 / 双书隔离 / 持久化 / 回流

| 截图 | 看什么 |
|---|---|
| `45-i4-knowledge-change-impact.png` | 改背景规则 → 影响清单写**可枚举受影响范围** + 「已发布正文不改」 |
| `46-i4-ending-confirmed.png` | 结局方向可确认，其余保留候选；写入**本书**影响清单 |
| `47-i5-two-books-scope.png` | 双书 + 新空书切换：scope 正确、不串作、**卷不重复全书章节** |
| `48-i6-migration-preserved.png` | `w1 → w2` 迁移**保留用户既有编辑**（不以清空 localStorage 换测试通过） |
| `49`–`54-i7-*.png` | 回流链闭合：市场方向 → 正文 → 发布队列 → 归因 → 经验 → **回到下一章场景准备** |

---

## 评审建议动线（约 8 分钟）

1. `README.md` §1 → 双击 `index.html` 或 `index.single.html` 打开。
2. 左侧「作品 → 作品库」：**新建作品** → 进「故事状态」确认是真实空（无他作人物）→ 「创作内核」填定位 → 新增背景 / 人物 / 大纲 / 场景。
3. 「作品 → 正文写作」：手写两段并保存 → 「按场景计划生成候选」→ 采纳 → 确认生成正式版本（线上不变）。
4. 「作品 → 审校与质量」：分别点 **审稿 / 校对 / 表达质量**「发起检查」，观察三类问题各自带位置与证据 → 「按建议修改」/「忽略并留理由」/「复查」。
5. 「作品 → 旧稿接续」：载入示例文本 → 改一行分类 → 确认写入（只产草稿）→ 抽取设定候选。
6. 「作品 → 创作内核 → 背景」：改一条规则 → 点「影响清单」看受影响范围与「未改动部分」。
7. 「作品 → 正文与候选」：点第 43 章 → 采纳 / 拒绝 → 确认生成正式版本（正式 ≠ 已发布）。
