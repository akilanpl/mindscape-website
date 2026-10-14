const video=document.querySelector('#hero-video');
const toggle=document.querySelector('.film-toggle');
const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
let userPaused=reduced.matches;
function sync(){toggle.textContent=video.paused?'Play film':'Pause film';toggle.setAttribute('aria-label',video.paused?'Play research film':'Pause research film');}
function play(){if(!userPaused&&!document.hidden)video.play().catch(sync);}
if(userPaused){video.autoplay=false;video.pause();}
toggle.addEventListener('click',()=>{userPaused=!video.paused;if(userPaused)video.pause();else video.play().catch(sync);});
video.addEventListener('play',sync);video.addEventListener('pause',sync);video.addEventListener('canplay',play);
document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else play();});
reduced.addEventListener('change',e=>{if(e.matches){userPaused=true;video.pause();}});
sync();play();
