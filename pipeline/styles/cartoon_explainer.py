"""7) Cartoon Explainer: Anna and Chelli, the channel's own characters, talk it through with real mouth movement.
Best for: the question-and-answer beats, relatable moments, anything that needs a human.
Pass env={'ANNA': [...], 'CHELLI': [...]} from voice_envelope() so lips follow the real voice."""
import math, subprocess
import cairo
import numpy as np
from PIL import Image
from core import *
import characters as ch

DURATION = 8.0
DEFAULT = dict(topic='WHY IS GOLD SO EXPENSIVE?', lines=[dict(who='CHELLI', t0=.15, t1=2.9, text='But why does everyone want gold?'), dict(who='ANNA', t0=3.2, t1=7.7, text='Because nobody can print more of it.')], env=None, fps=30)


def voice_envelope(path, fps=30):
    """Per-frame mouth opening from a voice file. Soft attack, slower release: lips glide, they do not flap."""
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-ar', '16000', '-ac', '1', '-f', 'f32le', '-'], capture_output=True).stdout, np.float32)
    hop = 160; n = len(x) // hop; r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-6; db = 20 * np.log10(r); hi = np.percentile(db, 97); u = np.clip((db - (hi - 30)) / 30, 0, 1)
    out = np.zeros_like(u); y = 0.0
    for i, q in enumerate(u): y += (q - y) * (.35 if q > y else .12); out[i] = y
    k = 100 / fps; idx = (np.arange(int(len(out) / k)) * k).astype(int); return np.clip(out[idx] ** 1.2 * .85, 0, .75).tolist()


def _synth(v, seed):
    """Stand-in speech rhythm for previews only: syllables with phrase breaks."""
    a = .5 + .5 * math.sin(v * 15.7 + seed + 1.6 * math.sin(v * 3.1 + seed)); b = .55 + .45 * math.sin(v * 2.3 + seed * 2)
    return clamp(a ** 1.5 * b * .68, 0, .7)


def _blink(t, period, ph):
    u = (t + ph) % period; return 1 - abs(u - .07) / .07 if u < .14 else 0


def _speech(s, v, who):
    for l in s['lines']:
        if l['who'] == who and l['t0'] <= v <= l['t1']:
            if s['env'] and who in s['env']:
                e = s['env'][who]; i = int(v * s['fps']); return e[i] if i < len(e) else 0.0, l
            return _synth(v, 1.3 if who == 'ANNA' else 4.1) * prog(v, l['t0'], l['t0'] + .08) * (1 - prog(v, l['t1'] - .08, l['t1'])), l
    return 0.0, None


def _bubble(img, st, txt, cx, tail_x, tail_y, bottom, k):
    from PIL import ImageDraw
    if k <= .01: return
    px = 52 if st.portrait else 46; maxw = st.sw - 90 if st.portrait else 860; L = wrap(txt, 'head', px, maxw); f = pick(txt, 'head', px); w = int(max(f.getlength(l) for l in L) + 76); h = int(len(L) * px * 1.28 + 50); top = int(max(st.y0 + 110, bottom - h))
    x0 = int(clamp(cx - w / 2, st.x0, st.x1 - w)); spr = Image.new('RGBA', (st.W, st.H), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); d.rounded_rectangle((x0, top, x0 + w, top + h), radius=34, fill=CREAM + (255,))
    bx = clamp(tail_x, x0 + 70, x0 + w - 70); d.polygon([(bx - 34, top + h - 3), (bx + 34, top + h - 3), (tail_x, tail_y)], fill=CREAM + (255,))
    for i, l in enumerate(L): d.text((x0 + w / 2, top + 25 + (i + .5) * px * 1.28), l, font=f, fill=INK + (255,), anchor='mm')
    a = spr.getchannel('A').point(lambda p: int(p * clamp(k))); img.paste(spr, (0, 0), a)


def draw(st, v, spec=None):
    s = merge(DEFAULT, spec); W, H = st.W, st.H; P = st.portrait; surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, .98, .90, .72); g.add_color_stop_rgb(.72, .96, .78, .49); g.add_color_stop_rgb(.73, .55, .35, .20); g.add_color_stop_rgb(1, .36, .22, .13); c.set_source(g); c.paint()
    c.set_source_rgba(1, 1, 1, .22)
    for i in range(7):
        a0 = -1.9 + i * .34 + .03 * math.sin(v * .5); c.move_to(W / 2, -160); c.line_to(W / 2 + math.tan(a0 * .55) * H * 1.3, H); c.line_to(W / 2 + math.tan((a0 + .15) * .55) * H * 1.3, H); c.close_path(); c.fill()
    sc = .95 if P else .68; floor = H * .925 if P else H * .955; ax, cx_ = (st.x0 + 190, st.x1 - 175) if P else (st.W * .32, st.W * .68)
    ta, la = _speech(s, v, 'ANNA'); tc, lc = _speech(s, v, 'CHELLI'); q = 1.0
    ch.anna(c, ax, floor, sc, v, talk=ta, blink=_blink(v, 3.7, .4), gesture=(.35 + .3 * math.sin(v * 1.3)) if la else .05, look=(.45, -.05) if lc else (.1, 0), tilt=4 * math.sin(v * .7) if la else 0)
    ch.chelli(c, cx_, floor, sc * (.92 if P else .92), v, talk=tc, blink=_blink(v, 4.3, 2.1), gesture=(.3 + .25 * math.sin(v * 1.7)) if lc else .04, look=(-.45, -.05) if la else (-.1, 0), tilt=-3 * math.sin(v * .9) if lc else 0, q=0)
    surf.flush(); a = np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4)[..., [2, 1, 0]].copy(); img = Image.fromarray(a, 'RGB')
    text(img, s['topic'], st.cx, st.y0 + 44, 64 if P else 66, INK, maxw=st.sw)
    if la: _bubble(img, st, la['text'], ax + 120, ax + 40, floor - 915 * sc, floor - 985 * sc, e_back(prog(v, la['t0'], la['t0'] + .2)) * (1 - prog(v, la['t1'] - .06, la['t1'])))
    if lc: _bubble(img, st, lc['text'], cx_ - 120, cx_ - 30, floor - 815 * sc * .92, floor - 985 * sc, e_back(prog(v, lc['t0'], lc['t0'] + .2)) * (1 - prog(v, lc['t1'] - .06, lc['t1'])))
    return img
