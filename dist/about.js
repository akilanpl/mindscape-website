const tabs = [...document.querySelectorAll('[role="tab"]')];
function selectTab(tab, focus = false) {
  tabs.forEach(t => { const selected = t === tab; t.setAttribute('aria-selected',String(selected));t.tabIndex=selected?0:-1;document.getElementById(t.getAttribute('aria-controls')).hidden=!selected; });
  if (focus) tab.focus();
}
tabs.forEach((tab,index) => {
  tab.addEventListener('click',()=>selectTab(tab));
  tab.addEventListener('keydown',event=>{let next;if(event.key==='ArrowRight')next=(index+1)%tabs.length;if(event.key==='ArrowLeft')next=(index-1+tabs.length)%tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;if(next!==undefined){event.preventDefault();selectTab(tabs[next],true);}});
});
document.querySelector('[data-select-numeric]').addEventListener('click',()=>selectTab(document.querySelector('#numeric-tab')));
