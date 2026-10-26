# Long video cues: "Dussehra Is NOT One Story. It's Three."  Scenes anchored to spoken phrases.
import anim_long as AN
RED = (240, 72, 56); AMBER = (255, 178, 36); GREEN = (120, 210, 120); CREAM = (244, 241, 234)

# ---- credits ----
PEX = 'Pexels'
CR = dict(
    E2='Ravana erupts · Pete Birkinshaw · CC BY 2.0 · Wikimedia Commons',
    E3='Ravana fizzles · Pete Birkinshaw · CC BY 2.0 · Wikimedia Commons',
    E4='Ravan Dahan · Hetavee · CC0 · Wikimedia Commons',
    E5='Burning of Ravan · DiplomatTesterMan · CC BY-SA 4.0 · Wikimedia Commons',
    P3='Mysore Dasara procession · Kalyan Kumar · CC BY-SA 2.0 · Wikimedia Commons',
    P6='Shami leaves · J.M.Garg · CC BY-SA 3.0 · Wikimedia Commons',
    P10a='Ramlila performance · PKritika · CC BY-SA 4.0 · Wikimedia Commons',
    P10b='A scene of Ramlila · TarunNTL1998 · CC BY-SA 4.0 · Wikimedia Commons',
    P11='Tulsidas composing the Ramcharitmanas · bazaar art, 1940s · Public domain',
    P12='Ramcharitmanas illustration, Jodhpur c.1775 · Mehrangarh Museum Trust · Public domain',
    P13='Ram Leela at Ramnagar · James Prinsep, 1834 · Public domain',
    P14='Ramnagar Fort · Dksahani18 · CC BY-SA 4.0 · Wikimedia Commons',
    BAS='Bastar Dussehra · Sushil.skk · CC BY-SA 4.0 · Wikimedia Commons',
    BAIJ='Baijnath Temple · Shivendujha · CC BY-SA 4.0 · Wikimedia Commons',
    RV_P1='Bisrakh Ravana Temple · Deepak Prayagi · CC BY 3.0 · Wikimedia Commons',
    RV_P2='Ravana statue, Mandsaur · Rohit MDS · CC BY-SA 4.0 · Wikimedia Commons',
    W_dibba1='Mahanavami Dibba, Hampi · Wingedtree · CC BY-SA 4.0 · Wikimedia Commons',
    W_dibba2='Mahanavami Dibba · Soham Banerjee · CC BY 2.0 · Wikimedia Commons',
    W_bathukamma1='Bathukamma, Telangana · Lsprasath · CC BY-SA 4.0 · Wikimedia Commons',
    W_bathukamma2='Engili pula Bathukamma · Chanduclicks · CC BY-SA 4.0 · Wikimedia Commons',
    W_trinidad='Newly arrived indentured labourers, Trinidad · Public domain',
    W_kullu='Kullu Dussehra procession · Kondephy · CC BY-SA 3.0 · Wikimedia Commons',
)
def img(name, dim=.3, focus=(.5, .5), fit=False, zoom=(1.0, 1.08)):
    return ('img', name + ('.jpg' if '.' not in name else ''), dim, focus, fit, zoom)
def clip(cid, dim=.3): return ('clip', cid, dim)
def credit_of(name):
    n = name.split('.')[0]
    if n in CR: return CR[n]
    if n.startswith(('P_', 'V_')) or n in ('garba',): return PEX
    return None

CHAPTERS = {'en': ['INTRO', 'THE NAME', 'RAMA', 'DURGA', 'PANDAVAS', 'MYSURU', 'HAMPI', 'RAMLILA', 'KOLKATA', '9 NIGHTS', 'RAVANA', 'THE PATTERN'],
            'te': ['మొదలు', 'పేరు', 'రాముడు', 'దుర్గమ్మ', 'పాండవులు', 'మైసూర్', 'హంపి', 'రామ్‌లీలా', 'కొలకత్తా', '9 రాత్రులు', 'రావణుడు', 'పాటర్న్']}

def get_cues(lang, A):
    """A(phrase) -> time. Phrases are in the spoken language."""
    te = lang == 'te'
    L = (lambda en, tel: tel if te else en)
    S = []
    def sc(t, bg, kind='head', **kw):
        d = dict(t=t, bg=bg, kind=kind); d.update(kw)
        if bg[0] == 'img' and 'credit' not in d: d['credit'] = credit_of(bg[1])
        if bg[0] == 'img' and bg[1].startswith(('L_', 'A_')): d['ai'] = True
        S.append(d); return d
    P = A.p   # phrase dictionary for this language: P[key] -> time
    ch = lambda i: dict(chap=i)

    # ---------------- INTRO (hook) ----------------
    pins = [(L('RAJASTHAN', 'రాజస్థాన్'), 75.8, 25.2, P['raj'], L('100+ FT RAVANA', '100+ అడుగుల రావణుడు'), 'l'),
            (L('KOLKATA', 'కొలకత్తా'), 88.36, 22.57, P['kol'], L('DURGA TO THE RIVER', 'నదిలోకి దుర్గమ్మ'), 'r'),
            (L('MYSURU', 'మైసూర్'), 76.64, 12.3, P['mys'], L('750 KG HOWDAH', '750 కిలోల అంబారీ'), 'r'),
            (L('NEPAL', 'నేపాల్'), 85.32, 27.71, P['nep'], L('RED TIKA', 'ఎర్రటి తిలకం'), 'ru'),
            (L('TELANGANA', 'తెలంగాణ'), 78.47, 17.38, P['tel'], L('JAMMI = GOLD', 'జమ్మి = బంగారం'), 'r')]
    sc(0.0, clip('crowd', .0), 'big', big=L('ONE DAY', 'ఒకే ఒక రోజు'), lab=L('EVERY AUTUMN', 'ప్రతి సంవత్సరం'), bpx=230, bd=.0, sfx=False, **ch(0))
    sc(P['strange'], ('anim',), 'anim', fn='india_hook', args=dict(pins=[(a, b, c, P['strange'] + .1 + i * .3, None, f) for i, (a, b, c, d, e, f) in enumerate(pins)]),
       title=(L('ONE DAY', 'ఒకే ఒక రోజు'), L('ACROSS INDIA', 'ఇండియా అంతా')))
    sc(P['raj'], img('E4', .15), 'place', name=L('RAJASTHAN', 'రాజస్థాన్'), state=L('100+ FT RAVANA', '100+ అడుగుల రావణుడు'))
    sc(P['flames'], img('E2', .05), boom=True)
    sc(P['kol'], clip('durgaproc', .2), 'place', name=L('KOLKATA', 'కొలకత్తా'), state=L('WEST BENGAL', 'పశ్చిమ బెంగాల్'))
    sc(P['mys'], clip('mysore', .2), 'place', name=L('MYSURU', 'మైసూర్'), state=L('KARNATAKA', 'కర్ణాటక'))
    sc(P['howdah'], img('P3', .45, fit=True), 'big', big='~750 KG', lab=L('GOLDEN HOWDAH', 'బంగారు అంబారీ'), bpx=220)
    sc(P['nep'], img('P_dashain_family', .2, (.5, .25)), 'place', name=L('NEPAL', 'నేపాల్'), state=L('DASHAIN', 'దశైన్'))
    sc(P['grass'], img('P_dashain_tika', .2))
    sc(P['tel'], img('P6', .25), 'place', name=L('TELANGANA', 'తెలంగాణ'), state=L('JAMMI LEAVES = GOLD', 'జమ్మి ఆకులు = బంగారం'))
    # recap on the map: all five pins drop fast
    tq = P['onefest']; S.append(dict(t=tq, bg=('anim',), kind='anim', fn='india_hook', args=dict(pins=[(a, b, c, tq + .15 + i * .22, e, f) for i, (a, b, c, d, e, f) in enumerate(pins)]),
                                     title=(L('ONE FESTIVAL?', 'ఒకే పండుగా?'), L('HOW?', 'ఎలా?'))))
    sc(P['notone'], img('L_villains', .55), 'big', big=L('NOT ONE STORY', 'ఒక్క కథ కాదు'), bpx=150, bcol=RED)
    sc(P['three'], ('anim',), 'anim', fn='three_lines', args=dict(lanes=[(L('RAMA', 'రాముడు'), L('DEFEATS RAVANA', 'రావణ సంహారం'), P['three'] + .2, RED),
                                                                        (L('DURGA', 'దుర్గమ్మ'), L('DEFEATS MAHISHASURA', 'మహిషాసుర సంహారం'), P['three'] + .7, AMBER),
                                                                        (L('PANDAVAS', 'పాండవులు'), L('THE SHAMI TREE', 'జమ్మి చెట్టు'), P['three'] + 1.2, GREEN)],
                                                                 day_lab=(L('DAY 10', '10వ రోజు'), L('VIJAYADASHAMI', 'విజయదశమి')), t_day=P['three'] + 1.4))
    sc(P['explain'], ('black',), 'why', sfx=True)

    # ---------------- THE NAME ----------------
    sc(P['name'], img('P_aarti', .6, (.5, .4)), 'chapter', num=L('CLUE #1', 'క్లూ #1'), title=L('THE NAME', 'పేరు'), **ch(1))
    sc(P['dcomes'], ('anim',), 'anim', fn='word_merge', args=dict(parts=[(L('DASHA', 'దశ'), L('10', 'పది'), min(P['dasha'], P['dcomes'] + .35)), (L('HARA', 'హర'), L('DEFEAT', 'ఓడించడం'), P['hara'])],
                                                                 result=(L('DUSSEHRA', 'దసరా'), P['defeat10']), sub=L('THE DEFEAT OF THE 10-HEADED ONE', 'పది తలల వాడిని ఓడించడం')))
    sc(P['vijaya'], ('anim',), 'anim', fn='word_merge', args=dict(parts=[(L('VIJAYA', 'విజయ'), L('VICTORY', 'విజయం'), P['vijaya'] + .1), (L('DASHAMI', 'దశమి'), L('10TH DAY', 'పదో రోజు'), P['vijaya'] + .5)],
                                                                   result=(L('VIJAYADASHAMI', 'విజయదశమి'), P['victory10'] + .6), sub=L('VICTORY ON THE 10TH DAY', 'పదో రోజు విజయం')))
    sc(P['monsoon'], clip('monsoon', .25))
    sc(P['harvest'], clip('paddy', .2))
    sc(P['newbeg'], img('P_aarti', .3, (.5, .4)), 'big', big=L('NEW BEGINNINGS', 'కొత్త మొదలు'), bpx=130)
    sc(P['day10'], ('anim',), 'anim', fn='three_lines', args=dict(lanes=[(L('STORY 1', 'కథ 1'), '?', P['day10'] + .9, RED), (L('STORY 2', 'కథ 2'), '?', P['day10'] + 1.3, AMBER), (L('STORY 3', 'కథ 3'), '?', P['day10'] + 1.7, GREEN)],
                                                                day_lab=(L('DAY 10', '10వ రోజు'), L('VIJAYADASHAMI', 'విజయదశమి')), t_day=P['day10'] + .1))

    # ---------------- STORY 1: RAMA ----------------
    sc(P['first'], img('L_setu', .55), 'chapter', num=L('STORY 1', 'కథ 1'), title=L('RAMA VS RAVANA', 'రాముడు vs రావణుడు'), **ch(2))
    sc(P['kidnap'], img('L_villains', .25, (.5, .5), zoom=(1.15, 1.3)))
    sc(P['rama'], img('L_setu', .2, (.4, .5)))
    sc(P['sea'], img('L_setu', .15, (.8, .5), zoom=(1.1, 1.2)))
    sc(P['kills'], img('E3', .15))
    sc(P['tradvic'], img('L_inner_ravana', .3, (.6, .4)), 'big', big=L('VIJAYADASHAMI', 'విజయదశమి'), lab=L('TRADITION SAYS', 'సంప్రదాయం ప్రకారం'), bpx=130)
    sc(P['ramlila1'], img('P10b', .25, fit=True))
    sc(P['effigy1'], img('E5', .1))

    # ---------------- STORY 2: DURGA ----------------
    sc(P['east'], clip('durgaidol', .35), 'chapter', num=L('STORY 2', 'కథ 2'), title=L('DURGA VS MAHISHASURA', 'దుర్గమ్మ vs మహిషాసురుడు'), **ch(3))
    sc(P['buffalo'], img('L_villains', .2, (.0, .4), zoom=(1.35, 1.45)), 'big', big=L('MAHISHASURA', 'మహిషాసురుడు'), lab=L('THE BUFFALO DEMON', 'దున్నపోతు రాక్షసుడు'), bpx=140, by=760)
    sc(P['boon'], ('anim',), 'anim', fn='loophole', args=dict(slots=[(L('NO MAN', 'ఏ మగవాడూ'), False, P['noman']), (L('NO GOD', 'ఏ దేవుడూ'), False, P['nogod'])]))
    sc(P['heavens'], img('L_villains', .3, (.0, .3), zoom=(1.2, 1.3)))
    sc(P['combined'], img('L_durga_birth', .15))
    sc(P['notman'], img('L_durga_birth', .65), 'anim', fn='loophole', args=dict(slots=[(L('NO MAN', 'ఏ మగవాడూ'), False, P['notman'] - .3), (L('NO GOD', 'ఏ దేవుడూ'), False, P['notman'] - .2),
                                                                                   (L('A GODDESS', 'ఒక దేవత'), True, P['loophole'])]))
    sc(P['ninen'], img('L_durga_fight', .45), 'big', big=L('9 NIGHTS', '9 రాత్రులు'), lab=L('NAVARATRI', 'నవరాత్రులు'), bpx=200)
    sc(P['won'], img('L_durga_fight', .1, (.6, .5), zoom=(1.05, 1.18)), 'big', big=L('DAY 10', '10వ రోజు'), lab=L('SHE WON', 'అమ్మవారి విజయం'), bpx=180, by=780, bd=.6)
    sc(P['devimah'], img('P_kumartuli', .35), src=L('DEVI MAHATMYA · MARKANDEYA PURANA', 'దేవీ మహత్యం · మార్కండేయ పురాణం'))

    # ---------------- STORY 3: PANDAVAS ----------------
    sc(P['twostories'], img('L_shami', .55), 'chapter', num=L('STORY 3', 'కథ 3'), title=L('THE PANDAVAS', 'పాండవులు'), **ch(4))
    sc(P['mahab'], img('L_shami', .2, (.3, .5), zoom=(1.0, 1.1)))
    sc(P['hiding'], img('L_shami', .45, (.2, .6), zoom=(1.2, 1.3)), 'big', big=L('1 YEAR', '1 సంవత్సరం'), lab=L('IN HIDING', 'అజ్ఞాతవాసం'), bpx=220)
    sc(P['hid'], img('L_shami', .15, (.85, .4), zoom=(1.25, 1.35)))
    sc(P['jammichettu'], img('P6', .2), 'big', big=L('JAMMI CHETTU', 'జమ్మి చెట్టు'), lab=L('THE SHAMI TREE', 'శమీ వృక్షం'), bpx=150, by=760)
    sc(P['arjuna'], img('L_shami', .15, (.8, .3), zoom=(1.1, 1.2)))
    sc(P['tradconn'], img('L_shami', .45), 'big', big=L('VIJAYADASHAMI', 'విజయదశమి'), lab=L('TRADITION CONNECTS IT WITH', 'సంప్రదాయం కలిపి చెబుతుంది'), bpx=130)
    sc(P['worship'], img('P6', .25, (.3, .6), zoom=(1.1, 1.2)))
    sc(P['ayudha'], img('A_weapons_real', .3, fit=True), 'big', big=L('AYUDHA PUJA', 'ఆయుధ పూజ'), bpx=150, by=760)
    sc(P['backthen'], ('anim',), 'chips', items=[(L('WEAPONS', 'ఆయుధాలు'), P['backthen'] + .4), (L('PLOUGHS', 'నాగళ్లు'), P['plough']), (L('BOOKS', 'పుస్తకాలు'), P['books'])], title=L('THEN', 'అప్పట్లో'))
    sc(P['today'], img('A_bike', .3, fit=True), 'chips', items=[(L('BIKES', 'బైక్‌లు'), P['bikes']), (L('LAPTOPS', 'ల్యాప్‌టాప్‌లు'), P['laptops']), (L('PHONES', 'ఫోన్లు'), P['phones'])], title=L('NOW', 'ఇప్పుడు'))

    # ---------------- MYSURU ----------------
    sc(P['watch'], img('P_mysorepalace', .3), 'place', name=L('MYSURU', 'మైసూర్'), state=L('WHERE THE STORIES MEET', 'కథలు కలిసే చోటు'), **ch(5))
    sc(P['chamundi'], clip('durgaidol', .3), 'big', big=L('CHAMUNDESHWARI', 'చాముండేశ్వరి'), lab=L('THE GODDESS OF MYSURU', 'మైసూర్ అమ్మవారు'), bpx=120, by=780)
    sc(P['named'], ('anim',), 'anim', fn='word_merge', args=dict(parts=[(L('MAHISHA', 'మహిష'), L('THE BUFFALO DEMON', 'మహిషాసురుడు'), P['named'] + .8), (L('URU', 'ఊరు'), L('TOWN', 'ఊరు'), P['mahishuru'])],
                                                                         result=(L('MYSURU', 'మైసూర్'), P['thenmys']), sub=L('MAHISHURU → MYSURU', 'మహిషూరు → మైసూర్')))
    sc(P['jambu'], clip('mysore', .25), 'big', big=L('JAMBU SAVARI', 'జంబూ సవారీ'), lab=L('THE ELEPHANT PROCESSION', 'ఏనుగుల ఊరేగింపు'), bpx=140, by=780)
    sc(P['banni'], img('L_mysore_banni', .2, (.3, .5)), 'big', big=L('BANNIMANTAP', 'బన్నిమంటప్'), bpx=130, by=800, bd=.4)
    sc(P['shami2'], img('L_mysore_banni', .1, (.2, .4), zoom=(1.2, 1.3)), 'big', big=L('THE SHAMI TREE', 'శమీ వృక్షం'), lab=L("THE PANDAVAS' TREE", 'పాండవుల చెట్టు'), bpx=130, by=800)
    sc(P['oneproc'], ('anim',), 'anim', fn='three_lines', args=dict(lanes=[(L('DURGA', 'దుర్గమ్మ'), L('CHAMUNDESHWARI', 'చాముండేశ్వరి'), P['oneproc'], AMBER),
                                                                           (L('MAHABHARATA', 'మహాభారతం'), L('THE SHAMI TREE', 'శమీ వృక్షం'), P['oneproc'] + .5, GREEN)],
                                                                    day_lab=(L('ONE', 'ఒకే'), L('PROCESSION', 'ఊరేగింపు')), t_day=P['oneproc'] + .1))

    # ---------------- THE ASK ----------------
    sc(P['wait'], ('black',), 'big', big=L('WAIT.', 'ఆగండి.'), bpx=260, by=470, sfx=True, ask=True)
    sc(P['before'], img('L_paes', .7), 'big', big=L('HOW OLD?', 'ఎంత పాతది?'), bpx=170, by=440, ask=True)
    sc(P['watched'], ('black',), 'subask', tap=P['hoping'] if 'hoping' in P else P['grow'] + .8, ask=True)
    sc(P['backstory'], img('L_paes', .5), 'head', music_switch=True)

    # ---------------- HAMPI (500 years) ----------------
    sc(P['howold'], img('P_hampi', .35), 'big', big=L('500+ YEARS', '500+ ఏళ్ళు'), lab=L('AT LEAST', 'కనీసం'), bpx=200, bd=.9, **ch(6))
    sc(P['paes'], img('L_paes', .25, (.15, .5)), 'big', big='1520', lab=L('DOMINGO PAES', 'డొమింగో పేస్'), bpx=200, by=780)
    sc(P['vijayanagara'], img('P_hampi', .3), 'place', name=L('HAMPI', 'హంపి'), state=L('VIJAYANAGARA EMPIRE', 'విజయనగర సామ్రాజ్యం'))
    sc(P['feast'], img('L_paes', .25, (.6, .5), zoom=(1.15, 1.25)), 'big', big=L('9 DAYS', '9 రోజులు'), lab=L('A GREAT FEAST', 'గొప్ప పండుగ'), bpx=200, by=780)
    sc(P['platform'], img('L_paes', .15, (.45, .45), zoom=(1.3, 1.4)))
    sc(P['victoryhouse'], img('W_dibba1', .35), 'big', big=L('HOUSE OF VICTORY', 'విజయ భవనం'), bpx=120, by=780)
    sc(P['dibba'], img('W_dibba2', .3), 'place', name=L('MAHANAVAMI DIBBA', 'మహానవమి దిబ్బ'), state=L('STILL STANDING · HAMPI', 'ఇప్పటికీ హంపిలో'))
    sc(P['declined'], ('anim',), 'anim', fn='timeline', args=dict(nodes=[('1520', L('HAMPI', 'హంపి'), P['declined'] + .2), ('1610', L('SRIRANGAPATNA', 'శ్రీరంగపట్నం'), P['y1610']),
                                                                           (L('TODAY', 'ఇప్పుడు'), L('MYSURU', 'మైసూర్'), P['movedmys'])]))
    sc(P['weknow'], img('P3', .2, fit=True))

    # ---------------- RAMLILA ----------------
    sc(P['north'], img('P10a', .5, fit=True), 'chapter', num=L('NORTH INDIA', 'నార్త్ ఇండియా'), title=L('RAMLILA', 'రామ్‌లీలా'), **ch(7))
    sc(P['tulsi'], img('P11', .3, (.5, .3), fit=True), 'big', big=L('1500s', '1500లు'), lab=L('TULSIDAS · RAMCHARITMANAS', 'తులసీదాస్ · రామచరితమానస్'), bpx=200, by=780)
    sc(P['ramnagar'], img('P14', .3), 'place', name=L('RAMNAGAR', 'రాంనగర్'), state=L('NEAR VARANASI', 'వారణాసి దగ్గర'))
    sc(P['31'], img('P13', .4, fit=True), 'big', big=L('31 DAYS', '31 రోజులు'), bpx=220)
    sc(P['town'], ('anim',), 'anim', fn='town_stage', args=dict(spots=[(L('AYODHYA', 'అయోధ్య'), (380, 640), P['ayodhya']), (L('FOREST', 'అడవి'), (960, 380), P['forest']), (L('LANKA', 'లంక'), (1540, 660), P['lanka'])],
                                                                    walk_t=P['walks']))
    sc(P['family'], img('P10a', .4, fit=True), 'big', big=L('150+ YEARS', '150+ ఏళ్ళు'), lab=L('ONE FAMILY PLAYED RAVANA', 'ఒకే కుటుంబం రావణుడిగా'), bpx=200)
    sc(P['unesco08'], img('P10b', .55, fit=True), 'big', big='2008', lab='UNESCO', bpx=240, card=dict(source='UNESCO', date='2008', head=L('Ramlila, the traditional performance of the Ramayana', 'Ramlila, the traditional performance of the Ramayana'), hl=(0,)), card_t=P['unesco08'] + 1.2)
    sc(P['indentured'], img('W_trinidad', .3, fit=True), 'big', big=L('1800s', '1800లు'), lab=L('INDENTURED LABOURERS', 'కూలీలుగా విదేశాలకు'), bpx=200, by=800)
    sc(P['carried'], img('W_trinidad', .25, (.3, .6), fit=True, zoom=(1.15, 1.3)))
    sc(P['performed'], ('anim',), 'anim', fn='diaspora', args=dict(dests=[(L('TRINIDAD', 'ట్రినిడాడ్'), -61.2, 10.6, P['trinidad'], 'ru'), (L('GUYANA', 'గయానా'), -58.9, 4.9, P['guyana'], 'r'),
                                                                          ('FIJI' if not te else 'ఫిజీ', 178.0, -17.7, P['fiji'], 'l'), (L('MAURITIUS', 'మారిషస్'), 57.5, -20.2, P['mauritius'], 'l'),
                                                                          (L('SURINAME', 'సురినామ్'), -55.2, 3.9, P['suriname'], 'rd')]))

    # ---------------- KOLKATA ----------------
    sc(P['kolkata2'], img('P_howrahnight', .3), 'place', name=L('KOLKATA', 'కొలకత్తా'), state=L('DURGA PUJA', 'దుర్గా పూజ'), **ch(8))
    sc(P['unesco21'], clip('howrah', .45), 'big', big='2021', lab='UNESCO', bpx=240)
    sc(P['clay'], img('P_kumartuli', .2), 'big', big=L('GANGA CLAY', 'గంగా మట్టి'), bpx=150, by=800)
    sc(P['sonagachi'], img('P_kumartuli', .35, (.7, .5), zoom=(1.2, 1.3)), 'big', big=L('SONAGACHI', 'సోనాగాచి'), lab=L('IN SOME TRADITIONAL PUJAS', 'కొన్ని సాంప్రదాయ పూజల్లో'), bpx=150, by=780)
    sc(P['soil'], img('P_kumartuli', .25, (.15, .5), zoom=(1.3, 1.4)))
    sc(P['belief'], clip('statues', .35), 'big', big=L('GOODNESS AT THE DOORSTEP', 'గడప దగ్గర మంచితనం'), bpx=90, by=760)
    sc(P['lastday'], ('anim',), 'anim', fn='clay_cycle', args=dict(nodes=[(L('GANGA RIVER', 'గంగా నది'), P['lastday']), (L('CLAY', 'మట్టి'), P['lastday'] + .6), (L('DURGA IDOL', 'దుర్గమ్మ విగ్రహం'), P['lastday'] + 1.2),
                                                                         (L('BACK TO THE RIVER', 'మళ్ళీ నదిలోకి'), P['sameriver'])], center=(L('THE GODDESS GOES HOME', 'అమ్మవారు ఇంటికి'), P['goeshome'])))

    # ---------------- 9 NIGHTS ----------------
    days = [(L('GUJARAT', 'గుజరాత్'), 72.57, 23.02, 0, L('GARBA', 'గర్బా'), 'ld'), (L('TELANGANA', 'తెలంగాణ'), 78.47, 17.38, 0, L('BATHUKAMMA', 'బతుకమ్మ'), 'l'),
            (L('KULLU', 'కులు'), 77.1, 31.96, 0, L('STARTS ON DAY 10', 'దసరా తర్వాత మొదలు'), 'l'), (L('BASTAR', 'బస్తర్'), 82.02, 19.07, 0, L('75 DAYS', '75 రోజులు'), 'r'),
            (L('NEPAL', 'నేపాల్'), 85.32, 27.71, 0, L('15 DAYS', '15 రోజులు'), 'r')]
    tn = P['ninenights']
    sc(tn, ('anim',), 'anim', fn='india_days', args=dict(pins=[(a, b, c, tn + .3 + i * .35, e, f) for i, (a, b, c, d, e, f) in enumerate(days)]), **ch(9))
    sc(P['garba'], clip('garba', .2), 'place', name=L('GUJARAT', 'గుజరాత్'), state=L('GARBA · UNESCO 2023', 'గర్బా · UNESCO 2023'))
    sc(P['bathukamma'], img('W_bathukamma2', .25), 'place', name=L('TELANGANA', 'తెలంగాణ'), state=L('BATHUKAMMA', 'బతుకమ్మ'))
    sc(P['floats'], img('W_bathukamma1', .2))
    sc(P['kullu'], img('W_kullu', .3), 'place', name=L('KULLU', 'కులు'), state=L('STARTS WHEN OTHERS FINISH', 'అందరూ ముగించాక మొదలు'))
    sc(P['bastar'], img('BAS', .35), 'big', big=L('75 DAYS', '75 రోజులు'), lab=L('BASTAR · GODDESS DANTESHWARI', 'బస్తర్ · దంతేశ్వరి అమ్మవారు'), bpx=200)
    sc(P['nepal2'], img('P_dashain_tika', .3), 'big', big=L('15 DAYS', '15 రోజులు'), lab=L('DASHAIN · NEPAL', 'దశైన్ · నేపాల్'), bpx=200)

    sc(P['redtika2'], img('P_dashain_family', .2, (.5, .25)))

    # ---------------- RAVANA ----------------
    sc(P['andravana'], img('P_effigy2', .35), 'big', big=L('NEVER', 'ఎక్కడా లేదు'), lab=L('IN THE RAMAYANA', 'రామాయణంలో'), bpx=240, bcol=RED, bd=.6, **ch(10))
    sc(P['lastscene'], img('P10b', .3, fit=True), src=L('LAST SCENE OF RAMLILA', 'రామ్‌లీలా చివరి సీన్'))
    sc(P['bisrakh'], img('RV_P1', .3), 'place', name=L('BISRAKH', 'బిస్రఖ్'), state=L('UTTAR PRADESH', 'ఉత్తర ప్రదేశ్'))
    sc(P['mandsaur'], img('RV_P2', .3), 'place', name=L('MANDSAUR', 'మందసౌర్'), state=L('MADHYA PRADESH', 'మధ్యప్రదేశ్'))
    sc(P['baijnath'], img('BAIJ', .3, fit=True), 'place', name=L('BAIJNATH', 'బైజ్‌నాథ్'), state=L('HIMACHAL PRADESH', 'హిమాచల్ ప్రదేశ్'))
    sc(P['pray'], img('RV_P2', .45, (.5, .3), zoom=(1.15, 1.25)), 'big', big=L('THEY PRAY TO HIM', 'పూజిస్తారు'), bpx=130, by=780)

    # ---------------- THE PATTERN ----------------
    sc(P['why1'], ('anim',), 'anim', fn='three_lines', args=dict(lanes=[(L('RAMA', 'రాముడు'), L('DEFEATS RAVANA', 'రావణ సంహారం'), P['why1'] + .2, RED),
                                                                        (L('DURGA', 'దుర్గమ్మ'), L('DEFEATS MAHISHASURA', 'మహిషాసుర సంహారం'), P['why1'] + .5, AMBER),
                                                                        (L('PANDAVAS', 'పాండవులు'), L('THE SHAMI TREE', 'జమ్మి చెట్టు'), P['why1'] + .8, GREEN)],
                                                                 day_lab=(L('DAY 10', '10వ రోజు'), L('VIJAYADASHAMI', 'విజయదశమి')), t_day=P['why1']), **ch(11))
    sc(P['villain'], img('L_villains', .25), 'big', big=L('POWER', 'శక్తి'), lab=L('EVERY VILLAIN BEGINS WITH', 'ప్రతి విలన్ మొదలయ్యేది'), bpx=220, by=760)
    sc(P['ravknow'], img('L_villains', .72), 'anim', fn='power_table', args=dict(rows=[(L('RAVANA', 'రావణుడు'), L('KNOWLEDGE + A KINGDOM', 'జ్ఞానం + రాజ్యం'), P['ravknow']),
                                                                                         (L('MAHISHASURA', 'మహిషాసురుడు'), L('A BOON', 'వరం'), P['mboon']),
                                                                                         (L('KAURAVAS', 'కౌరవులు'), L('AN EMPIRE', 'సామ్రాజ్యం'), P['kempire'])]))
    sc(P['power'], ('black',), 'stack', items=[(L('POWER', 'శక్తి'), P['power'] + .1, CREAM), (L("WASN'T THE PROBLEM.", 'సమస్య కాదు.'), P['power'] + .7, CREAM),
                                               (L('WHAT THEY DID WITH IT', 'దాంతో ఏం చేశారు'), P['whatdid'], AMBER), (L('WAS.', 'అనేదే.'), P['whatdid'] + .9, AMBER)], boom=True)
    sc(P['truth'], img('L_inner_ravana', .4, (.7, .4)), 'big', big=L('THE TRUTH CATCHES UP', 'నిజమే గెలుస్తుంది'), bpx=110, by=780)
    sc(P['ramawins'], img('L_setu', .15, (.3, .5)))
    sc(P['durgawins'], img('L_durga_fight', .1, (.3, .5)))
    sc(P['pandavas2'], img('L_shami', .1, (.5, .5)))
    sc(P['thatsd'], img('E4', .3), 'stack', items=[(L('NOT THE FIRE.', 'మంటలు కాదు.'), P['notfire'], CREAM), (L('NOT THE FIREWORKS.', 'బాణసంచా కాదు.'), P['notfw'], CREAM)])
    sc(P['newbeg2'], img('P_aarti', .3, (.5, .4)), 'big', big=L('A NEW BEGINNING', 'ఒక కొత్త మొదలు'), bpx=130)
    sc(P['inside'], img('L_inner_ravana', .1), boom=True)

    # ---------------- END ----------------
    sc(P['end'], ('black',), 'cta', src=L('SOURCES & CREDITS IN DESCRIPTION', 'ఆధారాలు & క్రెడిట్స్ డిస్క్రిప్షన్‌లో'))
    for d in S:
        if d['kind'] == 'chapter': d['t'] -= .6
    S.sort(key=lambda d: d['t'])
    EV = []
    for i, s in enumerate(S):
        if s.get('card'):
            d = dict(s['card']); d['t'] = s['card_t']; d['t1'] = S[i + 1]['t']; d['y'] = 820; EV.append(d)
    return S, EV
