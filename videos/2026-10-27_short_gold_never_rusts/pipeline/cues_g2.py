# Scene cues for Gold Short 2 "Why gold never rusts"
import json, os, re
ROOT = '/home/claude/gold2/'
PLAT = os.environ.get('PLAT', 'yt')
CR = dict(TUT='Tutankhamun mask · Roland Unger · CC BY-SA 3.0 · Wikimedia Commons',
          NBI='Niels Bohr Institute · Thue · Public domain · Wikimedia Commons',
          SIG='Signal magazine, May 1940 · Public domain · Wikimedia Commons',
          RUST='Eudes cs · Pexels', GCH='cottonbro studio · Pexels', TUBE='Mikhail Nilov · Pexels',
          B='crazy motions · Pexels (3D animation)', J='Sururi Ballidag · Pexels')

def get_cues(lang):
    TE = lang == 'te'
    if not TE:
        ws = json.load(open(ROOT + f'ven_{PLAT}.words.json'))
        norm = lambda w: re.sub(r"[^a-z0-9']", '', w.lower())
        def at(word, after=0.0):
            for s, e, w in ws:
                if s >= after - 1e-6 and norm(w).startswith(word): return s
            raise KeyError(word)
        seq = [('years', '3'), ('nail', 'leave'), ('rusty', 'rusty'), ('never', 'but'), ('reason', 'and'), ('oxy', 'see'), ('gives', 'iron'),
               ('grip', 'but'), ('cant', 'oxygen'), ('mind', 'and'), ('year', 'just'), ('hexa', 'gold'), ('split', 'so'), ('invinc', 'but'),
               ('liquid', 'there'), ('aqua', 'aqua'), ('royal', 'literally'), ('acids', 'two'), ('fav', 'and'), ('y1940', 'in'),
               ('medals', 'scientists'), ('dissolve', 'so'), ('dropin', 'dissolve'), ('leave', 'leave'), ('war', 'whole'), ('back', 'after'),
               ('came', 'literally'), ('rust2', "doesn't"), ('fade', "doesn't"), ('comes', 'keeps'), ('costly', 'no'), ('tomorrow', "i'm"), ('cta', 'if')]
        T = dict(hook=0.0); last = 0.0
        for k, w in seq: T[k] = at(w, last + .01); last = T[k]
    else:
        st = [m[0] for m in json.load(open(ROOT + f'voice_te_{PLAT}.wav.map.json'))]
        en = st[1:] + [st[-1] + 3]
        p = lambda i, f=0.0: st[i] + f * (en[i] - st[i])
        T = dict(hook=0.0, years=p(1, .2), nail=p(3), rusty=p(4), never=p(5), reason=p(6), oxy=p(7), gives=p(8), grip=p(9), cant=p(10),
                 mind=p(11), year=p(12), hexa=p(13), split=p(15), invinc=p(16), liquid=p(17), aqua=p(18), royal=p(19), acids=p(20), fav=p(21),
                 y1940=p(22), medals=p(25), dissolve=p(27), dropin=p(28), leave=p(29), war=p(30), back=p(32), came=p(34), rust2=p(35), fade=p(36),
                 comes=p(37), costly=p(38), tomorrow=p(39), cta=p(41))
    L = (lambda e, t: t if TE else e)
    SC = [
        dict(t=T['hook'], kind='hook', bg=('still', 'tut.jpg', .1, (.5, .32), (1.0, 1.12)), credit=CR['TUT'], sfx=False),
        dict(t=T['nail'], kind='rusty', bg=('clip', 'RUST', .15, (1.0, 1.1)), credit=CR['RUST']),
        dict(t=T['never'], kind='big', bg=('clip', 'GCH', .25, (1.0, 1.1)), big=L('NEVER', 'పట్టదు!'), bcol='amber', bpx=200 if not TE else 170, by=640, bd=.25, stamp=True, lab=L('GOLD?', 'గోల్డ్‌కి?'), credit=CR['GCH']),
        dict(t=T['reason'], kind='plain', bg=('still', 'tut.jpg', .45, (.5, .28), (1.25, 1.35)), credit=CR['TUT']),
        dict(t=T['oxy'], kind='ironox', bg=('glow',)),
        dict(t=T['grip'], kind='goldox', bg=('glow',)),
        dict(t=T['mind'], kind='proof', bg=('stars',)),
        dict(t=T['hexa'], kind='hexa', bg=('glow',)),
        dict(t=T['invinc'], kind='big', bg=('clip', 'B', .35, (1.0, 1.1)), big=L('NOT INVINCIBLE', 'కానీ...'), bcol='cream', bpx=104 if not TE else 150, by=560, bd=.3, credit=CR['B']),
        dict(t=T['liquid'], kind='aqua', bg=('clip', 'TUBE', .3, (1.0, 1.12)), credit=CR['TUBE']),
        dict(t=T['fav'], kind='fav', bg=('black',)),
        dict(t=T['y1940'], kind='y1940', bg=('still', 'signal.jpg', .5, (.5, .1), (1.0, 1.12)), credit=CR['SIG']),
        dict(t=T['medals'], kind='medals', bg=('still', 'nbi.jpg', .45, (.5, .5), (1.05, 1.15)), credit=CR['NBI']),
        dict(t=T['dissolve'], kind='jar', bg=('glow',)),
        dict(t=T['back'], kind='recast', bg=('glow',), sfx=False),
        dict(t=T['rust2'], kind='chips', bg=('clip', 'J', .55, (1.0, 1.1)), credit=CR['J']),
        dict(t=T['tomorrow'], kind='big', bg=('clip', 'B', .45, (1.05, 1.15), 5.0), big=L('TOMORROW', 'రేపు'), bcol='amber', bpx=150, by=560, bd=.4, lab=L('THE FULL GOLD STORY', 'గోల్డ్ ఫుల్ స్టోరీ'), credit=CR['B']),
        dict(t=T['cta'], kind='cta', bg=('grid', ['J', 'GCH', 'B', 'RUST'], .72), src=L('SOURCES & CREDITS IN DESCRIPTION', 'సోర్సెస్ & క్రెడిట్స్ డిస్క్రిప్షన్‌లో')),
    ]
    return SC, T
