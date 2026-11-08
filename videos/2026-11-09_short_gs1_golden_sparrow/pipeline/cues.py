import os, json
LANGV=os.environ.get('LANGV','en'); PLAT=os.environ.get('PLAT','yt')
LEAD=0.15; TAIL=0.0; FPS=30
ROOT='/home/claude/gs1s/'
M={k:(a+LEAD,b+LEAD) for k,(a,b) in json.load(open(ROOT+f'marks_{LANGV}.json')).items()}
WORDS=[[a+LEAD,b+LEAD,w,k] for a,b,w,k in json.load(open(ROOT+f'words_{LANGV}.json'))]
VOICE_END=max(b for a,b in M.values())
DUR=round(VOICE_END+0.30,3)
def S(k): return M[k][0]
def E(k): return M[k][1]
def AT(key,en,te,n=1,off=0.0,end=False):
    sub=en if LANGV=='en' else te
    if sub is None: return S(key)+off
    if isinstance(sub,float): return S(key)+sub*(E(key)-S(key))+off
    c=0
    for a,b,w,k in WORDS:
        if k==key and sub.lower() in w.lower():
            c+=1
            if c==n: return (b if end else a)+off
    raise KeyError((LANGV,key,sub))
TE=LANGV=='te'
def L(en,te): return te if TE else en
def has(k): return k in M
# scene boundaries
SC=[('hook',0.0)]
SC.append(('cartoon1',S('Q1')-0.15)); SC.append(('chart',S('1.4')-0.1))
if has('1.4e'): SC.append(('circle',S('1.4e')-0.05))
SC.append(('cartoon2',S('Q2')-0.15)); SC.append(('people',S('1.6')-0.1)); SC.append(('paper',S('1.7')-0.1))
SC.append(('cartoon3',S('Q3')-0.15)); SC.append(('reveal',S('1.8b')-0.1)); SC.append(('tease',S('T')-0.1))
SC.append(('slide',S('tease2')-0.05)); SC.append(('loop',S('L')))
def scene_at(t):
    cur=SC[0]
    for i,(n,s) in enumerate(SC):
        if t>=s: cur=(n,s,SC[i+1][1] if i+1<len(SC) else DUR)
    return cur
