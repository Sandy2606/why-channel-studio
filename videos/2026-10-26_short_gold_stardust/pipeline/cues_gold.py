# Scene cues for Gold Short 1, anchored to spoken words (EN) / voice pieces (TE)
import json, os, re
ROOT = '/home/claude/gold1/'
PLAT = os.environ.get('PLAT', 'yt')
CR_NASA = "NASA's Goddard Space Flight Center / CI Lab"
CR = dict(R='Kat IE · Pexels', E='Adis Resic · Pexels', S='Adis Resic · Pexels', B='crazy motions · Pexels (3D animation)',
          M='Jason Pittman · Pexels', P='Alex Moliski · Pexels', J='Sururi Ballidag · Pexels', N=CR_NASA)

def get_cues(lang):
    TE = lang == 'te'
    if not TE:
        ws = json.load(open(ROOT + f'ven_{PLAT}.words.json'))
        norm = lambda w: re.sub(r"[^a-z0-9']", '', w.lower())
        def at(word, after=0.0, d=0.0):
            for s, e, w in ws:
                if s >= after - 1e-6 and norm(w).startswith(word): return s + d
            raise KeyError(word)
        T = dict(
            hook=0.0, notearth=at('it'), notsun=at('not', 2), explain=at('let'), stars=at('stars'), squeeze=at('squeezing'),
            H=at('hydrogen'), He=at('helium'), C=at('carbon'), Fe=at('iron'), stop=at('stops'),
            heavy=at('gold', 11), sun2=at('so', 13), where=at('so', 15.8), giant=at('when'), collapse=at('collapse'), neutron=at('neutron'),
            dense=at('so', 20), cube=at('sugar'), weigh=at('weigh'), billion=at('billion'),
            imagine=at('now'), crash=at('crash', 28), y2017=at('in', 29.5), away=at('130'),
            glow=at('and', 34), heavym=at('heavy', 37), goldw=at('gold', 38.5), twist=at('but', 39.5), young=at('when', 40.5),
            sank=at('sank'), today=at('the', 44.4), falling=at('came', 45.5), ring=at('so', 48), older=at('older'), stardust=at('it', 50.5),
            costly=at('but', 52), wed=at('the', 55.4), cta=at('if', 57.4))
    else:
        st = [m[0] for m in json.load(open(ROOT + f'voice_te_{PLAT}.wav.map.json'))]
        en = st[1:] + [st[-1] + 3]
        p = lambda i, f=0.0: st[i] + f * (en[i] - st[i])
        T = dict(
            hook=0.0, notearth=p(1), notsun=p(2), explain=p(3), stars=p(4), squeeze=p(5),
            H=p(7), He=p(7, .55), C=p(8, .6), Fe=p(9, .45), stop=p(10),
            heavy=p(11), sun2=p(12), where=p(13), giant=p(14), collapse=p(14, .5), neutron=p(14, .6),
            dense=p(15), cube=p(16), weigh=p(16, .7), billion=p(17),
            imagine=p(18), crash=p(20, .78), y2017=p(21), away=p(22),
            glow=p(23), heavym=p(23, .55), goldw=p(23, .62), twist=p(24), young=p(25),
            sank=p(25, .7), today=p(26), falling=p(27), ring=p(28), older=p(29), stardust=p(30),
            costly=p(32), wed=p(34), cta=p(35))
    L = (lambda en_, te_: te_ if TE else en_)
    SC = [
        dict(t=T['hook'], kind='plain', bg=('clip', 'R', .05, (1.0, 1.12)), credit=CR['R'], sfx=False),
        dict(t=T['notearth'], kind='big', bg=('clip', 'E', .15, (1.0, 1.06)), big=L('NOT EARTH', 'భూమి కాదు'), bcol='red', bpx=150, by=520, bd=.35, lab=L('MADE ON EARTH?', 'భూమి మీద పుట్టిందా?'), credit=CR['E']),
        dict(t=T['notsun'], kind='big', bg=('clip', 'S', .2, (1.0, 1.1)), big=L('NOT THE SUN', 'సూర్యుడు కాదు'), bcol='red', bpx=116, by=420, bd=.3, lab=L('MADE IN THE SUN?', 'సూర్యుడిలో పుట్టిందా?'), credit=CR['S']),
        dict(t=T['explain'], kind='fusion', bg=('glow',)),
        dict(t=T['heavy'], kind='scale', bg=('glow',)),
        dict(t=T['sun2'], kind='big', bg=('clip', 'S', .35, (1.08, 1.16), 3.0), big=L("CAN'T MAKE GOLD", 'గోల్డ్ తయారు కాదు'), bcol='red', bpx=86, by=430, bd=.5, lab=L('EVEN OUR SUN', 'మన సూర్యుడు కూడా'), stamp=True, credit=CR['S']),
        dict(t=T['where'], kind='why', bg=('stars',), word=L('WHERE?', 'ఎక్కడి నుంచి?')),
        dict(t=T['giant'], kind='collapse', bg=('stars',)),
        dict(t=T['dense'], kind='sugar', bg=('stars',)),
        dict(t=T['imagine'], kind='nasa1', bg=('nasa',), credit=CR_NASA),
        dict(t=T['y2017'], kind='y2017', bg=('nasa',), credit=CR_NASA, sfx=False),
        dict(t=T['glow'], kind='spectrum', bg=('nasa',), credit=CR_NASA, sfx=False),
        dict(t=T['heavym'], kind='metals', bg=('clip', 'B', .25, (1.0, 1.1)), credit=CR['B']),
        dict(t=T['twist'], kind='twist', bg=('black',), drop=True),
        dict(t=T['young'], kind='cutaway', bg=('stars',)),
        dict(t=T['today'], kind='plain', bg=('clip', 'P', .1, (1.0, 1.08)), credit=CR['P'], pill=L('THE GOLD WE MINE TODAY', 'ఈరోజు తవ్వే గోల్డ్')),
        dict(t=T['falling'], kind='meteor', bg=('clip', 'M', .05, (1.0, 1.06)), credit=CR['M']),
        dict(t=T['ring'], kind='timeline', bg=('clip', 'R', .62, (1.12, 1.18), 4.0), credit=CR['R']),
        dict(t=T['stardust'], kind='stardust', bg=('clip', 'R', .1, (1.0, 1.15), 8.0), credit=CR['R']),
        dict(t=T['costly'], kind='big', bg=('clip', 'J', .35, (1.0, 1.1)), big=L('SO WHY SO\nEXPENSIVE?', 'మరి ఇంత\nకాస్ట్లీ ఎందుకు?'), bcol='amber', bpx=120, by=470, bd=.9, credit=CR['J']),
        dict(t=T['wed'], kind='big', bg=('clip', 'B', .45, (1.05, 1.15), 5.0), big=L('WEDNESDAY', 'బుధవారం'), bcol='amber', bpx=150, by=560, bd=.45, lab=L('THE FULL VIDEO', 'ఫుల్ వీడియో')),
        dict(t=T['cta'], kind='cta', bg=('grid', ['J', 'S', 'B', 'P'], .72), src=L('SOURCES & CREDITS IN DESCRIPTION', 'సోర్సెస్ & క్రెడిట్స్ డిస్క్రిప్షన్‌లో')),
    ]
    return SC, T
