"""Self-test for pipeline/qc: synthetic fixtures with known-good and deliberately failing cases.

usage: python3 pipeline/qc/tests/run_tests.py [--keep DIR]
Each case states the overall verdict and the check statuses it must produce. Fixtures are generated
with ffmpeg into a temporary folder, so nothing in the repository is touched.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); QC = os.path.dirname(HERE); REPO = os.path.dirname(os.path.dirname(QC))
sys.path.insert(0, QC)
import qc_video, qc_layout, check_exports, check_copy, check_assets, check_sources, check_rules

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
Platform limits verified 2026-11-10 (platform_rules.md).

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
        ('exports: all four correct', check_exports, [E3, '--base', 'Z'], 'PASS', {'same body': 'PASS'}),
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
        ('copy: compliant', check_copy, [f'{T}/copy_good.md'], 'INCOMPLETE', {'hashtags': 'PASS', 'disclosure': 'PASS', 'verification date': 'PASS', 'brand hashtag': 'PASS'}),
        ('copy: long title, 11 hashtags, no disclosure', check_copy, [f'{T}/copy_bad.md'], 'FAIL', {'title length': 'FAIL', 'hashtags': 'FAIL', 'disclosure': 'FAIL'}),
        ('sources: every claim registered', check_sources, [f'{T}/script.md', '--brief', f'{T}/brief_full.md'], 'INCOMPLETE', {'register entry': 'PASS'}),
        ('sources: claim C2 missing from register', check_sources, [f'{T}/script.md', '--brief', f'{T}/brief_gap.md'], 'FAIL', {'register entry': 'FAIL'}),
        ('sources: script without markers', check_sources, [f'{T}/script_nomarks.md', '--brief', f'{T}/brief_full.md'], 'INCOMPLETE', {'claim markers': 'NOT PERFORMED'}),
        ('rules: this branch', check_rules, [], 'PASS', {'one owner': 'PASS', 'retired wording': 'PASS'}),
        ('rules: duplicate rule ID', check_rules, ['--root', R2], 'FAIL', {'one owner': 'FAIL'}),
        ('rules: retired wording reintroduced', check_rules, ['--root', R3], 'FAIL', {'retired wording': 'FAIL'}),
    ]
    if gs1: cases.append(('copy: GS 1/6 original (shipped 30 hashtags; known defect)', check_copy, [f'{T}/copy_gs1_original.md'], 'FAIL', {'IG hashtags': 'FAIL'}))
    rows, fails = [], 0
    for i, (name, tool, argv, ov, st) in enumerate(cases):
        res = run(tool, argv, O(f'{i:02d}'))
        ok, got_ov, got = expect(res, ov, st)
        fails += not ok
        rows.append(f"| {'ok' if ok else 'MISMATCH'} | {name} | expected {ov or 'any'} | got {got_ov} | " + '; '.join(f'{k}: {v}' for k, v in got.items())[:300].replace('|', '/') + ' |')
    rep = ['# pipeline/qc self-test', '', f'{len(cases) - fails} of {len(cases)} cases behaved as expected.', '',
           '| Result | Case | Expected | Got | Check statuses |', '|---|---|---|---|---|'] + rows
    open(os.path.join(T, 'TEST_REPORT.md'), 'w').write('\n'.join(rep) + '\n'); print('\n'.join(rep))
    if a.report: open(a.report, 'w').write('\n'.join(rep) + '\n')
    if a.keep: print('fixtures in', T)
    else: shutil.rmtree(T, ignore_errors=True)
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main())
