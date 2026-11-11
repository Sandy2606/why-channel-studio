const { chromium } = require('playwright');
const fs=require('fs');
const targets=[
 ['A1_christian_pilot','The king, when he received this message, sent a Christian pilot','sent a Christian pilot'],
 ['A2_calecut_christians','The city of Calecut is inhabited by Christians','The city of Calecut is inhabited by Christians'],
 ['B1_fn132_gujarat','This pilot was a native of Gujarat','This pilot was a native of Gujarat'],
 ['W1_tunis','two Moors from Tunis, who could speak Castilian and Genoese','two Moors from Tunis, who could speak Castilian and Genoese'],
 ['W2_gifts','the poorest merchant from Mecca','the poorest merchant from Mecca, or any other part of India, gave more'],
];
(async()=>{
 const b=await chromium.launch(); const p=await b.newPage({viewport:{width:430,height:1400},deviceScaleFactor:2.4});
 await p.goto('file://'+process.cwd()+'/rav.htm');
 const out={};
 for(const [id,anchor,hl] of targets){
  const r=await p.evaluate(([anchor,hl])=>{
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_ELEMENT);
    let best=null;
    for(const el of document.querySelectorAll('p,div.footnote,div')){ if(el.textContent.replace(/\s+/g,' ').includes(anchor)){ if(!best||el.textContent.length<best.textContent.length) best=el; } }
    if(!best) return null;
    best.scrollIntoView({block:'center'});
    // find highlight range
    const tw=document.createTreeWalker(best,NodeFilter.SHOW_TEXT); let n, full='', nodes=[];
    while(n=tw.nextNode()){ nodes.push([n,full.length]); full+=n.textContent; }
    const norm=full.replace(/\s/g,' '); const i=norm.indexOf(hl); let rects=[];
    if(i>=0){ const j=i+hl.length; const range=document.createRange();
      const loc=(k)=>{ for(let q=nodes.length-1;q>=0;q--) if(nodes[q][1]<=k) return [nodes[q][0],k-nodes[q][1]]; };
      const [sn,so]=loc(i),[en,eo]=loc(j); range.setStart(sn,so); range.setEnd(en,eo);
      rects=[...range.getClientRects()].map(r=>({x:r.x,y:r.y,w:r.width,h:r.height})); }
    const br=best.getBoundingClientRect();
    return {box:{x:br.x,y:br.y,w:br.width,h:br.height},rects,text:best.textContent.replace(/\s+/g,' ').trim()};
  },[anchor,hl]);
  if(!r){console.log('MISS',id);continue;}
  await p.screenshot({path:id+'.png',clip:{x:r.box.x-14,y:r.box.y-10,width:r.box.w+28,height:r.box.h+20}});
  r.rects=r.rects.map(q=>({x:(q.x-r.box.x+14)*2.4,y:(q.y-r.box.y+10)*2.4,w:q.w*2.4,h:q.h*2.4}));
  out[id]=r; console.log(id,Math.round(r.box.w*2.4),Math.round(r.box.h*2.4),r.rects.length,r.text.slice(0,90));
 }
 fs.writeFileSync('clips.json',JSON.stringify(out,null,1)); await b.close();
})();
