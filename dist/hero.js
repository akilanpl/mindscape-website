const sections = {
  about: {title:'About Mindscape', text:'Mindscape is an experimental architecture for explicit state, bounded actions, memory, and verification around learned policies. It studies how an inspectable execution process can support grounded work.', link:'https://github.com/akilanpl/mindscape', label:'Explore the project ↗'},
  research: {title:'Research', text:'The frozen coding lockbox covers 100 independent tasks and 400 condition/task executions. Mindscape C achieved 49/50 repairs on IID tasks and 18/50 on structural OOD tasks. Unequal supervision and interaction budgets limit architecture-only conclusions.', link:'assets/Mindscape-Research-Report.pdf',label:'Read the research report ↗'},
  advancements: {title:'Advancements',text:'Verified progress includes completed bounded coding studies, preserved negative results, controlled numeric masking findings, and two real coding-forward diagnostics. Broader learned generalization and a full Research v2 completion remain unestablished.',link:'assets/Mindscape-Research-Report.pdf',label:'Inspect the findings ↗'},
  architecture: {title:'Architecture',text:'Observation → structured state → policy proposal → bounded action → actual environment result → recorded transition → terminal verification. Hypothetical predictions remain separate from executed evidence.',link:'https://github.com/akilanpl/mindscape',label:'View the source ↗'},
  safety: {title:'Safety',text:'Generated code runs inside a capability-limited WASI guest. Trusted host tools validate edits; private tests remain outside policy observations. These controls bound execution and evidence access; they do not establish comprehensive alignment or security certification.',link:'assets/Mindscape-Research-Report.pdf',label:'Read security and integrity notes ↗'},
  resources: {title:'Resources',text:'Explore the source repository and the consolidated research report, including experiment protocols, benchmark interpretation, limitations, and reproduction references.',link:'assets/Mindscape-Research-Report.pdf',label:'Open the full report ↗'}
};
const dialog = document.querySelector('#section-dialog');
let activeLink = null;
function showSection(key) {
  if (key === "resources") { location.href="resources/"; return; }
  if (key === "safety") { location.href = "safety/"; return; }
  if (key === "architecture") { location.href = "architecture/"; return; }
  if (key === "advancements") { location.href = "advancements/"; return; }
  if (key === "research") { window.location.href = "research/"; return; }
  if (key === "about") { location.href = "about/"; return; }
  const section = sections[key];
  if (!section) return;
  document.querySelector('#section-title').textContent = section.title;
  const content = document.querySelector('#section-content');
  content.replaceChildren();
  const paragraph = document.createElement('p'); paragraph.textContent = section.text;
  const link = document.createElement('a'); link.href = section.link; link.textContent = section.label; link.target = '_blank'; link.rel = 'noopener noreferrer';
  content.append(paragraph,link);
  document.querySelectorAll('[data-section]').forEach(a => a.removeAttribute('aria-current'));
  activeLink = document.querySelector(`[data-section="${key}"]`); activeLink?.setAttribute('aria-current','true');
  if (!dialog.open) dialog.showModal();
}
document.querySelectorAll('[data-section]').forEach(link => link.addEventListener('click', event => { event.preventDefault(); history.replaceState(null,'',link.hash); showSection(link.dataset.section); }));
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) { const r=dialog.getBoundingClientRect(); if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close(); } });
dialog.addEventListener('close', () => { history.replaceState(null,'',location.pathname+location.search); activeLink?.removeAttribute('aria-current'); activeLink?.focus(); });
showSection(location.hash.slice(1));
