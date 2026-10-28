"""voice + real SFX + ducked calm music -> mix_<lang>_<plat>.wav ; env LANGV, PLAT"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render4 as R
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
NUDGE = (A['p38'], A['p38'] + 2.4)
E = [
    ('sub_knock', 0.2, 0.55), ('sub_knock', A['broke'] - 0.1, 0.45),
    ('paper_slide', A['weeks'] - 0.35, 0.45), ('marker', A['weeks'], 0.4),
    ('map_unfold', A['sends'] - 0.05, 0.45), ('pin_push', A['sends'], 0.45), ('pin_push', A['abroad'] - 0.3, 0.45),
    ('woosh_air', A['t47'] - 0.2, 0.3), ('sub_knock', A['t47'], 0.5),
    ('paper_slide', A['loan'] - 0.6, 0.4), ('marker', A['loan'] - 0.4, 0.35),
    ('shutter', A['worked'] - 0.05, 0.4), ('sub_knock', A['survived'], 0.4),
    ('impact_big', A['y2024'], 0.3), ('paper_slide', A['opposite'] - 0.6, 0.45),
    ('map_unfold', A['t100'] - 0.15, 0.35), ('woosh_air', A['t100'] - 0.05, 0.3), ('sub_knock', A['t100'], 0.45),
    ('woosh_air', A['t102'] - 0.3, 0.3), ('sub_knock', A['t102'], 0.45),
    ('paper_slide', A['diwali'] - 0.2, 0.4), ('marker', A['diwali'] + 0.2, 0.35),
    ('paper_slide', A['y2023'] - 0.05, 0.4), ('ticker_run', A['p38'] - 0.1, 0.25), ('ticker_run', A['p77'] - 0.2, 0.3), ('marker', A['p77'] - 0.1, 0.35),
    ('shutter', A['why'] - 0.05, 0.4), ('heartbeat', A['why'] + 0.1, 0.35),
    ('paper_slide', A['y2022'] - 0.05, 0.45), ('marker', A['b300'] - 0.05, 0.35), ('sub_knock', A['b300'], 0.5),
    ('vault_open', A['froze'] - 0.2, 0.35), ('stamp', A['froze'], 0.45),
    ('paper_slide', A['lesson'] - 0.1, 0.4), ('marker', A['keep'] + 0.5, 0.35),
    ('map_unfold', A['y1991b'] - 0.05, 0.4), ('woosh_air', A['y1991b'], 0.25), ('woosh_air', A['now2'], 0.3),
    ('impact_big', A['protect'], 0.35),
    ('page_turn', A['full'] - 0.1, 0.45), ('marker', A['full'] + 0.3, 0.25),
    ('paper_slide', A['comment'] - 0.1, 0.35),
    ('mouse_click', NUDGE[0] + 0.5, 0.45), ('mouse_click', A['comment'] + 0.4, 0.45),
]
for n, t, g in E: put(n, t, g)
put('typing_run', A['comment'] - 0.05, 0.25, maxlen=0.5, fade=0.1)

def run(tag):
    vf = R.VFILE
    wf.write(R.ROOT + f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vf, '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/long/music/where_the_river_bends.wav'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.23,"
          f"volume=enable='between(t,{A['why']-0.2},{A['y2022']})':volume=0.4,afade=t=out:st={DUR-1.2}:d=1.2[m];"
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
