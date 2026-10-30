/* Galeria adicional. Não modifica MAT nem o desenho das Ramificações. */
window.MentalMaps=(()=>{
 'use strict';
 const selected=new Map();
 const catalog=()=>window.MENTAL_MAPS||[];
 const key=(lesson,block)=>`${lesson}:${block||0}`;
 const available=(lesson=mt.a,block=selectedLessonBlocks[lesson]||0)=>catalog().filter(m=>m.lesson===lesson&&(!block||m.block===block));
 function current(){const maps=available();return maps.find(m=>m.id===selected.get(key(mt.a,selectedLessonBlocks[mt.a])))||maps[0]}
 function select(id,focus=true){const map=available().find(m=>m.id===id);if(!map)return;selected.set(key(mt.a,selectedLessonBlocks[mt.a]),id);if(!focus)return;go();document.querySelector(`[data-visual-map-choice="${id}"]`)?.focus({preventScroll:true})}
 const text=m=>[m.title,...m.branches.flatMap(([label,items])=>[label,...items]),m.note].join(' · ');
 function transcript(m){return `<div class="visual-map-transcript">${m.branches.map(([label,items])=>`<section><h4>${escapeText(label)}</h4><ul>${items.map(t=>`<li>${escapeText(t)}</li>`).join('')}</ul></section>`).join('')}<p>${escapeText(m.note)}</p></div>`}
 function render(){
  const maps=available(),m=current();if(!m)return '<p class="empty-state">Ainda não há mapa visual para esta seleção.</p>';
  return `${maps.length>1?`<nav class="visual-map-choices" aria-label="Mapas desta aula">${maps.map(item=>`<button type="button" data-visual-map-choice="${item.id}" aria-pressed="${m.id===item.id}" onclick="MentalMaps.select('${item.id}')"><span class="visual-map-choice-number">${String(maps.indexOf(item)+1).padStart(2,'0')}</span>${escapeText(item.title)}</button>`).join('')}</nav>`:''}<section class="visual-map-panel" data-visual-map="${m.id}" aria-labelledby="visual-map-title"><header class="visual-map-toolbar"><div><span class="material-eyebrow">MAPA ${maps.indexOf(m)+1} DE ${maps.length}</span><h3 id="visual-map-title">${escapeText(m.title)}</h3></div><div class="visual-map-actions"><button type="button" data-map-open="${m.id}" onclick="MentalMaps.open('${m.id}')">${uiIcon('search')}Ampliar</button><a href="${m.src}" download="${m.id}.webp">Baixar imagem ${uiIcon('arrow')}</a></div></header><figure><button type="button" class="visual-map-preview" aria-label="Ampliar mapa mental: ${escapeText(m.title)}" onclick="MentalMaps.open('${m.id}')"><img src="${m.src}" width="1536" height="1024" decoding="async" alt="Mapa mental de ${escapeText(m.title)}. Versão em texto disponível abaixo." onerror="this.closest('button').hidden=true;this.closest('figure').querySelector('.visual-map-error').hidden=false"></button><p class="visual-map-error" hidden>Não foi possível carregar a imagem. Você pode consultar o conteúdo em texto abaixo.</p><figcaption>Síntese visual · Aula ${m.lesson}${m.block?' · '+escapeText(m.sourceTitle):''}</figcaption></figure><details class="visual-map-text"><summary>Consultar conteúdo em texto</summary>${transcript(m)}</details></section>`;
 }
 let opener=null,scale=1,mapInViewer=null;
 function viewer(){
  let dialog=document.getElementById('mental-map-viewer');if(dialog)return dialog;
  dialog=document.createElement('dialog');dialog.id='mental-map-viewer';dialog.className='mental-map-viewer';dialog.setAttribute('aria-labelledby','mental-map-viewer-title');
  dialog.innerHTML='<header><h2 id="mental-map-viewer-title"></h2><div class="visual-map-actions"><button type="button" data-map-zoom="-1" aria-label="Diminuir mapa">−</button><output aria-live="polite">100%</output><button type="button" data-map-zoom="1" aria-label="Aumentar mapa">+</button><button type="button" data-map-fit>Ajustar</button><button type="button" data-map-close>Fechar</button></div></header><p class="mental-map-viewer-help">Use + e − para ampliar. Role a imagem para ver os detalhes. Esc fecha.</p><div class="mental-map-canvas" role="region" aria-label="Imagem ampliada do mapa mental" tabindex="0"><img width="1536" height="1024"></div>';
  document.body.append(dialog);
  dialog.querySelector('[data-map-close]').onclick=()=>dialog.close();
  dialog.querySelector('[data-map-fit]').onclick=()=>zoom(0,true);
  dialog.querySelectorAll('[data-map-zoom]').forEach(b=>b.onclick=()=>zoom(Number(b.dataset.mapZoom)));
  dialog.addEventListener('keydown',e=>{if(e.key==='+'||e.key==='='){e.preventDefault();zoom(1)}else if(e.key==='-'){e.preventDefault();zoom(-1)}});
  dialog.addEventListener('close',()=>{document.body.classList.remove('mental-map-viewing');const focus=opener?.isConnected?opener:document.querySelector(`[data-map-open="${mapInViewer}"]`);focus?.focus({preventScroll:true})});
  return dialog;
 }
 function zoom(delta,fit=false){const dialog=viewer();scale=fit?1:Math.max(1,Math.min(3,Math.round((scale+delta*.25)*100)/100));dialog.querySelector('.mental-map-canvas img').style.width=`${scale*100}%`;dialog.querySelector('output').value=Math.round(scale*100)+'%';dialog.querySelector('[data-map-zoom="-1"]').disabled=scale===1;dialog.querySelector('[data-map-zoom="1"]').disabled=scale===3}
 function open(id){const m=catalog().find(m=>m.id===id);if(!m)return;opener=document.activeElement;mapInViewer=id;const dialog=viewer();dialog.querySelector('h2').textContent=m.title;const img=dialog.querySelector('img');img.src=m.src;img.alt=`Mapa mental: ${m.title}`;zoom(0,true);if(!dialog.open)dialog.showModal();document.body.classList.add('mental-map-viewing');dialog.querySelector('[data-map-close]').focus();dialog.querySelector('.mental-map-canvas').scrollTo(0,0)}
 return {catalog,available,current,select,text,transcript,render,open};
})();
