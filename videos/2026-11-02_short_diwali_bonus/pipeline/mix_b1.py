"""voice + real SFX + ducked music -> mix_<lang>_<plat>.wav"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.argv = sys.argv[:1]
import render_b1 as R
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
E = [('woosh_air', 0.02, 0.25), ('sparkle_soft', A['gift'] - 0.1, 0.35), ('stamp', A['law1'] + 0.05, 0.4), ('impact_big', A['n21'] - 0.05, 0.32), ('sub_knock', A['n21'], 0.45),
     ('paper_slide', S('2'), 0.4), ('stamp', A['corr'], 0.5), ('marker', A['sorry'], 0.35), ('page_turn', A['since'] - 0.2, 0.4), ('marker', A['since'] + 0.15, 0.3), ('impact_big', A['code2'] - 0.1, 0.22),
     ('paper_slide', S('3') + 0.4, 0.3), ('metal_transform', A['merge'] - 0.1, 0.3), ('scribble', A['never'] + 0.4, 0.35), ('ui_pop', A['annual'] - 0.1, 0.4), ('sparkle_soft', A['many'], 0.3),
     ('woosh_air', A['test'] - 0.2, 0.25), ('paper_drop', A['boxes'] - 0.1, 0.35), ('ui_pop', A['counts'] - 0.1, 0.3), ('coins_clink', A['r18'], 0.28),
     ('tick', A['less'] - 0.3, 0.5), ('ui_pop', A['d30'] - 0.1, 0.35), ('stamp', A['must'] - 0.1, 0.5), ('tick', A['old5'], 0.4), ('tick', A['old5'] + 0.35, 0.4),
     ('woosh_deep', A['arjun'] - 0.1, 0.3), ('coins_clink', A['a45'], 0.25), ('sub_knock', A['cover'] - 0.1, 0.4), ('paper_slide', A['contract'] - 0.2, 0.4),
     ('heartbeat_slow', A['surpr'], 0.25), ('sparkle_soft', A['protect'] - 0.2, 0.4),
     ('ui_pop', A['catch'] - 0.2, 0.4), ('sub_knock', A['notfull'] - 0.2, 0.35),
     ('ui_pop', S('9'), 0.3), ('pin_push', A['city'] - 0.1, 0.35), ('pin_push', A['city'] + 0.2, 0.35), ('ui_bell', A['every'] - 0.1, 0.35),
     ('scribble', A['not18'] - 0.3, 0.35), ('impact_big', A['m12'] - 0.15, 0.2), ('paper_slide', A['that12'] + 0.2, 0.35), ('marker', A['that12'] + 0.5, 0.3),
     ('key_press', S('12') - 0.05, 0.4), ('key_press', S('12') + 0.25, 0.4), ('key_press', A['twelve'] - 0.1, 0.4), ('coin_win', A['about12'] - 0.15, 0.3), ('coins_clink', A['r288'] - 0.2, 0.35),
     ('woosh_deep', S('13'), 0.3), ('impact_big', A['four'] - 0.1, 0.25),
     ('coin_flutter', S('14') + 0.2, 0.3), ('ui_bell', A['bank'] + 0.2, 0.4), ('tick', A['cash'] + 0.2, 0.4),
     ('ui_pop', A['w12'] - 0.2, 0.35), ('marker', A['w20'] - 0.2, 0.3), ('stamp', A['lose'] - 0.1, 0.4),
     ('page_turn', A['notif'] - 0.2, 0.4), ('paper_slide', A['aug'] - 0.3, 0.4), ('marker', A['aug'], 0.3), ('paper_slide', A['aug'] + 1.2, 0.3),
     ('ui_pop', A['fraud'] - 0.1, 0.3), ('ui_pop', A['fraud'] + 0.2, 0.3), ('ui_pop', A['fraud'] + 0.5, 0.3), ('impact_big', A['now17'] - 0.1, 0.25),
     ('page_turn', S('18'), 0.35), ('scribble', A['nov30'] - 0.2, 0.35), ('stamp', A['didnt'] - 0.1, 0.35),
     ('woosh_tunnel', S('19') - 0.1, 0.3), ('swoosh_slow', S('L'), 0.25)]
for i in range(4): E.append(('swoosh_slow', S('3') + 0.15 * i, 0.22))
for i in range(4): E.append(('tick', A['skilled'] - 0.2 + 0.12 * i, 0.3))
for i in range(6): E.append(('ui_pop', S('19') + 0.55 + 0.15 * i, 0.22))
for n, t, g in E: put(n, t, g)
put('riser', A['howmuch'], 0.18, maxlen=1.6); put('riser_synth', A['p20'] - 0.4, 0.18, maxlen=1.8)
put('machine_hum', S('15'), 0.12, maxlen=3.0, fade=0.8); put('space_drone', S('19'), 0.22, maxlen=4.0, fade=1.0)
for n_, t_, g_ in CTA.events(R.END_T0, R.PLAT): put(n_, t_, g_)
def run(tag):
    wf.write(R.ROOT + f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.VFILE, '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), R.ROOT + f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/long/music/the_quiet_meridian.wav'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{S('19')-0.2},{DUR})':volume=0.45,afade=t=in:st=0:d=0.25,afade=t=out:st={DUR-0.6}:d=0.6[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', R.ROOT + f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', R.ROOT + f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', R.ROOT + f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.0:LRA=8', '-ar', '48000', R.ROOT + f'mix_{tag}.wav'], check=True)
    print('mixed', tag, round(DUR, 2))
if __name__ == '__main__':
    run(f"{os.environ.get('LANGV','en')}_{os.environ.get('PLAT','yt')}")
