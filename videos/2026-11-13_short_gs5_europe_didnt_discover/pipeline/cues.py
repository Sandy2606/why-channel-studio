import os, json
LANGV=os.environ.get('LANGV','en'); PLAT=os.environ.get('PLAT','yt')
LEAD=0.15; FPS=30
ROOT='/home/claude/gs5/'
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
    norm=lambda s:s.lower().strip('.,?!…:;')
    exact=[x for x in WORDS if x[3]==key and norm(x[2])==norm(sub)]
    if len(exact)>=n: a,b=exact[n-1][0],exact[n-1][1]; return (b if end else a)+off
    for a,b,w,k in WORDS:
        if k==key and sub.lower() in w.lower():
            c+=1
            if c==n: return (b if end else a)+off
    raise KeyError((LANGV,key,sub))
TE=LANGV=='te'
def L(en,te): return te if TE else en
def has(k): return k in M
SC=[('hook',0.0),('cartoon1',S('Q1')-0.15),('ocean',S('53A')-0.1),('monsoon',S('5.5')-0.1),('cartoon2',S('Q2')-0.15),
    ('route',S('5.6a')-0.1),('pilot',S('PILOT')-0.1),('cartoon3',S('Q3')-0.15),('welcome',S('5.7')-0.1),('gifts',S('5.8')-0.1),
    ('old',S('5.9' if has('5.9') else 'OLD')-0.1),('force',S('FORCE')-0.1),('tease',S('tease')-0.1),('slide',E('tease')+0.05),('loop',S('L'))]
def scene_at(t):
    cur=SC[0]
    for i,(n,s) in enumerate(SC):
        if t>=s: cur=(n,s,SC[i+1][1] if i+1<len(SC) else DUR)
    return cur
