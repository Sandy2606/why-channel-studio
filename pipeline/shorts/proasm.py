# Pro voice edit: denoise -> take assembly with tight gaps -> internal pause compression -> broadcast chain
import json, subprocess, numpy as np, scipy.io.wavfile as wf, noisereduce as nr
from pedalboard import (Pedalboard, HighpassFilter, PeakFilter, HighShelfFilter, LowShelfFilter,
                        Compressor, Limiter, Gain, NoiseGate)
SR = 48000
ROOT = '/home/claude/sun/'

def rms_db(a, hop=480):
    n = len(a) // hop
    return 20 * np.log10(np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-9)

def denoise(name):
    sr, a = wf.read(ROOT + f'rec/{name}.wav'); a = a.astype(np.float32) / 32768
    db = rms_db(a); thr = np.percentile(db, 8)
    # noise profile: quietest 10ms frames
    idx = np.where(db < thr + 2)[0][:400]
    noise = np.concatenate([a[i * 480:(i + 1) * 480] for i in idx]) if len(idx) > 20 else None
    y = nr.reduce_noise(y=a, sr=sr, y_noise=noise, stationary=True, prop_decrease=0.9, n_fft=2048)
    return y.astype(np.float32)

def snap(db, thr, s, e):
    v = db > thr; n = len(v); i = int(s * 100); j = int(e * 100)
    if i < n and v[i]:
        lo = max(0, i - 30)
        while i > lo and v[i - 1]: i -= 1
    else:
        k = i
        while k < min(n, i + 30) and not v[k]: k += 1
        if k < min(n, i + 30): i = k
    hi = min(n, j + 50)
    if j < n and not v[j]:
        k = j
        while k > i and not v[k - 1]: k -= 1
        j = k
    else:
        while j < hi and v[j:j + 10].any(): j += 1
    return max(0, i / 100 - 0.035), min(n / 100, j / 100 + 0.06)

CUTS = []
def squeeze(seg, thr, maxgap=0.13, keep=0.08):
    """shorten internal pauses longer than maxgap down to keep seconds"""
    db = rms_db(seg); v = db > thr; out = []; last = 0; i = 0; n = len(v)
    while i < n:
        if not v[i]:
            j = i
            while j < n and not v[j]: j += 1
            if (j - i) / 100 > maxgap and i > 0 and j < n:
                a0 = (i * 480) + int(keep / 2 * SR); b0 = (j * 480) - int(keep / 2 * SR)
                out.append(seg[last:a0]); last = b0; CUTS.append((a0, b0))
            i = j
        else: i += 1
    out.append(seg[last:])
    # short crossfades at joins
    y = out[0]; f = int(.008 * SR)
    for p in out[1:]:
        if len(y) > f and len(p) > f:
            y = np.concatenate([y[:-f], y[-f:] * np.linspace(1, 0, f) + p[:f] * np.linspace(0, 1, f), p[f:]])
        else: y = np.concatenate([y, p])
    return y

CHAIN = Pedalboard([
    HighpassFilter(90),
    LowShelfFilter(cutoff_frequency_hz=160, gain_db=1.5),       # warmth
    PeakFilter(cutoff_frequency_hz=320, gain_db=-3.0, q=1.0),   # remove boxiness / mud
    PeakFilter(cutoff_frequency_hz=3200, gain_db=3.0, q=0.9),   # presence / clarity
    HighShelfFilter(cutoff_frequency_hz=10000, gain_db=2.5),     # air
    Compressor(threshold_db=-24, ratio=3.5, attack_ms=4, release_ms=70),
    Compressor(threshold_db=-12, ratio=6, attack_ms=1, release_ms=40),   # second stage: punch, even level
    Gain(4),
    Limiter(threshold_db=-1.5, release_ms=60),
])

def build(name, keep, out, gap=0.07, tempo=1.0):
    a = denoise(name); db = rms_db(a); thr = np.percentile(db, 10) + 16
    parts = []; log = []; f = int(.01 * SR)
    B = [snap(db, thr, k[0], k[1]) if (len(k) < 3 or k[2] != 'raw') else (k[0], k[1]) for k in keep]
    for i in range(len(B) - 1):
        if B[i + 1][0] < B[i][1] and B[i + 1][0] > B[i][0]: B[i] = (B[i][0], B[i + 1][0] - 0.01)
    for (s2, e2) in B:
        seg = a[int(s2 * SR):int(e2 * SR)].copy()
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        log.append((round(s2, 2), round(e2, 2), len(seg) / SR))
        parts += [seg, np.zeros(int(gap * SR), np.float32)]
    starts = np.cumsum([0] + [len(p) for p in parts])[0::2][:len(log)]
    y = np.concatenate(parts); CUTS.clear()
    dby = rms_db(y); med = np.median(dby[dby > thr])
    y = squeeze(y, med - 24, maxgap=0.16, keep=0.10)
    # de-ess (ffmpeg) + tempo, then pro chain
    wf.write(out + '.raw.wav', SR, (np.clip(y, -1, 1) * 32767).astype(np.int16))
    af = 'deesser=i=0.4:m=0.5:f=0.5'
    if tempo != 1.0: af += f',atempo={tempo}'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out + '.raw.wav', '-af', af, '-ar', '48000', out + '.ds.wav'], check=True)
    _, z = wf.read(out + '.ds.wav'); z = z.astype(np.float32) / 32768
    z = CHAIN(z[None, :], SR)[0]
    wf.write(out + '.ch.wav', SR, (np.clip(z, -1, 1) * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out + '.ch.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=6', '-ar', '48000', out], check=True)
    f8 = int(.008 * SR)
    def o(p): return (p - sum(min(b, p) - a for a, b in CUTS if a < p) - f8 * sum(1 for a, b in CUTS if b <= p)) / SR
    log = [(round(o(st), 2),) + tuple(l[:2]) for st, l in zip(starts, log)]
    json.dump(log, open(out + '.map.json', 'w'))
    print(f'{out}: {len(z) / SR:.2f}s, {len(log)} pieces')
