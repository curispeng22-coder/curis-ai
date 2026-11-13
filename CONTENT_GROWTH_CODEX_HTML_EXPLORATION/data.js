window.SEED={
 accounts:[
 {id:'a1',platform:'小红书',name:'品牌号',mark:'书',stage:'增长验证',goal:'三个月净增粉丝 8,000',focus:'高收藏的 AI 职场方法',rhythm:'每周 3 篇',supply:'6 天',owner:'林岚',status:'可经营',note:'收藏率上升，但创始人访谈素材不足；先不扩频。'},
 {id:'a2',platform:'抖音',name:'创始人 IP',mark:'抖',stage:'表达验证',goal:'建立 AI 职场效率的可信认知',focus:'短视频口播',rhythm:'每周 2 条',supply:'2 天',owner:'林岚',status:'授权缺口',note:'数字人口播可制作，发布前需确认出镜授权。'},
 {id:'a3',platform:'公众号',name:'品牌官方号',mark:'号',stage:'稳定经营',goal:'将深度内容带向咨询转化',focus:'方法论长文章',rhythm:'每周 1 篇',supply:'5 天',owner:'林岚',status:'手动发布',note:'平台权限不足，沿用导出发布包与人工核验。'}],
 watch:[
 {id:'watch1',name:'AI 职场效率',platform:'抖音 / 小红书',kind:'关键词 + 话题',frequency:'每 6 小时',state:'运行中',last:'09:20',method:'公开页面观察 · Mock'},
 {id:'watch2',name:'对标账号：效率观察室',platform:'抖音',kind:'对标账号',frequency:'每日',state:'运行中',last:'08:00',method:'浏览器可见页面 · Mock'},
 {id:'watch3',name:'评论中的重复提问',platform:'小红书',kind:'受众反馈',frequency:'每日',state:'已暂停',last:'昨日',method:'手动提交样本 · Mock'}],
 signals:[
 {id:'sig1',title:'“AI 会取代岗位吗”讨论升温',platform:'抖音',change:'+46%',window:'近 24 小时',source:'公开话题页 · Mock',seen:'09:20',context:'与创始人 IP 的职场方向相关；仅表示当前观察到热度变化。'},
 {id:'sig2',title:'可直接复用的工作清单被高频收藏',platform:'小红书',change:'+31%',window:'近 24 小时',source:'关键词检索 · Mock',seen:'09:20',context:'多条内容出现“看完能照做”反馈。'},
 {id:'sig3',title:'“效率工具太多怎么选”评论集中',platform:'公众号',change:'新问题',window:'近 48 小时',source:'用户反馈 · 手动样本',seen:'昨日',context:'样本有限，适合先研究，不宜直接下结论。'}],
 refs:[{id:'ref0',title:'三秒反问式开头',source:'抖音公开视频 · 演示来源',published:'2026-09-20',captured:'2026-09-23 09:20',signal:'sig1',hook:'“你以为 AI 会抢你的工作？”',opening:'先抛出误区，再展示可验证的工作场景',structure:'误区 → 两个场景 → 清单 → 行动',rhythm:'前三秒快切，之后每 8 秒换一个证据',visual:'人像近景 + 关键词字幕',cta:'保存岗位任务清单',feedback:'评论更关心如何亲手试一次',why:'具体问题让观众代入；是否真的带来增长尚待验证。',evidence:'来源视频结构观察 + 12 条可见评论（Mock）',fit:'抖音｜创始人 IP',limit:'不复制原文、镜头或声音；品牌号图文需要重新组织。',pattern:'问题先于观点，结尾给可执行清单'}],
 topics:[{id:'topic0',title:'普通人如何识别可以交给 AI 的工作',stage:'可提案',account:'a1',from:'ref0',note:'把“岗位替代”转为“任务拆解”，以收藏为目标。'}],
 proposals:[{id:'prop0',title:'把一天工作拆成 AI 可协作的 5 步',account:'a1',why:'账号本周期需要高收藏的实用内容',goal:'提升收藏率并获得有效咨询',method:'图文',criterion:'发布后 7 天的收藏率与同账号近 5 篇图文比较',source:'ref0',topic:'topic0',limits:'不承诺岗位结果；具体案例需事实核对',state:'待开工'}],
 works:[
 {id:'w1',title:'把一天工作拆成 AI 可协作的 5 步',account:'a1',method:'图文',step:'封面与页序',owner:'周砚',collab:'乔叶',state:'制作中',version:2,artifact:'五页图文稿',source:'prop0',next:'检查封面可读性后交把关',review:false,accepted:false},
 {id:'w2',title:'AI 会不会取代你的岗位',account:'a2',method:'口播',step:'数字人口播',owner:'高戈',collab:'徐白',state:'制作中',version:3,artifact:'Script v3 · 言舟 v2 口播预览',source:'ref0',next:'试听前三秒，再进入后期',review:false,accepted:false},
 {id:'w3',title:'从工具焦虑到工作方法',account:'a3',method:'长文章',step:'专业审查',owner:'徐白',collab:'沈述',state:'待把关',version:1,artifact:'长文章正文 v1',source:'topic0',next:'核对事实与示例后交发布',review:false,accepted:false},
 {id:'w4',title:'一次会做的事，比十个工具更重要',account:'a2',method:'视频',step:'镜头剪辑',owner:'乔叶',collab:'高戈',state:'制作中',version:1,artifact:'六镜头短视频预览',source:'topic0',next:'核对字幕与镜头许可',review:false,accepted:false},
 {id:'w5',title:'普通人怎样开始使用 AI',account:'a2',method:'口播',step:'已交付',owner:'高戈',collab:'徐白',state:'已发布',version:1,artifact:'口播成片 v1',source:'历史内容',next:'对照当前内容复盘',review:true,accepted:true},
 {id:'w6',title:'AI 会不会取代你的岗位',account:'a1',method:'图文',step:'已交付',owner:'周砚',collab:'乔叶',state:'已发布',version:1,artifact:'五页图文 v1',source:'跨平台同主题',next:'对照抖音口播表现',review:true,accepted:true}],
 publications:[{id:'pub0',work:'w3',account:'a3',version:1,mode:'人工发布',state:'等待人工发布',receipt:'尚无外部回执',window:'发布确认后 7 天',url:''},
 {id:'pub5',work:'w5',account:'a2',version:1,mode:'人工核验',state:'已核验上线',receipt:'演示历史回执',window:'发布后 7 天',url:''},
 {id:'pub6',work:'w6',account:'a1',version:1,mode:'人工核验',state:'已核验上线',receipt:'演示历史回执',window:'发布后 7 天',url:''}],
 observations:[{id:'obs0',work:'w2',account:'a2',version:2,views:[230,390,610,880,1170,1420,1680],saves:[8,13,19,28,35,47,54],follows:[1,2,4,6,7,9,11],completion:[23,25,27,28,31,34,35],source:'平台截图 · 人工录入演示',window:'发布后第 1–7 天',comments:'12 条可见评论；5 条讨论“具体如何分任务”',change:'前三秒留存较上版改善；样本和投放条件不同，不能断言开头导致增长。'},
 {id:'obs5',work:'w5',account:'a2',version:1,views:[190,320,500,660,910,1130,1320],saves:[5,9,16,21,28,34,41],follows:[1,1,2,3,4,5,6],completion:[19,20,23,24,26,27,28],source:'平台截图 · 人工录入演示',window:'发布后第 1–7 天',comments:'样本评论较少',change:'旧内容作为同账号、同形态参考，不等于同条件实验。'},
 {id:'obs6',work:'w6',account:'a1',version:1,views:[120,220,350,490,670,820,950],saves:[11,18,27,39,48,57,68],follows:[1,2,3,3,4,5,7],completion:[null,null,null,null,null,null,null],source:'平台截图 · 人工录入演示',window:'发布后第 1–7 天',comments:'同主题图文，不适用视频完播率',change:'跨平台形态不同，只并排看可比字段；完播率为不适用。'}],
 experiments:[{id:'exp0',name:'问题式开头 vs 直接结论',account:'a2',hypothesis:'问题式开头可能提升前三秒留存',variants:'W-202 口播 v2 / v3',publication:'历史演示发布样本',observation:'obs0',result:'v3 观察窗未结束',state:'观察中'}],
 learning:[{id:'learn0',title:'方法清单更容易被保存',scope:'小红书｜品牌号｜图文',basis:'过去 5 篇同类图文的手动观察',confidence:'待重复验证',state:'已接受',use:'作为下一轮选题的结构候选，不自动复制旧文'}],
 assets:[{id:'asset1',name:'品牌封面模板',kind:'模板',version:'v3',rights:'品牌内部可用',used:'W-201 · 图文封面'}, {id:'asset2',name:'言舟',kind:'数字人',version:'v2',rights:'创始人 IP 账号授权待补',used:'W-202 · 口播'}, {id:'asset3',name:'产品界面截图',kind:'图片',version:'v1',rights:'自有素材',used:'W-201 · 页 3'}, {id:'asset4',name:'职场访谈片段',kind:'视频',version:'v1',rights:'需确认受访者授权',used:'未用于正式成品'}],
 messages:[], activity:[{kind:'已处理',text:'沈述发现岗位讨论热度变化，已建立来源观察',time:'09:20'}, {kind:'进行中',text:'高戈正在制作 W-202 的数字人口播',time:'09:34'}, {kind:'等你决定',text:'创始人 IP 的出镜授权尚待确认',time:'今天'}]
};
