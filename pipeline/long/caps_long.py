# caption words for the long video (EN from whisper on the final voice + phrase fixes; TE from script lines per piece)
import json, re, os, numpy as np, scipy.io.wavfile as wf
ROOT = '/home/claude/long/'

def norm(t): return re.sub(r"[^\w']", '', t.lower())

EN_SUBS = [  # (heard, written)
    ('hoda', 'howdah'), ('tikka', 'tika'), ('gemmy', 'Jammi'), ('dasara', 'Dussehra'), ('dasra', 'Dussehra'), ('dasaras', "Dussehra's"),
    ('10 headed womb', '10-headed one.'), ('vijay dashmi', 'Vijayadashami'), ('maisha sura', 'Mahishasura,'), ('mysasura', 'Mahishasura.'),
    ('maishasura', 'Mahishasura'), ('mahatnya', 'Mahatmya,'), ('jami', 'Jammi'), ('chaitu', 'chettu.'), ('adjuna', 'Arjuna'), ('aida', 'Ayudha'),
    ('bani mandap', 'Bannimantap.'), ('shime', 'Shami'), ('mahavartha', 'Mahabharata'), ('durga story', "Durga's story"), ('peis', 'Paes'),
    ('vodiar', 'Wodeyar'), ('tulsi das ram sharit manas', "Tulsidas's Ramcharitmanas"), ('ram nagar', 'Ramnagar'),
    ('within the storage', 'with the story.'), ('ram leela', 'Ramlila'), ('ram lila', 'Ramlila'), ('guwana', 'Guyana,'),
    ('go to the kolkata', 'Go to Kolkata,'), ('mirrored', 'made'), ('batkama', 'Bathukamma'), ('loads them', 'floats them'),
    ('kulu', 'Kullu'), ('basta', 'Bastar'), ('dasha in', 'Dashain,'), ('jambara', 'jamara'), ('in ravana', 'And Ravana?'),
    ('bisrak', 'Bisrakh,'), ('mansar', 'Mandsaur,'), ('bhaijnaad', 'Baijnath,'), ('ravana sefiki', "Ravana's effigy."),
    ('come on', 'came on'), ('the god combined', 'the gods combined'), ('9 nights', 'nine nights'), ('9 days', 'nine days.'),
    ('labors', 'laborers'), ('celebrate with', 'celebrates with'), ('everyday', 'every day'),
]

def en_words():
    import difflib
    ws = json.load(open(ROOT + 'ven.words.json')); A = [norm(w[2]) for w in ws]
    sc = open(ROOT + 'script_en.txt').read().split(); B = [norm(x) for x in sc]
    numfix = {'hundred': '100', '10headed': '10', 'nine': '9'}
    sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
    tim = [None] * len(B)
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == 'equal':
            for k in range(b1 - b0): tim[b0 + k] = (ws[a0 + k][0], ws[a0 + k][1])
        elif op == 'replace' and a1 > a0:
            s, e = ws[a0][0], ws[a1 - 1][1]; n = b1 - b0
            for k in range(n): tim[b0 + k] = (s + (e - s) * k / n, s + (e - s) * (k + 1) / n)
    # interpolate gaps (script words with no audio match)
    for i in range(len(B)):
        if tim[i] is None:
            j = i
            while j < len(B) and tim[j] is None: j += 1
            s = tim[i - 1][1] if i > 0 else 0.0; e = tim[j][0] if j < len(B) else s + .4 * (j - i)
            for k in range(i, j): tim[k] = (s + (e - s) * (k - i) / (j - i), s + (e - s) * (k - i + 1) / (j - i))
    return [(tim[i][0], tim[i][1], sc[i]) for i in range(len(B))]

def en_words_old():
    ws = json.load(open(ROOT + 'ven.words.json'))
    toks = [norm(w) for _, _, w in ws]; out = []; i = 0
    subs = sorted([(s.split(), r) for s, r in EN_SUBS], key=lambda x: -len(x[0]))
    while i < len(ws):
        hit = None
        for pat, rep in subs:
            if toks[i:i + len(pat)] == pat: hit = (pat, rep); break
        if hit:
            pat, rep = hit; s = ws[i][0]; e = ws[i + len(pat) - 1][1]; rw = rep.split()
            last = ws[i + len(pat) - 1][2]; tail = re.sub(r"^.*?([.,?!]*)$", r"\1", last)
            if tail and rw[-1][-1] not in '.,?!': rw[-1] += tail
            for j, r in enumerate(rw):
                out.append((s + (e - s) * j / len(rw), s + (e - s) * (j + 1) / len(rw), r))
            i += len(pat)
        else:
            out.append(tuple(ws[i])); i += 1
    return out

TE_LINES = []   # filled from keep_te.py (one script line per piece)

def te_words(lines, voice, mapf):
    sr, a = wf.read(voice); a = a.astype(np.float32) / 32768
    if a.ndim > 1: a = a.mean(1)
    hop = sr // 100; n = len(a) // hop
    db = 20 * np.log10(np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-9); vo = db > np.median(db) - 20
    mp = json.load(open(mapf)); starts = [m[0] for m in mp] + [n / 100]
    out = []
    for i, line in enumerate(lines):
        s, e = starts[i], starts[i + 1]
        fr = np.where(vo[int(s * 100):int(e * 100)])[0] / 100 + s
        if len(fr) == 0: fr = np.array([s, e])
        ws = line.split(); L = np.array([max(2, len(w)) for w in ws], float); c = np.concatenate([[0], np.cumsum(L) / L.sum()])
        for j, w in enumerate(ws):
            t0 = fr[min(len(fr) - 1, int(c[j] * (len(fr) - 1)))]; t1 = fr[min(len(fr) - 1, int(c[j + 1] * (len(fr) - 1)))]
            out.append((float(t0), float(max(t1, t0 + .12)), w, j == len(ws) - 1))
    return out

def chunks(ws, maxw=5, maxc=30):
    C = []; cur = []
    for k, x in enumerate(ws):
        cur.append(x); txt = ' '.join(y[2] for y in cur)
        nxt = ws[k + 1] if k + 1 < len(ws) else None
        brk = (len(x) > 3 and x[3]) or len(cur) >= maxw or len(txt) >= maxc or x[2][-1] in '.,?!' or (nxt and nxt[0] - x[1] > .35)
        if nxt and len(txt + ' ' + nxt[2]) > maxc + 4: brk = True
        if brk or not nxt: C.append(cur); cur = []
    out = []
    for i, c in enumerate(C):
        s = c[0][0]; e = C[i + 1][0][0] if i + 1 < len(C) else c[-1][1] + .4
        out.append((s, min(e, c[-1][1] + .6), c))
    return out

class Anchor:
    """sequential phrase lookup in caption words -> start time"""
    def __init__(self, ws): self.ws = ws; self.toks = [norm(w[2]) for w in ws]; self.i = 0
    def __call__(self, phrase, d=0.0):
        p = [norm(x) for x in phrase.split()]
        for i in range(self.i, len(self.toks)):
            if self.toks[i:i + len(p)] == p: self.i = i + 1; return self.ws[i][0] + d
        raise KeyError(f'anchor not found after #{self.i}: {phrase}')

if __name__ == '__main__':
    w = en_words(); print(len(w)); print(' '.join(x[2] for x in w))
