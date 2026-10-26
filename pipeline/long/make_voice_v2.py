# Build a long-form voice with the Why? Pace Model and print a report against the targets.
import sys, json; sys.path.insert(0, '/home/claude/long')
from proasm import build_long
from caps_long import en_words, te_words, Anchor
import pacing
lang = sys.argv[1]; texts = json.load(open(f'pieces_{lang}.json'))
fmap = json.load(open(f'voice_{lang}_fast.map.json')); st = [m[0] for m in fmap]
if lang == 'en':
    ns = {}; exec(open('keep_en.py').read().split("build('enx'")[0].replace('from proasm import build', 'pass').replace("len(sys.argv)>1 and sys.argv[1]=='fixed'", 'True'), ns)
    keep = ns['out']; name = 'enx'; ws = en_words(); from phr_en import PH
else:
    from keep_te import P; keep = [k for k, _ in P]; name = 'te'
    ws = te_words(texts, 'voice_te_fast.wav', 'voice_te_fast.map.json'); from phr_te import PH
# anchor on the piece texts themselves (timeline-independent): word k of piece i gets time st[i] + k*1e-3
ws = [(st[i] + k * 1e-3, st[i] + k * 1e-3, w) for i, t in enumerate(texts) for k, w in enumerate(t.split())]
A = Anchor(ws); T = {k: A(ph) for k, ph in PH}
pa = lambda k: max(i for i in range(len(st)) if st[i] <= T[k] + .05)
marks = dict(hook_end=pa('name'), ask=pa('wait'), ask_end=pa('howold'), cta=pa('end'),
             chapters=[pa(k) for k in ['name', 'first', 'east', 'twostories', 'watch', 'howold', 'north', 'kolkata2', 'ninenights', 'andravana', 'why1', 'end']],
             tease=[(pa('first'), pa('tradvic'))],
             lists=[(pa('trinidad'), pa('kolkata2')), (pa('bisrakh'), pa('why1')), (pa('ravknow'), pa('power')), (pa('ramawins'), pa('newbeg2'))],
             reveal=[pa('power'), pa('newbeg2'), pa('inside')])
dur = [b - a for a, b in zip(st, st[1:] + [st[-1] + 3])]
role, gaps, intra = pacing.plan(texts, marks, dur)
json.dump(role, open(f'roles_{lang}.json', 'w'))
build_long(name, keep, f'/home/claude/long/voice_{lang}.wav', gaps, intra=intra)
import scipy.io.wavfile as wf
sr, a = wf.read(f'voice_{lang}.wav'); total = len(a) / sr
om = json.load(open(f'voice_{lang}.wav.map.json'))
from collections import Counter
print('roles', dict(Counter(role)))
print('report', pacing.report(texts, role, om, total, lang), 'total', round(total, 1))
fst = sum(dur); print('slowdown vs fast edit', round(total / (fmap and (json.load(open(f'voice_{lang}_fast.map.json'))[-1][0] + 3)), 2))
dp = sum(1 for g in gaps if g >= .6); print('deliberate pauses/min', round(dp / (total / 60), 1))
for i, (r, t) in enumerate(zip(role, texts)):
    if r != 'EXPLAIN': print('  ', i, r, round(gaps[i], 2), t[:60])
