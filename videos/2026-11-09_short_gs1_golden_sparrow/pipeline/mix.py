"""voice + real SFX (sfx/ only) + ducked approved music -> mix_<lang>_<plat>.wav (−14 LUFS)"""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/gs1s'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
from cues import *
import cta_card as CTA
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
# hook: low hit on the 24%, field bed under hook + reveal
E += [('sub_knock', 0.18, 0.45)]
amb('village.mp3', 0.0, SCs['cartoon1'] + 0.3, 0.55)
amb('birds_cattle.mp3', SCs['reveal'] - 0.2, SCs['tease'] + 0.2, 0.45)
# chart: ticker as each bar grows, knock on 24.4, card slide for the border note, page for the source card
for w in (('24', '24'), ('1950', '1950')): E.append(('ticker_run', AT('1.4', *w) - 0.2, 0.25))
E.append(('ticker_run', AT('1.4', 'About', 'దాదాపు', n=2) - 0.1, 0.22))
E.append(('sub_knock', AT('1.4', '24', '24') + 0.9, 0.45))
E.append(('paper_slide', AT('1.4', '1950', '1950') - 0.1, 0.25))
E.append(('page_turn', AT('1.4', 'Maddison', 'Maddison') - 0.1, 0.25))
if 'circle' in SCs:
    E += [('marker', SCs['circle'] + 0.1, 0.3), ('marker', AT('1.4e', '22', '22') - 0.1, 0.3), ('sub_knock', AT('1.4e', 'half', 'half'), 0.4)]
# people / income
E += [('tick', AT('1.6', 'quarter', 'నాలుగో'), 0.3), ('ui_pop', AT('1.6', 'quarter', 'నాలుగో') + 0.3, 0.18), ('tick', AT('1.6', 'huge', 'పెద్దది'), 0.25),
      ('ticker_run', AT('1.6', 'Income', 'ఒక్కొక్కరి'), 0.2), ('sub_knock', AT('1.6', 'below', 'తక్కువగా'), 0.4)]
# paper-cut
E += [('paper_slide', SCs['paper'] + 0.1, 0.3), ('paper_slide', AT('1.7', 'split.', 'సమానంగా'), 0.32), ('paper_slide', AT('1.7', 'Caste', 'చాలామంది') - 0.1, 0.3),
      ('page_turn', AT('1.7', 'schooling', 'చదువు') - 0.1, 0.3)]
if TE: E.append(('scribble', AT('1.7', 'ప్రతి', 'ప్రతి') + 0.3, 0.3))
# reveal: coins, then swell into the cotton, silence on "field"
E += [('coin_flutter', SCs['reveal'] + 0.2, 0.2), ('riser', AT('1.8b', 'field.', 'పొలంలోనే') - 0.15, 0.12)]
# tease: stamp + page turn on the Act flash
E += [('stamp', AT('T', 'Britain', 'బ్రిటన్'), 0.55), ('page_turn', M['T'][1] - 0.9, 0.3)]
# slide: CTA click/bell (no hissy woosh)
for n_, t_, g_ in CTA.events(SCs['slide'] + 0.9, PLAT):
    if n_ != 'woosh_air': put(n_, t_, g_ * 0.8)
put('swoosh_slow', SCs['loop'] + 0.05, 0.18)
for n, t, g in E: put(n, t, g)
def run(tag):
    os.chdir(ROOT); wf.write(f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'voice_{LANGV}.wav', '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), f'vlead_{tag}.wav'], check=True)
    music = '/home/claude/why-channel-studio/music/where_the_river_bends.mp3'
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{SCs['slide']},{DUR})':volume=1.6,afade=t=in:st=0:d=0.3,afade=t=out:st={DUR-0.5}:d=0.5[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', music, '-i', f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', f'mixpre_{tag}.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=8', '-ar', '48000', f'mix_{tag}.wav'], check=True)
    print('mixed', tag, DUR)
if __name__ == '__main__':
    run(f'{LANGV}_{PLAT}')
