"""voice + real SFX + ducked music -> mix_<lang>_<plat>.wav"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render_b2 as R
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
E = [('woosh_air', 0.02, 0.25), ('stamp', A['itsnot'] - 0.15, 0.45), ('stamp', A['itsnot'] + 0.07, 0.45), ('stamp', A['itsnot'] + 0.29, 0.5),
     ('phone_typing', A['fwd'] - 0.3, 0.25), ('page_turn', S('3') - 0.05, 0.4), ('marker', S('3') + 0.8, 0.35), ('paper_drop', A['y2003'] - 0.2, 0.3), ('ui_pop', A['mil'] - 0.2, 0.3),
     ('swoosh_slow', S('4') + 0.1, 0.25), ('scribble', A['fire'] + 0.3, 0.35), ('ui_pop', A['years4'] - 0.1, 0.35),
     ('tick', A['white'] - 0.15, 0.45), ('tick', A['blue'] - 0.15, 0.45), ('tick', A['green'] - 0.15, 0.45), ('tick', A['red'] - 0.15, 0.45),
     ('impact_big', A['growing'], 0.3), ('marker', A['onenight'], 0.4), ('sub_knock', A['onenight'] + 0.05, 0.4),
     ('sparkle_soft', A['clouds'] - 0.2, 0.35), ('sparkle_soft', A['city7'] - 0.1, 0.35),
     ('woosh_deep', A['real8'] - 0.3, 0.3), ('ui_pop', A['real8'] + 0.4, 0.3), ('tick', S('9') + 0.6, 0.45), ('sub_knock', A['rainbow'] - 0.2, 0.4),
     ('paper_slide', S('10') - 0.05, 0.4), ('marker', A['subtle'] - 0.2, 0.4), ('pin_push', A['m750'] - 0.3, 0.35), ('impact_big', A['k824'] - 0.1, 0.2),
     ('sparkle_soft', S('12'), 0.3), ('ui_bell', A['blends'] - 0.2, 0.3), ('typing_run', A['reply'] + 0.1, 0.25), ('ui_pop', A['wrong'] + 0.4, 0.4),
     ('woosh_tunnel', S('14') - 0.1, 0.3), ('swoosh_slow', S('L'), 0.25)]
for i in range(5): E.append(('ui_pop', A['fwd'] + 0.4 + 0.25 * i, 0.2))
for i in range(6): E.append(('ui_pop', S('14') + 0.35 + 0.1 * i, 0.22))
for n, t, g in E: put(n, t, g)
put('space_drone', S('7'), 0.2, maxlen=4.0, fade=1.0); put('riser', A['k824'] - 1.2, 0.15, maxlen=1.4)
for n_, t_, g_ in CTA.events(R.END_T0, R.PLAT): put(n_, t_, g_)
def run(tag):
    wf.write(R.ROOT + f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.VFILE, '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/long/music/beneath_the_rising_current.wav'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{S('14')-0.2},{DUR})':volume=0.45,afade=t=in:st=0:d=0.25,afade=t=out:st={DUR-0.6}:d=0.6[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', R.ROOT + f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', R.ROOT + f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', R.ROOT + f'mix_{tag}.wav'], check=True)
    print('mixed', tag, round(DUR, 2))
if __name__ == '__main__':
    run(f"{os.environ.get('LANGV','en')}_{os.environ.get('PLAT','yt')}")
