"""word times per line. EN: whisper small.en per line, snapped to the script text. TE: script words spread over voiced runs."""
import json, sys, re, difflib
import numpy as np, soundfile as sf
LANG = sys.argv[1]
TL = json.load(open(f'tl_{LANG}.json')); SR = 48000
toks_all = []


def spread(words, runs, t0, t1):
    runs = [r for r in runs if r[1] - r[0] > 0.05] or [(t0, t1)]
    tot = sum(e - s for s, e in runs); L = [max(2, len(w)) for w in words]; S = sum(L)
    out = []; acc = 0
    def at(x):  # x in [0,tot] -> time
        for s, e in runs:
            if x <= e - s: return s + x
            x -= e - s
        return runs[-1][1]
    for w, l in zip(words, L):
        a = acc / S * tot; acc += l; b = acc / S * tot
        out.append([round(at(a), 3), round(at(b) - 0.02, 3), w])
    return out


if LANG == 'en':
    from faster_whisper import WhisperModel
    m = WhisperModel('small.en', device='cpu', compute_type='int8')
    audio, _ = sf.read('voice_en_raw.wav', dtype='float32')
    import subprocess
    for ln in TL['lines']:
        a = audio[int(ln['t0'] * SR): int(ln['t1'] * SR)]
        a16 = a[::3].copy()  # 48k -> 16k
        segs, _ = m.transcribe(a16, language='en', word_timestamps=True, beam_size=5, condition_on_previous_text=False)
        hw = [(w.start + ln['t0'], w.end + ln['t0'], w.word.strip()) for s in segs for w in s.words]
        sw = ln['text'].replace('…', '… ').split()
        def nz(x): return re.sub(r'[^a-z0-9]', '', x.lower())
        sm = difflib.SequenceMatcher(None, [nz(x) for x in sw], [nz(x[2]) for x in hw], autojunk=False)
        tm = [None] * len(sw)
        for blk in sm.get_matching_blocks():
            for k in range(blk.size): tm[blk.a + k] = hw[blk.b + k][:2]
        for op, a1, a2, b1, b2 in sm.get_opcodes():
            if op == 'replace' and a2 - a1 == b2 - b1:
                for k in range(a2 - a1): tm[a1 + k] = hw[b1 + k][:2]
        # interpolate gaps via spread over runs
        i = 0
        while i < len(sw):
            if tm[i] is None:
                j = i
                while j < len(sw) and tm[j] is None: j += 1
                s0 = tm[i - 1][1] if i > 0 else ln['t0']; s1 = tm[j][0] if j < len(sw) else ln['t1']
                rr = [(max(s, s0), min(e, s1)) for s, e in ln['runs'] if min(e, s1) > max(s, s0)]
                for k, x in enumerate(spread(sw[i:j], rr or [(s0, s1)], s0, s1)): tm[i + k] = x[:2]
                i = j
            else: i += 1
        ln['words'] = [[round(a, 3), round(b, 3), w] for (a, b), w in zip(tm, sw)]
        miss = sum(1 for x in sm.get_opcodes() if x[0] != 'equal')
        if miss > 2: print('check', ln['n'], ' '.join(x[2] for x in hw)[:120])
else:
    for ln in TL['lines']:
        sw = ln['text'].replace('…', '… ').split()
        ln['words'] = spread(sw, ln['runs'], ln['t0'], ln['t1'])
json.dump(TL, open(f'tl_{LANG}.json', 'w'), ensure_ascii=False, indent=1)
print('ok', sum(len(l['words']) for l in TL['lines']))
