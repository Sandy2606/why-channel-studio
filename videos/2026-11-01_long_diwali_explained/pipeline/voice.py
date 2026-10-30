"""Diwali long: assemble the voice track from per-line clips (Pace Model v2 gaps), word times, envelope."""
import json, re, subprocess, sys
import numpy as np
LANG = sys.argv[1]
R = '/home/claude/why-channel-studio/'
SR = 48000
T = [t for t in json.load(open(R + 'videos/2026-11-01_long_diwali_explained/voice_takes.json')) if t[0] == LANG]
L = json.load(open('/home/claude/dwv/lines.json'))[LANG]
_LIB = {'en': [('69', 'voice_lib/en/dd84f197b924.mp3', "If you like learning things like this, we post a full video every Sunday and a new Short the other six days. So there's always something new."),
               ('69s', 'voice_lib/en/e84ee89ef316.mp3', "Subscribe, and we'll make it worth it.")],
        'te': [('69', 'voice_lib/te/9aeade589e56.mp3', 'ఇలాంటి కొత్త విషయాలు నేర్చుకోవడం నచ్చితే, ప్రతి ఆదివారం ఒక full video, మిగతా ఆరు రోజులు రోజుకో Short పెడతాం. ఎప్పుడూ ఏదో ఒక కొత్తది ఉంటుంది.'),
               ('69s', 'voice_lib/te/58abc54b4e38.mp3', 'Subscribe చేయండి, మీకు నచ్చేలా చేస్తాం.')]}[LANG]
for n_, f_, tx_ in _LIB:
    T.append((LANG, n_, f_, 0)); L.append(dict(n=n_, sp='ANNA', text=tx_))
CH_START = {'6': 1, '22': 2, '30': 3, '41': 4, '48': 5, '56': 6, '63b': 7}
PUNCH = {'21', '31', '42', '63', '57', '44'}
TEMPO = {'en': 1.06, 'te': 1.06}[LANG]
KEEP_TEMPO = {'69s'}  # library schedule CTA: regular pace on the subscribe line


def load(p, tempo=1.0):
    af = ['-af', f'atempo={tempo}'] if tempo != 1.0 else []
    return np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p] + af + ['-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'],
                                        capture_output=True).stdout, np.float32).copy()


def frames_db(a, fr):
    n = len(a) // fr
    e = np.sqrt(np.mean(a[:n * fr].reshape(-1, fr) ** 2, 1))
    return 20 * np.log10(e + 1e-9)


def tighten(a):
    """trim edges, cap internal pauses > 0.45 s to 0.40 s. returns audio + list of voiced runs (s, e) in seconds."""
    fr = int(0.01 * SR); db = frames_db(a, fr); v = db > -42
    idx = np.where(v)[0]
    s0 = max(0, idx[0] - 3) * fr; s1 = min(len(a), (idx[-1] + 6) * fr)
    a = a[s0:s1]; v = v[max(0, idx[0] - 3): max(0, idx[0] - 3) + len(a) // fr]
    # find silent runs
    out = []; runs = []; i = 0; n = len(v); cur = 0
    seg_start = 0
    while i < n:
        if not v[i]:
            j = i
            while j < n and not v[j]: j += 1
            ln = (j - i) * 0.01
            if ln > 0.45 and i > 0 and j < n:
                keep = int(0.40 * SR); x0 = i * fr; x1 = j * fr
                out.append(a[seg_start:x0 + keep // 2]); seg_start = x1 - keep // 2
            i = j
        else: i += 1
    out.append(a[seg_start:])
    b = np.concatenate(out)
    # voiced runs of the tightened clip
    db2 = frames_db(b, fr); vv = db2 > -40; runs = []; i = 0
    while i < len(vv):
        if vv[i]:
            j = i
            while j < len(vv) and (vv[j] or (j + 12 < len(vv) and vv[j:j + 12].any())): j += 1
            runs.append((i * 0.01, j * 0.01)); i = j
        else: i += 1
    return b, runs


def clean(t): return re.sub(r'\[[^\]]*\]\s*', '', t).replace('**', '').strip()


pieces = []; t = 0.0; meta = []
prev = None
for (lg, n, f, d), x in zip(T, L):
    assert n == x['n']
    a = load(R + f, 1.0 if n in KEEP_TEMPO else TEMPO)
    a, runs = tighten(a)
    if prev is not None:
        if n == '6': gap = 4.4                   # title slide + chapter 1 card
        elif n in CH_START: gap = 1.30
        elif prev['n'] == '5c': gap = 3.2          # title slide
        elif prev['text'].rstrip().endswith('?'): gap = 0.45
        elif n in PUNCH: gap = 0.50
        elif prev['sp'] != x['sp']: gap = 0.28
        else: gap = 0.20
        pieces.append(np.zeros(int(gap * SR), np.float32)); t += gap
    meta.append(dict(n=n, sp=x['sp'], text=clean(x['text']), raw=x['text'], t0=round(t, 3), t1=round(t + len(a) / SR, 3),
                     runs=[(round(t + s, 3), round(t + e, 3)) for s, e in runs]))
    pieces.append(a); t += len(a) / SR; prev = meta[-1]
voice = np.concatenate(pieces)
import soundfile as sf
sf.write(f'voice_{LANG}_raw.wav', voice, SR)
# envelope at 30 fps for lip-sync
fr = SR // 30; n = len(voice) // fr
env = np.sqrt(np.mean(voice[:n * fr].reshape(-1, fr) ** 2, 1)); env = np.clip(env / (np.percentile(env[env > 1e-4], 95) + 1e-9), 0, 1)
np.save(f'env_{LANG}.npy', env.astype(np.float32))
json.dump(dict(dur=round(len(voice) / SR, 3), lines=meta), open(f'tl_{LANG}.json', 'w'), ensure_ascii=False, indent=1)
words = sum(len(m['text'].split()) for m in meta)
print(LANG, 'dur', round(len(voice) / SR / 60, 2), 'min', 'wpm overall', round(words / (len(voice) / SR / 60)))
