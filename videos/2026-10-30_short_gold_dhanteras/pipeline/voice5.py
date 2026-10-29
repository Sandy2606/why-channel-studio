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


LIB = '/home/claude/why-channel-studio/voice_lib/'
idx = json.load(open(LIB + 'index.json'))
def lib(text):
    for e in idx:
        if e['text'] == text: return load(LIB.rsplit('/voice_lib/', 1)[0] + '/' + e['file'])
    raise KeyError(text)
EN_FULL = lib('The full gold story is out now on our channel.'); TE_FULL = lib('Gold full story మన channel లో ఇప్పుడే వచ్చింది.')
EN_SUB = lib('If you like learning things like this, subscribe for a new why every day.'); EN_FOL = lib('If you like learning things like this, follow for a new why every day.'); EN_COM = lib("Comment your why below, and we'll find the answer.")
TE_SUB = lib('ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం subscribe చేయండి.')
TE_FOL = lib('ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం follow అవ్వండి.')
TE_COM = lib('మీకు ఏదైనా why ఉంటే comment చేయండి, answer మేము వెతికి చెప్తాం.')
def trim(x, thr=-50):
    hop = 480; n = len(x) // hop; db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
    v = np.where(db > thr)[0]
    return x[max(0, v[0] * hop - 1200):min(len(x), (v[-1] + 1) * hop + 2400)]
EN_B, TE_B = load('en/block.wav'), load('te/block.wav')
EN_BODY = trim(EN_B)
TE_BODY = trim(TE_B)
def build(lang, plat, tempo):
    full, body = (trim(EN_FULL), EN_BODY) if lang == 'en' else (trim(TE_FULL), TE_BODY)
    cta = {('en', 'yt'): EN_SUB, ('en', 'ig'): EN_FOL, ('te', 'yt'): TE_SUB, ('te', 'ig'): TE_FOL}[(lang, plat)]
    com = trim(EN_COM if lang == 'en' else TE_COM)
    parts = [body, np.zeros(int(.45 * SR), np.float32), full, np.zeros(int(.3 * SR), np.float32), trim(cta), np.zeros(int(.1 * SR), np.float32), com]
    y = np.concatenate(parts)
    db = proasm.rms_db(y); thr = np.percentile(db, 10) + 16; med = np.median(db[db > thr])
    offs = np.cumsum([0] + [len(p) for p in parts])
    proasm.CUTS.clear(); y = proasm.squeeze(y, med - 24, maxgap=0.22, keep=0.14)
    json.dump({'cuts': proasm.CUTS, 'offs': [int(o) for o in offs], 'tempo': tempo, 'full': len(full), 'body': len(body)}, open(f'map_{lang}_{plat}.json', 'w'))
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
