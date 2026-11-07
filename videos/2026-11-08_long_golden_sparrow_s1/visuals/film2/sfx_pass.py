"""Sound-design pass: real recordings from sfx/ under the narration, ducked by the voice stem, then loudnorm -14."""
import sys, json, subprocess, re, numpy as np
L = sys.argv[1]; U = L.upper(); SR = 48000
SFX = '/home/claude/why-channel-studio/sfx/'; O = f'/home/claude/gs/out/{L}/'
def load(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
mix = load(O + f'GS_S1_film_{U}.wav'); voice = load(O + f'GS_S1_film_{U}_voice.wav')
n = len(mix); voice = np.pad(voice, ((0, max(0, n - len(voice))), (0, 0)))[:n]
TL = json.load(open(f'/home/claude/gs/out/timeline_{L}.json'))['lines']
shots = []
for ln in subprocess.run(['python3', 'film.py', L, 'shots'], cwd='/home/claude/gs/film2', capture_output=True, text=True, check=True).stdout.splitlines():
    m = re.match(r'([\d.]+) ([\d.]+) (\S+) \((.*)\)', ln)
    if m: shots.append((float(m[1]), float(m[2]), m[3], m[4]))
def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
SRC = {k: load(SFX + f) for k, f in [('loom', 'loom_shuttle.mp3'), ('harbour', 'harbour_waves.wav'), ('ship', 'ship_creak.mp3'),
                                     ('quill', 'quill_writing.mp3'), ('cannon', 'cannon_distant.wav')]}
# level: RMS target in dBFS before voice ducking
LEVEL = {'loom': -24, 'harbour': -25, 'ship': -26, 'quill': -25, 'cannon': -21}
bed = np.zeros_like(mix); log = []
def place(k, a, b, off=0.0, fade=0.8):
    s = SRC[k]; a_ = int(a * SR); b_ = min(n, int(b * SR)); m = b_ - a_
    if m <= 0: return
    i0 = int(off * SR) % len(s); seg = np.concatenate([s[i0:]] + [s] * (m // len(s) + 1))[:m]
    act = seg[np.abs(seg).mean(1) > 1e-4]
    g = 10 ** ((LEVEL[k] - rms_db(act if len(act) else seg)) / 20)
    f = min(int(fade * SR), m // 2); env = np.ones(m); env[:f] = np.linspace(0, 1, f); env[m - f:] = np.linspace(1, 0, f)
    bed[a_:b_] += seg * g * env[:, None]; log.append((k, round(a, 2), round(b, 2)))
line = lambda i: TL.get(i)
# loom: cold open + the weaving lines
for i in ('0.1', '2.1', '2.2', '2.3'):
    if line(i): place('loom', line(i)[0] - 0.3, line(i)[1] + 0.5, off=float(i.split('.')[1]) * 7)
# harbour: port shots and port lines
done = []
for a, b, i, sp in shots:
    if any(f"'{g}'" in sp for g in ('G09', 'G21', 'G10')): done.append((a, b))
for i in ('3.3', '4.11', '5.2'):
    if line(i): done.append(tuple(line(i)))
done.sort(); merged = []
for a, b in done:
    if merged and a <= merged[-1][1] + 1.5: merged[-1][1] = max(merged[-1][1], b)
    else: merged.append([a, b])
for a, b in merged: place('harbour', a, b, off=a % 60, fade=1.0)
# ship creak with the ship (T1) shots
for a, b, i, sp in shots:
    if "'T1'" in sp: place('ship', a, b, off=a % 15)
# quill: short strokes at the start of the writing lines
for i in ('2.8', '3.11', '4.8', '6.2'):
    if line(i): place('quill', line(i)[0], min(line(i)[1], line(i)[0] + 3.5), off=12 + float(i.split('.')[1]), fade=0.4)
# distant cannon: once at 5.10, and TE 7.4 (Masulipatnam 1759); never under Plassey 7.2 or the famine
for i in ('5.10',) + (('7.4',) if L == 'te' else ()):
    if line(i): place('cannon', line(i)[0] - 0.4, line(i)[0] + 4.2, off=2.8, fade=0.3)
# silence everything in the famine (4.9-4.10) and keep Plassey (7.2) clean
for i in ('4.9', '4.10', '7.2'):
    if line(i): a_, b_ = int((line(i)[0] - 1) * SR), int((line(i)[1] + 1) * SR); bed[a_:b_] = 0
# duck under the voice: -9 dB while narration is active (300 ms attack/release smoothing)
lv = np.abs(voice).mean(1); w = int(0.3 * SR); env = np.convolve(lv, np.ones(w) / w, 'same')
act = np.clip(env / (np.percentile(env[env > 1e-4], 50) * 0.35), 0, 1)
bed *= (1 - (1 - 10 ** (-10 / 20)) * act)[:, None]
out = mix + bed
open(f'/home/claude/gs/sfxpass/{L}_cues.json', 'w').write(json.dumps(log, indent=0))
tmp = f'/home/claude/gs/sfxpass/{L}_pre.wav'
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', tmp], input=out.astype(np.float32).tobytes(), check=True)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', '48000', O + f'GS_S1_film_{U}_sfx.wav'], check=True)
print(L, 'cues', len(log), 'bed rms', round(rms_db(bed[np.abs(bed).sum(1) > 0]), 1))
