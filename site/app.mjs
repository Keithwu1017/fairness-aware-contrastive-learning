/* Browser-only presentation. No inference, network upload, or private model code. */
export const columns = ['scenario', 'model', 'group', 'auroc', 'tpr', 'tnr', 'n'];
export const models = ['Baseline', 'Fairness-aware'];

export function parseCSV(text) {
  text = text.replace(/^\uFEFF/, '');
  const records = []; let record = [], value = '', quoted = false, closed = false;
  const field = () => {record.push(value); value = ''; closed = false;};
  const row = () => {field(); if (record.some(v => v.trim() !== '')) records.push(record); record = [];};
  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    if (quoted) {
      if (ch === '"' && text[i + 1] === '"') {value += '"'; i++;}
      else if (ch === '"') {quoted = false; closed = true;}
      else value += ch;
    } else if (ch === ',' ) field();
    else if (ch === '\n' || ch === '\r') {if (ch === '\r' && text[i + 1] === '\n') i++; row();}
    else if (ch === '"') {
      if (value !== '' || closed) throw new Error('CSV 引號格式有誤。');
      quoted = true;
    } else {if (closed) throw new Error('CSV 引號結束後須接逗號或換行。'); value += ch;}
    if (records.length > 1001) throw new Error('最多支援 1000 列彙總數據。');
  }
  if (quoted) throw new Error('CSV 有未結束的引號。');
  if (value !== '' || record.length || closed) row();
  if (records.length < 2) throw new Error('CSV 需要標題與資料。');
  const header = records.shift().map(v => v.trim());
  if (new Set(header).size !== header.length) throw new Error('CSV 欄位名稱不可重複。');
  const missing = columns.filter(c => !header.includes(c));
  if (missing.length) throw new Error(`缺少欄位：${missing.join(', ')}`);
  return records.map((values, i) => {
    if (values.length !== header.length) throw new Error(`第 ${i + 2} 列欄位數不符。`);
    return Object.fromEntries(columns.map(c => [c, values[header.indexOf(c)]]));
  });
}

export function validateRows(input) {
  if (!input.length || input.length > 1000) throw new Error('請提供 1–1000 列彙總數據。');
  const rows = input.map(row => {
    const out = {};
    for (const key of ['scenario', 'model', 'group']) {
      if (row[key] == null) throw new Error(`${key} 不可為空。`);
      out[key] = String(row[key]).trim();
      if (!out[key].length || out[key].length > 80) throw new Error(`${key} 須為 1–80 字元。`);
    }
    for (const key of ['auroc', 'tpr', 'tnr', 'n']) {
      const raw = row[key];
      if (raw == null || String(raw).trim() === '' || !Number.isFinite(Number(raw))) throw new Error(`${key} 須為有限數字。`);
      out[key] = Number(raw);
    }
    if (['auroc','tpr','tnr'].some(key => out[key] < 0 || out[key] > 1)) throw new Error('AUROC、TPR、TNR 必須介於 0 與 1。');
    if (!Number.isSafeInteger(out.n) || out.n <= 0) throw new Error('n 須為正整數。');
    return out;
  });
  const keys = rows.map(r => JSON.stringify([r.scenario, r.model, r.group]));
  if (new Set(keys).size !== keys.length) throw new Error('同一情境、模型與群體不可重複。');
  for (const scenario of new Set(rows.map(r => r.scenario))) {
    const part = rows.filter(r => r.scenario === scenario);
    if (new Set(part.map(r=>r.model)).size !== 2 || part.some(r=>!models.includes(r.model))) throw new Error('每個情境須同時包含 Baseline 與 Fairness-aware。');
    const a = part.filter(r=>r.model===models[0]);
    const b = part.filter(r=>r.model===models[1]);
    if (a.length < 2 || a.length > 12 || a.length !== b.length || a.some(r=>!b.some(s=>s.group===r.group))) throw new Error('兩模型須有相同的 2–12 個群體。');
    if (a.some(r=>b.find(s=>s.group===r.group).n!==r.n)) throw new Error('同群體的兩模型 n 必須相同。');
  }
  return rows;
}

export function summarize(rows) {
  const gap = values => Math.max(...values) - Math.min(...values);
  return models.map(model => {
    const part = rows.filter(r=>r.model === model);
    return {model, auroc:part.reduce((sum,r)=>sum+r.auroc,0)/part.length,
      eopp:gap(part.map(r=>r.tpr)), ebacc:gap(part.map(r=>(r.tpr+r.tnr)/2))};
  });
}

const NS='http://www.w3.org/2000/svg';
function svgNode(name, attributes={}, text) {
  const node=document.createElementNS(NS,name);
  for(const [key,value] of Object.entries(attributes)) node.setAttribute(key,String(value));
  if(text!==undefined) node.textContent=text;
  return node;
}
function barChart(container, labels, values, maximum, title) {
  const width=560,height=310,left=44,right=14,top=24,bottom=44;
  const innerW=width-left-right,innerH=height-top-bottom;
  const svg=svgNode('svg',{viewBox:`0 0 ${width} ${height}`,role:'img','aria-label':title});
  svg.append(svgNode('title',{},title));
  for(let i=0;i<=4;i++) {
    const y=top+innerH*(1-i/4);
    svg.append(svgNode('line',{x1:left,x2:width-right,y1:y,y2:y,stroke:'#e8ece2','stroke-width':1}));
    svg.append(svgNode('text',{x:left-9,y:y+4,'text-anchor':'end',class:'tick-label'},(maximum*i/4).toFixed(maximum===1?2:3).replace(/0+$/,'').replace(/\.$/,'')));
  }
  const step=innerW/labels.length,barW=Math.min(46,step*.27);
  labels.forEach((label,index)=> {
    const center=left+step*(index+.5);
    const shortened=label.length>18?`${label.slice(0,16)}…`:label;
    const tick=svgNode('text',{x:center,y:height-17,'text-anchor':'middle'},shortened);
    tick.append(svgNode('title',{},label)); svg.append(tick);
    for(let m=0;m<2;m++) {
      const number=values[m][index],h=number/maximum*innerH;
      const x=center+(m===0?-barW-3:3),y=top+innerH-h;
      const rect=svgNode('rect',{x,y,width:barW,height:Math.max(h,.6),fill:m===0?'#cbd2c0':'#315b49',rx:1,tabindex:0,'aria-label':`${models[m]}，${label}：${number.toFixed(3)}`});
      rect.append(svgNode('title',{},`${models[m]} · ${label}：${number.toFixed(3)}`));
      svg.append(rect);
      if(labels.length<=4) svg.append(svgNode('text',{x:x+barW/2,y:Math.max(13,y-7),'text-anchor':'middle',class:'value-label'},number.toFixed(3)));
    }
  });
  // More groups keep readable bar widths and allow horizontal scrolling.
  if(labels.length>4) {svg.style.minWidth=`${labels.length*105}px`;container.style.overflowX='auto';}
  else container.style.overflowX='visible';
  container.replaceChildren(svg);
}
function tableContent(table, headers, rows) {
  table.querySelectorAll('thead,tbody').forEach(node=>node.remove());
  const head=document.createElement('thead'),headRow=document.createElement('tr');
  for(const header of headers) {const th=document.createElement('th');th.scope='col';th.textContent=header;headRow.append(th);}
  head.append(headRow); const body=document.createElement('tbody');
  for(const row of rows) {const tr=document.createElement('tr');for(const value of row){const td=document.createElement('td');td.textContent=String(value);tr.append(td);}body.append(tr);}
  table.append(head,body);
}

async function initialize() {
  const $=id=>document.getElementById(id);
  let frame=[],demo=[],source='合成示範數據';
  const navigate=()=> {
    const selected=['overview','results','methods'].includes(location.hash.slice(1))?location.hash.slice(1):'overview';
    document.querySelectorAll('.page-section').forEach(section=>section.hidden=section.id!==selected);
    document.querySelectorAll('.page-nav a').forEach(link=>{if(link.hash===`#${selected}`)link.setAttribute('aria-current','page');else link.removeAttribute('aria-current');});
  };
  window.addEventListener('hashchange',navigate);navigate();
  function updateScenarios() {
    $('scenario').replaceChildren(...[...new Set(frame.map(r=>r.scenario))].map(s=>{const o=document.createElement('option');o.value=s;o.textContent=s;return o;}));
  }
  function render() {
    const part=frame.filter(r=>r.scenario===$('scenario').value);
    const [baseline,aware]=summarize(part);
    const delta=(baseline.eopp-aware.eopp)*100;
    // Only computed, finite numbers enter this fixed markup; CSV text uses textContent.
    $('summary-kpis').innerHTML=`<div class="summary-card"><div class="summary-label">群體 AUROC 平均</div><div class="summary-value">${aware.auroc.toFixed(3)}<span>Fairness-aware</span></div><div class="summary-meta">Baseline ${baseline.auroc.toFixed(3)} · 非 pooled AUROC</div></div><div class="summary-card"><div class="summary-label">EOpp gap · 越低越好</div><div class="summary-value">${aware.eopp.toFixed(3)}<span>← ${baseline.eopp.toFixed(3)}</span></div><div class="summary-meta">召回率的群體間落差</div></div><div class="summary-card"><div class="summary-label">EOpp gap 縮減</div><div class="summary-value">${delta>=0?'+':''}${delta.toFixed(1)}<span>個百分點</span></div><div class="summary-meta">觀察值變化，未執行統計顯著性檢定</div></div>`;
    const metric=document.querySelector('input[name=metric]:checked').value;
    const title={auroc:'AUROC',tpr:'Recall / TPR',tnr:'Specificity / TNR'}[metric];
    $('performance-title').textContent=`群體效能比較 · ${title}`;
    const labels=part.filter(r=>r.model===models[0]).map(r=>r.group).sort();
    const values=models.map(m=>labels.map(g=>part.find(r=>r.model===m&&r.group===g)[metric]));
    barChart($('performance-chart'),labels,values,1,`${source}，${title}，各群體模型比較`);
    const upper=Math.min(1,Math.max(.1,Math.ceil(Math.max(baseline.eopp,aware.eopp,baseline.ebacc,aware.ebacc)*1.3*20)/20));
    barChart($('fairness-chart'),['EOpp gap','EBAcc gap'],[[baseline.eopp,baseline.ebacc],[aware.eopp,aware.ebacc]],upper,`${source}，EOpp 與 EBAcc 群體落差，越低越好`);
    document.querySelectorAll('.chart-source').forEach(el=>el.textContent=source==='合成示範數據'?source:'使用者匯入 · 未驗證');
    $('metric-note').replaceChildren();
    const note=document.createElement('p');note.textContent=`數據來源：${source} · EOpp gap 變化：${delta>=0?'+':''}${delta.toFixed(1)} 個百分點（正值表示縮小）。`;
    const limitation=document.createElement('p');limitation.textContent='AUROC 為群體算術平均，並非整體 pooled AUROC。此面板未執行統計顯著性檢定；差距縮小不等同已證明消除偏差。';
    $('metric-note').append(note,limitation);
    tableContent($('summary-table'),['模型','群體 AUROC 平均','EOpp gap','EBAcc gap'],[baseline,aware].map(r=>[r.model,r.auroc.toFixed(4),r.eopp.toFixed(4),r.ebacc.toFixed(4)]));
    tableContent($('data-table'),columns,part.map(r=>columns.map(c=>r[c])));
  }
  $('scenario').addEventListener('change',render);
  document.querySelectorAll('input[name=metric]').forEach(el=>el.addEventListener('change',render));
  const setStatus=(message,error=false)=>{$('import-status').textContent=message;$('import-status').classList.toggle('error',error);};
  $('import-button').addEventListener('click',async()=> {
    const file=$('csv-file').files[0];
    if(!file){setStatus('請先選擇 CSV。',true);return;}
    if(file.size>1_000_000){setStatus('檔案不可超過 1 MB。',true);return;}
    $('import-button').disabled=true;
    try {
      const rows=validateRows(parseCSV(new TextDecoder('utf-8',{fatal:true}).decode(await file.arrayBuffer())));
      frame=rows;source='使用者匯入彙總數據（未經本專案驗證）';
      document.querySelector('input[name=metric][value=auroc]').checked=true;
      updateScenarios();render();setStatus('已載入；這些數據的來源與真實性須由提供者確認。');
    } catch(error){setStatus(`CSV 格式有誤：${error.message}`,true);}
    finally{$('import-button').disabled=false;}
  });
  $('reset-button').addEventListener('click',()=> {
    frame=demo;source='合成示範數據';$('csv-file').value='';
    document.querySelector('input[name=metric][value=auroc]').checked=true;
    updateScenarios();render();setStatus('已還原合成示範。');
  });
  try {
    const response=await fetch('./data/demo_metrics.csv');
    if(!response.ok) throw new Error('示範數據無法讀取。');
    demo=validateRows(parseCSV(await response.text()));frame=demo;updateScenarios();render();
  } catch(error){$('metric-note').textContent=`無法載入示範資料：${error.message}`;}
}
if(typeof document!=='undefined') initialize();
