"""Voice + real SFX library + ducked calm music -> mix_<plat>.wav"""
import sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render2 as R
A, LEAD, DUR = R.A, R.LEAD, R.DUR
SR = 48000
LIB = '/home/claude/sandy2606/why-channel-studio/sfx/'
CAT = json.load(open(LIB + 'catalog.json'))
def load(name):
    f = LIB + name + ('.wav' if not name.startswith('amb_') else '.mp3')
    out = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout
    return np.frombuffer(out, np.float32).reshape(-1, 2).copy()
N = int(DUR * SR) + SR
SFX = np.zeros((N, 2), np.float32)
def put(name, t, gain=0.5, maxlen=None, fade=0.25):
    a = load(name)
    hit = CAT.get(name, {}).get('hit_at', 0) or 0
    if maxlen:
        a = a[:int(maxlen * SR)].copy(); f = int(fade * SR); a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int((t - hit) * SR)
    if i < 0: a = a[-i:]; i = 0
    j = min(N, i + len(a)); SFX[i:j] += a[:j - i] * gain

E = [
    ('sub_knock', A['35'], 0.7),
    ('paper_slide', A['women'], 0.45),
    ('sub_knock', A['just'], 0.5),
    ('impact_big', A['why'], 0.32),
    ('map_unfold', A['people'], 0.45),
    ('pin_push', A['people'] + 0.8, 0.55),
    ('paper_slide', A['mandodari'], 0.45),
    ('polaroid', R.T('was') - 0.05, 0.4),
    ('stamp', A['son'] - 0.05, 0.55),
    ('shutter', A['dasara1'], 0.45),
    ('map_unfold', A['but'], 0.4),
    ('pin_push', A['pray1'] - 0.15, 0.45),
    ('paper_slide', A['pray1'], 0.4),
    ('woosh_air', A['jodhpur'] - 0.1, 0.35),
    ('marker', A['jodhpur'] + 0.1, 0.35),
    ('pin_push', A['jodhpur'] + 0.6, 0.5),
    ('paper_slide', A['devgoda'] - 0.1, 0.45),
    ('stamp', A['descend'], 0.55),
    ('shutter', A['dasara2'], 0.45),
    ('sub_knock', A['city'], 0.5),
    ('page_turn', A['bath'] - 0.1, 0.5),
    ('marker', A['funeral'] + 0.05, 0.4),
    ('paper_slide', R.T('go') - 0.1, 0.4),
    ('marker', A['temple1'] - 0.15, 0.4),
    ('woosh_air', A['baijnath'] - 0.4, 0.35),
    ('marker', A['baijnath'] - 0.2, 0.3),
    ('pin_push', A['baijnath'] + 0.4, 0.5),
    ('shutter', A['penance'] - 0.25, 0.45),
    ('paper_slide', A['penance'], 0.4),
    ('shutter', A['so'], 0.4),
    ('sub_knock', A['devotee'] - 0.2, 0.5),
    ('stamp', A['stopped'], 0.6),
    ('page_turn', A['because'], 0.5),
    ('marker', A['villain'] - 0.1, 0.45),
    ('key_press', A['villain'] + 0.25, 0.35), ('key_press', A['villain'] + 0.47, 0.35), ('key_press', A['villain'] + 0.69, 0.35),
    ('heartbeat', A['soyes'] + 0.2, 0.45),
    ('impact_big', A['family'], 0.5),
    ('mouse_click', A['comment'], 0.5),
]
for n, t, g in E: put(n, t, g)
put('typing_run', A['cta'] + 0.1, 0.35, maxlen=0.65, fade=0.1)
put('riser', A['family'], 0.25)
put('amb_fire', A['dasara1'], 0.10, maxlen=A['but'] - A['dasara1'], fade=0.4)
put('amb_fire', A['dasara2'], 0.10, maxlen=A['bath'] - A['dasara2'], fade=0.3)

def run(plat):
    E2 = []
    put_click = [('mouse_click', 25.6, 0.5)]
    S = SFX.copy()
    a = load('mouse_click'); i = int(25.6 * SR); S[i:i + len(a)] += a * 0.5
    wf.write(R.ROOT + 'sfx_track.wav', SR, S)
    # voice with lead
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + 'voice.wav', '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + 'vlead.wav'], check=True)
    music = '/home/claude/long/music/where_the_river_bends.wav'
    fc = (
        f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.24,"
        f"volume=enable='between(t,{A['soyes']-0.3},{A['family']})':volume=0.35,"
        f"afade=t=out:st={DUR-1.2}:d=1.2[m];"
        f"[0:a]asplit=2[v][vs];"
        f"[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
        f"[2:a]volume=1.0[s];"
        f"[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
        f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + 'vlead.wav', '-stream_loop', '-1', '-i', music, '-i', R.ROOT + 'sfx_track.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', R.ROOT + 'mix_pre.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + 'mix_pre.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', R.ROOT + 'mix.wav'], check=True)

if __name__ == '__main__':
    run('both')
    print('mixed')
