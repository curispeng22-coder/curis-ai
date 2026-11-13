(function () {
  var page = (location.pathname.split('/').pop() || 'ceo-home.html').toLowerCase();
  var groups = [
    {key:'ceo',label:'总裁办公室',icon:'⌂',href:'ceo-home.html',children:[['决策中心','decision-center.html'],['重要汇报','reports.html'],['战略会议室','strategy-room.html']]},
    {key:'project',label:'项目中心',icon:'▣',href:'project-center.html',children:[['研发部项目','project-dept.html?dept=研发部'],['内容增长部项目','project-dept.html?dept=内容增长部'],['产品部项目','project-dept.html?dept=产品部'],['运营部项目','project-dept.html?dept=运营部']]},
    {key:'org',label:'组织中心',icon:'♧',href:'org-center.html',children:[['部门空间','org-center.html#department-spaces'],['人事部 · 员工管理','org-employees.html']]},
    {key:'capability',label:'能力中心',icon:'◇',href:'capability-center.html',children:[['模型 Model','capability-model-list.html'],['Skill','capability-skill-list.html'],['Tool','capability-tool-list.html'],['Workflow','capability-workflow-list.html']]},
    {key:'analytics',label:'经营分析',icon:'⌁',href:'analytics.html',children:[['组织维度','analytics-org.html'],['项目维度','analytics-project.html'],['Workflow 维度','analytics-workflow.html']]},
    {key:'brainstorm',label:'头脑风暴室',icon:'✦',href:'brainstorm.html',children:[['进行中的会话','brainstorm-active.html'],['产出结果','brainstorm-results.html']]},
    {key:'knowledge',label:'知识中心',icon:'▤',href:'knowledge.html',children:[['公司级知识','knowledge-company.html'],['项目级知识','knowledge-project.html'],['部门级知识','knowledge-dept.html']]},
    {key:'execution',label:'执行工作台',icon:'›',href:'execution.html',children:[['任务队列','execution-tasks.html'],['运行记录','execution-runs.html']]},
    {key:'settings',label:'公司设置',icon:'⚙',href:'settings.html',children:[['公司档案','settings-profile.html'],['品牌与视觉','settings-brand.html'],['通知设置','settings-notify.html']]}
  ];
  var query=location.search||'';
  function base(href){return href.split('?')[0].split('#')[0]}
  function matches(href){var parts=href.split('?');return page===base(href)&&(!parts[1]||query===('?'+parts[1]))}
  function groupKey(){
    for(var i=0;i<groups.length;i++){
      if(matches(groups[i].href)) return groups[i].key;
      for(var j=0;j<groups[i].children.length;j++) if(matches(groups[i].children[j][1])) return groups[i].key;
      if(groups[i].key==='project' && /^(project-(detail|miniapp-detail|xhs-workflow-detail|dept))\.html$/.test(page)) return 'project';
      if(groups[i].key==='org' && /^(department-detail|employee-detail|org-dept|org-employees)\.html$/.test(page)) return 'org';
      if(groups[i].key==='capability' && /^(skill-detail|capability-.*-list)\.html$/.test(page)) return 'capability';
      if(groups[i].key==='ceo' && page==='company-runtime.html') return 'ceo';
    }
    return 'ceo';
  }
  function render(host){
    var activeKey=groupKey(); host.classList.add('curis-nav-v2');
    host.innerHTML='<div class="curis-brand"><span class="curis-brand-mark">C</span><span>Curis</span></div><nav class="curis-nav-menu" aria-label="产品导航"></nav><div class="curis-nav-note">对象详情从中心列表进入，导航只保留稳定产品空间。</div>';
    var nav=host.querySelector('.curis-nav-menu');
    groups.forEach(function(g){
      var active=g.key===activeKey, link=document.createElement('a'); link.className='curis-nav-link'+(active?' active':''); link.href=g.href; link.innerHTML='<span class="curis-nav-icon" aria-hidden="true">'+g.icon+'</span><span class="curis-nav-text">'+g.label+'</span><span class="curis-nav-chevron" aria-hidden="true">›</span>'; nav.appendChild(link);
      var sub=document.createElement('div'); sub.className='curis-subnav'+(active?' open':'');
      g.children.forEach(function(c){var a=document.createElement('a');a.className='curis-sub-link'+(matches(c[1])?' active':'');a.href=c[1];a.textContent=c[0];sub.appendChild(a)}); nav.appendChild(sub);
      link.addEventListener('click',function(e){if(active&&e.target.closest('.curis-nav-chevron')){e.preventDefault();sub.classList.toggle('open');link.classList.toggle('active')}});
    });
  }
  function install(){
    if(document.body&&document.body.dataset.curisNavInstalled)return;
    if(document.body)document.body.dataset.curisNavInstalled='1';
    if(!document.querySelector('link[data-curis-nav-css],link[href*="navigation-ia.css"]')){var css=document.createElement('link');css.rel='stylesheet';css.href='../assets/navigation-ia.css';css.dataset.curisNavCss='';document.head.appendChild(css)}
    var host=document.querySelector('.sidebar')||document.querySelector('.side');
    if(!host){var runtime=document.querySelector('.runtime-main');if(runtime){host=document.createElement('aside');host.className='sidebar';runtime.parentNode.insertBefore(host,runtime)}}
    if(!host)return; render(host);
    if(window.matchMedia&&window.matchMedia('(max-width:767px)').matches){var t=document.createElement('button');t.type='button';t.className='curis-nav-toggle';t.setAttribute('aria-label','打开产品导航');t.textContent='☰';var b=document.createElement('div');b.className='curis-nav-backdrop';document.body.appendChild(t);document.body.appendChild(b);t.onclick=function(){host.classList.toggle('open');b.classList.toggle('open')};b.onclick=function(){host.classList.remove('open');b.classList.remove('open')}}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();
