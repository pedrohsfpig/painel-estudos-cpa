/* Demonstração independente: sem imports do aplicativo, conta ou armazenamento local. */
(() => {
  'use strict';
  const {lessons, rows} = window.PREVIEW_CATALOG;
  const $ = s => document.querySelector(s);
  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const fold = s => String(s).normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const nf = n => n.toLocaleString('pt-BR');
  const paths = {
    home:'M3 10 12 3l9 7M5 9v12h5v-7h4v7h5V9',
    book:'M12 5v16M3 4c4-1 6-1 9 1 3-2 5-2 9-1v15c-4-1-6-1-9 2-3-3-5-3-9-2Z',
    search:'M21 21l-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
    practice:'M6 3h12v18H6zM9 7h6M9 11h6M9 15h3',
    warning:'m12 3 10 18H2ZM12 9v5M12 17h.01',
    file:'M5 3h9l5 5v13H5zM14 3v6h5M8 13h8M8 17h6',
    bank:'m2 8 10-5 10 5ZM4 21h16M6 11v7M12 11v7M18 11v7',
    chart:'M5 21V12M12 21V3M19 21V8',
    target:'M21 12a9 9 0 1 1-9-9M17 12a5 5 0 1 1-5-5M12 12l9-9M17 3h4v4',
    arrow:'M4 12h16m-6-6 6 6-6 6',
    chevron:'m9 5 7 7-7 7',
    check:'m5 12 4 4L19 6',
    cross:'m6 6 12 12M18 6 6 18',
    sun:'M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5 19 19M5 19l1.5-1.5M17.5 6.5 19 5M16 12a4 4 0 1 1-8 0 4 4 0 0 1 8 0',
    moon:'M20.6 14.3A9 9 0 0 1 9.7 3.4a9 9 0 1 0 10.9 10.9Z',
    menu:'M4 6h16M4 12h16M4 18h16',
    clock:'M12 7v5l3 2M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0',
    info:'M12 11v6M12 7h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0',
    help:'M9 8a3 3 0 1 1 4 3c-1 .5-1 1-1 3M12 17h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0',
    layers:'m12 3 10 5-10 5L2 8ZM2 12l10 5 10-5M2 16l10 5 10-5',
    link:'m10 13 4-4M8 16l-1 1a4 4 0 0 1-6-6l4-4a4 4 0 0 1 6 0M16 8l1-1a4 4 0 0 1 6 6l-4 4a4 4 0 0 1-6 0',
    shield:'M12 3 3 6v6c0 5 9 10 9 10s9-5 9-10V6ZM8 12l3 3 5-6'
  };
  const icon = name => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="${paths[name] || paths.book}"/></svg>`;
  const params = new URLSearchParams(location.search);
  const state = {
    page:params.get('p') === 'praticar' ? 'praticar' : 'painel',
    theme:params.get('t') === 'light' ? 'light' : 'dark',
    mode:'e', level:-1, history:'all', count:10, search:'',
    selected:new Set(lessons.map(l => l.id)), units:new Map(lessons.filter(l=>l.units.length).map(l=>[l.id,new Set(l.units.map(u=>u.id))])), expanded:new Set()
  };
  // Cenário fictício: 248 respostas, sendo 196 acertos e 52 erros.
  const mockHistory = new Map();
  const ordered = rows.filter(r=>!r[4]).sort((a,b)=>((a[0]*7919)%1451)-((b[0]*7919)%1451));
  ordered.slice(0,248).forEach((r,i)=>mockHistory.set(r[0],i<196));
  const modeInfo = {
    e:{title:'Estudo',icon:'book',description:'Ajudas disponíveis e explicações após cada resposta.',start:'Iniciar estudo'},
    s:{title:'Simulado',icon:'practice',description:'Sem ajudas. Confira o resultado e as explicações ao finalizar.',start:'Iniciar simulado'},
    h:{title:'Hardcore',icon:'target',description:'Questões de maior dificuldade, sem ajudas durante a sessão.',start:'Iniciar Hardcore'},
    b:{title:'Bate-pronto',icon:'link',description:'Conceitos diretos, duas alternativas e explicações após a resposta.',start:'Iniciar Bate-pronto'}
  };
  const pool = () => rows.filter(r =>
    state.selected.has(r[1]) && (!lessons[r[1]-1].units.length || state.units.get(r[1])?.has(r[2])) &&
    (state.mode==='b' ? r[4] : !r[4] && (state.mode==='h' ? r[3]===3 : r[3]<3 && (state.level<0 || r[3]===state.level))) &&
    (state.history==='all' || state.history==='new' && !mockHistory.has(r[0]) || state.history==='errors' && mockHistory.get(r[0])===false));
  function stock(lesson,unit=0){return rows.filter(r=>r[1]===lesson&&(!unit||r[2]===unit)&&(state.mode==='b'?r[4]:!r[4]&&(state.mode==='h'?r[3]===3:r[3]<3))).length}
  function fullLesson(id){const l=lessons[id-1];return state.selected.has(id)&&(!l.units.length||state.units.get(id)?.size===l.units.length)}
  const allSelected = () => lessons.every(l=>fullLesson(l.id));
  function setLesson(id,checked){
    if(checked){state.selected.add(id);state.units.set(id,new Set(lessons[id-1].units.map(u=>u.id)))}
    else state.selected.delete(id);
  }
  function applyTheme(){
    document.documentElement.dataset.theme=state.theme;
    document.querySelectorAll('.theme-control').forEach(b=>{
      b.innerHTML=icon(state.theme==='dark'?'sun':'moon');
      b.setAttribute('aria-label',`Ativar tema ${state.theme==='dark'?'claro':'escuro'}`);
    });
  }
  function renderNav(){
    const nav=[['painel','Painel','home'],['','Trilha','book'],['','Consulta','search'],['praticar','Praticar','practice'],['','Erros','warning'],['','Material de apoio','file'],['','Quadro do SFN','bank'],['','Estatísticas','chart'],['','Guia da prova','practice']];
    $('.main-nav').innerHTML=nav.map(([id,title,i],n)=>`${n===7?'<div class="nav-spacer" aria-hidden="true"></div>':''}<button class="nav-item ${id&&state.page===id?'on':''}" ${id?`data-page="${id}" ${state.page===id?'aria-current="page"':''}`:'disabled title="Esta prévia apresenta Painel e Praticar"'}>${icon(i)}<span class="nav-label">${title}</span>${n===4?'<span class="nav-counter">52</span>':''}</button>`).join('');
  }
  const arrowLink=(text,action,extra='')=>`<button class="link-button" data-action="${action}" ${extra}>${text}${icon('arrow')}</button>`;
  function chart(){
    const days=[['29/10',24,18],['30/10',32,26],['31/10',28,23],['01/11',40,30],['02/11',26,19],['03/11',34,29],['04/11',36,29],['05/11',28,22]];
    const point=(r,i)=>[44+i*65,122-Math.round(r[2]/r[1]*100)*.82];
    return `<div class="evolution-scroll" tabindex="0" aria-label="Evolução de acertos e quantidade de respostas; dados ilustrativos"><svg class="evolution-chart" viewBox="0 0 530 232" role="img" aria-labelledby="chart-title chart-description"><title id="chart-title">Aproveitamento e questões respondidas por dia</title><desc id="chart-description">Exemplo ilustrativo: ${days.map(r=>`${r[0]}: ${r[1]} respostas, ${r[2]} acertos, ${Math.round(r[2]/r[1]*100)} por cento`).join('; ')}.</desc>${[50,75,100].map(n=>`<line class="chart-grid" x1="29" x2="516" y1="${122-n*.82}" y2="${122-n*.82}"/><text class="chart-axis" x="0" y="${125-n*.82}">${n}%</text>`).join('')}<polyline class="chart-line" points="${days.map(point).map(p=>p.join(',')).join(' ')}"/>${days.map((r,i)=>{const [x,y]=point(r,i),pct=Math.round(r[2]/r[1]*100),bh=r[1]*.85;return `<g tabindex="0"><title>${r[0]}: ${pct}% de acerto; ${r[1]} questões respondidas</title><circle class="chart-point" cx="${x}" cy="${y}" r="3.3"/><text class="chart-value" text-anchor="middle" x="${x}" y="${y-13}">${pct}%</text><rect class="volume-bar" x="${x-13}" y="${195-bh}" width="26" height="${bh}"/><text class="chart-axis" text-anchor="middle" x="${x}" y="${188-bh}">${r[1]}</text><text class="chart-date" text-anchor="middle" x="${x}" y="216">${r[0]}</text></g>`}).join('')}<line x1="29" x2="516" y1="195" y2="195" stroke="var(--line)"/></svg></div>`;
  }
  function reviewItems(){
    const counts=new Map();rows.filter(r=>mockHistory.get(r[0])===false).forEach(r=>{const key=r[1]+'|'+r[5];counts.set(key,(counts.get(key)||0)+1)});
    return [...counts].sort((a,b)=>b[1]-a[1]).slice(0,3).map(([key,count])=>{const [l,...topic]=key.split('|'),name=topic.join('|').replace(/^[^:]+: /,'');return `<div class="review-item"><div class="review-top"><span>${esc(name)}</span><span class="review-count">${count} ${count===1?'erro':'erros'}</span></div><p>Aula ${String(l).padStart(2,'0')} · respostas do exemplo</p><div class="review-track" aria-hidden="true"><i style="width:${Math.min(100,count*23)}%"></i></div></div>`}).join('');
  }
  function learningRows(){
    return [1,3,13].map(id=>{
      const l=lessons[id-1],total=rows.filter(r=>r[1]===id&&!r[4]).length,done=rows.filter(r=>r[1]===id&&mockHistory.has(r[0])).length;
      return `<div class="learning-row"><span class="lesson-number">${String(id).padStart(2,'0')}</span><div><div class="learning-row-name">${esc(l.name)}</div><div class="learning-row-caption">${done} de ${total} questões praticadas</div></div><div class="learning-percent">${Math.round(done/total*100)}%<div class="mini-track" aria-hidden="true"><i style="width:${done/total*100}%"></i></div></div></div>`;
    }).join('');
  }
  function renderDashboard(){
    $('#page').innerHTML=`<div class="dashboard-page"><header class="page-header"><div><h1>Painel</h1><p>Quinta-feira, 5 de novembro</p></div><div class="header-search-wrap"><label class="input-box">${icon('search')}<input id="header-search" placeholder="Buscar uma aula" aria-label="Buscar uma aula" autocomplete="off" aria-controls="search-results" aria-expanded="false"><span class="search-hint" aria-hidden="true">/</span></label><div id="search-results" class="search-popover" hidden></div></div></header>
    <section class="daily" aria-labelledby="daily-title"><div><div class="daily-title-row">${icon('book')}<h2 id="daily-title">Estudo de hoje</h2></div><p class="daily-sub">20 questões para manter o estudo em dia.</p><div class="daily-details"><span><strong>5</strong> fáceis · <strong>10</strong> médias · <strong>5</strong> difíceis</span><span class="detail-rule" aria-hidden="true"></span><span><strong>3 dias</strong> de constância</span><span class="day-dots" aria-hidden="true">${Array.from({length:7},(_,i)=>`<i class="${i<3?'filled':''}"></i>`).join('')}</span></div></div><div class="daily-button-zone"><button class="primary" data-action="daily">Começar estudo${icon('arrow')}</button><small>Um checkpoint por dia</small></div></section>
    <section class="metrics" aria-label="Acompanhamento ilustrativo"><div class="metric"><span class="metric-label">${icon('practice')}Respondidas</span><strong>248</strong><small>No histórico completo</small></div><div class="metric"><span class="metric-label">${icon('check')}Acertos</span><strong>196</strong><small>Respostas corretas</small></div><div class="metric"><span class="metric-label">${icon('cross')}Erros</span><strong>52</strong><small class="pending">Para orientar a revisão</small></div><div class="metric"><span class="metric-label">${icon('chart')}Aproveitamento</span><strong>79<span style="font-size:20px">%</span></strong><small class="positive">196 de 248 respostas</small></div></section>
    <div class="dashboard-grid"><div class="dashboard-main"><section class="chart-section"><div class="section-head"><div><h2>Evolução do estudo</h2><p>Acertos e volume de questões, juntos.</p></div>${arrowLink('Ver histórico','history')}</div><div class="chart-legend"><span><i class="legend-dot"></i>Acertos (%)</span><span><i class="legend-bar"></i>Questões respondidas</span></div>${chart()}<p class="chart-note">Todos os dias do histórico ilustrativo · horário de Brasília</p></section>
    <section class="learning-section"><div class="section-head"><h2>Andamento das aulas</h2>${arrowLink('Ver todas','all-lessons')}</div>${learningRows()}<p class="chart-note">Andamento mede questões únicas praticadas.</p></section></div>
    <div class="dashboard-aside"><section class="aside-panel"><div class="section-head"><h2>Para revisar</h2>${icon('warning')}</div>${reviewItems()}${arrowLink('Abrir revisão','review')}<div class="continue-panel"><span class="eyebrow">Último conteúdo aberto</span><h3>Classificação de Investidores</h3><p>Aula 13 · Bloco Final · Aula interna 5</p>${arrowLink('Praticar este conteúdo','continue')}</div></section></div></div><footer class="page-foot"><span>Seu espaço para aprender, praticar e revisar.</span><span>Prévia independente · sem alterar seu progresso</span></footer></div>`;
  }
  function listMarkup(){
    const query=fold(state.search),visible=lessons.filter(l=>fold(l.name+' aula '+l.id+' '+l.units.map(u=>u.name).join(' ')).includes(query));
    if(!visible.length)return '<p class="no-lessons">Nenhuma aula encontrada. Tente outro termo.</p>';
    return visible.map(l=>{
      const full=fullLesson(l.id),partial=state.selected.has(l.id)&&!full,open=state.expanded.has(l.id);
      return `<div class="lesson-row ${state.selected.has(l.id)?'selected':''}"><input class="check lesson-check" type="checkbox" data-lesson="${l.id}" id="lesson-${l.id}" ${full?'checked':''} ${partial?'data-partial="true"':''} aria-label="Selecionar aula ${l.id}: ${esc(l.name)}"><span class="lesson-number">${String(l.id).padStart(2,'0')}</span><button class="lesson-select" data-lesson-toggle="${l.id}" data-focus="lesson-title-${l.id}" aria-label="Selecionar aula ${l.id}: ${esc(l.name)}">${esc(l.name)}</button><span class="lesson-stock">${stock(l.id)} questões</span>${l.units.length?`<button class="expand-lesson" data-expand="${l.id}" data-focus="expand-${l.id}" aria-expanded="${open}" aria-controls="units-${l.id}" aria-label="${open?'Recolher':'Mostrar'} conteúdos da aula ${l.id}">${icon('chevron')}</button>`:'<span></span>'}</div>${l.units.length?`<div class="unit-options" id="units-${l.id}" ${!open?'hidden':''}>${l.units.map(u=>`<label class="unit-row"><input class="check" type="checkbox" data-unit="${u.id}" data-unit-lesson="${l.id}" id="unit-${l.id}-${u.id}" ${state.selected.has(l.id)&&state.units.get(l.id)?.has(u.id)?'checked':''}><span>${esc(u.name)}</span><small>${stock(l.id,u.id)}</small></label>`).join('')}</div>`:''}`;
    }).join('');
  }
  function distributionMarkup(){
    const p=pool(),selected=lessons.filter(l=>state.selected.has(l.id));
    return `<details class="distribution"><summary>Ver conteúdo selecionado</summary><div class="distribution-rows">${selected.length?selected.map(l=>`<div class="distribution-row"><span>${String(l.id).padStart(2,'0')} · ${esc(l.name)}</span><span>${p.filter(r=>r[1]===l.id).length}</span></div>`).join(''):'<span class="muted">Selecione uma aula para começar.</span>'}</div></details>`;
  }
  function sessionMarkup(){
    const p=pool(),canStart=state.count>0&&Number.isInteger(state.count)&&state.count<=p.length,info=modeInfo[state.mode];
    return `<section class="session-panel" aria-label="Configurar sessão"><span class="eyebrow">Configuração</span><h2>Sua sessão</h2><div class="settings-wrap"><div class="settings-group"><h3>Dificuldade${icon('help')}</h3><div class="level-buttons" role="group" aria-label="Dificuldade">${state.mode==='h'?'<span class="level-choice is-fixed"><i class="level-dot level-3"></i>Hardcore</span>':state.mode==='b'?'<span class="level-choice is-fixed">Conceitual</span>':[[-1,'Todas'],[0,'Fácil'],[1,'Médio'],[2,'Difícil']].map(([id,name])=>`<button class="level-choice" data-level="${id}" data-focus="level-${id}" aria-pressed="${state.level===id}">${id>=0?`<i class="level-dot level-${id}"></i>`:''}${name}</button>`).join('')}</div>${state.mode==='b'?'<p>Questões diretas, sem divisão por dificuldade.</p>':''}</div>
    <div class="settings-group"><h3>Histórico</h3><div class="history-buttons" role="group" aria-label="Histórico das questões">${[['all','Todas as questões'],['new','Nunca respondidas'],['errors','As que errei']].map(([id,name])=>`<button class="history-choice" data-history="${id}" data-focus="history-${id}" aria-pressed="${state.history===id}"><span class="radio-indicator" aria-hidden="true"></span>${name}</button>`).join('')}</div></div>
    <div class="settings-group"><h3>Quantidade</h3><div class="quantity-buttons" role="group" aria-label="Quantidade de questões">${[5,10,15,20,30].map(n=>`<button class="quantity-choice" data-count="${n}" data-focus="count-${n}" aria-pressed="${state.count===n}" ${n>p.length?'disabled':''}>${n}</button>`).join('')}</div>${state.mode==='b'?'<label class="input-box" style="margin-top:10px"><input type="number" id="custom-count" min="1" max="'+p.length+'" placeholder="Outra quantidade" aria-label="Quantidade personalizada de Bate-pronto"></label>':''}<p>${nf(p.length)} disponíveis com esses filtros.</p></div>
    </div><div class="session-plan"><div class="session-total"><strong id="count-display">${nf(state.count)}</strong><span>questões</span></div><div class="session-plan-line"><span>Modo</span><strong>${info.title}</strong></div><div class="session-plan-line"><span>Conteúdo</span><strong>${allSelected()?'Todas as aulas':state.selected.size+' '+(state.selected.size===1?'aula selecionada':'aulas selecionadas')}</strong></div></div><button class="primary" id="start-session" data-action="start" ${canStart?'':'disabled'}>${info.start}${icon('arrow')}</button><p class="session-foot">${canStart?'Estude no seu ritmo.':'Amplie a seleção ou ajuste a quantidade.'}</p>${distributionMarkup()}</section><p class="study-quote">${icon('shield')}A prévia não inicia uma sessão real nem grava respostas.</p>`;
  }
  function renderPractice(){
    const focused=document.activeElement,focusId=focused?.id,focusKey=focused?.dataset?.focus,listScroll=$('.lessons-list')?.scrollTop||0,info=modeInfo[state.mode],selected=state.selected.size;
    $('#page').innerHTML=`<div class="practice-page"><header class="page-header practice-header"><div><h1>Praticar</h1><p>Escolha o conteúdo e prepare sua sessão.</p></div><div class="practice-header-aside"><strong>13 aulas disponíveis</strong>Uma aula, várias ou o bloco completo.</div></header><div class="mode-tabs" role="tablist" aria-label="Modo de prática">${Object.entries(modeInfo).map(([id,m])=>`<button class="mode-tab" role="tab" aria-selected="${state.mode===id}" tabindex="${state.mode===id?'0':'-1'}" data-mode="${id}" data-focus="mode-${id}" aria-controls="practice-content">${icon(m.icon)}${m.title}</button>`).join('')}</div><p class="mode-description">${icon('info')}${info.description}</p><div class="practice-grid" id="practice-content"><section class="practice-content" aria-labelledby="content-title"><div class="content-header"><h2 id="content-title">Aulas e conteúdos</h2><span class="selection-label">${allSelected()?'Todas selecionadas':selected+' '+(selected===1?'selecionada':'selecionadas')}</span></div><label class="input-box lessons-search">${icon('search')}<input id="lesson-search" type="search" value="${esc(state.search)}" placeholder="Buscar por aula ou assunto" aria-label="Buscar por aula ou assunto" autocomplete="off"></label><label class="all-lessons-row"><input class="check" type="checkbox" id="select-all" ${allSelected()?'checked':''}><strong>Todas as aulas</strong><span class="muted">Banco completo</span></label><div class="lessons-list" aria-label="Aulas disponíveis">${listMarkup()}</div><div class="list-foot"><span>13 aulas · banco original de conteúdos</span><button class="link-button" data-action="clear-selection">Limpar seleção</button></div></section><div class="session-side">${sessionMarkup()}</div></div><footer class="page-foot"><span>Seu conteúdo, organizado para praticar.</span><span>Prévia independente · dados ilustrativos</span></footer></div>`;
    $('.lessons-list').scrollTop=listScroll;
    document.querySelectorAll('[data-partial]').forEach(n=>n.indeterminate=true);
    $('#select-all').indeterminate=selected>0&&!allSelected();
    if(focusId)document.getElementById(focusId)?.focus({preventScroll:true});
    else if(focusKey)document.querySelector(`[data-focus="${CSS.escape(focusKey)}"]`)?.focus({preventScroll:true});
  }
  function render(){
    renderNav();applyTheme();state.page==='painel'?renderDashboard():renderPractice();
    document.title=`${state.page==='painel'?'Painel':'Praticar'} · Prévia CPA Estudos`;
    history.replaceState(null,'',`?p=${state.page}&t=${state.theme}`);
  }
  function go(page){state.page=page;$('.sidebar').classList.remove('open');$('.drawer-shade').hidden=true;$('.menu-control').setAttribute('aria-expanded','false');render();window.scrollTo(0,0)}
  function openDialog(title,summary){
    $('#dialog-title').textContent=title;$('#session-summary').innerHTML=summary;$('#session-dialog').showModal();
  }
  function selectOnly(id,unit=null){
    state.selected.clear();setLesson(id,true);
    if(unit){state.units.set(id,new Set([unit]));state.expanded.add(id)}
    state.mode='e';state.level=-1;state.history='all';state.search='';go('praticar');
  }
  function toast(message){const el=$('.toast');el.textContent=message;el.classList.add('on');clearTimeout(toast.timer);toast.timer=setTimeout(()=>el.classList.remove('on'),3500)}
  document.addEventListener('click',e=>{
    const b=e.target.closest('button');if(!b)return;
    if(b.classList.contains('theme-control')){state.theme=state.theme==='dark'?'light':'dark';applyTheme();history.replaceState(null,'',`?p=${state.page}&t=${state.theme}`);return}
    if(b.classList.contains('menu-control')){const open=$('.sidebar').classList.toggle('open');$('.drawer-shade').hidden=!open;b.setAttribute('aria-expanded',String(open));return}
    if(b.classList.contains('close-dialog')){$('#session-dialog').close();return}
    if(b.dataset.page){go(b.dataset.page);return}
    if(b.dataset.mode){state.mode=b.dataset.mode;state.level=-1;renderPractice();return}
    if(b.dataset.level!==undefined){state.level=Number(b.dataset.level);renderPractice();return}
    if(b.dataset.history){state.history=b.dataset.history;renderPractice();return}
    if(b.dataset.count){state.count=Number(b.dataset.count);renderPractice();return}
    if(b.dataset.lessonToggle){const id=Number(b.dataset.lessonToggle);setLesson(id,!fullLesson(id));renderPractice();return}
    if(b.dataset.expand){const id=Number(b.dataset.expand);state.expanded.has(id)?state.expanded.delete(id):state.expanded.add(id);renderPractice();return}
    if(b.dataset.searchLesson){selectOnly(Number(b.dataset.searchLesson));return}
    const action=b.dataset.action;
    if(action==='daily')openDialog('Seu estudo de hoje.', '<strong>20 questões</strong><br>5 fáceis · 10 médias · 5 difíceis<br>Conteúdo de todas as aulas.');
    if(action==='all-lessons'){state.selected=new Set(lessons.map(l=>l.id));lessons.forEach(l=>state.units.set(l.id,new Set(l.units.map(u=>u.id))));state.history='all';state.search='';go('praticar')}
    if(action==='continue')selectOnly(13,5);
    if(action==='review'){state.history='errors';state.mode='e';state.level=-1;go('praticar')}
    if(action==='history'){toast('O gráfico apresenta os oito dias completos do exemplo.');$('.evolution-scroll').focus()}
    if(action==='clear-selection'){state.selected.clear();renderPractice()}
    if(action==='start'&&state.count>0&&state.count<=pool().length)openDialog('Sua sessão está preparada.',`<strong>${nf(state.count)} questões · ${modeInfo[state.mode].title}</strong><br>${allSelected()?'Todas as aulas':state.selected.size+' aula(s) selecionada(s)'}<br>${nf(pool().length)} questões disponíveis nos filtros escolhidos.`);
  });
  document.addEventListener('change',e=>{
    const n=e.target;
    if(n.id==='select-all'){const checked=n.checked;lessons.forEach(l=>setLesson(l.id,checked));renderPractice()}
    if(n.dataset.lesson){const id=Number(n.dataset.lesson);setLesson(id,!fullLesson(id));renderPractice()}
    if(n.dataset.unit){
      const id=Number(n.dataset.unitLesson),unit=Number(n.dataset.unit),set=state.units.get(id)||new Set();
      n.checked?set.add(unit):set.delete(unit);state.units.set(id,set);
      set.size?state.selected.add(id):state.selected.delete(id);renderPractice();
    }
    if(n.id==='custom-count'){const value=Number(n.value);if(Number.isInteger(value)&&value>0){state.count=value;renderPractice()}}
  });
  document.addEventListener('input',e=>{
    if(e.target.id==='lesson-search'){state.search=e.target.value;$('.lessons-list').innerHTML=listMarkup();document.querySelectorAll('[data-partial]').forEach(n=>n.indeterminate=true)}
    if(e.target.id==='header-search'){
      const q=fold(e.target.value).trim(),out=$('#search-results');out.hidden=!q;e.target.setAttribute('aria-expanded',String(!!q));
      if(q){const hits=lessons.filter(l=>fold(l.name+' '+l.id).includes(q)).slice(0,5);out.innerHTML=hits.length?hits.map(l=>`<button data-search-lesson="${l.id}"><span class="muted">${String(l.id).padStart(2,'0')} · </span>${esc(l.name)}</button>`).join(''):'<p>Nenhuma aula encontrada.</p>'}
    }
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape'){$('.sidebar').classList.remove('open');$('.drawer-shade').hidden=true;$('.menu-control').setAttribute('aria-expanded','false');if($('#search-results')){$('#search-results').hidden=true;$('#header-search').setAttribute('aria-expanded','false')}}
    if(e.key==='/'&&!/INPUT|TEXTAREA/.test(document.activeElement.tagName)&&!$('#session-dialog').open){const target=$('#header-search')||$('#lesson-search');if(target){e.preventDefault();target.focus()}}
    if(e.key==='Enter'&&e.target.id==='header-search'){$('#search-results button')?.click()}
    if(e.target.dataset.mode&&['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){
      e.preventDefault();const keys=Object.keys(modeInfo),at=keys.indexOf(state.mode),next=e.key==='Home'?0:e.key==='End'?3:(at+(e.key==='ArrowRight'?1:3))%4;state.mode=keys[next];state.level=-1;renderPractice();document.querySelector(`[data-mode="${state.mode}"]`).focus();
    }
  });
  $('.drawer-shade').addEventListener('click',()=>{$('.sidebar').classList.remove('open');$('.drawer-shade').hidden=true;$('.menu-control').setAttribute('aria-expanded','false');$('.menu-control').focus()});
  $('#session-dialog').addEventListener('click',e=>{if(e.target===e.currentTarget){const r=e.currentTarget.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.currentTarget.close()}});
  $('.menu-control').innerHTML=icon('menu');document.querySelectorAll('.close-dialog.icon-button').forEach(b=>b.innerHTML=icon('cross'));
  render();
})();
