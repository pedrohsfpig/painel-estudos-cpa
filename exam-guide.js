/* Referência fornecida pelo usuário em 27/10/2026. Não alimenta o sorteio. */
const EXAM_GUIDE_REFERENCE=Object.freeze({
 recordedAt:'2026-10-27',source:'Quadro de prioridades fornecido pelo usuário',
 rows:Object.freeze([
  {rank:1,lesson:13,block:'F',topic:'Métricas Matemáticas, Gestão de Riscos e Clientes',importance:'maxima',detail:'40% da prova / 20 questões'},
  {rank:2,lesson:11,block:'D',topic:'Macroeconomia, Atividade e Política Fiscal',importance:'alta',detail:'20% da prova / 10 questões'},
  {rank:3,lesson:1,block:null,topic:'Sistema Financeiro Nacional',importance:'alta',detail:'Base conceitual obrigatória'},
  {rank:4,lesson:3,block:null,topic:'Banco Central do Brasil',importance:'media-alta',detail:'Autarquia mais cobrada'},
  {rank:5,lesson:4,block:null,topic:'Comissão de Valores Mobiliários',importance:'media-alta',detail:'Mercado de Capitais'},
  {rank:6,lesson:8,block:'A',topic:'Inovação, Pagamentos e Crédito Digital',importance:'media',detail:'~10% a 15% da prova'},
  {rank:7,lesson:9,block:'B',topic:'Autorregulação, Proteção e Livre Mercado',importance:'media',detail:'~10% a 15% da prova'},
  {rank:8,lesson:2,block:null,topic:'Conselho Monetário Nacional',importance:'media',detail:'Fixação de metas'},
  {rank:9,lesson:5,block:null,topic:'Seguros e Previdência (SUSEP/PREVIC)',importance:'media',detail:'Estrutura técnica'},
  {rank:10,lesson:6,block:null,topic:'Operadores Monetários',importance:'media',detail:'Bancos Múltiplos e Comerciais'},
  {rank:11,lesson:7,block:null,topic:'Operadores Não Monetários',importance:'media',detail:'Corretoras e Financeiras'},
  {rank:12,lesson:10,block:'C',topic:'Infraestrutura, Negociação e Risco Sistêmico',importance:'baixa',detail:'~5% da prova'},
  {rank:13,lesson:12,block:'E',topic:'Mercado de Câmbio e Relações Internacionais',importance:'baixa',detail:'~5% da prova'}
 ].map(Object.freeze))
});
const EXAM_GUIDE_LEVELS=Object.freeze({'maxima':'Máxima','alta':'Alta','media-alta':'Média-alta','media':'Média','baixa':'Baixa'});
const examGuideState={query:'',importance:'all',sort:'rank'};
function examGuideNormalize(value){return String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase()}
function examGuideAvailable(row){return !!AL[row.lesson-1]}
function examGuideRows(){
 const state=examGuideState,aliases={bacen:'banco central',bc:'banco central',cvm:'comissao de valores mobiliarios',cmn:'conselho monetario nacional',sfn:'sistema financeiro nacional'};
 const terms=examGuideNormalize(state.query).trim().split(/\s+/).filter(Boolean).flatMap(term=>(aliases[term]||term).split(' '));
 return EXAM_GUIDE_REFERENCE.rows.filter(row=>{
  const text=examGuideNormalize(`Aula ${row.lesson} ${String(row.lesson).padStart(2,'0')} ${row.topic} ${EXAM_GUIDE_LEVELS[row.importance]} ${row.detail} ${AL[row.lesson-1]?.t||''}`);
  return (state.importance==='all'||row.importance===state.importance)&&terms.every(term=>text.includes(term));
 }).sort((a,b)=>state.sort==='lesson'?a.lesson-b.lesson:a.rank-b.rank);
}
function examGuideFilterGroup(key,label,options){
 return `<div class="exam-filter-group" role="group" aria-label="${label}"><span>${label}</span><div class="chips">${options.map(([value,text])=>`<button type="button" class="chip${examGuideState[key]===value?' on':''}" data-exam-filter="${key}:${value}" aria-pressed="${examGuideState[key]===value}" onclick="setExamGuideFilter('${key}','${value}')">${text}</button>`).join('')}</div></div>`;
}
function setExamGuideFilter(key,value){
 const allowed={importance:['all',...Object.keys(EXAM_GUIDE_LEVELS)],sort:['rank','lesson']};
 if(!allowed[key]?.includes(value))return;
 examGuideState[key]=value;refreshExamGuide();document.querySelector(`[data-exam-filter="${key}:${value}"]`)?.focus({preventScroll:true});
}
function searchExamGuide(value){examGuideState.query=value;refreshExamGuide()}
function resetExamGuide(){Object.assign(examGuideState,{query:'',importance:'all',sort:'rank'});const input=document.getElementById('exam-guide-search');if(input)input.value='';refreshExamGuide();input?.focus({preventScroll:true})}
function examGuideResults(){
 const rows=examGuideRows();
 return `<div class="exam-results-heading"><p role="status">${rows.length} de ${EXAM_GUIDE_REFERENCE.rows.length} aulas</p>${examGuideFilterGroup('sort','Ordenar por',[['rank','Prioridade'],['lesson','Aula']])}</div>${rows.length?`<div class="exam-table-wrap"><table class="exam-table"><caption class="sr-only">Prioridades da prova CPA, conforme quadro fornecido pelo usuário. Posição original preservada ao filtrar ou ordenar.</caption><thead><tr><th scope="col">Posição</th><th scope="col">Aula</th><th scope="col">Foco temático</th><th scope="col">Importância na prova</th></tr></thead><tbody>${rows.map(row=>`<tr data-exam-lesson="${row.lesson}" class="exam-priority-${row.importance}"><td data-label="Posição"><span class="exam-rank${row.rank<=3?' is-top':''}">${row.rank}º</span></td><td data-label="Aula"><div class="exam-lesson"><strong>Aula ${String(row.lesson).padStart(2,'0')}</strong>${examGuideAvailable(row)?'':'<span class="exam-planned">Prevista · ainda não cadastrada</span>'}</div></td><th scope="row" data-label="Foco temático">${escapeText(row.topic)}</th><td data-label="Importância na prova"><span class="exam-importance"><i aria-hidden="true"></i>${EXAM_GUIDE_LEVELS[row.importance]}</span><span class="exam-detail">${escapeText(row.detail)}</span></td></tr>`).join('')}</tbody></table></div>`:'<div class="exam-empty">'+uiIcon('search')+'<h3>Nenhuma aula encontrada</h3><p>Tente outro termo ou limpe os filtros.</p><button type="button" onclick="resetExamGuide()">Limpar filtros e busca</button></div>'}`;
}
function examGuideFilters(){return examGuideFilterGroup('importance','Importância',[['all','Todas'],...Object.entries(EXAM_GUIDE_LEVELS)])}
function refreshExamGuide(){const filters=document.getElementById('exam-guide-filters'),results=document.getElementById('exam-guide-results');if(filters)filters.innerHTML=examGuideFilters();if(results)results.innerHTML=examGuideResults()}
function examGuidePage(){
 return `<div class="exam-guide-page"><section class="exam-reference" aria-labelledby="exam-reference-title"><div class="exam-reference-icon">${uiIcon('practice')}</div><div><span class="exam-eyebrow">SUA REFERÊNCIA DE ESTUDOS</span><h2 id="exam-reference-title">O que priorizar para a CPA</h2><p>As 13 aulas na ordem de relevância do teu quadro, com os pesos e os focos temáticos preservados.</p></div><span class="exam-reference-date">Registrado em 27/10/2026</span></section><section class="exam-guide-panel" aria-label="Tabela interativa de prioridades"><div class="exam-search-row"><div><label for="exam-guide-search">Buscar aula, tema ou conteúdo</label><div class="exam-search">${uiIcon('search')}<input id="exam-guide-search" type="search" placeholder="Ex.: Bacen, câmbio, riscos…" value="${escapeText(examGuideState.query)}" oninput="searchExamGuide(this.value)" onkeydown="if(event.key==='Escape'){this.value='';searchExamGuide('')}"></div></div><button type="button" class="exam-reset" onclick="resetExamGuide()">Limpar filtros</button></div><div id="exam-guide-filters" class="exam-filters">${examGuideFilters()}</div><div id="exam-guide-results">${examGuideResults()}</div></section><details class="exam-reference-notes"><summary>Sobre esta referência</summary><div><p>Fonte: quadro que tu forneceste em 27/10/2026. Esta é a referência de planejamento do sistema até tu informares uma atualização; não representa uma conferência independente de edital.</p><p>Pesos aproximados e descrições foram mantidos como recebidos. Não somamos percentuais de linhas nem inferimos pesos para aulas sem percentual.</p><p>A Aula 13 está prevista no quadro e será identificada como cadastrada quando seu conteúdo for incluído. Consultar, filtrar ou ordenar esta tabela não altera questões, dificuldades, sorteios, simulados ou histórico.</p></div></details></div>`;
}
