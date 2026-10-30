"""voice + real SFX + ducked calm music -> mix_<lang>_<plat>.wav ; env LANGV, PLAT"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render6 as R
CTA = R.CTA
A, LEAD, DUR = R.A, R.LEAD, R.DUR
SR = 48000
LIB = '/home/claude/sandy2606/why-channel-studio/sfx/'
CAT = json.load(open(LIB + 'catalog.json'))
EXTRA = {'chime': '/home/claude/g3/clips/mixkit-crystal-chime-3108.wav'}
def load(name):
    f = EXTRA.get(name) or (LIB + name + ('.mp3' if name.startswith('amb_') else '.wav'))
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()
N = int(DUR * SR) + SR
SFX = np.zeros((N, 2), np.float32)
def put(name, t, gain=0.5, maxlen=None, fade=0.2):
    a = load(name); hit = CAT.get(name, {}).get('hit_at', 0) or 0
    if maxlen:
        a = a[:int(maxlen * SR)].copy(); f = int(fade * SR); a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int((t - hit) * SR)
    if i < 0: a = a[-i:]; i = 0
    j = min(N, i + len(a)); SFX[i:j] += a[:j - i] * gain
NUDGE = (0, 0)
E = [
    ('sub_knock', 0.15, 0.5), ('ticker_run', 0.6, 0.25), ('paper_slide', 0.9, 0.4), ('marker', 1.4, 0.35), ('sub_knock', A['below'], 0.5),
    ('impact_big', A['thirty'] - 0.05, 0.3), ('paper_slide', A['thirty'] + 0.1, 0.4), ('marker', A['thirty'] + 0.5, 0.35), ('heartbeat', A['safest'], 0.3),
    ('shutter', A['r1'] - 0.05, 0.35), ('coins_clink', A['fd'], 0.3), ('ticker_run', A['fd'] + 0.1, 0.2), ('pin_push', A['sits'], 0.3),
    ('woosh_air', A['rates'] - 0.1, 0.3), ('paper_slide', A['fed'] - 0.4, 0.4), ('marker', A['y2023'] - 0.8, 0.35),
    ('shutter', A['r2'] - 0.05, 0.35), ('pin_push', A['oil'] - 0.1, 0.35), ('pin_push', A['hikes'] - 1.8, 0.35), ('pin_push', A['hikes'] - 0.7, 0.35), ('sub_knock', A['hikes'] + 0.2, 0.45),
    ('shutter', A['r3'] - 0.05, 0.35), ('paper_slide', A['cash'] - 0.2, 0.4), ('marker', A['cash'] + 0.2, 0.3), ('stamp', A['sold'], 0.5), ('woosh_air', A['rushed'], 0.3), ('woosh_deep', A['out'] - 0.2, 0.3),
    ('vault_open', A['nobody'] - 0.1, 0.3), ('paper_slide', A['nobody'], 0.4), ('marker', A['t63'] - 0.2, 0.35), ('sub_knock', A['t63'], 0.45),
    ('woosh_air', A['traders'] - 0.1, 0.3), ('sub_knock', A['buying'] - 0.2, 0.4),
    ('paper_slide', A['y2011'] - 0.1, 0.4), ('marker', A['y2011'] + 0.1, 0.3), ('impact_big', A['nine'], 0.25), ('coin_win', A['x17'] - 0.5, 0.3),
    ('swoosh_slow', A['updown'] - 0.1, 0.3), ('metal_transform', A['years'], 0.3),
    ('shutter', A['secrets'] - 0.05, 0.35), ('polaroid', A['q1'] - 0.2, 0.45), ('paper_slide', A['q2'] - 0.05, 0.4), ('marker', A['q2'] + 0.3, 0.3), ('polaroid', A['q3'] - 0.2, 0.45), ('paper_slide', A['q3'] + 0.5, 0.35),
    ('stamp', A['another'] - 0.05, 0.35), ('typing_run', A['comment'] + 0.1, 0.2),
    ('page_turn', A['wrap'] - 0.1, 0.45), ('paper_drop', A['wrap'] + 0.25, 0.35), ('pin_push', A['wrap'] + 1.5, 0.3),
]
for n_, t_, g_ in CTA.events(R.MID_T0, R.PLAT): E.append((n_, t_, g_ * 0.5))
for n_, t_, g_ in CTA.events(R.END_T0, R.PLAT): E.append((n_, t_, g_))
for n, t, g in E: put(n, t, g)

def run(tag):
    vf = R.VFILE
    wf.write(R.ROOT + f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vf, '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/long/music/where_the_river_bends.wav'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.23,"
          f"volume=enable='between(t,{A['wrap']-0.2},{DUR})':volume=0.45,afade=t=out:st={DUR-1.2}:d=1.2[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', R.ROOT + f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', R.ROOT + f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', R.ROOT + f'mix_{tag}.wav'], check=True)
    json.dump({'nudge': NUDGE, 'end': A['comment']}, open(R.ROOT + f'ov_{tag}.json', 'w'))
    print('mixed', tag, round(DUR, 2))

if __name__ == '__main__':
    run(f"{os.environ.get('LANGV','en')}_{os.environ.get('PLAT','yt')}")
