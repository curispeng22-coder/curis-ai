(function(){
  const modal=document.querySelector('[data-create-modal]');
  const toast=document.querySelector('[data-toast]');
  const statusNodes=document.querySelectorAll('[data-project-status]');
  const open=()=>{if(modal) modal.hidden=false};
  const close=()=>{if(modal) modal.hidden=true};
  document.querySelectorAll('[data-open-create]').forEach(el=>el.addEventListener('click',open));
  document.querySelectorAll('[data-close-create]').forEach(el=>el.addEventListener('click',close));
  if(modal) modal.addEventListener('click',e=>{if(e.target===modal)close()});
  if(modal && new URLSearchParams(location.search).get('create')==='1') open();
  const form=document.querySelector('[data-create-form]');
  if(form) form.addEventListener('submit',e=>{
    e.preventDefault();
    statusNodes.forEach(el=>{el.textContent='已创建草稿';el.classList.remove('planning');el.classList.add('running')});
    close();
    if(toast){toast.textContent='项目草稿已创建。当前为本地原型状态，尚未写入后端。';toast.hidden=false;setTimeout(()=>{toast.hidden=true},3200)}
  });
  const preview=document.querySelector('[data-preview-run]');
  if(preview) preview.addEventListener('click',()=>{
    document.querySelectorAll('[data-node-state]').forEach((el,i)=>{if(i<3){el.textContent='预览完成';el.style.color='var(--state-success)'}});
    if(toast){toast.textContent='已生成一次本地预览，不会触发真实发布。';toast.hidden=false;setTimeout(()=>{toast.hidden=true},3200)}
  });
})();

(function(){
  const overlay=document.querySelector('[data-resource-overlay]');
  if(!overlay) return;
  const title=overlay.querySelector('[data-resource-title]');
  const subtitle=overlay.querySelector('[data-resource-subtitle]');
  const options=overlay.querySelector('[data-resource-options]');
  const summary=overlay.querySelector('[data-resource-summary]');
  const toast=document.querySelector('[data-toast]');
  const catalog={
    model:[['Curis Auto','按任务自动选择可用模型'],['GPT-4o','通用推理 · 适合结构化输出'],['Claude 3.5','长文本与代码审阅']],
    skill:[['code-generation','代码生成 · 研发任务'],['content-planning','内容策划 · 选题与结构'],['brand-tone','品牌语气 · 统一表达']],
    tool:[['GitHub Tool','代码仓库与变更记录'],['微信开发者工具','小程序预览与构建'],['内容选题库 Tool','读取内容增长选题']]
  };
  const labels={model:'模型',skill:'Skill',tool:'Tool'};
  let active='model';
  const defaults={model:'Curis Auto',skill:'code-generation',tool:'GitHub Tool'};
  let selection={...defaults};
  const selections={};
  let source=null;
  const close=()=>{overlay.hidden=true};
  const render=()=>{
    overlay.querySelectorAll('[data-resource-tab]').forEach(tab=>tab.classList.toggle('active',tab.dataset.resourceTab===active));
    options.innerHTML=catalog[active].map(item=>`<button class="resource-option ${selection[active]===item[0]?'selected':''}" type="button" data-resource-option="${item[0]}"><span><span class="resource-option-name">${item[0]}</span><span class="resource-option-meta">${item[1]}</span></span><span class="resource-check">${selection[active]===item[0]?'✓':''}</span></button>`).join('');
    summary.innerHTML=Object.keys(selection).map(kind=>`<span class="resource-chip ${kind}">${labels[kind]} · ${selection[kind]}</span>`).join('');
  };
  document.querySelectorAll('[data-open-resource-picker]').forEach(el=>el.addEventListener('click',()=>{
    source=el;
    selection={...(selections[el.dataset.scope]||defaults)};
    const agent=el.dataset.agent;
    title.textContent=agent?`配置执行员工 · ${agent}`:'配置本次对话资源';
    subtitle.textContent=agent?'点击下方选项，覆盖该员工本次执行使用的模型、Skill 和 Tool。':'只作用于当前对话，不改变项目默认配置。';
    active='model';render();overlay.hidden=false;
  }));
  overlay.addEventListener('click',e=>{
    if(e.target===overlay||e.target.closest('[data-close-resource]')) close();
    const tab=e.target.closest('[data-resource-tab]');
    if(tab){active=tab.dataset.resourceTab;render()}
    const option=e.target.closest('[data-resource-option]');
    if(option){selection[active]=option.dataset.resourceOption;render()}
    if(e.target.closest('[data-apply-resources]')){
      if(source){const scope=source.dataset.scope;selections[scope]={...selection};const scopeEl=scope&&document.querySelector(`[data-resource-scope="${scope}"]`);if(scopeEl) Object.keys(selection).forEach(kind=>{const chip=scopeEl.querySelector(`[data-resource-chip="${kind}"]`);if(chip) chip.textContent=`${labels[kind]} · ${selection[kind]}`})}
      close();
      if(toast){toast.textContent='资源配置已应用到当前对话/执行员工（本地原型状态）。';toast.hidden=false;setTimeout(()=>toast.hidden=true,3000)}
    }
  });
})();
