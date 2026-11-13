const fs = require('fs');
const path = require('path');

const PAGES_DIR = path.join(__dirname, 'pages');

let skipCount = 0;

function processFile(filename, replacements) {
  const filePath = path.join(PAGES_DIR, filename);
  let html = fs.readFileSync(filePath, 'utf8');
  let applied = 0;
  for (const [search, replace] of replacements) {
    if (!html.includes(search)) {
      console.log(`    [SKIP] "${search.substring(0, 80)}"`);
      skipCount++;
      continue;
    }
    html = html.split(search).join(replace);
    applied++;
  }
  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`  OK: ${filename} (${applied} replacements applied)`);
}

console.log('=== Placeholder Replacement v3 ===\n');

// ============================================================
// 1. project-center.html
// ============================================================
processFile('project-center.html', [
  ['上次同步：--', '上次同步：2 分钟前'],
  ['<div class="fact-label">项目总数</div>\n            <div class="fact-num">--</div>',
   '<div class="fact-label">项目总数</div>\n            <div class="fact-num">12</div>'],
  ['<div class="fact-num" style="color:var(--state-success)">--</div>',
   '<div class="fact-num" style="color:var(--state-success)">7</div>'],
  ['<div class="fact-num" style="color:var(--state-warning)">--</div>',
   '<div class="fact-num" style="color:var(--state-warning)">2</div>'],
  ['<div class="fact-num" style="color:var(--state-info)">--</div>',
   '<div class="fact-num" style="color:var(--state-info)">3</div>'],
  // Timeline 1: 规划阶段 - 客户管理系统 v2.0
  ['<div class="timeline-stage">规划阶段</div>\n                <div class="timeline-project">--</div>\n                <div class="timeline-meta">-- · --</div>\n                <div class="timeline-right">\n                  <div class="timeline-stage-tag planning">规划</div>\n                  <div class="timeline-progress">\n                    <div class="timeline-progress-bar" style="width:--%"></div>\n                  </div>\n                  <span class="timeline-pct">--%</span>',
   '<div class="timeline-stage">规划阶段</div>\n                <div class="timeline-project">客户管理系统 v2.0</div>\n                <div class="timeline-meta">研发部 · 张伟(PM)</div>\n                <div class="timeline-right">\n                  <div class="timeline-stage-tag planning">规划</div>\n                  <div class="timeline-progress">\n                    <div class="timeline-progress-bar" style="width:30%"></div>\n                  </div>\n                  <span class="timeline-pct">30%</span>'],
  // Timeline 2: 执行阶段 - 移动端性能优化
  ['<div class="timeline-stage">执行阶段</div>\n                <div class="timeline-project">--</div>\n                <div class="timeline-meta">-- · --</div>\n                <div class="timeline-right">\n                  <div class="timeline-stage-tag running">执行</div>\n                  <div class="timeline-progress">\n                    <div class="timeline-progress-bar running" style="width:--%"></div>\n                  </div>\n                  <span class="timeline-pct">--%</span>',
   '<div class="timeline-stage">执行阶段</div>\n                <div class="timeline-project">移动端性能优化</div>\n                <div class="timeline-meta">研发部 · 李明(PM)</div>\n                <div class="timeline-right">\n                  <div class="timeline-stage-tag running">执行</div>\n                  <div class="timeline-progress">\n                    <div class="timeline-progress-bar running" style="width:65%"></div>\n                  </div>\n                  <span class="timeline-pct">65%</span>'],
  // Timeline 3: 执行阶段 - AI 智能客服部署
  ['<div class="timeline-stage">执行阶段</div>\n                <div class="timeline-project">--</div>\n                <div class="timeline-meta">-- · --</div>',
   '<div class="timeline-stage">执行阶段</div>\n                <div class="timeline-project">AI 智能客服部署</div>\n                <div class="timeline-meta">产品部 · 王芳(PM)</div>'],
  ['<div class="timeline-progress-bar running" style="width:--%"></div>',
   '<div class="timeline-progress-bar running" style="width:48%"></div>'],
  ['<span class="timeline-pct">--%</span>',
   '<span class="timeline-pct">48%</span>'],
  // Timeline 4: 受阻 - 供应链数据迁移
  ['<div class="timeline-stage">受阻</div>\n                <div class="timeline-project">--</div>\n                <div class="timeline-meta">-- · --</div>\n                <div class="timeline-right">\n                  <div class="timeline-stage-tag blocked">受阻</div>\n                  <div class="timeline-progress">\n                    <div class="timeline-progress-bar blocked" style="width:--%"></div>\n                  </div>\n                  <span class="timeline-pct">--%</span>',
   '<div class="timeline-stage">受阻</div>\n                <div class="timeline-project">供应链数据迁移</div>\n                <div class="timeline-meta">运营部 · 陈强(PM)</div>\n                <div class="timeline-right">\n                  <div class="timeline-stage-tag blocked">受阻</div>\n                  <div class="timeline-progress">\n                    <div class="timeline-progress-bar blocked" style="width:35%"></div>\n                  </div>\n                  <span class="timeline-pct">35%</span>'],
  // Timeline 5: 已完成 - 官网品牌升级
  ['<div class="timeline-stage">已完成</div>\n                <div class="timeline-project">--</div>\n                <div class="timeline-meta">-- · --</div>',
   '<div class="timeline-stage">已完成</div>\n                <div class="timeline-project">官网品牌升级</div>\n                <div class="timeline-meta">市场部 · 刘洋(PM)</div>'],
  // Dept project section
  ['共 -- 个部门', '共 3 个部门'],
  // 研发部
  ['<div class="dept-project-name">研发部</div>\n              <div class="dept-project-count">-- 个项目</div>',
   '<div class="dept-project-name">研发部</div>\n              <div class="dept-project-count">5 个项目</div>'],
  ['<div class="dept-project-status green"></div>\n                <div class="dept-project-info">\n                  <div class="dept-project-title">--</div>\n                  <div class="dept-project-tag green">执行中</div>',
   '<div class="dept-project-status green"></div>\n                <div class="dept-project-info">\n                  <div class="dept-project-title">客户管理系统 v2.0</div>\n                  <div class="dept-project-tag green">执行中</div>'],
  ['<div class="dept-project-status amber"></div>\n                <div class="dept-project-info">\n                  <div class="dept-project-title">--</div>\n                  <div class="dept-project-tag amber">受阻</div>',
   '<div class="dept-project-status amber"></div>\n                <div class="dept-project-info">\n                  <div class="dept-project-title">供应链数据迁移</div>\n                  <div class="dept-project-tag amber">受阻</div>'],
  // 商务部 -> 产品部
  ['<div class="dept-project-name">商务部</div>\n              <div class="dept-project-count">-- 个项目</div>',
   '<div class="dept-project-name">产品部</div>\n              <div class="dept-project-count">4 个项目</div>'],
  ['<div class="dept-project-title">--</div>\n                  <div class="dept-project-tag green">执行中</div>',
   '<div class="dept-project-title">AI 智能客服部署</div>\n                  <div class="dept-project-tag green">执行中</div>'],
  ['<div class="dept-project-title">--</div>\n                  <div class="dept-project-tag done">已完成</div>',
   '<div class="dept-project-title">移动端性能优化</div>\n                  <div class="dept-project-tag done">已完成</div>'],
  // 运营部
  ['<div class="dept-project-name">运营部</div>\n              <div class="dept-project-count">-- 个项目</div>',
   '<div class="dept-project-name">运营部</div>\n              <div class="dept-project-count">3 个项目</div>'],
  // 战略部
  ['<div class="dept-project-name">战略部</div>\n              <div class="dept-project-count">-- 个项目</div>',
   '<div class="dept-project-name">战略部</div>\n              <div class="dept-project-count">0 个项目</div>'],
  ['<div class="dept-project-title">--</div>\n                  <div class="dept-project-tag planning">规划中</div>',
   '<div class="dept-project-title">新零售业务探索</div>\n                  <div class="dept-project-tag planning">规划中</div>'],
  // Remaining -- title (运营部's green one)
  ['<div class="dept-project-title">--</div>',
   '<div class="dept-project-title">供应链数据迁移</div>'],
  // Portfolio
  ['<span class="portfolio-stage-name">规划</span>\n                <span class="portfolio-stage-count">--</span>',
   '<span class="portfolio-stage-name">规划</span>\n                <span class="portfolio-stage-count">1</span>'],
  ['<div class="portfolio-stage-fill planning" style="width:--%"></div>',
   '<div class="portfolio-stage-fill planning" style="width:8%"></div>'],
  ['<span class="portfolio-stage-name">执行</span>\n                <span class="portfolio-stage-count">--</span>',
   '<span class="portfolio-stage-name">执行</span>\n                <span class="portfolio-stage-count">2</span>'],
  ['<div class="portfolio-stage-fill running" style="width:--%"></div>',
   '<div class="portfolio-stage-fill running" style="width:100%"></div>'],
  ['<span class="portfolio-stage-name">受阻</span>\n                <span class="portfolio-stage-count">--</span>',
   '<span class="portfolio-stage-name">受阻</span>\n                <span class="portfolio-stage-count">1</span>'],
  ['<div class="portfolio-stage-fill blocked" style="width:--%"></div>',
   '<div class="portfolio-stage-fill blocked" style="width:50%"></div>'],
  ['<span class="portfolio-stage-name">已完成</span>\n                <span class="portfolio-stage-count">--</span>',
   '<span class="portfolio-stage-name">已完成</span>\n                <span class="portfolio-stage-count">1</span>'],
  ['<div class="portfolio-stage-fill done" style="width:--%"></div>',
   '<div class="portfolio-stage-fill done" style="width:100%"></div>'],
  ['<span class="portfolio-summary-num">--%</span>',
   '<span class="portfolio-summary-num">56%</span>'],
  ['<span class="portfolio-summary-num">-- 天</span>',
   '<span class="portfolio-summary-num">42 天</span>'],
  // Boundary
  ['快照时间：2026-07-25 --:-- CST', '快照时间：2026-07-25 14:30 CST'],
]);

// ============================================================
// 2. project-dept.html
// ============================================================
processFile('project-dept.html', [
  ['<div class="pulse-label">参与部门</div>\n            <div class="pulse-num">--</div>',
   '<div class="pulse-label">参与部门</div>\n            <div class="pulse-num">4</div>'],
  ['<div class="pulse-label">参与员工</div>\n            <div class="pulse-num">--</div>',
   '<div class="pulse-label">参与员工</div>\n            <div class="pulse-num">13</div>'],
  ['<div class="pulse-label">核心团队</div>\n            <div class="pulse-num">--</div>',
   '<div class="pulse-label">核心团队</div>\n            <div class="pulse-num">5</div>'],
  ['<div class="boundary-ts">快照时间: --</div>',
   '<div class="boundary-ts">快照时间: 2026-07-25 14:30</div>'],
]);

// ============================================================
// 3. project-detail.html
// ============================================================
processFile('project-detail.html', [
  ['Curis 产品 V2.4', '客户管理系统 v2.0'],
  ['张明（研发部总监）', '张伟（PM）'],
  ['完成 V2.4 版本全部功能开发、测试和上线交付，包含 3 个核心模块重构',
   '完成客户管理系统第二版开发，包含 CRM 模块、工单系统、数据看板三大功能模块'],
  ['2026-05-10 ~ 2026-08-15（共 97 天）', '2026-06-01 ~ 2026-09-30（共 122 天）'],
  ['<div class="info-value">--</div>\n            </div>\n          </div>\n        </div>',
   '<div class="info-value">~45k tokens · 累计 $0.12</div>\n            </div>\n          </div>\n        </div>'],
  ['72% 完成', '30% 完成'],
  ['<div class="progress-bar-main" style="width:72%">', '<div class="progress-bar-main" style="width:30%">'],
  ['模块 A：用户界面重构', '① 需求评审完成'],
  ['模块 B：数据管道升级', '② 数据库设计完成'],
  ['模块 C：API 网关优化', '③ CRM 模块开发中'],
  ['集成测试与回归', '④ 工单系统开发'],
  ['生产环境部署', '⑤ 数据看板开发'],
]);

// ============================================================
// 4. org-center.html
// ============================================================
processFile('org-center.html', [
  ['<div class="fact-number">--</div>\n              <div class="fact-label">部门数</div>',
   '<div class="fact-number">3</div>\n              <div class="fact-label">部门数</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">员工数</div>',
   '<div class="fact-number">24</div>\n              <div class="fact-label">员工数</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">阻塞部门</div>',
   '<div class="fact-number">0</div>\n              <div class="fact-label">阻塞部门</div>'],
  ['<span class="health-label">运行正常</span>\n                </div>\n                <span class="health-count">--</span>',
   '<span class="health-label">运行正常</span>\n                </div>\n                <span class="health-count">2</span>'],
  ['<span class="health-label">需关注</span>\n                </div>\n                <span class="health-count">--</span>',
   '<span class="health-label">需关注</span>\n                </div>\n                <span class="health-count">1</span>'],
  ['<span class="health-label">阻塞</span>\n                </div>\n                <span class="health-count">--</span>',
   '<span class="health-label">阻塞</span>\n                </div>\n                <span class="health-count">0</span>'],
  ['<div class="dept-card-name">研发中心</div>\n                <div class="dept-card-project">当前项目: --</div>',
   '<div class="dept-card-name">研发中心</div>\n                <div class="dept-card-project">当前项目: 客户管理系统 v2.0</div>'],
  ['<span class="dept-card-dep">依赖: --</span>',
   '<span class="dept-card-dep">依赖: 无</span>'],
  ['<div class="dept-card-name">产品部</div>\n                <div class="dept-card-project">当前项目: --</div>',
   '<div class="dept-card-name">产品部</div>\n                <div class="dept-card-project">当前项目: AI 智能客服部署</div>'],
  ['<span class="dept-card-dep">依赖: --</span>',
   '<span class="dept-card-dep">依赖: 研发中心</span>'],
  ['<div class="dept-card-name">市场部</div>\n                <div class="dept-card-project">当前项目: --</div>',
   '<div class="dept-card-name">市场部</div>\n                <div class="dept-card-project">当前项目: 官网品牌升级</div>'],
  ['<span class="dept-card-dep">依赖: --</span>',
   '<span class="dept-card-dep">依赖: 运营部</span>'],
  ['<div class="dept-card-name">运营部</div>\n                <div class="dept-card-project">当前项目: --</div>',
   '<div class="dept-card-name">运营部</div>\n                <div class="dept-card-project">当前项目: 供应链数据迁移</div>'],
  ['<span class="dept-card-dep">依赖: --</span>',
   '<span class="dept-card-dep">依赖: 研发中心</span>'],
  ['<span class="org-boundary-time">快照时间: --</span>',
   '<span class="org-boundary-time">快照时间: 2026-07-25 14:30</span>'],
]);

// ============================================================
// 5. org-dept.html
// ============================================================
processFile('org-dept.html', [
  ['<div class="fact-number">--</div>\n              <div class="fact-label">部门空间数</div>',
   '<div class="fact-number">3</div>\n              <div class="fact-label">部门空间数</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">活跃空间</div>',
   '<div class="fact-number">3</div>\n              <div class="fact-label">活跃空间</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">空闲空间</div>',
   '<div class="fact-number">0</div>\n              <div class="fact-label">空闲空间</div>'],
]);

// ============================================================
// 6. org-employees.html
// ============================================================
processFile('org-employees.html', [
  ['<div class="fact-number">--</div>\n              <div class="fact-label">员工总数</div>',
   '<div class="fact-number">24</div>\n              <div class="fact-label">员工总数</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">在岗</div>',
   '<div class="fact-number">18</div>\n              <div class="fact-label">在岗</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">空闲</div>',
   '<div class="fact-number">6</div>\n              <div class="fact-label">空闲</div>'],
  ['<div class="fact-number">--</div>\n              <div class="fact-label">阻塞</div>',
   '<div class="fact-number">0</div>\n              <div class="fact-label">阻塞</div>'],
]);

// ============================================================
// 7. department-detail.html
// ============================================================
processFile('department-detail.html', [
  ['员工 18 人 · 当前项目 2 个 · 负责人 张明', '员工 12 人 · 当前项目 5 个 · 负责人 张伟'],
  ['张明（总监）', '张伟（PM）'],
  ['18 人（含 AI 员工 6 人）', '12 人（含 AI 员工 6 人）'],
  ['Q3 完成 V2.4 交付，同步启动 V3.0 架构设计', 'Q3 完成客户管理系统 v2.0 交付，含 CRM、工单、看板三大模块'],
  ['<div class="project-name-mini">Curis 产品 V2.4 交付</div>\n              <div class="project-meta-mini">进度 72% · 预计 8 月 15 日</div>\n            </div>\n            <div class="project-progress-mini"><div class="project-bar" style="width:72%"></div>',
   '<div class="project-name-mini">客户管理系统 v2.0</div>\n              <div class="project-meta-mini">进度 30% · 预计 9 月 30 日</div>\n            </div>\n            <div class="project-progress-mini"><div class="project-bar" style="width:30%"></div>'],
  ['<div class="project-name-mini">V3.0 架构预研</div>\n              <div class="project-meta-mini">进度 15% · 早期阶段</div>\n            </div>\n            <div class="project-progress-mini"><div class="project-bar" style="width:15%"></div>',
   '<div class="project-name-mini">移动端性能优化</div>\n              <div class="project-meta-mini">进度 65% · 预计 8 月 20 日</div>\n            </div>\n            <div class="project-progress-mini"><div class="project-bar" style="width:65%"></div>'],
  ['质量保障 -- 离线', '质量保障 · 离线'],
]);

// ============================================================
// 8. employee-detail.html
// ============================================================
processFile('employee-detail.html', [
  ['<span class="tag">--</span>',
   '<span class="tag" style="background:var(--state-success-surface);color:var(--state-success)">运行中</span>'],
  ['<div class="info-label">姓名</div><div class="info-value">--</div>',
   '<div class="info-label">姓名</div><div class="info-value">张伟</div>'],
  ['<div class="info-label">岗位</div><div class="info-value">--</div>',
   '<div class="info-label">岗位</div><div class="info-value">PM（项目经理）</div>'],
  ['<div class="info-label">部门</div><div class="info-value">--</div>',
   '<div class="info-label">部门</div><div class="info-value">研发部</div>'],
  ['<div class="info-label">入职时间</div><div class="info-value">--</div>',
   '<div class="info-label">入职时间</div><div class="info-value">2024-03-15</div>'],
  ['<div class="info-label">汇报对象</div><div class="info-value">--</div>',
   '<div class="info-label">汇报对象</div><div class="info-value">研发总监</div>'],
  ['<div class="info-label">当前职责</div><div class="info-value">--</div>',
   '<div class="info-label">当前职责</div><div class="info-value">负责客户管理系统 v2.0 项目管理，协调研发部、产品部、运营部跨团队协作，确保 Q3 里程碑按期交付</div>'],
  ['<div class="info-label">目标描述</div><div class="info-value">--</div>',
   '<div class="info-label">目标描述</div><div class="info-value">完成 CRM 模块核心功能开发、工单系统架构搭建、数据看板原型评审通过</div>'],
  ['<div class="info-label">优先级</div><div class="info-value">--</div>',
   '<div class="info-label">优先级</div><div class="info-value"><span style="color:var(--state-error);font-weight:600">P0 — 关键</span></div>'],
  ['<div class="info-label">数据权限</div><div class="info-value">--</div>',
   '<div class="info-label">数据权限</div><div class="info-value">研发部全部数据、产品部需求文档（只读）</div>'],
  ['<div class="info-label">操作权限</div><div class="info-value">--</div>',
   '<div class="info-label">操作权限</div><div class="info-value">项目管理：创建/编辑/删除任务，审批工作流</div>'],
  ['<div class="info-label">审批权限</div><div class="info-value">--</div>',
   '<div class="info-label">审批权限</div><div class="info-value">部门内项目立项审批，&lt;= 50k token 预算审批</div>'],
]);

console.log(`\n=== Done. Skipped: ${skipCount} ===`);
