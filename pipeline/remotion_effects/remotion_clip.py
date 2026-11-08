"""Thin bridge from the Python editors to the Remotion effects.

    from remotion_clip import render_clip, iter_frames, cue
    mp4 = render_clip('stat-chart', props, aspect='9x16', lang='te', out='scene12.mp4')
    for img in iter_frames(mp4): ...   # PIL images for a render_*.py pipeline

Props carry `language`, `cues` (beat name -> frame, use cue(seconds)) and `durationFrames`.
"""
import json, os, subprocess, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = {'9x16': (1080, 1920), '16x9': (1920, 1080)}
FPS = 30


def cue(seconds, fps=FPS):
    """Voice timestamp in seconds, measured from the start of this clip, to a frame number."""
    return int(round(seconds * fps))


def render_clip(effect, props=None, aspect='9x16', lang='en', out=None):
    """Render one effect to a silent MP4 and return its path. Raises if props fail validation."""
    out = os.path.abspath(out or os.path.join(HERE, 'renders', f'{effect}_{aspect}_{lang}.mp4'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cmd = ['node', 'cli/render.mjs', effect, '--aspect', aspect, '--lang', lang, '--out', out]
    tmp = None
    if props is not None:
        tmp = tempfile.NamedTemporaryFile('w', suffix='.json', delete=False, encoding='utf-8')
        json.dump({'language': lang, **props}, tmp, ensure_ascii=False); tmp.close()
        cmd += ['--props', tmp.name]
    try:
        r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
        if r.returncode or not os.path.exists(out):
            raise RuntimeError(f'{effect} failed:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}')
    finally:
        if tmp: os.unlink(tmp.name)
    return out


def iter_frames(mp4, aspect='9x16'):
    """Yield the clip's frames as RGB PIL images."""
    w, h = SIZES[aspect]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', mp4, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    try:
        while True:
            b = p.stdout.read(w * h * 3)
            if len(b) < w * h * 3: break
            yield Image.frombytes('RGB', (w, h), b)
    finally:
        p.stdout.close(); p.wait()
