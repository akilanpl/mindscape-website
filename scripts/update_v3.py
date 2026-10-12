"""Publish bounded, source-bound V3 evidence without rewriting historical assets."""
import hashlib, html, json, re, shutil
from pathlib import Path

SITE=Path(__file__).resolve().parents[1]
D=SITE/'dist'
RESEARCH=Path('/Users/akilan/Documents/Codex/2026-10-12/you-are-gpt-6-1-sol/work/mindscape-v3')
COMMIT='9ce27a3'
ORIGIN='https://mindscape-website-dusky.vercel.app'
A=D/'assets/v3'; A.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def link(url,label): return f'<a href="{html.escape(url)}">{html.escape(label)} ↗</a>'
def report(file,label): return link('/assets/v3/'+file,label)
def table(headers,rows):
    return '<div class="v3-table-wrap"><table><thead><tr>'+''.join('<th scope="col">'+html.escape(x)+'</th>' for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in row)+'</tr>' for row in rows)+'</tbody></table></div>'
def card(title,body,url,label='Read the evidence'):
    return f'<article class="v3-card"><h3>{title}</h3><p>{body}</p>{link(url,label)}</article>'
def section(title,body,identity='current-research'):
    return f'<section class="v3-section" id="{identity}" aria-labelledby="{identity}-title"><p class="v3-eyebrow">Research update · 12 October 2026</p><h2 id="{identity}-title">{title}</h2>{body}<p class="v3-boundary">Learned cross-domain transfer: <strong>NOT YET ESTABLISHED.</strong></p></section>'

sources=[
('v3-mathematics.md','docs/v3_math/scientific-report.md','Mathematical learning: results and limits','Mathematics','Conclusion','The 50% structural-length target was not reached; finite memory and procedural scaffolding complicate neural-necessity claims.'),
('v3-coding.md','docs/v3_coding/scientific-report.md','Python repair: matched comparisons and failures','Coding','Conclusion','Mindscape solved 8/12 OOD tasks, versus 9/12 without concepts. The superiority gate failed.'),
('v3-physics.md','docs/v3_physics/recovery/scientific-report.md','Physics V3: completed study, failed improvement target','Physics','Conclusion','Independent verification passed; long-horizon motion divergence and the failed 20% improvement target remain negative findings.'),
('v3-1-physics.md','docs/v3_1_physics/diagnostic-review.md','Physics V3.1: stability pilot NO-GO','Physics','Conclusion','Finite 32-step predictions passed stability gates, but matched improvement and calibration gates failed. No scaling authorized by these results.'),
('v3-integration.md','docs/v3_integration/handoff.md','Three-domain runtime: verified integration','Methods','Milestone','Four requests replayed through direct and shared-kernel paths. Math 0/2, coding 1/1, physics 1/1; engineering PASS is not transfer.'),
('v3-architecture.md','docs/v3_integration/README.md','V3 runtime architecture and domain boundaries','Methods','Publication','One typed API, existing specialists, independent executors, training-only memories, and native MPS neural execution.'),
('v3-math-protocol.md','docs/v3_math/protocol.md','Mathematical concept-learning protocol','Mathematics','Publication','Frozen example budgets, structural holdouts and information-matched comparisons.'),
('v3-physics-architecture.md','docs/v3_1_physics/architecture.md','Object-centric dynamics architecture','Physics','Publication','Permutation-consistent interactions, bounded residual dynamics and multi-step supervision; benefits require matched evidence.'),
('v3-physics-commands.md','docs/v3_physics/recovery/commands.md','Physics study reproduction and preserved evidence','Physics','Publication','Historical reproduction commands; completion does not authorize repeating the full study.'),
('v3-coding-architecture.md','docs/v3_coding/architecture.md','Verified Python experience and repair evaluation','Coding','Publication','Contracts, AST relations, approved memories, learned proposal evaluation and terminal WASI scoring.'),
]
records=[]; provenance=[]
for file,path,title,topic,category,description in sources:
    src=RESEARCH/path
    if not src.exists():
        if path.endswith('protocol.md'): src=RESEARCH/'docs/v3_math/experimental-protocol.md'
        if not src.exists(): raise FileNotFoundError(path)
    shutil.copy2(src,A/file)
    record=dict(title=title,description=description,category=category,topic=topic,pages=0,file=file,source=str(src.relative_to(RESEARCH)),url='/assets/v3/'+file,format='Markdown',version='V3.1' if 'v3-1' in file else 'V3',date='2026-10-12')
    records.append(record)
    provenance.append(dict(file=file,source=record['source'],sha256=sha(src),source_url=f'https://github.com/akilanpl/mindscape/blob/{COMMIT}/{record["source"]}'))
for p in (RESEARCH/'experiments/v3_integration/native_v1').glob('*.json'): shutil.copy2(p,A/p.name)
for name in ['learning-curves.svg','learning-curves.csv']: shutil.copy2(RESEARCH/'docs/v3_math/figures'/name,A/name)

integration=json.loads((A/'summary.json').read_text())
evidence=dict(updated='2026-10-12',research_commit=COMMIT,integration=integration,mathematics=dict(budgets=[10,25,50,100,250,500,1000],compact_concepts_ood_percent=[.67,2.22,4.44,10.89,17.78,23.56,26.89],adapter_concepts_ood_percent=[.89,1.78,5.56,11.11,19.33,24.89,31.33],length_ood_percent=dict(compact=27.78,adapter=30.0),target_achieved=False),coding=dict(ood_successes=8,ood_tasks=12,wilson95_percent=[39.1,86.2],strongest_reference_successes=9,paired_difference_points=-8.3,paired_bootstrap95_points=[-25,0],superiority_gate=False),physics=dict(primary_forecasts=6000,all_forecasts=19200,planning_episodes=2160,engineering_verified=True,improvement_target_achieved=False),physics_v3_1=dict(development_scenes=26,forecasts=780,planning_outcomes=32,decision='NO-GO',motion_improvement_percent=1.52,interaction_improvement_percent=-.31,coverage_percent=[75.40,68.62]),sources=provenance,learned_cross_domain_transfer='NOT YET ESTABLISHED')
(A/'current-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
(A/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')

common_cards='<div class="v3-cards">'+card('Mathematics','Neural transition learners compose local claims under declared procedural scaffolds. The target was not reached; the two integration examples both fail.','/assets/v3/v3-mathematics.md')+card('Python coding','Structured repair and verified training memories run through WASI. New-benchmark OOD success is 8/12; the strongest reference solves 9/12.','/assets/v3/v3-coding.md')+card('Physical dynamics','The complete V3 study exposed catastrophic motion divergence. V3.1 stabilizes finite rollouts, but fails improvement and calibration gates.','/assets/v3/v3-1-physics.md')+'</div>'
demo_table=table(['Frozen request','Actual result','Verified task outcome'],[['487 + 376','833; expected 863','FAIL'],['73 − 29','43; expected 44','FAIL'],['Python threshold repair','> 4 → >= 4; visible 2/2, private 4/4','PASS'],['8-step motion planning','Goal distance 0.316; prediction MSE 1.225','PASS']])
demo='<p>One native MPS run exercised existing specialists directly and through the common kernel. All four requests independently replayed in both paths. Results agree, including the failures. These demonstrations are not an accuracy benchmark.</p>'+demo_table+report('v3-integration.md','Integration report and failure diagnosis')
metrics=table(['Study','Observed result','Scientific conclusion'],[['Mathematics, 1,000 examples','Compact concepts 26.89% OOD; adapter concepts 31.33% (three-seed means)','50% length target not reached; neural rule necessity not established'],['Coding, fresh structural OOD','8/12 (66.7%); 95% Wilson 39.1–86.2%; no-concepts reference 9/12','Paired difference −8.3 points, 95% bootstrap −25 to 0; superiority gate failed'],['V3 physics, final budget','Motion OOD MSE 9.33957e7 vs 18.1353 matched; interaction 7.74368 vs 3.66973','20% improvement target failed; severe motion divergence'],['V3.1 development pilot','32-step stress error: motion 2.8930, interaction 1.0058','Finite/stability gates passed; improvement and calibration gates failed']])
cycle='<ol class="v3-cycle">'+''.join(f'<li>{x}</li>' for x in ['Observe','Represent','Propose','Predict','Act','Verify','Update'])+'</ol>'
contents={
'index.html':section('Three domains. One inspectable research runtime.','<p>Mindscape V3 now connects mathematical learning, Python debugging and simulated physical dynamics through one typed runtime. Engineering integration is verified; reliable generalization remains an open research problem.</p>'+common_cards+'<p class="v3-status">Verified integration · Mathematical errors retained · Physics improvement NO-GO</p>'+link('/advancements/#current-research','Inspect the current results')),
'about/index.html':section('What Mindscape can demonstrate today','<p>The project has grown from multiplication and Python repair into a shared cognitive kernel with three domain adapters. Existing learned models propose numerical transitions, code repairs and physical outcomes. Independent executors and scorers check what actually happens.</p>'+common_cards+'<p>The latest milestone is reproducible integration, not a reasoning breakthrough. The mathematical study missed its target; coding concepts did not beat the strongest matched reference; physics stability research remains NO-GO for scaling. Future work should diagnose these failures before expanding training.</p>'+report('v3-integration.md','Current project handoff')),
'research/index.html':section('Current research: learning, repair and dynamics',common_cards+'<p>V3 uses frozen task identities, matched information, raw predictions, independent execution and explicit negative-result reporting. Historical V1/V2 evidence remains preserved and is presented separately below.</p>'+link('/research/library/','Browse current and historical protocols')),
'research/library/index.html':section('A versioned research record','<p>Current V3/V3.1 reports are indexed alongside the 45 preserved historical documents. Filter by research version and domain. Dates on current entries identify this website’s evidence update, not an invented publication date.</p>'+report('provenance.json','Source files, commit references and SHA-256 hashes')),
'research/reports/index.html':section('Latest findings, with the failures intact',metrics+'<p>Each study has its own tasks, denominators and protocol. V3.1 uses different error scales and development scenes from V3; their MSE values are not directly comparable.</p>'+report('v3-integration.md','Verified integration milestone')),
'advancements/index.html':section('V3 progress is measurable—and incomplete.',metrics+'<h3>Mathematical learning curves</h3><figure><img src="/assets/v3/learning-curves.svg" alt="Frozen mathematical learning curves across seven budgets; the predeclared 50 percent length target was not reached." loading="lazy"><figcaption>Preserved study figure; means across three seeds. '+report('learning-curves.csv','Download original curve data')+'</figcaption></figure><h3>Physics stability and calibration gates</h3>'+table(['V3.1 gate','Threshold','Motion','Interaction'],[['32-step stress error','≤10','2.8930 · PASS','1.0058 · PASS'],['32/8 error growth','≤4','3.2570 · PASS','1.0570 · PASS'],['Matched improvement','≥10%','1.52% · FAIL','−0.31% · FAIL'],['Nominal 95% coverage','≥80%','75.40% · FAIL','68.62% · FAIL']])+'<p>The V3 study completed 6,000 primary forecasts, 19,200 forecasts overall and 2,160 planning episodes with independent verification. V3.1 independently verified 780 horizon-conditioned forecasts and 32 action outcomes on 26 development scenes. Repeated conditions and seeds are not independent scenes. Sealed V3.1 final trajectories were not evaluated.</p><h3>The integration demonstration</h3>'+demo+'<p>Next priority: small, independent development diagnostics for stable dynamics and measurement equivalence; investigate mathematical consistency errors and fair coding comparisons. No larger physics study is justified by the current pilot.</p>'),
'architecture/index.html':section('The V3 cognitive kernel',cycle+'<p>Typed requests, observations, proposed actions, predicted transitions, executed transitions and independent evaluations connect interchangeable domain adapters. Predictions remain hypothetical until an executor produces an actual result. Evaluation does not update training memory or model weights.</p>'+common_cards+'<p>Math uses a compact neural transition model plus explicit digit/sign scheduling. Its executor writes proposed claims without arithmetic correction. Coding uses Qwen2.5-Coder-1.5B, approved structured training memories and a learned proposal evaluator; generated Python runs only in WASI. Physics uses object-centric dynamics and bounded candidate planning; hidden simulator parameters and future states stay outside model observations.</p><p>Math and physics macro routing submits specialist proposals deterministically; it is not learned semantic reasoning. The runtime does not pool learned knowledge between domains.</p><h3>Recorded integration—not a live assistant</h3>'+demo+report('0-mathematics.json','Failed addition: full direct and kernel traces')+' · '+report('2-coding.json','Successful WASI repair trace')+' · '+report('3-physics.json','Selected-action physics trace')+'<p>Raw math claims are retained, but exact math/sign logits were not recorded. Traces show what happened; they do not prove causal concept use.</p>'),
'safety/index.html':section('Current safeguards and their limits','<div class="v3-cards">'+card('Execute within boundaries','Generated Python runs through the existing pinned WASI executor, never the host interpreter. Typed inputs reject unknown/private fields and unsafe source.','/assets/v3/v3-coding-architecture.md')+card('Keep scoring independent','Private terminal tests are unavailable to generation. Mathematical teachers and simulator truth judge outcomes after proposals. Successful evaluation episodes do not enter training memory.','/assets/v3/v3-integration.md')+card('Preserve failed evidence','Frozen datasets, model hashes, historical releases and unsuccessful runs are retained. Native neural execution requires MPS and rejects CPU fallback.','/assets/v3/provenance.json')+'</div><p>The integration passed independent replay and 108 software tests plus four subtests. Final focused validation passed 15 tests plus four domain subtests. These are scoped engineering checks, not certification, production readiness or proof against every adversarial input.</p><p>The two mathematics failures and physics model limitations remain part of the safety and integrity record. Strong execution isolation cannot make an incorrect neural prediction correct.</p>'),
'safety/deployment/index.html':section('Research execution, not production certification','<p>The verified integration uses existing pinned local model files and a pinned WASI runtime. All neural workloads run on native Apple MPS; unavailable devices or enabled fallback block execution. CPU simulation, replay and statistics are separate from neural inference.</p><p>Checkpoint, source and dataset identities bind the results. Preserve failed directories; incompatible source/checkpoint identities require a fresh versioned run. No training or full physics rerun is required to inspect these saved demonstrations.</p>'+report('v3-integration.md','Runtime requirements and reproduction commands')+' · '+report('verification.json','Independent replay receipt')+'<p>Public website hosting is distinct from deploying the research agent. These results do not establish production abuse prevention, real-world physical safety, semantic factuality or comprehensive prompt-injection resistance.</p>'),
'resources/index.html':section('Current reports, traces and reproducibility','<p>Start with the V3 integration handoff, then inspect each domain’s scientific findings and original protocols. Historical PDFs and figures remain available unchanged.</p><div class="v3-cards">'+card('Scientific findings','Read mathematical learning failures, matched Python repair comparisons and the physics NO-GO diagnosis.','/research/library/')+card('Machine-readable evidence','Download current summaries, provenance, native outcomes and independent replay verification.','/assets/v3/current-evidence.json')+card('Reproduce the runtime','Existing local assets and native MPS are required. No retraining or model download is part of the integration workflow.','/assets/v3/v3-integration.md')+'</div>'+report('provenance.json','Source manifest')+' · '+report('verification.json','Verification receipt')+' · '+report('learning-curves.csv','Mathematics curve data')),
}

# Preserve the complete historical PDF/graph corpus with a public hash manifest.
old_files={str(p.relative_to(D)):sha(p) for folder in ['assets/reports','assets/graphs'] for p in (D/folder).rglob('*') if p.is_file()}
for name in ['Mindscape-Research-Report.pdf','Mindscape-Document-Library.pdf','benchmark-data.json','architecture-traces.json']:
    old_files['assets/'+name]=sha(D/'assets'/name)
(A/'historical-preservation.json').write_text(json.dumps(old_files,indent=2)+'\n')

for relative,new in contents.items():
    p=D/relative; s=p.read_text()
    if 'id="current-research"' in s: raise RuntimeError('Update already applied')
    if relative=='research/library/index.html':
        s=re.sub(r'(<h1[^>]*>.*?</h1>)',lambda m:m[0]+new,s,count=1,flags=re.S)
    else:
        # Insert after the first complete section, including nested sections.
        start=s.index('<main'); first=s.index('<section',start); depth=0; end=None
        for m in re.finditer(r'</?section\b[^>]*>',s[first:]):
            depth+= -1 if m[0].startswith('</') else 1
            if depth==0: end=first+m.end(); break
        assert end is not None
        s=s[:end]+new+s[end:]
    s=s.replace('</head>','<link rel="stylesheet" href="/v3.css?v=20261012"></head>')
    route='/' if relative=='index.html' else '/'+relative.removesuffix('index.html')
    s=re.sub(r'<link[^>]+rel="canonical"[^>]*>','',s)
    s=s.replace('</head>',f'<link rel="canonical" href="{ORIGIN}{route}"><meta property="og:url" content="{ORIGIN}{route}"></head>')
    s=s.replace('Full research report ↗','Historical V1/V2 report ↗').replace('The complete research and security report','Historical V1/V2 research and security report')
    # Historical study dates remain explicit; footer represents the current website.
    s=s.replace('Research snapshot · 10 October 2026</p>','Research update · 12 October 2026</p>')
    p.write_text(s)

# Clarify older text that otherwise describes current architecture incorrectly.
replacements={
'about/index.html': [('It does not establish general intelligence, a learned world model, broad model superiority, or a demonstrated benefit from dreaming.','It does not establish general intelligence, reliable learned physical dynamics, broad model superiority, or a demonstrated benefit from dreaming.'),('Learn more about what we study','Historical studies: where the project began'),('Where we go from here','What remains scientifically unresolved')],
'architecture/index.html':[('The project has two backends with different mechanisms.','The historical V1/V2 configuration had two backends with different mechanisms.'),('Two backends. Different mechanisms.','Historical V1/V2 backends and diagnostics.'),('Research v2 remains incomplete.','The historical V2 research remained incomplete; current V3 findings are shown below.')],
'advancements/index.html':[('Research snapshot · 10 October 2026','Historical V1/V2 snapshot · 10 October 2026'),('Verified progress. Bounded findings.','Preserved V1/V2 findings.'),('The preserved research now spans','The historical record spans')],
'research/reports/index.html':[('Archived documents · 10 October 2026 snapshot','Current V3/V3.1 reports and the preserved 10 October V1/V2 archive'),('Browse all 45 source documents','Browse current and historical source documents')],
'resources/index.html':[('Two recorded coding diagnostic trajectories.','Historical coding diagnostics; current three-domain traces are available above.')],
}
for relative, pairs in replacements.items():
    p=D/relative;s=p.read_text()
    for old,new in pairs:s=s.replace(old,new)
    p.write_text(s)
# Homepage FAQs: update tested domains without introducing unsupported claims.
p=D/'index.html';s=p.read_text();s=s.replace('Coding studies, controlled experiments, and preserved failures','Mathematics, coding and physics studies, with preserved failures')
s=re.sub(r'(<summary>What has it been tested on\?</summary>).*?(</details>)',r'\1<p>V3 studies mathematical transitions, Python repair and simulated motion/interactions. A four-request native integration demonstration independently replayed all outcomes: mathematics 0/2, coding 1/1 and physics 1/1. These are demonstrations, not general accuracy estimates.</p>\2',s,flags=re.S)
p.write_text(s)
# Contact stays functional; no test email is sent.
p=D/'contact/index.html';s=p.read_text();s=s.replace('</ul></section>','</ul><p class="v3-contact-note">We welcome collaboration on mathematical learning, verified Python repair, physics stability and independent replication. Mindscape is a research system; shared learned knowledge across domains has not yet been demonstrated.</p></section>',1)
s=s.replace('<option>Research support</option>','<option>Research support</option><option>Mathematical learning</option><option>Python debugging</option><option>Physics stability</option><option>Independent replication</option>')
s=s.replace('Tell us what you have in mind.','Tell us the research question, domain and evidence you would like to explore.')
s=s.replace('</head>','<link rel="stylesheet" href="/v3.css?v=20261012"><link rel="canonical" href="'+ORIGIN+'/contact/"></head>');p.write_text(s)

# Current entries link directly to new Markdown exports; historical PDFs remain untouched.
p=D/'research-data.js'; old=json.loads(p.read_text().removeprefix('window.MindscapeResearch=').rstrip(';\n'))
for r in old:r['version']='Historical V1/V2';r['format']='PDF'
p.write_text('window.MindscapeResearch='+json.dumps(records+old)+';\n')
for relative in ['research/library/index.html','resources/index.html']:
    p=D/relative;s=p.read_text()
    if 'id="research-topic"' in s:
        s=s.replace('<option>Methods</option>','<option>Methods</option><option>Mathematics</option><option>Physics</option>')
        s=s.replace('<option value="Methods">Methods</option>','<option value="Methods">Methods</option><option value="Mathematics">Mathematics</option><option value="Physics">Physics</option>')
        s=s.replace('</select></label>', '</select></label>',1)
        s=s.replace('<div id="research-list"', '<label class="v3-version">Research version<select id="research-version"><option value="All">All versions</option><option value="V3">V3</option><option value="V3.1">V3.1</option><option value="Historical V1/V2">Historical V1/V2</option></select></label><div id="research-list"')
    else:
        s=s.replace('<button data-filter="Coding"','<button data-filter="Mathematics" aria-pressed="false">Mathematics</button><button data-filter="Physics" aria-pressed="false">Physics</button><button data-filter="Coding"',1)
    s=s.replace('Preserved document library · Snapshot 10 October 2026.','Versioned document library · Updated 12 October 2026. Historical snapshot: 10 October 2026.')
    p.write_text(s)
# Existing alias remains synchronized.
shutil.copy2(D/'research/library/index.html',D/'research/index/index.html')
# Add source-bound metadata and current report promotion.
p=D/'research.js';s=p.read_text()
s=s.replace("${depth}assets/reports/${esc(r.file)}", "${esc(r.url||depth+'assets/reports/'+r.file)}")
s=s.replace("${r.pages} ${r.pages===1?'page':'pages'}", "${r.format==='Markdown'?r.version+' · Markdown':r.pages+' '+(r.pages===1?'page':'pages')}")
s=s.replace("let rows=data.filter(r=>", "let rows=data.filter(r=>(document.getElementById('research-version').value==='All'||r.version===document.getElementById('research-version').value)&&")
s=s.replace('[search,topic,sort].forEach','[search,topic,sort,document.getElementById("research-version")].forEach')
s=s.replace("search.value='';topic.value='All';limit=9", "search.value='';topic.value='All';document.getElementById('research-version').value='All';limit=9")
s=s.replace("const slides=[", "const slides=[['V3: verified three-domain integration','v3/v3-integration.md'],['V3.1 physics: stability pilot NO-GO','v3/v3-1-physics.md'],['V3 mathematical learning: findings and limits','v3/v3-mathematics.md'],")
s=s.replace("'The complete research and security report'","'Historical V1/V2 research and security report'")
p.write_text(s)
p=D/'resources.js';s=p.read_text().replace("a.href='../assets/reports/'+r.file","a.href=r.url||'../assets/reports/'+r.file")
s=s.replace("pages.textContent='PDF · '+r.pages+' pages'", "pages.textContent=r.format==='Markdown'?r.version+' · Markdown':'PDF · '+r.pages+' pages'")
s=s.replace("image.src='../assets/graphs/'+thumbnails(r)+'.png'", "image.src=r.version==='Historical V1/V2'?'../assets/graphs/'+thumbnails(r)+'.png':'../assets/favicon.svg'")
p.write_text(s)
# Featured report markup before JS starts.
p=D/'research/reports/index.html';s=p.read_text().replace('Historical V1/V2 research and security report','V3: verified three-domain integration',1)
s=re.sub(r'(<a[^>]*id="featured-report"[^>]*href=")[^"]+',r'\1/assets/v3/v3-integration.md',s)
s=s.replace('1 / 3','1 / 6');p.write_text(s)

css='''/* Current research shares the site's quiet editorial style. */
.v3-section{max-width:1160px;margin:56px auto;padding:48px 28px;border-top:1px solid #ddd;border-bottom:1px solid #ddd;background:#fff;color:#181818;text-align:left;box-sizing:border-box;font-family:inherit}.v3-section h2{font-size:clamp(29px,4vw,48px);font-weight:500;letter-spacing:-.035em;line-height:1.12;margin:12px 0 24px}.v3-section h3{font-size:23px;font-weight:500;line-height:1.3;margin:26px 0 14px}.v3-section p{font-size:17px;line-height:1.65;max-width:90ch;margin:16px 0}.v3-section a{color:#135cbd;text-decoration:underline;text-underline-offset:4px}.v3-eyebrow{font-size:12px!important;letter-spacing:.12em;text-transform:uppercase;color:#666}.v3-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin:28px 0}.v3-card{border-top:2px solid #222;padding:8px 0 22px}.v3-card h3{margin:14px 0}.v3-card p{font-size:16px}.v3-boundary,.v3-status{font-size:14px!important;padding:16px 18px;background:#f2f4f6;border-radius:8px}.v3-table-wrap{width:100%;overflow-x:auto;margin:24px 0}.v3-section table{border-collapse:collapse;width:100%;min-width:560px;font-size:15px;line-height:1.5}.v3-section th,.v3-section td{text-align:left;padding:15px 14px;border-bottom:1px solid #ddd;vertical-align:top}.v3-section th{font-weight:600;background:#f6f6f6}.v3-cycle{display:flex;flex-wrap:wrap;gap:10px;padding:0;list-style-position:inside}.v3-cycle li{padding:12px;background:#f2f4f6;border-radius:6px;font-size:15px}.v3-section figure{margin:30px 0}.v3-section figure img{max-width:100%;height:auto}.v3-section figcaption{font-size:13px;line-height:1.5;color:#555}.v3-version{display:block;margin:25px 0;font-size:14px}.v3-version select{margin-left:12px;padding:10px;border:1px solid #bbb;border-radius:6px;font:inherit}.v3-contact-note{font-size:16px;line-height:1.65;max-width:440px;margin:28px 0}.archive>.v3-section{margin:20px 0 35px;padding:28px 0}.v3-section :focus-visible{outline:3px solid #2468d0;outline-offset:5px}@media(max-width:760px){.v3-section{margin:28px 16px;padding:28px 4px}.v3-cards{grid-template-columns:1fr;gap:12px}.v3-section h2{font-size:32px}.v3-section p{font-size:16px}.v3-section table{font-size:14px}.v3-section th,.v3-section td{padding:12px 10px}.v3-version select{display:block;margin:10px 0;width:100%}}
'''
(D/'v3.css').write_text(css)
# Sitemap only includes canonical pages; preserve legacy redirect/alias.
routes=['/','/about/','/research/','/research/library/','/research/reports/','/advancements/','/architecture/','/safety/','/safety/deployment/','/resources/','/contact/']
(D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}{r}</loc><lastmod>2026-10-12</lastmod></url>' for r in routes)+'</urlset>')
(D/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n')
print('Updated 11 canonical pages plus legacy alias; exported',len(records),'current reports; historical corpus',len(old_files),'files preserved')
