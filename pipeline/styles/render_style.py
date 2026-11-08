#!/usr/bin/env python3
"""Render any library style to a still, a video, or a contact sheet.
  python3 pipeline/styles/render_style.py glow_atom --aspect 9x16 --t 5 --out atom.png
  python3 pipeline/styles/render_style.py domino_reveal --spec spec.json --video out.mp4 --dur 9
  python3 pipeline/styles/render_style.py all --sheet sheet.jpg
In a scene script: `from render_style import frame` then `frame('glow_atom', v, '9x16', spec)`."""
import argparse, importlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
from core import Stage

STYLES = ['isometric', 'paper_cut', 'chart_3d', 'synthwave', 'explainer_3d', 'maths_diagram', 'cartoon_explainer', 'domino_reveal', 'glow_atom']
_stages = {}


def mod(name): return importlib.import_module(name)


def frame(style, v, aspect='9x16', spec=None):
    st = _stages.setdefault(aspect, Stage(aspect)); return mod(style).draw(st, v, spec).convert('RGB')


def video(style, out, dur, aspect, spec, fps=30):
    st = Stage(aspect); p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{st.W}x{st.H}', '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(int(dur * fps)): p.stdin.write(frame(style, i / fps, aspect, spec).tobytes())
    p.stdin.close(); p.wait()


def sheet(out, aspect, times=None):
    tw, th = (270, 480) if aspect == '9x16' else (480, 270); times = times or (.0, .5, .85); S = Image.new('RGB', ((tw + 8) * len(STYLES), (th + 8) * len(times)), (40, 40, 40))
    for x, s in enumerate(STYLES):
        for y, f in enumerate(times): S.paste(frame(s, mod(s).DURATION * f, aspect).resize((tw, th), Image.LANCZOS), (x * (tw + 8) + 4, y * (th + 8) + 4))
    S.save(out, quality=88)


if __name__ == '__main__':
    a = argparse.ArgumentParser(); a.add_argument('style'); a.add_argument('--aspect', default='9x16', choices=['9x16', '16x9']); a.add_argument('--t', type=float, default=5.0); a.add_argument('--out', default='style.png'); a.add_argument('--spec'); a.add_argument('--video'); a.add_argument('--dur', type=float); a.add_argument('--sheet'); o = a.parse_args()
    spec = json.load(open(o.spec)) if o.spec else None
    if o.sheet: sheet(o.sheet, o.aspect)
    elif o.video: video(o.style, o.video, o.dur or mod(o.style).DURATION, o.aspect, spec)
    else: frame(o.style, o.t, o.aspect, spec).save(o.out)
