"""Technical QC for one delivered video (any project; 9:16 Shorts and 16:9 films).

usage:
  python3 pipeline/qc/qc_video.py VIDEO.mp4 [--format auto|short|long] [--out DIR]
         [--holds holds.json] [--scenes scenes.json] [--loop] [--no-sheets]
         [--lufs -14] [--lufs-tol 1.0] [--tp-max -1.0]

holds.json   intentional stills from the scene sheet (DIR-02 HOLD marks): [[t0, t1, "purpose"], ...]
scenes.json  scene starts for per-scene sharpness: [["name", t0], ...]; without it, fixed windows are used

Rules: FMT-01, ED-03, QC-06 (and QC-01 for the inspection sheets, which a person must review).
"""
import argparse, os, re, subprocess, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from common import Report, PASS, FAIL, REVIEW, NP, PROFILES, probe, detect_format, frame, load_json


def intervals(text, key_s, key_e):
    starts = [float(x) for x in re.findall(key_s + r':\s*(\d+(?:\.\d+)?)', text)]
    ends = [float(x) for x in re.findall(key_e + r':\s*(\d+(?:\.\d+)?)', text)]
    return [(s, ends[i] if i < len(ends) else None) for i, s in enumerate(starts)]


def covered(iv, holds, dur):
    s, e = iv; e = dur if e is None else e
    for h in holds:
        ov = max(0.0, min(e, h[1]) - max(s, h[0]))
        if e - s > 0 and ov / (e - s) >= 0.8: return h
    return None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('video'); ap.add_argument('--format', default='auto'); ap.add_argument('--out')
    ap.add_argument('--holds'); ap.add_argument('--scenes'); ap.add_argument('--loop', action='store_true')
    ap.add_argument('--no-sheets', action='store_true')
    ap.add_argument('--lufs', type=float, default=-14.0); ap.add_argument('--lufs-tol', type=float, default=1.0)
    ap.add_argument('--tp-max', type=float, default=-1.0)
    a = ap.parse_args(argv)
    R = Report('qc_video', a.video)
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.video)), 'qc', os.path.splitext(os.path.basename(a.video))[0])
    info = probe(a.video)
    if not info or not info['width']:
        R.add('readable video stream', FAIL, 'ffprobe found no video stream', 'QC-06'); return R.finish(out)
    fmt = detect_format(info) if a.format == 'auto' else a.format
    if fmt not in PROFILES:
        R.add('format', FAIL, f"{info['width']}x{info['height']} is neither 1080x1920 (Short) nor 1920x1080 (film)", 'QC-06')
        return R.finish(out)
    P = PROFILES[fmt]; W, H, dur = info['width'], info['height'], info['duration']
    if (W, H) != (P['W'], P['H']): R.add('dimensions', FAIL, f'{W}x{H}, expected {P["W"]}x{P["H"]} for {fmt}', 'QC-06')
    else: R.add('dimensions', PASS, f'{W}x{H} ({fmt})', 'QC-06')
    R.coverage = dict(format=fmt, duration_s=round(dur, 2), fps=info['fps'])

    # duration
    if P['max_duration']:
        R.add('duration under 3:00', PASS if dur < P['max_duration'] else FAIL, f'{dur:.2f} s', 'FMT-01')
    else:
        R.add('duration', PASS, f'{dur:.2f} s (films have no fixed limit)', 'FMT-01')

    # one decoding pass: black, freeze, loudness, silence
    holds = load_json(a.holds, [])
    vf = 'blackdetect=d=0.3:pix_th=0.03,freezedetect=n=0.003:d=1.5'
    af = 'ebur128=peak=true,silencedetect=n=-50dB:d=2'
    cmd = ['ffmpeg', '-hide_banner', '-nostats', '-i', a.video, '-vf', vf]
    if info['acodec']: cmd += ['-af', af]
    cmd += ['-f', 'null', '-']
    o = subprocess.run(cmd, capture_output=True, text=True).stderr

    blacks = intervals(o, 'black_start', 'black_end')
    R.add('black frames', FAIL if blacks else PASS, f'{len(blacks)} black interval(s) {blacks[:5]}' if blacks else 'none', 'QC-06')

    fr = intervals(o, 'freeze_start', 'freeze_end')
    unmarked = [(round(s, 2), round(e, 2) if e else None) for s, e in fr if not covered((s, e), holds, dur)]
    marked = [(round(s, 2), round(e, 2) if e else None) for s, e in fr if covered((s, e), holds, dur)]
    if not fr: R.add('freezes (holds over 1.5 s)', PASS, 'none', 'QC-06')
    elif unmarked:
        R.add('freezes (holds over 1.5 s)', REVIEW,
              f'{len(unmarked)} unmarked: {unmarked[:8]}' + ('' if a.holds else '; no HOLD list supplied') +
              f'; {len(marked)} inside marked HOLDs. Fix, or mark as HOLD in the scene sheet if intentional (DIR-02)', 'QC-06')
    else: R.add('freezes (holds over 1.5 s)', PASS, f'{len(marked)} freeze(s), all inside marked HOLDs', 'QC-06')

    if not info['acodec']:
        R.add('audio stream', FAIL, 'no audio stream', 'ED-03')
    else:
        s = o[o.rfind('Summary:'):]
        try:
            I = float(re.search(r'I:\s*(-?[\d.]+) LUFS', s).group(1)); tp = float(re.search(r'Peak:\s*(-?[\d.]+|-inf) dBFS', s).group(1))
        except Exception:
            I = tp = None
        if I is None: R.add('loudness', NP, 'ebur128 summary not found', 'ED-03')
        else:
            R.add('integrated loudness', PASS if abs(I - a.lufs) <= a.lufs_tol else FAIL, f'{I} LUFS (target {a.lufs} ± {a.lufs_tol})', 'ED-03')
            R.add('true peak', PASS if tp <= a.tp_max else FAIL, f'{tp} dBTP (max {a.tp_max})', 'ED-03')
        sil = intervals(o, 'silence_start', 'silence_end')
        R.add('audio dropouts (silence over 2 s below -50 dB)', REVIEW if sil else PASS,
              f'{sil[:6]} (check: deliberate silence or a dropout?)' if sil else 'none', 'ED-03')

    err = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-f', 'null', '-'], capture_output=True, text=True).stderr.strip()
    R.add('decode errors', FAIL if err else PASS, f'{len(err.splitlines())} error line(s): {err[:200]}' if err else '0', 'QC-06')

    f0 = frame(a.video, 0.0, W, H)
    if f0 is None: R.add('frame 1 brightness', NP, 'could not read frame 1', 'DIR-08')
    else:
        m = float(f0.mean()); R.add('frame 1 brightness', PASS if m > 60 else FAIL, f'mean {m:.1f}/255 (min 60)', 'DIR-08')
    if a.loop:
        fl = frame(a.video, max(0, dur - 0.25), W, H)
        if f0 is None or fl is None: R.add('loop seam', NP, 'frames unreadable', 'FMT-06')
        else:
            d = float(np.abs(f0.astype(float) - fl.astype(float)).mean())
            R.add('loop seam (first vs last frame)', PASS if d < 3.0 else FAIL, f'mean difference {d:.2f} (max 3.0)', 'FMT-06')

    # sharpness: Laplacian variance per scene, centre region (excludes corner and caption bands)
    import cv2
    sc = load_json(a.scenes)
    if sc: bounds = [(n, t0, (sc[i + 1][1] if i + 1 < len(sc) else dur)) for i, (n, t0) in enumerate(sc)]
    else:
        step = 5.0 if fmt == 'short' else 20.0
        bounds = [(f'{t:.0f}s', t, min(dur, t + step)) for t in np.arange(0, dur, step)]
    y0, y1 = int(H * P['top_band'][1]), int(H * P['caption_band'][0])
    sharp = {}
    for n, t0, t1 in bounds:
        fm = frame(a.video, (t0 + t1) / 2, W, H)
        if fm is None: continue
        g = cv2.cvtColor(fm, cv2.COLOR_RGB2GRAY)[y0:y1]
        sharp[n] = round(float(cv2.Laplacian(g, cv2.CV_64F).var()), 1)
    if not sharp: R.add('sharpness per scene', NP, 'no frames read', 'QC-06')
    else:
        med = float(np.median(list(sharp.values())))
        low = {k: v for k, v in sharp.items() if v < max(20.0, 0.25 * med)}
        R.add('sharpness per scene', REVIEW if low else PASS,
              (f'low scores {low} (median {med:.0f}). Flat vector maps and diagrams score low by nature (known false positive); '
               'image scale is verified by check_assets') if low else f'{len(sharp)} scenes, median {med:.0f}, none low', 'QC-06')
    R.coverage['scenes_sampled'] = len(sharp)

    # inspection sheets for the human frame-level review (QC-01)
    if not a.no_sheets:
        from PIL import Image, ImageDraw
        os.makedirs(out, exist_ok=True)
        tw = 216 if fmt == 'short' else 320; th = int(tw * H / W)
        ts = np.arange(0, dur, 1.0 if dur < 300 else 5.0); cols = 10; rows = (len(ts) + cols - 1) // cols
        cs = Image.new('RGB', (cols * tw, rows * (th + 20)), (30, 30, 30)); d = ImageDraw.Draw(cs)
        for i, t in enumerate(ts):
            fm = frame(a.video, t, W, H)
            if fm is None: continue
            cs.paste(Image.fromarray(fm).resize((tw, th), Image.LANCZOS), ((i % cols) * tw, (i // cols) * (th + 20)))
            d.text(((i % cols) * tw + 4, (i // cols) * (th + 20) + th + 4), f'{t:.0f}s', fill='white')
        cs.save(os.path.join(out, 'contact_sheet.jpg'), quality=82)
        fs = Image.new('RGB', (10 * tw, 9 * th))
        for i in range(90):
            fm = frame(a.video, i / 30, W, H)
            if fm is not None: fs.paste(Image.fromarray(fm).resize((tw, th), Image.LANCZOS), ((i % 10) * tw, (i // 10) * th))
        fs.save(os.path.join(out, 'first_3s.jpg'), quality=82)
        bands = Image.new('RGB', (W, 12 * 200))
        for i, t in enumerate(np.linspace(1, max(1, dur - 1), 12)):
            fm = frame(a.video, t, W, H)
            if fm is None: continue
            tb = fm[int(H * P['top_band'][0]):int(H * P['top_band'][1])]; cb = fm[int(H * P['caption_band'][0]):int(H * P['caption_band'][1])]
            bands.paste(Image.fromarray(tb).resize((W, 100)), (0, i * 200)); bands.paste(Image.fromarray(cb).resize((W, 100)), (0, i * 200 + 100))
        bands.save(os.path.join(out, 'corners_captions.jpg'), quality=85)
        pw = P['phone_w']; phh = int(pw * H / W); ph = Image.new('RGB', (6 * pw, 2 * phh))
        for i, t in enumerate(np.linspace(min(2, dur / 2), max(0, dur - 2), 12)):
            fm = frame(a.video, t, W, H)
            if fm is not None: ph.paste(Image.fromarray(fm).resize((pw, phh), Image.LANCZOS), ((i % 6) * pw, (i // 6) * phh))
        ph.save(os.path.join(out, 'phone_size.jpg'), quality=82)
        R.coverage['sheets'] = 'contact_sheet, first_3s, corners_captions, phone_size'
    R.add('professional visual QC (12-item checklist, frame-level inspection)', NP,
          'human review required; use the sheets in the output folder' + ('' if not a.no_sheets else ' (sheets skipped)'), 'QC-01')
    return R.finish(out)


if __name__ == '__main__':
    sys.exit(main())
