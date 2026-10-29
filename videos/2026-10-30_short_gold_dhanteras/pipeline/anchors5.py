
# ---------------- voice / words / anchors ----------------
VFILE = ROOT + f'voice_{LANGV}_{PLAT}.wav'
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
KEYS = {  # key: (EN word, nth, TE unit, frac or substring)
    'tonnes': ('tonnes', 1, 0, 0.7), 'add': ('add', 1, 1, 0.0),
    'america': ('america', 1, 2, 'America'), 'germany': ('germany', 1, 2, 'Germany'), 'italy': ('italy', 1, 2, 'Italy'),
    'france': ('france', 1, 2, 'France'), 'russia': ('russia', 1, 2, 'Russia'), 'china': ('china', 1, 2, 'China'),
    'switz': ('switzerland', 1, 2, 'Switzerland'), 'rbi': ('rbi', 1, 2, 'RBI'), 'japan': ('japan', 1, 2, 'Japan'), 'neth': ('netherlands', 1, 2, 'Netherlands'),
    'more': ('indian', 2, 3, 0.0), 'why': ('why', 1, 4, 0.0), 'trad': ('tradition', 1, 5, 0.3), 'math': ('math', 1, 6, 0.2),
    'say': ('say', 1, 7, 0.0), 'y2006': ('2006', 1, 7, 0.0), 'lakh': ('lakh', 1, 8, 0.7), 'nearly': ('nearly', 1, 9, 0.0),
    'same': ('same', 1, 10, 0.0), 'fd': ('fd', 1, 10, 0.25), 'k38': ('38,000', 1, 11, 0.3),
    'hidden': ('hidden', 1, 12, 0.0), 'oneprice': ('one', 1, 13, 0.0), 'rupee1': ('rupee', 1, 14, 0.0),
    'y2006b': ('2006', 2, 15, 0.0), 'd45': ('45', 1, 15, 0.6), 'd95': ('95', 1, 16, 0.5),
    'loses': ('loses', 1, 17, 0.3), 'gold2': ("doesn't", 2, 18, 0.0), 'protects': ('protects', 1, 19, 0.3),
    'cash': ('cash', 1, 20, 0.0), 'pledge': ('pledge', 1, 21, 0.0), 'minutes': ('minutes', 1, 21, 0.4), 'paper': ('paperwork', 1, 21, 0.8),
    'thats': ("that's", 1, 22, 0.0), 'second': ('second-biggest', 1, 22, 0.45), 'l16': ('16', 1, 23, 0.1),
    'next': ('next', 1, 24, 0.0), 'mom': ('mom', 1, 24, 'అమ్మ'), 'sister': ('sister', 1, 24, 'చెల్లి'), 'gf': ('girlfriend', 1, 24, 'girlfriend'),
    'wasting': ('wasting', 1, 25, 0.5), 'saving': ('saving', 1, 26, 0.0), 'future': ('future', 1, 26, 0.6),
    'full': ('full', 1, 27, 0.0), 'cta': ('if', 1, 28, 0.0), 'comment': ('comment', 1, 29, 0.0),
}
if LANGV == 'en':
    WORDS = json.load(open(ROOT + f'words_en_{PLAT}.json'))
    def norm(w): return w.strip('.,?!$%').lower()
    def T(word, n=1):
        k = 0
        for s, e, w in WORDS:
            if norm(w) == word or (word.isdigit() and norm(w).startswith(word)):
                k += 1
                if k == n: return s + LEAD
        raise KeyError(word)
    A = {key: T(w, n) for key, (w, n, u, f) in KEYS.items()}
else:
    _J = json.load(open(ROOT + f'words_te_{PLAT}.json')); WORDS = _J['words']; SS = _J['sent'] + [VOICE_LEN]; UN = _J['units']
    A = {}
    for key, (w, n, u, f) in KEYS.items():
        if isinstance(f, str): f = max(0, UN[u].find(f)) / len(UN[u])
        A[key] = SS[u] + f * (SS[u + 1] - SS[u]) + LEAD
A['end'] = DUR

CAP = []
for s, e, w in WORDS:
    w = {'tons': 'tonnes'}.get(w, w)
    CAP.append([s, e, w])
GROUPS = []; g = []; MAXC = 16 if LANGV == 'en' else 22
for i, (s, e, w) in enumerate(CAP):
    g.append((s + LEAD, e + LEAD, w))
    nxt = CAP[i + 1][0] if i + 1 < len(CAP) else 99
    if len(g) >= 3 or w[-1] in '.,?!…' or nxt - e > 0.35 or sum(len(x[2]) for x in g) > MAXC:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
K.GROUPS = GROUPS; R3.GROUPS = GROUPS; R3.TECACHE = {}
