/* ============================================================================
   Writing Business HTML Exploration — Mock 数据层
   Authority Class: RESEARCH（本轮探索自有数据，不进入 Curis Authority）
   全部为虚构样例：书名为虚构，平台名称为公开平台名，链接指向公开页面。
   规则：Unknown 不填 0；不跨平台合并指标；不摊造章节收益；不伪造平台字段。
   ========================================================================== */
window.WB_DATA = (function () {

  var meta = {
    today: '2026-09-21',
    business: '写作经营',
    owner: '作者（你）',
    caseNote: '本书与人物均为虚构样例；平台与页面入口为公开来源，未登录、未发布、未读取真实稿费。',
    figureNote: '同一本《夜行灯》在番茄（免费·广告）与《白鹭洲纪事》在起点（付费订阅）分平台显示，不合并、不换算。'
  };

  /* ---------------- 员工与责任 ---------------- */
  var employees = [
    {id:'E-05',name:'许清禾',role:'独立审校编辑',initials:'许',color:'#60766b',resp:['R-REVIEW 审稿与校对']},
    { id: 'E-01', name: '沈知远', role: '责任编辑（创作内核）', also: '代行经营计划（Leader）', initials: '沈', color: '#1f7ae0',
      resp: ['R-EDIT 创作与候选', 'R-LEAD 经营计划（兼任）'], note: '默认一人承担创作内核；重大方向仍由作者决定。' },
    { id: 'E-02', name: '陆晓白', role: '市场研究责任人', initials: '陆', color: '#0e8f7e', resp: ['R-MARKET 市场观察与参考'] },
    { id: 'E-03', name: '郑一鸣', role: '发布责任人', initials: '郑', color: '#b87922', resp: ['R-PUB 发布队列与回执'] },
    { id: 'E-04', name: '何茵', role: '反馈分析责任人', initials: '何', color: '#8a4fbf', resp: ['R-ANALY 表现、评论与归因'] }
  ];

  /* 责任清单：No Owner 是合法状态，不发明在岗员工 */
  var responsibilities = [
    {id:'R-REVIEW',name:'审稿与校对',owner:'E-05',area:'book'},
    { id: 'R-EDIT', name: '创作与候选', owner: 'E-01', area: 'book' },
    { id: 'R-LEAD', name: '经营计划与决定', owner: 'E-01', area: 'operate', note: '兼任；重大方向需作者确认' },
    { id: 'R-MARKET', name: '市场观察与参考', owner: 'E-02', area: 'market' },
    { id: 'R-PUB', name: '发布与回执', owner: 'E-03', area: 'publish' },
    { id: 'R-ANALY', name: '反馈与归因', owner: 'E-04', area: 'audience' },
    { id: 'R-FIN', name: '收益核对', owner: null, area: 'audience', note: '缺责任人：收益差异只能登记为待办，不能自动对账' }
  ];

  /* ---------------- 平台账号与映射 ---------------- */
  var accounts = [
    { id: 'ACC-01', platform: '番茄小说', site: '主站', holder: '作者本人', scope: '免费阅读·广告与礼物分成（样例合同）',
      capability: ['草稿与定时发表', '章节管理', '公开榜单'], gap: ['章级收益明细', '完整评论接口', '数据导出'],
      rules: '平台规则按适用站点与作品形态核验；本轮未确认完整 AI 条款。', verified: '2026-09-21 核对公开说明' },
    { id: 'ACC-02', platform: '起点 / 阅文', site: '主站', holder: '作者本人', scope: '付费订阅·打赏·稿酬（样例合同）',
      capability: ['作品管理', '草稿与发布', '定时/预审提示'], gap: ['章级订阅明细', '评论锚点粒度', '开放接口'],
      rules: '内容合作接口不等于普通作者可用 API；不作为执行能力。', verified: '2026-09-21 核对公开说明' }
  ];

  var mappings = [
    { id: 'M-01', bookId: 'B-01', bookTitle: '夜行灯', accountId: 'ACC-01', externalId: 'FQ-8821470（样例）', externalTitle: '夜行灯',
      scope: '全书（1–42 章已核验，第 40 章状态未知）', chapterMap: '内部章号 = 平台章号（未拆分合并）', status: 'verified' },
    { id: 'M-02', bookId: 'B-02', bookTitle: '白鹭洲纪事', accountId: 'ACC-02', externalId: 'QD-1043922（样例）', externalTitle: '白鹭洲纪事',
      scope: '导入既有连载：18 章已确认，第 19 章本地为新章', chapterMap: '内部章号 = 平台章号', status: 'verified' },
    { id: 'M-03', bookId: 'B-01', bookTitle: '夜行灯', accountId: 'ACC-02', externalId: '—', externalTitle: '—',
      scope: '跨平台发布须先核验独家/授权范围', chapterMap: '—', status: 'blocked', note: '未确认授权范围前不提交，仅保留目标建议。' }
  ];

  /* ---------------- 作品 ---------------- */
  var books = [
    { id: 'B-01', title: '夜行灯', genre: '都市奇谈 / 悬疑', platform: '番茄小说', accountId: 'ACC-01', model: '免费阅读·广告与礼物',
      status: '连载中', startedAt: '2026-06-02', positioning: '单元剧外壳 + 主线长线；每 2–3 章一个可独立成立的小案，同时推进「灯」的来源。',
      audience: '20–35 岁、都市奇谈与轻悬疑读者（依据：本作已发布章节的评论与平台分类，非平台画像导出）',
      volumeCount: 3, publishedCount: 42, publishedThrough: 'ch43', formalStock: 0,
      goal: '卷三完结第一卷主线，同时保持周更 3 章节奏（当前目标，待决定是否调整）',
      origin: 'direction', originRef: 'D-01', imported: false },
    { id: 'B-02', title: '白鹭洲纪事', genre: '民国悬疑', platform: '起点 / 阅文', accountId: 'ACC-02', model: '付费订阅·打赏',
      status: '连载中（导入既有作品）', startedAt: '2025-11-20', positioning: '双线叙事：查案线与家事线交替，每卷收束一条线。',
      audience: '起点悬疑分类读者（依据：分类与订阅结构，非账号画像）', volumeCount: 2, publishedCount: 18,
      goal: '保持两周更 1 章，卷末完成第一条家事线收束。', origin: 'imported', imported: true,
      importNote: '导入时只取得公开元数据与本地已备份正文；平台侧历史数据按可获得范围记录，缺失字段保留为未知。' }
  ];

  var volumes = {
    'B-01': [
      { id: 'V-01', name: '卷一 · 灯下客', chapters: ['ch01', 'ch18'] },
      { id: 'V-02', name: '卷二 · 无名巷', chapters: ['ch19', 'ch36'] },
      { id: 'V-03', name: '卷三 · 长明（进行中）', chapters: ['ch37', 'ch45'], open: true }
    ],
    'B-02': [
      { id: 'V-01', name: '卷一 · 潮信', chapters: ['ch01', 'ch12'] },
      { id: 'V-02', name: '卷二 · 归舟（进行中）', chapters: ['ch13', 'ch20'], open: true }
    ]
  };

  /* 章节身份：内部稳定；平台有独立外部 ID */
  var chapters = {
    'ch39': { bookId: 'B-01', vol: 'V-03', no: 39, title: '第九盏灯', formal: 'v1', published: 'v1', state: 'published', publishedAt: '2026-09-02 20:00' },
    'ch40': { bookId: 'B-01', vol: 'V-03', no: 40, title: '井底的钟', formal: 'v1', published: null, state: 'unknown',
      note: '提交后网络中断，平台侧是否已上线未知。核验前不重发。' },
    'ch41': { bookId: 'B-01', vol: 'V-03', no: 41, title: '巷口的信', formal: 'v1', published: 'v1', state: 'published', publishedAt: '2026-09-08 20:00' },
    'ch42': { bookId: 'B-01', vol: 'V-03', no: 42, title: '旧年账', formal: 'v1', published: null, state: 'rejected',
      rejectReason: '章节内出现真实机构全称，需脱敏后重新提交。', rejectAt: '2026-09-12 11:20' },
    'ch43': { bookId: 'B-01', vol: 'V-03', no: 43, title: '对面', formal: 'v2', formalAcceptedAt: '2026-09-13 22:40',
      published: 'v2', publishedAt: '2026-09-14 20:00', candidate: 'C-43', state: 'published' },
    'ch44': { bookId: 'B-01', vol: 'V-03', no: 44, title: '停摆', formal: null, candidate: 'C-44', state: 'candidate',
      conflict: '与 Canon C-01 冲突：候选写林砚已识破顾晚身份，Canon 记为林砚尚不知情。' },
    'ch45': { bookId: 'B-01', vol: 'V-03', no: 45, title: '（仅大纲）', formal: null, candidate: null, state: 'outline',
      outline: '兑现 F-01「旧钟停在 3:40」；对手戏第二次前置；卷三收束。' },
    'B02-ch17': { bookId: 'B-02', vol: 'V-02', no: 17, title: '潮退之后', formal: 'v1', published: 'v1', state: 'published', publishedAt: '2026-08-28 21:00' },
    'B02-ch18': { bookId: 'B-02', vol: 'V-02', no: 18, title: '第二封信', formal: 'v1', published: 'v1', state: 'published', publishedAt: '2026-09-04 21:00' },
    'B02-ch19': { bookId: 'B-02', vol: 'V-02', no: 19, title: '归舟', formal: 'v1', formalAcceptedAt: '2026-09-19 23:10', published: null, state: 'queued' },
    'B02-ch20': { bookId: 'B-02', vol: 'V-02', no: 20, title: '（起草中）', formal: null, candidate: null, state: 'draft' }
  };

  /* ---------------- 正文与候选 ----------------
     正文三态严格分离，各自保存可回查的正文快照：
       paragraphs   = 草稿（作者工作副本；手写编辑 / 局部修复 / 采纳候选都先落到这里）
       .formal      = 正式稿快照（作者确认后生成，确认 ≠ 发布）
       .published   = 线上稿快照（平台回执核验后才登记）
     versions[] 为历史快照，每一项都带 paragraphs，因此可读、可回退（回退不改历史）。 */
  var ch43Paras = [
    '雨停在后半夜。便利店的自动门还在来回开合，像有人站在门框里犹豫不决。',
    '林砚把伞收在门口的桶里，走到靠窗第二张桌子前坐下。桌上那杯早已凉透的豆浆没有被人碰过，杯壁上凝着一圈细小的水珠。',
    '「你不问我为什么约在这儿？」',
    '对面的人把兜帽往后拨了拨，露出半张脸。灯光斜着打过来，照见她左手腕上那道浅浅的旧疤。',
    '林砚没有答话。他把那盏随手带来的旧台灯放在桌面中央，插头没有插电，灯却亮了——很弱，像一口气息。',
    '「巷子里那盏灯，是你灭的。」他说。',
    '顾晚看着他，很久没有动。便利店的风铃又响了一次，，门外并没有人进来。',
    '「是我。」她说，「但不是我一个人。」',
    '这句话落下之后，空气里的水声突然显得很大。林砚听见自己心里某个一直悬着的东西，轻轻地落到了底。',
    '接下来的一刻钟，两个人把各自知道的事情摊在桌面上：三年前那场火、井底停摆的钟、还有那封信上不属于任何人的字迹。林砚说得慢，顾晚说得更慢，每当话题接近某个名字，两个人都会不约而同地停下来，听门外的雨。',
    '「所以你在替谁做事？」林砚问。',
    '「替我自己。」顾晚说，「也替一个还不想被你知道的人。」',
    '她把杯子推过去一点，像是在确认两件事之间还隔着多远的距离。',
    '凌晨三点四十分，街对面的钟楼没有响。'
  ];
  var ch43Draft = ch43Paras.slice();
  ch43Draft[9] = '接下来的一刻钟，两个人把各自知道的事情摊在桌面上：三年前那场火、井底停摆的钟、还有那封信上不属于任何人的字迹。林砚说得慢，顾晚说得更慢，每当话题接近某个名字，两个人都会停下来，听门外的雨。';
  ch43Draft[13] = '凌晨三点四十分，街对面的钟楼没有响。顾晚把兜帽重新拉上，先走了。';

  var manuscripts = {
    'ch43': {
      bookId: 'B-01', no: 43, title: '第四十三章 · 对面',
      /* 草稿：作者正在改的工作副本（与正式 v2 尚未一致——改的是下一版） */
      paragraphs: ch43Draft,
      draftNote: '作者草稿：已按 C-43 采纳项调整章末与措辞，尚未确认为正式稿',
      formalVersion: 'v2',
      formal: { version: 'v2', paragraphs: ch43Paras.slice(), acceptedAt: '2026-09-13 22:40',
        note: '由 C-43 的 2 项采纳确认生成' },
      published: { version: 'v2', paragraphs: ch43Paras.slice(), at: '2026-09-14 20:00',
        note: '番茄上线版本；此后本地改动不影响线上' },
      versions: [
        { v: 'v1', at: '2026-09-11 21:05', kind: 'draft', note: '初稿，作者手写第 1–6 段',
          paragraphs: ch43Paras.slice(0, 6) },
        { v: 'v2', at: '2026-09-13 22:40', kind: 'formal', note: '作者确认生成正式 v2（旧 v1 保留）',
          paragraphs: ch43Paras.slice() },
        { v: 'v2', at: '2026-09-14 20:00', kind: 'published', note: '平台回执核验：线上版本 = v2',
          paragraphs: ch43Paras.slice(), published: true },
        { v: '草稿 r1', at: '2026-09-20 23:20', kind: 'draft', note: '按 C-43 采纳项改写章末（草稿，未确认）',
          paragraphs: ch43Draft.slice() }
      ]
    }
  };

  /* 候选：每一项可独立采纳，作者可部分采纳 */
  var candidates = {
    'C-43': {
      id: 'C-43', bookId: 'B-01', chapter: 'ch43', baseVersion: 'v2', kind: '修订候选',
      title: '第 43 章 · 对峙段与章末处理',
      createdAt: '2026-09-20 23:10', by: 'E-01',
      rationale: '依据 A-01 的观察与 19 条评论，把第 9–12 段的对峙写实，删掉解释性旁白，并试写一个更直接的章末钩子。',
      refs: ['A-01', 'K-01', 'L-01', 'L-03'],
      changes: [
        { id: 'C43-1', label: '对峙写实', why: 'L-01 经验：章前三分之一进入一次正面对峙；当前对峙偏概括，读者说「像在开会」。',
          before: '两个人把知道的事情都说了出来，谈了很久。', after: '接下来的一刻钟，两个人把各自知道的事情摊在桌面上：三年前那场火、井底停摆的钟、还有那封信上不属于任何人的字迹。林砚说得慢，顾晚说得更慢。', applied: null },
        { id: 'C43-2', label: '删去解释性旁白', why: 'L-03 负向经验：连续解释会拖慢节奏；把判断留给读者。',
          before: '（保留原第 10 段后的两句解释：这里其实是伏笔，读者会在后面的章节明白……）', after: '（删除该段，直接进入对话）', applied: null },
        { id: 'C43-3', label: '章末钩子改为对白', why: 'Pattern P-02 提议；采纳与否需作者判断，因可能与第 44 章开头重复。',
          before: '凌晨三点四十分，街对面的钟楼没有响。', after: '「明天别去巷子。」顾晚说，「他们今天就是在等你。」', applied: null }
      ]
    },
    'C-44': {
      id: 'C-44', bookId: 'B-01', chapter: 'ch44', baseVersion: null, kind: '新章候选',
      title: '第 44 章 · 停摆（候选稿）',
      createdAt: '2026-09-21 00:35', by: 'E-01',
      rationale: '承接 ch43 的对峙，兑现 F-01「旧钟停在 3:40」。',
      refs: ['F-01', 'K-03'],
      conflict: '候选第 4 段写了林砚已经识破顾晚的身份，与 Canon C-01（林砚尚不知情，ch31 正文）冲突。需要作者决定：改候选，或修订 Canon。',
      opening: [
        '钟楼的指针停在三点四十，已经停了三年。',
        '林砚站在巷口，没有进去。他把手里那盏灯举高了一点，光落在墙上，照出一小片褪色的招贴。',
        '顾晚没有来。这是他第一次觉得，一个人不来，比来了更让人不安。'
      ],
      changes: [
        { id: 'C44-1', label: '兑现 F-01（旧钟）', why: '伏笔计划在第 44 章兑现。', before: null, after: '钟楼的指针停在三点四十，已经停了三年。', applied: null }
      ]
    },
    'R-42': {
      id: 'R-42', bookId: 'B-01', chapter: 'ch42', baseVersion: 'v1', kind: '审核修改稿',
      title: '第 42 章 · 旧年账（脱敏修改）',
      createdAt: '2026-09-20 20:05', by: 'E-01',
      rationale: '按平台审核意见：把真实机构全称改为虚构名称，其余不动。',
      refs: [],
      changes: [
        { id: 'R42-1', label: '机构名脱敏', why: '平台审核不通过原因：出现真实机构全称。', before: '（原：市立第三人民医院）', after: '（改：临川市立三院）', applied: null }
      ]
    }
  };

  /* ---------------- 故事状态 ---------------- */
  var storyState = {
    'B-01': {
      characters: [
        { id: 'CH-01', name: '林砚', role: '主角 · 夜巡人', first: 'ch01', status: '在册' },
        { id: 'CH-02', name: '顾晚', role: '引路人 · 身份未明', first: 'ch03', status: '在册' },
        { id: 'CH-03', name: '老周', role: '店主 · 师徒关系', first: 'ch02', status: '在册' },
        { id: 'CH-04', name: '闻笙', role: '对手', first: 'ch17', status: '在册' }
      ],
      relations: [
        { a: '林砚', b: '顾晚', type: '合作 / 互相隐瞒', since: 'ch11' },
        { a: '林砚', b: '老周', type: '师徒', since: 'ch02' },
        { a: '顾晚', b: '闻笙', type: '旧识（未展开）', since: 'ch26' }
      ],
      canon: [
        { id: 'C-01', text: '林砚尚不知顾晚的身份', source: '正文 ch31', by: '作者已写', changeable: '作者决定' },
        { id: 'C-02', text: '夜巡人的能力在灯灭时失效', source: '正文 ch05', by: '作者已写', changeable: '作者决定' },
        { id: 'C-03', text: '故事发生在虚构城市「临川」，时代为 1990 年代末', source: '作者决定 2026-06-02', by: '作者', changeable: '作者决定' }
      ],
      threads: [
        { id: 'F-01', text: '旧钟停在 3:40', planted: 'ch07', plan: 'ch44 兑现', state: '待兑现' },
        { id: 'F-02', text: '顾晚左手腕的旧疤', planted: 'ch22', plan: 'ch46 兑现', state: '待兑现' },
        { id: 'F-03', text: '巷口那盏不亮的灯', planted: 'ch03', plan: '未计划', state: '未决' }
      ],
      timeline: [
        { at: 'ch01–ch18', note: '卷一：单元案 + 灯的出现' },
        { at: 'ch19–ch36', note: '卷二：无名巷，闻笙登场' },
        { at: 'ch37–', note: '卷三：主线推进，灯的来源逐步逼近' }
      ]
    },
    'B-02': {
      characters: [
        { id: 'CH-11', name: '沈砚秋', role: '主角 · 记者的妹妹', first: 'ch01', status: '在册' },
        { id: 'CH-12', name: '陆沉', role: '查案人', first: 'ch01', status: '在册' }
      ],
      relations: [{ a: '沈砚秋', b: '陆沉', type: '合作 · 各有所图', since: 'ch03' }],
      canon: [{ id: 'C-11', text: '白鹭洲的渡口在卷一时已炸毁', source: '正文 ch12', by: '作者已写', changeable: '作者决定' }],
      threads: [{ id: 'F-11', text: '第二封信的落款年份不对', planted: 'ch18', plan: 'ch21', state: '待兑现' }],
      timeline: [{ at: 'ch01–ch12', note: '卷一 · 潮信' }, { at: 'ch13–', note: '卷二 · 归舟' }]
    }
  };

  /* ---------------- 市场与方向 ---------------- */
  var watches = [
    { id: 'W-01', name: '番茄 · 都市分类榜', kind: '榜单', source: '公开榜单页', cadence: '每日 09:00', method: '正常授权浏览器浏览公开页面',
      state: 'active', last: '2026-09-21 09:02', next: '2026-09-22 09:00', result: '新增 3 条快照，其中 2 条与本作题材相邻', budget: '每次 ≤ 6 页' },
    { id: 'W-02', name: '起点 · 悬疑分类榜', kind: '榜单', source: '公开分类/推荐入口', cadence: '每周一 09:00', method: '正常授权浏览器浏览公开页面',
      state: 'paused', last: '2026-09-15 09:05', next: null, pausedBy: '作者（避免与番茄榜重复占用注意力）' },
    { id: 'W-03', name: '番茄 · 创作者公告目录', kind: '公告', source: '公开公告目录', cadence: '每 2 日 09:00', method: '正常授权浏览器浏览公开页面',
      state: 'failed', last: '2026-09-21 09:06', next: '2026-09-23 09:00', fail: '公告正文页跳转失败，本轮无法读取正文内容', failSince: '2026-09-21',
      note: '失败保留原状，等待渠道可读；不代替阅读，不推测规则内容。' }
  ];

  var marketObservations = [
    { id: 'MO-01', watchId: 'W-01', at: '2026-09-21', platform: '番茄', scope: '都市分类榜 · 前 20 名（公开）',
      change: '前 20 名中「单元剧 + 长线悬疑」结构从 2 本增至 4 本；2 本新入榜作品标题均含具体地点词。',
      limit: '单次排名不能说明趋势；未取得在读与收入数据，不能推算营收。', sample: true },
    { id: 'MO-02', watchId: 'W-01', at: '2026-09-18', platform: '番茄', scope: '都市分类榜 · 前 20 名（公开）',
      change: '与 09-14 快照相比，前 5 名变动 1 位。', limit: '快照间隔 4 天，不能得出「上升」结论。', sample: true },
    { id: 'MO-03', watchId: 'W-03', at: '2026-09-21', platform: '番茄', scope: '创作者公告目录（仅标题可读）',
      change: '目录新增 1 条治理类公告标题；正文未读取。', limit: '标题不足以形成规则判断；不据此修改正文。', sample: true, partial: true },
    { id: 'MO-04', at: '2026-09-15', platform: '番茄', scope: '短故事数据口径公告（仅摘要可读）',
      change: '公告提到累计口径与日期窗口口径存在差异。', limit: '该口径针对短故事渠道，不能直接套用长篇连载。', sample: true, partial: true }
  ];

  /* 三次同口径、虚构的榜单观察。数字只用于验证变化视图，不声称平台真实提供。 */
  var marketSnapshots = [
    { id: 'MS-01', watchId: 'W-01', at: '2026-09-15 09:00', platform: '番茄', source: '都市分类榜公开页', scope: '都市分类榜 · 前 20', metric: '演示观察值', unit: '人', evidence: 'Mock 截图 MS-01', mock: true,
      entries: [{ id: 'MW-01', title: '《子夜巡灯》（虚构样例）', genre: '都市奇谈', stage: '连载中', rank: 3, value: 120000, refId: 'R-01' }, { id: 'MW-02', title: '《街角档案》（虚构样例）', genre: '都市奇谈', stage: '新书', rank: 19, value: 8000 }, { id: 'MW-03', title: '《雾城夜话》（虚构样例）', genre: '都市悬疑', stage: '新书', rank: 17, value: 6200 }] },
    { id: 'MS-02', watchId: 'W-01', at: '2026-09-18 09:00', platform: '番茄', source: '都市分类榜公开页', scope: '都市分类榜 · 前 20', metric: '演示观察值', unit: '人', evidence: 'Mock 截图 MS-02', mock: true,
      entries: [{ id: 'MW-01', title: '《子夜巡灯》（虚构样例）', genre: '都市奇谈', stage: '连载中', rank: 3, value: 120700, refId: 'R-01' }, { id: 'MW-02', title: '《街角档案》（虚构样例）', genre: '都市奇谈', stage: '新书', rank: 14, value: 10100 }, { id: 'MW-03', title: '《雾城夜话》（虚构样例）', genre: '都市悬疑', stage: '新书', rank: 16, value: 6900 }] },
    { id: 'MS-03', watchId: 'W-01', at: '2026-09-21 09:00', platform: '番茄', source: '都市分类榜公开页', scope: '都市分类榜 · 前 20', metric: '演示观察值', unit: '人', evidence: 'Mock 截图 MS-03', mock: true,
      entries: [{ id: 'MW-01', title: '《子夜巡灯》（虚构样例）', genre: '都市奇谈', stage: '连载中', rank: 3, value: 121500, refId: 'R-01' }, { id: 'MW-02', title: '《街角档案》（虚构样例）', genre: '都市奇谈', stage: '新书', rank: 9, value: 12800 }, { id: 'MW-03', title: '《雾城夜话》（虚构样例）', genre: '都市悬疑', stage: '新书', rank: 10, value: 8200 }] }
  ];

  /* 参考：条目为虚构样例，来源指向公开入口；范围与局限必须随行 */
  var references = [
    { id: 'R-01', title: '《子夜巡灯》（虚构样例）', platform: '番茄', genre: '都市奇谈',
      source: '番茄公开榜单页（公开元数据）+ 作者本人阅读笔记', scope: '公开元数据 + 公开可读章节的阅读笔记，未导入全文，未下载',
      theme: '以「巡夜人」职业外壳承托单元案', conflict: '每案在章前三分之一进入一次正面对峙',
      character: '主角克制、配角承担信息量', structure: '单元案 2–3 章一收，主线以物证推进',
      rhythm: '章末多为对白收束而非环境收束', style: '短句、少形容词、对话推动',
      limit: '仅 1 本书的观察；未取得该作品数据，不能据此判断「写完读率」；作者风格不可迁移。',
      sample: true, saved: true },
    { id: 'R-02', title: '《雾港来信》（虚构样例）', platform: '起点', genre: '民国悬疑',
      source: '起点公开分类页（公开元数据）+ 公开章节阅读笔记', scope: '公开元数据 + 公开章节阅读笔记',
      theme: '双线叙事，家事线与查案线交替', conflict: '冲突后置，靠信息差维持',
      character: '主角被动、对手主动', structure: '每卷收束一条线', rhythm: '慢热，单章信息密度低',
      style: '长句、环境描写多',
      limit: '与本作节奏取向相反，作为对照参考而非模板；不复制设定。', sample: true, saved: false },
    { id: 'R-03', title: '自有对照 · 《夜行灯》ch41', platform: '番茄', genre: '都市奇谈',
      source: '本书已发布正式稿（v1）', scope: '自有正文，可完整引用',
      theme: '信息揭示型章节', conflict: '无双人正面对峙', character: '配角独白为主', structure: '单线推进',
      rhythm: '中段偏缓', style: '与 ch43 同一作者声纹',
      limit: '本章为信息章，与 ch43 的冲突章不可直接比较；观察年龄须一致。', sample: false, own: true }
  ];

  var patterns = [
    { id: 'P-01', text: '章前三分之一放入一次正面对峙', scope: '本书 + 同类都市悬疑',
      counter: 'ch31 使用同类前置，当周无可见变化', caution: '未排除推荐曝光与时段影响；不适用于信息章。',
      from: ['R-01'], state: '候选' },
    { id: 'P-02', text: '章末用对白收束，而非环境描写', scope: '仅本书（尚未跨作品授权）',
      counter: 'ch36 用环境收束，当周表现与邻章持平', caution: '可能与下一章开头重复；需作者逐章判断。',
      from: ['R-01'], state: '候选' }
  ];

  var directions = [
    { id: 'D-01', title: '卷三方向：单元收束 + 长线逼近', status: 'accepted', acceptedAt: '2026-09-18 22:15',
      bookId: 'B-01', platform: '番茄', reader: '都市奇谈 · 轻悬疑读者',
      genre: '都市奇谈 / 悬疑', core: '把主线悬疑拆成三个可独立成立的单元，每单元结束时推进一点「灯」的来源。',
      keep: '作者坚持的克制叙述与不解释原则', goal: '卷三完结第一卷主线，同时保持周更 3 章',
      refs: ['R-01', 'P-01'], diff: '与《雾港来信》相反：不做慢热长线，改做前置冲突。',
      risk: '前置冲突过多可能使单元案同质化', unknown: '未确认平台推荐权重；未确认读者对单元结构的接受度',
      appliedTo: '已更新卷三 Outline 提案（ch44–ch45）' },
    { id: 'D-02', title: '新书《雾港来信》（虚构样例）', status: 'pending', bookId: null,
      platform: '起点 / 阅文', reader: '民国悬疑 · 付费订阅读者',
      genre: '民国悬疑', core: '双线叙事 + 每卷收束一条线，与既有《白鹭洲纪事》形成同一读者池的第二部。',
      keep: '作者对 1990 年代背景的把握（与本书为不同年代，需另立设定）', goal: '先在起点连载，作者本人评估',
      refs: ['R-02'], diff: '相比《白鹭洲纪事》，把家事线前置。',
      risk: '与已有作品题材接近，可能分散产能；跨平台授权需先核验',
      unknown: '未确认独家/授权范围；未确认起点当前签约要求',
      decidedAt: null }
  ];

  /* ---------------- 发布 ---------------- */
  var queue = [
    { id: 'Q-01', bookId: 'B-01', chapter: 'ch40', title: '第 40 章 · 井底的钟', version: 'v1', account: 'ACC-01', target: '番茄小说',
      plannedAt: '2026-09-06 20:00', submittedAt: '2026-09-06 20:04', state: 'unknown',
      stateNote: '提交后网络中断，平台侧是否已上线未知', evidence: '本地导出包 + 提交时间记录；无平台回执' },
    { id: 'Q-02', bookId: 'B-01', chapter: 'ch41', title: '第 41 章 · 巷口的信', version: 'v1', account: 'ACC-01', target: '番茄小说',
      plannedAt: '2026-09-08 20:00', submittedAt: '2026-09-08 20:02', state: 'live', verifiedAt: '2026-09-08 21:30',
      evidence: '平台章节页可见，版本与本地 v1 一致；线上链接已登记' },
    { id: 'Q-03', bookId: 'B-01', chapter: 'ch42', title: '第 42 章 · 旧年账', version: 'v1', account: 'ACC-01', target: '番茄小说',
      plannedAt: '2026-09-12 20:00', submittedAt: '2026-09-12 10:55', state: 'rejected', rejectAt: '2026-09-12 11:20',
      rejectReason: '章节内出现真实机构全称，需脱敏后重新提交', fixCandidate: 'R-42' },
    { id: 'Q-04', bookId: 'B-01', chapter: 'ch43', title: '第 43 章 · 对面', version: 'v2', account: 'ACC-01', target: '番茄小说',
      plannedAt: '2026-09-14 20:00', submittedAt: '2026-09-14 19:50', state: 'live', verifiedAt: '2026-09-14 20:40',
      publishedVersion: 'v2', evidence: '平台章节页可见；线上版本 = 本地 v2；观察窗 24h / 7d 已建立' },
    { id: 'Q-05', bookId: 'B-02', chapter: 'B02-ch19', title: '第 19 章 · 归舟', version: 'v1', account: 'ACC-02', target: '起点 / 阅文',
      plannedAt: '2026-09-22 21:00', submittedAt: null, state: 'scheduled', evidence: '正式稿已接受（09-19 23:10）；排期未到' }
  ];

  var receipts = {
    'Q-01': { kind: 'none', note: '无回执。核验路径：打开平台作品管理 → 核对第 40 章是否存在且版本一致 → 再决定是否补发。' },
    'Q-02': { kind: 'verified', screens: ['线上章节页（09-08 21:30 核对）'], onlineVersion: 'v1' },
    'Q-03': { kind: 'rejected', screens: ['审核意见（09-12 11:20）'], reason: '出现真实机构全称' },
    'Q-04': { kind: 'verified', screens: ['线上章节页（09-14 20:40 核对）'], onlineVersion: 'v2' },
    'Q-05': { kind: 'pending', note: '排期未到，尚无提交动作。' }
  };

  var submitModes = [
    { key: 'manual', label: '人工提交（本次演示采用）', note: '按平台正常后台路径提交；Curis 只登记提交事实与回执，不代替平台动作。' },
    { key: 'export', label: '导出后人工提交', note: '导出发布包只完成准备，不等于发布。' },
    { key: 'api', label: '平台 API', note: '当前未确认普通作者可用接口，不作为可用执行能力。' }
  ];

  /* ---------------- 读者与收益 ---------------- */
  var performance = {
    'B-01': {
      platform: '番茄', model: '免费阅读 · 广告与礼物', coverage: '2026-09-14 – 2026-09-21（平台后台读数，手动录入）',
      updatedAt: '2026-09-21 10:20', source: '平台后台读数 + 截图核对',
      bookLevel: [
        { key: '在读', unit: '人', note: '平台「在读」口径，不等于读者总数', series: [1180, 1235, 1290, 1264, 1338, 1402, 1451], ages: ['09-15', '09-16', '09-17', '09-18', '09-19', '09-20', '09-21'] },
        { key: '新增收藏', unit: '人', note: '区间新增，非存量', series: [41, 38, 47, 41, 52, 49, 58], ages: ['09-15', '09-16', '09-17', '09-18', '09-19', '09-20', '09-21'] },
        { key: '广告收益（预估）', unit: '¥', note: '平台展示的预估口径，未结算', series: [86, 91, 88, 95, 104, 111, 118], ages: ['09-15', '09-16', '09-17', '09-18', '09-19', '09-20', '09-21'] }
      ],
      chapterLevel: [
        { chapter: 'ch43', key: '章节读完率', value: 71, unit: '%', denom: 'unknown', note: '平台只展示百分比，未提供分子/分母与样本口径，不能与前章平均，也不能推算人数。' },
        { chapter: 'ch41', key: '章节读完率', value: 64, unit: '%', denom: 'unknown', note: '同上，无分母。' },
        { chapter: 'ch43', key: '章节收益', value: null, unit: '¥', note: '平台未提供章级收益。不能按章节摊分书级收益。' }
      ]
    },
    'B-02': {
      platform: '起点 / 阅文', model: '付费订阅 · 打赏', coverage: '2026-09-01 – 2026-09-20（导入平台导出 + 手录）',
      updatedAt: '2026-09-21 10:05', source: '平台导出（作者本人）+ 截图核对',
      bookLevel: [
        { key: '订阅', unit: '章次', note: '书级可得；章级明细待核', series: [312, 298, 341, 366, 352, 388, 401], ages: ['09-14', '09-15', '09-16', '09-17', '09-18', '09-19', '09-20'] },
        { key: '打赏', unit: '¥', note: '区间累计', series: [12, 0, 20, 8, 0, 60, 40], ages: ['09-14', '09-15', '09-16', '09-17', '09-18', '09-19', '09-20'] }
      ],
      chapterLevel: [
        { chapter: 'B02-ch18', key: '章级订阅', value: null, unit: '—', note: '本轮未取得章级明细；显示缺口，不推导。' }
      ]
    }
  };

  var observationsWindow = [
    { chapter: 'ch43', publishedAt: '2026-09-14 20:00', age24h: { 在读: 1264, 新增收藏: 41 }, age7d: { 在读: 1451, 新增收藏: 245 },
      note: '固定日期趋势与「发布后观察年龄」分开记录；跨章比较只在观察年龄一致时进行。' }
  ];

  var dataEntries = [
    { id: 'DE-01', kind: 'import', platform: '起点 / 阅文', at: '2026-09-21 09:40', rows: 3, mapped: 2, conflicts: 1,
      fields: [['章节', 'chapter_no'], ['日期', 'window_date'], ['订阅', 'subs'], ['打赏(¥)', 'tips']],
      conflictNote: '其中 1 行的时间窗与 09-20 已有录入重叠，值不同（388 vs 392）→ 需要确认来源后才覆盖。',
      status: 'pending' },
    { id: 'DE-02', kind: 'correction', platform: '番茄', at: '2026-09-18 23:20', field: '新增收藏（09-17）',
      before: 47, after: 41, reason: '重新截图核对后订正：原先把「在读」列误读为「新增收藏」。原记录保留。', status: 'done' },
    { id: 'DE-03', kind: 'manual', platform: '番茄', at: '2026-09-21 10:20', field: '在读 / 新增收藏 / 广告收益（预估）', note: '按观察计划手录，只填平台真实可得的字段。', status: 'done' }
  ];

  var comments = {
    sample: '番茄评论区当前作者可见 62 条（09-14 – 09-21）；平台隐藏/删除的评论不可见，热评权重未知 → 不能当作全体读者意见。',
    clusters: [
      { id: 'K-01', topic: '人物对峙（正面）', size: 19, coverage: '62 条中 19 条', quote: '「这章两个人坐在便利店那一段最好看，终于说人话了。」',
        counter: '另有 1 条认为对峙「太长、没必要」。', anchor: { chapter: 'ch43', from: 8, to: 12, conf: 'confirmed' } },
      { id: 'K-02', topic: '节奏偏慢（混合）', size: 14, coverage: '62 条中 14 条', quote: '「39 到 41 章有点拖。」',
        counter: '5 条明确表示喜欢慢节奏铺垫。', anchor: { chapter: 'ch39–ch41', conf: 'inferred', note: '读者未指明具体段落，无法直接定位；标为推断待确认。' } },
      { id: 'K-03', topic: '章末钩子（正面）', size: 11, coverage: '62 条中 11 条', quote: '「每次最后一句都让人想点下一章。」',
        counter: '2 条表示章末过于刻意。', anchor: { chapter: 'ch43', from: 15, to: 15, conf: 'inferred' } }
    ],
    actions: { reply: false, replyNote: '本轮不自动回复读者；回复由作者在平台执行。' }
  };

  var analyses = [
    { id: 'A-01', bookId: 'B-01', chapter: 'ch43', publishedVersion: 'v2', publishedAt: '2026-09-14 20:00',
      window: '发布后 7 日（09-14 20:00 – 09-21 20:00）', createdAt: '2026-09-21 10:35', by: 'E-04',
      layers: {
        observation: 'ch43 上线后 7 日窗口内，本书「新增收藏」累计 245（同期前三章 3 个 7 日窗分别为 198 / 205 / 212）；平台展示的 ch43 章节读完率 71%（无分母）。',
        evidence: [
          '平台后台读数（09-21 10:20 手录，截图核对）',
          '评论区 62 条中 19 条指向便利店对峙段（K-01）',
          '已发布正文 v2 第 8–12 段（线上版本与本地 v2 一致，09-14 20:40 核对）'
        ],
        hypothesis: '冲突兑现前置（把正面对峙放在章前三分之一）可能提高了本章的读完与后续收藏转化。',
        alternatives: ['平台推荐曝光在本窗口内变化', '09-19–09-21 为周末，阅读量整体抬升', '第 40 章状态未知可能造成追更集中', '章名「对面」的点击吸引'],
        counter: '第 31 章曾使用同类「前置对峙」写法，其 7 日窗（162）低于邻章 → 减弱该写法的普适性。',
        learningDraft: { text: '章前三分之一放入一次正面对峙，可能提升本作都市悬疑题材的本章读完', scope: '本书 + 同类都市悬疑', exclude: '未排除曝光、时段与章名影响' },
        recommendation: '在 ch45 再做一次同观察年龄的观察（同时记录当日曝光），不改动全书节奏；若 ch45 无同类变化，则缩小经验适用范围。',
        owner: '作者决定'
      },
      evidenceGap: '没有章级收益、没有推荐曝光数据 → 不能把收藏变化归因给「收入」；也不能证明因果关系。',
      limitation: '若只有书级数据可用，则表述缩小为「同期本书表现变化」，不定位到第 43 章。',
      linkedComments: ['K-01'], linkedRefs: ['R-03'], learningId: 'L-01-later' },
    { id: 'A-02', bookId: 'B-01', chapter: null, publishedVersion: null, publishedAt: null,
      window: '书级 · 09-15 – 09-21', createdAt: '2026-09-21 10:40', by: 'E-04', bookLevelOnly: true,
      layers: {
        observation: '本书同期「在读」由 1180 升至 1451（+23%），「新增收藏」累计 245。',
        evidence: ['平台后台书级读数；无章级数据'],
        hypothesis: '无法定位到具体章节；可能与近期更新节奏、平台推荐、书名与封面共同相关。',
        alternatives: ['更新频率变化', '平台推荐位变化', '季节性阅读量'],
        counter: '没有对照章节，也没有实验条件。',
        learningDraft: null,
        recommendation: '登记为书级观察，不生成章节经验；先补齐章级粒度再分析。',
        owner: '分析责任人'
      },
      evidenceGap: '缺少章级数据与曝光数据。',
      limitation: '仅书级；不得声称某一章带来增长。' }
  ];

  var revenue = {
    'B-01': { platform: '番茄', currency: 'CNY', updatedAt: '2026-09-21 10:20',
      items: [
        { kind: '广告收益', stage: '预估', window: '09-01 – 09-15', amount: 1240.50, note: '平台展示的预估口径，未结算' },
        { kind: '广告收益', stage: '已结算', window: '08-01 – 08-31', amount: 980.20, note: '已到账 2026-09-10' },
        { kind: '礼物', stage: '预估', window: '09-14 – 09-21', amount: 86.00, note: '区间累计' },
        { kind: '章节收益', stage: '—', window: '—', amount: null, note: '平台未提供章级收益，不能按章节摊分书级收入。' }
      ] },
    'B-02': { platform: '起点 / 阅文', currency: 'CNY', updatedAt: '2026-09-21 10:05',
      items: [
        { kind: '订阅收入', stage: '结算中', window: '09-01 – 09-20', amount: 2310.00, note: '账期：次月 15 日' },
        { kind: '打赏', stage: '结算中', window: '09-01 – 09-20', amount: 140.00, note: '与订阅合并出账' },
        { kind: '稿酬', stage: '已到账', window: '08-01 – 08-31', amount: 1980.00, note: '到账 2026-09-15' }
      ] }
  };

  /* ---------------- 写作经验 ---------------- */
  var learnings = [
    { id: 'L-01', text: '章前三分之一放入一次正面对峙，可能提升本章读完', kind: '正向',
      scope: '本书 + 同类都市悬疑', platform: '番茄', stage: '卷三 · 冲突章',
      evidence: ['A-01', 'K-01'], counter: 'ch31 同类写法 7 日窗低于邻章',
      used: 3, verified: 1, usedNote: '「应用次数」与「验证次数」分开：应用 3 次中只有 1 次带同观察年龄的对照。',
      accepted: 'author', acceptedAt: '2026-09-19 09:10', validUntil: null, deactivated: false,
      notExcluded: '未排除推荐曝光、周末时段与章名影响' },
    { id: 'L-02', text: '章末用对白收束而非环境描写', kind: '正向',
      scope: '仅本书', platform: '番茄', stage: '各章章末',
      evidence: ['K-03', 'R-01'], counter: 'ch36 用环境收束，当周表现与邻章持平',
      used: 2, verified: 0, usedNote: '尚无同观察年龄的验证。',
      accepted: 'author', acceptedAt: '2026-09-20 21:00', deactivated: false,
      notExcluded: '可能与下一章开头重复；不适用于收束性章节' },
    { id: 'L-03', text: '连续两段以上解释性旁白会拖慢节奏', kind: '负向',
      scope: '本书', platform: '番茄', stage: '中段',
      evidence: ['K-02', 'A-01'], counter: 'ch28 有一段解释性旁白，当周表现正常',
      used: 1, verified: 1, usedNote: '作为负向经验记录：写坏的方式也能沉淀。',
      accepted: 'author', acceptedAt: '2026-09-18 20:30', deactivated: false,
      notExcluded: '仅 1 次应用与 1 次验证' }
  ];

  var learningUsage = [
    { id: 'LU-01', learningId: 'L-01', where: 'ch43', target: '候选 C-43 · C43-1', at: '2026-09-20 23:10', decision: 'pending',
      reason: '编辑建议：把概括式对峙改为写实对话，与观察一致。' },
    { id: 'LU-02', learningId: 'L-03', where: 'ch43', target: '候选 C-43 · C43-2', at: '2026-09-20 23:10', decision: 'pending',
      reason: '删去解释性旁白，避免拖慢。' },
    { id: 'LU-03', learningId: 'L-02', where: 'ch43', target: '候选 C-43 · C43-3', at: '2026-09-20 23:10', decision: 'pending',
      reason: '提议章末改为对白钩子；作者已表示可能与 ch44 开头重复。' },
    { id: 'LU-04', learningId: 'L-01', where: 'ch39', target: '正式稿 v1', at: '2026-09-02 20:00', decision: 'applied',
      followUp: 'ch39 的 7 日窗未见明显变化 → 计入反例候选。' }
  ];

  /* ---------------- 经营决定 ---------------- */
  var decisions = [
    { id: 'DEC-01', kind: 'Operating', title: '《夜行灯》更新节奏：周更 3 章 → 2 章？', status: 'pending', raisedAt: '2026-09-21 10:45', by: 'E-01',
      target: 'B-01', question: '可发布正式章库存为 0（ch43 已上线，ch44 候选未采纳）。是否把节奏从周更 3 章调整为 2 章以保质量？',
      evidence: ['库存 0 可发布正式章', 'ch44 候选存在 1 处 Canon 冲突', 'A-01 显示本书在读上升但不可归因', '作者本周可用写作时间约 6 小时'],
      options: [
        { key: 'keep', label: '保持周更 3 章', impact: '需在 09-24 前接受 ch44 并再写 ch45；ch44 的 Canon 冲突须先解决；候选可能被迫提前采纳。', risk: '质量下降与 Canon 松动风险' },
        { key: 'slow', label: '调为周更 2 章（编辑建议）', impact: '下一章 09-25 上线；留出 canon 与候选的决策时间；短期在读增速可能放缓。', risk: '平台节奏预期与读者追更体验' },
        { key: 'wait', label: '先观察一周再定', impact: '本周只发布 ch44（若采纳）；09-28 复查后再决定。', risk: '决定延后会压缩 ch45 的兑现窗口' }
      ],
      boundary: '不因单章数据自动调整节奏；此次为编辑建议，须作者确认。', decidedAt: null, decision: null },
    { id: 'DEC-02', kind: 'Choice', title: '第 43 章修订候选（C-43）是否部分采纳？', status: 'pending', raisedAt: '2026-09-20 23:10', by: 'E-01',
      target: 'ch43', question: '候选含 3 项改动，可逐项采纳。采纳并确认后生成正式 v3，旧版本 v2 保留。',
      evidence: ['A-01', 'K-01', 'L-01', 'L-03'], options: [], boundary: '候选不覆盖正式稿；确认前线上仍是 v2。', decidedAt: null, decision: null },
    { id: 'DEC-03', kind: 'Gate', title: '第 42 章脱敏修改稿重新提交（外部动作）', status: 'pending', raisedAt: '2026-09-20 20:05', by: 'E-03',
      target: 'ch42', question: '按审核意见完成脱敏（R-42）。重新提交会产生外部副作用，需要作者授权。',
      evidence: ['平台审核不通过原因（09-12 11:20）', 'R-42 修改稿'], options: [], boundary: '批准 ≠ 上线；提交后须等待回执并核验。', decidedAt: null, decision: null },
    { id: 'DEC-00', kind: 'Operating', title: '接受卷三方向提案 D-01', status: 'applied', raisedAt: '2026-09-18 21:40', by: 'E-01',
      target: 'B-01', question: '是否接受「单元收束 + 长线逼近」作为卷三方向？', evidence: ['R-01', 'P-01'],
      options: [], boundary: '接受后更新后续 Outline，不改历史章。', decidedAt: '2026-09-18 22:15', decision: 'accepted',
      appliedNote: '已更新卷三 Outline 提案（ch44–ch45）；未改动任何已发布章节。', appliedAt: '2026-09-18 22:30' }
  ];

  /* ---------------- Work（团队行动） ---------------- */
  var works = [
    { id: 'W-101', title: '市场扫描 · 番茄都市榜（W-01）', owner: 'E-02', status: 'done', at: '2026-09-21 09:02',
      artifact: '市场快照 MO-01 / MO-02', next: '已回市场观察；无待办', area: 'market', obj: 'W-01' },
    { id: 'W-102', title: '第 44 章候选稿（C-44）', owner: 'E-01', status: 'choice', at: '2026-09-21 00:35',
      artifact: '候选 C-44（1 项改动 + 1 处 Canon 冲突）', next: '等作者决定：改候选或修订 Canon', area: 'book', obj: 'C-44' },
    { id: 'W-103', title: '第 43 章归因分析（A-01）', owner: 'E-04', status: 'done', at: '2026-09-21 10:35',
      artifact: 'A-01（五层）', next: '已回原观测与评论；候选经验待作者接受', area: 'audience', obj: 'A-01' },
    { id: 'W-104', title: '第 42 章脱敏修改稿（R-42）', owner: 'E-01', status: 'working', at: '2026-09-20 20:05',
      artifact: '修改候选 R-42', next: '等作者授权后由发布责任人重新提交', area: 'book', obj: 'R-42' },
    { id: 'W-105', title: '关注来源维护 · 公告目录读取失败（W-03）', owner: 'E-02', status: 'wait', at: '2026-09-21 09:06',
      artifact: '失败记录 + 下次检查 09-23', next: '等渠道可读；不推测规则内容', area: 'market', obj: 'W-03' },
    { id: 'W-106', title: '数据补录 · 起点导出字段映射（DE-01）', owner: null, status: 'wait', at: '2026-09-21 09:40',
      artifact: '待映射表（3 行，1 行冲突）', next: '缺责任人：需指派后确认映射', area: 'audience', obj: 'DE-01' },
    { id: 'W-107', title: '第 19 章排期发布（Q-05）', owner: 'E-03', status: 'wait', at: '2026-09-19 23:10',
      artifact: '正式稿 v1 + 排期 09-22 21:00', next: '排期未到；到期后人工提交并登记回执', area: 'publish', obj: 'Q-05' },
    { id: 'W-108', title: '收益核对 · 8 月账期差异', owner: null, status: 'wait', at: '2026-09-20 16:20',
      artifact: '差异待办（¥12.40）', next: '缺财务责任人；只登记不对账', area: 'audience', obj: 'REV-DIFF' }
  ];

  var nextCheck = {
    at: '2026-09-22 10:00',
    items: [
      { k: '观察窗到期', v: 'ch43 发布后 7 日窗（09-21 20:00 到期）→ 需确认是否形成经验' },
      { k: '库存', v: '可发布正式章 0；ch44 候选未采纳' },
      { k: '外部未知', v: 'ch40 平台侧状态未核验（不得重发）' },
      { k: '待决', v: '3 项（节奏 / ch43 候选 / ch42 重新提交）' },
      { k: '数据缺口', v: '起点章级订阅缺失；番茄章节收益缺失' }
    ]
  };

  /* ---------------- 对话种子（有正确对象与版本范围） ---------------- */
  var conversations = {
    'E-01|ch43': [
      { who: 'me', text: 'C-43 里第 3 项我倾向拒绝，会跟 ch44 开头撞。前两项按你的建议采纳。', at: '2026-09-21 10:50' },
      { who: 'emp', text: '收到。我把第 3 项标为拒绝并保留理由；前两项采纳后生成 v3，v2 会留档。要不要顺带把 ch44 的那处 Canon 冲突一起看？', at: '2026-09-21 10:52' }
    ],
    'E-02|W-03': [
      { who: 'me', text: '公告目录这次还是读不到正文，先不用管，别猜规则。', at: '2026-09-21 09:10' },
      { who: 'emp', text: '已保留失败原因与下次检查 09-23；本轮不生成任何规则结论。', at: '2026-09-21 09:11' }
    ]
  };

  /* ============================================================================
     创作内核（Book Creative Core）—— 每部作品独立，绑定本书
     §13 合同对象：定位 / 世界 / 主支线与结局 / 多级大纲 / 人物与认知域 / 场景准备
     事实状态（不进 Canon 的推断必须显式标注）：
       CONFIRMED_CANON 作者已确认 | MANUSCRIPT_FACT 正文已发生 | PLANNED 计划未发生
       AI_INFERRED 推断待确认 | CONFLICTED 冲突 | TO_EXPLORE 待探索
     读者分区（男频/女频/不限）与题材（都市/悬疑…）是两个不同维度，不合并。
     ========================================================================== */

  /* 空书模板：新建/空作品得到真实空结构（TO_EXPLORE + 空数组），不是别的书的样例 */
  function blankCraft(bookId, title) {
    return {
      bookId: bookId,
      positioning: {
        workingTitle: title || '未命名',
        readerPartition: null, partitionNote: '读者分区是运营分区，与题材是两个维度；不先填也可以开始写。',
        genres: [], genreNote: '题材可组合、暂定或自定义；平台分类映射另核验。',
        coreOriginal: null, perspective: null, style: null, lengthPlan: null,
        platform: null, taboos: [], readerPromise: null,
        /* 作者的原话构思（「从一句想法开始」时原样保存，不加工）。
           编辑的方向候选以此为唯一依据；coreOriginal 是收敛后的一句话故事。 */
        seed: null, seedAt: null, seedBy: null,
        fields: { coreOriginal: 'empty', perspective: 'empty', style: 'empty', lengthPlan: 'empty',
          readerPromise: 'empty', genres: 'empty', readerPartition: 'empty', seed: 'empty' },
        /* 创作选择（L01–L24）：tags[维度] = { sel:[已选], primary:主值, note:组合/自定义说明,
           req:自动整理的自然语言写作要求, custom:作者自填, undecided:待定 }。
           tagScope 记录本组选择作用于哪个范围；章级覆盖写在 chapters[ck].tagOverride。 */
        tags: {}, tagScope: 'book', tagUpdatedAt: null,
        origin: 'manual', originRef: null, updatedAt: null
      },
      world: [], arc: { premise: null, mainConflict: null, mainLines: [], subLines: [], turns: [], climax: null, endings: [], promises: [] },
      outline: [], scenes: {}, characters: [], importRecords: [], reviewRuns: [], impactLog: []
    };
  }

  /* ==========================================================================
     创作选择词库 L01–L24（Authority Class: RESEARCH）
     依据：CURIS_WRITING_FULL_PRODUCT_INTERACTION_DESIGN_CANDIDATE.md §16.1 / §16.2
     约定：
       · mode  single＝同一范围通常一个主值；multi＝可组合并标主次；combo＝基础选择＋可编辑说明。
       · 每个维度都可「待定 / 自定义」；选项是本轮要保留的候选范围，不代表模型一定遵循。
       · 探索版允许少数维度只放代表性样本，但必须在 README / 报告逐组列出省略项。
       · 词库是「定位 / 写作偏好 / 章节要求」的产品字段，不新建第二套标签 Runtime。
     ========================================================================== */
  var TAG_GROUPS = [
    { id: 'G1', name: '作品与读者', note: '作品放在哪、给谁看' },
    { id: 'G2', name: '世界与故事', note: '故事发生在什么世界、靠什么驱动' },
    { id: 'G3', name: '叙事与表达', note: '怎么讲、用什么语气与文字' },
    { id: 'G4', name: '期待与边界', note: '读者的情绪回报与作者禁区' },
    { id: 'G5', name: '篇幅与当前任务', note: '生产节奏与本次修改要求' }
  ];

  var WRITING_TAGS = [
    { id: 'L01', group: 'G1', name: '作品形态', mode: 'single', scope: '本书',
      opts: ['长篇小说', '中篇小说', '短篇小说', '短篇合集'],
      why: '决定结构建议与人物规模，不强制分卷' },
    { id: 'L02', group: 'G1', name: '读者分区', mode: 'single', scope: '本书定位',
      opts: ['男频向', '女频向', '不限定'],
      why: '记录目标市场意向；不推定主角性别、感情线或读者个人性别' },
    { id: 'L03', group: 'G1', name: '主要题材', mode: 'multi', scope: '本书',
      opts: ['都市', '现实', '校园青春', '职场', '历史', '架空历史', '玄幻', '奇幻', '仙侠', '武侠',
        '科幻', '悬疑', '推理', '惊悚', '冒险', '言情', '游戏竞技', '体育', '童话/儿童文学'],
      why: '给故事承诺和资料建议；允许科幻＋悬疑等组合，不合并成一条不可解释标签' },
    { id: 'L04', group: 'G1', name: '细分方向', mode: 'multi', scope: '按题材相关性推荐，全部可搜索',
      searchable: true,
      opts: ['都市生活', '行业职场', '家庭群像', '商战创业', '校园成长', '太空探索', '赛博朋克',
        '人工智能', '时间旅行', '末日生存', '探案解谜', '社会悬疑', '密室推理', '东方玄幻',
        '西方奇幻', '修真成长', '江湖侠义', '古代言情', '现代言情', '电竞', '体育竞技'],
      why: '帮作者缩小方向；不是固定父子排他分类，不适用不展示空字段' },
    { id: 'L05', group: 'G2', name: '时代与空间', mode: 'combo', scope: '本书 / 场景',
      optGroups: [
        { name: '时代', opts: ['当代', '近未来', '远未来', '古代', '近代', '架空时代', '多时间线'] },
        { name: '空间', opts: ['现实城市', '小镇乡村', '校园', '职场', '异世界', '太空', '封闭空间'] }
      ],
      why: '形成背景建议；标签不能代替具体地点与世界规则' },
    { id: 'L06', group: 'G2', name: '主角结构', mode: 'single', scope: '本书，可解释例外',
      opts: ['单主角', '双主角', '群像', '多视角主角'],
      why: '帮规划叙事重心；不强制男女双主角' },
    { id: 'L07', group: 'G2', name: '核心故事驱动', mode: 'multi', scope: '本书 / 故事线', core: true,
      opts: ['解谜', '求生', '复仇', '成长', '守护', '寻找', '救赎', '竞争', '探索', '关系变化', '权力冲突', '职业目标'],
      why: '编辑把抽象驱动转成具体人物目标、阻力与代价' },
    { id: 'L08', group: 'G2', name: '情节机制', mode: 'multi', scope: '本书 / 故事线', optional: true,
      opts: ['穿越', '重生', '循环', '系统', '身份隐藏', '身份互换', '契约', '试炼', '任务挑战', '误会', '卧底', '失忆'],
      why: '提供构思支点；选择后明确机制限制，不默认生成套路剧情' },
    { id: 'L09', group: 'G2', name: '冲突来源', mode: 'multi', scope: '故事线 / 章',
      opts: ['人与人', '人与组织/制度', '人与环境', '人与技术', '人与自我', '价值观冲突', '关系冲突'],
      why: '帮明确阻力；落到具体行动，不能只把冲突标签塞入提示' },
    { id: 'L10', group: 'G2', name: '核心主题', mode: 'multi', scope: '本书',
      opts: ['自由与责任', '身份与归属', '信任与背叛', '记忆与真相', '成长与代价', '爱与失去',
        '权力与正义', '技术与人性', '家庭与自我'],
      why: '指导选择和价值张力，不要求正文直接讲道理' },
    { id: 'L11', group: 'G2', name: '情感 / 关系线', mode: 'combo', scope: '故事线',
      optGroups: [
        { name: '关系', opts: ['无核心感情线', '爱情', '亲情', '友情', '师徒', '搭档', '宿敌'] },
        { name: '发展速度', opts: ['慢热', '并肩成长', '关系修复', '相互试探', '破镜重圆'] }
      ],
      why: '允许非爱情作品；关系名称/发展速度分开，具体人物仍在 D09' },
    { id: 'L12', group: 'G3', name: '叙事人称', mode: 'single', scope: '本书，章可有明确例外',
      opts: ['第一人称', '第三人称', '第二人称实验表达'],
      why: '约束叙述方式；第二人称非默认推荐但不删除作者选择' },
    { id: 'L13', group: 'G3', name: '认知视角', mode: 'combo', scope: '本书 / 章 / 场景',
      opts: ['限知', '全知', '多视角交替', '不可靠叙述'],
      why: '明确谁能知道什么；多视角不等于全知，具体知情仍读故事状态' },
    { id: 'L14', group: 'G3', name: '叙事时序', mode: 'combo', scope: '本书 / 卷 / 章',
      opts: ['顺叙', '倒叙', '插叙', '双线交织', '多线并行', '非线性'],
      why: '组织讲述顺序；不更改事件实际发生时间' },
    { id: 'L15', group: 'G3', name: '整体基调', mode: 'multi', scope: '本书 / 章', core: true,
      opts: ['轻松', '幽默', '温暖', '治愈', '热血', '紧张', '冷峻', '悲凉', '荒诞', '黑色幽默', '浪漫', '史诗感'],
      why: '避免把互补情绪一概判冲突；作者可规定何处转调' },
    { id: 'L16', group: 'G3', name: '语言风格', mode: 'multi', scope: '作者方法 / 本书 / 章', core: true,
      opts: ['简洁直接', '口语自然', '克制留白', '细腻感性', '诗性意象', '冷硬简练', '古典雅致', '纪实', '讽刺', '对白驱动'],
      why: '转成可编辑要求与样例；“高级/优美”不能作为唯一验收标准' },
    { id: 'L17', group: 'G3', name: '节奏与描写', mode: 'combo', scope: '本书 / 章 / 选区',
      optGroups: [
        { name: '节奏（事件密度）', opts: ['快节奏', '均衡推进', '慢热铺陈'] },
        { name: '句式', opts: ['短句为主', '长短交替'] },
        { name: '描写侧重', opts: ['行动优先', '对话优先', '心理细描', '环境氛围', '细节留白'] }
      ],
      why: '选择后解释改的是事件密度、句式还是描写，三者不混成一个快慢开关' },
    { id: 'L18', group: 'G4', name: '读者期待 / 情绪回报', mode: 'multi', scope: '本书 / 章',
      opts: ['逆境突破', '能力成长', '谜底揭晓', '身份揭示', '公平伸张', '智谋取胜', '关系推进',
        '情感共鸣', '探索发现', '伏笔兑现'],
      why: '表达期待与兑现计划，不能用爽点标签替代因果与人物动机' },
    { id: 'L19', group: 'G4', name: '开篇 / 章末方法', mode: 'combo', scope: '章 / 场景',
      optGroups: [
        { name: '开篇', opts: ['行动切入', '异常事件', '人物困境', '关键对话', '悬念引入', '氛围铺垫'] },
        { name: '章末', opts: ['疑问', '选择', '反转', '危险', '情绪余韵', '阶段落点'] }
      ],
      why: '编辑提供适合本章的方法；并非每章必须悬崖式悬念' },
    { id: 'L20', group: 'G4', name: '结局方向', mode: 'single', scope: '全书 / 故事线',
      opts: ['圆满', '遗憾', '悲剧', '开放', '阶段性完成', '暂未决定'],
      why: '帮反推人物弧线与承诺；始终是计划，不是已发生事实' },
    { id: 'L21', group: 'G4', name: '作者禁区 / 避免项', mode: 'multi', scope: '本书 / 任务', core: true,
      opts: ['避免强行降智', '避免重复套路', '避免无因反转', '避免机械说教', '避免重复比喻', '避免滥用误会',
        '避免人物声纹趋同', '避免视角越界', '避免过量信息堆砌', '避免过度血腥描写'],
      allowCustom: true,
      why: '具体检查与保留要求；不是绕过平台规则，也不提供规避 AI 检测选项' },
    { id: 'L22', group: 'G5', name: '篇幅与生产节奏', mode: 'combo', scope: '本书 / 章 / 发布计划',
      optGroups: [
        { name: '篇幅意向', opts: ['短篇意向', '中篇意向', '长篇意向'] },
        { name: '生产节奏', opts: ['完稿后发布', '边写边连载'] }
      ],
      fields: [
        { key: 'targetChars', label: '目标字数范围', placeholder: '如 90–120 万' },
        { key: 'chapterChars', label: '章节长度范围', placeholder: '如 2500–3500 字/章' },
        { key: 'cadence', label: '更新计划', placeholder: '自定，不强制日更' }
      ],
      why: '数值使用范围输入，不伪造统一字数标准或强制日更；发布计划引用 D17' },
    { id: 'L23', group: 'G5', name: '修改任务要求', mode: 'combo', scope: '当前任务（不写成永久本书标签）',
      taskOnly: true,
      optGroups: [
        { name: '操作', opts: ['续写', '扩写', '压缩', '重写', '润色', '对白调整', '节奏调整'] },
        { name: '力度', opts: ['轻度', '中度', '深度'] },
        { name: '保护项（不得越过）', opts: ['保留事件', '保留人物动机', '保留视角', '保留选定句', '仅改选区'] }
      ],
      why: '是操作参数，不是永久本书标签；力度不能越过明确保护项' },
    { id: 'L24', group: 'G5', name: '作者样例与自定义方法', mode: 'combo', scope: '作者授权范围 / 本书 / 任务',
      freeText: true,
      opts: ['正面样例', '反面样例', '角色对白样例', '自有写作规则', '已接受经验'],
      fields: [
        { key: 'sample', label: '样例或规则内容', placeholder: '粘贴或写下你认可/不认可的写法' },
        { key: 'useScope', label: '允许使用方式', placeholder: '如：仅本书 / 仅本章 / 可跨作品引用' }
      ],
      why: '不要求把风格只能压成标签；引用的正文与权限明确，可预览、排除和更换' }
  ];

  /* 「和编辑一起想」候选组（Mock，带理由）：选择后真的更新题材/读者/基调等标签与定位。
     不是自动勾满；作者可改、可不用；已手选项不被静默替换。 */
  var TAG_SUGGESTIONS = [
    { id: 'SUG-01', name: '档案员 · 悬疑向', by: 'E-01',
      forWhat: '「一个档案员收到未来来信」这类种子',
      tags: { L02: ['不限定'], L03: ['悬疑', '科幻'], L15: ['冷峻', '紧张'], L16: ['克制留白', '冷硬简练'],
        L07: ['解谜', '探索'], L18: ['谜底揭晓', '伏笔兑现'] },
      why: '把「未来来信」当成待解的谜，而不是能力设定。读者回报集中在「谜底揭晓」，最省笔墨也最容易闭环。',
      tradeoff: '代价：情绪回报偏冷，前 3 章需要靠一个具体钩子留人；不适合想要爽感连击的读者。' },
    { id: 'SUG-02', name: '来信 · 温情向', by: 'E-01',
      forWhat: '同一颗种子的另一种走法',
      tags: { L02: ['不限定'], L03: ['现实', '科幻'], L15: ['温暖', '治愈'], L16: ['细腻感性', '口语自然'],
        L07: ['寻找', '关系变化'], L10: ['记忆与真相', '爱与失去'] },
      why: '把「未来来信」当成一次迟到的告别。冲突来自人际关系与时间，情绪回报是「情感共鸣」。',
      tradeoff: '代价：强冲突弱，需要靠人物关系立住；读者留存更依赖声纹而非情节。' },
    { id: 'SUG-03', name: '机构 · 都市职场向', by: 'E-01',
      forWhat: '若你其实想写「体制内的未来情报」',
      tags: { L02: ['男频向'], L03: ['都市', '职场', '科幻'], L15: ['紧张', '冷峻'], L16: ['简洁直接', '对白驱动'],
        L09: ['人与组织/制度'], L07: ['权力冲突', '职业目标'] },
      why: '冲突落在「人与组织/制度」，题材走都市职场，读者分区偏男频向。适合写程序、权限与信息不对称。',
      tradeoff: '代价：需要一定的行业细节支撑，否则组织冲突会显得空；世界观表达受限。' }
  ];

  /* 新书「从想法开始」的起步方式（D05 要求：从想法开始 / 导入旧稿 / 先手写，不是只建空卡） */
  var START_PATHS = [
    { id: 'idea', name: '从一句想法开始', desc: '写下一句构思，编辑接住它并提出两三种方向（含具体故事内容与取舍）', primary: true },
    { id: 'import', name: '导入旧稿', desc: '已有稿件：先预览卷章识别与分类，确认后写入草稿，并抽取设定候选' },
    { id: 'write', name: '先手写', desc: '跳过规划：直接开第 1 章手写，定位与方向稍后再补——未填不阻止写作' }
  ];

  /* 方向候选模板：每条都带具体故事内容、差异与取舍，不是标签包。
     编辑按作者自己的话挑选其中最贴近的两条，并保留作者原话为依据。 */
  var START_DIRECTIONS = [
    { id: 'SD-01', name: '机制悬疑 · 有代价的预知', keys: ['档案', '报纸', '记录', '档', '未来', '明天', '预知', '近未来', '悬疑'],
      premise: '近未来的档案员每天提前收到一份印着明天日期的报纸；他只能撤回其中一条既成事实，而每撤回一次都要交出一段自己的记忆。',
      conflict: '他想救人，但每改一次就少一段与亡妻有关的记忆——救人与留住自己之间必须选一个。',
      viewpoint: '第三人称限知（随档案员）', tone: ['冷峻', '紧张'],
      drivers: ['解谜', '救赎'], payoff: ['谜底揭晓', '伏笔兑现'],
      why: '把「收到明天的报纸」写成有代价的机制，而不是万能能力——天然生成连载级悬念，且不需要堆砌世界观。',
      tradeoff: '偏冷、代价明确：前 3 章要靠一个具体钩子留人，不适合想要爽感连击的读者。',
      tags: { L01: ['长篇小说'], L03: ['科幻', '悬疑'], L07: ['解谜', '救赎'], L12: ['第三人称'],
        L15: ['冷峻', '紧张'], L16: ['冷硬简练'], L18: ['谜底揭晓', '伏笔兑现'] } },
    { id: 'SD-02', name: '人物悬疑 · 迟到的告别', keys: ['信', '报纸', '档案', '亲人', '家人', '记忆', '去世', '思念', '关系'],
      premise: '档案员收到的不是明天的新闻，而是明天会寄到自己手上的那封信——寄信人是三年前已经去世的父亲。',
      conflict: '他想按信里的指示去做，又怕证实父亲当年对他撒了谎；真相与他对父亲的记忆互相撕扯。',
      viewpoint: '第一人称（档案员本人）', tone: ['温暖', '悲凉'],
      drivers: ['寻找', '关系变化'], payoff: ['情感共鸣', '身份揭示'],
      why: '把超常设定收进一段私人关系里，冲突来自记忆与信任，情绪回报落在「情感共鸣」，对声纹要求高但不依赖大场面。',
      tradeoff: '外部冲突弱：需要靠人物关系与声纹立住，读者留存更依赖写法而不是情节密度。',
      tags: { L01: ['长篇小说'], L03: ['现实', '悬疑'], L07: ['寻找', '关系变化'], L12: ['第一人称'],
        L15: ['温暖', '悲凉'], L16: ['细腻感性'], L18: ['情感共鸣', '身份揭示'] } },
    { id: 'SD-03', name: '机构悬疑 · 谁在提前印发', keys: ['档案', '机构', '体制', '权限', '程序', '部门', '情报', '系统', '报纸'],
      premise: '报纸不是奇迹而是流程：档案员所在的机构每天提前印出明天，而他是唯一发现印数对不上死人数的核对员。',
      conflict: '上报意味着承认自己所在的机构在选择性救人；沉默则要继续替这份报纸签字。',
      viewpoint: '第三人称限知，多线交替（档案员 / 上级）', tone: ['紧张', '冷峻'],
      drivers: ['权力冲突', '解谜'], payoff: ['谜底揭晓', '逆境突破'],
      why: '把「明天的报纸」解释成制度行为，冲突落在人与组织之间；信息不对称本身就是悬疑引擎，且能持续供料。',
      tradeoff: '需要行业与程序细节支撑，否则组织冲突会显空；世界观表达空间比机制向更窄。',
      tags: { L01: ['长篇小说'], L03: ['都市', '悬疑', '科幻'], L07: ['权力冲突', '解谜'], L12: ['第三人称'],
        L15: ['紧张', '冷峻'], L16: ['简洁直接', '对白驱动'], L18: ['谜底揭晓', '逆境突破'] } }
  ];

  var craft = {
    'B-01': {
      bookId: 'B-01',
      positioning: {
        workingTitle: '夜行灯',
        readerPartition: '不限（偏男频向）', partitionNote: '读者分区是运营分区，不等于题材；不因此限定主角性别。',
        genres: ['都市', '奇谈', '悬疑'], genreNote: '题材可组合；此处为作者自定标签，平台分类另映射核验。',
        coreOriginal: '「灯」不是道具而是代价：每点亮一次要拿走持有者一段记忆；主角靠记忆清单维持身份。',
        perspective: '第三人称限知（跟随林砚）', style: '冷硬克制、短句、对话推动',
        lengthPlan: '长篇（约 90–120 万字，3 卷）', platform: '番茄小说（免费阅读）',
        taboos: ['不写真实机构全称', '作者禁区：不解释超自然成因'],
        readerPromise: '每 2–3 章一个可独立成立的小案；主线以物证推进，不做无代价的爽感。',
        fields: { coreOriginal: 'confirmed', perspective: 'confirmed', style: 'confirmed',
          lengthPlan: 'tentative', readerPromise: 'confirmed', genres: 'confirmed', readerPartition: 'tentative' },
        /* 创作选择 L01–L24（数组＝直选；对象＝可带 note/req/custom/undecided） */
        tags: {
          L01: ['长篇小说'], L02: ['不限定'], L03: ['都市', '悬疑'], L04: ['探案解谜', '社会悬疑'],
          L05: { L05a: ['当代'], L05b: ['现实城市'] }, L06: ['单主角'], L07: ['解谜', '探索'],
          L08: { sel: ['身份隐藏'], note: '「灯」的代价机制只做限制，不做升级系统。' },
          L09: ['人与人', '人与自我'], L10: ['记忆与真相', '身份与归属'],
          L11: { L11a: ['搭档'], L11b: ['相互试探'] }, L12: ['第三人称'], L13: ['限知'], L14: ['顺叙'],
          L15: ['冷峻', '紧张'], L16: ['冷硬简练', '简洁直接'],
          L17: { L17a: ['均衡推进'], L17b: ['短句为主'], L17c: ['细节留白'] },
          L18: ['谜底揭晓', '伏笔兑现'],
          L19: { L19a: ['异常事件'], L19b: ['疑问'] }, L20: ['阶段性完成'],
          L21: ['避免强行降智', '避免无因反转', '避免视角越界'],
          L22: { L22a: ['长篇意向'], L22b: ['边写边连载'],
            targetChars: '90–120 万字', chapterChars: '2500–3500 字/章', cadence: '不强制日更，按卷推送' },
          L24: { sel: ['正面样例', '自有写作规则'],
            sample: '认可：把判断藏在动作里（「他把灯按灭，没说话。」）——不解释情绪。',
            useScope: '仅本书可用' }
        },
        tagScope: 'book', tagUpdatedAt: '2026-09-18 22:30',
        origin: 'direction', originRef: 'D-01', updatedAt: '2026-09-18 22:30'
      },
      world: [
        { id: 'WD-01', kind: '规则', name: '夜巡人的灯',
          cond: '灯亮起时，持有者能看见「未了之事」的轮廓。', cost: '每点亮一次，烧掉持有者一段与目标无关的记忆。',
          limit: '同一夜只能点亮一次。', exception: '在「长明」处点灯不付代价（作者已定，尚未写明出处）。',
          state: 'CONFIRMED_CANON', source: '正文 ch05 / 作者决定 2026-06-02', evidence: 'ch05', refs: ['C-02'] },
        { id: 'WD-02', kind: '地点', name: '无名巷',
          cond: '巷内在 3:40 会短暂「停摆」，除钟声外的声响消失。', cost: '—', limit: '仅 3:40 前后数分钟。', exception: '未知。',
          state: 'MANUSCRIPT_FACT', source: '正文 ch19–ch36', evidence: 'ch19', refs: ['F-01'] },
        { id: 'WD-03', kind: '势力', name: '收灯人',
          cond: '未知：只知他们在回收「灭掉的灯」。', cost: '—', limit: '—', exception: '—',
          state: 'TO_EXPLORE', source: '作者待探索（卷三计划）', evidence: null, refs: [] }
      ],
      arc: {
        premise: '一个靠记忆清单才能确认「我是谁」的夜巡人，追查一盏不该存在的灯。',
        mainConflict: '点亮灯要付记忆代价；而查清真相必须反复点灯。',
        mainLines: [
          { id: 'ML-01', text: '追查「灯」的来源与代价机制', from: 'ch01', state: 'PLANNED' },
          { id: 'ML-02', text: '林砚与顾晚从互相试探到结成同盟', from: 'ch11', state: 'MANUSCRIPT_FACT' }
        ],
        subLines: [
          { id: 'SL-01', text: '老周的师徒情与隐瞒', from: 'ch02', state: 'MANUSCRIPT_FACT' },
          { id: 'SL-02', text: '闻笙的动机（对手线）', from: 'ch17', state: 'MANUSCRIPT_FACT' }
        ],
        turns: [
          { id: 'T-01', at: '卷三', text: '顾晚承认巷子的灯是她灭的（ch43 已写）', state: 'MANUSCRIPT_FACT' },
          { id: 'T-02', at: '卷三', text: '林砚第一次为查案主动付掉一段关于母亲的记忆', state: 'PLANNED' }
        ],
        climax: '计划：卷三收束在「长明」处——点灯不付代价的例外被证伪。',
        endings: [
          { id: 'EN-01', text: '林砚烧掉最后一段记忆换来真相，成为下一个收灯人。', state: 'candidate' },
          { id: 'EN-02', text: '顾晚替他承受代价，林砚带着不完整的记忆继续夜巡。', state: 'candidate' }
        ],
        promises: [
          { id: 'PR-01', text: '每卷至少兑现一次旧伏笔（卷三兑现 F-01）', state: 'PLANNED' },
          { id: 'PR-02', text: '已埋未兑现：F-02 顾晚的旧疤（计划 ch46）', state: 'PLANNED' }
        ]
      },
      /* 大纲与章节：用显式 chapterKey / chapterNo 关联（禁止按标题正则猜章；
         章节改名或换号不影响关联）。 */
      outline: [
        { id: 'O-B', level: 'book', parent: null, chapterKey: null, title: '全书总纲', purpose: '三卷结构：灯下客 / 无名巷 / 长明',
          events: '卷一建世界与单元案；卷二引入对手与巷；卷三逼近来源并收束主线。', emotion: '克制悬疑 → 收紧 → 代价感',
          origin: 'author', version: 'v2' },
        { id: 'O-V3', level: 'volume', parent: 'O-B', chapterKey: null, title: '卷三 · 长明', purpose: '主线收束：来源、代价、长明的例外',
          events: 'ch44 兑现旧钟；ch45 对峙第二次前置；卷末逼近「长明」。', emotion: '紧迫 → 决断',
          origin: 'author', version: 'v2' },
        { id: 'O-C44', level: 'chapter', parent: 'O-V3', chapterKey: 'ch44', chapterNo: 44, title: '第 44 章 · 停摆',
          purpose: '兑现 F-01「旧钟停在 3:40」；推进对手线',
          events: '巷内在 3:40 停摆；林砚发现钟不是坏了，而是被人按住。', emotion: '不安',
          origin: 'ai', version: 'v1' },
        { id: 'O-C45', level: 'chapter', parent: 'O-V3', chapterKey: 'ch45', chapterNo: 45, title: '第 45 章 · 第二次前置',
          purpose: '卷三收束前的第二次正面对峙', events: '（待细化）', emotion: '—', origin: 'ai', version: 'v1' }
      ],
      scenes: {
        'ch44': [
          { id: 'SC-44-1', order: 1, purpose: '入巷：建立停摆的异常', pov: '林砚', cast: ['林砚'], place: '无名巷口',
            conflict: '环境反常（无声）', reveal: '巷内在 3:40 停摆', notReveal: '谁按住了钟', emotion: '不安',
            endState: '林砚决定入巷', length: '约 800 字', refs: ['WD-02', 'F-01'] },
          { id: 'SC-44-2', order: 2, purpose: '对峙前哨：顾晚不出现', pov: '林砚', cast: ['林砚', '顾晚'], place: '巷中',
            conflict: '同伴缺席带来的不安', reveal: '顾晚的缺席本身是信号', notReveal: '顾晚去向', emotion: '警觉',
            endState: '察觉有人在暗处', length: '约 900 字', refs: ['WD-02'] }
        ]
      },
      characters: [
        { id: 'CH-01', name: '林砚', role: '主角 · 夜巡人',
          goal: '查清灯的来源，同时保住自己的记忆清单',
          motivation: '三年前那场火里他失去了一个记不清的人，夜巡是他确认「我是谁」的方式。',
          weakness: '越接近真相越要点灯，越点灯越不记得为什么要点。', abilityLimit: '灯灭时能力失效（C-02）',
          arc: '从「靠清单活着」到「主动选择要记住什么」',
          voice: '短句、少形容词、把判断藏在动作里', first: 'ch01', status: '在册',
          knows: { character: ['灯可点亮、要付记忆', '顾晚在替某人做事'], author: ['收灯人的存在'],
            reader: ['顾晚的旧疤（ch22 已写）'], unrevealed: ['林砚其实救过顾晚'] } },
        { id: 'CH-02', name: '顾晚', role: '引路人 · 身份未明',
          goal: '替「一个还不想被知道的人」办事',
          motivation: '报恩兼赎罪：她是三年前那场火的另一个幸存者。', weakness: '不肯解释，导致同盟反复被消耗。',
          abilityLimit: '左手旧伤影响持械；不能在强光下久留。', arc: '从隐瞒到有限坦白（ch43 是转折）',
          voice: '话少而稳、答非所问、句末常留白', first: 'ch03', status: '在册',
          knows: { character: ['林砚尚不知她的身份'], author: ['她替谁做事'], reader: [], unrevealed: ['她的真实姓名'] } },
        { id: 'CH-03', name: '老周', role: '店主 · 师徒关系',
          goal: '守着店与旧账', motivation: '愧疚：他知道三年前的事却没去救。',
          weakness: '回避，宁可沉默。', abilityLimit: '年长，行动力下降', arc: '从回避到开口',
          voice: '絮叨、爱打岔', first: 'ch02', status: '在册',
          knows: { character: ['知道部分真相'], author: ['全部'], reader: ['部分'], unrevealed: ['他藏起的信'] } },
        { id: 'CH-04', name: '闻笙', role: '对手',
          goal: '回收所有「灭掉的灯」', motivation: '认为灯是灾祸之源。',
          weakness: '不相信任何同盟。', abilityLimit: '—', arc: '从对立到被迫合作（未定）',
          voice: '礼貌而冷、句短', first: 'ch17', status: '在册',
          knows: { character: ['林砚的存在'], author: ['收灯人组织'], reader: [], unrevealed: ['他与顾晚的旧识关系'] } }
      ],
      importRecords: [],
      reviewRuns: [],
      impactLog: [
        { id: 'IM-01', at: '2026-09-18 22:30', change: '接受方向 D-01（单元收束 + 长线逼近）',
          affected: ['O-V3（卷三大纲）', 'ch44 / ch45 章纲'], unchanged: '已发布 ch39–ch43 正文不改',
          decidedBy: '作者', state: 'applied' }
      ]
    },

    'B-02': {
      bookId: 'B-02',
      positioning: {
        workingTitle: '白鹭洲纪事',
        readerPartition: '不限', partitionNote: '导入既有作品，读者分区按平台分类反推待核验。',
        genres: ['民国', '悬疑'], genreNote: '题材为作者自定；平台分类另映射。',
        coreOriginal: '一封落款年份不对的信，牵出渡口爆炸案的另一种解释。',
        perspective: '双线第三人称（查案线 / 家事线）', style: '环境描写多、长句、慢热',
        lengthPlan: '长篇（3 卷，已写 2 卷）', platform: '起点 / 阅文（付费订阅）',
        taboos: ['不写真实历史人物全名'],
        readerPromise: '每卷收束一条线。',
        fields: { coreOriginal: 'confirmed', perspective: 'confirmed', style: 'confirmed',
          lengthPlan: 'confirmed', readerPromise: 'confirmed', genres: 'confirmed', readerPartition: 'tentative' },
        tags: {
          L01: ['长篇小说'], L02: ['不限定'], L03: ['历史', '悬疑'], L04: ['社会悬疑', '探案解谜'],
          L05: { L05a: ['近代'], L05b: ['小镇乡村'] }, L06: ['双主角'], L07: ['寻找', '解谜'],
          L09: ['人与人', '人与组织/制度'], L10: ['记忆与真相', '家庭与自我'],
          L11: { L11a: ['亲情'], L11b: ['关系修复'] }, L12: ['第三人称'], L13: ['多视角交替'], L14: ['双线交织'],
          L15: ['冷峻', '悲凉'], L16: ['纪实', '细腻感性'],
          L17: { L17a: ['慢热铺陈'], L17b: ['长短交替'], L17c: ['环境氛围'] },
          L18: ['谜底揭晓', '情感共鸣'],
          L19: { L19a: ['氛围铺垫'], L19b: ['阶段落点'] }, L20: ['开放'],
          L21: ['避免强行降智', '避免重复套路'],
          L22: { L22a: ['长篇意向'], L22b: ['完稿后发布'],
            targetChars: '（未定，导入时未记录）', chapterChars: '（未记录）', cadence: '按卷推进' },
          /* L24「作者样例」有意留空：导入既有作品时并未授权引用原文，示例展示真实空状态。 */
        },
        tagScope: 'book', tagUpdatedAt: '2025-11-20',
        origin: 'imported', originRef: null, updatedAt: '2025-11-20'
      },
      world: [
        { id: 'WD-11', kind: '地点', name: '白鹭洲渡口',
          cond: '卷一时已炸毁，现为废墟。', cost: '—', limit: '—', exception: '—',
          state: 'MANUSCRIPT_FACT', source: '正文 ch12', evidence: 'ch12', refs: ['C-11'] },
        { id: 'WD-12', kind: '规则', name: '书信的年代线索',
          cond: '信件落款年份与邮戳不符时，指向一个「另立的时间线」。', cost: '—', limit: '仅对纸质信件成立。',
          exception: '未知。', state: 'AI_INFERRED', source: '从 ch18 正文抽取，待作者确认', evidence: 'ch18', refs: ['F-11'] }
      ],
      arc: {
        premise: '记者的妹妹与查案人在一座废渡口的两条线里，追同一桩爆炸案。',
        mainConflict: '查案线要真相，家事线要保全名声，两者互相牵制。',
        mainLines: [{ id: 'ML-11', text: '查案线：渡口爆炸案的另一种解释', from: 'ch01', state: 'MANUSCRIPT_FACT' }],
        subLines: [{ id: 'SL-11', text: '家事线：沈家与渡口的关系', from: 'ch01', state: 'MANUSCRIPT_FACT' }],
        turns: [], climax: '计划：卷末完成第一条家事线收束。',
        endings: [],
        promises: [{ id: 'PR-11', text: '已埋未兑现：F-11 第二封信的落款年份', state: 'PLANNED' }]
      },
      outline: [
        { id: 'O-B2', level: 'book', parent: null, chapterKey: null, title: '全书总纲（导入）', purpose: '双线交替，每卷收束一条线',
          events: '卷一潮信引入两线；卷二归舟收束家事线。', emotion: '克制的旧案感', origin: 'author', version: 'v1' },
        { id: 'O-B2V2', level: 'volume', parent: 'O-B2', chapterKey: null, title: '卷二 · 归舟', purpose: '收束家事线',
          events: '第 19 章归舟：第二条线收束开始。', emotion: '收束', origin: 'author', version: 'v1' },
        { id: 'O-B2C19', level: 'chapter', parent: 'O-B2V2', chapterKey: 'B02-ch19', chapterNo: 19,
          title: '第 19 章 · 归舟', purpose: '第二条线收束开始；第二封信落款年份的第一次正面处理',
          events: '沈砚秋在渡口旧址找到落款年份不符的第二封信。', emotion: '下沉的确定感',
          origin: 'author', version: 'v1' }
      ],
      scenes: {},
      characters: [
        { id: 'CH-11', name: '沈砚秋', role: '主角 · 记者的妹妹', goal: '查清哥哥的死因',
          motivation: '哥哥留下的最后一封信。', weakness: '把查案当成替哥哥活下去。', abilityLimit: '—',
          arc: '从替哥哥查案到为自己查案', voice: '冷静、书面语偏多', first: 'ch01', status: '在册',
          knows: { character: [], author: ['渡口与沈家的关系'], reader: [], unrevealed: ['哥哥真正死因'] } },
        { id: 'CH-12', name: '陆沉', role: '查案人', goal: '结案',
          motivation: '旧案未结是他的职业污点。', weakness: '为结案倾向简化真相。', abilityLimit: '职权受限',
          arc: '从对立到妥协合作', voice: '简短、公文体', first: 'ch01', status: '在册',
          knows: { character: [], author: ['爆炸案另有内情'], reader: [], unrevealed: ['他隐瞒的证据'] } }
      ],
      importRecords: [
        { id: 'IMP-01', at: '2025-11-20 15:40', fileName: '白鹭洲_前19章.txt', chars: 92300,
          classes: [{ kind: '正文', count: 19, conf: 0.97 }, { kind: '大纲', count: 2, conf: 0.62 }, { kind: '设定', count: 1, conf: 0.41 }],
          state: 'confirmed', note: '导入时只取得本地已备份正文；平台侧历史数据按可获得范围记录，缺失字段保留为未知。' }
      ],
      reviewRuns: [],
      impactLog: []
    }
  };

  return {
    meta: meta, employees: employees, responsibilities: responsibilities, accounts: accounts, mappings: mappings,
    books: books, volumes: volumes, chapters: chapters, manuscripts: manuscripts, candidates: candidates,
    storyState: storyState, watches: watches, marketObservations: marketObservations, marketSnapshots: marketSnapshots, references: references,
    patterns: patterns, directions: directions, queue: queue, receipts: receipts, submitModes: submitModes,
    performance: performance, observationsWindow: observationsWindow, dataEntries: dataEntries, comments: comments,
    analyses: analyses, revenue: revenue, learnings: learnings, learningUsage: learningUsage,
    decisions: decisions, works: works, nextCheck: nextCheck, conversations: conversations,
    craft: craft, blankCraft: blankCraft,
    tagGroups: TAG_GROUPS, writingTags: WRITING_TAGS, tagSuggestions: TAG_SUGGESTIONS,
    startPaths: START_PATHS, startDirections: START_DIRECTIONS
  };
})();
