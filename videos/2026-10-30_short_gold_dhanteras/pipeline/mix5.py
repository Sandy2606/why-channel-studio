"""voice + real SFX + ducked calm music -> mix_<lang>_<plat>.wav ; env LANGV, PLAT"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render5 as R
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
NUDGE = (A['add'] + 0.5, A['add'] + 2.9)
E = [
    ('sub_knock', 0.15, 0.55), ('coins_clink', 0.5, 0.35), ('paper_slide', A['tonnes'] - 0.35, 0.45), ('marker', A['tonnes'] + 0.1, 0.4),
    ('woosh_air', A['add'] - 0.15, 0.3),
] + [('tick', A[k] - 0.1, 0.35) for k in ('america','germany','italy','france','russia','china','switz','rbi','japan','neth')] + [
    ('woosh_deep', A['more'] - 0.1, 0.35), ('sub_knock', A['more'] + 0.5, 0.5), ('stamp', A['more'] + 1.1, 0.4),
    ('shutter', A['why'] - 0.05, 0.4), ('heartbeat', A['why'] + 0.2, 0.3), ('scribble', A['trad'] + 0.3, 0.35), ('impact_big', A['math'] - 0.1, 0.3),
    ('page_turn', A['say'] - 0.1, 0.4), ('ticker_run', A['y2006'], 0.3), ('coin_win', A['lakh'] + 0.1, 0.35), ('paper_slide', A['y2006'] + 0.2, 0.35), ('marker', A['y2006'] + 0.5, 0.3),
    ('pin_push', A['nearly'] - 0.1, 0.4),
    ('woosh_air', A['same'] - 0.15, 0.3), ('riser', A['same'] - 0.05, 0.15), ('sub_knock', A['fd'], 0.4), ('tick', A['k38'] - 0.2, 0.35),
    ('shutter', A['hidden'] - 0.05, 0.4), ('sparkle_soft', A['oneprice'], 0.35), ('woosh_air', A['rupee1'] - 0.1, 0.3),
    ('paper_slide', A['y2006b'] - 0.1, 0.35), ('page_turn', A['d95'] - 0.15, 0.45), ('sub_knock', A['d95'], 0.4),
    ('swoosh_slow', A['loses'] - 0.1, 0.3), ('ticker_run', A['gold2'], 0.3), ('coin_prize', A['protects'] - 0.1, 0.3),
    ('mouse_click', A['cash'] - 0.05, 0.35), ('jar_set_down', A['pledge'], 0.35), ('woosh_air', A['minutes'] - 0.35, 0.3), ('coins_clink', A['minutes'] - 0.1, 0.35), ('stamp', A['paper'], 0.35),
    ('paper_slide', A['thats'] - 0.05, 0.45), ('marker', A['second'], 0.4), ('paper_slide', A['l16'] - 0.4, 0.35), ('marker', A['l16'] - 0.1, 0.3), ('impact_big', A['l16'] + 0.2, 0.3),
    ('polaroid', A['mom'] - 0.1, 0.45), ('polaroid', A['sister'] - 0.1, 0.45), ('polaroid', A['gf'] - 0.1, 0.45), ('scribble', A['wasting'] + 0.3, 0.35),
    ('woosh_deep', A['saving'] - 0.2, 0.3), ('metal_transform', A['future'], 0.3), ('impact_big', A['future'] + 0.3, 0.25),
    ('page_turn', A['full'] - 0.1, 0.45), ('pin_push', A['full'] + 0.3, 0.35), ('paper_slide', A['comment'] - 0.1, 0.35),
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
          f"volume=enable='between(t,{A['saving']-0.2},{A['full']})':volume=0.4,afade=t=out:st={DUR-1.2}:d=1.2[m];"
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
