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
import subprocess
AUDIO_SR = 8000


def audio_window(path, t0, dur):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{dur:.3f}', '-i', path, '-vn', '-ac', '1', '-ar', str(AUDIO_SR),
                        '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.frombuffer(b, np.float32).astype(float)
    return x if len(x) >= int(0.5 * AUDIO_SR) else None


def xcorr_lag(x, y, sr, max_lag):
    """lag (s) of y relative to x and the normalised correlation at that lag"""
    n = min(len(x), len(y)); x, y = x[:n] - x[:n].mean(), y[:n] - y[:n].mean()
    m = int(max_lag * sr); f = 1 << (2 * n - 1).bit_length()
    cc = np.fft.irfft(np.fft.rfft(y, f) * np.conj(np.fft.rfft(x, f)), f)
    cc = np.concatenate([cc[-m:], cc[:m + 1]]); k = int(np.argmax(cc)) - m
    a, b = (x[:n - k], y[k:]) if k >= 0 else (x[-k:], y[:n + k])
    c = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-12))
    return k / sr, c


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('dir'); ap.add_argument('--base', required=True)
    ap.add_argument('--langs', default='EN,TE'); ap.add_argument('--platforms', default='YT,IG')
    ap.add_argument('--format', default='short', choices=list(PROFILES)); ap.add_argument('--pattern', default='{base}_{lang}_{platform}.mp4')
    ap.add_argument('--fps', type=float, default=30.0); ap.add_argument('--out')
    ap.add_argument('--ending-seconds', type=float, default=10.0, help='tail excluded from the body comparison (platform-specific ending)')
    ap.add_argument('--points', type=int, default=8, help='frames compared across the body')
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
    # same body across the platform versions of one language: several frames across the body + audio sync.
    # The last --ending-seconds (series slide, platform button, loop) may differ by design and are excluded.
    plats = a.platforms.split(',')
    for lang in a.langs.split(','):
        vs = [found[(lang, p)] for p in plats if (lang, p) in found]
        if len(vs) < 2: continue
        W, H = vs[0][1]['width'], vs[0][1]['height']
        body_end = min(v[1]['duration'] for v in vs) - a.ending_seconds
        if body_end < 2:
            R.add(f'{lang}: same body on every platform', NP, f'body shorter than 2 s after excluding the last {a.ending_seconds} s', 'FMT-09'); continue
        pts = [body_end * (i + 0.5) / a.points for i in range(a.points)]
        diffs, bad = [], []
        for t in pts:
            fr = [frame(v[0], t, W, H) for v in vs]
            if any(f is None for f in fr): bad.append(f'{t:.1f}s unreadable'); continue
            d = max(float(np.abs(fr[0].astype(float) - f.astype(float)).mean()) for f in fr[1:])
            diffs.append(round(d, 2))
            if d >= 2.0: bad.append(f'{t:.1f}s differs ({d:.1f})')
        R.add(f'{lang}: video body identical at {len(pts)} points (ending excluded)', FAIL if bad else PASS,
              (f'mismatch: {bad}' if bad else f'max difference {max(diffs):.2f} (limit 2.0)') + f'; points {[round(t, 1) for t in pts]}', 'FMT-09')
        lag_report, lag_bad = [], []
        for v in vs[1:]:
            win = min(5.0, body_end / 3)          # windows always end inside the body, never in the ending
            for frac in (0.2, 0.5, 0.8):
                t0 = min(max(0.0, body_end * frac - win / 2), body_end - win)
                x, y = audio_window(vs[0][0], t0, win), audio_window(v[0], t0, win)
                if x is None or y is None or x.std() < 1e-6: lag_bad.append(f'{t0:.0f}s: no audio'); continue
                lag, c = xcorr_lag(x, y, AUDIO_SR, 0.5)
                lag_report.append(f'{t0:.0f}s lag {lag * 1000:+.0f} ms r={c:.2f}')
                if abs(lag) > 0.040 or c < 0.9: lag_bad.append(f'{t0:.0f}s lag {lag * 1000:+.0f} ms r={c:.2f}')
        R.add(f'{lang}: audio in sync across platforms (3 windows, ending excluded)', FAIL if lag_bad else PASS,
              ('; '.join(lag_bad) if lag_bad else '; '.join(lag_report)) + ' (limits: |lag| <= 40 ms, r >= 0.9)', 'FMT-09')
        durs = [round(v[1]['duration'], 2) for v in vs]
        R.add(f'{lang}: platform endings', PASS, f'durations {durs} s; the last {a.ending_seconds} s may differ by design (FMT-06)', 'FMT-06')
    R.coverage = dict(expected=len(a.langs.split(',')) * len(plats), found=len(found))
    return R.finish(a.out)


if __name__ == '__main__':
    sys.exit(main())
