"""DIWALI · 6/6 'Why Delhi chokes around Diwali' — style v2, loops into its own opening."""
import sys, os, json, math, subprocess
import numpy as np, cairo
from PIL import Image, ImageDraw, ImageFont, ImageFilter
_argv = sys.argv; sys.argv = sys.argv[:1]
LANGV = os.environ.get('LANGV', 'en'); PLAT = os.environ.get('PLAT', 'yt')
sys.path.insert(0, '/home/claude/g3'); sys.path.insert(0, '/home/claude/rv')
import render3 as R3
import render2 as K
sys.argv = _argv
W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.30
ROOT = '/home/claude/b7/'
CREAM, AMBER, AMBER2, INK = K.CREAM, K.AMBER, K.AMBER2, K.INK
prog, e_out, e_io, e_back, clamp = K.prog, K.e_out, K.e_io, K.e_back, K.clamp
font, rrect = K.font, K.rrect
glowdot, glass_dark, agrad = K.glowdot, K.glass_dark, K.agrad
surf_from_pil, torn, board_bg = R3.surf_from_pil, R3.torn, R3.board_bg
import te_text as TT
def head(c, txt, x, y, px, col=CREAM, a=1.0, anchor='c', shadow=True):
    if LANGV == 'te' and txt in TT.TR: return TT.draw(c, TT.TR[txt], x, y, px * 0.80, col, a, anchor, 'Black', stroke=3 if shadow else 0)
    return K.head(c, txt, x, y, px, col, a, anchor, shadow)
def mono(c, txt, x, y, px, col=AMBER, a=1.0, anchor='c', kind='monob'):
    if LANGV == 'te' and txt in TT.TR: return TT.draw(c, TT.TR[txt], x, y, px * (1.15 if px < 30 else 0.95), col, a, anchor, 'Bold')
    return K.mono(c, txt, x, y, px, col, a, anchor, kind)
def pill(c, txt, cx, cy, px=34, fill=AMBER, col=K.BLACK, a=1.0, s=1.0, kind='head'):
    if s <= 0.01 or a <= 0: return
    if LANGV == 'te' and txt in TT.TR:
        sf, _ = TT.surf(TT.TR[txt], px * 0.95, INK if fill == AMBER else CREAM, 'Bold'); w = sf.get_width() + px * 1.1; h = px * 1.85
        c.save(); c.translate(cx, cy); c.scale(s, s)
        if fill == AMBER: rrect(c, -w / 2, -h / 2, w, h, h / 2); c.set_source_rgba(*AMBER, a); c.fill()
        else: glass_dark(c, -w / 2, -h / 2, w, h, h / 2, a)
        c.set_source_surface(sf, -sf.get_width() / 2, -sf.get_height() / 2); c.paint_with_alpha(a); c.restore(); return
    K.pill(c, txt, cx, cy, px, fill, col, a, s, kind)

# ---------------- voice / words / anchors ----------------
VFILE = ROOT + f'voice_{LANGV}.wav'
VOICE_LEN = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', VFILE], capture_output=True, text=True).stdout)
DUR = LEAD + VOICE_LEN + TAIL
MK = {k: (a + LEAD, b + LEAD) for k, (a, b) in json.load(open(ROOT + f'marks_{LANGV}.json')).items()}
def S(k): return MK[k][0]
def E(k): return MK[k][1]
if LANGV == 'en':
    WORDS = json.load(open(ROOT + 'words_en.json'))
else:
    WORDS = json.load(open(ROOT + 'words_te.json'))['words']
def AT(line, en, te, n=1, off=0.0):
    sub = en if LANGV == 'en' else te
    if sub is None: return S(line) + off
    if isinstance(sub, float): return S(line) + sub * (E(line) - S(line)) + off
    k = 0
    for s, e, w, ln in WORDS:
        if ln == line and sub.lower() in w.lower():
            k += 1
            if k == n: return s + LEAD + off
    raise KeyError((LANGV, line, sub))
