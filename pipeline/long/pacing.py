"""Why? Pace Model v1 — dynamic narration pacing for long-form explainers.

Evidence it is built on:
- Popular English YouTube speech runs ~171 wpm median (captions study); entertainment ~154; TED top talks ~175.
- Explainer / documentary narration is advised at ~135–160 wpm; technical explanation 120–140.
- Deliberate pauses are 0.6–1.5 s at clause/sentence ends, 3–6 per minute is the healthy band;
  pause length follows structure (longest at major breaks, shortest inside phrases).
- Speakers who hold attention speed up to build interest and slow down for weight/impact.
- Calibration to the narrator's own raw delivery: ~0.6 s after '.', ~0.4 s after ',', ~0.66 s after '?'.

Each spoken piece gets a ROLE; the role sets (a) the pause after it, (b) how much of its internal
pauses are kept. Structural markers (chapter starts, reveals) add a breath before them.
"""
import re

ROLE_RULES = {
    # Pace Model v2: fast baseline (viewer feedback: v1 at 159 wpm felt slow), beats only where they do work
    #            after '.'  after '?'  after ','  no punct   intra: (cap, keep)
    'HOOK':     dict(dot=.12, q=.45, comma=.08, none=.06, intra=(.16, .10)),
    'LIST':     dict(dot=.14, q=.45, comma=.10, none=.08, intra=(.16, .10)),
    'TEASE':    dict(dot=.14, q=.45, comma=.10, none=.08, intra=(.16, .10)),
    'ASK':      dict(dot=.20, q=.35, comma=.14, none=.10, intra=(.25, .16)),
    'CTA':      dict(dot=.14, q=.35, comma=.10, none=.08, intra=(.16, .10)),
    'EXPLAIN':  dict(dot=.18, q=.45, comma=.10, none=.08, intra=(.20, .12)),
    'QUESTION': dict(dot=.45, q=.50, comma=.20, none=.14, intra=(.30, .20)),
    'PUNCH':    dict(dot=.40, q=.50, comma=.20, none=.14, intra=(.30, .20)),
}
CHAPTER_BREATH = 1.30     # before a new chapter
REVEAL_BREATH = .50       # before a punchline / answer
TARGETS = dict(overall=(175, 190), EXPLAIN=(170, 185), fast=(190, 260), deliberate_per_min=(1.5, 4))

NEG = re.compile(r"\b(not|wasn't|isn't|never|no)\b|కాదు|లేదు", re.I)

def end_punct(t):
    t = t.strip()
    # ignore a dangling 1–2 word fragment after the last real punctuation (alignment spill)
    m = re.search(r'[.?!,:;]["\')]*\s+(\S+\s?){1,2}$', t)
    if m: t = t[:m.start() + 1]
    return t[-1:] if t else ''

def nwords(t): return len(t.split())

def classify(texts, marks, dur=None):
    """marks: dict of structural indices -> {'hook_end','ask','ask_end','cta','chapters':[...],'tease':[...],'lists':[...]}"""
    n = len(texts); role = ['EXPLAIN'] * n
    for i in range(marks['hook_end']): role[i] = 'HOOK'
    for i in range(marks['ask'], marks['ask_end']): role[i] = 'ASK'
    for i in range(marks['cta'], n): role[i] = 'CTA'
    for a, b in marks.get('tease', []):
        for i in range(a, b): role[i] = 'TEASE'
    for a, b in marks.get('lists', []):
        for i in range(a, b): role[i] = 'LIST'
    # (auto LIST disabled: lists come from story structure marks)
    for i in range(0):
        if role[i] == 'EXPLAIN' and all((dur[j] <= 1.3) if dur else (nwords(texts[j]) <= 4) for j in (i, i + 1, i + 2)):
            role[i] = role[i + 1] = role[i + 2] = 'LIST'
    # automatic: questions get a beat; short contrast lines after a question are punchlines
    for i in range(n):
        if role[i] == 'EXPLAIN' and end_punct(texts[i]) == '?': role[i] = 'QUESTION'
    for i in range(1, n):
        if role[i] == 'EXPLAIN' and ((dur[i] <= 2.6) if dur else (nwords(texts[i]) <= 9)) and (end_punct(texts[i - 1]) == '?' or NEG.search(texts[i])):
            role[i] = 'PUNCH'
    return role

def plan(texts, marks, dur=None):
    role = classify(texts, marks, dur); n = len(texts); gaps = []; intra = []
    for i in range(n):
        r = ROLE_RULES[role[i]]; c = end_punct(texts[i])
        gaps.append(r['dot'] if c in '.!' and c else r['q'] if c == '?' else r['comma'] if c in ',:;' and c else r['none'])
        it = r['intra']
        if '?' in texts[i].strip()[:-1]: it = (max(it[0], .45), max(it[1], .35))   # keep the beat after a mid-line question
        intra.append(it)
    for i in range(1, n):
        if role[i] == 'PUNCH' and role[i - 1] not in ('HOOK', 'LIST', 'CTA'): gaps[i - 1] = max(gaps[i - 1], REVEAL_BREATH)
    for i in marks.get('reveal', []):
        if i > 0: gaps[i - 1] = max(gaps[i - 1], REVEAL_BREATH)
    for i in marks['chapters']:
        if i > 0: gaps[i - 1] = max(gaps[i - 1], CHAPTER_BREATH)
    gaps[-1] = 0.0
    return role, gaps, intra

def report(texts, role, out_map, total, lang='en'):
    """measure the built track against the targets"""
    import numpy as np
    st = [m[0] for m in out_map] + [total]; rows = {}
    for i, t in enumerate(texts):
        d = st[i + 1] - st[i]; k = 'fast' if role[i] in ('HOOK', 'LIST', 'TEASE', 'CTA') else role[i]
        w, s = rows.get(k, (0, 0)); rows[k] = (w + nwords(t), s + d)
    W = sum(nwords(t) for t in texts)
    out = {'overall_wpm': round(W / (total / 60))}
    for k, (w, s) in rows.items(): out[f'{k}_wpm'] = round(w / (s / 60))
    return out
