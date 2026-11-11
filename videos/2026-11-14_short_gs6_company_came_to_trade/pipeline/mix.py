"""GS 6/6: voice + real SFX (sfx/ only) + ducked approved music -> mix_<lang>_<plat>.wav (-14 LUFS, true peak <= -1 dBTP after mux).
Events follow on-screen action. Built so far for the preview ranges (Plassey, silver -> revenue); other scenes are added after approval."""
import os, sys, json, subprocess, numpy as np, scipy.io.wavfile as wf
sys.path.insert(0, '/home/claude/gs6'); sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
from cues import *
import cta_card as CTA
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
def bed(path, t0, t1, gain, fade=0.8, skip=0.0):
    a = load(path)[int(skip * SR):]; n = int((t1 - t0) * SR)
    while len(a) < n: a = np.concatenate([a, a])
    a = a[:n].copy(); r = np.sqrt((a ** 2).mean()) + 1e-6; a *= 0.05 / r; f = int(fade * SR); a[:f] *= np.linspace(0, 1, f)[:, None]; a[-f:] *= np.linspace(1, 0, f)[:, None]
    i = int(t0 * SR); SFX[i:i + n] += a * gain
SCs = dict(SC); KC = 'C' if has('C') else 'C2'; KC1 = 'C' if has('C') else 'C1'
# ---- Plassey: the plate lands; the two sides draw in; one soft tick per Company dot; a distant battlefield under the 50,000;
#      the cavalry slides aside (a slow swoosh, no gallop: it did not fight); the painting arrives with a page turn
c3 = AT('B', 'three', 'మూడు') - .1; c50 = AT('B', 'fifty', 'యాభై') - .1; cnv = AT(KC1, 'never', 'యుద్ధమే') - .1
cmj = AT(KC1, 'Mir', 'మీర్') - .1; chp = AT(KC1, 'helped', 'కంపెనీ') - .15
put('page_turn', SCs['plassey'] + .05, .18); put('swoosh_slow', SCs['plassey'] + .6, .10)
for i in range(6): put('tick', c3 + .1 + i * .08, .07)
put('paper_slide', AT('B', 'troops', 'సైనికులు…'), .12)
bed(LIB + 'amb/drums.mp3', SCs['plassey'] + .2, S('Q2') - .1, .12, fade=1.2)
bed(LIB + 'amb/battle.mp3', c50 - .2, S('Q2') + .1, .30, fade=1.0); put('swoosh_slow', c50, .14)
bed(LIB + 'amb/battle.mp3', E('Q2') + .1, chp, .16, fade=.8, skip=8.0)
put('swoosh_slow', cnv + .1, .18); put('paper_slide', cmj + .05, .14); put('page_turn', chp + .05, .18)
# ---- payoff: silver bars clink into the cloth; cloth leaves for Europe; after 1765 the coins rise from Bengal's fields
c_sil = AT(KC, 'silver', 'వెండి') - .15; c_after = AT(KC, 'After', 'తర్వాత,') - .15; c_end = AT(KC, 'collected', 'పన్నులతోనే') - .1
put('page_turn', SCs['payoff'] + .05, .16); bed(LIB + 'harbour_waves.wav', SCs['payoff'], c_after + .6, .22, fade=1.0)
put('jar_set_down', c_sil + .25, .10)
put('swoosh_slow', c_after - .1, .16); put('coins_clink', c_after + .55, .18); put('coin_flutter', c_after + 1.2, .10)
put('paper_slide', c_end + .05, .14)
# ---- the question: the season line fills mark by mark
for i in range(7): put('tick', SCs['question'] + .1 + i * 1.3 / 6, .06)
put('paper_slide', SCs['question'] + .85, .12)

# ---- hook: a quiet court; the years run; Fort William arrives with a page turn
c150 = AT('A', 'hundred', 'నూట') - .15; chelp = AT('A', 'helped', 'బెంగాల్') - .15
bed(LIB + 'amb/court.mp3', 0.0, c150 + .3, .30, fade=.3); put('ticker_run', c150 + .05, .10, maxlen=chelp - c150, fade=.15); put('page_turn', chelp + .02, .18)
if not TE:
    # ---- permission (EN): the map opens; Surat and Agra pinned; the road drawn; Swally at sea (one distant cannon, owner-cleared, provenance unverified); 1613; Roe at court
    s0p = SCs['perm']; ch_ = AT('A', 'Hawkins', '') - .15; cj_ = AT('A', 'Jahangir.', ''); c12 = AT('A', '1612,', '') - .15; csw = AT('A', 'Swally,', '') - .2
    cdl = AT('A', 'deal', '') - .15; ccf = AT('A', 'confirmed', '') - .15; c15 = AT('A', '1615', '') - .2
    put('map_unfold', s0p + .05, .14); put('pin_push', ch_ + .05, .16); put('scribble', AT('A', 'travelled', ''), .06, maxlen=1.4, fade=.3); put('pin_push', cj_ - .25, .16)
    bed(LIB + 'harbour_waves.wav', c12, cdl + .4, .30, fade=.6); bed(LIB + 'ship_creak.mp3', c12 + .3, cdl, .22, fade=.6)
    put('cannon_distant', csw + .1, .14)
    put('paper_slide', cdl + .05, .14); put('marker', ccf + .2, .10)
    put('page_turn', c15 + .05, .18); bed(LIB + 'amb/court.mp3', c15, SCs['war'], .22, fade=.6)
# ---- 1686: the war (one low knock on LOST), the three terms, Calcutta
s0w = SCs['war']; c86 = AT('A', '1686,', '1686లో') - .15; cwar = AT('A', 'war', 'యుద్ధానికి') - .1; clost = AT('A', 'lost.', 'ఓడిపోయింది.') - .15
put('map_unfold', s0w + .05, .12)
if TE: put('pin_push', s0w + .15, .14); put('pin_push', s0w + 1.25, .16)
put('swoosh_slow', cwar, .14); put('sub_knock', clost + .05, .16)
for en, te in (('pardon,', 'క్షమాపణ'), ('fine,', 'జరిమానా'), ('promise', 'ఉంటామని')): put('paper_slide', AT('A', en, te) - .15, .12)
put('pin_push', AT('A', '1690,', '1690లో') - .1, .18)
# ---- 1717: the farman (quill), one paper per term; the river with the passes
s0f = SCs['farman']; cco = AT('A', 'men', 'కంపెనీ', n=1 if not TE else 3) - (.5 if not TE else .15)
put('page_turn', s0f + .05, .16); put('quill_writing.mp3', AT('A', 'farman:', 'ఫర్మానా') - .1, .12, maxlen=1.6, fade=.3, path=LIB + 'quill_writing.mp3')
for en, te in (('duty-free', 'సుంకం'), ('3,000', '3,000'), ('passes', 'దస్తక్')): put('paper_drop', AT('A', en, te) - .15, .10)
bed(LIB + 'harbour_waves.wav', cco, SCs['cartoon1'] + .2, .28, fade=.6); put('marker', AT('A', 'misused', 'దుర్వినియోగం') - .1, .10)
# ---- the wars in the south: pins, the clash, sepoys drilling (soft footsteps and very low drums), the thrones
s0s = SCs['wars']; csp = AT('B', 'sepoys,', 'సిపాయిలు') - .2; cba = AT('B', 'backed', 'కర్ణాటక,') - .3
put('map_unfold', s0s + .05, .12); put('pin_push', AT('B', 'French', 'ఫ్రెంచ్,') - .1, .14); put('pin_push', AT('B', 'English', 'ఇంగ్లీష్') - .1, .14)
bed(LIB + 'amb/footsteps_stone.mp3', csp, cba, .22, fade=.5); bed(LIB + 'amb/drums.mp3', csp, cba + .3, .10, fade=.6)
put('paper_drop', AT('B', 'Carnatic', 'కర్ణాటక,') - .1, .12); put('paper_drop', AT('B', 'Hyderabad.', 'హైదరాబాద్') - .1, .12)
put('paper_slide', AT('B', 'French', 'మొదట', n=2 if not TE else 1) - .1, .12)
# ---- the lesson: a low knock on FAILED, a soft lift on PAID
put('page_turn', SCs['lesson'] + .05, .14); put('sub_knock', AT('B', 'failed.', 'ఓడిపోయింది.') - .1, .12); put('sparkle_soft', AT('B', 'paid.', 'లాభం.') - .1, .10)
# ---- Siraj-ud-Daulah: the fort, the labels, Calcutta taken, the army sails from Madras
s0j = SCs['siraj']; put('page_turn', s0j + .05, .14); bed(LIB + 'harbour_waves.wav', s0j, SCs['plassey'], .22, fade=.8)
put('marker', AT('B', 'fortifications', 'కోటలు') - .1, .10); put('marker', AT('B', 'passes.', 'పాసులను') - .1, .10)
put('pin_push', AT('B', 'seized', 'కలకత్తాను') - .1, .18); put('swoosh_slow', AT('B', 'army', 'సైన్యాన్ని') - .2, .14); bed(LIB + 'ship_creak.mp3', AT('B', 'army', 'సైన్యాన్ని'), SCs['plassey'], .20, fade=.5)
# ---- Buxar and the diwani: pins, the hatched grant, the painting
s0b = SCs['buxar']; put('map_unfold', s0b + .05, .12); put('pin_push', AT(KC, 'Buxar', 'బక్సర్‌లో') - .1, .16)
put('quill_writing.mp3', AT(KC, 'right', 'బెంగాల్,') - .1, .12, maxlen=1.6, fade=.3, path=LIB + 'quill_writing.mp3'); put('page_turn', AT(KC, 'emperor', 'మొఘల్') - .15, .14)
# ---- tease and the Season 1 slide (real click/bell)
put('swoosh_slow', SCs['tease'] + .05, .16)
for n_, t_, g_ in CTA.events(SCs['slide'] + 0.9, PLAT):
    if n_ != 'woosh_air': put(n_, t_, g_ * 0.8)

def run(tag):
    os.chdir(ROOT); wf.write(f'sfx_{tag}.wav', SR, SFX)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'voice_{LANGV}.wav', '-af', f'adelay={int(LEAD*1000)}|{int(LEAD*1000)},apad', '-ac', '2', '-ar', '48000', '-t', str(DUR), f'vlead_{tag}.wav'], check=True)
    lift = (c_after - .3, c_end + 2.5)      # music lifts slightly under the payoff
    fc = (f"[1:a]equalizer=f=2200:t=q:w=1:g=-5,highshelf=f=6000:g=-5,lowpass=f=10000,volume=0.22,"
          f"volume=enable='between(t,{lift[0]},{lift[1]})':volume=1.35,volume=enable='between(t,{SCs['slide']},{DUR})':volume=1.6,afade=t=in:st=0:d=0.3,afade=t=out:st={DUR-0.5}:d=0.5[m];"
          f"[0:a]asplit=2[v][vs];[m][vs]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=300:makeup=1[md];"
          f"[2:a]volume=1.0[s];[s][v]sidechaincompress=threshold=0.05:ratio=2.2:attack=10:release=250:makeup=1[sd];"
          f"[0:a][md][sd]amix=inputs=3:normalize=0:duration=first,alimiter=limit=0.95[mx]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'vlead_{tag}.wav', '-stream_loop', '-1', '-i', MUSIC, '-i', f'sfx_{tag}.wav',
                    '-filter_complex', fc, '-map', '[mx]', '-t', str(DUR), '-ar', '48000', f'mixpre_{tag}.wav'], check=True)
    # loudness to -14 LUFS with a -2 dBTP target, then a 4x-oversampled true-peak limiter so the AAC encode stays under -1 dBTP
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'mixpre_{tag}.wav', '-af', 'loudnorm=I=-14:TP=-2:LRA=8,aresample=192000,alimiter=limit=0.76:attack=1:release=60:level=disabled,aresample=48000', '-ar', '48000', f'mix_{tag}.wav'], check=True)
    print('mixed', tag, DUR)
if __name__ == '__main__':
    run(f'{LANGV}_{PLAT}')
