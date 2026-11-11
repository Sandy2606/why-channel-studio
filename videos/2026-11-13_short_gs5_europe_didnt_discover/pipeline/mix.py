"""GS 5/6: voice + real SFX (sfx/ only) + ducked approved music -> mix_<lang>_<plat>.wav (-14 LUFS).
Events follow on-screen action. Built so far for the preview ranges (ocean/monsoon, route/pilot); other scenes are added after approval."""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/gs5')
from cues import *
MUSIC = '/home/claude/why-channel-studio/music/where_the_river_bends.mp3'
SR = 48000; LIB = '/home/claude/why-channel-studio/sfx/'
CAT = json.load(open(LIB + 'catalog.json'))
def load(path):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()
N = int(DUR * SR) + SR; SFX = np.zeros((N, 2), np.float32)
def put(name, t, gain=0.4, maxlen=None, fade=0.2, path=None):
    p = path or (LIB + name + ('' if '.' in name else '.wav')); a = load(p); hit = (CAT.get(name, {}) or {}).get('hit_at', 0) or 0
    if maxlen:
        a = a[:int(maxlen * SR)].copy(); f = int(fade * SR); a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int((t - hit) * SR)
    if i < 0: a = a[-i:]; i = 0
    j = min(N, i + len(a)); SFX[i:j] += a[:j - i] * gain
def bed(path, t0, t1, gain, fade=0.8):
    a = load(path); n = int((t1 - t0) * SR)
    while len(a) < n: a = np.concatenate([a, a])
    a = a[:n].copy(); r = np.sqrt((a ** 2).mean()) + 1e-6; a *= 0.05 / r; f = int(fade * SR); a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t0 * SR); SFX[i:i + n] += a * gain
SCs = dict(SC)
# ---- ocean: harbour bed, one soft pin per people group, Malacca pin (TE: one coin)
bed(LIB + 'harbour_waves.wav', SCs['ocean'], SCs['monsoon'] + .6, .55)
bed(LIB + 'ship_creak.mp3', SCs['ocean'] + 1.0, SCs['monsoon'], .18)
for en, te in (('Indian,', 'భారతీయులు,'), ('Arab,', 'అరబ్బులు,'), ('Persian,', 'పర్షియన్లు,'), ('African,', 'ఆఫ్రికన్లు,'), ('Chinese', 'చైనీయులు,'), ('Malay', 'మలయా')):
    put('pin_push', AT('53A', en, te) - .05, .10)
put('pin_push', S('5.3b') + .2, .16); put('paper_slide', S('5.3b') + .5, .14)
if TE and has('5.4'): put('coins_clink', AT('5.4', 'తెలుగు', 'తెలుగు') + .35, .16)
# ---- monsoon: wind rises, turns at the reversal; the calendar lands
c_back = AT('5.5', 'back', 'మిగతా') - .1; c_sail = AT('5.5', 'Sailors', 'నావికులు') - .15
put('wind_ambience', SCs['monsoon'] - .2, .30, maxlen=SCs['cartoon2'] - SCs['monsoon'] + .4, fade=.9)
put('swoosh_slow', c_back + .2, .18); put('paper_slide', c_sail + .05, .14)
# ---- route: map widens, the arc crosses the sea, pins at Malindi and Calicut
c_mal = AT('5.6a', 'Malindi', 'మాలిండి') - .15; c_gui = AT('5.6a', 'guided', 'అతనే') - .15; c_cal = AT('5.6a', 'Calicut.', 'కాలికట్') - .1
put('map_unfold', SCs['route'] + .05, .14); put('pin_push', c_mal + .05, .16)
bed(LIB + 'ship_creak.mp3', c_gui - .2, c_cal + .9, .30); bed(LIB + 'harbour_waves.wav', SCs['route'], SCs['pilot'] + .3, .35)
put('swoosh_slow', c_gui + .1, .16); put('pin_push', c_cal + .05, .18)
# ---- pilot: one page turn per exhibit, paper for each clipping, marker on each underline, quill on the name, pin on Gujarat
c_x = AT('PILOT', "'Christian'…", "'క్రైస్తవుడు'") - .25; c_h = AT('PILOT', 'but', 'కానీ') - .15
c_lat = AT('PILOT', 'Later', 'తర్వాతి') - .2; c_name = AT('PILOT', 'Malemo', 'మాలెమో') - .15; c_fam = AT('PILOT', 'famous', 'అతను') - .2
c_unl = AT('PILOT', 'unlikely.', 'కానీ', n=1 if not TE else 2) - .2; c_ver = AT('PILOT', 'So', 'అంటే', n=2 if not TE else 1) - .2
c_guj = AT('PILOT', 'Gujarat,', 'గుజరాత్‌కు', n=2) - .2
E = [('page_turn', SCs['pilot'] + .05, .20), ('paper_slide', c_x + .05, .16), ('marker', c_x + .55, .14),
     ('paper_slide', c_h + .05, .16), ('marker', c_h + .55, .14),
     ('page_turn', c_lat - .1, .20), ('quill_writing.mp3', c_name + .3, .16), ('page_turn', c_fam - .1, .20), ('marker', c_unl + .1, .10),
     ('map_unfold', c_ver - .2, .14), ('pin_push', c_guj + .75, .22)]
for n, t, g in E:
    if n.endswith('.mp3'): put(n, t, g, maxlen=1.6, fade=.3, path=LIB + n)
    else: put(n, t, g)
def run(tag):
    os.chdir(ROOT); wf.write(f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'voice_{LANGV}.wav', '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), f'vlead_{tag}.wav'], check=True)
    lift = (c_ver, c_ver + 6.0)      # music lifts slightly under the verdict
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{lift[0]},{lift[1]})':volume=1.35,volume=enable='between(t,{SCs['slide']},{DUR})':volume=1.6,afade=t=in:st=0:d=0.3,afade=t=out:st={DUR-0.5}:d=0.5[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', MUSIC, '-i', f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=8', '-ar', '48000', f'mix_{tag}.wav'], check=True)
    print('mixed', tag, DUR)
if __name__ == '__main__':
    run(f'{LANGV}_{PLAT}')
