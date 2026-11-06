"""Golden Sparrow S1 listening test: opening (0.1-0.5 + title sting) and final question (7.9 + Season 2 sting), EN + TE.
Natural documentary pacing: NO tempo change, NO pause squeeze; only edge trims and deliberate gaps."""
import sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/shorts'); import proasm
SR = 48000
ST = '/home/claude/why-channel-studio'
CAT = json.load(open(f'{ST}/sfx/catalog.json'))

def load(p, ch=1):
    a = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ar', str(SR), '-ac', str(ch), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).copy()
    return a if ch == 1 else a.reshape(-1, 2).mean(1)

def trim(x, thr=-50):
    hop = 480; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9); v = np.where(db > thr)[0]
    return x[max(0, v[0] * hop - 960):min(len(x), (v[-1] + 1) * hop + 2400)]

def fade(x, a=0.01, b=0.03):
    x = x.copy(); fa = int(a * SR); fb = int(b * SR); x[:fa] *= np.linspace(0, 1, fa); x[-fb:] *= np.linspace(1, 0, fb); return x

def sfx(name):
    c = CAT[name]; return load(f'{ST}/sfx/{c["file"]}', 2), c['hit_at']

def db(g): return 10 ** (g / 20)

def place(buf, x, t, g=0.0):
    i = int(t * SR); n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n] * db(g)

def build(lang, part):
    if part == 'open':
        ids = ['0.1', '0.2', '0.3', '0.4', '0.5']
        gaps = {'0.1': 0.55, '0.2': 0.40, '0.3': 0.45, '0.4': 0.60}   # beats: after the "Why?", before the big question
        lead = 1.2
    else:
        ids = ['7.9']; gaps = {}; lead = 1.6
    V = [fade(trim(load(f'raw/{lang}_{i}.mp3'))) for i in ids]
    marks = {}; t = lead; segs = []
    for i, v in zip(ids, V):
        marks[i] = (round(t, 2), round(t + len(v) / SR, 2)); segs.append((t, v)); t += len(v) / SR + gaps.get(i, 0)
    vend = marks[ids[-1]][1]
    tail = 4.2 if part == 'open' else 5.0
    total = vend + 0.9 + tail
    voice = np.zeros(int(total * SR) + SR, np.float32)
    for st, v in segs: place(voice, v, st)
    voice = proasm.CHAIN(voice[None, :], SR)[0]
    fx = np.zeros_like(voice); mus = np.zeros_like(voice)
    # music bed: low under voice, swells into the title card
    m = load(f'{ST}/music/beneath_the_rising_current.mp3' if part == 'open' else f'{ST}/music/the_quiet_meridian.mp3', 2)
    m = m[int((8 if part == 'open' else 20) * SR):][:len(mus)]
    env = np.full(len(mus), db(-26), np.float32)
    hit = vend + 0.9
    i0 = int(lead * 0.5 * SR); env[:i0] = np.linspace(0, db(-26), i0)
    a, b = int((hit - 0.4) * SR), int(hit * SR); env[a:b] = np.linspace(db(-26), db(-14), b - a); env[b:] = db(-14)
    fo = int(2.2 * SR); env[-fo:] = np.linspace(db(-14), 0, fo)
    mus[:len(m)] = m * env[:len(m)]
    # sound design (real recordings from sfx/)
    w, _ = sfx('wind_ambience'); place(fx, w[int(6 * SR):int(6 * SR) + int(total * SR)] * np.linspace(0, 1, min(len(w) - int(6 * SR), int(total * SR))) ** 0.5, 0, -30)
    if part == 'open':
        hb, h = sfx('heartbeat_slow'); place(fx, hb, marks['0.5'][0] - h - 0.15, -16)
        r, h = sfx('riser'); place(fx, r, hit - h, -14)
        bi, h = sfx('boom_impact'); place(fx, bi, hit - h, -6)
    else:
        bd, h = sfx('boom_distant'); place(fx, bd, marks['7.9'][0] + 0.3 - h, -22)
        r, h = sfx('riser_synth') if 'riser_synth' in CAT else sfx('riser'); place(fx, r, hit - h, -16)
        it, h = sfx('impact_trailer'); place(fx, it, hit - h, -7)
    y = voice + mus + fx
    wf.write('/tmp/claude-0/mt.wav', SR, (np.clip(y, -1, 1) * 32767).astype(np.int16))
    out = f'GS_test_{lang.upper()}_{"opening" if part == "open" else "final_question"}.mp3'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/claude-0/mt.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', '-b:a', '192k', out], check=True)
    return out, marks, round(total, 2), round(hit, 2)

if __name__ == '__main__':
    res = {}
    for lang in ('en', 'te'):
        for part in ('open', 'final'):
            out, marks, total, hit = build(lang, part)
            res[out] = dict(marks=marks, title_hit=hit, file_len=total)
            print(out, 'voice', marks, 'sting at', hit, 'file', total)
    json.dump(res, open('test_marks.json', 'w'), indent=1)
