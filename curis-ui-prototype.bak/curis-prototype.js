/**
 * Curis Hi-Fi Prototype — shared interaction layer
 * Handles cross-page navigation, active nav state, toast feedback,
 * and common button affordances for the click-through demo.
 */
(function () {
  'use strict';

  const STORAGE_KEY = 'curis-prototype-state';

  const PAGE_BRIEFS = {
    'ceo-desk.html': '早上好。我已整理公司脉搏、今天必须决定的事项和即将到期的检查点。',
    'founding-flow.html': '我会陪你把第一家公司搭起来。每一步都可以接受、修改或跳过。',
    'business.html': '我正在看每条业务的承诺、真实结果和下一步安排。',
    'operating.html': '我在看运行中的业务、阻塞和需要你决定的变化。',
    'ai-organization.html': '我会持续观察 AI 团队的责任、负载和升级路径。',
    'workspace-portal.html': '我正在守着每个业务空间的运行状态和下一检查点。',
    'workspace-studio.html': '我会帮你把业务工序、岗位、能力和失败出口装配成可运行的空间。',
    'meeting.html': '我已替你准备会议目标、背景和待决事项，会议结束后会把共识转成可追踪的决议。',
    'decision-room.html': '我把事实、观点、未知和影响整理在这里，等你做最后判断。',
    'workspace-runtime-shortvideo.html': '我正在收集业务交付和外部平台反馈，遇到例外会来找你。',
    'workspace-runtime-xhs.html': '我正在守着小红书内容从研究到发布和结果回流的完整闭环。',
    'workspace-runtime-software.html': '研发办公室正在准备 Curis v0.2 的真实验收，我会把证据和 CEO 反馈带回下一周期。',
    'workspace-runtime-department.html': '我正在守着这间部门办公室的首项责任，等真实结果回来后替你准备下一次判断。',
    'assets.html': '我把公司已经验证的成果、依据和可复用流程整理在这里。',
    'knowledge.html': '我把 CEO 的资料、竞品信息、平台规则和公司经验整理成每个业务都能调用的上下文。',
    'finance.html': '我把收入、成本、AI 员工产出和每条业务的真实结果整理成经营判断。',
    'calendar.html': '我把公司的关键时刻、自动运行和成长记录整理成一条不会丢失的时间线。'
  };

  const ROOM_NAMES = {
    'ceo-desk.html': 'CEO 办公桌 · 今日经营',
    'founding-flow.html': '创建公司 · 第一间办公室',
    'business.html': '公司业务版图',
    'operating.html': '经营办公室 · 公司运行',
    'ai-organization.html': 'AI 团队办公室',
    'workspace-portal.html': '工作空间 · 部门办公室',
    'workspace-studio.html': '工作空间搭建 · 装修现场',
    'meeting.html': '会议工作台 · 外部合作方周会',
    'decision-room.html': '决策室 · CEO 决策',
    'workspace-runtime-shortvideo.html': '抖音 / TikTok 运营办公室 · 运行现场',
    'workspace-runtime-xhs.html': '小红书运营办公室 · 运行现场',
    'workspace-runtime-software.html': '研发办公室 · Curis v0.2',
    'workspace-runtime-department.html': '部门办公室 · 运行现场',
    'assets.html': '成果库 · 公司成果',
    'knowledge.html': '知识库 · 公司上下文',
    'finance.html': '财务与经营 · CEO 视角',
    'calendar.html': '公司日历 · 成长记录'
  };

  const ASSISTANT_ROUTES = [
    { words: ['预算', '决策', '批准', '风险'], label: '决策室', route: 'decision-room.html' },
    { words: ['会议', '周会', '议程', '共识'], label: '会议工作台', route: 'meeting.html' },
    { words: ['抖音', '短视频', '视频', '内容'], label: '内容办公室', route: 'workspace-runtime-shortvideo.html' },
    { words: ['软件开发', 'Curis v0.2', '研发', '验收', '代码'], label: '研发办公室', route: 'workspace-runtime-software.html' },
    { words: ['团队', '员工', '组织', '负载'], label: 'AI 组织办公室', route: 'ai-organization.html' },
    { words: ['工作空间', '空间', '办公室'], label: '工作空间入口', route: 'workspace-portal.html' },
    { words: ['业务', '机会', '扩大', '暂停'], label: '业务版图', route: 'business.html' },
    { words: ['创建公司', '从零', '创业'], label: '公司创建', route: 'founding-flow.html' }
  ];

  const FOUNDING_TEMPLATES = {
    software: {
      label: '软件开发 · Curis 自研', description: '产品、研发、测试与 CEO 验收协同，把 Curis 自己持续做出来。',
      opportunity: 'Curis 需要一个能持续研发自己的 AI 团队，让每次产品改进都能被真实使用反馈验证。', outcome: '30 天内完成 Curis v0.2 验收，并由 CEO 通过首轮真实使用。', feedback: 'CEO 验收 + 产品使用反馈',
      teamIntro: '基于“软件开发 · Curis 自研”，我建议先配置产品、研发、QA 和运行反馈四个责任位。每个角色都有明确交接，发布前保留 CEO 真实验收。',
      team: [
        ['产品 AI', '把 CEO 意图转成可验证的产品增量', '需求拆解', '验收标准'],
        ['研发 AI', '在批准范围内完成 Curis 的实现与发布准备', '代码实现', '回归修复'],
        ['QA AI', '验证真实路径、回归和证据可信度', '场景回归', '证据整理'],
        ['运行反馈 AI', '回收真实使用反馈，整理下一周期改进', '反馈归因', '改进建议']
      ],
      simulation: ['正常：30 天内交付可运行增量并完成 CEO 真实验收', 'CEO 离线 7 天：研发继续在批准范围内执行，验收事项自动升级', '失败：验收未通过，保留证据并生成返工与下一周期决策']
    },
    xhs: {
      label: '内容增长 · 小红书', description: '选题、脚本、发布与平台数据回传。',
      opportunity: '小红书需要持续、可信的内容供给，AI 团队可以用更低成本验证内容增长。', outcome: '30 天内发布 12 条内容，获得首批真实互动与线索。', feedback: '小红书平台数据 + CEO 复盘',
      teamIntro: '基于“小红书内容增长”，我建议先配置策略、内容、发布和复盘四个责任位。AI 可以连续运行，但品牌边界、敏感表达和发布仍由 CEO 把关。',
      team: [
        ['策略 AI', '研究平台趋势、竞品和账号历史，形成选题依据', '趋势研究', '选题策略'],
        ['内容 AI', '生成标题、正文、封面方向和多版本草稿', '文案生成', '品牌语气'],
        ['发布 AI', '完成发布准备、排期和平台权限检查', '发布排期', '平台检查'],
        ['复盘 AI', '回收阅读、赞、藏、评、粉丝与线索，提出下一轮改进', '数据回收', '结果归因']
      ],
      simulation: ['正常：每周 3 条内容进入发布队列，数据在窗口结束后自动回收', 'CEO 离线 7 天：内容停在发布前检查点，低风险复盘继续运行', '失败：授权或敏感表达异常时暂停发布并把修改意见交回内容 AI']
    },
    douyin: {
      label: '抖音 / TikTok 运营 · 抖音 / TikTok', description: '内容策划、制作、发布和外部结果复盘。',
      opportunity: '抖音 / TikTok 内容需要稳定产出并回收播放、互动与成交数据，AI 团队负责从选题到复盘的完整链路。', outcome: '30 天内发布 12 条视频，建立播放、粉丝和成交反馈闭环。', feedback: '抖音平台数据 + 手动补录',
      teamIntro: '基于“抖音 / TikTok 运营”，我建议先配置策略、脚本、制作和数据复盘四个责任位。平台授权不可用时，结果窗口会保留给 CEO 手动补录。',
      team: [
        ['策略 AI', '研究平台趋势、受众和账号历史，确定视频假设', '趋势研究', '选题优先级'],
        ['脚本 AI', '拆解结构、写脚本、设计开场和行动引导', '脚本生成', '结构检查'],
        ['制作 AI', '准备拍摄、剪辑和发布素材，保留版本记录', '素材编排', '剪辑检查'],
        ['数据 AI', '回收播放、完播、互动、粉丝和成交，整理投入产出线索', '数据回收', '复盘归因']
      ],
      simulation: ['正常：视频按排期发布，平台数据在授权窗口回流并形成复盘', 'CEO 离线 7 天：素材继续准备，发布和投流停在授权检查点', '失败：数据授权或内容风险异常时暂停，保留原始素材和反馈窗口']
    }
  };

  const I18N = [
    ['Curis Labs', 'Curis 公司'],
    ['Business Engineering AI', '业务工程 AI'],
    ['Business Analysis AI', '业务分析 AI'],
    ['Engineering AI', '研发 AI'],
    ['Content AI', '内容 AI'],
    ['Growth AI', '增长 AI'],
    ['Research AI', '研究 AI'],
    ['Publishing AI', '发布 AI'],
    ['Shooting AI', '拍摄 AI'],
    ['Editor AI', '剪辑 AI'],
    ['Video AI', '视频 AI'],
    ['Data AI', '数据 AI'],
    ['Review AI', '复盘 AI'],
    ['Professional AI', '专业 AI'],
    ['reviewers', '评审'],
    ['Operating Day', '经营日'],
    ['CEO OPERATING DAY', 'CEO 经营日'],
    ['CEO OFFICE', 'CEO 办公室'],
    ['DAY 01', '第一天'],
    ['Workforce Map', 'AI 员工地图'],
    ['Research Lead', '研究负责人'],
    ['Engineering Lead', '研发负责人'],
    ['Truth Layer', '事实层'],
    ['Commitment', '承诺'],
    ['Research', '研究'],
    ['Finance', '财务'],
    ['pipeline', '流水线'],
    ['mock', '模拟'],
    ['sprint', '迭代周期'],
    ['pass', '通过'],
    ['week', '周'],
    ['hook', '开场钩子'],
    ['Task', '任务'],
    ['Truth', '事实'],
    ['Operating', '运行中'],
    ['Day', '日'],
    ['Lead', '负责人'],
    ['commit', '提交'],
    ['Workspace AI', '空间 AI'],
    ['CEO Assistant', 'CEO 助理'],
    ['Assistant · Curis', '助理 · Curis'],
    ['Assistant', '助理'],
    ['Decision Room', '决策室'],
    ['Founding Flow', '创建公司'],
    ['Curis 创建公司', 'Curis'],
    ['Workspace Studio', '工作空间搭建'],
    ['Workspace Runtime', '工作空间运行'],
    ['Workspace Blueprint', '工作空间蓝图'],
    ['Discover', '发现'],
    ['Compose', '编排'],
    ['Bind', '绑定'],
    ['Staff', '岗位'],
    ['Simulate', '模拟'],
    ['Approver', '审批人'],
    ['Approve', '审批'],
    ['Operate', '运行'],
    ['Role Slot', '岗位槽位'],
    ['Tools', '工具'],
    ['Tool', '工具'],
    ['Skills', '能力'],
    ['Knowledge', '知识'],
    ['Analysis AI', '分析 AI'],
    ['Script AI', '脚本 AI'],
    ['External System', '外部系统'],
    ['Acceptance', '验收'],
    ['Layout', '布局'],
    ['History', '历史'],
    ['AI Team', 'AI 团队'],
    ['Workspace', '工作空间'],
    ['Runtime', '运行'],
    ['Studio', '搭建'],
    ['Business', '业务'],
    ['Step ', '第 '],
    ['Strategy', '策略'],
    ['Content', '内容'],
    ['Operations', '运营'],
    ['Sales', '商务'],
    ['Engineering Lead', '研发负责人'],
    ['Engineering', '工程'],
    ['Blueprint Canvas', '蓝图画布'],
    ['Blueprint', '蓝图'],
    ['Operating', '运行中'],
    ['Verified', '已验证'],
    ['Tracking', '跟踪中'],
    ['Paused', '已暂停'],
    ['On Track', '运行正常'],
    ['Attention', '关注'],
    ['Blocked', '阻塞'],
    ['Agent', 'AI 员工'],
    ['Handoff', '交接'],
    ['Stage', '阶段'],
    ['Truth Layer', '事实层'],
    ['Approval Packet', '审批包'],
    ['Credential Vault', '凭证库'],
    ['Outcome Timeline', '业务结果时间线'],
    ['Workspace Outcome', '业务结果'],
    ['Evidence & Acceptance', '证据与验收'],
    ['Evidence / Truth Layer', '证据 / 事实层'],
    ['Outcome', '业务结果'],
    ['Result', '结果'],
    ['Feedback', '外部反馈'],
    ['Decision', '决策'],
    ['Scaling', '扩大'],
    ['Experiment', '实验中'],
    ['At Risk', '有风险'],
    ['Exit', '退出'],
    ['Current Cycle', '当前周期'],
    ['Platform Data', '平台数据'],
    ['Trend Analysis', '趋势分析'],
    ['Next Cycle', '下一周期'],
    ['CEO Decision', 'CEO 决策'],
    ['Input', '输入'],
    ['Output', '输出'],
    ['Owner', '负责人'],
    ['Evidence', '证据'],
    ['Stale', '数据过期'],
    ['Unknown', '待补充'],
    ['Cycle', '周期'],
    ['Bet', '方向'],
    ['bet', '方向'],
    ['业务赌注', '业务方向'],
    ['业务下注', '业务方向'],
    ['首个业务赌注', '首个业务方向'],
    ['下月下注', '下月方向'],
    ['投资组合', '业务版图'],
    ['下注', '业务方向'],
    ['押注', '业务方向'],
    ['赌注', '业务方向'],
    ['ROI', '投入产出'],
    ['KPI', '工作指标'],
    ['可复用工作流', '可复用流程'],
    ['工作流资产', '流程成果'],
    ['工作流', '流程'],
    ['外部结果', '真实结果'],
    ['经营假设', '经营想法'],
    ['公司资产', '公司成果'],
    ['有效资产', '有效成果'],
    ['复用资产', '复用成果'],
    ['投资', '投入'],
    ['下一次投入判断', '下一步安排'],
    ['投入判断', '下一步安排'],
    ['实验中', '试运行中'],
    ['下一 方向', '下一步'],
    ['下一方向', '下一步'],
    ['回报', '反馈']
  ];

  // ── Navigation map (label text → page file)
  const NAV_MAP = {
    'CEO 工作台': 'ceo-desk.html',
    'CEO 办公桌': 'ceo-desk.html',
    '经营': 'operating.html',
    '经营概览': 'operating.html',
    '业务': 'business.html',
    '业务空间': 'business.html',
    '公司': 'ai-organization.html',
    'AI 团队': 'ai-organization.html',
    '工作空间': 'workspace-portal.html',
    '决策': 'decision-room.html',
    '决策室': 'decision-room.html',
    '会议': 'meeting.html',
    '设置': '#',
    '帮助': '#',
    '帮助与反馈': '#',
    '员工目录': '#',
    '能力中心': '#'
    ,'成果': 'assets.html'
    ,'成果库': 'assets.html'
    ,'财务': 'finance.html'
    ,'财务与经营': 'finance.html'
    ,'日历': 'calendar.html'
    ,'自动化': 'calendar.html'
  };

  function readState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch (_) {
      return {};
    }
  }

  function writeState(patch) {
    const next = { ...readState(), ...patch };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    window.dispatchEvent(new CustomEvent('curis-state-changed', { detail: next }));
    return next;
  }

  function updateScheduledRunStatus(runId, status, extra = {}) {
    const current = readState();
    const events = Array.isArray(current.calendarEvents) ? current.calendarEvents : [];
    const target = events.find(event => event.runId === runId);
    if (!target) return null;
    const { assistantMessage, ...runPatch } = extra;
    const statusUpdatedAt = new Date().toISOString();
    const next = { ...target, ...runPatch, status, statusUpdatedAt };
    if (status === 'acknowledged' && target.finishedAt && !next.ceoResponseMs) next.ceoResponseMs = Math.max(0, Date.parse(statusUpdatedAt) - Date.parse(target.finishedAt));
    if (status === 'resolved' && target.openedAt && !next.ceoResolutionMs) next.ceoResolutionMs = Math.max(0, Date.parse(statusUpdatedAt) - Date.parse(target.openedAt));
    const calendarEvents = events.map(event => event.runId === runId ? next : event);
    writeState({ calendarEvents, ...(current.lastScheduledRun?.runId === runId ? { lastScheduledRun: next } : {}), ...(assistantMessage ? { lastAssistantMessage: assistantMessage } : {}) });
    return next;
  }

  function resolveScheduledRuns(runIds, { outcomeId = '', resolutionNote = '结果已回流，进入下一次复盘。' } = {}) {
    [...new Set((Array.isArray(runIds) ? runIds : [runIds]).filter(id => id && id !== 'manual'))].forEach(runId => {
      const run = (readState().calendarEvents || []).find(item => item.runId === runId);
      if (!run || !['waiting_ceo', 'acknowledged', 'failed'].includes(run.status)) return;
      updateScheduledRunStatus(runId, 'resolved', { requiresCEO: false, resolvedAt: new Date().toISOString(), nextStage: '进入复盘', resolutionNote, ...(outcomeId ? { outcomeId } : {}) });
    });
  }

  function promoteQueuedRuns(business) {
    const current = readState();
    const events = Array.isArray(current.calendarEvents) ? current.calendarEvents : [];
    const contract = current.capacityContracts?.[business] || { maxConcurrent: 3 };
    const active = events.filter(event => event.business === business && event.status === 'running').length;
    const slots = Math.max(0, Number(contract.maxConcurrent || 3) - active);
    const queued = events.filter(event => event.business === business && event.status === 'queued').sort((a, b) => String(a.queuedAt || a.requestedAt || '').localeCompare(String(b.queuedAt || b.requestedAt || ''))).slice(0, slots);
    if (!queued.length) return 0;
    const now = new Date().toISOString();
    const promoted = queued.map(run => ({ ...run, status: 'running', title: `${String(run.title || run.task || '自动任务').replace(/ · 排队中$/, '')} · 执行中`, startedAt: now, statusUpdatedAt: now, output: run.task || run.output, nextStage: '运行中' }));
    const calendarEvents = events.map(event => promoted.find(run => run.runId === event.runId) || event);
    const next = writeState({ calendarEvents, lastScheduledRun: promoted[promoted.length - 1], lastAssistantMessage: `${business} 已释放 ${promoted.length} 个容量，队列中的自动任务开始执行。`, lastAssistantHandoff: { label: '公司日历', route: 'calendar.html', message: '排队任务已开始执行' } });
    promoted.forEach(run => {
      window.setTimeout(() => {
        const finishedAt = new Date().toISOString();
        const waiting = Boolean(run.requiresCEOHint) || /CEO|授权|回传|失败|异常|确认/.test(`${run.task || ''}`);
        const costRecord = Number(run.cost || 0) > 0 ? { business: run.business, category: '模型与调用', amount: Number(run.cost), source: `自动运行 · ${run.owner || 'AI 员工'}`, model: run.capability?.model || '共享模型', agent: run.capability?.agent || run.owner || 'AI 员工', skills: run.capability?.skills || [], tools: run.capability?.tools || [], connector: run.capability?.connector || '手动录入', runId: run.runId, at: finishedAt } : null;
        const latest = readState();
        updateScheduledRunStatus(run.runId, waiting ? 'waiting_ceo' : 'completed', { title: `${String(run.title || '自动任务').replace(/ · 执行中$/, '')} · ${waiting ? '需 CEO 处理' : '已完成'}`, finishedAt, executionMs: Math.max(1, Date.parse(finishedAt) - Date.parse(run.startedAt || finishedAt)), requiresCEO: waiting, nextStage: waiting ? 'CEO 助理待汇报' : '进入下一工作阶段', output: run.task || run.output, assistantMessage: waiting ? `${run.title || '自动任务'} 已运行到需要 CEO 判断的节点。` : `${run.title || '自动任务'} 已完成并写回公司日历。` });
        if (costRecord) writeState({ financeCosts: [...(Array.isArray(latest.financeCosts) ? latest.financeCosts : []), costRecord].slice(-40) });
        promoteQueuedRuns(run.business);
      }, 180);
    });
    return promoted.length;
  }

  function syncAssistantRuntime(state, page) {
    const hasIntent = page === 'founding-flow.html' && Boolean(state.foundingIntent || document.querySelector('#ceo-intent')?.value?.trim());
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    const stage = !state.companyCreatedAt && !hasIntent
      ? { key: 'created', label: '已创建', index: 0, note: '正在等待 CEO 表达经营意图；公司还没有被假数据填满。' }
      : !commitment?.name
        ? { key: 'learning_context', label: '熟悉公司', index: 1, note: '我先熟悉公司的边界、业务意图和你的优先级。' }
        : commitment.status === 'pending_revision'
          ? { key: 'upgraded', label: '等待升级', index: 4, note: '已收到 CEO 的调整要求，正在把责任带回工作空间搭建。' }
          : state.departmentResult
            ? { key: 'evaluating', label: '评估中', index: 3, note: '已收到真实结果，正在整理证据并准备下一次 CEO 判断。' }
            : { key: 'operating', label: '运行中', index: 2, note: `正在守住${department?.name || '业务办公室'}的首项责任，等待真实结果回报。` };
    const previous = state.ceoAssistant || {};
    const runtime = {
      id: 'ceo-assistant',
      role: 'CEO 首席助理',
      reportsTo: 'CEO',
      responsibility: '观察、准备、提醒、跟进，并连接 CEO 与 AI 团队',
      lifecycleStage: stage.key,
      status: stage.label,
      lastTransitionAt: previous.lifecycleStage === stage.key ? (previous.lastTransitionAt || new Date().toISOString()) : new Date().toISOString()
    };
    if (previous.lifecycleStage !== runtime.lifecycleStage || previous.status !== runtime.status || !previous.id) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({ ...state, ceoAssistant: runtime }));
    }
    return stage;
  }

  function paintAssistantRuntime(root, stage, department) {
    if (!root || !stage) return;
    root.querySelector('.curis-assistant-runtime-state').textContent = stage.label;
    root.querySelector('.curis-assistant-runtime-note').textContent = stage.note;
    root.querySelector('.curis-companion-status').textContent = department?.name ? `正在关注${department.name}的运行` : stage.note.split('；')[0];
    root.querySelectorAll('.curis-assistant-runtime-step').forEach((step, index) => {
      step.classList.toggle('done', index < stage.index);
      step.classList.toggle('active', index === stage.index);
    });
  }

  function assistantAttention(state) {
    if (state.lastScheduledRun?.status === 'queued') return '自动任务等待可用容量';
    if (state.lastScheduledRun?.status === 'waiting_ceo') return '自动任务待你处理';
    if (state.lastScheduledRun?.status === 'acknowledged') return '自动任务已打开 · 等待完成处理';
    if (state.lastScheduledRun?.status === 'failed') return '自动任务异常';
    if (state.lastConnector?.status === 'pending') return '连接器授权待确认';
    const nextCycle = Object.values(state.growthNextCyclePlans || {}).find(item => item?.status === '已排期' || item?.status === '已进入选题池');
    if (nextCycle) return `${nextCycle.business}下一轮已准备`;
    if (state.departmentResult) return '结果已回报 · 等待你的判断';
    if (state.softwareAcceptance && state.softwareAcceptance.choice !== 'accept') return '研发验收需要你的判断';
    if (state.financeBrief) return '财务简报已准备';
    if (state.lastDecision) return '决策已记录 · 团队正在执行';
    if (state.meetingDecision) return '会议共识已归档 · 等待交接';
    return '';
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, character => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[character]));
  }

  function injectGlobalStyles() {
    if (document.getElementById('curis-global-layer')) return;
    const style = document.createElement('style');
    style.id = 'curis-global-layer';
    const darkTokens = `
      --background:#191a1d; --foreground:#e2e3e7; --card:#202226; --card-foreground:#e2e3e7;
      --popover:#25272b; --popover-foreground:#f4f5f7; --primary:#32f08c; --primary-foreground:#0c0c0d;
      --secondary:#2a2c31; --secondary-foreground:#eef0f3; --muted:#a4a7af; --muted-foreground:#a4a7af;
      --accent:#32f08c; --accent-foreground:#0c0c0d; --border:rgba(224,226,242,.12); --input:rgba(224,226,242,.18);
      --ring:#32f08c; --bg-base-default:#191a1d; --bg-base-secondary:#202226; --bg-base-tertiary:#25272b;
      --bg-overlay-l1:rgba(224,226,242,.04); --bg-overlay-l2:rgba(224,226,242,.06); --bg-overlay-l3:rgba(224,226,242,.08);
      --brand-500:#32f08c; --brand-600:#0fdc78; --brand-900:#02743b; --text-default:#e2e3e7;
      --text-default-hover:#f4f5f7; --text-secondary:#a4a7af; --text-tertiary:#777c86; --text-brand:#32f08c; --icon-brand:#32f08c;
      --border-neutral-l1:rgba(224,226,242,.10); --border-neutral-l2:rgba(224,226,242,.16); --border-neutral-l3:rgba(224,226,242,.24);
      --status-warning:#d6c49c; --status-error:#d8a5aa; --status-success:#a8c8b8; --status-primary:#aab6ff;
      --status-warning-surface:rgba(173,148,91,.14); --status-error-surface:rgba(172,108,119,.14);
      --status-success-surface:rgba(111,149,125,.14); --status-primary-surface:rgba(126,137,190,.14);`;
    const lightTokens = `
      --background:#f7f7f8; --foreground:#292b30; --card:#ffffff; --card-foreground:#292b30;
      --popover:#ffffff; --popover-foreground:#17181a; --primary:#30333a; --primary-foreground:#ffffff;
      --secondary:#eef0f2; --secondary-foreground:#292b30; --muted:#707681; --muted-foreground:#707681;
      --accent:#30333a; --accent-foreground:#ffffff; --border:rgba(25,28,34,.12); --input:rgba(25,28,34,.16);
      --ring:#30333a; --bg-base-default:#f7f7f8; --bg-base-secondary:#ffffff; --bg-base-tertiary:#f0f1f3;
      --bg-overlay-l1:rgba(25,28,34,.03); --bg-overlay-l2:rgba(25,28,34,.05); --bg-overlay-l3:rgba(25,28,34,.08);
      --brand-500:#30333a; --brand-600:#17181a; --brand-900:#626873; --text-default:#292b30;
      --text-default-hover:#17181a; --text-secondary:#626873; --text-tertiary:#8a909a; --text-brand:#30333a; --icon-brand:#30333a;
      --border-neutral-l1:rgba(25,28,34,.08); --border-neutral-l2:rgba(25,28,34,.14); --border-neutral-l3:rgba(25,28,34,.20);
      --status-warning:#8b6d2d; --status-error:#a05d66; --status-success:#467456; --status-primary:#5f6fd7;
      --status-warning-surface:rgba(174,143,69,.14); --status-error-surface:rgba(160,93,102,.12);
      --status-success-surface:rgba(70,116,86,.12); --status-primary-surface:rgba(95,111,215,.12);`;
    style.textContent = `
      html.dark, html[data-theme="dark"], html[data-theme="system"] { ${darkTokens} }
      html[data-theme="light"] { ${lightTokens} }
      @media (prefers-color-scheme: light) { html[data-theme="system"] { ${lightTokens} } }
      .main-area, .content, .main, .content-scroll, .workspace, .shell { background:var(--bg-base-default) !important; background-image:none !important; }
      /* Calm Executive Workspace: a surface may carry hierarchy, never decoration. */
      body[data-curis-neutral] * { background-image:none !important; }
      /* Neutral runtime pages use their own compact token names; keep the shell and cards on one surface. */
      body[data-curis-neutral], body[data-curis-neutral] .main, body[data-curis-neutral] .content { background:var(--bg) !important; color:var(--text); background-image:none !important; }
      html[data-theme="light"] body[data-curis-neutral] { --bg:#f7f7f8; --panel:#ffffff; --panel2:#f0f1f3; --text:#292b30; --muted:#626873; --faint:#8a909a; --line:rgba(25,28,34,.12); --accent:#30333a; --accentText:#ffffff; --ok:#467456; --warn:#8b6d2d; }
      html[data-theme="dark"] body[data-curis-neutral], html.dark body[data-curis-neutral] { --bg:#191a1d; --panel:#202226; --panel2:#1d1f22; --text:#e2e3e7; --muted:#a4a7af; --faint:#777c86; --line:rgba(224,226,242,.12); --accent:#32f08c; --accentText:#0c0c0d; --ok:#a8c8b8; --warn:#d6c49c; }
      @media (prefers-color-scheme: light) { html[data-theme="system"] body[data-curis-neutral] { --bg:#f7f7f8; --panel:#ffffff; --panel2:#f0f1f3; --text:#292b30; --muted:#626873; --faint:#8a909a; --line:rgba(25,28,34,.12); --accent:#30333a; --accentText:#ffffff; --ok:#467456; --warn:#8b6d2d; } }
      @media (prefers-color-scheme: dark) { html[data-theme="system"] body[data-curis-neutral] { --bg:#191a1d; --panel:#202226; --panel2:#1d1f22; --text:#e2e3e7; --muted:#a4a7af; --faint:#777c86; --line:rgba(224,226,242,.12); --accent:#32f08c; --accentText:#0c0c0d; --ok:#a8c8b8; --warn:#d6c49c; } }
      body[data-curis-neutral] .sidebar { background:var(--panel2) !important; }
      body[data-curis-neutral] .topbar { background:var(--bg) !important; }
      /* One company shell: every route uses the same brand, rhythm and left-aligned navigation. */
      body[data-curis-neutral] .app { width:100% !important; max-width:none !important; height:100vh !important; }
      body[data-curis-neutral] { margin:0 !important; min-height:100vh; }
      body[data-curis-neutral] .shell { display:flex !important; width:100% !important; min-height:100vh !important; }
      body[data-curis-neutral] .shell > .main { flex:1 1 auto !important; min-width:0 !important; min-height:100vh !important; overflow:auto !important; }
      body[data-curis-neutral] .shell > .main > .content { max-width:1120px; margin:0 auto; padding:32px !important; }
      body[data-curis-neutral] .shell > .main > .content > .header { display:flex; align-items:flex-start; justify-content:space-between; gap:24px; margin:0 0 24px; }
      body[data-curis-neutral] .shell > .main > .content .summary { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:10px; margin:0 0 18px; }
      body[data-curis-neutral] .shell > .main > .content .metric,
      body[data-curis-neutral] .shell > .main > .content .card,
      body[data-curis-neutral] .shell > .main > .content .callout { background:var(--bg-base-secondary) !important; border:1px solid var(--border-neutral-l1) !important; border-radius:10px; padding:16px; }
      body[data-curis-neutral] .shell > .main > .content .grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }
      body[data-curis-neutral] .shell > .main > .content .filters { display:flex; flex-wrap:wrap; gap:8px; margin:14px 0; }
      body[data-curis-neutral] .shell > .main > .content .filters button { padding:7px 10px; color:var(--text-secondary); background:transparent; border:1px solid var(--border-neutral-l2); border-radius:7px; font:inherit; cursor:pointer; }
      body[data-curis-neutral] .shell > .main > .content .filters button.is-active { color:var(--primary-foreground); background:var(--primary); border-color:var(--primary); }
      body[data-curis-neutral] .shell > .main > .content .asset-row { display:flex; align-items:center; justify-content:space-between; gap:16px; padding:13px 0; border-top:1px solid var(--border-neutral-l1); }
      body[data-curis-neutral] .shell > .main > .content .asset-actions { display:flex; gap:8px; flex:none; }
      body[data-curis-neutral] .shell > .main > .content .asset-actions button { padding:7px 9px; color:var(--text-default); background:transparent; border:1px solid var(--border-neutral-l2); border-radius:7px; font:inherit; cursor:pointer; }
      body[data-curis-neutral] .shell > .main > .content a.nav-item { color:var(--text-secondary) !important; text-decoration:none !important; }
      body[data-curis-neutral] .sidebar { width:220px !important; min-width:220px !important; flex:0 0 220px !important; box-sizing:border-box; padding:16px 12px !important; }
      body[data-curis-neutral] .sidebar > .brand,
      body[data-curis-neutral] .sidebar > .sidebar-brand { display:flex !important; align-items:center !important; gap:10px !important; min-height:28px; margin:0 0 24px !important; padding:0 12px !important; color:var(--text-default-hover,#f4f5f7) !important; font-size:18px !important; font-weight:700 !important; letter-spacing:-.02em; }
      body[data-curis-neutral] .sidebar .brand-mark { display:grid !important; place-items:center; width:22px; height:22px; flex:0 0 22px; border-radius:7px; color:var(--primary-foreground,#0c0c0d) !important; background:var(--primary,#32f08c) !important; font-size:13px; font-weight:800; }
      body[data-curis-neutral] .sidebar .brand-dot { display:grid !important; place-items:center; width:22px; height:22px; flex:0 0 22px; border-radius:7px; color:var(--primary-foreground,#0c0c0d) !important; background:var(--primary,#32f08c) !important; }
      body[data-curis-neutral] .sidebar .brand-dot::after { content:"C"; font-size:13px; font-weight:800; }
      body[data-curis-neutral] .sidebar .curis-canonical-sidebar-main { display:flex !important; flex-direction:column !important; flex:1 !important; min-height:0 !important; overflow:auto !important; }
      body[data-curis-neutral] .sidebar .curis-nav-section { display:grid !important; gap:3px !important; margin:0 !important; }
      body[data-curis-neutral] .sidebar .nav-label { margin:14px 0 3px !important; padding:0 10px !important; color:var(--text-secondary,#a4a7af) !important; font-size:11px !important; font-weight:500 !important; }
      body[data-curis-neutral] .sidebar .nav-item { display:flex !important; align-items:center !important; justify-content:flex-start !important; gap:10px !important; width:100% !important; min-height:32px; box-sizing:border-box; padding:8px 10px !important; border-radius:8px; text-align:left !important; }
      body[data-curis-neutral] .sidebar .nav-item { color:var(--text-secondary) !important; text-decoration:none !important; }
      body[data-curis-neutral] .sidebar .nav-item > .nav-icon,
      body[data-curis-neutral] .sidebar .nav-item > .icon { width:18px; min-width:18px; flex:0 0 18px; margin:0 !important; text-align:center; }
      body[data-curis-neutral] .sidebar .nav-item > .nav-badge { margin-left:auto !important; }
      body[data-curis-neutral] .sidebar .assistant-mini { display:none !important; }
      body[data-curis-neutral] .sidebar .nav-item.active { color:var(--text-default-hover,#f4f5f7) !important; background:var(--bg-base-tertiary,#25272b) !important; }
      body[data-curis-neutral] .topbar { height:52px !important; min-height:52px !important; box-sizing:border-box; padding:0 24px !important; }
      body[data-curis-neutral] .decision-panel .panel-header { background:var(--bg-base-secondary) !important; color:var(--text-default) !important; }
      body[data-curis-neutral] .decision-panel .decision-area { background:var(--bg-base-secondary) !important; }
      /* Every runtime page shares the same quiet executive palette; business-specific layouts may vary, but not the visual noise. */
      body[data-curis-neutral] {
        --background:var(--bg); --foreground:var(--text); --card:var(--panel); --card-foreground:var(--text);
        --popover:var(--panel2); --popover-foreground:var(--text); --primary:var(--accent); --primary-foreground:var(--accentText);
        --secondary:var(--panel2); --secondary-foreground:var(--text); --accent-foreground:var(--accentText); --border:var(--line); --input:var(--line); --ring:var(--accent);
        --bg-base-default:var(--bg); --bg-base-secondary:var(--panel); --bg-base-tertiary:var(--panel2); --base:var(--panel2);
        --brand-100:var(--text); --brand-200:var(--text); --brand-300:var(--text); --brand-400:var(--accent); --brand-500:var(--accent); --brand-600:var(--accent); --brand-700:var(--accent); --brand-800:var(--accent); --brand-900:var(--muted);
        --text-onbrand:var(--accentText); --text-brand:var(--accent); --text-brand-hover:var(--accent); --icon-brand:var(--accent); --border-brand:var(--accent);
        --status-error:#b8757d; --status-error-surface:rgba(184,117,125,.14); --status-warning:var(--warn); --status-warning-surface:rgba(139,109,45,.14); --status-success:var(--ok); --status-success-surface:rgba(70,116,86,.14); --status-primary:var(--accent); --status-primary-surface:rgba(95,111,215,.14);
      }
      .logo, .assistant-avatar { background:var(--primary) !important; box-shadow:none !important; }
      .card.green { background:var(--bg-base-secondary) !important; border-color:var(--border-neutral-l2) !important; }
      .workspace-card, .anomaly-card, .matter-card { border-left-width:1px !important; border-left-color:var(--border-neutral-l2,rgba(224,226,242,.16)) !important; }
      .pill-blocked { background:var(--status-error-surface,#ac6c77) !important; color:var(--status-error,#d8a5aa) !important; }
      .curis-companion { position:fixed; right:24px; bottom:24px; z-index:1100; font-family:var(--font-body,system-ui,sans-serif); }
      body:has([data-capability-runtime]) .curis-companion { bottom:88px; }
      .curis-companion-entry { display:flex; align-items:center; gap:10px; padding:9px 13px 9px 9px; color:var(--text-default-hover,#f5f9fe); background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:999px; cursor:pointer; box-shadow:0 6px 18px rgba(0,0,0,.18); transition:background .18s ease,border-color .18s ease,transform .18s ease; }
      .curis-companion-entry:hover { background:var(--bg-base-tertiary,#25272b); border-color:var(--border-neutral-l3,rgba(224,226,242,.24)); transform:translateY(-1px); }
      .curis-companion.has-attention .curis-companion-entry { border-color:var(--status-primary,#aab6ff); }
      .curis-companion.has-attention .curis-companion-status { color:var(--text-default-hover,#f4f5f7); }
      .curis-companion.has-attention .curis-companion-status::before { background:var(--status-primary,#aab6ff); box-shadow:0 0 0 3px color-mix(in srgb,var(--status-primary,#aab6ff) 16%,transparent); }
      .curis-companion-footer { bottom:84px; }
      .curis-companion-studio { bottom:160px; }
      .curis-companion-avatar { display:grid; place-items:center; width:28px; height:28px; border-radius:50%; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); font-size:12px; font-weight:700; }
      .curis-companion-copy { display:flex; flex-direction:column; gap:2px; text-align:left; }
      .curis-companion-name { font-size:12px; font-weight:600; line-height:1.2; }
      .curis-companion-status { display:flex; align-items:center; gap:5px; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.2; }
      .curis-companion-status::before { content:""; width:5px; height:5px; border-radius:50%; background:var(--status-success,#a8c8b8); }
      body[data-curis-neutral] .result > button[data-runtime-action="manual-result"], body[data-curis-neutral] .result > button[data-runtime-action="xhs-feedback"] { display:inline-flex; align-items:center; justify-content:center; width:max-content; margin-top:4px; padding:8px 10px; color:var(--text,#e2e3e7); background:transparent; border:1px solid var(--line,rgba(224,226,242,.12)); border-radius:7px; font:inherit; font-size:11px; cursor:pointer; }
      body[data-curis-neutral] .result > button[data-runtime-action="manual-result"]:hover, body[data-curis-neutral] .result > button[data-runtime-action="xhs-feedback"]:hover { background:var(--panel2,#1d1f22); border-color:var(--text-secondary,#a4a7af); }
      .curis-companion-panel { display:none; width:min(360px,calc(100vw - 32px)); margin-bottom:10px; overflow:hidden; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:14px; box-shadow:0 16px 44px rgba(0,0,0,.32); }
      .curis-companion.is-open .curis-companion-panel { display:block; }
      .curis-companion.is-open .curis-companion-entry { display:none; }
      .curis-companion-head { display:flex; align-items:center; justify-content:space-between; padding:14px 16px; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-companion-head strong { font-size:13px; }
      .curis-companion-close { border:0; color:var(--text-secondary,#a4a7af); background:transparent; cursor:pointer; font-size:18px; line-height:1; }
      .curis-companion-body { padding:16px; }
      .curis-companion-greeting { margin:0; color:var(--text-default,#e2e3e7); font-size:13px; line-height:1.55; }
      .curis-companion-context { margin:12px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-companion-room { margin:6px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-assistant-runtime { display:grid; gap:8px; margin-top:14px; padding-top:12px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-assistant-runtime-head { display:flex; align-items:center; justify-content:space-between; gap:10px; }
      .curis-assistant-runtime-title { color:var(--text-secondary,#a4a7af); font-size:10px; letter-spacing:.02em; }
      .curis-assistant-runtime-state { display:inline-flex; align-items:center; gap:5px; color:var(--status-success,#a8c8b8); font-size:10px; }
      .curis-assistant-runtime-state::before { content:""; width:5px; height:5px; border-radius:50%; background:currentColor; }
      .curis-assistant-runtime-steps { display:grid; grid-template-columns:repeat(5,1fr); gap:4px; }
      .curis-assistant-runtime-step { height:3px; border-radius:3px; background:var(--bg-base-tertiary,#25272b); }
      .curis-assistant-runtime-step.done, .curis-assistant-runtime-step.active { background:var(--status-success,#a8c8b8); }
      .curis-assistant-runtime-step.active { box-shadow:0 0 0 2px color-mix(in srgb,var(--status-success,#a8c8b8) 18%,transparent); }
      .curis-assistant-runtime-note { color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.4; }
      .curis-companion-next { display:none; width:100%; margin-top:9px; padding:7px 9px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; text-align:left; }
      .curis-companion-next.is-visible { display:block; }
      .curis-companion-next:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-companion-form { display:flex; gap:8px; margin-top:14px; }
      .curis-companion-form input { min-width:0; flex:1; padding:9px 10px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; outline:none; }
      .curis-companion-form input:focus { border-color:var(--accent,#aab6ff); box-shadow:0 0 0 2px color-mix(in srgb,var(--accent,#aab6ff) 20%,transparent); }
      .curis-companion-form button { padding:0 12px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:8px; cursor:pointer; font-size:12px; font-weight:600; }
      .curis-theme-row { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:14px; padding-top:12px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-theme-row select { padding:5px 7px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; font:inherit; }
      @media (max-width:640px) { .curis-companion { right:16px; bottom:16px; } }
      @media (prefers-reduced-motion:reduce) { .curis-companion-entry { transition:none; } }
      .curis-business-map, .curis-office-shelf { margin:0 0 24px; padding:20px 22px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:12px; }
      .curis-map-header, .curis-office-header { display:flex; align-items:flex-start; justify-content:space-between; gap:20px; margin-bottom:18px; }
      .curis-map-kicker, .curis-office-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-map-title, .curis-office-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:18px; font-weight:600; letter-spacing:-.01em; }
      .curis-map-meta, .curis-office-meta { color:var(--text-tertiary,#777c86); font-size:12px; white-space:nowrap; }
      .curis-map-company { width:150px; margin:0 auto 14px; padding:10px 12px; text-align:center; color:var(--text-default-hover,#f4f5f7); background:var(--bg-base-tertiary,#25272b); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:9px; }
      .curis-map-company strong, .curis-map-node strong, .curis-office-item strong { display:block; font-size:13px; }
      .curis-map-company span, .curis-map-node span, .curis-office-item span { display:block; margin-top:4px; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-map-stem { width:1px; height:18px; margin:0 auto 4px; background:var(--border-neutral-l2,rgba(224,226,242,.16)); }
      .curis-map-nodes, .curis-office-list { display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:10px; }
      .curis-map-node, .curis-office-item { min-height:70px; padding:11px 12px; text-align:left; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:9px; cursor:pointer; transition:border-color .18s ease,background .18s ease,transform .18s ease; }
      .curis-map-node:hover, .curis-office-item:hover { background:var(--bg-base-tertiary,#25272b); border-color:var(--border-neutral-l3,rgba(224,226,242,.24)); transform:translateY(-1px); }
      .curis-map-node em, .curis-office-item em { display:inline-flex; margin-top:9px; padding:2px 6px; color:var(--text-secondary,#a4a7af); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-radius:999px; font-size:10px; font-style:normal; }
      .curis-map-relations { display:flex; flex-wrap:wrap; gap:7px 14px; margin-top:13px; padding-top:11px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-map-relations span { display:inline-flex; align-items:center; gap:5px; }
      .curis-map-relations b { color:var(--text-secondary,#a4a7af); font-weight:500; }
      .curis-office-list { grid-template-columns:repeat(3,minmax(0,1fr)); }
      .curis-office-item { min-height:82px; }
      .curis-office-item em { color:var(--status-success,#a8c8b8); }
      .curis-business-decision { margin:0 0 24px; padding:16px 18px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-business-decision-head { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; }
      .curis-business-decision-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-business-decision-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-business-decision-note { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; line-height:1.5; }
      .curis-business-decision-metrics { display:flex; flex-wrap:wrap; gap:6px 14px; margin-top:10px; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-business-decision-metrics span { white-space:nowrap; }
      .curis-business-decision-metrics b { font-weight:600; }
      .curis-business-decision-actions { display:flex; flex-wrap:wrap; gap:7px; margin-top:14px; }
      .curis-business-decision-actions button { padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; }
      .curis-business-decision-actions button.primary { color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-color:var(--primary,#d9dbe1); font-weight:600; }
      .curis-business-decision-actions button:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-business-decision-actions button.primary:hover { background:var(--brand-600,#f1f2f4); }
      .curis-business-create { margin:0 0 22px; padding:15px 18px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-business-create-head { display:flex; align-items:flex-start; justify-content:space-between; gap:14px; }
      .curis-business-create-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-business-create-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-business-create-note { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; line-height:1.5; }
      .curis-business-create-toggle { padding:7px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:1px solid var(--primary,#d9dbe1); border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; white-space:nowrap; }
      .curis-business-create-form { display:none; margin-top:14px; }
      .curis-business-create.is-open .curis-business-create-form { display:grid; gap:10px; }
      .curis-business-create-field { display:grid; gap:5px; }
      .curis-business-create-field label { color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-business-create-field input, .curis-business-create-field textarea { width:100%; box-sizing:border-box; padding:8px 9px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; font:inherit; font-size:11px; resize:vertical; }
      .curis-business-create-options { display:flex; flex-wrap:wrap; gap:7px; }
      .curis-business-create-option { padding:7px 9px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; }
      .curis-business-create-option:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-business-create-submit { justify-self:start; padding:7px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:1px solid var(--primary,#d9dbe1); border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; }
      .curis-focus { outline:2px solid var(--accent,#aab6ff) !important; outline-offset:3px; }
      @media (max-width:900px) { .curis-map-nodes { grid-template-columns:repeat(3,minmax(0,1fr)); } .curis-office-list { grid-template-columns:1fr; } .curis-map-header, .curis-office-header { flex-direction:column; gap:8px; } }
      @media (max-width:620px) { .curis-map-nodes { grid-template-columns:1fr 1fr; } }
      @media (prefers-reduced-motion:reduce) { .curis-map-node, .curis-office-item { transition:none; } }
      .curis-arrival-space { max-width:720px; margin:30px auto 28px; text-align:left; }
      .curis-arrival-frame { display:grid; grid-template-columns:1.05fr .95fr; overflow:hidden; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:14px; }
      .curis-arrival-room { padding:22px; background:var(--bg-base-default,#191a1d); }
      .curis-arrival-kicker { display:flex; align-items:center; justify-content:space-between; margin:0 0 28px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-arrival-kicker span:last-child { color:var(--text-tertiary,#777c86); }
      .curis-arrival-desk { display:grid; gap:9px; }
      .curis-arrival-slot { min-height:54px; padding:11px 12px; background:var(--bg-base-secondary,#202226); border:1px dashed var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:9px; }
      .curis-arrival-slot strong { display:block; color:var(--text-default,#e2e3e7); font-size:12px; font-weight:500; }
      .curis-arrival-slot span { display:block; margin-top:5px; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-arrival-slot.next { border-style:solid; border-color:var(--accent,#aab6ff); }
      .curis-arrival-slot.next span { color:var(--accent,#aab6ff); }
      .curis-arrival-note { display:flex; flex-direction:column; justify-content:space-between; padding:22px; }
      .curis-arrival-note h2 { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:17px; font-weight:600; line-height:1.4; }
      .curis-arrival-note p { margin:12px 0 0; color:var(--text-secondary,#a4a7af); font-size:12px; line-height:1.65; }
      .curis-arrival-steps { display:grid; gap:9px; margin-top:22px; }
      .curis-arrival-step { display:flex; gap:9px; align-items:flex-start; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.45; }
      .curis-arrival-step b { display:grid; place-items:center; width:18px; height:18px; flex:0 0 18px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-radius:50%; font-size:10px; }
      .curis-arrival-quote { margin-top:22px !important; color:var(--text-default,#e2e3e7) !important; }
      .curis-arrival-intent { display:flex; gap:7px; margin-top:18px; }
      .curis-arrival-intent input { min-width:0; flex:1; padding:8px 9px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; outline:none; font:inherit; font-size:11px; }
      .curis-arrival-intent input:focus { border-color:var(--accent,#aab6ff); }
      .curis-arrival-intent button { padding:0 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; white-space:nowrap; }
      .curis-template-panel { display:none; width:min(720px,100%); margin:20px auto 0; padding:16px; text-align:left; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:12px; }
      .curis-template-panel.is-open { display:block; }
      .curis-template-panel h2 { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-template-panel p { margin:5px 0 13px; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-template-list { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; }
      .curis-template-option { min-height:78px; padding:11px; text-align:left; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; cursor:pointer; transition:background .18s ease,border-color .18s ease; }
      .curis-template-option:hover { background:var(--bg-base-tertiary,#25272b); border-color:var(--border-neutral-l3,rgba(224,226,242,.24)); }
      .curis-template-option strong { display:block; font-size:12px; font-weight:600; }
      .curis-template-option span { display:block; margin-top:5px; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.45; }
      @media (max-width:620px) { .curis-template-list { grid-template-columns:1fr; } }
      @media (prefers-reduced-motion:reduce) { .curis-template-option { transition:none; } }
      @media (max-width:720px) { .curis-arrival-frame { grid-template-columns:1fr; } }
      .curis-discussion-section { padding:24px 0; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-discussion-header { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-bottom:16px; }
      .curis-discussion-header h2 { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:18px; font-weight:600; }
      .curis-discussion-header p { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-discussion-legend { display:flex; gap:6px; flex-wrap:wrap; justify-content:flex-end; }
      .curis-chat-stream { display:grid; gap:12px; }
      .curis-chat-message { display:flex; align-items:flex-start; gap:9px; max-width:92%; }
      .curis-chat-message.user { justify-content:flex-end; margin-left:auto; }
      .curis-chat-avatar { display:grid; place-items:center; width:28px; height:28px; flex:0 0 28px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-radius:50%; font-size:10px; font-weight:700; }
      .curis-chat-message.user .curis-chat-avatar { order:2; color:var(--text-default-hover,#f4f5f7); background:var(--bg-base-tertiary,#25272b); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); }
      .curis-chat-bubble { padding:10px 12px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:4px 12px 12px 12px; }
      .curis-chat-message.user .curis-chat-bubble { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-radius:12px 4px 12px 12px; }
      .curis-chat-meta { display:flex; align-items:center; gap:7px; margin-bottom:5px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-chat-name { color:var(--text-secondary,#a4a7af); font-weight:600; }
      .curis-chat-label { padding:2px 5px; border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:4px; color:var(--text-tertiary,#777c86); }
      .curis-chat-label.fact { color:var(--status-success,#a8c8b8); }
      .curis-chat-label.opinion { color:var(--accent,#aab6ff); }
      .curis-chat-label.unknown { color:var(--status-warning,#d6c49c); }
      .curis-chat-label.recommendation { color:var(--text-default-hover,#f4f5f7); }
      .curis-chat-text { margin:0; color:var(--text-default,#e2e3e7); font-size:12px; line-height:1.6; }
      .curis-chat-compose { display:flex; gap:8px; margin-top:14px; }
      .curis-chat-compose select, .curis-chat-compose input { min-width:0; padding:9px 10px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; font:inherit; outline:none; }
      .curis-chat-compose select { width:88px; flex:0 0 88px; }
      .curis-chat-compose input { flex:1; }
      .curis-chat-compose button { padding:0 12px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:8px; cursor:pointer; font-size:12px; font-weight:600; }
      @media (max-width:640px) { .curis-discussion-header { flex-direction:column; } .curis-chat-message { max-width:100%; } .curis-chat-compose { flex-wrap:wrap; } .curis-chat-compose input { min-width:calc(100% - 96px); } }
      .curis-office-presence { margin:0 0 18px; padding:18px 0 16px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-office-presence-head { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-bottom:16px; }
      .curis-office-presence-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-office-presence-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:18px; font-weight:600; letter-spacing:-.01em; }
      .curis-office-presence-subtitle { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-office-live { display:inline-flex; align-items:center; gap:7px; padding-top:3px; color:var(--text-secondary,#a4a7af); font-size:11px; white-space:nowrap; }
      .curis-office-live::before { content:""; width:6px; height:6px; border-radius:50%; background:var(--status-success,#a8c8b8); }
      .curis-office-presence-body { display:grid; grid-template-columns:minmax(0,1.12fr) minmax(260px,.88fr); gap:22px; }
      .curis-office-team { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; }
      .curis-office-person { min-width:0; padding:10px; text-align:left; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; cursor:pointer; transition:background .18s ease,border-color .18s ease; }
      .curis-office-person:hover, .curis-office-person.is-selected { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-color:var(--border-neutral-l3,rgba(224,226,242,.24)); }
      .curis-office-person-top { display:flex; align-items:center; gap:8px; }
      .curis-office-avatar { display:grid; place-items:center; width:24px; height:24px; flex:0 0 24px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-radius:50%; font-size:9px; font-weight:700; }
      .curis-office-person-name { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:11px; font-weight:600; }
      .curis-office-person-state { display:flex; align-items:center; gap:5px; margin:9px 0 0 32px; color:var(--text-secondary,#a4a7af); font-size:10px; line-height:1.35; }
      .curis-office-person-state::before { content:""; width:5px; height:5px; flex:0 0 5px; border-radius:50%; background:var(--status-success,#a8c8b8); }
      .curis-office-person.waiting .curis-office-person-state::before { background:var(--status-warning,#d6c49c); }
      .curis-office-route { padding-left:18px; border-left:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-office-route-title { margin:0 0 9px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-office-route-list { display:flex; flex-wrap:wrap; align-items:center; gap:7px; }
      .curis-office-route-step { padding:6px 8px; color:var(--text-default,#e2e3e7); background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:6px; font-size:10px; }
      .curis-office-route-arrow { color:var(--text-tertiary,#777c86); font-size:12px; }
      .curis-office-route-note { margin:10px 0 0; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.5; }
      @media (max-width:860px) { .curis-office-presence-body { grid-template-columns:1fr; } .curis-office-route { padding:14px 0 0; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-left:0; } }
      @media (max-width:620px) { .curis-office-presence-head { flex-direction:column; gap:7px; } .curis-office-team { grid-template-columns:repeat(2,minmax(0,1fr)); } }
      @media (prefers-reduced-motion:reduce) { .curis-office-person { transition:none; } }
      .curis-org-room { margin:0 0 22px; padding:18px 20px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:12px; }
      .curis-org-room-head { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; margin-bottom:15px; }
      .curis-org-room-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-org-room-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:18px; font-weight:600; letter-spacing:-.01em; }
      .curis-org-room-subtitle { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; }
      .curis-org-room-meta { color:var(--text-secondary,#a4a7af); font-size:11px; white-space:nowrap; }
      .curis-org-room-grid { display:grid; grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr); gap:18px; }
      .curis-org-room-team { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
      .curis-org-room-person { display:flex; align-items:center; gap:9px; min-width:0; padding:10px; text-align:left; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; cursor:pointer; transition:background .18s ease,border-color .18s ease; }
      .curis-org-room-person:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-color:var(--border-neutral-l3,rgba(224,226,242,.24)); }
      .curis-org-room-avatar { display:grid; place-items:center; width:26px; height:26px; flex:0 0 26px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-radius:50%; font-size:9px; font-weight:700; }
      .curis-org-room-person-copy { min-width:0; }
      .curis-org-room-person strong { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:11px; font-weight:600; }
      .curis-org-room-person span { display:block; margin-top:3px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-org-room-person em { margin-left:auto; color:var(--status-success,#a8c8b8); font-size:10px; font-style:normal; white-space:nowrap; }
      .curis-org-room-activity { padding-left:17px; border-left:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-org-room-activity-title { margin:0 0 9px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-org-room-event { display:grid; grid-template-columns:auto 1fr; gap:8px; padding:7px 0; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-org-room-event:first-of-type { border-top:0; }
      .curis-org-room-event-path { color:var(--text-default,#e2e3e7); font-size:10px; }
      .curis-org-room-event-note { color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-capacity-callout { margin:0 0 22px; padding:16px 18px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-capacity-callout.is-approved { border-color:var(--status-success,#a8c8b8); }
      .curis-capacity-callout-head { display:flex; align-items:flex-start; justify-content:space-between; gap:18px; }
      .curis-capacity-callout-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-capacity-callout-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-capacity-callout-note { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; line-height:1.5; }
      .curis-capacity-callout-grid { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; margin-top:13px; }
      .curis-capacity-callout-item { padding:9px 10px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; }
      .curis-capacity-callout-item span { display:block; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-capacity-callout-item strong { display:block; margin-top:4px; color:var(--text-default,#e2e3e7); font-size:12px; font-weight:500; }
      .curis-capacity-callout-actions { display:flex; flex-wrap:wrap; gap:7px; margin-top:13px; }
      .curis-capacity-callout-actions button { padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; }
      .curis-capacity-callout-actions button.primary { color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-color:var(--primary,#d9dbe1); font-weight:600; }
      .curis-capacity-callout-actions button:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-capacity-callout-actions button.primary:hover { background:var(--brand-600,#f1f2f4); }
      .curis-department-create { margin:0 0 22px; padding:15px 18px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-department-create-head { display:flex; align-items:flex-start; justify-content:space-between; gap:14px; }
      .curis-department-create-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-department-create-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-department-create-note { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; line-height:1.5; }
      .curis-department-create-toggle, .curis-department-create-submit { padding:7px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:1px solid var(--primary,#d9dbe1); border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; white-space:nowrap; }
      .curis-department-create-form { display:none; margin-top:14px; gap:10px; }
      .curis-department-create.is-open .curis-department-create-form { display:grid; }
      .curis-department-create-field { display:grid; gap:5px; }
      .curis-department-create-field label { color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-department-create-field input, .curis-department-create-field textarea { width:100%; box-sizing:border-box; padding:8px 9px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; font:inherit; font-size:11px; resize:vertical; }
      .curis-operating-state { margin:0 0 22px; padding:14px 16px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-operating-state-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-operating-state-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-operating-state-note { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; line-height:1.5; }
      .curis-operating-state-actions { display:flex; flex-wrap:wrap; gap:7px; margin-top:12px; }
      .curis-operating-state-actions button { padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; }
      .curis-operating-state-actions button:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-operating-archive { margin:0 0 22px; padding:15px 18px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-operating-archive-head { display:flex; align-items:baseline; justify-content:space-between; gap:12px; margin-bottom:11px; }
      .curis-operating-archive-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:14px; font-weight:600; }
      .curis-operating-archive-note { margin:0; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-operating-archive-list { display:grid; gap:7px; }
      .curis-operating-archive-item { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:9px 10px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; cursor:pointer; text-align:left; }
      .curis-operating-archive-item:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-operating-archive-item strong { display:block; font-size:11px; font-weight:500; }
      .curis-operating-archive-item span { display:block; margin-top:3px; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.35; }
      .curis-operating-archive-item em { color:var(--text-tertiary,#777c86); font-size:10px; font-style:normal; white-space:nowrap; }
      .curis-meeting-runtime { display:grid; grid-template-columns:190px minmax(0,1fr) 220px; gap:16px; }
      .curis-meeting-panel { min-width:0; padding:14px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-meeting-panel-title { margin:0 0 10px; color:var(--text-secondary,#a4a7af); font-size:10px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; }
      .curis-meeting-agenda { display:grid; gap:6px; }
      .curis-meeting-agenda-item { padding:8px 9px; color:var(--text-secondary,#a4a7af); background:transparent; border:1px solid transparent; border-radius:7px; font-size:11px; line-height:1.4; }
      .curis-meeting-agenda-item.is-current { color:var(--text-default,#e2e3e7); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-color:var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-meeting-chat { display:flex; flex-direction:column; min-height:470px; }
      .curis-meeting-chat-head { display:flex; justify-content:space-between; gap:10px; padding-bottom:12px; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-meeting-chat-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:14px; font-weight:600; }
      .curis-meeting-chat-note { margin:4px 0 0; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.45; }
      .curis-meeting-chat-state { color:var(--status-success,#a8c8b8); font-size:10px; white-space:nowrap; }
      .curis-meeting-stream { display:grid; gap:12px; flex:1; padding:14px 0; overflow:auto; }
      .curis-meeting-message { display:flex; gap:8px; align-items:flex-start; }
      .curis-meeting-avatar { display:grid; place-items:center; flex:0 0 auto; width:25px; height:25px; border-radius:50%; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); font-size:9px; font-weight:700; }
      .curis-meeting-bubble { min-width:0; padding:8px 10px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:9px; }
      .curis-meeting-meta { display:flex; flex-wrap:wrap; align-items:center; gap:6px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-meeting-name { color:var(--text-secondary,#a4a7af); font-weight:600; }
      .curis-meeting-tag { padding:2px 5px; border-radius:4px; color:var(--text-secondary,#a4a7af); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-meeting-tag.fact { color:var(--status-success,#a8c8b8); }
      .curis-meeting-tag.opinion { color:var(--status-primary,#aab6ff); }
      .curis-meeting-tag.unknown { color:var(--status-warning,#d6c49c); }
      .curis-meeting-tag.recommendation { color:var(--status-error,#d8a5aa); }
      .curis-meeting-text { margin:6px 0 0; color:var(--text-default,#e2e3e7); font-size:12px; line-height:1.55; white-space:pre-wrap; }
      .curis-meeting-composer { display:flex; gap:7px; padding-top:10px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-meeting-composer input { min-width:0; flex:1; padding:8px 9px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; font:inherit; font-size:11px; }
      .curis-meeting-composer button, .curis-meeting-decision { padding:8px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:1px solid var(--primary,#d9dbe1); border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; white-space:nowrap; }
      .curis-meeting-commitment { display:grid; gap:9px; }
      .curis-meeting-commitment-item { padding:9px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; }
      .curis-meeting-commitment-item strong { display:block; color:var(--text-default,#e2e3e7); font-size:11px; font-weight:500; line-height:1.4; }
      .curis-meeting-commitment-item span { display:block; margin-top:4px; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.4; }
      .curis-meeting-commitment-item.is-committed { border-color:rgba(168,200,184,.3); }
      .curis-meeting-commitment-item.is-committed span { color:var(--status-success,#a8c8b8); }
      .curis-meeting-summary { display:none; margin-top:12px; padding:10px; color:var(--text-secondary,#a4a7af); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-radius:7px; font-size:11px; line-height:1.5; }
      .curis-meeting-summary.is-visible { display:block; }
      @media (max-width:900px) { .curis-meeting-runtime { grid-template-columns:1fr; } .curis-meeting-panel.agenda { order:2; } .curis-meeting-panel.commitments { order:3; } }
      @media (max-width:860px) { .curis-org-room-grid { grid-template-columns:1fr; } .curis-org-room-activity { padding:14px 0 0; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-left:0; } }
      @media (max-width:620px) { .curis-org-room-head { flex-direction:column; gap:7px; } .curis-org-room-team { grid-template-columns:1fr; } .curis-capacity-callout-grid { grid-template-columns:1fr; } }
      @media (prefers-reduced-motion:reduce) { .curis-org-room-person { transition:none; } }
      .curis-feedback-capture .curis-feedback-head { display:flex; align-items:flex-start; justify-content:space-between; gap:10px; }
      .curis-feedback-capture { margin-bottom:16px; }
      .curis-feedback-capture .curis-feedback-title { color:var(--text-default-hover,#f4f5f7); font-size:13px; font-weight:600; }
      .curis-feedback-capture .curis-feedback-status { margin-top:4px; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.45; }
      .curis-feedback-capture .curis-feedback-status strong { color:var(--status-warning,#d6c49c); font-weight:500; }
      .curis-feedback-capture .curis-feedback-open { padding:6px 8px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:10px; white-space:nowrap; }
      .curis-feedback-capture .curis-feedback-open:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-feedback-form { display:none; margin-top:13px; padding-top:13px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-feedback-form.is-open { display:block; }
      .curis-feedback-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
      .curis-feedback-field { display:flex; flex-direction:column; gap:4px; }
      .curis-feedback-field label { color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-feedback-field input, .curis-feedback-field textarea { width:100%; min-width:0; padding:7px 8px; color:var(--text-default,#e2e3e7); background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:6px; outline:none; font:inherit; font-size:11px; }
      .curis-feedback-field textarea { min-height:48px; resize:vertical; }
      .curis-feedback-field input:focus, .curis-feedback-field textarea:focus { border-color:var(--accent,#aab6ff); }
      .curis-feedback-field.full { grid-column:1 / -1; }
      .curis-feedback-submit { width:100%; margin-top:9px; padding:8px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; }
      .curis-feedback-latest { display:none; margin-top:10px; padding:8px; color:var(--text-secondary,#a4a7af); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-radius:6px; font-size:10px; line-height:1.45; }
      .curis-feedback-latest.is-visible { display:block; }
      .curis-feedback-history { display:grid; gap:6px; margin-top:10px; }
      .curis-feedback-history-item { padding:8px 0; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.45; }
      .curis-feedback-history-item strong { display:block; color:var(--text-secondary,#a4a7af); font-weight:500; }
      @media (max-width:620px) { .curis-feedback-grid { grid-template-columns:1fr; } .curis-feedback-field.full { grid-column:auto; } }
      .curis-desk-opening { display:flex; align-items:center; justify-content:space-between; gap:14px; margin-bottom:14px; padding-bottom:14px; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-desk-opening-identity { display:flex; align-items:center; gap:9px; }
      .curis-desk-opening-avatar { display:grid; place-items:center; width:28px; height:28px; flex:0 0 28px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-radius:50%; font-size:11px; font-weight:700; }
      .curis-desk-opening-copy strong { display:block; color:var(--text-default-hover,#f4f5f7); font-size:12px; font-weight:600; }
      .curis-desk-opening-copy span { display:block; margin-top:2px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-desk-opening-action { padding:7px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; white-space:nowrap; }
      .curis-desk-opening-action:hover { background:var(--brand-600,#f1f2f4); }
      .curis-first-day { display:flex; align-items:flex-start; justify-content:space-between; gap:20px; margin:0 0 24px; padding:16px 18px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-first-day-kicker { margin:0 0 5px; color:var(--text-secondary,#a4a7af); font-size:10px; }
      .curis-first-day-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-first-day-note { margin:5px 0 0; color:var(--text-tertiary,#777c86); font-size:11px; line-height:1.5; }
      .curis-first-day-facts { display:grid; grid-template-columns:repeat(2,minmax(110px,1fr)); gap:8px 16px; min-width:270px; }
      .curis-first-day-fact span { display:block; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-first-day-fact strong { display:block; margin-top:3px; overflow:hidden; color:var(--text-default,#e2e3e7); font-size:11px; font-weight:500; text-overflow:ellipsis; white-space:nowrap; }
      .curis-first-day-action { align-self:center; flex:0 0 auto; padding:7px 9px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:10px; white-space:nowrap; }
      .curis-first-day-action:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      @media (max-width:760px) { .curis-first-day { flex-direction:column; } .curis-first-day-facts { width:100%; min-width:0; } .curis-first-day-action { align-self:flex-start; } }
      .curis-day-ribbon { display:flex; align-items:center; gap:18px; margin:0 0 18px; padding:10px 14px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-day-ribbon-head { flex:0 0 auto; min-width:150px; }
      .curis-day-ribbon-kicker { margin:0 0 2px; color:var(--text-tertiary,#777c86); font-size:10px; letter-spacing:.04em; }
      .curis-day-ribbon-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:13px; font-weight:600; }
      .curis-day-ribbon-sub { margin:2px 0 0; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-day-ribbon-track { display:flex; align-items:center; gap:0; flex:1; min-width:0; }
      .curis-day-ribbon-step { display:flex; align-items:center; gap:6px; min-width:0; padding:0; color:var(--text-tertiary,#777c86); background:transparent; border:0; font:inherit; font-size:10px; text-align:left; white-space:nowrap; cursor:pointer; }
      .curis-day-ribbon-step::before { content:""; width:7px; height:7px; flex:0 0 7px; border:1px solid var(--border-neutral-l3,rgba(224,226,242,.24)); border-radius:50%; background:var(--bg-base-default,#191a1d); }
      .curis-day-ribbon-step.is-done { color:var(--text-secondary,#a4a7af); }
      .curis-day-ribbon-step.is-done::before { background:var(--text-secondary,#a4a7af); border-color:var(--text-secondary,#a4a7af); }
      .curis-day-ribbon-step.is-current { color:var(--text-default-hover,#f4f5f7); font-weight:600; }
      .curis-day-ribbon-step.is-current::before { background:var(--text-default-hover,#f4f5f7); border-color:var(--text-default-hover,#f4f5f7); box-shadow:0 0 0 3px var(--bg-overlay-l3,rgba(224,226,242,.08)); }
      .curis-day-ribbon-connector { height:1px; flex:1; min-width:14px; margin:0 8px; background:var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-day-ribbon-time { display:block; margin-bottom:1px; color:var(--text-tertiary,#777c86); font-family:var(--font-mono,monospace); font-size:9px; font-weight:400; }
      @media (max-width:760px) { .curis-day-ribbon { align-items:flex-start; flex-direction:column; gap:10px; } .curis-day-ribbon-track { width:100%; overflow-x:auto; padding-bottom:2px; } .curis-day-ribbon-step { flex:0 0 auto; } }
      .curis-feedback-digest { margin:24px 0 0; }
      .curis-feedback-digest .card-body { display:flex; align-items:center; justify-content:space-between; gap:18px; }
      .curis-feedback-digest-copy { min-width:0; }
      .curis-feedback-digest-kicker { margin:0 0 5px; color:var(--text-tertiary,#777c86); font-size:10px; letter-spacing:.02em; }
      .curis-feedback-digest-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:14px; font-weight:600; }
      .curis-feedback-digest-note { margin:5px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.5; }
      .curis-feedback-digest-metrics { display:flex; flex-wrap:wrap; gap:6px 12px; margin-top:9px; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-feedback-digest-metrics span { white-space:nowrap; }
      .curis-feedback-digest-metrics b { font-weight:600; }
      .curis-feedback-digest-action { flex:0 0 auto; padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; white-space:nowrap; }
      .curis-feedback-digest-action:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-software-digest { margin:24px 0 0; }
      .curis-software-digest .card-body { display:flex; align-items:center; justify-content:space-between; gap:18px; }
      .curis-software-digest-copy { min-width:0; }
      .curis-software-digest-kicker { margin:0 0 5px; color:var(--text-tertiary,#777c86); font-size:10px; letter-spacing:.02em; }
      .curis-software-digest-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:14px; font-weight:600; }
      .curis-software-digest-note { margin:5px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.5; }
      .curis-software-digest-metrics { display:flex; flex-wrap:wrap; gap:6px 12px; margin-top:9px; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-software-digest-metrics span { white-space:nowrap; }
      .curis-software-digest-action { flex:0 0 auto; padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; white-space:nowrap; }
      .curis-software-digest-action:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-department-digest { margin:24px 0 0; }
      .curis-department-digest .card-body { display:flex; align-items:center; justify-content:space-between; gap:18px; }
      .curis-department-digest-copy { min-width:0; }
      .curis-department-digest-kicker { margin:0 0 5px; color:var(--text-tertiary,#777c86); font-size:10px; letter-spacing:.02em; }
      .curis-department-digest-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:14px; font-weight:600; }
      .curis-department-digest-note { margin:5px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.5; }
      .curis-department-digest-metrics { display:flex; flex-wrap:wrap; gap:6px 12px; margin-top:9px; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-department-digest-metrics span { white-space:nowrap; }
      .curis-department-digest-metrics b { font-weight:600; }
      .curis-department-digest-action { flex:0 0 auto; padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:11px; white-space:nowrap; }
      .curis-department-digest-action:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-finance-digest { margin:24px 0 0; }
      .curis-finance-digest .card-header { align-items:flex-start; }
      .curis-finance-digest-metrics { display:flex; flex-wrap:wrap; gap:6px 14px; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-finance-digest-metrics span { white-space:nowrap; }
      .curis-finance-digest-metrics b { font-weight:600; }
      .curis-finance-digest-note { margin:10px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.5; }
      .curis-finance-capacity-plan { grid-column:1 / -1; }
      .curis-finance-capacity-plan .plan-grid { display:flex; flex-wrap:wrap; gap:8px 18px; margin-top:10px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-finance-capacity-plan .plan-grid strong { color:var(--text-default-hover,#f4f5f7); font-weight:600; }
      .curis-finance-agent-performance { grid-column:1 / -1; }
      .curis-finance-agent-performance-list { display:grid; gap:8px; margin-top:10px; }
      .curis-finance-agent-performance-row { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:9px 0; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); font-size:11px; }
      .curis-finance-agent-performance-row span { color:var(--text-secondary,#a4a7af); }
      .curis-finance-agent-performance-row strong { color:var(--text-default-hover,#f4f5f7); font-weight:600; white-space:nowrap; }
      .curis-meeting-digest { margin:24px 0 0; }
      .curis-meeting-digest .card-header { align-items:flex-start; }
      .curis-meeting-digest-summary { margin:0; color:var(--text-default,#e2e3e7); font-size:12px; line-height:1.55; }
      .curis-meeting-digest-commitments { display:flex; flex-wrap:wrap; gap:6px 14px; margin-top:10px; color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-meeting-digest-commitments span { white-space:nowrap; }
      @media (max-width:620px) { .curis-meeting-digest .card-header { align-items:flex-start; flex-direction:column; } }
      .curis-runtime-decision-banner { display:flex; align-items:flex-start; justify-content:space-between; gap:14px; margin:0 0 16px; padding:13px 15px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:10px; }
      .curis-runtime-decision-copy { min-width:0; }
      .curis-runtime-decision-kicker { margin:0 0 4px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-runtime-decision-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:13px; font-weight:600; }
      .curis-runtime-decision-note { margin:5px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.5; }
      .curis-runtime-decision-action { flex:0 0 auto; padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font:inherit; font-size:11px; white-space:nowrap; }
      .curis-runtime-decision-blocked { opacity:.46; cursor:not-allowed !important; }
      @media (max-width:620px) { .curis-runtime-decision-banner { flex-direction:column; } }
      @media (max-width:620px) { .curis-feedback-digest .card-body { align-items:flex-start; flex-direction:column; } }
      @media (max-width:620px) { .curis-finance-digest .card-header { align-items:flex-start; flex-direction:column; } }
      .curis-decision-next { display:inline-flex; align-items:center; margin-top:12px; padding:8px 10px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:7px; cursor:pointer; font-size:11px; font-weight:600; }
      .curis-decision-next:hover { background:var(--brand-600,#f1f2f4); }
      .curis-option-commit { display:none; align-items:center; margin-top:10px; padding:6px 9px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:6px; cursor:pointer; font-size:10px; font-weight:600; }
      .option-card.selected .curis-option-commit { display:inline-flex; }
      .curis-option-commit:hover { background:var(--brand-600,#f1f2f4); }
      .curis-studio-assembly { display:flex; align-items:flex-start; justify-content:space-between; gap:14px; margin:0 0 12px; padding:10px 12px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; }
      .curis-studio-assembly-copy { min-width:0; }
      .curis-studio-assembly-title { margin:0; color:var(--text-default,#e2e3e7); font-size:11px; font-weight:600; }
      .curis-studio-assembly-note { margin:3px 0 0; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.4; }
      .curis-studio-assembly-list { display:flex; flex-wrap:wrap; justify-content:flex-end; gap:5px; }
      .curis-studio-chip { display:inline-flex; align-items:center; gap:5px; padding:4px 7px; color:var(--text-secondary,#a4a7af); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:999px; font-size:10px; }
      .curis-studio-chip button { padding:0; color:var(--text-tertiary,#777c86); background:transparent; border:0; cursor:pointer; font-size:12px; line-height:1; }
      .curis-studio-chip button:hover { color:var(--text-default-hover,#f4f5f7); }
      .curis-studio-submit { flex:0 0 auto; padding:7px 9px; color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border:0; border-radius:7px; cursor:pointer; font-size:10px; font-weight:600; white-space:nowrap; }
      .curis-studio-submit:hover:not(:disabled) { background:var(--brand-600,#f1f2f4); }
      .curis-studio-submit:disabled { opacity:.45; cursor:not-allowed; }
      .curis-studio-assembly.is-ready { border-color:var(--status-success,#a8c8b8); }
      .curis-studio-assembly.is-ready .curis-studio-assembly-note { color:var(--status-success,#a8c8b8); }
      .curis-workflow-shelf { grid-column:1 / -1; margin-top:10px; padding-top:10px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-workflow-shelf-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
      .curis-workflow-shelf-head strong { display:block; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-workflow-shelf-head span { display:block; margin-top:3px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-workflow-shelf-head em { color:var(--text-tertiary,#777c86); font-size:10px; font-style:normal; white-space:nowrap; }
      .curis-workflow-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:6px; margin-top:8px; }
      .curis-workflow-row { display:flex; align-items:center; justify-content:space-between; gap:8px; min-width:0; padding:8px 9px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; }
      .curis-workflow-row > div { min-width:0; flex:1 1 auto; }
      .curis-workflow-row strong { display:block; overflow:hidden; color:var(--text-default,#e2e3e7); font-size:10px; text-overflow:ellipsis; white-space:nowrap; }
      .curis-workflow-row span { display:block; margin-top:3px; overflow:hidden; color:var(--text-tertiary,#777c86); font-size:9px; text-overflow:ellipsis; white-space:nowrap; }
      .curis-workflow-row button { flex:0 0 auto; padding:5px 7px; color:var(--text-secondary,#a4a7af); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:6px; cursor:pointer; font:inherit; font-size:10px; }
      .curis-workflow-row button:hover { color:var(--text-default-hover,#f4f5f7); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-check-resolved { opacity:.58; }
      .curis-platform-guide { display:flex; align-items:center; justify-content:space-between; gap:16px; margin:0 0 16px; padding:14px 16px; background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:10px; }
      .curis-platform-guide-copy { min-width:0; }
      .curis-platform-guide-kicker { margin:0 0 4px; color:var(--text-tertiary,#777c86); font-size:10px; letter-spacing:.03em; }
      .curis-platform-guide-title { margin:0; color:var(--text-default-hover,#f4f5f7); font-size:13px; font-weight:600; }
      .curis-platform-guide-note { margin:4px 0 0; color:var(--text-secondary,#a4a7af); font-size:10px; line-height:1.45; }
      .curis-platform-guide-state { display:inline-flex; align-items:center; gap:6px; margin-top:7px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-platform-guide-state::before { content:""; width:6px; height:6px; border-radius:50%; background:var(--status-warning,#d6c49c); }
      .curis-platform-guide.is-ready .curis-platform-guide-state { color:var(--status-success,#a8c8b8); }
      .curis-platform-guide.is-ready .curis-platform-guide-state::before { background:var(--status-success,#a8c8b8); }
      .curis-platform-guide-action { flex:0 0 auto; padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:10px; white-space:nowrap; }
      .curis-platform-guide-action:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-guide-dialog { width:min(620px,calc(100vw - 32px)); max-height:min(720px,calc(100vh - 32px)); padding:0; color:var(--text-default,#e2e3e7); background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:14px; box-shadow:0 22px 80px rgba(0,0,0,.42); }
      .curis-guide-dialog::backdrop { background:rgba(0,0,0,.52); }
      .curis-guide-head { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; padding:18px 20px; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-guide-head h2 { margin:0; font-size:16px; font-weight:600; }
      .curis-guide-head p { margin:5px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.45; }
      .curis-guide-close { padding:0 4px; color:var(--text-secondary,#a4a7af); background:transparent; border:0; cursor:pointer; font-size:18px; line-height:1; }
      .curis-guide-body { padding:18px 20px; overflow:auto; }
      .curis-guide-step { display:grid; grid-template-columns:26px 1fr; gap:10px; padding:12px 0; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-guide-step:last-child { border-bottom:0; }
      .curis-guide-step-index { display:grid; place-items:center; width:22px; height:22px; color:var(--text-secondary,#a4a7af); background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-radius:50%; font-size:10px; }
      .curis-guide-step strong { display:block; color:var(--text-default-hover,#f4f5f7); font-size:12px; font-weight:600; }
      .curis-guide-step p { margin:4px 0 7px; color:var(--text-secondary,#a4a7af); font-size:10px; line-height:1.5; }
      .curis-guide-check { display:flex; align-items:center; gap:7px; color:var(--text-tertiary,#777c86); font-size:10px; cursor:pointer; }
      .curis-guide-check input { accent-color:var(--primary,#d9dbe1); }
      .curis-guide-foot { display:flex; align-items:center; justify-content:space-between; gap:10px; padding:14px 20px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-guide-foot-note { color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-guide-foot-actions { display:flex; gap:7px; }
      .curis-guide-foot-actions button { padding:7px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:10px; }
      .curis-guide-foot-actions .primary { color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-color:var(--primary,#d9dbe1); font-weight:600; }
      .curis-studio-assembly-actions { display:flex; align-items:center; gap:7px; flex:0 0 auto; }
      .curis-studio-import { padding:7px 9px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:10px; white-space:nowrap; }
      .curis-studio-import:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); }
      .curis-finance-detail { margin-top:16px; }
      .curis-finance-detail-head { display:flex; align-items:flex-start; justify-content:space-between; gap:12px; }
      .curis-finance-detail-head button { flex:0 0 auto; padding:7px 9px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; cursor:pointer; font-size:10px; }
      .curis-cost-item { display:flex; align-items:center; justify-content:space-between; gap:10px; padding:10px 0; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-cost-item strong { display:block; color:var(--text-default,#e2e3e7); font-size:11px; font-weight:600; }
      .curis-cost-item span { display:block; margin-top:3px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-cost-item b { color:var(--text-default-hover,#f4f5f7); font-size:12px; font-weight:600; white-space:nowrap; }
      .curis-finance-total { display:flex; align-items:center; justify-content:space-between; margin-top:8px; padding-top:11px; border-top:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); color:var(--text-secondary,#a4a7af); font-size:11px; }
      .curis-finance-total strong { color:var(--text-default-hover,#f4f5f7); font-size:15px; }
      .curis-value-list { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }
      .curis-value-list > div { padding:10px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:7px; }
      .curis-value-list span,.curis-value-list small { display:block; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-value-list strong { display:block; margin:4px 0; color:var(--text-default-hover,#f4f5f7); font-size:15px; font-weight:600; }
      .curis-value-breakdown { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; margin-top:10px; }
      .curis-value-breakdown > div { padding:8px; border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-value-breakdown span,.curis-value-breakdown small { display:block; color:var(--text-tertiary,#777c86); font-size:9px; }
      .curis-value-breakdown strong { display:block; margin-top:3px; color:var(--text-default,#e2e3e7); font-size:12px; font-weight:600; }
      .curis-finance-note { margin:12px 0 0; color:var(--text-tertiary,#777c86); font-size:10px; line-height:1.45; }
      @media (max-width:620px) { .curis-value-list,.curis-value-breakdown { grid-template-columns:1fr; } }
      .curis-stage-dialog { width:min(520px,calc(100vw - 32px)); padding:0; color:var(--text-default,#e2e3e7); background:var(--bg-base-secondary,#202226); border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:12px; box-shadow:0 18px 60px rgba(0,0,0,.38); }
      .curis-stage-dialog::backdrop { background:rgba(0,0,0,.48); }
      .curis-stage-dialog-head { display:flex; align-items:flex-start; justify-content:space-between; gap:16px; padding:18px 20px; border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); }
      .curis-stage-dialog-head h2 { margin:0; font-size:16px; font-weight:650; }
      .curis-stage-dialog-head p { margin:4px 0 0; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-stage-dialog-close { border:0; padding:0 4px; color:var(--text-secondary,#a4a7af); background:transparent; cursor:pointer; font-size:20px; line-height:1; }
      .curis-stage-dialog-body { display:grid; gap:14px; padding:18px 20px; }
      .curis-stage-dialog-meta { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:8px; }
      .curis-stage-dialog-meta div,.curis-stage-dialog-section { padding:10px; background:var(--bg-base-default,#191a1d); border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1)); border-radius:8px; }
      .curis-stage-dialog-meta span,.curis-stage-dialog-section span { display:block; color:var(--text-tertiary,#777c86); font-size:10px; }
      .curis-stage-dialog-meta strong { display:block; margin-top:4px; color:var(--text-default,#e2e3e7); font-size:11px; }
      .curis-stage-dialog-section p { margin:6px 0 0; color:var(--text-secondary,#a4a7af); font-size:11px; line-height:1.55; }
      .curis-stage-dialog-actions { display:flex; justify-content:flex-end; gap:8px; padding:0 20px 18px; }
      .curis-stage-dialog-actions button { padding:8px 10px; color:var(--text-default,#e2e3e7); background:transparent; border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16)); border-radius:7px; font:inherit; font-size:10px; cursor:pointer; }
      .curis-stage-dialog-actions .primary { color:var(--primary-foreground,#17181a); background:var(--primary,#d9dbe1); border-color:var(--primary,#d9dbe1); font-weight:600; }
      .loop .stage,.flow .stage { cursor:pointer; }
      .loop .stage:focus-visible,.flow .stage:focus-visible { outline:2px solid var(--ring,#aab6ff); outline-offset:3px; }
      .canvas-area { --studio-zoom:1; transform-origin:top left; transition:transform .18s ease,grid-template-columns .18s ease; }
      .canvas-area[style*="--studio-zoom"] { transform:scale(var(--studio-zoom)); }
      .canvas-area.is-compact .node-card { padding:8px !important; }
      .canvas-area.is-compact .node-card p { max-height:34px; overflow:hidden; }
      body[data-curis-neutral] .loop { grid-template-columns:repeat(9,minmax(0,1fr)) !important; }
      @media (max-width:1020px) { body[data-curis-neutral] .loop { grid-template-columns:repeat(5,minmax(0,1fr)) !important; } }
      @media (max-width:720px) { body[data-curis-neutral] .loop { grid-template-columns:repeat(2,minmax(0,1fr)) !important; } }
      @media (max-width:900px) { .curis-workflow-list { grid-template-columns:1fr; } }
      @media (max-width:760px) { .curis-studio-assembly { flex-direction:column; } .curis-studio-assembly-list { justify-content:flex-start; } }
      @media (max-width:620px) { .curis-platform-guide { align-items:flex-start; flex-direction:column; } .curis-guide-foot { align-items:flex-start; flex-direction:column; } }
      .curis-day-route { cursor:pointer; transition:background .18s ease,border-color .18s ease; }
      .curis-day-route:hover { background:var(--bg-overlay-l2,rgba(224,226,242,.06)); border-radius:8px; }
      .curis-day-route:focus-visible { outline:2px solid var(--ring,#aab6ff); outline-offset:3px; border-radius:8px; }
      .curis-extra-nav-label { margin:0 10px 5px; color:var(--text-tertiary,#777c86); font-size:10px; }
      .stage-paused { background:var(--status-error-surface,rgba(184,117,125,.14)) !important; color:var(--status-error,#b8757d) !important; border-color:var(--status-error,#b8757d) !important; }
      @media (max-width:620px) { .curis-desk-opening { align-items:flex-start; flex-direction:column; } }
    `;
    document.head.appendChild(style);
  }

  function translateVisibleText() {
    const translate = value => I18N.reduce((text, [from, to]) => text.split(from).join(to), value);
    const translatedTitle = translate(document.title);
    if (translatedTitle !== document.title) document.title = translatedTitle;
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const parent = walker.currentNode.parentElement;
      if (parent && !['SCRIPT', 'STYLE'].includes(parent.tagName)) nodes.push(walker.currentNode);
    }
    nodes.forEach(node => {
      const value = translate(node.nodeValue);
      if (value !== node.nodeValue) node.nodeValue = value;
    });
    document.querySelectorAll('[aria-label], [title], [placeholder]').forEach(node => {
      ['aria-label', 'title', 'placeholder'].forEach(attribute => {
        const value = node.getAttribute(attribute);
        const translated = value && translate(value);
        if (translated && translated !== value) node.setAttribute(attribute, translated);
      });
    });
  }

  function watchDynamicText() {
    const observer = new MutationObserver(records => {
      if (records.some(record => record.type === 'childList' || record.type === 'characterData')) translateVisibleText();
    });
    observer.observe(document.body, { childList: true, subtree: true, characterData: true });
  }

  function renderCompanion() {
    if (document.getElementById('curis-companion')) return;
    const page = window.location.pathname.split('/').pop() || 'ceo-desk.html';
    const state = readState();
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    const assistantStage = syncAssistantRuntime(state, page);
    const attention = assistantAttention(state);
    const root = document.createElement('div');
    root.id = 'curis-companion';
    const companionPosition = page === 'workspace-studio.html' ? ' curis-companion-studio' : ['founding-flow.html', 'decision-room.html'].includes(page) ? ' curis-companion-footer' : '';
    root.className = `curis-companion${companionPosition}`;
    root.innerHTML = `
      <div class="curis-companion-panel" role="dialog" aria-label="CEO 助理">
        <div class="curis-companion-head"><strong>Curis · CEO 首席助理</strong><button class="curis-companion-close" type="button" aria-label="关闭">×</button></div>
        <div class="curis-companion-body">
          <p class="curis-companion-greeting"></p>
          <p class="curis-companion-context">我会把需要你知道的事整理好，把可以交给团队的事继续推进。</p>
          <p class="curis-companion-room">当前所在：${ROOM_NAMES[page] || '公司空间'}</p>
          <div class="curis-assistant-runtime" aria-label="CEO 助理运行状态">
            <div class="curis-assistant-runtime-head"><span class="curis-assistant-runtime-title">CEO 助理运行状态</span><span class="curis-assistant-runtime-state"></span></div>
            <div class="curis-assistant-runtime-steps" aria-hidden="true"><span class="curis-assistant-runtime-step"></span><span class="curis-assistant-runtime-step"></span><span class="curis-assistant-runtime-step"></span><span class="curis-assistant-runtime-step"></span><span class="curis-assistant-runtime-step"></span></div>
            <span class="curis-assistant-runtime-note" aria-live="polite"></span>
          </div>
          <button class="curis-companion-next" type="button" data-curis-handled="true"></button>
          <form class="curis-companion-form"><input name="message" autocomplete="off" placeholder="告诉我下一步要做什么" /><button type="submit">交给我</button></form>
          <div class="curis-theme-row"><span>界面主题</span><select id="curis-theme" aria-label="界面主题"><option value="system">跟随系统</option><option value="light">浅色</option><option value="dark">深色</option></select></div>
        </div>
      </div>
      <button class="curis-companion-entry" type="button" aria-label="打开 CEO 助理">
        <span class="curis-companion-avatar">C</span><span class="curis-companion-copy"><span class="curis-companion-name">Curis · CEO 首席助理</span><span class="curis-companion-status"></span></span>
      </button>`;
    document.body.appendChild(root);
    root.querySelector('.curis-companion-greeting').textContent = state.lastAssistantMessage || PAGE_BRIEFS[page] || '我在这里，随时帮你整理信息、推动执行和准备决策。';
    root.classList.toggle('has-attention', Boolean(attention));
    const runtimeNote = root.querySelector('.curis-assistant-runtime-note');
    const nextButton = root.querySelector('.curis-companion-next');
    paintAssistantRuntime(root, assistantStage, department);
    if (attention) root.querySelector('.curis-companion-status').textContent = attention;
    const showHandoff = handoff => {
      if (!handoff?.route || !handoff?.label) return;
      runtimeNote.textContent = `已委派给${handoff.label}；我会在结果回来后向你汇报。`;
      nextButton.textContent = `进入${handoff.label} →`;
      nextButton.classList.add('is-visible');
      nextButton.onclick = () => { window.location.href = handoff.route; };
    };
    showHandoff(state.lastAssistantHandoff);
    const refresh = nextState => {
      const latest = nextState || readState();
      const latestStage = syncAssistantRuntime(latest, page);
      const latestAttention = assistantAttention(latest);
      root.querySelector('.curis-companion-greeting').textContent = latest.lastAssistantMessage || PAGE_BRIEFS[page] || '我在这里，随时帮你整理信息、推动执行和准备决策。';
      root.classList.toggle('has-attention', Boolean(latestAttention));
      paintAssistantRuntime(root, latestStage, latest.departmentDraft);
      if (latestAttention) root.querySelector('.curis-companion-status').textContent = latestAttention;
      nextButton.classList.remove('is-visible');
      nextButton.onclick = null;
      showHandoff(latest.lastAssistantHandoff);
    };
    window.addEventListener('curis-state-changed', event => refresh(event.detail));
    const themeSelect = root.querySelector('#curis-theme');
    themeSelect.value = state.theme || 'system';
    const open = () => root.classList.add('is-open');
    const close = () => root.classList.remove('is-open');
    root.querySelector('.curis-companion-entry').addEventListener('click', open);
    root.querySelector('.curis-companion-close').addEventListener('click', close);
    themeSelect.addEventListener('change', event => {
      const mode = applyTheme(event.target.value);
      writeState({ theme: mode });
      showToast(`已切换为${mode === 'system' ? '跟随系统' : mode === 'light' ? '浅色' : '深色'}主题`);
    });
    root.querySelector('form').addEventListener('submit', event => {
      event.preventDefault();
      const input = event.currentTarget.elements.message;
      const message = input.value.trim();
      if (!message) return;
      const matched = ASSISTANT_ROUTES.find(item => item.words.some(word => message.includes(word)));
      const handoff = matched ? { label: matched.label, route: matched.route, message } : null;
      writeState({ lastAssistantMessage: matched ? `收到。我先把“${message}”交给${matched.label}，并替你守住上下文。` : `收到。我会先把“${message}”整理成下一步，并在有结果时回来汇报。`, lastAssistantHandoff: handoff });
      root.querySelector('.curis-companion-greeting').textContent = readState().lastAssistantMessage;
      if (handoff) showHandoff(handoff);
      else {
        runtimeNote.textContent = '已记下这件事；我会先整理，再在需要你决定时回来。';
        nextButton.classList.remove('is-visible');
      }
      input.value = '';
      showToast(matched ? `已委派给${matched.label}` : '已交给 CEO 助理，后续会在这里回报');
    });
  }

  function initDeskOperatingDay() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-day-route')) return;
    const routes = ['#', 'decision-room.html', 'meeting.html', 'workspace-runtime-software.html', 'ai-organization.html', 'operating.html'];
    const timelineItems = [...document.querySelectorAll('.timeline-item')];
    const state = readState();
    const decision = state.lastDecision;
    const xhsFeedback = state.latestXhsFeedback;
    const shortVideoFeedback = state.latestExternalFeedback;
    const feedback = [xhsFeedback ? { ...xhsFeedback, platform: '小红书' } : null, shortVideoFeedback ? { ...shortVideoFeedback, platform: '抖音 / TikTok' } : null]
      .filter(Boolean).sort((a, b) => String(b.at || b.time || '').localeCompare(String(a.at || a.time || '')))[0];
    const softwareAcceptance = state.softwareAcceptance;
    const departmentResult = state.departmentResult;
    const scheduledRun = state.lastScheduledRun;
    const scheduledRunAt = String(scheduledRun?.finishedAt || scheduledRun?.at || '');
    const feedbackAt = String(feedback?.at || feedback?.time || '');
    const scheduledRunIsLatest = Boolean(scheduledRun && scheduledRunAt && scheduledRunAt >= feedbackAt);
    if (!state.companyCreatedAt) {
      timelineItems.forEach((item, index) => {
        item.classList.remove('active', 'past');
        item.classList.add('curis-day-empty');
        const title = item.querySelector('.timeline-title');
        const description = item.querySelector('.timeline-desc');
        if (title) title.textContent = index === 0 ? '等待公司启动' : '创建公司后开始记录';
        if (description) description.textContent = index === 0 ? '完成第一间 CEO 办公室的创建后，助理会从这里开始记录经营日。' : '这一步会在公司启动、真实运行或 CEO 决策发生后出现。';
      });
      routes.splice(1, routes.length - 1, ...Array(routes.length - 1).fill(null));
      routes[0] = 'founding-flow.html';
    }
    if (departmentResult) routes[4] = 'workspace-runtime-department.html';
    if (state.operatingDayClosedAt && timelineItems[5]) {
      timelineItems[5].classList.remove('active');
      timelineItems[5].classList.add('past');
      timelineItems[5].querySelector('.timeline-title').textContent = '日终收束：已归档';
      timelineItems[5].querySelector('.timeline-desc').textContent = '今日经营记录已生成，未解决事项与明日承接已经交给 CEO 助理。';
      [...document.querySelectorAll('.page-meta > span')]
        .find(item => item.textContent.includes('经营日状态'))
        ?.querySelector('strong')
        ?.replaceChildren(document.createTextNode('已归档'));
    }
    if (decision && timelineItems[1]) {
      const decisionLabels = { approve: '已批准', defer: '已延后', revise: '已退回修改', reject: '已拒绝' };
      timelineItems[1].classList.remove('active');
      timelineItems[1].classList.add('past');
      timelineItems[1].querySelector('.timeline-title').textContent = `预算决策：${decisionLabels[decision.choice] || '已记录'}`;
      timelineItems[1].querySelector('.timeline-desc').textContent = decision.choice === 'approve'
        ? 'CEO 已批准，内容办公室正在按 Runtime v1.1 执行；下一检查点会由 CEO 助理提前准备。'
        : decision.choice === 'defer'
          ? 'CEO 已延后 3 天，CEO 助理正在守住检查点并准备下一次决策包。'
          : decision.choice === 'revise'
            ? 'CEO 已要求修改，工作空间搭建现场会补齐缺口后重新提交。'
            : 'CEO 已拒绝本次发布，当前 Runtime v1.0 继续运行。';
    }
    if (feedback && timelineItems[4]) {
      timelineItems[4].classList.remove('active');
      timelineItems[4].classList.add('past');
      timelineItems[4].querySelector('.timeline-title').textContent = '外部结果已回流';
      timelineItems[4].querySelector('.timeline-desc').textContent = feedback.platform === '小红书'
        ? `小红书运营办公室带回：阅读 ${feedback.reads || 0} · 收藏 ${feedback.saves || 0} · 新增粉丝 ${feedback.follows || 0}，已进入下一次复盘。`
        : `内容办公室带回：播放 ${feedback.plays || 0} · 新增粉丝 ${feedback.follows || 0} · 成交 ${feedback.orders || 0}，已进入下一次复盘。`;
    }
    if (departmentResult && timelineItems[4]) {
      timelineItems[4].classList.remove('active');
      timelineItems[4].classList.add('past');
      timelineItems[4].querySelector('.timeline-title').textContent = '部门责任结果已回报';
      timelineItems[4].querySelector('.timeline-desc').textContent = `${state.departmentDraft?.name || '部门办公室'}：${departmentResult.status}，CEO 助理正在准备继续、调整或暂停判断。`;
    }
    if (scheduledRunIsLatest && timelineItems[4]) {
      const waiting = ['queued', 'waiting_ceo', 'acknowledged'].includes(scheduledRun.status) || scheduledRun.requiresCEO;
      timelineItems[4].classList.remove('active', 'past');
      timelineItems[4].classList.add(waiting ? 'active' : 'past');
      timelineItems[4].querySelector('.timeline-title').textContent = `自动运行：${String(scheduledRun.title || '任务已运行').replace(/ · (已完成|需 CEO 处理)$/, '')}`;
      timelineItems[4].querySelector('.timeline-desc').textContent = waiting
        ? `${scheduledRun.owner || 'AI 员工'} ${scheduledRun.status === 'queued' ? '正在等待能力释放' : scheduledRun.status === 'acknowledged' ? '已被 CEO 打开，等待完成处理' : '已运行到需要 CEO 处理的节点'}：${scheduledRun.output || '请查看运行记录'}。下一步已交给 CEO 助理。`
        : `${scheduledRun.owner || 'AI 员工'} ${scheduledRun.status === 'resolved' ? '已由 CEO 处理并进入复盘' : '已完成'}：${scheduledRun.resolutionNote || scheduledRun.output || '任务产出已写回公司日历'}。下一阶段会继续沿着${scheduledRun.route || '业务空间'}运行。`;
      routes[4] = scheduledRun.status === 'queued' ? 'ai-organization.html' : scheduledRun.route || 'calendar.html';
    }
    if (softwareAcceptance && timelineItems[3]) {
      timelineItems[3].classList.remove('active');
      timelineItems[3].classList.add(softwareAcceptance.choice === 'accept' ? 'past' : 'active');
      timelineItems[3].querySelector('.timeline-title').textContent = softwareAcceptance.choice === 'accept' ? 'Curis v0.2 已验收' : 'Curis v0.2 等待 CEO 验收';
      timelineItems[3].querySelector('.timeline-desc').textContent = softwareAcceptance.choice === 'accept'
        ? 'CEO 已通过首轮真实使用，研发办公室开始准备下一次软件增量。'
        : '研发办公室已提交新的验收包，CEO 反馈会决定退回修改还是进入下一周期。';
    }
    timelineItems.forEach((item, index) => {
      const route = routes[index];
      if (!route) return;
      item.classList.add('curis-day-route');
      item.setAttribute('role', 'link');
      item.setAttribute('tabindex', '0');
      item.setAttribute('aria-label', `${item.querySelector('.timeline-time')?.textContent.trim() || ''} ${item.querySelector('.timeline-title')?.textContent.trim() || ''}`);
      const navigate = () => {
        if (route === '#') return showToast('早报已完成，CEO 助理正在关注下一项变化');
        window.location.href = route;
      };
      item.addEventListener('click', navigate);
      item.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); navigate(); }
      });
    });
  }

  function persistFoundingResult() {
    if (!window.launchCompany || window.launchCompany.__curisWrapped) return;
    const original = window.launchCompany;
    const wrapped = function () {
      const name = document.getElementById('company-name')?.value?.trim();
      const business = document.querySelector('.bet-option.selected h4')?.textContent?.trim();
      const selectedTemplate = readState().selectedTemplate;
      const template = FOUNDING_TEMPLATES[selectedTemplate];
      const values = document.getElementById('company-values')?.value?.split(/[,，]/).map(value => value.trim()).filter(Boolean) || [];
      const members = [...document.querySelectorAll('.team-card.assigned h4')].map(node => node.textContent.trim()).filter(Boolean).filter(name => name !== 'Curis');
      writeState({
        companyName: name || 'Curis',
        firstBusiness: template?.label || business || '第一个业务',
        companyCharter: document.getElementById('company-charter')?.value?.trim() || '',
        companyLegal: document.getElementById('company-legal')?.value || '',
        companyValues: values,
        firstBusinessOpportunity: template?.opportunity || document.getElementById('business-opportunity')?.value?.trim() || '',
        firstBusinessOutcome: template?.outcome || document.getElementById('business-outcome')?.value?.trim() || '',
        firstBusinessTimebox: document.getElementById('business-timebox')?.value || '',
        externalFeedbackPath: template?.feedback || document.getElementById('business-evidence')?.value || '',
        aiTeam: ['CEO 助理', ...members.filter(name => name !== 'CEO 助理')],
        companyCreatedAt: new Date().toISOString(),
        companyPhase: 'operating',
        firstOperatingDay: true,
        lastAssistantMessage: '公司已经启动。我会从今天的经营状态开始，替你守住决策、执行和结果回报。'
      });
      return original.apply(this, arguments);
    };
    wrapped.__curisWrapped = true;
    window.launchCompany = wrapped;
  }

  function applyCompanyState() {
    const state = readState();
    if (!state.companyName) return;
    document.querySelectorAll('strong, span, div, h1, h2, h3, p').forEach(node => {
      if (node.children.length === 0 && /Curis Labs|Curis AI 有限公司/.test(node.textContent)) {
        node.textContent = node.textContent.replace(/Curis Labs|Curis AI 有限公司/g, state.companyName || 'Curis');
      }
    });
  }

  function applyTheme(mode = readState().theme || 'system') {
    const root = document.documentElement;
    const resolved = ['dark', 'light', 'system'].includes(mode) ? mode : 'system';
    const systemDark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)').matches : true;
    root.dataset.theme = resolved;
    root.classList.toggle('dark', resolved === 'dark' || (resolved === 'system' && systemDark));
    const themeLabel = { system: '跟随系统', light: '浅色', dark: '深色' }[resolved];
    document.querySelectorAll('[data-curis-theme-label]').forEach(node => { node.textContent = `主题：${themeLabel}`; });
    return resolved;
  }

  function focusBusiness(id) {
    const card = document.querySelector(`.biz-card[data-id="${id}"], .workspace-card[data-business="${id}"]`);
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.add('curis-focus');
    window.setTimeout(() => card.classList.remove('curis-focus'), 1400);
  }

  function capacityMatchesBusiness(capacity, businessTitle, platform) {
    if (!capacity) return false;
    if (capacity.businessTitle && businessTitle) return capacity.businessTitle === businessTitle;
    if (capacity.platform && platform) return capacity.platform === platform;
    return true;
  }

  function initBusinessMap() {
    if (!window.location.pathname.endsWith('business.html') || document.querySelector('.curis-business-map')) return;
    const anchor = document.querySelector('.filter-bar');
    if (!anchor) return;
    const map = document.createElement('section');
    map.className = 'curis-business-map';
    map.setAttribute('aria-label', '公司业务版图');
    map.innerHTML = `
      <div class="curis-map-header">
        <div><p class="curis-map-kicker">公司业务版图</p><h2 class="curis-map-title">现在，公司靠哪些业务创造价值？</h2></div>
        <span class="curis-map-meta">3 条业务 · 2 条运行中 · 1 条实验</span>
      </div>
      <div class="curis-map-company"><strong>Curis</strong><span>公司意图 · 持续创造可验证结果</span></div>
      <div class="curis-map-stem" aria-hidden="true"></div>
      <div class="curis-map-nodes">
        <button class="curis-map-node" type="button" data-business-target="software-dev"><strong>软件开发</strong><span>Curis 自研</span><em>研发办公室</em></button>
        <button class="curis-map-node" type="button" data-business-target="content-growth"><strong>小红书运营</strong><span>品牌与获客</span><em>小红书运营办公室</em></button>
        <button class="curis-map-node" type="button" data-business-target="short-video"><strong>抖音 / TikTok 运营</strong><span>短视频实验</span><em>抖音 / TikTok 运营办公室</em></button>
      </div>
      <div class="curis-map-relations" aria-label="业务关系">
        <span><b>产品内生</b> 软件开发 → Curis 产品</span>
        <span><b>增长供给</b> 抖音 / TikTok → 小红书与品牌增长</span>
      </div>`;
    const state = readState();
    if (!state.companyCreatedAt) {
      map.querySelector('.curis-map-title').textContent = '公司还没有业务版图';
      map.querySelector('.curis-map-meta').textContent = '完成公司创建后，业务会以办公室的方式出现在这里';
      map.querySelector('.curis-map-company strong').textContent = '等待公司成立';
      map.querySelector('.curis-map-company span').textContent = '先说出你想解决的问题，再建立第一间办公室';
      map.querySelector('.curis-map-nodes').innerHTML = '<button type="button" class="curis-map-node curis-map-empty"><strong>创建第一间业务</strong><span>软件开发、小红书或抖音 / TikTok</span><em>开始创建公司 →</em></button>';
      map.querySelector('.curis-map-relations').innerHTML = '<span><b>尚未建立</b> 公司成立后才会形成业务关系</span>';
      anchor.parentNode.insertBefore(map, anchor);
      map.querySelector('.curis-map-empty')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
      return;
    }
    const portfolioCount = state.departmentDraft?.name && state.departmentCommitment?.name ? 4 : 3;
    const decision = state.lastDecision;
    const xhsFeedback = state.latestXhsFeedback;
    const shortVideoFeedback = state.latestExternalFeedback;
    const feedback = [xhsFeedback ? { ...xhsFeedback, platform: '小红书' } : null, shortVideoFeedback ? { ...shortVideoFeedback, platform: '抖音 / TikTok' } : null]
      .filter(Boolean).sort((a, b) => String(b.at || b.time || '').localeCompare(String(a.at || a.time || '')))[0];
    const capacity = state.capacityDecision;
    const softwareAcceptance = state.softwareAcceptance;
    const feedbackHistory = [
      ...(Array.isArray(state.xhsFeedbackHistory) ? state.xhsFeedbackHistory : (xhsFeedback ? [xhsFeedback] : [])),
      ...(Array.isArray(state.externalFeedbackHistory) ? state.externalFeedbackHistory : (shortVideoFeedback ? [shortVideoFeedback] : []))
    ];
    const mapMeta = map.querySelector('.curis-map-meta');
    const shortVideoNode = map.querySelector('[data-business-target="short-video"]');
    const xhsNode = map.querySelector('[data-business-target="content-growth"]');
    if (decision?.choice === 'approve') {
      mapMeta.textContent = `${portfolioCount} 条业务 · 抖音 / TikTok 运营正在执行 · 首周检查点进行中`;
      shortVideoNode?.querySelector('em').replaceChildren(document.createTextNode('Runtime v1.1 执行中'));
    }
    if (feedback) {
      mapMeta.textContent = `${portfolioCount} 条业务 · ${feedback.platform}最新结果已回流 · ${feedbackHistory.length} 条记录`;
      const targetNode = feedback.platform === '小红书' ? xhsNode : shortVideoNode;
      targetNode?.querySelector('em').replaceChildren(document.createTextNode('真实结果已回流'));
    }
    const decisionBusiness = state.businessDecision?.businessTitle || (state.businessDecision?.platform === '小红书' ? '小红书运营' : state.businessDecision?.platform === '抖音 / TikTok' ? '抖音 / TikTok 运营' : '');
    const scaleApproved = (state.businessDecision?.choice === 'scale' || state.businessDecision?.label === '扩大业务')
      && (capacity?.choice === 'approve' || capacity?.label === '确认扩容配置')
      && capacityMatchesBusiness(capacity, decisionBusiness, state.businessDecision?.platform);
    if (scaleApproved) {
      mapMeta.textContent = feedback
        ? `${portfolioCount} 条业务 · 最新结果已回流 · 扩大业务已批准`
        : `${portfolioCount} 条业务 · 扩大业务已批准 · 新容量运行中`;
      (feedback?.platform === '小红书' ? xhsNode : shortVideoNode)?.querySelector('em').replaceChildren(document.createTextNode('新容量运行中'));
    }
    if (softwareAcceptance?.choice === 'accept') {
      const softwareNode = map.querySelector('[data-business-target="software-dev"]');
      softwareNode?.querySelector('em').replaceChildren(document.createTextNode('Curis v0.2 已验收'));
    }
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    if (department?.name && commitment?.name) {
      const node = document.createElement('button');
      node.className = 'curis-map-node';
      node.type = 'button';
      node.dataset.businessTarget = 'department-commitment';
      const statusLabel = commitment.status === 'paused'
        ? '已暂停'
        : state.departmentResult?.status || commitment.status === 'pending_revision'
          ? (state.departmentResult?.status || '待调整')
          : '运行中';
      node.innerHTML = '<strong></strong><span></span><em></em>';
      node.querySelector('strong').textContent = commitment.name;
      node.querySelector('span').textContent = department.name;
      node.querySelector('em').textContent = statusLabel;
      map.querySelector('.curis-map-nodes')?.appendChild(node);
      mapMeta.textContent = `4 条业务 · ${department.name} 已纳入业务版图 · ${statusLabel}`;
      const portfolio = document.querySelector('#portfolioGrid');
      if (portfolio && !portfolio.querySelector('.curis-dynamic-business-card')) {
        const card = document.createElement('article');
        const paused = commitment.status === 'paused';
        const result = state.departmentResult;
        card.className = 'biz-card curis-dynamic-business-card';
        card.dataset.stage = paused ? 'paused' : 'operating';
        card.dataset.id = 'department-commitment';
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `查看 ${commitment.name} 详情`);
      card.innerHTML = `<div class="biz-card-header"><div class="biz-card-top"><div><h2 class="biz-name"></h2><p class="biz-target"></p></div><span class="stage-pill ${paused ? 'stage-paused' : 'stage-operating'}">${paused ? '已暂停' : '运行中'}</span></div><div class="health-row"><div class="health-item health-ontrack"><div class="health-label">价值健康</div><div class="health-value"><span class="health-dot"></span>${result?.status === '已验证价值' ? '已验证' : '待补充'}</div></div><div class="health-item health-attention"><div class="health-label">执行健康</div><div class="health-value"><span class="health-dot"></span>${paused ? '已暂停' : '跟踪中'}</div></div></div></div><div class="biz-card-body"><div class="biz-section"><div class="biz-section-title">业务结果</div><p class="biz-outcome"></p></div><div class="biz-section"><div class="biz-section-title">外部结果</div><div class="evidence-list"><div class="evidence-item"><span class="evidence-name">状态</span><span class="evidence-value"></span></div><div class="evidence-item"><span class="evidence-name">回报记录</span><span class="evidence-value">${Array.isArray(state.departmentResultHistory) ? state.departmentResultHistory.length : result ? 1 : 0}</span></div></div></div><div class="biz-section"><div class="biz-section-title">下一检查点</div><div class="checkpoint"><span>${paused ? '等待重启判断' : '下一次 CEO 回报'}</span><span class="checkpoint-time">待安排</span></div></div></div><div class="biz-card-footer"><button class="btn btn-primary btn-sm" type="button" data-curis-handled="true">进入工作空间</button></div>`;
        card.querySelector('.biz-name').textContent = commitment.name;
        card.querySelector('.biz-target').textContent = department.name;
        card.querySelector('.biz-outcome').textContent = commitment.outcome || '等待结果定义';
        card.querySelector('.evidence-value').textContent = result?.status || '待补充';
        portfolio.appendChild(card);
        const route = () => { window.location.href = paused ? 'operating.html' : 'workspace-runtime-department.html'; };
        card.addEventListener('click', event => { if (event.target.closest('button')) return route(); route(); });
        card.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); route(); } });
        [...document.querySelectorAll('.summary-item')].forEach(item => {
          const label = item.querySelector('.summary-label')?.textContent.trim();
          const value = item.querySelector('.summary-value');
          if (label === '总业务数' && value) value.textContent = String(portfolioCount);
          if (label === '运行中' && value && !paused) value.textContent = String(Number(value.textContent || 0) + 1);
          if (label === '暂停' && value && paused) value.textContent = String(Number(value.textContent || 0) + 1);
        });
      }
    }
    anchor.parentNode.insertBefore(map, anchor);
    map.querySelectorAll('[data-business-target]').forEach(node => node.addEventListener('click', () => {
      const target = node.dataset.businessTarget;
      if (target === 'software-dev') return window.location.href = 'workspace-runtime-software.html';
      if (target === 'content-growth') return window.location.href = 'workspace-runtime-xhs.html';
      if (target === 'short-video') return window.location.href = 'workspace-runtime-shortvideo.html';
      if (target === 'department-commitment') return window.location.href = commitment?.status === 'active' ? 'workspace-runtime-department.html' : commitment?.status === 'paused' ? 'operating.html' : 'workspace-studio.html';
      focusBusiness(target);
    }));
  }

  function initBusinessOutcomeDecision() {
    if (!window.location.pathname.endsWith('business.html') || document.querySelector('.curis-business-decision')) return;
    if (!readState().companyCreatedAt) return;
    const map = document.querySelector('.curis-business-map');
    if (!map) return;
    const state = readState();
    const xhsFeedback = state.latestXhsFeedback;
    const shortVideoFeedback = state.latestExternalFeedback;
    const feedback = [
      xhsFeedback ? { ...xhsFeedback, platform: '小红书', at: xhsFeedback.at || '' } : null,
      shortVideoFeedback ? { ...shortVideoFeedback, platform: '抖音 / TikTok', at: shortVideoFeedback.at || '' } : null
    ].filter(Boolean).sort((a, b) => String(b.at).localeCompare(String(a.at)))[0];
    const history = [
      ...(Array.isArray(state.xhsFeedbackHistory) ? state.xhsFeedbackHistory : (xhsFeedback ? [xhsFeedback] : [])),
      ...(Array.isArray(state.externalFeedbackHistory) ? state.externalFeedbackHistory : (shortVideoFeedback ? [shortVideoFeedback] : []))
    ];
    const decision = state.businessDecision;
    const panel = document.createElement('section');
    panel.className = 'curis-business-decision';
    panel.setAttribute('aria-labelledby', 'curis-business-decision-title');
    const resultStatus = feedback?.resultStatus || (String(feedback?.credibility || '').startsWith('高') ? '已验证价值' : '数据待验证');
    const metrics = feedback ? (feedback.platform === '小红书'
      ? `<div class="curis-business-decision-metrics"><span>阅读 <b>${escapeHtml(feedback.reads || 0)}</b></span><span>收藏 <b>${escapeHtml(feedback.saves || 0)}</b></span><span>评论 <b>${escapeHtml(feedback.comments || 0)}</b></span><span>新增粉丝 <b>${escapeHtml(feedback.follows || 0)}</b></span><span>线索价值 <b>¥${escapeHtml(Number(feedback.value || 0).toLocaleString())}</b></span><span>状态 <b>${escapeHtml(resultStatus)}</b></span><span>可信度 <b>${escapeHtml(feedback.credibility || '中')}</b></span><span>${history.length} 条结果记录</span></div>`
      : `<div class="curis-business-decision-metrics"><span>播放 <b>${escapeHtml(feedback.plays || 0)}</b></span><span>点赞 <b>${escapeHtml(feedback.likes || 0)}</b></span><span>新增粉丝 <b>${escapeHtml(feedback.follows || 0)}</b></span><span>成交 <b>${escapeHtml(feedback.orders || 0)}</b></span><span>成交价值 <b>¥${escapeHtml(Number(feedback.value || 0).toLocaleString())}</b></span><span>状态 <b>${escapeHtml(resultStatus)}</b></span><span>可信度 <b>${escapeHtml(feedback.credibility || '中')}</b></span><span>${history.length} 条结果记录</span></div>`)
      : '';
    const feedbackRoute = feedback?.platform === '小红书' ? 'workspace-runtime-xhs.html' : 'workspace-runtime-shortvideo.html';
    const feedbackOffice = feedback?.platform === '小红书' ? '小红书运营办公室' : '抖音 / TikTok 运营办公室';
    const portfolioCount = state.departmentDraft?.name && state.departmentCommitment?.name ? 4 : 3;
    panel.innerHTML = `<div class="curis-business-decision-head"><div><p class="curis-business-decision-kicker">CEO 下一次经营判断</p><h2 id="curis-business-decision-title" class="curis-business-decision-title">${feedback ? `这条${feedback.platform}真实结果，意味着下一步怎么走？` : '业务还在等待第一条真实结果'}</h2><p class="curis-business-decision-note">${feedback ? '结果已经回到公司，下一步不是继续看数据，而是决定资源是否继续投入。' : '没有平台授权时，先去业务办公室手动补录；结果回来后，CEO 再决定继续、扩大或暂停。'}</p>${metrics}</div></div><div class="curis-business-decision-actions"><button type="button" data-business-decision="continue" class="primary" data-curis-handled="true">继续验证</button><button type="button" data-business-decision="scale" data-curis-handled="true">扩大业务</button><button type="button" data-business-decision="pause" data-curis-handled="true">暂停复盘</button><button type="button" data-business-decision="feedback" data-curis-handled="true">去录入结果</button></div>`;
    map.parentNode.insertBefore(panel, map.nextSibling);
    if (feedback && resultStatus !== '已验证价值') {
      panel.querySelector('.curis-business-decision-note').textContent = `当前结果状态为“${resultStatus}”，扩大业务前需要先补充证据并确认价值。`;
    }
    const actions = panel.querySelector('.curis-business-decision-actions');
    const updateMap = choice => {
      const meta = map.querySelector('.curis-map-meta');
      const node = map.querySelector(`[data-business-target="${feedback?.platform === '小红书' ? 'content-growth' : 'short-video'}"] em`);
      const capacityApproved = (state.capacityDecision?.choice === 'approve' || state.capacityDecision?.label === '确认扩容配置')
        && capacityMatchesBusiness(state.capacityDecision, feedbackOffice === '小红书运营办公室' ? '小红书运营' : '抖音 / TikTok 运营', feedback?.platform);
      const copy = choice === 'scale' && capacityApproved
        ? ['扩大业务已批准 · 新容量运行中', '新容量运行中']
        : {
        continue: [`继续验证中 · ${feedbackOffice}保持当前投入`, '继续验证'],
        scale: ['业务扩大准备中 · 等待能力供给调整', '扩大能力供给'],
        pause: [`${feedbackOffice}已暂停 · 等待下一次复盘`, '暂停复盘']
        }[choice];
      if (!copy) return;
      if (meta) meta.textContent = `${portfolioCount} 条业务 · ${copy[0]}`;
      if (node) node.textContent = copy[1];
    };
    if (decision?.choice) updateMap(decision.choice);
    if (decision?.choice) {
      const labels = { continue: '继续验证', scale: '扩大业务', pause: '暂停复盘' };
      panel.querySelector('.curis-business-decision-title').textContent = `已记录：${labels[decision.choice] || '经营判断'}`;
      const capacityApproved = decision.choice === 'scale'
        && state.capacityDecision?.choice === 'approve'
        && capacityMatchesBusiness(state.capacityDecision, feedbackOffice === '小红书运营办公室' ? '小红书运营' : '抖音 / TikTok 运营', feedback?.platform);
      panel.querySelector('.curis-business-decision-note').textContent = capacityApproved
        ? `扩容配置已经确认，${feedbackOffice}正在按新容量运行。`
        : `CEO 的判断已交给对应办公室，CEO 助理会在下一次结果回来后继续汇报。`;
    }
    actions.querySelectorAll('[data-business-decision]').forEach(button => button.addEventListener('click', () => {
      const choice = button.dataset.businessDecision;
      if (choice === 'feedback') {
        window.location.href = feedbackRoute;
        return;
      }
      if (!feedback) {
        showToast('先取得一条外部结果，再做下一次经营判断');
        return;
      }
      if (choice === 'scale' && resultStatus !== '已验证价值') {
        showToast('只有“已验证价值”的结果可以支持扩大业务；请先补证据或进入复盘');
        return;
      }
      const labels = { continue: '继续验证', scale: '扩大业务', pause: '暂停复盘' };
      const routes = { continue: { label: feedbackOffice, route: feedbackRoute }, scale: { label: 'AI 组织办公室', route: 'ai-organization.html' }, pause: { label: '经营办公室', route: 'operating.html' } };
      const target = routes[choice];
      if (!target) return;
      const nextDecision = { choice, label: labels[choice], platform: feedback?.platform || '', at: new Date().toISOString() };
      writeState({
        businessDecision: nextDecision,
        lastAssistantMessage: `你已选择${labels[choice]}。我会把这次判断交给${target.label}，并在下一次结果回来后继续汇报。`,
        lastAssistantHandoff: { label: target.label, route: target.route, message: labels[choice] }
      });
      updateMap(choice);
      window.__curisPaintBusinessDecision?.(nextDecision);
      panel.querySelector('.curis-business-decision-title').textContent = `已记录：${labels[choice]}`;
      panel.querySelector('.curis-business-decision-note').textContent = `CEO 的判断已交给${target.label}，CEO 助理会在下一次结果回来后继续汇报。`;
      showToast(`已记录：${labels[choice]}`);
    }));
  }

  function initReviewWorkbench() {
    if (!window.location.pathname.endsWith('business.html') || document.querySelector('.curis-review-workbench')) return;
    const anchor = document.querySelector('.curis-business-decision') || document.querySelector('.curis-business-map');
    if (!anchor) return;
    const state = readState();
    const histories = {
      '小红书运营': Array.isArray(state.xhsFeedbackHistory) ? state.xhsFeedbackHistory : (state.latestXhsFeedback ? [state.latestXhsFeedback] : []),
      '抖音 / TikTok 运营': Array.isArray(state.externalFeedbackHistory) ? state.externalFeedbackHistory : (state.latestExternalFeedback ? [state.latestExternalFeedback] : [])
    };
    const latestOutcome = business => (Array.isArray(state.outcomeAttributions) ? state.outcomeAttributions : []).filter(item => item.business === business).sort((a, b) => String(b.at || '').localeCompare(String(a.at || '')))[0];
    const last = list => list.slice().sort((a, b) => String(b.at || '').localeCompare(String(a.at || '')))[0];
    const formatDelta = (current, previous) => {
      if (previous === undefined || previous === null || previous === '') return '首轮基线';
      const delta = Number(current || 0) - Number(previous || 0);
      return `${delta >= 0 ? '+' : ''}${delta.toLocaleString()}`;
    };
    const number = value => Number(value || 0).toLocaleString();
    const reviews = [];
    [['小红书运营', histories['小红书运营'], 'workspace-runtime-xhs.html'], ['抖音 / TikTok 运营', histories['抖音 / TikTok 运营'], 'workspace-runtime-shortvideo.html']].forEach(([business, history, route]) => {
      const record = last(history);
      if (!record) return;
      const previous = history.length > 1 ? history[history.length - 2] : null;
      const outcome = latestOutcome(business);
      const isXhs = business === '小红书运营';
      reviews.push({ business, route, outcome, record, title: isXhs ? '小红书内容复盘' : '抖音 / TikTok 内容复盘', status: record.resultStatus || '数据待验证', metrics: isXhs ? [['阅读', number(record.reads), formatDelta(record.reads, previous?.reads)], ['收藏', number(record.saves), formatDelta(record.saves, previous?.saves)], ['新增粉丝', number(record.follows), formatDelta(record.follows, previous?.follows)], ['线索价值', `¥${number(record.value)}`, previous ? `¥${formatDelta(record.value, previous.value)}` : '首轮基线']] : [['播放', number(record.plays), formatDelta(record.plays, previous?.plays)], ['点赞', number(record.likes), formatDelta(record.likes, previous?.likes)], ['新增粉丝', number(record.follows), formatDelta(record.follows, previous?.follows)], ['成交价值', `¥${number(record.value)}`, previous ? `¥${formatDelta(record.value, previous.value)}` : '首轮基线']] });
    });
    if (state.softwareAcceptance) {
      const outcome = latestOutcome('软件开发');
      reviews.push({ business: '软件开发', route: 'workspace-runtime-software.html', outcome, title: 'Curis 自研交付复盘', status: state.softwareAcceptance.choice === 'accept' ? '已验证价值' : state.softwareAcceptance.label || '待处理', record: state.softwareAcceptance, metrics: [['验收状态', state.softwareAcceptance.label || '待处理', state.softwareAcceptance.choice === 'accept' ? '通过真实使用' : '等待下一次验收'], ['证据', state.softwareAcceptance.evidenceRef || '未登记', state.softwareAcceptance.evidenceType || '待补充'], ['运行关联', outcome ? runLabelForState(state, outcome.runId, outcome.runIds) : '未指定运行', outcome ? '已关联' : '可补关联'], ['可归因价值', outcome ? `¥${number(outcome.value)}` : '待归因', outcome?.status || '等待 CEO 确认']] });
    }
    const workbench = document.createElement('section');
    workbench.className = 'curis-review-workbench';
    workbench.setAttribute('aria-labelledby', 'curis-review-workbench-title');
    workbench.innerHTML = `<div class="curis-review-workbench-head"><div><p class="curis-review-workbench-kicker">结果复盘 · 下一轮经营输入</p><h2 id="curis-review-workbench-title">每条结果都要回答：下一步做什么？</h2><p>把结果、变化、成本和下一次动作放在同一处，CEO 不需要在业务空间、成果库和财务之间来回寻找。</p></div><span>${reviews.length} 个业务结果</span></div><div class="curis-review-workbench-grid"></div>`;
    const grid = workbench.querySelector('.curis-review-workbench-grid');
    if (!reviews.length) grid.innerHTML = '<div class="curis-review-empty"><strong>等待第一条真实结果</strong><span>结果回流后，这里会显示基线变化、证据、成本和下一次动作。</span></div>';
    reviews.forEach(review => {
      const card = document.createElement('article');
      card.className = 'curis-review-card';
      card.innerHTML = `<div class="curis-review-card-head"><div><p></p><h3></h3></div><span class="curis-review-status"></span></div><div class="curis-review-metrics"></div><div class="curis-review-card-foot"><p></p><div><button type="button" data-review-action="evidence">查看证据</button><button type="button" data-review-action="capability">调整能力</button><button type="button" data-review-action="next" class="primary">安排下一轮</button></div></div>`;
      card.querySelector('p').textContent = `${review.business} · ${review.record.at ? new Date(review.record.at).toLocaleDateString('zh-CN') : '最近一轮'}`;
      card.querySelector('h3').textContent = review.title;
      card.querySelector('.curis-review-status').textContent = review.status;
      card.querySelector('.curis-review-metrics').innerHTML = review.metrics.map(metric => `<div><span>${escapeHtml(metric[0])}</span><strong>${escapeHtml(metric[1])}</strong><em>${escapeHtml(metric[2])}</em></div>`).join('');
      const outcome = review.outcome;
      const nextNote = review.status === '已验证价值' ? '价值已经可以支持下一次投入判断；CEO 可以继续验证或扩大业务。' : '先补充证据或继续观察，再决定是否扩大投入。';
      card.querySelector('.curis-review-card-foot p').textContent = `${nextNote}${outcome?.evidenceRef ? ` 证据：${outcome.evidenceRef}` : ''}`;
      card.querySelector('[data-review-action="evidence"]').addEventListener('click', () => {
        if (outcome) return openEvidenceReview({ title: `${review.business} · 结果证据`, source: outcome.source || review.record.source || 'CEO 结果回传', summary: `${review.title}\n${review.metrics.map(metric => `${metric[0]}：${metric[1]}`).join(' · ')}`, status: outcome.evidenceStatus || '待 CEO 采用', confidence: outcome.status === '已验证价值' ? 'CEO 已确认价值' : '待复核', outcomeId: outcome.id, evidenceType: outcome.evidence?.type || outcome.evidenceType || '未登记', evidenceVersion: outcome.evidence?.version || '—', capturedAt: outcome.evidence?.capturedAt || outcome.at || '—' });
        window.location.href = review.route;
      });
      card.querySelector('[data-review-action="capability"]').addEventListener('click', () => { writeState({ capabilityFocusRoute: review.route, lastAssistantMessage: `${review.business}下一轮需要重新确认模型、负责人 AI、技能和连接器。`, lastAssistantHandoff: { label: 'AI 能力配置', route: review.route, message: '复盘后调整能力组合' } }); window.location.href = review.route; });
      card.querySelector('[data-review-action="next"]').addEventListener('click', () => openFormDialog({ title: `安排${review.business}下一轮`, description: '复盘不是写总结，而是把下一次假设、检查点和负责人交给业务空间继续运行。', submitLabel: '安排下一轮', fields: [{ name: 'objective', label: '下一轮要验证什么', type: 'textarea', placeholder: '例如：保留高收藏主题，测试两个更具体的标题结构。', required: true }, { name: 'checkpoint', label: '检查点', placeholder: '例如：3 天后回收首轮数据', required: true }, { name: 'schedule', label: '触发节奏', placeholder: '例如：每天 08:00 / 3 天后', required: true }], onSubmit: values => { const current = readState(); const actions = Array.isArray(current.reviewActions) ? current.reviewActions : []; const action = { business: review.business, route: review.route, ...values, at: new Date().toISOString(), status: '已安排' }; const schedules = JSON.parse(localStorage.getItem('curis-schedules') || '[]'); schedules.push({ id: `review-${Date.now()}`, name: `${review.business} · 复盘后下一轮`, business: review.business, schedule: values.schedule, owner: review.business === '软件开发' ? '产品 AI' : review.business === '小红书运营' ? '策略 AI' : '数据 AI', task: values.objective, estimatedCost: 0, route: review.route, enabled: true }); localStorage.setItem('curis-schedules', JSON.stringify(schedules.slice(-24))); writeState({ reviewActions: [...actions, action].slice(-24), lastAssistantMessage: `${review.business}下一轮已安排：${values.objective}`, lastAssistantHandoff: { label: review.business, route: review.route, message: '复盘后下一轮已安排' } }); showToast('下一轮已安排，业务空间会按检查点继续运行'); } }));
      grid.appendChild(card);
    });
    const style = document.createElement('style');
    style.textContent = '.curis-review-workbench{margin-top:16px;padding:20px;border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:12px;background:var(--bg-base-secondary,#202226)}.curis-review-workbench-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px}.curis-review-workbench-kicker{margin:0 0 6px;color:var(--text-secondary,#a4a7af);font-size:10px;letter-spacing:.08em;text-transform:uppercase}.curis-review-workbench-head h2{margin:0;font-size:17px;letter-spacing:-.02em}.curis-review-workbench-head p{max-width:680px;margin:7px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.5}.curis-review-workbench-head>span{padding:6px 8px;color:var(--text-secondary,#a4a7af);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:999px;font-size:10px;white-space:nowrap}.curis-review-workbench-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:16px}.curis-review-card{display:grid;gap:12px;padding:14px;border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:9px;background:var(--bg-base-default,#191a1d)}.curis-review-card-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}.curis-review-card-head p{margin:0 0 4px;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-review-card-head h3{margin:0;font-size:13px}.curis-review-status{padding:4px 6px;color:var(--text-secondary,#a4a7af);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:5px;font-size:10px;white-space:nowrap}.curis-review-metrics{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1px;background:var(--border-neutral-l1,rgba(224,226,242,.1));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:7px;overflow:hidden}.curis-review-metrics>div{display:grid;gap:4px;padding:9px;background:var(--bg-base-secondary,#202226)}.curis-review-metrics span,.curis-review-metrics em{color:var(--text-secondary,#a4a7af);font-size:10px;font-style:normal}.curis-review-metrics strong{font-size:15px}.curis-review-card-foot{display:grid;gap:10px}.curis-review-card-foot p{margin:0;color:var(--text-secondary,#a4a7af);font-size:10px;line-height:1.5}.curis-review-card-foot>div{display:flex;gap:7px}.curis-review-card-foot button{padding:7px 9px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}.curis-review-card-foot button.primary{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}.curis-review-empty{display:grid;gap:6px;padding:18px;border:1px dashed var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:8px}.curis-review-empty span{color:var(--text-secondary,#a4a7af);font-size:11px}@media(max-width:900px){.curis-review-workbench-grid{grid-template-columns:1fr 1fr}}@media(max-width:620px){.curis-review-workbench-head{flex-direction:column}.curis-review-workbench-grid{grid-template-columns:1fr}}';
    document.head.appendChild(style);
    anchor.parentNode.insertBefore(workbench, anchor.nextSibling);
  }

  function initBusinessCardActions() {
    if (!window.location.pathname.endsWith('business.html')) return;
    const routeForBusiness = title => /软件|Curis|研发/.test(title) ? 'workspace-runtime-software.html' : /小红书|图文|内容增长/.test(title) ? 'workspace-runtime-xhs.html' : /短视频|抖音|视频/.test(title) ? 'workspace-runtime-shortvideo.html' : 'workspace-portal.html';
    const paintDecision = decision => {
      if (!decision?.choice) return;
      const title = decision.businessTitle || (decision.platform === '小红书' ? '小红书运营' : decision.platform === '抖音 / TikTok' ? '抖音 / TikTok 运营' : '');
      if (!title) return;
      const card = [...document.querySelectorAll('.biz-card')].find(item => item.querySelector('.biz-name')?.textContent.trim() === title);
      if (!card) return;
      const pill = card.querySelector('.stage-pill');
      const health = card.querySelectorAll('.health-value');
      const copy = { continue: ['验证中', 'stage-experiment', '继续验证'], scale: ['扩大中', 'stage-scaling', '资源扩充'], pause: ['已暂停', 'stage-paused', '暂停复盘'], close: ['已归档', 'stage-paused', '已归档'] }[decision.choice];
      if (!copy) return;
      pill?.classList.remove('stage-operating', 'stage-scaling', 'stage-experiment', 'stage-paused');
      if (pill) { pill.classList.add(copy[1]); pill.textContent = copy[0]; }
      if (health[1]) health[1].lastChild.replaceWith(document.createTextNode(copy[2]));
    };
    const record = (choice, label, route, message, businessTitle = '') => {
      const decision = { choice, label, businessTitle, at: new Date().toISOString() };
      writeState(choice === 'close' ? { businessArchive: decision, lastAssistantMessage: message, lastAssistantHandoff: { label, route, message: label } } : { businessDecision: decision, lastAssistantMessage: message, lastAssistantHandoff: { label, route, message: label } });
      paintDecision(decision);
      showToast(`${label}已记录`);
    };
    window.__curisPaintBusinessDecision = paintDecision;
    document.querySelectorAll('.biz-card .biz-card-footer button').forEach(button => {
      if (button.dataset.curisBusinessBound === 'true') return;
      const label = button.textContent.trim();
      if (!['扩大', '暂停', '关闭'].includes(label)) return;
      button.dataset.curisBusinessBound = 'true';
      button.addEventListener('click', event => {
        event.stopPropagation();
        const title = button.closest('.biz-card')?.querySelector('.biz-name')?.textContent.trim() || '当前业务';
        if (label === '扩大') return record('scale', '扩大业务', 'ai-organization.html', `已记录扩大“${title}”的判断，先检查 AI 团队容量和交接。`, title);
        if (label === '暂停') return record('pause', '暂停复盘', 'operating.html', `已暂停“${title}”的新周期启动，保留现有证据等待复盘。`, title);
        return record('close', '关闭业务', 'business.html', `已归档“${title}”的当前运行，证据和决策仍保留在公司记录中。`, title);
      });
    });
    document.querySelectorAll('#businessDrawer .drawer-actions button').forEach(button => {
      if (button.dataset.curisBusinessBound === 'true') return;
      button.dataset.curisBusinessBound = 'true';
      button.addEventListener('click', event => {
        event.stopPropagation();
        const label = button.textContent.trim();
        const title = document.querySelector('#drawerTitle')?.textContent.trim() || '当前业务';
        if (label === '查看 工作空间') { window.location.href = routeForBusiness(title); return; }
        if (label === '扩大投入') { record('scale', '扩大业务', 'ai-organization.html', `已记录扩大“${title}”的判断，AI 组织办公室会先检查容量。`, title); document.querySelector('#drawerClose')?.click(); return; }
        if (label === '暂停业务') { record('pause', '暂停复盘', 'operating.html', `已暂停“${title}”的新周期启动，CEO 助理会在下一次复盘时提醒。`, title); document.querySelector('#drawerClose')?.click(); }
      });
    });
    const current = readState();
    paintDecision(current.businessDecision || current.businessArchive);
  }

  function initBusinessCreation() {
    if (!window.location.pathname.endsWith('business.html') || document.querySelector('.curis-business-create')) return;
    const map = document.querySelector('.curis-business-map');
    if (!map) return;
    const panel = document.createElement('section');
    panel.className = 'curis-business-create';
    panel.setAttribute('aria-labelledby', 'curis-business-create-title');
    if (!readState().companyCreatedAt) {
      panel.innerHTML = '<div class="curis-business-create-head"><div><p class="curis-business-create-kicker">第一步</p><h2 id="curis-business-create-title" class="curis-business-create-title">先创建公司，再建立业务</h2><p class="curis-business-create-note">业务属于公司。完成公司意图、第一项业务方向和 CEO 助理配置后，才能进入业务空间搭建。</p></div><button class="curis-business-create-submit" type="button" data-create-company>开始创建公司 →</button></div>';
      map.parentNode.insertBefore(panel, map.nextSibling);
      panel.querySelector('[data-create-company]')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
      return;
    }
    panel.innerHTML = `<div class="curis-business-create-head"><div><p class="curis-business-create-kicker">下一条业务</p><h2 id="curis-business-create-title" class="curis-business-create-title">从一个新的经营假设搭建业务空间</h2><p class="curis-business-create-note">业务不是列表项。先定义要验证的结果，再让业务工程 AI 把它装修成一间可运行的办公室。</p></div><button class="curis-business-create-toggle" type="button" data-curis-handled="true">创建新业务</button></div><form class="curis-business-create-form"><div class="curis-business-create-field"><label for="curis-new-business-name">业务名称</label><input id="curis-new-business-name" name="name" placeholder="例如：小红书内容增长" required /></div><div class="curis-business-create-field"><label for="curis-new-business-outcome">第一阶段要证明的结果</label><textarea id="curis-new-business-outcome" name="outcome" rows="2" placeholder="例如：30 天内发布 12 条内容，获得首批真实互动与线索" required></textarea></div><div class="curis-business-create-options" aria-label="可复用业务模板"><button type="button" class="curis-business-create-option" data-new-business-template="xhs">套用小红书模板</button><button type="button" class="curis-business-create-option" data-new-business-template="douyin">套用抖音模板</button><button type="button" class="curis-business-create-option" data-new-business-template="software">套用软件开发模板</button></div><button class="curis-business-create-submit" type="submit" data-curis-handled="true">进入工作空间搭建 →</button></form>`;
    map.parentNode.insertBefore(panel, map.nextSibling);
    const form = panel.querySelector('form');
    const activeDepartment = readState().departmentDraft?.name && readState().departmentStatus === 'active' ? readState().departmentDraft.name : '';
    if (activeDepartment) {
      panel.querySelector('.curis-business-create-kicker').textContent = '部门办公室 · 首项责任';
      panel.querySelector('.curis-business-create-title').textContent = `为${activeDepartment}指定第一项业务责任`;
      panel.querySelector('.curis-business-create-note').textContent = '先定义这间办公室要承接的第一项业务结果，再把责任、能力和验收路径装修成可运行空间。';
      panel.querySelector('label[for="curis-new-business-name"]').textContent = '责任 / 业务名称';
      panel.querySelector('label[for="curis-new-business-outcome"]').textContent = '第一项要承诺的结果';
      panel.querySelector('.curis-business-create-toggle').textContent = '修改首项责任';
      panel.classList.add('is-open');
    }
    const applyTemplate = key => {
      const template = FOUNDING_TEMPLATES[key];
      if (!template) return;
      form.elements.name.value = template.label;
      form.elements.outcome.value = template.outcome;
      showToast(`${template.label} 已带入，可继续修改`);
    };
    panel.querySelector('[data-curis-handled="true"]').addEventListener('click', () => {
      panel.classList.toggle('is-open');
      if (panel.classList.contains('is-open')) form.elements.name.focus();
    });
    panel.querySelectorAll('[data-new-business-template]').forEach(button => button.addEventListener('click', () => applyTemplate(button.dataset.newBusinessTemplate)));
    form.addEventListener('submit', event => {
      event.preventDefault();
      const draft = { name: form.elements.name.value.trim(), outcome: form.elements.outcome.value.trim(), at: new Date().toISOString() };
      if (!draft.name || !draft.outcome) return;
      writeState({
        newBusinessDraft: activeDepartment ? { ...draft, departmentName: activeDepartment } : draft,
        ...(activeDepartment ? { departmentCommitment: { departmentName: activeDepartment, name: draft.name, outcome: draft.outcome, status: 'pending', at: draft.at } } : {}),
        lastAssistantMessage: `新的业务假设“${draft.name}”已经记录。我会让业务工程 AI 先把结果、岗位和能力装配成一间可运行的空间。`,
        lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: `搭建新业务：${draft.name}` }
      });
      showToast('业务假设已记录，正在进入工作空间搭建');
      window.setTimeout(() => { window.location.href = 'workspace-studio.html'; }, 180);
    });
  }

  function initOfficeShelf() {
    if (!window.location.pathname.endsWith('workspace-portal.html') || document.querySelector('.curis-office-shelf')) return;
    const anchor = document.querySelector('.quick-stats');
    if (!anchor) return;
    const shelf = document.createElement('section');
    shelf.className = 'curis-office-shelf';
    shelf.setAttribute('aria-label', '部门办公室');
    shelf.innerHTML = `
      <div class="curis-office-header">
        <div><p class="curis-office-kicker">公司空间</p><h2 class="curis-office-title">进入一间正在工作的部门办公室</h2></div>
        <span class="curis-office-meta">业务空间不是项目列表，是 AI 团队的工作现场</span>
      </div>
      <div class="curis-office-list">
        <button class="curis-office-item" type="button" data-business-target="software-dev"><strong>研发办公室</strong><span>研发 AI · QA AI · 产品 AI</span><em>当前：Curis v0.2</em></button>
        <button class="curis-office-item" type="button" data-business-target="short-video"><strong>抖音 / TikTok 办公室</strong><span>策略 · 脚本 · 剪辑 · 数据复盘</span><em>当前：首条视频待回传</em></button>
        <button class="curis-office-item" type="button" data-business-target="content-growth"><strong>小红书运营办公室</strong><span>研究 · 选题 · 内容 · 平台运营</span><em>当前：等待平台授权</em></button>
      </div>`;
    const state = readState();
    if (!state.companyCreatedAt) {
      shelf.querySelector('.curis-office-title').textContent = '公司空间还没有办公室';
      shelf.querySelector('.curis-office-meta').textContent = '完成公司创建后，AI 员工和业务办公室会从这里开始出现';
      shelf.querySelector('.curis-office-list').innerHTML = '<button class="curis-office-item curis-office-empty" type="button"><strong>创建第一间办公室</strong><span>先说出你想经营什么，再选择业务模板或从零搭建。</span><em>开始创建公司 →</em></button>';
      anchor.parentNode.insertBefore(shelf, anchor);
      shelf.querySelector('.curis-office-empty')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
      return;
    }
    const firstBusiness = String(state.firstBusiness || state.newBusinessDraft?.name || '');
    const activeOfficeHrefs = new Set();
    if (/软件|Curis|研发/.test(firstBusiness) || state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html')) activeOfficeHrefs.add('workspace-runtime-software.html');
    if (/小红书/.test(firstBusiness) || state.latestXhsFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-xhs.html')) activeOfficeHrefs.add('workspace-runtime-xhs.html');
    if (/抖音|TikTok|短视频/.test(firstBusiness) || state.latestExternalFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-shortvideo.html')) activeOfficeHrefs.add('workspace-runtime-shortvideo.html');
    shelf.querySelectorAll('.curis-office-item[data-business-target]').forEach(item => {
      const href = item.dataset.businessTarget === 'software-dev' ? 'workspace-runtime-software.html' : item.dataset.businessTarget === 'content-growth' ? 'workspace-runtime-xhs.html' : 'workspace-runtime-shortvideo.html';
      const visible = activeOfficeHrefs.has(href);
      item.hidden = !visible;
      item.style.display = visible ? '' : 'none';
    });
    const decision = state.lastDecision;
    const feedback = state.latestExternalFeedback;
    const capacity = state.capacityDecision;
    const softwareAcceptance = state.softwareAcceptance;
    const shortVideoOffice = shelf.querySelector('[data-business-target="short-video"] em');
    const softwareOffice = shelf.querySelector('[data-business-target="software-dev"] em');
    if (decision?.choice === 'approve') shortVideoOffice.textContent = '当前：Runtime v1.1 执行中';
    if (feedback) shortVideoOffice.textContent = '当前：真实结果已回流';
    if ((state.businessDecision?.choice === 'scale' || state.businessDecision?.label === '扩大业务')
      && (capacity?.choice === 'approve' || capacity?.label === '确认扩容配置')) shortVideoOffice.textContent = '当前：新容量运行中';
    if (softwareAcceptance?.choice === 'accept') softwareOffice.textContent = '当前：Curis v0.2 已验收';
    if (state.departmentDraft?.name && state.departmentStatus === 'active') {
      const office = document.createElement('button');
      office.className = 'curis-office-item';
      office.type = 'button';
      office.dataset.departmentRoute = 'workspace-studio.html';
      const commitment = state.departmentCommitment;
      office.innerHTML = '<strong></strong><span></span><em></em>';
      office.querySelector('strong').textContent = state.departmentDraft.name;
      office.querySelector('span').textContent = commitment?.status === 'active'
        ? `首项责任：${commitment.name}`
        : commitment?.status === 'paused'
          ? `已暂停：${commitment.name}`
          : commitment?.status === 'pending_revision'
            ? `待调整：${commitment.name}`
        : '部门责任 · 业务工程 AI · 共享能力';
      office.querySelector('em').textContent = commitment?.status === 'active' ? '当前：运行中' : commitment?.status === 'paused' ? '当前：已暂停' : commitment?.status === 'pending_revision' ? '下一步：调整责任 →' : '下一步：指定第一项责任 →';
      shelf.querySelector('.curis-office-list')?.appendChild(office);
      office.addEventListener('click', () => { window.location.href = commitment?.status === 'active' ? 'workspace-runtime-department.html' : commitment?.status === 'paused' ? 'operating.html' : commitment?.status === 'pending_revision' ? 'workspace-studio.html' : 'business.html'; });
    }
    anchor.parentNode.insertBefore(shelf, anchor);
    shelf.querySelectorAll('[data-business-target]').forEach(node => node.addEventListener('click', () => {
      if (node.dataset.businessTarget === 'software-dev') return window.location.href = 'workspace-runtime-software.html';
      if (node.dataset.businessTarget === 'short-video') return window.location.href = 'workspace-runtime-shortvideo.html';
      if (node.dataset.businessTarget === 'content-growth') return window.location.href = 'workspace-runtime-xhs.html';
    }));
  }

  function initOperatingState() {
    if (!window.location.pathname.endsWith('operating.html') || document.querySelector('.curis-operating-state')) return;
    const header = document.querySelector('.page-header');
    if (!header) return;
    const state = readState();
    if (!state.companyCreatedAt) return;
    const decision = state.businessDecision;
    const meetingDecision = state.meetingDecision;
    const softwareAcceptance = state.softwareAcceptance;
    const departmentActive = state.departmentDraft?.name && state.departmentCommitment?.status === 'active';
    const departmentResult = state.departmentResult;
    const scheduledRunWaiting = ['queued', 'waiting_ceo', 'acknowledged', 'failed'].includes(state.lastScheduledRun?.status);
    if (!decision?.choice && !meetingDecision && !softwareAcceptance?.choice && !departmentActive && !departmentResult && !scheduledRunWaiting) return;
    const copy = scheduledRunWaiting && !decision?.choice && !meetingDecision && !softwareAcceptance?.choice
      ? [state.lastScheduledRun.status === 'failed' ? '自动任务出现异常' : state.lastScheduledRun.status === 'queued' ? '自动任务等待可用容量' : state.lastScheduledRun.status === 'acknowledged' ? '自动任务已打开 · 等待完成处理' : '自动任务等待 CEO 处理', state.lastScheduledRun.output || '请查看公司日历中的运行记录，确认下一步。']
      : departmentResult && !decision?.choice && !meetingDecision && !softwareAcceptance?.choice
      ? [`${state.departmentDraft.name} 已收到首项责任回报`, `${departmentResult.status}：${departmentResult.note || 'CEO 已记录结果。'} CEO 助理会把这条回报带入下一次经营判断。`]
      : departmentActive && !decision?.choice && !meetingDecision && !softwareAcceptance?.choice
        ? [`${state.departmentDraft.name} 已开始运行`, `首项责任“${state.departmentCommitment.name}”已经交给执行 AI，CEO 助理正在等待第一条真实结果。`]
      : meetingDecision && !decision?.choice && !softwareAcceptance?.choice
      ? ['外部合作方周会已形成决议', '一周试运行与预算边界已经确认，CEO 助理会守住档期和外部回传，结果回来后进入下一次经营判断。']
      : softwareAcceptance?.choice && !decision?.choice && !meetingDecision
        ? (softwareAcceptance.choice === 'accept'
          ? ['Curis v0.2 已验收', 'CEO 已通过真实使用，研发办公室会把反馈带入下一次软件增量。']
          : ['Curis v0.2 等待下一步', softwareAcceptance.choice === 'rework' ? '研发 AI 正在处理 CEO 反馈，完成后会重新提交。' : '研发 AI 正在准备现场演示，CEO 助理会守住下一次验收。'])
      : {
      continue: ['抖音 / TikTok 运营继续验证中', '抖音 / TikTok 运营办公室保持当前投入，下一条外部结果回来后再决定是否增加容量。'],
      scale: ['抖音 / TikTok 运营已进入扩大准备', state.capacityDecision?.choice === 'approve' && capacityMatchesBusiness(state.capacityDecision, decision.businessTitle || '抖音 / TikTok 运营', decision.platform) ? '扩容配置已确认，抖音 / TikTok 运营办公室正在按新容量运行。' : '等待 AI 组织确认负载、岗位和下一次交接。'],
      pause: ['抖音 / TikTok 运营已暂停 · 等待下一次复盘', '当前承诺已停止新增投入，已有结果与学习记录保留在业务版图，CEO 可以随时重新开启。']
      }[decision.choice];
    if (!copy) return;
    const panel = document.createElement('section');
    panel.className = 'curis-operating-state';
    panel.setAttribute('aria-labelledby', 'curis-operating-state-title');
    panel.innerHTML = `<p class="curis-operating-state-kicker">CEO 判断已生效</p><h2 id="curis-operating-state-title" class="curis-operating-state-title"></h2><p class="curis-operating-state-note"></p><div class="curis-operating-state-actions"><button type="button" data-operating-route="business.html">回到业务版图</button><button type="button" data-operating-route="ceo-desk.html">让 CEO 助理继续守住</button></div>`;
    panel.querySelector('.curis-operating-state-title').textContent = copy[0];
    panel.querySelector('.curis-operating-state-note').textContent = copy[1];
    header.parentNode.insertBefore(panel, header.nextSibling);
    panel.querySelectorAll('[data-operating-route]').forEach(button => button.addEventListener('click', () => { window.location.href = button.dataset.operatingRoute; }));
  }

  function initOperatingArchive() {
    if (!window.location.pathname.endsWith('operating.html') || document.querySelector('.curis-operating-archive')) return;
    const header = document.querySelector('.page-header');
    if (!header) return;
    const state = readState();
    const items = [];
    if (Array.isArray(state.operatingDeferredItems)) {
      state.operatingDeferredItems.slice(-8).reverse().forEach(item => items.push({ ...item, title: `已延后 · ${item.title}`, note: `下一检查点：${item.checkpoint} · ${item.reason}`, route: 'operating.html', source: '经营办公室' }));
    }
    if (Array.isArray(state.operatingArchivedItems)) {
      state.operatingArchivedItems.slice(-8).reverse().forEach(item => items.push({ ...item, source: item.source || '经营办公室' }));
    }
    if (state.softwareAcceptance) {
      const result = state.softwareAcceptance;
      items.push({ title: `Curis v0.2 · ${result.label || '验收记录'}`, note: result.feedback || '研发办公室的 CEO 验收结果，已进入下一周期。', route: 'workspace-runtime-software.html', source: '研发办公室' });
    }
    if (state.meetingDecision) {
      items.push({ title: state.meetingDecision.title || '外部合作方周会 · 会议决议', note: state.meetingDecision.summary || '会议共识已形成，承诺等待回报。', route: 'meeting.html', source: '会议工作台' });
    }
    if (state.latestExternalFeedback) {
      const feedback = state.latestExternalFeedback;
      items.push({ title: '抖音 / TikTok · 外部结果回流', note: `播放 ${feedback.plays || 0} · 新增粉丝 ${feedback.follows || 0} · 成交 ${feedback.orders || 0} · 状态 ${feedback.resultStatus || '数据待验证'} · 可信度 ${feedback.credibility || '中'}`, route: 'workspace-runtime-shortvideo.html', source: '抖音 / TikTok 运营办公室' });
    }
    if (state.departmentResult && state.departmentDraft?.name) {
      const result = state.departmentResult;
      items.push({ title: `${state.departmentDraft.name} · ${state.departmentCommitment?.name || '首项责任'} 回报`, note: `${result.status} · ${result.note || 'CEO 已记录结果。'}`, route: 'workspace-runtime-department.html', source: state.departmentDraft.name });
    }
    if (state.businessDecision) {
      items.push({ title: `经营判断 · ${state.businessDecision.label || state.businessDecision.choice}`, note: 'CEO 判断已写入业务版图，等待下一次结果验证。', route: 'business.html', source: '业务版图' });
    }
    if (state.lastScheduledRun) {
      const run = state.lastScheduledRun;
      const runStatus = run.status === 'queued' ? '排队中 · 等待能力释放' : run.status === 'running' ? '执行中' : run.status === 'waiting_ceo' ? '等待 CEO 打开' : run.status === 'acknowledged' ? '已打开 · 等待完成处理' : run.status === 'failed' ? '运行异常' : run.status === 'resolved' ? '已处理 · 进入复盘' : '已完成';
      items.push({ title: `自动运行 · ${run.title || '公司任务'}`, note: `${runStatus} · ${run.resolutionNote || run.output || '结果已写回公司日历。'}`, route: run.requiresCEO ? 'calendar.html' : (run.route || 'calendar.html'), source: '公司日历' });
    }
    const archive = document.createElement('section');
    archive.className = 'curis-operating-archive';
    archive.setAttribute('aria-labelledby', 'curis-operating-archive-title');
    const list = items.length
      ? items.map(item => `<button type="button" class="curis-operating-archive-item" data-archive-route="${escapeHtml(item.route)}"><span><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.note)}</span></span><em>${escapeHtml(item.source)} →</em></button>`).join('')
      : '<div class="curis-operating-archive-item"><span><strong>还没有新的共识或结果</strong><span>会议、验收和外部反馈会在形成后自动归档到这里。</span></span><em>等待中</em></div>';
    archive.innerHTML = `<div class="curis-operating-archive-head"><h2 id="curis-operating-archive-title" class="curis-operating-archive-title">共识与结果归档</h2><p class="curis-operating-archive-note">让公司的记忆可以被下一次决策引用</p></div><div class="curis-operating-archive-list">${list}</div>`;
    const anchor = document.querySelector('.curis-operating-state') || header;
    anchor.parentNode.insertBefore(archive, anchor.nextSibling);
    archive.querySelectorAll('[data-archive-route]').forEach(button => button.addEventListener('click', () => { window.location.href = button.dataset.archiveRoute; }));
  }

  function initFirstArrival() {
    if (!window.location.pathname.endsWith('founding-flow.html') || document.querySelector('.curis-arrival-space')) return;
    const welcome = document.querySelector('.step-panel[data-step="0"] .welcome-center');
    const anchor = welcome?.querySelector('.welcome-actions');
    if (!welcome || !anchor) return;
    const arrival = document.createElement('div');
    arrival.className = 'curis-arrival-space';
    arrival.setAttribute('aria-label', 'Curis 初次抵达空间');
    arrival.innerHTML = `
      <div class="curis-arrival-frame">
        <div class="curis-arrival-room">
          <p class="curis-arrival-kicker"><span>CEO OFFICE · DAY 01</span><span>还没有员工</span></p>
          <div class="curis-arrival-desk">
            <div class="curis-arrival-slot next"><strong>公司意图</strong><span>从一句想法开始</span></div>
            <div class="curis-arrival-slot"><strong>第一条业务</strong><span>等待你的第一个业务方向</span></div>
            <div class="curis-arrival-slot"><strong>第一位员工</strong><span>CEO 助理会先来到这里</span></div>
          </div>
        </div>
        <div class="curis-arrival-note">
          <div><h2>先不用把一切想清楚。</h2><p>这里现在是空的，但不是空旷。你说出想经营什么，我会陪你把公司、业务和第一支 AI 团队一步步搭起来。</p><form class="curis-arrival-intent"><input aria-label="你的经营想法" placeholder="告诉我，你想先经营什么……" autocomplete="off" /><button type="submit" data-curis-handled="true">开始讲给我听</button></form></div>
          <div class="curis-arrival-steps"><div class="curis-arrival-step"><b>1</b><span>说出你想解决的问题和服务对象</span></div><div class="curis-arrival-step"><b>2</b><span>确认第一条业务要证明的结果</span></div><div class="curis-arrival-step"><b>3</b><span>让 AI 员工接过执行并回来汇报</span></div></div>
          <p class="curis-arrival-quote">“我会替你守住上下文，也会在该安静的时候保持安静。”<br>— Curis · CEO 首席助理</p>
        </div>
      </div>`;
    welcome.insertBefore(arrival, anchor);
    arrival.querySelector('form')?.addEventListener('submit', event => {
      event.preventDefault();
      const value = event.currentTarget.querySelector('input').value.trim();
      const intent = document.getElementById('ceo-intent');
      if (!value || !intent) return;
      intent.value = value;
      writeState({ foundingIntent: value, lastAssistantMessage: '我收到你的经营意图了。先把它整理成公司简报，再一起确认第一条业务。' });
      goToStep(1);
      paintAssistantRuntime(document.getElementById('curis-companion'), syncAssistantRuntime(readState(), 'founding-flow.html'));
      window.setTimeout(() => intent.focus(), 120);
    });
  }

  function initRuntimeBusinessDecision() {
    const page = window.location.pathname.split('/').pop();
    const business = page === 'workspace-runtime-software.html' ? '软件开发' : page === 'workspace-runtime-xhs.html' ? '小红书运营' : page === 'workspace-runtime-shortvideo.html' ? '抖音 / TikTok 运营' : '';
    if (!business || document.querySelector('.curis-runtime-decision-banner')) return;
    const state = readState();
    const platform = business === '小红书运营' ? '小红书' : business === '抖音 / TikTok' ? '抖音 / TikTok' : '';
    const decision = [state.businessArchive, state.businessDecision].filter(Boolean).find(item => item.businessTitle === business || item.platform === platform);
    if (!decision) return;
    const capacityApproved = (state.capacityDecision?.choice === 'approve' || state.capacityDecision?.label === '确认扩容配置')
      && capacityMatchesBusiness(state.capacityDecision, business, platform);
    const copy = {
      continue: ['继续验证中', '当前保持原有投入，等待下一条真实结果再决定是否改变容量。', '回到业务版图', 'business.html'],
      scale: [capacityApproved ? '扩大业务已批准' : '扩大业务等待能力配置', capacityApproved ? 'AI 组织已确认新容量，办公室按新的投入继续运行。' : '先完成 AI 团队容量与交接配置，当前运行不会被静默改变。', '查看 AI 组织', 'ai-organization.html'],
      pause: ['业务已暂停', '当前不再启动新的产出；历史结果、成果和手动回传仍然保留。', '回到经营办公室', 'operating.html'],
      close: ['业务已归档', '该业务停止运行，但历史证据和成果仍可从业务版图与成果库追溯。', '查看业务版图', 'business.html']
    }[decision.choice];
    if (!copy) return;
    const anchor = document.querySelector('main.content .header') || document.querySelector('.commitment-bar');
    if (!anchor?.parentNode) return;
    const banner = document.createElement('section');
    banner.className = 'curis-runtime-decision-banner';
    banner.setAttribute('aria-label', `${business}经营判断状态`);
    banner.innerHTML = `<div class="curis-runtime-decision-copy"><p class="curis-runtime-decision-kicker">业务判断 · ${escapeHtml(business)}</p><h2 class="curis-runtime-decision-title">${escapeHtml(copy[0])}</h2><p class="curis-runtime-decision-note">${escapeHtml(copy[1])}</p></div><button type="button" class="curis-runtime-decision-action" data-curis-handled="true">${escapeHtml(copy[2])} →</button>`;
    anchor.parentNode.insertBefore(banner, anchor.nextSibling);
    banner.querySelector('button').addEventListener('click', () => { window.location.href = copy[3]; });
    const frozen = ['pause', 'close'].includes(decision.choice);
    if (!frozen) return;
    const blockedLabels = page === 'workspace-runtime-shortvideo.html'
      ? ['+ 新建选题', '推进到下一阶段']
      : page === 'workspace-runtime-xhs.html'
        ? ['授权小红书', '调整 AI 能力']
        : page === 'workspace-runtime-software.html'
          ? ['退回修改', '请求现场演示']
          : ['继续运行', '调整责任'];
    document.querySelectorAll('button').forEach(button => {
      const label = button.textContent.trim();
      if (!blockedLabels.some(item => label.includes(item))) return;
      button.disabled = true;
      button.classList.add('curis-runtime-decision-blocked');
      button.title = decision.choice === 'close' ? '业务已归档，不能再启动新的执行' : '业务已暂停，先从经营办公室重新开启';
      button.setAttribute('aria-disabled', 'true');
    });
  }

  function initSoftwareRuntime() {
    if (!window.location.pathname.endsWith('workspace-runtime-software.html')) return;
    const acceptance = document.querySelector('#software-acceptance');
    if (!acceptance || acceptance.dataset.curisBound === 'true') return;
    acceptance.dataset.curisBound = 'true';
    const softwareFeedback = acceptance.querySelector('#software-ceo-feedback');
    if (softwareFeedback && !acceptance.querySelector('#software-evidence-ref')) {
      const valueLabel = document.createElement('label');
      valueLabel.className = 'feedback-label';
      valueLabel.htmlFor = 'software-value-input';
      valueLabel.textContent = '本次已确认业务价值（可选，元）';
      const valueInput = document.createElement('input');
      valueInput.id = 'software-value-input';
      valueInput.type = 'number';
      valueInput.min = '0';
      valueInput.inputMode = 'decimal';
      valueInput.placeholder = '例如：节省时间折算或外部客户验收价值';
      valueInput.style.cssText = 'display:block;width:100%;margin-top:6px;padding:9px 10px;color:var(--text-default,#e2e3e7);background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px;';
      softwareFeedback.insertAdjacentElement('afterend', valueLabel);
      valueLabel.insertAdjacentElement('afterend', valueInput);
      const evidenceLabel = document.createElement('label');
      evidenceLabel.className = 'feedback-label';
      evidenceLabel.htmlFor = 'software-evidence-ref';
      evidenceLabel.textContent = '验收证据引用（可选）';
      const evidenceType = document.createElement('select');
      evidenceType.id = 'software-evidence-type';
      evidenceType.setAttribute('aria-label', '证据类型');
      evidenceType.innerHTML = '<option>测试报告 / 提交记录</option><option>截图 / 图片</option><option>本地文件</option><option>客户验收 / 回访记录</option><option>平台页面 / 数据导出</option><option>其他</option>';
      evidenceType.style.cssText = 'display:block;width:100%;margin-top:6px;padding:9px 10px;color:var(--text-default,#e2e3e7);background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px;';
      const evidenceInput = document.createElement('input');
      evidenceInput.id = 'software-evidence-ref';
      evidenceInput.type = 'text';
      evidenceInput.placeholder = '例如：本地验收记录 / 提交号 / 测试报告路径';
      evidenceInput.style.cssText = 'display:block;width:100%;margin-top:6px;padding:9px 10px;color:var(--text-default,#e2e3e7);background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px;';
      softwareFeedback.insertAdjacentElement('afterend', evidenceLabel);
      evidenceLabel.insertAdjacentElement('afterend', evidenceType);
      evidenceType.insertAdjacentElement('afterend', evidenceInput);
    }
    const header = document.querySelector('main.content .header');
    if (header && !header.querySelector('[data-software-change]')) {
      const actions = document.createElement('div');
      actions.className = 'actions curis-software-actions';
      actions.innerHTML = '<button type="button" data-software-change>提出产品变更</button>';
      header.appendChild(actions);
      actions.querySelector('[data-software-change]').addEventListener('click', () => openFormDialog({
        title: '提出产品变更',
        description: '把 CEO 在真实使用中发现的问题交给产品 AI。研发办公室会先整理影响，再决定是否进入下一版本。',
        submitLabel: '交给产品 AI',
        fields: [
          { name: 'request', label: '想改善什么', type: 'textarea', placeholder: '例如：创建公司后第一眼看不到今天必须决定的事情', required: true },
          { name: 'reason', label: '为什么重要', type: 'textarea', placeholder: '例如：会影响 CEO 是否能快速开始经营', required: true },
          { name: 'priority', label: '优先级', type: 'select', options: ['本周期处理', '下一周期评估', '先记录观察'] }
        ],
        onSubmit: values => {
          const current = readState();
          const changes = Array.isArray(current.softwareChangeRequests) ? current.softwareChangeRequests : [];
          const record = { ...values, at: new Date().toISOString(), status: '待产品分析' };
          writeState({ softwareChangeRequests: [...changes, record].slice(-20), lastAssistantMessage: `产品变更“${values.request}”已交给产品 AI，下一步会先整理影响和验收标准。`, lastAssistantHandoff: { label: '研发办公室', route: 'workspace-runtime-software.html', message: '产品变更待分析' } });
          showToast('产品变更已进入研发办公室');
        }
      }));
    }
    if (!document.querySelector('.curis-software-value-card')) {
      const valueCard = document.createElement('section');
      valueCard.className = 'card curis-software-value-card';
      valueCard.innerHTML = '<div class="curis-software-value-head"><div><h2>本周期业务价值与成本</h2><p class="card-note">研发成果要回到经营账：节省的时间、可运行版本和 CEO 验收，都会成为可追踪价值。</p></div><button type="button" data-runtime-action="finance">查看经营账</button></div><div class="curis-software-value-grid"><div><span>节省研发时间</span><strong data-software-value="hours">120 小时</strong><small data-software-value-note="hours">估算 · 基线对比 · QA 与回归</small></div><div><span>AI 与工具成本</span><strong data-software-value="cost">¥1,920</strong><small data-software-value-note="cost">估算 · 模型调用 · CI · 浏览器</small></div><div><span>可归因价值</span><strong data-software-value="value">¥14,400</strong><small data-software-value-note="value">估算 · CEO 验收后确认</small></div><div><span>本周期 ROI</span><strong data-software-value="roi">—</strong><small data-software-value-note="roi">等待 CEO 验收</small></div></div><p class="curis-software-value-note">外部客户验收或真实使用反馈回来后，价值口径才会从“估算”变成“已验证”。</p>';
      acceptance.parentNode.insertBefore(valueCard, acceptance);
      const style = document.createElement('style');
      style.textContent = '.curis-software-value-card{margin-bottom:16px}.curis-software-value-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.curis-software-value-head h2{margin:0;font-size:14px}.curis-software-value-head button{padding:8px 11px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px;cursor:pointer;white-space:nowrap}.curis-software-value-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;margin-top:14px;background:var(--border-neutral-l1,rgba(224,226,242,.1));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px;overflow:hidden}.curis-software-value-grid>div{display:grid;gap:5px;padding:13px;background:var(--bg-base-secondary,#202226)}.curis-software-value-grid span,.curis-software-value-grid small{color:var(--text-secondary,#a4a7af);font-size:10px}.curis-software-value-grid strong{font-size:17px;letter-spacing:-.02em}.curis-software-value-note{margin:12px 0 0;color:var(--text-tertiary,#777c86);font-size:10px;line-height:1.5}@media(max-width:760px){.curis-software-value-grid{grid-template-columns:repeat(2,1fr)}.curis-software-value-head{flex-direction:column}}';
      document.head.appendChild(style);
    }
    if (!document.querySelector('.curis-software-change-queue')) {
      const queue = document.createElement('section');
      queue.className = 'card curis-software-change-queue';
      queue.innerHTML = '<h2>CEO 产品变更</h2><p class="card-note">真实使用中的问题会先进入产品分析，不会直接打断当前交付。</p><div data-software-change-list></div>';
      acceptance.parentNode.insertBefore(queue, acceptance);
      const renderChanges = () => {
        const list = queue.querySelector('[data-software-change-list]');
        const items = readState().softwareChangeRequests || [];
        list.innerHTML = items.length ? items.slice(-5).reverse().map(item => `<div class="curis-software-change-item"><strong>${escapeHtml(item.request)}</strong><span>${escapeHtml(item.priority || '下一周期评估')} · ${escapeHtml(item.status || '待产品分析')}</span></div>`).join('') : '<p class="card-note">还没有新的产品变更，CEO 的真实反馈会在这里形成下一周期输入。</p>';
      };
      renderChanges();
      window.addEventListener('curis-state-changed', renderChanges);
      const style = document.createElement('style');
      style.textContent = '.curis-software-change-queue{margin-bottom:16px}.curis-software-change-item{display:flex;align-items:center;justify-content:space-between;gap:14px;padding:10px 0;border-top:1px solid var(--line)}.curis-software-change-item:first-child{border-top:0}.curis-software-change-item strong{font-size:11px;font-weight:500}.curis-software-change-item span{color:var(--muted);font-size:10px;white-space:nowrap}';
      document.head.appendChild(style);
    }
    const renderValue = () => {
      const current = readState();
      const card = document.querySelector('.curis-software-value-card');
      if (!card) return;
      const accepted = current.softwareAcceptance?.choice === 'accept';
      const costs = (Array.isArray(current.financeCosts) ? current.financeCosts : []).filter(item => /软件|Curis|研发/.test(String(item.business || ''))).reduce((sum, item) => sum + Number(item.amount || 0), 0);
      const outcome = (Array.isArray(current.outcomeAttributions) ? current.outcomeAttributions : []).filter(item => item.business === '软件开发').sort((a, b) => String(b.at || '').localeCompare(String(a.at || '')))[0];
      const value = Number(outcome?.value || 0);
      const set = (key, valueText, noteText) => { card.querySelector(`[data-software-value="${key}"]`)?.replaceChildren(document.createTextNode(valueText)); card.querySelector(`[data-software-value-note="${key}"]`)?.replaceChildren(document.createTextNode(noteText)); };
      set('hours', accepted ? '120 小时' : '—', accepted ? '已验证 · QA 与回归' : '等待真实基线与 CEO 验收');
      set('cost', costs ? `¥${costs.toLocaleString()}` : '—', costs ? '已记录 · 模型调用 · CI · 浏览器' : '暂无成本记录');
      set('value', accepted && value ? `¥${value.toLocaleString()}` : '—', accepted && value ? '已验证 · CEO 真实使用验收' : '等待验收与价值归因');
      set('roi', accepted && value && costs ? `${(value / costs).toFixed(1)}x` : '—', accepted && value && costs ? '已验证 · 价值 / 实际成本' : '等待验收与成本回写');
    };
    const render = () => {
      const result = readState().softwareAcceptance;
      renderValue();
      const status = document.querySelector('#software-runtime-status');
      const handoffTitle = document.querySelector('#software-handoff-title');
      const handoffNote = document.querySelector('#software-handoff-note');
      const title = document.querySelector('#software-acceptance-title');
      const note = document.querySelector('#software-acceptance-note');
      acceptance.classList.toggle('is-accepted', result?.choice === 'accept');
      const flowStages = [...document.querySelectorAll('.flow .stage')];
      const activeStage = result?.choice === 'accept' ? 5 : result?.choice === 'rework' ? 2 : result?.choice === 'demo' ? 4 : 3;
      flowStages.forEach((stage, index) => stage.classList.toggle('current', index === activeStage));
      if (!result) return;
      const copy = {
        accept: ['Curis v0.2 已验收', 'CEO 已通过真实使用，研发办公室开始准备下一次软件增量。', '验收已记录', '结果已回到公司，下一周期会从 CEO 反馈继续。'],
        rework: ['等待修改后再次验收', 'CEO 退回了当前版本，研发 AI 需要先处理反馈再提交。', '需要返工', '问题已经交给研发 AI，当前版本不会进入发布。'],
        demo: ['等待 CEO 现场演示', 'CEO 要求先由研发 AI 带着走一遍完整路径。', '演示已请求', '演示完成后，CEO 助理会重新打开验收入口。']
      }[result.choice];
      if (!copy) return;
      if (status) status.textContent = copy[0];
      if (handoffTitle) handoffTitle.textContent = copy[2];
      if (handoffNote) handoffNote.textContent = copy[1];
      if (title) title.textContent = copy[2];
      if (note) note.textContent = result.feedback ? `CEO 反馈：${result.feedback}` : copy[3];
    };
    render();
    acceptance.querySelectorAll('[data-software-choice]').forEach(button => button.addEventListener('click', () => {
      const choice = button.dataset.softwareChoice;
      const feedback = acceptance.querySelector('#software-ceo-feedback')?.value.trim() || '';
      const evidenceRef = acceptance.querySelector('#software-evidence-ref')?.value.trim() || '';
      const evidenceType = acceptance.querySelector('#software-evidence-type')?.value || '其他';
      const labels = { accept: '验收通过', rework: '退回修改', demo: '请求现场演示' };
      const softwareRun = (readState().calendarEvents || []).filter(item => item.route === 'workspace-runtime-software.html' && ['waiting_ceo', 'acknowledged', 'failed'].includes(item.status)).sort((a, b) => String(b.finishedAt || '').localeCompare(String(a.finishedAt || '')))[0];
      const value = Number(acceptance.querySelector('#software-value-input')?.value || 0);
      const attribution = choice === 'accept' ? recordOutcomeAttribution({ business: '软件开发', route: 'workspace-runtime-software.html', runId: softwareRun?.runId || 'manual', runIds: softwareRun ? [softwareRun.runId] : ['manual'], value, status: '已验证价值', source: 'CEO 真实使用验收', evidenceRef, evidenceType }) : {};
      writeState({
        softwareAcceptance: { choice, label: labels[choice], feedback, value, evidenceRef, evidenceType, at: new Date().toISOString() },
        ...attribution,
        lastAssistantMessage: choice === 'accept' ? 'CEO 已验收 Curis v0.2。研发办公室会把这次真实使用反馈带入下一周期。' : choice === 'rework' ? 'CEO 已退回 Curis v0.2。研发 AI 会先处理反馈，完成后重新提交验收。' : 'CEO 要求现场演示 Curis v0.2。我会让研发 AI 准备完整路径并回来汇报。',
        lastAssistantHandoff: { label: 'CEO 工作台', route: 'ceo-desk.html', message: labels[choice] }
      });
      resolveScheduledRuns(softwareRun ? [softwareRun.runId] : [], { outcomeId: attribution.lastOutcomeAttribution?.id, resolutionNote: `CEO 已完成软件验收：${labels[choice]}${feedback ? ` · ${feedback}` : ''}` });
      render();
      showToast(`已记录：${labels[choice]}`);
    }));
  }

  function initSoftwareNextCycle() {
    if (!window.location.pathname.endsWith('workspace-runtime-software.html') || document.querySelector('.curis-software-next-cycle')) return;
    const acceptance = document.querySelector('#software-acceptance');
    if (!acceptance?.parentNode) return;
    const panel = document.createElement('section');
    panel.className = 'card curis-software-next-cycle';
    panel.setAttribute('aria-labelledby', 'curis-software-next-cycle-title');
    panel.innerHTML = '<div class="curis-software-next-cycle-head"><div><p>交付之后</p><h2 id="curis-software-next-cycle-title">下一版本承接</h2><p data-software-next-note>CEO 完成真实验收后，研发办公室会把反馈转成下一版本范围，不让验收结果停在一条记录里。</p></div><span data-software-next-state>等待 CEO 验收</span></div><div class="curis-software-next-cycle-body"><div><span>当前版本</span><strong data-software-next-version>Curis v0.2</strong></div><div><span>下一步责任</span><strong data-software-next-owner>等待验收结果</strong></div><div><span>验收反馈</span><p data-software-next-feedback>还没有 CEO 反馈。</p></div></div><div class="curis-software-next-cycle-actions"><button type="button" data-software-next="intent">形成下一版本意图</button><button type="button" data-software-next="schedule">安排下一次验收</button><button type="button" data-software-next="changes">查看产品变更</button></div>';
    acceptance.parentNode.insertBefore(panel, acceptance);
    const style = document.createElement('style');
    style.textContent = '.curis-software-next-cycle{margin-bottom:16px}.curis-software-next-cycle-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.curis-software-next-cycle-head p:first-child{margin:0 0 5px;color:var(--text-secondary,#a4a7af);font-size:10px;letter-spacing:.06em}.curis-software-next-cycle-head h2{margin:0;font-size:15px}.curis-software-next-cycle-head p[data-software-next-note]{max-width:680px;margin:6px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.5}.curis-software-next-cycle-head>span{padding:5px 7px;color:var(--text-secondary,#a4a7af);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font-size:10px;white-space:nowrap}.curis-software-next-cycle-body{display:grid;grid-template-columns:1fr 1fr 1.4fr;gap:1px;margin-top:14px;background:var(--border-neutral-l1,rgba(224,226,242,.1));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px;overflow:hidden}.curis-software-next-cycle-body>div{padding:11px;background:var(--bg-base-secondary,#202226)}.curis-software-next-cycle-body span{display:block;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-software-next-cycle-body strong{display:block;margin-top:5px;font-size:12px}.curis-software-next-cycle-body p{margin:5px 0 0;color:var(--text-secondary,#a4a7af);font-size:10px;line-height:1.45}.curis-software-next-cycle-actions{display:flex;justify-content:flex-end;gap:7px;margin-top:11px}.curis-software-next-cycle-actions button{padding:7px 9px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}.curis-software-next-cycle-actions button:first-child{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}.curis-software-next-cycle-actions button:disabled{opacity:.45;cursor:not-allowed}@media(max-width:700px){.curis-software-next-cycle-head{flex-direction:column}.curis-software-next-cycle-body{grid-template-columns:1fr}.curis-software-next-cycle-actions{align-items:stretch;flex-direction:column}.curis-software-next-cycle-actions button{width:100%}}';
    document.head.appendChild(style);
    const render = () => {
      const state = readState();
      const result = state.softwareAcceptance;
      const plan = state.softwareNextCycle;
      const stateLabel = result?.choice === 'accept' ? '已验收 · 可进入下一版本' : result?.choice === 'rework' ? '退回修改 · 等待返工' : result?.choice === 'demo' ? '等待现场演示' : '等待 CEO 验收';
      panel.querySelector('[data-software-next-state]').textContent = plan?.status || stateLabel;
      panel.querySelector('[data-software-next-owner]').textContent = plan?.goal || (result?.choice === 'accept' ? '产品 AI 整理 v0.3 范围' : result?.choice === 'rework' ? '研发 AI 处理 CEO 反馈' : result?.choice === 'demo' ? '研发 AI 准备完整演示' : '等待验收结果');
      panel.querySelector('[data-software-next-feedback]').textContent = result?.feedback || '还没有 CEO 反馈；验收时可以补充真实使用感受。';
      const ready = Boolean(result);
      panel.querySelector('[data-software-next="intent"]').disabled = !ready;
      panel.querySelector('[data-software-next="schedule"]').disabled = !ready;
    };
    const openIntent = () => {
      const result = readState().softwareAcceptance;
      if (!result) return showToast('先完成 CEO 验收，再形成下一版本意图');
      openFormDialog({ title: '形成下一版本意图', description: '把 CEO 的真实使用反馈转成产品范围和验收路径，交给产品 AI 与研发办公室继续承接。', submitLabel: '保存下一版本', fields: [{ name: 'goal', label: '下一版本要改善什么', type: 'textarea', value: result.feedback || '', placeholder: '例如：让 CEO 在第一眼看到所有待决策事项，并减少跨页面寻找。', required: true }, { name: 'acceptancePath', label: '下一次验收路径', type: 'textarea', placeholder: '例如：创建公司 → 查看今日经营 → 打开业务办公室 → 完成一次结果回传', required: true }, { name: 'priority', label: '优先级', type: 'select', options: ['本周期处理', '下一周期评估', '先记录观察'] }], onSubmit: values => { const current = readState(); const changes = Array.isArray(current.softwareChangeRequests) ? current.softwareChangeRequests : []; const change = result.feedback ? { request: result.feedback, reason: '来自 CEO 真实验收', priority: values.priority, source: 'CEO 验收', at: new Date().toISOString(), status: '待产品分析' } : null; writeState({ softwareNextCycle: { ...values, status: '已形成下一版本意图', at: new Date().toISOString() }, ...(change ? { softwareChangeRequests: [...changes, change].slice(-20) } : {}), lastAssistantMessage: `下一版本意图已形成：${values.goal}。产品 AI 会先整理影响和验收标准。`, lastAssistantHandoff: { label: '研发办公室', route: 'workspace-runtime-software.html', message: '下一版本意图已形成' } }); render(); showToast('下一版本意图已保存'); } });
    };
    const schedule = () => {
      const state = readState();
      if (!state.softwareAcceptance) return showToast('先完成 CEO 验收，再安排下一次验收');
      openFormDialog({ title: '安排下一次软件验收', description: '把版本目标、验收路径和时间写入公司日历，研发办公室会按检查点回报。', submitLabel: '保存验收排期', fields: [{ name: 'schedule', label: '验收时间', placeholder: '例如：周五 14:00', required: true }, { name: 'checkpoint', label: '验收检查点', type: 'textarea', placeholder: '例如：完成创建公司和一次真实结果回传，确认 CEO 是否能独立完成', required: true }], onSubmit: values => { let schedules = []; try { schedules = JSON.parse(localStorage.getItem('curis-schedules') || '[]'); } catch (_) {} const item = { id: `software-review-${Date.now()}`, name: '研发 · 下一次 CEO 验收', business: '软件开发', schedule: values.schedule, owner: 'QA AI', task: `${values.checkpoint}；失败时暂停发布并回到研发办公室`, estimatedCost: 55, route: 'workspace-runtime-software.html', enabled: true }; localStorage.setItem('curis-schedules', JSON.stringify([...schedules, item].slice(-24))); writeState({ softwareNextCycle: { ...(readState().softwareNextCycle || {}), ...values, status: '验收已排期', scheduledAt: new Date().toISOString() }, lastAssistantMessage: `下一次软件验收已排期：${values.schedule}。QA AI 会按检查点准备证据包。`, lastAssistantHandoff: { label: '公司日历', route: 'calendar.html', message: '软件验收已排期' } }); render(); showToast('下一次验收已排期'); } });
    };
    panel.addEventListener('click', event => { const button = event.target.closest('[data-software-next]'); if (!button) return; if (button.dataset.softwareNext === 'intent') openIntent(); if (button.dataset.softwareNext === 'schedule') schedule(); if (button.dataset.softwareNext === 'changes') document.querySelector('.curis-software-change-queue')?.scrollIntoView({ behavior: 'smooth', block: 'center' }); });
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initSoftwareOfficePresence() {
    if (!window.location.pathname.endsWith('workspace-runtime-software.html') || document.querySelector('.curis-software-presence')) return;
    const goal = document.querySelector('.goal');
    if (!goal) return;
    const initialState = readState();
    const runtimeRuns = (initialState.calendarEvents || []).filter(item => item.route === 'workspace-runtime-software.html');
    const accepted = initialState.softwareAcceptance?.choice === 'accept';
    const liveLabel = accepted ? 'CEO 已验收 · 进入下一周期' : runtimeRuns.length ? '真实运行已记录 · 等待 CEO 验收' : '岗位已配置 · 等待首轮研发运行';
    const teamStates = accepted
      ? ['已完成本轮范围', '已提交可运行版本', `${runtimeRuns.length} 次真实运行已记录`, '已确认可用']
      : runtimeRuns.length
        ? ['本轮范围已记录', '可运行版本已提交', `${runtimeRuns.length} 次运行已记录`, '等待 CEO 真实使用']
        : ['等待 CEO 提出产品意图', '等待研发范围确认', '等待真实回归记录', '等待 CEO 验收'];
    const presence = document.createElement('section');
    presence.className = 'curis-office-presence curis-software-presence';
    presence.setAttribute('aria-label', '研发办公室运行现场');
    presence.innerHTML = `<div class="curis-office-presence-head"><div><p class="curis-office-presence-kicker">部门办公室 · 研发</p><h2 class="curis-office-presence-title">研发办公室正在交付 Curis v0.2</h2><p class="curis-office-presence-subtitle">当前目标：通过 CEO 真实验收，再把反馈带入下一周期</p></div><span class="curis-office-live">${liveLabel}</span></div><div class="curis-office-presence-body"><div class="curis-office-team"><button class="curis-office-person" type="button" data-software-office-stage="product"><span class="curis-office-person-top"><span class="curis-office-avatar">P</span><span class="curis-office-person-name">产品 AI</span></span><span class="curis-office-person-state">${teamStates[0]}</span></button><button class="curis-office-person" type="button" data-software-office-stage="engineering"><span class="curis-office-person-top"><span class="curis-office-avatar">E</span><span class="curis-office-person-name">研发 AI</span></span><span class="curis-office-person-state">${teamStates[1]}</span></button><button class="curis-office-person" type="button" data-software-office-stage="qa"><span class="curis-office-person-top"><span class="curis-office-avatar">Q</span><span class="curis-office-person-name">QA AI</span></span><span class="curis-office-person-state">${teamStates[2]}</span></button><button class="curis-office-person waiting" type="button" data-software-office-stage="acceptance"><span class="curis-office-person-top"><span class="curis-office-avatar">CEO</span><span class="curis-office-person-name">CEO</span></span><span class="curis-office-person-state">${teamStates[3]}</span></button></div><div class="curis-office-route"><p class="curis-office-route-title">今日交接动线</p><div class="curis-office-route-list"><button class="curis-office-route-step" type="button" data-software-office-stage="product">产品</button><span class="curis-office-route-arrow">→</span><button class="curis-office-route-step" type="button" data-software-office-stage="engineering">研发</button><span class="curis-office-route-arrow">→</span><button class="curis-office-route-step" type="button" data-software-office-stage="qa">QA</button><span class="curis-office-route-arrow">→</span><button class="curis-office-route-step" type="button" data-software-office-stage="acceptance">CEO 验收</button></div><p class="curis-office-route-note">点击一位员工或阶段，直接查看这一步的输入、产出与验收责任。</p></div></div>`;
    goal.parentNode.insertBefore(presence, goal.nextSibling);
    const stages = [...document.querySelectorAll('.flow .stage')];
    const targets = { product: stages[1], engineering: stages[2], qa: stages[3], acceptance: stages[4] };
    presence.querySelectorAll('[data-software-office-stage]').forEach(node => node.addEventListener('click', () => {
      const target = targets[node.dataset.softwareOfficeStage];
      if (!target) return;
      presence.querySelectorAll('.curis-office-person.is-selected,.curis-office-route-step.is-selected').forEach(item => item.classList.remove('is-selected'));
      node.classList.add('is-selected');
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      target.classList.add('curis-focus');
      window.setTimeout(() => target.classList.remove('curis-focus'), 1200);
    }));
  }

  function initDepartmentRuntime() {
    if (!window.location.pathname.endsWith('workspace-runtime-department.html')) return;
    const state = readState();
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    if (!department?.name || !commitment?.name) return;
    const title = document.querySelector('#department-runtime-title');
    const subtitle = document.querySelector('#department-runtime-subtitle');
    const goal = document.querySelector('#department-runtime-goal');
    const outcome = document.querySelector('#department-runtime-outcome');
    const status = document.querySelector('#department-runtime-status');
    const owner = document.querySelector('#department-runtime-owner');
    const crumb = document.querySelector('#department-crumb-name');
    const nav = document.querySelector('#department-nav-name');
    const handoffTitle = document.querySelector('#department-runtime-handoff-title');
    const handoffNote = document.querySelector('#department-runtime-handoff-note');
    const commitmentState = document.querySelector('#department-runtime-commitment-state');
    const executionState = document.querySelector('#department-runtime-execution-state');
    const resultState = document.querySelector('#department-runtime-result-state');
    const resultCount = document.querySelector('#department-runtime-result-count');
    const resultLog = document.querySelector('#department-runtime-result-log');
    const feedbackTitle = document.querySelector('#department-runtime-feedback-title');
    const feedbackNote = document.querySelector('#department-runtime-feedback-note');
    const resultStatus = document.querySelector('#department-result-status');
    const resultSource = document.querySelector('#department-result-source');
    const resultNote = document.querySelector('#department-result-note');
    const history = () => Array.isArray(readState().departmentResultHistory) ? readState().departmentResultHistory : (readState().departmentResult ? [readState().departmentResult] : []);
    const render = () => {
      const current = readState();
      const activeCommitment = current.departmentCommitment || commitment;
      const latest = current.departmentResult;
      const records = history();
      const paused = activeCommitment.status === 'paused';
      if (title) title.textContent = department.name;
      if (nav) nav.textContent = department.name;
      if (crumb) crumb.textContent = commitment.name;
      if (subtitle) subtitle.textContent = `${department.name} 正在承接“${commitment.name}”。这里展示团队如何把责任变成执行、结果和下一次 CEO 判断。`;
      if (goal) goal.textContent = commitment.name;
      if (outcome) outcome.textContent = commitment.outcome || '等待 CEO 确认这项责任的验收结果。';
      if (status) { status.textContent = paused ? '已暂停' : latest?.status === '已验证价值' ? '结果已验证' : latest?.status === '结果异常' ? '结果异常' : latest ? '等待下一次判断' : '运行中'; status.style.color = paused ? 'var(--bad)' : latest?.status === '已验证价值' ? 'var(--ok)' : 'var(--warn)'; }
      if (owner) owner.innerHTML = `负责人<br /><strong>业务工程 AI</strong><br /><span>${paused ? '回报：已暂停，等待 CEO 重启' : latest ? '回报：已记录，等待下一步' : '回报：等待首轮执行'}</span>`;
      if (handoffTitle) handoffTitle.textContent = paused ? '责任已暂停' : latest ? '结果已回到 CEO 助理' : '首项责任正在执行';
      if (handoffNote) handoffNote.textContent = paused ? '不会继续消耗团队能力；历史责任和结果仍然保留。' : latest ? `最近回报：${latest.note || 'CEO 已记录结果状态。'} 助理会据此准备下一步。` : '执行 AI 按批准范围推进，反馈 AI 等待第一条真实回报。';
      if (commitmentState) commitmentState.textContent = paused ? '已暂停' : '已批准';
      if (executionState) executionState.textContent = paused ? '已停止' : latest ? '已回报' : '执行中';
      if (resultState) resultState.textContent = latest?.status || '待补充';
      if (resultCount) resultCount.textContent = String(records.length);
      if (feedbackTitle) feedbackTitle.textContent = paused ? '责任已暂停' : latest ? `最近回报：${latest.status}` : '等待第一条回报';
      if (feedbackNote) feedbackNote.textContent = paused ? '如需继续，先回到 CEO 工作台重新确认资源与责任。' : latest ? '结果已经写入责任周期，CEO 可以继续运行、调整或暂停。' : '结果回到公司后，CEO 再决定继续、调整或暂停，不让 AI 自己宣布成功。';
      if (resultLog) {
        resultLog.replaceChildren();
        records.slice().reverse().forEach(record => {
          const item = document.createElement('div');
          item.className = 'result-item';
          const strong = document.createElement('strong');
          strong.textContent = `${record.status} · ${record.time || '刚刚'}`;
          const copy = document.createElement('div');
          copy.textContent = `${record.source ? `来源：${record.source} · ` : ''}${record.note || 'CEO 未补充说明'}`;
          item.append(strong, copy);
          resultLog.appendChild(item);
        });
      }
    };
    render();
    const feedback = document.querySelector('#department-runtime-feedback');
    if (!feedback || feedback.dataset.curisBound === 'true') return;
    feedback.dataset.curisBound = 'true';
    feedback.querySelector('[data-department-result="save"]')?.addEventListener('click', () => {
      const note = resultNote?.value.trim() || '';
      const statusValue = resultStatus?.value || '待验证';
      const source = resultSource?.value || 'CEO 手动补录';
      if (!note) return showToast('请先写下这次真实回报，再记录结果');
      const record = { status: statusValue, source, note, time: new Date().toLocaleString('zh-CN', { hour: '2-digit', minute: '2-digit' }), at: new Date().toISOString() };
      const current = readState();
      const records = Array.isArray(current.departmentResultHistory) ? current.departmentResultHistory : (current.departmentResult ? [current.departmentResult] : []);
      writeState({ departmentResult: record, departmentResultHistory: [...records, record].slice(-12), departmentCommitment: { ...(current.departmentCommitment || commitment), status: 'active' }, lastAssistantMessage: `“${commitment.name}”已有一条真实回报：${statusValue}。我会把 CEO 的说明带回${department.name}，准备下一步判断。`, lastAssistantHandoff: { label: 'CEO 工作台', route: 'ceo-desk.html', message: '部门责任结果已回报' } });
      if (resultNote) resultNote.value = '';
      render();
      showToast('结果已记录，CEO 助理会在下一次经营汇报中带上它');
    });
    feedback.querySelector('[data-department-result="continue"]')?.addEventListener('click', () => {
      const current = readState();
      const cycle = Number(current.departmentCommitment?.cycle || 1) + 1;
      writeState({ departmentCommitment: { ...(current.departmentCommitment || commitment), status: 'active', cycle }, lastAssistantMessage: `你已决定继续运行“${commitment.name}”。我会让${department.name}进入第 ${cycle} 个责任周期，并在下一次回报回来后再请你判断。`, lastAssistantHandoff: { label: 'CEO 工作台', route: 'ceo-desk.html', message: '部门责任继续运行' } });
      render();
      showToast(`已进入第 ${cycle} 个责任周期`);
    });
    feedback.querySelector('[data-department-result="revise"]')?.addEventListener('click', () => {
      const current = readState();
      writeState({ departmentCommitment: { ...(current.departmentCommitment || commitment), status: 'pending_revision' }, lastAssistantMessage: `你要求调整“${commitment.name}”。我会把责任带回工作空间搭建现场，保留已有结果作为修改依据。`, lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '部门责任需要调整' } });
      showToast('已回到工作空间搭建，准备调整责任');
      window.location.href = 'workspace-studio.html';
    });
    feedback.querySelector('[data-department-result="pause"]')?.addEventListener('click', () => {
      const current = readState();
      writeState({ departmentCommitment: { ...(current.departmentCommitment || commitment), status: 'paused' }, lastAssistantMessage: `你已暂停“${commitment.name}”。我会保留已有证据，并把资源释放情况带回经营办公室。`, lastAssistantHandoff: { label: '经营办公室', route: 'operating.html', message: '部门责任已暂停' } });
      render();
      showToast('这项责任已暂停，历史结果已保留');
    });
  }

  function initOfficePresence() {
    if (!window.location.pathname.endsWith('workspace-runtime-shortvideo.html') || document.querySelector('.curis-office-presence')) return;
    const anchor = document.querySelector('.commitment-bar');
    if (!anchor) return;
    const presence = document.createElement('section');
    presence.className = 'curis-office-presence';
    presence.setAttribute('aria-label', '内容办公室运行现场');
    presence.innerHTML = `
      <div class="curis-office-presence-head"><div><p class="curis-office-presence-kicker">部门办公室 · 抖音 / TikTok 运营</p><h2 class="curis-office-presence-title">抖音 / TikTok 制作团队正在工作</h2><p class="curis-office-presence-subtitle">当前目标：稳定产出并验证内容结果</p></div><span class="curis-office-live">4 位 AI 员工在线 · 2 项待 CEO 验收</span></div>
      <div class="curis-office-presence-body">
        <div class="curis-office-team" aria-label="AI 员工当前状态">
          <button class="curis-office-person" type="button" data-office-stage="topic"><span class="curis-office-person-top"><span class="curis-office-avatar">G</span><span class="curis-office-person-name">增长 AI</span></span><span class="curis-office-person-state">正在找下一条选题</span></button>
          <button class="curis-office-person" type="button" data-office-stage="script"><span class="curis-office-person-top"><span class="curis-office-avatar">C</span><span class="curis-office-person-name">内容 AI</span></span><span class="curis-office-person-state">正在打磨脚本 v2</span></button>
          <button class="curis-office-person" type="button" data-office-stage="shoot"><span class="curis-office-person-top"><span class="curis-office-avatar">V</span><span class="curis-office-person-name">视频 AI</span></span><span class="curis-office-person-state">等待素材确认</span></button>
          <button class="curis-office-person waiting" type="button" data-office-stage="review"><span class="curis-office-person-top"><span class="curis-office-avatar">CEO</span><span class="curis-office-person-name">CEO</span></span><span class="curis-office-person-state">今天 18:00 前验收</span></button>
        </div>
        <div class="curis-office-route"><p class="curis-office-route-title">今日交接动线</p><div class="curis-office-route-list"><button class="curis-office-route-step" type="button" data-office-stage="topic">策略</button><span class="curis-office-route-arrow">→</span><button class="curis-office-route-step" type="button" data-office-stage="script">脚本</button><span class="curis-office-route-arrow">→</span><button class="curis-office-route-step" type="button" data-office-stage="shoot">制作</button><span class="curis-office-route-arrow">→</span><button class="curis-office-route-step" type="button" data-office-stage="review">CEO 验收</button></div><p class="curis-office-route-note">点击一位员工或一个阶段，直接进入当前工作的执行现场。</p></div>
      </div>`;
    const decision = readState().lastDecision;
    if (decision?.choice === 'approve') {
      presence.querySelector('.curis-office-presence-title').textContent = '抖音 / TikTok 制作团队正在执行 Runtime v1.1';
      presence.querySelector('.curis-office-presence-subtitle').textContent = 'CEO 已批准 · 当前目标：完成首周产出并回收真实结果';
      presence.querySelector('.curis-office-live').textContent = '4 位 AI 员工在线 · 首周检查点进行中';
      presence.querySelector('.curis-office-route-note').textContent = 'CEO 的批准已传给团队；点击一位员工或一个阶段，查看它正在怎样执行。';
    }
    anchor.parentNode.insertBefore(presence, anchor);
    presence.querySelectorAll('[data-office-stage]').forEach(node => node.addEventListener('click', () => {
      const stage = document.querySelector(`.stage[data-stage="${node.dataset.officeStage}"]`);
      if (!stage) return;
      document.querySelectorAll('.curis-office-person.is-selected').forEach(item => item.classList.remove('is-selected'));
      node.classList.add('is-selected');
      stage.scrollIntoView({ behavior: 'smooth', block: 'center' });
      stage.classList.add('curis-focus');
      window.setTimeout(() => stage.classList.remove('curis-focus'), 1400);
    }));
  }

  function getRunOptions(route) {
    const runs = (readState().calendarEvents || []).filter(item => item.route === route).sort((a, b) => String(b.finishedAt || b.at || '').localeCompare(String(a.finishedAt || a.at || '')));
    return [{ value: 'manual', label: '未指定运行 · CEO 手动回传' }, ...runs.slice(0, 8).map(run => ({ value: run.runId, label: `${run.time || '最近运行'} · ${run.owner || '负责人未登记'} · ${run.output || run.title || '运行记录'}` }))];
  }

  function runLabelForState(state, runId, runIds) {
    const ids = (Array.isArray(runIds) ? runIds : [runId]).filter(id => id && id !== 'manual');
    if (!ids.length) return '未指定运行';
    const labels = ids.map(id => { const run = (state.calendarEvents || []).find(item => item.runId === id); return run ? (run.time || run.title || '运行记录') : `运行 ${id}`; });
    return `关联 ${labels.slice(0, 3).join('、')}${labels.length > 3 ? ` 等 ${labels.length} 次` : ''}`;
  }

  function recordOutcomeAttribution({ business, route, runId = 'manual', runIds, value = 0, status = '数据待验证', source = 'CEO 手动回传', evidenceRef = '', evidenceType = '其他', at = new Date().toISOString() }) {
    const current = readState();
    const runs = (current.calendarEvents || []).filter(item => item.route === route).sort((a, b) => String(b.finishedAt || b.at || '').localeCompare(String(a.finishedAt || a.at || '')));
    const selectedRunIds = [...new Set((Array.isArray(runIds) ? runIds : [runId]).filter(id => id && id !== 'manual'))];
    const selectedRuns = selectedRunIds.map(id => runs.find(item => item.runId === id)).filter(Boolean);
    const run = selectedRuns[0] || (runId === 'manual' ? null : runs.find(item => item.runId === runId));
    const capability = run?.capability || current.capabilityRuntimeByContext?.[route] || { model: '手动录入', agent: 'CEO 手动回传', skills: [], tools: [], connector: '手动录入' };
    const contributors = selectedRuns.map(item => ({ runId: item.runId, agent: item.capability?.agent || item.owner || '未指定负责人', model: item.capability?.model || '模型未登记', cost: Number(item.cost || 0) }));
    const singleAllocation = contributors.length === 1 ? [{ runId: contributors[0].runId, agent: contributors[0].agent, weight: 100 }] : [];
    const evidence = evidenceRef ? { id: `evidence-${Date.now()}`, type: evidenceType, ref: evidenceRef, version: 'v1', capturedAt: at, status: '待 CEO 采用' } : null;
    const attribution = { id: `outcome-${Date.now()}`, business, route, value: Number(value || 0), status, source, evidenceRef, evidenceType, evidence, evidenceStatus: evidenceRef ? '待 CEO 采用' : '未登记', runId: run?.runId || 'manual', runIds: selectedRunIds.length ? selectedRunIds : ['manual'], contributors, allocationStatus: contributors.length > 1 && status === '已验证价值' ? 'pending_review' : 'confirmed', allocation: singleAllocation, agent: capability.agent || 'CEO 手动回传', model: capability.model || '手动录入', skills: capability.skills || [], tools: capability.tools || [], at };
    const history = Array.isArray(current.outcomeAttributions) ? current.outcomeAttributions : [];
    return { lastOutcomeAttribution: attribution, outcomeAttributions: [...history, attribution].slice(-24) };
  }

  function summarizeOutcomeValue(state, business, fallbackValue = 0, fallbackRecord) {
    const records = (Array.isArray(state.outcomeAttributions) ? state.outcomeAttributions : []).filter(item => item.business === business);
    if (!records.length && fallbackRecord) records.push(fallbackRecord);
    if (!records.length) return { verified: 0, pending: 0 };
    return records.reduce((summary, item) => {
      const value = Number(item.value || 0);
      if (item.status === '已验证价值') summary.verified += value;
      else summary.pending += value;
      return summary;
    }, { verified: 0, pending: 0 });
  }

  function initExternalFeedback() {
    if (!window.location.pathname.endsWith('workspace-runtime-shortvideo.html') || document.querySelector('.curis-feedback-capture')) return;
    const boardLayout = document.querySelector('.board-layout');
    if (!boardLayout) return;
    const panel = document.createElement('section');
    panel.className = 'panel curis-feedback-capture';
    panel.setAttribute('aria-label', '外部结果回传');
    panel.innerHTML = `<div class="panel-body"><div class="curis-feedback-head"><div><div class="curis-feedback-title">外部结果回传</div><div class="curis-feedback-status"><strong>平台授权尚未连接</strong> · 可先手动补录，数据会进入本周期复盘。</div></div><button class="curis-feedback-open" type="button" data-curis-handled="true">手动记录</button></div><form class="curis-feedback-form"><div class="curis-feedback-grid"><div class="curis-feedback-field"><label for="curis-feedback-plays">播放量</label><input id="curis-feedback-plays" name="plays" type="number" min="0" inputmode="numeric" required /></div><div class="curis-feedback-field"><label for="curis-feedback-likes">点赞</label><input id="curis-feedback-likes" name="likes" type="number" min="0" inputmode="numeric" /></div><div class="curis-feedback-field"><label for="curis-feedback-follows">新增粉丝</label><input id="curis-feedback-follows" name="follows" type="number" min="0" inputmode="numeric" /></div><div class="curis-feedback-field"><label for="curis-feedback-orders">成交单数</label><input id="curis-feedback-orders" name="orders" type="number" min="0" inputmode="numeric" /></div><div class="curis-feedback-field"><label for="curis-feedback-value">成交 / 线索价值（元）</label><input id="curis-feedback-value" name="value" type="number" min="0" inputmode="numeric" /></div><div class="curis-feedback-field"><label for="curis-feedback-window">数据时间窗口</label><input id="curis-feedback-window" name="window" type="date" required /></div><div class="curis-feedback-field"><label for="curis-feedback-credibility">CEO 判断可信度</label><select id="curis-feedback-credibility" name="credibility"><option value="高">高 · 已有截图或平台凭证</option><option value="中" selected>中 · CEO 手动核对</option><option value="低">低 · 待后续验证</option></select></div><div class="curis-feedback-field"><label for="curis-feedback-run">关联运行（可多选）</label><select id="curis-feedback-run" name="runIds" multiple size="4"></select></div><div class="curis-feedback-field full"><label for="curis-feedback-source">数据来源</label><input id="curis-feedback-source" name="source" placeholder="例如：抖音后台截图 / 外部平台链接" required /></div><div class="curis-feedback-field"><label for="curis-feedback-evidence-type">证据类型</label><select id="curis-feedback-evidence-type" name="evidenceType"><option>平台页面 / 数据导出</option><option>截图 / 图片</option><option>本地文件</option><option>客户验收 / 回访记录</option><option>测试报告 / 提交记录</option><option>其他</option></select></div><div class="curis-feedback-field"><label for="curis-feedback-evidence">证据引用</label><input id="curis-feedback-evidence" name="evidenceRef" placeholder="例如：平台链接 / 本地截图路径 / 客户验收单号" /></div><div class="curis-feedback-field full"><label for="curis-feedback-note">CEO 备注</label><textarea id="curis-feedback-note" name="note" placeholder="补充这条结果的上下文、异常或待验证事项"></textarea></div></div><button class="curis-feedback-submit" type="submit" data-curis-handled="true">保存这次结果</button></form><div class="curis-feedback-latest"></div><div class="curis-feedback-history" aria-label="外部结果历史"></div></div>`;
    const feedbackGrid = panel.querySelector('.curis-feedback-grid');
    const resultField = document.createElement('div');
    resultField.className = 'curis-feedback-field';
    resultField.innerHTML = '<label for="curis-feedback-result-status">结果状态</label><select id="curis-feedback-result-status" name="resultStatus"><option value="已验证价值">已验证价值</option><option value="数据待验证" selected>数据待验证</option><option value="结果异常">结果异常</option></select>';
    feedbackGrid?.insertBefore(resultField, feedbackGrid.querySelector('.curis-feedback-field.full'));
    boardLayout.parentNode.insertBefore(panel, boardLayout);
    const status = panel.querySelector('.curis-feedback-status');
    const form = panel.querySelector('form');
    const latest = panel.querySelector('.curis-feedback-latest');
    const historyList = panel.querySelector('.curis-feedback-history');
    const runSelect = panel.querySelector('[name="runIds"]');
    if (runSelect) { runSelect.innerHTML = getRunOptions('workspace-runtime-shortvideo.html').map(option => `<option value="${escapeHtml(option.value)}">${escapeHtml(option.label)}</option>`).join(''); runSelect.querySelector('option[value="manual"]')?.setAttribute('selected', 'selected'); }
    const saved = readState().latestExternalFeedback;
    const windowField = panel.querySelector('[name="window"]');
    if (windowField) windowField.value = new Date().toISOString().slice(0, 10);
    const renderLatest = record => {
      if (!record) return;
      status.textContent = `最近手动回传 · ${record.time} · ${record.resultStatus || '数据待验证'} · 可信度 ${record.credibility || '中'}`;
      latest.textContent = `最新结果：播放 ${record.plays} · 点赞 ${record.likes || 0} · 新增粉丝 ${record.follows || 0} · 成交 ${record.orders || 0} · 价值 ¥${Number(record.value || 0).toLocaleString()} · ${record.window || '时间待补'} · ${record.resultStatus || '数据待验证'} · 可信度 ${record.credibility || '中'} · ${runLabelForState(readState(), record.runId, record.runIds)}${record.evidenceRef ? ` · 证据：${record.evidenceRef}` : ''}`;
      latest.classList.add('is-visible');
    };
    const renderHistory = () => {
      const history = readState().externalFeedbackHistory || [];
      if (!historyList) return;
      historyList.innerHTML = history.slice(-5).reverse().map(record => `<div class="curis-feedback-history-item"><strong>${escapeHtml(record.window || '时间待补')} · ${escapeHtml(record.resultStatus || '数据待验证')} · 可信度 ${escapeHtml(record.credibility || '中')} · ${escapeHtml(runLabelForState(readState(), record.runId, record.runIds))}</strong>播放 ${escapeHtml(record.plays || 0)} · 点赞 ${escapeHtml(record.likes || 0)} · 粉丝 ${escapeHtml(record.follows || 0)} · 成交 ${escapeHtml(record.orders || 0)} · 价值 ¥${escapeHtml(Number(record.value || 0).toLocaleString())}${record.evidenceRef ? ` · 证据：${escapeHtml(record.evidenceRef)}` : ''}</div>`).join('');
    };
    const applySummary = record => {
      if (!record) return;
      const grids = panel.querySelectorAll('.metrics-grid');
      const setMetric = (grid, label, value, note) => {
        const metric = [...(grid?.querySelectorAll('.metric') || [])].find(item => item.querySelector('.metric-label')?.textContent.trim() === label);
        if (!metric) return;
        metric.querySelector('.metric-value')?.replaceChildren(document.createTextNode(value));
        if (note) metric.querySelector('.metric-delta')?.replaceChildren(document.createTextNode(note));
      };
      setMetric(grids[0], '总播放', Number(record.plays || 0).toLocaleString(), `${record.resultStatus || '数据待验证'} · 手动回传`);
      setMetric(grids[0], '新增粉丝', Number(record.follows || 0).toLocaleString(), `来源：${record.source || 'CEO 记录'}`);
      setMetric(grids[1], '可归因价值', `¥${Number(record.value || 0).toLocaleString()}`, '本轮外部结果');
      const shortVideoCost = (readState().financeCosts || []).filter(item => /抖音|TikTok|短视频/.test(String(item.business || ''))).reduce((sum, item) => sum + Number(item.amount || 0), 0);
      setMetric(grids[1], '本周期 ROI', shortVideoCost > 0 ? `${(Number(record.value || 0) / shortVideoCost).toFixed(1)}x` : '—', shortVideoCost > 0 ? `成交价值 / 已记录成本 · ¥${shortVideoCost.toLocaleString()}` : '有结果和成本后计算');
    };
    renderLatest(saved);
    applySummary(saved);
    renderHistory();
    panel.querySelector('.curis-feedback-open').addEventListener('click', () => {
      form.classList.toggle('is-open');
      if (form.classList.contains('is-open')) form.querySelector('input')?.focus();
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      const data = new FormData(form);
      const plays = String(data.get('plays') || '').trim();
      if (!plays) return;
      const runIds = data.getAll('runIds').filter(Boolean);
      const record = { plays, likes: String(data.get('likes') || '').trim(), follows: String(data.get('follows') || '').trim(), orders: String(data.get('orders') || '').trim(), value: Number(data.get('value') || 0), window: String(data.get('window') || '').trim(), source: String(data.get('source') || '').trim(), evidenceType: String(data.get('evidenceType') || '其他').trim(), evidenceRef: String(data.get('evidenceRef') || '').trim(), credibility: String(data.get('credibility') || '中').trim(), resultStatus: String(data.get('resultStatus') || '数据待验证').trim(), runIds: runIds.length ? runIds : ['manual'], runId: runIds.find(id => id !== 'manual') || 'manual', note: String(data.get('note') || '').trim(), time: new Date().toLocaleString('zh-CN', { hour: '2-digit', minute: '2-digit' }), at: new Date().toISOString() };
      const current = readState();
      const history = Array.isArray(current.externalFeedbackHistory)
        ? current.externalFeedbackHistory
        : (current.latestExternalFeedback ? [current.latestExternalFeedback] : []);
      const attribution = recordOutcomeAttribution({ business: '抖音 / TikTok 运营', route: 'workspace-runtime-shortvideo.html', runId: record.runId, runIds: record.runIds, value: record.value, status: record.resultStatus, source: record.source, evidenceRef: record.evidenceRef, evidenceType: record.evidenceType, at: record.at });
      writeState({
        latestExternalFeedback: record,
        externalFeedbackHistory: [...history, record].slice(-12),
        ...attribution,
        lastAssistantMessage: `外部结果已回流：播放 ${record.plays}、新增粉丝 ${record.follows || 0}、成交 ${record.orders || 0}。我会把这条信号带回下一次经营决策。`,
        lastAssistantHandoff: { label: '业务版图', route: 'business.html', message: '真实结果已回流，准备下一步安排' }
      });
      resolveScheduledRuns(record.runIds, { outcomeId: attribution.lastOutcomeAttribution?.id, resolutionNote: `外部结果已回流：播放 ${record.plays} · 新增粉丝 ${record.follows || 0} · 成交 ${record.orders || 0}。${record.resultStatus}` });
      const runtime = window.curisShortVideoRuntime;
      const feedbackVideo = runtime?.videos?.find(video => video.stage === 'data') || runtime?.videos?.find(video => video.stage === 'publish');
      if (feedbackVideo && record.resultStatus !== '结果异常') {
        feedbackVideo.stage = 'review';
        localStorage.setItem('curis-video-stages', JSON.stringify(Object.fromEntries(runtime.videos.map(video => [video.id, video.stage]))));
        runtime.renderPipeline?.();
      }
      renderLatest(record);
      applySummary(record);
      renderHistory();
      form.reset();
      form.classList.remove('is-open');
      showToast('外部结果已记录，CEO 助理会在复盘时带上这条反馈');
    });
  }

  function initXhsFeedbackCapture() {
    if (!window.location.pathname.endsWith('workspace-runtime-xhs.html')) return;
    const button = document.querySelector('[data-runtime-action="manual-result"]');
    if (!button || button.dataset.xhsFeedbackBound === 'true') return;
    button.dataset.xhsFeedbackBound = 'true';
    button.dataset.runtimeAction = 'xhs-feedback';
    const applySummary = record => {
      const metric = label => [...document.querySelectorAll('.summary .metric')].find(item => item.querySelector('span')?.textContent.trim() === label);
      const followers = metric('新增粉丝');
      const value = metric('线索价值');
      const roi = metric('本周期 ROI');
      if (followers) { followers.querySelector('strong')?.replaceChildren(document.createTextNode(Number(record.follows || 0).toLocaleString())); followers.querySelector('small')?.replaceChildren(document.createTextNode(`${record.resultStatus || '数据待验证'} · 手动回传`)); }
      if (value) { value.querySelector('strong')?.replaceChildren(document.createTextNode(`¥${Number(record.value || 0).toLocaleString()}`)); value.querySelector('small')?.replaceChildren(document.createTextNode(`来源：${record.source || 'CEO 记录'}${record.evidenceRef ? ` · 证据：${record.evidenceRef}` : ''}`)); }
      if (roi) {
        const cost = (readState().financeCosts || []).filter(item => /小红书/.test(String(item.business || ''))).reduce((sum, item) => sum + Number(item.amount || 0), 0);
        roi.querySelector('strong')?.replaceChildren(document.createTextNode(record.value && cost ? `${(Number(record.value || 0) / cost).toFixed(1)}x` : '—'));
        roi.querySelector('small')?.replaceChildren(document.createTextNode(record.value && cost ? `价值 / 已记录成本 · ${runLabelForState(readState(), record.runId, record.runIds)}` : '有结果和成本后计算'));
      }
    };
    button.addEventListener('click', event => {
      event.stopPropagation();
      openFormDialog({
        title: '补录小红书本轮结果',
        description: '没有平台授权时，用 CEO 可核对的后台数据补齐本轮结果；每个数字都保留时间窗口、来源和可信度。',
        submitLabel: '保存结果',
        fields: [
          { name: 'reads', label: '阅读量', type: 'number', placeholder: '例如：12000', required: true },
          { name: 'likes', label: '点赞', type: 'number', placeholder: '例如：920' },
          { name: 'saves', label: '收藏', type: 'number', placeholder: '例如：380' },
          { name: 'comments', label: '评论', type: 'number', placeholder: '例如：96' },
          { name: 'follows', label: '新增粉丝', type: 'number', placeholder: '例如：210' },
          { name: 'leads', label: '有效线索数', type: 'number', placeholder: '例如：12' },
          { name: 'value', label: '线索或成交价值（元）', type: 'number', placeholder: '例如：12400' },
          { name: 'window', label: '数据时间窗口', type: 'date', required: true },
          { name: 'runIds', label: '关联运行（可多选）', type: 'multiselect', options: getRunOptions('workspace-runtime-xhs.html'), value: ['manual'] },
          { name: 'resultStatus', label: '结果状态', type: 'select', options: ['已验证价值', '数据待验证', '结果异常'] },
          { name: 'source', label: '数据来源', placeholder: '例如：小红书后台截图 / 客户回访', required: true },
          { name: 'evidenceType', label: '证据类型', type: 'select', options: ['平台页面 / 数据导出', '截图 / 图片', '本地文件', '客户验收 / 回访记录', '测试报告 / 提交记录', '其他'] },
          { name: 'evidenceRef', label: '证据引用', placeholder: '例如：平台链接 / 本地截图路径 / 客户回访编号' },
          { name: 'credibility', label: 'CEO 判断可信度', type: 'select', options: ['高 · 有平台凭证', '中 · CEO 手动核对', '低 · 待后续验证'] },
          { name: 'note', label: '备注', type: 'textarea', placeholder: '补充异常、内容版本或待验证事项' }
        ],
        onSubmit: values => {
          const reads = Number(values.reads || 0);
          if (!Number.isFinite(reads) || reads < 0) return showToast('请输入有效阅读量');
          const record = { ...values, reads, at: new Date().toISOString() };
          const current = readState();
          const history = Array.isArray(current.xhsFeedbackHistory) ? current.xhsFeedbackHistory : (current.latestXhsFeedback ? [current.latestXhsFeedback] : []);
          const runIds = Array.isArray(values.runIds) && values.runIds.length ? values.runIds : ['manual'];
          record.runIds = runIds;
          record.runId = runIds.find(id => id !== 'manual') || 'manual';
          const attribution = recordOutcomeAttribution({ business: '小红书运营', route: 'workspace-runtime-xhs.html', runId: record.runId, runIds: record.runIds, value: record.value, status: record.resultStatus, source: record.source, evidenceRef: record.evidenceRef, evidenceType: record.evidenceType, at: record.at });
          writeState({ latestXhsFeedback: record, xhsFeedbackHistory: [...history, record].slice(-12), ...attribution, lastAssistantMessage: `小红书本轮结果已回流：阅读 ${reads.toLocaleString()}、收藏 ${values.saves || 0}、新增粉丝 ${values.follows || 0}。我会把它带入下一轮选题复盘。`, lastAssistantHandoff: { label: '业务版图', route: 'business.html', message: '小红书结果已回流' } });
          resolveScheduledRuns(record.runIds, { outcomeId: attribution.lastOutcomeAttribution?.id, resolutionNote: `小红书结果已回流：阅读 ${reads.toLocaleString()} · 收藏 ${values.saves || 0} · 新增粉丝 ${values.follows || 0}。${record.resultStatus}` });
          const row = label => [...document.querySelectorAll('.result-row')].find(item => item.querySelector('span')?.textContent.trim() === label);
          row('已验证阅读')?.querySelector('strong')?.replaceChildren(document.createTextNode(reads.toLocaleString()));
          row('收藏 / 评论')?.querySelector('strong')?.replaceChildren(document.createTextNode(`${values.saves || 0} / ${values.comments || 0}`));
          row('线索价值')?.querySelector('strong')?.replaceChildren(document.createTextNode(`¥${Number(values.value || 0).toLocaleString()}`));
          applySummary(record);
          showToast('小红书结果已记录，已进入下一轮复盘');
        }
      });
    });
    const saved = readState().latestXhsFeedback;
    if (saved) {
      const row = label => [...document.querySelectorAll('.result-row')].find(item => item.querySelector('span')?.textContent.trim() === label);
      row('已验证阅读')?.querySelector('strong')?.replaceChildren(document.createTextNode(Number(saved.reads || 0).toLocaleString()));
      row('收藏 / 评论')?.querySelector('strong')?.replaceChildren(document.createTextNode(`${saved.saves || 0} / ${saved.comments || 0}`));
      row('线索价值')?.querySelector('strong')?.replaceChildren(document.createTextNode(`¥${Number(saved.value || 0).toLocaleString()}`));
      applySummary(saved);
    }
  }

  function initXhsContentReview() {
    if (!window.location.pathname.endsWith('workspace-runtime-xhs.html')) return;
    const rows = [...document.querySelectorAll('.content-row')];
    if (!rows.length) return;
    const queueRoot = rows[0].parentElement;
    let queue = Array.isArray(readState().xhsContentQueue) ? readState().xhsContentQueue : [];
    const renderCurrentStage = () => {
      const stages = [...document.querySelectorAll('.loop .stage')];
      if (!stages.length) return;
      const state = readState();
      const reviews = state.xhsContentReviews || {};
      const hasApproved = Object.values(reviews).some(item => item?.decision === '通过发布');
      const hasAnalysis = queue.some(item => item.status === '分析中');
      const activeIndex = state.latestXhsFeedback ? 6 : hasApproved ? 4 : hasAnalysis ? 2 : 3;
      stages.forEach((stage, index) => stage.classList.toggle('current', index === activeIndex));
    };
    const renderQueue = () => {
      queueRoot?.querySelectorAll('[data-xhs-queued], [data-xhs-result]').forEach(node => node.remove());
      const state = readState();
      const hasRealRecord = Boolean(state.latestXhsFeedback);
      if (hasRealRecord) {
        const record = state.latestXhsFeedback;
        const row = document.createElement('div');
        row.className = 'content-row curis-xhs-result';
        row.dataset.xhsResult = 'true';
        row.innerHTML = '<div><strong>最近一轮真实结果 · 小红书</strong><p></p></div><span class="pill"></span><button type="button" data-xhs-result-review>去复盘</button>';
        row.querySelector('p').textContent = `平台回传 · 阅读 ${Number(record.reads || 0).toLocaleString()} · 收藏 ${Number(record.saves || 0).toLocaleString()} · 新增粉丝 ${Number(record.follows || 0).toLocaleString()}`;
        row.querySelector('.pill').textContent = record.resultStatus || '数据待验证';
        queueRoot?.insertBefore(row, rows[0]);
      }
      queue.slice(-6).reverse().forEach(item => {
        const row = document.createElement('div');
        row.className = 'content-row curis-xhs-queued';
        row.dataset.xhsQueued = item.id;
        row.innerHTML = '<div><strong></strong><p></p></div><span class="pill"></span><button type="button" data-xhs-queued-action>审阅</button>';
        row.querySelector('strong').textContent = item.title;
        row.querySelector('p').textContent = `内容 AI · ${item.angle || '等待拆解'} · ${item.source || 'CEO 输入'}`;
        row.querySelector('.pill').textContent = item.status || '草稿';
        queueRoot?.insertBefore(row, rows[0]);
      });
      rows.forEach(row => {
        const button = row.querySelector('[data-runtime-action]');
        row.querySelector('p')?.replaceChildren(document.createTextNode(hasRealRecord ? '业务模板示例 · 本周期真实结果已单独记录' : '业务模板已加载 · 等待真实发布与平台结果'));
        row.querySelector('.pill')?.replaceChildren(document.createTextNode(hasRealRecord ? '模板' : '待首轮运行'));
        if (button && button.dataset.curisTemplate !== 'true') {
          button.dataset.curisTemplate = 'true';
          button.removeAttribute('data-runtime-action');
          button.textContent = '查看模板';
          button.addEventListener('click', () => showToast('这是业务模板示例，真实内容进入队列后才会产生平台结果。'));
        }
      });
      renderCurrentStage();
    };
    const headerActions = document.querySelector('.header .actions');
    if (headerActions && !headerActions.querySelector('[data-xhs-new-topic]')) {
      const create = document.createElement('button');
      create.type = 'button';
      create.dataset.xhsNewTopic = 'true';
      create.textContent = '新建选题';
      headerActions.insertBefore(create, headerActions.firstChild);
      create.addEventListener('click', () => openFormDialog({
        title: '新建小红书选题',
        description: '先记录想验证的主题，策略 AI 会补齐平台趋势、竞品拆解和下一步内容 Brief。',
        submitLabel: '加入内容队列',
        fields: [
          { name: 'title', label: '选题名称', placeholder: '例如：一人公司如何用 AI 少开一半会议', required: true },
          { name: 'angle', label: '希望验证的角度', placeholder: '例如：效率提升 / 产品方法 / 真实案例', required: true },
          { name: 'source', label: '已有依据', placeholder: '例如：CEO 想法 / 竞品观察 / 评论区问题' }
        ],
        onSubmit: values => {
          const item = { id: `xhs-topic-${Date.now()}`, title: values.title, angle: values.angle, source: values.source, status: '待分析', at: new Date().toISOString() };
          queue = [...queue, item].slice(-12);
          writeState({ xhsContentQueue: queue, lastAssistantMessage: `选题“${item.title}”已加入小红书内容队列，策略 AI 会先完成信息搜集和拆解。`, lastAssistantHandoff: { label: '小红书运营办公室', route: 'workspace-runtime-xhs.html', message: '新选题已进入分析' } });
          renderQueue();
          showToast('选题已加入内容队列');
        }
      }));
    }
    const renderSaved = () => {
      const reviews = readState().xhsContentReviews || {};
      rows.forEach(row => {
        const title = row.querySelector('strong')?.textContent.trim();
        const review = title && reviews[title];
        const button = row.querySelector('[data-runtime-action]');
        const pill = row.querySelector('.pill');
        if (!review || !button) return;
        button.textContent = review.decision === '通过发布' ? '已通过' : '已退回';
        button.disabled = true;
        if (pill) pill.textContent = review.decision === '通过发布' ? '已批准发布' : '待修改';
      });
    };
    rows.forEach(row => {
      const button = row.querySelector('[data-runtime-action="save-workflow"]');
      if (!button) return;
      button.dataset.runtimeAction = 'xhs-review';
    });
    queueRoot?.addEventListener('click', event => {
      if (event.target.closest('[data-xhs-result-review]')) {
        writeState({ lastAssistantMessage: '小红书真实结果已打开，先确认数据可信度，再决定是否采纳下一轮建议。', lastAssistantHandoff: { label: '业务版图', route: 'business.html', message: '进入结果复盘' } });
        window.location.href = 'business.html';
        return;
      }
      const action = event.target.closest('[data-xhs-queued-action]');
      const row = action?.closest('[data-xhs-queued]');
      const item = queue.find(candidate => candidate.id === row?.dataset.xhsQueued);
      if (!item) return;
      openFormDialog({
        title: `选题审阅 · ${item.title}`,
        description: `已有依据：${item.source || 'CEO 输入'}。策略 AI 会在通过后继续完成拆解和内容 Brief。`,
        submitLabel: '保存审阅结果',
        fields: [{ name: 'decision', label: 'CEO 决定', type: 'select', options: ['进入分析', '退回调整'] }, { name: 'note', label: '审阅说明', type: 'textarea', placeholder: '例如：更聚焦独立开发者的真实场景。' }],
        onSubmit: values => {
          item.status = values.decision === '进入分析' ? '分析中' : '待调整';
          item.review = values.note;
          item.reviewedAt = new Date().toISOString();
          writeState({ xhsContentQueue: queue, lastAssistantMessage: values.decision === '进入分析' ? `选题“${item.title}”已进入分析，策略 AI 会继续生成内容 Brief。` : `选题“${item.title}”已退回调整，原始依据仍保留在队列中。`, lastAssistantHandoff: { label: '小红书运营办公室', route: 'workspace-runtime-xhs.html', message: item.status } });
          renderQueue();
          showToast(values.decision === '进入分析' ? '选题已进入分析' : '选题已退回调整');
        }
      });
    });
    renderQueue();
    renderSaved();
    window.addEventListener('curis-state-changed', () => { queue = Array.isArray(readState().xhsContentQueue) ? readState().xhsContentQueue : queue; renderQueue(); });
  }

  function initShortVideoTruthBoard() {
    if (!window.location.pathname.endsWith('workspace-runtime-shortvideo.html')) return;
    const runtime = window.curisShortVideoRuntime;
    if (!runtime?.videos || typeof runtime.renderPipeline !== 'function') return;
    const truthStyleId = 'curis-shortvideo-truth-style';
    if (!document.getElementById(truthStyleId)) {
      const style = document.createElement('style');
      style.id = truthStyleId;
      style.textContent = '.curis-shortvideo-empty{padding:15px;color:var(--text-secondary,#9599a6);background:var(--bg-overlay-l1,rgba(224,226,242,.04));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:7px;font-size:11px;line-height:1.55}.curis-shortvideo-empty strong{display:block;margin-bottom:5px;color:var(--text-default,#d1d3db);font-size:12px}.curis-shortvideo-empty button{margin-top:10px;padding:7px 9px;color:var(--text-default,#d1d3db);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}';
      document.head.appendChild(style);
    }
    const render = () => {
      const state = readState();
      const record = state.latestExternalFeedback;
      if (!record) {
        runtime.videos.forEach(video => {
          video.evidence = '业务模板已加载 · 尚无真实外部证据';
          video.checkpoint = '等待平台发布、结果回传与 CEO 判断';
          video.statusLabel = '待首轮运行';
          video.status = 'ontrack';
          video.urgent = false;
          video.stats = { plays: '—', completion: '—', interaction: '—', follows: '—' };
        });
        runtime.renderPipeline();
      } else {
        const dataVideo = runtime.videos.find(video => video.stage === 'data') || runtime.videos[0];
        if (dataVideo) {
          dataVideo.evidence = `最近回传：播放 ${Number(record.plays || 0).toLocaleString()} · 新增粉丝 ${Number(record.follows || 0).toLocaleString()} · ${record.resultStatus || '数据待验证'}`;
          dataVideo.checkpoint = '进入复盘，生成下一轮内容假设';
          dataVideo.statusLabel = record.resultStatus === '结果异常' ? '结果异常' : '待复盘';
          dataVideo.status = record.resultStatus === '结果异常' ? 'risk' : 'attention';
          dataVideo.stats = { plays: Number(record.plays || 0).toLocaleString(), completion: record.completion ? `${record.completion}%` : '—', interaction: Number(record.plays || 0) ? `${(((Number(record.likes || 0) + Number(record.comments || 0)) / Number(record.plays || 1)) * 100).toFixed(1)}%` : '—', follows: Number(record.follows || 0).toLocaleString() };
          runtime.renderPipeline();
        }
      }
      const acceptanceList = document.querySelector('.acceptance-list');
      if (acceptanceList && !record) acceptanceList.innerHTML = '<div class="curis-shortvideo-empty"><strong>等待首条真实内容结果</strong><span>当前卡片是工作流模板，不代表已经发布。平台回传或 CEO 手动补录后，待验收内容会出现在这里。</span><br><button type="button" data-shortvideo-open-feedback>打开结果回传</button></div>';
      if (acceptanceList && record) {
        const acceptance = state.shortVideoResultAcceptance;
        const choice = acceptance?.choice || '待 CEO 判断';
        const acceptanceKey = `${record.at || record.time || ''}:${choice}`;
        if (acceptanceList.dataset.curisAcceptanceKey !== acceptanceKey) {
          acceptanceList.dataset.curisAcceptanceKey = acceptanceKey;
          const decided = choice !== '待 CEO 判断';
          acceptanceList.innerHTML = `<div class="acceptance-item"><div class="acceptance-thumb">▶</div><div class="acceptance-info"><div class="acceptance-title">最近一条回传内容</div><div class="acceptance-stats"><span>播放 ${Number(record.plays || 0).toLocaleString()}</span><span>粉丝 ${Number(record.follows || 0).toLocaleString()}</span><span>价值 ¥${Number(record.value || 0).toLocaleString()}</span></div><div class="acceptance-actions"><button class="btn btn-primary" type="button" data-shortvideo-accept ${decided ? 'disabled' : ''}>${choice === '采用结果' ? '已采用' : '采用结果'}</button><button class="btn btn-secondary" type="button" data-shortvideo-reject ${decided ? 'disabled' : ''}>${choice === '待核' ? '已标记待核' : '标记待核'}</button><span class="curis-acceptance-state">${choice}</span></div></div></div>`;
        }
      }
      const insightsPanel = [...document.querySelectorAll('.side-panels .panel')].find(panel => panel.querySelector('.panel-title')?.textContent.includes('洞察与下一步'));
      const insightBody = insightsPanel?.querySelector('.panel-body');
      if (insightBody && !record) insightBody.innerHTML = '<div class="curis-shortvideo-empty"><strong>等待第一条真实结果</strong><span>增长 AI 会在播放、完播、互动、粉丝或成交数据回传后，生成趋势归因和下一轮建议。</span></div>';
      if (insightBody && record && !insightBody.dataset.curisRendered) { insightBody.dataset.curisRendered = 'true'; insightBody.innerHTML = `<div class="insight-card"><div class="insight-label">本轮回传</div><div class="insight-title">先确认结果可信度，再决定是否扩大产能</div><div class="insight-text">播放 ${Number(record.plays || 0).toLocaleString()}，新增粉丝 ${Number(record.follows || 0).toLocaleString()}，成交 / 线索价值 ¥${Number(record.value || 0).toLocaleString()}。复盘 AI 会把这条结果带入下一轮。</div><span class="insight-tag">${record.resultStatus || '数据待验证'}</span></div>`; }
    };
    document.addEventListener('click', event => {
      if (event.target.closest('[data-shortvideo-open-feedback]')) document.querySelector('.curis-feedback-open')?.click();
      if (event.target.closest('[data-shortvideo-accept]')) { writeState({ shortVideoResultAcceptance: { choice: '采用结果', at: new Date().toISOString() }, lastAssistantMessage: '短视频本轮结果已采用，增长 AI 可以据此生成下一轮内容假设。' }); showToast('结果已采用，进入下一轮复盘'); }
      if (event.target.closest('[data-shortvideo-reject]')) { writeState({ shortVideoResultAcceptance: { choice: '待核', at: new Date().toISOString() }, lastAssistantMessage: '短视频本轮结果已标记待核，暂不把它作为扩大投入依据。' }); showToast('结果已标记待核'); }
    });
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initPlatformOnboarding() {
    const page = window.location.pathname.split('/').pop();
    const key = page === 'workspace-runtime-software.html' ? 'software' : page === 'workspace-runtime-xhs.html' ? 'xhs' : page === 'workspace-runtime-shortvideo.html' ? 'douyin' : '';
    if (!key || document.querySelector('.curis-platform-guide')) return;
    const config = {
      software: {
        label: '软件研发',
        title: '先把研发环境与验收口径准备好，再让研发办公室开始跑',
        note: '研发办公室会自己拆解、实现和测试，但发布前的真实使用验收仍由 CEO 负责。先把边界说清楚，AI 才能独立推进又不越界。',
        steps: [
          ['版本目标', '确认本轮要交付的版本、目标用户和必须解决的业务问题。'],
          ['代码与环境', '准备代码仓库、分支规则、运行环境与可回滚版本。'],
          ['质量门槛', '确认测试范围、阻断条件、已知风险和 QA AI 的通过标准。'],
          ['真实验收', '写下 CEO 将亲自验证的使用路径，以及外部客户会判断的结果。'],
          ['发布与反馈', '确认发布方式、问题回报入口和下一轮优化如何回到研发办公室。']
        ]
      },
      xhs: {
        label: '小红书',
        title: '先把小红书账号接好，再让内容办公室开始跑',
        note: '第一次进入只需要准备这些信息。授权失败时，仍可用手动窗口运行，不会用假数据填满结果。',
        steps: [
          ['账号与定位', '准备账号主页链接、目标人群、内容主题和首周发布频率。'],
          ['品牌规则', '准备品牌语气、禁用词、可引用资料和需要 CEO 亲自确认的边界。'],
          ['平台权限', '在小红书开放平台开通内容发布与数据读取；没有授权可先保留手动回传。'],
          ['结果口径', '确认阅读、点赞、收藏、评论、粉丝和线索价值的记录方式。'],
          ['首轮目标', '确认 7 天要验证的结果，例如 3 条内容、收藏率基线和首批线索。']
        ]
      },
      douyin: {
        label: '抖音 / TikTok',
        title: '先把抖音 / TikTok 的账号与发布权限接好',
        note: '短视频流程会同时覆盖选题、制作、发布、数据回流和复盘；平台权限决定哪些步骤能自动运行。',
        steps: [
          ['账号与地区', '准备账号主页、运营地区、语言和目标受众；TikTok 还需确认地区可用能力。'],
          ['素材与版权', '准备可用素材、出镜规则、音乐与字体版权说明，避免发布后才发现无法使用。'],
          ['平台权限', '开通发布、数据读取；若涉及带货，再确认橱窗、订单和成交数据权限。'],
          ['安全与合规', '准备敏感词、品牌安全、评论处理和账号异常时的暂停规则。'],
          ['首轮目标', '确认 7 天发布数量、完播率基线、粉丝目标和每条内容可接受成本。']
        ]
      }
    }[key];
    const anchor = document.querySelector('.header') || document.querySelector('.outcome-bar');
    if (!anchor?.parentNode) return;
    const current = readState().platformOnboarding?.[key] || {};
    const guide = document.createElement('section');
    guide.className = 'curis-platform-guide';
    guide.setAttribute('aria-label', `${config.label}业务接入准备`);
    guide.innerHTML = `<div class="curis-platform-guide-copy"><p class="curis-platform-guide-kicker">首次接入 · ${config.label}业务</p><h2 class="curis-platform-guide-title">${config.title}</h2><p class="curis-platform-guide-note">${config.note}</p><span class="curis-platform-guide-state"></span></div><button type="button" class="curis-platform-guide-action" data-platform-guide-open>查看准备清单</button>`;
    anchor.parentNode.insertBefore(guide, anchor.nextSibling);
    const dialog = document.createElement('dialog');
    dialog.className = 'curis-guide-dialog';
    dialog.setAttribute('aria-labelledby', 'curis-guide-title');
    dialog.innerHTML = `<div class="curis-guide-head"><div><h2 id="curis-guide-title">${config.label}业务接入准备</h2><p>把资料、权限和结果口径准备好，办公室才知道哪些可以自动完成，哪些必须请 CEO 判断。</p></div><button type="button" class="curis-guide-close" data-guide-close aria-label="关闭">×</button></div><div class="curis-guide-body" data-guide-body></div><div class="curis-guide-foot"><span class="curis-guide-foot-note" data-guide-foot-note></span><div class="curis-guide-foot-actions"><button type="button" data-guide-capability>${key === 'software' ? '去配置研发能力' : '先去连接平台'}</button><button type="button" class="primary" data-guide-save>保存接入进度</button></div></div>`;
    document.body.appendChild(dialog);
    const checked = () => new Set((readState().platformOnboarding?.[key]?.checked || []));
    const renderGuide = () => {
      const done = checked();
      dialog.querySelector('[data-guide-body]').innerHTML = config.steps.map((step, index) => `<label class="curis-guide-step"><span class="curis-guide-step-index">${index + 1}</span><span><strong>${step[0]}</strong><p>${step[1]}</p><span class="curis-guide-check"><input type="checkbox" data-guide-check="${index}" ${done.has(index) ? 'checked' : ''} />我已准备好这一项</span></span></label>`).join('');
      const complete = done.size === config.steps.length;
      dialog.querySelector('[data-guide-foot-note]').textContent = complete ? '准备已完成，可以开始首轮运行。' : `已完成 ${done.size} / ${config.steps.length} 项`;
      guide.classList.toggle('is-ready', complete);
      guide.querySelector('.curis-platform-guide-state').textContent = complete ? `已准备 ${done.size}/${config.steps.length} · 可开始试运行` : `待准备 ${config.steps.length - done.size} 项 · 先完成接入清单`;
      guide.querySelector('[data-platform-guide-open]').textContent = complete ? '查看接入状态' : '查看准备清单';
    };
    const saveProgress = () => {
      const next = [...dialog.querySelectorAll('[data-guide-check]')].filter(input => input.checked).map(input => Number(input.dataset.guideCheck));
      const state = readState();
      writeState({ platformOnboarding: { ...(state.platformOnboarding || {}), [key]: { checked: next, updatedAt: new Date().toISOString() } }, lastAssistantMessage: `${config.label}接入准备已更新。我会只在权限和资料满足时推进自动运行。` });
      renderGuide();
      dialog.close();
      showToast('接入进度已保存');
    };
    guide.querySelector('[data-platform-guide-open]').addEventListener('click', () => { renderGuide(); if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', ''); });
    dialog.querySelector('[data-guide-close]').addEventListener('click', () => dialog.close());
    dialog.querySelector('[data-guide-save]').addEventListener('click', saveProgress);
    dialog.querySelector('[data-guide-capability]').addEventListener('click', () => { dialog.close(); document.querySelector('[data-capability-runtime]')?.click(); if (key !== 'software') document.querySelector('[data-runtime-action="authorize"]')?.click(); });
    renderGuide();
  }

  function initShortVideoInteractions() {
    if (!window.location.pathname.endsWith('workspace-runtime-shortvideo.html')) return;
    const runtime = window.curisShortVideoRuntime;
    const findButton = label => [...document.querySelectorAll('button')].find(button => button.textContent.trim() === label);
    if (!document.getElementById('curis-short-video-interaction-style')) {
      const style = document.createElement('style');
      style.id = 'curis-short-video-interaction-style';
      style.textContent = '.curis-idea-queue{margin:0 0 14px;padding:14px 16px;background:var(--bg-base-secondary,#222427);border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:10px}.curis-idea-queue-head{display:flex;align-items:center;justify-content:space-between;gap:12px;color:var(--text-secondary,#9599a6);font-size:11px}.curis-idea-queue-head strong{display:block;color:var(--text-default,#d1d3db);font-size:13px}.curis-idea-queue-head span span,.curis-idea-queue-head div span{display:block;margin-top:4px}.curis-idea-queue-list{display:grid;gap:8px;margin-top:12px}.curis-idea-item{display:flex;align-items:center;gap:12px;padding:10px 0;border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-idea-item>div{min-width:0;flex:1}.curis-idea-item strong{display:block;color:var(--text-default,#d1d3db);font-size:11px}.curis-idea-item p{margin:4px 0 0;color:var(--text-secondary,#9599a6);font-size:10px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.curis-idea-item button{padding:6px 9px;color:var(--text-default,#d1d3db);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}.curis-idea-status,.curis-acceptance-state{color:var(--text-secondary,#9599a6);font-size:10px;white-space:nowrap}.curis-acceptance-state{display:block;margin-top:6px;color:var(--text-brand,#32f08c)}.curis-idea-empty{margin:12px 0 0;color:var(--text-secondary,#9599a6);font-size:11px}';
      document.head.appendChild(style);
    }
    const queueAnchor = document.querySelector('.board-layout');
    const getIdeas = () => {
      const ideas = readState().shortVideoIdeas;
      return Array.isArray(ideas) ? ideas : [];
    };
    const renderIdeaQueue = () => {
      if (!queueAnchor) return;
      let queue = document.querySelector('[data-short-video-ideas]');
      if (!queue) {
        queue = document.createElement('section');
        queue.dataset.shortVideoIdeas = 'true';
        queue.className = 'curis-idea-queue';
        queueAnchor.parentNode.insertBefore(queue, queueAnchor);
      }
      const ideas = getIdeas();
      queue.innerHTML = `<div class="curis-idea-queue-head"><div><strong>选题池</strong><span>CEO 提出的方向先在这里补证据，再进入内容流水线。</span></div><span>${ideas.length} 条</span></div>${ideas.length ? `<div class="curis-idea-queue-list">${ideas.slice().reverse().map((idea, index) => { const runtimeId = `idea-${idea.at || index}`; const admitted = runtime?.videos?.some(video => video.id === runtimeId); return `<article class="curis-idea-item"><div><strong>${escapeHtml(idea.topic || '未命名选题')}</strong><p>${escapeHtml(idea.audience || '目标人群未填写')} · ${escapeHtml(idea.hypothesis || '等待验证假设')}</p></div><span class="curis-idea-status">${admitted ? '已进入选题' : (idea.status || '待分析')}</span>${admitted ? '' : `<button type="button" data-admit-idea="${escapeHtml(runtimeId)}">送入选题阶段</button>`}</article>`; }).join('')}</div>` : '<p class="curis-idea-empty">还没有 CEO 提出的选题。先新增一个方向，分析 AI 会补齐证据和优先级。</p>'}`;
    };
    const syncAcceptances = () => {
      const acceptances = readState().shortVideoAcceptances || {};
      document.querySelectorAll('.acceptance-item').forEach(item => {
        const title = item.querySelector('.acceptance-title')?.textContent.trim();
        const result = title && acceptances[title];
        if (!result) return;
        const actions = item.querySelector('.acceptance-actions');
        actions?.querySelectorAll('button').forEach(button => { button.disabled = true; button.textContent = button.textContent === '通过' || button.textContent === '已通过' ? (result.status === '已通过' ? '已通过' : '通过') : (result.status === '已打回' ? '已打回' : '打回'); });
        let state = item.querySelector('.curis-acceptance-state');
        if (!state) { state = document.createElement('span'); state.className = 'curis-acceptance-state'; actions?.appendChild(state); }
        state.textContent = `${result.status} · ${new Date(result.at).toLocaleString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' })}`;
      });
    };
    if (runtime && !runtime.__curisCustomIdeasLoaded) {
      getIdeas().forEach((idea, index) => {
        const id = `idea-${idea.at || index}`;
        if (runtime.videos.some(video => video.id === id)) return;
        runtime.videos.push({ id, title: idea.topic || '未命名选题', stage: 'topic', owner: 'Growth AI', ownerType: 'growth', status: 'ontrack', statusLabel: '待分析', duration: '—', evidence: '等待分析 AI 补齐平台趋势与历史表现证据', checkpoint: '分析完成后提交 3 个内容角度', urgent: false, stats: { plays: '—', completion: '—', interaction: '—', follows: '—' } });
      });
      runtime.__curisCustomIdeasLoaded = true;
      runtime.renderPipeline?.();
    }
    renderIdeaQueue();
    const ideaButton = findButton('+ 新建选题');
    if (ideaButton && ideaButton.dataset.curisHandled !== 'true') {
      ideaButton.dataset.curisHandled = 'true';
      ideaButton.addEventListener('click', () => openFormDialog({
        title: '新增选题',
        description: '把一个内容假设交给策略 AI。保存后会进入选题阶段，由分析 AI 补齐证据和优先级。',
        submitLabel: '加入选题池',
        fields: [
          { name: 'topic', label: '选题方向', placeholder: '例如：AI 员工如何减少 CEO 的重复沟通', required: true },
          { name: 'audience', label: '目标人群', placeholder: '例如：正在搭建一人公司的创业者', required: true },
          { name: 'hypothesis', label: '要验证的假设', type: 'textarea', placeholder: '例如：有具体经营场景的内容，比泛泛介绍更容易被收藏。', required: true }
        ],
        onSubmit: values => { const current = readState(); const ideas = Array.isArray(current.shortVideoIdeas) ? current.shortVideoIdeas : []; writeState({ shortVideoIdeas: [...ideas, { ...values, at: new Date().toISOString(), status: '待分析' }].slice(-20), lastAssistantMessage: `新选题“${values.topic}”已进入内容办公室，分析 AI 会先补齐证据再安排制作。` }); renderIdeaQueue(); showToast('选题已加入内容办公室'); }
      }));
    }
    document.querySelector('[data-short-video-ideas]')?.addEventListener('click', event => {
      const button = event.target.closest('[data-admit-idea]');
      if (!button || !runtime) return;
      const idea = getIdeas().find(item => `idea-${item.at}` === button.dataset.admitIdea);
      if (!idea) return;
      const video = { id: button.dataset.admitIdea, title: idea.topic, stage: 'topic', owner: 'Growth AI', ownerType: 'growth', status: 'ontrack', statusLabel: '待分析', duration: '—', evidence: '已进入选题阶段，等待分析 AI 补齐平台趋势与历史表现证据', checkpoint: '分析完成后提交 3 个内容角度', urgent: false, stats: { plays: '—', completion: '—', interaction: '—', follows: '—' } };
      if (!runtime.videos.some(item => item.id === video.id)) runtime.videos.push(video);
      runtime.renderPipeline?.();
      writeState({ shortVideoIdeas: getIdeas().map(item => item.at === idea.at ? { ...item, status: '已进入选题' } : item), lastAssistantMessage: `选题“${idea.topic}”已进入选题阶段，分析 AI 开始补证据。` });
      renderIdeaQueue();
      showToast('已送入选题阶段');
    });
    const weekButton = findButton('本周');
    if (weekButton && weekButton.dataset.curisHandled !== 'true') {
      weekButton.dataset.curisHandled = 'true';
      weekButton.addEventListener('click', () => showToast('当前查看本周内容周期；历史周期保留在成果库中'));
    }
    document.querySelectorAll('.acceptance-item .acceptance-actions button').forEach(button => {
      if (button.dataset.curisHandled === 'true') return;
      button.dataset.curisHandled = 'true';
      button.addEventListener('click', () => {
        const item = button.closest('.acceptance-item');
        const title = item?.querySelector('.acceptance-title')?.textContent.trim() || '这条内容';
        const approved = button.textContent.trim() === '通过';
        const current = readState();
        const acceptances = { ...(current.shortVideoAcceptances || {}), [title]: { status: approved ? '已通过' : '已打回', at: new Date().toISOString() } };
        writeState({ shortVideoAcceptances: acceptances, lastAssistantMessage: approved ? `“${title}”已通过验收，内容办公室可以继续回收平台数据。` : `“${title}”已打回，内容 AI 会保留原版本并按反馈重新制作。` });
        button.parentElement.querySelectorAll('button').forEach(itemButton => { itemButton.disabled = true; });
        button.textContent = approved ? '已通过' : '已打回';
        syncAcceptances();
        showToast(approved ? '内容已通过验收' : '内容已打回修改');
      });
    });
    syncAcceptances();
    window.addEventListener('curis-state-changed', () => { renderIdeaQueue(); syncAcceptances(); });
    const dataButton = findButton('查看全部平台数据');
    if (dataButton && dataButton.dataset.curisHandled !== 'true') {
      dataButton.dataset.curisHandled = 'true';
      dataButton.addEventListener('click', () => { writeState({ lastAssistantMessage: '平台数据已整理到财务与经营，CEO 可以从结果价值和成本一起判断下一周期。', lastAssistantHandoff: { label: '财务与经营', route: 'finance.html', message: '查看平台数据' } }); window.location.href = 'finance.html'; });
    }
    const drawerActions = document.querySelectorAll('#detailDrawer .drawer-actions button');
    drawerActions.forEach(button => {
      if (button.dataset.curisHandled === 'true') return;
      button.dataset.curisHandled = 'true';
      button.addEventListener('click', () => {
        const label = button.textContent.trim();
        const title = document.querySelector('#drawerTitle')?.textContent.trim();
        if (label === '关闭') return runtime?.closeDrawer?.();
        if (label === '查看证据') return openEvidenceReview({ title: title || '当前视频证据', source: '抖音 / TikTok 运营办公室 · 视频详情', summary: document.querySelector('#drawerBody .insight-card')?.textContent?.trim() || '当前视频的证据与平台数据', status: '待 CEO 采用', confidence: '待复核' });
        if (label !== '推进到下一阶段') return;
        const video = runtime?.videos?.find(item => item.title === title);
        if (!video || !runtime?.stages) return showToast('当前视频上下文已失效，请重新打开');
        const index = runtime.stages.findIndex(stage => stage.id === video.stage);
        const next = runtime.stages[index + 1];
        if (!next) return showToast('这条内容已进入复盘归档');
        const old = video.stage;
        video.stage = next.id;
        localStorage.setItem('curis-video-stages', JSON.stringify(Object.fromEntries(runtime.videos.map(item => [item.id, item.stage]))));
        runtime.closeDrawer?.();
        runtime.renderPipeline?.();
        writeState({ lastAssistantMessage: `“${title}”已从${runtime.stages.find(stage => stage.id === old)?.name}推进到${next.name}。`, lastAssistantHandoff: { label: '内容办公室', route: 'workspace-runtime-shortvideo.html', message: '内容已推进' } });
        showToast(`已推进到${next.name}`);
      });
    });
  }

  function initRuntimeTruthMetrics() {
    const page = window.location.pathname.split('/').pop();
    if (!['workspace-runtime-xhs.html', 'workspace-runtime-shortvideo.html'].includes(page)) return;
    const stateFor = () => readState();
    const text = (node, value) => node?.replaceChildren(document.createTextNode(value));
    const addTemplateState = (anchor, message) => {
      if (!anchor?.parentNode || document.querySelector('[data-curis-truth-state]')) return;
      const note = document.createElement('div');
      note.dataset.curisTruthState = 'true';
      note.className = 'curis-truth-state';
      note.textContent = message;
      anchor.parentNode.insertBefore(note, anchor.nextSibling);
    };
    if (!document.getElementById('curis-truth-state-style')) {
      const style = document.createElement('style');
      style.id = 'curis-truth-state-style';
      style.textContent = '.curis-truth-state{margin:10px 0;padding:9px 11px;color:var(--text-secondary,#a4a7af);background:var(--bg-base-secondary,#202226);border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:7px;font-size:10px;line-height:1.45}.curis-truth-state::before{content:"当前口径 · ";color:var(--text-default,#e2e3e7);font-weight:600}';
      document.head.appendChild(style);
    }
    const outcomesFor = business => (Array.isArray(stateFor().outcomeAttributions) ? stateFor().outcomeAttributions : []).filter(item => item.business === business);
    const costFor = business => (Array.isArray(stateFor().financeCosts) ? stateFor().financeCosts : []).filter(item => business === '小红书运营' ? /小红书/.test(String(item.business || '')) : /抖音|TikTok|短视频/.test(String(item.business || ''))).reduce((sum, item) => sum + Number(item.amount || 0), 0);
    const renderXhs = () => {
      const state = stateFor();
      const record = state.latestXhsFeedback;
      const metrics = [...document.querySelectorAll('.summary .metric')];
      const queue = Array.isArray(state.xhsContentQueue) ? state.xhsContentQueue : [];
      const reads = Number(record?.reads || 0);
      const saves = Number(record?.saves || 0);
      const value = Number(record?.value || 0);
      const cost = costFor('小红书运营');
      const verified = outcomesFor('小红书运营').filter(item => item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
      const shownValue = value || verified;
      if (metrics.length >= 5) {
        text(metrics[0].querySelector('strong'), queue.length ? String(queue.filter(item => /已发布|发布中|待发布/.test(item.status || '')).length || queue.length) : '—');
        text(metrics[0].querySelector('small'), queue.length ? '已登记内容 · 目标由 CEO 设置' : '尚无真实发布记录');
        text(metrics[1].querySelector('strong'), reads ? `${((saves / reads) * 100).toFixed(1)}%` : '—');
        text(metrics[1].querySelector('small'), reads ? `${record.resultStatus || '数据待验证'} · 本轮回传` : '等待平台结果');
        text(metrics[2].querySelector('strong'), record ? Number(record.follows || 0).toLocaleString() : '—');
        text(metrics[2].querySelector('small'), record ? `${record.resultStatus || '数据待验证'} · ${record.source || 'CEO 手动回传'}` : '等待平台结果');
        text(metrics[3].querySelector('strong'), shownValue ? `¥${shownValue.toLocaleString()}` : '—');
        text(metrics[3].querySelector('small'), shownValue ? `${record?.resultStatus || (verified ? '已验证价值' : '数据待验证')} · 结果归因` : '等待线索或成交回传');
        text(metrics[4].querySelector('strong'), shownValue && cost ? `${(shownValue / cost).toFixed(1)}x` : '—');
        text(metrics[4].querySelector('small'), shownValue && cost ? '价值 / 已记录成本' : '有结果和成本后计算');
      }
      const rows = [...document.querySelectorAll('.result-row')];
      const row = label => rows.find(item => item.querySelector('span')?.textContent.trim() === label);
      text(row('数据来源')?.querySelector('strong'), record ? `${record.source || 'CEO 手动回传'} · ${record.resultStatus || '数据待验证'}` : '尚无平台结果');
      text(row('已验证阅读')?.querySelector('strong'), record ? reads.toLocaleString() : '—');
      text(row('收藏 / 评论')?.querySelector('strong'), record ? `${saves.toLocaleString()} / ${Number(record.comments || 0).toLocaleString()}` : '—');
      text(row('线索价值')?.querySelector('strong'), shownValue ? `¥${shownValue.toLocaleString()}` : '—');
      if (!record) addTemplateState(document.querySelector('.curis-platform-guide') || document.querySelector('.header'), '业务模板已加载；尚无本周期真实平台回传，示例内容不会计入经营账。');
    };
    const renderShortVideo = () => {
      const state = stateFor();
      const record = state.latestExternalFeedback;
      const value = Number(record?.value || 0);
      const cost = costFor('抖音 / TikTok 运营');
      const verified = outcomesFor('抖音 / TikTok 运营').filter(item => item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
      const shownValue = value || verified;
      const meta = [...document.querySelectorAll('.outcome-meta span')];
      const ideas = Array.isArray(state.shortVideoIdeas) ? state.shortVideoIdeas : [];
      if (meta.length >= 4) [ideas.length ? `${ideas.length}` : '—', state.calendarEvents?.filter(item => item.route === page && !['resolved', 'completed'].includes(item.status)).length ? String(state.calendarEvents.filter(item => item.route === page && !['resolved', 'completed'].includes(item.status)).length) : '—', record ? '1' : '—', record ? '已回传' : '—'].forEach((valueText, index) => text(meta[index].querySelector('strong'), valueText));
      const grids = [...document.querySelectorAll('.side-panels .metrics-grid')];
      const setGrid = (grid, index, valueText, note) => { const item = grid?.querySelectorAll('.metric')[index]; text(item?.querySelector('.metric-value'), valueText); text(item?.querySelector('.metric-delta'), note); };
      if (grids[0]) {
        setGrid(grids[0], 0, record ? Number(record.plays || 0).toLocaleString() : '—', record ? `${record.resultStatus || '数据待验证'} · ${record.source || 'CEO 手动回传'}` : '等待平台回传');
        setGrid(grids[0], 1, record?.completion ? `${record.completion}%` : '—', record ? '本轮回传' : '等待平台回传');
        const interaction = record && Number(record.plays || 0) ? ((Number(record.likes || 0) + Number(record.comments || 0)) / Number(record.plays || 1) * 100).toFixed(1) : '';
        setGrid(grids[0], 2, interaction ? `${interaction}%` : '—', record ? '点赞 + 评论 / 播放' : '等待平台回传');
        setGrid(grids[0], 3, record ? Number(record.follows || 0).toLocaleString() : '—', record ? '本轮新增粉丝' : '等待平台回传');
      }
      if (grids[1]) {
        setGrid(grids[1], 0, shownValue ? `¥${shownValue.toLocaleString()}` : '—', shownValue ? `${record?.resultStatus || (verified ? '已验证价值' : '数据待验证')} · 成交 / 线索` : '等待成交或线索回传');
        setGrid(grids[1], 1, cost ? `¥${cost.toLocaleString()}` : '—', cost ? 'AI、工具与投流 · 已记录' : '等待成本记录');
        const runs = (state.calendarEvents || []).filter(item => item.route === page && Number(item.cost || 0) > 0).length;
        setGrid(grids[1], 2, cost && runs ? `¥${(cost / runs).toFixed(0)}` : '—', runs ? `${runs} 次已记录运行` : '等待运行记录');
        setGrid(grids[1], 3, shownValue && cost ? `${(shownValue / cost).toFixed(1)}x` : '—', shownValue && cost ? '价值 / 已记录成本' : '有结果和成本后计算');
      }
      if (!record) addTemplateState(document.querySelector('.outcome-bar'), '业务模板已加载；尚无本周期真实平台回传，示例内容不会计入经营账。');
      const presence = document.querySelector('.curis-office-presence');
      if (presence && !record) {
        text(presence.querySelector('.curis-office-live'), '岗位已配置 · 等待首轮结果');
        presence.querySelectorAll('.curis-office-person-state').forEach((node, index) => text(node, ['等待 CEO 提出首个选题', '等待首条脚本输入', '等待素材与权限', '等待首轮验收'][index] || '等待首轮运行'));
      }
    };
    const render = page === 'workspace-runtime-xhs.html' ? renderXhs : renderShortVideo;
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initSoftwareTruthMetrics() {
    if (!window.location.pathname.endsWith('workspace-runtime-software.html')) return;
    const render = () => {
      const state = readState();
      const runs = (state.calendarEvents || []).filter(item => item.route === 'workspace-runtime-software.html');
      const acceptance = state.softwareAcceptance;
      const hasEvidence = runs.length || acceptance;
      const text = (node, value) => node?.replaceChildren(document.createTextNode(value));
      const handoff = document.querySelector('#software-handoff-note');
      if (!hasEvidence) text(handoff, '研发办公室已配置岗位，但还没有本周期真实运行记录。完成一次研发运行后，证据和交接会在这里出现。');
      const stages = [...document.querySelectorAll('.flow .stage')];
      if (stages[3]) text(stages[3].querySelector('span'), runs.length ? `${runs.length} 次真实运行记录` : '等待真实回归记录');
      const evidence = [...document.querySelectorAll('.evidence .metric')];
      if (evidence.length >= 4) {
        text(evidence[0].querySelector('strong'), hasEvidence ? (acceptance?.version || '版本待登记') : '—');
        text(evidence[0].querySelector('small'), hasEvidence ? '运行记录或 CEO 验收' : '等待首轮运行');
        text(evidence[1].querySelector('strong'), acceptance?.commit || '—');
        text(evidence[1].querySelector('small'), acceptance?.evidenceRef ? `CEO 证据 · ${acceptance.evidenceRef}` : '尚无提交证据');
        const passed = runs.filter(item => ['completed', 'waiting_ceo', 'acknowledged', 'resolved'].includes(item.status)).length;
        text(evidence[2].querySelector('strong'), passed ? `${passed} 次` : '—');
        text(evidence[2].querySelector('small'), passed ? '真实运行已完成' : '等待 QA 回归记录');
        text(evidence[3].querySelector('strong'), acceptance?.choice === 'accept' ? '0' : hasEvidence ? '待观察' : '—');
        text(evidence[3].querySelector('small'), acceptance?.choice === 'accept' ? 'CEO 已完成验收' : hasEvidence ? 'CEO 真实使用后确认' : '等待真实使用');
      }
      const capabilityCard = [...document.querySelectorAll('.card')].find(card => card.querySelector('h2')?.textContent.includes('本周期 AI 能力与成本'));
      capabilityCard?.querySelectorAll('.person')?.forEach(person => {
        const em = person.querySelector('em');
        if (!em || person.dataset.capabilityRuntime !== undefined) return;
        if (!hasEvidence) text(em, '等待真实运行记录');
      });
      const assetCard = [...document.querySelectorAll('.card')].find(card => card.querySelector('h2')?.textContent.includes('成果与复用'));
      if (assetCard && !hasEvidence) {
        text(assetCard.querySelector('.acceptance-state strong'), '尚无真实成果沉淀');
        text(assetCard.querySelector('.acceptance-state span'), '完成一次研发运行并通过 CEO 验收后，产品简报、代码提交、QA 报告和验收包会进入成果库。');
      }
      const presence = document.querySelector('.curis-office-presence');
      if (presence && !hasEvidence) {
        text(presence.querySelector('.curis-office-live'), '岗位已配置 · 等待首轮研发运行');
        presence.querySelectorAll('.curis-office-person-state').forEach((node, index) => text(node, ['等待 CEO 提出产品意图', '等待研发范围确认', '等待真实回归记录', '等待 CEO 验收'][index] || '等待首轮运行'));
      }
    };
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initBusinessTruthCards() {
    if (!window.location.pathname.endsWith('business.html')) return;
    const text = (node, value) => node?.replaceChildren(document.createTextNode(value));
    const stateFor = () => readState();
    const cardFor = id => document.querySelector(`.biz-card[data-id="${id}"]`);
    const evidenceValue = (card, matcher) => [...(card?.querySelectorAll('.evidence-item') || [])].find(item => matcher.test(item.querySelector('.evidence-name')?.textContent || ''))?.querySelector('.evidence-value');
    const updateDrawer = () => {
      const title = document.querySelector('#drawerTitle')?.textContent || '';
      const state = stateFor();
      const drawerId = document.querySelector('#businessDrawer')?.dataset.businessId || '';
      const business = drawerId === 'content-growth' || /小红书/.test(title) || (!drawerId && /小红书/.test(state.firstBusiness || '')) ? 'xhs' : drawerId === 'short-video' || /抖音|TikTok|短视频/.test(title) || (!drawerId && /抖音|TikTok|短视频/.test(state.firstBusiness || '')) ? 'short' : drawerId === 'software-dev' || /软件|Curis|研发/.test(title) || (!drawerId && /软件|Curis|研发/.test(state.firstBusiness || '')) ? 'software' : '';
      const record = business === 'xhs' ? state.latestXhsFeedback : business === 'short' ? state.latestExternalFeedback : null;
      const outcome = (state.outcomeAttributions || []).filter(item => item.business === (business === 'xhs' ? '小红书运营' : business === 'short' ? '抖音 / TikTok 运营' : '软件开发')).filter(item => item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
      const values = business === 'xhs' ? [record ? Number(record.reads || 0).toLocaleString() : '—', record ? `${((Number(record.saves || 0) / Math.max(Number(record.reads || 1), 1)) * 100).toFixed(1)}%` : '—', record ? Number(record.leads || 0).toLocaleString() : '—'] : business === 'short' ? [record ? Number(record.plays || 0).toLocaleString() : '—', record ? `${(((Number(record.likes || 0) + Number(record.comments || 0)) / Math.max(Number(record.plays || 1), 1)) * 100).toFixed(1)}%` : '—', record ? Number(record.orders || 0).toLocaleString() : '—'] : [state.softwareAcceptance ? '已记录' : '—', state.softwareAcceptance?.choice === 'accept' ? '已通过' : '—', outcome ? `¥${outcome.toLocaleString()}` : '—'];
      const labels = business === 'xhs' ? [/阅读|周阅读/, /收藏/, /线索/] : business === 'short' ? [/播放|平均播放/, /互动/, /发布|测试/] : [/commit/, /CI/, /验收/];
      const rows = [...document.querySelectorAll('#drawerEvidence .evidence-item')];
      labels.forEach((matcher, index) => { const row = rows.find(item => matcher.test(item.querySelector('.evidence-name')?.textContent || '')); text(row?.querySelector('.evidence-value'), values[index]); });
      const impact = [...document.querySelectorAll('#businessDrawer .impact-value')];
      if (impact.length >= 4) {
        const costs = (state.financeCosts || []).filter(item => business === 'xhs' ? /小红书/.test(item.business || '') : business === 'short' ? /抖音|TikTok|短视频/.test(item.business || '') : /软件|Curis|研发/.test(item.business || '')).reduce((sum, item) => sum + Number(item.amount || 0), 0);
        text(impact[2], costs ? `¥ ${costs.toLocaleString()}` : '—');
        text(impact[3], record?.value || outcome ? `¥${Number(record?.value || outcome).toLocaleString()}` : '—');
      }
      const commitments = document.querySelector('#drawerCommitments');
      if (commitments) {
        const rows = business === 'xhs'
          ? [['持续产出内容', '内容 AI · CEO 发布确认'], ['获得平台真实回传', '发布 AI · API 或 CEO 手动录入']]
          : business === 'short'
            ? [['完成短视频发布节奏', '脚本与制作 AI · CEO 发布确认'], ['回收播放、互动与成交', '数据回收 AI · 平台 API 或手动窗口']]
            : [['交付可验收的软件增量', '研发 AI · CEO 验收'], ['通过测试并保留交付证据', 'QA AI · 真实运行记录']];
        commitments.innerHTML = rows.map(([title, meta]) => `<div class="commitment-item"><div class="commitment-title">${escapeHtml(title)}</div><div class="commitment-meta">负责人：${escapeHtml(meta)}</div></div>`).join('');
      }
    };
    const render = () => {
      const state = stateFor();
      const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
      const cards = ['software-dev', 'content-growth', 'short-video'].map(cardFor).filter(Boolean);
      const portfolio = document.querySelector('#portfolioGrid');
      const empty = document.querySelector('[data-business-empty]');
      if (!state.companyCreatedAt) {
        cards.forEach(card => { card.hidden = true; });
        if (portfolio && !empty) {
          const notice = document.createElement('article');
          notice.dataset.businessEmpty = 'true';
          notice.className = 'biz-card curis-business-empty';
          notice.innerHTML = '<div class="biz-card-header"><div class="biz-card-top"><div><h2 class="biz-name">还没有业务</h2><p class="biz-target">先创建公司，再建立第一间办公室</p></div></div></div><div class="biz-card-body"><p class="biz-outcome">选择软件开发、小红书或抖音 / TikTok，业务工程 AI 会把它装配成可运行空间。</p></div><div class="biz-card-footer"><button type="button" class="btn btn-primary btn-sm">开始创建公司 →</button></div>';
          portfolio.appendChild(notice);
          notice.querySelector('button')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
        }
        document.querySelectorAll('.summary-item').forEach(item => item.querySelector('.summary-value')?.replaceChildren(document.createTextNode('0')));
        document.querySelectorAll('.roi-card').forEach(card => { text(card.querySelector('.roi-value'), '—'); text(card.querySelector('.roi-delta'), '等待公司启动'); });
        return;
      }
      if (empty) empty.remove();
      const firstBusiness = String(state.firstBusiness || '');
      const activeIds = new Set();
      if (/小红书/.test(firstBusiness)) activeIds.add('content-growth');
      if (/抖音|TikTok|短视频/.test(firstBusiness)) activeIds.add('short-video');
      if (/软件|Curis|研发/.test(firstBusiness)) activeIds.add('software-dev');
      if (state.softwareAcceptance || runs.some(item => item.route === 'workspace-runtime-software.html')) activeIds.add('software-dev');
      if (state.latestXhsFeedback || runs.some(item => item.route === 'workspace-runtime-xhs.html')) activeIds.add('content-growth');
      if (state.latestExternalFeedback || runs.some(item => item.route === 'workspace-runtime-shortvideo.html')) activeIds.add('short-video');
      if (!activeIds.size && state.companyCreatedAt) cards.forEach(card => activeIds.add(card.dataset.id));
      document.querySelectorAll('.summary-item').forEach(item => {
        const label = item.querySelector('.summary-label')?.textContent.trim();
        const value = item.querySelector('.summary-value');
        if (label === '总业务数' && value) value.textContent = String(activeIds.size);
      });
      cards.forEach(card => { const visible = activeIds.has(card.dataset.id); card.hidden = !visible; card.style.display = visible ? '' : 'none'; });
      document.querySelectorAll('.curis-business-map .curis-map-node[data-business-target]').forEach(node => {
        const id = node.dataset.businessTarget;
        const visible = id === 'software-dev' ? activeIds.has('software-dev') : id === 'content-growth' ? activeIds.has('content-growth') : id === 'short-video' ? activeIds.has('short-video') : true;
        node.hidden = !visible;
        node.style.display = visible ? '' : 'none';
      });
      const configs = {
        'software-dev': { record: state.softwareAcceptance, values: state.softwareAcceptance ? ['已记录', state.softwareAcceptance.choice === 'accept' ? '已通过' : '待处理', (state.outcomeAttributions || []).filter(item => item.business === '软件开发' && item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0) ? '已归因' : '待归因'] : ['—', '—', '—'], stage: state.softwareAcceptance?.choice === 'accept' ? '已验收' : '待首轮结果' },
        'content-growth': { record: state.latestXhsFeedback, values: state.latestXhsFeedback ? [Number(state.latestXhsFeedback.reads || 0).toLocaleString(), `${((Number(state.latestXhsFeedback.saves || 0) / Math.max(Number(state.latestXhsFeedback.reads || 1), 1)) * 100).toFixed(1)}%`, Number(state.latestXhsFeedback.leads || 0).toLocaleString()] : ['—', '—', '—'], stage: state.latestXhsFeedback ? (state.latestXhsFeedback.resultStatus || '待复盘') : '待首轮结果' },
        'short-video': { record: state.latestExternalFeedback, values: state.latestExternalFeedback ? [Number(state.latestExternalFeedback.plays || 0).toLocaleString(), `${(((Number(state.latestExternalFeedback.likes || 0) + Number(state.latestExternalFeedback.comments || 0)) / Math.max(Number(state.latestExternalFeedback.plays || 1), 1)) * 100).toFixed(1)}%`, Number(state.latestExternalFeedback.orders || 0).toLocaleString()] : ['—', '—', '—'], stage: state.latestExternalFeedback ? (state.latestExternalFeedback.resultStatus || '待复盘') : '待首轮结果' }
      };
      Object.entries(configs).forEach(([id, config]) => {
        const card = cardFor(id);
        if (!card) return;
        [...card.querySelectorAll('.evidence-item')].forEach((row, index) => text(row.querySelector('.evidence-value'), config.values[index] || '—'));
        text(card.querySelector('.stage-pill'), config.stage);
        const health = card.querySelectorAll('.health-value');
        if (!config.record) { text(health[0], '等待结果'); text(health[1], '尚未运行'); }
        const checkpoint = card.querySelector('.checkpoint');
        if (!config.record) { text(checkpoint?.querySelector('span'), '等待首轮结果'); text(checkpoint?.querySelector('.checkpoint-time'), '未安排'); }
      });
      const activity = [state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html'), state.latestXhsFeedback || (state.xhsContentQueue || []).length, state.latestExternalFeedback || (state.shortVideoIdeas || []).length];
      const paused = [state.businessDecision?.choice === 'pause' && state.businessDecision?.platform === '小红书', state.businessDecision?.choice === 'pause' && state.businessDecision?.platform === '抖音 / TikTok'].filter(Boolean).length;
      const total = activeIds.size + (state.departmentDraft?.name && state.departmentCommitment?.name ? 1 : 0);
      const running = activity.filter((value, index) => value && activeIds.has(['software-dev', 'content-growth', 'short-video'][index])).length;
      const experiment = Math.max(0, total - running - paused);
      const summaryValues = { '运行中': running, '实验中': experiment, '暂停': paused, '总业务数': total };
      document.querySelectorAll('.summary-item').forEach(item => { const label = item.querySelector('.summary-label')?.textContent.trim(); if (label in summaryValues) text(item.querySelector('.summary-value'), String(summaryValues[label])); });
      const costTotal = (state.financeCosts || []).reduce((sum, item) => sum + Number(item.amount || 0), 0);
      const verifiedValue = (state.outcomeAttributions || []).filter(item => item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
      const roiCards = [...document.querySelectorAll('.roi-card')];
      const roiValues = [costTotal ? `¥ ${costTotal.toLocaleString()}` : '—', runs.length ? `${Math.min(100, runs.length * 12)}%` : '—', verifiedValue ? `¥ ${verifiedValue.toLocaleString()}` : '—', costTotal && verifiedValue ? `${(verifiedValue / costTotal).toFixed(1)}x` : '—'];
      roiCards.forEach((card, index) => { text(card.querySelector('.roi-value'), roiValues[index]); text(card.querySelector('.roi-delta'), roiValues[index] === '—' ? '等待真实记录' : index === 0 ? '本周期已记录' : '按当前周期计算'); });
      const mapMeta = document.querySelector('.curis-map-meta');
      if (mapMeta && !state.latestXhsFeedback && !state.latestExternalFeedback && !state.businessDecision?.choice && !state.softwareAcceptance) mapMeta.textContent = `${total} 条业务 · ${running} 条运行中 · ${experiment} 条实验`;
      updateDrawer();
    };
    render();
    window.addEventListener('curis-state-changed', render);
    const drawer = document.querySelector('#businessDrawer');
    const title = document.querySelector('#drawerTitle');
    if (drawer && title) new MutationObserver(updateDrawer).observe(title, { childList: true, characterData: true, subtree: true });
  }

  function initGrowthNextCycle() {
    const page = window.location.pathname.split('/').pop();
    if (!['workspace-runtime-xhs.html', 'workspace-runtime-shortvideo.html'].includes(page) || document.querySelector('.curis-growth-next-cycle')) return;
    const isXhs = page === 'workspace-runtime-xhs.html';
    const config = isXhs
      ? { business: '小红书运营', label: '小红书下一轮', key: 'latestXhsFeedback', queueKey: 'xhsContentQueue', route: page, owner: '增长 AI', cost: 42, title: '下一轮内容优化建议' }
      : { business: '抖音 / TikTok 运营', label: '短视频下一轮', key: 'latestExternalFeedback', queueKey: 'shortVideoIdeas', route: page, owner: '增长 AI', cost: 68, title: '下一轮内容优化建议' };
    const anchor = isXhs
      ? document.querySelector('.result')?.closest('.card') || document.querySelector('.content-row')?.closest('.card')
      : document.querySelector('.curis-feedback-capture') || document.querySelector('.board-layout');
    if (!anchor?.parentNode) return;
    const panel = document.createElement('section');
    panel.className = 'card curis-growth-next-cycle';
    panel.setAttribute('aria-labelledby', 'curis-growth-next-cycle-title');
    panel.innerHTML = `<div class="curis-growth-next-cycle-head"><div><p class="curis-growth-next-cycle-kicker">结果已经回到业务</p><h2 id="curis-growth-next-cycle-title">${config.title}</h2><p class="curis-growth-next-cycle-note">外部结果不是终点。增长 AI 会把本轮证据翻译成下一轮选题、节奏和能力安排，CEO 只需要确认是否采纳。</p></div><span data-growth-cycle-state>等待第一条结果</span></div><div class="curis-growth-next-cycle-body"><div class="curis-growth-next-cycle-evidence" data-growth-cycle-evidence></div><div class="curis-growth-next-cycle-recommendation" data-growth-cycle-recommendation></div></div><div class="curis-growth-next-cycle-actions"><button type="button" data-growth-action="adopt">采纳到选题池</button><button type="button" data-growth-action="schedule">安排下一轮</button><button type="button" data-growth-action="capability">调整能力</button></div>`;
    anchor.parentNode.insertBefore(panel, anchor.nextSibling);
    const style = document.createElement('style');
    style.textContent = '.curis-growth-next-cycle{margin:16px 0}.curis-growth-next-cycle-head{display:flex;align-items:flex-start;justify-content:space-between;gap:16px}.curis-growth-next-cycle-kicker{margin:0 0 5px;color:var(--text-secondary,#a4a7af);font-size:10px;letter-spacing:.06em}.curis-growth-next-cycle-head h2{margin:0;font-size:15px}.curis-growth-next-cycle-note{max-width:680px;margin:6px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.5}.curis-growth-next-cycle-head>span{padding:5px 7px;color:var(--text-secondary,#a4a7af);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font-size:10px;white-space:nowrap}.curis-growth-next-cycle-body{display:grid;grid-template-columns:1fr 1.35fr;gap:1px;margin-top:14px;background:var(--border-neutral-l1,rgba(224,226,242,.1));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px;overflow:hidden}.curis-growth-next-cycle-body>div{padding:12px;background:var(--bg-base-secondary,#202226)}.curis-growth-next-cycle-body span{display:block;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-growth-next-cycle-body strong{display:block;margin-top:5px;font-size:12px}.curis-growth-next-cycle-body p{margin:5px 0 0;color:var(--text-secondary,#a4a7af);font-size:10px;line-height:1.5}.curis-growth-next-cycle-actions{display:flex;justify-content:flex-end;gap:7px;margin-top:11px}.curis-growth-next-cycle-actions button{padding:7px 9px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}.curis-growth-next-cycle-actions button:first-child{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}.curis-growth-next-cycle-actions button:disabled{opacity:.45;cursor:not-allowed}@media(max-width:700px){.curis-growth-next-cycle-head{flex-direction:column}.curis-growth-next-cycle-body{grid-template-columns:1fr}.curis-growth-next-cycle-actions{align-items:stretch;flex-direction:column}.curis-growth-next-cycle-actions button{width:100%}}';
    document.head.appendChild(style);
    const stateFor = () => readState();
    const recommendationFor = record => {
      if (!record) return { title: '先完成第一条可验证回报', body: '当平台数据或 CEO 手动结果回来后，我会自动比较基线，并生成下一轮建议。', source: '尚无外部结果' };
      const denominator = Number(isXhs ? record.reads : record.plays) || 0;
      const engagement = Number(isXhs ? record.saves : record.likes) || 0;
      const rate = denominator ? engagement / denominator : 0;
      const strong = rate >= (isXhs ? 0.05 : 0.04);
      const title = strong ? (isXhs ? '保留高收藏结构，扩大同一问题簇' : '保留前三秒钩子，测试两个新版本') : (isXhs ? '重写开场与封面，再验证收藏意愿' : '优先测试前三秒表达，降低无效制作成本');
      const body = isXhs
        ? `本轮阅读 ${Number(record.reads || 0).toLocaleString()}，收藏 ${Number(record.saves || 0).toLocaleString()}，收藏率 ${(rate * 100).toFixed(1)}%。${record.follows ? `新增粉丝 ${Number(record.follows).toLocaleString()}，说明主题有持续关注价值。` : '新增粉丝还没有形成明显信号。'}`
        : `本轮播放 ${Number(record.plays || 0).toLocaleString()}，点赞 ${Number(record.likes || 0).toLocaleString()}，互动率 ${(rate * 100).toFixed(1)}%。${record.orders || record.value ? `已记录成交 ${Number(record.orders || 0).toLocaleString()} 单 / ¥${Number(record.value || 0).toLocaleString()}，保留转化路径。` : '还没有成交信号，先把注意力放在内容质量和完播表现。'}`;
      return { title, body, source: `${record.resultStatus || '数据待验证'} · ${record.source || 'CEO 手动回传'}` };
    };
    const render = () => {
      const state = stateFor();
      const record = state[config.key];
      const recommendation = recommendationFor(record);
      const planned = state.growthNextCyclePlans?.[config.business];
      panel.querySelector('[data-growth-cycle-state]').textContent = planned ? '下一轮已安排' : record ? recommendation.source : '等待第一条结果';
      panel.querySelector('[data-growth-cycle-evidence]').innerHTML = `<span>本轮依据</span><strong>${escapeHtml(recommendation.source)}</strong><p>${escapeHtml(record ? (record.window || record.time || '时间窗口待补') : '先在上方记录平台数据或客户回报')}</p>`;
      panel.querySelector('[data-growth-cycle-recommendation]').innerHTML = `<span>增长 AI 建议</span><strong>${escapeHtml(recommendation.title)}</strong><p>${escapeHtml(recommendation.body)}</p>`;
      const adopt = panel.querySelector('[data-growth-action="adopt"]');
      adopt.disabled = !record || planned;
      adopt.textContent = planned ? '已进入下一轮' : '采纳到选题池';
      panel.querySelector('[data-growth-action="schedule"]').disabled = !record;
    };
    const adopt = () => {
      const state = stateFor();
      const record = state[config.key];
      if (!record) return showToast('先记录一条外部结果，再生成下一轮建议');
      const recommendation = recommendationFor(record);
      const currentItems = Array.isArray(state[config.queueKey]) ? state[config.queueKey] : [];
      const item = isXhs
        ? { id: `xhs-cycle-${Date.now()}`, title: recommendation.title, angle: recommendation.body, source: '上一轮结果复盘', status: '待分析', at: new Date().toISOString() }
        : { topic: recommendation.title, audience: '当前账号目标受众', hypothesis: recommendation.body, source: '上一轮结果复盘', status: '待分析', at: new Date().toISOString() };
      writeState({ [config.queueKey]: [...currentItems, item].slice(-20), growthNextCyclePlans: { ...(state.growthNextCyclePlans || {}), [config.business]: { business: config.business, recommendation, adoptedAt: new Date().toISOString(), status: '已进入选题池' } }, lastAssistantMessage: `${config.business}已采纳下一轮建议，${config.owner}会带上本轮结果继续工作。`, lastAssistantHandoff: { label: `${config.business}办公室`, route: config.route, message: '下一轮建议已采纳' } });
      render();
      showToast('下一轮建议已进入选题池');
    };
    const schedule = () => {
      const state = stateFor();
      if (!state[config.key]) return showToast('先记录一条外部结果，再安排下一轮');
      openFormDialog({ title: `安排${config.business}下一轮`, description: '把复盘结论变成下一次真实运行。排期会保留业务、负责人、成本和 CEO 检查点。', submitLabel: '保存排期', fields: [{ name: 'schedule', label: '运行节奏', placeholder: '例如：明天 09:00 / 每周一 08:00', required: true }, { name: 'target', label: '本轮要验证什么', type: 'textarea', value: recommendationFor(state[config.key]).title, required: true }, { name: 'checkpoint', label: 'CEO 检查点', placeholder: '例如：发布前确认品牌语气；结果回流后确认是否扩大', required: true }], onSubmit: values => { let schedules = []; try { schedules = JSON.parse(localStorage.getItem('curis-schedules') || '[]'); } catch (_) {} const item = { id: `growth-${Date.now()}`, name: `${config.business} · 下一轮优化`, business: config.business, schedule: values.schedule, owner: config.owner, task: `${values.target}；${values.checkpoint}`, estimatedCost: config.cost, route: config.route, enabled: true }; localStorage.setItem('curis-schedules', JSON.stringify([...schedules, item].slice(-24))); writeState({ growthNextCyclePlans: { ...(state.growthNextCyclePlans || {}), [config.business]: { business: config.business, ...values, scheduledAt: new Date().toISOString(), status: '已排期' } }, lastAssistantMessage: `${config.business}下一轮已排期：${values.schedule}。CEO 检查点和结果回传会保留在公司日历。`, lastAssistantHandoff: { label: '公司日历', route: 'calendar.html', message: '下一轮已排期' } }); render(); showToast('下一轮已排期'); } });
    };
    panel.querySelector('[data-growth-action="adopt"]').addEventListener('click', adopt);
    panel.querySelector('[data-growth-action="schedule"]').addEventListener('click', schedule);
    panel.querySelector('[data-growth-action="capability"]').addEventListener('click', () => document.querySelector('[data-capability-runtime]')?.click() || showToast('当前页面还没有可切换的能力组合'));
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initRuntimeStageDetails() {
    const page = window.location.pathname.split('/').pop();
    const definitions = page === 'workspace-runtime-shortvideo.html'
      ? [
        ['选题', '增长 AI', '平台趋势、受众问题与历史表现', '候选选题、热度信号和验证假设', 'AI 自动；CEO 只在方向冲突时介入'],
        ['脚本', '内容 AI', '选题 Brief、知识库和品牌规则', '脚本版本、事实引用和开场钩子测试', 'CEO 处理品牌边界与重大取舍'],
        ['拍摄', '视频 AI', '分镜、素材、出镜与版权清单', '可剪辑素材、拍摄证据和缺口列表', '素材缺失或版权异常时升级'],
        ['剪辑', '视频 AI', '原始素材、节奏规则和目标时长', 'A/B 剪辑版本、字幕与封面', 'CEO 选择版本或调整表达'],
        ['发布', '发布 AI', '最终视频、平台权限和发布时间', '发布记录、版本号和平台链接', 'CEO 确认账号与品牌安全'],
        ['数据', '增长 AI', '平台 API 或手动数据窗口', '播放、完播、互动、粉丝和成交数据', 'CEO 确认价值口径与异常'],
        ['复盘', '增长 AI', '内容版本、外部结果与历史基线', '归因结论、可复用知识和下一步', 'CEO 决定是否增加投入'],
        ['提升', '增长 AI + CEO', '复盘结论、产能和经营账', '下一轮选题权重、频率和预算', 'CEO 批准扩大、维持或暂停'],
        ['归档', '成果库', '版本、证据、CEO 判断与复盘知识', '可复用规则、素材与工作流', '自动完成；下一轮运行时带入上下文']
      ]
      : page === 'workspace-runtime-xhs.html'
      ? [
        ['信息搜集', '策略分析 AI', '平台趋势、竞品内容、账号历史', '趋势摘要、竞品拆解和可引用来源', '自动运行；CEO 只调整关注主题'],
        ['拆解', '业务分析 AI', '关键词、封面、标题、评论与互动', '内容结构、关键词簇和表现假设', '自动运行；异常数据升级'],
        ['分析', '策略分析 AI', '拆解结果与公司知识库', '选题优先级、内容 Brief 和验证假设', 'CEO 调整方向与目标人群'],
        ['产出', '内容制作 AI', '内容 Brief、品牌语气和素材', '标题、正文、封面与版本记录', 'CEO 设定品牌边界；AI 负责初稿'],
        ['待发布', '内容制作 AI', '最终稿、敏感词规则、账号权限', '发布包、合规检查和发布时间', 'CEO 必须确认品牌与敏感表达'],
        ['数据', '数据回收 AI', '平台 API 或 CEO 手动窗口', '阅读、点赞、收藏、评论、粉丝和线索价值', 'CEO 确认数据可信度与价值口径'],
        ['复盘', '增长 AI', '内容版本、平台结果和历史基线', '归因结论、知识更新和下一轮建议', 'CEO 决定是否修改规则或扩大投入'],
        ['提升', '增长 AI + CEO', '复盘结论、容量与经营账', '下一周期选题权重、排期和预算变化', 'CEO 批准扩大、维持或暂停'],
        ['归档', '成果库', '内容版本、平台结果与 CEO 判断', '可复用选题规则、素材与工作流', '自动完成；下一轮运行时带入上下文']
      ]
      : page === 'workspace-runtime-software.html'
        ? [
          ['意图', 'CEO', '经营问题与想改善的体验', '可验证的产品目标与验收标准', 'CEO 说明要解决什么'],
          ['产品', '产品 AI', 'CEO 意图、反馈和历史决策', '版本范围、产品 Brief 和变更记录', 'CEO 确认范围与取舍'],
          ['研发', '研发 AI', '产品范围、代码库和能力配置', '代码提交、可运行版本和发布说明', '风险、外部依赖或预算异常时介入'],
          ['QA', 'QA AI', '候选版本、验收标准和回归环境', '回归记录、已知未知和证据包', 'CEO 观察首次真实使用'],
          ['CEO 验收', 'CEO', '可运行版本、证据和使用路径', '验收通过、退回修改或现场演示记录', '必须由 CEO 真实使用判断'],
          ['下一周期', 'CEO 助理 + 产品 AI', '验收反馈、缺陷和业务结果', '下一版本意图、复盘知识和排期', 'CEO 选择继续、调整或暂停'],
          ['归档', '成果库', '验收反馈、版本与证据', '可复用成果、知识与工作流', '自动完成；下一版本引用']
        ]
        : [];
    if (!definitions.length) return;
    const stageSelector = page === 'workspace-runtime-shortvideo.html' ? '#pipeline .stage-header' : page === 'workspace-runtime-xhs.html' ? '.loop .stage' : '.flow .stage';
    const stageContainer = page === 'workspace-runtime-shortvideo.html'
      ? document.querySelector('#pipeline')
      : document.querySelector(page === 'workspace-runtime-xhs.html' ? '.loop' : '.flow');
    let nodes = [...document.querySelectorAll(stageSelector)];
    while (stageContainer && nodes.length < definitions.length) {
      const definition = definitions[nodes.length];
      const node = document.createElement('div');
      node.className = page === 'workspace-runtime-shortvideo.html' ? 'stage-header' : 'stage';
      node.innerHTML = `<strong>${definition[0]}</strong><span>${definition[3]}</span><em>${definition[1]} · 自动</em>`;
      stageContainer.appendChild(node);
      nodes = [...document.querySelectorAll(stageSelector)];
    }
    if (!nodes.length || document.getElementById('curis-stage-dialog')) return;
    const dialog = document.createElement('dialog');
    dialog.id = 'curis-stage-dialog';
    dialog.className = 'curis-stage-dialog';
    dialog.setAttribute('aria-labelledby', 'curis-stage-dialog-title');
    dialog.innerHTML = '<div class="curis-stage-dialog-head"><div><h2 id="curis-stage-dialog-title"></h2><p data-stage-subtitle></p></div><button class="curis-stage-dialog-close" type="button" data-stage-close aria-label="关闭">×</button></div><div class="curis-stage-dialog-body"><div class="curis-stage-dialog-meta"><div><span>负责人</span><strong data-stage-owner></strong></div><div><span>运行方式</span><strong data-stage-mode></strong></div><div><span>CEO 介入</span><strong data-stage-ceo></strong></div></div><div class="curis-stage-dialog-section"><span>输入</span><p data-stage-input></p></div><div class="curis-stage-dialog-section"><span>产出</span><p data-stage-output></p></div></div><div class="curis-stage-dialog-actions"><button type="button" data-stage-assets>查看相关成果</button><button type="button" data-stage-advance>推进到下一阶段</button><button type="button" class="primary" data-stage-close>知道了</button></div>';
    document.body.appendChild(dialog);
    const close = () => dialog.close();
    dialog.querySelectorAll('[data-stage-close]').forEach(button => button.addEventListener('click', close));
    dialog.querySelector('[data-stage-assets]').addEventListener('click', () => { writeState({ lastAssistantMessage: '已打开成果库，相关阶段的输入、输出和证据会保留在公司资产中。' }); window.location.href = 'assets.html'; });
    const progressKey = `curis-runtime-progress-${page}`;
    const initialProgress = () => {
      try { const saved = Number(localStorage.getItem(progressKey)); if (Number.isInteger(saved) && saved >= 0) return saved; } catch (_) {}
      return Math.max(0, nodes.findIndex(node => node.classList.contains('current')));
    };
    let progress = initialProgress();
    const applyProgress = () => nodes.forEach((node, index) => { node.classList.toggle('current', index === progress); node.dataset.runtimeStageIndex = String(index); });
    applyProgress();
    let selectedIndex = 0;
    const openDefinition = definition => {
      if (!definition) return;
      selectedIndex = definitions.indexOf(definition);
      dialog.querySelector('#curis-stage-dialog-title').textContent = definition[0];
      dialog.querySelector('[data-stage-subtitle]').textContent = `${page === 'workspace-runtime-shortvideo.html' ? '抖音 / TikTok 运营办公室' : page === 'workspace-runtime-xhs.html' ? '小红书运营办公室' : '研发办公室'} · 当前阶段的责任与交接`;
      dialog.querySelector('[data-stage-owner]').textContent = definition[1];
      dialog.querySelector('[data-stage-mode]').textContent = definition[4].includes('自动') ? 'AI 自动' : 'CEO 检查点';
      dialog.querySelector('[data-stage-ceo]').textContent = definition[4];
      dialog.querySelector('[data-stage-input]').textContent = definition[2];
      dialog.querySelector('[data-stage-output]').textContent = definition[3];
      const advance = dialog.querySelector('[data-stage-advance]');
      const next = definitions[selectedIndex + 1];
      advance.textContent = next ? `推进到${next[0]}` : '已完成全部阶段';
      advance.disabled = !next;
      dialog.showModal();
    };
    dialog.querySelector('[data-stage-advance]').addEventListener('click', () => {
      const next = definitions[selectedIndex + 1];
      if (!next) return;
      progress = selectedIndex + 1;
      localStorage.setItem(progressKey, String(progress));
      applyProgress();
      writeState({ lastAssistantMessage: `${definitions[selectedIndex][0]}已完成，${next[0]}开始接手。`, lastAssistantHandoff: { label: page === 'workspace-runtime-xhs.html' ? '小红书运营办公室' : '研发办公室', route: page, message: `${next[0]}已开始` } });
      close();
      showToast(`已推进到${next[0]}`);
    });
    nodes.forEach((node, index) => {
      const definition = definitions[index];
      if (!definition) return;
      node.setAttribute('role', 'button');
      node.setAttribute('tabindex', '0');
      if (page === 'workspace-runtime-shortvideo.html') return;
      const open = () => openDefinition(definition);
      node.addEventListener('click', open);
      node.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); } });
    });
    if (page === 'workspace-runtime-shortvideo.html') {
      const pipeline = document.querySelector('#pipeline');
      const stageDefinition = node => {
        const label = node.querySelector('.stage-name')?.textContent.trim().replace(/\s*\d+\s*$/, '');
        return definitions.find(item => item[0] === label || label?.startsWith(`${item[0]} `));
      };
      pipeline?.addEventListener('click', event => {
        const node = event.target.closest('.stage-header');
        if (!node) return;
        openDefinition(stageDefinition(node));
      });
      pipeline?.addEventListener('keydown', event => {
        if (!['Enter', ' '].includes(event.key)) return;
        const node = event.target.closest('.stage-header');
        if (!node) return;
        event.preventDefault();
        openDefinition(stageDefinition(node));
      });
    }
  }

  function ensureFoundingTemplateOptions() {
    if (!window.location.pathname.endsWith('founding-flow.html')) return;
    const options = document.querySelector('.bet-options');
    if (!options) return;
    Object.entries(FOUNDING_TEMPLATES).forEach(([key, template]) => {
      let option = options.querySelector(`[data-curis-template="${key}"]`);
      if (!option) {
        option = document.createElement('div');
        option.className = 'bet-option';
        option.dataset.curisTemplate = key;
        option.innerHTML = `<h4></h4><p></p>`;
        options.appendChild(option);
      }
      option.querySelector('h4').textContent = template.label;
      option.querySelector('p').textContent = template.description;
      if (!option.__curisBound) {
        option.__curisBound = true;
        option.addEventListener('click', () => {
          writeState({ selectedTemplate: key });
          applyFoundingTemplateSelection(key);
        });
      }
    });
    document.querySelectorAll('.bet-option:not([data-curis-template])').forEach(option => {
      if (option.__curisBound) return;
      option.__curisBound = true;
      option.addEventListener('click', () => writeState({ selectedTemplate: null }));
    });
    const state = readState();
    if (!Object.prototype.hasOwnProperty.call(state, 'selectedTemplate')) {
      const initial = options.querySelector('.bet-option.selected')?.dataset.curisTemplate || 'software';
      writeState({ selectedTemplate: initial });
      applyFoundingTemplateSelection(initial);
    }
  }

  function applyFoundingTemplateSelection(key) {
    const template = FOUNDING_TEMPLATES[key];
    const option = document.querySelector(`[data-curis-template="${key}"]`);
    if (!template || !option) return;
    document.querySelectorAll('.bet-option').forEach(item => item.classList.toggle('selected', item === option));
    const opportunity = document.getElementById('business-opportunity');
    const outcome = document.getElementById('business-outcome');
    const evidence = document.getElementById('business-evidence');
    if (opportunity) opportunity.value = template.opportunity;
    if (outcome) outcome.value = template.outcome;
    if (evidence) {
      let matching = [...evidence.options].find(item => item.textContent.includes(template.feedback));
      if (!matching) {
        matching = document.createElement('option');
        matching.textContent = template.feedback;
        matching.value = template.feedback;
        evidence.appendChild(matching);
      }
      evidence.value = matching.value;
    }
    const assistantText = document.querySelector('.step-panel[data-step="4"] .assistant-text');
    if (assistantText && template.teamIntro) assistantText.textContent = template.teamIntro;
    const teamCards = [...document.querySelectorAll('.step-panel[data-step="4"] .team-card')].slice(0, 4);
    (template.team || []).forEach((member, index) => {
      const card = teamCards[index];
      if (!card) return;
      const role = card.querySelector('.role');
      const name = card.querySelector('h4');
      const description = card.querySelector('p');
      const tags = card.querySelectorAll('.capability-tag');
      if (role) role.textContent = member[0];
      if (name) name.textContent = member[0];
      if (description) description.textContent = member[1];
      tags.forEach((tag, tagIndex) => { tag.textContent = member[tagIndex + 2] || ''; });
    });
    const simValues = [...document.querySelectorAll('.step-panel[data-step="5"] .sim-panel .sim-value')];
    (template.simulation || []).forEach((text, index) => { if (simValues[index]) simValues[index].textContent = text; });
    const simLabels = {
      software: ['正常场景', '缺席场景（CEO 离线 7 天）', '失败场景（验收未通过）'],
      xhs: ['正常场景', '缺席场景（CEO 离线 7 天）', '失败场景（授权或表达异常）'],
      douyin: ['正常场景', '缺席场景（CEO 离线 7 天）', '失败场景（授权或内容风险）']
    }[key] || ['正常场景', '缺席场景（CEO 离线 7 天）', '失败场景（运行异常）'];
    [...document.querySelectorAll('.step-panel[data-step="5"] .sim-panel .sim-label')].forEach((label, index) => { if (simLabels[index]) label.textContent = simLabels[index]; });
  }

  function initTemplateChoice() {
    if (!window.location.pathname.endsWith('founding-flow.html') || document.querySelector('.curis-template-panel')) return;
    const welcome = document.querySelector('.step-panel[data-step="0"] .welcome-center');
    const actions = welcome?.querySelector('.welcome-actions');
    const trigger = actions?.querySelector('.btn-secondary');
    if (!welcome || !actions || !trigger) return;
    const panel = document.createElement('section');
    panel.className = 'curis-template-panel';
    panel.setAttribute('aria-label', '可复用业务模板');
    panel.innerHTML = `<h2>选择一间已经跑通的业务办公室</h2><p>模板只是起点。进入后你仍可以修改能力、员工数量、工作流和验收标准。</p><div class="curis-template-list"><button class="curis-template-option" type="button" data-template="software"><strong>软件开发 · Curis 自研</strong><span>研发、测试、产品协同，把 Curis 自己继续做出来。</span></button><button class="curis-template-option" type="button" data-template="xhs"><strong>内容增长 · 小红书</strong><span>选题、脚本、发布与平台数据回传。</span></button><button class="curis-template-option" type="button" data-template="douyin"><strong>抖音 / TikTok 运营</strong><span>内容策划、制作、发布和外部结果复盘。</span></button></div>`;
    actions.parentNode.insertBefore(panel, actions.nextSibling);
    const templateIntents = {
      software: '我想先用 Curis 自己的 AI 研发团队，把 Curis 做成一个真正能经营公司的产品。',
      xhs: '我想经营小红书内容增长业务，验证 AI 团队能否持续产出内容并通过平台数据获得真实反馈。',
      douyin: '我想经营抖音短视频业务，验证从选题、制作、发布到播放和成交数据回流的完整闭环。'
    };
    trigger.onclick = event => {
      event.preventDefault();
      panel.classList.toggle('is-open');
      if (panel.classList.contains('is-open')) panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    };
    panel.querySelectorAll('[data-template]').forEach(option => option.addEventListener('click', () => {
      const key = option.dataset.template;
      const intent = document.getElementById('ceo-intent');
      if (!intent || !templateIntents[key]) return;
      intent.value = templateIntents[key];
      writeState({ selectedTemplate: key });
      ensureFoundingTemplateOptions();
      applyFoundingTemplateSelection(key);
      goToStep(1);
      window.setTimeout(() => intent.focus(), 120);
    }));
  }

  function initOrganizationRoom() {
    if (!window.location.pathname.endsWith('ai-organization.html') || document.querySelector('.curis-org-room')) return;
    const map = document.querySelector('.org-map');
    const anchor = map?.closest('.section');
    if (!anchor) return;
    const orgState = readState();
    const room = document.createElement('section');
    room.className = 'curis-org-room';
    room.setAttribute('aria-label', 'AI 团队办公现场');
    room.innerHTML = `
      <div class="curis-org-room-head"><div><p class="curis-org-room-kicker">公司空间 · AI 团队</p><h2 class="curis-org-room-title">大家正在各自的办公室里工作</h2><p class="curis-org-room-subtitle">CEO 助理负责汇总，专业 AI 负责推进，Workspace AI 在业务现场执行。</p></div><span class="curis-org-room-meta">5 位专业 AI · 4 个业务空间 AI</span></div>
      <div class="curis-org-room-grid">
        <div class="curis-org-room-team" aria-label="当前在线员工">
          <button class="curis-org-room-person" type="button" data-org-employee="assistant"><span class="curis-org-room-avatar">C</span><span class="curis-org-room-person-copy"><strong>CEO 助理</strong><span>整理早报与待决策事项</span></span><em>工作中</em></button>
          <button class="curis-org-room-person" type="button" data-org-employee="business-engineering"><span class="curis-org-room-avatar">BE</span><span class="curis-org-room-person-copy"><strong>业务工程 AI</strong><span>搭建 Curis v0.2 研发空间</span></span><em>工作中</em></button>
          <button class="curis-org-room-person" type="button" data-org-employee="content-ws"><span class="curis-org-room-avatar">XH</span><span class="curis-org-room-person-copy"><strong>小红书运营 AI</strong><span>等待首条内容数据回传</span></span><em>等待反馈</em></button>
          <button class="curis-org-room-person" type="button" data-org-employee="growth"><span class="curis-org-room-avatar">G</span><span class="curis-org-room-person-copy"><strong>增长营销 AI</strong><span>评估下一条业务方向</span></span><em>分析中</em></button>
        </div>
        <div class="curis-org-room-activity"><p class="curis-org-room-activity-title">最近交接</p><div class="curis-org-room-event"><span class="curis-org-room-event-path">业务工程 AI → 研发 AI</span><span class="curis-org-room-event-note">Curis v0.2 测试包已提交</span></div><div class="curis-org-room-event"><span class="curis-org-room-event-path">小红书运营 AI → CEO 助理</span><span class="curis-org-room-event-note">首条内容等待平台数据授权</span></div><div class="curis-org-room-event"><span class="curis-org-room-event-path">增长营销 AI → 业务分析 AI</span><span class="curis-org-room-event-note">新业务机会进入评估</span></div></div>
      </div>`;
    anchor.parentNode.insertBefore(room, anchor);
    if (!orgState.companyCreatedAt) {
      room.querySelector('.curis-org-room-title').textContent = '公司还没有 AI 团队';
      room.querySelector('.curis-org-room-subtitle').textContent = '完成公司创建后，CEO 助理会先加入，再按第一项业务建立专业 AI 员工。';
      room.querySelector('.curis-org-room-meta').textContent = '等待公司成立';
      room.querySelector('.curis-org-room-team').innerHTML = '<button type="button" class="curis-org-room-person curis-org-create-company"><span class="curis-org-room-avatar">+</span><span class="curis-org-room-person-copy"><strong>创建公司</strong><span>从第一间办公室开始</span></span><em>开始 →</em></button>';
      room.querySelector('.curis-org-room-activity').innerHTML = '<p class="curis-org-room-activity-title">最近交接</p><div class="curis-org-room-event"><span class="curis-org-room-event-path">尚无 AI 员工</span><span class="curis-org-room-event-note">公司成立后，责任、能力和交接才会进入组织记录。</span></div>';
      room.querySelector('.curis-org-create-company')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
      return;
    }
    const hasEvidence = Boolean(orgState.softwareAcceptance || orgState.latestXhsFeedback || orgState.latestExternalFeedback || (orgState.calendarEvents || []).length || (orgState.outcomeAttributions || []).length);
    if (!hasEvidence) {
      room.querySelector('.curis-org-room-meta')?.replaceChildren(document.createTextNode('岗位已配置 · 等待首轮运行'));
      room.querySelectorAll('.curis-org-room-team em').forEach((node, index) => node.textContent = ['等待第一条经营汇报', '等待真实研发运行', '等待平台结果', '等待首个业务假设'][index] || '等待首轮运行');
      const activity = room.querySelector('.curis-org-room-activity');
      if (activity) activity.innerHTML = '<p class="curis-org-room-activity-title">最近交接</p><div class="curis-org-room-event"><span class="curis-org-room-event-path">尚无真实交接</span><span class="curis-org-room-event-note">AI 员工开始运行并产生结果后，交接记录会出现在这里。</span></div>';
    }
    if (orgState.departmentDraft?.name && orgState.departmentStatus === 'active') {
      const team = room.querySelector('.curis-org-room-team');
      const office = document.createElement('button');
      office.className = 'curis-org-room-person';
      office.type = 'button';
      const commitment = orgState.departmentCommitment;
      office.innerHTML = '<span class="curis-org-room-avatar">新</span><span class="curis-org-room-person-copy"><strong></strong><span></span></span><em></em>';
      office.querySelector('strong').textContent = orgState.departmentDraft.name;
      office.querySelector('.curis-org-room-person-copy span').textContent = commitment?.status === 'active'
        ? `首项责任：${commitment.name}`
        : commitment?.status === 'paused'
          ? `已暂停：${commitment.name}`
          : commitment?.status === 'pending_revision'
            ? `待调整：${commitment.name}`
        : '新部门已建立，等待第一项业务承诺';
      office.querySelector('em').textContent = commitment?.status === 'active' ? '运行中' : commitment?.status === 'paused' ? '已暂停' : commitment?.status === 'pending_revision' ? '调整责任 →' : '指定责任 →';
      team?.appendChild(office);
      office.addEventListener('click', () => { window.location.href = commitment?.status === 'active' ? 'workspace-runtime-department.html' : commitment?.status === 'paused' ? 'operating.html' : commitment?.status === 'pending_revision' ? 'workspace-studio.html' : 'business.html'; });
    }
    const business = String(orgState.firstBusiness || '');
    const teamProfiles = /小红书/.test(business)
      ? [['CEO 助理', '整理平台结果与待决策事项', '工作中'], ['策略 AI', '把选题和受众假设交给内容岗位', '等待运行'], ['内容 AI', '准备首轮内容与发布前检查', '等待运行'], ['发布 AI', '等待平台授权或 CEO 手动回传', '等待反馈']]
      : /抖音|TikTok|短视频/.test(business)
        ? [['CEO 助理', '整理播放、互动与成交结果', '工作中'], ['策略 AI', '拆解选题与内容假设', '等待运行'], ['脚本 AI', '准备脚本和制作清单', '等待运行'], ['制作 AI', '等待外部发布与数据回流', '等待反馈']]
        : [['CEO 助理', '整理经营汇报与待决策事项', '工作中'], ['产品 AI', '拆解需求与验收标准', '等待运行'], ['研发 AI', '准备 Curis 增量并提交交付物', '等待运行'], ['QA AI', '等待测试结果与 CEO 验收', '等待验收']];
    room.querySelectorAll('.curis-org-room-person').forEach((button, index) => {
      const profile = teamProfiles[index];
      if (!profile) return;
      button.querySelector('strong')?.replaceChildren(document.createTextNode(profile[0]));
      const note = button.querySelector('.curis-org-room-person-copy span');
      if (note) note.textContent = profile[1];
      const status = button.querySelector('em');
      if (status && hasEvidence) status.textContent = profile[2];
      const avatar = button.querySelector('.curis-org-room-avatar');
      if (avatar) avatar.textContent = profile[0].split(/\s+/).map(part => part[0]).join('').slice(0, 2);
    });
    const roomMeta = room.querySelector('.curis-org-room-meta');
    if (roomMeta) roomMeta.textContent = `${teamProfiles.length} 位核心 AI · ${business ? business.replace('内容增长 · ', '') : '首个业务'}办公室`;
    room.querySelectorAll('[data-org-employee]').forEach(button => button.addEventListener('click', () => {
      const node = document.querySelector(`.org-node[data-employee="${button.dataset.orgEmployee}"]`);
      if (!node) return;
      node.scrollIntoView({ behavior: 'smooth', block: 'center' });
      node.classList.add('curis-focus');
      node.click();
      window.setTimeout(() => node.classList.remove('curis-focus'), 1400);
    }));
  }

  function initOrganizationPerformance() {
    if (!window.location.pathname.endsWith('ai-organization.html') || document.querySelector('.curis-ai-scoreboard')) return;
    const anchor = document.querySelector('.curis-org-room') || document.querySelector('.org-map')?.closest('.section');
    if (!anchor) return;
    const board = document.createElement('section');
    board.className = 'card curis-ai-scoreboard';
    board.setAttribute('aria-labelledby', 'curis-ai-scoreboard-title');
    board.innerHTML = '<div class="curis-ai-scoreboard-head"><div><h2 id="curis-ai-scoreboard-title">AI 员工产出与成本</h2><p>不只看“是否在线”，而是看每位员工是否持续交付可验证结果。</p></div><span>本周期</span></div><div class="curis-ai-scoreboard-list"></div>';
    const style = document.createElement('style');
    style.id = 'curis-ai-scoreboard-style';
    style.textContent = '.curis-ai-scoreboard{margin:0 0 22px}.curis-ai-scoreboard-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px}.curis-ai-scoreboard-head h2{margin:0;font-size:14px}.curis-ai-scoreboard-head p{margin:5px 0 0;color:var(--text-tertiary,#777c86);font-size:10px;line-height:1.45}.curis-ai-scoreboard-head>span{color:var(--text-tertiary,#777c86);font-size:10px;white-space:nowrap}.curis-ai-scoreboard-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;margin-top:14px}.curis-ai-score{min-width:0;padding:11px;background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px}.curis-ai-score strong{display:block;font-size:11px}.curis-ai-score span{display:block;margin-top:5px;color:var(--text-secondary,#a4a7af);font-size:10px;line-height:1.4}.curis-ai-score em{display:block;margin-top:9px;color:var(--status-success,#a8c8b8);font-size:10px;font-style:normal}.curis-ai-score.is-attention em{color:var(--status-warning,#d6c49c)}@media(max-width:860px){.curis-ai-scoreboard-list{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:520px){.curis-ai-scoreboard-list{grid-template-columns:1fr}}';
    document.head.appendChild(style);
    anchor.parentNode.insertBefore(board, anchor.nextSibling);
    const render = () => {
      const state = readState();
      const xhs = state.latestXhsFeedback;
      const shortVideo = state.latestExternalFeedback;
      const software = state.softwareAcceptance;
      const costFor = business => { const pattern = business === '小红书运营' ? /小红书/ : business === '抖音 / TikTok 运营' ? /抖音|TikTok|短视频/ : /软件|Curis|研发/; return (state.financeCosts || []).filter(item => pattern.test(String(item.business || ''))).reduce((sum, item) => sum + Number(item.amount || 0), 0); };
      const softwareRuns = (state.calendarEvents || []).filter(item => item.route === 'workspace-runtime-software.html').length;
      const firstBusiness = String(state.firstBusiness || '');
      const rows = !state.companyCreatedAt ? [
        ['AI 团队', '公司成立后，CEO 助理会先加入', '等待公司创建', true]
      ] : [
        ['CEO 助理', state.lastAssistantMessage ? '最近一次经营汇报已更新' : '等待第一条经营汇报', state.lastAssistantMessage ? '上下文正常' : '待启动', false],
        ...(/小红书/.test(firstBusiness) ? [['小红书内容 AI', xhs ? `最近回传：阅读 ${Number(xhs.reads || 0).toLocaleString()} · 粉丝 ${Number(xhs.follows || 0).toLocaleString()}` : '首条内容等待平台结果', xhs ? `线索价值 ¥${Number(xhs.value || 0).toLocaleString()}` : costFor('小红书运营') ? `已记录成本 ¥${costFor('小红书运营').toLocaleString()}` : '等待成本记录', !xhs]] : /抖音|TikTok|短视频/.test(firstBusiness) ? [['数据回收 AI', shortVideo ? `最近回传：播放 ${Number(shortVideo.plays || 0).toLocaleString()} · 粉丝 ${Number(shortVideo.follows || 0).toLocaleString()}` : '等待抖音 / TikTok 数据', shortVideo ? `成交价值 ¥${Number(shortVideo.value || 0).toLocaleString()}` : costFor('抖音 / TikTok 运营') ? `已记录成本 ¥${costFor('抖音 / TikTok 运营').toLocaleString()}` : '连接器或手动窗口待确认', !shortVideo]] : [['研发 AI', software?.choice === 'accept' ? 'Curis v0.2 已通过 CEO 真实验收' : softwareRuns ? `${softwareRuns} 次研发运行 · 等待 CEO 验收` : '等待真实研发运行', software?.choice === 'accept' ? '已验证 · 真实使用' : costFor('软件开发') ? `已记录成本 ¥${costFor('软件开发').toLocaleString()}` : '等待成本记录', software?.choice !== 'accept']])
      ];
      board.querySelector('.curis-ai-scoreboard-list').innerHTML = rows.map(([name, output, cost, attention]) => `<article class="curis-ai-score${attention ? ' is-attention' : ''}"><strong>${escapeHtml(name)}</strong><span>${escapeHtml(output)}</span><em>${escapeHtml(cost)}</em></article>`).join('');
    };
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initOrganizationResourceView() {
    if (!window.location.pathname.endsWith('ai-organization.html') || document.querySelector('.curis-organization-resource')) return;
    const anchor = document.querySelector('.curis-ai-scoreboard') || document.querySelector('.curis-org-room') || document.querySelector('.org-map')?.closest('.section');
    if (!anchor) return;
    const routeFor = business => business === '软件开发' ? 'workspace-runtime-software.html' : business === '小红书运营' ? 'workspace-runtime-xhs.html' : 'workspace-runtime-shortvideo.html';
    const normalize = value => /小红书/.test(String(value || '')) ? '小红书运营' : /抖音|TikTok|短视频/.test(String(value || '')) ? '抖音 / TikTok 运营' : /软件|Curis 自研|研发/.test(String(value || '')) ? '软件开发' : '公司共享';
    const defaultContracts = { '软件开发': { maxConcurrent: 3, capacityPct: 82, queuePolicy: '失败即暂停' }, '小红书运营': { maxConcurrent: 4, capacityPct: 72, queuePolicy: 'CEO 发布前确认' }, '抖音 / TikTok 运营': { maxConcurrent: 3, capacityPct: 68, queuePolicy: '授权或结果异常时升级' } };
    const view = document.createElement('section');
    view.className = 'card curis-organization-resource';
    view.setAttribute('aria-labelledby', 'curis-organization-resource-title');
    view.innerHTML = '<div class="curis-resource-head"><div><p class="curis-resource-kicker">公司能力供给 · 负载与交接</p><h2 id="curis-organization-resource-title">AI 团队正在被哪些业务占用？</h2><p>把业务投入和 AI 员工负载放在一起看。压力不是单纯的在线人数，而是等待 CEO、运行成本、结果价值和下一次交接是否匹配。</p></div><button type="button" data-resource-snapshot>保存当前资源判断</button></div><div class="curis-resource-grid"></div>';
    const render = () => {
      const state = readState();
      const businesses = ['软件开发', '小红书运营', '抖音 / TikTok 运营'];
      const firstBusiness = String(state.firstBusiness || '');
      const active = !state.companyCreatedAt ? [] : businesses.filter(business => business === '软件开发' && /软件|Curis|研发/.test(firstBusiness) || business === '小红书运营' && /小红书/.test(firstBusiness) || business === '抖音 / TikTok 运营' && /抖音|TikTok|短视频/.test(firstBusiness));
      const outcomes = Array.isArray(state.outcomeAttributions) ? state.outcomeAttributions : [];
      const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
      const capabilityByContext = state.capabilityRuntimeByContext || {};
      const contracts = state.capacityContracts || {};
      const rows = active.map(business => {
        const businessRuns = runs.filter(run => normalize(run.business) === business);
        const pending = businessRuns.filter(run => ['waiting_ceo', 'acknowledged'].includes(run.status)).length;
        const queued = businessRuns.filter(run => run.status === 'queued').length;
        const totalRuns = businessRuns.length;
        const cost = businessRuns.reduce((sum, run) => sum + Number(run.cost || 0), 0);
        const value = outcomes.filter(item => normalize(item.business) === business && item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
        const averageMinutes = key => { const values = businessRuns.map(run => Number(run[key] || 0)).filter(value => value > 0); return values.length ? `${Math.round(values.reduce((sum, value) => sum + value, 0) / values.length / 60000)} 分钟` : '—'; };
        const responseTime = averageMinutes('ceoResponseMs');
        const resolutionTime = averageMinutes('ceoResolutionMs');
        const route = routeFor(business);
        const capability = capabilityByContext[route] || {};
        const contract = { ...defaultContracts[business], ...(contracts[business] || {}) };
        const loadUnits = (pending + queued) * 2 + Math.min(totalRuns, contract.maxConcurrent);
        const utilization = Math.min(100, Math.round((loadUnits / Math.max(1, contract.maxConcurrent * 2)) * 100));
        const pressure = utilization >= 90 || (totalRuns >= 4 && value === 0) ? '需要重新分配' : utilization >= 70 || pending ? '需要关注' : '可承接';
        const defaultAgent = business === '软件开发' ? '研发 AI' : business === '小红书运营' ? '内容 AI' : '数据 AI';
        return { business, route, pending, queued, totalRuns, cost, value, pressure, utilization, contract, responseTime, resolutionTime, model: capability.model || '共享模型', agent: capability.agent || defaultAgent, connector: capability.connector || (business === '软件开发' ? '手动录入' : '需要授权') };
      });
      view.querySelector('.curis-resource-grid').innerHTML = rows.length ? rows.map(row => `<article class="curis-resource-row"><div class="curis-resource-row-head"><div><h3>${escapeHtml(row.business)}</h3><p>${escapeHtml(row.agent)} · ${escapeHtml(row.model)} · ${escapeHtml(row.connector)}</p></div><span class="${row.pressure === '可承接' ? 'is-ok' : 'is-attention'}">${escapeHtml(row.pressure)}</span></div><div class="curis-resource-metrics"><div><small>容量占用</small><strong>${row.utilization}%</strong></div><div><small>并发上限</small><strong>${row.contract.maxConcurrent} 项</strong></div><div><small>排队中</small><strong>${row.queued} 项</strong></div><div><small>待 CEO 处理</small><strong>${row.pending} 次</strong></div><div><small>运行成本</small><strong>¥${row.cost.toLocaleString()}</strong></div><div><small>CEO 响应</small><strong>${escapeHtml(row.responseTime)}</strong></div><div><small>闭环处理</small><strong>${escapeHtml(row.resolutionTime)}</strong></div><div><small>已验证价值</small><strong>¥${row.value.toLocaleString()}</strong></div><div><small>升级规则</small><strong>${escapeHtml(row.contract.queuePolicy)}</strong></div></div><div class="curis-resource-row-foot"><span>${row.queued ? '队列正在等待容量释放' : row.pending ? '先清理交接，再承接更多业务' : row.totalRuns ? `当前占用 ${row.utilization}%，可以继续观察` : '还没有真实运行记录'}</span><div><button type="button" data-resource-open="${escapeHtml(row.business)}">查看业务</button><button type="button" data-resource-adjust="${escapeHtml(row.business)}">调整分配</button></div></div></article>`).join('') : '<div class="curis-org-empty"><strong>还没有已启用的业务办公室</strong><span>先创建公司并启用第一项业务，AI 团队的容量才会有真实归属。</span></div>';
      view.querySelectorAll('[data-resource-open]').forEach(button => button.addEventListener('click', () => { const business = button.dataset.resourceOpen; writeState({ lastAssistantMessage: `已打开${business}的运行现场，CEO 助理会带上当前负载和能力组合。`, lastAssistantHandoff: { label: business, route: routeFor(business), message: '查看业务运行现场' } }); window.location.href = routeFor(business); }));
      view.querySelectorAll('[data-resource-adjust]').forEach(button => button.addEventListener('click', () => { const business = button.dataset.resourceAdjust; const existing = contracts[business] || defaultContracts[business]; openFormDialog({ title: `调整${business}能力分配`, description: '先写清楚容量边界和交接，再改变模型、Agent 或投入比例；已有上下文不会被删除。', submitLabel: '保存分配', fields: [{ name: 'maxConcurrent', label: '最大并发事项', type: 'number', value: existing.maxConcurrent, required: true }, { name: 'capacityPct', label: '本周期可用容量（%）', type: 'number', value: existing.capacityPct, required: true }, { name: 'queuePolicy', label: '升级规则', type: 'select', options: ['失败即暂停', 'CEO 发布前确认', '授权或结果异常时升级', '低风险自动推进'], value: existing.queuePolicy, required: true }, { name: 'allocation', label: '本周期容量安排', placeholder: '例如：策略 AI 60% · 内容 AI 80%', required: true }, { name: 'handoff', label: '交接路径', placeholder: '例如：研究 AI → 内容 AI → CEO 发布确认', required: true }, { name: 'reason', label: '为什么调整', type: 'textarea', placeholder: '例如：待 CEO 事项增加，需要先减少新任务并清理发布前检查点。', required: true }], onSubmit: values => { const current = readState(); const allocations = Array.isArray(current.resourceAllocations) ? current.resourceAllocations : []; const contracts = { ...(current.capacityContracts || {}), [business]: { maxConcurrent: Math.max(1, Number(values.maxConcurrent || existing.maxConcurrent)), capacityPct: Math.min(100, Math.max(0, Number(values.capacityPct || existing.capacityPct))), queuePolicy: values.queuePolicy } }; const record = { business, ...values, maxConcurrent: contracts[business].maxConcurrent, capacityPct: contracts[business].capacityPct, route: routeFor(business), at: new Date().toISOString() }; writeState({ capacityContracts: contracts, resourceAllocations: [...allocations, record].slice(-24), employeeAssignments: { ...(current.employeeAssignments || {}), [`business:${business}`]: record }, lastAssistantMessage: `${business}的能力分配已更新：并发上限 ${record.maxConcurrent} 项，容量 ${record.capacityPct}%。我会在下一次结果回报时检查交接是否变顺。`, lastAssistantHandoff: { label: 'AI 组织办公室', route: 'ai-organization.html', message: '能力分配已更新' } }); const promoted = promoteQueuedRuns(business); render(); showToast(promoted ? `能力分配已保存，已释放 ${promoted} 项排队任务` : '能力分配已保存'); } }); }));
    };
    const style = document.createElement('style');
    style.textContent = '.curis-organization-resource{margin:0 0 22px}.curis-resource-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px}.curis-resource-kicker{margin:0 0 5px;color:var(--text-secondary,#a4a7af);font-size:10px;letter-spacing:.08em}.curis-resource-head h2{margin:0;font-size:15px}.curis-resource-head p{max-width:720px;margin:6px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.5}.curis-resource-head button,.curis-resource-row-foot button{padding:7px 9px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer;white-space:nowrap}.curis-resource-grid{display:grid;gap:8px;margin-top:15px}.curis-resource-row{padding:12px;border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px;background:var(--bg-base-default,#191a1d)}.curis-resource-row-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.curis-resource-row-head h3{margin:0;font-size:12px}.curis-resource-row-head p{margin:4px 0 0;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-resource-row-head>span{padding:4px 6px;color:var(--status-warning,#d6c49c);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:5px;font-size:10px;white-space:nowrap}.curis-resource-row-head>span.is-ok{color:var(--status-success,#a8c8b8)}.curis-resource-metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;margin-top:10px;background:var(--border-neutral-l1,rgba(224,226,242,.1));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:6px;overflow:hidden}.curis-resource-metrics>div{display:grid;gap:4px;padding:8px;background:var(--bg-base-secondary,#202226)}.curis-resource-metrics small{color:var(--text-secondary,#a4a7af);font-size:9px}.curis-resource-metrics strong{font-size:13px}.curis-resource-row-foot{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-resource-row-foot>div{display:flex;gap:6px}.curis-resource-row-foot button:last-child{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}@media(max-width:900px){.curis-resource-metrics{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:620px){.curis-resource-head,.curis-resource-row-foot{align-items:flex-start;flex-direction:column}.curis-resource-head button,.curis-resource-row-foot button{width:100%}.curis-resource-row-foot>div{width:100%}.curis-resource-row-foot>div button{flex:1}.curis-resource-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}';
    document.head.appendChild(style);
    view.querySelector('[data-resource-snapshot]').addEventListener('click', () => { const current = readState(); writeState({ organizationResourceSnapshotAt: new Date().toISOString(), organizationResourceSnapshot: { runs: (current.calendarEvents || []).length, pendingCEO: (current.calendarEvents || []).filter(item => ['waiting_ceo', 'acknowledged'].includes(item.status)).length, capacityContracts: current.capacityContracts || {} }, lastAssistantMessage: '公司能力供给快照已保存，下一次经营汇报会比较负载和交接变化。' }); showToast('资源判断已保存'); });
    anchor.parentNode.insertBefore(view, anchor.nextSibling);
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initDepartmentCreation() {
    if (!window.location.pathname.endsWith('ai-organization.html') || document.querySelector('.curis-department-create')) return;
    const anchor = document.querySelector('.curis-org-room') || document.querySelector('.org-map')?.closest('.section');
    if (!anchor) return;
    const panel = document.createElement('section');
    panel.className = 'curis-department-create';
    panel.setAttribute('aria-labelledby', 'curis-department-create-title');
    panel.innerHTML = `<div class="curis-department-create-head"><div><p class="curis-department-create-kicker">公司结构 · 部门办公室</p><h2 id="curis-department-create-title" class="curis-department-create-title">当重复责任需要共同能力，就创建一间新办公室</h2><p class="curis-department-create-note">部门不是多一层管理，而是把稳定的责任、共享能力和交接路径放在一起。</p></div><button class="curis-department-create-toggle" type="button" data-curis-handled="true">创建部门</button></div><form class="curis-department-create-form"><div class="curis-department-create-field"><label for="curis-department-name">部门名称</label><input id="curis-department-name" name="name" placeholder="例如：研发办公室" required /></div><div class="curis-department-create-field"><label for="curis-department-purpose">承担的共同责任</label><textarea id="curis-department-purpose" name="purpose" rows="2" placeholder="例如：持续交付 Curis 软件增量，并负责测试与 CEO 验收" required></textarea></div><button class="curis-department-create-submit" type="submit" data-curis-handled="true">生成部门办公室草案 →</button></form>`;
    anchor.parentNode.insertBefore(panel, anchor);
    const form = panel.querySelector('form');
    panel.querySelector('.curis-department-create-toggle').addEventListener('click', () => {
      panel.classList.toggle('is-open');
      if (panel.classList.contains('is-open')) form.elements.name.focus();
    });
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!readState().companyCreatedAt) {
        writeState({ lastAssistantMessage: '部门属于公司结构。先完成公司创建，再安排新的办公室。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '先完成公司创建' } });
        window.location.href = 'founding-flow.html';
        return;
      }
      const draft = { name: form.elements.name.value.trim(), purpose: form.elements.purpose.value.trim(), at: new Date().toISOString() };
      if (!draft.name || !draft.purpose) return;
      writeState({
        departmentDraft: draft,
        departmentStatus: 'pending_approval',
        departmentCommitment: null,
        lastAssistantMessage: `部门办公室草案“${draft.name}”已经形成。我会先检查它是否有稳定责任、共享能力和可承接的业务结果。`,
        lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: `搭建部门办公室：${draft.name}` }
      });
      panel.classList.add('is-ready');
      panel.querySelector('.curis-department-create-title').textContent = `${draft.name} 办公室草案已生成`;
      panel.querySelector('.curis-department-create-note').textContent = '下一步：业务工程 AI 会把责任、能力和工作流装配成可模拟的业务空间。';
      const submit = panel.querySelector('.curis-department-create-submit');
      submit.textContent = '进入工作空间搭建 →';
      submit.type = 'button';
      submit.onclick = () => { window.location.href = 'workspace-studio.html'; };
      showToast('部门草案已生成');
    });
  }

  function initOrganizationDynamicMap() {
    if (!window.location.pathname.endsWith('ai-organization.html') || document.querySelector('.curis-dynamic-org-node')) return;
    const state = readState();
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    if (!department?.name || !commitment?.name || state.departmentStatus !== 'active') return;
    const levels = [...document.querySelectorAll('.org-map .org-level')];
    const level = levels[levels.length - 1];
    if (!level) return;
    const node = document.createElement('div');
    node.className = 'org-node curis-dynamic-org-node';
    node.setAttribute('role', 'button');
    node.setAttribute('tabindex', '0');
    const paused = commitment.status === 'paused';
    const result = state.departmentResult;
    node.innerHTML = '<div class="org-avatar" style="color:var(--text-secondary)">新</div><div class="org-name"></div><div class="org-role"></div><div class="org-meta"><span class="pill"></span><div class="org-capacity-bar"><div class="org-capacity-fill"></div></div></div>';
    node.querySelector('.org-name').textContent = department.name;
    node.querySelector('.org-role').textContent = commitment.name;
    const pill = node.querySelector('.pill');
    pill.className = `pill ${paused ? 'pill-attention' : result?.status === '结果异常' ? 'pill-blocked' : 'pill-ontrack'}`;
    pill.textContent = paused ? '已暂停' : result?.status === '结果异常' ? '异常' : result ? '有结果' : '运行中';
    const fill = node.querySelector('.org-capacity-fill');
    fill.style.width = paused ? '0%' : result ? '58%' : '44%';
    level.appendChild(node);
    const mapMeta = document.querySelector('.org-map')?.closest('.card')?.querySelector('.section-meta');
    if (mapMeta) mapMeta.textContent = `${department.name} 已加入组织 · 首项责任：${commitment.name}`;
    const matrix = document.querySelector('.matrix-table tbody');
    if (matrix && !matrix.querySelector('.curis-dynamic-matrix-row')) {
      const row = document.createElement('tr');
      row.className = 'curis-dynamic-matrix-row';
      row.innerHTML = '<td><div class="row-name"></div><div class="row-role">部门办公室</div></td><td><span class="matrix-icon icon-full">●</span> 首项责任</td><td><span class="matrix-icon icon-delegate">△</span> 向下委派</td><td><span class="matrix-icon icon-full">●</span> 责任范围内</td><td><span class="matrix-icon icon-coord">Assistant / CEO</span></td><td><span class="matrix-icon icon-coord">CEO</span></td>';
      row.querySelector('.row-name').textContent = department.name;
      matrix.appendChild(row);
    }
    const capacityValue = document.querySelector('.capacity-grid .capacity-item .capacity-value');
    if (capacityValue && !paused) capacityValue.textContent = result ? '76%' : '74%';
    const navigate = () => { window.location.href = paused ? 'operating.html' : 'workspace-runtime-department.html'; };
    node.addEventListener('click', navigate);
    node.addEventListener('keydown', event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); navigate(); } });
  }

  function initOrganizationTruthMap() {
    if (!window.location.pathname.endsWith('ai-organization.html')) return;
    const state = readState();
    const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
    const pending = runs.filter(item => ['waiting_ceo', 'acknowledged'].includes(item.status)).length;
    const hasEvidence = Boolean(runs.length || state.softwareAcceptance || state.latestXhsFeedback || state.latestExternalFeedback || (state.outcomeAttributions || []).length);
    const map = document.querySelector('.org-map');
    if (map) {
      const firstBusiness = String(state.firstBusiness || state.newBusinessDraft?.name || '');
      const activeEmployeeIds = /小红书/.test(firstBusiness)
        ? new Set(['ceo', 'assistant', 'business-analysis', 'growth', 'content-ws'])
        : /抖音|TikTok|短视频/.test(firstBusiness)
          ? new Set(['ceo', 'assistant', 'business-analysis', 'growth', 'shortvideo-ws'])
          : /软件|Curis|研发/.test(firstBusiness)
            ? new Set(['ceo', 'assistant', 'business-engineering', 'engineering', 'dev-ws'])
            : new Set(['ceo', 'assistant']);
      map.querySelectorAll('.org-node[data-employee]').forEach(node => {
        const visible = activeEmployeeIds.has(node.dataset.employee);
        node.hidden = !visible;
        node.style.display = visible ? '' : 'none';
      });
      const mapProfiles = /小红书/.test(firstBusiness)
        ? { 'business-analysis': ['策略 AI', '趋势与选题分析'], growth: ['复盘 AI', '结果归因与下一轮'], 'content-ws': ['小红书 Workspace AI', '内容生产与发布'] }
        : /抖音|TikTok|短视频/.test(firstBusiness)
          ? { 'business-analysis': ['策略 AI', '受众与选题分析'], growth: ['数据 AI', '结果回收与复盘'], 'shortvideo-ws': ['抖音 / TikTok Workspace AI', '制作、发布与数据回流'] }
          : { 'business-engineering': ['业务工程 AI', '研发空间交付'], engineering: ['研发 AI', '实现与发布准备'], 'dev-ws': ['研发 Workspace AI', '代码、测试与验收'] };
      Object.entries(mapProfiles).forEach(([id, [name, role]]) => {
        const node = map.querySelector(`.org-node[data-employee="${id}"]`);
        if (!node) return;
        node.querySelector('.org-name')?.replaceChildren(document.createTextNode(name));
        node.querySelector('.org-role')?.replaceChildren(document.createTextNode(role));
      });
      map.querySelectorAll('.org-node:not([data-employee="ceo"])').forEach(node => {
        node.querySelector('.org-capacity-bar')?.remove();
        const pill = node.querySelector('.org-meta .pill');
        if (pill) {
          pill.className = `pill ${hasEvidence ? (pending ? 'pill-attention' : 'pill-ontrack') : 'pill-attention'}`;
          pill.textContent = hasEvidence ? (pending ? '有待处理' : '已记录运行') : '岗位已配置';
        }
      });
      const card = map.closest('.card');
      const meta = card?.querySelector('.section-meta');
      if (meta) meta.textContent = hasEvidence ? '组织关系固定 · 运行数据见下方能力供给' : '组织关系已配置 · 等待首轮运行';
    }
    const capacityItems = [...document.querySelectorAll('.capacity-grid .capacity-item, .grid-3 .capacity-item')];
    const summaries = [
      ['AI 团队运行记录', runs.length ? `${runs.length} 次` : '—', runs.length ? '当前周期已写回公司日历' : '等待首轮运行'],
      ['CEO 待处理事项', pending ? `${pending} 项` : '—', pending ? '来自真实运行交接' : '暂无真实待处理记录'],
      ['外部平台连接', state.lastConnector?.status === 'pending' ? '待授权' : (state.latestXhsFeedback || state.latestExternalFeedback ? '已有回传' : '—'), state.lastConnector?.status === 'pending' ? '授权完成前保留手动窗口' : '等待 API 或 CEO 手动回传'],
      ['内容创作能力', state.latestXhsFeedback || state.latestExternalFeedback ? '已有结果' : '待首轮运行', state.latestXhsFeedback || state.latestExternalFeedback ? '结果已进入复盘' : '还没有真实内容结果'],
      ['软件开发能力', state.softwareAcceptance ? (state.softwareAcceptance.choice === 'accept' ? '已验收' : '待处理') : '待首轮运行', state.softwareAcceptance ? 'CEO 验收记录已保存' : '还没有真实研发验收']
    ];
    capacityItems.forEach((item, index) => {
      const summary = summaries[index];
      if (!summary) return;
      const label = item.querySelector('.capacity-label');
      const value = item.querySelector('.capacity-value');
      const note = item.querySelector('.capacity-note');
      if (label) label.textContent = summary[0];
      if (value) value.textContent = summary[1];
      if (note) note.textContent = summary[2];
      item.querySelector('.capacity-bar')?.remove();
      item.querySelector('.capacity-fill')?.remove();
    });
  }

  function initOrganizationEscalationTruth() {
    if (!window.location.pathname.endsWith('ai-organization.html')) return;
    const list = document.querySelector('.escalation-list');
    const anomalyGrid = document.querySelector('.anomaly-grid');
    if (!list || !anomalyGrid) return;
    const render = () => {
      const state = readState();
      const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
      const pending = runs.filter(run => ['queued', 'waiting_ceo', 'acknowledged', 'failed'].includes(run.status));
      const connectorPending = state.lastConnector?.status === 'pending';
      const pill = list.closest('.card')?.querySelector('.card-header .pill');
      if (pill) pill.textContent = `${pending.length + (connectorPending ? 1 : 0)} 项活跃`;
      if (!pending.length && !connectorPending) {
        list.innerHTML = '<div class="curis-org-empty"><strong>当前没有需要 CEO 介入的升级事项</strong><span>失败、权限异常、结果异常或等待 CEO 决策的真实运行会出现在这里。</span></div>';
      } else {
        const items = pending.map(run => {
          const status = run.status === 'failed' ? '失败后暂停' : run.status === 'waiting_ceo' || run.status === 'acknowledged' ? '等待 CEO 处理' : '排队等待容量';
          const label = run.business || run.title || '公司共享运行';
          return `<div class="escalation-item"><div class="escalation-path"><span class="escalation-node">${escapeHtml(run.agent || run.owner || 'Workspace AI')}</span><span class="escalation-arrow">→</span><span class="escalation-node">CEO 助理</span>${run.requiresCEO ? '<span class="escalation-arrow">→</span><span class="escalation-node current">CEO</span>' : ''}</div><div class="escalation-desc">${escapeHtml(run.output || run.task || status)}</div><div class="escalation-impact">影响：${escapeHtml(label)} · ${escapeHtml(status)}</div><div class="escalation-actions"><button class="btn btn-secondary btn-sm" type="button" data-org-run-route="${escapeHtml(run.route || 'calendar.html')}">查看</button></div></div>`;
        });
        if (connectorPending) items.push('<div class="escalation-item"><div class="escalation-path"><span class="escalation-node">外部连接器</span><span class="escalation-arrow">→</span><span class="escalation-node current">CEO</span></div><div class="escalation-desc">平台授权尚未完成，暂时保留手动结果窗口。</div><div class="escalation-impact">影响：外部结果暂不能自动回传</div><div class="escalation-actions"><button class="btn btn-secondary btn-sm" type="button" data-org-run-route="calendar.html">查看日历</button></div></div>');
        list.innerHTML = items.join('');
        list.querySelectorAll('[data-org-run-route]').forEach(button => button.addEventListener('click', () => { window.location.href = button.dataset.orgRunRoute; }));
      }
      const anomalies = [];
      if (connectorPending) anomalies.push(['外部连接待授权', '平台结果暂时不能自动回流，CEO 需要确认授权或手动窗口。']);
      if (pending.some(run => run.status === 'failed')) anomalies.push(['运行失败', '至少有一项真实运行失败，相关业务已暂停等待处理。']);
      const activeRuns = runs.filter(run => ['running', 'queued', 'waiting_ceo', 'acknowledged'].includes(run.status)).length;
      if (activeRuns > 0 && activeRuns > Number(state.capacityContracts?.['公司共享']?.maxConcurrent || 99)) anomalies.push(['公司共享容量', '真实运行数量超过当前共享能力合同，需要重新安排。']);
      anomalyGrid.innerHTML = anomalies.length ? anomalies.map(([title, note]) => `<div class="anomaly-card overload"><div class="anomaly-title">${escapeHtml(title)}</div><div class="anomaly-meta">${escapeHtml(note)}</div><div class="anomaly-actions"><button class="btn btn-secondary btn-sm" type="button" data-org-anomaly-route="decision-room.html">进入决策室</button></div></div>`).join('') : '<div class="curis-org-empty"><strong>当前没有需要 CEO 关注的组织异常</strong><span>组织异常只在真实运行、连接器或能力容量产生证据后出现。</span></div>';
      const meta = anomalyGrid.closest('.section')?.querySelector('.section-meta');
      if (meta) meta.textContent = anomalies.length ? '需 CEO 关注或决策' : '暂无真实异常';
      anomalyGrid.querySelectorAll('[data-org-anomaly-route]').forEach(button => button.addEventListener('click', () => { window.location.href = button.dataset.orgAnomalyRoute; }));
    };
    const style = document.createElement('style');
    style.textContent = '.curis-org-empty{display:flex;flex-direction:column;gap:5px;padding:18px;border:1px dashed var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:8px;color:var(--text-secondary,#a4a7af);font-size:11px}.curis-org-empty strong{color:var(--text-default,#e2e3e7);font-size:12px}.curis-org-empty span{line-height:1.5}';
    document.head.appendChild(style);
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initCapacityExpansion() {
    if (!window.location.pathname.endsWith('ai-organization.html') || document.querySelector('.curis-capacity-callout')) return;
    const state = readState();
    const decision = state.businessDecision;
    if (decision?.choice !== 'scale') return;
    const businessTitle = decision.businessTitle || (decision.platform === '小红书' ? '小红书运营' : decision.platform === '抖音 / TikTok' ? '抖音 / TikTok 运营' : '软件开发');
    const profiles = {
      '软件开发': { title: '研发业务需要一组新的容量安排', roles: [['工程 AI', '78% → 88%'], ['QA AI', '55% → 72%']], handoff: '研发提交 → QA 回归', office: '研发办公室', route: 'workspace-runtime-software.html', cost: 680 },
      '小红书运营': { title: '小红书业务需要一组新的容量安排', roles: [['内容制作 AI', '60% → 78%'], ['策略分析 AI', '45% → 62%']], handoff: '研究 → 产出', office: '小红书运营办公室', route: 'workspace-runtime-xhs.html', cost: 420 },
      '抖音 / TikTok 运营': { title: '短视频业务需要一组新的容量安排', roles: [['Content AI', '60% → 80%'], ['Growth AI', '52% → 65%']], handoff: '数据回流 → 复盘', office: '抖音 / TikTok 运营办公室', route: 'workspace-runtime-shortvideo.html', cost: 960 }
    };
    const profile = profiles[businessTitle] || profiles['软件开发'];
    const anchor = document.querySelector('.curis-org-room') || document.querySelector('.org-map')?.closest('.section');
    if (!anchor) return;
    const saved = readState().capacityDecision;
    const callout = document.createElement('section');
    callout.className = `curis-capacity-callout${saved?.choice === 'approve' ? ' is-approved' : ''}`;
    callout.setAttribute('aria-labelledby', 'curis-capacity-callout-title');
    callout.innerHTML = `<div class="curis-capacity-callout-head"><div><p class="curis-capacity-callout-kicker">扩大业务 · 能力供给调整</p><h2 id="curis-capacity-callout-title" class="curis-capacity-callout-title"></h2><p class="curis-capacity-callout-note">CEO 已选择扩大业务。先确认负载、岗位和下一次交接，再让业务办公室接住更多结果。</p></div></div><div class="curis-capacity-callout-grid"><div class="curis-capacity-callout-item"><span></span><strong></strong></div><div class="curis-capacity-callout-item"><span></span><strong></strong></div><div class="curis-capacity-callout-item"><span>新增交接</span><strong></strong></div></div><div class="curis-capacity-callout-actions"><button class="primary" type="button" data-capacity-choice="approve" data-curis-handled="true">确认扩容配置</button><button type="button" data-capacity-choice="hold" data-curis-handled="true">先维持现状</button><button type="button" data-capacity-choice="workspace" data-curis-handled="true">去工作空间</button></div>`;
    const gridItems = callout.querySelectorAll('.curis-capacity-callout-item');
    gridItems[0].querySelector('span').textContent = profile.roles[0][0];
    gridItems[0].querySelector('strong').textContent = profile.roles[0][1];
    gridItems[1].querySelector('span').textContent = profile.roles[1][0];
    gridItems[1].querySelector('strong').textContent = profile.roles[1][1];
    gridItems[2].querySelector('strong').textContent = profile.handoff;
    const costItem = document.createElement('div');
    costItem.className = 'curis-capacity-callout-item';
    costItem.innerHTML = '<span>预计新增成本 / 周期</span><strong></strong>';
    costItem.querySelector('strong').textContent = `¥${profile.cost.toLocaleString()}`;
    callout.querySelector('.curis-capacity-callout-grid').appendChild(costItem);
    anchor.parentNode.insertBefore(callout, anchor);
    const render = () => {
      const approved = readState().capacityDecision?.choice === 'approve';
      callout.classList.toggle('is-approved', approved);
      callout.querySelector('.curis-capacity-callout-title').textContent = approved ? `${businessTitle}扩容配置已确认` : profile.title;
      callout.querySelector('.curis-capacity-callout-note').textContent = approved ? `${profile.office}已接收新的容量与交接安排；预计每周期增加 ¥${profile.cost.toLocaleString()}，CEO 助理会在下一次结果回来后继续汇报。` : `CEO 已选择扩大${businessTitle}。AI 组织需要先确认负载、岗位和下一次交接，再让${profile.office}接住更多结果。预计每周期增加 ¥${profile.cost.toLocaleString()}。`;
    };
    render();
    callout.querySelectorAll('[data-capacity-choice]').forEach(button => button.addEventListener('click', () => {
      const choice = button.dataset.capacityChoice;
      if (choice === 'workspace') {
        window.location.href = 'workspace-portal.html';
        return;
      }
      const labels = { approve: '确认扩容配置', hold: '先维持现状' };
      if (!labels[choice]) return;
      const cadence = { '软件开发': '每次提交后 · QA 并行回归', '小红书运营': '每天 08:00 / 14:00', '抖音 / TikTok 运营': '每天 12:00 / 18:00' }[businessTitle];
      if (choice === 'approve' && cadence) {
        try {
          const schedules = JSON.parse(localStorage.getItem('curis-schedules') || '[]');
          const scheduleIds = { '软件开发': 'qa-regression', '小红书运营': 'xhs-research', '抖音 / TikTok 运营': 'shortvideo-data' };
          const scheduled = schedules.find(item => item.id === scheduleIds[businessTitle]);
          if (scheduled) { scheduled.schedule = cadence; scheduled.capacity = profile.roles; }
          localStorage.setItem('curis-schedules', JSON.stringify(schedules));
        } catch (_) {}
      }
      writeState({
        capacityDecision: { choice, label: labels[choice], businessTitle, platform: decision.platform || '', allocation: profile.roles, handoff: profile.handoff, schedule: choice === 'approve' ? cadence : '', incrementalCost: profile.cost, at: new Date().toISOString() },
        financeCapacityPlan: { businessTitle, status: choice === 'approve' ? 'approved' : 'held', incrementalCost: profile.cost, schedule: choice === 'approve' ? cadence : '', allocation: profile.roles, at: new Date().toISOString() },
        lastAssistantMessage: choice === 'approve' ? '扩容配置已确认。我会让内容办公室按新的容量继续运行，并在下一次结果回来后汇报。' : '你选择先维持现状。我会继续观察团队负载，超过阈值时再回来提醒。',
        lastAssistantHandoff: { label: choice === 'approve' ? profile.office : 'CEO 工作台', route: choice === 'approve' ? profile.route : 'ceo-desk.html', message: labels[choice] }
      });
      render();
      showToast(`已记录：${labels[choice]}`);
    }));
  }

  function initOrganizationActions() {
    if (!window.location.pathname.endsWith('ai-organization.html')) return;
    const save = [...document.querySelectorAll('.page-actions button')].find(button => button.textContent.trim() === '保存团队快照');
    if (save && save.dataset.curisHandled !== 'true') {
      save.dataset.curisHandled = 'true';
      save.onclick = () => {
        writeState({ organizationSnapshotSavedAt: new Date().toISOString(), lastAssistantMessage: 'AI 团队快照已保存。我会在下一次经营汇报里引用这份组织状态。' });
        showToast('团队快照已保存');
      };
    }
    const arrange = [...document.querySelectorAll('.page-actions button')].find(button => button.textContent.trim() === '安排团队');
    const createToggle = document.querySelector('.curis-department-create-toggle');
    if (arrange && createToggle && arrange.dataset.curisHandled !== 'true') {
      arrange.dataset.curisHandled = 'true';
      arrange.onclick = () => {
        createToggle.click();
        document.querySelector('.curis-department-create')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      };
    }
    document.querySelectorAll('.anomaly-actions button').forEach(button => {
      const label = button.textContent.trim();
      if (label === '安排团队' && createToggle && button.dataset.curisHandled !== 'true') {
        button.dataset.curisHandled = 'true';
        button.onclick = () => {
          if (!document.querySelector('.curis-department-create')?.classList.contains('is-open')) createToggle.click();
          document.querySelector('.curis-department-create')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        };
      }
      if (label === '进入决策室' && button.dataset.curisHandled !== 'true') {
        button.dataset.curisHandled = 'true';
        button.onclick = () => { window.location.href = 'decision-room.html'; };
      }
    });
    const decision = [...document.querySelectorAll('.topbar-right button')].find(button => button.textContent.trim() === '决策室');
    if (decision && decision.dataset.curisHandled !== 'true') {
      decision.dataset.curisHandled = 'true';
      decision.onclick = () => { window.location.href = 'decision-room.html'; };
    }
    const viewMatrix = [...document.querySelectorAll('button')].find(button => button.textContent.trim() === '查看全部');
    if (viewMatrix && viewMatrix.dataset.curisHandled !== 'true') {
      viewMatrix.dataset.curisHandled = 'true';
      viewMatrix.onclick = () => document.querySelector('.matrix-table')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    document.querySelectorAll('.escalation-actions button, .escalation-path button').forEach(button => {
      const label = button.textContent.trim();
      if (button.dataset.curisHandled === 'true') return;
      button.dataset.curisHandled = 'true';
      button.onclick = () => {
        if (label === '标记已处理') {
          button.textContent = '已处理';
          button.disabled = true;
          writeState({ lastAssistantMessage: '一条组织升级已被标记为已处理，我会继续观察后续证据。' });
          showToast('升级已标记为已处理');
          return;
        }
        writeState({ lastAssistantMessage: label === '协调' ? '组织升级已交给 CEO 助理协调，我会在责任重新对齐后汇报。' : '已打开这条组织升级记录。' });
        showToast(label === '协调' ? '已交给 CEO 助理协调' : '已打开升级详情');
      };
    });
    document.querySelectorAll('.drawer-actions button').forEach(button => {
      if (button.dataset.curisHandled === 'true') return;
      const label = button.textContent.trim();
      button.dataset.curisHandled = 'true';
      button.onclick = () => {
        const key = document.querySelector('.org-node.active')?.dataset.employee || 'assistant';
        const employee = window.curisEmployees?.[key] || { name: document.getElementById('drawerTitle')?.textContent || '当前员工', role: 'AI 员工' };
        if (label === '查看完整档案') {
          window.curisOpenEmployeeDrawer?.(key);
          writeState({ lastAssistantMessage: `已展开${employee.name}的完整档案，责任、授权和最近证据均保留在当前组织上下文。` });
          showToast('完整档案已展开');
          return;
        }
        if (label === '调配') {
          openFormDialog({ title: `调配 · ${employee.name}`, description: '调整责任或容量前，先明确新的交接边界；保存后由 CEO 助理带回组织运行状态。', submitLabel: '保存调配', fields: [{ name: 'responsibility', label: '新的责任重点', value: employee.contract || '', type: 'textarea', required: true }, { name: 'handoff', label: '交接给谁', placeholder: '例如：交给业务工程 AI / 保留 CEO 验收', required: true }, { name: 'capacity', label: '容量安排', placeholder: '例如：本周期 70%' }], onSubmit: values => { const current = readState(); writeState({ employeeAssignments: { ...(current.employeeAssignments || {}), [key]: { ...values, at: new Date().toISOString() } }, lastAssistantMessage: `${employee.name}的责任与容量已调整，CEO 助理会观察下一次交接是否顺畅。` }); showToast('调配方案已保存'); } });
          return;
        }
        const current = readState();
        writeState({ employeeStatuses: { ...(current.employeeStatuses || {}), [key]: 'paused' }, lastAssistantMessage: `${employee.name}已暂停，当前证据会保留，新的执行不会继续派发。` });
        if (window.curisEmployees?.[key]) { window.curisEmployees[key].status = '已暂停'; window.curisEmployees[key].statusClass = 'pill-blocked'; }
        document.querySelector(`.org-node[data-employee="${key}"] .pill`)?.replaceChildren(document.createTextNode('已暂停'));
        showToast(`${employee.name}已暂停，历史证据已保留`);
      };
    });
  }

  function initOperatingActions() {
    if (!window.location.pathname.endsWith('operating.html')) return;
    const routes = {
      '生成决策包': 'decision-room.html',
      '生成蓝图': 'workspace-studio.html'
    };
    const labels = new Set(['补充证据', '延后', '查看', '查看记录', '查看合同', '查看工单', '升级', '追踪', '调配', '设计实验', '暂缓', '查看提案', '归档', '评估数据源', '查看注意力日历', '查看授权清单', '调配容量']);
    document.querySelectorAll('button').forEach(button => {
      const label = button.textContent.trim();
      if (button.dataset.curisHandled === 'true' || button.onclick || (!routes[label] && !labels.has(label))) return;
      button.dataset.curisHandled = 'true';
      button.onclick = () => {
        if (routes[label]) {
          writeState({ lastAssistantMessage: label === '生成蓝图' ? '业务分析 AI 已准备生成新的业务空间蓝图。' : '决策包已准备，我会把事实、未知与影响交给 CEO 判断。', lastAssistantHandoff: { label: label === '生成蓝图' ? '工作空间搭建' : '决策室', route: routes[label], message: label } });
          window.location.href = routes[label];
          return;
        }
        const matter = button.closest('.matter-card, .constraint-card, .risk-list, .card');
        const title = matter?.querySelector('.matter-title, .constraint-label, h2')?.textContent.trim() || label;
        if (label === '查看') {
          openEvidenceReview({ title, source: matter?.querySelector('.matter-meta-value')?.textContent.trim() || '经营事项记录', summary: matter?.querySelector('.matter-summary, .recovery-text, .constraint-desc')?.textContent.trim() || '当前事项的原始记录、影响和责任已保留在经营上下文。', status: '已记录', confidence: '待复核', evidenceType: '经营事项记录' });
          return;
        }
        if (label === '补充证据' || label === '查看记录' || label === '查看合同' || label === '查看工单') {
          openEvidenceReview({ title, source: matter?.querySelector('.matter-meta-value')?.textContent.trim() || '经营办公室记录', summary: matter?.querySelector('.matter-summary, .recovery-text, .constraint-desc')?.textContent.trim() || '当前事项的原始记录与责任已保留在经营上下文。', status: label === '补充证据' ? '待补证据' : '已记录', confidence: label === '补充证据' ? '不足' : '待复核' });
          return;
        }
        if (label === '延后') {
          openFormDialog({ title: `延后处理 · ${title}`, description: '延后不是忽略。请留下下一检查点和原因，CEO 助理会在到期时重新汇报。', submitLabel: '保存检查点', fields: [{ name: 'checkpoint', label: '下一检查点', placeholder: '例如：明天 12:00 / 2026-08-08 18:00', required: true }, { name: 'reason', label: '延后原因', type: 'textarea', placeholder: '例如：等待平台授权续签确认。', required: true }], onSubmit: values => { const current = readState(); const items = Array.isArray(current.operatingDeferredItems) ? current.operatingDeferredItems : []; const item = { title, ...values, at: new Date().toISOString(), status: '待到期复查' }; writeState({ operatingDeferredItems: [...items.filter(entry => entry.title !== title), item].slice(-20), lastAssistantMessage: `“${title}”已延后到${values.checkpoint}，我会在检查点重新提醒。` }); button.textContent = '已延后'; button.disabled = true; const archiveList = document.querySelector('.curis-operating-archive-list'); if (archiveList) { const archiveButton = document.createElement('button'); archiveButton.type = 'button'; archiveButton.className = 'curis-operating-archive-item'; archiveButton.dataset.archiveRoute = 'operating.html'; archiveButton.innerHTML = '<span><strong></strong><span></span></span><em>经营办公室 →</em>'; archiveButton.querySelector('strong').textContent = `已延后 · ${title}`; archiveButton.querySelector('span span').textContent = `下一检查点：${values.checkpoint} · ${values.reason}`; archiveList.prepend(archiveButton); archiveButton.addEventListener('click', () => { window.location.href = 'operating.html'; }); } showToast('已设置下一检查点'); } });
          return;
        }
        if (label === '查看注意力日历') { window.location.href = 'calendar.html'; return; }
        if (label === '查看授权清单') { window.location.href = 'calendar.html'; return; }
        if (label === '调配' || label === '调配容量') { window.location.href = 'ai-organization.html'; return; }
        if (label === '升级') { window.location.href = 'decision-room.html'; return; }
        if (label === '设计实验') {
          openFormDialog({ title: `设计实验 · ${title}`, description: '把机会变成可验证的小步实验，先定义窗口、指标和停止条件，再交给对应 AI 执行。', submitLabel: '保存实验', fields: [{ name: 'window', label: '验证窗口', placeholder: '例如：2 周', required: true }, { name: 'metric', label: '成功指标', placeholder: '例如：通过率 ≥ 80%', required: true }, { name: 'stop', label: '停止条件', placeholder: '例如：成本超过 ¥500 或结果异常' }], onSubmit: values => { writeState({ operatingExperiment: { title, ...values, at: new Date().toISOString() }, lastAssistantMessage: `“${title}”实验已保存，我会在检查点带回结果。` }); showToast('实验已保存'); } });
          return;
        }
        if (label === '查看提案') {
          openFormDialog({ title: `提案 · ${title}`, description: '这是 AI 根据现有证据整理的建议，CEO 可以保存判断，也可以先要求补证据。', submitLabel: '记录判断', fields: [{ name: 'decision', label: 'CEO 判断', type: 'select', options: ['进入验证', '补充证据', '暂不处理'] }, { name: 'note', label: '判断说明', type: 'textarea' }], onSubmit: values => { writeState({ operatingProposal: { title, ...values, at: new Date().toISOString() }, lastAssistantMessage: `关于“${title}”的判断已记录。` }); showToast('判断已记录'); } });
          return;
        }
        if (label === '归档') {
          const current = readState();
          const archived = Array.isArray(current.operatingArchivedItems) ? current.operatingArchivedItems : [];
          const item = { title, note: matter?.querySelector('.matter-summary, .recovery-text, .constraint-desc')?.textContent.trim() || '经营事项已由 CEO 收束。', route: 'operating.html', source: '经营办公室', at: new Date().toISOString() };
          writeState({ operatingArchivedItems: [...archived.filter(entry => entry.title !== title), item].slice(-20), lastAssistantMessage: `“${title}”已归档，历史证据仍可在成果库中追溯。` });
          button.textContent = '已归档'; button.disabled = true;
          const archiveList = document.querySelector('.curis-operating-archive-list');
          if (archiveList) {
            const archiveButton = document.createElement('button');
            archiveButton.type = 'button'; archiveButton.className = 'curis-operating-archive-item'; archiveButton.dataset.archiveRoute = item.route;
            archiveButton.innerHTML = '<span><strong></strong><span></span></span><em>经营办公室 →</em>';
            archiveButton.querySelector('strong').textContent = item.title;
            archiveButton.querySelector('span span').textContent = item.note;
            archiveList.prepend(archiveButton);
            archiveButton.addEventListener('click', () => { window.location.href = item.route; });
          }
          showToast('事项已归档'); return;
        }
        writeState({ lastAssistantMessage: '经营事项“' + label + '”已交给对应 AI 员工处理，我会在证据或下一步判断准备好后回来汇报。' });
        showToast(label + '已记录，CEO 助理会继续跟进');
      };
    });
  }

  function initOperatingTruth() {
    if (!window.location.pathname.endsWith('operating.html')) return;
    const state = readState();
    const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
    const hasEvidence = Boolean(state.companyCreatedAt && (runs.length || state.businessDecision || state.meetingDecision || state.softwareAcceptance || state.latestXhsFeedback || state.latestExternalFeedback || state.departmentResult));
    const pending = runs.filter(item => ['waiting_ceo', 'acknowledged'].includes(item.status)).length;
    const subtitle = document.querySelector('.page-subtitle');
    if (!hasEvidence) {
      if (subtitle) subtitle.textContent = '公司启动后，经营办公室会把运行、异常、待决策和已归档事项放在这里。当前还没有真实经营记录。';
      document.querySelectorAll('.matter-card').forEach(card => {
        card.querySelector('.matter-type')?.replaceChildren(document.createTextNode('待开始'));
        card.querySelector('.matter-title')?.replaceChildren(document.createTextNode('等待公司启动后的第一项经营记录'));
        card.querySelector('.matter-summary')?.replaceChildren(document.createTextNode('先完成公司创建和第一条业务配置；运行、风险与 CEO 决策会在真实发生后出现在这里。'));
        card.querySelector('.matter-actions')?.replaceChildren();
      });
      const drawerBubble = document.querySelector('#drawer .chat-bubble');
      if (drawerBubble) drawerBubble.textContent = '公司还没有启动。我会在你完成第一条业务配置后，开始整理运行、风险和待决策事项。';
      document.querySelectorAll('.pulse-card').forEach(card => {
        card.classList.remove('pulse-ontrack', 'pulse-attention', 'pulse-risk');
        card.classList.add('pulse-unknown');
        card.querySelector('.pulse-status-pill')?.replaceChildren(document.createTextNode('等待启动'));
        card.querySelector('.pulse-summary')?.replaceChildren(document.createTextNode('还没有真实经营记录；首轮运行或结果回传后，这个维度才会有状态。'));
        card.querySelector('.pulse-evidence')?.replaceChildren();
      });
      document.querySelectorAll('.risk-list .filterable, .queue-table .filterable, [aria-labelledby="opportunity-heading"] .matter-card').forEach(card => card.remove());
      document.querySelectorAll('.risk-column-count, .filter-tab').forEach(node => { if (node.classList.contains('risk-column-count')) node.textContent = '0'; });
      document.querySelectorAll('.card-subtitle').forEach(node => { if (/共 6 项|等待 CEO 决定|新信号/.test(node.textContent)) node.textContent = '当前没有真实记录'; });
      document.querySelectorAll('.risk-list, .queue-table tbody, [aria-labelledby="opportunity-heading"] .grid-2').forEach(list => {
        if (!list.children.length) list.innerHTML = '<div class="curis-org-empty"><strong>还没有真实经营事项</strong><span>完成公司创建、配置业务并产生首轮运行后，相关记录会在这里出现。</span></div>';
      });
    }
    if (hasEvidence) {
      const verifiedValue = [...(state.outcomeAttributions || [])].filter(item => item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
      const feedback = state.latestXhsFeedback || state.latestExternalFeedback;
      const pulseValues = [
        [verifiedValue ? '正常' : '等待结果', verifiedValue ? `本周期已验证价值 ¥${verifiedValue.toLocaleString()}` : '结果回传后才形成价值判断', verifiedValue ? 'pulse-ontrack' : 'pulse-unknown'],
        [runs.length ? (pending ? '需关注' : '正常') : '等待运行', runs.length ? `${runs.length} 次真实运行记录 · ${pending ? '有交接未收束' : '当前没有运行异常'}` : '等待首轮自动运行', runs.length && pending ? 'pulse-attention' : runs.length ? 'pulse-ontrack' : 'pulse-unknown'],
        [state.aiTeam?.length ? '已配置' : '待配置', state.aiTeam?.length ? `${state.aiTeam.length} 位 AI 员工已获批` : '还没有可承担责任的 AI 员工', state.aiTeam?.length ? 'pulse-ontrack' : 'pulse-unknown'],
        [state.lastConnector?.status === 'pending' || runs.some(item => item.status === 'failed') ? '有风险' : '正常', state.lastConnector?.status === 'pending' ? '外部连接待 CEO 确认；手动窗口已保留' : '当前没有真实异常记录', state.lastConnector?.status === 'pending' ? 'pulse-risk' : 'pulse-ontrack'],
        [feedback || state.meetingDecision ? '有依据' : '待验证', feedback ? '外部结果已回传，增长 AI 可以开始复盘' : state.meetingDecision ? '会议共识已写入经营节奏' : '等待第一条真实业务信号', feedback || state.meetingDecision ? 'pulse-ontrack' : 'pulse-unknown'],
        [state.companyCreatedAt ? '在运行' : '待启动', state.companyCreatedAt ? '公司已启动；自动节奏和结果回报会持续写入记录' : '公司成立后才会开始承接下一天', state.companyCreatedAt ? 'pulse-ontrack' : 'pulse-unknown']
      ];
      document.querySelectorAll('.pulse-card').forEach((card, index) => {
        const data = pulseValues[index] || pulseValues[0];
        card.classList.remove('pulse-ontrack', 'pulse-attention', 'pulse-risk', 'pulse-unknown');
        card.classList.add(data[2]);
        card.querySelector('.pulse-status-pill')?.replaceChildren(document.createTextNode(data[0]));
        card.querySelector('.pulse-summary')?.replaceChildren(document.createTextNode(data[1]));
        card.querySelector('.pulse-evidence')?.replaceChildren();
      });
      document.querySelectorAll('[aria-labelledby="risk-heading"] .filterable, [aria-labelledby="exception-heading"] .filterable, .queue-table tbody .filterable, [aria-labelledby="opportunity-heading"] .matter-card').forEach(node => node.remove());
      const pendingItems = runs.filter(item => ['queued', 'running', 'waiting_ceo', 'acknowledged', 'failed'].includes(item.status));
      const connectorItem = state.lastConnector?.status === 'pending' ? { title: `连接申请待确认 · ${state.lastConnector.source || '外部数据来源'}`, summary: state.lastConnector.scope || '授权完成前不会读取平台数据；手动录入窗口已保留。', business: '公司共享', status: '待 CEO' } : null;
      const riskList = document.querySelector('.risk-list');
      [...pendingItems.map(item => ({ title: item.title || '自动运行', summary: item.output || item.task || '运行结果等待处理', business: item.business || '公司共享', status: item.status === 'failed' ? '异常' : '待处理' })), connectorItem].filter(Boolean).slice(0, 4).forEach(item => {
        const card = document.createElement('article');
        card.className = 'matter-card exception';
        card.innerHTML = `<div class="matter-type exception">${escapeHtml(item.status)}</div><h3 class="matter-title"></h3><p class="matter-summary"></p><div class="matter-meta"><div class="matter-meta-cell"><span class="matter-meta-label">业务</span><span>${escapeHtml(item.business)}</span></div></div>`;
        card.querySelector('.matter-title').textContent = item.title;
        card.querySelector('.matter-summary').textContent = item.summary;
        riskList?.appendChild(card);
      });
      document.querySelectorAll('[aria-labelledby="risk-heading"] .risk-list').forEach(list => {
        if (!list.children.length) list.innerHTML = '<div class="curis-org-empty"><strong>当前没有真实异常</strong><span>自动运行、授权或外部结果出现需要处理的变化后，这里会显示升级事项。</span></div>';
      });
      const riskCounts = [pendingItems.filter(item => item.status !== 'failed').length + (connectorItem ? 1 : 0), pendingItems.filter(item => item.status === 'failed').length];
      document.querySelectorAll('.risk-column-count').forEach((node, index) => { node.textContent = String(riskCounts[index] || 0); });
      const exceptionGrid = document.querySelector('[aria-labelledby="exception-heading"] .grid-3');
      if (exceptionGrid && pendingItems.length) {
        pendingItems.slice(0, 3).forEach(item => {
          const card = document.createElement('article');
          card.className = 'matter-card exception';
          card.innerHTML = `<div class="matter-type exception">${escapeHtml(item.status === 'failed' ? '活跃异常' : '待处理')}</div><h3 class="matter-title"></h3><p class="matter-summary"></p><div class="matter-meta"><div class="matter-meta-cell"><div class="matter-meta-label">负责人</div><div class="matter-meta-value">${escapeHtml(item.owner || item.capability?.agent || 'AI 员工')}</div></div><div class="matter-meta-cell"><div class="matter-meta-label">业务</div><div class="matter-meta-value">${escapeHtml(item.business || '公司共享')}</div></div></div>`;
          card.querySelector('.matter-title').textContent = item.title || '自动运行';
          card.querySelector('.matter-summary').textContent = item.output || item.task || '运行结果等待处理。';
          exceptionGrid.appendChild(card);
        });
      }
      if (exceptionGrid && !exceptionGrid.children.length) exceptionGrid.innerHTML = '<div class="curis-org-empty"><strong>当前没有已升级异常</strong><span>只有失败、阻塞或需要 CEO 介入的运行才会进入异常队列。</span></div>';
      const queueBody = document.querySelector('.queue-table tbody');
      const queueItems = [...pendingItems, ...(state.meetingDecision ? [{ title: state.meetingDecision.title || '会议共识', output: state.meetingDecision.summary || '会议决议已形成，等待承诺回报。', business: '会议工作台', status: '待跟进' }] : [])];
      queueItems.slice(0, 6).forEach(item => {
        const row = document.createElement('tr');
        row.className = 'queue-row';
        row.innerHTML = `<td><div class="queue-title"></div><div class="queue-sub"></div></td><td>${escapeHtml(item.business || '公司共享')}</td><td><span class="status-badge status-warning">${escapeHtml(item.status || '待处理')}</span></td><td><button type="button" class="btn btn-secondary">查看</button></td>`;
        row.querySelector('.queue-title').textContent = item.title || '自动运行';
        row.querySelector('.queue-sub').textContent = item.output || item.task || '结果等待处理';
        queueBody?.appendChild(row);
      });
      if (queueBody && !queueItems.length) queueBody.innerHTML = '<tr><td colspan="5"><div class="curis-org-empty"><strong>当前没有待 CEO 决定的事项</strong><span>产生真实运行、会议共识或业务结果后，决策队列会在这里出现。</span></div></td></tr>';
      const opportunities = document.querySelector('[aria-labelledby="opportunity-heading"] .grid-2');
      if (opportunities && feedback) {
        const card = document.createElement('article');
        card.className = 'matter-card opportunity';
        card.innerHTML = `<div class="matter-type opportunity">新信号</div><h3 class="matter-title"></h3><p class="matter-summary"></p><div class="matter-meta"><div class="matter-meta-cell"><span class="matter-meta-label">下一步</span><span>进入业务复盘并生成下一轮建议</span></div></div>`;
        card.querySelector('.matter-title').textContent = `${feedback.platform || '业务'}外部结果已回传`;
        card.querySelector('.matter-summary').textContent = '真实结果已经回到公司，CEO 可以决定继续验证、扩大投入或暂停复盘。';
        opportunities.appendChild(card);
      }
    }
    const constraints = [...document.querySelectorAll('.constraint-card')];
    const constraintData = [
      ['CEO 待处理事项', pending ? `${pending} 项` : '—', pending ? '来自真实运行交接' : '等待首轮运行'],
      ['外部平台连接', state.lastConnector?.status === 'pending' ? '待授权' : (state.latestXhsFeedback || state.latestExternalFeedback ? '已有回传' : '—'), state.lastConnector?.status === 'pending' ? '授权完成前保留手动窗口' : '等待 API 或 CEO 手动回传'],
      ['AI 团队运行记录', runs.length ? `${runs.length} 次` : '—', runs.length ? '成本、负责人和下一阶段已写回' : '等待真实运行记录']
    ];
    constraints.forEach((card, index) => {
      const data = constraintData[index];
      if (!data) return;
      card.querySelector('.constraint-label')?.replaceChildren(document.createTextNode(data[0]));
      card.querySelector('.constraint-value')?.replaceChildren(document.createTextNode(data[1]));
      card.querySelector('.constraint-desc')?.replaceChildren(document.createTextNode(data[2]));
    });
  }

  function initDeskOpening() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-desk-opening')) return;
    const brief = document.querySelector('.brief-card .brief-header');
    if (!brief) return;
    const state = readState();
    const closed = Boolean(state.operatingDayClosedAt);
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    const departmentResult = state.departmentResult;
    const hasDepartment = Boolean(department?.name && commitment?.name);
    const attention = assistantAttention(state);
    const scheduledRun = state.lastScheduledRun;
    const onboarding = !state.companyCreatedAt;
    const scheduledNeedsAttention = ['queued', 'waiting_ceo', 'acknowledged', 'failed'].includes(scheduledRun?.status);
    const nextRoute = onboarding
      ? 'founding-flow.html'
      : scheduledNeedsAttention
      ? (scheduledRun.status === 'queued' ? 'ai-organization.html' : (scheduledRun.route || 'calendar.html'))
      : state.lastAssistantHandoff?.route || (state.lastDecision ? 'operating.html' : 'decision-room.html');
    const opening = document.createElement('div');
    opening.className = 'curis-desk-opening';
    opening.innerHTML = `<div class="curis-desk-opening-identity"><span class="curis-desk-opening-avatar">C</span><div class="curis-desk-opening-copy"><strong>Curis · CEO 首席助理</strong><span>${onboarding ? '公司还没有启动 · 先从第一间办公室开始' : closed ? '经营日已归档 · 明日承接已准备好' : hasDepartment ? `${department.name} · ${departmentResult ? '结果已回报，等待你的判断' : `正在守住“${commitment.name}”`}` : attention || '今天还没有需要你处理的变化'}</span></div></div><button class="curis-desk-opening-action" type="button" data-curis-handled="true">${onboarding ? '创建公司' : closed ? '查看明日承接' : scheduledRun?.status === 'queued' ? '查看排队状态' : scheduledNeedsAttention ? '处理这次自动运行' : hasDepartment ? '查看部门回报' : attention ? '查看助理提醒' : '查看公司状态'}</button>`;
    brief.insertBefore(opening, brief.firstChild);
    if (!closed && hasDepartment) {
      const greeting = brief.querySelector('.brief-greeting');
      const lead = brief.querySelector('.brief-lead');
      if (greeting) greeting.textContent = departmentResult ? `早上好，${department.name} 带回一条${departmentResult.status}结果` : `早上好，我正在替你守住${commitment.name}`;
      if (lead) lead.textContent = departmentResult ? `${departmentResult.note || 'CEO 已记录一条真实回报。'} 我已把证据、责任和下一步放在部门办公室，等你决定继续、调整或暂停。` : `${department.name} 已经开始承接“${commitment.name}”。暂时还没有真实结果，我会持续观察，只有需要你判断时才来打扰。`;
    } else if (onboarding) {
      const greeting = brief.querySelector('.brief-greeting');
      const lead = brief.querySelector('.brief-lead');
      if (greeting) greeting.textContent = '欢迎来到 Curis';
      if (lead) lead.textContent = '这里还没有公司。先说出你想经营什么，CEO 助理会陪你创建公司、定义第一条业务并配置第一支 AI 团队。';
    } else if (!closed && attention) {
      const greeting = brief.querySelector('.brief-greeting');
      const lead = brief.querySelector('.brief-lead');
      if (greeting) greeting.textContent = `早上好，${attention}`;
      if (lead) lead.textContent = state.lastAssistantMessage || '我已把相关证据和下一步整理好，等你确认后再让团队继续向前。';
    }
    opening.querySelector('button').addEventListener('click', () => {
      if (closed) {
        document.querySelector('#closeout-heading')?.closest('.card')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }
      window.location.href = hasDepartment ? 'workspace-runtime-department.html' : nextRoute;
    });
  }

  function initDeskOperatingDayRibbon() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-day-ribbon')) return;
    const header = document.querySelector('.page-header');
    if (!header) return;
    const state = readState();
    if (!state.companyCreatedAt) return;
    const decisionDone = Boolean(state.lastDecision || state.meetingDecision);
    const resultDone = Boolean(state.departmentResult || state.latestExternalFeedback || state.softwareAcceptance);
    const closed = Boolean(state.operatingDayClosedAt);
    const currentIndex = closed ? 4 : resultDone ? 3 : decisionDone ? 2 : 1;
    const steps = [
      ['08:30', '经营简报'],
      ['11:00', 'CEO 决策'],
      ['14:00', '团队执行'],
      ['17:00', '结果回报'],
      ['18:00', '明日承接']
    ];
    const ribbon = document.createElement('section');
    ribbon.className = 'curis-day-ribbon';
    ribbon.setAttribute('aria-label', 'CEO 经营日');
    const targets = ['.brief-card', '.matter-card.decision', '.timeline', '.handoff-list', '#closeout-heading'];
    ribbon.innerHTML = `<div class="curis-day-ribbon-head"><p class="curis-day-ribbon-kicker">CEO OPERATING DAY</p><h2 class="curis-day-ribbon-title">今天的公司如何向前</h2><p class="curis-day-ribbon-sub">助理只在需要 CEO 介入时出现</p></div><div class="curis-day-ribbon-track">${steps.map((step, index) => `<button class="curis-day-ribbon-step ${index < currentIndex ? 'is-done' : index === currentIndex ? 'is-current' : ''}" type="button" data-day-target="${targets[index]}" aria-label="${step[0]} ${step[1]}"><span><span class="curis-day-ribbon-time">${step[0]}</span>${step[1]}</span></button>${index < steps.length - 1 ? '<span class="curis-day-ribbon-connector" aria-hidden="true"></span>' : ''}`).join('')}</div>`;
    header.parentNode.insertBefore(ribbon, header.nextSibling);
    ribbon.querySelectorAll('[data-day-target]').forEach(button => button.addEventListener('click', () => {
      const target = document.querySelector(button.dataset.dayTarget);
      if (!target) return;
      target.scrollIntoView({ behavior: 'smooth', block: 'center' });
      target.classList.add('curis-focus');
      window.setTimeout(() => target.classList.remove('curis-focus'), 1200);
    }));
  }

  function initDeskPulse() {
    if (!window.location.pathname.endsWith('ceo-desk.html')) return;
    const items = [...document.querySelectorAll('.pulse-grid .pulse-item')];
    if (items.length < 6) return;
    const state = readState();
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    const result = state.departmentResult;
    if (!department?.name || !commitment?.name) return;
    const paused = commitment.status === 'paused';
    const values = [
      result?.status === '已验证价值' ? ['新增证据', 'pulse-ontrack'] : result?.status === '结果异常' ? ['有异常', 'pulse-attention'] : ['未知', 'pulse-unknown'],
      paused ? ['已暂停', 'pulse-attention'] : result ? ['有结果', 'pulse-ontrack'] : ['进行中', 'pulse-attention'],
      ['正常', 'pulse-ontrack'],
      result?.status === '结果异常' ? ['有风险', 'pulse-attention'] : paused ? ['待恢复', 'pulse-attention'] : ['可控', 'pulse-ontrack'],
      result ? ['待判断', 'pulse-attention'] : ['执行中', 'pulse-ontrack'],
      paused ? ['待恢复', 'pulse-attention'] : ['正常', 'pulse-ontrack']
    ];
    items.forEach((item, index) => {
      const [label, tone] = values[index];
      item.classList.remove('pulse-ontrack', 'pulse-attention', 'pulse-unknown', 'pulse-risk');
      item.classList.add(tone);
      item.querySelector('.pulse-status').textContent = label;
      item.setAttribute('aria-label', `${item.querySelector('.pulse-name')?.textContent.trim() || ''}：${label}`);
    });
    const pulseNote = document.querySelector('#pulse-heading + .card-subtitle');
    if (pulseNote) pulseNote.textContent = `${department.name} · ${commitment.name} 的实时运行状态已纳入公司脉搏`;
  }

  function initFirstOperatingDay() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-first-day')) return;
    const state = readState();
    if (!state.companyCreatedAt) return;
    const pageHeader = document.querySelector('.page-header');
    const topGrid = document.querySelector('.brief-card')?.closest('.layout-grid');
    if (!pageHeader || !topGrid) return;
    const firstDay = document.createElement('section');
    firstDay.className = 'curis-first-day';
    firstDay.setAttribute('aria-labelledby', 'curis-first-day-title');
    const closed = Boolean(state.operatingDayClosedAt);
    firstDay.innerHTML = `<div><p class="curis-first-day-kicker">${closed ? '公司运行中 · 第一天记录已归档' : '公司已启动 · 第一天经营'}</p><h2 id="curis-first-day-title" class="curis-first-day-title">${closed ? '从明日承接继续经营' : `欢迎进入${escapeHtml(state.companyName || '你的公司')}`}</h2><p class="curis-first-day-note">${closed ? '第一天的变化、未解决事项和明日承接已经归档。CEO 助理会在下一次打开时从这份记录继续汇报。' : '第一位员工已经到岗。你不需要记住所有细节，CEO 助理会从今天开始替你守住业务、团队和结果。'}</p></div><div class="curis-first-day-facts"><div class="curis-first-day-fact"><span>第一条业务</span><strong>${escapeHtml(state.firstBusiness || '尚未定义')}</strong></div><div class="curis-first-day-fact"><span>目标结果</span><strong>${escapeHtml(state.firstBusinessOutcome || '等待确认')}</strong></div><div class="curis-first-day-fact"><span>反馈路径</span><strong>${escapeHtml(state.externalFeedbackPath || '手动记录')}</strong></div><div class="curis-first-day-fact"><span>AI 团队</span><strong>${escapeHtml(`${(state.aiTeam || ['CEO 助理']).length} 位已获批`)}</strong></div></div><button class="curis-first-day-action" type="button" data-curis-handled="true">${closed ? '查看明日承接 →' : '进入第一项决策 →'}</button>`;
    pageHeader.parentNode.insertBefore(firstDay, topGrid);
    firstDay.querySelector('button').addEventListener('click', () => {
      const target = closed ? document.querySelector('#closeout-heading')?.closest('.card') : document.querySelector('.matter-card.decision');
      target?.scrollIntoView({ behavior: 'smooth', block: 'center' });
      target?.classList.add('curis-focus');
      window.setTimeout(() => target?.classList.remove('curis-focus'), 1400);
    });
  }

  function initDeskFeedbackDigest() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-feedback-digest')) return;
    const topGrid = document.querySelector('.brief-card')?.closest('.layout-grid');
    if (!topGrid) return;
    const digest = document.createElement('section');
    digest.className = 'card curis-feedback-digest';
    digest.setAttribute('aria-labelledby', 'curis-feedback-digest-title');
    const state = readState();
    const xhsRecord = state.latestXhsFeedback ? { ...state.latestXhsFeedback, platform: '小红书' } : null;
    const shortVideoRecord = state.latestExternalFeedback ? { ...state.latestExternalFeedback, platform: '抖音 / TikTok' } : null;
    const record = [xhsRecord, shortVideoRecord].filter(Boolean).sort((a, b) => String(b.at || b.time || '').localeCompare(String(a.at || a.time || '')))[0];
    const history = [
      ...(Array.isArray(state.xhsFeedbackHistory) ? state.xhsFeedbackHistory : (xhsRecord ? [xhsRecord] : [])),
      ...(Array.isArray(state.externalFeedbackHistory) ? state.externalFeedbackHistory : (shortVideoRecord ? [shortVideoRecord] : []))
    ];
    const isXhs = record?.platform === '小红书';
    const metrics = record
      ? isXhs
        ? `<div class="curis-feedback-digest-metrics"><span>阅读 <b>${escapeHtml(record.reads || 0)}</b></span><span>收藏 <b>${escapeHtml(record.saves || 0)}</b></span><span>新增粉丝 <b>${escapeHtml(record.follows || 0)}</b></span><span>线索价值 <b>¥${escapeHtml(Number(record.value || 0).toLocaleString())}</b></span></div>`
        : `<div class="curis-feedback-digest-metrics"><span>播放 <b>${escapeHtml(record.plays || 0)}</b></span><span>点赞 <b>${escapeHtml(record.likes || 0)}</b></span><span>新增粉丝 <b>${escapeHtml(record.follows || 0)}</b></span><span>成交 <b>${escapeHtml(record.orders || 0)}</b></span></div>`
      : '';
    digest.innerHTML = `<div class="card-header"><div><h2 id="curis-feedback-digest-title" class="card-title">外部结果回流</h2><p class="card-subtitle">业务有没有创造真实价值，最终要回到这里</p></div></div><div class="card-body"><div class="curis-feedback-digest-copy"><p class="curis-feedback-digest-kicker">${record ? `${escapeHtml(record.platform)} · 最近一条回传 · ${escapeHtml(record.time || '刚刚')} · ${history.length} 条记录` : '还没有外部结果'}</p><h3 class="curis-feedback-digest-title">${record ? `${escapeHtml(record.platform)}运营办公室带回了一条真实市场信号` : '等待第一条真实市场信号'}</h3><p class="curis-feedback-digest-note"></p>${metrics}</div><button class="curis-feedback-digest-action" type="button" data-curis-handled="true">${record ? `去${escapeHtml(record.platform)}运营办公室 →` : '去内容办公室 →'}</button></div>`;
    const nextCycle = record ? state.growthNextCyclePlans?.[isXhs ? '小红书运营' : '抖音 / TikTok 运营'] : null;
    digest.querySelector('.curis-feedback-digest-note').textContent = record
      ? `${record.note ? `${record.note} · ` : ''}来源：${record.source || '待补充'} · 时间窗口：${record.window || '待补充'} · 状态：${record.resultStatus || '数据待验证'} · 可信度：${record.credibility || '中'}${nextCycle ? ` · 下一轮：${nextCycle.status}` : ' · 下一步：进入业务复盘'}`
      : '平台尚未授权时，可以先在内容办公室手动补录；助理会把结果带回经营决策。';
    topGrid.parentNode.insertBefore(digest, topGrid.nextSibling);
    digest.querySelector('button').addEventListener('click', () => {
      window.location.href = isXhs ? 'workspace-runtime-xhs.html' : 'workspace-runtime-shortvideo.html';
    });
  }

  function initDeskSoftwareDigest() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-software-digest')) return;
    const state = readState();
    const firstBusiness = String(state.firstBusiness || '');
    const result = state.softwareAcceptance;
    if (!result && !/软件开发|Curis v0\.2|研发/.test(firstBusiness)) return;
    const topGrid = document.querySelector('.brief-card')?.closest('.layout-grid');
    if (!topGrid) return;
    const accepted = result?.choice === 'accept';
    const digest = document.createElement('section');
    digest.className = 'card curis-software-digest';
    digest.setAttribute('aria-labelledby', 'curis-software-digest-title');
    const runs = (state.calendarEvents || []).filter(item => item.route === 'workspace-runtime-software.html');
    const metrics = `<div class="curis-software-digest-metrics"><span>版本 <b>${escapeHtml(result?.version || '待登记')}</b></span><span>研发运行 <b>${runs.length ? `${runs.length} 次` : '—'}</b></span><span>提交 <b>${escapeHtml(result?.commit || '—')}</b></span></div>`;
    digest.innerHTML = `<div class="card-header"><div><h2 id="curis-software-digest-title" class="card-title">软件结果回流</h2><p class="card-subtitle">Curis 自己的产品，也必须回到 CEO 的真实使用里验收</p></div></div><div class="card-body"><div class="curis-software-digest-copy"><p class="curis-software-digest-kicker">${result ? '最近一次 CEO 验收' : '研发办公室等待 CEO 验收'}</p><h3 class="curis-software-digest-title">${accepted ? 'Curis v0.2 已通过真实使用' : result?.choice === 'rework' ? 'Curis v0.2 已退回修改' : result?.choice === 'demo' ? 'Curis v0.2 等待现场演示' : '研发办公室已提交 Curis v0.2'}</h3><p class="curis-software-digest-note"></p>${metrics}</div><button class="curis-software-digest-action" type="button" data-curis-handled="true">去研发办公室 →</button></div>`;
    digest.querySelector('.curis-software-digest-note').textContent = result?.feedback
      ? `CEO 反馈：${result.feedback}`
      : accepted
        ? '验收记录已经进入下一周期，研发办公室会从这次反馈继续。'
        : '真实使用是软件业务的外部结果；CEO 的选择会决定发布、返工或演示。';
    topGrid.parentNode.insertBefore(digest, topGrid.nextSibling);
    digest.querySelector('button').addEventListener('click', () => { window.location.href = 'workspace-runtime-software.html'; });
  }

  function initDeskDepartmentDigest() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-department-digest')) return;
    const state = readState();
    const department = state.departmentDraft;
    const commitment = state.departmentCommitment;
    if (!department?.name || !commitment?.name) return;
    const topGrid = document.querySelector('.brief-card')?.closest('.layout-grid');
    if (!topGrid) return;
    const result = state.departmentResult;
    const history = Array.isArray(state.departmentResultHistory) ? state.departmentResultHistory : (result ? [result] : []);
    const digest = document.createElement('section');
    digest.className = 'card curis-department-digest';
    digest.setAttribute('aria-labelledby', 'curis-department-digest-title');
    digest.innerHTML = `<div class="card-header"><div><h2 id="curis-department-digest-title" class="card-title">部门责任回报</h2><p class="card-subtitle">CEO 助理正在替你守住首项责任，结果回来后再请求下一次判断</p></div></div><div class="card-body"><div class="curis-department-digest-copy"><p class="curis-department-digest-kicker">${escapeHtml(department.name)} · ${escapeHtml(commitment.name)} · ${history.length} 条回报</p><h3 class="curis-department-digest-title"></h3><p class="curis-department-digest-note"></p><div class="curis-department-digest-metrics"><span>责任 <b>${escapeHtml(commitment.status === 'paused' ? '已暂停' : '运行中')}</b></span><span>结果 <b>${escapeHtml(result?.status || '待补充')}</b></span></div></div><button class="curis-department-digest-action" type="button" data-curis-handled="true">去部门办公室 →</button></div>`;
    digest.querySelector('.curis-department-digest-title').textContent = result
      ? `${department.name} 带回了一条${result.status}回报`
      : commitment.status === 'paused'
        ? `${department.name} 的首项责任已暂停`
        : `${department.name} 正在等待首项责任结果`;
    digest.querySelector('.curis-department-digest-note').textContent = result
      ? `${result.note || 'CEO 已记录结果。'} 助理会据此准备继续、调整或暂停。`
      : commitment.status === 'paused'
        ? '历史责任仍然保留；如果要重启，先在经营办公室确认资源和方向。'
        : `目标结果：${commitment.outcome || '等待真实回报'}。还没有结果时，我不会替你宣布成功。`;
    topGrid.parentNode.insertBefore(digest, topGrid.nextSibling);
    digest.querySelector('button').addEventListener('click', () => { window.location.href = 'workspace-runtime-department.html'; });
  }

  function initDeskFinanceDigest() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-finance-digest')) return;
    const state = readState();
    const brief = state.financeBrief;
    if (!brief) return;
    const topGrid = document.querySelector('.brief-card')?.closest('.layout-grid');
    if (!topGrid) return;
    const digest = document.createElement('section');
    digest.className = 'card curis-finance-digest';
    digest.setAttribute('aria-labelledby', 'curis-finance-digest-title');
    const planNote = state.financeCapacityPlan ? ` 扩容预算：${escapeHtml(state.financeCapacityPlan.businessTitle || '当前业务')}预计新增 ¥${Number(state.financeCapacityPlan.incrementalCost || 0).toLocaleString()} / 周期。` : '';
    digest.innerHTML = `<div class="card-header"><div><p class="eyebrow">CEO 财务简报 · ${escapeHtml(new Date(brief.at || Date.now()).toLocaleDateString('zh-CN'))}</p><h2 id="curis-finance-digest-title" class="card-title">本周期经营账已准备好</h2><p class="card-subtitle">收入、成本和非收入价值已经整理成下一次投入判断。</p></div><button type="button" class="btn btn-secondary" data-curis-handled="true">查看经营账 →</button></div><div class="card-body"><div class="curis-finance-digest-metrics"><span>可确认收入 <b>¥${Number(brief.revenue || 0).toLocaleString()}</b></span><span>总成本 <b>¥${Number(brief.cost || 0).toLocaleString()}</b></span><span>结果价值 <b>¥${Number(brief.value || 0).toLocaleString()}</b></span></div><p class="curis-finance-digest-note">这份简报不会替 CEO 决定扩大或暂停；它只把证据、口径和下一步判断准备好。${planNote}</p></div>`;
    topGrid.parentNode.insertBefore(digest, topGrid.nextSibling);
    digest.querySelector('button').addEventListener('click', () => { window.location.href = 'finance.html'; });
  }

  function initDeskMeetingDigest() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-meeting-digest')) return;
    const decision = readState().meetingDecision;
    if (!decision) return;
    const topGrid = document.querySelector('.brief-card')?.closest('.layout-grid');
    if (!topGrid) return;
    const commitments = Array.isArray(decision.commitments) ? decision.commitments : [];
    const digest = document.createElement('section');
    digest.className = 'card curis-meeting-digest';
    digest.setAttribute('aria-labelledby', 'curis-meeting-digest-title');
    digest.innerHTML = `<div class="card-header"><div><p class="eyebrow">会议决议 · ${escapeHtml(new Date(decision.at || Date.now()).toLocaleDateString('zh-CN'))}</p><h2 id="curis-meeting-digest-title" class="card-title">会议已经收束，承诺正在执行</h2></div><button type="button" class="btn btn-secondary" data-curis-handled="true">查看会议记录 →</button></div><div class="card-body"><p class="curis-meeting-digest-summary">${escapeHtml(decision.summary || '会议共识已形成，等待负责人回报。')}</p><div class="curis-meeting-digest-commitments">${commitments.map(item => `<span>• ${escapeHtml(item)}</span>`).join('')}</div></div>`;
    topGrid.parentNode.insertBefore(digest, topGrid.nextSibling);
    digest.querySelector('button').addEventListener('click', () => { window.location.href = 'meeting.html'; });
  }

  function initDeskCloseout() {
    if (!window.location.pathname.endsWith('ceo-desk.html')) return;
    const card = document.querySelector('#closeout-heading')?.closest('.card');
    if (!card || card.dataset.curisCloseoutBound === 'true') return;
    card.dataset.curisCloseoutBound = 'true';
    const state = readState();
    const note = card.querySelector('.muted');
    const primary = card.querySelector('.matter-actions .btn-primary');
    const secondary = card.querySelector('.matter-actions .btn-ghost');
    const status = document.createElement('span');
    status.className = 'curis-closeout-status';
    status.style.cssText = 'display:inline-flex;align-items:center;margin-top:12px;color:var(--text-secondary);font-size:12px;';
    card.querySelector('.card-header > div')?.appendChild(status);
    const render = closed => {
      status.textContent = closed ? '今日记录已生成' : '等待 CEO 确认今日收束';
      if (closed && note) note.textContent = '今日经营记录已归档。未解决事项与明日承接已交给 CEO 助理，明早会从这份记录继续。';
      if (!closed && note) note.textContent = '日终收束将在 18:00 自动生成。当前 Research AI 的反馈聚类已归档为学习记录；达人合作预算与 v0.2 发布两项结果将决定明日承接清单。';
      if (primary) {
        primary.textContent = closed ? '已生成今日记录' : '生成今日经营记录';
        primary.dataset.curisHandled = 'true';
        primary.onclick = event => {
          event.preventDefault();
          if (!readState().operatingDayClosedAt) {
            writeState({
              operatingDayClosedAt: new Date().toISOString(),
              lastAssistantMessage: '今日经营记录已经归档。明早我会从未解决事项和明日承接继续向你汇报。',
              lastAssistantHandoff: { label: 'CEO 工作台', route: 'ceo-desk.html', message: '今日经营记录已生成' }
            });
            card.classList.add('curis-focus');
            window.setTimeout(() => card.classList.remove('curis-focus'), 1200);
            render(true);
            showToast('今日经营记录已生成');
          } else {
            showToast('今日经营记录已归档');
          }
        };
      }
      if (secondary) {
        secondary.textContent = closed ? '查看明日承接' : '编辑明日承接';
        secondary.dataset.curisHandled = 'true';
        secondary.onclick = () => showToast(closed ? '明日承接已交给 CEO 助理守住' : '明日承接将在收束时一起归档');
      }
    };
    render(Boolean(state.operatingDayClosedAt));
  }

  function initDeskDynamicTruth() {
    if (!window.location.pathname.endsWith('ceo-desk.html') || document.querySelector('.curis-desk-dynamic-truth')) return;
    const timelineCard = document.querySelector('#timeline-heading')?.closest('.card');
    const routineCard = document.querySelector('#routine-heading')?.closest('.card');
    const handoffList = document.querySelector('.handoff-list');
    const closeoutCard = document.querySelector('#closeout-heading')?.closest('.card');
    if (!timelineCard && !routineCard && !handoffList && !closeoutCard) return;
    const marker = document.createElement('span');
    marker.className = 'curis-desk-dynamic-truth';
    marker.hidden = true;
    document.body.appendChild(marker);
    const businessKey = value => /小红书/.test(String(value || '')) ? '小红书运营' : /抖音|TikTok|短视频/.test(String(value || '')) ? '抖音 / TikTok 运营' : /软件|研发|Curis/.test(String(value || '')) ? '软件开发' : '公司共享';
    const routeFor = business => business === '软件开发' ? 'workspace-runtime-software.html' : business === '小红书运营' ? 'workspace-runtime-xhs.html' : business === '抖音 / TikTok 运营' ? 'workspace-runtime-shortvideo.html' : 'ceo-desk.html';
    const statusLabel = status => ({ queued: '排队中', running: '执行中', waiting_ceo: '待 CEO', acknowledged: '已打开', resolved: '已处理', failed: '异常', completed: '已完成' }[status] || '已记录');
    const avatarFor = name => String(name || 'AI').replace(/AI|CEO|助理|负责人|运营|研发|内容|数据|策略|复盘|发布|脚本|视频/g, '').trim().slice(0, 2) || 'AI';
    const activeBusinesses = state => {
      const active = new Set(['公司共享']);
      [state.firstBusiness, state.newBusinessDraft?.name, state.departmentCommitment?.name].forEach(value => active.add(businessKey(value)));
      if (state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html')) active.add('软件开发');
      if (state.latestXhsFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-xhs.html')) active.add('小红书运营');
      if (state.latestExternalFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-shortvideo.html')) active.add('抖音 / TikTok 运营');
      return active;
    };
    const readSchedules = () => {
      const defaults = [
        { name: '小红书 · 每日研究', business: '小红书运营', schedule: '每天 08:00', owner: '策略分析 AI', task: '输出 3 条候选选题', enabled: true },
        { name: '抖音 / TikTok · 数据回流', business: '抖音 / TikTok 运营', schedule: '每天 18:00', owner: '数据回收 AI', task: 'API 失败则提醒 CEO 手动补录', enabled: true },
        { name: '公司 · 每周经营简报', business: '公司共享', schedule: '每周一 09:00', owner: 'CEO 助理', task: '汇总财务、成果和风险', enabled: true },
        { name: '研发 · 回归检查', business: '软件开发', schedule: '每次提交后', owner: 'QA AI', task: '失败时暂停发布并升级', enabled: true }
      ];
      try { const saved = JSON.parse(localStorage.getItem('curis-schedules') || '[]'); return saved.length ? saved : defaults; } catch (_) { return defaults; }
    };
    const renderRoutine = state => {
      const timeline = routineCard?.querySelector('.timeline');
      if (!timeline) return;
      const active = activeBusinesses(state);
      const schedules = readSchedules().filter(item => active.has(businessKey(item.business)) && item.enabled !== false);
      timeline.innerHTML = schedules.length
        ? schedules.slice(0, 6).map(item => `<div class="timeline-item"><div class="timeline-time">${escapeHtml(item.schedule || '按需')}</div><div class="timeline-title">${escapeHtml(item.name || '自动任务')}</div><div class="timeline-desc">${escapeHtml(item.owner || 'AI 员工')} · ${escapeHtml(item.task || '等待任务说明')}${item.lastRunStatus ? ` · 最近${escapeHtml(statusLabel(item.lastRunStatus))}` : ''}</div></div>`).join('')
        : '<div class="curis-desk-empty-line"><strong>还没有启用的自动节奏</strong><span>完成公司创建并在公司日历启用第一项任务后，这里会显示 CEO 不必每天盯着的运行安排。</span></div>';
    };
    const renderTimeline = state => {
      const timeline = timelineCard?.querySelector('.timeline');
      if (!timeline) return;
      const records = [];
      if (state.companyCreatedAt) records.push({ at: state.companyCreatedAt, title: `${state.companyName || '公司'}正式成立`, note: `第一条业务：${state.firstBusiness || '待定义'} · AI 团队已配置`, status: '已归档' });
      (state.calendarEvents || []).slice(-8).forEach(run => records.push({ at: run.statusUpdatedAt || run.requestedAt, title: run.title || '自动运行', note: `${run.output || run.task || '结果等待回报'}${run.cost ? ` · 成本 ¥${Number(run.cost).toLocaleString()}` : ''}`, status: statusLabel(run.status) }));
      if (state.meetingDecision) records.push({ at: state.meetingDecision.at, title: '会议形成共识', note: state.meetingDecision.summary || '会议决议已进入执行跟踪。', status: '已记录' });
      if (state.softwareAcceptance) records.push({ at: state.softwareAcceptance.at, title: `软件开发 · ${state.softwareAcceptance.label || '验收记录'}`, note: state.softwareAcceptance.feedback || '研发办公室已提交 CEO 验收结果。', status: state.softwareAcceptance.choice === 'accept' ? '已验证' : '待处理' });
      if (state.latestXhsFeedback) records.push({ at: state.latestXhsFeedback.at, title: '小红书运营 · 外部结果回流', note: `阅读 ${Number(state.latestXhsFeedback.reads || 0).toLocaleString()} · 粉丝 ${Number(state.latestXhsFeedback.follows || 0).toLocaleString()} · ${state.latestXhsFeedback.resultStatus || '待复核'}`, status: state.latestXhsFeedback.resultStatus || '待复核' });
      if (state.latestExternalFeedback) records.push({ at: state.latestExternalFeedback.at, title: '抖音 / TikTok 运营 · 外部结果回流', note: `播放 ${Number(state.latestExternalFeedback.plays || 0).toLocaleString()} · 粉丝 ${Number(state.latestExternalFeedback.follows || 0).toLocaleString()} · ${state.latestExternalFeedback.resultStatus || '待复核'}`, status: state.latestExternalFeedback.resultStatus || '待复核' });
      records.sort((a, b) => String(a.at || '').localeCompare(String(b.at || '')));
      timeline.innerHTML = records.length
        ? records.slice(-8).map((record, index, list) => `<div class="timeline-item ${index === list.length - 1 ? 'active' : 'past'}"><div class="timeline-time">${escapeHtml(record.at ? new Date(record.at).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : '刚刚')}</div><div class="timeline-title">${escapeHtml(record.title)}</div><div class="timeline-desc">${escapeHtml(record.note)} · ${escapeHtml(record.status)}</div></div>`).join('')
        : '<div class="curis-desk-empty-line"><strong>等待第一条真实经营记录</strong><span>首轮自动运行、会议共识、验收或外部结果回来后，时间线会留下公司的成长记忆。</span></div>';
    };
    const renderHandoffs = state => {
      if (!handoffList) return;
      const members = Array.isArray(state.aiTeam) && state.aiTeam.length ? state.aiTeam : ['CEO 助理'];
      const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
      const latestFor = name => runs.filter(run => String(run.owner || run.capability?.agent || '').includes(String(name).replace(/ AI$/, ''))).sort((a, b) => String(b.statusUpdatedAt || '').localeCompare(String(a.statusUpdatedAt || '')))[0];
      handoffList.innerHTML = members.slice(0, 6).map(name => {
        const latest = latestFor(name);
        const result = name === 'CEO 助理' ? (state.lastAssistantMessage ? '最近一次汇报已更新' : '等待首轮运行') : latest ? `${latest.output || latest.task || '已接收工作'} · ${statusLabel(latest.status)}` : `等待${businessKey(state.firstBusiness) === '公司共享' ? '首项任务' : '第一项业务工作'}`;
        const stateText = latest ? statusLabel(latest.status) : name === 'CEO 助理' && state.companyCreatedAt ? '守候中' : '待启动';
        return `<div class="handoff-item"><div class="handoff-avatar">${escapeHtml(avatarFor(name))}</div><div class="handoff-info"><div class="handoff-name">${escapeHtml(name)}</div><div class="handoff-role">${escapeHtml(result)}</div></div><div class="handoff-status"><strong>${escapeHtml(stateText)}</strong>${latest?.statusUpdatedAt ? escapeHtml(new Date(latest.statusUpdatedAt).toLocaleString('zh-CN', { month: 'numeric', day: '2-digit', hour: '2-digit', minute: '2-digit' })) : '等待回报'}</div></div>`;
      }).join('');
    };
    const renderCloseout = state => {
      if (!closeoutCard) return;
      const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
      const decisions = [state.lastDecision, state.meetingDecision, state.businessDecision, state.softwareAcceptance].filter(Boolean).length;
      const unresolved = runs.filter(run => ['queued', 'waiting_ceo', 'acknowledged', 'failed'].includes(run.status)).length + (state.outcomeAttributions || []).filter(item => item.status !== '已验证价值').length;
      const changes = [state.companyCreatedAt, ...runs.map(run => run.statusUpdatedAt || run.requestedAt), state.latestXhsFeedback?.at, state.latestExternalFeedback?.at, state.softwareAcceptance?.at].filter(Boolean).length;
      const carry = Math.max(0, unresolved + (state.firstBusiness && !runs.length ? 1 : 0));
      const values = [changes, decisions, unresolved, carry];
      closeoutCard.querySelectorAll('.closeout-value').forEach((node, index) => { node.textContent = String(values[index] || 0); });
      const note = closeoutCard.querySelector('.muted');
      if (note && !state.operatingDayClosedAt) note.textContent = changes ? `已记录 ${changes} 条真实经营变化；${unresolved ? `还有 ${unresolved} 项需要 CEO 处理。` : '当前没有异常或待确认结果。'} 日终收束后，助理会把未解决事项带入明日承接。` : '还没有真实经营记录。首轮运行、会议共识或外部结果产生后，日终收束会自动汇总今天的变化。';
    };
    const renderContext = state => {
      const group = document.querySelector('.context-group');
      if (!group) return;
      const items = [...group.querySelectorAll('.context-item')];
      const separators = [...group.querySelectorAll('.context-sep')];
      const business = /小红书/.test(state.firstBusiness || '') ? '小红书运营办公室' : /抖音|TikTok|短视频/.test(state.firstBusiness || '') ? '抖音 / TikTok 运营办公室' : /软件|研发|Curis/.test(state.firstBusiness || '') ? '研发办公室' : '尚未配置业务空间';
      const companyNode = items[0]?.querySelector('strong') || items[0];
      if (companyNode) companyNode.textContent = state.companyName || 'Curis';
      if (items[1]) items[1].textContent = state.companyCreatedAt ? business : '尚未创建公司';
      items.slice(2).forEach(item => { item.hidden = true; item.style.display = 'none'; });
      separators.forEach((separator, index) => { separator.hidden = index > 0; separator.style.display = index > 0 ? 'none' : ''; });
    };
    const render = () => { const state = readState(); renderContext(state); renderRoutine(state); renderTimeline(state); renderHandoffs(state); renderCloseout(state); };
    const style = document.createElement('style');
    style.textContent = '.curis-desk-empty-line{padding:12px 0;color:var(--text-secondary,#9599a6);font-size:11px;line-height:1.5}.curis-desk-empty-line strong{display:block;margin-bottom:4px;color:var(--text-default,#d1d3db);font-size:12px}.handoff-item{min-height:54px}';
    document.head.appendChild(style);
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function openEvidenceReview({ title = '证据复核', source = '当前工作空间', summary = '暂无摘要', status = '待确认', confidence = '未知', outcomeId = '', evidenceType = '未登记', evidenceVersion = '—', capturedAt = '—' } = {}) {
    let dialog = document.getElementById('curis-evidence-review');
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.id = 'curis-evidence-review';
      dialog.className = 'curis-evidence-review';
      dialog.innerHTML = '<div class="curis-evidence-review-head"><div><p>证据复核</p><h2 data-evidence-title></h2></div><button type="button" data-evidence-close aria-label="关闭">×</button></div><div class="curis-evidence-review-body"><div class="curis-evidence-review-grid"><div><span>来源</span><strong data-evidence-source></strong></div><div><span>证据类型</span><strong data-evidence-type></strong></div><div><span>状态</span><strong data-evidence-status></strong></div><div><span>可信度</span><strong data-evidence-confidence></strong></div><div><span>版本</span><strong data-evidence-version></strong></div><div><span>采集时间</span><strong data-evidence-captured-at></strong></div></div><section><span>原始结果 / 摘要</span><p data-evidence-summary></p></section><section><span>Curis 解释</span><p>这条记录可以作为当前判断的输入，但不会静默替代原始来源。采用后会写入证据链；标记未知则保留缺口并交给 CEO 助理跟进。</p></section></div><div class="curis-evidence-review-actions"><button type="button" data-evidence-unknown>标记未知</button><button type="button" data-evidence-request>请求补证据</button><button type="button" class="primary" data-evidence-accept>采用为事实</button></div>';
      const style = document.createElement('style');
      style.id = 'curis-evidence-review-style';
      style.textContent = '#curis-evidence-review{width:min(560px,calc(100vw - 32px));padding:0;color:var(--text-default,#e2e3e7);background:var(--bg-base-secondary,#202226);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:14px;box-shadow:0 20px 70px rgba(0,0,0,.42)}#curis-evidence-review::backdrop{background:rgba(0,0,0,.5)}.curis-evidence-review-head{display:flex;justify-content:space-between;gap:16px;padding:18px;border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-evidence-review-head p{margin:0;color:var(--text-tertiary,#777c86);font-size:10px}.curis-evidence-review-head h2{margin:5px 0 0;font-size:15px}.curis-evidence-review-head button{border:0;background:transparent;color:var(--text-secondary,#a4a7af);font-size:20px;cursor:pointer}.curis-evidence-review-body{display:grid;gap:16px;padding:18px}.curis-evidence-review-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.curis-evidence-review-grid div{padding:9px;background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:7px}.curis-evidence-review-grid span,.curis-evidence-review-body section>span{display:block;color:var(--text-tertiary,#777c86);font-size:10px}.curis-evidence-review-grid strong{display:block;margin-top:5px;color:var(--text-default,#e2e3e7);font-size:11px;font-weight:500;line-height:1.4}.curis-evidence-review-body section{padding-top:12px;border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-evidence-review-body section p{margin:7px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.55}.curis-evidence-review-actions{display:flex;justify-content:flex-end;gap:8px;padding:0 18px 18px}.curis-evidence-review-actions button{padding:8px 10px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px;cursor:pointer}.curis-evidence-review-actions button.primary{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}@media(max-width:560px){.curis-evidence-review-grid{grid-template-columns:repeat(2,1fr)}}';
      document.head.appendChild(style);
      document.body.appendChild(dialog);
      dialog.querySelector('[data-evidence-close]').addEventListener('click', () => dialog.close());
      const save = status => { const context = dialog._evidenceContext || {}; const current = readState(); const evidenceStatus = status === '采用为事实' ? '已采用' : status === '未知' ? '未知' : '待补证据'; const outcome = context.outcomeId ? (current.outcomeAttributions || []).find(item => item.id === context.outcomeId) : null; const nextOutcome = outcome ? { ...outcome, evidenceStatus, evidenceReviewedAt: new Date().toISOString() } : null; writeState({ evidenceReview: { title: context.title || '证据复核', source: context.source || '当前工作空间', status, outcomeId: context.outcomeId || '', at: new Date().toISOString() }, ...(nextOutcome ? { outcomeAttributions: (current.outcomeAttributions || []).map(item => item.id === nextOutcome.id ? nextOutcome : item), lastOutcomeAttribution: nextOutcome } : {}), lastAssistantMessage: `证据“${context.title || '当前记录'}”已标记为${status}，后续判断会保留来源与可信度。` }); dialog.close(); showToast(`已${status}`); };
      dialog.querySelector('[data-evidence-unknown]').addEventListener('click', () => save('未知'));
      dialog.querySelector('[data-evidence-request]').addEventListener('click', () => save('请求补证据'));
      dialog.querySelector('[data-evidence-accept]').addEventListener('click', () => save('采用为事实'));
    }
    dialog._evidenceContext = { title, source, outcomeId, evidenceType, evidenceVersion, capturedAt };
    dialog.querySelector('[data-evidence-title]').textContent = title;
    dialog.querySelector('[data-evidence-source]').textContent = source;
    dialog.querySelector('[data-evidence-type]').textContent = evidenceType;
    dialog.querySelector('[data-evidence-status]').textContent = status;
    dialog.querySelector('[data-evidence-confidence]').textContent = confidence;
    dialog.querySelector('[data-evidence-version]').textContent = evidenceVersion;
    dialog.querySelector('[data-evidence-captured-at]').textContent = capturedAt === '—' ? capturedAt : new Date(capturedAt).toLocaleString('zh-CN');
    dialog.querySelector('[data-evidence-summary]').textContent = summary;
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
  }

  function initDeskActions() {
    if (!window.location.pathname.endsWith('ceo-desk.html')) return;
    const labels = new Set(['查看证据', '查看', '委派', '调查', '暂缓']);
    document.querySelectorAll('.matter-actions button').forEach(button => {
      const label = button.textContent.trim();
      if (button.dataset.curisHandled === 'true' || button.onclick || !labels.has(label)) return;
      button.dataset.curisHandled = 'true';
      button.onclick = () => {
        const matter = button.closest('.matter-card');
        const context = matter?.textContent || '';
        if (label === '查看' && /v0\.2|登录回调/.test(context)) {
          window.location.href = 'workspace-runtime-software.html';
          return;
        }
        const message = label === '查看证据'
          ? '我已把这项经营事项的证据链整理好，CEO 可以继续查看或直接做决定。'
          : label === '委派'
            ? '这项异常已交给对应专业 AI 员工，CEO 助理会守住回报时间。'
            : label === '调查'
              ? '这条业务机会已进入分析，结果准备好后我会再请 CEO 判断。'
              : '这项经营事项已暂缓，我会保留上下文并在检查点前提醒你。';
        writeState({ lastAssistantMessage: message });
        if (label === '查看证据') openEvidenceReview({ title: '经营事项证据', source: 'CEO 工作台 · 当前事项', summary: context.slice(0, 260), status: '待 CEO 采用', confidence: '需要复核' });
        else showToast(label + '已记录，CEO 助理会继续跟进');
      };
    });
    document.querySelectorAll('.evidence-link').forEach(link => {
      if (link.dataset.curisHandled === 'true') return;
      link.dataset.curisHandled = 'true';
      link.setAttribute('role', 'button');
      link.setAttribute('tabindex', '0');
      const open = () => {
        writeState({ lastAssistantMessage: '已打开证据“' + link.textContent.trim() + '”，我会把它保留在当前经营事项上下文里。' });
        openEvidenceReview({ title: link.textContent.trim() || '当前证据', source: link.closest('.matter-card')?.textContent?.slice(0, 180) || 'CEO 工作台', summary: '已从当前经营事项打开；原始来源、时间窗和解释会在这里保持同一条证据链。', status: '待 CEO 采用', confidence: '待复核' });
      };
      link.addEventListener('click', open);
      link.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); open(); }
      });
    });
  }

  function initDeskTruthBrief() {
    if (!window.location.pathname.endsWith('ceo-desk.html')) return;
    const state = readState();
    const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
    const hasEvidence = Boolean(state.companyCreatedAt && (runs.length || state.businessDecision || state.meetingDecision || state.softwareAcceptance || state.latestXhsFeedback || state.latestExternalFeedback || state.departmentResult));
    const meta = document.querySelector('.page-meta');
    if (meta) {
      meta.querySelector('.mono')?.replaceChildren(document.createTextNode(state.companyCreatedAt ? '公司启动日' : '尚未启动'));
      meta.querySelectorAll('strong').forEach((node, index) => node.replaceChildren(document.createTextNode(index === 0 ? (state.companyCreatedAt ? '等待首轮运行' : '等待公司创建') : 'CEO · 首席助理')));
      const sync = [...meta.querySelectorAll('span')].find(node => node.textContent.includes('上次同步'));
      if (sync) sync.textContent = '尚无经营记录';
    }
    const brief = document.querySelector('.brief-card');
    if (brief) {
      const statusLabel = status => ({ queued: '排队中', running: '执行中', waiting_ceo: '待 CEO', acknowledged: '已打开', resolved: '已处理', failed: '异常', completed: '已完成' }[status] || '已记录');
      const activeBusiness = /小红书/.test(state.firstBusiness || '') ? '小红书运营' : /抖音|TikTok|短视频/.test(state.firstBusiness || '') ? '抖音 / TikTok 运营' : /软件|研发|Curis/.test(state.firstBusiness || '') ? '软件开发' : '公司';
      const pendingRun = [...runs].reverse().find(item => ['waiting_ceo', 'acknowledged', 'failed'].includes(item.status));
      const activeRun = [...runs].reverse().find(item => ['queued', 'running'].includes(item.status));
      const completedRun = [...runs].reverse().find(item => ['completed', 'resolved'].includes(item.status));
      const feedback = state.latestXhsFeedback || state.latestExternalFeedback;
      const items = [
        pendingRun || (state.lastConnector?.status === 'pending' ? { title: `连接申请待确认 · ${state.lastConnector.source || '外部数据来源'}`, output: state.lastConnector.scope || '授权完成前不会读取平台数据；手动录入窗口已保留。', status: 'waiting_ceo', business: activeBusiness } : null),
        activeRun,
        feedback ? { title: `${feedback.platform || activeBusiness} · 外部结果已回传`, output: `${feedback.reads || feedback.plays || 0} ${feedback.reads ? '次阅读' : '次播放'} · 新增粉丝 ${feedback.follows || 0} · ${feedback.resultStatus || '待复核'}`, status: feedback.resultStatus === '已验证价值' ? 'completed' : 'running', business: activeBusiness } : completedRun
      ];
      const totalChanges = items.filter(Boolean).length;
      brief.querySelector('.brief-greeting')?.replaceChildren(document.createTextNode(!state.companyCreatedAt ? '欢迎来到 Curis，先从创建公司开始' : totalChanges ? `早上好，今天有 ${totalChanges} 项变化需要你留意` : '公司已经启动，今天还没有新的经营变化'));
      brief.querySelector('.brief-lead')?.replaceChildren(document.createTextNode(!state.companyCreatedAt ? '这里会成为你的 CEO 办公桌。完成公司创建后，我会替你整理业务、团队、风险和下一步。' : `CEO 助理会持续观察${activeBusiness}的运行，只在需要判断、授权或真实结果回传时回来汇报。`));
      brief.querySelectorAll('.brief-section').forEach((section, index) => {
        const item = items[index];
        const titles = ['必须决定', '建议关注', '已由团队处理'];
        const empty = ['还没有需要 CEO 决定的事项', '还没有运行中的事项', '还没有可以归档的公司经验'];
        const descriptions = ['AI 员工运行到需要 CEO 判断、授权或确认的节点后，会把输入、影响和选项放在这里。', '自动任务正在运行或排队；没有异常时，CEO 不需要每天盯着。', '会议决议、自动运行、软件验收和外部结果会在真实发生后成为公司的记忆。'];
        const titleNode = section.querySelector('.brief-section-title span:last-child');
        const marker = section.querySelector('.brief-item-marker');
        const itemTitle = section.querySelector('.brief-item-title');
        const itemDesc = section.querySelector('.brief-item-desc');
        if (titleNode) titleNode.textContent = item ? (index === 0 ? titles[0] : index === 1 ? titles[1] : titles[2]) : (state.companyCreatedAt ? titles[index] : ['等待 CEO 输入', '等待运行记录', '等待结果归档'][index]);
        if (marker) { marker.className = `brief-item-marker ${index === 0 ? 'decision' : index === 1 ? 'attention' : 'handled'}`; }
        if (item) {
          if (itemTitle) itemTitle.textContent = item.title || '自动运行';
          if (itemDesc) itemDesc.textContent = `${item.output || item.task || '结果已写回公司记录'} · ${item.business || activeBusiness} · ${statusLabel(item.status)}`;
        } else {
          if (itemTitle) itemTitle.textContent = state.companyCreatedAt ? empty[index] : ['还没有需要 CEO 决定的事项', '还没有异常或阻塞', '还没有可以归档的公司经验'][index];
          if (itemDesc) itemDesc.textContent = state.companyCreatedAt ? descriptions[index] : ['先完成公司创建并配置第一条业务，决策事项会在证据充分时出现。', 'AI 员工开始运行后，只有需要你介入的异常才会进入这里。', '会议决议、软件验收和外部结果会在真实发生后成为公司的记忆。'][index];
        }
        section.querySelector('.evidence-links')?.replaceChildren();
      });
    }
    const pulseRuns = runs.filter(item => ['queued', 'running', 'waiting_ceo', 'acknowledged', 'failed', 'completed', 'resolved'].includes(item.status));
    const pulsePending = runs.some(item => ['queued', 'waiting_ceo', 'acknowledged', 'failed'].includes(item.status)) || state.lastConnector?.status === 'pending';
    const pulseHasValue = Boolean(state.latestXhsFeedback || state.latestExternalFeedback || state.softwareAcceptance);
    const pulseValues = state.companyCreatedAt
      ? [[pulseHasValue ? '正常' : '等待结果', pulseHasValue ? 'pulse-ontrack' : 'pulse-unknown'], [pulseRuns.length ? (pulsePending ? '需关注' : '正常') : '等待运行', pulseRuns.length && pulsePending ? 'pulse-attention' : pulseRuns.length ? 'pulse-ontrack' : 'pulse-unknown'], [state.aiTeam?.length ? '已配置' : '待配置', state.aiTeam?.length ? 'pulse-ontrack' : 'pulse-unknown'], [pulsePending ? '有待处理' : '正常', pulsePending ? 'pulse-attention' : 'pulse-ontrack'], [state.firstBusiness ? (pulseHasValue ? '有依据' : '待验证') : '待定义', pulseHasValue ? 'pulse-ontrack' : 'pulse-unknown'], [state.companyCreatedAt ? (pulseRuns.length ? '在运行' : '已启动') : '待启动', state.companyCreatedAt ? 'pulse-ontrack' : 'pulse-unknown']]
      : Array(6).fill(['等待启动', 'pulse-unknown']);
    document.querySelectorAll('.pulse-item').forEach((item, index) => {
      const [label, className] = pulseValues[index] || ['等待启动', 'pulse-unknown'];
      item.classList.remove('pulse-ontrack', 'pulse-attention', 'pulse-unknown');
      item.classList.add(className);
      item.querySelector('.pulse-status')?.replaceChildren(document.createTextNode(label));
    });
    const matterRuns = [...runs].reverse();
    const matterRecords = [
      matterRuns.find(item => ['waiting_ceo', 'acknowledged', 'failed'].includes(item.status)) || (state.lastConnector?.status === 'pending' ? { title: `连接申请待确认 · ${state.lastConnector.source || '外部数据来源'}`, output: state.lastConnector.scope, owner: 'CEO 助理', business: '公司共享', status: 'waiting_ceo' } : null),
      matterRuns.find(item => ['queued', 'running'].includes(item.status)),
      state.latestXhsFeedback ? { title: '小红书运营 · 外部结果已回传', output: `阅读 ${Number(state.latestXhsFeedback.reads || 0).toLocaleString()} · 收藏 ${Number(state.latestXhsFeedback.saves || 0).toLocaleString()} · 新增粉丝 ${Number(state.latestXhsFeedback.follows || 0).toLocaleString()}`, owner: '增长 AI', business: '小红书运营', status: 'completed' } : state.latestExternalFeedback ? { title: '抖音 / TikTok 运营 · 外部结果已回传', output: `播放 ${Number(state.latestExternalFeedback.plays || 0).toLocaleString()} · 互动 ${Number(state.latestExternalFeedback.likes || 0).toLocaleString()}`, owner: '增长 AI', business: '抖音 / TikTok 运营', status: 'completed' } : state.softwareAcceptance ? { title: '软件开发 · CEO 验收已记录', output: state.softwareAcceptance.feedback || '研发办公室已收到 CEO 的真实使用反馈。', owner: 'CEO', business: '软件开发', status: 'completed' } : null
    ];
    document.querySelectorAll('.matter-card').forEach((card, index) => {
      const record = matterRecords[index];
      card.classList.remove('decision', 'exception', 'opportunity', 'unknown');
      if (!record) {
        card.classList.add('unknown');
        card.querySelector('.matter-type')?.replaceChildren(document.createTextNode(state.companyCreatedAt ? '待开始' : '待启动'));
        card.querySelector('.matter-title')?.replaceChildren(document.createTextNode(state.companyCreatedAt ? '等待公司启动后的第一项经营事项' : '先创建公司，再开始经营'));
        card.querySelectorAll('.matter-meta-row').forEach(row => row.remove());
        card.querySelector('.matter-actions')?.replaceChildren();
        return;
      }
      const live = ['queued', 'running', 'waiting_ceo', 'acknowledged', 'failed'].includes(record.status);
      card.classList.add(record.status === 'waiting_ceo' || record.status === 'acknowledged' ? 'decision' : live ? 'exception' : 'opportunity');
      card.querySelector('.matter-type')?.replaceChildren(document.createTextNode(record.status === 'waiting_ceo' || record.status === 'acknowledged' ? '待 CEO' : live ? '运行中' : '已记录'));
      card.querySelector('.matter-title')?.replaceChildren(document.createTextNode(record.title || '自动运行'));
      const meta = card.querySelector('.matter-meta');
      if (meta) meta.innerHTML = `<div class="matter-meta-row"><span class="matter-meta-label">负责人</span><span>${escapeHtml(record.owner || record.capability?.agent || 'AI 员工')}</span></div><div class="matter-meta-row"><span class="matter-meta-label">业务</span><span>${escapeHtml(record.business || '公司共享')}</span></div><div class="matter-meta-row"><span class="matter-meta-label">结果</span><span>${escapeHtml(record.output || record.task || '等待回报')}</span></div>`;
      const actions = card.querySelector('.matter-actions');
      if (actions) {
        actions.replaceChildren();
        const open = document.createElement('button');
        open.type = 'button'; open.className = 'btn btn-secondary'; open.textContent = record.status === 'completed' ? '查看结果' : '打开处理';
        open.addEventListener('click', () => { writeState({ lastAssistantHandoff: { label: record.business || '公司日历', route: record.route || 'calendar.html', message: record.title || '经营事项' } }); window.location.href = record.route || 'calendar.html'; });
        actions.appendChild(open);
      }
    });
    const drawer = document.querySelector('#drawer');
    drawer?.querySelector('.chat-bubble')?.replaceChildren(document.createTextNode(state.companyCreatedAt ? '公司已经启动，但还没有需要你处理的变化。我会在首轮运行或结果回传后主动回来汇报。' : '公司还没有启动。我会陪你从第一间办公室开始，把公司、业务和 AI 团队一步步搭起来。'));
    drawer?.querySelectorAll('.matter-card').forEach(card => { card.querySelector('.matter-title')?.replaceChildren(document.createTextNode('等待公司启动')); card.querySelector('.matter-summary')?.replaceChildren(document.createTextNode('真实经营记录产生后，这里会出现需要 CEO 处理的事项。')); });
  }

  function initWorkspaceStudio() {
    if (!window.location.pathname.endsWith('workspace-studio.html') || document.querySelector('.curis-studio-assembly')) return;
    const canvas = document.querySelector('.canvas-wrap');
    const canvasHeader = canvas?.querySelector('.canvas-header');
    const canvasArea = canvas?.querySelector('.canvas-area');
    const paletteItems = [...document.querySelectorAll('.palette-item')];
    if (!canvasHeader || !canvasArea || !paletteItems.length) return;
    const state = readState();
    if (!state.companyCreatedAt) {
      canvasHeader.querySelector('h1')?.replaceChildren(document.createTextNode('先创建公司，再装修业务空间'));
      canvasHeader.querySelector('.canvas-meta')?.replaceChildren(document.createTextNode('业务空间搭建需要先有公司意图和第一项业务承诺'));
      canvasArea.hidden = true;
      paletteItems.forEach(item => { item.setAttribute('aria-disabled', 'true'); item.style.opacity = '.45'; item.style.pointerEvents = 'none'; });
      const notice = document.createElement('section');
      notice.className = 'curis-studio-empty';
      notice.innerHTML = '<strong>还没有可装修的业务空间</strong><span>完成公司创建后，选择软件开发、小红书或抖音 / TikTok 模板，业务工程 AI 会把它装配成办公室。</span><button type="button" class="primary">开始创建公司 →</button>';
      canvasArea.parentNode.insertBefore(notice, canvasArea);
      notice.querySelector('button')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
      return;
    }
    const newBusiness = state.newBusinessDraft;
    const department = state.departmentDraft;
    const commitment = ['pending', 'pending_revision'].includes(state.departmentCommitment?.status) ? state.departmentCommitment : null;
    const workspaceDraft = commitment?.name
      ? { name: commitment.name, outcome: commitment.outcome, departmentName: commitment.departmentName }
      : department?.name && (!newBusiness?.at || department.at > newBusiness.at)
      ? { name: department.name, outcome: department.purpose }
      : newBusiness || (department?.name ? { name: department.name, outcome: department.purpose } : null);
    const studioBusinessHint = `${workspaceDraft?.name || ''} ${newBusiness?.name || ''} ${department?.name || ''} ${state.firstBusiness || ''}`;
    const studioKey = /小红书/.test(studioBusinessHint) ? 'xhs' : /抖音|TikTok|短视频/.test(studioBusinessHint) ? 'douyin' : /软件|研发|Curis/.test(studioBusinessHint) ? 'software' : (state.selectedTemplate || 'software');
    const studioBlueprints = {
      software: [
        ['意图', 'CEO', '经营问题、真实使用反馈', '可验证的产品目标与验收标准', 'CEO 负责取舍'],
        ['产品', '产品 AI', 'CEO 意图、历史决策', '版本范围、产品 Brief、变更记录', 'CEO 确认范围'],
        ['研发', '研发 AI', '产品范围、代码库、能力配置', '可运行版本、提交记录、发布说明', '风险异常时升级'],
        ['QA', 'QA AI', '候选版本、验收标准', '回归记录、已知未知、证据包', '质量门槛自动执行'],
        ['验收', 'CEO', '可运行版本、证据包', '通过、退回修改或现场演示记录', '必须真实使用'],
        ['反馈', '运行反馈 AI', 'CEO 反馈、使用路径', '问题归因、改进建议、复现证据', '异常时提醒 CEO'],
        ['复盘', '产品 AI', '验收结果、缺陷、业务结果', '下一周期意图与优先级', 'CEO 决定是否继续'],
        ['下一周期', 'CEO 助理', '复盘结论、容量、经营账', '新的研发承诺与检查点', 'CEO 批准投入'],
        ['归档', '成果库', '验收反馈、版本与证据', '可复用成果、知识与工作流', '进入下一周期上下文']
      ],
      xhs: [
        ['搜集', '策略分析 AI', '平台趋势、竞品、账号历史', '趋势摘要与可引用来源', '自动运行'],
        ['拆解', '业务分析 AI', '关键词、封面、评论、互动', '内容结构与表现假设', '异常时升级'],
        ['分析', '策略分析 AI', '拆解结果、公司知识库', '选题优先级与内容 Brief', 'CEO 调整方向'],
        ['产出', '内容制作 AI', 'Brief、品牌语气、素材', '标题、正文、封面与版本', 'AI 先出初稿'],
        ['待发布', '发布 AI', '最终稿、敏感词、账号权限', '发布包与发布时间', 'CEO 确认边界'],
        ['数据', '数据回收 AI', '平台 API 或手动窗口', '阅读、互动、粉丝、线索价值', 'CEO 确认可信度'],
        ['复盘', '增长 AI', '内容版本、结果、历史基线', '归因结论与知识更新', 'CEO 决定投入'],
        ['提升', '增长 AI + CEO', '复盘结论、容量、经营账', '下一轮选题权重与排期', '批准扩大或暂停'],
        ['归档', '成果库', '内容版本、平台结果与 CEO 判断', '可复用选题规则、素材与工作流', '带上下文进入下一轮']
      ],
      douyin: [
        ['选题', '策略 AI', '平台趋势、受众、账号历史', '视频假设与候选选题', '自动运行'],
        ['脚本', '脚本 AI', '选题 Brief、知识库、品牌规则', '脚本、分镜、开场测试', 'CEO 处理重大取舍'],
        ['制作', '制作 AI', '分镜、素材、版权清单', '可剪辑素材与制作证据', '版权异常时升级'],
        ['剪辑', '视频 AI', '原始素材、节奏规则', '多版成片、字幕与封面', 'CEO 选择版本'],
        ['发布', '发布 AI', '最终视频、平台权限', '发布记录与平台链接', 'CEO 确认账号安全'],
        ['数据', '数据 AI', '平台 API 或手动窗口', '播放、完播、互动、粉丝、成交', 'CEO 确认价值口径'],
        ['复盘', '增长 AI', '内容版本、外部结果、基线', '归因结论与可复用知识', 'CEO 决定下一步'],
        ['提升', '增长 AI + CEO', '复盘、产能、经营账', '下一轮频率、预算与容量', '批准扩大、维持或暂停'],
        ['归档', '成果库', '视频版本、平台结果与 CEO 判断', '可复用脚本、素材与工作流', '带上下文进入下一轮']
      ]
    };
    const blueprint = studioBlueprints[studioKey] || studioBlueprints.software;
    const studioChecks = {
      software: [
        ['CEO 真实验收路径未确认', '需要明确创建公司、进入经营日、进入业务空间和反馈改进的完整路径'],
        ['研发 AI 容量待确认', '当前版本开发、QA 与运行反馈共用容量，模拟会验证交接是否顺畅'],
        ['真实使用反馈入口未绑定', '验收通过、退回修改和现场演示都必须回到下一周期']
      ],
      xhs: [
        ['外部数据授权未配置', '小红书账号授权缺失，数据节点先保留 CEO 手动回传窗口'],
        ['策略分析 AI 容量告警', '研究、拆解和复盘共用容量，建议先运行一轮再决定是否增加实例'],
        ['CEO 品牌反馈入口未绑定', '发布前的品牌语气和敏感表达必须形成结构化反馈']
      ],
      douyin: [
        ['平台数据授权未配置', '抖音 / TikTok 数据权限缺失，结果节点先保留手动补录窗口'],
        ['制作与数据 AI 容量待确认', '制作、发布和数据回收共用容量，模拟会验证发布后的回流交接'],
        ['CEO 内容安全反馈入口未绑定', '账号安全、版权和内容风险必须形成可回退的 CEO 检查点']
      ]
    }[studioKey] || [];
    ['gap', 'overload', 'risk'].forEach((kind, index) => {
      const check = studioChecks[index];
      if (!check) return;
      const item = document.querySelector(`.check-item.${kind}`);
      item?.querySelector('.check-text')?.replaceChildren(document.createTextNode(check[0]));
      item?.querySelector('.check-meta')?.replaceChildren(document.createTextNode(check[1]));
    });
    [...canvasArea.querySelectorAll('.node')].slice(0, blueprint.length).forEach((node, index) => {
      const [name, badge, input, output, evidence] = blueprint[index];
      node.querySelector('.node-name')?.replaceChildren(document.createTextNode(name));
      node.querySelector('.node-badge')?.replaceChildren(document.createTextNode(badge));
      const values = node.querySelectorAll('.node-value');
      [input, output, evidence].forEach((value, valueIndex) => values[valueIndex]?.replaceChildren(document.createTextNode(value)));
    });
    const studioBreadcrumb = [...document.querySelectorAll('.breadcrumbs span')]
      .find(item => item.textContent.trim() !== 'Curis' && item.textContent.trim() !== '/');
    if (studioBreadcrumb) studioBreadcrumb.replaceChildren(document.createTextNode(workspaceDraft?.name || FOUNDING_TEMPLATES[studioKey]?.label || '业务空间'));
    if (!workspaceDraft?.name) canvasHeader.querySelector('h1')?.replaceChildren(document.createTextNode(`${FOUNDING_TEMPLATES[studioKey]?.label || '业务'} 业务空间蓝图`));
    if (workspaceDraft?.name) {
      canvasHeader.querySelector('h1')?.replaceChildren(document.createTextNode(`${workspaceDraft.name} 业务空间蓝图`));
      const meta = canvasHeader.querySelector('.canvas-meta');
      if (meta) meta.textContent = `新空间草案 · 目标结果：${workspaceDraft.outcome}`;
      [...document.querySelectorAll('.breadcrumbs span')]
        .find(item => item.textContent.trim() !== 'Curis' && item.textContent.trim() !== '/')
        ?.replaceChildren(document.createTextNode(workspaceDraft.name));
    }
    const reusedAsset = state.lastReusedAsset;
    const reusedOutcome = state.lastReusedOutcome;
    const savedAdditions = Array.isArray(state.workspaceStudio?.additions) ? state.workspaceStudio.additions : [];
    const additions = [
      ...(reusedAsset && !savedAdditions.some(item => item.label === `复用成果 · ${reusedAsset}`) ? [...savedAdditions, { label: `复用成果 · ${reusedAsset}`, category: '复用成果' }] : savedAdditions),
      ...(reusedOutcome && !savedAdditions.some(item => item.outcomeId === reusedOutcome.id) ? [{ label: `结果包 · ${reusedOutcome.business}`, category: '业务结果', outcomeId: reusedOutcome.id, note: `价值 ¥${Number(reusedOutcome.value || 0).toLocaleString()} · ${runLabelForState(state, reusedOutcome.runId, reusedOutcome.runIds)}` }] : [])
    ].slice(-8);
    let studio = {
      issuesResolved: Boolean(state.workspaceStudio?.issuesResolved),
      simulationPassed: Boolean(state.workspaceStudio?.simulationPassed),
      additions,
      externalAgents: Array.isArray(state.workspaceStudio?.externalAgents) ? state.workspaceStudio.externalAgents : []
    };
    if (reusedAsset || reusedOutcome) writeState({ workspaceStudio: studio, lastReusedAsset: null, lastReusedOutcome: null });
    const assembly = document.createElement('div');
    assembly.className = 'curis-studio-assembly';
    assembly.setAttribute('aria-label', '业务空间装配记录');
    assembly.innerHTML = `<div class="curis-studio-assembly-copy"><p class="curis-studio-assembly-title">正在装修这间业务办公室</p><p class="curis-studio-assembly-note">点击或拖入左侧模块，把岗位、能力和外部验收装进可运行的业务空间。</p></div><div class="curis-studio-assembly-list"></div><div class="curis-studio-assembly-actions"><button class="curis-studio-import" type="button" data-external-agent-import>导入外部 Agent</button><button class="curis-studio-submit" type="button" data-curis-handled="true" disabled>等待模拟通过</button></div>`;
    canvasHeader.parentNode.insertBefore(assembly, canvasArea);
    const assemblyList = assembly.querySelector('.curis-studio-assembly-list');
    const submitAssembly = assembly.querySelector('.curis-studio-submit');
    const workflowShelf = document.createElement('section');
    workflowShelf.className = 'curis-workflow-shelf';
    workflowShelf.setAttribute('aria-label', '可复用工作流');
    workflowShelf.innerHTML = '<div class="curis-workflow-shelf-head"><div><strong>可复用工作流</strong><span>把已经验证过的业务工序带进这间办公室，保留原始上下文。</span></div><em>工作流资产</em></div><div class="curis-workflow-list"></div>';
    assembly.insertBefore(workflowShelf, assembly.querySelector('.curis-studio-assembly-actions'));
    const workflowList = workflowShelf.querySelector('.curis-workflow-list');
    const workflowSeeds = [
      { id: 'seed-software', name: 'Curis 软件交付闭环', source: '研发办公室', status: '业务模板 · 待本公司验证' },
      { id: 'seed-xhs', name: '小红书内容增长闭环', source: '小红书运营办公室', status: '业务模板 · 待本公司验证' },
      { id: 'seed-douyin', name: '抖音 / TikTok 数据增长闭环', source: '抖音 / TikTok 运营办公室', status: '业务模板 · 待本公司验证' }
    ];
    const readWorkflows = () => {
      try { return JSON.parse(localStorage.getItem('curis-workflows') || '[]'); } catch (_) { return []; }
    };
    const renderWorkflows = () => {
      const saved = readWorkflows().filter(item => item?.name);
      const workflows = [...workflowSeeds, ...saved].filter((item, index, list) => list.findIndex(candidate => candidate.name === item.name) === index).slice(-8);
      workflowList.replaceChildren();
      workflows.forEach(workflow => {
        const row = document.createElement('div');
        row.className = 'curis-workflow-row';
        const copy = document.createElement('div');
        const title = document.createElement('strong');
        title.textContent = workflow.name;
        const meta = document.createElement('span');
        meta.textContent = `${workflow.source || '公司工作流'} · ${workflow.status || '已保存'}`;
        copy.append(title, meta);
        const reuse = document.createElement('button');
        reuse.type = 'button';
        reuse.dataset.curisHandled = 'true';
        reuse.dataset.workflowReuse = workflow.name;
        reuse.textContent = '复用';
        row.append(copy, reuse);
        workflowList.appendChild(row);
      });
    };
    const save = patch => {
      studio = { ...studio, ...patch };
      writeState({ workspaceStudio: studio });
      render();
    };
    const reuseWorkflow = name => {
      const additions = [...studio.additions, { label: `工作流 · ${name}`, category: '工作流' }].slice(-8);
      save({ additions, issuesResolved: false, simulationPassed: false });
      writeState({ lastAssistantMessage: `已把“${name}”带入当前业务空间，原有来源和交接规则仍然保留。`, lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '工作流已复用' } });
      showToast(`已复用“${name}”，请重新运行模拟`);
    };
    workflowList.addEventListener('click', event => {
      const reuse = event.target.closest('[data-workflow-reuse]');
      if (reuse) reuseWorkflow(reuse.dataset.workflowReuse);
    });
    const addModule = label => {
      const value = String(label || '').trim();
      if (!value) return;
      const category = '业务结构';
      const additions = [...studio.additions, { label: value, category }].slice(-8);
      save({ additions, issuesResolved: false, simulationPassed: false });
      showToast(`${value} 已加入业务空间`);
    };
    const submitApproval = () => {
      if (!studio.issuesResolved) return showToast('请先修复配置问题');
      if (!studio.simulationPassed) return showToast('请先运行模拟');
      if (studio.externalAgents.some(agent => !agent.reviewed)) return showToast('请先审阅已导入的外部 Agent');
      writeState({
        lastAssistantMessage: '工作空间蓝图已经通过模拟。我已替你准备审批包，下一步需要你在决策室做最后判断。',
        lastAssistantHandoff: { label: '决策室', route: 'decision-room.html', message: '工作空间蓝图已通过模拟，等待 CEO 审批' }
      });
      window.location.href = 'decision-room.html';
    };
    submitAssembly.addEventListener('click', submitApproval);
    assembly.querySelector('[data-external-agent-import]')?.addEventListener('click', () => openFormDialog({
      title: '拆解并导入外部 Agent',
      description: '只带入它的职责、输入输出和交接规则，不直接复制不可见的内部提示。导入后由 CEO 审阅，再放入当前业务空间。',
      submitLabel: '拆解为可复用模块',
      fields: [
        { name: 'name', label: 'Agent 名称', placeholder: '例如：小红书选题研究 Agent', required: true },
        { name: 'source', label: '来源', placeholder: '例如：外部产品 / 本地脚本 / 个人经验', required: true },
        { name: 'responsibility', label: '要承担的责任', type: 'textarea', placeholder: '例如：每天收集平台趋势并产出 3 条可验证选题', required: true },
        { name: 'handoff', label: '交接给谁', placeholder: '例如：分析 AI → CEO 验收', required: true }
      ],
      onSubmit: values => {
        const current = readState();
        const imported = { id: Date.now(), ...values, reviewed: false, at: new Date().toISOString() };
        const existing = Array.isArray(current.workspaceStudio?.externalAgents) ? current.workspaceStudio.externalAgents : [];
        const additions = [...studio.additions, { label: `外部 Agent · ${values.name}`, category: '外部 Agent' }].slice(-8);
        save({ additions, externalAgents: [...existing, imported].slice(-12), issuesResolved: false, simulationPassed: false });
        writeState({ lastAssistantMessage: `外部 Agent“${values.name}”已拆解成职责、输入输出和交接模块，等待 CEO 审阅后进入模拟。`, lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '外部 Agent 已拆解' } });
        showToast(`已导入并拆解“${values.name}”`);
      }
    }));
    const render = () => {
      assemblyList.replaceChildren();
      studio.additions.forEach((item, index) => {
        const chip = document.createElement('span');
        chip.className = 'curis-studio-chip';
        const text = document.createElement('span');
        text.textContent = item.label;
        if (item.note) chip.title = item.note;
        const external = item.category === '外部 Agent'
          ? studio.externalAgents.find(agent => item.label === `外部 Agent · ${agent.name}`)
          : null;
        if (external && !external.reviewed) {
          const review = document.createElement('button');
          review.type = 'button';
          review.className = 'curis-studio-review';
          review.textContent = '审阅';
          review.addEventListener('click', () => openFormDialog({
            title: `审阅外部 Agent · ${external.name}`,
            description: `来源：${external.source}\n责任：${external.responsibility}\n交接：${external.handoff}\n\n确认后只把这些可见契约纳入当前业务空间，不复制外部 Agent 的不可见内部提示。`,
            submitLabel: '纳入当前空间',
            fields: [{ name: 'note', label: 'CEO 审阅备注', type: 'textarea', placeholder: '例如：只允许读取公开平台数据，发布前必须回到 CEO。' }],
            onSubmit: values => {
              save({ externalAgents: studio.externalAgents.map(agent => agent.id === external.id ? { ...agent, reviewed: true, reviewNote: values.note || '', reviewedAt: new Date().toISOString() } : agent), issuesResolved: false, simulationPassed: false });
              showToast(`已审阅并纳入“${external.name}”`);
            }
          }));
          chip.appendChild(review);
        }
        const remove = document.createElement('button');
        remove.type = 'button';
        remove.setAttribute('aria-label', `移除 ${item.label}`);
        remove.textContent = '×';
        remove.addEventListener('click', () => save({ additions: studio.additions.filter((_, itemIndex) => itemIndex !== index), externalAgents: external ? studio.externalAgents.filter(agent => agent.id !== external.id) : studio.externalAgents, issuesResolved: false, simulationPassed: false }));
        chip.append(text, remove);
        assemblyList.appendChild(chip);
      });
      assembly.classList.toggle('is-ready', studio.issuesResolved && studio.simulationPassed && studio.externalAgents.every(agent => agent.reviewed));
      if (workspaceDraft?.outcome) assembly.querySelector('.curis-studio-assembly-note').textContent = `${workspaceDraft.departmentName ? `${workspaceDraft.departmentName} 首项责任 · ` : ''}目标结果：${workspaceDraft.outcome} 点击或拖入模块，把岗位、能力和外部验收装进可运行的业务空间。`;
      const meta = document.querySelector('.canvas-meta');
      if (meta) {
        const count = 5 + studio.additions.length;
        const status = studio.simulationPassed ? '模拟已通过，可提交审批' : studio.issuesResolved ? '配置已通过 · 等待运行模拟' : '3 项配置检查未通过';
        meta.textContent = `${workspaceDraft?.name ? '新空间草案' : '草稿 v0.3'} · ${count} 个模块已组装 · ${status}`;
      }
      const configSub = document.querySelector('.config-sub');
      const pendingAgents = studio.externalAgents.filter(agent => !agent.reviewed).length;
      if (configSub) configSub.textContent = pendingAgents ? `还有 ${pendingAgents} 个外部 Agent 待 CEO 审阅` : studio.issuesResolved ? '配置已通过 · 可以运行模拟' : '未通过 3 项 · 无法提交审批';
      submitAssembly.disabled = !studio.simulationPassed || pendingAgents > 0;
      submitAssembly.textContent = pendingAgents ? `待审阅 ${pendingAgents} 个外部 Agent` : studio.simulationPassed ? '提交审批 →' : '等待模拟通过';
      const statusPill = document.querySelector('.role-strip .pill');
      if (statusPill) {
        statusPill.className = studio.issuesResolved ? 'pill pill-ontrack' : 'pill pill-attention';
        statusPill.textContent = studio.issuesResolved ? '配置已通过' : '3 项待修复';
      }
      renderWorkflows();
      document.querySelectorAll('.check-item.gap, .check-item.overload, .check-item.risk').forEach(item => item.classList.toggle('curis-check-resolved', studio.issuesResolved));
      const fixButton = document.querySelector('.config-actions .btn-secondary');
      if (fixButton) {
        fixButton.textContent = studio.issuesResolved ? '问题已修复' : '修复问题';
        fixButton.disabled = studio.issuesResolved;
      }
      const simButtons = [...document.querySelectorAll('.config-actions .btn-primary, .bottom-actions .btn-primary')].filter(button => button.textContent.includes('运行模拟'));
      simButtons.forEach(button => { button.textContent = studio.simulationPassed ? '模拟已通过' : '运行模拟'; button.disabled = studio.simulationPassed; });
      const lifecycle = [...document.querySelectorAll('.lifecycle-step')];
      lifecycle.forEach(step => step.classList.remove('current'));
      const currentLabels = studio.simulationPassed ? ['Approve', '审批'] : studio.issuesResolved ? ['Simulate', '模拟'] : ['Blueprint', '蓝图'];
      lifecycle.find(step => currentLabels.includes(step.textContent.trim()))?.classList.add('current');
    };
    paletteItems.forEach(item => {
      const label = item.textContent.trim();
      item.addEventListener('click', () => addModule(label));
      item.addEventListener('dragstart', event => event.dataTransfer?.setData('text/plain', label));
    });
    canvasArea.addEventListener('dragover', event => event.preventDefault());
    canvasArea.addEventListener('drop', event => {
      event.preventDefault();
      addModule(event.dataTransfer?.getData('text/plain'));
    });
    const fixButton = document.querySelector('.config-actions .btn-secondary');
    if (fixButton) {
      fixButton.dataset.curisHandled = 'true';
      fixButton.onclick = () => {
        if (studio.issuesResolved) return;
        save({ issuesResolved: true });
        showToast('配置问题已修复，下一步可以运行模拟');
      };
    }
    const simulationButtons = [...document.querySelectorAll('.config-actions .btn-primary, .bottom-actions .btn-primary')].filter(button => button.textContent.includes('运行模拟'));
    simulationButtons.forEach(button => {
      button.dataset.curisHandled = 'true';
      button.onclick = () => {
        if (!studio.issuesResolved) return showToast('请先修复配置问题');
        if (studio.simulationPassed) return;
        save({ simulationPassed: true });
        showToast('运行模拟通过，审批包已准备');
      };
    });
    const submitButton = [...document.querySelectorAll('.bottom-actions .btn-primary')].find(button => button.textContent.includes('提交审批'));
    if (submitButton) {
      submitButton.dataset.curisHandled = 'true';
      submitButton.onclick = submitApproval;
    }
    render();
  }

  function initWorkspacePortal() {
    if (!window.location.pathname.endsWith('workspace-portal.html')) return;
    const renderWorkspaceTruth = () => {
      const state = readState();
      const records = [
        { business: '软件开发', match: /软件开发/, result: state.softwareAcceptance, waiting: '研发办公室等待首轮真实运行' },
        { business: '小红书运营', match: /小红书/, result: state.latestXhsFeedback, waiting: '等待平台结果或 CEO 手动回传' },
        { business: '抖音 / TikTok 运营', match: /抖音|TikTok/, result: state.latestExternalFeedback, waiting: '等待平台结果或 CEO 手动回传' }
      ];
      const businessKey = value => /小红书/.test(String(value || '')) ? '小红书运营' : /抖音|TikTok|短视频/.test(String(value || '')) ? '抖音 / TikTok 运营' : /软件|研发|Curis/.test(String(value || '')) ? '软件开发' : '公司共享';
      const activeBusinesses = new Set(['公司共享', businessKey(state.firstBusiness), businessKey(state.newBusinessDraft?.name), businessKey(state.departmentCommitment?.name)]);
      if (state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html')) activeBusinesses.add('软件开发');
      if (state.latestXhsFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-xhs.html')) activeBusinesses.add('小红书运营');
      if (state.latestExternalFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-shortvideo.html')) activeBusinesses.add('抖音 / TikTok 运营');
      const cardState = card => records.find(item => item.match.test(card.querySelector('.card-title')?.textContent || ''));
      const running = records.filter(item => item.result).length;
      const building = ['draft', 'simulated', 'pending_approval'].includes(state.workspaceDraft?.status) ? 1 : 0;
      const archived = Array.isArray(state.operatingArchivedItems) ? state.operatingArchivedItems.length : 0;
      document.querySelectorAll('.summary-tabs .tab-btn').forEach(tab => {
        const label = tab.textContent.replace(/\d+/g, '').trim();
        const count = label.includes('运行') ? running : label.includes('装修') ? building : archived;
        const node = tab.querySelector('.count'); if (node) node.textContent = String(count);
      });
      const stats = document.querySelectorAll('.quick-stats .stat-card');
      const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
      if (stats[0]) { stats[0].querySelector('.value').textContent = String(new Set(runs.filter(run => ['running', 'queued'].includes(run.status)).map(run => run.business || run.route)).size); stats[0].querySelector('.meta').textContent = running ? '已收到真实运行或结果记录' : '尚无真实运行记录'; }
      if (stats[1]) { const waiting = runs.filter(run => run.status === 'waiting_ceo').length; stats[1].querySelector('.value').textContent = String(waiting); stats[1].querySelector('.meta').textContent = waiting ? '需要 CEO 处理的运行结果' : '尚无待 CEO 验收事项'; }
      if (stats[2]) { stats[2].querySelector('.value').textContent = '0'; stats[2].querySelector('.meta').textContent = '未把等待结果误报为阻塞'; }
      if (stats[3]) { const evidence = (state.outcomeAttributions || []).length + (state.softwareAcceptance ? 1 : 0) + (state.latestXhsFeedback ? 1 : 0) + (state.latestExternalFeedback ? 1 : 0); stats[3].querySelector('.value').textContent = String(evidence); stats[3].querySelector('.meta').textContent = evidence ? '最近一轮真实证据已写回' : '等待第一条真实证据'; }
      const sectionTitle = document.querySelector('#panel-running .section-title');
      const cards = [...document.querySelectorAll('.workspace-card')];
      const empty = document.querySelector('[data-workspace-empty]');
      if (!state.companyCreatedAt) {
        if (sectionTitle) { const hint = sectionTitle.querySelector('.hint'); sectionTitle.firstChild.textContent = '公司还没有业务空间'; if (hint) hint.textContent = '完成公司创建后，第一间办公室会出现在这里'; }
        cards.forEach(card => { card.hidden = true; card.style.display = 'none'; });
        if (!empty) {
          const notice = document.createElement('article');
          notice.dataset.workspaceEmpty = 'true';
          notice.className = 'workspace-card unknown';
          notice.innerHTML = '<div class="card-title">第一间办公室还没有建立</div><p class="card-summary">先创建公司，再选择软件开发、小红书或抖音 / TikTok 业务模板。</p><button type="button" class="primary" data-workspace-create>开始创建公司</button>';
          document.querySelector('#panel-running')?.appendChild(notice);
          notice.querySelector('[data-workspace-create]')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
        }
        return;
      }
      if (empty) empty.remove();
      cards.forEach(card => {
        const info = cardState(card);
        const visible = Boolean(info && activeBusinesses.has(info.business));
        card.hidden = !visible;
        card.style.display = visible ? '' : 'none';
      });
      const visibleCards = cards.filter(card => !card.hidden);
      if (sectionTitle) { const hint = sectionTitle.querySelector('.hint'); sectionTitle.firstChild.textContent = '已配置的业务空间'; if (hint) hint.textContent = `${visibleCards.length} 个业务空间已配置，${running ? `${running} 个已有真实运行记录` : '等待首轮真实运行'}`; }
      cards.forEach(card => {
        const info = cardState(card); if (!info) return;
        const hasResult = Boolean(info.result);
        card.classList.toggle('unknown', !hasResult); card.classList.toggle('attention', hasResult && /软件/.test(card.textContent)); card.classList.toggle('blocked', false); card.classList.toggle('ontrack', hasResult && !/软件/.test(card.textContent));
        const pill = card.querySelector('.pill'); if (pill) { pill.className = `pill ${hasResult ? 'pill-ontrack' : 'pill-unknown'}`; pill.textContent = hasResult ? '已有结果' : '待首轮结果'; }
        const fields = [...card.querySelectorAll('.field')];
        const cycle = fields.find(field => field.querySelector('.field-label')?.textContent.includes('当前周期'))?.querySelector('.field-value');
        const checkpoint = fields.find(field => field.querySelector('.field-label')?.textContent.includes('下一检查点'))?.querySelector('.field-value');
        const block = card.querySelector('.block-line');
        const external = fields.find(field => field.querySelector('.field-label')?.textContent.includes('外部结果'))?.querySelector('.evidence-line');
        if (!hasResult) { if (cycle) cycle.textContent = '业务模板已加载'; if (checkpoint) checkpoint.textContent = '等待首轮真实运行'; if (block) { block.className = 'block-line neutral'; block.textContent = info.waiting; } if (external) external.innerHTML = '<span class="pending">− 尚无真实回传</span>'; }
      });
    };
    renderWorkspaceTruth();
    window.addEventListener('curis-state-changed', renderWorkspaceTruth);
    document.querySelectorAll('[data-runtime-page]').forEach(button => {
      if (button.dataset.curisHandled === 'true') return;
      button.dataset.curisHandled = 'true';
      button.addEventListener('click', () => {
        const route = button.dataset.runtimePage;
        if (!route) return;
        writeState({ lastAssistantMessage: `已打开${button.closest('.workspace-card')?.querySelector('.card-title')?.textContent?.trim() || '业务空间'}运行现场。`, lastAssistantHandoff: { label: '业务空间运行', route, message: '进入 Runtime' } });
        window.location.href = route;
      });
    });
    document.querySelectorAll('.btn-studio').forEach(button => {
      if (button.dataset.curisHandled === 'true') return;
      button.dataset.curisHandled = 'true';
      button.addEventListener('click', () => {
        writeState({ lastAssistantMessage: '我已把这间业务办公室带回搭建现场，继续调整岗位、能力和验收路径。', lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '查看 Studio' } });
        window.location.href = 'workspace-studio.html';
      });
    });
    const modal = document.querySelector('#studio-modal');
    if (!modal || modal.dataset.curisRuntimeBound === 'true') return;
    modal.dataset.curisRuntimeBound = 'true';
    const modalButtons = [...modal.querySelectorAll('button')];
    const findModalButton = label => modalButtons.find(button => button.textContent.trim().includes(label));
    const simulationButton = findModalButton('运行模拟');
    const submitButton = findModalButton('提交审批');
    const saveButton = findModalButton('保存草稿');
    const fullStudioButton = modal.querySelector('button[onclick*="workspace-studio"]');
    const checks = [...modal.querySelectorAll('.studio-checks .check')];
    const portalDraft = readState().workspacePortalDraft || {};
    let simulationPassed = Boolean(portalDraft.simulationPassed);
    const refreshModalActions = () => {
      if (simulationButton) {
        simulationButton.dataset.curisHandled = 'true';
        simulationButton.disabled = simulationPassed;
        simulationButton.textContent = simulationPassed ? '模拟已通过' : '运行模拟';
      }
      if (submitButton) {
        submitButton.dataset.curisHandled = 'true';
        submitButton.disabled = !simulationPassed;
      }
    };
    if (simulationPassed) {
      const check = checks.find(node => node.textContent.includes('未运行模拟')) || checks[checks.length - 1];
      if (check) { check.className = 'check ok'; check.textContent = '✓ 运行模拟已通过'; }
    }
    refreshModalActions();
    simulationButton?.addEventListener('click', () => {
      if (checks.some(node => node.classList.contains('warn'))) {
        writeState({ lastAssistantMessage: '新业务空间还有配置缺口，我建议先进入 Studio 完整视图处理，再运行模拟。', lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '配置检查未通过' } });
        return showToast('还有配置缺口，请进入 Studio 完整视图处理');
      }
      simulationPassed = true;
      const check = checks.find(node => node.textContent.includes('未运行模拟')) || checks[checks.length - 1];
      if (check) { check.className = 'check ok'; check.textContent = '✓ 运行模拟已通过'; }
      refreshModalActions();
      writeState({ workspacePortalDraft: { ...readState().workspacePortalDraft, simulationPassed: true, at: new Date().toISOString() }, lastAssistantMessage: '新业务空间的首轮运行模拟已通过，下一步可以提交 CEO 审批。' });
      showToast('运行模拟已通过，可以提交审批');
    });
    submitButton?.addEventListener('click', () => {
      if (!simulationPassed && !checks.some(node => node.textContent.includes('运行模拟已通过'))) return showToast('请先运行模拟，再提交审批');
      writeState({ workspacePortalDraft: { ...readState().workspacePortalDraft, simulationPassed: true, status: 'pending_approval', at: new Date().toISOString() }, workspaceDraft: { status: 'pending_approval', source: 'workspace-portal.html', at: new Date().toISOString() }, lastAssistantMessage: '新业务空间已提交审批。我会把配置检查和模拟证据带到决策室，请 CEO 做最后判断。', lastAssistantHandoff: { label: '决策室', route: 'decision-room.html', message: '新业务空间等待审批' } });
      window.location.href = 'decision-room.html';
    });
    saveButton?.addEventListener('click', () => {
      writeState({ workspacePortalDraft: { ...readState().workspacePortalDraft, simulationPassed, status: simulationPassed ? 'simulated' : 'draft', at: new Date().toISOString() }, workspaceDraft: { status: simulationPassed ? 'simulated' : 'draft', source: 'workspace-portal.html', at: new Date().toISOString() }, lastAssistantMessage: '新业务空间草稿已保存，下一次进入工作空间时可以继续装修。' });
      showToast('草稿已保存，稍后可以继续搭建');
    });
    fullStudioButton?.addEventListener('click', event => {
      event.preventDefault();
      writeState({ lastAssistantMessage: '我已把新业务带入完整搭建画布，继续定义阶段、岗位、能力和验收。', lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '进入完整搭建' } });
      window.location.href = 'workspace-studio.html';
    });
  }

  function initStudioToolbar() {
    if (!window.location.pathname.endsWith('workspace-studio.html')) return;
    const canvasArea = document.querySelector('.canvas-area');
    const zoom = [...document.querySelectorAll('button')].find(button => button.textContent.trim() === '100%');
    const layout = [...document.querySelectorAll('button')].find(button => button.textContent.trim() === '布局');
    const history = [...document.querySelectorAll('button')].find(button => button.textContent.trim() === '历史');
    if (zoom && zoom.dataset.curisHandled !== 'true') {
      zoom.dataset.curisHandled = 'true';
      zoom.addEventListener('click', () => {
        const next = zoom.textContent.trim() === '100%' ? '110%' : zoom.textContent.trim() === '110%' ? '90%' : '100%';
        zoom.textContent = next;
        if (canvasArea) canvasArea.style.setProperty('--studio-zoom', next.replace('%', '') / 100);
        showToast(`画布缩放至 ${next}`);
      });
    }
    if (layout && layout.dataset.curisHandled !== 'true') {
      layout.dataset.curisHandled = 'true';
      layout.addEventListener('click', () => {
        canvasArea?.classList.toggle('is-compact');
        showToast(canvasArea?.classList.contains('is-compact') ? '已切换紧凑布局' : '已恢复标准布局');
      });
    }
    if (history && history.dataset.curisHandled !== 'true') {
      history.dataset.curisHandled = 'true';
      history.addEventListener('click', () => showToast('已打开蓝图版本记录：v0.3 → 运行版 v1.0'));
    }
  }

  function initDecisionRuntime() {
    if (!window.location.pathname.endsWith('decision-room.html') || typeof window.makeDecision !== 'function' || window.makeDecision.__curisWrapped) return;
    const original = window.makeDecision;
    const runtimeState = readState();
    const departmentDraft = runtimeState.departmentDraft?.name ? runtimeState.departmentDraft : null;
    const departmentName = runtimeState.departmentDraft?.name || '';
    const nonSoftwareDepartment = departmentName && !/软件开发|研发办公室|Curis v0\.2/.test(departmentName);
    const softwareFlow = !nonSoftwareDepartment && [runtimeState.firstBusiness, runtimeState.newBusinessDraft?.name, departmentName, runtimeState.departmentCommitment?.name]
      .filter(Boolean)
      .some(value => /软件开发|研发办公室|Curis v0\.2/.test(value));
    const commitmentFlow = Boolean(departmentDraft && ['pending', 'pending_revision'].includes(runtimeState.departmentCommitment?.status));
    const departmentFlow = Boolean(departmentDraft && !softwareFlow && (commitmentFlow || runtimeState.departmentStatus !== 'active'));
    const routes = {
      approve: { action: '批准并发布 Runtime v1.1', label: '抖音 / TikTok 运营办公室', route: 'workspace-runtime-shortvideo.html', next: '进入抖音 / TikTok 运营办公室执行 →', message: '你已批准抖音 / TikTok 运营 Runtime v1.1。我会把执行交给运营办公室，并在结果回来后汇报。' },
      defer: { action: '延后 3 天', label: 'CEO 工作台', route: 'ceo-desk.html', next: '回到 CEO 工作台 →', message: '你已将这项决策延后 3 天。我会替你守住检查点，准备下一次决策包。' },
      revise: { action: '要求修改', label: '工作空间搭建', route: 'workspace-studio.html', next: '回到工作空间搭建 →', message: '你已要求修改 Blueprint。我会把缺口交回工作空间搭建现场，并在重新提交时提醒你。' },
      reject: { action: '拒绝并保留 v1.0', label: 'CEO 工作台', route: 'ceo-desk.html', next: '回到 CEO 工作台 →', message: '你已拒绝本次发布，当前 Runtime v1.0 继续运行。我会保留这条判断和依据。' }
    };
    const fallbacks = {
      approve: { title: '已批准：抖音 / TikTok 运营 Workspace Runtime v1.1 正式发布', body: '下一步：抖音 / TikTok 运营办公室接管全链路；首周检查点设为 2026-08-05 09:00。旧 Runtime v1.0 保留 14 天作为回滚路径。' },
      defer: { title: '已延后：3 天后重新决策', body: '下一步：业务工程 AI 安排限流实测；当前 v1.0 继续运行，检查点顺延至 8/8。' },
      revise: { title: '已退回：要求修改 Blueprint v0.3', body: '下一步：回到工作空间搭建，补充 4K 基准测试、品牌安全审核清单和限流应对策略后重新提交。' },
      reject: { title: '已拒绝：保留 Runtime v1.0', body: '下一步：继续运行当前 Runtime v1.0；Blueprint v0.3 归档为待办，不触发额外成本。' }
    };
    if (softwareFlow) {
      routes.approve = { action: '批准并发布 Curis v0.2', label: '研发办公室', route: 'workspace-runtime-software.html', next: '进入研发办公室执行 →', message: '你已批准 Curis v0.2。研发办公室会接管真实验收，并在 CEO 反馈回来后汇报下一次软件增量。' };
      fallbacks.approve = { title: '已批准：Curis v0.2 进入真实验收', body: '下一步：研发办公室接管验收路径；CEO 通过真实使用确认后，形成下一周期软件增量。' };
      document.getElementById('decision-title')?.replaceChildren(document.createTextNode('批准 Curis v0.2 → 研发办公室真实验收'));
      document.querySelector('#q-title strong')?.replaceChildren(document.createTextNode('CEO 需要决定：是否批准将 Curis v0.2 交给研发办公室进行真实使用验收？'));
    }
    if (departmentFlow) {
      const departmentName = departmentDraft.name;
      routes.approve = commitmentFlow
        ? { action: `批准并启动 ${departmentName} 首项责任`, label: '工作空间入口', route: 'workspace-portal.html', next: '进入部门办公室 →', message: `你已批准${departmentName}承接首项责任。我会把这项承诺交给它的业务空间，并在结果回来后汇报。` }
        : { action: `批准并建立 ${departmentName}`, label: 'AI 团队办公室', route: 'ai-organization.html', next: '进入 AI 团队办公室 →', message: `你已批准建立${departmentName}。我会把这间办公室登记进公司组织，并提醒它承接第一项共同责任。` };
      routes.revise = { action: '退回工作空间搭建', label: '工作空间搭建', route: 'workspace-studio.html', next: '回到工作空间搭建 →', message: `你已要求修改${departmentName}办公室草案。我会把缺口交回搭建现场，保留这次判断。` };
      fallbacks.approve = commitmentFlow
        ? { title: `已启动：${departmentName} 开始承接首项责任`, body: `下一步：${departmentName} 的首项业务空间已获批准，AI 团队会按这项承诺运行并回传结果。` }
        : { title: `已建立：${departmentName} 正式进入公司组织`, body: `下一步：${departmentName} 已登记为正式办公室，AI 组织会继续等待它承接第一项业务责任。` };
      fallbacks.revise = { title: `已退回：${departmentName} 办公室需要修改`, body: '下一步：回到工作空间搭建，补齐责任、能力或验收路径后重新提交。' };
      document.title = `决策室 · ${departmentName} · Curis`;
      document.getElementById('decision-title')?.replaceChildren(document.createTextNode(commitmentFlow ? `启动 ${departmentName} 首项责任` : `建立 ${departmentName} 办公室`));
      document.querySelector('#q-title strong')?.replaceChildren(document.createTextNode(commitmentFlow
        ? `CEO 需要决定：是否批准${departmentName}承接“${runtimeState.departmentCommitment.name}”，并让业务空间进入运行？`
        : `CEO 需要决定：是否批准将${departmentName}登记为公司的正式 AI 办公室，并让它承接已定义的共同责任？`));
      document.querySelector('.section[aria-labelledby="q-title"] .card p')?.replaceChildren(document.createTextNode(commitmentFlow
        ? `这项决定会把“${runtimeState.departmentCommitment.name}”从业务空间草案变成${departmentName}的首项正式承诺。批准后，团队开始执行并等待真实结果；退回或延后不会丢失当前搭建记录。`
        : `这项决定会把${departmentName}从办公室草案变成正式组织单元。批准后，组织关系、共享能力和第一项责任会进入运行状态；退回或延后不会丢失当前搭建记录。`));
      document.querySelector('.topic-meta span')?.replaceChildren(document.createTextNode('来源：Workspace Studio · Business Engineering AI'));
      const optionTitles = [...document.querySelectorAll('.option-title')];
      const optionDescriptions = [...document.querySelectorAll('.option-desc')];
      if (optionTitles[0]) optionTitles[0].textContent = commitmentFlow ? `A. 批准并启动 ${departmentName} 首项责任` : `A. 批准并建立 ${departmentName}`;
      if (optionTitles[1]) optionTitles[1].textContent = 'B. 延后 3 天';
      if (optionTitles[2]) optionTitles[2].textContent = 'C. 要求修改';
      if (optionTitles[3]) optionTitles[3].textContent = 'D. 拒绝并保留草案';
      if (optionDescriptions[0]) optionDescriptions[0].textContent = commitmentFlow
        ? `启动“${runtimeState.departmentCommitment.name}”，让${departmentName}开始执行并等待真实结果回流。`
        : `登记${departmentName}，让它进入公司组织；保留 CEO 对第一项责任的确认门。`;
      if (optionDescriptions[1]) optionDescriptions[1].textContent = '保留当前草案，等待更多责任、能力或业务优先级信息后再决定。';
      if (optionDescriptions[2]) optionDescriptions[2].textContent = '退回工作空间搭建，补充缺口后重新提交审批。';
      if (optionDescriptions[3]) optionDescriptions[3].textContent = `不建立${departmentName}，当前草案归档，不触发组织变更。`;
      const cycleNote = document.querySelector('.impact-note.cycle');
      const capacityNote = document.querySelector('.impact-note.capacity');
      const riskNote = document.querySelector('.impact-note.risk');
      if (cycleNote) cycleNote.innerHTML = commitmentFlow
        ? `<strong>经营变化：</strong>批准后将把“${escapeHtml(runtimeState.departmentCommitment.name)}”交给${escapeHtml(departmentName)}执行，并等待首条真实结果。`
        : `<strong>组织变化：</strong>批准后将把“${escapeHtml(departmentName)}”登记为正式 AI 办公室，并等待第一项责任承接。`;
      if (capacityNote) capacityNote.innerHTML = `<strong>能力变化：</strong>办公室先复用当前共享能力；只有真实责任重复出现后，才继续增加岗位或专属能力。`;
      if (riskNote) riskNote.innerHTML = '<strong>承诺风险：</strong>办公室可以先建立，但在没有第一项明确业务责任前，不应被视为已经产生业务结果。';
      const simOutcome = document.querySelector('#sim-normal .sim-outcome');
      if (simOutcome) simOutcome.textContent = commitmentFlow
        ? `${departmentName} 已准备承接“${runtimeState.departmentCommitment.name}”，责任矩阵和共享能力已经挂接；下一步是运行并回收真实结果。`
        : `${departmentName} 已完成组织登记，责任矩阵和共享能力可被下一项业务调用；CEO 仍需为它指定第一项承诺。`;
      const factTitles = [...document.querySelectorAll('.fact-title')];
      const factSources = [...document.querySelectorAll('.fact-source')];
      [`${departmentName} 办公室蓝图已覆盖责任与能力`, '运行模拟全部通过', `${departmentName} 的组织关系已对齐`, '当前共享能力可以承接办公室初始运行', '业务结果尚未绑定，暂无财务估算'].forEach((text, index) => { if (factTitles[index]) factTitles[index].textContent = text; });
      [`来源：Workspace Studio · Business Engineering AI`, '来源：模拟控制台 · 正常路径 / Agent 缺席 / 外部延迟 / CEO 拒绝', `来源：AI 团队办公室 · 责任人：CEO 助理`, '来源：公司能力面 · 当前容量可用', '来源：业务结果层 · 等待第一项责任承诺'].forEach((text, index) => { if (factSources[index]) factSources[index].textContent = text; });
      const unknownTitles = [...document.querySelectorAll('.unknown-item .fact-title')];
      const unknownSources = [...document.querySelectorAll('.unknown-item .fact-source')];
      ['第一项业务责任尚未绑定', '办公室独立承载能力暂无真实负载数据', '是否继续扩充岗位需要真实结果后判断'].forEach((text, index) => { if (unknownTitles[index]) unknownTitles[index].textContent = text; });
      ['风险：办公室建立后仍需要 CEO 指定第一项可验证承诺。', '风险：第一次运行可能暴露共享能力或容量缺口，需要先观察真实负载。', '建议：在第一项责任形成结果后，再决定增加岗位、能力或新的业务空间。'].forEach((text, index) => { if (unknownSources[index]) unknownSources[index].textContent = text; });
      const impactValues = [...document.querySelectorAll('.metric-card .value')];
      const impactDeltas = [...document.querySelectorAll('.metric-card .delta')];
      ['组织建立', '+1 办公室', '待真实结果'].forEach((text, index) => { if (impactValues[index]) impactValues[index].textContent = text; });
      ['批准后进入组织', '先复用共享能力', '不提前承诺收入'].forEach((text, index) => { if (impactDeltas[index]) impactDeltas[index].textContent = text; });
      const simPanels = [...document.querySelectorAll('.sim-panel')];
      const simTitles = ['正常路径：办公室进入组织', '能力缺席：共享资源暂不可用', '外部延迟：第一项结果尚未回流', 'CEO 拒绝：保留办公室草案'];
      const simOutcomes = [`${departmentName} 已登记，组织关系生效；CEO 在工作台指定第一项责任后，办公室才开始承接业务结果。`, '办公室暂不接收新承诺，CEO 助理保留草案并等待能力恢复或重新分配。', '办公室保持已建立状态，但业务结果标记为待补充，直到责任与反馈路径明确。', '办公室草案归档，不触发组织变更；当前共享能力和 CEO 注意力保持不变。'];
      const simMetrics = [['5 条机会', 'CEO 验收', '待观察'], ['1 项责任', '待重分配', '需升级'], ['结果未知', '待 CEO 补录', '关注'], ['0', '保留草案', '搭建后重提']];
      simPanels.forEach((panel, index) => {
        if (panel.querySelector('.sim-title')) panel.querySelector('.sim-title').textContent = simTitles[index];
        if (panel.querySelector('.sim-outcome')) panel.querySelector('.sim-outcome').textContent = simOutcomes[index];
        panel.querySelectorAll('.sim-metric .val').forEach((value, metricIndex) => { if (simMetrics[index]?.[metricIndex]) value.textContent = simMetrics[index][metricIndex]; });
      });
      const decisionHint = document.querySelector('.decision-hint');
      if (decisionHint) decisionHint.innerHTML = '<strong>生效条件：</strong>批准后立即登记 · <strong>退出路径：</strong>退回搭建或保留草案，不丢失当前责任记录';
    }
    const wrapped = function (choice) {
      const result = original.apply(this, arguments);
      const config = routes[choice];
      if (!config) return result;
      const now = new Date();
      const current = readState();
      const history = Array.isArray(current.decisionHistory)
        ? current.decisionHistory
        : (current.lastDecision ? [current.lastDecision] : []);
      const decision = { choice, action: config.action, at: now.toISOString(), source: 'decision-room.html' };
      const departmentPatch = current.departmentDraft
        ? { departmentStatus: choice === 'approve' ? 'active' : 'pending_approval', ...(['pending', 'pending_revision'].includes(current.departmentCommitment?.status) ? { departmentCommitment: { ...current.departmentCommitment, status: choice === 'approve' ? 'active' : 'pending' } } : {}) }
        : {};
      writeState({
        lastDecision: decision,
        decisionHistory: [...history, decision].slice(-12),
        ...departmentPatch,
        lastAssistantMessage: config.message,
        lastAssistantHandoff: { label: config.label, route: config.route, message: config.action }
      });
      const after = document.getElementById('afterDecision');
      if (after) {
        const fallback = fallbacks[choice];
        const nowText = now.toISOString().replace('T', ' ').slice(0, 19);
        document.getElementById('afterTitle').textContent = fallback.title;
        document.getElementById('afterBody').textContent = fallback.body;
        document.getElementById('evidenceId').textContent = `decision://${now.toISOString().slice(0, 10)}/${choice}-${now.getTime()}`;
        document.getElementById('evidenceTrace').innerHTML = `<div><span class="tertiary">决策动作：</span>${config.action}</div><div><span class="tertiary">执行路径：</span>${fallback.body.replace('下一步：', '')}</div><div><span class="tertiary">记录时间：</span><span class="mono">${nowText}</span></div><div><span class="tertiary">来源页面：</span>决策室 / decision-room.html</div><div><span class="tertiary">写入层：</span>Evidence / Truth Layer · 状态：不可篡改</div>`;
        after.classList.add('active');
        const pill = document.querySelector('.pill-decision');
        if (pill) { pill.className = 'pill pill-ontrack'; pill.textContent = '已决策'; }
        let next = after.querySelector('.curis-decision-next');
        if (!next) {
          next = document.createElement('button');
          next.className = 'curis-decision-next';
          next.type = 'button';
          next.setAttribute('data-curis-handled', 'true');
          after.querySelector('.after-body')?.appendChild(next);
        }
        next.textContent = config.next;
        next.onclick = () => { window.location.href = config.route; };
      }
      return result;
    };
    wrapped.__curisWrapped = true;
    window.makeDecision = wrapped;
    const buttonChoices = ['approve', 'defer', 'revise', 'reject'];
    document.querySelectorAll('#decisionButtons .btn').forEach((button, index) => {
      if (!buttonChoices[index]) return;
      button.dataset.curisHandled = 'true';
      button.onclick = () => window.makeDecision(buttonChoices[index]);
    });
    document.querySelectorAll('.option-card[data-option]').forEach(card => {
      const choice = card.dataset.option;
      const body = card.querySelector('.option-body');
      if (!body || body.querySelector('.curis-option-commit')) return;
      const commit = document.createElement('button');
      commit.className = 'curis-option-commit';
      commit.type = 'button';
      commit.dataset.curisHandled = 'true';
      commit.textContent = '确认这项方案';
      commit.addEventListener('click', event => {
        event.stopPropagation();
        window.makeDecision(choice);
      });
      body.appendChild(commit);
    });
  }

  function initDecisionTruth() {
    if (!window.location.pathname.endsWith('decision-room.html')) return;
    const state = readState();
    const hasDecisionContext = Boolean(
      state.businessDecision || state.workspaceDraft || state.departmentDraft ||
      state.newBusinessDraft || state.departmentCommitment ||
      state.lastDecision?.source === 'decision-room.html'
    );
    if (hasDecisionContext) return;
    document.title = '决策室 · 等待提交 · Curis';
    document.querySelector('.pill-decision')?.replaceChildren(document.createTextNode('无待决策项'));
    document.getElementById('decision-title')?.replaceChildren(document.createTextNode('当前没有待 CEO 决策的业务空间'));
    document.querySelector('.topic-meta span:first-child')?.replaceChildren(document.createTextNode('来源：等待 Workspace Studio 提交真实决策包'));
    document.querySelector('.topic-meta span:nth-child(2)')?.replaceChildren(document.createTextNode('提交时间：尚未提交'));
    document.querySelector('.topic-meta span:nth-child(3)')?.replaceChildren(document.createTextNode('决策到期：未设定'));
    document.querySelector('#q-title strong')?.replaceChildren(document.createTextNode('CEO 现在不需要做决定：先在工作空间完成配置、模拟和真实证据收集。'));
    document.querySelector('.section[aria-labelledby="q-title"] .card p')?.replaceChildren(document.createTextNode('这里不会预填成功结果。只有当 Workspace Studio 生成真实蓝图、运行模拟并交接一份决策包后，决策室才会显示事实、未知、影响和 CEO 可执行的选择。'));
    const facts = [...document.querySelectorAll('.fact-item')];
    facts.forEach((item, index) => {
      item.querySelector('.fact-title')?.replaceChildren(document.createTextNode(index === 0 ? '尚无可用于决策的事实证据' : '等待真实运行记录'));
      item.querySelector('.fact-source')?.replaceChildren(document.createTextNode('来源：Evidence / Truth 层 · 尚未生成'));
      const icon = item.querySelector('.fact-icon');
      if (icon) icon.textContent = '—';
    });
    const unknowns = [...document.querySelectorAll('.unknown-item')];
    unknowns.forEach((item, index) => {
      item.querySelector('.fact-title')?.replaceChildren(document.createTextNode(index === 0 ? '当前没有待解释的决策风险' : '真实业务运行后再形成未知项'));
      item.querySelector('.fact-source')?.replaceChildren(document.createTextNode('说明：没有真实决策包，不提前推测风险。'));
    });
    [...document.querySelectorAll('.option-card')].forEach(card => {
      card.setAttribute('aria-disabled', 'true');
      card.querySelector('.option-title')?.replaceChildren(document.createTextNode('等待真实决策包'));
      card.querySelector('.option-desc')?.replaceChildren(document.createTextNode('工作空间完成搭建并提交后，这里才会出现 CEO 可比较的方案。'));
      card.querySelector('.option-tag')?.remove();
    });
    const impactValues = [...document.querySelectorAll('.metric-card .value')];
    const impactDeltas = [...document.querySelectorAll('.metric-card .delta')];
    impactValues.forEach(value => { value.textContent = '—'; });
    impactDeltas.forEach(delta => { delta.textContent = '等待真实记录'; delta.className = 'delta'; });
    [...document.querySelectorAll('.impact-note')].forEach(note => note.textContent = '影响分析会在真实决策包生成后出现。');
    [...document.querySelectorAll('.sim-panel')].forEach(panel => {
      panel.querySelector('.sim-title')?.replaceChildren(document.createTextNode('等待真实运行模拟'));
      panel.querySelector('.sim-outcome')?.replaceChildren(document.createTextNode('当前没有可展示的模拟结果；先从 Workspace Studio 完成一项真实业务空间。'));
      panel.querySelectorAll('.sim-metric .val').forEach(value => { value.textContent = '—'; });
    });
    document.querySelector('.decision-hint')?.replaceChildren(document.createTextNode('当前没有待决策项 · 返回 Workspace Studio 创建真实提交'));
    document.querySelectorAll('#decisionButtons .btn, .curis-option-commit').forEach(button => {
      button.disabled = true;
      button.setAttribute('aria-disabled', 'true');
      button.removeAttribute('onclick');
    });
  }

  function initMeetingRuntime() {
    if (!window.location.pathname.endsWith('meeting.html') || document.querySelector('.curis-meeting-runtime')) return;
    const anchor = document.querySelector('.meeting-anchor');
    if (!anchor) return;
    const state = readState();
    const meetingTitle = state.meetingStarted?.title || '外部合作方周会';
    const seed = [
      { name: 'CEO 助理', avatar: 'C', label: 'fact', text: `本次会议只讨论“${meetingTitle}”的目标、边界和下一步承诺。`, time: '11:00' },
      { name: '增长 AI', avatar: 'G', label: 'fact', text: '过去两条内容的投入产出高于当前基线，追加预算可以覆盖 3 位候选合作方。', time: '11:03' },
      { name: '外部合作方', avatar: 'O', label: 'opinion', text: '建议先锁定一周试运行，再根据首轮数据决定是否延长合作。', time: '11:06' },
      { name: 'CEO 助理', avatar: 'C', label: 'unknown', text: '尚未确认：合作方能否在周三前交付全部素材。需要在会议结束前得到明确答复。', time: '11:08' }
    ];
    let messages = Array.isArray(state.meetingMessages) && state.meetingMessages.length ? state.meetingMessages : seed;
    const labels = { fact: '事实', opinion: '观点', unknown: '未知', recommendation: '建议' };
    const stage = document.createElement('section');
    stage.className = 'curis-meeting-runtime';
    stage.setAttribute('aria-label', '会议工作台');
    stage.innerHTML = `<aside class="curis-meeting-panel agenda"><h2 class="curis-meeting-panel-title">本次会议</h2><div class="curis-meeting-agenda"><div class="curis-meeting-agenda-item is-current">${escapeHtml(state.meetingStarted?.agenda || '确认会议目标与结果')}</div><div class="curis-meeting-agenda-item">确认事实、未知与责任边界</div><div class="curis-meeting-agenda-item">形成可执行的会后承诺</div></div></aside><section class="curis-meeting-panel curis-meeting-chat"><div class="curis-meeting-chat-head"><div><h2 class="curis-meeting-chat-title"></h2><p class="curis-meeting-chat-note">事实、观点和未知会保留在讨论里；只有形成共识后，才进入决议与交接。</p></div><span class="curis-meeting-chat-state">${state.meetingDecision ? '已形成决议' : '进行中'}</span></div><div class="curis-meeting-stream" role="log" aria-live="polite"></div><form class="curis-meeting-composer"><input aria-label="会议发言" placeholder="把你的判断说给会议参与者…" autocomplete="off" /><button type="submit" data-curis-handled="true">发送</button></form></section><aside class="curis-meeting-panel commitments"><h2 class="curis-meeting-panel-title">会后承诺</h2><div class="curis-meeting-commitment"><div class="curis-meeting-commitment-item"><strong>负责人 · 确认下一步产出</strong><span>会议结束后 · 待会议确认</span></div><div class="curis-meeting-commitment-item"><strong>CEO 助理 · 追踪回报</strong><span>按检查点 · 未确认</span></div><div class="curis-meeting-commitment-item"><strong>CEO · 做出最终判断</strong><span>会议结束前 · 待确认</span></div></div><button class="curis-meeting-decision" type="button" data-curis-handled="true">${state.meetingDecision ? '决议已生成' : '结束会议并生成决议'}</button><div class="curis-meeting-summary${state.meetingDecision ? ' is-visible' : ''}"></div></aside>`;
    stage.querySelector('.curis-meeting-chat-title').textContent = meetingTitle;
    document.querySelector('.page-header h1')?.replaceChildren(document.createTextNode(meetingTitle));
    document.querySelector('.page-header .status')?.replaceChildren(document.createTextNode(state.meetingDecision ? '已收束 · 会议记录可追溯' : '进行中 · CEO 与 AI 团队')); 
    anchor.replaceWith(stage);
    const pageStatus = document.querySelector('.page-header .status');
    if (pageStatus) pageStatus.textContent = state.meetingDecision ? '已收束 · 3 位参与者' : '进行中 · 3 位参与者';
    const stream = stage.querySelector('.curis-meeting-stream');
    const summary = stage.querySelector('.curis-meeting-summary');
    const renderMessage = message => {
      const article = document.createElement('article');
      article.className = 'curis-meeting-message';
      const avatar = document.createElement('span');
      avatar.className = 'curis-meeting-avatar';
      avatar.textContent = message.avatar || 'C';
      const bubble = document.createElement('div');
      bubble.className = 'curis-meeting-bubble';
      bubble.innerHTML = `<div class="curis-meeting-meta"><span class="curis-meeting-name"></span><span class="curis-meeting-tag ${message.label || 'opinion'}">${labels[message.label] || '观点'}</span><span>${message.time || '刚刚'}</span></div><p class="curis-meeting-text"></p>`;
      bubble.querySelector('.curis-meeting-name').textContent = message.name || 'CEO';
      bubble.querySelector('.curis-meeting-text').textContent = message.text || '';
      article.append(avatar, bubble);
      stream.appendChild(article);
    };
    messages.forEach(renderMessage);
    const meetingForm = stage.querySelector('form');
    meetingForm.addEventListener('submit', event => {
      event.preventDefault();
      const input = meetingForm.querySelector('input');
      const text = input.value.trim();
      if (!text) return;
      const next = { name: '你', avatar: 'CEO', label: 'opinion', text, time: '刚刚' };
      messages = [...messages, next].slice(-20);
      writeState({ meetingMessages: messages, lastAssistantMessage: `会议里新增了一条 CEO 判断：“${text}”。我会在结束时把它带入决议包。` });
      renderMessage(next);
      input.value = '';
      stream.scrollTop = stream.scrollHeight;
    });
    const decisionButton = stage.querySelector('.curis-meeting-decision');
    const renderDecision = () => {
      const decision = readState().meetingDecision;
      if (!decision) return;
      stage.querySelector('.curis-meeting-chat-state').textContent = '已形成决议';
      decisionButton.textContent = '决议已生成';
      summary.textContent = `${decision.summary} 已生成决议包，CEO 助理会把承诺交给增长 AI 和外部合作方，并在回传后汇报。`;
      summary.classList.add('is-visible');
      stage.querySelectorAll('.curis-meeting-commitment-item').forEach(item => {
        item.classList.add('is-committed');
        const owner = item.querySelector('strong')?.textContent.split('·')[0].trim() || '负责人';
        const span = item.querySelector('span');
        if (span) span.textContent = `已交接 · ${owner} 会在承诺时间回报`;
      });
    };
    decisionButton.addEventListener('click', () => {
      if (readState().meetingDecision) return showToast('会议决议已经生成');
      const meetingFollowup = { id: 'meeting-followup', name: '外部合作方周会 · 回传追踪', business: '公司共享', routeLabel: '会议工作台', schedule: '周三 12:00', owner: 'CEO 助理', task: '追踪最终档期与首轮 ROI 回传；异常时提醒 CEO', estimatedCost: 15, route: 'meeting.html', enabled: true };
      try {
        const schedules = JSON.parse(localStorage.getItem('curis-schedules') || '[]');
        if (!schedules.some(item => item.id === meetingFollowup.id)) localStorage.setItem('curis-schedules', JSON.stringify([...schedules, meetingFollowup].slice(-24)));
      } catch (_) {}
      writeState({
        meetingDecision: { title: '外部合作方周会', summary: '确认一周试运行，预算先按 3 位合作方执行', commitments: ['增长 AI：更新 ROI 模拟', '外部合作方：回传最终档期', 'CEO 助理：生成决议包'], at: new Date().toISOString() },
        lastAssistantMessage: '外部合作方周会已经形成决议。我会把预算、档期和回传承诺交给对应 AI 员工，结果回来后再向你汇报。',
        lastAssistantHandoff: { label: '经营办公室', route: 'operating.html', message: '会议决议已生成' }
      });
      renderDecision();
      showToast('会议已收束，决议包已生成');
    });
    renderDecision();
  }

  function initMeetingFollowups() {
    if (!window.location.pathname.endsWith('meeting.html') || document.querySelector('.curis-meeting-followups')) return;
    const stage = document.querySelector('.curis-meeting-runtime');
    const anchor = stage?.querySelector('.curis-meeting-panel.commitments');
    if (!stage || !anchor) return;
    const items = [
      { id: 'growth-roi', title: '增长 AI · 更新 ROI 模拟', owner: '增长 AI', due: '今天 17:00', task: '更新 ROI 模拟' },
      { id: 'partner-date', title: '外部合作方 · 回传最终档期', owner: '外部合作方', due: '周三 12:00', task: '回传最终档期' },
      { id: 'assistant-brief', title: 'CEO 助理 · 生成决议包', owner: 'CEO 助理', due: '会议结束后', task: '生成决议包' }
    ];
    const followups = document.createElement('section');
    followups.className = 'curis-meeting-followups';
    followups.setAttribute('aria-labelledby', 'curis-meeting-followups-title');
    followups.innerHTML = '<div class="curis-meeting-followups-head"><div><p>决议之后</p><h3 id="curis-meeting-followups-title">会后跟进</h3></div><button type="button" data-meeting-followup-calendar>查看日历</button></div><div data-meeting-followup-list></div>';
    anchor.appendChild(followups);
    const style = document.createElement('style');
    style.textContent = '.curis-meeting-followups{margin-top:14px;padding-top:14px;border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-meeting-followups-head{display:flex;align-items:center;justify-content:space-between;gap:10px}.curis-meeting-followups-head p{margin:0;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-meeting-followups-head h3{margin:3px 0 0;font-size:13px}.curis-meeting-followups-head button{padding:6px 8px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}.curis-meeting-followups-head button:disabled{opacity:.45;cursor:not-allowed}.curis-meeting-followup-row{display:grid;grid-template-columns:minmax(0,1fr) auto auto;align-items:center;gap:8px;padding:10px 0;border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-meeting-followup-row:last-child{border-bottom:0}.curis-meeting-followup-row strong,.curis-meeting-followup-row span,.curis-meeting-followup-row small{display:block}.curis-meeting-followup-row strong{font-size:11px}.curis-meeting-followup-row span,.curis-meeting-followup-row small{margin-top:3px;color:var(--text-secondary,#a4a7af);font-size:10px;line-height:1.35}.curis-meeting-followup-row em{font-style:normal;color:var(--status-warning,#d6c49c);font-size:10px;white-space:nowrap}.curis-meeting-followup-row em.completed{color:var(--status-success,#a8c8b8)}.curis-meeting-followup-row em.blocked{color:var(--status-error,#e4a6a6)}.curis-meeting-followup-row>button{padding:6px 8px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer;white-space:nowrap}.curis-meeting-followups-empty{margin:12px 0 0;color:var(--text-secondary,#a4a7af);font-size:10px;line-height:1.4}@media(max-width:620px){.curis-meeting-followup-row{grid-template-columns:1fr auto}.curis-meeting-followup-row>button{grid-column:1/-1;width:100%}}';
    document.head.appendChild(style);
    const statusLabel = status => ({ completed: '已完成', pending: '待回报', blocked: '有异常' }[status] || '待回报');
    const render = () => {
      const state = readState();
      const decided = Boolean(state.meetingDecision);
      const records = state.meetingFollowups || {};
      const list = followups.querySelector('[data-meeting-followup-list]');
      followups.querySelector('[data-meeting-followup-calendar]').disabled = !decided;
      list.innerHTML = decided
        ? items.map(item => { const record = records[item.id] || {}; const status = record.status || 'pending'; return `<div class="curis-meeting-followup-row"><div><strong>${escapeHtml(item.title)}</strong><span>${escapeHtml(item.due)} · ${escapeHtml(item.task)}</span>${record.note ? `<small>${escapeHtml(record.note)}</small>` : ''}</div><em class="${status}">${statusLabel(status)}</em><button type="button" data-meeting-followup="${item.id}">${status === 'completed' ? '更新回报' : '记录回报'}</button></div>`; }).join('')
        : '<p class="curis-meeting-followups-empty">会议结束并生成决议后，承诺会在这里变成可追踪的回报。</p>';
    };
    const record = id => {
      const item = items.find(candidate => candidate.id === id);
      if (!item) return;
      const current = readState();
      const existing = current.meetingFollowups?.[id] || {};
      openFormDialog({ title: `记录回报 · ${item.title}`, description: '把会后承诺的实际进展写回公司。完成、待回报和异常都要留下原因，CEO 助理才知道是否需要再次提醒。', submitLabel: '保存回报', fields: [{ name: 'status', label: '当前状态', type: 'select', options: ['completed', 'pending', 'blocked'], value: existing.status || 'completed', required: true }, { name: 'note', label: '回报说明', type: 'textarea', value: existing.note || '', placeholder: '例如：已收到最终档期，周三 12:00 可以开始试运行。', required: true }, { name: 'evidence', label: '证据引用', placeholder: '例如：邮件、文件路径、平台链接或客户确认记录' }], onSubmit: values => { const nextRecords = { ...(readState().meetingFollowups || {}), [id]: { ...values, at: new Date().toISOString() } }; const complete = items.every(candidate => nextRecords[candidate.id]?.status === 'completed'); writeState({ meetingFollowups: nextRecords, meetingFollowupsClosedAt: complete ? new Date().toISOString() : null, lastAssistantMessage: `${item.title}已更新为${statusLabel(values.status)}。${complete ? '本次会议承诺已经全部收束。' : '我会继续守住剩余承诺。'}`, lastAssistantHandoff: { label: '会议工作台', route: 'meeting.html', message: '会后回报已更新' } }); render(); showToast(complete ? '会后承诺已全部收束' : '会后回报已保存'); } });
    };
    followups.addEventListener('click', event => { const button = event.target.closest('[data-meeting-followup]'); if (button) record(button.dataset.meetingFollowup); if (event.target.closest('[data-meeting-followup-calendar]') && readState().meetingDecision) window.location.href = 'calendar.html'; });
    render();
    window.addEventListener('curis-state-changed', render);
  }

  function initDecisionDiscussion() {
    if (!window.location.pathname.endsWith('decision-room.html') || document.querySelector('.curis-discussion-section')) return;
    const optionsSection = document.querySelector('.options-list')?.closest('.section');
    if (!optionsSection) return;
    const state = readState();
    const commitmentFlow = Boolean(state.departmentDraft?.name && ['pending', 'pending_revision'].includes(state.departmentCommitment?.status));
    const departmentFlow = Boolean(state.departmentDraft?.name && !/软件开发|研发办公室|Curis v0\.2/.test(state.departmentDraft.name) && (commitmentFlow || state.departmentStatus !== 'active'));
    const discussion = document.createElement('section');
    discussion.className = 'curis-discussion-section';
    discussion.setAttribute('aria-labelledby', 'curis-discussion-title');
    discussion.innerHTML = `
      <div class="curis-discussion-header"><div><h2 id="curis-discussion-title">团队讨论</h2><p>AI 员工先把事实、观点和未知说清楚，再把决定交给 CEO。</p></div><div class="curis-discussion-legend"><span class="curis-chat-label fact">事实</span><span class="curis-chat-label opinion">观点</span><span class="curis-chat-label unknown">未知</span><span class="curis-chat-label recommendation">建议</span></div></div>
      <div class="curis-chat-stream" id="curis-chat-stream">
        <article class="curis-chat-message"><span class="curis-chat-avatar">BE</span><div class="curis-chat-bubble"><div class="curis-chat-meta"><span class="curis-chat-name">业务工程 AI</span><span class="curis-chat-label fact">事实</span><span>14:32</span></div><p class="curis-chat-text">6 类运行模拟全部通过，责任矩阵已经覆盖 Runtime v1.1 的每个阶段。</p></div></article>
        <article class="curis-chat-message"><span class="curis-chat-avatar">CA</span><div class="curis-chat-bubble"><div class="curis-chat-meta"><span class="curis-chat-name">内容 AI</span><span class="curis-chat-label opinion">观点</span><span>14:36</span></div><p class="curis-chat-text">如果今天发布，我可以按新链路完成首周 12 条内容，但品牌安全检查仍需要 CEO 保留人工确认。</p></div></article>
        <article class="curis-chat-message"><span class="curis-chat-avatar">GA</span><div class="curis-chat-bubble"><div class="curis-chat-meta"><span class="curis-chat-name">增长 AI</span><span class="curis-chat-label unknown">未知</span><span>14:39</span></div><p class="curis-chat-text">视频号限流策略还没有真实数据。它不阻止发布，但可能让外部结果延迟 1–2 天回流。</p></div></article>
        <article class="curis-chat-message"><span class="curis-chat-avatar">C</span><div class="curis-chat-bubble"><div class="curis-chat-meta"><span class="curis-chat-name">CEO 助理</span><span class="curis-chat-label recommendation">建议</span><span>14:41</span></div><p class="curis-chat-text">建议批准并保留人工检查点。我会在 8 月 5 日前替你追踪首轮结果和回滚条件。</p></div></article>
      </div>
      <form class="curis-chat-compose" id="curis-chat-compose"><select aria-label="讨论标签"><option value="fact">事实</option><option value="opinion">观点</option><option value="unknown">未知</option><option value="recommendation">建议</option></select><input name="message" autocomplete="off" placeholder="补充一条事实、观点或未知" /><button type="submit" data-curis-handled="true">发送</button></form>`;
    if (departmentFlow) {
      const name = state.departmentDraft.name;
      discussion.querySelector('#curis-discussion-title').textContent = `${name} 办公室讨论`;
      discussion.querySelector('.curis-discussion-header p').textContent = commitmentFlow
        ? 'AI 团队先确认首项责任的结果、能力和验收路径，再把启动决定交给 CEO。'
        : 'AI 团队先确认这间办公室的责任与能力，再把建立决定交给 CEO。';
      const seeded = [...discussion.querySelectorAll('.curis-chat-text')];
      [
        commitmentFlow ? `“${state.departmentCommitment.name}”的责任边界、共享能力和模拟路径已经形成，当前没有未解释的配置缺口。` : `${name} 的责任边界、共享能力和模拟路径已经形成，当前没有未解释的配置缺口。`,
        commitmentFlow ? `启动后可以先执行“${state.departmentCommitment.name}”，再根据真实结果决定是否继续扩充岗位。` : `建立后可以先承接一项明确责任，再根据真实结果决定是否继续扩充岗位。`,
        commitmentFlow ? '未知：首项责任的真实负载和外部结果尚未产生，需要在运行后回收。' : '未知：第一项业务承诺尚未绑定，办公室建立后仍需要 CEO 指定优先结果。',
        commitmentFlow ? `建议批准${name}启动首项责任，并把结果回报交给 CEO 助理持续追踪。` : `建议批准建立${name}，并把第一项责任留在 CEO 工作台上作为下一次经营承接。`
      ].forEach((text, index) => { if (seeded[index]) seeded[index].textContent = text; });
    } else if (!state.businessDecision && !state.workspaceDraft && !state.newBusinessDraft && !state.departmentDraft && !state.departmentCommitment) {
      const seeded = [...discussion.querySelectorAll('.curis-chat-text')];
      [
        '当前没有 Workspace Studio 提交的事实证据。',
        '观点会在真实业务空间运行后，由对应 AI 员工补充。',
        '未知：尚未产生外部结果、成本或 CEO 验收记录。',
        '建议先回到 Workspace Studio 搭建并提交一项真实业务。'
      ].forEach((text, index) => { if (seeded[index]) seeded[index].textContent = text; });
    }
    optionsSection.parentNode.insertBefore(discussion, optionsSection);
    const stream = discussion.querySelector('#curis-chat-stream');
    const saved = readState().decisionDiscussion;
    (Array.isArray(saved) ? saved : []).forEach(item => appendDiscussionMessage(stream, item));
    discussion.querySelector('form').addEventListener('submit', event => {
      event.preventDefault();
      const input = event.currentTarget.elements.message;
      const label = event.currentTarget.elements[0].value;
      const message = input.value.trim();
      if (!message) return;
      const item = { label, message, time: '刚刚' };
      const current = readState().decisionDiscussion;
      writeState({ decisionDiscussion: [...(Array.isArray(current) ? current : []), item].slice(-8) });
      appendDiscussionMessage(stream, item);
      input.value = '';
      showToast('已加入团队讨论，CEO 助理会在决策包中保留这条记录');
    });
  }

  function appendDiscussionMessage(stream, item) {
    const labels = { fact: '事实', opinion: '观点', unknown: '未知', recommendation: '建议' };
    const message = document.createElement('article');
    message.className = 'curis-chat-message user';
    message.innerHTML = `<span class="curis-chat-avatar">CEO</span><div class="curis-chat-bubble"><div class="curis-chat-meta"><span class="curis-chat-name">你</span><span class="curis-chat-label ${item.label}">${labels[item.label] || '记录'}</span><span>${item.time || '刚刚'}</span></div><p class="curis-chat-text"></p></div>`;
    message.querySelector('.curis-chat-text').textContent = item.message;
    stream.appendChild(message);
  }

  function initMeetingLobby() {
    if (!window.location.pathname.endsWith('meeting.html') || document.querySelector('.curis-meeting-runtime') || document.querySelector('.curis-meeting-lobby')) return;
    const state = readState();
    if (state.meetingStarted || state.meetingDecision) return;
    const anchor = document.querySelector('.meeting-anchor');
    if (!anchor) return;
    const lobby = document.createElement('section');
    lobby.className = 'curis-meeting-lobby';
    lobby.innerHTML = state.companyCreatedAt
      ? '<div class="curis-meeting-lobby-copy"><p>会议只在需要共识时出现</p><h2>现在没有进行中的会议</h2><span>CEO 助理会在事实分歧、外部协作或高影响决定需要共同讨论时，替你准备会议。你也可以从一个具体问题开始。</span></div><form class="curis-meeting-lobby-form"><label>会议主题<input name="title" required placeholder="例如：确认下周合作排期与预算边界" /></label><label>希望先讨论什么<textarea name="agenda" required placeholder="写下这场会议必须形成的共识或决定"></textarea></label><label>参与者<input name="participants" placeholder="例如：增长 AI、外部合作方" /></label><div><button type="submit" class="primary">准备会议</button></div></form>'
      : '<div class="curis-meeting-lobby-copy"><p>会议会在公司开始运行后出现</p><h2>先建立公司，再召集团队</h2><span>会议不是空白入口。等公司有 AI 员工、业务责任和需要共识的问题后，CEO 助理才会替你准备会议。</span></div><div class="curis-meeting-lobby-form"><button type="button" class="primary" data-meeting-create-company>开始创建公司 →</button></div>';
    const style = document.createElement('style');
    style.textContent = '.curis-meeting-lobby{display:grid;grid-template-columns:1fr 1.2fr;gap:22px;padding:22px;background:var(--panel,#202226);border:1px solid var(--line,rgba(224,226,242,.12));border-radius:10px}.curis-meeting-lobby-copy p{margin:0 0 7px;color:var(--muted,#a4a7af);font-size:10px}.curis-meeting-lobby-copy h2{margin:0;font-size:18px}.curis-meeting-lobby-copy span{display:block;margin-top:9px;color:var(--muted,#a4a7af);font-size:11px;line-height:1.6}.curis-meeting-lobby-form{display:grid;gap:10px}.curis-meeting-lobby-form label{display:grid;gap:5px;color:var(--muted,#a4a7af);font-size:10px}.curis-meeting-lobby-form input,.curis-meeting-lobby-form textarea{width:100%;padding:9px;color:var(--text,#e2e3e7);background:var(--bg,#191a1d);border:1px solid var(--line,rgba(224,226,242,.12));border-radius:7px;font:inherit;font-size:11px}.curis-meeting-lobby-form textarea{min-height:74px;resize:vertical}.curis-meeting-lobby-form button{padding:8px 11px;color:var(--primaryText,#17181a);background:var(--primary,#d9dbe1);border:1px solid var(--primary,#d9dbe1);border-radius:7px;font:inherit;font-size:11px;font-weight:600;cursor:pointer}@media(max-width:760px){.curis-meeting-lobby{grid-template-columns:1fr}}';
    document.head.appendChild(style);
    anchor.replaceWith(lobby);
    document.querySelector('.page-header h1')?.replaceChildren(document.createTextNode('会议工作台'));
    document.querySelector('.page-header .status')?.replaceChildren(document.createTextNode('没有进行中的会议'));
    lobby.querySelector('[data-meeting-create-company]')?.addEventListener('click', () => { writeState({ lastAssistantMessage: '从第一间办公室开始创建公司。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '开始创建公司' } }); window.location.href = 'founding-flow.html'; });
    if (!state.companyCreatedAt) return;
    lobby.querySelector('form').addEventListener('submit', event => {
      event.preventDefault();
      const data = new FormData(event.currentTarget);
      const title = String(data.get('title') || '').trim();
      const agenda = String(data.get('agenda') || '').trim();
      if (!title || !agenda) return;
      writeState({ meetingStarted: { title, agenda, participants: String(data.get('participants') || '').trim(), at: new Date().toISOString() }, lastAssistantMessage: `会议“${title}”已准备。我会先把事实、未知和责任边界整理好。`, lastAssistantHandoff: { label: '会议工作台', route: 'meeting.html', message: '会议已准备' } });
      window.location.reload();
    });
  }

  // ── CEO-facing runtime controls shared by business offices
  function initExtendedNav() {
    const sidebar = document.querySelector('aside.sidebar');
    if (!sidebar || sidebar.dataset.curisCanonicalNav === 'true') return;
    sidebar.dataset.curisCanonicalNav = 'true';
    const brand = sidebar.querySelector('.brand, .sidebar-brand');
    if (brand) {
      brand.className = 'brand';
      brand.innerHTML = '<span class="brand-mark">C</span><span>Curis</span>';
    }
    sidebar.querySelector('.assistant-mini')?.remove();
    const page = window.location.pathname.split('/').pop() || 'ceo-desk.html';
    const primary = [
      ['CEO 工作台', 'ceo-desk.html', '◆'],
      ['经营', 'operating.html', '◎'],
      ['业务', 'business.html', '◇'],
      ['AI 团队', 'ai-organization.html', '□'],
      ['工作空间', 'workspace-portal.html', '▣']
    ];
    const tools = [
      ['会议工作台', 'meeting.html', '◌'],
      ['决策室', 'decision-room.html', '◇']
    ];
    const resources = [
      ['成果库', 'assets.html', '▤'],
      ['知识库', 'knowledge.html', '⌘'],
      ['财务', 'finance.html', '¥'],
      ['日历', 'calendar.html', '◷']
    ];
    const runtimePages = ['workspace-runtime-software.html', 'workspace-runtime-xhs.html', 'workspace-runtime-shortvideo.html', 'workspace-runtime-department.html'];
    const offices = [
      ['研发办公室', 'workspace-runtime-software.html', '◉'],
      ['小红书运营办公室', 'workspace-runtime-xhs.html', '◌'],
      ['抖音 / TikTok 运营办公室', 'workspace-runtime-shortvideo.html', '◌']
    ];
    if (page === 'workspace-runtime-department.html') offices.push(['部门办公室', 'workspace-runtime-department.html', '◉']);
    const state = readState();
    const activeOfficeHrefs = new Set();
    if (state.companyCreatedAt) {
      const firstBusiness = String(state.firstBusiness || state.newBusinessDraft?.name || '');
      if (/软件|Curis|研发/.test(firstBusiness) || state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html')) activeOfficeHrefs.add('workspace-runtime-software.html');
      if (/小红书/.test(firstBusiness) || state.latestXhsFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-xhs.html')) activeOfficeHrefs.add('workspace-runtime-xhs.html');
      if (/抖音|TikTok|短视频/.test(firstBusiness) || state.latestExternalFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-shortvideo.html')) activeOfficeHrefs.add('workspace-runtime-shortvideo.html');
    }
    const activeOffices = offices.filter(item => activeOfficeHrefs.has(item[1]) || item[1] === page || item[1] === 'workspace-runtime-department.html' && state.departmentStatus === 'active');

    const textOf = node => (node?.textContent || '').replace(/\s+/g, ' ').trim();
    const oldItems = [...sidebar.querySelectorAll('.nav-item')];
    const badgeFor = label => {
      const state = readState();
      if (label === 'CEO 工作台') {
        const pending = (state.calendarEvents || []).filter(item => ['queued', 'waiting_ceo', 'acknowledged', 'failed'].includes(item.status)).length + (state.lastConnector?.status === 'pending' ? 1 : 0);
        return pending ? String(pending) : '';
      }
      if (label === '工作空间' && state.companyCreatedAt) {
        const offices = new Set();
        if (/软件|Curis|研发/.test(state.firstBusiness || '') || state.softwareAcceptance) offices.add('software');
        if (/小红书/.test(state.firstBusiness || '') || state.latestXhsFeedback) offices.add('xhs');
        if (/抖音|TikTok|短视频/.test(state.firstBusiness || '') || state.latestExternalFeedback) offices.add('short');
        return offices.size > 1 ? String(offices.size) : '';
      }
      return '';
    };
    const sidebarFoot = sidebar.querySelector('.sidebar-foot')?.cloneNode(true);
    const currentOfficeNav = [...sidebar.querySelectorAll('a[href]')].filter(link => runtimePages.includes(link.getAttribute('href')));
    const hasDepartmentOffice = page === 'workspace-runtime-department.html' || currentOfficeNav.some(link => link.getAttribute('href') === 'workspace-runtime-department.html');
    const officeItems = hasDepartmentOffice ? activeOffices : (runtimePages.includes(page) ? activeOffices.filter(item => item[1] !== 'workspace-runtime-department.html') : []);

    sidebar.querySelectorAll('.nav-section,.nav-list,.nav-group,.nav,.nav-footer,.sidebar-footer,.nav-label').forEach(node => node.remove());

    const makeSection = (label, items, sectionClass = '') => {
      const section = document.createElement('section');
      section.className = `curis-nav-section ${sectionClass}`.trim();
      section.style.cssText = 'display:grid;gap:3px;';
      if (label) {
        const heading = document.createElement('p');
        heading.className = 'nav-label';
        heading.textContent = label;
        heading.style.cssText = 'margin:14px 0 3px;padding:0 10px;';
        section.appendChild(heading);
      }
      const nav = document.createElement('nav');
      nav.className = 'nav curis-canonical-nav-group';
      nav.setAttribute('aria-label', label || '主导航');
      nav.style.cssText = 'display:grid;gap:2px;';
      const links = [];
      items.forEach(([name, href, icon]) => {
        const link = document.createElement('a');
        link.className = 'nav-item';
        link.href = href;
        link.dataset.curisCanonicalLink = 'true';
        const isWorkspaceStudio = page === 'workspace-studio.html' && href === 'workspace-portal.html';
        link.setAttribute('aria-current', href === page || isWorkspaceStudio ? 'page' : 'false');
        if (href === page || isWorkspaceStudio) link.classList.add('active');
        const badge = badgeFor(name);
        link.innerHTML = `<span class="nav-icon icon">${icon}</span><span>${name}</span>${badge ? `<span class="nav-badge">${badge}</span>` : ''}`;
        links.push(link);
      });
      links.forEach(link => nav.appendChild(link));
      section.appendChild(nav);
      return section;
    };

    const main = document.createElement('div');
    main.className = 'curis-canonical-sidebar-main';
    main.style.cssText = 'display:flex;flex-direction:column;gap:2px;flex:1;min-height:0;overflow:auto;';
    main.appendChild(makeSection('公司', primary));
    main.appendChild(makeSection('经营工具', tools, 'curis-tool-nav'));
    if (officeItems.length) main.appendChild(makeSection('办公室', officeItems, 'curis-office-nav'));
    main.appendChild(makeSection('公司资源', resources, 'curis-resource-nav'));
    sidebar.appendChild(main);

    const footer = document.createElement('div');
    footer.className = 'nav-footer curis-canonical-footer';
    footer.style.cssText = 'margin-top:auto;display:grid;gap:2px;padding-top:14px;';
    footer.innerHTML = '<a class="nav-item" href="#"><span class="nav-icon icon">○</span><span>设置</span></a><a class="nav-item" href="#"><span class="nav-icon icon">?</span><span>帮助与反馈</span></a>';
    sidebar.appendChild(footer);
    if (sidebarFoot) sidebar.appendChild(sidebarFoot);
  }

  function initNeutralShell() {
    const page = window.location.pathname.split('/').pop() || '';
    if (['founding-flow.html', 'ceo-desk.html', 'operating.html', 'business.html', 'ai-organization.html', 'workspace-portal.html', 'workspace-studio.html', 'workspace-runtime-department.html', 'workspace-runtime-software.html', 'workspace-runtime-xhs.html', 'workspace-runtime-shortvideo.html', 'meeting.html', 'decision-room.html', 'assets.html', 'knowledge.html', 'finance.html', 'calendar.html'].includes(page)) {
      document.body.dataset.curisNeutral = 'true';
    }
  }

  function initFocusModeShell() {
    const page = window.location.pathname.split('/').pop() || '';
    const modes = {
      'founding-flow.html': { mode: 'founding', title: '创建公司 · 第一间办公室', exits: [['a[href="ceo-desk.html"]', '进入 CEO 工作台']] },
      'decision-room.html': { mode: 'decision', title: '决策室 · CEO 决策', exits: [['a[href="workspace-studio.html"]', '返回 Workspace Studio'], ['button[aria-label="关闭决策室"]', '关闭决策室']] }
    };
    const config = modes[page];
    if (!config) return;
    document.documentElement.dataset.curisFocusMode = config.mode;
    document.body.dataset.curisFocusMode = config.mode;
    document.body.dataset.curisFocusTitle = config.title;
    config.exits.forEach(([selector, label]) => {
      document.querySelectorAll(selector).forEach(exit => {
        exit.dataset.curisFocusExit = 'true';
        exit.setAttribute('aria-label', label);
      });
    });
  }

  function initWorkspaceOfficeNav() {
    const page = window.location.pathname.split('/').pop() || '';
    const runtimePages = ['workspace-runtime-software.html', 'workspace-runtime-xhs.html', 'workspace-runtime-shortvideo.html'];
    if (!runtimePages.includes(page)) return;
    const sidebar = document.querySelector('aside.sidebar');
    if (!sidebar || sidebar.querySelector('.curis-office-nav')) return;
    const officeItemsAll = [
      ['研发办公室', 'workspace-runtime-software.html', '◉'],
      ['小红书运营办公室', 'workspace-runtime-xhs.html', '◌'],
      ['抖音 / TikTok 运营办公室', 'workspace-runtime-shortvideo.html', '◌']
    ];
    const state = readState();
    const activeOfficeHrefs = new Set();
    if (state.companyCreatedAt) {
      const firstBusiness = String(state.firstBusiness || state.newBusinessDraft?.name || '');
      if (/软件|Curis|研发/.test(firstBusiness) || state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html')) activeOfficeHrefs.add('workspace-runtime-software.html');
      if (/小红书/.test(firstBusiness) || state.latestXhsFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-xhs.html')) activeOfficeHrefs.add('workspace-runtime-xhs.html');
      if (/抖音|TikTok|短视频/.test(firstBusiness) || state.latestExternalFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-shortvideo.html')) activeOfficeHrefs.add('workspace-runtime-shortvideo.html');
    }
    const officeItems = officeItemsAll.filter(item => activeOfficeHrefs.has(item[1]) || item[1] === page);
    const existingLabel = [...sidebar.querySelectorAll('.nav-label')].find(node => node.textContent.trim() === '办公室');
    const existingNav = existingLabel?.nextElementSibling?.matches('.nav') ? existingLabel.nextElementSibling : null;
    const label = existingLabel || document.createElement('p');
    label.className = 'nav-label curis-office-nav-label';
    label.textContent = '办公室';
    label.style.marginTop = '24px';
    const nav = existingNav || document.createElement('nav');
    nav.className = 'nav curis-office-nav';
    nav.innerHTML = officeItems.map(([name, href, icon]) => `<a class="nav-item" href="${href}"><span class="nav-icon">${icon}</span><span>${name}</span></a>`).join('');
    if (!existingLabel) sidebar.append(label, nav);
    else nav.classList.add('curis-office-nav');
    nav.querySelectorAll('a').forEach(link => link.classList.toggle('active', link.getAttribute('href') === page));
  }

  function initCapabilityRuntime() {
    const roots = document.querySelectorAll('[data-capability-runtime]');
    if (!roots.length || document.getElementById('capability-drawer')) return;
    const state = readState();
    const contextKey = window.location.pathname.split('/').pop() || 'company';
    const defaultsByPage = {
      'workspace-runtime-software.html': { model: 'GPT-5', agent: '研发 AI', skills: ['结构化输出', '复盘归因'], tools: ['文件库', '浏览器'], connector: '手动录入', knowledgeScope: '当前业务空间' },
      'workspace-runtime-xhs.html': { model: 'GPT-5', agent: '内容制作 AI', skills: ['研究拆解', '内容生成', '复盘归因'], tools: ['浏览器', '文件库', '平台数据连接器'], connector: '需要授权', knowledgeScope: '当前业务空间' },
      'workspace-runtime-shortvideo.html': { model: 'GPT-5', agent: '视频 AI', skills: ['内容生成', '复盘归因'], tools: ['文件库', '平台数据连接器'], connector: '需要授权', knowledgeScope: '当前业务空间' },
      'workspace-runtime-department.html': { model: 'GPT-5', agent: '业务工程 AI', skills: ['结构化输出', '复盘归因'], tools: ['文件库', '浏览器'], connector: '手动录入', knowledgeScope: '当前业务空间' }
    };
    const defaultCapability = defaultsByPage[contextKey] || { model: 'GPT-5', agent: '业务分析 AI', skills: ['研究拆解', '结构化输出'], tools: ['浏览器', '文件库'], connector: '手动录入', knowledgeScope: '当前业务空间' };
    let activeContextKey = contextKey;
    let activeSaved = state.capabilityRuntimeByContext?.[contextKey] || state.capabilityRuntime || defaultCapability;
    let activeSavedKnowledge = state.knowledgeContextByContext?.[contextKey] || activeSaved.knowledgeContext || [];
    const drawer = document.createElement('aside');
    drawer.id = 'capability-drawer';
    drawer.className = 'curis-capability-drawer';
    drawer.setAttribute('aria-label', 'AI 能力配置');
    drawer.innerHTML = `<div class="curis-capability-head"><div><strong>AI 能力编排</strong><p>切换只影响当前步骤，输入、上下文和已有成果会保留。</p></div><button type="button" data-capability-close aria-label="关闭">×</button></div><div class="curis-capability-body"><label>模型<select data-capability-model><option>GPT-5</option><option>GPT-5 mini</option><option>Claude Sonnet</option><option>本地模型</option></select></label><label>负责人 AI<select data-capability-agent><option>业务分析 AI</option><option>策略分析 AI</option><option>增长 AI</option><option>内容制作 AI</option><option>内容 AI</option><option>发布 AI</option><option>视频 AI</option><option>工程实现 AI</option><option>研发 AI</option><option>QA AI</option><option>产品 AI</option><option>数据回收 AI</option><option>CEO 助理</option></select></label><div class="curis-capability-section"><span>技能</span><div class="curis-chip-row"><button type="button" data-capability-skill="研究拆解">研究拆解</button><button type="button" data-capability-skill="结构化输出">结构化输出</button><button type="button" data-capability-skill="内容生成">内容生成</button><button type="button" data-capability-skill="复盘归因">复盘归因</button></div></div><div class="curis-capability-section"><span>工具 / MCP</span><div class="curis-chip-row"><button type="button" data-capability-tool="浏览器">浏览器</button><button type="button" data-capability-tool="文件库">文件库</button><button type="button" data-capability-tool="平台数据连接器">平台数据连接器</button></div></div><div class="curis-connector-row"><div><strong>结果回传</strong><small data-capability-connector-note>连接器授权失败时，可由 CEO 手动补录</small></div><select data-capability-connector><option>已连接 · API</option><option>需要授权</option><option>手动录入</option></select></div><div class="curis-knowledge-scope"><div><strong>知识范围</strong><small>决定本步骤可检索与引用的内部、外部资料</small></div><div><select data-capability-knowledge><option>当前业务空间</option><option>公司知识库</option><option>全局知识库</option></select><button type="button" data-capability-knowledge-open>管理引用范围</button></div><p class="curis-capability-context" data-capability-knowledge-context></p></div><div class="curis-workflow-row"><div><strong>可复用工作流</strong><small data-capability-workflow-note>保存后可带回当前步骤</small></div><div><select data-capability-workflow-select><option value="">选择工作流</option></select><button type="button" data-capability-workflow-load>载入</button></div></div><div class="curis-cost-row"><span>本步骤预估成本</span><strong data-capability-cost>¥0.18</strong></div><div class="curis-capability-actions"><button type="button" data-capability-save class="primary">应用到下一步</button><button type="button" data-capability-workflow>保存为工作流</button></div></div>`;
    document.body.appendChild(drawer);
    const style = document.createElement('style');
    style.id = 'curis-capability-style';
    style.textContent = `.curis-capability-drawer{position:fixed;right:20px;top:20px;bottom:20px;width:min(390px,calc(100vw - 40px));z-index:2200;display:none;background:var(--bg-base-secondary,#202226);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:14px;box-shadow:0 18px 60px rgba(0,0,0,.4);color:var(--text-default,#e2e3e7)}.curis-capability-drawer.is-open{display:block}.curis-capability-head{display:flex;justify-content:space-between;gap:12px;padding:18px;border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-capability-head strong{font-size:14px}.curis-capability-head p{margin:5px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.5}.curis-capability-head button{border:0;background:transparent;color:var(--text-secondary,#a4a7af);font-size:22px}.curis-capability-body{display:grid;gap:14px;padding:18px;overflow:auto;height:calc(100% - 78px)}.curis-capability-body label{display:grid;gap:6px;color:var(--text-secondary,#a4a7af);font-size:11px}.curis-capability-body select{padding:9px;color:var(--text-default,#e2e3e7);background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit}.curis-capability-section{display:grid;gap:8px}.curis-capability-section>span{color:var(--text-secondary,#a4a7af);font-size:11px}.curis-chip-row{display:flex;flex-wrap:wrap;gap:6px}.curis-chip-row button{padding:6px 8px;color:var(--text-secondary,#a4a7af);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:999px;font-size:10px}.curis-chip-row button.is-selected{color:var(--text-default-hover,#f4f5f7);border-color:var(--status-primary,#aab6ff);background:var(--status-primary-surface,rgba(126,137,190,.14))}.curis-connector-row,.curis-cost-row,.curis-knowledge-scope,.curis-workflow-row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px;background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px}.curis-connector-row strong,.curis-knowledge-scope strong,.curis-workflow-row strong{display:block;font-size:11px}.curis-connector-row small,.curis-knowledge-scope small,.curis-workflow-row small{display:block;margin-top:4px;color:var(--text-tertiary,#777c86);font-size:10px}.curis-connector-row select,.curis-knowledge-scope select,.curis-workflow-row select{max-width:140px}.curis-knowledge-scope{position:relative;flex-wrap:wrap}.curis-knowledge-scope>div:last-child,.curis-workflow-row>div:last-child{display:flex;align-items:center;gap:6px}.curis-knowledge-open,.curis-workflow-row button{padding:7px 9px;color:var(--text-secondary,#a4a7af);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font-size:10px}.curis-capability-context{width:100%;margin:0;color:var(--text-tertiary,#777c86);font-size:10px;line-height:1.4}.curis-cost-row span{color:var(--text-secondary,#a4a7af);font-size:11px}.curis-cost-row strong{font-size:15px}.curis-capability-actions{display:flex;gap:8px}.curis-capability-actions button{flex:1;padding:9px;border-radius:7px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));font:inherit;font-size:11px}.curis-capability-actions button.primary{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}`;
    document.head.appendChild(style);
    const renderKnowledgeContext = () => {
      const current = readState().knowledgeContextByContext?.[activeContextKey] || activeSavedKnowledge;
      const target = drawer.querySelector('[data-capability-knowledge-context]');
      if (target) target.textContent = current.length ? `已引用 ${current.length} 份资料：${current.slice(-2).join('、')}` : '尚未指定资料；默认检索当前业务空间。';
    };
    const renderVisibleSummary = (runtime, root) => {
      const anchor = root?.closest('.person,.capability,.panel,.card') || root;
      if (!anchor || !runtime) return;
      const cost = ({ 'GPT-5': '¥0.18', 'GPT-5 mini': '¥0.06', 'Claude Sonnet': '¥0.14', '本地模型': '¥0.02' }[runtime.model] || '按调用计费');
      const skills = (runtime.skills || []).join(' / ') || '按当前步骤配置';
      const tools = (runtime.tools || []).join(' / ') || '按需启用';
      const heading = [...anchor.querySelectorAll('strong,.panel-title,h2,h3')].find(node => /当前.*能力组合|配置当前步骤|调整能力与成本/.test(node.textContent || ''));
      if (heading) heading.textContent = /当前.*能力组合/.test(heading.textContent || '') ? `当前能力组合：${runtime.model} · ${runtime.agent}` : `当前步骤能力：${runtime.model} · ${runtime.agent}`;
      const detail = [...anchor.querySelectorAll('span,div')].find(node => node !== heading && /能力：|Skills：|点击切换模型|能力可切换/.test(node.textContent || '') && node.children.length === 0);
      if (detail) detail.textContent = `能力：${skills} · 工具：${tools} · 结果回传：${runtime.connector || '手动录入'} · 预估 ${cost}`;
    };
    const fill = () => { drawer.querySelector('[data-capability-model]').value = activeSaved.model; drawer.querySelector('[data-capability-agent]').value = activeSaved.agent; drawer.querySelector('[data-capability-connector]').value = activeSaved.connector; drawer.querySelector('[data-capability-knowledge]').value = activeSaved.knowledgeScope || '当前业务空间'; drawer.querySelectorAll('[data-capability-skill],[data-capability-tool]').forEach(btn => btn.classList.toggle('is-selected', [...(activeSaved.skills || []), ...(activeSaved.tools || [])].includes(btn.dataset.capabilitySkill || btn.dataset.capabilityTool))); renderKnowledgeContext(); };
    const renderWorkflowOptions = () => {
      const select = drawer.querySelector('[data-capability-workflow-select]');
      const note = drawer.querySelector('[data-capability-workflow-note]');
      if (!select) return;
      const workflows = JSON.parse(localStorage.getItem('curis-workflows') || '[]');
      select.innerHTML = '<option value="">选择工作流</option>' + workflows.slice(-12).reverse().map(workflow => `<option value="${workflow.id}">${escapeHtml(workflow.name || '未命名工作流')}</option>`).join('');
      if (note) note.textContent = workflows.length ? `已保存 ${workflows.length} 条 · 载入后仍需应用` : '还没有已保存工作流';
    };
    fill();
    renderVisibleSummary(activeSaved, roots[0]);
    renderWorkflowOptions();
    const updateCapabilityCost = () => { drawer.querySelector('[data-capability-cost]').textContent = ({ 'GPT-5': '¥0.18', 'GPT-5 mini': '¥0.06', 'Claude Sonnet': '¥0.14', '本地模型': '¥0.02' }[drawer.querySelector('[data-capability-model]').value] || '按调用计费'); };
    updateCapabilityCost();
    drawer.querySelector('[data-capability-model]').addEventListener('change', updateCapabilityCost);
    const connectorSelect = drawer.querySelector('[data-capability-connector]');
    const renderConnectorHint = () => {
      const note = drawer.querySelector('[data-capability-connector-note]');
      if (!note) return;
      note.textContent = connectorSelect.value === '需要授权'
        ? '仅登记授权需求；完成授权前不会读取平台数据。'
        : connectorSelect.value === '手动录入'
          ? '没有授权也能运行；结果节点会等待 CEO 手动补录。'
          : '已连接 · 运行失败时仍保留手动补录窗口。';
    };
    connectorSelect.addEventListener('change', renderConnectorHint);
    renderConnectorHint();
    const open = root => {
      const anchor = root?.closest('.person,.capability,.panel,.card') || root;
      const label = root?.dataset.capabilityLabel || anchor?.querySelector('strong,h2,h3')?.textContent?.trim() || '当前步骤';
      if (root && !root.dataset.capabilityLabel) root.dataset.capabilityLabel = label;
      const stepKey = root?.dataset.capabilityContext || `step-${Math.max(1, [...roots].indexOf(root) + 1)}`;
      if (root) root.dataset.capabilityContext = stepKey;
      activeContextKey = `${contextKey}::${stepKey}`;
      const latest = readState();
      activeSaved = latest.capabilityRuntimeByContext?.[activeContextKey] || latest.capabilityRuntimeByContext?.[contextKey] || latest.capabilityRuntime || defaultCapability;
      activeSavedKnowledge = latest.knowledgeContextByContext?.[activeContextKey] || activeSaved.knowledgeContext || [];
      drawer.querySelector('.curis-capability-head strong').textContent = `AI 能力编排 · ${label}`;
      fill();
      renderVisibleSummary(activeSaved, root);
      updateCapabilityCost();
      renderConnectorHint();
      document.getElementById('curis-companion')?.classList.remove('is-open');
      drawer.classList.add('is-open');
    };
    roots.forEach(root => root.addEventListener('click', () => open(root)));
    if (state.capabilityFocusRoute === contextKey) {
      open(roots[0]);
      writeState({ capabilityFocusRoute: '' });
    }
    drawer.addEventListener('click', event => {
      const button = event.target.closest('button');
      if (!button) return;
      if (button.dataset.capabilityClose !== undefined) drawer.classList.remove('is-open');
      if (button.dataset.capabilitySkill || button.dataset.capabilityTool) button.classList.toggle('is-selected');
      if (button.dataset.capabilityWorkflowLoad !== undefined) {
        const id = drawer.querySelector('[data-capability-workflow-select]')?.value;
        const workflow = JSON.parse(localStorage.getItem('curis-workflows') || '[]').find(item => String(item.id) === String(id));
        if (!workflow?.capability) return showToast('先选择一条已保存工作流');
        activeSaved = workflow.capability;
        activeSavedKnowledge = workflow.capability.knowledgeContext || [];
        fill();
        updateCapabilityCost();
        renderConnectorHint();
        showToast(`已载入：${workflow.name || '已保存工作流'}，确认后应用到当前步骤`);
      }
      if (button.dataset.capabilityKnowledgeOpen !== undefined) { writeState({ knowledgeReturnRoute: contextKey, knowledgeReturnContext: activeContextKey, lastAssistantMessage: '我把当前步骤带到知识库，引用后会原样带回这个工作流。' }); drawer.classList.remove('is-open'); window.location.href = 'knowledge.html'; return; }
      if (button.dataset.capabilitySave !== undefined) { const latest = readState(); const currentContext = latest.knowledgeContextByContext?.[activeContextKey] || activeSavedKnowledge; const next = { model: drawer.querySelector('[data-capability-model]').value, agent: drawer.querySelector('[data-capability-agent]').value, connector: drawer.querySelector('[data-capability-connector]').value, knowledgeScope: drawer.querySelector('[data-capability-knowledge]').value, knowledgeContext: currentContext, skills: [...drawer.querySelectorAll('[data-capability-skill].is-selected')].map(x => x.dataset.capabilitySkill), tools: [...drawer.querySelectorAll('[data-capability-tool].is-selected')].map(x => x.dataset.capabilityTool) }; const capabilityRuntimeByContext = { ...(latest.capabilityRuntimeByContext || {}), [activeContextKey]: next }; const connectorPending = next.connector === '需要授权'; writeState({ capabilityRuntime: next, capabilityRuntimeByContext, capabilityHistory: [...(latest.capabilityHistory || []), { ...next, contextKey: activeContextKey, at: new Date().toISOString() }].slice(-12), ...(connectorPending ? { lastConnector: { status: 'pending', contextKey: activeContextKey, at: new Date().toISOString() } } : {}), lastAssistantMessage: connectorPending ? `当前步骤已切换能力，但连接器仍待授权；我会保留手动录入窗口。` : `当前步骤已切换为 ${next.model} · ${next.agent}，原有上下文和成果已保留。` }); const cost = { 'GPT-5': '¥0.18', 'GPT-5 mini': '¥0.06', 'Claude Sonnet': '¥0.14', '本地模型': '¥0.02' }[next.model] || '按调用计费'; drawer.querySelector('[data-capability-cost]').textContent = cost; activeSaved = next; activeSavedKnowledge = currentContext; renderVisibleSummary(next, roots.find(item => item.dataset.capabilityContext === activeContextKey.split('::').pop()) || roots[0]); drawer.classList.remove('is-open'); showToast(connectorPending ? '能力已保存；等待连接器授权后再运行' : `已切换为 ${next.model} · ${next.agent}，当前步骤上下文已保留`); }
      if (button.dataset.capabilityWorkflow !== undefined) { const workflows = JSON.parse(localStorage.getItem('curis-workflows') || '[]'); workflows.push({ id: Date.now(), name: `${document.title.split('·')[0].trim()} · 当前流程`, contextKey: activeContextKey, capability: readState().capabilityRuntimeByContext?.[activeContextKey] || activeSaved, savedAt: new Date().toISOString() }); localStorage.setItem('curis-workflows', JSON.stringify(workflows.slice(-12))); renderWorkflowOptions(); showToast('已保存为可复用工作流'); }
    });
  }

  function openFormDialog({ title, description, fields, submitLabel = '保存', onSubmit }) {
    let dialog = document.getElementById('curis-form-dialog');
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.id = 'curis-form-dialog';
      dialog.innerHTML = '<form method="dialog" class="curis-form-dialog-form"><div class="curis-form-dialog-head"><div><strong data-dialog-title></strong><p data-dialog-description></p></div><button type="button" data-dialog-close aria-label="关闭">×</button></div><div class="curis-form-dialog-fields" data-dialog-fields></div><div class="curis-form-dialog-actions"><button type="button" data-dialog-cancel>取消</button><button type="submit" class="primary" data-dialog-submit></button></div></form>';
      const style = document.createElement('style');
      style.id = 'curis-form-dialog-style';
      style.textContent = '#curis-form-dialog{width:min(460px,calc(100vw - 32px));padding:0;color:var(--text-default,#e2e3e7);background:var(--bg-base-secondary,#202226);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:14px;box-shadow:0 20px 70px rgba(0,0,0,.42)}#curis-form-dialog::backdrop{background:rgba(0,0,0,.48)}.curis-form-dialog-form{margin:0}.curis-form-dialog-head{display:flex;justify-content:space-between;gap:16px;padding:18px;border-bottom:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-form-dialog-head strong{font-size:14px}.curis-form-dialog-head p{margin:5px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.45}.curis-form-dialog-head button{border:0;background:transparent;color:var(--text-secondary,#a4a7af);font-size:20px;cursor:pointer}.curis-form-dialog-fields{display:grid;gap:12px;padding:18px}.curis-form-dialog-field{display:grid;gap:6px}.curis-form-dialog-field label{color:var(--text-secondary,#a4a7af);font-size:11px}.curis-form-dialog-field input,.curis-form-dialog-field textarea,.curis-form-dialog-field select{width:100%;padding:9px 10px;color:var(--text-default,#e2e3e7);background:var(--bg-base-default,#191a1d);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px}.curis-form-dialog-field select[multiple]{min-height:96px}.curis-form-dialog-field textarea{min-height:72px;resize:vertical}.curis-form-dialog-actions{display:flex;justify-content:flex-end;gap:8px;padding:0 18px 18px}.curis-form-dialog-actions button{padding:8px 11px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:7px;font:inherit;font-size:11px;cursor:pointer}.curis-form-dialog-actions button.primary{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}';
      document.head.appendChild(style);
      document.body.appendChild(dialog);
      dialog.querySelector('[data-dialog-close]').addEventListener('click', () => dialog.close());
      dialog.querySelector('[data-dialog-cancel]').addEventListener('click', () => dialog.close());
      dialog.querySelector('form').addEventListener('submit', event => {
        event.preventDefault();
        const values = Object.fromEntries(new FormData(event.currentTarget).entries());
        event.currentTarget.querySelectorAll('select[multiple]').forEach(select => { values[select.name] = [...select.selectedOptions].map(option => option.value); });
        dialog.close();
        dialog._onSubmit?.(values);
      });
    }
    dialog.querySelector('[data-dialog-title]').textContent = title;
    dialog.setAttribute('aria-label', title);
    dialog.querySelector('[data-dialog-description]').textContent = description || '';
    dialog.querySelector('[data-dialog-submit]').textContent = submitLabel;
    const fieldsRoot = dialog.querySelector('[data-dialog-fields]');
    fieldsRoot.innerHTML = fields.map(field => {
      const isSelect = field.type === 'select' || field.type === 'multiselect';
      const tag = field.type === 'textarea' ? 'textarea' : isSelect ? 'select' : 'input';
      const value = field.value || (field.type === 'multiselect' ? [] : '');
      const selectedValues = Array.isArray(value) ? value.map(String) : [String(value)];
      const options = isSelect ? (field.options || []).map(option => { const optionValue = typeof option === 'object' ? option.value : option; const optionLabel = typeof option === 'object' ? option.label : option; return `<option value="${escapeHtml(optionValue)}"${selectedValues.includes(String(optionValue)) ? ' selected' : ''}>${escapeHtml(optionLabel)}</option>`; }).join('') : '';
      const content = field.type === 'textarea' ? escapeHtml(value) : options;
      const valueAttribute = field.type === 'textarea' || isSelect ? '' : `value="${escapeHtml(value)}"`;
      const multipleAttribute = field.type === 'multiselect' ? ' multiple size="4"' : '';
      return `<div class="curis-form-dialog-field"><label for="curis-dialog-${escapeHtml(field.name)}">${escapeHtml(field.label)}</label><${tag} id="curis-dialog-${escapeHtml(field.name)}" name="${escapeHtml(field.name)}" ${field.type && !['textarea', 'select', 'multiselect'].includes(field.type) ? `type="${escapeHtml(field.type)}"` : ''} ${valueAttribute}${multipleAttribute} placeholder="${escapeHtml(field.placeholder || '')}" ${field.required ? 'required' : ''}>${content}</${tag}></div>`;
    }).join('');
    dialog._onSubmit = onSubmit;
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '');
    fieldsRoot.querySelector('input,textarea,select')?.focus();
  }

  function initRuntimeActions() {
    document.querySelectorAll('[data-runtime-action]').forEach(button => button.addEventListener('click', () => {
      const action = button.dataset.runtimeAction;
      if (action === 'manual-result') openFormDialog({ title: '记录外部结果', description: '把平台数据或客户回报带回本周期；没有授权时也可以先手动记录。', submitLabel: '保存结果', fields: [{ name: 'summary', label: '结果摘要', type: 'textarea', placeholder: '例如：阅读 12000，收藏 380，成交额 ¥420', required: true }, { name: 'source', label: '来源', placeholder: '例如：平台后台截图 / 客户验收', required: true }], onSubmit: values => { writeState({ lastExternalResult: { value: values.summary, source: values.source, at: new Date().toISOString() } }); showToast('外部结果已回流，CEO 助理会准备复盘'); } });
      else if (action === 'xhs-review') { const row = button.closest('.content-row'); const title = row?.querySelector('strong')?.textContent.trim() || '当前内容'; openFormDialog({ title: `内容审阅 · ${title}`, description: '发布前由 CEO 确认品牌语气和敏感表达；决定会保留版本与反馈，退回后内容 AI 按反馈重新制作。', submitLabel: '保存审阅结果', fields: [{ name: 'decision', label: 'CEO 决定', type: 'select', options: ['通过发布', '退回修改'] }, { name: 'feedback', label: '审阅意见', type: 'textarea', placeholder: '例如：保留案例，但把标题改得更具体。' }], onSubmit: values => { const current = readState(); writeState({ xhsContentReviews: { ...(current.xhsContentReviews || {}), [title]: { decision: values.decision, feedback: values.feedback, at: new Date().toISOString() } }, lastAssistantMessage: values.decision === '通过发布' ? `“${title}”已通过 CEO 审阅，发布 AI 可以按当前版本上架。` : `“${title}”已退回修改，内容 AI 会保留意见并生成下一版。` }); button.textContent = values.decision === '通过发布' ? '已通过' : '已退回'; button.disabled = true; row?.querySelector('.pill')?.replaceChildren(document.createTextNode(values.decision === '通过发布' ? '已批准发布' : '待修改')); showToast(values.decision === '通过发布' ? '内容已批准发布' : '已退回内容修改'); } }); }
      else if (action === 'authorize') { const drawer = document.getElementById('capability-drawer'); const connector = drawer?.querySelector('[data-capability-connector]'); if (drawer) { drawer.classList.add('is-open'); if (connector) connector.value = '需要授权'; showToast('请确认连接器授权方式；失败时仍可手动补录'); } else openFormDialog({ title: '登记外部连接器', description: '先登记读取来源和范围，真正授权前不会执行任务；授权失败时仍会保留手动录入窗口。', submitLabel: '保存连接申请', fields: [{ name: 'source', label: '连接来源', placeholder: '例如：Google Calendar / 抖音开放平台', required: true }, { name: 'scope', label: '读取范围', type: 'textarea', placeholder: '例如：日历事件、任务触发记录、平台结果数据', required: true }], onSubmit: values => { const current = readState(); writeState({ lastConnector: { status: 'pending', ...values, at: new Date().toISOString() }, lastAssistantMessage: `已登记“${values.source}”连接申请，等待授权确认；失败时仍保留手动录入路径。`, lastAssistantHandoff: { label: 'CEO 助理', route: 'calendar.html', message: '连接申请待确认' } }); showToast('连接申请已登记，等待授权确认'); } }); }
      else if (action === 'save-workflow' && button.textContent.trim() === '查看') showToast('已打开当前内容的版本、证据与下一动作');
      else if (action === 'save-workflow' && button.textContent.trim() === '编辑') openFormDialog({ title: '调整自动任务', description: '修改触发时间和交接规则；保存后会保留负责人、输入和失败出口。', submitLabel: '保存节奏', fields: [{ name: 'schedule', label: '触发时间', placeholder: '例如：每天 08:00', required: true }, { name: 'escalation', label: '升级条件', type: 'textarea', placeholder: '例如：API 失败或结果异常时提醒 CEO' }], onSubmit: values => { writeState({ lastScheduleEdit: values }); showToast('自动任务节奏已更新'); } });
      else if (action === 'save-workflow' && ['已启用', '已暂停'].includes(button.textContent.trim())) { const paused = button.textContent.trim() === '已启用'; button.textContent = paused ? '已暂停' : '已启用'; writeState({ scheduledRoutinesPaused: paused }); showToast(paused ? '自动任务已暂停，恢复时会继续从当前上下文运行' : '自动任务已恢复'); }
      else if (action === 'save-workflow') { const workflows = JSON.parse(localStorage.getItem('curis-workflows') || '[]'); workflows.push({ id: Date.now(), name: button.dataset.workflowName || '业务运行工作流', savedAt: new Date().toISOString() }); localStorage.setItem('curis-workflows', JSON.stringify(workflows.slice(-12))); showToast('工作流已保存，可在工作空间搭建中复用'); }
      else if (action === 'asset-detail') showToast(`已打开“${button.dataset.assetTitle || '成果'}”的证据与版本记录`);
      else if (action === 'asset') window.location.href = 'assets.html';
      else if (action === 'finance') window.location.href = 'finance.html';
      else showToast(button.textContent.trim() || '已推进到下一阶段');
    }));
    document.querySelectorAll('[data-platform]').forEach(button => button.addEventListener('click', () => { document.querySelectorAll('[data-platform]').forEach(item => item.classList.toggle('is-active', item === button)); const platform = button.dataset.platform; document.querySelectorAll('[data-platform-name]').forEach(node => node.textContent = platform); writeState({ shortVideoPlatform: platform }); showToast(`已切换到 ${platform} 运营视图`); }));
  }

  function initCalendarPage() {
    if (window.location.pathname.split('/').pop() !== 'calendar.html') return;
    const root = document.querySelector('main.content');
    if (!root || root.dataset.calendarBound === 'true') return;
    root.dataset.calendarBound = 'true';
    const defaults = [
      { id: 'xhs-research', name: '小红书 · 每日研究', business: '小红书运营', schedule: '每天 08:00', owner: '策略分析 AI', task: '输出 3 条候选选题', estimatedCost: 42, route: 'workspace-runtime-xhs.html', enabled: true },
      { id: 'shortvideo-data', name: '抖音 / TikTok · 数据回流', business: '抖音 / TikTok 运营', schedule: '每天 18:00', owner: '数据回收 AI', task: 'API 失败则提醒 CEO 手动补录', estimatedCost: 68, route: 'workspace-runtime-shortvideo.html', enabled: true },
      { id: 'weekly-brief', name: '公司 · 每周经营简报', business: '公司共享', schedule: '每周一 09:00', owner: 'CEO 助理', task: '汇总财务、成果和风险', estimatedCost: 12, route: 'ceo-desk.html', enabled: true },
      { id: 'qa-regression', name: '研发 · 回归检查', business: '软件开发', schedule: '每次提交后', owner: 'QA AI', task: '失败时暂停发布并升级', estimatedCost: 55, route: 'workspace-runtime-software.html', enabled: true }
    ];
    const companyReady = () => Boolean(readState().companyCreatedAt);
    const businessKey = value => /小红书/.test(String(value || '')) ? '小红书运营' : /抖音|TikTok|短视频/.test(String(value || '')) ? '抖音 / TikTok 运营' : /软件|研发|Curis/.test(String(value || '')) ? '软件开发' : '公司共享';
    const activeBusinesses = state => {
      const active = new Set(['公司共享']);
      [state.firstBusiness, state.newBusinessDraft?.name, state.departmentCommitment?.name].forEach(value => active.add(businessKey(value)));
      if (state.softwareAcceptance || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-software.html')) active.add('软件开发');
      if (state.latestXhsFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-xhs.html')) active.add('小红书运营');
      if (state.latestExternalFeedback || (state.calendarEvents || []).some(item => item.route === 'workspace-runtime-shortvideo.html')) active.add('抖音 / TikTok 运营');
      return active;
    };
    let schedules = defaults.map(item => ({ ...item }));
    try {
      const saved = JSON.parse(localStorage.getItem('curis-schedules') || '[]');
      saved.forEach(item => { const index = schedules.findIndex(current => current.id === item.id); if (index >= 0) schedules[index] = { ...schedules[index], ...item }; else schedules.push(item); });
    } catch (_) {}
    const persist = () => localStorage.setItem('curis-schedules', JSON.stringify(schedules));
    const rowFor = id => [...root.querySelectorAll('.routine')].find(row => row.dataset.scheduleId === id);
    const statusLabel = status => ({ queued: '排队中', running: '执行中', completed: '已完成', waiting_ceo: '待 CEO', acknowledged: '已打开', resolved: '已处理', failed: '异常' }[status] || '已记录');
    const renderCalendarSurface = () => {
      const state = readState();
      const topbar = root.closest('.main')?.querySelector('.topbar span:last-child');
      if (topbar) {
        if (!state.companyCreatedAt) topbar.textContent = '公司尚未成立 · 经营日历待启动';
        else {
          const days = Math.max(1, Math.floor((Date.now() - Date.parse(state.companyCreatedAt)) / 86400000) + 1);
          topbar.textContent = `公司成立第 ${days} 天 · ${new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })}`;
        }
      }
      const routineCard = [...root.querySelectorAll('.card')].find(card => card.querySelector('h2')?.textContent.includes('自动运行'));
      if (routineCard) {
        routineCard.querySelector('h2').textContent = companyReady() ? '自动运行中的节奏' : '可复用的自动节奏';
        routineCard.querySelector('.note').textContent = companyReady()
          ? 'AI 会按节奏运行，只有异常、需要权限或需要价值判断时才升级给 CEO。'
          : '这些是业务模板里的建议节奏，创建公司后才会启用，不会在空公司里提前运行。';
      }
      const actual = [
        state.companyCreatedAt && { at: state.companyCreatedAt, title: '公司成立', milestone: true },
        state.meetingDecision && { at: state.meetingDecision.at, title: '会议共识', milestone: true },
        state.softwareAcceptance && { at: state.softwareAcceptance.at, title: 'Curis 验收', milestone: true },
        state.latestXhsFeedback && { at: state.latestXhsFeedback.at, title: '小红书结果', milestone: false },
        state.latestExternalFeedback && { at: state.latestExternalFeedback.at, title: '抖音 / TikTok 结果', milestone: false },
        state.financeBrief && { at: state.financeBrief.at, title: '财务简报', milestone: true },
        ...(Array.isArray(state.calendarEvents) ? state.calendarEvents.map(item => ({ at: item.statusUpdatedAt || item.requestedAt, title: item.title || '自动运行', milestone: ['waiting_ceo', 'resolved'].includes(item.status) })) : [])
      ].filter(item => item?.at).sort((a, b) => String(a.at).localeCompare(String(b.at)));
      const days = [...root.querySelectorAll('.month .day')];
      days.forEach(day => {
        day.querySelector('em')?.remove();
        day.classList.remove('milestone', 'today');
        const dayNumber = Number(day.querySelector('strong')?.textContent || 0);
        const match = actual.find(item => { const date = new Date(item.at); return date.getMonth() === 7 && date.getDate() === dayNumber; });
        if (match) {
          const label = document.createElement('em');
          label.textContent = match.title;
          day.appendChild(label);
          if (match.milestone) day.classList.add('milestone');
        }
      });
      let note = root.querySelector('[data-calendar-truth-note]');
      if (!note) {
        note = document.createElement('p');
        note.dataset.calendarTruthNote = 'true';
        note.className = 'note';
        root.querySelector('.month')?.parentElement?.appendChild(note);
      }
      note.textContent = actual.length
        ? `日历已显示 ${actual.length} 条真实经营记录；自动节奏只在公司成立后生效。`
        : '这里暂时没有真实经营记录。创建公司并完成一次运行后，日历会开始记录成长。';
    };
    const renderCalendarTimeline = () => {
      const timeline = root.querySelector('.timeline');
      if (!timeline) return;
      timeline.querySelectorAll('.event:not([data-schedule-history]):not(.curis-growth-event)').forEach(node => node.remove());
      const state = readState();
      const events = [];
      if (state.companyCreatedAt) events.push({ at: state.companyCreatedAt, title: `${state.companyName || '公司'}正式成立`, note: 'CEO 已完成公司意图、第一条业务和 AI 团队的初始配置。', status: '已归档' });
      if (state.softwareAcceptance) events.push({ at: state.softwareAcceptance.at, title: `软件开发 · ${state.softwareAcceptance.choice === 'accept' ? 'CEO 已验收' : '等待验收判断'}`, note: state.softwareAcceptance.evidenceRef || '研发办公室已提交真实使用验收。', status: state.softwareAcceptance.choice === 'accept' ? '已验证' : '待 CEO' });
      if (state.latestXhsFeedback) events.push({ at: state.latestXhsFeedback.at, title: '小红书运营 · 外部结果已回传', note: '平台数据或 CEO 手动回传已进入业务复盘。', status: state.latestXhsFeedback.resultStatus || '待复盘' });
      if (state.latestExternalFeedback) events.push({ at: state.latestExternalFeedback.at, title: '抖音 / TikTok 运营 · 外部结果已回传', note: '平台数据或 CEO 手动回传已进入业务复盘。', status: state.latestExternalFeedback.resultStatus || '待复盘' });
      if (state.meetingDecision) events.push({ at: state.meetingDecision.at, title: '会议共识 · 已写入经营节奏', note: state.meetingDecision.summary || '会议决定已经形成负责人、下一步和回报口径。', status: '已记录' });
      if (state.financeBrief) events.push({ at: state.financeBrief.at, title: '财务简报 · 待 CEO 判断', note: `收入 ¥${Number(state.financeBrief.revenue || 0).toLocaleString()} · 成本 ¥${Number(state.financeBrief.cost || 0).toLocaleString()} · 结果价值 ¥${Number(state.financeBrief.value || 0).toLocaleString()}`, status: '待 CEO' });
      if (state.lastConnector?.status === 'pending') events.push({ at: state.lastConnector.at, title: `连接申请 · ${state.lastConnector.source || '外部数据来源'}`, note: state.lastConnector.scope || '授权完成前不会读取平台数据；手动录入窗口已保留。', status: '待授权' });
      if (state.departmentResult) events.push({ at: state.departmentResult.at, title: `${state.departmentDraft?.name || '部门办公室'} · 首项责任已回报`, note: state.departmentResult.note || 'CEO 已记录这项责任的真实结果。', status: state.departmentResult.status || '待判断' });
      (state.operatingArchivedItems || []).forEach(item => events.push({ at: item.at, title: `经营事项已归档 · ${item.title}`, note: item.note || '经营办公室事项已收束，历史证据仍可追溯。', status: '已归档' }));
      (state.calendarEvents || []).filter(item => item.status !== 'running').forEach(item => events.push({ at: item.statusUpdatedAt || item.requestedAt, title: item.title || '自动运行', note: item.resolutionNote || item.output || '自动运行结果已写回公司日历。', status: statusLabel(item.status) }));
      if (!events.length) events.push({ at: null, title: '等待第一条经营记录', note: '自动任务、真实结果和 CEO 决策发生后，会在这里形成公司的成长记忆。', status: '待开始' });
      events.forEach(item => {
        const event = document.createElement('div'); event.className = 'event';
        const date = item.at ? new Date(item.at).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }) : '尚无日期';
        event.innerHTML = `<time>${escapeHtml(date)}</time><div><strong></strong><p></p><span class="status"></span></div>`;
        event.querySelector('strong').textContent = item.title; event.querySelector('p').textContent = item.note; event.querySelector('.status').textContent = item.status; timeline.appendChild(event);
      });
    };
    const runSchedule = item => {
      // ponytail: deterministic prototype run; replace this boundary with the real scheduler/runtime.
      if (!companyReady()) {
        writeState({ lastAssistantMessage: '公司还没有成立，自动任务暂时不会运行。先完成公司创建，再回来安排经营节奏。', lastAssistantHandoff: { label: '创建公司', route: 'founding-flow.html', message: '先完成公司创建' } });
        showToast('先完成公司创建，再运行自动任务');
        window.location.href = 'founding-flow.html';
        return;
      }
      const requestedAt = new Date().toISOString();
      const waiting = /CEO|授权|回传|失败|异常|确认/.test(`${item.task} ${item.schedule}`);
      const current = readState();
      const contextKey = item.route || 'company';
      const fallbackModel = contextKey === 'workspace-runtime-shortvideo.html' ? 'GPT-5 mini' : contextKey === 'ceo-desk.html' ? 'GPT-5 mini' : 'GPT-5';
      const capability = current.capabilityRuntimeByContext?.[contextKey] || { model: fallbackModel, agent: item.owner || 'CEO 助理', skills: [], tools: [], connector: '手动录入' };
      const cost = Number(item.estimatedCost || 0);
      const businessKey = /小红书/.test(item.business || '') ? '小红书运营' : /抖音|TikTok|短视频/.test(item.business || '') ? '抖音 / TikTok 运营' : /软件|研发|Curis/.test(item.business || '') ? '软件开发' : '公司共享';
      const maxConcurrent = Number(current.capacityContracts?.[businessKey]?.maxConcurrent || 3);
      const activeRuns = (current.calendarEvents || []).filter(run => run.business === item.business && ['running'].includes(run.status)).length;
      const queued = activeRuns >= maxConcurrent;
      const startedAt = queued ? null : requestedAt;
      const run = { runId: `run-${Date.now()}`, scheduleId: item.id, title: `${item.name} · ${queued ? '排队中' : '执行中'}`, owner: item.owner, business: item.business || '公司共享', status: queued ? 'queued' : 'running', requestedAt, queuedAt: queued ? requestedAt : null, startedAt, finishedAt: null, executionMs: null, statusUpdatedAt: requestedAt, task: item.task, requiresCEOHint: waiting, output: queued ? `当前容量已满，已进入队列（并发上限 ${maxConcurrent} 项）` : item.task, nextStage: queued ? '等待可用容量' : '运行中', requiresCEO: false, route: item.route || 'calendar.html', escalation: item.task, cost, capability, capacityContract: current.capacityContracts?.[businessKey] || null, time: new Date().toLocaleString('zh-CN', { month: 'numeric', day: '2-digit', hour: '2-digit', minute: '2-digit' }) };
      const costRecord = !queued && cost > 0 ? { business: run.business, category: '模型与调用', amount: cost, source: `自动运行 · ${item.owner}`, model: capability.model, agent: capability.agent, skills: capability.skills || [], tools: capability.tools || [], connector: capability.connector, runId: run.runId, at: requestedAt } : null;
      writeState({ lastScheduledRun: run, calendarEvents: [...(current.calendarEvents || []), run].slice(-24), ...(costRecord ? { financeCosts: [...(Array.isArray(current.financeCosts) ? current.financeCosts : []), costRecord].slice(-40) } : {}), lastAssistantMessage: queued ? `${item.name} 已进入容量队列：当前并发上限 ${maxConcurrent} 项` : `${item.name} 已开始运行：${item.task}`, lastAssistantHandoff: { label: queued ? 'AI 组织办公室' : '公司日历', route: queued ? 'ai-organization.html' : run.route, message: statusLabel(run.status) } });
      item.lastRunStatus = run.status;
      item.lastRunAt = requestedAt;
      persist();
      updateRow(item);
      renderRunHistory();
      if (queued) return showToast(`“${item.name}”已进入容量队列`);
      showToast(`“${item.name}”已开始运行`);
      window.setTimeout(() => {
        const finishedAt = new Date().toISOString();
        const finalStatus = waiting ? 'waiting_ceo' : 'completed';
        updateScheduledRunStatus(run.runId, finalStatus, { title: `${item.name} · ${waiting ? '需 CEO 处理' : '已完成'}`, startedAt: run.startedAt || requestedAt, finishedAt, executionMs: Math.max(1, Date.parse(finishedAt) - Date.parse(run.startedAt || requestedAt)), requiresCEO: waiting, nextStage: waiting ? 'CEO 助理待汇报' : '进入下一工作阶段', output: item.task, assistantMessage: waiting ? `${item.name} 已运行到需要 CEO 判断的节点：${item.task}` : `${item.name} 已完成：${item.task}` });
        item.lastRunStatus = finalStatus;
        item.lastRunAt = finishedAt;
        persist();
        updateRow(item);
        renderRunHistory();
        showToast(waiting ? `“${item.name}”已运行，等待 CEO 处理` : `“${item.name}”已完成并写回公司日历`);
        promoteQueuedRuns(run.business);
      }, 180);
    };
    const updateRow = item => {
      const row = rowFor(item.id);
      if (!row) return;
      const ready = companyReady();
      const hidden = ready && !activeBusinesses(readState()).has(businessKey(item.business));
      row.hidden = hidden;
      row.style.display = hidden ? 'none' : '';
      const title = row.querySelector('strong');
      if (title) title.textContent = item.name;
      row.classList.toggle('is-paused', !ready || !item.enabled);
      const details = row.querySelector('span');
      if (details) details.textContent = `${ready ? (item.business || '公司共享') : '业务模板'} · ${item.schedule} · ${item.owner} · ${item.task} · ${ready ? `预计 ¥${Number(item.estimatedCost || 0).toLocaleString()}/次` : '创建公司后启用'}${item.lastRunStatus ? ` · 最近${statusLabel(item.lastRunStatus)}` : ''}`;
      const toggle = row.querySelector('[data-schedule-action="toggle"]');
      if (toggle) { toggle.textContent = ready ? (item.enabled ? '已启用' : '已暂停') : '待创建公司'; toggle.disabled = !ready; }
      const run = row.querySelector('[data-schedule-action="run"]');
      if (run) { run.disabled = !ready || !item.enabled; run.title = ready ? '' : '创建公司后才能运行'; }
    };
    const openEditor = item => {
      const businessOptions = ['公司共享', '软件开发', '小红书运营', '抖音 / TikTok 运营'].filter(option => option === '公司共享' || activeBusinesses(readState()).has(businessKey(option)) || item?.business === option);
      return openFormDialog({
      title: item ? `调整自动任务 · ${item.name}` : '新建自动任务',
      description: '任务会按时触发，但不会绕过负责人、失败出口和 CEO 价值判断。保存后可随时暂停。',
      submitLabel: item ? '保存任务' : '创建任务',
      fields: [
        { name: 'name', label: '任务名称', placeholder: '例如：小红书 · 每日研究', value: item?.name || '', required: true },
        { name: 'business', label: '所属业务', type: 'select', options: businessOptions, value: item?.business || '公司共享', required: true },
        { name: 'routeLabel', label: '运行入口', type: 'select', options: ['CEO 工作台', '会议工作台', '研发办公室', '小红书运营办公室', '抖音 / TikTok 运营办公室'], value: item?.routeLabel || ({ 'workspace-runtime-software.html': '研发办公室', 'workspace-runtime-xhs.html': '小红书运营办公室', 'workspace-runtime-shortvideo.html': '抖音 / TikTok 运营办公室', 'meeting.html': '会议工作台', 'ceo-desk.html': 'CEO 工作台' }[item?.route] || 'CEO 工作台'), required: true },
        { name: 'schedule', label: '触发节奏', placeholder: '例如：每天 08:00 / 每周一 09:00', value: item?.schedule || '', required: true },
        { name: 'owner', label: '负责人', placeholder: '例如：策略分析 AI', value: item?.owner || '', required: true },
        { name: 'estimatedCost', label: '预计单次成本（元）', type: 'number', placeholder: '例如：42', value: item?.estimatedCost || '' },
        { name: 'task', label: '任务产出与失败出口', type: 'textarea', placeholder: '例如：输出 3 条候选选题；API 失败时提醒 CEO 手动补录', value: item?.task || '', required: true }
      ],
      onSubmit: values => {
        const routeMap = { 'CEO 工作台': 'ceo-desk.html', '会议工作台': 'meeting.html', '研发办公室': 'workspace-runtime-software.html', '小红书运营办公室': 'workspace-runtime-xhs.html', '抖音 / TikTok 运营办公室': 'workspace-runtime-shortvideo.html' };
        const normalized = { ...values, route: routeMap[values.routeLabel] || 'ceo-desk.html', estimatedCost: Number(values.estimatedCost || 0) };
        if (item) Object.assign(item, normalized, { enabled: item.enabled });
        else schedules.push({ id: `schedule-${Date.now()}`, ...normalized, business: values.business || '公司共享', enabled: true });
        persist();
        if (item) updateRow(item); else renderRows();
        showToast(item ? '自动任务已更新' : '自动任务已创建，默认处于启用状态');
      }
      });
    };
    const renderRows = () => {
      const existing = [...root.querySelectorAll('.routine')];
      existing.forEach((row, index) => { if (schedules[index]) { row.dataset.scheduleId = schedules[index].id; updateRow(schedules[index]); } });
      const container = existing[0]?.parentElement;
      schedules.slice(existing.length).forEach(item => {
        if (!container) return;
        const row = document.createElement('div');
        row.className = 'routine';
        row.dataset.scheduleId = item.id;
        row.innerHTML = `<div><strong></strong><span></span></div><div class="routine-actions"><button type="button" data-schedule-action="edit">编辑</button><button type="button" data-schedule-action="toggle"></button><button type="button" data-schedule-action="run">立即运行</button></div>`;
        container.appendChild(row);
        updateRow(item);
      });
    };
    const renderRunHistory = () => {
      const timeline = root.querySelector('.timeline');
      if (!timeline) return;
      renderCalendarTimeline();
      timeline.querySelectorAll('[data-schedule-history]').forEach(node => node.remove());
      const history = readState().calendarEvents || [];
      schedules.forEach(item => {
        const latest = history.filter(event => event.scheduleId === item.id).sort((a, b) => String(b.statusUpdatedAt || b.requestedAt || '').localeCompare(String(a.statusUpdatedAt || a.requestedAt || '')))[0];
        if (latest) { item.lastRunStatus = latest.status; item.lastRunAt = latest.statusUpdatedAt || latest.requestedAt; updateRow(item); }
      });
      history.slice(-6).reverse().forEach(eventRecord => {
        const event = document.createElement('div');
        event.className = 'event';
        event.dataset.scheduleHistory = 'true';
        const actionLabel = eventRecord.status === 'queued' ? '查看容量' : eventRecord.status === 'waiting_ceo' ? '打开并确认' : eventRecord.status === 'acknowledged' ? '完成处理' : eventRecord.status === 'failed' ? '记录异常已处理' : eventRecord.status === 'resolved' ? '进入复盘' : '';
        event.innerHTML = `<time>${escapeHtml(eventRecord.time || '刚刚')}</time><div><strong></strong><p></p><span class="status">${escapeHtml(statusLabel(eventRecord.status))}</span>${actionLabel ? `<button type="button" data-schedule-history-action>${actionLabel}</button>` : ''}</div>`;
        event.querySelector('strong').textContent = eventRecord.title || '自动任务已运行';
        event.querySelector('p').textContent = `${eventRecord.resolutionNote || eventRecord.output || eventRecord.note || '结果会在回报后进入经营简报。'}${eventRecord.cost ? ` · 实际成本 ¥${Number(eventRecord.cost).toLocaleString()}` : ''}`;
        event.querySelector('.status').dataset.runStatus = eventRecord.status || 'recorded';
        event.querySelector('[data-schedule-history-action]')?.addEventListener('click', clickEvent => {
          clickEvent.stopPropagation();
          if (eventRecord.status === 'queued') {
            writeState({ lastAssistantMessage: `${eventRecord.title || '自动任务'}正在等待可用容量，我已把当前队列和能力合同放到 AI 组织办公室。`, lastAssistantHandoff: { label: 'AI 组织办公室', route: 'ai-organization.html', message: '自动任务排队中' } });
            window.location.href = 'ai-organization.html';
            return;
          }
          if (eventRecord.status === 'resolved') {
            writeState({ lastAssistantMessage: `${eventRecord.title || '自动任务'}已处理，下一步进入业务复盘。`, lastAssistantHandoff: { label: eventRecord.business || '业务空间', route: eventRecord.route || 'business.html', message: '自动运行已处理 · 进入复盘' } });
            window.location.href = eventRecord.route || 'business.html';
            return;
          }
          if (eventRecord.status === 'acknowledged' || eventRecord.status === 'failed') {
            return openFormDialog({ title: eventRecord.status === 'failed' ? '记录自动运行异常' : '完成自动运行处理', description: '把 CEO 的处理结果写回运行记录，避免同一条提醒在经营日里反复出现。', submitLabel: '保存处理结果', fields: [{ name: 'resolutionNote', label: '处理结果', type: 'textarea', placeholder: '例如：已确认结果，下一次继续观察；或已手动补录平台数据。', required: true }], onSubmit: values => { updateScheduledRunStatus(eventRecord.runId, 'resolved', { requiresCEO: false, resolvedAt: new Date().toISOString(), nextStage: '进入复盘', resolutionNote: values.resolutionNote, assistantMessage: `${eventRecord.title || '自动任务'}已处理，结果已进入下一次复盘。` }); renderRunHistory(); showToast('自动运行已处理并进入复盘'); } });
          }
          updateScheduledRunStatus(eventRecord.runId, 'acknowledged', { openedAt: new Date().toISOString(), requiresCEO: true, nextStage: 'CEO 完成处理', assistantMessage: `${eventRecord.title || '自动任务'}已打开，我已把你带到对应工作空间。` });
          writeState({ lastAssistantHandoff: { label: eventRecord.business || '业务空间', route: eventRecord.route || 'calendar.html', message: '自动运行已打开 · 等待完成处理' } });
          window.location.href = eventRecord.route || 'calendar.html';
        });
        timeline.prepend(event);
      });
    };
    const renderGrowthHistory = () => {
      const timeline = root.querySelector('.timeline');
      if (!timeline) return;
      timeline.querySelectorAll('[data-company-milestone]').forEach(node => node.remove());
      const state = readState();
      const records = [
        state.companyCreatedAt && { at: state.companyCreatedAt, title: `${state.companyName || '公司'}正式成立`, note: 'CEO 已完成公司意图、第一条业务和 AI 团队的初始配置。', status: '已归档', route: 'ceo-desk.html' },
        state.meetingDecision && { at: state.meetingDecision.at, title: '会议形成第一项可执行共识', note: state.meetingDecision.summary || '会议承诺已经写入日历，等待负责人回报。', status: '已记录', route: 'meeting.html' },
        state.softwareAcceptance && { at: state.softwareAcceptance.at, title: `Curis v0.2${state.softwareAcceptance.choice === 'accept' ? '通过' : '进入下一次验收'}`, note: state.softwareAcceptance.feedback || '研发办公室已经收到 CEO 的真实使用反馈。', status: state.softwareAcceptance.choice === 'accept' ? '已验证' : '待处理', route: 'workspace-runtime-software.html' },
        state.latestXhsFeedback && { at: state.latestXhsFeedback.at, title: '小红书结果回流', note: `阅读 ${Number(state.latestXhsFeedback.reads || 0).toLocaleString()} · 新增粉丝 ${Number(state.latestXhsFeedback.follows || 0).toLocaleString()} · 线索价值 ¥${Number(state.latestXhsFeedback.value || 0).toLocaleString()}`, status: state.latestXhsFeedback.resultStatus || '待复核', route: 'workspace-runtime-xhs.html' },
        state.latestExternalFeedback && { at: state.latestExternalFeedback.at, title: '抖音 / TikTok 结果回流', note: `播放 ${Number(state.latestExternalFeedback.plays || 0).toLocaleString()} · 新增粉丝 ${Number(state.latestExternalFeedback.follows || 0).toLocaleString()} · 成交价值 ¥${Number(state.latestExternalFeedback.value || 0).toLocaleString()}`, status: state.latestExternalFeedback.resultStatus || '待复核', route: 'workspace-runtime-shortvideo.html' },
        state.financeBrief && { at: state.financeBrief.at, title: '本周期财务简报已准备', note: `收入 ¥${Number(state.financeBrief.revenue || 0).toLocaleString()} · 成本 ¥${Number(state.financeBrief.cost || 0).toLocaleString()} · 结果价值 ¥${Number(state.financeBrief.value || 0).toLocaleString()}`, status: '待 CEO 判断', route: 'finance.html' },
        state.lastConnector?.status === 'pending' && { at: state.lastConnector.at, title: `连接申请待确认 · ${state.lastConnector.source || '外部数据来源'}`, note: state.lastConnector.scope || '授权完成前不会读取平台数据；手动录入窗口已保留。', status: '待授权', route: 'calendar.html' },
        state.departmentResult && { at: state.departmentResult.at, title: `${state.departmentDraft?.name || '部门办公室'}完成首项责任回报`, note: state.departmentResult.note || 'CEO 已记录这项责任的真实结果。', status: state.departmentResult.status || '待判断', route: 'workspace-runtime-department.html' },
        ...((state.operatingArchivedItems || []).map(item => ({ at: item.at, title: `经营事项已归档 · ${item.title}`, note: item.note || '经营办公室事项已收束，历史证据仍可追溯。', status: '已归档', route: 'operating.html' })))
      ].filter(Boolean).sort((a, b) => String(b.at).localeCompare(String(a.at))).slice(0, 8);
      records.forEach(record => {
        const event = document.createElement('div');
        event.className = 'event curis-growth-event';
        event.dataset.companyMilestone = 'true';
        event.innerHTML = `<time></time><div><strong></strong><p></p><span class="status"></span></div>`;
        event.querySelector('time').textContent = new Date(record.at).toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
        event.querySelector('strong').textContent = record.title;
        event.querySelector('p').textContent = record.note;
        event.querySelector('.status').textContent = record.status;
        if (record.route) {
          event.setAttribute('role', 'link');
          event.tabIndex = 0;
          const go = () => { window.location.href = record.route; };
          event.addEventListener('click', go);
          event.addEventListener('keydown', eventKey => { if (['Enter', ' '].includes(eventKey.key)) { eventKey.preventDefault(); go(); } });
        }
        timeline.prepend(event);
      });
    };
    const style = document.createElement('style');
    style.textContent = '.routine-actions{display:flex;gap:6px;flex:none}.routine.is-paused{opacity:.58}.routine-actions button{padding:7px 9px!important}.routine-actions button[data-schedule-action="run"]{color:var(--accentText);background:var(--accent);border-color:var(--accent)}.event [data-schedule-history-action]{margin-top:7px;padding:5px 8px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}.event [data-schedule-history-action]:hover{background:var(--bg-overlay-l2,rgba(224,226,242,.06))}@media(max-width:620px){.routine{align-items:flex-start!important;flex-direction:column}.routine-actions{width:100%}.routine-actions button{flex:1}}';
    document.head.appendChild(style);
    const headerButton = root.querySelector('.header .actions button:first-child');
    if (headerButton) {
      headerButton.removeAttribute('data-runtime-action');
      headerButton.removeAttribute('data-workflow-name');
      headerButton.dataset.scheduleAction = 'new';
      headerButton.textContent = '新建自动任务';
    }
    const rows = [...root.querySelectorAll('.routine')];
    rows.forEach((row, index) => {
      const item = schedules[index];
      if (!item) return;
      row.dataset.scheduleId = item.id;
      const original = row.querySelector('button');
      if (original) {
        original.removeAttribute('data-runtime-action');
        original.dataset.scheduleAction = index === 1 ? 'connect' : index > 1 ? 'toggle' : 'edit';
        if (index > 1) original.textContent = item.enabled ? '已启用' : '已暂停';
        const actions = document.createElement('div');
        actions.className = 'routine-actions';
        original.replaceWith(actions);
        actions.appendChild(original);
        const run = document.createElement('button');
        run.type = 'button'; run.dataset.scheduleAction = 'run'; run.textContent = '立即运行';
        actions.appendChild(run);
      }
      updateRow(item);
    });
    root.addEventListener('click', event => {
      const action = event.target.closest('[data-schedule-action]');
      if (!action) return;
      const item = schedules.find(current => current.id === action.closest('.routine')?.dataset.scheduleId);
      const type = action.dataset.scheduleAction;
      if (type === 'new') return openEditor();
      if (!item) return;
      if (type === 'edit') return openEditor(item);
      if (type === 'run') return runSchedule(item);
      if (type === 'connect') return openFormDialog({ title: `连接数据来源 · ${item.name}`, description: '连接器只读取平台数据。授权失败时，任务会保留手动录入窗口，不会伪造结果。', submitLabel: '保存连接', fields: [{ name: 'source', label: '来源', placeholder: '例如：抖音开放平台 / TikTok Analytics', required: true }, { name: 'scope', label: '读取范围', type: 'textarea', placeholder: '例如：播放、完播、互动、粉丝与成交数据', required: true }], onSubmit: values => { item.connection = values; persist(); writeState({ lastConnector: { status: 'pending', ...values, scheduleId: item.id, at: new Date().toISOString() }, lastAssistantMessage: `已登记“${values.source}”连接申请，等待授权确认；${item.name} 未授权前仍保留手动窗口。`, lastAssistantHandoff: { label: '公司日历', route: 'calendar.html', message: '连接申请待确认' } }); showToast('数据来源已登记，等待授权确认'); } });
      if (type === 'toggle') { item.enabled = !item.enabled; persist(); updateRow(item); writeState({ scheduledRoutinesPaused: schedules.filter(current => !current.enabled).map(current => current.id) }); showToast(item.enabled ? `已恢复“${item.name}”` : `已暂停“${item.name}”`); }
    });
    renderRows();
    renderCalendarSurface();
    renderRunHistory();
    window.addEventListener('curis-state-changed', () => { renderCalendarSurface(); renderRows(); renderRunHistory(); });
  }

  function initWorkspaceScheduleEntry() {
    const page = window.location.pathname.split('/').pop();
    const labels = {
      'workspace-runtime-software.html': ['软件开发 · 每次提交后回归', '软件开发', 'QA AI', '每次提交后', 55],
      'workspace-runtime-xhs.html': ['小红书 · 每日研究与发布检查', '小红书运营', '策略分析 AI', '每天 08:00', 42],
      'workspace-runtime-shortvideo.html': ['抖音 / TikTok · 数据回流与复盘', '抖音 / TikTok 运营', '数据回收 AI', '每天 18:00', 68],
      'workspace-runtime-department.html': ['部门责任 · 每日进展回报', '公司共享', '业务工程 AI', '每天 18:00', 30]
    }[page];
    if (!labels) return;
    const header = document.querySelector('main.content .header');
    const actions = document.querySelector('.header .actions') || document.querySelector('.topbar-right');
    if (!header && !actions) return;
    if (document.querySelector('[data-workspace-schedule]')) return;
    const button = document.createElement('button');
    button.type = 'button'; button.dataset.workspaceSchedule = 'true'; button.textContent = '安排自动运行';
    if (page === 'workspace-runtime-shortvideo.html') {
      button.className = 'btn btn-secondary';
      (actions || header).insertBefore(button, actions?.firstChild || null);
    } else {
      button.className = 'btn btn-secondary';
      let holder = actions;
      if (!holder) {
        holder = document.createElement('div');
        holder.className = 'actions workspace-schedule-actions';
        const status = header.querySelector('.status');
        if (status) { status.replaceWith(holder); holder.append(status); }
        else header.appendChild(holder);
      }
      holder.insertBefore(button, holder.firstChild);
    }
    button.addEventListener('click', () => openFormDialog({
      title: '安排自动运行',
      description: '定时任务会在无异常时自行推进；需要 CEO 判断、授权或真实结果时，CEO 助理会回来汇报。',
      submitLabel: '保存到公司日历',
      fields: [
        { name: 'schedule', label: '触发节奏', placeholder: `例如：${labels[3]}`, required: true },
        { name: 'owner', label: '负责人', placeholder: labels[2], required: true },
        { name: 'estimatedCost', label: '预计单次成本（元）', type: 'number', value: labels[4], required: true },
        { name: 'escalation', label: '升级条件', type: 'textarea', placeholder: '例如：平台授权失效、结果异常或需要 CEO 确认品牌边界' }
      ],
      onSubmit: values => {
        const schedules = JSON.parse(localStorage.getItem('curis-schedules') || '[]');
        schedules.push({ id: `workspace-${Date.now()}`, name: labels[0], business: labels[1], schedule: values.schedule, owner: values.owner, task: values.escalation || '按当前工作空间流程运行', estimatedCost: Number(values.estimatedCost || labels[4]), route: page, enabled: true });
        localStorage.setItem('curis-schedules', JSON.stringify(schedules.slice(-24)));
        writeState({ lastScheduledWorkspace: { name: labels[0], ...values, at: new Date().toISOString() }, lastAssistantMessage: `已把“${labels[0]}”加入公司日历。没有异常时我会替你守住这条节奏。`, lastAssistantHandoff: { label: '公司日历', route: 'calendar.html', message: '自动运行已安排' } });
        button.textContent = '已加入日历';
        showToast('已加入公司日历，自动运行已启用');
      }
    }));
  }

  function initScheduledRunContext() {
    const page = window.location.pathname.split('/').pop();
    if (!page || page === 'calendar.html' || page === 'ceo-desk.html' || document.querySelector('[data-scheduled-run-context]')) return;
    const run = readState().lastScheduledRun;
    if (!run || run.route !== page || !['waiting_ceo', 'acknowledged', 'failed'].includes(run.status)) return;
    const header = document.querySelector('main.content .header, main.content .page-header, main.main > .topbar, .board-layout');
    if (!header) return;
    const banner = document.createElement('section');
    banner.dataset.scheduledRunContext = 'true';
    banner.className = 'curis-scheduled-run-context';
    const actionLabel = run.status === 'waiting_ceo' ? '打开并确认' : run.status === 'failed' ? '记录异常已处理' : '完成处理';
    banner.innerHTML = `<div><p class="curis-scheduled-run-kicker">CEO 助理 · 自动运行交接</p><strong></strong><span></span></div><button type="button">${actionLabel}</button>`;
    banner.querySelector('strong').textContent = run.title || '自动任务已运行';
    banner.querySelector('span').textContent = run.status === 'failed' ? (run.output || '运行出现异常，请记录处理结果。') : run.status === 'acknowledged' ? `${run.output || '任务结果已准备好'} · 已打开，等待 CEO 完成处理` : (run.output || '任务已运行到需要 CEO 判断的节点。');
    banner.querySelector('button').addEventListener('click', () => {
      if (run.status === 'waiting_ceo') {
        updateScheduledRunStatus(run.runId, 'acknowledged', { openedAt: new Date().toISOString(), requiresCEO: true, nextStage: 'CEO 完成处理', assistantMessage: `${run.title || '自动任务'}已打开，我已把当前业务空间交给 CEO。` });
        banner.querySelector('button').textContent = '完成处理';
        banner.querySelector('span').textContent = `${run.output || '任务结果已准备好'} · 已打开，等待 CEO 完成处理`;
        showToast('自动运行已打开，请确认结果后完成处理');
        return;
      }
      openFormDialog({ title: run.status === 'failed' ? '记录自动运行异常' : '完成自动运行处理', description: '把 CEO 的处理结果写回运行记录，完成后才会进入下一次复盘。', submitLabel: '保存处理结果', fields: [{ name: 'resolutionNote', label: '处理结果', type: 'textarea', placeholder: '例如：已确认结果，下一次继续观察；或已手动补录平台数据。', required: true }], onSubmit: values => { updateScheduledRunStatus(run.runId, 'resolved', { requiresCEO: false, resolvedAt: new Date().toISOString(), nextStage: '进入复盘', resolutionNote: values.resolutionNote, assistantMessage: `${run.title || '自动任务'}已处理，结果已进入下一次复盘。` }); banner.remove(); showToast('自动运行已处理并进入复盘'); } });
    });
    const style = document.createElement('style');
    style.textContent = '.curis-scheduled-run-context{display:flex;align-items:center;justify-content:space-between;gap:14px;margin:0 0 18px;padding:14px 16px;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:10px;background:var(--bg-base-secondary,#202226)}.curis-scheduled-run-context>div{display:grid;gap:4px}.curis-scheduled-run-kicker{margin:0;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-scheduled-run-context strong{font-size:13px}.curis-scheduled-run-context span{color:var(--text-secondary,#a4a7af);font-size:11px}.curis-scheduled-run-context button{padding:8px 11px;color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border:0;border-radius:7px;font:inherit;font-size:11px;font-weight:600;cursor:pointer}@media(max-width:620px){.curis-scheduled-run-context{align-items:flex-start;flex-direction:column}.curis-scheduled-run-context button{width:100%}}';
    document.head.appendChild(style);
    header.parentNode.insertBefore(banner, header.nextSibling);
  }

  function initAssetLibrary() {
    const root = document.querySelector('[data-assets-page]');
    if (!root) return;
    let assets = [];
    const rebuildAssets = () => {
      assets = [];
      const currentState = readState();
      const importedAgents = currentState.workspaceStudio?.externalAgents || [];
      importedAgents.forEach(agent => assets.push({ type: '外部 Agent', title: `${agent.name} · 拆解包`, owner: '业务工程 AI', version: agent.reviewed ? '已审阅' : '待审阅', evidence: `职责：${agent.responsibility}${agent.reviewNote ? ` · CEO 备注：${agent.reviewNote}` : ''}`, reuse: '工作空间搭建', reviewed: Boolean(agent.reviewed) }));
      (currentState.outcomeAttributions || []).slice(-12).forEach(outcome => {
        const pendingAllocation = outcome.allocationStatus === 'pending_review';
        assets.push({ type: `业务结果 · ${outcome.business}`, title: `${outcome.business} · 结果包`, owner: pendingAllocation ? 'CEO 待分配' : (outcome.agent || 'CEO 手动回传'), version: new Date(outcome.at || Date.now()).toLocaleDateString('zh-CN'), evidence: `${outcome.status} · 价值 ¥${Number(outcome.value || 0).toLocaleString()} · ${runLabelForState(currentState, outcome.runId, outcome.runIds)}${outcome.evidenceRef ? ` · 证据：${outcome.evidenceRef} · ${outcome.evidenceStatus || '待 CEO 采用'}` : ' · 未登记证据'}${pendingAllocation ? ' · 协作贡献待确认' : ''}`, reuse: outcome.business, outcomeId: outcome.id, reviewed: !pendingAllocation, reviewAction: pendingAllocation ? '去分配' : '复用' });
      });
      try {
        const workflows = JSON.parse(localStorage.getItem('curis-workflows') || '[]');
        workflows.slice(-12).forEach(workflow => assets.push({ type: '可复用流程', title: workflow.name || '业务运行流程', owner: 'CEO 助理', version: workflow.savedAt ? new Date(workflow.savedAt).toLocaleDateString('zh-CN') : '当前版', evidence: '已保存能力组合 · 可带上下文复用', reuse: '工作空间搭建' }));
      } catch (_) {}
    };
    rebuildAssets();
    const filterRoot = root.querySelector('.filters');
    if (filterRoot && !filterRoot.querySelector('[data-asset-filter="业务结果"]')) { const resultFilter = document.createElement('button'); resultFilter.type = 'button'; resultFilter.dataset.assetFilter = '业务结果'; resultFilter.textContent = '业务结果'; filterRoot.appendChild(resultFilter); }
    const list = root.querySelector('[data-asset-list]');
    const summary = root.querySelectorAll('.summary .metric');
    if (!document.getElementById('curis-assets-empty-style')) { const style = document.createElement('style'); style.id = 'curis-assets-empty-style'; style.textContent = '.curis-assets-empty{display:grid;gap:5px;padding:26px 0;color:var(--text-secondary,#a4a7af);border-top:1px solid var(--line,rgba(224,226,242,.12))}.curis-assets-empty strong{color:var(--text-default,#e2e3e7);font-size:12px}.curis-assets-empty span{font-size:10px;line-height:1.5}'; document.head.appendChild(style); }
    const renderSummary = () => {
      const verified = assets.filter(item => item.reviewed !== false && /业务结果|软件|小红书|抖音/.test(item.type)).length;
      const workflows = assets.filter(item => item.type === '可复用流程').length;
      const sources = new Set(assets.map(item => item.source).filter(Boolean)).size;
      const pending = assets.filter(item => item.reviewed === false).length;
      [[verified, verified ? '已记录成果' : '完成验收后产生'], [workflows, workflows ? '已保存工作流' : '保存后可复用'], [sources, sources ? '来源已登记' : '等待来源'], [pending, pending ? '需要 CEO 处理' : '暂无待补证据']].forEach(([value, note], index) => { summary[index]?.querySelector('strong')?.replaceChildren(document.createTextNode(String(value))); summary[index]?.querySelector('small')?.replaceChildren(document.createTextNode(note)); });
    };
    const render = filter => { const filtered = assets.filter(item => filter === '全部' || item.type.includes(filter)); list.innerHTML = filtered.length ? filtered.map(item => `<article class="asset-row"><div class="asset-main"><span class="asset-type">${escapeHtml(item.type)}</span><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.owner)} · ${escapeHtml(item.version)} · ${escapeHtml(item.evidence)}</p></div><div class="asset-actions"><button type="button" data-asset-action="reuse" data-asset-title="${escapeHtml(item.title)}" data-asset-outcome-id="${escapeHtml(item.outcomeId || '')}" data-asset-reviewed="${item.reviewed === false ? 'false' : 'true'}">${item.reviewAction || (item.reviewed === false ? '去审阅' : '复用')}</button><button type="button" data-asset-action="detail" data-asset-title="${escapeHtml(item.title)}" data-asset-outcome-id="${escapeHtml(item.outcomeId || '')}">查看</button></div></article>`).join('') : '<div class="curis-assets-empty"><strong>成果库还没有内容</strong><span>AI 员工完成交付、CEO 验收或外部结果回传后，成果会带着来源和版本出现在这里。</span></div>'; };
    renderSummary();
    render('全部');
    window.addEventListener('curis-state-changed', () => {
      rebuildAssets();
      renderSummary();
      render(root.querySelector('[data-asset-filter].is-active')?.dataset.assetFilter || '全部');
    });
    root.addEventListener('click', event => {
      const reuse = event.target.closest('[data-asset-action="reuse"]');
      if (!reuse) return;
      const outcome = reuse.dataset.assetOutcomeId ? (readState().outcomeAttributions || []).find(item => item.id === reuse.dataset.assetOutcomeId) : null;
      if (reuse.dataset.assetReviewed === 'false') {
        if (outcome) {
          writeState({ lastAssistantMessage: `“${outcome.business}”的协作结果还没有完成贡献分配，先到财务与经营确认 KPI 归因。`, lastAssistantHandoff: { label: '财务与经营', route: 'finance.html', message: '待分配协作结果' } });
          window.setTimeout(() => { window.location.href = 'finance.html'; }, 180);
          return;
        }
        writeState({ lastAssistantMessage: `“${reuse.dataset.assetTitle}”还没有经过 CEO 审阅，先回到工作空间搭建确认职责和交接。`, lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: '等待外部 Agent 审阅' } });
        window.setTimeout(() => { window.location.href = 'workspace-studio.html'; }, 180);
        return;
      }
      writeState({ lastReusedAsset: reuse.dataset.assetTitle, ...(outcome ? { lastReusedOutcome: outcome } : {}), lastAssistantMessage: `已把“${reuse.dataset.assetTitle}”交给工作空间搭建，保留原始上下文和版本关系。`, lastAssistantHandoff: { label: '工作空间搭建', route: 'workspace-studio.html', message: `复用成果：${reuse.dataset.assetTitle}` } });
      window.setTimeout(() => { window.location.href = 'workspace-studio.html'; }, 180);
    });
    root.addEventListener('click', event => { const filter = event.target.closest('[data-asset-filter]'); if (filter) { root.querySelectorAll('[data-asset-filter]').forEach(x => x.classList.toggle('is-active', x === filter)); render(filter.dataset.assetFilter); } const detail = event.target.closest('[data-asset-action="detail"]'); if (detail) { const current = readState(); const outcome = detail.dataset.assetOutcomeId ? (current.outcomeAttributions || []).find(item => item.id === detail.dataset.assetOutcomeId) : null; if (outcome) return openEvidenceReview({ title: detail.dataset.assetTitle || `${outcome.business} · 结果包`, source: outcome.evidenceRef || outcome.source || 'CEO 结果回传', summary: `价值 ¥${Number(outcome.value || 0).toLocaleString()} · ${runLabelForState(current, outcome.runId, outcome.runIds)} · 参与 AI：${(outcome.contributors || []).map(item => item.agent).join('、') || outcome.agent || '未登记'}`, status: outcome.evidenceStatus || '待 CEO 采用', confidence: outcome.status === '已验证价值' ? 'CEO 已确认价值' : '待复核', outcomeId: outcome.id, evidenceType: outcome.evidence?.type || outcome.evidenceType || '未登记', evidenceVersion: outcome.evidence?.version || '—', capturedAt: outcome.evidence?.capturedAt || outcome.at || '—' }); const softwareEvidence = outcome?.business === '软件开发' ? current.softwareAcceptance?.evidenceRef : ''; const summary = outcome ? `业务：${outcome.business}\n状态：${outcome.status}\n价值：¥${Number(outcome.value || 0).toLocaleString()}\n来源：${outcome.source || 'CEO 手动回传'}\n证据：${outcome.evidenceRef || softwareEvidence || '未登记'}\n${runLabelForState(current, outcome.runId, outcome.runIds)}\n参与 AI：${(outcome.contributors || []).map(item => item.agent).join('、') || outcome.agent || '未登记'}${outcome.allocationStatus === 'pending_review' ? '\n贡献分配：待 CEO 确认' : outcome.allocationNote ? `\n贡献说明：${outcome.allocationNote}` : ''}` : '已保留原始输入、负责人、版本和验证证据。复用时会把当前业务上下文一并带入。'; openFormDialog({ title: detail.dataset.assetTitle || '成果详情', description: '查看这份成果的来源、版本关系和可复用边界。', submitLabel: '知道了', fields: [{ name: 'summary', label: '当前记录', type: 'textarea', value: summary }] }); } });
  }

  function initKnowledgePage() {
    const root = document.querySelector('[data-knowledge-page]');
    if (!root || root.dataset.curisBound === 'true') return;
    root.dataset.curisBound = 'true';
    const seeded = [];
    const stateItems = Array.isArray(readState().knowledgeItems) ? readState().knowledgeItems : [];
    let items = [...seeded, ...stateItems];
    const list = root.querySelector('[data-knowledge-list]');
    const search = root.querySelector('[data-knowledge-search]');
    const count = root.querySelector('[data-knowledge-count]');
    const sourceCount = root.querySelector('[data-knowledge-source-count]');
    const knowledgeReturn = readState();
    const contextKey = knowledgeReturn.knowledgeReturnContext || knowledgeReturn.knowledgeReturnRoute || 'company';
    const returnRoute = knowledgeReturn.knowledgeReturnRoute || '';
    let connections = Array.isArray(readState().knowledgeConnections) ? readState().knowledgeConnections : [];
    const sourceList = root.querySelector('.source');
    const contextBar = document.createElement('section');
    contextBar.className = 'curis-knowledge-context-bar';
    contextBar.innerHTML = '<div><strong>当前工作流引用</strong><span data-knowledge-context-copy>尚未选择资料；引用后会保留来源和版本。</span></div><button type="button" data-knowledge-return>返回当前工作流</button>';
    const contextAnchor = root.querySelector('.search') || list;
    contextAnchor?.parentNode.insertBefore(contextBar, contextAnchor);
    const style = document.createElement('style');
    style.id = 'curis-knowledge-context-style';
    style.textContent = '.curis-knowledge-context-bar{display:flex;align-items:center;justify-content:space-between;gap:14px;margin:0 0 12px;padding:11px 13px;border:1px solid var(--line,rgba(0,0,0,.12));border-radius:8px;background:var(--surface-subtle,rgba(0,0,0,.025));font-size:11px}.curis-knowledge-context-bar strong{display:block;color:var(--text,#17181b);font-size:12px}.curis-knowledge-context-bar span{display:block;margin-top:3px;color:var(--muted,#777);line-height:1.4}.curis-knowledge-context-bar button{padding:6px 8px;border:1px solid var(--line,rgba(0,0,0,.16));border-radius:6px;background:transparent;color:inherit;font:inherit;cursor:pointer;white-space:nowrap}.curis-knowledge-context-bar button[hidden]{display:none}.curis-knowledge-source-actions{display:flex;align-items:center;gap:8px}.curis-knowledge-source-actions button{padding:5px 7px;font-size:10px}.curis-knowledge-source-actions button[hidden]{display:none}';
    document.head.appendChild(style);
    const renderConnections = () => {
      if (!sourceList) return;
      sourceList.querySelectorAll('[data-knowledge-connection], [data-knowledge-empty]').forEach(node => node.remove());
      sourceList.querySelectorAll(':scope > .source-item').forEach(node => node.remove());
      connections.slice(-12).forEach(connection => {
        const row = document.createElement('div');
        row.className = 'source-item';
        row.dataset.knowledgeConnection = connection.id;
        row.innerHTML = '<div><strong></strong><span></span></div><div class="curis-knowledge-source-actions"><span class="status"></span><button type="button" data-knowledge-confirm>确认读取</button></div>';
        row.querySelector('strong').textContent = connection.source;
        row.querySelector('span').textContent = `${connection.scope || '自定义读取范围'} · CEO 登记`;
        const status = row.querySelector('.status');
        const confirm = row.querySelector('[data-knowledge-confirm]');
        const connected = connection.status === 'connected';
        status.textContent = connected ? '已连接' : '待确认';
        status.classList.toggle('warn', !connected);
        confirm.hidden = connected;
        sourceList.appendChild(row);
      });
      if (!connections.length) { const empty = document.createElement('p'); empty.dataset.knowledgeEmpty = 'true'; empty.className = 'note'; empty.textContent = '还没有已连接的外部知识来源。可以先导入本地资料，或登记一个只读连接。'; sourceList.appendChild(empty); }
      if (sourceCount) sourceCount.textContent = String(connections.filter(item => item.status === 'connected').length);
      const pending = root.querySelector('[data-knowledge-pending]');
      if (pending) pending.textContent = String(connections.filter(item => item.status !== 'connected').length || '—');
      const summary = root.querySelectorAll('.summary .metric');
      summary[2]?.querySelector('small')?.replaceChildren(document.createTextNode(connections.length ? '外部来源已登记' : '等待外部来源'));
    };
    renderConnections();
    const renderContext = () => {
      const state = readState();
      const selected = state.knowledgeContextByContext?.[contextKey] || [];
      const copy = contextBar.querySelector('[data-knowledge-context-copy]');
      if (copy) copy.textContent = selected.length ? `已引用 ${selected.length} 份：${selected.slice(-3).join('、')}。AI 会在当前步骤中带上这些资料。` : '尚未选择资料；引用后会保留来源和版本。';
      const back = contextBar.querySelector('[data-knowledge-return]');
      if (back) back.hidden = contextKey === 'company';
    };
    const render = () => {
      const active = root.querySelector('[data-knowledge-filter].active')?.dataset.knowledgeFilter || '全部';
      const query = (search?.value || '').trim().toLowerCase();
      const filtered = items.filter(item => (active === '全部' || item.type === active) && (!query || `${item.title}${item.note}${item.source}`.toLowerCase().includes(query)));
      const selected = readState().knowledgeContextByContext?.[contextKey] || [];
      list.innerHTML = filtered.length ? filtered.map(item => { const used = selected.includes(item.title); return `<article class="knowledge-row"><div class="knowledge-main"><span class="knowledge-type">${escapeHtml(item.type)}</span><h3>${escapeHtml(item.title)}</h3><p>${escapeHtml(item.note)} · 来源：${escapeHtml(item.source)}</p></div><div class="knowledge-actions"><button type="button" data-knowledge-use="${escapeHtml(item.title)}">${used ? '已引用' : '引用'}</button><button type="button" data-knowledge-detail="${escapeHtml(item.title)}">来源</button></div></article>`; }).join('') : '<p class="note">没有匹配资料。可以导入一份新资料，或换一个筛选条件。</p>';
      if (count) count.textContent = String(items.length || '—');
      const summary = root.querySelectorAll('.summary .metric');
      summary[1]?.querySelector('strong')?.replaceChildren(document.createTextNode(items.length ? String(items.filter(item => item.updatedAt || item.at).length) : '—'));
      summary[1]?.querySelector('small')?.replaceChildren(document.createTextNode(items.length ? '已有更新时间记录' : '导入资料后统计'));
      renderContext();
    };
    const openImport = () => openFormDialog({ title: '导入公司资料', description: '支持文档、链接、图片或视频。导入后先记录来源和引用范围，之后才会被 AI 使用。', submitLabel: '保存资料', fields: [{ name: 'title', label: '资料名称', placeholder: '例如：竞品账号 7 月内容拆解', required: true }, { name: 'type', label: '资料类型', type: 'select', options: ['竞品', '平台规则', '内容素材', '研发', '公司知识'] }, { name: 'source', label: '来源', placeholder: '例如：本地文件 / 网页链接 / Notion', required: true }, { name: 'note', label: '说明与引用范围', type: 'textarea', placeholder: '例如：允许小红书和抖音工作空间引用；只读。' }], onSubmit: values => { items = [...items, values]; writeState({ knowledgeItems: items.slice(-80).filter(item => !seeded.includes(item)), lastAssistantMessage: `资料“${values.title}”已进入知识库。使用时会带上来源和引用范围。` }); render(); showToast('资料已加入知识库'); } });
    const openConnect = () => openFormDialog({ title: '连接外部知识库', description: '连接只建立读取入口，不会自动上传或修改外部资料。首次使用会明确权限和引用范围。', submitLabel: '保存连接', fields: [{ name: 'source', label: '知识库名称', placeholder: '例如：Notion 工作区 / 网页收藏 / 视频素材盘', required: true }, { name: 'scope', label: '读取范围', type: 'textarea', placeholder: '例如：只读“竞品研究”和“平台规则”两个目录', required: true }], onSubmit: values => { const record = { id: `knowledge-source-${Date.now()}`, ...values, status: 'pending', at: new Date().toISOString() }; connections = [...connections, record].slice(-12); const current = readState(); writeState({ knowledgeConnections: connections, knowledgeSourceCount: connections.length, knowledgeLastConnection: record, lastAssistantMessage: `外部知识库“${values.source}”已登记，等待 CEO 确认读取范围。` }); renderConnections(); showToast('外部知识库已登记，等待确认读取范围'); } });
    root.querySelectorAll('[data-knowledge-action]').forEach(button => button.addEventListener('click', () => { const action = button.dataset.knowledgeAction; if (action === 'import') openImport(); else if (action === 'connect') openConnect(); else if (action === 'search') render(); }));
    root.querySelectorAll('[data-knowledge-filter]').forEach(button => button.addEventListener('click', () => { root.querySelectorAll('[data-knowledge-filter]').forEach(item => item.classList.toggle('active', item === button)); render(); }));
    search?.addEventListener('input', render);
    contextBar.querySelector('[data-knowledge-return]')?.addEventListener('click', () => { const route = readState().knowledgeReturnRoute || returnRoute; if (route && route !== 'company') { writeState({ knowledgeReturnRoute: null, knowledgeReturnContext: null, lastAssistantMessage: '引用资料已带回原工作流，来源和版本关系保持不变。' }); window.location.href = route; } });
    root.addEventListener('click', event => { const use = event.target.closest('[data-knowledge-use]'); const detail = event.target.closest('[data-knowledge-detail]'); const confirm = event.target.closest('[data-knowledge-confirm]'); if (confirm) { const row = confirm.closest('[data-knowledge-connection]'); const connection = connections.find(item => item.id === row?.dataset.knowledgeConnection); if (!connection) return; connection.status = 'connected'; writeState({ knowledgeConnections: connections, lastAssistantMessage: `已确认“${connection.source}”的读取范围；后续引用会保留来源和版本。` }); renderConnections(); showToast('读取范围已确认，知识库已连接'); return; } if (use) { const title = use.dataset.knowledgeUse; const current = readState(); const byContext = { ...(current.knowledgeContextByContext || {}) }; const selected = Array.isArray(byContext[contextKey]) ? byContext[contextKey] : []; byContext[contextKey] = selected.includes(title) ? selected.filter(item => item !== title) : [...selected, title].slice(-20); writeState({ knowledgeContextByContext: byContext, lastKnowledgeUsed: title, lastAssistantMessage: byContext[contextKey].includes(title) ? `“${title}”已加入当前工作流引用范围。` : `已从当前工作流移除“${title}”。` }); render(); showToast(byContext[contextKey].includes(title) ? `“${title}”已加入当前工作流上下文` : `已移除“${title}”`); } if (detail) showToast(`已打开“${detail.dataset.knowledgeDetail}”的原始来源与引用记录`); });
    render();
  }

  function initFinancePage() {
    const root = document.querySelector('[data-finance-page]');
    if (!root || root.dataset.curisFinanceBound === 'true') return;
    root.dataset.curisFinanceBound = 'true';
    const entry = root.querySelector('[data-finance-entry]');
    const currentState = readState();
    let costs = Array.isArray(currentState.financeCosts) ? currentState.financeCosts : [];
    let revenues = Array.isArray(currentState.financeRevenueRecords) ? currentState.financeRevenueRecords : [];
    const totalRevenue = () => revenues.filter(item => item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0);
    const normalizeBusiness = value => /小红书/.test(String(value || '')) ? '小红书运营' : /抖音|TikTok|短视频/.test(String(value || '')) ? '抖音 / TikTok 运营' : /软件|Curis 自研|研发/.test(String(value || '')) ? '软件开发' : '公司共享';
    const portfolioRoutes = { '软件开发': 'workspace-runtime-software.html', '小红书运营': 'workspace-runtime-xhs.html', '抖音 / TikTok 运营': 'workspace-runtime-shortvideo.html' };
    const portfolio = document.createElement('section');
    portfolio.className = 'card curis-portfolio-compare';
    portfolio.setAttribute('aria-labelledby', 'curis-portfolio-compare-title');
    portfolio.innerHTML = '<div class="curis-portfolio-head"><div><p class="curis-portfolio-kicker">公司业务版图 · 同一经营口径</p><h2 id="curis-portfolio-compare-title">公司现在把时间和成本用在哪里？</h2><p>横向比较真实结果、投入、AI 运行和下一步动作；没有结果的业务会明确显示“待产生”，不会用估算掩盖空白。</p></div><button type="button" data-portfolio-route>打开业务版图</button></div><div class="curis-portfolio-grid"></div>';
    const renderPortfolio = () => {
      const state = readState();
      const businesses = ['软件开发', '小红书运营', '抖音 / TikTok 运营'];
      const firstBusiness = String(state.firstBusiness || '');
      const activeBusinesses = !state.companyCreatedAt ? [] : businesses.filter(business => business === '软件开发' && /软件|Curis|研发/.test(firstBusiness) || business === '小红书运营' && /小红书/.test(firstBusiness) || business === '抖音 / TikTok 运营' && /抖音|TikTok|短视频/.test(firstBusiness));
      const stateCosts = Array.isArray(state.financeCosts) ? state.financeCosts : [];
      const allCosts = stateCosts;
      const outcomes = Array.isArray(state.outcomeAttributions) ? state.outcomeAttributions : [];
      const rows = activeBusinesses.map(business => {
        const businessOutcomes = outcomes.filter(item => normalizeBusiness(item.business) === business);
        const verified = businessOutcomes.filter(item => item.status === '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
        const pending = businessOutcomes.filter(item => item.status !== '已验证价值').reduce((sum, item) => sum + Number(item.value || 0), 0);
        const cost = allCosts.filter(item => normalizeBusiness(item.business) === business).reduce((sum, item) => sum + Number(item.amount || 0), 0);
        const revenue = (Array.isArray(state.financeRevenueRecords) ? state.financeRevenueRecords : []).filter(item => item.status !== '待确认' && normalizeBusiness(item.business) === business).reduce((sum, item) => sum + Number(item.amount || 0), 0);
        const runs = (state.calendarEvents || []).filter(item => normalizeBusiness(item.business) === business || normalizeBusiness(item.route) === business);
        const activeRuns = runs.filter(item => ['waiting_ceo', 'acknowledged'].includes(item.status)).length;
        const latest = business === '小红书运营' ? state.latestXhsFeedback : business === '抖音 / TikTok 运营' ? state.latestExternalFeedback : state.softwareAcceptance;
        const decision = state.businessDecision && ((business === '小红书运营' && state.businessDecision.platform === '小红书') || (business === '抖音 / TikTok 运营' && state.businessDecision.platform === '抖音 / TikTok')) ? state.businessDecision : null;
        const status = decision?.choice === 'pause' ? '已暂停' : verified > 0 ? '已验证价值' : pending > 0 || latest ? '待复盘' : '运行中';
        const signal = business === '小红书运营' ? (latest ? `阅读 ${Number(latest.reads || 0).toLocaleString()} · 粉丝 ${Number(latest.follows || 0).toLocaleString()}` : '等待首条平台结果') : business === '抖音 / TikTok 运营' ? (latest ? `播放 ${Number(latest.plays || 0).toLocaleString()} · 成交 ${Number(latest.orders || 0).toLocaleString()}` : '等待首条平台结果') : (latest ? `${latest.label || '验收结果'} · ${latest.evidenceRef || '证据待补充'}` : '等待 CEO 首次验收');
        return { business, route: portfolioRoutes[business], verified, pending, cost, revenue, roi: cost && verified ? `${(verified / cost).toFixed(1)}x` : '—', activeRuns, status, signal, outcome: businessOutcomes.sort((a, b) => String(b.at || '').localeCompare(String(a.at || '')))[0] };
      });
      portfolio.querySelector('.curis-portfolio-grid').innerHTML = rows.map(row => `<article class="curis-portfolio-row"><div class="curis-portfolio-row-head"><div><h3>${escapeHtml(row.business)}</h3><p>${escapeHtml(row.signal)}</p></div><span>${escapeHtml(row.status)}</span></div><div class="curis-portfolio-row-metrics"><div><small>已验证价值</small><strong>¥${row.verified.toLocaleString()}</strong></div><div><small>待验证价值</small><strong>¥${row.pending.toLocaleString()}</strong></div><div><small>投入成本</small><strong>¥${row.cost.toLocaleString()}</strong></div><div><small>ROI</small><strong>${escapeHtml(row.roi)}</strong></div><div><small>可确认收入</small><strong>¥${row.revenue.toLocaleString()}</strong></div><div><small>待 CEO 处理</small><strong>${row.activeRuns} 次</strong></div></div><div class="curis-portfolio-row-foot"><span>${row.status === '已验证价值' ? '可以进入下一次投入判断' : row.status === '待复盘' ? '先复盘结果，再决定是否扩大' : '继续积累第一条可验证结果'}</span><div><button type="button" data-portfolio-open="${escapeHtml(row.business)}">${row.status === '待复盘' ? '去复盘' : '打开业务'}</button><button type="button" data-portfolio-invest="${escapeHtml(row.business)}">调整投入</button></div></div></article>`).join('');
      portfolio.querySelectorAll('[data-portfolio-open]').forEach(button => button.addEventListener('click', () => { const business = button.dataset.portfolioOpen; writeState({ lastAssistantMessage: `${business}已从公司业务版图打开，CEO 助理会带上当前价值和下一检查点。`, lastAssistantHandoff: { label: business, route: portfolioRoutes[business], message: rowForPortfolioStatus(rows, business) } }); window.location.href = portfolioRoutes[business]; }));
      portfolio.querySelectorAll('[data-portfolio-invest]').forEach(button => button.addEventListener('click', () => { const business = button.dataset.portfolioInvest; openFormDialog({ title: `调整${business}投入`, description: '投入判断会保留理由、检查点和下一次回报，不会直接删除已有成果。', submitLabel: '保存投入判断', fields: [{ name: 'choice', label: '下一步', type: 'select', options: ['继续当前投入', '增加投入', '减少投入', '暂停新增投入'] }, { name: 'checkpoint', label: '下一检查点', placeholder: '例如：3 天后回收结果', required: true }, { name: 'reason', label: '判断依据', type: 'textarea', placeholder: '例如：当前 ROI 尚未验证，但成本可控，继续观察一轮。', required: true }], onSubmit: values => { const current = readState(); const actions = Array.isArray(current.portfolioInvestmentDecisions) ? current.portfolioInvestmentDecisions : []; const record = { business, ...values, at: new Date().toISOString() }; writeState({ portfolioInvestmentDecisions: [...actions, record].slice(-24), lastAssistantMessage: `${business}已记录“${values.choice}”，下一检查点：${values.checkpoint}。`, lastAssistantHandoff: { label: business === '软件开发' ? '研发办公室' : '经营办公室', route: business === '软件开发' ? portfolioRoutes[business] : 'operating.html', message: '投资判断已记录' } }); renderPortfolio(); showToast('投入判断已保存'); } }); }));
    };
    const rowForPortfolioStatus = (rows, business) => rows.find(item => item.business === business)?.status || '已记录';
    const portfolioStyle = document.createElement('style');
    portfolioStyle.textContent = '.curis-portfolio-compare{margin:16px 0}.curis-portfolio-head{display:flex;align-items:flex-start;justify-content:space-between;gap:18px}.curis-portfolio-kicker{margin:0 0 5px;color:var(--text-secondary,#a4a7af);font-size:10px;letter-spacing:.08em}.curis-portfolio-head h2{margin:0;font-size:16px;letter-spacing:-.02em}.curis-portfolio-head p{max-width:700px;margin:6px 0 0;color:var(--text-secondary,#a4a7af);font-size:11px;line-height:1.5}.curis-portfolio-head button,.curis-portfolio-row-foot button{padding:7px 9px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer;white-space:nowrap}.curis-portfolio-head button:hover,.curis-portfolio-row-foot button:hover{background:var(--bg-overlay-l2,rgba(224,226,242,.06))}.curis-portfolio-grid{display:grid;gap:8px;margin-top:15px}.curis-portfolio-row{padding:12px;border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:8px;background:var(--bg-base-default,#191a1d)}.curis-portfolio-row-head{display:flex;align-items:flex-start;justify-content:space-between;gap:12px}.curis-portfolio-row-head h3{margin:0;font-size:12px}.curis-portfolio-row-head p{margin:4px 0 0;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-portfolio-row-head>span{padding:4px 6px;color:var(--text-secondary,#a4a7af);border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:5px;font-size:10px;white-space:nowrap}.curis-portfolio-row-metrics{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:1px;margin-top:10px;background:var(--border-neutral-l1,rgba(224,226,242,.1));border:1px solid var(--border-neutral-l1,rgba(224,226,242,.1));border-radius:6px;overflow:hidden}.curis-portfolio-row-metrics>div{display:grid;gap:4px;padding:8px;background:var(--bg-base-secondary,#202226)}.curis-portfolio-row-metrics small{color:var(--text-secondary,#a4a7af);font-size:9px}.curis-portfolio-row-metrics strong{font-size:13px}.curis-portfolio-row-foot{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:10px;color:var(--text-secondary,#a4a7af);font-size:10px}.curis-portfolio-row-foot>div{display:flex;gap:6px}.curis-portfolio-row-foot button:first-child{color:var(--primary-foreground,#17181a);background:var(--primary,#d9dbe1);border-color:var(--primary,#d9dbe1);font-weight:600}@media(max-width:900px){.curis-portfolio-row-metrics{grid-template-columns:repeat(3,minmax(0,1fr))}}@media(max-width:620px){.curis-portfolio-head,.curis-portfolio-row-foot{align-items:flex-start;flex-direction:column}.curis-portfolio-head button,.curis-portfolio-row-foot button{width:100%}.curis-portfolio-row-foot>div{width:100%}.curis-portfolio-row-foot>div button{flex:1}.curis-portfolio-row-metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}';
    document.head.appendChild(portfolioStyle);
    portfolio.querySelector('[data-portfolio-route]').addEventListener('click', () => { writeState({ lastAssistantMessage: '已打开公司业务版图，CEO 可以查看每条业务的承诺、结果和下一检查点。', lastAssistantHandoff: { label: '业务版图', route: 'business.html', message: '查看公司业务版图' } }); window.location.href = 'business.html'; });
    const summary = root.querySelector('.summary');
    summary?.parentNode.insertBefore(portfolio, summary.nextSibling);
    renderPortfolio();
    window.addEventListener('curis-state-changed', renderPortfolio);
    const details = document.createElement('section');
    details.className = 'grid curis-finance-detail';
    details.innerHTML = `<section class="card"><div class="curis-finance-detail-head"><div><h2>成本结构</h2><p class="card-note">成本不只包含模型调用，也包含广告投流、平台服务、工具订阅和人工支出。</p></div><button type="button" data-finance-action="cost">记录成本</button></div><div data-finance-cost-list></div><div class="curis-finance-total"><span>当前周期总成本</span><strong data-finance-total></strong></div></section><section class="card"><h2>业务价值构成</h2><p class="card-note">收入只是结果的一部分；浏览、互动、粉丝、收藏、线索和节省时间都应进入价值账。</p><div class="curis-value-list"><div><span>外部收入</span><strong data-finance-value="revenue">—</strong><small>尚无已确认回款</small></div><div><span>内容增长</span><strong data-finance-value="content">—</strong><small>等待平台结果或 CEO 补录</small></div><div><span>研发效率</span><strong data-finance-value="software">—</strong><small>等待软件验收与价值归因</small></div><div><span>有效资产</span><strong data-finance-value="assets">—</strong><small>等待已验证成果</small></div></div><div class="curis-value-breakdown" aria-label="增长价值明细"><div><span>总播放</span><strong data-finance-breakdown="plays">—</strong><small>等待平台回传</small></div><div><span>点赞与收藏</span><strong data-finance-breakdown="engagement">—</strong><small>等待平台回传</small></div><div><span>新增粉丝</span><strong data-finance-breakdown="follows">—</strong><small>等待平台回传</small></div><div><span>有效线索</span><strong data-finance-breakdown="leads">—</strong><small>等待 CEO 确认</small></div><div><span>节省时间</span><strong data-finance-breakdown="hours">—</strong><small>等待研发验收</small></div><div><span>复用资产</span><strong data-finance-breakdown="assets">—</strong><small>等待成果入库</small></div></div><p class="curis-finance-note">价值口径由 CEO 确认；估算值会标记来源和可信度，不会与平台原始数据混在一起。</p></section>`;
    const anchor = root.querySelector('.grid') || root.querySelector('.summary');
    anchor?.parentNode.insertBefore(details, anchor.nextSibling);
    const revenueCard = document.createElement('section');
    revenueCard.className = 'card curis-finance-revenue-card';
    revenueCard.innerHTML = '<div class="curis-finance-detail-head"><div><h2>收入与回款</h2><p class="card-note">每笔收入都保留业务、来源和确认状态，避免把估算当成已到账。</p></div><button type="button" data-finance-action="record">补录收入</button></div><div data-finance-revenue-list></div><div class="curis-finance-total"><span>本周期可确认收入</span><strong data-finance-revenue-total></strong></div>';
    details.insertBefore(revenueCard, details.firstChild);
    const capacityPlan = currentState.financeCapacityPlan;
    if (capacityPlan) {
      const plan = document.createElement('section');
      plan.className = 'card curis-finance-capacity-plan';
      const status = capacityPlan.status === 'approved' ? '已批准' : '暂缓';
      plan.innerHTML = `<div class="curis-finance-detail-head"><div><h2>扩容预算</h2><p class="card-note">扩容预算独立于已发生成本；只有实际运行后才进入本周期成本。</p></div><button type="button" data-capacity-plan-route="true">查看 AI 组织</button></div><div class="plan-grid"><span>业务 <strong></strong></span><span>状态 <strong></strong></span><span>预计新增 <strong></strong></span><span>运行节奏 <strong></strong></span><span>交接 <strong></strong></span></div>`;
      plan.querySelector('.plan-grid span:nth-child(1) strong').textContent = capacityPlan.businessTitle || '当前业务';
      plan.querySelector('.plan-grid span:nth-child(2) strong').textContent = status;
      plan.querySelector('.plan-grid span:nth-child(3) strong').textContent = `¥${Number(capacityPlan.incrementalCost || 0).toLocaleString()} / 周期`;
      plan.querySelector('.plan-grid span:nth-child(4) strong').textContent = capacityPlan.schedule || '维持现状';
      plan.querySelector('.plan-grid span:nth-child(5) strong').textContent = capacityPlan.handoff || '待配置';
      plan.querySelector('[data-capacity-plan-route]').addEventListener('click', () => { window.location.href = 'ai-organization.html'; });
      details.appendChild(plan);
    }
    const performance = document.createElement('section');
    performance.className = 'card curis-finance-agent-performance';
    performance.innerHTML = '<h2>AI 员工运行绩效</h2><p class="card-note">把运行、结果价值和成本放在同一条经营链路里；协作结果先由 CEO 分配贡献，再计入个人 KPI。</p><div class="curis-finance-agent-performance-list"></div><div class="curis-finance-agent-performance-reviews"></div>';
    details.appendChild(performance);
    const performanceStyle = document.createElement('style');
    performanceStyle.textContent = '.curis-finance-agent-performance-reviews{display:grid;gap:8px;margin-top:14px;padding-top:14px;border-top:1px solid var(--border-neutral-l1,rgba(224,226,242,.1))}.curis-finance-agent-performance-review-title{color:var(--text-secondary,#a4a7af);font-size:11px}.curis-finance-agent-performance-review{display:flex;align-items:center;justify-content:space-between;gap:10px;color:var(--text-secondary,#a4a7af);font-size:11px}.curis-finance-agent-performance-review button{padding:6px 8px;color:var(--text-default,#e2e3e7);background:transparent;border:1px solid var(--border-neutral-l2,rgba(224,226,242,.16));border-radius:6px;font:inherit;font-size:10px;cursor:pointer}';
    document.head.appendChild(performanceStyle);
    const renderPerformance = () => {
      const state = readState();
      const runs = (state.calendarEvents || []).filter(item => item.owner);
      const outcomes = Array.isArray(state.outcomeAttributions) ? state.outcomeAttributions : [];
      const grouped = {};
      const pendingReviews = [];
      const makeGroup = model => ({ count: 0, cost: 0, value: 0, pendingValue: 0, pendingAllocation: 0, outcomes: 0, collaborations: 0, model: model || '模型未登记', pending: 0 });
      const groupFor = (key, model) => { grouped[key] = grouped[key] || makeGroup(model); return grouped[key]; };
      runs.forEach(run => {
        const key = run.capability?.agent || run.owner || '未指定负责人';
        const current = groupFor(key, run.capability?.model || '模型未登记');
        current.count += 1;
        current.cost += Number(run.cost || 0);
        if (['waiting_ceo', 'acknowledged'].includes(run.status)) current.pending += 1;
      });
      outcomes.forEach(outcome => {
        const value = Number(outcome.value || 0);
        const contributors = Array.isArray(outcome.contributors) ? outcome.contributors : [];
        if (outcome.status === '已验证价值' && outcome.allocationStatus === 'pending_review' && contributors.length > 1) {
          const current = groupFor('协作结果 · 待 CEO 分配', '多员工协作');
          current.pendingAllocation += value;
          current.outcomes += 1;
          pendingReviews.push(outcome);
          return;
        }
        if (outcome.status === '已验证价值') {
          const allocations = Array.isArray(outcome.allocation) && outcome.allocation.length ? outcome.allocation : [{ runId: outcome.runId, agent: outcome.agent, weight: 100 }];
          allocations.forEach((share, index) => {
            const contributor = contributors.find(item => item.runId === share.runId);
            const key = share.agent || contributor?.agent || outcome.agent || 'CEO 手动回传';
            const current = groupFor(key, contributor?.model || outcome.model || '手动录入');
            current.value += value * (Number(share.weight || 0) / 100);
            if (index === 0) current.outcomes += 1;
            else current.collaborations += 1;
          });
        } else {
          const current = groupFor(outcome.agent || 'CEO 手动回传', outcome.model || '手动录入');
          current.outcomes += 1;
          current.pendingValue += value;
          current.collaborations += Math.max(0, (outcome.runIds || []).filter(id => id !== 'manual').length - 1);
        }
      });
      const rows = Object.entries(grouped).sort((a, b) => ((b[1].value + b[1].pendingAllocation) - (a[1].value + a[1].pendingAllocation)) || (b[1].cost - a[1].cost));
      performance.querySelector('.curis-finance-agent-performance-list').innerHTML = rows.length
        ? rows.slice(0, 8).map(([agent, item]) => {
          const roi = item.cost > 0 && item.value > 0 ? ` · ROI ${(item.value / item.cost).toFixed(1)}x` : '';
          const pendingValue = item.pendingValue > 0 ? ` · 待验证 ¥${item.pendingValue.toLocaleString()}` : '';
          const pendingAllocation = item.pendingAllocation > 0 ? ` · 待分配 ¥${item.pendingAllocation.toLocaleString()}` : '';
          return `<div class="curis-finance-agent-performance-row"><span>${escapeHtml(agent)} · ${escapeHtml(item.model)} · ${item.count} 次运行${item.outcomes ? ` · ${item.outcomes} 条结果` : ''}${item.collaborations ? ` · 协作 ${item.collaborations} 次` : ''}${item.pending ? ` · ${item.pending} 次待 CEO` : ''}</span><strong>价值 ¥${item.value.toLocaleString()} · 成本 ¥${item.cost.toLocaleString()}${roi}${pendingValue}${pendingAllocation}</strong></div>`;
        }).join('')
        : '<div class="curis-finance-agent-performance-row"><span>还没有自动运行记录</span><strong>等待第一次运行</strong></div>';
      const reviewRoot = performance.querySelector('.curis-finance-agent-performance-reviews');
      if (reviewRoot) reviewRoot.innerHTML = pendingReviews.length ? `<div class="curis-finance-agent-performance-review-title">待分配的协作结果</div>${pendingReviews.map(outcome => `<div class="curis-finance-agent-performance-review"><span>${escapeHtml(outcome.business)} · ¥${Number(outcome.value || 0).toLocaleString()} · ${outcome.contributors.length} 位协作 AI</span><button type="button" data-outcome-review="${escapeHtml(outcome.id)}">分配贡献</button></div>`).join('')}` : '';
    };
    renderPerformance();
    window.addEventListener('curis-state-changed', renderPerformance);
    performance.addEventListener('click', event => {
      const button = event.target.closest('[data-outcome-review]');
      if (!button) return;
      const outcome = (readState().outcomeAttributions || []).find(item => item.id === button.dataset.outcomeReview);
      if (!outcome) return;
      const contributors = Array.isArray(outcome.contributors) ? outcome.contributors : [];
      openFormDialog({ title: '分配协作结果贡献', description: '贡献比例只用于 AI 员工 KPI 与复盘，不会改变这条业务结果的总价值。合计必须等于 100%。', submitLabel: '保存贡献分配', fields: contributors.map((item, index) => ({ name: `weight_${index}`, label: `${item.agent} · 贡献比例（%）`, type: 'number', placeholder: '例如：50', value: index === 0 ? 50 : '', required: true })).concat([{ name: 'note', label: 'CEO 说明', type: 'textarea', placeholder: '说明这次结果为什么这样分配。' }]), onSubmit: values => { const allocation = contributors.map((item, index) => ({ runId: item.runId, agent: item.agent, weight: Number(values[`weight_${index}`] || 0) })); const total = allocation.reduce((sum, item) => sum + item.weight, 0); if (Math.abs(total - 100) > 0.01 || allocation.some(item => item.weight < 0)) return showToast('贡献比例必须为非负数且合计 100%'); const current = readState(); const nextOutcome = { ...outcome, allocationStatus: 'reviewed', allocation, allocationNote: values.note || '', allocationAt: new Date().toISOString() }; writeState({ outcomeAttributions: (current.outcomeAttributions || []).map(item => item.id === outcome.id ? nextOutcome : item), lastOutcomeAttribution: nextOutcome, lastAssistantMessage: `已完成${outcome.business}这条协作结果的贡献分配，下一次 KPI 会按 CEO 确认的比例计算。` }); showToast('贡献分配已保存'); } });
    });
    const renderCosts = () => {
      const list = details.querySelector('[data-finance-cost-list]');
      const total = costs.reduce((sum, item) => sum + Number(item.amount || 0), 0);
      list.innerHTML = costs.length ? costs.slice(-8).map(item => `<div class="curis-cost-item"><div><strong>${escapeHtml(item.business)}</strong><span>${escapeHtml(item.category)} · ${escapeHtml(item.source)}${item.model || item.agent ? ` · ${escapeHtml(item.model || '模型未登记')} · ${escapeHtml(item.agent || '负责人未登记')}` : ''}</span></div><b>¥${Number(item.amount || 0).toLocaleString()}</b></div>`).join('') : '<p class="card-note">还没有真实成本记录；AI 运行后或 CEO 补录账单，成本才会进入本周期。</p>';
      details.querySelector('[data-finance-total]').textContent = `¥${total.toLocaleString()}`;
    };
    const renderRevenues = () => {
      const list = details.querySelector('[data-finance-revenue-list]');
      if (!list) return;
      list.innerHTML = revenues.length ? revenues.slice(-8).reverse().map(item => `<div class="curis-cost-item"><div><strong>${escapeHtml(item.business || '公司共享')}</strong><span>${escapeHtml(item.status || '待确认')} · ${escapeHtml(item.source || 'CEO 手动录入')}</span></div><b>¥${Number(item.amount || 0).toLocaleString()}</b></div>`).join('') : '<p class="card-note">还没有单笔回款记录；可以先补录一笔已确认收入。</p>';
      const total = revenues.filter(item => item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0);
      details.querySelector('[data-finance-revenue-total]').textContent = `¥${total.toLocaleString()}`;
    };
    const openCost = () => openFormDialog({ title: '记录一笔经营成本', description: '广告、投流、平台服务和人工支出都要带来源；保存后会进入当前周期成本账。', submitLabel: '保存成本', fields: [{ name: 'business', label: '所属业务', type: 'select', options: ['Curis 自研', '小红书运营', '抖音 / TikTok', '公司共享'] }, { name: 'category', label: '成本类型', type: 'select', options: ['模型与调用', '广告 / 投流', '平台服务', '工具订阅', '人工支出', '其他'] }, { name: 'amount', label: '金额（元）', type: 'number', placeholder: '例如：1200', required: true }, { name: 'source', label: '来源', placeholder: '例如：平台后台 / 发票 / 账单', required: true }], onSubmit: values => { const amount = Number(values.amount); if (!Number.isFinite(amount) || amount < 0) return showToast('请输入有效金额'); const record = { ...values, amount, at: new Date().toISOString() }; costs = [...costs, record]; writeState({ financeCosts: [...(readState().financeCosts || []), record].slice(-40), lastAssistantMessage: `已记录${values.business}的${values.category}成本 ¥${amount.toLocaleString()}，我会在下一次经营简报里同步 ROI。` }); renderCosts(); showToast('成本已记录，经营账已更新'); } });
    root.addEventListener('click', event => { const button = event.target.closest('[data-finance-action]'); if (!button) return; const action = button.dataset.financeAction; if (action === 'record') openFormDialog({ title: '补录收入', description: '按业务记录一笔回款；待确认数据会保留状态，不会直接算进可确认收入。', submitLabel: '保存收入', fields: [{ name: 'business', label: '所属业务', type: 'select', options: ['Curis 自研', '小红书运营', '抖音 / TikTok 运营', '公司共享'] }, { name: 'amount', label: '金额（元）', type: 'number', placeholder: '例如：8600', required: true }, { name: 'status', label: '确认状态', type: 'select', options: ['已确认到账', '待确认'] }, { name: 'source', label: '来源', placeholder: '例如：订单记录 / 客户回款 / 平台后台', required: true }], onSubmit: values => { const amount = Number(values.amount); if (!Number.isFinite(amount) || amount < 0) return showToast('请输入有效金额'); const record = { ...values, amount, at: new Date().toISOString() }; revenues = [...revenues, record].slice(-40); const confirmed = revenues.filter(item => item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0); writeState({ financeRevenueRecords: revenues, financeManualRevenue: confirmed || amount, financeManualRevenueSource: values.source, lastAssistantMessage: `已记录${values.business}回款 ¥${amount.toLocaleString()}，状态：${values.status}。经营简报会按确认状态计算。` }); if (entry) entry.textContent = `已补录 ¥${amount.toLocaleString()} · ${values.status}`; renderRevenues(); showToast('收入已记录，经营账已更新'); } }); else if (action === 'cost') openCost(); else if (action === 'brief') { const current = readState(); const xhs = summarizeOutcomeValue(current, '小红书运营', 0, current.latestXhsFeedback); const shortVideo = summarizeOutcomeValue(current, '抖音 / TikTok 运营', 0, current.latestExternalFeedback); const software = summarizeOutcomeValue(current, '软件开发', 0, current.softwareAcceptance?.choice === 'accept' ? { status: '已验证价值', value: Number(current.softwareAcceptance.value || 0) } : current.softwareAcceptance ? { status: '数据待验证', value: 0 } : null); const brief = { revenue: totalRevenue(), cost: costs.reduce((sum, item) => sum + Number(item.amount || 0), 0), value: xhs.verified + shortVideo.verified + software.verified, pendingValue: xhs.pending + shortVideo.pending + software.pending, at: new Date().toISOString() }; writeState({ financeBrief: brief, lastAssistantMessage: `本周期财务简报已准备：收入 ¥${brief.revenue.toLocaleString()} · 成本 ¥${brief.cost.toLocaleString()} · 已验证价值 ¥${brief.value.toLocaleString()}${brief.pendingValue ? ` · 待验证 ¥${brief.pendingValue.toLocaleString()}` : ''}。`, lastAssistantHandoff: { label: 'CEO 工作台', route: 'ceo-desk.html', message: '财务简报已准备' } }); showToast('CEO 财务简报已准备，可回到工作台查看'); } else if (action === 'assets') window.location.href = 'assets.html'; });
    renderCosts();
    renderRevenues();
  }

  function initFinanceSummary() {
    const root = document.querySelector('[data-finance-page]');
    if (!root || root.dataset.curisFinanceSummaryBound === 'true') return;
    root.dataset.curisFinanceSummaryBound = 'true';
    const metrics = root.querySelectorAll('.summary .metric');
    const setText = (node, value) => { if (node && node.textContent !== value) node.textContent = value; };
    const update = () => {
      if (metrics.length < 5) return;
      const state = readState();
      const costs = Array.isArray(state.financeCosts) ? state.financeCosts : [];
      const total = costs.reduce((sum, item) => sum + Number(item.amount || 0), 0);
      const aiCost = costs.filter(item => item.category === '模型与调用').reduce((sum, item) => sum + Number(item.amount || 0), 0);
      const revenueRecords = Array.isArray(state.financeRevenueRecords) ? state.financeRevenueRecords : [];
      const confirmedRevenue = revenueRecords.filter(item => item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0);
      const revenue = confirmedRevenue;
      const xhs = summarizeOutcomeValue(state, '小红书运营', 0, state.latestXhsFeedback);
      const shortVideo = summarizeOutcomeValue(state, '抖音 / TikTok 运营', 0, state.latestExternalFeedback);
      const software = summarizeOutcomeValue(state, '软件开发', 0, state.softwareAcceptance?.choice === 'accept' ? { status: '已验证价值', value: Number(state.softwareAcceptance.value || 0) } : null);
      const xhsValue = xhs.verified;
      const shortVideoValue = shortVideo.verified;
      const softwareValue = software.verified;
      const pendingValue = xhs.pending + shortVideo.pending + software.pending;
      const totalValue = xhsValue + shortVideoValue + softwareValue;
      const pendingItems = revenueRecords.filter(item => item.status === '待确认').length + (state.outcomeAttributions || []).filter(item => item.status !== '已验证价值').length + (state.calendarEvents || []).filter(item => item.requiresCEO && !['resolved', 'completed'].includes(item.status)).length;
      const plays = Number(state.latestExternalFeedback?.plays || 0);
      const likes = Number(state.latestExternalFeedback?.likes || 0) + Number(state.latestXhsFeedback?.likes || 0);
      const saves = Number(state.latestXhsFeedback?.saves || 0);
      const follows = Number(state.latestExternalFeedback?.follows || 0) + Number(state.latestXhsFeedback?.follows || 0);
      const leads = Number(state.latestXhsFeedback?.leads || 0) + Number(state.latestExternalFeedback?.leads || 0);
      const margin = revenue ? `${(((revenue - total) / revenue) * 100).toFixed(1)}%` : '—';
      setText(metrics[0].querySelector('strong'), revenue ? `¥${revenue.toLocaleString()}` : '—');
      setText(metrics[0].querySelector('small'), revenue ? '本周期 · 已确认回款' : '尚无已确认回款');
      setText(metrics[1].querySelector('span'), '本周期总成本');
      setText(metrics[1].querySelector('strong'), total ? `¥${total.toLocaleString()}` : '—');
      setText(metrics[1].querySelector('small'), total ? `AI ¥${aiCost.toLocaleString()} · 投流/其他 ¥${(total - aiCost).toLocaleString()}` : '等待真实运行记录');
      setText(metrics[2].querySelector('span'), '总价值');
      setText(metrics[2].querySelector('strong'), totalValue ? `¥${totalValue.toLocaleString()}` : '—');
      setText(metrics[2].querySelector('small'), totalValue || pendingValue ? `已验证：外部结果 ¥${(xhsValue + shortVideoValue).toLocaleString()} · 研发效率 ¥${softwareValue.toLocaleString()}${pendingValue ? ` · 待验证 ¥${pendingValue.toLocaleString()}` : ''}` : '等待平台结果或 CEO 验收');
      setText(metrics[3].querySelector('span'), '可确认收入毛利率');
      setText(metrics[3].querySelector('strong'), margin);
      setText(metrics[3].querySelector('small'), `收入 ¥${revenue.toLocaleString()} - 总成本 ¥${total.toLocaleString()}`);
      setText(metrics[4].querySelector('strong'), pendingItems ? String(pendingItems) : '—');
      setText(metrics[4].querySelector('small'), pendingItems ? '需要 CEO 判断' : '暂无待确认事项');
      const kpiRows = root.querySelectorAll('.kpi-row');
      if (kpiRows.length >= 5) {
        const runs = Array.isArray(state.calendarEvents) ? state.calendarEvents : [];
        const outcomes = Array.isArray(state.outcomeAttributions) ? state.outcomeAttributions : [];
        const analysisRuns = runs.filter(item => /分析|策略|研究/.test(`${item.owner || ''}${item.capability?.agent || ''}`));
        const contentResults = [state.latestXhsFeedback, state.latestExternalFeedback].filter(Boolean).length;
        const engineeringRuns = runs.filter(item => /研发|工程|QA|产品/.test(`${item.owner || ''}${item.capability?.agent || ''}`));
        const escalations = runs.filter(item => item.requiresCEO || ['waiting_ceo', 'acknowledged'].includes(item.status)).length;
        const capacity = runs.filter(item => ['running', 'waiting_ceo', 'acknowledged'].includes(item.status)).length;
        const kpis = [
          [`业务分析 AI · 已验证成果`, outcomes.filter(item => item.status === '已验证价值' && /分析|策略|研究/.test(`${item.agent || ''}${(item.contributors || []).map(person => person.agent).join('')}`)).length ? `${outcomes.filter(item => item.status === '已验证价值' && /分析|策略|研究/.test(`${item.agent || ''}${(item.contributors || []).map(person => person.agent).join('')}`)).length} 条` : (analysisRuns.length ? '—' : '—')],
          [`内容制作 AI · 平台结果`, contentResults ? `${contentResults} 条已回传` : '—'],
          [`工程实现 AI · 首次通过`, state.softwareAcceptance?.choice === 'accept' ? '已验收' : (engineeringRuns.length ? '—' : '—')],
          [`CEO 助理 · 经营提醒`, escalations ? `${escalations} 次待处理` : '—'],
          [`容量风险`, capacity ? `${capacity} 次占用` : '—']
        ];
        kpis.forEach(([label, value], index) => { setText(kpiRows[index].querySelector('span'), label); setText(kpiRows[index].querySelector('strong'), value); });
      }
      const recommendation = [...root.querySelectorAll('.note')].find(node => node.querySelector('strong')?.textContent.includes('下一步建议'));
      if (recommendation) {
        const button = recommendation.querySelector('button');
        [...recommendation.childNodes].forEach(node => { if (node.nodeType === Node.TEXT_NODE) node.remove(); });
        let copy = recommendation.querySelector('[data-finance-recommendation]');
        if (!copy) { copy = document.createElement('span'); copy.dataset.financeRecommendation = 'true'; recommendation.insertBefore(copy, button || null); }
        const hasSignal = Boolean(totalValue || pendingValue || revenue || total);
        copy.textContent = hasSignal
          ? `已整理 ${pendingValue ? `待验证价值 ¥${pendingValue.toLocaleString()}，` : ''}${totalValue ? `已验证价值 ¥${totalValue.toLocaleString()}` : '尚无已验证价值'}。CEO 可进入对应业务办公室补证据，再决定继续、扩大或暂停。`
          : '当前还没有真实结果或成本记录；先完成首轮运行，再生成投入建议。';
      }
      const rows = root.querySelectorAll('.table .row');
      if (rows.length < 5) return;
      setText(rows[0].querySelector('span:nth-child(3)'), '总成本');
      setText(rows[0].querySelector('span:nth-child(5)'), '价值 / 成本');
      const rowData = [
        { business: 'Curis 自研', revenue: revenueRecords.filter(item => /Curis 自研|软件开发/.test(item.business || '') && item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0), value: softwareValue, pending: software.pending },
        { business: '小红书运营', revenue: revenueRecords.filter(item => item.business === '小红书运营' && item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0), value: xhsValue, pending: xhs.pending },
        { business: '抖音 / TikTok', revenue: revenueRecords.filter(item => /抖音|TikTok/.test(item.business || '') && item.status !== '待确认').reduce((sum, item) => sum + Number(item.amount || 0), 0), value: shortVideoValue, pending: shortVideo.pending }
      ];
      const firstBusiness = String(state.firstBusiness || '');
      const activeBusinesses = !state.companyCreatedAt ? new Set() : new Set(/小红书/.test(firstBusiness) ? ['小红书运营'] : /抖音|TikTok|短视频/.test(firstBusiness) ? ['抖音 / TikTok'] : /软件|Curis|研发/.test(firstBusiness) ? ['Curis 自研'] : rowData.map(item => item.business));
      rowData.forEach((item, index) => {
        const row = rows[index + 1];
        row.hidden = !activeBusinesses.has(item.business);
        row.style.display = row.hidden ? 'none' : '';
        const cost = costs.filter(entry => entry.business === item.business).reduce((sum, entry) => sum + Number(entry.amount || 0), 0);
        setText(row.querySelector('span:nth-child(2)'), item.revenue ? `¥${item.revenue.toLocaleString()}` : '—');
        setText(row.querySelector('span:nth-child(3)'), cost ? `¥${cost.toLocaleString()}` : '—');
        setText(row.querySelector('span:nth-child(4)'), item.pending ? `待验证 ¥${item.pending.toLocaleString()}` : item.value ? (item.business === 'Curis 自研' ? `研发效率 ¥${item.value.toLocaleString()}` : `¥${item.value.toLocaleString()}`) : '—');
        setText(row.querySelector('span:nth-child(5)'), item.value && cost ? `${(item.value / cost).toFixed(1)}x` : '—');
      });
      setText(rows[4].querySelector('span:nth-child(2)'), revenue ? `¥${revenue.toLocaleString()}` : '—');
      setText(rows[4].querySelector('span:nth-child(3)'), total ? `¥${total.toLocaleString()}` : '—');
      setText(rows[4].querySelector('span:nth-child(4)'), totalValue ? `¥${totalValue.toLocaleString()}` : '—');
      setText(rows[4].querySelector('span:nth-child(5)'), totalValue && total ? `${(totalValue / total).toFixed(1)}x` : '—');
      setText(root.querySelector('[data-finance-value="revenue"]'), revenue ? `¥${revenue.toLocaleString()}` : '—');
      setText(root.querySelector('[data-finance-value="content"]'), xhsValue + shortVideoValue ? `¥${(xhsValue + shortVideoValue).toLocaleString()}` : '—');
      setText(root.querySelector('[data-finance-value="software"]'), softwareValue ? `${softwareValue.toLocaleString()} 元` : '—');
      setText(root.querySelector('[data-finance-breakdown="plays"]'), plays ? plays.toLocaleString() : '—');
      setText(root.querySelector('[data-finance-breakdown="engagement"]'), likes || saves ? `${likes.toLocaleString()} / ${saves.toLocaleString()}` : '—');
      setText(root.querySelector('[data-finance-breakdown="follows"]'), follows ? follows.toLocaleString() : '—');
      setText(root.querySelector('[data-finance-breakdown="leads"]'), leads ? leads.toLocaleString() : '—');
      setText(root.querySelector('[data-finance-breakdown="hours"]'), softwareValue ? '120 小时' : '—');
      setText(root.querySelector('[data-finance-value="assets"]'), state.outcomeAttributions?.length ? `${state.outcomeAttributions.length} 份` : '—');
    };
    update();
    window.addEventListener('curis-state-changed', update);
    new MutationObserver(update).observe(root, { subtree: true, childList: true, characterData: true });
  }

  // ── Wire sidebar nav items
  function initNavigation() {
    const currentPage = (window.location.pathname.split('/').pop() || 'ceo-desk.html');

    document.querySelectorAll('.sidebar .nav-item, aside.sidebar .nav-item, .nav-list .nav-item').forEach(item => {
      // Skip if already a link
      if (item.tagName === 'A') return;

      // Determine target from data-href or text content
      let target = item.dataset.href;
      if (!target) {
        const text = item.textContent.trim().split(/\s+/).join(' ');
        for (const [label, href] of Object.entries(NAV_MAP)) {
          if (text.includes(label)) {
            target = href;
            break;
          }
        }
      }

      if (target) {
        item.style.cursor = 'pointer';
        item.setAttribute('role', 'link');
        item.setAttribute('tabindex', '0');
        item.dataset.href = target;

        const navigate = () => {
          if (target === '#') {
            showToast('该入口将在设置中心接入；当前工作上下文已保留');
            return;
          }
          window.location.href = target;
        };

        item.addEventListener('click', navigate);
        item.addEventListener('keydown', e => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            navigate();
          }
        });
      }

      // Active state
      const href = item.dataset.href;
      if (href && href !== '#') {
        const active = currentPage === href || currentPage.endsWith('/' + href);
        item.classList.toggle('active', active);
      }
    });
  }

  // ── Toast
  function showToast(message, duration = 2200) {
    let toast = document.getElementById('proto-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'proto-toast';
      toast.setAttribute('role', 'status');
      toast.setAttribute('aria-live', 'polite');
      toast.style.cssText = `
        position: fixed;
        left: 50%;
        bottom: 28px;
        transform: translateX(-50%) translateY(20px);
        background: var(--bg-base-secondary, #222427);
        color: var(--text-default-hover, #f5f9fe);
        border: 1px solid var(--border-neutral-l2, rgba(224,226,242,.16));
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 13px;
        box-shadow: 0 8px 24px rgba(0,0,0,.4);
        opacity: 0;
        pointer-events: none;
        transition: opacity .2s ease, transform .2s ease;
        z-index: 9999;
        white-space: nowrap;
      `;
      document.body.appendChild(toast);
    }

    toast.textContent = message;
    requestAnimationFrame(() => {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    clearTimeout(toast._timer);
    toast._timer = setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(-50%) translateY(20px)';
    }, duration);
  }

  // ── Button click feedback (where no specific handler exists)
  function initButtonFeedback() {
    document.addEventListener('click', e => {
      const btn = e.target.closest('button, .btn');
      if (!btn) return;
      if (btn.dataset.curisHandled === 'true') return;

      // If button already has onclick or bound listener, skip generic feedback
      if (btn.onclick) return;
      if (btn.closest('a')) return;

      const label = btn.textContent.trim();
      if (!label) return;

      // Capture a few generic actions across pages
      if (/^(决策|查看|调查|委派|暂缓|修复问题|运行模拟|提交审批|批准|拒绝|延后|要求修改|预览|编辑|发送|保存|查看影响|查看全部|协调|处理|标记已处理|查看完整档案)$/.test(label)) {
        e.preventDefault();
        const messages = {
          '查看': '已打开当前事项的证据与下一步',
          '查看全部': '已展开完整组织状态',
          '查看影响': '已打开影响范围与回滚路径',
          '调查': '已交给分析 AI，结果回来后会提醒你',
          '委派': '已交给对应 AI 员工，等待回报',
          '协调': '已交给 CEO 助理协调责任与交接',
          '处理': '已记录处理动作，后续结果会回到这里',
          '标记已处理': '已标记为已处理，助理会继续观察',
          '暂缓': '已暂缓，原始上下文和检查点已保留',
          '延后': '已延后到下一检查点',
          '修复问题': '已打开配置问题，处理后才能继续',
          '运行模拟': '已开始运行模拟，结果会写入蓝图记录',
          '提交审批': '已准备审批材料，等待 CEO 判断',
          '批准': '已记录批准，相关团队可以继续执行',
          '拒绝': '已记录拒绝，原方案不会继续运行',
          '要求修改': '已退回修改，原上下文仍然保留',
          '预览': '已打开当前版本预览',
          '编辑': '已打开可编辑设置',
          '发送': '已发送，等待参与者回应',
          '保存': '已保存当前修改',
          '查看完整档案': '已打开员工完整档案'
        };
        writeState({ lastAssistantMessage: messages[label] || `${label}已记录` });
        showToast(messages[label] || `${label}已记录`);
      }
    });
  }

  function initPlaceholderLinks() {
    document.addEventListener('click', event => {
      const link = event.target.closest('a[href="#"]');
      if (!link) return;
      event.preventDefault();
      const source = link.textContent.trim() || '当前来源';
      if (link.closest('.fact-source')) {
        openFormDialog({ title: `查看来源 · ${source}`, description: '来源记录只读展示；原始证据、时间和负责人会跟随这条判断保存。', submitLabel: '关闭', fields: [{ name: 'record', label: '证据记录', type: 'textarea', value: `${source}\n\n当前页面已保留来源名称、责任方和时间戳。接入真实系统后，这里会打开对应原始记录。` }] });
        return;
      }
      writeState({ lastAssistantMessage: `“${source}”暂未连接原始系统，已记录为待补充来源。` });
      showToast('来源已记录，等待接入原始系统');
    });
  }

  function retireLegacyAssistant() {
    document.querySelectorAll('#drawer, #drawer-overlay, .ask-fab, .ask-top-btn').forEach(node => node.remove());
    document.querySelectorAll('button').forEach(button => {
      if (/Assistant|询问助理|问助理/.test(button.textContent || '')) button.remove();
    });
  }

  // ── Expose globals for inline onclick handlers that may be missing
  window.showToast = showToast;

  // ── Auto-init when DOM is ready. Each initializer is isolated so one legacy
  // page-specific control cannot prevent the CEO Assistant and shared shell
  // from starting on the rest of the page.
  const initialize = () => {
    const initializers = [
      initNavigation, initButtonFeedback, initPlaceholderLinks, retireLegacyAssistant,
      applyTheme, injectGlobalStyles, initBusinessMap, initBusinessTruthCards, initBusinessOutcomeDecision, initReviewWorkbench,
      initBusinessCardActions, initBusinessCreation, initOfficeShelf, initOperatingState,
      initOperatingArchive, initOperatingActions, initOperatingTruth, initFirstArrival, initTemplateChoice,
      ensureFoundingTemplateOptions, initOfficePresence, initExternalFeedback,
      initXhsFeedbackCapture, initXhsContentReview, initPlatformOnboarding,
      initShortVideoInteractions, initShortVideoTruthBoard, initRuntimeTruthMetrics, initSoftwareTruthMetrics, initGrowthNextCycle, initOrganizationRoom, initOrganizationPerformance, initOrganizationResourceView, initOrganizationDynamicMap, initOrganizationTruthMap, initOrganizationEscalationTruth,
      initDepartmentCreation, initOrganizationActions, initCapacityExpansion,
      initRuntimeBusinessDecision, initSoftwareRuntime, initSoftwareNextCycle, initSoftwareOfficePresence, initDepartmentRuntime,
      initDeskOpening, initDeskOperatingDayRibbon, initDeskPulse, initFirstOperatingDay,
      initDeskFeedbackDigest, initDeskSoftwareDigest, initDeskDepartmentDigest, initDeskFinanceDigest, initDeskMeetingDigest,
      initDeskCloseout, initDeskDynamicTruth, initDeskActions, initDeskTruthBrief, initWorkspaceStudio, initWorkspacePortal,
      initStudioToolbar, initDeskOperatingDay, initDecisionDiscussion, initMeetingLobby, initMeetingRuntime, initMeetingFollowups,
      initDecisionRuntime, initDecisionTruth, initNeutralShell, initFocusModeShell, initWorkspaceOfficeNav, initExtendedNav,
      initCapabilityRuntime, initCalendarPage, initWorkspaceScheduleEntry, initScheduledRunContext,
      initRuntimeActions, initRuntimeStageDetails, initAssetLibrary, initKnowledgePage,
      initFinancePage, initFinanceSummary, translateVisibleText, applyCompanyState,
      persistFoundingResult, renderCompanion, watchDynamicText
    ];
    initializers.forEach(initializer => {
      try {
        initializer();
      } catch (error) {
        window.__curisErrors = [...(window.__curisErrors || []), `${initializer.name}: ${error.message}`].slice(-20);
      }
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize);
  else initialize();
})();
