# 前端团队强制对齐指令 v2 · Curis v1 Desktop（按 canonical-nav 100% 重建 + 清测试 fixture）

> **主理人 · 齐构成 · 2026-08-06 · 强制执行 · 不容含糊**
>
> **这是 v2 版本**，上一版指令（`Frontend_Team_Structure_Align_Handoff_2026-08-05.md`）你们**未遵守**——CEO 已发严辞批评，截图证据表明你们做的是自创 IA（CEO 协调型）而非 Frozen 原型（公司/经营工具/办公室/公司资源 + 底部）。**这次必须 100% 对齐 canonical-nav.js**，任何自定义 IA 视为违反。

| 项 | 内容 |
| --- | --- |
| **From** | 主理人（齐构成） |
| **To** | 软件前端团队 `software-frontend-align`（team-lead 接收 + 分派 engineer × 2 + QA） |
| **Date** | 2026-08-06 |
| **Gate** | G-强制对齐（用户视角验收，不信自报） |
| **上一版失败** | 2026-08-05 `Frontend_Team_Structure_Align_Handoff_2026-08-05.md`——已完成 12 个提交（基线文档 0 违规、25 路由 200）但**实际导航与 Frozen 原型 0 匹配** |

---

## 一、用户批评（原文，不许辩解）

> 「这个应用做的就是一坨大便，我说了好几遍，前端对齐最新的 ui，最新的 ui 里边哪里有什么战略会议室，什么 ai 团队，这个导航跟对齐的 ui 完全不一样，还有确认的研发、小红书、抖音工作空间呢？我要的是一个干干净净的部署的本地桌面应用，把那些测试数据都接在里边是什么意思？」

**用户视角截图证据**（已附）：
- 侧栏出现「总裁办公室/重要汇报/战略会议室/运行轨迹/项目中心/组织中心/能力中心/经营工具/头脑风暴室/执行工作台」——**这些是你们自创的，原型没有**
- 工作空间展开是「当前栏目」——**原型是研发办公室/小红书运营办公室/抖音 TikTok 运营办公室/部门办公室 4 个**
- 主区出现「d2/debug部门/测试部/研发部/质量验证研发部」+「小张/小账/小影/e2/验证-architect/验证-backend_engineer」——**这些是测试 fixture，不是 v1 部署内容**

---

## 二、Frozen 原型权威 IA（唯一真源，逐字对齐）

文件：`curis-ui-prototype/_system/canonical-nav.js` 的 `NAV_MODEL`（已拷贝关键片段于此，禁止自由发挥）：

```javascript
NAV_MODEL = {
  primary: [    // 标题「公司」
    ['CEO 工作台',   'ceo-desk.html',                     '◆'],
    ['经营',         'operating.html',                    '◎'],
    ['业务',         'business.html',                     '◇'],
    ['AI 团队',      'ai-organization.html',              '□'],
    ['工作空间',     'workspace-portal.html',             '▣']
  ],
  tools: [      // 标题「经营工具」
    ['会议工作台',   'meeting.html',                      '◌'],
    ['决策室',       'decision-room.html',                '◇']
  ],
  offices: [    // 「办公室」二级菜单（动态挂在「工作空间」下）
    ['研发办公室',           'workspace-runtime-software.html',    '◉'],
    ['小红书运营办公室',    'workspace-runtime-xhs.html',         '◌'],
    ['抖音 / TikTok 运营办公室', 'workspace-runtime-shortvideo.html','◌'],
    ['部门办公室',           'workspace-runtime-department.html',  '◉']
  ],
  resources: [  // 标题「公司资源」
    ['成果库',     'assets.html',     '▤'],
    ['知识库',     'knowledge.html',  '⌘'],
    ['财务',       'finance.html',    '¥'],
    ['日历',       'calendar.html',   '◷']
  ],
  footer: [      // 底部固定
    ['设置',       '#',  '○'],
    ['帮助与反馈', '#',  '?']
  ]
}
```

---

## 三、强制任务（逐项必做，不许讨价还价）

### 任务 A · 导航 IA 重建（software-engineer）

**完全重写 `frontend/components/terra/TerraNavData.js`**，必须满足：

| 分组（label） | item label | route | 备注 |
|---|---|---|---|
| **公司** | CEO 工作台 | `/ceo-office` | 一级 |
| 公司 | 经营 | `/ceo-office/analytics` | 一级 |
| 公司 | 业务 | `/ceo-office/projects` | 一级 |
| 公司 | AI 团队 | `/ceo-office/organization` | 一级 |
| 公司 | 工作空间 | `/ceo-office/company-runtime` | **展开二级（offices 数组 4 项）** |
| 公司 > 工作空间 > | 研发办公室 | `/ceo-office/workspace/software` | **新建占位页** |
| 公司 > 工作空间 > | 小红书运营办公室 | `/ceo-office/workspace/xhs` | **新建占位页** |
| 公司 > 工作空间 > | 抖音 / TikTok 运营办公室 | `/ceo-office/workspace/shortvideo` | **新建占位页** |
| 公司 > 工作空间 > | 部门办公室 | `/ceo-office/workspace/department/[id]` | **新建占位页** |
| **经营工具** | 会议工作台 | `/ceo-office/meeting` | 一级 |
| 经营工具 | 决策室 | `/ceo-office/decisions` | 一级 |
| **公司资源** | 成果库 | `/ceo-office/company-runtime` | 一级 |
| 公司资源 | 知识库 | `/ceo-office/knowledge` | 一级 |
| 公司资源 | 财务 | `/ceo-office/finance` | 占位（v1 暂不建设，标「规划中 · Blueprint §16」） |
| 公司资源 | 日历 | `/ceo-office/calendar` | 占位 |
| **底部固定** | 设置 | `/ceo-office/settings` | 一级 |
| 底部固定 | 帮助与反馈 | `/ceo-office/help` | 一级 |

**禁止出现**（v1 必须删除）：
- ❌ 「总裁办公室 / 重要汇报 / 战略会议室 / 运行轨迹」——CEO 工作台就是 CEO 工作台
- ❌ 「项目中心 / 组织中心 / 能力中心」——AI 团队 = 原型的组织语义；业务 = 原型业务；不存在「项目中心/组织中心/能力中心」这种二级划分
- ❌ 「头脑风暴室 / 执行工作台」——v1 不在原型里（如要建走独立 issue，不在本任务）
- ❌ 「工作空间→当前栏目」——工作空间展开必须 = 原型 offices 数组 4 项

### 任务 B · 测试 fixture 清除（software-engineer + 后端协作）

**问题源**（后端 seed 写死的脏数据）：
```
backend/seed_wave1.py
backend/app/agent_conversion/seed_pilot_b.py
backend/app/agent_conversion/seed_multisource.py
backend/app/agent_conversion/seed.py
```

**当前 SQLite 里被塞的脏数据**（实测）：
- 部门：`待归属业务部 / d2 / debug部门 / 测试部 / 研发部 / 质量验证研发部`
- 员工：`小张 / 小账 / 小影 / e2 / 验证-architect / 验证-backend_engineer / devops_engineer / tech_lead`

**强制动作**：
1. **修改 `seed_wave1.py`**：v1 selfuse 模式（`CURIS_ENV=local`）下，**默认只创建 1 个空 company**（无部门、无员工、无项目）。其他 seed 文件改为只在非 selfuse 模式（带 admin token）才执行。
2. **前端空数据态走原型 §6 数据态纪律**：
   - 无部门 → 显示「尚未配置业务部门 · 提示：从业务中心创建」
   - 无员工 → 显示「未记录」
   - 无项目 → 显示「未读取事实」
   - 不得用 `$0` 冒充未知成本
   - 不得用 `d2` 这种占位名显示
3. **前端不再引入任何 fixture**（之前 grep `frontend/app/` 无 mock 引用，保持现状）

### 任务 C · 路由映射（software-engineer）

需要新建的占位页（与 §任务 A 对齐）：
- `/ceo-office/workspace/software` — 研发办公室占位
- `/ceo-office/workspace/xhs` — 小红书运营办公室占位
- `/ceo-office/workspace/shortvideo` — 抖音 TikTok 运营办公室占位
- `/ceo-office/workspace/department/[id]` — 部门办公室占位

每个占位页结构（参考 `/ceo-office/meeting` 占位）：TerraShell + TerraPageHead + TerraEmpty + 「办公室 · 规划中 · v1 暂不建设（Blueprint §16 明确暂不建设 · 业务启动后可激活）」文案。

### 任务 D · QA 独立验收（software-qa-engineer）—— 用户视角，不信自报

**不要再采信 engineer 自报结论**——上次就是这么失败的。这次必须：

1. **侧栏像素级对比**（puppeteer-core + 系统 Chrome，1440×900）：
   - 启动真实 .app（不要 next dev 绕过 sidecar），截 CEO 工作台侧栏展开态
   - 与 `curis-ui-prototype/ceo-desk.html` 原型侧栏并排
   - **任何 IA 不一致都视为不通过**（包括命名、分组、顺序、二级菜单）
2. **工作空间二级菜单验证**：截图保存 + 必须出现 `研发办公室 / 小红书运营办公室 / 抖音 TikTok 运营办公室 / 部门办公室` 4 个
3. **fixture 检测**：连后端 `curl /api/workspace/departments`，确认返回 `[]` 或仅 1 个默认空 company；不允许返回 `d2 / debug部门 / 测试部 / 研发部 / 质量验证研发部` 等任何 fixture 命名
4. **空数据态文案**：用空数据时 Organization 页面必须显示「未记录/尚未配置」原型 §6 文案

---

## 四、完成标准（用户视角验收清单）

| # | 项 | 验证方法 |
|---|---|---|
| 1 | TerraNavData 5 分组（公司/经营工具/公司资源/底部/工作空间二级） | cat 文件，肉眼对照 §二表格 |
| 2 | 工作空间展开 = 原型 offices 4 项 | 启动 .app，puppeteer 截图侧栏 |
| 3 | 没有任何自创 IA 残留（重要汇报/项目中心/能力中心/头脑风暴室等） | grep 关键词，全为 0 |
| 4 | 后端 seed 默认空数据 | curl departments 返回 `[]` 或 1 项默认 |
| 5 | 没有 d2/debug/测试部/研发部 等 fixture | grep 数据库 + 前端 |
| 6 | 空数据态显示「未记录」 | 浏览器实测空 company |
| 7 | 5 个新占位页路由 200 | curl 全部占位页 |
| 8 | 应用启动后侧栏与原型 ceo-desk.html 像素级匹配 | puppeteer 截图并排 |

---

## 五、纪律（这次是真的）

1. **不许在原型外加任何自定义项**——canonical-nav.js NAV_MODEL 是唯一真源
2. **不许借口「兼容现有路由」**——已有的 `项目中心/组织中心/能力中心/头脑风暴室/执行工作台` 等 v2 旧路由**该删就删、该合并就合并**（合并到原型对应项）
3. **不许信 engineer 自报**——QA 必须独立 puppeteer 截图与原型并排
4. **不许塞测试 fixture**——seed_wave1.py 默认空数据
5. **不许改后端业务路由契约**——仅改 seed 默认值
6. **一个 issue 一提交**（参考记忆 #6 Git 纪律）

---

## 六、汇报格式（回主理人）

完成时提交：
1. TerraNavData.js 完整 diff（含 5 分组模型 + offices 二级）
2. seed_wave1.py diff（selfuse 默认空数据）
3. 4 个新占位页的文件清单
4. **puppeteer 截图 5 张**（CEO 办公室侧栏 + 工作空间展开 4 项 + 空数据态）
5. **与原型 ceo-desk.html 的并排对比报告**（标注每个分组/每项是否一致）
6. commit hash

**ETA：1 个 PR / 1 个 commit。完成后由 CEO 用户亲自截屏验收。**

---

*主理人 · 齐构成 · 2026-08-06 · 强制版 v2*