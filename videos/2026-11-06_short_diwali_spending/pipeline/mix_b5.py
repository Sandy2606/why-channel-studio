"""voice + real SFX + ducked music -> mix_<lang>_<plat>.wav"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render_b5 as R
CTA = R.CTA; A, LEAD, DUR, S = R.A, R.LEAD, R.DUR, R.S
SR = 48000; LIB = '/home/claude/why-channel-studio/sfx/'
CAT = json.load(open(LIB + 'catalog.json'))
def load(name):
    f = LIB + name + ('.mp3' if name.startswith('amb_') else '.wav')
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()
N = int(DUR * SR) + SR; SFX = np.zeros((N, 2), np.float32)
def put(name, t, gain=0.5, maxlen=None, fade=0.2):
    a = load(name); hit = (CAT.get(name, {}) or {}).get('hit_at', 0) or 0
    if maxlen:
        a = a[:int(maxlen * SR)].copy(); f = int(fade * SR); a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int((t - hit) * SR)
    if i < 0: a = a[-i:]; i = 0
    j = min(N, i + len(a)); SFX[i:j] += a[:j - i] * gain
E = [('coins_clink', 0.05, 0.3), ('paper_drop', A['trade1'] - 0.2, 0.25), ('marker', A['trade1'] + 0.1, 0.3), ('ui_pop', A['where'] - 0.1, 0.35),
     ('woosh_air', S('2'), 0.3), ('coin_flutter', S('2') + 1.3, 0.35),
     ('sub_knock', S('3') + 0.15, 0.3), ('coins_clink', A['groc'], 0.4), ('paper_drop', A['groc'] + 0.5, 0.2), ('marker', A['groc'] + 0.8, 0.3),
     ('coins_clink', A['gold4'], 0.35), ('coins_clink', A['elec'], 0.35), ('coin_flutter', A['appl'], 0.35), ('coin_flutter', A['decor'], 0.35),
     ('coins_clink', A['sweets'] + 0.4, 0.35), ('ui_bell', A['sweets'] + 1.0, 0.3),
     ('woosh_air', S('7') - 0.05, 0.25), ('ui_pop', A['k80'] - 0.2, 0.3),
     ('coin_flutter', S('8') + 0.2, 0.3), ('ui_pop', A['lakshmi'] - 0.2, 0.3), ('ui_click', A['busiest'] - 0.3, 0.3),
     ('ticker_run', A['p85'] - 0.3, 0.2), ('ui_bell', A['p85'] + 0.7, 0.3), ('paper_drop', A['p85'] + 1.0, 0.2), ('marker', A['p85'] + 1.3, 0.3),
     ('ticker_run', S('10'), 0.15), ('ui_pop', A['j50'] - 0.1, 0.35),
     ('stamp', S('11') + 0.1, 0.45), ('sparkle_soft', A['small'] - 0.3, 0.3),
     ('woosh_tunnel', S('12') - 0.1, 0.3), ('paper_slide', S('L') + 0.1, 0.3), ('coins_clink', S('L') + 0.8, 0.18)]
for i in range(3): E.append(('ui_pop', A['services'] - 0.2 + 0.2 * i, 0.25))
for i in range(6): E.append(('ui_pop', S('12') + 0.35 + 0.1 * i, 0.22))
for n, t, g in E: put(n, t, g)
put('footsteps_soft_indoor', S('8') + 0.3, 0.12, maxlen=3.0, fade=0.8)
for n_, t_, g_ in CTA.events(R.END_T0, R.PLAT): put(n_, t_, g_)
def run(tag):
    wf.write(R.ROOT + f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.VFILE, '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/long/music/where_the_river_bends.wav'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{S('12')-0.2},{DUR})':volume=0.45,afade=t=in:st=0:d=0.25,afade=t=out:st={DUR-0.6}:d=0.6[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', R.ROOT + f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', R.ROOT + f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', R.ROOT + f'mix_{tag}.wav'], check=True)
    print('mixed', tag, round(DUR, 2))
if __name__ == '__main__':
    run(f"{os.environ.get('LANGV','en')}_{os.environ.get('PLAT','yt')}")
