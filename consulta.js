/* Consulta local e extrativa. Nenhuma chamada a modelos, APIs ou fontes externas. */
window.Consulta=(()=>{
 'use strict';
 const state={draft:'',entries:[],context:[]};
 let cache=null;
 const stop=new Set('a o as os de da do das dos e em no na nos nas para por um uma uns umas ao aos a ao com que qual quais quanto quantos quanta quantas quem como onde quando porque porque me mim meu minha seus suas seu sua voce voces tu eu nos gostaria quero queria saber diga diz explique explicar favor hoje atualmente agora orgao responsavel informacao informacoes sobre respeito referente refere relacao existe existem ter tem sao ser esta esse essa esses essas isto isso aquilo pode podem poderia poderia mostre mostrar traga trazer preciso entender entre versus vs x'.split(' '));
 const fold=value=>String(value??'').replace(/\{\{(?:atencao|negacao)\|([^{}]+)\}\}/g,'$1').replace(/\*\*/g,'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('pt-BR').replace(/[^a-z0-9]+/g,' ').trim();
 const plain=value=>searchPlain(String(value??''));
 function stem(word){
  const irregular={papeis:'papel',reais:'real',fiscais:'fiscal',capitais:'capital',membros:'membro',diretores:'diretor',valores:'valor',maiores:'maior',menores:'menor',funcoes:'funcao',compoem:'compor',composto:'composicao',composta:'composicao'};
  if(irregular[word])return irregular[word];
  if(word.length<5)return word;
  if(/coes$/.test(word))return word.slice(0,-4)+'cao';
  if(/oes$/.test(word))return word.slice(0,-3)+'ao';
  if(/ais$/.test(word))return word.slice(0,-3)+'al';
  if(/ores$/.test(word))return word.slice(0,-4)+'or';
  if(/s$/.test(word)&&!/[sx]s$/.test(word))return word.slice(0,-1);
  return word;
 }
 const synonymGroups=[['funcao','atribuicao','competencia','papel','responsabilidade','faz','fazer','atuacao','atua','atuam','serve','servem'],['objetivo','finalidade','proposito'],['composicao','membro','integrante','colegiado','compor'],['mandato','reconducao'],['limite','teto','cobertura'],['captacao','captar'],['emissao','emitir','emite'],['impressao','imprimir','imprime'],['regulacao','regular','regula','regulamentacao','regulamenta'],['autorizacao','autoriza','autorizar'],['garantia','garante','garantido','coberto'],['credito','emprestimo','financiamento'],['conceder','concede','concedem'],['definicao','conceito','significado','significa'],['diferenca','diferenciar','comparacao','comparar','distincao'],['fiscalizacao','fiscaliza','supervisao','supervisiona'],['remuneracao','rendimento','rentabilidade']];
 const synonyms=new Map(synonymGroups.flatMap(group=>group.map(word=>[word,group[0]])));
 const words=value=>fold(value).split(/\s+/).filter(word=>word&&!stop.has(word)).map(stem);
 const terms=value=>[...new Set(words(value).map(word=>synonyms.get(word)||word))];
 const FACETS=[
  {id:'composition',label:'Composição e liderança',pattern:/composicao|membro|integrante|colegiad|diretoria|presiden|superintendente|quem compoe|quem preside/},
  {id:'scope',label:'Área e público',pattern:/^area$|segmento|publico|^foco$|ambito|abrangencia/},
  {id:'role',label:'Função e atuação',pattern:/funcao|funcoes|atribuic|competencia|papel|papeis|finalidade|objetivo|atuacao|o que .*faz|o que faz|para que serve|responsab|fiscaliz|supervi/},
  {id:'nature',label:'Natureza e vinculação',pattern:/natureza|autarquia|vincul|subordin|minister|sede|onde fica|personalidade|forma juridica/},
  {id:'mandate',label:'Mandato',pattern:/mandato|reconduc|exonera|requisito/},
  {id:'appointment',label:'Nomeação e indicação',pattern:/nomea|nomei|indicac|quem indica|caminho do diretor|caminho/},
  {id:'resources',label:'Recursos e remuneração',pattern:/recurso|remuner|captac|capta|rendimento|funding|^fonte|deposito/},
  {id:'limits',label:'Limites e condições',pattern:/limite|teto|condic|prazo|cobertura|garantia|permit|proibi|vedad|quanto custa/},
  {id:'rules',label:'Regras e funcionamento',pattern:/reuniao|reunioes|quorum|decisao|votacao|periodic|funcionamento|liquidac|operac|fluxo|conta|registro/},
  {id:'definition',label:'Conceito',pattern:/definic|conceito|signific|o que e/}
 ];
 function facetOf(label,text=''){
  const f=fold(label);if(/^(macete|observac|dica|pegadinha)/.test(f))return [];
  const matches=FACETS.filter(item=>item.pattern.test(f)).map(item=>item.id);
  if(matches.includes('mandate'))return ['mandate'];
  if(matches.includes('appointment'))return ['appointment'];
  if(/quorum|reuniao|reunioes|presenca/.test(f))return ['rules'];
  if(matches.length)return matches;
  return /quatro papeis|competencia|finalidade|atribuicao|funcao/.test(fold(text))?['role']:[];
 }
 function index(){
  const stamp=[AL.length,Q.length,BP.length,Object.keys(MAT).length].join(':');
  if(cache?.stamp===stamp)return cache;
  const entities=[],aliasOwners=new Map(),records=[],tables=[];
  function entity(name,aliases=[]){
   const names=[name,...aliases].filter(Boolean),existing=names.map(n=>aliasOwners.get(words(n).join(' '))).find(Boolean);
   const result=existing||{id:'entity-'+entities.length,name,aliases:[],sequences:[]};
   if(!existing)entities.push(result);
   names.forEach(n=>{const sequence=words(n),key=sequence.join(' ');if(!key||result.aliases.includes(n))return;result.aliases.push(n);result.sequences.push(sequence);if(!aliasOwners.has(key))aliasOwners.set(key,result)});
   return result;
  }
  QUESTION_ACRONYMS.forEach(entry=>entity(entry.name,[...entry.aliases,...entry.variants,...entry.aliases.filter(a=>/^[A-Z]{2,}$/.test(a)).map(a=>a+'s')]));
  const extras={bc:['bacem','bacin','bacém'],susep:['suzep'],anbima:['ambima'],fgcoop:['fgcop','fgc coop']};
  QUESTION_ACRONYMS.forEach(entry=>{if(extras[entry.id])entity(entry.name,extras[entry.id])});
  Object.values(LESSON_OVERVIEWS).forEach(overview=>overview.rows.forEach(row=>entity(row.name,[row.short,...(row.short||'').split(/\s*·\s*/)].filter(Boolean))));
  // Apelidos de operadores vêm dos títulos cadastrados, não acrescentam fatos.
  const operatorAliases=[['Banco comercial',['bancos comerciais']],['Banco múltiplo',['bancos múltiplos']],['Banco de investimento',['bancos de investimentos']],['Banco de desenvolvimento',['bancos de desenvolvimento']],['Cooperativa de crédito',['cooperativas de crédito']],['Instituição de pagamento',['instituições de pagamentos','instituição de pagamentos']],['Corretora de Títulos e Valores Mobiliários',['corretora','corretoras']],['Distribuidora de Títulos e Valores Mobiliários',['distribuidora','distribuidoras']],['Entidade Aberta de Previdência Complementar',['previdência aberta']],['Entidade Fechada de Previdência Complementar',['previdência fechada','fundos de pensão']]];
  operatorAliases.forEach(([name,aliases])=>entity(name,aliases));
  const genericLabels=/^(natureza|diretoria|composicao|objetivo|competencia|atribuicao|funcao|papel|papeis|recurso|requisito|caminho|mandato|exoneracao|autorizacao|penalidade|poder|macete|dica|pegadinha|numero|atencao|cuidados|regra|reuniao|observac|exemplo|comparac)/;
  Object.values(MAT).forEach(M=>(M.mm?.[1]||[]).forEach(branch=>{const label=branch[0];if(typeof label!=='string'||genericLabels.test(fold(label))||FACETS.some(f=>f.pattern.test(fold(label)))||words(label).length>5||(words(label).length===1&&!/^(inflacao|compulsorio|redesconto|deflacao|poupanca|liquidez)$/.test(stem(fold(label)))))return;const key=words(label).join(' ');if(!aliasOwners.has(key))entity(label).topic=true}));
  [['Inflação',[]],['Taxa Selic',['meta Selic']]].forEach(([name,aliases])=>entity(name,aliases).topic=true);
  const sequenceAt=(hay,needle,at)=>needle.every((word,i)=>hay[at+i]===word);
  function detect(text){
   const input=words(text),matches=[];
   entities.forEach(e=>e.sequences.forEach(sequence=>{for(let at=0;at<=input.length-sequence.length;at++)if(sequenceAt(input,sequence,at))matches.push({e,at,length:sequence.length})}));
   const occupied=new Set(),found=[];
   matches.sort((a,b)=>b.length-a.length||a.at-b.at).forEach(match=>{if(Array.from({length:match.length},(_,i)=>match.at+i).some(i=>occupied.has(i)))return;for(let i=0;i<match.length;i++)occupied.add(match.at+i);if(!found.some(item=>item.e.id===match.e.id))found.push(match)});
   return found.sort((a,b)=>a.at-b.at).map(item=>item.e);
  }
  function ownerFor(label,fallback=[]){const found=detect(label);return found.length===1?(found[0].topic?[...new Set([...fallback,found[0].id])]:found.map(e=>e.id)):found.length>1?[]:fallback}
  function add({lesson,type,title,label=title,lines,owners=[],base=10,facets=null,table=null}){
   lines=lines.flat(Infinity).filter(value=>typeof value==='string'&&value.trim()).map(plain);if(!lines.length)return;
   const text=lines.join(' · '),record={id:records.length,lesson,type,title:plain(title),label:plain(label),lines,owners,base,facets:facets||facetOf(label,text),table};
   record.terms=terms([title,label,text].join(' '));record.labelTerms=terms(label);record.mentions=detect([label,text].join(' ')).map(e=>e.id);
   records.push(record);
  }
  AL.forEach((lesson,i)=>{
   const n=i+1,M=MAT[n],defaultOwners=ownerFor(M?.mm?.[0]||lesson.t);
   [['r','Resumo'],['d','Dicas e macetes'],['p','Pegadinhas']].forEach(([key,type])=>(lesson[key]||[]).forEach((text,at)=>{
    const prefix=plain(text).split(':')[0];add({lesson:n,type,title:type+' · '+lesson.t,label:prefix,lines:[text],owners:ownerFor(prefix,defaultOwners),base:key==='r'?22:8});
   }));
   (lesson.n||[]).forEach(([value,label])=>add({lesson:n,type:'Números para decorar',title:label,label,lines:[`${value} — ${label}`],owners:ownerFor(label,defaultOwners),base:20}));
   if(M){
    const walk=(branches,path,owners,inherited=[])=>branches.forEach(branch=>{
     if(!Array.isArray(branch))return;
     const [label,items]=branch;if(!Array.isArray(items))return;
     const own=ownerFor(label,owners),direct=items.filter(item=>typeof item==='string');
     add({lesson:n,type:'Mapa mental',title:[...path,label].join(' · '),label,lines:direct,owners:own,base:25,facets:facetOf(label).length?facetOf(label):inherited});
     walk(items.filter(Array.isArray),[...path,label],own,facetOf(label).length?facetOf(label):inherited);
    });
    walk(M.mm?.[1]||[],[],defaultOwners);
    (M.tb||[]).forEach(([title,headers,rows])=>{
     const table={id:tables.length,lesson:n,title,headers,rows};tables.push(table);
     const columnOwners=headers.slice(1).map(h=>detect(h));
     const compared=columnOwners.length>=2&&columnOwners.every(found=>found.length===1);
     rows.forEach(row=>{
      if(compared)row.slice(1).forEach((cell,j)=>add({lesson:n,type:'Tabela',title:title+' · '+row[0],label:row[0],lines:[String(cell)],owners:[columnOwners[j][0].id],base:30,table:table.id}));
      else {
       const rowEntities=detect(String(row[0])),own=rowEntities.length===1?rowEntities.map(e=>e.id):ownerFor(title,defaultOwners);
       const lines=row.slice(1).map((cell,j)=>headers.length>2?`${headers[j+1]}: ${cell}`:String(cell));
       add({lesson:n,type:'Tabela',title:title+' · '+row[0],label:row[0],lines,owners:own,base:25,facets:facetOf(row[0],title+' '+lines.join(' ')),table:table.id});
      }
     });
    });
    (M.dg||[]).forEach((diagram)=>diagram[2].forEach(node=>add({lesson:n,type:'Diagrama',title:diagram[1],label:node[0],lines:node.slice(0,2).filter(v=>typeof v==='string'),owners:ownerFor(diagram[1],defaultOwners),base:16})));
    (M.tl||[]).forEach(([title,items])=>items.forEach(item=>add({lesson:n,type:'Linha do tempo',title,label:item[0],lines:searchStrings(item),owners:ownerFor(title,defaultOwners),base:18,facets:facetOf(title,searchStrings(item).join(' '))})));
    (M.fc||[]).forEach(([question,answer])=>add({lesson:n,type:'Flashcard',title:question,label:question,lines:[answer],owners:ownerFor(question,defaultOwners),base:26}));
   }
   const overview=LESSON_OVERVIEWS[n];
   if(overview)overview.rows.forEach(row=>{
    const own=ownerFor(row.name),mapping={scope:'scope',powers:'role',focus:'scope',activity:'role',role:'role',leadership:'composition',affiliation:'nature',resources:'resources',limits:'limits',rules:'rules',account:'rules',flows:'rules',base:'definition'};
    add({lesson:n,type:'Quadro comparativo',title:row.name,label:'Natureza',lines:[row.kind,row.form].filter(Boolean),owners:own,base:30,facets:['nature']});
    overview.columns.slice(1).forEach(([key,label])=>add({lesson:n,type:'Quadro comparativo',title:row.name+' · '+label,label,lines:searchStrings(row[key]),owners:own,base:32,facets:mapping[key]?[mapping[key]]:facetOf(label)}));
   });
  });
  Q.forEach((q,i)=>add({lesson:q[0],type:'Explicação de questão',title:q[1]+' · questão '+(i+1),label:q[1],lines:[q[11]?.[0]||q[8]],owners:ownerFor(q[1]),base:1}));
  BP.forEach((q,i)=>add({lesson:q[0],type:'Explicação Bate-pronto',title:q[2]+' · cartão '+(i+1),label:q[2],lines:[q[5]],owners:ownerFor(q[2]),base:2}));
  const vocabulary=[...new Set(records.flatMap(record=>record.terms))];
  return cache={stamp,entities,records,tables,detect,vocabulary,lessonOwners:AL.map(lesson=>detect(lesson.t).map(e=>e.id))};
 }
 function editDistanceOne(a,b){
  if(Math.abs(a.length-b.length)>1)return false;let i=0,j=0,edits=0;
  while(i<a.length&&j<b.length){if(a[i]===b[j]){i++;j++;continue}if(++edits>1)return false;if(a.length>=b.length)i++;if(b.length>=a.length)j++}
  return edits+(i<a.length||j<b.length?1:0)<=1;
 }
 function interpret(query,context=[]){
  const db=index(),raw=fold(query),input=terms(query),subjects=db.detect(query);
  let comparison=/compar|diferenc|distinc|versus|\bvs\b|\bx\b/.test(raw)||(subjects.length>1&&input.every(token=>subjects.some(e=>terms(e.aliases.join(' ')).includes(token))));
  // Nomes com substantivo compartilhado: "bancos comercial e múltiplo", "fluxos real e monetário".
  if(comparison&&subjects.length>=1){
   const first=subjects.find(e=>e.sequences.some(sequence=>sequence.length>1))||subjects[0],queryWords=words(query);
   db.entities.forEach(candidate=>{if(subjects.includes(candidate))return;const shared=candidate.sequences.some(sequence=>sequence.length>1&&first.sequences.some(other=>other.length>1&&other[0]===sequence[0])&&sequence.slice(1).every(word=>queryWords.includes(word)));if(shared){const suffix=candidate.sequences.find(sequence=>sequence.length>1&&first.sequences.some(other=>other.length>1&&other[0]===sequence[0])&&sequence.slice(1).every(word=>queryWords.includes(word)))?.slice(1).join(' ');const generic=subjects.findIndex(e=>e.sequences.some(sequence=>sequence.join(' ')===suffix));if(generic>=0)subjects.splice(generic,1,candidate);else subjects.push(candidate)}});
  }
  const facets=FACETS.filter(f=>f.pattern.test(raw)).map(f=>f.id);
  for(const [token,facet] of [['funcao','role'],['objetivo','role'],['composicao','composition'],['mandato','mandate'],['limite','limits'],['definicao','definition']])if(input.includes(token)&&!facets.includes(facet))facets.push(facet);
  if(!subjects.length&&context.length&&facets.length){subjects.push(...context.map(id=>db.entities.find(e=>e.id===id)).filter(Boolean));if(subjects.length>1)comparison=true}
  const entityTerms=new Set(subjects.flatMap(e=>terms(e.aliases.join(' '))));
  const keys=input.filter(token=>!entityTerms.has(token)&&!['diferenca','comparacao','comparar','comparativo','explicar','entender','informacao','informacoes'].includes(token));
  const corrections=[],anchored=subjects.length>0||keys.some(token=>token.length>=4&&db.vocabulary.includes(token));
  const keywords=keys.map(token=>{
   if(db.vocabulary.includes(token)||token.length<5||(!anchored&&!(keys.length===1&&token.length>=8)))return token;
   const candidates=db.vocabulary.filter(word=>word.length>=5&&token[0]===word[0]&&editDistanceOne(token,word));
   if(candidates.length===1){corrections.push([token,candidates[0]]);return candidates[0]}return token;
  });
  return {query,subjects:subjects.slice(0,4),extraSubjects:Math.max(0,subjects.length-4),facets,keywords,comparison,corrections};
 }
 function rank(record,request,subject=null,facet=null){
  const selected=subject?[subject]:request.subjects;
  const owns=selected.filter(e=>record.owners.includes(e.id)).length,mentions=selected.filter(e=>!record.owners.includes(e.id)&&record.mentions.includes(e.id)).length;
  if(selected.length&&!owns&&!mentions)return null;
  const hits=request.keywords.filter(token=>record.terms.some(word=>word===token||(token.length>=4&&word.startsWith(token))));
  const labelHits=hits.filter(token=>record.labelTerms.includes(token));
  const matchedFacets=record.facets.filter(f=>request.facets.includes(f));
  if(!selected.length&&!hits.length)return null;
  if(facet&&!record.facets.includes(facet))return null;
  const coverage=request.keywords.length?hits.length/request.keywords.length:1;
  const structured=['Tabela','Quadro comparativo','Mapa mental','Resumo'].includes(record.type)?30:0;
  const primary=selected.some(e=>index().lessonOwners[record.lesson-1]?.includes(e.id))?18:0;
  const score=record.base+structured+primary+(record.type==='Quadro comparativo'&&record.label==='Competências'?20:0)+owns*65+mentions*8+hits.length*20+labelHits.length*8+coverage*25+matchedFacets.length*23+(facet?25:0)+(record.lines.join(' ').length<20?-8:0);
  return {record,score,coverage,owns,hits};
 }
 function unique(ranked,limit){
  const result=[];
  for(const item of ranked){
   const text=fold(item.record.lines.join(' '));
   const signature=value=>new Set(terms(value).filter(t=>!['diretoria','colegiada','colegiado','composicao','1'].includes(t)));
   if(result.some(previous=>{const other=fold(previous.record.lines.join(' '));if(text===other)return true;const a=signature(text),b=signature(other),shared=[...a].filter(x=>b.has(x)).length;return a.size>=4&&b.size>=4&&shared/Math.max(a.size,b.size)>=.8||(a.size>=2&&[...a].every(token=>/^\d+$/.test(token)&&b.has(token)))}))continue;
   result.push(item);if(result.length===limit)break;
  }return result;
 }
 function answer(query,context=[]){
  query=String(query).trim().slice(0,500);const db=index(),request=interpret(query,context);
  if(!query||(!request.keywords.length&&!request.subjects.length))return {query,request,status:'empty',items:[],comparisons:[]};
  const ranked=db.records.map(record=>rank(record,request)).filter(Boolean).sort((a,b)=>b.score-a.score||a.record.id-b.record.id);
  const strong=ranked.filter(item=>(!request.subjects.length||item.owns>0)&&(!request.keywords.length||item.coverage>=.6)&&(!request.subjects.length||request.comparison||request.subjects.every(e=>item.record.owners.includes(e.id)||item.record.mentions.includes(e.id))));
  const focused=strong.filter(item=>request.subjects.length>1&&!request.comparison||!request.facets.length||request.facets.some(f=>item.record.facets.includes(f)));
  const chosen=focused.length?focused:strong.length?strong:ranked;
  const material=chosen.filter(item=>!item.record.type.startsWith('Explicação'));
  const items=unique(material.length?material:chosen,12);
  const status=!items.length?'missing':strong.length?'found':'related';
  const comparisons=[];
  if(request.comparison&&request.subjects.length>=2){
   const facets=request.facets.length?request.facets:['definition','scope','role','nature','composition','mandate','appointment','resources','limits'];
   facets.forEach(facet=>{
    const cells=request.subjects.map(subject=>unique(db.records.map(record=>rank(record,request,subject,facet)).filter(item=>item&&item.owns>0).sort((a,b)=>b.score-a.score||a.record.id-b.record.id),1));
    if(request.facets.length?cells.some(cell=>cell.length):cells.filter(cell=>cell.length).length>=2)comparisons.push({facet,label:FACETS.find(f=>f.id===facet).label,cells});
   });
  }
  if(request.comparison&&request.subjects.length>=2&&!comparisons.length){
   const cells=request.subjects.map(subject=>unique(db.records.map(record=>rank(record,request,subject)).filter(item=>item&&item.owns>0&&!item.record.type.startsWith('Explicação')).sort((a,b)=>Number(b.record.facets.some(f=>['definition','role','scope'].includes(f)))-Number(a.record.facets.some(f=>['definition','role','scope'].includes(f)))||b.score-a.score),1));
   if(cells.filter(cell=>cell.length).length>=2)comparisons.push({facet:'overview',label:'Conceito e características',cells});
  }
  // Sugestões vêm de títulos reais, sem inventar assuntos quando não há correspondência.
  const suggestions=unique(ranked,5).map(item=>item.record.label);
  let originalTable=null;
  if(request.comparison&&request.subjects.length>=2){
   const table=db.tables.find(table=>request.subjects.every(subject=>table.headers.slice(1).some(header=>db.detect(header).length===1&&db.detect(header)[0].id===subject.id)));
   if(table){const columns=request.subjects.map(subject=>table.headers.findIndex((header,i)=>i>0&&db.detect(header).length===1&&db.detect(header)[0].id===subject.id));originalTable={...table,headers:[table.headers[0],...columns.map(i=>table.headers[i])],rows:table.rows.filter(row=>!request.facets.length||facetOf(row[0]).some(f=>request.facets.includes(f))).map(row=>[row[0],...columns.map(i=>row[i])])};if(!originalTable.rows.length)originalTable=null}
  }
  if(!request.comparison&&request.subjects.length===1&&request.keywords.length){
   originalTable=db.tables.find(table=>{
    const found=db.detect(table.title),titleTerms=terms(table.title);
    return table.rows.length<=8&&found.length===1&&found[0].id===request.subjects[0].id&&request.keywords.every(token=>titleTerms.includes(token))&&(!request.facets.length||table.rows.some(row=>facetOf(row[0],table.title).some(f=>request.facets.includes(f))));
   })||null;
  }
  return {query,request,status,items,comparisons,suggestions,originalTable};
 }
 const source=record=>`<span class="consult-source">Aula ${record.lesson} · ${escapeText(record.type)} · ${escapeText(record.title)}</span>`;
 function quote(record){return `<ul class="consult-facts">${record.lines.map(line=>`<li>${escapeText(line)}</li>`).join('')}</ul>${source(record)}`}
 function response(result){
  const {request}=result;
  const messages={found:'Conteúdo encontrado nos seus materiais',related:'Encontrei trechos relacionados',missing:'Não encontrei conteúdo para essa pergunta',empty:'Escreva um assunto ou uma pergunta'};
  let html=`<div class="consult-response-head"><span>${uiIcon('book')}${messages[result.status]}</span></div>`;
  if(result.status==='empty'||result.status==='missing')return html+'<p class="consult-message">Tente citar o nome do órgão, uma sigla ou palavras do assunto. Exemplos: “funções do Bacen”, “limites do FGC” ou “liquidação no SPI”.</p>';
  if(request.extraSubjects)html+='<p class="consult-message">Esta consulta mostra os quatro primeiros assuntos identificados. Para comparar os demais, faça outra pergunta com seus nomes.</p>';
  if(result.status==='related')html+='<p class="consult-message">Estes trechos podem ajudar, mas não encontrei uma resposta específica para todos os termos da pergunta.</p>';
  if(request.comparison&&!result.comparisons.length&&!result.originalTable)html+='<p class="consult-message">Não identifiquei dois assuntos com características para comparar. Abaixo está o conteúdo relacionado que encontrei.</p>';
  if(result.comparisons.length&&!result.originalTable){
   html+=`<div class="consult-table-scroll" role="region" tabindex="0" aria-label="Comparação encontrada nos materiais"><table class="consult-table"><caption>Comparação entre ${request.subjects.map(e=>escapeText(e.name)).join(' e ')}</caption><thead><tr><th scope="col">Característica</th>${request.subjects.map(e=>`<th scope="col">${escapeText(e.name)}</th>`).join('')}</tr></thead><tbody>${result.comparisons.map(row=>`<tr><th scope="row">${row.label}</th>${row.cells.map(cell=>`<td>${cell.length?cell.map(item=>quote(item.record)).join('<div class="consult-cell-gap"></div>'):'<p class="consult-unavailable">Não encontrei essa característica para este assunto nos materiais.</p>'}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }else if(result.originalTable){
   const table=result.originalTable;
   html+=`<div class="consult-table-scroll" role="region" tabindex="0" aria-label="Tabela encontrada nos materiais"><table class="consult-table"><caption>${escapeText(table.title)}</caption><thead><tr>${table.headers.map(label=>`<th scope="col">${escapeText(label)}</th>`).join('')}</tr></thead><tbody>${table.rows.map(row=>`<tr>${row.map((cell,i)=>i?`<td>${escapeText(String(cell))}</td>`:`<th scope="row">${escapeText(String(cell))}</th>`).join('')}</tr>`).join('')}</tbody></table></div><p class="consult-source">Aula ${table.lesson} · Tabela · ${escapeText(table.title)}</p>`;
  }else {
   const primary=result.items.slice(0,3);
   html+=`<div class="consult-answer-grid">${primary.map(item=>`<article class="consult-extract"><h3>${escapeText(item.record.label)}</h3>${item.record.owners.length?`<p class="consult-subject">${escapeText(item.record.owners.map(id=>index().entities.find(e=>e.id===id)?.name).filter(Boolean).join(' · '))}</p>`:''}${quote(item.record)}</article>`).join('')}</div>`;
   if(result.items.length>3)html+=`<details class="consult-more"><summary>Mais trechos relacionados (${result.items.length-3})</summary><div class="consult-answer-grid">${result.items.slice(3).map(item=>`<article class="consult-extract"><h3>${escapeText(item.record.label)}</h3>${item.record.owners.length?`<p class="consult-subject">${escapeText(item.record.owners.map(id=>index().entities.find(e=>e.id===id)?.name).filter(Boolean).join(' · '))}</p>`:''}${quote(item.record)}</article>`).join('')}</div></details>`;
  }
  return html;
 }
 // Destaque aplicado só a nós de texto: preserva fontes, conteúdo e atributos HTML.
 function highlightSequences(request){
  const filler=new Set('funcao faz fazer serve servem atua atuam atribuicao competencia papel responsabilidade objetivo finalidade comparacao comparar comparativo diferenca diferenciar distincao definicao conceito significado significa explicar entender'.split(' '));
  const key=word=>{
   const value=stem(fold(word));
   return value.length>=6&&/(?:ari|ici)[ao]$/.test(value)?value.slice(0,-1):value;
  };
  const sequences=request.subjects.flatMap(subject=>subject.aliases.map(alias=>[...alias.matchAll(/[\p{L}\p{N}]+/gu)].map(match=>key(match[0]))));
  const entityWords=new Set(sequences.flat());
  const keywords=[...words(request.query),...request.keywords].filter(word=>!filler.has(word)&&!entityWords.has(key(word)));
  keywords.forEach(word=>{if(word.length>1)sequences.push([key(word)])});
  return {key,sequences:sequences.filter(sequence=>sequence.length)};
 }
 function highlightedResponse(result){
  const root=document.createElement('div');root.innerHTML=response(result);
  const {key,sequences}=highlightSequences(result.request);
  if(!sequences.length)return root.innerHTML;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),nodes=[];
  while(walker.nextNode())if(!walker.currentNode.parentElement.closest('.consult-source,.consult-response-head,.consult-message,.consult-unavailable'))nodes.push(walker.currentNode);
  nodes.forEach(node=>{
   const text=node.nodeValue,tokens=[...text.matchAll(/[\p{L}\p{N}]+/gu)].map(match=>({key:key(match[0]),start:match.index,end:match.index+match[0].length}));
   const ranges=[];
   sequences.forEach(sequence=>{
    for(let at=0;at<=tokens.length-sequence.length;at++)if(sequence.every((word,i)=>tokens[at+i].key===word))ranges.push([tokens[at].start,tokens[at+sequence.length-1].end]);
   });
   if(!ranges.length)return;
   const merged=[];
   ranges.sort((a,b)=>a[0]-b[0]||b[1]-a[1]).forEach(range=>{const last=merged.at(-1);if(last&&range[0]<last[1])last[1]=Math.max(last[1],range[1]);else merged.push([...range])});
   const fragment=document.createDocumentFragment();let cursor=0;
   merged.forEach(([start,end])=>{fragment.append(document.createTextNode(text.slice(cursor,start)));const mark=document.createElement('mark');mark.className='consult-highlight';mark.textContent=text.slice(start,end);fragment.append(mark);cursor=end});
   fragment.append(document.createTextNode(text.slice(cursor)));node.replaceWith(fragment);
  });
  return root.innerHTML;
 }
 function toggleHistory(section){
  const container=section.querySelector('.consult-history-content');if(!container)return;
  container.innerHTML=section.open?state.entries.slice(0,-1).reverse().map(entry=>`<details class="consult-previous"><summary>${escapeText(entry.query)}</summary>${highlightedResponse(entry)}</details>`).join(''):'';
 }
 function view(){
  return `<section class="consult-page"><div class="consult-intro"><span class="consult-eyebrow">SEUS CONTEÚDOS, EM UM SÓ LUGAR</span><h2>Qual é a sua dúvida?</h2><p>Pergunte sobre as aulas ou compare assuntos. Os trechos e suas fontes aparecem aqui mesmo.</p></div><form class="consult-form" onsubmit="event.preventDefault();Consulta.submit()"><label for="consult-question">Escreva sua pergunta</label><textarea id="consult-question" rows="2" maxlength="500" placeholder="Ex.: Quantos membros compõem a diretoria do Bacen?" oninput="Consulta.draft(this.value)" onkeydown="if(event.key==='Enter'&&!event.shiftKey&&!event.isComposing){event.preventDefault();Consulta.submit()}">${escapeText(state.draft)}</textarea><div class="consult-form-footer"><span>Consulta aos materiais cadastrados</span><div><button type="button" onclick="Consulta.clear()">Limpar</button><button type="submit" class="consult-submit">${uiIcon('search')}Consultar</button></div></div></form><div id="consult-answers">${answers()}</div></section>`;
 }
 function answers(){
  if(!state.entries.length)return `<div class="consult-welcome">${uiIcon('search')}<h3>Consulte sem sair desta tela</h3><p>Busque funções, composição, prazos, limites e diferenças entre os assuntos. As respostas reproduzem o conteúdo das aulas.</p></div>`;
  const current=state.entries.at(-1);
  return `<section class="consult-current" aria-labelledby="consult-answer-title"><h2 id="consult-answer-title" tabindex="-1">${escapeText(current.query)}</h2><div role="status" class="sr-only">Consulta concluída. ${current.items.length} trechos encontrados.</div>${highlightedResponse(current)}</section>${state.entries.length>1?`<details class="consult-history" ontoggle="Consulta.toggleHistory(this)"><summary>Perguntas anteriores <span>${state.entries.length-1}</span></summary><div class="consult-history-content"></div></details>`:''}`;
 }
 function submit(){
  const input=document.getElementById('consult-question'),value=(input?.value||state.draft).trim().slice(0,500);
  if(!value){input?.focus();return}
  state.draft=value;const result=answer(value,state.context);state.entries.push(result);
  state.context=result.request.subjects.map(e=>e.id);
  document.getElementById('consult-answers').innerHTML=answers();document.getElementById('consult-answer-title')?.focus({preventScroll:true});
 }
 function clear(){state.draft='';state.entries=[];state.context=[];const root=document.querySelector('.consult-page');if(root)root.outerHTML=view();document.getElementById('consult-question')?.focus()}
 return {view,submit,toggleHistory,clear,draft(value){state.draft=String(value).slice(0,500)},answer,interpret,index};
})();
