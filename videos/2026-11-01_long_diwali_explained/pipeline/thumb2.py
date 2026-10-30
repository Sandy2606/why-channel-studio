"""Thumbnail v2: Anna & Chelli laughing with sparklers, question cards across the background, logo top-left, DIWALI EXPLAINED bottom."""
import os, math, numpy as np, cairo
from PIL import Image
from base import *
import room as RM, gfx1 as G1
import chars2 as CH

s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
# night background
g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.06, 0.05, 0.10); g.add_color_stop_rgb(1, 0.14, 0.08, 0.05)
c.set_source(g); c.paint()
rng = np.random.default_rng(8)
for i in range(70):  # bokeh
    x, y, r = rng.uniform(0, W), rng.uniform(0, H * 0.8), rng.uniform(6, 34)
    col = AMBER if i % 3 else (1.0, 0.55, 0.25)
    bg = cairo.RadialGradient(x, y, 0, x, y, r); bg.add_color_stop_rgba(0, *col, 0.35); bg.add_color_stop_rgba(1, *col, 0)
    c.set_source(bg); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


def burst(cx, cy, R, col, n=28, a=0.8):
    for k in range(n):
        an = k * 2 * math.pi / n
        x0, y0 = cx + math.cos(an) * R * 0.25, cy + math.sin(an) * R * 0.25
        x1, y1 = cx + math.cos(an) * R, cy + math.sin(an) * R
        lg = cairo.LinearGradient(x0, y0, x1, y1); lg.add_color_stop_rgba(0, *col, 0); lg.add_color_stop_rgba(1, *col, a)
        c.set_source(lg); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
        c.set_source_rgba(1, 0.95, 0.8, a); c.arc(x1, y1, 4, 0, 2 * math.pi); c.fill()


burst(330, 300, 170, (1.0, 0.72, 0.2)); burst(1620, 250, 200, (1.0, 0.55, 0.3)); burst(980, 120, 120, (0.6, 0.85, 1.0), 22, 0.6)
burst(1780, 640, 110, (1.0, 0.8, 0.4), 20, 0.6); burst(130, 700, 100, (0.6, 0.85, 1.0), 18, 0.5)
# question cards across the background
POS = [(300, 150, -6), (760, 90, 3), (1250, 110, -3), (1700, 120, 5), (170, 470, 4), (1760, 420, -5), (420, 640, -3), (1560, 640, 4), (980, 300, 2)]
POS = [(660, 70, -3), (1190, 62, 2), (1640, 100, -3), (330, 300, 4), (1640, 290, -4), (230, 520, -3), (1700, 500, 3), (960, 230, 2), (420, 700, 3)]
for i, (x, y, r) in enumerate(POS):
    w = (text_w(c, L(*G1.QCARDS[i]), 30) + 90) * 1.45
    x = min(max(x, w / 2 + 24), W - w / 2 - 24)
    c.save(); c.translate(x, y); c.rotate(math.radians(r)); G1.qcard(c, i, 0, 0, 99, 0, sc=1.45, locked=False, a=0.92); c.restore()
c.set_source_rgba(0.05, 0.04, 0.06, 0.25); c.paint()


def sparkler(hx, hy, ang, t=1.0):
    ex, ey = hx + math.cos(ang) * 150, hy + math.sin(ang) * 150
    c.set_source_rgb(0.35, 0.33, 0.32); c.set_line_width(6); c.move_to(hx, hy); c.line_to(ex, ey); c.stroke()
    gl = cairo.RadialGradient(ex, ey, 0, ex, ey, 190); gl.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.85); gl.add_color_stop_rgba(0.3, 1, 0.75, 0.3, 0.35); gl.add_color_stop_rgba(1, 1, 0.7, 0.3, 0)
    c.set_source(gl); c.arc(ex, ey, 190, 0, 2 * math.pi); c.fill()
    r2 = np.random.default_rng(int(hx))
    for k in range(60):
        an = r2.uniform(0, 2 * math.pi); L_ = r2.uniform(30, 150)
        x1, y1 = ex + math.cos(an) * L_, ey + math.sin(an) * L_
        c.set_source_rgba(1, r2.uniform(0.8, 1.0), r2.uniform(0.5, 0.9), r2.uniform(0.5, 1)); c.set_line_width(2.5)
        c.move_to(ex + math.cos(an) * L_ * 0.4, ey + math.sin(an) * L_ * 0.4); c.line_to(x1, y1); c.stroke()
        if k % 4 == 0:
            c.save(); c.translate(x1, y1); c.move_to(-8, 0); c.line_to(8, 0); c.move_to(0, -8); c.line_to(0, 8); c.stroke(); c.restore()
    c.set_source_rgb(1, 1, 0.92); c.arc(ex, ey, 10, 0, 2 * math.pi); c.fill()


# characters laughing (eyes squeezed, mouth open), sparklers in raised hands
AS, CS = 1.12, 1.12; ax, cx, by = 640, 1290, 1330
T_ = 0.6
CH.anna(c, ax, by, AS, t=T_, talk=0.95, blink=1.0, gesture=0.95, look=(0, 0), tilt=-6)
CH.chelli(c, cx, by, CS, t=T_, talk=0.95, blink=1.0, gesture=0.95, look=(0, 0), tilt=7, q=0)


def happy(x, sc, hy, r, rot, br):
    c.save(); c.translate(x, by); c.scale(sc, sc); c.translate(0, br); c.translate(0, hy); c.rotate(math.radians(rot))
    ex, ey, ew = r * 0.36, -r * 0.02, r * 0.21
    for d in (-1, 1):
        c.set_source_rgb(*CH.SKIN); c.save(); c.translate(d * ex, ey); c.scale(1, 0.5); c.arc(0, 0, ew * 1.15, 0, 2 * math.pi); c.restore(); c.fill()
        c.set_source_rgb(*CH.OUT); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.arc(d * ex, ey + ew * 0.55, ew * 0.85, math.pi * 1.12, math.pi * 1.88); c.stroke()
    c.restore()


happy(ax, AS, -735, 150, -6 + 2 * math.sin(T_ * 1.3), math.sin(T_ * 2.0) * 2)
happy(cx, CS, -660, 132, 7 + 2.5 * math.sin(T_ * 1.5 + 0.5), math.sin(T_ * 2.3 + 1) * 2)
g_ = 0.95
sparkler(ax + (150 + 50 * g_ + 2) * AS, by + (-330 - 250 * g_ + 14 * (1 - g_)) * AS, math.radians(-70))
sparkler(cx + (122 + 40 * g_ + 2) * CS, by + (-310 - 230 * g_ + 10 * (1 - g_)) * CS, math.radians(-65))
RM.qmark(c, cx + 10, by - (660 + 168) * CS - 110, 150, 0.0, 1.0)
# bottom title
g = cairo.LinearGradient(0, 700, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(0.55, 0, 0, 0, 0.75); g.add_color_stop_rgba(1, 0, 0, 0, 0.95)
c.set_source(g); c.rectangle(0, 700, W, H - 700); c.fill()
if LANG == 'en':
    w1 = text_w(c, 'DIWALI ', 165); w2 = text_w(c, 'EXPLAINED', 165); x0 = W / 2 - (w1 + w2) / 2
    txt(c, 'DIWALI ', x0, 880, 165, CREAM, anchor='l', stroke=12); txt(c, 'EXPLAINED', x0 + w1, 880, 165, grad=True, anchor='l', stroke=12)
else:
    w1 = text_w(c, 'దీపావళి ', 155); w2 = text_w(c, 'వివరంగా', 155); x0 = W / 2 - (w1 + w2) / 2
    txt(c, 'దీపావళి ', x0, 870, 155, CREAM, anchor='l', stroke=12); txt(c, 'వివరంగా', x0 + w1, 870, 155, grad=True, anchor='l', stroke=12)
a = np.ndarray((H, W, 4), np.uint8, s.get_data())[:, :, [2, 1, 0]].copy()
import sys
sys.path.insert(0, '/home/claude/why-channel-studio/videos/2026-10-26_short_gold_stardust/pipeline'); sys.path.insert(0, '/home/claude/elnino')
from thumbkit import logo
from epic import font as efont
from PIL import ImageFont, ImageDraw
base = Image.fromarray(a).convert('RGBA')
def tagpill(im, text, cy):
    if LANG == 'en': f = efont('mono', 40)
    else:
        f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', 40, layout_engine=ImageFont.Layout.RAQM)
        try: f.set_variation_by_name('Bold')
        except Exception: pass
    w = int(f.getlength(text) + (len(text) * 6 if LANG == 'en' else 0) + 76); h = 78
    t = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t)
    d.rounded_rectangle((1, 1, w - 2, h - 2), radius=39, fill=(10, 10, 10, 170), outline=(255, 178, 36, 255), width=3)
    if LANG == 'en':
        x = 38
        for ch in text: d.text((x, h / 2), ch, font=f, fill=(255, 178, 36), anchor='lm'); x += f.getlength(ch) + 6
    else: d.text((w / 2, h / 2), text, font=f, fill=(255, 178, 36), anchor='mm')
    im.alpha_composite(t, (int((W - w) / 2), cy - h // 2))
tagpill(base, 'DIWALI · FULL STORY' if LANG == 'en' else 'దీపావళి · FULL STORY', 1010)
logo(base, 56, 46, 80)
base.convert('RGB').resize((1280, 720), Image.LANCZOS).save(f'/home/claude/dl/thumb2_diwali_long_{LANG.upper()}.jpg', quality=92)
print('ok')
