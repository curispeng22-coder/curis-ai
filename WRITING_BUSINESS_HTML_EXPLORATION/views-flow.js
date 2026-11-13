/* Author journey presentation. Reuses Book, manuscript, review and publishing state.
   No model/platform execution; reference conclusions remain attributed reading notes. */
(function () {
  'use strict';
  var e = WB.esc, ui = WB.ui;
  function btn(text, action, attrs, primary) { return '<button class="btn' + (primary ? ' primary' : '') + '" data-action="' + action + '" ' + (attrs || '') + '>' + e(text) + '</button>'; }
  function chs(id) { return Object.keys(WB.S.chapters).filter(function (k) { return WB.S.chapters[k].bookId === id; }).sort(function (a,b) { return WB.S.chapters[a].no-WB.S.chapters[b].no; }); }
  function nav(text, view, attrs, primary) { return btn(text, 'nav.view', 'data-area="book" data-view="'+view+'" '+(attrs||''), primary); }
  function head(kicker, title, action) { return '<header class="flow-head"><div><div class="eyeline">'+e(kicker)+'</div><h1>'+e(title)+'</h1></div><div class="btnrow">'+(action||'')+'</div></header>'; }
  function editor(obj, text, reviewer) {var id=reviewer?'E-05':'E-01',person=WB.emp(id);return '<div class="editor-line"><span class="editor-avatar">'+e(person.initials)+'</span><div><b>'+e(person.name)+'</b><span>'+e(person.role)+' · '+e(text)+'</span></div>'+btn(reviewer?'与审校编辑讨论':'与编辑讨论','conv.open','data-emp="'+id+'" data-obj="'+e(obj)+'" data-label="'+e(WB.S.chapters[obj]?'第 '+WB.S.chapters[obj].no+' 章 · '+WB.S.chapters[obj].title:(WB.book(obj)||{}).title||text)+'"')+'</div>'; }

  function chapterButton(ck, stage, label, primary) { return btn(label,'flow.stage','data-chapter="'+e(ck)+'" data-stage="'+stage+'"',primary); }
  function latest(ck,kind) { return (WB.S.reviewRuns||[]).find(function (r) { return r.chapter===ck && r.kind===kind; }); }
  var kinds=[['review','审稿'],['proof','校对'],['style','表达质量']];
  function reviewStatus(ck) {
    var ms=WB.msOf(ck), text=ms ? ms.paragraphs.join('\n') : '';
    return kinds.map(function (k) {var r=latest(ck,k[0]);return {key:k[0],label:k[1],run:r,current:!!r&&r.inputText===text&&r.ruleSnapshot===WB.reviewRuleSnapshot(WB.S.chapters[ck].bookId)&&WB.reviewBatchCurrent(ck,r.batchId), open:r?r.findings.filter(function (f) { return f.state!=='ignored'&&f.state!=='rechecked'; }).length:0};});
  }
  WB.reviewStandards=[{text:'文字、标点、称谓与数字一致性',type:'员工专业标准',source:'许清禾 · 校对方法 v1'},{text:'前文衔接、人物动机、背景规则与伏笔',type:'员工专业标准',source:'许清禾 · 连续性方法 v1'},{text:'叙事节奏、人物声纹、重复句式与空泛表达',type:'员工专业标准',source:'许清禾 · 表达方法 v1'}];
  WB.reviewRules=function(id){var c=WB.craftOf(id);return c.reviewRules||(c.reviewRules={version:1,items:[],history:[]});};
  WB.reviewRuleSnapshot=function(id){var r=WB.reviewRules(id);return JSON.stringify({version:r.version,standards:WB.reviewStandards,bookContext:WB.reviewBookContext(id),items:r.items.filter(function(x){return x.active;})});};
  WB.reviewBookContext=function(id){var c=WB.craftOf(id);return {positioning:c.positioning,world:c.world,characters:c.characters,arc:c.arc,outline:c.outline,scenes:c.scenes,storyState:(WB.S.storyState||{})[id],previousChapters:Object.keys(WB.S.chapters).filter(function(k){return WB.S.chapters[k].bookId===id;}).map(function(k){var m=WB.msOf(k);return {chapter:k,text:m?m.paragraphs:null};})};};
  WB.reviewBatchCurrent=function(ck,batchId){var b=(WB.S.reviewBatches||{})[ck];return !!b&&b.id===batchId&&b.state==='done'&&b.basis===WB.reviewRuleSnapshot(b.book)&&b.text===(WB.msOf(ck)||{paragraphs:[]}).paragraphs.join('\n');};
  function changeRules(id){var r=WB.reviewRules(id);r.history.push({at:WB.now(),version:r.version,items:WB.clone(r.items)});r.version++;return r;}
  WB.on['rules.open']=function(_,d){var r=WB.reviewRules(d.book);WB.modal({title:'本书写作与审校规则 · v'+r.version,body:'<h3>员工专业审校标准</h3><p>'+WB.reviewStandards.map(function(x){return e(x.text);}).join('；')+'</p><p>这些是默认审校方法，并非必须由用户填表。员工可补充本书专用标准；当前原型通过下方添加入口演示。</p><h3>本书依据</h3><p>已确认方向、人物、背景、大纲、故事状态与已载入章节；缺失的前文不视为检查通过。</p><h3>补充规则与硬性要求</h3><p>写前作为编辑要求，审校引用同一版规则。平台要求请记来源与核验日期；传闻留为待核实，不承诺避免限流。</p>'+r.items.map(function(x){return '<div class="reference-use"><b>'+e(x.text)+'</b><p>'+e(x.type)+' · '+e(x.source)+' · '+(x.active?'使用中':'已停用')+'</p>'+btn('编辑','rules.edit','data-book="'+d.book+'" data-id="'+x.id+'"')+btn(x.active?'移除（保留记录）':'恢复','rules.toggle','data-book="'+d.book+'" data-id="'+x.id+'"')+'</div>';}).join('')+'<small>历史规则版本：'+r.history.length+'；已生成报告继续保留旧规则依据。无关键词的语义要求会明确标为待核对。</small>',footer:btn('关闭','close-modal')+btn('请审校编辑补充标准','rules.suggest','data-book="'+d.book+'"')+btn('添加规则','rules.edit','data-book="'+d.book+'"',true)});};
  WB.on['rules.suggest']=function(_,d){var c=WB.craftOf(d.book),p=c.positioning||{},text='核对人物行为是否符合已确认动机，检查背景限制与伏笔兑现；';if(p.coreOriginal)text+='重点保持本书核心构思：'+p.coreOriginal;else text+='核心构思尚未确认时，先列为待作者核实，不替作者设定。';WB.S.__reviewSuggestion={book:d.book,text:text};WB.modal({title:'许清禾 · 本书审校标准建议',body:'<p>基于本书已载入设定整理（本地演示，未调用模型）。补充标准不放宽或覆盖你的硬性要求。</p><p>'+e(text)+'</p>',footer:btn('暂不加入','close-modal')+btn('加入本书审校依据','rules.acceptSuggestion','data-book="'+d.book+'"',true)});};
  WB.on['rules.acceptSuggestion']=function(_,d){var suggestion=WB.S.__reviewSuggestion;if(!suggestion||suggestion.book!==d.book)return;var r=WB.reviewRules(d.book);if(!r.items.some(function(x){return x.active&&x.type==='员工补充标准'&&x.text===suggestion.text;})){r=changeRules(d.book);r.items.push({id:'rule-'+r.version,text:suggestion.text,type:'员工补充标准',source:'许清禾 · 本书设定整理（演示）',phrase:'',active:true});}delete WB.S.__reviewSuggestion;WB.save();WB.render();WB.on['rules.open'](null,d);};
  WB.on['rules.edit']=function(_,d){var x=WB.reviewRules(d.book).items.find(function(r){return r.id===d.id;})||{};WB.modal({title:x.id?'编辑规则':'添加规则',body:'<label>规则要求<textarea class="ta" id="ruleText">'+e(x.text||'')+'</textarea></label><label>来源类型<select class="inp" id="ruleType">'+['用户硬性要求','作者偏好','员工补充标准','平台要求（用户提供）','待核实信息'].map(function(t){return '<option '+(x.type===t?'selected':'')+'>'+t+'</option>';}).join('')+'</select></label><label>来源／平台／核验日期<input class="inp" id="ruleSource" value="'+e(x.source||'')+'"></label><label>需要提醒的原句或词语（可选，按原文匹配）<input class="inp" id="rulePhrase" value="'+e(x.phrase||'')+'"></label>',footer:btn('取消','rules.open','data-book="'+d.book+'"')+btn('保存规则','rules.save','data-book="'+d.book+'" data-id="'+(x.id||'')+'"',true)});};
  WB.on['rules.save']=function(_,d){var v=function(id){return document.getElementById(id).value.trim();},text=v('ruleText'),type=v('ruleType'),source=v('ruleSource'),phrase=v('rulePhrase');if(!text||!source){WB.toast('请填写规则要求和来源，作者偏好也请标明。','warn');return;}var r=changeRules(d.book),x=r.items.find(function(x){return x.id===d.id;});if(!x){x={id:'rule-'+r.version,active:true};r.items.push(x);}Object.assign(x,{text:text,type:type,source:source,phrase:phrase});WB.save();WB.render();WB.on['rules.open'](null,d);};
  WB.on['rules.toggle']=function(_,d){var r=changeRules(d.book),x=r.items.find(function(x){return x.id===d.id;});x.active=!x.active;WB.save();WB.render();WB.on['rules.open'](null,d);};
  var reviewOrder=['proof','review','style'], reviewLabels=['文字与标点','剧情衔接与设定','表达质量与规则'];
  var activeReview={};
  WB.reviewFlow=function(id,ck){var batch=(WB.S.reviewBatches||{})[ck],running=batch&&batch.state==='running'&&activeReview[ck]===batch.id,current=batch&&WB.reviewBatchCurrent(ck,batch.id);return '<section class="flow-section"><div class="section-heading"><h2>许清禾 · 完整审稿</h2>'+btn('审校依据与规则','rules.open','data-book="'+id+'"')+'</div><div class="chapter-flow" role="status" aria-live="polite">'+reviewLabels.map(function(label,i){return '<span>'+((running&&batch.step===i)?'正在检查 · ':batch&&batch.completed>i?'✓ ':'')+label+'</span>';}).join('<span> → </span>')+'<span> → 汇总意见</span></div><p>员工专业标准＋本书设定与前文＋用户硬性要求。一次启动，自动完成各项检查。</p><p class="quiet-copy">本地流程演示：语义审校尚未接入模型；未发现问题不代表质量或平台审核通过。</p>'+ (running?'<p>许清禾正在审稿，无需逐项启动。</p>':btn(batch?'重新审稿':'开始审稿','review.start','data-book="'+id+'" data-chapter="'+ck+'"',true))+(batch&&!current&&!running?'<p class="notice">'+e(batch.state==='error'?'本轮中断：'+batch.error:batch.state==='running'?'上次审稿已中断，请重新开始。':'正文或审校依据已变化，请重新审稿；旧意见保留。')+'</p>':'')+'</section>';};
  WB.on['review.start']=function(_,d){var ch=WB.S.chapters[d.chapter];if(!ch)return;d.book=ch.bookId;var ms=WB.msOf(d.chapter);if(WB.S.__msDraft&&WB.S.__msDraft[d.chapter]!=null){WB.toast('请先保存草稿。','warn');return;}if(!ms||!ms.paragraphs.join('').trim()){WB.toast('请先写正文或合入候选草稿。','warn');return;}if(activeReview[d.chapter])return;
    WB.S.reviewBatches=WB.S.reviewBatches||{};var prior=WB.S.reviewBatches[d.chapter];WB.S.reviewBatchHistory=WB.S.reviewBatchHistory||[];if(prior)WB.S.reviewBatchHistory.push(WB.clone(prior));
    var batch={id:'audit-'+Date.now()+'-'+d.chapter,book:d.book,chapter:d.chapter,state:'running',step:0,completed:0,reportIds:[],text:ms.paragraphs.join('\n'),basis:WB.reviewRuleSnapshot(d.book),at:WB.now()};WB.S.reviewBatches[d.chapter]=batch;activeReview[d.chapter]=batch.id;WB.save();WB.go('book','manuscript',{bookId:d.book,chapter:d.chapter,stage:'review'});
    // ponytail: local passes yield to paint, not simulated provider progress; replace with real execution events when a model is connected.
    function advance(){try{if(batch.text!==WB.msOf(d.chapter).paragraphs.join('\n')||batch.basis!==WB.reviewRuleSnapshot(d.book)||(WB.S.__msDraft&&WB.S.__msDraft[d.chapter]!=null))throw Error('正文或审校依据发生变化，未混用两个版本。');
      var run=WB.act.reviewRun(d.book,d.chapter,reviewOrder[batch.step],batch.id);if(!run)throw Error('检查未返回结果');batch.reportIds.push(run.id);batch.completed++;batch.step++;
      if(batch.step===reviewOrder.length){batch.state='done';batch.finishedAt=WB.now();delete activeReview[d.chapter];}WB.save();WB.render();if(batch.state==='running')setTimeout(advance,120);
    }catch(err){batch.state='error';batch.error=err.message;delete activeReview[d.chapter];WB.save();WB.render();}}setTimeout(advance,120);
  };
  WB.on['review.next']=WB.on['review.start'];
  WB.reviewReport=function(id,ck){var b=(WB.S.reviewBatches||{})[ck];if(!b||b.state!=='done')return '<p class="quiet-copy">整套检查结束后在这里汇总审稿意见。</p>';return '<section><h2>本轮审稿意见</h2><p>同一份草稿 · 同一套依据 · 作者逐项裁决</p>'+reviewOrder.map(function(k,i){return '<details class="flow-details" open><summary>'+reviewLabels[i]+'</summary>'+WB.views['book.review'].render({params:{chapter:ck,kind:k,linear:true,batchId:b.id}})+'</details>';}).join('')+'</section>';};
  function referenceUses(b) {
    var uses=WB.craftOf(b.id).referenceUses||[];
    if (!uses.length) return '';
    return '<details class="flow-details"><summary>本书采用的参考方法 · '+uses.length+'</summary>'+uses.map(function (u) {
      var r=WB.byId(WB.S.references,u.refId);
      return '<div class="reference-use"><b>'+e(u.label)+'</b><p>'+e(u.adaptation)+'</p><small>用于'+e(u.targetLabel)+' · 来自 '+e(r?r.title:u.refId)+'</small>'+btn('回看拆解','market.refDetail','data-id="'+e(u.refId)+'"')+'</div>';
    }).join('')+'</details>';
  }

  WB.bookSummary=function(b){
    var keys=chs(b.id),words=keys.reduce(function(n,k){var m=WB.msOf(k);return n+(m?m.paragraphs.join('').replace(/\s/g,'').length:0);},0);
    var pending=keys.filter(function(k){var c=WB.S.chapters[k];return c.formal&&!c.published;}).length;var revisions=keys.filter(function(k){var c=WB.S.chapters[k];return c.formal&&c.published&&c.formal!==c.published;}).length;
    var first=b.serializationStartedAt,days=first?Math.max(0,Math.floor((new Date()-new Date(first))/86400000)):null;
    var count=b.publishedCount!=null?b.publishedCount+'章（快照）':'未登记';
    return '<div class="shelf-stats"><span>开书 <b>'+e(b.startedAt||'未登记')+'</b></span><span>连载 <b>'+e(days==null?'起始日未登记':days+'天')+'</b></span><span>正文 <b>'+(b.totalWordCount==null?words.toLocaleString()+'字（已载入）':b.totalWordCount.toLocaleString()+'字（已登记）')+'</b></span><span>已发布 <b>'+count+'</b></span><span>待发布 <b>'+pending+'章（已载入）</b></span><span>待发布修订 <b>'+revisions+'章（已载入）</b></span></div>';
  };
  WB.bookUtility=function(){var b=WB.scopeBook(),mode=WB.S.__ui.bookPanel||'positioning';
    var modes=[['positioning','方向'],['world','背景'],['characters','人物'],['arc','故事线'],['outline','大纲'],['scenes','场景']];
    if(WB.S.__route.view==='craft')return '<h2>故事准备</h2><p>'+e(b.title)+'</p>'+btn('回到刚才的工作','flow.prepReturn');
    return '<div class="utility-book"><h2>本书准备</h2><small>'+e(b.title)+'</small><div class="utility-modes">'+modes.map(function(x){return '<button class="'+(mode===x[0]?'active':'')+'" data-action="book.craftGo" data-book="'+b.id+'" data-mode="'+x[0]+'">'+x[1]+'</button>';}).join('')+'</div>'+nav('展开编辑','craft','data-book-id="'+b.id+'" data-mode="'+mode+'" data-full="1"')+WB.craftPanel(mode,{params:WB.S.__route.params||{}})+'</div>';
  };
  WB.bookShelf=function () {
    return head('作品','我的书架',btn('导入旧稿','nav.view','data-area="book" data-view="import"')+btn('开一本新书','act.b','data-fn="createBook"',true))+
      '<div class="book-shelf">'+WB.allBooks().map(function (b,i) {
        var keys=chs(b.id), c=WB.craftOf(b.id), last=keys.filter(function(k){return WB.S.chapters[k].candidate||(WB.msOf(k)&&!WB.S.chapters[k].published);}).slice(-1)[0]||keys[keys.length-1], ch=WB.S.chapters[last], title=c.positioning.coreOriginal||b.positioning||'从一个想法，开始你的故事。';
        return '<article class="shelf-book"><div class="book-spine tone-'+(i%3)+'"><span>'+e((b.genre||'创作中').split('/')[0])+'</span><strong>'+e(b.title)+'</strong></div><div class="shelf-copy"><div class="eyeline">'+e(b.platform||'平台待定')+' · '+(keys.length?'创作中':'准备开写')+'</div><h2>'+e(b.title)+'</h2><p>'+e(title)+'</p><div class="shelf-next">'+e(ch?'第 '+ch.no+' 章 · '+ch.title:'还没有章节，编辑陪你从构思开始')+'</div>'+WB.bookSummary(b)+'<div class="btnrow">'+btn('进入这本书','book.open','data-id="'+b.id+'"',true)+'</div></div></article>';
      }).join('')+'</div>';
  };
  WB.bookHome=function (ctx) {
    var b=WB.book(ctx.params.bookId||WB.S.__scope.bookId), c=WB.craftOf(b.id), keys=chs(b.id);
    WB.S.__scope.bookId=b.id;
    var o=WB.onbState(b.id), ck=keys.filter(function(k){var m=WB.msOf(k);return !!WB.S.chapters[k].candidate||(m&&m.paragraphs.length&&!WB.S.chapters[k].published);}).slice(-1)[0]||keys[keys.length-1], ch=WB.S.chapters[ck];
    var steps=[['positioning','构思方向','一句故事、题材与文风'],['world','背景与规则','故事发生的地方与限制'],['characters','人物','动机、关系与成长'],['arc','故事线与结局','主线、支线与走向'],['outline','大纲','从全书到章节'],['scenes','场景准备','让下一章有明确的推进']];
    return head('我的书架 / 本书创作',b.title,nav('返回书架','library'))+
      (o.done && ck ? '<section class="next-work"><div class="eyeline">继续你的故事</div><h2>第 '+ch.no+' 章 · '+e(ch.title)+'</h2><p>'+e(c.positioning.coreOriginal||b.positioning||'继续本书创作')+'</p>'+editor(ck,'负责这一章的写作与修改')+chapterButton(ck,'write','继续这一章',true)+'</section>' : WB.onbPanel(b,c))+
      '<details class="flow-details"><summary>故事准备 · 人物、背景、大纲与场景在右栏编辑</summary><div class="planning-links">'+steps.map(function (s) {return '<button data-action="book.craftGo" data-book="'+b.id+'" data-mode="'+s[0]+'"><b>'+s[1]+'</b><span>'+s[2]+'</span><i>↗</i></button>';}).join('')+'</div></details>'+
      (function(){var items=WB.S.learningUsage.filter(function(u){return u.where==='outline:'+b.id;});return items.length?'<section class="flow-section"><div class="section-heading"><h2>后续大纲采用的经验</h2></div>'+items.map(function(u){var l=u.sourceSnapshot||WB.learning(u.learningId);return '<div class="chapter-row"><b>'+e(l?l.text:u.learningId)+'</b><p>计划调整：'+e(u.adaptation||u.reason||'未填写')+' · 依据 '+e(((l&&l.evidence)||u.source||[]).join('、'))+' · 反例 '+e((l&&l.counter)||u.counter||'待补')+'</p></div>';}).join('')+'<div class="sm t3">作为编辑规划依据；大纲尚未自动改写，后续需作者确认并观察。</div></section>':'';})()+
      '<section class="flow-section"><div class="section-heading"><h2>章节</h2>'+btn('新增一章','act.b','data-fn="newChapter" data-a1="'+b.id+'"')+'</div>'+
      (keys.length?keys.map(function (k) {var x=WB.S.chapters[k];return '<div class="chapter-row"><span class="chapter-no">'+String(x.no).padStart(2,'0')+'</span><div><b>'+e(x.title)+'</b><small>'+e(WB.chapState(x)[0])+'</small></div>'+chapterButton(k,'write','打开')+'</div>';}).join(''):'<p class="quiet-copy">构思准备好后，就可以从第一章开始。也可以直接手写。</p>')+'</section>'+referenceUses(b)+
      '<details class="flow-details"><summary>本书资料与经营</summary><div class="btnrow">'+nav('故事资料','story')+btn('发布记录','nav.view','data-area="publish" data-view="queue"')+btn('读者反馈','nav.view','data-area="audience" data-view="comments"')+nav('导入旧稿','import')+'</div></details>';
  };
  // Existing onboarding actions and state remain the source of truth; only reduce its presentation.
  WB.onbPanel=function (b,c) {
    var st=WB.onbState(b.id), step=st.step||{id:'chapter',name:'准备第一章'}, seed=(WB.S.__seedDraft||{})[b.id]!=null?WB.S.__seedDraft[b.id]:(c.positioning.seedRaw||c.positioning.seed||'');
    var configs={idea:['写下一点构思','不用先想好一切。可以是一种题材、一个人物，或者一个让你想写下去的场景。','book.onbSeed','请编辑一起构思'],dir:['选择故事方向','沈知远已准备好方向候选。比较冲突和取舍，再决定你想写哪一种。','book.onbDir','查看方向候选'],base:['让故事有自己的世界和人物','先补这一章会用到的背景、主角与冲突。所有建议由你确认。','book.onbBase','和编辑补设定'],plan:['把想法连成故事','从主线和转折开始，决定第一章把读者带到哪里。','book.onbPlan','一起规划故事线'],chapter:['试写第一章','先拿到一个开头，再一起修改。生成内容仍是待你选择的候选。','book.onbFirst','准备第一章候选']};
    var x=configs[step.id]||configs.chapter;
    return '<section class="next-work"><div class="onb-ladder">'+WB.onbSteps().map(function (s,i) {return '<span class="onb-step '+(i<st.idx?'done':i===st.idx?'cur':'')+'">'+(i<st.idx?'✓ ':'')+e(s.name)+'</span>';}).join('<span class="onb-arrow">→</span>')+'</div><h2>'+x[0]+'</h2><p>'+x[1]+'</p>'+editor(b.id,'陪你构思这本书')+
      (step.id==='idea'?'<label class="sr-only" for="onbSeed">故事构思</label><textarea class="ta idea-input" id="onbSeed" data-input="flow.seed" placeholder="例如：档案员每天收到一份明天的报纸……">'+e(seed)+'</textarea>':seed?'<blockquote>'+e(seed)+'</blockquote>':'')+
      '<div class="btnrow">'+btn(x[3],x[2],'data-book="'+b.id+'"',true)+btn('先手写','book.onbSkipIdea','data-book="'+b.id+'"')+'</div><small class="quiet-copy">可随时返回继续 · 编辑建议为本地演示</small></section>';
  };
  WB.on['flow.prepReturn']=function(){WB.back();};
  WB.on['flow.seed']=function(_,d){WB.S.__seedDraft=WB.S.__seedDraft||{};WB.S.__seedDraft[WB.S.__scope.bookId]=d.value;WB.save();};
  WB.on['flow.stage']=function (_,d) {
    var ch=WB.S.chapters[d.chapter]; if(!ch)return;
    WB.go('book','manuscript',{bookId:ch.bookId,chapter:d.chapter,stage:d.stage||'write'});
  };
  WB.on['flow.chapter']=function (_,d) {WB.on['flow.stage'](null,{chapter:d.value,stage:'write'});};
  WB.on['flow.checkAll']=WB.on['review.start'];
  WB.canFinalize=function (ck) {
    var stale=reviewStatus(ck).some(function(r){return !r.current;});
    if(stale){WB.toast('请先检查当前草稿的审稿、校对与表达质量，再确认定稿。','warn');WB.on['flow.stage'](null,{chapter:ck,stage:'review'});return false;}
    return true;
  };
  WB.on['flow.finalize']=function (_,d) {
    if(!WB.canFinalize(d.chapter))return;
    var unresolved=reviewStatus(d.chapter).reduce(function(n,r){return n+r.open;},0);
    var reason=(document.getElementById('authorReason')||{}).value||'';
    if(unresolved&&!reason.trim()){WB.toast('仍有检查建议：请处理，或写明作者保留当前表达的理由。','warn');return;}
    var ms=WB.msOf(d.chapter);
    if(WB.S.__msDraft&&WB.S.__msDraft[d.chapter]!=null){WB.toast('存在未保存修改，先返回正文保存。','warn');return;}
    ms.authorReview={at:WB.now(),reason:reason.trim(),reports:reviewStatus(d.chapter).map(function(r){return r.run.id;})};
    WB.act.msConfirmFormal(d.chapter);
    WB.on['flow.stage'](null,{chapter:d.chapter,stage:'publish'});
  };
  WB.mergeCandidateDraft=function (id) {
    var c=WB.candidate(id),st=WB.candidateState(id),ch=c&&WB.S.chapters[c.chapter];
    if(!c||!ch)return;
    if(st.open){WB.toast('先逐项采纳或拒绝候选。','warn');return;}
    if(c.draftMerged){WB.on['flow.stage'](null,{chapter:c.chapter,stage:'review'});return;}
    var ms=WB.msOf(c.chapter)||WB.msEnsure(c.chapter,ch.bookId,ch.title);
    if(WB.S.__msDraft&&WB.S.__msDraft[c.chapter]!=null){WB.toast('有未保存的手写修改，请先保存。','warn');return;}
    if(c.baseVersion&&ms.formalVersion&&c.baseVersion!==ms.formalVersion){WB.toast('候选基于旧正式版本，请先重新对照。','warn');return;}
    var picks=c.changes.filter(function(x){return x.applied===true;});
    if(picks.some(function(x){return x.before&&ms.paragraphs[(x.para||1)-1]!==x.before;})){WB.toast('原段落已经变化，未覆盖；请重新生成局部候选。','warn');return;}
    picks.forEach(function(x){var i=(x.para||ms.paragraphs.length+1)-1;if(x.after){if(i<ms.paragraphs.length)ms.paragraphs[i]=x.after;else ms.paragraphs.push(x.after);}});
    if(!ms.paragraphs.length){WB.toast('本次未采纳任何正文，可继续手写或重新讨论。','warn');return;}
    ms.updatedAt=WB.now();ms.versions.push({v:'草稿 r'+(ms.versions.filter(function(x){return x.kind==='draft';}).length+1),kind:'draft',at:WB.now(),note:'候选 '+id+' 合入草稿；尚未定稿',paragraphs:ms.paragraphs.slice()});
    c.draftMerged=WB.now();WB.save();WB.on['flow.stage'](null,{chapter:c.chapter,stage:'review'});
    WB.toast('已合入草稿，接下来检查本章。正式稿与线上稿未改变。','ok');
  };
  WB.act.applyCandidate=WB.mergeCandidateDraft; // All candidate entry points stop at draft review.
  function statusSummary(ck) {return '<div class="check-summary">'+reviewStatus(ck).map(function(r){return '<span><b>'+r.label+'</b> '+(!r.run?'尚未检查':!r.current?'需重新检查':r.open?r.open+' 条建议':'已检查')+'</span>';}).join('')+'</div>';}
  WB.chapterFrame=function (b,ck,msBlock,candCol,ctx) {
    var ch=WB.S.chapters[ck],ms=WB.msOf(ck),stage=ctx.params.stage||'write',keys=chs(b.id),cand=ch.candidate&&WB.candidate(ch.candidate);
    var stages=[['write','写作'],['review','审校'],['confirm','确认定稿'],['publish','排期与发布']];
    var top=head(b.title,'第 '+ch.no+' 章 · '+ch.title,nav('返回本书','overview'))+
      '<div class="chapter-toolbar"><label>章节 <select data-change="flow.chapter" aria-label="选择章节">'+keys.map(function(k){return '<option value="'+k+'"'+(k===ck?' selected':'')+'>第 '+WB.S.chapters[k].no+' 章 · '+e(WB.S.chapters[k].title)+'</option>';}).join('')+'</select></label>'+btn('本章要求','craft.picker','data-book="'+b.id+'" data-scope="chapter" data-chapter="'+ck+'"')+btn('版本记录','book.versions','data-chapter="'+ck+'"')+'</div>'+
      '<nav class="chapter-flow" aria-label="本章工作流程">'+stages.map(function(x,i){return '<button class="'+(stage===x[0]?'active':'')+'" data-action="flow.stage" data-chapter="'+ck+'" data-stage="'+x[0]+'"'+(stage===x[0]?' aria-current="step"':'')+'><span>0'+(i+1)+'</span>'+x[1]+'</button>';}).join('')+'</nav>'+
      editor(ck,stage==='review'?'检查本章的情节、文字与表达':stage==='confirm'?'整理修改，等待你确认定稿':stage==='publish'?'本章创作已交付，发布由郑一鸣接续':'与你一起推进本章',stage==='review');
    var content='';
    if(stage==='write'){
      var showCandidate=!!cand&&!cand.draftMerged&&!WB.candidateState(cand.id).applied;
      content=btn('本书写作与审校规则','rules.open','data-book="'+b.id+'"')+'<div class="chapter-writing">'+msBlock+'</div>'+ (showCandidate?'<details class="flow-details candidate-details"'+(cand.baseVersion&&ms&&ms.formalVersion&&cand.baseVersion!==ms.formalVersion?'':' open')+'><summary>编辑候选 · '+(cand.baseVersion&&ms&&ms.formalVersion&&cand.baseVersion!==ms.formalVersion?'基于旧版本，需重新对照':'逐项选择后合入草稿')+'</summary>'+candCol+'</details>':'')+
        '<div class="flow-next"><span>草稿随时可以保存。写完这一章后，继续审校。</span>'+chapterButton(ck,'review','写完了，去审校 →',true)+'</div>'+referenceUses(b)+
        '<details class="flow-details"><summary>场景与写作依据</summary>'+nav('打开场景准备','craft','data-mode="scenes"')+(WB.craftBasisHtml?WB.craftBasisHtml(b.id,ck,{compact:true}):'')+'</details>';
    }else if(stage==='review'){
      content=WB.reviewFlow(b.id,ck)+
        WB.reviewReport(b.id,ck)+
        '<div class="flow-next">'+chapterButton(ck,'write','← 回到正文修改')+chapterButton(ck,'confirm','检查后，确认定稿 →',true)+'</div>';
    }else if(stage==='confirm'){
      var checks=reviewStatus(ck),ready=checks.every(function(r){return r.current;}),open=checks.reduce(function(n,r){return n+r.open;},0);
      var identical=ms&&ms.formal&&!WB.draftDiverged(ck);
      content='<section class="formal-confirm"><h2>'+(identical?'当前草稿与正式稿一致':'把这一版确认为正式稿')+'</h2><p>确认后保留历史版本；尚未提交到平台。</p>'+statusSummary(ck)+
        '<div class="manuscript-preview">'+(ms&&ms.paragraphs.length?ms.paragraphs.slice(0,3).map(function(p){return '<p>'+e(p)+'</p>';}).join(''):'<p>本章尚无正文。</p>')+'</div>'+
        (!ready?'<p class="notice">检查尚未齐备，或正文有了新修改。请返回审校当前草稿。</p>':'')+
        (ready&&open?'<label for="authorReason">仍有 '+open+' 条建议。若决定保留当前表达，请写下理由</label><textarea class="ta" id="authorReason" placeholder="例如：这一处重复是我有意保留的叙述节奏。"></textarea>':'')+
        '<div class="flow-next">'+chapterButton(ck,'review','← 回到审校')+(identical?chapterButton(ck,'publish','查看排期与发布 →',true):'<button class="btn primary" data-action="flow.finalize" data-chapter="'+ck+'"'+(!ready||!ms||!ms.paragraphs.length?' disabled':'')+'>确认定稿，继续发布准备</button>')+'</div></section>';
    }else{
      var q=WB.S.queue.filter(function(x){return x.chapter===ck&&x.version===ch.formal;}).slice(-1)[0];
      var names={draft:'待排期',scheduled:'已排期（本地计划）',waiting:'等待平台回执',unknown:'外部状态未知',live:'已核验上线',rejected:'平台退回'};
      content='<section class="publication-step"><div class="section-heading"><h2>这一章的发布</h2>'+WB.ownerHtml('E-03')+'</div>'+
        '<dl class="flow-facts"><dt>正式版本</dt><dd>'+e(ch.formal||'尚未定稿')+'</dd><dt>目标平台</dt><dd>'+e(b.platform||'待设置')+'</dd><dt>线上版本</dt><dd>'+e(ch.published||'尚未发布')+'</dd><dt>当前状态</dt><dd>'+e(q?names[q.state]||q.state:'尚未加入发布队列')+'</dd>'+(q?'<dt>计划时间</dt><dd>'+e(q.plannedAt||'待设置')+'</dd>':'')+'</dl><div class="btnrow">'+
        (!ch.formal?chapterButton(ck,'confirm','先确认正式稿',true):!q?btn('加入发布队列','act.q','data-fn="queueAdd" data-a1="'+ck+'"',true):
          (q.state==='draft'||q.state==='scheduled'?btn('设置排期','pub.resched','data-id="'+q.id+'"',true):'')+btn('查看发布包与交接','pub.pkg','data-id="'+q.id+'"'))+
        btn('打开发布队列','nav.view','data-area="publish" data-view="queue"')+'</div><p class="quiet-copy">这里准备和跟踪发布。平台提交、等待回执与核验上线是不同状态。</p></section>';
    }
    return top+content;
  };

  // Reference analysis: stable dimensions, honest evidence and explicit reuse destination.
  var dimensions=[['theme','主题与读者承诺'],['structure','结构与篇章组织'],['storyline','主支线与因果'],['rhythm','叙事节奏'],['character','人物性格与塑造'],['relationship','人物关系与成长弧'],['conflict','冲突与悬念'],['hook','开篇与章末钩子'],['style','文风、视角与对白'],['world','背景与世界规则'],['payoff','伏笔、转折与兑现']];
  WB.analysisDimensions=dimensions;
  function analysisRows(r){return dimensions.map(function(d){var own=(r.breakdown||{})[d[0]]||{};return {key:d[0],label:d[1],observation:own.observation||r[d[0]]||'',evidence:own.evidence||'',reuse:own.reuse||'',limit:own.limit||r.limit||'尚无充分依据'};});}
  WB.views['market.references'].render=function () {
    return head('市场与方向','参考书与拆解','')+'<p class="quiet-copy">读懂一本书，再决定哪些写作方法值得借鉴。</p><div class="reference-list">'+WB.S.references.map(function(r){var rows=analysisRows(r),done=rows.filter(function(x){return !!x.observation;}).length;return '<article class="reference-row"><div class="reference-mark">书</div><div><h2>'+e(r.title)+'</h2><p>'+e(r.genre)+' · '+e(r.platform)+' · '+done+'/'+dimensions.length+' 项有阅读笔记</p><small>'+e(r.scope)+'</small></div>'+btn('打开拆解','market.refDetail','data-id="'+r.id+'"',true)+'</article>';}).join('')+'</div>';
  };
  WB.on['market.refDetail']=function (_,d){WB.closeDrawer();WB.go('market','reference',{id:d.id});};
  WB.register('market.reference',{render:function(ctx){
    var r=WB.byId(WB.S.references,ctx.params.id);if(!r)return ui.empty('未找到参考','返回参考列表重新选择。');
    var rows=analysisRows(r),active=ctx.params.dimension||'structure',x=rows.find(function(y){return y.key===active;})||rows[0];
    var patterns=WB.S.patterns.filter(function(p){return(p.from||[]).indexOf(r.id)>=0;});
    return head('参考书与拆解',r.title,btn('返回参考列表','nav.view','data-area="market" data-view="references"'))+
      '<div class="source-strip"><span>'+e(r.genre)+' · '+e(r.scope)+'</span><span>'+e(r.sample?'虚构演示样例':r.own?'自有作品':'阅读笔记')+'</span></div>'+
      '<div class="editor-line"><span class="editor-avatar">陆</span><div><b>陆晓白</b><span>研究编辑 · 阅读依据、提炼方法；由你决定如何借用</span></div></div>'+
      '<div class="reference-analysis"><nav aria-label="拆解维度">'+rows.map(function(y){return '<button data-action="ref.dimension" data-id="'+r.id+'" data-key="'+y.key+'" class="'+(y.key===x.key?'active':'')+'">'+y.label+'<small>'+(y.observation?'已记录':'待分析')+'</small></button>';}).join('')+'</nav><section class="analysis-main"><div class="section-heading"><h2>'+x.label+'</h2>'+btn('编辑分析','ref.edit','data-id="'+r.id+'" data-key="'+x.key+'"')+'</div>'+
      '<div class="analysis-part"><label>观察结论</label><p>'+e(x.observation||'尚未分析。只读了元数据时，不推断正文写法。')+'</p></div><div class="analysis-part"><label>原文依据 / 章节范围</label><p>'+e(x.evidence||'尚未记录原文位置；现有摘要仅为阅读笔记，待补依据。')+'</p></div><div class="analysis-part"><label>可复用的方法</label><p>'+e(x.reuse||'还未提炼。说明借鉴什么方法，以及本书如何做出不同表达。')+'</p></div><div class="analysis-part"><label>适用边界 / 反例</label><p>'+e(x.limit)+'</p></div><div class="flow-next"><span>只引用方法，不复制参考的正文或人物设定。</span>'+btn('用于我的作品','ref.use','data-id="'+r.id+'" data-key="'+x.key+'"',true)+'</div></section></div>'+
      '<details class="flow-details"><summary>已提炼的方法候选 · '+patterns.length+'</summary>'+patterns.map(function(p){return '<div class="reference-use"><b>'+e(p.text)+'</b><p>适用：'+e(p.scope)+'</p><p>反例：'+e(p.counter)+'</p><small>'+e(p.caution)+'</small></div>';}).join('')+'</details>';
  }});
  WB.on['ref.dimension']=function (_,d){WB.go('market','reference',{id:d.id,dimension:d.key},{replace:true});};
  WB.on['ref.edit']=function (_,d){var r=WB.byId(WB.S.references,d.id),x=analysisRows(r).find(function(y){return y.key===d.key;});WB.modal({title:'编辑拆解 · '+x.label,body:[['observation','观察结论'],['evidence','原文依据与位置'],['reuse','可复用方法'],['limit','适用边界与反例']].map(function(a){return '<label for="ref-'+a[0]+'">'+a[1]+'</label><textarea class="ta" id="ref-'+a[0]+'">'+e(x[a[0]])+'</textarea>';}).join(''),footer:btn('取消','close-modal')+btn('保存分析','ref.save','data-id="'+r.id+'" data-key="'+d.key+'"',true)});};
  WB.on['ref.save']=function (_,d){var r=WB.byId(WB.S.references,d.id),x={};['observation','evidence','reuse','limit'].forEach(function(k){x[k]=document.getElementById('ref-'+k).value.trim();});r.breakdown=r.breakdown||{};r.breakdown[d.key]=x;WB.closeModal();WB.rerender();};
  WB.on['ref.use']=function (_,d){var r=WB.byId(WB.S.references,d.id),x=analysisRows(r).find(function(y){return y.key===d.key;});WB.modal({title:'把方法用于自己的故事',body:'<p>'+e(x.label)+' · '+e(x.reuse||x.observation||'先写下想借鉴的方法')+'</p><label for="refBook">用在哪本书</label><select id="refBook" class="sel">'+WB.allBooks().map(function(b){return '<option value="'+b.id+'"'+(b.id===WB.S.__scope.bookId?' selected':'')+'>'+e(b.title)+'</option>';}).join('')+'</select><label for="refTarget">用于什么</label><select id="refTarget" class="sel"><option value="positioning">创作方向</option><option value="outline">大纲与故事线</option><option value="characters">人物塑造</option><option value="scenes">章节与场景准备</option></select><label for="refAdapt">我的转化方式</label><textarea id="refAdapt" class="ta" placeholder="写下如何用于自己的故事，而不是照搬参考。"></textarea>'+(!x.evidence?'<p class="notice">原文依据尚未补齐，将作为待验证参考保留。</p>':''),footer:btn('取消','close-modal')+btn('确认引用，进入本书','ref.attach','data-id="'+r.id+'" data-key="'+x.key+'"',true)});};
  WB.on['ref.attach']=function (_,d){var bid=document.getElementById('refBook').value,target=document.getElementById('refTarget'),adapt=document.getElementById('refAdapt').value.trim();if(!adapt){WB.toast('请说明如何转化到自己的故事。','warn');return;}var r=WB.byId(WB.S.references,d.id),x=analysisRows(r).find(function(y){return y.key===d.key;}),c=WB.craftOf(bid);c.referenceUses=c.referenceUses||[];var existing=c.referenceUses.find(function(u){return u.refId===r.id&&u.dimension===x.key&&u.target===target.value;});var use={refId:r.id,dimension:x.key,label:x.label,target:target.value,targetLabel:target.options[target.selectedIndex].text,adaptation:adapt,evidence:x.evidence,confirmedAt:WB.now()};if(existing)Object.assign(existing,use);else c.referenceUses.push(use);WB.S.__scope.bookId=bid;WB.closeModal();WB.save();WB.go('book','craft',{bookId:bid,mode:target.value});WB.toast('方法已关联本书，可在创作依据中回看；正文未改动。','ok');};
  var craftRender=WB.views['book.craft'].render;
  WB.views['book.craft'].render=function(ctx){return craftRender(ctx)+referenceUses(WB.scopeBook());};
})();
