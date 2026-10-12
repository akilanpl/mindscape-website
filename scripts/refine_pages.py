"""One-time page-specific refinement of the published V3 update."""
import csv,json,re,subprocess
from pathlib import Path
D=Path('dist')
def remove_section(s,identifier='current-research'):
 m=re.search(r'<section\b[^>]*id="'+identifier+r'"[^>]*>',s)
 if not m:return s
 depth=0
 for t in re.finditer(r'</?section\b[^>]*>',s[m.start():]):
  depth+=-1 if t[0].startswith('</') else 1
  if depth==0:return s[:m.start()]+s[m.start()+t.end():]
 raise ValueError('Unclosed section')
def replace_section(s,identifier,body):
 m=re.search(r'<section\b[^>]*id="'+identifier+r'"[^>]*>',s)
 old=remove_section(s,identifier)
 return old[:m.start()]+body+old[m.start():]
def graph(kind,title,description,controls):
 return f'<section class="evidence-explorer" data-chart="{kind}" id="graph-{kind}"><div class="explorer-heading"><p class="explorer-kicker">Explore the evidence</p><h3>{title}</h3><p>{description}</p></div><div class="chart-controls">{controls}</div><div class="chart-drawing" aria-label="{title}"><p>Loading recorded measurements…</p></div><p class="chart-reading" role="status" aria-live="polite"></p><p class="chart-note"></p><details class="chart-values"><summary>View the values and source</summary><div class="chart-table"></div></details><noscript><p>Interactive charts require JavaScript. All source measurements remain in the <a href="/assets/v3/interactive-data.json">chart data download</a> and linked reports.</p></noscript></section>'
def select(key,label,options):
 return '<label>'+label+'<select data-control="'+key+'">'+''.join(f'<option value="{v}">{t}</option>' for v,t in options)+'</select></label>'
# Restore the home exactly, then add the small footer link requested.
s=subprocess.check_output(['git','show','b9cd5e6:dist/index.html'],text=True)
s=s.replace('<a href="contact/">Let’s explore together ↗</a>','<div class="launch-footer-links"><a href="advancements/#current-research">Research Update . 12 OCTOBER 2026</a><a href="contact/">Let’s explore together ↗</a></div>')
s=s.replace('</head>','<link rel="stylesheet" href="/page-refinements.css"></head>');(D/'index.html').write_text(s)
# Remove full-width update blocks from the requested editorial pages.
for route in ['about','research','research/reports','architecture']:
 p=D/route/'index.html';p.write_text(remove_section(p.read_text()))
for route in ['research/library','research/index']:
 p=D/route/'index.html';s=p.read_text();s=re.sub(r'<p class="v3-boundary">.*?</p>','',s,flags=re.S);p.write_text(s)
# About: use the original domain tabs and card styles.
p=D/'about/index.html';s=p.read_text().replace('Historical studies: where the project began','What we study')
s=s.replace('Numeric controls</button>','Numeric controls</button><button id="physics-tab" type="button" role="tab" aria-selected="false" aria-controls="physics-panel" tabindex="-1">Physics</button>',1)
physics='<div id="physics-panel" role="tabpanel" aria-labelledby="physics-tab" class="research-grid" hidden><article class="research-card"><div class="card-art code-art"><span>19,200</span><small>recorded forecasts</small></div><h3>Learning physical transitions</h3><p>V3 studied simulated motion and object interactions across three seeds and five training budgets. All forecasts and 2,160 selected-action episodes passed independent verification.</p></article><article class="research-card"><div class="card-art split-art"><span>32<small>step development rollouts</small></span></div><h3>Progress on finite-rollout stability</h3><p>The V3.1 object-centric candidate and matched model avoided the catastrophic divergence seen in V3. Both met finite-output and error-growth gates through 32 steps.</p></article><article class="research-card"><div class="card-art replay-art"><span>NO-GO</span><small>for scaling the candidate</small></div><h3>Better stability, unresolved advantage</h3><p>The candidate failed improvement and calibration gates. Stable execution is progress, but a reproducible advantage over the matched model remains unproven. <a href="../advancements/#graph-physics">Explore the physics results ↗</a></p></article></div>'
s=s.replace('<p class="evidence-context">',physics+'<p class="evidence-context">',1)
s=s.replace('Observed results from the preserved research package. Conditions differ in supervision and interactions; an architecture-only advantage is not established.','Coding and numeric-control tabs show preserved V1/V2 studies; Physics covers V3 and the V3.1 development pilot. Their metrics and protocols differ. Replay agreement and task success are separate measurements.')
s=re.sub(r'(<h2 id="next-title">).*?(</section>)',r'\1What remains scientifically unresolved</h2><p>V3 now connects mathematics, Python repair and simulated physics through a common, independently verified runtime. The open question is how explicit concepts improve learning and generalization under fair comparisons.</p><p>Mathematical learning missed its structural-length target and still produces inconsistent local claims. Coding reached 8/12 structural OOD repairs, but the no-concepts reference reached 9/12. Physics V3.1 improved finite-rollout stability while failing matched-improvement and calibration gates.</p><p>The next work is focused diagnosis: mathematical consistency, the contribution of concepts and memory, and physical prediction calibration. Reliable long-horizon dynamics and learned transfer between domains remain open research questions.</p>\2',s,flags=re.S)
p.write_text(s)
# Research overview: a peer physics topic, styled exactly like the existing topics.
p=D/'research/index.html';s=p.read_text()
physics='<section class="focus-area" id="physics"><h2>Physics</h2><p class="area-summary">Learning how objects move and interact from observed states and actions. V3 exposed severe long-horizon errors; the V3.1 pilot improves finite-rollout stability but does not yet demonstrate a reliable advantage over the matched neural baseline.</p><div class="focus-grid">'
for art,title,desc,url in [('orbit','Physical world models','The complete simulated study: motion, interactions, planning and independently verified negative findings.','v3-physics.md'),('wave','Stability and generalization','Object-centric states, pairwise interactions and multi-step supervision, evaluated at 8, 16 and 32 steps.','v3-physics-architecture.md'),('trace','Pilot findings and limits','Inspect the original gates, per-seed results, calibration failures and the NO-GO decision.','v3-1-physics.md')]:
 physics+=f'<a class="focus-card" href="../assets/v3/{url}"><div class="abstract-art {art}" aria-hidden="true"><span></span></div><h3>{title} ↗</h3><p>{desc}</p></a>'
physics+='</div></section>'
s=s.replace('<section class="focus-area"><h2>Verification',physics+'<section class="focus-area"><h2>Verification',1);p.write_text(s)
# Reports: third peer data card, no large update section.
p=D/'research/reports/index.html';s=p.read_text();needle='<section class="reports-section"><h2>Research highlights</h2>'
prior=s.index(needle);end=s.rfind('</div></section>',0,prior)
card='<a class="data-card" href="../../advancements/#graph-physics"><div class="data-art physics"><span aria-hidden="true">↗</span></div><h3>Physical dynamics</h3><p>Explore 8-, 16- and 32-step predictions, matched models and per-seed development results. See where stability improves and where the pilot fails.</p><span class="text-link">Explore the interactive graph ↗</span></a>'
s=s[:end]+card+s[end:];p.write_text(s)
# Architecture: evolve original sections rather than a separate announcement column.
p=D/'architecture/index.html';s=p.read_text()
s=s.replace('The historical V1/V2 configuration had two backends with different mechanisms. Numeric tasks use a small trained MLP; coding tasks use pinned Qwen2.5-Coder-1.5B weights and adapters. Their controllers, representations, and tools must be understood separately.','V3 connects three specialists through a shared typed kernel: neural mathematical transitions, Qwen-based Python repair and object-centric physical dynamics. Each domain keeps its own representation, learned model, executor and independent scorer. A shared interface does not by itself imply shared learned knowledge.')
s=s.replace('href="../assets/reports/final_architecture.pdf">Architecture document','href="../assets/v3/v3-architecture.md">Current architecture')
methods='<section id="methods"><h2>Methods</h2><h3>One cognitive cycle. Three domain specialists.</h3><p>The kernel follows OBSERVE → REPRESENT → PROPOSE → PREDICT → ACT → VERIFY → UPDATE. Typed observations and goals enter the system; predictions describe hypothetical transitions; independent execution records actual outcomes. Evaluation episodes do not update training memory or model weights.</p><div class="methods-diagram" role="img" aria-label="Observe and represent; propose and predict; execute, verify and update.">'
for number,title,symbol,desc,tag in [('1','Observe and represent','{ }','Build typed state, entities and relationships from permitted observations.','Input → representation'),('2','Propose and predict','↗','The domain specialist proposes actions and predicts their consequences.','Neural proposal → hypothesis'),('3','Act, verify and update','✓','Execute the selected action, independently judge the result and record the experience.','Actual transition → verification')]:
 methods+=f'<div class="method-step"><span class="step-number">Step {number}</span><h3>{title}</h3><div class="diagram-symbol" aria-hidden="true">{symbol}</div><p>{desc}</p><span class="method-tag">{tag}</span></div>'
methods+='</div><h3>Mathematics</h3><p>A compact learned model predicts local operations, numerical claims, carry/borrow quantities and next-state values. Declared digit/sign scheduling composes the claims. The executor writes those values without arithmetic correction; an independent arithmetic verifier scores the completed result. Both preserved integration examples fail because of incorrect neural claims.</p><h3>Python debugging</h3><p>Pinned Qwen2.5-Coder-1.5B receives visible code, contracts, static relationships and approved training experiences. A learned evaluator ranks repair proposals using estimated usefulness and cost. Trusted tools apply validated edits; generated code runs in WASI. Private terminal tests remain outside generation and memory updates.</p><h3>Physical dynamics</h3><p>The V3.1 candidate uses object-centric states, permutation-consistent pairwise interactions and multi-step supervision. A bounded planner scores action candidates with the learned model, then the simulator executes the selected action. Hidden simulator parameters and future states are excluded from model observations. Finite-rollout stability improved, while the matched-improvement and calibration gates failed.</p><h3>Memory, routing and measured outcomes</h3><p>Persistent experiences are restricted to approved training evidence. Hypothetical plans remain separate from verified outcomes. Mathematics and physics macro routing submits specialist proposals deterministically; it does not choose semantic answers for the learner. The shared runtime does not pool learned knowledge between domains.</p><p>Four recorded requests agree between direct specialists and the kernel: mathematics 0/2, coding 1/1, physics 1/1. These are integration demonstrations, not domain accuracy estimates. <a href="../assets/v3/v3-integration.md">Read the integration report ↗</a></p><div class="inline-actions"><a class="text-link" href="../assets/v3/v3-coding-architecture.md">Coding architecture ↗</a><a class="text-link" href="../assets/v3/v3-physics-architecture.md">Physics architecture ↗</a><a class="text-link" href="../advancements/">Measured findings ↗</a></div></section>'
s=replace_section(s,'methods',methods)
s=s.replace('<h2>Recorded diagnostics</h2>','<h2>Preserved coding diagnostics</h2>')
s=s.replace('One real coding task, shown two ways.','Historical V1/V2 instrumentation: one real coding task, shown two ways.')
s=s.replace('Further work remains: independent cross-domain and training-pipeline replication, broader adapter coverage, selected hidden activations, matched historical-model comparisons with approved access, and more precise confirmatory measurement.','Current studies retain these controls and add information-matched mathematical comparisons, coding component ablations, and physics stability/calibration gates. Explicit concepts have not established the intended advantage. The next work should test specific failure hypotheses on fresh development evidence before scaling.')
s=s.replace('<h2>Research record</h2><p>Mindscape · Snapshot 10 October 2026</p>','<h2>Research record</h2><p>Architecture updated 12 October 2026. Historical diagnostics retain their 10 October snapshot.</p>')
s=s.replace('This is a preserved research snapshot. The historical V2 research remained incomplete; current V3 findings are shown below.','Current V3 architecture with preserved V1/V2 diagnostic examples.')
p.write_text(s)
# Interactive graph mounts. All sliders select recorded points, never fabricate experiments.
math=graph('math','How does learning change with more examples?','Move through the seven recorded training budgets and compare learned systems. Each point is a three-seed mean.',select('model','Backbone',[('Compact neural','Compact neural'),('MiniLM residual adapter','MiniLM residual adapter')])+select('family','Evaluation family',[(v,t) for v,t in [('all','All structural OOD'),('length','Unseen length'),('carry_chain','Carry chains'),('digit_composition','Digit composition'),('sign_change','Sign changes'),('composition','Rule composition')]])+'<label class="range-control">Training examples <output data-value="budget">1,000</output><input data-control="budget" type="range" min="0" max="6" step="1" value="6" aria-label="Training example budget"></label>')
physics=graph('physics','How do errors grow over time?','Compare the V3.1 candidate with its matched baseline at each measured horizon. Change family, development panel and seed to inspect consistency.',select('family','Physics family',[('motion','Motion'),('interaction','Interaction')])+select('panel','Development panel',[('stress','Structural stress'),('iid','IID')])+select('seed','Training seed',[('11','11'),('23','23')])+'<label class="range-control">Rollout horizon <output data-value="horizon">32 steps</output><input data-control="horizon" type="range" min="0" max="2" step="1" value="2" aria-label="Rollout horizon"></label>')
coding=graph('coding','Which repairs generalize?','Switch between the historical lockbox and the fresh V3 panel. Each view keeps its own tasks and uncertainty.',select('study','Study',[('v3','V3 fresh panel'),('historical','V1 frozen lockbox')])+select('split','Evaluation split',[('ood','Structural OOD'),('iid','IID')]))
latency=graph('latency','What does an executed repair cost?','Inspect the dedicated historical MPS latency measurements. Four fresh samples per condition; timing includes different tool and interaction paths.',select('stat','Latency statistic',[('p50','Median / p50'),('p95','95th percentile / p95')]))
performance=graph('performance','Where does the physics model break down?','Compare V3 final-budget structural OOD error across mechanisms and controls. Use the logarithmic scale to see small baselines alongside divergent models.',select('family','Physics family',[('motion','Motion'),('interaction','Interaction')])+select('scale','Error scale',[('log','Logarithmic'),('linear','Linear')]))
p=D/'advancements/index.html';s=p.read_text();s=re.sub(r'<h3>Mathematical learning curves</h3><figure>.*?</figure>',math,s,count=1,flags=re.S)
s=s.replace('<h3>Physics stability and calibration gates</h3>',physics+'<h3>Physics stability and calibration gates</h3>',1)
s=s.replace('<h3>The integration demonstration</h3>',coding+performance+'<h3>The integration demonstration</h3>',1)
s=re.sub(r'<figure[^>]*>\s*<img[^>]*07-dedicated-latency[^>]*>.*?</figure>',latency,s,count=1,flags=re.S)
if 'data-chart="latency"' not in s:s=s.replace('<section id="latency" class="article-section">','<section id="latency" class="article-section">'+latency,1)
s=s.replace('</body>','<script src="/evidence-explorers.js"></script></body>');p.write_text(s)
for route in ['','about','research','research/reports','advancements','architecture','research/library','research/index']:
 p=D/route/'index.html';s=p.read_text()
 if 'page-refinements.css' not in s:s=s.replace('</head>','<link rel="stylesheet" href="/page-refinements.css"></head>')
 p.write_text(s)
# Parse chart data from preserved scientific reports, not manually invented values.
mathrows=list(csv.DictReader((D/'assets/v3/learning-curves.csv').open()))
for row in mathrows:
 for k in ['budget','seeds']:row[k]=int(row[k])
 for k in ['mean','seed_sample_sd']:row[k]=float(row[k])
physicsrows=[]
for line in (D/'assets/v3/v3-1-physics.md').read_text().splitlines():
 parts=[p.strip() for p in line.strip('|').split('|')]
 if len(parts)==6 and parts[0] in ['motion','interaction'] and parts[1] in ['11','23']:
  vals=[list(map(float,re.findall(r'[\d.]+',x))) for x in parts[3:]]
  physicsrows.append(dict(family=parts[0],seed=parts[1],panel=parts[2],candidate=[v[0] for v in vals],matched=[v[1] for v in vals]))
codingrows=[]
for line in (D/'assets/v3/v3-coding.md').read_text().splitlines():
 parts=[p.strip() for p in line.strip('|').split('|')]
 if len(parts)==7 and parts[0] in ['plain','structured','typed','mindscape','no_memory','no_planning','no_concepts','word_memory']:
  codingrows.append(dict(condition=parts[0],iid=list(map(int,parts[1].split('/'))),ood=list(map(int,parts[2].split('/')))))
perf=[]
for line in (D/'assets/v3/v3-physics.md').read_text().splitlines():
 parts=[p.strip() for p in line.strip('|').split('|')]
 if len(parts)==3 and parts[0] in ['mindscape','matched','no_relationships','no_concepts','no_memory','no_history','no_feedback','persistence','constant_velocity','analytical_available']:
  perf.append(dict(condition=parts[0],motion=float(parts[1]),interaction=float(parts[2])))
historical=json.loads((D/'assets/benchmark-data.json').read_text())['website_evidence']
data=dict(math=mathrows,physics=physicsrows,coding=codingrows,performance=perf,historical_coding=historical['lockbox'],latency=historical['latency'],sources=dict(math='/assets/v3/v3-mathematics.md',physics='/assets/v3/v3-1-physics.md',coding='/assets/v3/v3-coding.md',performance='/assets/v3/v3-physics.md',historical='/assets/benchmark-data.json'))
(D/'assets/v3/interactive-data.json').write_text(json.dumps(data,indent=2)+'\n')
print('Parsed chart rows:',{k:len(v) for k,v in data.items() if isinstance(v,list)})
