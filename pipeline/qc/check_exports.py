"""Check that every platform version exists and is technically correct.

usage:
  python3 pipeline/qc/check_exports.py DIR --base GoldenSparrow4 [--langs EN,TE] [--platforms YT,IG]
         [--format short|long] [--pattern "{base}_{lang}_{platform}.mp4"] [--out DIR]

Shorts default to four files (EN/TE x YT/IG, FMT-09); films typically use --platforms YT.
Rules: FMT-01, FMT-09, PLT-01, QC-06.
"""
import argparse, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP, PROFILES, probe, frame


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dir'); ap.add_argument('--base', required=True)
    ap.add_argument('--langs', default='EN,TE'); ap.add_argument('--platforms', default='YT,IG')
    ap.add_argument('--format', default='short', choices=list(PROFILES)); ap.add_argument('--pattern', default='{base}_{lang}_{platform}.mp4')
    ap.add_argument('--fps', type=float, default=30.0); ap.add_argument('--out')
    a = ap.parse_args(argv)
    P = PROFILES[a.format]; R = Report('check_exports', os.path.join(a.dir, a.base))
    found = {}
    for lang in a.langs.split(','):
        for plat in a.platforms.split(','):
            name = a.pattern.format(base=a.base, lang=lang, platform=plat); p = os.path.join(a.dir, name)
            if not os.path.exists(p):
                R.add(f'{name} present', FAIL, 'missing platform version', 'FMT-09'); continue
            info = probe(p)
            if not info or not info['width']:
                R.add(f'{name} readable', FAIL, 'no video stream', 'QC-06'); continue
            found[(lang, plat)] = (p, info)
            probs = []
            if (info['width'], info['height']) != (P['W'], P['H']): probs.append(f"{info['width']}x{info['height']} (expected {P['W']}x{P['H']})")
            if info['vcodec'] != 'h264': probs.append(f"video codec {info['vcodec']} (expected h264)")
            if not info['acodec']: probs.append('no audio stream')
            elif info['acodec'] != 'aac': probs.append(f"audio codec {info['acodec']} (expected aac)")
            if P['max_duration'] and info['duration'] >= P['max_duration']: probs.append(f"{info['duration']:.2f} s is not under 3:00")
            if info['fps'] and abs(info['fps'] - a.fps) > 0.05: probs.append(f"{info['fps']:.2f} fps (expected {a.fps:g})")
            R.add(f'{name}', FAIL if probs else PASS, '; '.join(probs) if probs else
                  f"{info['width']}x{info['height']}, {info['vcodec']}/{info['acodec']}, {info['duration']:.2f} s, {info['fps']:.0f} fps", 'FMT-09')
    # same body across the platform versions of one language
    plats = a.platforms.split(',')
    for lang in a.langs.split(','):
        vs = [found[(lang, p)] for p in plats if (lang, p) in found]
        if len(vs) < 2: continue
        d0 = vs[0][1]['duration']
        diffs = [abs(v[1]['duration'] - d0) for v in vs[1:]]
        W, H = vs[0][1]['width'], vs[0][1]['height']
        mids = [frame(v[0], d0 * 0.4, W, H) for v in vs]
        body = [float(np.abs(mids[0].astype(float) - m.astype(float)).mean()) for m in mids[1:] if m is not None and mids[0] is not None]
        ok = all(x <= 0.5 for x in diffs) and all(b < 2.0 for b in body)
        R.add(f'{lang}: same body on every platform', PASS if ok else REVIEW,
              f'duration differences {[round(x, 2) for x in diffs]} s; mid-frame difference {[round(b, 2) for b in body]}', 'FMT-09')
    R.coverage = dict(expected=len(a.langs.split(',')) * len(plats), found=len(found))
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())
