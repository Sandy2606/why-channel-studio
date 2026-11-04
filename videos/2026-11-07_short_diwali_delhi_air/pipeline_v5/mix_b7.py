"""voice + real SFX + ducked music -> mix_<lang>_<plat>.wav"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render_b6 as R
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
E14 = R.E
pc = A['three5'] - 0.3; cc = max(A['c23'] + 0.4, E14('13') - 2.7)
E = [('swoosh_slow', 0.3, 0.25), ('footsteps_soft_indoor', S('M1') - 0.3, 0.18), ('ui_pop', S('M1') - 0.1, 0.22), ('ui_pop', S('M2') - 0.1, 0.22),
     ('woosh_deep', S('3') - 0.2, 0.3), ('space_drone', S('3') - 0.1, 0.12), ('marker', A['hair'] - 0.1, 0.25),
     ('woosh_air', A['xr'], 0.25), ('shutter', A['xr'] + 0.1, 0.15), ('water_bubbles', A['alv'], 0.12),
     ('heartbeat', A['hb'] + 0.2, 0.35), ('sub_knock', A['strokes'] - 0.3, 0.3),
     ('swoosh_slow', S('4') - 0.1, 0.25), ('heartbeat_slow', A['eight4'] - 0.4, 0.2),
     ('woosh_air', S('5') - 0.1, 0.25), ('tick', A['b488'] - 0.4, 0.25), ('page_turn', pc, 0.3), ('marker', pc + 0.3, 0.3), ('sub_knock', A['eight5'] - 0.1, 0.3),
     ('firework_whistle_echo', A['crackers6'] - 0.5, 0.3), ('boom_distant', A['crackers6'] + 0.6, 0.25), ('boom_distant', A['crackers6'] + 1.5, 0.18),
     ('woosh_deep', S('7') - 0.1, 0.3), ('metal_transform', A['lid'] - 0.3, 0.25),
     ('ui_pop', A['veh8'], 0.25), ('ui_pop', A['dust'], 0.25), ('ui_pop', A['industry'], 0.25), ('ui_pop', A['garbage'], 0.25), ('marker', A['biggest'] - 0.3, 0.3),
     ('map_unfold', S('M8') - 0.1, 0.2), ('woosh_tunnel', S('9') - 0.1, 0.22), ('machine_hum', A['gurpreet'], 0.10),
     ('tick', A['two9'] - 0.2, 0.25), ('ticker_run', A['two9'], 0.12), ('ui_click', A['machines'] - 0.2, 0.3), ('match_light', A['burning'] - 0.25, 0.35),
     ('woosh_air', S('10') - 0.1, 0.25), ('marker', A['p7'] - 0.3, 0.3), ('marker', A['p22'] - 0.3, 0.3),
     ('woosh_deep', S('11') - 0.1, 0.25), ('ui_click', A['constr'], 0.3), ('ui_click', A['cars'], 0.3), ('ui_click', A['hybrid'], 0.3),
     ('woosh_air', S('12') - 0.1, 0.3), ('tick', A['pm10'] - 0.3, 0.25), ('ui_bell', A['p40'], 0.3),
     ('woosh_air', S('13') - 0.1, 0.2), ('ticker_run', A['cleanest'] - 0.4, 0.15), ('marker', A['annual'], 0.25),
     ('page_turn', cc, 0.3), ('marker', cc + 0.3, 0.3), ('marker', cc + 1.35, 0.3), ('sub_knock', A['didnt'], 0.3),
     ('woosh_tunnel', S('14') - 0.1, 0.25), ('ticker_run', A['y2013'], 0.15), ('ui_bell', A['v70'], 0.3),
     ('tick', A['coal'], 0.3), ('tick', A['gas'], 0.3), ('tick', A['vrules'], 0.3), ('tick', A['neigh'], 0.3), ('ui_bell', A['decade'], 0.25),
     ('woosh_deep', S('15') - 0.1, 0.25), ('ui_pop', A['spike15'], 0.25), ('ui_pop', A['winter15'], 0.25), ('ui_pop', A['every15'], 0.25),
     ('riser', A['region'] - 1.0, 0.15), ('sparkle_soft', A['region'] + 0.3, 0.3),
     ('woosh_tunnel', S('16') - 0.1, 0.3), ('ui_pop', A['sunday'] - 0.3, 0.22), ('swoosh_slow', S('L') + 0.1, 0.25)]
for i in range(3): E.append(('ui_pop', S('M5') + 0.3 + 0.15 * i, 0.25))
for k in ('M5', 'M8', 'M10', 'M12', 'M13'): E.append(('ui_pop', S(k) - 0.2, 0.18))
for i in range(6): E.append(('ui_pop', S('16') + 0.35 + 0.1 * i, 0.22))
for n, t, g in E: put(n, t, g)
put('wind_ambience', 0.0, 0.14, maxlen=S('M1'), fade=1.0)
put('amb_fire', A['burning'] - 0.2, 0.14, maxlen=S('11') - A['burning'], fade=0.6)
put('wind_ambience', S('L'), 0.14, maxlen=DUR - S('L'), fade=0.3)
for n_, t_, g_ in CTA.events(R.END_T0, R.PLAT): put(n_, t_, g_)
def run(tag):
    wf.write(R.ROOT + f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.VFILE, '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/long/music/the_quiet_meridian.wav'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{S('16')-0.2},{DUR})':volume=0.45,afade=t=in:st=0:d=0.25,afade=t=out:st={DUR-0.6}:d=0.6[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', R.ROOT + f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', R.ROOT + f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', R.ROOT + f'mix_{tag}.wav'], check=True)
    print('mixed', tag, round(DUR, 2))
if __name__ == '__main__':
    run(f"{os.environ.get('LANGV','en')}_{os.environ.get('PLAT','yt')}")
