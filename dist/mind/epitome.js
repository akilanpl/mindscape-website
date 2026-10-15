'use strict';
(() => {
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const canvas=document.querySelector('#epitome-stars'),ctx=canvas.getContext('2d');
  const header=document.querySelector('.site-header'),root=document.documentElement;
  const interaction=document.querySelector('#galaxy-interaction'),replay=document.querySelector('#replay-galaxy');
  const pause=document.querySelector("#pause-galaxy");let paused=reduced.matches;
  function pauseLabel(){pause.textContent=paused?"▶":"Ⅱ";pause.setAttribute("aria-label",paused?"Play star field animation":"Pause star field animation");pause.title=pause.getAttribute("aria-label");}
  let width=0,height=0,frame=0,last=0,clock=0,scroll=0,rotation=0,pitch=.54,targetRotation=0,targetPitch=.54,drag=null,seed=618;
  const random=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;};
  const stars=Array.from({length:6500},(_,i)=>{
    const r=Math.pow(random(),.66),arm=i%4,theta=r*8.2+arm*Math.PI/2+(random()-.5)*(.16+.21*r);
    return {x:Math.cos(theta)*r,y:Math.sin(theta)*r,z:(random()-.5)*(.018+.12*(1-r)),size:random()>.985?1.4+random()*1.7:.19+random()*.85,alpha:.2+random()*.8,color:random()<.16?2:random()<.4?1:0,phase:random()*6.28};
  });
  const backdrop=Array.from({length:470},()=>({x:random(),y:random(),size:.2+random()*.8,alpha:.08+random()*.45}));
  const sprites=['#eaf4ff','#9dbddc','#e6b88a'].map(color=>{const sprite=document.createElement('canvas');sprite.width=sprite.height=32;const c=sprite.getContext('2d');const glow=c.createRadialGradient(16,16,0,16,16,16);glow.addColorStop(0,'#ffffff');glow.addColorStop(.12,color);glow.addColorStop(.28,color+'a0');glow.addColorStop(.6,color+'20');glow.addColorStop(1,color+'00');c.fillStyle=glow;c.fillRect(0,0,32,32);return sprite;});
  function draw(){
    if(!ctx)return;
    ctx.clearRect(0,0,width,height);
    for(const s of backdrop){ctx.globalAlpha=s.alpha;ctx.fillStyle='#b6c8df';ctx.fillRect(s.x*width,s.y*height,s.size,s.size);}
    const out=Math.min(scroll/(height*.8),1),size=Math.min(width*.33,height*.46)*(width<600?1.25:1)*(1+out*1.8),cx=width/2,cy=height*.5;
    const turn=rotation+clock*.016,tilt=-.46+targetRotation*.08;
    const cos=Math.cos(turn),sin=Math.sin(turn),ct=Math.cos(tilt),st=Math.sin(tilt),cp=Math.cos(pitch),sp=Math.sin(pitch);
    ctx.globalCompositeOperation='lighter';
    for(const p of stars){
      const x=p.x*cos-p.y*sin,y=p.x*sin+p.y*cos,yy=y*cp-p.z*sp,z=y*sp+p.z*cp;
      const perspective=1/(1+z*.28),px=cx+(x*ct-yy*st)*size*perspective,py=cy+(x*st+yy*ct)*size*perspective;
      const radius=p.size*perspective*(width<600?.75:1)*(1+.12*Math.sin(clock*.7+p.phase));
      ctx.globalAlpha=p.alpha*(1-out*.68);
      if(radius>.95){const r=radius*5;ctx.drawImage(sprites[p.color],px-r,py-r,r*2,r*2);}else{ctx.fillStyle=p.color===2?'#e0b68f':p.color===1?'#94b5da':'#e2edfc';ctx.beginPath();ctx.arc(px,py,Math.max(.22,radius),0,Math.PI*2);ctx.fill();}
    }
    const core=ctx.createRadialGradient(cx,cy,0,cx,cy,size*.16);core.addColorStop(0,'rgba(242,248,255,.8)');core.addColorStop(.12,'rgba(228,238,255,.5)');core.addColorStop(.4,'rgba(185,205,233,.12)');core.addColorStop(1,'rgba(145,174,211,0)');ctx.globalAlpha=1-out;ctx.fillStyle=core;ctx.fillRect(cx-size*.17,cy-size*.17,size*.34,size*.34);ctx.globalCompositeOperation='source-over';ctx.globalAlpha=1;
  }
  function tick(time){
    if(document.hidden){frame=0;return;}
    if(time-last>32){clock+=.033;rotation+=(targetRotation-rotation)*.09;pitch+=(targetPitch-pitch)*.09;draw();last=time;}
    frame=requestAnimationFrame(tick);
  }
  function start(){if(!paused&&!frame&&!document.hidden)frame=requestAnimationFrame(tick);else draw();}
  function resize(){width=innerWidth;height=innerHeight;const scale=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.round(width*scale);canvas.height=Math.round(height*scale);ctx?.setTransform(scale,0,0,scale,0,0);draw();}
  function onScroll(){scroll=window.scrollY;root.style.setProperty('--shade',String(Math.min(scroll/(height*.8),1)));header.classList.toggle('scrolled',scroll>40);if(paused)draw();}
  interaction.addEventListener('pointerdown',e=>{if(e.pointerType==='touch')return;drag={x:e.clientX,y:e.clientY,r:targetRotation,p:targetPitch};interaction.setPointerCapture(e.pointerId);interaction.classList.add('dragging');});
  interaction.addEventListener('pointermove',e=>{if(!drag)return;targetRotation=drag.r+(e.clientX-drag.x)*.005;targetPitch=Math.max(.1,Math.min(1.1,drag.p+(e.clientY-drag.y)*.003));if(paused){rotation=targetRotation;pitch=targetPitch;draw();}});
  const stopDrag=()=>{drag=null;interaction.classList.remove('dragging');};interaction.addEventListener('pointerup',stopDrag);interaction.addEventListener('pointercancel',stopDrag);
  interaction.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Enter',' '].includes(e.key))return;e.preventDefault();if(e.key==='ArrowLeft')targetRotation-=.2;if(e.key==='ArrowRight')targetRotation+=.2;if(e.key==='ArrowUp')targetPitch=Math.min(1.1,targetPitch+.1);if(e.key==='ArrowDown')targetPitch=Math.max(.1,targetPitch-.1);if(e.key==='Enter'||e.key===' '){targetRotation=0;targetPitch=.54;}if(paused){rotation=targetRotation;pitch=targetPitch;draw();}});
  pause.addEventListener('click',()=>{paused=!paused;cancelAnimationFrame(frame);frame=0;pauseLabel();start();});pauseLabel();
  replay.addEventListener('click',()=>{clock=0;targetRotation=0;targetPitch=.54;rotation=0;pitch=.54;draw();start();});
  document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;}else start();});
  reduced.addEventListener('change',()=>{paused=reduced.matches;pauseLabel();cancelAnimationFrame(frame);frame=0;start();});window.addEventListener('resize',resize);window.addEventListener('scroll',onScroll,{passive:true});resize();onScroll();start();

  // Tabs are static evidence views, with keyboard navigation and readable fallbacks.
  document.querySelectorAll('[role="tablist"]').forEach(list=>{
    const tabs=[...list.querySelectorAll('[role="tab"]')];
    function select(tab,focus=false){tabs.forEach(t=>{const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;document.getElementById(t.getAttribute('aria-controls')).hidden=!active;});if(focus)tab.focus();}
    tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>select(tab));tab.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%tabs.length;if(e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;if(e.key==='Home')next=0;if(e.key==='End')next=tabs.length-1;if(next!==undefined){e.preventDefault();select(tabs[next],true);}});});
  });
  const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#site-menu');
  function closeMenu(){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');}
  menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';nav.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('open')){closeMenu();menu.focus();}});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
  matchMedia('(min-width:601px)').addEventListener('change',e=>{if(e.matches)closeMenu();});
  const video=document.querySelector('#showcase-video');let autoPaused=false,userPaused=false;
  video.addEventListener('pause',()=>{if(!autoPaused&&video.currentTime>0)userPaused=true;});video.addEventListener('play',()=>{userPaused=false;autoPaused=false;});
  if('IntersectionObserver' in window)new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting&&entry.intersectionRatio>.5&&!reduced.matches&&!userPaused&&!document.hidden){video.play().catch(()=>{});}else if(!video.paused){autoPaused=true;video.pause();}}},{threshold:[0,.5,.6]}).observe(video);
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&!video.paused){autoPaused=true;video.pause();}});
})();
