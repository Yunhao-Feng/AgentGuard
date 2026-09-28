(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const all = s => [...document.querySelectorAll(s)];
  const get = key => {try {return localStorage.getItem(key);} catch {return null;}};
  const save = (key,value) => {try {localStorage.setItem(key,value);} catch {}};
  const escape = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let lang = get('agent-lang') === 'zh' ? 'zh' : 'en';
  let policy = 'allow';
  let activeDialogProject = null;
  let pendingSeek = null;
  const tr = key => window.SITE_CONTENT[lang][key] ?? key;
  const ext = (label,url) => `<a href="${escape(url)}" target="_blank" rel="noopener noreferrer">${escape(label)} <span aria-hidden="true">↗</span></a>`;
  const numbers = window.PAPER_RESULTS;
  const video = $('#research-film');
  const starts = [0,3,7.5,12];
  function stats(p) {
    if(p.id==='agenthazard') return `<div class="double-stat"><div><strong>${numbers.agenthazard.instances.toLocaleString('en')}</strong><span>${tr('agenthazardStat')}</span></div><div><strong>${numbers.agenthazard.risks} × ${numbers.agenthazard.attacks}</strong><span>${tr('agenthazardStat2')}</span></div></div>`;
    if(p.id==='vera') return `<div class="double-stat"><div><strong>${numbers.vera.cases.toLocaleString('en')}</strong><span>${tr('veraStat')}</span></div><div><strong>${numbers.vera.risks}</strong><span>${tr('veraStat2')}</span></div></div>`;
    const value = p.id==='braveguard' ? `${numbers.braveguard.baseline.toFixed(2)} <span>→</span> ${numbers.braveguard.trained.toFixed(2)}%` : p.id==='hazardauditor' ? `+${(numbers.hazardauditor.auditor[3]-numbers.hazardauditor.baseline[3]).toFixed(1)} <small>${lang==='zh'?'百分点':'pp'}</small>` : `${numbers.adaguard.accuracy.toFixed(2)}%`;
    return `<div class="single-stat"><strong>${value}</strong><span>${tr(p.id+'Stat')}</span></div>`;
  }
  function renderProjects() {
    for (const kind of ['foundation','guard']) {
      $(`#${kind}-projects`).innerHTML=window.PROJECTS.filter(p=>p.kind===kind).map(p=>`<article id="${p.id}" class="project ${kind}"><div class="project-top"><span class="tag">${tr(p.id+'Label')}</span><span>${p.number}</span></div><h3>${p.name}</h3><h4>${tr(p.id+'Tagline')}</h4><p>${tr(p.id+'Desc')}</p>${stats(p)}<button class="figure-button" data-figure="${p.id}" aria-label="${escape(tr('figureOpen')+' — '+p.name)}"><img src="assets/methods/${p.id}.${lang}.svg" alt="${escape(p.name+' — '+tr('figure'))}" loading="lazy" width="900" height="450"><span>${tr('figure')} <span aria-hidden="true">↗</span></span></button>${p.id==='adaguard'?`<p class="release-note">${tr('adaguardRelease')}</p>`:''}<div class="project-links">${ext(tr('paper'),p.paper)}${p.links.map(([key,url])=>ext(tr(key),url)).join('')}<a href="metrics.html#${p.id}">${tr('metrics')} ↗</a><button data-cite="${p.id}">${tr('citation')} <span aria-hidden="true">{ }</span></button></div></article>`).join('');
    }
    all('[data-figure]').forEach(b=>b.addEventListener('click',()=>openFigure(b.dataset.figure)));
    all('[data-cite]').forEach(b=>b.addEventListener('click',()=>openCitation(b.dataset.cite)));
  }
  function renderChart() {
    const r=numbers.hazardauditor;
    $('#result-chart').innerHTML=`<div class="chart-rows">${r.frameworks.map((name,i)=>`<div class="chart-row"><strong>${escape(name)}</strong><div class="bar-pair"><div class="bar baseline" style="--value:${r.baseline[i]}%"><span>${r.baseline[i].toFixed(2)}%</span></div><div class="bar auditor" style="--value:${r.auditor[i]}%"><span>${r.auditor[i].toFixed(2)}%</span></div></div></div>`).join('')}</div><div class="chart-axis"><span>0</span><span>25</span><span>50</span><span>75</span><span>100%</span></div>`;
    $('#table-container').innerHTML=`<table><caption>${tr('chartTitle')}</caption><thead><tr><th scope="col">${tr('framework')}</th><th scope="col">BraveGuard</th><th scope="col">HazardAuditor</th><th scope="col">${tr('gain')}</th></tr></thead><tbody>${r.frameworks.map((name,i)=>`<tr><th scope="row">${name}</th><td>${r.baseline[i].toFixed(2)}%</td><td>${r.auditor[i].toFixed(2)}%</td><td>+${(r.auditor[i]-r.baseline[i]).toFixed(1)}</td></tr>`).join('')}</tbody></table>`;
  }
  const resources=[
    ['ourResources',[
      ['AgentHazard · Hugging Face','https://huggingface.co/datasets/Yunhao-Feng/AgentHazard','dataset'],
      ['VERA-Bench','https://github.com/Yunhao-Feng/Vera/tree/main/evaluation_bench','dataset'],
      ['VERA · AgentImages','https://huggingface.co/datasets/Yunhao-Feng/AgentImages','environments'],
      ['BraveGuard · Hugging Face','https://huggingface.co/Yunhao-Feng/BraveGuard','models'],
      ['HazardAuditor · Hugging Face','https://huggingface.co/Yunhao-Feng/HazardAuditor','models'],
      ['AdaGuard · 0.6B','https://huggingface.co/Yunhao-Feng/AdaGuard-0.6B','models'],
      ['AdaGuard · 4B','https://huggingface.co/Yunhao-Feng/AdaGuard-4B','models'],
      ['AdaGuard · 8B','https://huggingface.co/Yunhao-Feng/AdaGuard-8B','models']]],
    ['benchmarks',[
      ['AgentDojo','https://github.com/ethz-spylab/agentdojo','repository'],
      ['Agent-SafetyBench','https://github.com/thu-coai/Agent-SafetyBench','repository'],
      ['SWE-bench','https://www.swebench.com/','project'],
      ['OWASP GenAI Security','https://owasp.org/projects/top-10-for-large-language-model-applications','project'],
      ['MITRE ATLAS','https://atlas.mitre.org/','project']]],
    ['building',[
      ['HazardArena','https://hazardarena-team.github.io/','project'],
      ['OpenHands','https://github.com/All-Hands-AI/OpenHands','repository'],
      ['SWE-agent','https://github.com/SWE-agent/SWE-agent','repository'],
      ['Hugging Face','https://huggingface.co/','project'],
      ['arXiv · Artificial Intelligence','https://arxiv.org/list/cs.AI/recent','paperArxiv']]]
  ];
  function renderResources(){
    $('#resource-grid').innerHTML=resources.map(([title,items])=>`<div><h3>${tr(title)} <span aria-hidden="true">↗</span></h3>${items.map(([name,url,label])=>`<a href="${escape(url)}" target="_blank" rel="noopener noreferrer"><span>${escape(name)}</span><small>${tr(label)} ↗</small></a>`).join('')}</div>`).join('');
  }
  function updatePolicy(){
    const denied=policy==='deny';
    all('[data-policy]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.policy===policy)));
    $('#policy-rule').textContent=tr(denied?'ruleB':'ruleA');
    $('#verdict').classList.toggle('denied',denied);
    $('.verdict-icon').textContent=denied?'!':'✓';
    $('#verdict-title').textContent=tr(denied?'unsafe':'safe');
    $('#verdict-desc').textContent=tr(denied?'unsafeReason':'safeReason');
  }
  function renderChapters(){
    $('#chapters').innerHTML=starts.map((start,i)=>`<button data-time="${start}"><time>${String(Math.floor(start/60)).padStart(2,'0')}:${String(Math.floor(start%60)).padStart(2,'0')}</time><span>${tr('chapters')[i]}</span><span class="chapter-arrow" aria-hidden="true">↗</span></button>`).join('');
    all('[data-time]').forEach(b=>b.addEventListener('click',()=>playFrom(Number(b.dataset.time))));
    updateChapter();
  }
  function playFrom(time){
    if(video.readyState>=1){video.currentTime=time;}else{pendingSeek=time;}
    video.play().catch(()=>video.focus());
  }
  video.addEventListener('loadedmetadata',()=>{if(pendingSeek!==null){video.currentTime=pendingSeek;pendingSeek=null;}});
  function updateChapter(){
    const current=starts.reduce((a,s,i)=>video.currentTime>=s?i:a,0);
    all('[data-time]').forEach((b,i)=>{b.classList.toggle('active',i===current);if(i===current)b.setAttribute('aria-current','true');else b.removeAttribute('aria-current');});
  }
  function translate(){
    document.documentElement.lang=lang==='zh'?'zh-CN':'en';
    document.title=tr('title');$('meta[name="description"]').content=tr('description');
    all('[data-i18n]').forEach(e=>e.textContent=tr(e.dataset.i18n));
    all('[data-i18n-aria]').forEach(e=>e.setAttribute('aria-label',tr(e.dataset.i18nAria)));
    $('nav').setAttribute('aria-label',lang==='zh'?'主导航':'Main navigation');
    $('.hero-map').setAttribute('aria-label',lang==='zh'?'AgentHazard 和 VERA 将风险量化与执行验证连接到三个互补的防护研究方向':'AgentHazard and VERA connect risk measurement and verification to three complementary guards');
    const mapLabels=lang==='zh'?['01 / 数据集','02 / 框架','03 / 威胁演化','04 / 决策优化','05 / 策略适应']:['01 / DATASET','02 / FRAMEWORK','03 / EVOLVE','04 / ALIGN','05 / ADAPT'];
    all('.map-node>span').forEach((e,i)=>e.textContent=mapLabels[i]);
    $('.data-node small').textContent=lang==='zh'?'量化风险':'Measure risk';$('.framework-node small').textContent=lang==='zh'?'验证行为':'Verify behavior';
    $('.evidence-node').textContent=lang==='zh'?'真实执行证据':'EXECUTION EVIDENCE';$('.map-caption').textContent=lang==='zh'?'量化 → 验证 → 学习':'MEASURE → VERIFY → LEARN';$('.map-label').textContent=lang==='zh'?'研究 / 01—05':'RESEARCH / 01—05';
    all('[data-lang]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.lang===lang)));
    renderProjects();renderChart();renderResources();renderChapters();updatePolicy();
    if(activeDialogProject){const p=window.PROJECTS.find(p=>p.id===activeDialogProject);$('#figure-title').textContent=p.name+' · '+tr('figure');$('#citation-title').textContent=p.name+' · '+tr('citeLabel');$('#dialog-figure').alt=p.name+' — '+tr('figure');$('#dialog-figure').src=`assets/methods/${p.id}.${lang}.svg`;}
  }
  function openFigure(id){const p=window.PROJECTS.find(p=>p.id===id);activeDialogProject=id;$('#figure-title').textContent=p.name+' · '+tr('figure');$('#dialog-figure').src=`assets/methods/${id}.${lang}.svg`;$('#dialog-figure').alt=p.name+' — '+tr('figure');$('#figure-source').href=p.paper;$('#figure-dialog').showModal();}
  function openCitation(id){const p=window.PROJECTS.find(p=>p.id===id);activeDialogProject=id;$('#citation-title').textContent=p.name+' · '+tr('citeLabel');$('#citation-text').textContent=p.bib;$('#copy-status').textContent='';$('#citation-dialog').showModal();}
  all('.close-dialog').forEach(b=>b.addEventListener('click',()=>b.closest('dialog').close()));
  all('dialog').forEach(d=>{d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}});d.addEventListener('close',()=>activeDialogProject=null);});
  $('#copy-citation').addEventListener('click',async()=>{try{await navigator.clipboard.writeText($('#citation-text').textContent);$('#copy-status').textContent=tr('copied');}catch{$('#copy-status').textContent=tr('copyFailed');}});
  all('[data-lang]').forEach(b=>b.addEventListener('click',()=>{lang=b.dataset.lang;save('agent-lang',lang);translate();}));
  all('[data-policy]').forEach(b=>b.addEventListener('click',()=>{policy=b.dataset.policy;updatePolicy();}));
  $('#theme-button').addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=theme;save('agent-theme',theme);updateTheme();});
  function updateTheme(){const dark=document.documentElement.dataset.theme==='dark';$('#theme-button').setAttribute('aria-pressed',String(dark));$('meta[name="theme-color"]').content=dark?'#0b0f1a':'#ffffff';}
  $('#watch-button').addEventListener('click',()=>{$('#film').scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});video.play().catch(()=>video.focus());});
  video.addEventListener('timeupdate',updateChapter);
  const motion=matchMedia('(prefers-reduced-motion: reduce)');
  function setMotion(){if(motion.matches)$('.map-lines').pauseAnimations();else $('.map-lines').unpauseAnimations();}
  motion.addEventListener('change',setMotion);
  translate();updateTheme();setMotion();
})();
