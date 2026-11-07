"""Sound events for the v3 sequences (spot effects synced to the animation) + ambience beds."""
import sys
sys.path.insert(0, '/home/claude/gs/film3')
LOOM_HITS = [7.36, 10.28, 19.95, 29.71]          # onsets in loom_shuttle.mp3 (s)
def events(film, seqs):
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
        cw = cue('3.3', 'with', 'నేత') - 0.1
        for j in range(8): add('tick.wav', cw + j * 0.12 + 0.3, -24)
    return ev
