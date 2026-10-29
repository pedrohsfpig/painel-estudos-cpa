/* Consulta local e extrativa. Nenhuma chamada a modelos, APIs ou fontes externas. */
window.Consulta=(()=>{
 'use strict';
 const state={draft:'',entries:[],context:[],pending:null,filters:{lessons:[],types:[]}};
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
 const synonymGroups=[['funcao','atribuicao','competencia','papel','responsabilidade','faz','fazer','atuacao','atua','atuam','serve','servem'],['objetivo','finalidade','proposito'],['composicao','membro','integrante','colegiado','compor'],['mandato','reconducao'],['limite','teto','cobertura'],['captacao','captar'],['emissao','emitir','emite'],['impressao','imprimir','imprime'],['regulacao','regular','regula','regulamentacao','regulamenta'],['autorizacao','autoriza','autorizar'],['garantia','garante','garantido','coberto'],['credito','emprestimo','financiamento','emprestar'],['conceder','concede','concedem'],['definicao','conceito','significado','significa'],['diferenca','diferenciar','comparacao','comparar','distincao'],['fiscalizacao','fiscaliza','supervisao','supervisiona'],['remuneracao','rendimento','rentabilidade'],['reducao','reduzir','reduz'],['obrigacao','obriga','obrigar'],['afeta','afetam','afetar']];
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
   const names=[name,...aliases].filter(Boolean),key=words(name).join(' ');
   const existing=entities.find(e=>words(e.name).join(' ')===key)||aliasOwners.get(key)||names.slice(1).filter(n=>words(n).length>1).map(n=>aliasOwners.get(words(n).join(' '))).find(Boolean);
   const result=existing||{id:'entity-'+entities.length,name,aliases:[],sequences:[]};
   if(!existing)entities.push(result);
   names.forEach(n=>{const sequence=words(n),key=sequence.join(' ');if(!key||result.aliases.includes(n))return;result.aliases.push(n);result.sequences.push(sequence);if(!aliasOwners.has(key))aliasOwners.set(key,result)});
   return result;
  }
  QUESTION_ACRONYMS.forEach(entry=>entity(entry.name,[...entry.aliases,...entry.variants,...entry.name.split(/\s*—\s*/).filter(n=>words(n).length>1),...entry.aliases.filter(a=>/^[A-Z]{2,}$/.test(a)).map(a=>a+'s')]));
  const extras={bc:['bacem','bacin','bacém'],susep:['suzep'],anbima:['ambima'],fgcoop:['fgcop','fgc coop']};
  QUESTION_ACRONYMS.forEach(entry=>{if(extras[entry.id])entity(entry.name,extras[entry.id])});
  const definitions=[];
  AL.forEach((lesson,i)=>(lesson.r||[]).forEach(line=>{
   const match=plain(line).match(/^([A-Z][A-Z0-9-]{1,9})\s*[—–]\s*([^:]+):/);
   if(match&&/^[A-ZÁÀÂÃÉÊÍÓÔÕÚÇ]/.test(match[2].trim())&&words(match[2]).length>1&&words(match[2]).map(word=>word[0]).join('').toUpperCase()===match[1].replace(/-/g,'')){const concept=entity(match[2].trim(),[match[1],match[1]+'s']);definitions.push({lesson:i+1,entity:concept,text:plain(line)})}
  }));
  function overviewEntity(row){
   const key=words(row.name).join(' '),candidates=entities.filter(e=>e.sequences.some(seq=>seq.join(' ')===key));
   const hint=fold([row.kind,row.form,...searchStrings(row.base)].join(' '));
   const match=candidates.filter(e=>fold(e.name)===fold(row.kind)||hint.includes(fold(e.name)));
   return match.length===1?match[0]:entity(row.name,[row.short,...(row.short||'').split(/\s*·\s*/)].filter(Boolean));
  }
  Object.values(LESSON_OVERVIEWS).forEach(overview=>overview.rows.forEach(overviewEntity));
  // Apelidos de operadores vêm dos títulos cadastrados, não acrescentam fatos.
  const operatorAliases=[['Banco comercial',['bancos comerciais']],['Banco múltiplo',['bancos múltiplos']],['Banco de investimento',['bancos de investimentos']],['Banco de desenvolvimento',['bancos de desenvolvimento']],['Cooperativa de crédito',['cooperativas de crédito']],['Instituição de pagamento',['instituições de pagamentos','instituição de pagamentos']],['Corretora de Títulos e Valores Mobiliários',['corretora','corretoras']],['Distribuidora de Títulos e Valores Mobiliários',['distribuidora','distribuidoras']],['Entidade Aberta de Previdência Complementar',['previdência aberta']],['Entidade Fechada de Previdência Complementar',['previdência fechada','fundos de pensão']]];
  operatorAliases.forEach(([name,aliases])=>entity(name,aliases));
  const genericLabels=/^(natureza|diretoria|composicao|objetivo|competencia|atribuicao|funcao|papel|papeis|recurso|requisito|caminho|mandato|exoneracao|autorizacao|penalidade|poder|macete|dica|pegadinha|numero|atencao|cuidados|regra|reuniao|observac|exemplo|comparac)/;
  Object.values(MAT).forEach(M=>(M.mm?.[1]||[]).forEach(branch=>{const label=branch[0];if(typeof label!=='string'||genericLabels.test(fold(label))||FACETS.some(f=>f.pattern.test(fold(label)))||words(label).length>5||(words(label).length===1&&!/^(inflacao|compulsorio|redesconto|deflacao|poupanca|liquidez)$/.test(stem(fold(label)))))return;const key=words(label).join(' ');if(!aliasOwners.has(key))entity(label).topic=true}));
  [['Inflação',[]],['Taxa Selic',['meta Selic']]].forEach(([name,aliases])=>entity(name,aliases).topic=true);
  const sequenceAt=(hay,needle,at)=>needle.every((word,i)=>hay[at+i]===word);
  // Apelidos curtos também podem estar escritos como "Registradora (TR)".
  Object.values(MAT).forEach(material=>searchStrings(Object.values(material)).forEach(text=>{
   const match=text.match(/^([\p{L}][\p{L}\s-]{2,70})\s*\(([A-Z][A-Z0-9-]{1,9})\)$/u);
   if(!match)return;
   const label=match[1].trim(),key=words(match[2]).join(' '),labelWords=words(label);
   const candidates=entities.filter(e=>e.sequences.some(seq=>seq.join(' ')===key)&&e.aliases.some(alias=>labelWords.every(word=>words(alias).includes(word))));
   if(labelWords.length&&candidates.length===1){const concept=entity(candidates[0].name,[label]);concept.sourceAliases=[...new Set([...(concept.sourceAliases||[]),label])];}
  }));
  const meaningAliases=new Map();
  entities.forEach(e=>e.aliases.filter(alias=>/^[A-Z][A-Z0-9-]{1,9}s?$/.test(alias)).forEach(alias=>{
   const key=words(alias).join(' '),list=meaningAliases.get(key)||[];
   if(!list.some(item=>item.id===e.id))list.push(e);meaningAliases.set(key,list);
  }));
  const ambiguous=new Map([...meaningAliases].filter(([,list])=>list.length>1));
  const ambiguousEntities=[...new Set([...ambiguous.values()].flat())];
  AL.forEach((lesson,i)=>{
   const chunks=[...(lesson.r||[]),...searchStrings(Object.values(MAT[i+1]||{}))].map(plain);
   ambiguousEntities.forEach(e=>chunks.forEach(text=>{
    if(e.aliases.some(alias=>(words(alias).length>1||e.sourceAliases?.includes(alias))&&fold(text).includes(fold(alias))))definitions.push({lesson:i+1,entity:e,text});
   }));
  });
  function resolveMeaning(key,text,options={}){
   const candidates=ambiguous.get(key)||[],input=words(text),selected=options.choices?.[key];
   if(selected&&candidates.some(e=>e.id===selected))return candidates.find(e=>e.id===selected);
   const named=candidates.filter(e=>e.sequences.some(sequence=>sequence.length>1&&input.some((_,at)=>sequenceAt(input,sequence,at))));
   if(named.length===1)return named[0];
   const contextual=candidates.filter(e=>options.context?.includes(e.id));
   if(options.lesson){const found=candidates.filter(e=>definitions.some(d=>d.entity.id===e.id&&d.lesson===options.lesson));if(found.length===1)return found[0]}
   const generic=new Set(terms('função cálculo calculada calculado funciona comparação diferença significado conceito taxa explicar'));
   const queryTerms=terms(text).filter(t=>!generic.has(t)&&t!==key);
   const scores=candidates.map(e=>({e,score:definitions.filter(d=>d.entity.id===e.id).reduce((best,d)=>Math.max(best,queryTerms.filter(t=>terms(d.text).includes(t)).length),0)})).sort((a,b)=>b.score-a.score);
   if(scores[0]?.score>0&&scores[0].score>(scores[1]?.score||0))return scores[0].e;
   if(contextual.length===1)return contextual[0];
   return null;
  }
  function ambiguities(text,options={}){
   const input=words(text);
   return [...ambiguous].filter(([key])=>input.includes(key)&&!resolveMeaning(key,text,options)).map(([key,candidates])=>({key,label:candidates.flatMap(e=>e.aliases).find(a=>fold(a)===key)||key.toUpperCase(),candidates}));
  }
  function detect(text,options={}){
   const input=words(text),matches=[];
   entities.forEach(e=>e.sequences.forEach(sequence=>{for(let at=0;at<=input.length-sequence.length;at++)if(sequenceAt(input,sequence,at)){
    const key=sequence.join(' ');if(ambiguous.has(key)&&resolveMeaning(key,text,options)?.id!==e.id)continue;
    matches.push({e,at,length:sequence.length});
   }}));
   const occupied=new Set(),found=[];
   matches.sort((a,b)=>b.length-a.length||a.at-b.at).forEach(match=>{if(Array.from({length:match.length},(_,i)=>match.at+i).some(i=>occupied.has(i)))return;for(let i=0;i<match.length;i++)occupied.add(match.at+i);if(!found.some(item=>item.e.id===match.e.id))found.push(match)});
   return found.sort((a,b)=>a.at-b.at).map(item=>item.e);
  }
  function ownerFor(label,fallback=[],lesson=null){const found=detect(label,{lesson});return found.length===1?(found[0].topic?[...new Set([...fallback,found[0].id])]:found.map(e=>e.id)):found.length>1?[]:fallback}
  function add({lesson,type,title,label=title,lines,owners=[],base=10,facets=null,table=null,group=null}){
   lines=lines.flat(Infinity).filter(value=>typeof value==='string'&&value.trim()).map(plain);if(!lines.length)return;
   const text=lines.join(' · '),record={id:records.length,lesson,type,title:plain(title),label:plain(label),lines,owners,base,facets:facets||facetOf(label,text),table,group};
   record.terms=terms([title,label,text].join(' '));record.labelTerms=terms(label);record.mentions=detect([label,text].join(' '),{lesson}).map(e=>e.id);
   records.push(record);
  }
  AL.forEach((lesson,i)=>{
   const n=i+1,M=MAT[n],defaultOwners=ownerFor(M?.mm?.[0]||lesson.t,[],n);
   [['r','Resumo'],['d','Dicas e macetes'],['p','Pegadinhas']].forEach(([key,type])=>(lesson[key]||[]).forEach((text,at)=>{
    const prefix=plain(text).split(':')[0];add({lesson:n,type,title:type+' · '+lesson.t,label:prefix,lines:[text],owners:ownerFor(prefix,defaultOwners,n),base:key==='r'?22:8});
   }));
   (lesson.n||[]).forEach(([value,label])=>add({lesson:n,type:'Números para decorar',title:label,label,lines:[`${value} — ${label}`],owners:ownerFor(label,defaultOwners,n),base:20}));
   if(M){
    const walk=(branches,path,owners,inherited=[])=>branches.forEach(branch=>{
     if(!Array.isArray(branch))return;
     const [label,items]=branch;if(!Array.isArray(items))return;
     const own=ownerFor(label,owners,n),direct=items.filter(item=>typeof item==='string');
     add({lesson:n,type:'Mapa mental',title:[...path,label].join(' · '),label,lines:direct,owners:own,base:25,facets:facetOf(label).length?facetOf(label):inherited});
     walk(items.filter(Array.isArray),[...path,label],own,facetOf(label).length?facetOf(label):inherited);
    });
    walk(M.mm?.[1]||[],[],defaultOwners);
    (M.tb||[]).forEach(([title,headers,rows])=>{
     const table={id:tables.length,lesson:n,title,headers,rows};tables.push(table);
     const columnOwners=headers.slice(1).map(h=>detect(h,{lesson:n}));
     const compared=columnOwners.length>=2&&columnOwners.every(found=>found.length===1);
     rows.forEach(row=>{
      if(compared)row.slice(1).forEach((cell,j)=>add({lesson:n,type:'Tabela',title:title+' · '+row[0],label:row[0],lines:[String(cell)],owners:[columnOwners[j][0].id],base:30,table:table.id}));
      else {
       const rowEntities=detect(String(row[0]),{lesson:n}),own=rowEntities.length===1?rowEntities.map(e=>e.id):ownerFor(title,defaultOwners,n);
       const lines=row.slice(1).map((cell,j)=>headers.length>2?`${headers[j+1]}: ${cell}`:String(cell));
       add({lesson:n,type:'Tabela',title:title+' · '+row[0],label:row[0],lines,owners:own,base:25,facets:facetOf(row[0],title+' '+lines.join(' ')),table:table.id});
      }
     });
    });
    (M.dg||[]).forEach((diagram)=>diagram[2].forEach(node=>add({lesson:n,type:'Diagrama',title:diagram[1],label:node[0],lines:node.slice(0,2).filter(v=>typeof v==='string'),owners:ownerFor(diagram[1],defaultOwners,n),base:16})));
    (M.tl||[]).forEach(([title,items],at)=>{
     // O contexto pertence à mesma fonte, nunca a uma aula inteira.
     const group={id:`timeline-${n}-${at}`,text:searchStrings(items).join(' '),title:plain(title)};
     items.forEach(item=>add({lesson:n,type:'Linha do tempo',title,label:item[0],lines:searchStrings(item),owners:ownerFor(title,defaultOwners,n),base:18,facets:facetOf(title,searchStrings(item).join(' ')),group}));
    });
    (M.fc||[]).forEach(([question,answer])=>add({lesson:n,type:'Flashcard',title:question,label:question,lines:[answer],owners:ownerFor(question,defaultOwners,n),base:26}));
   }
   const overview=LESSON_OVERVIEWS[n];
   if(overview)overview.rows.forEach(row=>{
    const own=[overviewEntity(row).id],mapping={scope:'scope',powers:'role',focus:'scope',activity:'role',role:'role',leadership:'composition',affiliation:'nature',resources:'resources',limits:'limits',rules:'rules',account:'rules',flows:'rules',base:'definition'};
    add({lesson:n,type:'Quadro comparativo',title:row.name,label:'Natureza',lines:[row.kind,row.form].filter(Boolean),owners:own,base:30,facets:['nature']});
    overview.columns.slice(1).forEach(([key,label])=>add({lesson:n,type:'Quadro comparativo',title:row.name+' · '+label,label,lines:searchStrings(row[key]),owners:own,base:32,facets:mapping[key]?[mapping[key]]:facetOf(label)}));
   });
  });
  Q.forEach((q,i)=>add({lesson:q[0],type:'Explicação de questão',title:q[1]+' · questão '+(i+1),label:q[1],lines:[q[11]?.[0]||q[8]],owners:ownerFor(q[1],[],q[0]),base:1}));
  BP.forEach((q,i)=>add({lesson:q[0],type:'Explicação Bate-pronto',title:q[2]+' · cartão '+(i+1),label:q[2],lines:[q[5]],owners:ownerFor(q[2],[],q[0]),base:2}));
  records.forEach(record=>{
   if(record.group){record.group.mentions=detect(record.group.title+' '+record.group.text,{lesson:record.lesson}).map(e=>e.id);record.group.terms=terms(record.group.title+' '+record.group.text)}
  });
  const vocabulary=[...new Set(records.flatMap(record=>record.terms))];
  return cache={stamp,entities,records,tables,detect,ambiguities,vocabulary,lessonOwners:AL.map(lesson=>detect(lesson.t).map(e=>e.id))};
 }
 function editDistanceOne(a,b){
  if(Math.abs(a.length-b.length)>1)return false;let i=0,j=0,edits=0;
  while(i<a.length&&j<b.length){if(a[i]===b[j]){i++;j++;continue}if(++edits>1)return false;if(a.length>=b.length)i++;if(b.length>=a.length)j++}
  return edits+(i<a.length||j<b.length?1:0)<=1;
 }
 // Intenções orientam a seleção de evidências; não geram fatos novos.
 const RELATIONS=[
  {id:'history',query:/\bantes\b|\bantig[ao]s?\b|anterior|preced|anteced|mudou|mudanca|sucede|substitu|entrou no lugar|veio no lugar|passou a|quando .*(?:cri|entrou|passou|comec|inici|surg|adot)|em que ano|\brenome|novo nome|desde quando|\bdepois\b|historico|evolucao/,
   evidence:/substitu|mudanca de referencia|antes de \d{4}|desde .*\d{4}|instituiu|criad|originou|originando|integracao|se unem|adota/,
   ignore:'era eram foi foram usava usavam usada usado usados usadas utilizava utilizado utilizada entrou lugar veio depois antes antigamente anterior anteriormente antecedeu antecedia passou valer taxa referencia nova novo antiga antigo agora ainda acontece aconteceu mudou mudanca substituiu substituida substituido substitui substituicao sucedeu sucedida sucedido precedia precedeu data ano anos inicio iniciou comecou criada criado criacao historico evolucao so nome renomeacao apenas simples'},
  {id:'calculation',query:/calcul|como .*obt|como .*form|deriv|a partir de que|qual .*base|de onde vem/,
   evidence:/calcul|a partir|redutor|formula|composicao|combin|parcela|obtida|apurad|baseada|baseado/,
   ignore:'calculada calculado calcular calcula calculo obtida obtido formada formado forma deriva derivada derivado partir vem base'},
  {id:'cause',query:/por que|porque|motivo|consequencia|efeito|impacto|influenc|o que acontece|o que ocorre/,
   evidence:/porque|pois |devido|em razao|por isso|depende|dependem|pode |podem |permite|permitem|reduz|eleva|aumenta|afeta|pression|restring|incentiv|decorre|evita|condicion/,
   ignore:'motivo razao consequencia efeito impacto influencia acontece ocorre nao afeta afetam afetar'},
  {id:'sequence',query:/etapas|passo a passo|sequencia|qual .*ordem|como funciona|como .*funciona/,
   evidence:/primeir|segund|terceir|etapa|apos|antes|depois|encaminh|aprova|liquida|negocia|compensa|capta|empresta/,
   ignore:'etapa passo sequencia ordem funciona funcionamento'}
 ];
 function relationEvidence(record,request){
  if(!request.relation)return null;
  const rule=RELATIONS.find(r=>r.id===request.relation),local=record.label+' '+record.lines.join(' ');
  const grouped=record.group&&(request.relation==='history'||request.relation==='sequence');
  const text=fold((grouped?record.group.title+' '+record.group.text+' ':'')+local);
  if(!rule.evidence.test(text))return null;
  if(request.relation==='history'){
   const historical=text.replace(/\bnao (?:\w+ ){0,3}substitu\w*/g,'');
   if(!rule.evidence.test(historical))return null;
   if(!grouped&&request.direction&&!/substitu|anteced|sucede|entrou no lugar|mudanca de referencia/.test(historical))return null;
   if(!grouped&&request.subjects.length&&!request.subjects.some(e=>record.owners.includes(e.id)||index().detect(record.label).some(owner=>owner.id===e.id)))return null;
  }
  // Um item vizinho só é recuperado se a fonte inteira explicitar a relação.
  if(grouped&&request.relation==='history'&&!/mudanca|substitu|histor|marco|evolu|moderniz|cria|origem|integracao|datas/.test(fold(record.group.title)))return null;
  if(grouped&&request.relation==='history'&&request.direction&&!/mudanca|substitu|evolu|origem|integracao/.test(fold(record.group.title))&&!/substitu|se unem|originando/.test(fold(record.group.text)))return null;
  const mentions=grouped?record.group.mentions:record.mentions;
  if(request.subjects.length&&!request.subjects.every(e=>mentions.includes(e.id)))return null;
  const vocabulary=grouped?record.group.terms:record.terms;
  const hits=request.keywords.filter(token=>vocabulary.some(word=>word===token||(token.length>=4&&word.startsWith(token))));
  if(!request.subjects.length&&!hits.length)return null;
  const coverage=request.keywords.length?hits.length/request.keywords.length:1;
  // Intenção e relação explícita precedem a popularidade e a posse da entidade.
  const labelHits=hits.filter(token=>record.labelTerms.includes(token)).length;
  const direction=request.relation==='history'&&record.group?(
   request.direction==='before'&&/antes|anterior/.test(fold(local))||request.direction==='after'&&/desde|nova|substituiu/.test(fold(local))?25:0):0;
  const score=200+coverage*60+hits.length*16+labelHits*30+direction+(grouped?35:0)+(record.type==='Resumo'?20:0)+(record.type.startsWith('Explicação')?-50:0);
  return {record,score,coverage,owns:request.subjects.filter(e=>record.owners.includes(e.id)).length,hits,relation:true};
 }
 function interpret(query,context=[],options={}){
  const db=index(),raw=fold(query),input=terms(query),meaning={choices:options.choices,context,lesson:options.lessons?.length===1?options.lessons[0]:null},subjects=db.detect(query,meaning);
  const unresolved=db.ambiguities(query,meaning);
  const relation=['cause','calculation','history','sequence'].map(id=>RELATIONS.find(rule=>rule.id===id)).find(rule=>rule.query.test(raw))?.id||null;
  const direction=/antes|anterior|preced|antig/.test(raw)?'before':/depois|entrou no lugar|veio no lugar|sucede|substituiu/.test(raw)?'after':null;
  let comparison=/compar|diferenc|distinc|versus|\bvs\b|\bx\b/.test(raw)||(subjects.length>1&&input.every(token=>subjects.some(e=>terms(e.aliases.join(' ')).includes(token))));
  // Nomes com substantivo compartilhado: "bancos comercial e múltiplo", "fluxos real e monetário".
  if(comparison&&subjects.length>=1){
   const first=subjects.find(e=>e.sequences.some(sequence=>sequence.length>1))||subjects[0],queryWords=words(query);
   db.entities.forEach(candidate=>{if(subjects.includes(candidate))return;const shared=candidate.sequences.some(sequence=>sequence.length>1&&first.sequences.some(other=>other.length>1&&other[0]===sequence[0])&&sequence.slice(1).every(word=>queryWords.includes(word)));if(shared){const suffix=candidate.sequences.find(sequence=>sequence.length>1&&first.sequences.some(other=>other.length>1&&other[0]===sequence[0])&&sequence.slice(1).every(word=>queryWords.includes(word)))?.slice(1).join(' ');const generic=subjects.findIndex(e=>e.sequences.some(sequence=>sequence.join(' ')===suffix));if(generic>=0)subjects.splice(generic,1,candidate);else subjects.push(candidate)}});
  }
  const facets=FACETS.filter(f=>f.pattern.test(raw)).map(f=>f.id);
  for(const [token,facet] of [['funcao','role'],['objetivo','role'],['composicao','composition'],['mandato','mandate'],['limite','limits'],['definicao','definition']])if(input.includes(token)&&!facets.includes(facet))facets.push(facet);
  if(!subjects.length&&context.length&&(facets.length||relation)){subjects.push(...context.map(id=>db.entities.find(e=>e.id===id)).filter(Boolean));if(subjects.length>1)comparison=true}
  const entityTerms=new Set(subjects.flatMap(e=>terms(e.aliases.join(' '))));
  const relationWords=new Set(terms(RELATIONS.find(rule=>rule.id===relation)?.ignore||''));
  const keys=input.filter(token=>!entityTerms.has(token)&&!relationWords.has(token)&&!['diferenca','comparacao','comparar','comparativo','explicar','entender','informacao','informacoes'].includes(token));
  const corrections=[],anchored=subjects.length>0||keys.some(token=>token.length>=4&&db.vocabulary.includes(token));
  const keywords=keys.map(token=>{
   if(db.vocabulary.includes(token)||token.length<5||(!anchored&&!(keys.length===1&&token.length>=8)))return token;
   const candidates=db.vocabulary.filter(word=>word.length>=5&&token[0]===word[0]&&editDistanceOne(token,word));
   if(candidates.length===1){corrections.push([token,candidates[0]]);return candidates[0]}return token;
  });
  return {query,subjects:subjects.slice(0,4),extraSubjects:Math.max(0,subjects.length-4),facets,keywords,comparison,corrections,relation,direction,ambiguities:unresolved};
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
  if(facet==='mandate'){
   const body=fold(record.lines.filter(line=>fold(line)!==fold(record.label)).join(' '));
   if(!/\b(anos?|meses|prazo|duracao|periodo|mandato)\b|recondu|exoner/.test(body))return null;
  }
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
 const TYPES=['Resumo','Dicas e macetes','Pegadinhas','Números para decorar','Mapa mental','Tabela','Quadro comparativo','Diagrama','Linha do tempo','Flashcard','Explicação de questão','Explicação Bate-pronto'];
 function normalizeOptions(options={}){
  return {lessons:[...new Set((options.lessons||[]).filter(n=>Number.isInteger(n)&&n>0&&n<=AL.length))],types:[...new Set((options.types||[]).filter(t=>TYPES.includes(t)))],choices:{...(options.choices||{})},features:Array.isArray(options.features)?[...new Set(options.features.filter(f=>typeof f==='string'))]:null};
 }
 function answer(query,context=[],options={}){
  options=normalizeOptions(options);
  query=String(query).trim().slice(0,500);const db=index(),request=interpret(query,context,options);
  request.filters={lessons:options.lessons,types:options.types};
  if(request.ambiguities.length)return {query,request,status:'clarify',items:[],comparisons:[],options,contextUsed:[...context]};
  const records=db.records.filter(r=>(!options.lessons.length||options.lessons.includes(r.lesson))&&(!options.types.length||options.types.includes(r.type)));
  const tables=db.tables.filter(t=>(!options.lessons.length||options.lessons.includes(t.lesson))&&(!options.types.length||options.types.includes('Tabela')));
  if(!query||(!request.keywords.length&&!request.subjects.length))return {query,request,status:'empty',items:[],comparisons:[]};
  const related=request.relation&&!request.comparison?records.map(record=>relationEvidence(record,request)).filter(Boolean).sort((a,b)=>b.score-a.score||a.record.id-b.record.id):[];
  const ranked=records.map(record=>rank(record,request)).filter(Boolean).sort((a,b)=>b.score-a.score||a.record.id-b.record.id);
  const strong=ranked.filter(item=>(!request.subjects.length||item.owns>0)&&(!request.keywords.length||item.coverage>=.6)&&(!request.subjects.length||request.comparison||request.subjects.every(e=>item.record.owners.includes(e.id)||item.record.mentions.includes(e.id))));
  const focused=strong.filter(item=>request.subjects.length>1&&!request.comparison||!request.facets.length||request.facets.some(f=>item.record.facets.includes(f)));
  const relevant=related.filter(item=>item.coverage>=.75&&item.score>=related[0].score-(request.relation==='cause'?45:65));
  const chosen=relevant.length?relevant:related.length?related:focused.length?focused:strong.length?strong:ranked;
  const material=chosen.filter(item=>!item.record.type.startsWith('Explicação'));
  const items=unique(material.length?material:chosen,12);
  let status=!items.length?'missing':(request.relation&&!request.comparison?relevant.length:strong.length)?'found':'related';
  let comparisons=[];
  const availableComparisons=[];
  if(request.comparison&&request.subjects.length>=2){
   FACETS.forEach(({id:facet,label})=>{
    const cells=request.subjects.map(subject=>unique(records.map(record=>rank(record,request,subject,facet)).filter(item=>item&&item.owns>0).sort((a,b)=>b.score-a.score||a.record.id-b.record.id),1));
    if(cells.some(cell=>cell.length))availableComparisons.push({facet,label,cells});
   });
   comparisons=availableComparisons.filter(row=>request.facets.length?request.facets.includes(row.facet):row.facet!=='rules'&&row.cells.filter(cell=>cell.length).length>=2);
  }
  if(request.comparison&&request.subjects.length>=2&&!comparisons.length){
   const cells=request.subjects.map(subject=>unique(records.map(record=>rank(record,request,subject)).filter(item=>item&&item.owns>0&&!item.record.type.startsWith('Explicação')).sort((a,b)=>Number(b.record.facets.some(f=>['definition','role','scope'].includes(f)))-Number(a.record.facets.some(f=>['definition','role','scope'].includes(f)))||b.score-a.score),1));
   if(cells.filter(cell=>cell.length).length>=2){const overview={facet:'overview',label:'Conceito e características',cells};comparisons.push(overview);availableComparisons.push(overview)}
  }
  // Sugestões vêm de títulos reais, sem inventar assuntos quando não há correspondência.
  const suggestions=unique(ranked,5).map(item=>item.record.label);
  let originalTable=null,comparisonTable=null;
  if(request.comparison&&request.subjects.length>=2){
   const table=tables.find(table=>request.subjects.every(subject=>table.headers.slice(1).some(header=>db.detect(header,{lesson:table.lesson}).length===1&&db.detect(header,{lesson:table.lesson})[0].id===subject.id)));
   if(table){const columns=request.subjects.map(subject=>table.headers.findIndex((header,i)=>i>0&&db.detect(header,{lesson:table.lesson}).length===1&&db.detect(header,{lesson:table.lesson})[0].id===subject.id));comparisonTable={...table,headers:[table.headers[0],...columns.map(i=>table.headers[i])],rows:table.rows.map(row=>[row[0],...columns.map(i=>row[i])])};originalTable={...comparisonTable,rows:comparisonTable.rows.filter(row=>!request.facets.length||facetOf(row[0]).some(f=>request.facets.includes(f)))};if(!originalTable.rows.length){originalTable=null;comparisonTable=null}}
  }
  if(!request.relation&&!request.comparison&&request.subjects.length===1&&request.keywords.length){
   originalTable=tables.find(table=>{
    const found=db.detect(table.title),titleTerms=terms(table.title);
    return table.rows.length<=8&&found.length===1&&found[0].id===request.subjects[0].id&&request.keywords.every(token=>titleTerms.includes(token))&&(!request.facets.length||table.rows.some(row=>facetOf(row[0],table.title).some(f=>request.facets.includes(f))));
   })||null;
  }
  let characteristics=[],selectedFeatures=[];
  if(request.comparison&&request.subjects.length>=2){
   if(comparisonTable){
    characteristics=comparisonTable.rows.map((row,i)=>({id:'row-'+i,label:String(row[0])}));
    selectedFeatures=options.features===null?characteristics.filter((c,i)=>originalTable?.rows.includes(comparisonTable.rows[i])).map(c=>c.id):options.features.filter(id=>characteristics.some(c=>c.id===id));
    if(options.features!==null)originalTable={...comparisonTable,rows:comparisonTable.rows.filter((row,i)=>selectedFeatures.includes('row-'+i))};
   }else {
    characteristics=availableComparisons.map(row=>({id:row.facet,label:row.label}));
    selectedFeatures=options.features===null?comparisons.map(row=>row.facet):options.features.filter(id=>characteristics.some(c=>c.id===id));
    if(options.features!==null)comparisons=availableComparisons.filter(row=>selectedFeatures.includes(row.facet));
   }
  }
  if(relevant.length&&request.relation==='history'){
   const relatedIds=new Set(items.flatMap(item=>item.record.mentions));
   request.relatedSubjects=db.entities.filter(e=>relatedIds.has(e.id)&&!request.subjects.some(s=>s.id===e.id));
  }
  if(request.comparison&&request.subjects.some(e=>!records.some(r=>r.owners.includes(e.id))))status=items.length?'related':'missing';
  return {query,request,status,items,comparisons,suggestions,originalTable,characteristics,selectedFeatures,options,contextUsed:[...context]};
 }
 const source=record=>`<span class="consult-source">Aula ${record.lesson} · ${escapeText(record.type)} · ${escapeText(record.title)}</span>`;
 function passage(record,request){
  const queryTerms=new Set(request.keywords),subjects=[...request.subjects,...(request.relatedSubjects||[])];
  const score=text=>{
   const vocabulary=terms(text),entities=index().detect(text,{lesson:record.lesson});
   return request.facets.filter(id=>FACETS.find(f=>f.id===id)?.pattern.test(fold(text))).length*10+vocabulary.filter(t=>queryTerms.has(t)).length*8+subjects.filter(e=>entities.some(found=>found.id===e.id)).length*3+(request.relation&&RELATIONS.find(rule=>rule.id===request.relation).evidence.test(fold(text))?5:0);
  };
  const candidates=record.lines.map((line,i)=>({line,i,score:score(line)-(record.lines.length>1&&fold(line)===fold(record.label)?100:0)})).sort((a,b)=>b.score-a.score||a.i-b.i);
  const best=candidates[0];
  const sentences=typeof Intl.Segmenter==='function'?[...new Intl.Segmenter('pt-BR',{granularity:'sentence'}).segment(best.line)].map(item=>item.segment.trim()).filter(Boolean):[best.line];
  const focus=sentences.map((text,i)=>({text,i,score:score(text)})).sort((a,b)=>b.score-a.score||a.i-b.i)[0];
  let selected=sentences;
  if(best.line.length>340&&sentences.length>1){
   // Mantenha qualificadores explícitos junto da frase principal.
   const keep=new Set([focus.i]);
   sentences.forEach((text,i)=>{if(/\b(nao|sem|somente|apenas|conforme|depende|dependem|condicoes|ressalva|exceto)\b/.test(fold(text)))keep.add(i)});
   if(focus.i>0&&/^(isso|isto|essa|esse|ela|ele|sua|seu|essa regra|nesse|nessa)\b/.test(fold(focus.text)))keep.add(focus.i-1);
   selected=sentences.filter((_,i)=>keep.has(i));
  }
  let lines=best.line.length>340?selected:[best.line];
  const second=candidates.find(candidate=>candidate.i!==best.i&&fold(candidate.line)!==fold(record.label)&&candidate.score>=best.score-8);
  if(second&&best.line.length+second.line.length<360)lines=record.lines.filter((_,i)=>i===best.i||i===second.i);
  if(request.facets.includes('composition'))lines=record.lines;
  return {lines,focus:focus.text,context:lines.length!==record.lines.length||lines.some((line,i)=>line!==record.lines[i])};
 }
 function quote(record,request){
  const selected=passage(record,request),facts=lines=>`<ul class="consult-facts">${lines.map(line=>`<li>${escapeText(line)}</li>`).join('')}</ul>`;
  const emphasized=line=>{const at=line.indexOf(selected.focus);return at<0?escapeText(line):escapeText(line.slice(0,at))+`<strong class="consult-key-sentence">${escapeText(selected.focus)}</strong>`+escapeText(line.slice(at+selected.focus.length))};
  const excerpt=`<ul class="${selected.context?'consult-passage':'consult-facts'} consult-key-passage">${selected.lines.map(line=>`<li>${emphasized(line)}</li>`).join('')}</ul>`;
  return excerpt+(selected.context?`<details class="consult-context"><summary>Ver contexto</summary>${facts(record.lines)}</details>`:'')+source(record);
 }
 function scopeLabel(result){
  const filters=result.request.filters;if(!filters||(!filters.lessons.length&&!filters.types.length))return '';
  return `<p class="consult-scope">${escapeText([filters.lessons.length?'Aulas '+filters.lessons.join(', '):'Todas as aulas',filters.types.length?filters.types.join(' · '):'Todos os materiais'].join(' · '))}</p>`;
 }
 function clarification(result){
  const ambiguity=result.request.ambiguities[0];
  return `<div class="consult-clarify"><span class="consult-eyebrow">VAMOS ESCLARECER</span><h3>Qual significado de ${escapeText(ambiguity.label)} tu quer consultar?</h3><p>Essa sigla aparece com sentidos diferentes nos materiais. Escolhe um para continuar.</p><div class="consult-meaning-options">${ambiguity.candidates.map(e=>`<button type="button" data-alias="${ambiguity.key}" data-entity="${e.id}" onclick="Consulta.resolve(this.dataset.alias,this.dataset.entity)">${uiIcon('book')}<span>${escapeText(e.name)}</span>${uiIcon('arrow')}</button>`).join('')}</div></div>`;
 }
 function comparisonControls(result){
  return `<details class="consult-characteristics"><summary>Características da comparação <span>${result.selectedFeatures.length} de ${result.characteristics.length}</span></summary><div role="group" aria-label="Características da comparação"><button type="button" data-feature="all" aria-pressed="${result.selectedFeatures.length===result.characteristics.length}" onclick="Consulta.feature('all')">Todas</button>${result.characteristics.map(c=>`<button type="button" data-feature="${c.id}" aria-pressed="${result.selectedFeatures.includes(c.id)}" onclick="Consulta.feature(this.dataset.feature)">${escapeText(c.label)}</button>`).join('')}</div></details>`;
 }
 function response(result,interactive=false){
  const {request}=result;
  const messages={found:'Conteúdo encontrado nos seus materiais',related:'Encontrei trechos relacionados',missing:'Não encontrei conteúdo para essa pergunta',empty:'Escreva um assunto ou uma pergunta',clarify:'Escolha o sentido da sigla para continuar'};
  let html=`<div class="consult-response-head"><span>${uiIcon('book')}${messages[result.status]}</span></div>`;
  html+=scopeLabel(result);
  if(result.status==='clarify')return html+clarification(result);
  if(result.status==='missing'&&(request.filters?.lessons.length||request.filters?.types.length))return html+'<p class="consult-message">Não encontrei trechos dentro dos filtros selecionados. Experimente outras aulas ou tipos de material.</p>';
  if(result.status==='empty'||result.status==='missing')return html+'<p class="consult-message">Tente citar o nome do órgão, uma sigla ou palavras do assunto. Exemplos: “funções do Bacen”, “limites do FGC” ou “liquidação no SPI”.</p>';
  if(interactive&&result.characteristics?.length)html+=comparisonControls(result);
  if(result.options?.features&&result.characteristics?.length&&!result.selectedFeatures.length)return html+`<p class="consult-message">${interactive?'Selecione uma característica para exibir a comparação.':'Nenhuma característica foi selecionada nesta comparação.'}</p>`;
  if(request.extraSubjects)html+='<p class="consult-message">Esta consulta mostra os quatro primeiros assuntos identificados. Para comparar os demais, faça outra pergunta com seus nomes.</p>';
  if(result.status==='related')html+='<p class="consult-message">Estes trechos podem ajudar, mas não encontrei uma resposta específica para todos os termos da pergunta.</p>';
  if(request.comparison&&!result.comparisons.length&&!result.originalTable)html+='<p class="consult-message">Não identifiquei dois assuntos com características para comparar. Abaixo está o conteúdo relacionado que encontrei.</p>';
  if(result.comparisons.length&&!result.originalTable){
   html+=`<div class="consult-table-scroll" role="region" tabindex="0" aria-label="Comparação encontrada nos materiais"><table class="consult-table"><caption>Comparação entre ${request.subjects.map(e=>escapeText(e.name)).join(' e ')}</caption><thead><tr><th scope="col">Característica</th>${request.subjects.map(e=>`<th scope="col">${escapeText(e.name)}</th>`).join('')}</tr></thead><tbody>${result.comparisons.map(row=>`<tr><th scope="row">${row.label}</th>${row.cells.map(cell=>`<td>${cell.length?cell.map(item=>quote(item.record,{...request,facets:[row.facet]})).join('<div class="consult-cell-gap"></div>'):'<p class="consult-unavailable">Não encontrei essa característica para este assunto nos materiais.</p>'}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
  }else if(result.originalTable){
   const table=result.originalTable;
   html+=`<div class="consult-table-scroll" role="region" tabindex="0" aria-label="Tabela encontrada nos materiais"><table class="consult-table"><caption>${escapeText(table.title)}</caption><thead><tr>${table.headers.map(label=>`<th scope="col">${escapeText(label)}</th>`).join('')}</tr></thead><tbody>${table.rows.map(row=>`<tr>${row.map((cell,i)=>i?`<td>${escapeText(String(cell))}</td>`:`<th scope="row">${escapeText(String(cell))}</th>`).join('')}</tr>`).join('')}</tbody></table></div><p class="consult-source">Aula ${table.lesson} · Tabela · ${escapeText(table.title)}</p>`;
  }else {
   const primary=result.items.slice(0,3);
   html+=`<div class="consult-answer-grid">${primary.map(item=>`<article class="consult-extract"><h3>${escapeText(item.record.label)}</h3>${item.record.owners.length?`<p class="consult-subject">${escapeText(item.record.owners.map(id=>index().entities.find(e=>e.id===id)?.name).filter(Boolean).join(' · '))}</p>`:''}${quote(item.record,request)}</article>`).join('')}</div>`;
   if(result.items.length>3)html+=`<details class="consult-more"><summary>Mais trechos relacionados (${result.items.length-3})</summary><div class="consult-answer-grid">${result.items.slice(3).map(item=>`<article class="consult-extract"><h3>${escapeText(item.record.label)}</h3>${item.record.owners.length?`<p class="consult-subject">${escapeText(item.record.owners.map(id=>index().entities.find(e=>e.id===id)?.name).filter(Boolean).join(' · '))}</p>`:''}${quote(item.record,request)}</article>`).join('')}</div></details>`;
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
  const sequences=[...request.subjects,...(request.relatedSubjects||[])].flatMap(subject=>subject.aliases.map(alias=>[...alias.matchAll(/[\p{L}\p{N}]+/gu)].map(match=>key(match[0]))));
  const entityWords=new Set(sequences.flat());
  const keywords=[...words(request.query),...request.keywords].filter(word=>!filler.has(word)&&!entityWords.has(key(word)));
  keywords.forEach(word=>{if(word.length>1)sequences.push([key(word)])});
  return {key,sequences:sequences.filter(sequence=>sequence.length)};
 }
 function highlightedResponse(result,interactive=false){
  const root=document.createElement('div');root.innerHTML=response(result,interactive);
  const {key,sequences}=highlightSequences(result.request);
  if(!sequences.length)return root.innerHTML;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),nodes=[];
  while(walker.nextNode())if(!walker.currentNode.parentElement.closest('.consult-source,.consult-response-head,.consult-message,.consult-unavailable,.consult-characteristics,.consult-clarify,.consult-scope'))nodes.push(walker.currentNode);
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
  container.innerHTML=section.open?[...(state.pending&&!state.pending.replaceOnResolve?state.entries:state.entries.slice(0,-1))].reverse().map(entry=>`<details class="consult-previous"><summary>${escapeText(entry.query)}</summary>${highlightedResponse(entry)}</details>`).join(''):'';
 }
 function filterOptions(){
  const lessons=state.filters.lessons,types=state.filters.types;
  return `<fieldset><legend>Aulas</legend><div class="consult-filter-chips"><button type="button" data-filter="lesson-all" aria-pressed="${!lessons.length}" onclick="Consulta.filter('lessons',0)">Todas as aulas</button>${AL.map((lesson,i)=>`<button type="button" data-filter="lesson-${i+1}" aria-pressed="${lessons.includes(i+1)}" onclick="Consulta.filter('lessons',${i+1})"><span class="consult-lesson-number">${String(i+1).padStart(2,'0')}</span><span>${escapeText(lesson.t.replace(/^Aula \d+:\s*/,''))}</span></button>`).join('')}</div></fieldset><fieldset><legend>Tipos de material</legend><div class="consult-filter-chips"><button type="button" data-filter="type-all" aria-pressed="${!types.length}" onclick="Consulta.filter('types',-1)">Todos os materiais</button>${TYPES.map((type,i)=>`<button type="button" data-filter="type-${i}" aria-pressed="${types.includes(type)}" onclick="Consulta.filter('types',${i})">${escapeText(type)}</button>`).join('')}</div></fieldset><p>Os filtros limitam as fontes consultadas. Com uma pergunta aberta, a resposta se atualiza ao mudar a seleção.</p>`;
 }
 function filterSummary(){return state.filters.lessons.length||state.filters.types.length?`${state.filters.lessons.length?state.filters.lessons.length+(state.filters.lessons.length===1?' aula':' aulas'):'Todas as aulas'} · ${state.filters.types.length?state.filters.types.length+(state.filters.types.length===1?' tipo':' tipos'):'Todos os materiais'}`:'Todas as aulas · Todos os materiais'}
 function view(){
  return `<section class="consult-page"><div class="consult-intro"><span class="consult-eyebrow">SEUS CONTEÚDOS, EM UM SÓ LUGAR</span><h2>Qual é a sua dúvida?</h2><p>Pergunte sobre as aulas ou compare assuntos. Os trechos e suas fontes aparecem aqui mesmo.</p></div><form class="consult-form" onsubmit="event.preventDefault();Consulta.submit()"><label for="consult-question">Escreva sua pergunta</label><textarea id="consult-question" rows="2" maxlength="500" placeholder="Ex.: Quantos membros compõem a diretoria do Bacen?" oninput="Consulta.draft(this.value)" onkeydown="if(event.key==='Enter'&&!event.shiftKey&&!event.isComposing){event.preventDefault();Consulta.submit()}">${escapeText(state.draft)}</textarea><details class="consult-refine"><summary>${uiIcon('search')}Refinar pesquisa <span id="consult-filter-summary">${filterSummary()}</span></summary><div id="consult-refine-options">${filterOptions()}</div></details><div class="consult-form-footer"><span>Consulta aos materiais cadastrados</span><div><button type="button" onclick="Consulta.clear()">Limpar</button><button type="submit" class="consult-submit">${uiIcon('search')}Consultar</button></div></div></form><div id="consult-answers">${answers()}</div></section>`;
 }
 function answers(){
  if(!state.entries.length&&!state.pending)return `<div class="consult-welcome">${uiIcon('search')}<h3>Consulte sem sair desta tela</h3><p>Busque funções, composição, prazos, limites e diferenças entre os assuntos. As respostas reproduzem o conteúdo das aulas.</p></div>`;
  const current=state.pending||state.entries.at(-1),previous=state.pending&&!state.pending.replaceOnResolve?state.entries:state.entries.slice(0,-1);
  return `<section class="consult-current" aria-labelledby="consult-answer-title"><h2 id="consult-answer-title" tabindex="-1">${escapeText(current.query)}</h2><div role="status" class="sr-only">${current.status==='clarify'?'Escolha o significado da sigla para continuar.':'Consulta concluída. '+current.items.length+' trechos encontrados.'}</div>${highlightedResponse(current,true)}</section>${previous.length?`<details class="consult-history" ontoggle="Consulta.toggleHistory(this)"><summary>Perguntas anteriores <span>${previous.length}</span></summary><div class="consult-history-content"></div></details>`:''}`;
 }
 function paintAnswers(focus=true){
  const root=document.getElementById('consult-answers');if(!root)return;
  root.innerHTML=answers();
  if(focus){const target=root.querySelector('.consult-clarify button')||document.getElementById('consult-answer-title');target?.focus({preventScroll:true})}
 }
 function accept(result,replace=false){
  if(result.status==='clarify')state.pending=result;
  else {state.pending=null;if(replace)state.entries[state.entries.length-1]=result;else state.entries.push(result);state.context=result.request.subjects.map(e=>e.id)}
 }
 function submit(){
  const input=document.getElementById('consult-question'),value=(input?.value||state.draft).trim().slice(0,500);
  if(!value){input?.focus();return}
  state.draft=value;
  accept(answer(value,state.context,state.filters));paintAnswers();
 }
 function resolve(alias,id){
  const pending=state.pending;if(!pending||!pending.request.ambiguities.some(a=>a.key===alias&&a.candidates.some(e=>e.id===id)))return;
  const options={...pending.options,choices:{...pending.options.choices,[alias]:id}};
  const result=answer(pending.query,pending.contextUsed,options);result.replaceOnResolve=pending.replaceOnResolve;accept(result,!!pending.replaceOnResolve);paintAnswers();
 }
 function filter(kind,value){
  if(!['lessons','types'].includes(kind))return;
  const isLesson=kind==='lessons',item=isLesson?value:TYPES[value];
  if((isLesson&&value===0)||(!isLesson&&value===-1))state.filters[kind]=[];
  else {if(isLesson?(!Number.isInteger(value)||value<1||value>AL.length):!item)return;const previous=state.filters[kind];state.filters[kind]=previous.includes(item)?previous.filter(v=>v!==item):[...previous,item];if(isLesson)state.filters[kind].sort((a,b)=>a-b)}
  const target=isLesson?'lesson-'+(value||'all'):'type-'+(value===-1?'all':value);
  const root=document.getElementById('consult-refine-options');if(root)root.innerHTML=filterOptions();
  const summary=document.getElementById('consult-filter-summary');if(summary)summary.textContent=filterSummary();
  const current=state.pending||state.entries.at(-1);
  if(current&&state.draft.trim()===current.query){
   const replace=state.pending?!!state.pending.replaceOnResolve:true,result=answer(current.query,current.contextUsed,{...current.options,...state.filters,features:null});
   // A pending re-interpretation replaces its current response when resolved.
   result.replaceOnResolve=replace;accept(result,replace);paintAnswers(false);
  }
  document.querySelector(`[data-filter="${target}"]`)?.focus({preventScroll:true});
 }
 function feature(id){
  const current=state.entries.at(-1);if(!current||state.pending||!current.characteristics?.length)return;
  const allowed=current.characteristics.map(c=>c.id);if(id!=='all'&&!allowed.includes(id))return;
  const selected=id==='all'?allowed:current.selectedFeatures.includes(id)?current.selectedFeatures.filter(f=>f!==id):[...current.selectedFeatures,id];
  const result=answer(current.query,current.contextUsed,{...current.options,features:selected});accept(result,true);paintAnswers(false);
  const details=document.querySelector('.consult-current .consult-characteristics');if(details)details.open=true;
  document.querySelector(`.consult-current [data-feature="${id}"]`)?.focus({preventScroll:true});
 }
 function clear(){state.draft='';state.entries=[];state.context=[];state.pending=null;state.filters={lessons:[],types:[]};const root=document.querySelector('.consult-page');if(root)root.outerHTML=view();document.getElementById('consult-question')?.focus()}
 return {view,submit,toggleHistory,clear,resolve,filter,feature,draft(value){state.draft=String(value).slice(0,500)},answer,interpret,index};
})();
