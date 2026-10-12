/* Interactive views of frozen measurements. Controls never run or simulate a model. */
(()=>{
'use strict';
const roots=[...document.querySelectorAll('[data-chart]')];
const colors=['#246b70','#9c542e','#6d5b95','#a27b28','#5174a8','#817b73','#ad4c70','#34845e','#6a8692','#ab7e6c'];
const names={concepts:'Concepts + memory + planning',procedural:'Equal-information procedural',answer_only:'Answer only',no_memory:'Without memory',no_planning:'Without planning',model_only:'Model only',structured:'Structured',mindscape_b:'Mindscape B',mindscape_c:'Mindscape C',plain:'Plain Qwen',typed:'Typed tools',mindscape:'Mindscape',no_concepts:'Without concepts',word_memory:'Word-overlap memory',no_history:'Without history',no_relationships:'Without relationships',no_feedback:'Shuffled supervision',persistence:'Persistence',constant_velocity:'Constant velocity',analytical_available:'Analytical available'};
const fmt=n=>Math.abs(n)>=10000?n.toExponential(2):Number(n.toFixed(2)).toLocaleString();
function el(tag,text){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;return e;}
function svg(tag,attrs,text){const e=document.createElementNS('http://www.w3.org/2000/svg',tag);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));if(text!==undefined)e.textContent=text;return e;}
function wilson(k,n){const z=1.95996398454,p=k/n,d=1+z*z/n,c=(p+z*z/(2*n))/d,h=z*Math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d;return [(c-h)*100,(c+h)*100];}
function chart(root,series,{max=100,unit='%',log=false,xLabels=null,selected=null,target=null}={}){
 const box=root.querySelector('.chart-drawing');box.replaceChildren();
 const W=900,H=350,L=xLabels?65:195,R=35,T=32,B=55;
 const g=svg('svg',{viewBox:`0 0 ${W} ${H}`,role:'img','aria-label':root.querySelector('h3').textContent});
 const desc=svg('desc',{},'Recorded measurements. The exact values are available in the table below.');g.append(desc);
 const plotW=W-L-R,plotH=H-T-B;
 const scale=v=>log?Math.log10(Math.max(v,1))/Math.log10(Math.max(max,10)):v/max;
 if(xLabels){
  for(let i=0;i<=4;i++){const v=max*i/4,y=T+plotH*(1-i/4);g.append(svg('line',{x1:L,x2:W-R,y1:y,y2:y,stroke:'#e6e7e8'}),svg('text',{x:L-12,y:y+4,'text-anchor':'end',class:'axis-label'},fmt(v)));}
  const x=i=>L+i*plotW/(xLabels.length-1),y=v=>T+plotH*(1-scale(v));
  if(target!==null){g.append(svg('line',{x1:L,x2:W-R,y1:y(target),y2:y(target),stroke:'#999','stroke-dasharray':'5 5'}));g.append(svg('text',{x:W-R,y:y(target)-8,'text-anchor':'end',class:'axis-label'},'50% research target'));}
  xLabels.forEach((v,i)=>g.append(svg('text',{x:x(i),y:H-20,'text-anchor':'middle',class:'axis-label'},String(v))));
  if(selected!==null)g.append(svg('line',{x1:x(selected),x2:x(selected),y1:T,y2:H-B,stroke:'#222','stroke-dasharray':'3 5'}));
  series.forEach((s,j)=>{
   g.append(svg('path',{d:s.values.map((v,i)=>(i?'L':'M')+x(i)+','+y(v)).join(' '),fill:'none',stroke:colors[j], 'stroke-width':2.5}));
   s.values.forEach((v,i)=>{const c=svg('circle',{cx:x(i),cy:y(v),r:i===selected?6:3.5,fill:colors[j],stroke:'#fff','stroke-width':1.5});c.append(svg('title',{},`${s.label}: ${xLabels[i]} → ${fmt(v)} ${unit}`));g.append(c);});
  });
 }else{
  const ticks=log?[1,10,100,1000,10000,100000,1000000,10000000,100000000].filter(v=>v<=max):[0,max*.25,max*.5,max*.75,max];
  ticks.forEach(v=>{const x=L+scale(v)*plotW;g.append(svg('line',{x1:x,x2:x,y1:T,y2:H-B,stroke:'#e6e7e8'}),svg('text',{x,y:H-22,'text-anchor':'middle',class:'axis-label'},fmt(v)));});
  series.forEach((s,j)=>{const row=plotH/series.length,y=T+j*row;g.append(svg('text',{x:L-12,y:y+row*.58,'text-anchor':'end',class:'bar-label'},s.label));const bar=svg('rect',{x:L,y:y+row*.16,width:Math.max(1,scale(s.value)*plotW),height:row*.62,rx:3,fill:colors[j%colors.length],class:'metric-bar'});bar.append(svg('title',{},`${s.label}: ${fmt(s.value)} ${unit}`));g.append(bar);if(s.ci){const cy=y+row*.47,x1=L+scale(s.ci[0])*plotW,x2=L+scale(s.ci[1])*plotW;g.append(svg('line',{x1,x2,y1:cy,y2:cy,stroke:'#222','stroke-width':1.5}));for(const x of [x1,x2])g.append(svg('line',{x1:x,x2:x,y1:cy-4,y2:cy+4,stroke:'#222'}));}});
 }
 g.append(svg('text',{x:L,y:15,class:'axis-label'},unit));box.append(g);
 if(xLabels){const legend=el('div');legend.className='chart-legend';series.forEach((s,j)=>{const item=el('span',s.label);item.style.setProperty('--series-color',colors[j]);legend.append(item)});box.append(legend);}
}
function values(root,headers,rows,source){const box=root.querySelector('.chart-table');box.replaceChildren();const table=el('table'),head=el('thead'),tr=el('tr');headers.forEach(x=>{const th=el('th',x);th.scope='col';tr.append(th)});head.append(tr);table.append(head);const body=el('tbody');rows.forEach(row=>{const tr=el('tr');row.forEach(x=>tr.append(el('td',String(x))));body.append(tr)});table.append(body);const link=el('a','Source measurements ↗');link.href=source;box.append(table,link);}
function render(root,data){
 const kind=root.dataset.chart,get=n=>root.querySelector(`[data-control="${n}"]`).value;
 const reading=root.querySelector('.chart-reading'),note=root.querySelector('.chart-note');
 if(kind==='math'){
  const budgets=[10,25,50,100,250,500,1000],index=Number(get('budget')),budget=budgets[index],model=get('model'),family=get('family');
  const rows=data.math.filter(r=>r.model===model&&r.family===family);
  const conditions=[...new Set(rows.map(r=>r.condition))];
  const series=conditions.map(c=>({label:names[c]||c,values:budgets.map(b=>rows.find(r=>r.condition===c&&r.budget===b).mean*100)}));
  root.querySelector('[data-value="budget"]').textContent=budget.toLocaleString();root.querySelector('[data-control="budget"]').setAttribute('aria-valuetext',budget+' distinct training examples');
  chart(root,series,{xLabels:budgets,selected:index,max:100,unit:'Exact structural-OOD accuracy (%)',target:family==='length'?50:null});
  const chosen=rows.filter(r=>r.budget===budget);reading.textContent=`At ${budget.toLocaleString()} examples: ${chosen.map(r=>(names[r.condition]||r.condition)+' '+fmt(r.mean*100)+'%').join(' · ')}.`;
  note.textContent='Recorded budgets only; connecting lines guide the eye and do not estimate unmeasured budgets. Three-seed means; the table shows seed sample SD, not a confidence interval. The predeclared 50% unseen-length target was not reached.';
  values(root,['Condition','Examples','Accuracy','Seed SD'],chosen.map(r=>[names[r.condition]||r.condition,r.budget,fmt(r.mean*100)+'%',fmt(r.seed_sample_sd*100)+' points']),data.sources.math);
 }else if(kind==='physics'){
  const row=data.physics.find(r=>r.family===get('family')&&r.panel===get('panel')&&r.seed===get('seed')),index=Number(get('horizon')),h=[8,16,32][index];
  const max=Math.max(...row.candidate,...row.matched)*1.2;
  chart(root,[{label:'V3.1 candidate',values:row.candidate},{label:'Matched neural baseline',values:row.matched}],{xLabels:[8,16,32],selected:index,max,unit:'Rollout error (fixed unit scales)'});
  root.querySelector('[data-value="horizon"]').textContent=h+' steps';root.querySelector('[data-control="horizon"]').setAttribute('aria-valuetext',h+' steps');
  const improvement=(1-row.candidate[index]/row.matched[index])*100;
  reading.textContent=`${h} steps · candidate ${fmt(row.candidate[index])}, matched ${fmt(row.matched[index])}. Candidate ${improvement>=0?'improvement':'worsening'}: ${fmt(Math.abs(improvement))}%.`;
  note.textContent=`Development evidence only: ${get('panel')==='iid'?'six':'seven'} independent scenes in this family/panel. Lines connect measured horizons, not intermediate predictions. Error scales differ from V3. The pilot failed improvement and calibration gates.`;
  values(root,['Horizon','Candidate','Matched'],[8,16,32].map((v,i)=>[v,row.candidate[i],row.matched[i]]),data.sources.physics);
 }else if(kind==='coding'){
  const historic=get('study')==='historical',split=get('split');
  const rows=historic?data.historical_coding.filter(r=>r.split===(split==='iid'?'test':'ood_test')).map(r=>({label:names[r.condition],k:r.successes,n:r.episodes,ci:r.wilson_ci95.map(v=>v*100)})):data.coding.map(r=>({label:names[r.condition],k:r[split][0],n:r[split][1],ci:wilson(...r[split])}));
  chart(root,rows.map(r=>({...r,value:r.k/r.n*100})),{max:100,unit:'Task success (%) · 95% Wilson intervals'});
  reading.textContent=historic?'Historical lockbox: 50 independent tasks per split and condition.':'V3 panel: '+(split==='ood'?'12 structural-OOD':'6 IID')+' tasks per condition, evaluator seed 11.';
  note.textContent=historic?'Conditions differ in supervision and interactions. This is not a causal architecture comparison or a comparison against the separate V3 task panel.':'Fresh V3 tasks are different from the historical lockbox. OOD Mindscape solves 8/12; no-concepts solves 9/12. Seed-11 cells shown; cached deterministic Qwen outputs are not independent model samples.';
  values(root,['Condition','Successes','Accuracy','95% interval'],rows.map(r=>[r.label,`${r.k}/${r.n}`,fmt(r.k/r.n*100)+'%',r.ci.map(fmt).join('–')+'%']),historic?data.sources.historical:data.sources.coding);
 }else if(kind==='latency'){
  const stat=get('stat'),rows=data.latency.map(r=>({label:names[r.condition],value:r[stat]}));chart(root,rows,{max:50,unit:'Seconds per executed task'});
  reading.textContent=(stat==='p50'?'Median':'95th percentile')+' latency: '+rows.map(r=>r.label+' '+fmt(r.value)+' s').join(' · ')+'.';
  note.textContent='Historical dedicated sequential study: MPS float16, batch 1, caching disabled, four samples per condition. p95 is descriptive and unstable at this sample size; these are not current V3 latency benchmarks.';
  values(root,['Condition','Samples',stat==='p50'?'p50 seconds':'p95 seconds'],data.latency.map(r=>[names[r.condition],r.n,fmt(r[stat])]),data.sources.historical);
 }else if(kind==='performance'){
  const family=get('family'),log=get('scale')==='log',rows=data.performance.map(r=>({label:names[r.condition]||r.condition,value:r[family]}));const max=log?Math.pow(10,Math.ceil(Math.log10(Math.max(...rows.map(r=>r.value))))):Math.max(...rows.map(r=>r.value))*1.1;
  chart(root,rows,{max,log,unit:'V3 normalized structural-OOD rollout MSE'+(log?' · log10 axis':'')});
  reading.textContent=`${family==='motion'?'Motion':'Interaction'}: Mindscape ${fmt(rows[0].value)}, matched ${fmt(rows[1].value)}. Lower error is better.`;
  note.textContent='Final 250-trajectory budget; scene means after averaging three seeds, 100 independent scenes per neural cell. Ablations and nonneural controls have distinct information limits. Shuffled supervision is not a pure architecture ablation. V3 and V3.1 errors are not directly comparable.';
  values(root,['Condition','OOD rollout MSE'],rows.map(r=>[r.label,r.value]),data.sources.performance);
 }
}
fetch('/assets/v3/interactive-data.json').then(r=>{if(!r.ok)throw Error('Evidence unavailable');return r.json()}).then(data=>{roots.forEach(root=>{root.addEventListener('input',()=>render(root,data));root.addEventListener('change',()=>render(root,data));render(root,data)});const target=roots.find(root=>'#'+root.id===location.hash);if(target)target.scrollIntoView({block:'start',behavior:'instant'});}).catch(()=>roots.forEach(root=>{root.querySelector('.chart-drawing').textContent='Interactive data could not load. The preserved source reports and tables below remain available.'}));
})();
