"""Self-test for pipeline/qc: synthetic fixtures with known-good and deliberately failing cases.

usage: python3 pipeline/qc/tests/run_tests.py [--keep DIR]
Each case states the overall verdict and the check statuses it must produce. Fixtures are generated
with ffmpeg into a temporary folder, so nothing in the repository is touched.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); QC = os.path.dirname(HERE); REPO = os.path.dirname(os.path.dirname(QC))
sys.path.insert(0, QC)
import qc_video, qc_layout, check_exports, check_copy, check_assets, check_sources, check_rules, qc_summary

def ff(*args): subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)

def make_video(path, w, h, dur, kind='moving', audio='ok'):
    v = {'moving': f'testsrc2=s={w}x{h}:r=30:d={dur}', 'still': f'color=c=0x8a7f6a:s={w}x{h}:r=30:d={dur}'}[kind]
    # deterministic audio: a 997 Hz sine at +7 dB measures -14.1 LUFS / -11.1 dBTP (calibrated with ebur128)
    a = {'ok': f'sine=f=997:d={dur},volume=7dB', 'loud': f'sine=f=440:d={dur},volume=24dB',
         'gap': f'sine=f=997:d={dur},volume=7dB'}[audio]
    af = {'ok': 'anull', 'loud': 'anull', 'gap': f'volume=enable=\'between(t,1.5,{dur - 1})\':volume=0'}[audio]
    ff('-f', 'lavfi', '-i', v, '-f', 'lavfi', '-i', a, '-af', af, '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-ar', '48000', '-shortest', path)

def run(tool, argv, out):
    try: tool.main(argv + ['--out', out])
    except SystemExit: pass
    name = tool.__name__
    return json.load(open(os.path.join(out, f'{name}.json')))

def expect(res, overall, statuses):
    ok = overall is None or res['overall'] == overall
    got = {c['check']: c['status'] for c in res['checks']}
    for frag, st in statuses.items():
        m = [v for k, v in got.items() if frag in k]
        ok = ok and bool(m) and all(x == st for x in m)
    return ok, res['overall'], got

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--keep'); ap.add_argument('--report'); a = ap.parse_args()
    T = a.keep or tempfile.mkdtemp(prefix='qc_tests_'); os.makedirs(T, exist_ok=True)
    V = os.path.join(T, 'v'); os.makedirs(V, exist_ok=True)
    make_video(f'{V}/good_short.mp4', 1080, 1920, 4)
    make_video(f'{V}/good_long.mp4', 1920, 1080, 4)
    make_video(f'{V}/square.mp4', 1080, 1080, 3)
    make_video(f'{V}/loud.mp4', 1080, 1920, 3, audio='loud')
    make_video(f'{V}/dropout.mp4', 1080, 1920, 6, audio='gap')
    make_video(f'{V}/still.mp4', 1080, 1920, 4, kind='still')
    ff('-f', 'lavfi', '-i', 'color=c=black:s=1080x1920:r=30:d=1', '-i', f'{V}/good_short.mp4', '-filter_complex',
       '[0:v][1:v]concat=n=2:v=1[v]', '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-preset', 'ultrafast', '-c:a', 'aac', f'{V}/black_start.mp4')
    ff('-f', 'lavfi', '-i', 'color=c=0x445566:s=1080x1920:r=30:d=181', '-f', 'lavfi', '-i', 'sine=f=997:d=181,volume=7dB',
       '-c:v', 'libx264', '-preset', 'ultrafast', '-tune', 'stillimage', '-c:a', 'aac', '-shortest', f'{V}/too_long.mp4')
    json.dump([[0, 4, 'evidence hold']], open(f'{T}/holds.json', 'w'))
    E = os.path.join(T, 'exports'); os.makedirs(E, exist_ok=True)
    for n in ('X_EN_YT', 'X_EN_IG', 'X_TE_YT'): shutil.copy(f'{V}/good_short.mp4', f'{E}/{n}.mp4')
    E2 = os.path.join(T, 'exports2'); os.makedirs(E2, exist_ok=True)
    for n in ('Y_EN_YT', 'Y_EN_IG', 'Y_TE_YT'): shutil.copy(f'{V}/good_short.mp4', f'{E2}/{n}.mp4')
    shutil.copy(f'{V}/square.mp4', f'{E2}/Y_TE_IG.mp4')
    E3 = os.path.join(T, 'exports3'); os.makedirs(E3, exist_ok=True)
    for n in ('Z_EN_YT', 'Z_EN_IG', 'Z_TE_YT', 'Z_TE_IG'): shutil.copy(f'{V}/good_short.mp4', f'{E3}/{n}.mp4')

    # layout dumps (box = container, ink = text bounds)
    bl = dict(kind='badge', box=[64, 148, 300, 208], ink=[90, 165, 280, 192], owner='GOLD · 2/6', group='corner')
    br = dict(kind='badge', box=[820, 148, 1016, 208], ink=[846, 165, 990, 192], owner='1/3 MONEY', group='corner')
    cap = dict(kind='caption', box=[200, 1416, 880, 1476], ink=[212, 1426, 868, 1466], owner='the farmer paid')
    card = dict(kind='card', box=[140, 700, 940, 900], ink=[170, 730, 910, 870], owner='LAND REVENUE')
    img = dict(kind='image', box=[0, 300, 1080, 1360], owner='panel')
    good = {'1.00': [bl, br, cap, card, img]}
    D = lambda name, frames, **k: json.dump(dict(W=1080, H=1920, frames=frames, **k), open(f'{T}/{name}.json', 'w'))
    D('lay_good', good)
    D('lay_overlap', {'2.00': [bl, br, cap, dict(kind='label', box=[300, 1430, 600, 1470], ink=[310, 1440, 590, 1462], owner='GOLCONDA')]})
    D('lay_clipped', {'3.00': [bl, br, dict(cap, ink=[190, 1426, 900, 1466])]})
    D('lay_badges', {'4.00': [bl, dict(br, box=[820, 160, 1016, 220], ink=[846, 177, 990, 204]), cap]})
    D('lay_cap_on_image', {'5.00': [bl, br, dict(cap, box=[200, 1300, 880, 1360], ink=[212, 1310, 868, 1350]), img]})
    D('lay_edge', {'6.00': [bl, br, cap, dict(card, box=[10, 700, 940, 900], ink=[40, 730, 910, 870])]})
    D('lay_partial', dict(good, **{'7.00': [img]}), not_covered=[dict(t0=8, t1=12, what='Remotion Globe Arcs (labels baked in)')])
    D('lay_16x9', {'1.00': [dict(kind='caption', box=[500, 950, 1420, 1010], ink=[512, 960, 1408, 1000], owner='caption 16:9')]})
    json.dump(dict(W=1920, H=1080, frames={'1.00': [dict(kind='caption', box=[500, 950, 1420, 1010], ink=[512, 960, 1408, 1000], owner='c')]}), open(f'{T}/lay_16x9.json', 'w'))

    hdr = '| ID | Asset | Source / URL | Licence and credit line | Native size (px) | Largest on-screen size (px) | Scale ≤ 1.0? | Label | Used in scenes |\n|---|---|---|---|---|---|---|---|---|\n'
    open(f'{T}/assets_good.md', 'w').write('# Asset register\n\n' + hdr +
        '| A1 | farman.jpg | National Museum, New Delhi | Public domain; credit "National Museum" | 2400×3200 | 1080×1440 | yes |  | farman |\n'
        '| A2 | G18 revenue office (Gemini) | user generated, Gemini | own AI illustration | 1920×1080 | 1080×608 | yes | DRAMATIZED | Madanna |\n')
    open(f'{T}/assets_bad.md', 'w').write('# Asset register\n\n' + hdr +
        '| A1 | farman.jpg | National Museum |  | 2400×3200 | 1080×1440 | yes |  | farman |\n'
        '| A2 | G16 bowl (Gemini) | Gemini | own AI illustration | 1920×1080 | 1920×3456 | no |  | hook |\n')

    good_copy = """# post copy
Altered or synthetic content: No (stylised animation only), checked against YouTube policy 2026-11-10.
Platform limits re-checked 2026-11-10 against the official pages (platform_rules.md).

## ENGLISH · YouTube Short

**Title**
Why did India's weavers stay poor? #shorts

**Description**
Hook. SOURCES - A. Maddison 2001. CREDITS - National Museum. #WhyEveryQuestionHasAStory #history

**Tags**
india history, mughal, golden sparrow

## ENGLISH · Instagram Reel

**Caption**
Short recap. Question? Comment your why. #WhyEveryQuestionHasAStory #history #india #mughal
"""
    open(f'{T}/copy_good.md', 'w').write(good_copy)
    open(f'{T}/copy_bad.md', 'w').write(good_copy.replace('Altered or synthetic content: No (stylised animation only), checked against YouTube policy 2026-11-10.\n', '')
        .replace('Why did', 'W' * 120).replace('#mughal', ' '.join(f'#tag{i}' for i in range(8))))
    gs1 = subprocess.run(['git', '-C', REPO, 'show', '0b65210:videos/2026-11-09_short_gs1_golden_sparrow/GS1_Short_Post_Copy.md'], capture_output=True, text=True).stdout
    if gs1: open(f'{T}/copy_gs1_original.md', 'w').write(gs1)

    open(f'{T}/script.md', 'w').write('1. India made a quarter of world output [C1]. Revenue was a third to a half [C2].\n')
    open(f'{T}/script_nomarks.md', 'w').write('1. India made a quarter of world output.\n')
    rh = '| ID | Claim | Source (outlet, title, URL) | Date checked | Wording note |\n|---|---|---|---|---|\n'
    open(f'{T}/brief_full.md', 'w').write('## Source register\n' + rh + '| C1 | quarter | Maddison 2001 T B-20 | 2026-11-10 | estimate |\n| C2 | third to half | Habib 1999 | 2026-11-10 | varied |\n')
    open(f'{T}/brief_gap.md', 'w').write('## Source register\n' + rh + '| C1 | quarter | Maddison 2001 T B-20 | 2026-11-10 | estimate |\n')

    R2 = os.path.join(T, 'repo_dup'); R3 = os.path.join(T, 'repo_retired')
    for r in (R2, R3):  # a minimal copy of the Markdown rule system (no videos, assets or git history)
        for f in ('playbook', 'CLAUDE.md', 'README.md', 'plans'):
            src = os.path.join(REPO, f); dst = os.path.join(r, f)
            if os.path.isdir(src): shutil.copytree(src, dst, ignore=shutil.ignore_patterns('*.mp4', '*.wav', '*.mp3', '*.png', '*.jpg'))
            else: os.makedirs(r, exist_ok=True); shutil.copy(src, dst)
    with open(os.path.join(R2, 'playbook/roles/music.md'), 'a') as f: f.write('\n- **[BR-01]** (P, test) duplicate definition\n')
    with open(os.path.join(R3, 'playbook/roles/editor.md'), 'a') as f: f.write('\n- Shorts are 45–60 s long.\n')

    # ---- loop fixtures: smooth crossfade back to frame 0 / no return / hard cut in the last 0.25 s
    ff('-f', 'lavfi', '-i', 'testsrc2=s=1080x1920:r=30:d=4', '-frames:v', '1', f'{V}/f0.png')
    blue = 'color=c=0x1d3b6e:s=1080x1920:r=30:d={d}'
    still = lambda d: ['-loop', '1', '-framerate', '30', '-t', str(d), '-i', f'{V}/f0.png']
    tone = ['-f', 'lavfi', '-i', 'sine=f=997:d=6,volume=7dB']
    enc_v = lambda out, ins, fc, ai: ff(*ins, *tone, '-filter_complex', fc, '-map', '[v]', '-map', f'{ai}:a', '-c:v', 'libx264', '-preset', 'ultrafast',
                                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', out)
    # good: frame 0 -> fade to blue -> fade back to exactly frame 0
    enc_v(f'{V}/loop_good.mp4', still(1.4) + ['-f', 'lavfi', '-i', blue.format(d=2.4)] + still(1.2),
          '[0:v]format=yuv420p,fps=30,settb=1/30[a];[1:v]format=yuv420p,settb=1/30[b];[2:v]format=yuv420p,fps=30,settb=1/30[c];'
          '[a][b]xfade=transition=fade:duration=0.8:offset=0.6[ab];[ab][c]xfade=transition=fade:duration=0.8:offset=2.2[v]', 3)
    # bad: frame 0 -> blue, never returns
    enc_v(f'{V}/loop_bad.mp4', still(1) + ['-f', 'lavfi', '-i', blue.format(d=3)],
          '[0:v]format=yuv420p,fps=30[a];[1:v]format=yuv420p[b];[a][b]concat=n=2:v=1[v]', 2)
    # abrupt: frame 0 -> blue -> hard cut back to frame 0 for the last 0.25 s
    enc_v(f'{V}/loop_abrupt.mp4', still(1) + ['-f', 'lavfi', '-i', blue.format(d=2.75)] + still(0.25),
          '[0:v]format=yuv420p,fps=30[a];[1:v]format=yuv420p[b];[2:v]format=yuv420p,fps=30[c];[a][b][c]concat=n=3:v=1[v]', 3)
    # ---- export-body fixtures: same body + different endings / body changed mid-way / audio 200 ms late
    def enc(out, vf_inputs, fc, amap='[a]'):
        ff(*vf_inputs, '-filter_complex', fc, '-map', '[v]', '-map', amap, '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '48000', out)
    body = ['-f', 'lavfi', '-i', 'testsrc2=s=1080x1920:r=30:d=8', '-f', 'lavfi', '-i', 'anoisesrc=c=pink:seed=42:a=0.1:d=8']
    endA = ['-f', 'lavfi', '-i', 'color=c=0x8a2020:s=1080x1920:r=30:d=2', '-f', 'lavfi', '-i', 'sine=f=440:d=2']
    endB = ['-f', 'lavfi', '-i', 'color=c=0x20408a:s=1080x1920:r=30:d=2', '-f', 'lavfi', '-i', 'sine=f=660:d=2']
    cat = '[0:v][1:a][2:v][3:a]concat=n=2:v=1:a=1[v][a]'
    B = os.path.join(T, 'exports_body'); os.makedirs(B, exist_ok=True)
    enc(f'{B}/W_EN_YT.mp4', body + endA, cat); enc(f'{B}/W_EN_IG.mp4', body + endB, cat)
    enc(f'{B}/V_EN_YT.mp4', body + endA, cat)
    enc(f'{B}/V_EN_IG.mp4', body + endB + ['-f', 'lavfi', '-i', 'color=c=0x445566:s=1080x1920:r=30:d=2'],   # input 4 replaces 3-5 s
        '[0:v]split[x][y];[x]trim=0:3,setpts=PTS-STARTPTS[p1];[y]trim=5:8,setpts=PTS-STARTPTS[p2];[p1][4:v][p2]concat=n=3:v=1[bv];[bv][1:a][2:v][3:a]concat=n=2:v=1:a=1[v][a]')
    enc(f'{B}/U_EN_YT.mp4', body + endA, cat)
    enc(f'{B}/U_EN_IG.mp4', body + endB, '[1:a]adelay=200|200,atrim=0:8,asetpts=PTS-STARTPTS[d];[0:v][d][2:v][3:a]concat=n=2:v=1:a=1[v][a]')
    # ---- sound catalog fixtures
    SX = os.path.join(T, 'sfx'); os.makedirs(f'{SX}/amb', exist_ok=True)
    for n in ('knock.wav', 'amb/village.mp3', 'amb/extra.mp3', 'amb/village2.mp3', 'amb_fire.mp3'):
        ff('-f', 'lavfi', '-i', 'sine=f=300:d=0.5', f'{SX}/{n}')
    json.dump({'knock': {'file': 'lib/knock.wav'}, 'amb_village': {'file': 'amb/village.mp3'}, 'gone': {'file': 'amb/gone.mp3'},
               'amb_fire': {'file': 'amb_fire.mp3', 'licence_status': 'UNKNOWN', 'approved_for_new_work': False},
               'amb_owner': {'file': 'amb/extra.mp3', 'licence_status': 'APPROVED BY OWNER, SOURCE NOT RECORDED', 'approved_for_new_work': True,
                             'owner_approval': {'date': '2026-11-10'}, 'third_party_rights': 'UNVERIFIED: source never recorded'}}, open(f'{SX}/catalog.json', 'w'))
    def sreg(name, assets):
        open(f'{T}/{name}.md', 'w').write('# Asset register\n\n' + hdr + ''.join(
            f'| S{i} | {x} | test source | test licence |  |  |  |  | scene |\n' for i, x in enumerate(assets)))
    sreg('snd_good', ['knock', 'amb/village.mp3', 'lib/knock.wav', 'sfx/amb/village.mp3'])
    sreg('real_restricted', ['sfx_cannon_distant', 'amb_fire', 'amb_crowd', 'amb_drums'])
    sreg('real_approved', ['amb_village', 'amb/court.mp3', 'harbour_waves.wav', 'sfx_quill', 'impact_big', 'riser.wav']); sreg('real_stale', ['lib/riser.wav'])
    sreg('snd_missing_entry', ['amb/nope.mp3']); sreg('snd_missing_file', ['gone']); sreg('snd_uncat', ['amb/village2.mp3']); sreg('snd_owner', ['amb_owner']); sreg('snd_unknown', ['amb_fire'])
    # ---- limits come from platform_rules.md: a copy with a 3-hashtag limit must fail a 4-hashtag caption
    pr = open(os.path.join(REPO, 'playbook/platform_rules.md')).read().replace('"ig_hashtags_max":      {"value": 5,', '"ig_hashtags_max":      {"value": 3,')
    open(f'{T}/platform_rules_3tags.md', 'w').write(pr)
    # ---- human sign-off fixtures
    tpl = open(os.path.join(REPO, 'playbook/templates/qc_signoff.md')).read()
    signed = tpl.replace('| NOT DONE | | | |', '| PASS | Sandeep | 2026-11-12 | checked |')
    open(f'{T}/signoff_full.md', 'w').write(signed)
    open(f'{T}/signoff_partial.md', 'w').write(tpl.replace('| H11 | Licences and credits correct | RS-07, ART-02 | NOT DONE | | | |', '| H11 | Licences and credits correct | RS-07, ART-02 | PASS | Sandeep | 2026-11-12 | ok |'))
    open(f'{T}/signoff_fail.md', 'w').write(signed.replace('| H4 | Story and composition | ST-01, DIR-02 | PASS | Sandeep | 2026-11-12 | checked |', '| H4 | Story and composition | ST-01, DIR-02 | FAIL | Sandeep | 2026-11-12 | payoff unclear |'))
    open(f'{T}/signoff_noreviewer.md', 'w').write(signed.replace('| PASS | Sandeep | 2026-11-12 | checked |', '| PASS | | | looked fine |', 1))

    O = lambda n: os.path.join(T, 'out', n)
    cases = [
        ('video: good 9:16', qc_video, [f'{V}/good_short.mp4', '--no-sheets'], 'INCOMPLETE', {'dimensions': 'PASS', 'integrated loudness': 'PASS', 'true peak': 'PASS', 'black': 'PASS', 'visual QC': 'NOT PERFORMED'}),
        ('video: good 16:9 film', qc_video, [f'{V}/good_long.mp4', '--no-sheets'], 'INCOMPLETE', {'dimensions': 'PASS', 'duration': 'PASS'}),
        ('video: wrong dimensions (1080x1080)', qc_video, [f'{V}/square.mp4', '--no-sheets'], 'FAIL', {'format': 'FAIL'}),
        ('video: clipping, too loud', qc_video, [f'{V}/loud.mp4', '--no-sheets'], 'FAIL', {'true peak': 'FAIL', 'integrated loudness': 'FAIL'}),
        ('video: audio dropout (only the dropout verdict is asserted; a clip that is 70% silence has meaningless loudness)', qc_video, [f'{V}/dropout.mp4', '--no-sheets'], None, {'dropouts': 'REVIEW'}),
        ('video: black first second', qc_video, [f'{V}/black_start.mp4', '--no-sheets'], 'FAIL', {'black frames': 'FAIL', 'frame 1 brightness': 'FAIL'}),
        ('video: unmarked still (freeze)', qc_video, [f'{V}/still.mp4', '--no-sheets'], 'INCOMPLETE', {'freezes': 'REVIEW'}),
        ('video: same still marked HOLD', qc_video, [f'{V}/still.mp4', '--no-sheets', '--holds', f'{T}/holds.json'], 'INCOMPLETE', {'freezes': 'PASS'}),
        ('video: Short over 3:00', qc_video, [f'{V}/too_long.mp4', '--no-sheets'], 'FAIL', {'duration under 3:00': 'FAIL'}),
        ('exports: missing platform version', check_exports, [E, '--base', 'X'], 'FAIL', {'X_TE_IG.mp4 present': 'FAIL', 'X_EN_YT.mp4': 'PASS'}),
        ('exports: wrong dimensions in one version', check_exports, [E2, '--base', 'Y'], 'FAIL', {'Y_TE_IG.mp4': 'FAIL'}),
        ('exports: all four correct', check_exports, [E3, '--base', 'Z', '--ending-seconds', '1'], 'PASS', {'video body identical': 'PASS', 'audio in sync': 'PASS'}),
        ('layout: clean frame', qc_layout, ['--dump', f'{T}/lay_good.json'], 'INCOMPLETE', {'containment': 'PASS', 'font and colour': 'NOT PERFORMED'}),
        ('layout: caption overlaps a label', qc_layout, ['--dump', f'{T}/lay_overlap.json'], 'FAIL', {'containment': 'FAIL'}),
        ('layout: clipped caption text', qc_layout, ['--dump', f'{T}/lay_clipped.json'], 'FAIL', {'containment': 'FAIL'}),
        ('layout: misaligned corner badges', qc_layout, ['--dump', f'{T}/lay_badges.json'], 'FAIL', {'containment': 'FAIL'}),
        ('layout: caption on a picture', qc_layout, ['--dump', f'{T}/lay_cap_on_image.json'], 'FAIL', {'containment': 'FAIL'}),
        ('layout: card too close to the edge', qc_layout, ['--dump', f'{T}/lay_edge.json'], 'FAIL', {'containment': 'FAIL'}),
        ('layout: partial coverage never passes', qc_layout, ['--dump', f'{T}/lay_partial.json'], 'INCOMPLETE', {'unregistered': 'NOT PERFORMED', 'no registered text': 'REVIEW'}),
        ('layout: 16:9 frame size', qc_layout, ['--dump', f'{T}/lay_16x9.json'], 'INCOMPLETE', {'containment': 'PASS'}),
        ('assets: complete register', check_assets, [f'{T}/assets_good.md'], 'INCOMPLETE', {'source and licence': 'PASS', 'image scale': 'PASS', 'labelled': 'PASS'}),
        ('assets: missing licence, 1.8x enlargement, no AI label', check_assets, [f'{T}/assets_bad.md'], 'FAIL', {'source and licence': 'FAIL', 'image scale': 'FAIL', 'labelled': 'REVIEW'}),
        ('assets: no register', check_assets, [f'{T}/none.md'], 'INCOMPLETE', {'asset register': 'NOT PERFORMED'}),
        ('copy: compliant', check_copy, [f'{T}/copy_good.md', '--today', '2026-11-12'], 'INCOMPLETE', {'hashtags': 'PASS', 'disclosure': 'PASS', 're-checked for this upload': 'PASS', 'brand hashtag': 'PASS', 'central limits are current': 'PASS'}),
        ('copy: re-check 40 days old, central limits stale', check_copy, [f'{T}/copy_good.md', '--today', '2026-12-20'], 'INCOMPLETE', {'re-checked for this upload': 'REVIEW', 'central limits are current': 'REVIEW'}),
        ('copy: limits read from platform_rules (3-tag limit fails 4 tags)', check_copy, [f'{T}/copy_good.md', '--today', '2026-11-12', '--rules', f'{T}/platform_rules_3tags.md'], 'FAIL', {'IG hashtags': 'FAIL'}),
        ('copy: long title, 11 hashtags, no disclosure', check_copy, [f'{T}/copy_bad.md'], 'FAIL', {'title length': 'FAIL', 'IG hashtags': 'FAIL', 'disclosure': 'FAIL'}),
        ('loop: crossfade back to frame 0', qc_video, [f'{V}/loop_good.mp4', '--no-sheets', '--loop'], None, {'loop seam': 'PASS', 'loop transition': 'PASS'}),
        ('loop: never returns to frame 0', qc_video, [f'{V}/loop_bad.mp4', '--no-sheets', '--loop'], 'FAIL', {'loop seam': 'FAIL'}),
        ('loop: hard cut in the last 0.25 s', qc_video, [f'{V}/loop_abrupt.mp4', '--no-sheets', '--loop'], 'FAIL', {'loop seam': 'PASS', 'loop transition': 'FAIL'}),
        ('exports: same body, different endings', check_exports, [B, '--base', 'W', '--langs', 'EN', '--ending-seconds', '2.5'], 'PASS', {'video body identical': 'PASS', 'audio in sync': 'PASS'}),
        ('exports: body differs mid-way (3-5 s)', check_exports, [B, '--base', 'V', '--langs', 'EN', '--ending-seconds', '2.5'], 'FAIL', {'video body identical': 'FAIL'}),
        ('exports: IG audio 200 ms late', check_exports, [B, '--base', 'U', '--langs', 'EN', '--ending-seconds', '2.5'], 'FAIL', {'audio in sync': 'FAIL', 'video body identical': 'PASS'}),
        ('sounds: key, nested path, flat path, sfx/ prefix', check_assets, [f'{T}/snd_good.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX], 'INCOMPLETE', {'sounds:': 'PASS'}),
        ('sounds: not catalogued and no file', check_assets, [f'{T}/snd_missing_entry.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX], 'FAIL', {'sounds:': 'FAIL'}),
        ('sounds: catalogued but file missing', check_assets, [f'{T}/snd_missing_file.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX], 'FAIL', {'sounds:': 'FAIL'}),
        ('sounds: file present but uncatalogued', check_assets, [f'{T}/snd_uncat.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX], 'INCOMPLETE', {'sounds:': 'REVIEW'}),
        ('sounds: provenance UNKNOWN, not cleared', check_assets, [f'{T}/snd_unknown.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX], 'FAIL', {'sounds:': 'FAIL'}),
        ('sounds: owner-approved, source not recorded -> usable but flagged for review', check_assets, [f'{T}/snd_owner.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX], 'INCOMPLETE', {'sounds:': 'REVIEW'}),
        ('sounds (real catalog): the 4 owner-approved sounds resolve, flagged for review (provenance unverified)', check_assets, [f'{T}/real_restricted.md'], 'INCOMPLETE', {'sounds:': 'REVIEW'}),
        ('sounds (real catalog): approved and corrected-path sounds resolve', check_assets, [f'{T}/real_approved.md'], 'INCOMPLETE', {'sounds:': 'PASS'}),
        ('sounds (real catalog): the retired lib/ path form is rejected', check_assets, [f'{T}/real_stale.md'], 'FAIL', {'sounds:': 'FAIL'}),
        ('catalog integrity (real catalog): every entry has its file, no stale paths', check_assets, [f'{T}/none.md', '--catalog-integrity'], 'INCOMPLETE', {'catalog integrity': 'PASS'}),
        ('sounds: catalog integrity finds the missing file', check_assets, [f'{T}/snd_good.md', '--catalog', f'{SX}/catalog.json', '--sfx-root', SX, '--catalog-integrity'], 'FAIL', {'catalog integrity': 'FAIL'}),
        ('sources: every claim registered', check_sources, [f'{T}/script.md', '--brief', f'{T}/brief_full.md'], 'INCOMPLETE', {'register entry': 'PASS'}),
        ('sources: claim C2 missing from register', check_sources, [f'{T}/script.md', '--brief', f'{T}/brief_gap.md'], 'FAIL', {'register entry': 'FAIL'}),
        ('sources: script without markers', check_sources, [f'{T}/script_nomarks.md', '--brief', f'{T}/brief_full.md'], 'INCOMPLETE', {'claim markers': 'NOT PERFORMED'}),
        ('rules: this branch', check_rules, [], 'PASS', {'one owner': 'PASS', 'retired wording': 'PASS'}),
        ('rules: duplicate rule ID', check_rules, ['--root', R2], 'FAIL', {'one owner': 'FAIL'}),
        ('rules: retired wording reintroduced', check_rules, ['--root', R3], 'FAIL', {'retired wording': 'FAIL'}),
    ]
    SUMS = []   # (name, qc dir, type, sign-off, expected); built below from synthetic reports
    if gs1: cases.append(('copy: GS 1/6 original (shipped 30 hashtags; known defect)', check_copy, [f'{T}/copy_gs1_original.md'], 'FAIL', {'IG hashtags': 'FAIL'}))
    rows, fails = [], 0
    for i, (name, tool, argv, ov, st) in enumerate(cases):
        res = run(tool, argv, O(f'{i:02d}'))
        ok, got_ov, got = expect(res, ov, st)
        fails += not ok
        rows.append(f"| {'ok' if ok else 'MISMATCH'} | {name} | expected {ov or 'any'} | got {got_ov} | " + '; '.join(f'{k}: {v}' for k, v in got.items())[:300].replace('|', '/') + ' |')
    def fake_set(d, typ, drop=None):
        """a complete set of automated reports for a production type (all PASS), optionally without one"""
        vids = ['EN_YT', 'EN_IG', 'TE_YT', 'TE_IG'] if typ == 'short' else ['EN', 'TE']
        items = [('qc_video', f'X_{v}.mp4') for v in vids] + [('qc_layout', 'layout_en.json'), ('qc_layout', 'layout_te.json'),
                 ('check_exports', 'X'), ('check_copy', 'X_Post_Copy.md'), ('check_assets', 'asset_register.md'), ('check_sources', 'script.md')]
        os.makedirs(d, exist_ok=True)
        for i, (tool, target) in enumerate(items):
            if drop and target == drop: continue
            sub = os.path.join(d, f'{i:02d}'); os.makedirs(sub, exist_ok=True)
            json.dump(dict(tool=tool, target=target, overall='PASS', checks=[dict(check='synthetic', status='PASS', detail='', rule=None)]),
                      open(os.path.join(sub, f'{tool}.json'), 'w'))
        return d
    QS = fake_set(os.path.join(T, 'qs_short'), 'short'); QL = fake_set(os.path.join(T, 'qs_long'), 'long')
    QM = fake_set(os.path.join(T, 'qs_missing'), 'short', drop='X_EN_IG.mp4'); QE = os.path.join(T, 'qs_empty'); os.makedirs(QE, exist_ok=True)
    open(f'{T}/signoff_noH7.md', 'w').write('\n'.join(l for l in signed.splitlines() if not l.startswith('| H7 ')) + '\n')
    open(f'{T}/signoff_na_ok.md', 'w').write(signed.replace('| H6 | Telugu naturalness (voice, captions, on-screen text) | BR-06 | PASS | Sandeep | 2026-11-12 | checked |',
        '| H6 | Telugu naturalness (voice, captions, on-screen text) | BR-06 | N/A | Sandeep | 2026-11-12 | English-only test video |'))
    open(f'{T}/signoff_na_noreason.md', 'w').write(signed.replace('| H6 | Telugu naturalness (voice, captions, on-screen text) | BR-06 | PASS | Sandeep | 2026-11-12 | checked |',
        '| H6 | Telugu naturalness (voice, captions, on-screen text) | BR-06 | N/A | Sandeep | 2026-11-12 | |'))
    json.dump(dict(required=dict(qc_video=['EN_YT']), justification=''), open(f'{T}/manifest_nojust.json', 'w'))
    SUMS = [('summary: empty automated QC dir + fully signed form', QE, 'short', f'{T}/signoff_full.md', 'INCOMPLETE'),
            ('summary: one required automated report missing (EN_IG)', QM, 'short', f'{T}/signoff_full.md', 'INCOMPLETE'),
            ('summary: one required human row absent (H7)', QS, 'short', f'{T}/signoff_noH7.md', 'INCOMPLETE'),
            ('summary: complete reports + every row signed (Short)', QS, 'short', f'{T}/signoff_full.md', 'PASS'),
            ('summary: complete reports + every row signed (16:9 film)', QL, 'long', f'{T}/signoff_full.md', 'PASS'),
            ('summary: N/A with reviewer, date and reason', QS, 'short', f'{T}/signoff_na_ok.md', 'PASS'),
            ('summary: N/A without a reason does not count', QS, 'short', f'{T}/signoff_na_noreason.md', 'INCOMPLETE'),
            ('summary: no production type given', QS, None, f'{T}/signoff_full.md', 'INCOMPLETE'),
            ('summary: custom manifest without justification', QS, 'manifest', f'{T}/signoff_full.md', 'INCOMPLETE'),
            ('summary: no human sign-off', QS, 'short', None, 'INCOMPLETE'),
            ('summary: partial sign-off', QS, 'short', f'{T}/signoff_partial.md', 'INCOMPLETE'),
            ('summary: a human FAIL', QS, 'short', f'{T}/signoff_fail.md', 'FAIL'),
            ('summary: PASS without reviewer/date does not count', QS, 'short', f'{T}/signoff_noreviewer.md', 'INCOMPLETE')]
    for name, qd, typ, so, exp in SUMS:
        outp = os.path.join(T, f'summary_{len(rows)}.md')
        args = [qd, '--out', outp] + (['--signoff', so] if so else [])
        if typ == 'manifest': args += ['--manifest', f'{T}/manifest_nojust.json']
        elif typ: args += ['--type', typ]
        qc_summary.main(args)
        got = re.search(r'\*\*Overall: (\w+)', open(outp).read()).group(1)
        ok = got == exp; fails += not ok
        rows.append(f"| {'ok' if ok else 'MISMATCH'} | {name} | expected {exp} | got {got} | (qc_summary) |")
    rep = ['# pipeline/qc self-test', '', f'{len(cases) + len(SUMS) - fails} of {len(cases) + len(SUMS)} cases behaved as expected.', '',
           '| Result | Case | Expected | Got | Check statuses |', '|---|---|---|---|---|'] + rows
    open(os.path.join(T, 'TEST_REPORT.md'), 'w').write('\n'.join(rep) + '\n'); print('\n'.join(rep))
    if a.report: open(a.report, 'w').write('\n'.join(rep) + '\n')
    if a.keep: print('fixtures in', T)
    else: shutil.rmtree(T, ignore_errors=True)
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
