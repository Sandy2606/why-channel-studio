"""voice + real SFX (sfx/ only) + ducked approved music -> mix_<lang>_<plat>.wav (−14 LUFS)"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/gs3'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
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
# hook: gem reveal, map, the mystery
E += [('sparkle_soft', 0.15, 0.30), ('map_unfold', AT('S3_hook', 'many', 'ఎన్నో') - 0.15, 0.28), ('sub_knock', AT('S3_hook', 'But', 'కానీ') - 0.1, 0.45), ('riser', AT('S3_hook', 'something', 'వేరే') - 0.5, 0.10)]
# mine (sound-led: footsteps before the picture)
amb('footsteps_stone.mp3', SCs['mine'] - 0.6, SCs['tavernier'], 0.4)
E += [('page_turn', SCs['tavernier'], 0.3), ('typing_run', SCs['kohinoor'] + 0.1, 0.22)]
# payoff
c_cloth = AT('3.9', 'Cloth', 'ఓడలు') - 0.12; c_fist = AT('3.9', 'A', 'ఒక') - 0.1; c_fleet = AT('3.9', 'Cloth', 'గుడ్డ', n=2 if not TE else 1) - 0.12
E += [('sparkle_soft', AT('3.9', 'Diamonds', 'వజ్రాలు') - 0.1, 0.25), ('sub_knock', c_cloth, 0.55), ('paper_slide', c_cloth + min(1.15, (c_fist - c_cloth) * 0.42), 0.28), ('tick', c_fist + 0.1, 0.3)]
put('ship_bell', c_fleet - 0.45, 0.30, path=LIB + 'amb/ship_bell.mp3', maxlen=3.0)
amb('dock.wav', c_fleet - 0.3, SCs['cartoon3'] + 0.3, 0.5)
# ships + port (ship bell leads the harbour)
E += [('map_unfold', SCs['ships'] + 0.05, 0.28)]
for w in (('Persia,', 'Persia,'), ('Arabia,', 'అరేబియా,'), ('Burma', 'బర్మా,'), ('Southeast', 'ఆగ్నేయాసియా')): E.append(('pin_push', AT('3.3', *w) - 0.3, 0.25))
put('ship_bell', SCs['port'] - 0.5, 0.30, path=LIB + 'amb/ship_bell.mp3', maxlen=3.0)
amb('dock.wav', SCs['port'] - 0.3, AT('3.3', 'Local', 'మన'), 0.5)
E += [('ui_pop', AT('3.3', 'Dutch', 'డచ్') - 0.1, 0.18), ('ui_pop', AT('3.3', 'English', 'ఇంగ్లీష్') - 0.1, 0.18)]
amb('bazaar.mp3', AT('3.3', 'Local', 'మన') - 0.3, AT('3.3', 'weaving', 'నేత') - 0.7, 0.45)
amb('dock.wav', AT('3.3', 'weaving', 'నేత') - 0.9, SCs['b3'] + 0.3, 0.5)
E += [('sub_knock', AT('3.3', 'weaving', 'నేత') - 0.9, 0.35)]
E += [('coins_clink', SCs['tease'] + 0.8, 0.3)]
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
