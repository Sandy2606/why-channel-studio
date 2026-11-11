import os, json
LANGV=os.environ.get('LANGV','en'); PLAT=os.environ.get('PLAT','yt')
LEAD=0.15; FPS=30
ROOT='/home/claude/gs6/'
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
def PREV(key, en, te, n=1):
    """start of the word just before the named word (for 'In 1608', 'On 23 June' ...)"""
    t = AT(key, en, te, n); ws = [w for w in WORDS if w[0] < t - 0.01]; return ws[-1][0] if ws else t
KA = 'A'; KC = 'C' if has('C') else 'C2'
SC = [('hook', 0.0)]
if LANGV == 'en': SC += [('perm', PREV('A', '1608,', '') - 0.1)]
SC += [('war', (PREV('A', 'already', '') - 0.35) if LANGV == 'en' else AT('A', '', 'నిజానికి') - 0.1),
       ('farman', (PREV('A', '1717,', '') - 0.1) if LANGV == 'en' else AT('A', '', '1717లో') - 0.1),
       ('cartoon1', S('Q1') - 0.15), ('wars', S('B') - 0.1),
       ('lesson', (PREV('B', 'traders', '') - 0.1) if LANGV == 'en' else AT('B', '', 'వ్యాపారులు') - 0.1),
       ('siraj', (PREV('B', 'Bengal,', '') - 0.1) if LANGV == 'en' else AT('B', '', 'బెంగాల్‌లో') - 0.1),
       ('plassey', (AT('B', 'On', '') - 0.1) if LANGV == 'en' else AT('B', '', '1757') - 0.1),
       ('buxar', AT(KC, 'Plassey', 'ప్లాసీ') - 0.1), ('payoff', AT(KC, 'For', 'నూట') - 0.1),
       ('question', AT(KC, 'What', 'ఒకప్పుడు') - 0.1), ('tease', AT(KC, "That's", 'అక్కడి') - 0.1), ('slide', E(KC) + 0.05)]
def scene_at(t):
    cur=SC[0]
    for i,(n,s) in enumerate(SC):
        if t>=s: cur=(n,s,SC[i+1][1] if i+1<len(SC) else DUR)
    return cur
