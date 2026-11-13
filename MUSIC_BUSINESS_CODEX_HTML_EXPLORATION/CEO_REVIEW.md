# Music Business — Codex HTML Exploration

Status: Review  
Authority Class: EVIDENCE  
Disposition: READY FOR CEO REVIEW; not accepted Product Truth or delivered Runtime  
Date: 2026-09-22  
Owner: Codex; next decision: CEO  
Next Gate: CEO review of product expression and findings

## 入口与使用

- [统一 HTML](index.html)；当前本地预览：http://127.0.0.1:8768/
- 无安装、无构建依赖。可直接打开 index.html；本轮浏览器验收使用上述本地 HTTP 地址，未验收所有浏览器的 file 协议保存行为。
- 服务停止后，在本目录运行 `python3 -m http.server 8768 --bind 127.0.0.1`。
- 状态保存在本浏览器独立 localStorage 键。左下角「探索说明与记录」可导出、备份并恢复初始样例。

## 三个设计决定

1. Business 用作品推进、投入判断和反馈观察表达持续经营；进入 Song 后，用明确的歌曲名、封面、范围路径和返回入口切换到单首创作。
2. Song 是可持续修改的创作桌：歌词与结构在主面，可听候选并置；比较和员工会话展开为主工作面，来源、决定和历史按需检查。试听持续存在，但不成为娱乐播放器首页。
3. 表现分析必须回到固定发布版、评论和音乐位置。经验呈现来路、适用范围、反例、采用记录和版本，而不是知识库文件夹。

## 建议实际走一遍

市场与方向 → 打开 Reference → 试听与结构定位 → 提炼为创作方向 → 林音提出方向 → 编辑并确认 → 新 Song → 制作两个候选 → 展开比较 → 试听/选择版本 → 片段反馈 → 修改工作返回新候选 → 确认成品 → 准备发行包 → 模拟提交 → 用户接续 → 效果未知 → 查询状态 → 表现与评论 → 音乐归因 → 经验候选 → 接受范围 → 用于下一首方向。

已有「夜行线」可直接测试试听与创作；「慢潮」可直接测试已发布作品的观察闭环。

## Product Findings（提议，未改合同）

| Finding | 页面中暴露的问题 | 本轮表达与下一 Gate |
|---|---|---|
| PF-01 / 方向迭代 | 在途 Song 的 Direction 修订会影响哪些 Work/Candidate，合同关系需要更明确的版本接续规则。 | 本轮创建前可编辑 Direction，创建后来源只读；没有冒充完整方向版本编辑。下一步由产品定义批准范围与失效关系。 |
| PF-02 / 多次发行 | 同一 Song 换 Master 后，旧发布版本仍可能持续产生反馈，单个“发布状态”不足以表达多平台、多次发行。 | 当前发行包固定音频与歌词快照，重新准备时保留旧包历史；UI只展开当前发行包，未做完整多发行对照。正式化前明确 Publication 身份与观察归属。 |
| PF-03 / 创作经验独立性 | 独立专业区的价值来自跨作品验证和修订，不是条目数量；只生成总结会退化成资料库。 | 保留六区合同，以经验采用链表达；已有来源、反例、接受、停用与修订。下一 Gate 用多首真实作品验证长期使用频率，尚无理由直接删区。 |
| PF-04 / 经验效果 | “被采用”不等于“验证有效”；需要记录实际改变、观察窗口、未控制变量及失败样本。 | 本轮自动保留采用关系与经验版本，结果明确“待观察”；尚未实现后续表现自动回写或效果判定。 |
| PF-05 / 音乐定位 | 器乐结构锚点不能直接充当人声、唱词与语义对齐。评论提及前段也不等于精确时间戳。 | 音频可听，时间定位可操作；歌词是独立创作文本，明确“未演唱”。中文演唱、词曲匹配与片段编辑仍需真实制作验收。 |
| PF-06 / Business 会话 | Song 内完整会话可以维持上下文；跨 Song 的经营会话还需要独立的引用和行动目标选择。 | 本轮完整会话只实现于 Song Main，其他区的讨论入口明确提示范围限制；不自动把跨业务建议当作单首制作指令。 |

## Mock / Unknown

- **Mock**：市场观察、员工研究提议/回复/执行、候选返回、Provider来源、发布步骤与回执、播放统计、评论样本、归因和经验。均有页面标识，无外部请求、登录、上传、付费或发布。
- **真实可操作**：三段32秒本地器乐音频播放、进度/定位、候选选择与反馈、歌词本地版本、创作选择、模拟状态转换、经验采用关联、刷新保存及导出。
- **Unknown**：汽水真实后台字段、发布能力、评论/收益粒度、Provider能力价格与商用许可、真实中文演唱质量、发行规格。收益、完播和曝光缺失没有用0替代。
- 方向提议和回复是固定场景规则，不是任意意图理解。三段音频重复用于候选，不是真实重生成或局部修改。表现页使用同一演示数据形状，不是新歌真实表现。
- 封面为本轮 ImageGen 原创图，1254 × 1254，共用样例；内容为夜间列车窗外城市与温暖灯光。器乐由本地标准库合成，无第三方歌曲或人声素材。

## 实际验收

浏览器：Codex In-app Browser，1440 × 1000；补查390 × 844窄屏。测试日期2026-09-22。

| 路径/边界 | 结果 |
|---|---|
| 六区导航、Business/Song范围与进入返回 | PASS |
| Reference真实音频、拆解进入自然意图和Direction | PASS |
| 创建「回家以后」、生成A/B、切换试听、交换左右比较版本 | PASS |
| A位置反馈、保留旧版返回C、Song完整员工会话 | PASS |
| 确认C为Master、单独准备发行包 | PASS |
| 提交→等待用户→平台收件→效果未知→核验上线→回执 | PASS（本地模拟） |
| 表现证据→评论→发布版定位→归因→经验候选 | PASS |
| 经验接受→「下一站的光」→来源/采用记录→刷新仍保留 | PASS |
| 经验停用、修订为v2并回到待验证 | PASS |
| 拒绝B保留记录；改歌词后旧A批准被阻止 | PASS |
| 发行歌曲选择器跨对象切换 | PASS |
| 窄屏无页面横向溢出 | PASS：contentWidth=375 / clientWidth=375；创作桌纵向堆叠 |
| Console Error / Warning | 0 / 0，详见 console-check.json；仅覆盖本轮已测路径 |
| 状态断言 | `node check.cjs` PASS：Master版本约束、歌词快照、旧发行保存、接续与Unknown恢复、经验到下一Song关系 |

测试过程中修正：发行包歌词被后续编辑污染、发行详情切歌后路由覆盖选择、观察补录对象不一致、比较表音乐描述未随版本变化、方向形式刷新丢失、跳过导航的焦点目标。波形采用真实音频振幅预计算数据，无远端依赖。

已将验收中创建的样例备份并恢复初始状态，CEO可以从清晰的两首种子作品开始。截图中的「回家以后」「下一站的光」是实际验收中创建的本地对象。

## 关键截图

| 画面 | 文件 |
|---|---|
| 经营 | [01-business.png](screenshots/01-business.png) |
| Reference拆解 | [02-reference.png](screenshots/02-reference.png) |
| Song创作桌 | [03-song-workspace.png](screenshots/03-song-workspace.png) |
| Audition比较 | [04-audition.png](screenshots/04-audition.png) |
| 员工完整会话 | [05-conversation.png](screenshots/05-conversation.png) |
| 发布效果未知 | [06-release-unknown.png](screenshots/06-release-unknown.png) |
| 表现观察 | [07-performance.png](screenshots/07-performance.png) |
| 音乐归因 | [08-attribution.png](screenshots/08-attribution.png) |
| 经验采用 | [09-learning.png](screenshots/09-learning.png) |
| 窄屏创作 | [10-narrow.png](screenshots/10-narrow.png) |

## 合同与范围记录

主要来源为 `../docs/research/music-business-product-structure-2026-09-22/` 的 PRODUCT_STRUCTURE_CANDIDATE、RELATIONSHIP_MAP、GAP_AUDIT 三份文件；沿用CEO本轮接受的Candidate方向，不升级为Frozen。

视觉来源为 `../docs/research/professional-workspace-product-language-2026-09-21/CURIS_PROFESSIONAL_WORKSPACE_VISUAL_LANGUAGE_BASELINE_CANDIDATE.md` 与 `../CURIS_COLOR_DIRECTION_EXPLORATION/06_HYBRID_NOTES.md`。未参考WorkBuddy Music设计结果。

本轮仅新增此独立探索目录。Pointer/Index未更新：不新增Current Authority，不修改现有产品合同。没有修改Runtime、Backend、数据库，也没有commit/push。

MUSIC BUSINESS CODEX HTML EXPLORATION — READY FOR CEO REVIEW
