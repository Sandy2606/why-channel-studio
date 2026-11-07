"""Intelligibility proxy: speech vs everything-else ratio per 1 s window during narration, full band and 1-4 kHz."""
import sys, json, subprocess, numpy as np
from scipy.signal import butter, sosfilt
L = sys.argv[1]; U = L.upper(); SR = 16000
def load(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    return np.frombuffer(r, np.float32).copy()
mix = load(f'/home/claude/gs/out/{L}/GS_S1_film_{U}{sys.argv[2] if len(sys.argv)>2 else "_sfx"}.wav'); v = load(f'/home/claude/gs/out/{L}/GS_S1_film_{U}_voice.wav')
n = min(len(mix), len(v)); mix, v = mix[:n], v[:n]
sos = butter(4, [1000, 4000], 'bandpass', fs=SR, output='sos'); mixb, vb = sosfilt(sos, mix), sosfilt(sos, v)
TL = json.load(open(f'/home/claude/gs/out/timeline_{L}.json'))['lines']
rows = []; W = SR
for i, (a, b) in TL.items():
    for s in np.arange(a, b - 0.5, 1.0):
        x0, x1 = int(s * SR), int(min(b, s + 1) * SR)
        vv, mm = v[x0:x1], mix[x0:x1]
        if np.sqrt(np.mean(vv ** 2)) < 1e-3: continue
        g = np.dot(vv, mm) / np.dot(vv, vv); bg = mm - g * vv
        snr = 10 * np.log10(np.sum((g * vv) ** 2) / (np.sum(bg ** 2) + 1e-12))
        vb_, mb_ = vb[x0:x1], mixb[x0:x1]; gb = np.dot(vb_, mb_) / (np.dot(vb_, vb_) + 1e-12); bgb = mb_ - gb * vb_
        snrb = 10 * np.log10(np.sum((gb * vb_) ** 2) / (np.sum(bgb ** 2) + 1e-12))
        rows.append((i, round(float(s), 1), round(float(snr), 1), round(float(snrb), 1)))
S = np.array([r[2] for r in rows]); B = np.array([r[3] for r in rows])
print(L, 'windows', len(rows), 'speech/background dB: median', np.median(S).round(1), 'p5', np.percentile(S, 5).round(1), '| 1-4 kHz median', np.median(B).round(1), 'p5', np.percentile(B, 5).round(1))
low = [r for r in rows if r[2] < 12 or r[3] < 15]
print('flagged', len(low), low[:40])
json.dump(rows, open(f'/home/claude/gs/sfxpass/{L}_snr.json', 'w'))
