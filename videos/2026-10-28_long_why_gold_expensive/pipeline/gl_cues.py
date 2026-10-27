# Scene cues for the gold long video. Pieces are keyed by their English text prefix; Telugu pieces carry the same keys.
import json, re
ROOT = '/home/claude/goldL/'

def anchors(lang):
    keys = json.load(open(ROOT + f'keys_{lang}.json'))              # one key per piece (EN text for EN)
    mp = json.load(open(ROOT + f'voice_{lang}.wav.map.json')); st = [m[0] for m in mp]
    import scipy.io.wavfile as wf
    sr, a = wf.read(ROOT + f'voice_{lang}.wav'); total = len(a) / sr
    en = st[1:] + [total]
    ws = json.load(open(ROOT + 'ven.words.json')) if lang == 'en' else []
    norm = lambda w: re.sub(r"[^a-z0-9']", '', w.lower())
    def idx(prefix):
        for i, k in enumerate(keys):
            if k.startswith(prefix): return i
        raise KeyError(prefix)
    def K(prefix, frac=0.0, word=None, nth=0):
        i = idx(prefix)
        if word and ws:
            hits = [s for s, e, w in ws if st[i] - .15 <= s < en[i] + .05 and norm(w).startswith(word)]
            if len(hits) > nth: return hits[nth]
        return st[i] + frac * (en[i] - st[i])
    def E(prefix): i = idx(prefix); return en[i]
    return K, E, total

def get_cues(lang):
    K, E, total = anchors(lang); TE = lang == 'te'
    L = (lambda e, t: t if TE else e)
    SC = []
    def add(t, kind, bg, **kw): SC.append(dict(t=t, kind=kind, bg=bg, **kw))
    CRN = "NASA Goddard / CI Lab"; PX = 'Pexels'
    # ---------- cold open ----------
    add(0.0, 'plain', ('clip', 'FC', .15, (1.0, 1.08)), credit='Pexels')
    add(K('In January'), 'price5k', ('clip', 'B', .55, (1.0, 1.1)), credit='crazy motions · Pexels (3D)',
        t_gram=K("that's about 31", word='31'), t_cross=K('crossed', .7, word='cross'), t_first=K('For the first'))
    add(K('And think about'), 'notfood', ('clip', 'GC', .45, (1.0, 1.1)), credit='cottonbro studio · Pexels',
        t_metal=K('Gold is just'), t_eat=K("We can't eat"), t_cars=K("We can't run"))
    add(K('And yet the whole'), 'plain', ('clip', 'ST', .1, (1.0, 1.1)), credit='Pexels')
    add(K('So why is gold so expensive'), 'big', ('clip', 'J', .5, (1.0, 1.08)), big=L('WHY SO EXPENSIVE?', 'ఎందుకు ఇంత కాస్ట్లీ?'), bpx=150, bd=.15, credit='Sururi Ballidag · Pexels')
    add(K('I went really'), 'plain', ('clip', 'R', .05, (1.0, 1.12)), credit='Kat IE · Pexels', shine=K('And the answer'))
    add(K("Let's go.") + .75, 'jhintro', ('black',), sfx=False, nocap=True)
    # ---------- chapter 1 ----------
    add(K('Chapter one'), 'chapter', ('stars',), num=L('CHAPTER 1', 'చాప్టర్ 1'), title=L('IT CAME FROM THE STARS', 'స్టార్స్ నుంచి వచ్చింది'), chap=1)
    add(K('So, first'), 'plain', ('clip', 'E', .1, (1.0, 1.06)), credit='Adis Resic · Pexels', pill=L('NOT FROM EARTH', 'భూమి మీద కాదు'), pill_t=K('Not from Earth'))
    add(K('Not from Earth', .45), 'plain', ('clip', 'S', .15, (1.0, 1.1)), credit='Adis Resic · Pexels', pill=L('NOT FROM THE SUN', 'సూర్యుడిలో కాదు'), pill_t=K('Not from Earth', .5))
    add(K('Stars make new'), 'fusion', ('glow',), t_H=K('hydrogen', word='hydrogen'), t_He=K('hydrogen', .22, word='helium'), t_C=K('hydrogen', .52, word='carbon'),
        t_Fe=K('hydrogen', .82, word='iron'), t_stop=K('And there, it stops'), t_heavy=K('Gold is way heavier'))
    add(K('Gold is made when'), 'nasa', ('nasa',), credit=CRN, t_crash=K('Gold is made when', word='smash', frac=.75), label=L('TWO DEAD STARS', 'రెండు చనిపోయిన స్టార్స్'))
    add(K('And in 2017'), 'y2017', ('nasa',), credit=CRN, t_away=K('130 million'))
    add(K("And here's the twist"), 'cutaway', ('stars',), t_sank=K('When Earth was young', word='sank', frac=.7))
    add(K('The gold we dig up'), 'meteor', ('clip', 'M', .05, (1.0, 1.06)), credit='Jason Pittman · Pexels')
    add(K('So, the gold we can actually'), 'plain', ('clip', 'P', .1, (1.0, 1.08)), credit='Alex Moliski · Pexels', pill=L('A THIN DUSTING NEAR THE SURFACE', 'పైపైన కొంచెం పొడి'), pill_t=K('So, the gold we can actually', .3))
    add(K("That's reason number one"), 'reason', ('clip', 'B', .5, (1.05, 1.15), 3.0), credit='crazy motions · Pexels (3D)', n='1', word=L('RARE', 'అరుదు'))
    add(K('How rare'), 'allgold', ('stars',), t_count=K('in all of history', .4), t_cube=K('Melt it into'), t_bld=K('Roughly the height'), t_all=K("That's it."))
    # ---------- chapter 2 ----------
    add(K('Chapter two'), 'chapter', ('stars',), num=L('CHAPTER 2', 'చాప్టర్ 2'), title=L('IT LASTS FOREVER', 'ఎప్పటికీ ఉంటుంది'), chap=2)
    add(K('Now, reason number two'), 'reason', ('clip', 'GC', .45, (1.0, 1.1)), credit='cottonbro studio · Pexels', n='2', word=L('NEVER DIES', 'చావు లేదు'))
    add(K('Iron rusts'), 'metals4', ('glow',), t_fe=K('Iron rusts', word='iron'), t_ag=K('Iron rusts', word='silver', frac=.35), t_cu=K('Iron rusts', word='copper', frac=.7), t_au=K('But gold holds'))
    add(K('But gold holds'), 'goldox', ('glow',), t_cant=K('But gold holds', word='grab', frac=.75))
    add(K("That's why King Tut"), 'tut', ('still', 'tut.jpg'), credit='Roland Unger · CC BY-SA 3.0 · Wikimedia Commons', t_years=K("That's why King Tut", frac=.42))
    add(K('And this matters'), 'stillhere', ('clip', 'B', .5, (1.0, 1.1)), credit='crazy motions · Pexels (3D)', t_still=K('almost all the gold'))
    add(K('It just keeps changing'), 'hands', ('clip', 'J', .55, (1.0, 1.08)), credit='Sururi Ballidag · Pexels',
        ts=[K('Coin, to necklace', 0), K('Coin, to necklace', word='necklace', frac=.3), K('Coin, to necklace', word='bar', frac=.6), K('Coin, to necklace', word='ring', frac=.85)])
    add(K('So the gold chain'), 'plain', ('clip', 'BR', .1, (1.0, 1.1)), credit='Vikash Singh · Pexels')
    add(K('Some of that gold'), 'plain', ('clip', 'FC', .2, (1.0, 1.08)), credit='Pexels', pill=L("A KING'S COIN?", 'ఒక రాజు నాణెం?'), pill_t=K('Some of that gold', .4))
    add(K('Nobody can say'), 'plain', ('clip', 'R', .1, (1.0, 1.12), 3.0), credit='Kat IE · Pexels', shine=K('Nobody can say', .6))
    # ---------- chapter 3 ----------
    add(K('Chapter three'), 'chapter', ('stars',), num=L('CHAPTER 3', 'చాప్టర్ 3'), title=L('WHY GOLD BECAME MONEY', 'గోల్డ్ డబ్బు ఎందుకు అయ్యింది'), chap=3, subpop=True)
    add(K("Okay, but here's a question"), 'plain', ('clip', 'ST', .35, (1.0, 1.1)), credit='Pexels', bigq=L('WHY GOLD?', 'గోల్డ్ నే ఎందుకు?'), bigq_t=K('why did humans pick'))
    add(K('A chemist actually'), 'ptable', ('black',), t_gas=K('Gases?'), t_liq=K('Liquids'), t_fire=K('Metals that catch'), t_rad=K('Radioactive'),
        t_common=K('Then you cut the common'), t_rare=K('And you cut the super'), t_left=K("What's left"), t_ag=K('Silver tarnishes'),
        t_pt=K('Platinum was too hard'), t_win=K('So gold wins'))
    add(K("That's why for thousands"), 'tut', ('still', 'tut.jpg'), credit='Roland Unger · CC BY-SA 3.0 · Wikimedia Commons', t_years=None)
    # ---------- chapter 4 ----------
    add(K('Chapter four'), 'chapter', ('stars',), num=L('CHAPTER 4', 'చాప్టర్ 4'), title=L('SO HARD TO GET', 'తవ్వడం చాలా కష్టం'), chap=4)
    add(K('Reason number three'), 'reason', ('clip', 'MI', .4, (1.0, 1.1)), credit='Kevin Kramer · Pexels', n='3', word=L('HARD TO GET', 'తవ్వడం కష్టం'))
    add(K('Getting gold out'), 'plain', ('clip', 'MI', .1, (1.05, 1.15), 4.0), credit='Kevin Kramer · Pexels')
    add(K('In a typical gold mine'), 'tonne', ('clip', 'CR', .35, (1.0, 1.1)), credit='Pexels', t_rock=K('In a typical gold mine', .45), t_gold=K('In a typical gold mine', .8),
        t_pep=K('a piece of gold smaller'))
    add(K('And even with giant'), 'yearly', ('clip', 'MI', .5, (1.05, 1.15), 6.0), credit='Kevin Kramer · Pexels', t_n=K('And even with giant', .6), t_pct=K('That adds less'))
    add(K("You can't just print"), 'big', ('clip', 'PR', .45, (1.0, 1.1)), big=L("CAN'T PRINT GOLD", 'గోల్డ్ ప్రింట్ చేయలేం'), bpx=130, bd=.2, stamp=True, credit='Everett Bumstead · Pexels')
    # ---------- chapter 5 ----------
    add(K('Chapter five'), 'chapter', ('stars',), num=L('CHAPTER 5', 'చాప్టర్ 5'), title=L('WHY THE PRICE KEEPS CLIMBING', 'Price ఎందుకు పెరుగుతూనే ఉంది'), chap=5)
    add(K('So gold is rare'), 'three', ('clip', 'B', .55, (1.0, 1.1)), credit='crazy motions · Pexels (3D)',
        ts=[K('So gold is rare', .1), K('So gold is rare', .4), K('So gold is rare', .7)], t_always=K('But that was always'), t_q=K('So why has the price'))
    add(K("Here's the big one"), 'banks', ('clip', 'KP', .35, (1.0, 1.1)), credit='Kindel Media · Pexels', t_buy=K('Countries are buying'))
    add(K('Central banks'), 'cbchart', ('glow',), t_470=K('used to buy around'), t_1000=K('Then from 2022'), t_860=K('And in 2025'))
    add(K('Why?'), 'scary', ('clip', 'ST', .6, (1.05, 1.15)), credit='Pexels', ts=[K('wars, rising', 0), K('wars, rising', .3), K('wars, rising', .62)])
    add(K('gold is the one thing'), 'big', ('clip', 'B', .5, (1.0, 1.1), 4.0), big=L("NOBODY'S PROMISE", 'ఎవరి promise కాదు'), bpx=130, bd=.6, credit='crazy motions · Pexels (3D)')
    add(K('A government can print'), 'printvs', ('clip', 'PR', .5, (1.0, 1.1)), credit='Everett Bumstead · Pexels', t_gold=K('A government can print', .55))
    add(K('So the price took off'), 'pricechart', ('glow',), t_19=K('In 2019'), t_26=K('In January 2026'), t_now=K("It's come down"), t_x3=K("But that's still almost"))
    # ---------- chapter 6 ----------
    add(K('Chapter six'), 'chapter', ('stars',), num=L('CHAPTER 6', 'చాప్టర్ 6'), title=L("AND THEN THERE'S INDIA", 'ఇక మన India'), chap=6)
    add(K('And for us in India'), 'plain', ('clip', 'BR', .15, (1.0, 1.1), 4.0), credit='Vikash Singh · Pexels', pill=L("IT'S FAMILY", 'అది కుటుంబం'), pill_t=K('And for us in India', .7))
    add(K('Weddings'), 'festivals', ('clip', 'J', .55, (1.0, 1.08)), credit='Sururi Ballidag · Pexels',
        ts=[K('Weddings', 0), K('Weddings', .2), K('Weddings', .45)], t_date=K('Weddings', .75))
    add(K('Gold gets passed'), 'plain', ('clip', 'BR', .1, (1.1, 1.2), 8.0), credit='Vikash Singh · Pexels')
    add(K('India is one of the two'), 'top2', ('glow',), t_cn=K('India is one of the two', .8))
    add(K('So when you see gold'), 'plain', ('clip', 'ST', .2, (1.0, 1.1), 2.0), credit='Pexels')
    # ---------- ending ----------
    add(K('So, why is gold so expensive'), 'chapter', ('stars',), num=L('SO...', 'మరి...'), title=L('WHY IS GOLD SO EXPENSIVE?', 'Gold ఎందుకు ఇంత costly?'), chap=7)
    add(K('It was made in exploding'), 'recap', ('glow',), ts=[K('It was made in exploding'), K("There's very little"), K('It never rots'), K("It's brutal to dig"), K('And the moment the world')])
    add(K('That combination'), 'big', ('clip', 'B', .45, (1.05, 1.15), 2.0), big=L('NOTHING ELSE HAS IT', 'ఇంకే వస్తువుకీ లేదు'), bpx=130, bd=.9, credit='crazy motions · Pexels (3D)', shine=K('Nothing else on Earth'))
    add(K('If you like learning'), 'cta', ('grid', ['B', 'BR', 'N', 'J'], .72), src=L('SOURCES & CREDITS IN DESCRIPTION', 'సోర్సెస్ & క్రెడిట్స్ డిస్క్రిప్షన్‌లో'))
    return SC, total
