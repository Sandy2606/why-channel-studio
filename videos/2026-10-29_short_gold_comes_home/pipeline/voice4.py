"""Assemble GOLD 4/6 voice tracks (EN/TE x YT/IG) from ElevenLabs pieces + voice library; tighten pauses; pro chain."""
import sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/sandy2606/why-channel-studio/pipeline/shorts')
import proasm
SR = 48000
def load(p):
    if p.endswith('.wav'):
        sr, a = wf.read(p)
    else:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ar', str(SR), '-ac', '1', '-f', 's16le', '-'], capture_output=True).stdout
        a = np.frombuffer(raw, np.int16)
    return a.astype(np.float32) / 32768
def cut(a, s, e):
    x = a[int(s * SR):int(e * SR)].copy(); f = int(.01 * SR); x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f); return x
EN_L1, EN_B = load('en/l1.wav'), load('en/block.wav')
TE_L1, TE_B = load('te/l1.wav'), load('te/block.wav')
LIB = '/home/claude/why-channel-studio/voice_lib/'
idx = json.load(open(LIB + 'index.json'))
def lib(text):
    for e in idx:
        if e['text'] == text: return load(LIB.rsplit('/voice_lib/', 1)[0] + '/' + e['file'])
    raise KeyError(text)
TE_SUB = lib('ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం subscribe చేయండి.')
TE_FOL = lib('ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం follow అవ్వండి.')
TE_COM = lib('మీకు ఏదైనా why ఉంటే comment చేయండి, answer మేము వెతికి చెప్తాం.')
def trim(x, thr=-50):
    hop = 480; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    v = np.where(db > thr)[0]
    return x[max(0, v[0] * hop - 1200):min(len(x), (v[-1] + 1) * hop + 2400)]
EN_BODY = cut(EN_B, 0, 49.30); EN_SUB = cut(EN_B, 49.40, 53.12); EN_FOL = cut(EN_B, 53.18, 56.80); EN_COM = cut(EN_B, 56.80, len(EN_B) / SR)
TE_BODY = trim(TE_B)
def build(lang, plat, tempo):
    l1, body = (trim(EN_L1), EN_BODY) if lang == 'en' else (trim(TE_L1), TE_BODY)
    cta = {('en', 'yt'): EN_SUB, ('en', 'ig'): EN_FOL, ('te', 'yt'): TE_SUB, ('te', 'ig'): TE_FOL}[(lang, plat)]
    com = trim(EN_COM if lang == 'en' else TE_COM)
    parts = [l1, np.zeros(int(.25 * SR), np.float32), body, np.zeros(int(.3 * SR), np.float32), trim(cta), np.zeros(int(.1 * SR), np.float32), com]
    y = np.concatenate(parts)
    db = proasm.rms_db(y); thr = np.percentile(db, 10) + 16; med = np.median(db[db > thr])
    offs = np.cumsum([0] + [len(p) for p in parts])
    proasm.CUTS.clear(); y = proasm.squeeze(y, med - 24, maxgap=0.22, keep=0.14)
    json.dump({'cuts': proasm.CUTS, 'offs': [int(o) for o in offs], 'tempo': tempo, 'l1': len(l1), 'body': len(body)}, open(f'map_{lang}_{plat}.json', 'w'))
    np.save(f'raw_{lang}_{plat}.npy', np.concatenate(parts))
    tag = f'{lang}_{plat}'
    wf.write(f'v_{tag}.raw.wav', SR, (np.clip(y, -1, 1) * 32767).astype(np.int16))
    af = f'atempo={tempo}' if tempo != 1.0 else 'anull'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'v_{tag}.raw.wav', '-af', af, '-ar', '48000', f'v_{tag}.t.wav'], check=True)
    _, z = wf.read(f'v_{tag}.t.wav'); z = z.astype(np.float32) / 32768
    z = proasm.CHAIN(z[None, :], SR)[0]
    wf.write(f'v_{tag}.ch.wav', SR, (np.clip(z, -1, 1) * 32767).astype(np.int16))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'v_{tag}.ch.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=6', '-ar', '48000', f'voice_{tag}.wav'], check=True)
    print(tag, round(len(z) / SR, 2))
for lang, tempo in (('en', 1.03), ('te', 1.06)):
    for plat in ('yt', 'ig'): build(lang, plat, tempo)
