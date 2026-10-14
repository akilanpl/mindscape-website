const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const reduced of [false,true]){
 const events={},ve={},te={},me={};let text='',label='';
 const video={paused:true,autoplay:true,addEventListener:(n,f)=>ve[n]=f,play(){this.paused=false;ve.play?.();return Promise.resolve()},pause(){this.paused=true;ve.pause?.()}};
 const button={addEventListener:(n,f)=>te[n]=f,setAttribute:(n,v)=>label=v,set textContent(v){text=v}};
 const document={hidden:false,querySelector:s=>s==='#hero-video'?video:button,addEventListener:(n,f)=>events[n]=f};
 vm.runInNewContext(fs.readFileSync('dist/launch.js','utf8'),{document,window:{matchMedia:()=>({matches:reduced,addEventListener:(n,f)=>me[n]=f})}});
 assert.equal(video.paused,reduced);te.click();assert.equal(video.paused,!reduced);
 if(!video.paused)te.click();document.hidden=true;events.visibilitychange();document.hidden=false;events.visibilitychange();assert.equal(video.paused,true);
 te.click();assert.equal(video.paused,false);me.change({matches:true});assert.equal(video.paused,true);assert.equal(label,'Play research film');
}
console.log('Playback, manual pause persistence, visibility and reduced-motion checks pass');
