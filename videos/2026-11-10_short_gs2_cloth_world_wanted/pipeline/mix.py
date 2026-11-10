"""voice + real SFX (sfx/ only) + ducked approved music -> mix_<lang>_<plat>.wav (−14 LUFS)"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/gs2'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
from cues import *
import cta_card as CTA
MUSIC = '/home/claude/why-channel-studio/music/where_the_river_bends.mp3'
SR = 48000; LIB = '/home/claude/why-channel-studio/sfx/'
CAT = json.load(open(LIB + 'catalog.json'))
def load(path):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()
N = int(DUR * SR) + SR; SFX = np.zeros((N, 2), np.float32)
def put(name, t, gain=0.4, maxlen=None, fade=0.2, path=None):
    a = load(path or (LIB + name + '.wav')); hit = (CAT.get(name, {}) or {}).get('hit_at', 0) or 0
    if maxlen:
        a = a[:int(maxlen * SR)].copy(); f = int(fade * SR); a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int((t - hit) * SR)
    if i < 0: a = a[-i:]; i = 0
    j = min(N, i + len(a)); SFX[i:j] += a[:j - i] * gain
def amb(name, t0, t1, gain):
    a = load(LIB + 'amb/' + name); n = int((t1 - t0) * SR)
    while len(a) < n: a = np.concatenate([a, a])
    a = a[:n]; r = np.sqrt((a ** 2).mean()) + 1e-6; a *= 0.05 / r; f = int(0.8 * SR); a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t0 * SR); SFX[i:i + n] += a * gain
SCs = dict(SC)
E = []
E += [('stamp', 0.12, 0.5), ('stamp', AT('0.1', 'wearing', 'కొన్ని') - 0.2, 0.45)]
amb('village.mp3', SCs['boll'] - 0.2, SCs['cartoon2'] + 0.2, 0.5)
E += [('riser', SCs['boll'] + 0.2, 0.10)]
for i in range(8): E.append(('tick', AT('2.2', 'many', 'ఎంతోమంది') - 0.15 + .4 + i * .1, 0.18))
E += [('coins_clink', AT('2.3', 'advance', 'ముందుగానే') - 0.1, 0.3), ('marker', AT('2.3', 'price.', 'ధర') - 0.1, 0.3), ('sub_knock', AT('2.3', 'bargaining', 'బేరమాడే'), 0.35)]
E += [('sub_knock', AT('2.4', 'dyer.', 'అద్దేవాళ్లు.'), 0.4), ('water_bubbles', SCs['wash'] + 0.6, 0.35)]
for w in (('mordants,', 'పదార్థాలతో'), ('reds', 'ఎరుపు'), ('blue', 'నీలం'), ('wax', 'మైనం')): E.append(('paper_slide', AT('2.6', *w) - 0.1, 0.25))
E += [('scribble', SCs['kalam'] + 0.3, 0.25)]
if 'kalamkari' in SCs: E += [('pin_push', AT('2.7', 'శ్రీకాళహస్తిలో', 'శ్రీకాళహస్తిలో') - .1, .3), ('pin_push', AT('2.7', 'మచిలీపట్నం,', 'మచిలీపట్నం,') - .1, .3)]
E += [('typing_run', SCs['letter'] + 0.05, 0.25)]
if 'muslin' in SCs: E += [('sparkle_soft', AT('2.9', 'woven', 'woven') - .1, 0.2)]
for w in (('bright,', 'రంగురంగుల,'), ('light,', 'తేలికైన,'), ('washable', 'ఉతకగలిగే')): E.append(('ui_pop', AT('2.10', *w) - .05, 0.18))
E += [('sub_knock', AT('2.10', 'bans', 'నిషేధాలు'), 0.4)]
for (key, en, te) in (('2.11', 'France', 'ఫ్రాన్స్'), ('2.11', '1700', '1700'), ('2.12', '1721', '1721'), ('2.12', 'Christmas', 'క్రిస్మస్'), ('2.13', '1774.', '1774')): E.append(('tick', AT(key, en, te) - .15, 0.3))
cf = AT('2.12', 'further.', 'ముందుకెళ్లింది.', end=True); E += [('page_turn', cf, 0.3), ('stamp', AT('2.13', '1774.', '1774'), 0.35)]
E += [('paper_slide', AT('2.14', 'wool', 'ఉన్ని,') - .1, 0.25)]
if 'globe' in SCs: E += [('map_unfold', SCs['globe'] + 0.05, 0.3), ('ui_pop', AT('2.15', 'Even', 'Even'), 0.2), ('ui_pop', AT('2.15', 'Even', 'Even') + 1.2, 0.2)]
amb('dock.wav', SCs['tease'], SCs['slide'] + 0.3, 0.4)
for n_, t_, g_ in CTA.events(SCs['slide'] + 0.9, PLAT):
    if n_ != 'woosh_air': put(n_, t_, g_ * 0.8)
put('swoosh_slow', SCs['loop'] + 0.05, 0.18)
for n, t, g in E: put(n, t, g)
def run(tag):
    os.chdir(ROOT); wf.write(f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'voice_{LANGV}.wav', '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), f'vlead_{tag}.wav'], check=True)
    music = MUSIC
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{SCs['slide']},{DUR})':volume=1.6,afade=t=in:st=0:d=0.3,afade=t=out:st={DUR-0.5}:d=0.5[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=8', '-ar', '48000', f'mix_{tag}.wav'], check=True)
    print('mixed', tag, DUR)
if __name__ == '__main__':
    run(f'{LANGV}_{PLAT}')
