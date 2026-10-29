import json, re, difflib
S=open('/home/claude/why-channel-studio/videos/2026-10-30_short_gold_dhanteras/en.txt').read().replace('...',',')
S+=" The full gold story is out now on our channel. If you like learning things like this, {CTA} for a new why every day. Comment your why below, and we'll find the answer."
S=S.replace('7 percent','7%').replace('one dollar','1 dollar')
def n(w): return re.sub(r"[^\w%]","",w.lower())
for plat,cta in (('yt','subscribe'),('ig','follow')):
    toks=S.replace('{CTA}',cta).split(); W=json.load(open(f'words_en_{plat}.json'))
    a=[n(t) for t in toks]; b=[n(w[2]) for w in W]
    T=[None]*len(toks)
    for blk in difflib.SequenceMatcher(None,a,b,autojunk=False).get_matching_blocks():
        for k in range(blk.size): T[blk.a+k]=W[blk.b+k][:2]
    # interpolate gaps
    i=0
    while i<len(T):
        if T[i] is None:
            j=i
            while T[j] is None: j+=1
            s0=T[i-1][1]; e0=T[j][0]; L=j-i
            for k in range(L): T[i+k]=[s0+(e0-s0)*k/L, s0+(e0-s0)*(k+1)/L]
            print(plat,'fill',toks[i:j]); i=j
        i+=1
    out=[[round(t[0],3),round(t[1],3),w] for t,w in zip(T,toks)]
    json.dump(out,open(f'words_en_{plat}.json','w'))
