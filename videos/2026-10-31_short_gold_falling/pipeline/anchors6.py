
# ---------------- voice / words / anchors ----------------
VFILE = ROOT + f'voice_{LANGV}_{PLAT}.wav'
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
SUBW = 'subscribe' if PLAT == 'yt' else 'follow'
KEYS = {  # key: (EN word, nth, TE unit, frac)
    'below': ('below', 1, 2, 0.0), 'thirty': ('30', 1, 3, 0.3), 'safest': ('safest', 1, 4, 0.4),
    'r1': ('one', 1, 5, 0.0), 'fd': ('fd', 1, 7, 0.0), 'sits': ('sits', 1, 8, 0.4),
    'rates': ('rates', 1, 9, 0.3), 'fed': ('fed', 1, 10, 0.1), 'y2023': ('2023', 1, 10, 0.5),
    'r2': ('two', 1, 11, 0.0), 'oil': ('oil', 1, 12, 0.5), 'hikes': ('hikes', 1, 13, 0.6),
    'r3': ('three', 1, 14, 0.0), 'cash': ('cash', 1, 15, 0.7), 'easiest': ('easiest', 1, 16, 0.3), 'sold': ('sell', 1, 17, 0.0),
    'rushed': ('rushed', 1, 18, 0.3), 'out': ('out', 1, 18, 0.85),
    'nobody': ("nobody's", 1, 19, 0.0), 't63': ('63', 1, 20, 0.5), 'most': ('most', 1, 21, 0.0),
    'traders': ('traders', 1, 22, 0.0), 'buying': ('buying', 1, 22, 0.6),
    'y2011': ('2011', 1, 24, 0.0), 'nine': ('nine', 2, 25, 0.2), 'y2020': ('2020', 1, 25, 0.8), 'x17': ('17', 1, 26, 0.7),
    'updown': ('down', 1, 27, 0.0), 'years': ('years', 3, 28, 0.7),
    'secrets': ('secrets', 1, 29, 0.0), 'q1': ('olympic', 1, 30, 0.0), 'q2': ('andhra', 1, 31, 0.0), 'q3': ('scientists', 1, 33, 0.0),
    'another': ('another', 1, 34, 0.0), 'comment': ('comment', 1, 35, 0.3),
    'wrap': ('wrap', 1, 36, 0.0), 'sched': ('if', 2, 38, 0.0), 'sub': (SUBW, 1, 40, 0.0),
}
if LANGV == 'en':
    WORDS = json.load(open(ROOT + f'words_en_{PLAT}.json'))
    def norm(w): return w.strip('.,?!$%"…').lower()
    def T(word, n=1):
        k = 0
        for s, e, w in WORDS:
            if norm(w) == word or (word.isdigit() and norm(w).replace(',', '').startswith(word)):
                k += 1
                if k == n: return s + LEAD
        raise KeyError(word)
    A = {key: T(w, n) for key, (w, n, u, f) in KEYS.items()}; A['sold'] += 0.45
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
