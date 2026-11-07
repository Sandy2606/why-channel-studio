"""Sound events for the v3 sequences (spot effects synced to the animation) + ambience beds."""
import sys
sys.path.insert(0, '/home/claude/gs/film3')
LOOM_HITS = [7.36, 10.28, 19.95, 29.71]          # onsets in loom_shuttle.mp3 (s)
SUBEV = []
def events(film, seqs):
    import fx2
    SUBEV[:] = fx2.subscribe_events(film.SUB_T) if '3.12' in film.M else []
    """returns [(file, t_film, gain_db, src_offset, dur, fade, duck_db)]"""
    cue = film.cue; M = film.M; ev = []
    def add(f, t, g, off=0.0, dur=None, fade=0.05, duck=-6): ev.append((f, t, g, off, dur, fade, duck))
    if '2.1' in M:
        add('sub_knock.wav', cue('2.1', 'ban', 'నిషేధిస్తుంది') + 0.05, -14)
        add('swoosh_slow.wav', cue('2.1', 'follow', 'చేతుల') - 0.15, -18, dur=1.4)
    if '2.2' in M:
        add('sparkle_soft.wav', cue('2.2', 'many', 'ఎంతోమంది'), -22)
    if '2.3' in M:
        a, b = M['2.3']
        for k, h in enumerate(seqs.s23_hits(a, b)): add('loom_shuttle.mp3', h - 0.05, -4, off=LOOM_HITS[k % 4] - 0.05, dur=0.7, fade=0.03, duck=-4)
        add('coins_clink.wav', cue('2.3', 'advance', 'ముందుగానే') + 0.5, -12)
        add('stamp.wav', cue('2.3', 'price', 'ధర'), -10)
        add('sub_knock.wav', cue('2.3', 'bargaining', 'బేరమాడే') + 0.3, -14)
    if '2.6' in M:
        c = cue('2.6', 'drew', 'design'); add('quill_writing.mp3', c, -14, off=12, dur=4.2, fade=0.4, duck=-8)
        add('sparkle_soft.wav', cue('2.6', 'weeks', 'వారాల') + 0.6, -22)
    if '3.2' in M:
        c = cue('3.2', 'seagate', 'సముద్ర') - 0.1; a, b = M['3.2']
        add('ship_creak.mp3', c, -10, off=2, dur=b - c + 0.4, fade=0.5, duck=-8)
        add('harbour_waves.wav', c, -12, off=5, dur=b - c + 0.4, fade=0.6, duck=-10)
    if '3.3' in M:
        a, b = M['3.3']
        for k, (en, te) in enumerate([('Persia', 'Persia'), ('Arabia', 'అరేబియా'), ('Burma', 'బర్మా'), ('Southeast', 'ఆగ్నేయాసియా')]):
            add('ship_creak.mp3', cue('3.3', en, te), -16 - 2 * k, off=4 * k, dur=2.5, fade=0.4, duck=-8)
        c1 = cue('3.3', 'The', '1600ల') - 0.1; c2 = cue('3.3', 'Local', 'దళారులు') - 0.1; c3 = cue('3.3', 'buyers', 'కొనుగోలుదారులను') - 0.1
        add('harbour_waves.wav', c1, -11, off=20, dur=c2 - c1 + 0.3, fade=0.4, duck=-10)
        add('pin_push.wav', cue('3.3', 'Dutch', 'డచ్'), -16); add('pin_push.wav', cue('3.3', 'English', 'ఇంగ్లీష్'), -16)
        add('amb_crowd.mp3', c2, -14, off=3, dur=c3 - c2 + 0.3, fade=0.3, duck=-10)
        cw = cue('3.3', 'buyers', 'కొనుగోలుదారులను') + 0.3
        for j in range(8): add('tick.wav', cw + j * 0.12 + 0.3, -24)
    import math as _m
    if '0.1' in M:
        add('marker.wav', cue('0.1', 'banning', 'చట్టం') - 0.05, -12, dur=1.2)
        add('stamp.wav', cue('0.1', 'printed', 'నిషేధం') + 0.45, -6, duck=-3)
    if '0.2' in M: add('sub_knock.wav', cue('0.2', 'challenging', 'గట్టి'), -12)
    if '0.3' in M:
        add('ship_creak.mp3', cue('0.3', 'sailed', 'ప్రపంచం') - 0.6, -16, off=6, dur=3.0, fade=0.4, duck=-8)
        for en, te in (('pepper', 'మిరియాల'), ('diamonds', 'గోల్కొండ'), ('cloth', 'గుడ్డ')): add('ui_pop.wav', cue('0.3', en, te), -16)
    if '0.4' in M: add('sparkle_soft.wav', cue('0.4', 'quarter', 'నాలుగో'), -20)
    if '0.5' in M: add('swoosh_slow.wav', cue('0.5', 'company', 'కంపెనీ') - 0.25, -16, dur=1.2)
    if '3.12' in M:
        for nm, tt, g in SUBEV: add(nm + '.wav', tt, 20 * _m.log10(g) - 4, duck=-2)
    if '4.6' in M:
        add('coins_clink.wav', cue('4.6', 'land', 'భూమి') + 0.3, -14); add('coins_clink.wav', cue('4.6', 'cut', 'వాటా'), -14)
        add('stamp.wav', cue('4.6', 'permission', 'ఫర్మానా'), -12)
    if '4.10' in M:
        add('page_turn.wav', cue('4.10', 'Peter', 'Peter') - 0.15, -14); add('marker.wav', cue('4.10', 'Peter', 'Peter') + 1.05, -14, dur=1.0)
    if '7.2' in M: add('sub_knock.wav', cue('7.2', '3', 'మూడు') if not film.TE else cue('7.2', 'three', 'మూడు'), -14)
    if '7.5' in M:
        add('stamp.wav', cue('7.5', '1765', '1765'), -10); add('coins_clink.wav', cue('7.5', '1765', '1765') + 1.0, -14)
    if '7.6' in M: add('coins_clink.wav', cue('7.6', 'taxes', 'పన్నులతో'), -14)
    return ev
