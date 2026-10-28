import clipkit as C, json
from PIL import Image
def R(pdf,page,first,last,nf=1,nl=1,pad=(8,6),x=None,top=None):
    a=C.find(pdf,page,first,nf); b=C.find(pdf,page,last,nl); s=a+b
    x0=min(w[0] for w in s); x1=max(w[2] for w in s); y0=min(w[1] for w in a); y1=max(w[3] for w in b)
    if x: x0,x1=x
    if top is not None: y0=top
    return (x0-pad[0],y0-pad[1],x1+pad[0],y1+pad[1])
BT26='bt-may6-2026-article.pdf'; BT24='bt-2024-explainer.pdf'; WK='the-week-2024-gold.pdf'; DR='drishti-ias-gold-repatriation.pdf'; RT='reuters-factbox-syndicated.pdf'
SPEC={
 'bt26_head':[(BT26,1,R(BT26,1,'Business News','why',nl=2,x=(35,330)),[]), (BT26,1,R(BT26,1,'Nachiket','IST',x=(35,330)),[])],
 'bt26_q1':[(BT26,6,R(BT26,6,'In early 1991,','weeks of imports.',x=(35,330)),['barely enough for a few weeks of imports.'])],
 'bt26_q2':[(BT26,6,R(BT26,6,"worth remembering",'emergency loans.',x=(35,330)),['forced to transfer some of the gold abroad to secure emergency loans.'])],
 'bt24_head':[(BT24,1,R(BT24,1,'What made RBI','explainer',nf=2,nl=2,x=(14,330),top=24),[])],
 'wk_head':[(WK,1,R(WK,1,'JOURNALISM','IST',x=(40,520),top=22),['secret move to repatriate 102 metric tonnes'])],
 'dr_q':[(DR,3,R(DR,3,'RBI’S STRATEGIC','2026',x=(22,420)),[]),(DR,3,R(DR,3,'Dominant Domestic','2023.',x=(50,580)),['holds 77% of its total 880.52 MT'])],
 'rt_q':[(RT,1,R(RT,1,'Factbox:','-Reuters',x=(36,452)),[]),(RT,2,R(RT,2,'CENTRAL BANK ASSETS FROZEN','Siluanov.',x=(40,560)),['around $300 billion,'])],
}
out={}
for k,parts in SPEC.items():
    im,h=C.build(parts); im.save(f'/home/claude/g4/clip_{k}.png'); out[k]={'hl':h,'size':im.size}; print(k,im.size,len(h))
json.dump(out,open('/home/claude/g4/clips.json','w'))
