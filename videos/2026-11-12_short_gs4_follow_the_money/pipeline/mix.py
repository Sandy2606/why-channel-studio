"""voice + real SFX (sfx/ only) + ducked approved music -> mix_<lang>_<plat>.wav (−14 LUFS)"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/gs4'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
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
import importlib.util
# chain (cue helpers duplicated from the renderer)
c_drop = S('MONEY') + .05; c_farmer = max(AT('4.6a', 'farmer', 'రైతు') - .1, c_drop + 1.0); c_third = AT('4.6a', 'third', 'మూడో') - .1
c_coll = AT('4.6a', 'Collectors', 'వసూలు') - .15; c_cut = AT('4.6a', 'cut.', 'వాటా') - .1; c_state = AT('4.6a', 'state', 'రాజ్యం') - .15
c_army = AT('4.6a', 'armies', 'సైన్యాలకు,') - .15; c_bank = AT('4.6a', 'Bankers', 'వడ్డీ') - .15; c_every = AT('4.6a', 'everyone.', 'అందరికీ') - .1
E += [('coin_flutter', c_drop, .30), ('coins_clink', c_drop + .7, .28), ('marker', c_third + .1, .22), ('paper_slide', c_cut, .22)]
for c_ in (c_coll, c_state, c_army): E += [('coins_clink', c_ + .75, .22)]
E += [('ui_pop', c_bank, .15), ('swoosh_slow', c_every - .1, .16)]
# farman: document slides in; seal ringed; two highlights; notes (no stamp)
c_doc = S('FARMAN') + .5; c_f = AT('FARMAN', 'farmans,', 'ఫర్మానాలు') - .1
c_r = AT('FARMAN', 'trading', 'హక్కులు,', n=2 if not TE else 1) - .1; c_p = AT('FARMAN', 'privileges.', 'ప్రత్యేక') - .1
E += [('paper_slide', c_doc, .28), ('marker', c_f + .05, .2), ('marker', c_r + .05, .2), ('marker', c_p + .05, .2)]
for c_ in (c_f, c_r, c_p): E += [('ui_click', c_ + .3, .10)]
# rains -> famine: restrained, near silence
c_fail = AT('4.9', 'failed…', 'పడకపోతే…') + .1
put('rain_light_loop', SCs['rains'] - .3, .30, maxlen=c_fail + .9 - SCs['rains'] + .3, fade=.6)
put('wind_ambience', c_fail, .12, maxlen=SCs['turn'] - c_fail + .3, fade=1.2)
c_yr = AT('4.10', '1630', '1630') - .1; c_m = AT('4.10', 'Peter', 'Peter') - .25
E += [('map_unfold', c_yr - .05, .14), ('page_turn', c_m, .22), ('marker', c_m + 1.6, .16)]
# turn: thread, the port, the sea routes
c_but = AT('TURN', 'But', 'కానీ') - .15; c_tr = AT('TURN', 'trade', 'సముద్రాల') - .25
E += [('coins_clink', SCs['turn'] + 1.0, .18), ('swoosh_slow', c_tr, .22)]
amb('dock.wav', c_but - .2, SCs['tease'], .45)
put('harbour_waves', c_but, .18, maxlen=SCs['tease'] - c_but, fade=.6)
# tease
c_q = AT('tease2', 'who', 'వాస్కో') - .2
E += [('ticker_run', SCs['tease'], .16), ('sub_knock', c_q + .5, .35)]
for n_, t_, g_ in CTA.events(SCs['slide'] + 0.9, PLAT):
    if n_ != 'woosh_air': put(n_, t_, g_ * 0.8)
put('swoosh_slow', SCs['loop'] + 0.05, 0.18)
for n, t, g in E: put(n, t, g)
def run(tag):
    os.chdir(ROOT); wf.write(f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'voice_{LANGV}.wav', '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), f'vlead_{tag}.wav'], check=True)
    music = MUSIC
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{SCs['cartoon3']+1.2},{SCs['turn']})':volume=0.18,volume=enable='between(t,{SCs['slide']},{DUR})':volume=1.6,afade=t=in:st=0:d=0.3,afade=t=out:st={DUR-0.5}:d=0.5[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=8', '-ar', '48000', f'mix_{tag}.wav'], check=True)
    print('mixed', tag, DUR)
if __name__ == '__main__':
    run(f'{LANGV}_{PLAT}')
