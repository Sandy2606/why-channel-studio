# rebuild EN/TE voice in long-form pacing: natural pauses kept, punctuation-based gaps, bigger breaks at chapters
import sys, json, re; sys.path.insert(0, '/home/claude/long')
from proasm import build_long
from caps_long import en_words, Anchor
lang = sys.argv[1]
if lang == 'en':

    src = open('keep_en.py').read(); ns = {}
    exec(src.split("build('enx'")[0].replace("from proasm import build", "pass"), ns)
    keep = ns['out']; name = 'enx'
    mp = json.load(open('voice_en.wav.map.json')); ws = en_words()
    st = [m[0] for m in mp] + [1e9]
    text = [' '.join(w[2] for w in ws if st[i] - .05 <= w[0] < st[i + 1] - .05) for i in range(len(mp))]
    from phr_en import PH
else:
    from keep_te import P; keep = [k for k, _ in P]; name = 'te'; text = [t for _, t in P]
    mp = json.load(open('voice_te.wav.map.json')); st = [m[0] for m in mp] + [1e9]
    from phr_te import PH
# chapter-start pieces (from the phrase anchors used for chapters)
CH_KEYS = ['name', 'first', 'east', 'twostories', 'watch', 'howold', 'north', 'kolkata2', 'ninenights', 'andravana', 'why1', 'end']
BIG_BEFORE = ['wait', 'power', 'backstory', 'truth', 'inside']
if lang == 'en': ws_ = en_words()
else:
    from caps_long import te_words; ws_ = te_words(text, 'voice_te.wav', 'voice_te.wav.map.json')
A = Anchor(ws_); P_ = {k: A(ph) for k, ph in PH}
def piece_at(t): return max(i for i in range(len(mp)) if st[i] <= t + .05)
gaps = []
for i, t in enumerate(text):
    t = t.strip(); c = t[-1] if t else ''
    g = .48 if c in '.!' else .58 if c == '?' else .26 if c in ',:;' else .16
    gaps.append(g)
for k in CH_KEYS:
    i = piece_at(P_[k]);
    if i > 0: gaps[i - 1] = max(gaps[i - 1], .95)
for k in BIG_BEFORE:
    i = piece_at(P_[k])
    if i > 0: gaps[i - 1] = max(gaps[i - 1], .75)
# ---- dynamic pacing: fast zones (hooks, recaps, lists, asks, CTA) vs explaining pace ----
FAST = [('strange' if False else None, 'name'), ('first', 'tradvic'), ('wait', 'watched'), ('backstory', 'paes'), ('trinidad', 'kolkata2'),
        ('bisrakh', 'why1'), ('ravknow', 'power'), ('ramawins', 'newbeg2'), ('end', None)]
fast = [False] * len(text)
for a, b in FAST:
    i0 = 0 if a is None else piece_at(P_[a]); i1 = len(text) if b is None else piece_at(P_[b])
    for i in range(i0, i1): fast[i] = True
for i in range(len(text)):
    if fast[i]:
        c = text[i].strip()[-1:] if text[i].strip() else ''
        gaps[i] = .5 if c == '?' else .12          # keep the beat after a question, otherwise tight
for k in ['newbeg2', 'howold']:                     # a beat right before the reveal
    i = piece_at(P_[k]); gaps[i - 1] = max(gaps[i - 1], .6)
gaps[-1] = 0.0
print('fast pieces', sum(fast), 'of', len(fast))
json.dump(fast, open(f'/home/claude/long/fast_{lang}.json', 'w'))
build_long(name, keep, f'/home/claude/long/voice_{lang}.wav', gaps, maxgap=.5, keep_p=.36, fast=fast)
