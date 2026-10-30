"""Room set, Anna & Chelli staging, camera, props, overlays."""
import math, sys
import numpy as np, cairo
from base import *
sys.path.insert(0, '/home/claude/dw')
import chars2 as CH

AX, CX, BY, SC = 660, 1290, 1005, 0.9
_BG = None


def room_bg():
    global _BG
    if _BG is not None: return _BG
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    g = cairo.LinearGradient(0, 0, 0, 880); g.add_color_stop_rgb(0, 0.50, 0.36, 0.25); g.add_color_stop_rgb(1, 0.40, 0.28, 0.19)
    c.set_source(g); c.paint()
    # soft lamp glow left
    rg = cairo.RadialGradient(260, 420, 0, 260, 420, 700); rg.add_color_stop_rgba(0, 1.0, 0.80, 0.50, 0.30); rg.add_color_stop_rgba(1, 1, 0.8, 0.5, 0)
    c.set_source(rg); c.paint()
    # wainscot line
    c.set_source_rgba(0, 0, 0, 0.10); c.rectangle(0, 700, W, 180); c.fill()
    c.set_source_rgba(1, 0.85, 0.6, 0.12); c.rectangle(0, 698, W, 4); c.fill()
    # window (right)
    wx, wy, ww, wh = 1480, 150, 380, 380
    c.set_source_rgb(0.30, 0.20, 0.13); rrect(c, wx - 18, wy - 18, ww + 36, wh + 36, 14); c.fill()
    sg = cairo.LinearGradient(0, wy, 0, wy + wh); sg.add_color_stop_rgb(0, 0.07, 0.09, 0.20); sg.add_color_stop_rgb(1, 0.16, 0.12, 0.22)
    c.set_source(sg); c.rectangle(wx, wy, ww, wh); c.fill()
    rng = np.random.default_rng(3)
    for _ in range(26):
        x, y, r = wx + rng.uniform(10, ww - 10), wy + rng.uniform(wh * 0.45, wh - 10), rng.uniform(6, 20)
        bg = cairo.RadialGradient(x, y, 0, x, y, r); bg.add_color_stop_rgba(0, 1.0, 0.75, 0.3, 0.7); bg.add_color_stop_rgba(1, 1.0, 0.7, 0.3, 0)
        c.set_source(bg); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(0.30, 0.20, 0.13); c.rectangle(wx + ww / 2 - 7, wy, 14, wh); c.fill(); c.rectangle(wx, wy + wh / 2 - 7, ww, 14); c.fill()
    # frame on wall (left): rangoli art
    fx, fy = 120, 230
    c.set_source_rgb(0.30, 0.20, 0.13); rrect(c, fx, fy, 210, 210, 8); c.fill(); c.set_source_rgb(0.93, 0.88, 0.78); c.rectangle(fx + 14, fy + 14, 182, 182); c.fill()
    for k, col in enumerate([(0.93, 0.45, 0.20), TEAL, AMBER, (0.75, 0.25, 0.40)]):
        r = 80 - k * 18
        for i in range(8):
            a = i * math.pi / 4 + k * 0.2
            c.set_source_rgb(*col); c.save(); c.translate(fx + 105 + math.cos(a) * r * 0.55, fy + 105 + math.sin(a) * r * 0.55); c.rotate(a)
            c.scale(1, 0.5); c.arc(0, 0, r * 0.35, 0, 2 * math.pi); c.restore(); c.fill()
    c.set_source_rgb(*AMBER); c.arc(fx + 105, fy + 105, 12, 0, 2 * math.pi); c.fill()
    # floor
    fg = cairo.LinearGradient(0, 880, 0, H); fg.add_color_stop_rgb(0, 0.33, 0.22, 0.15); fg.add_color_stop_rgb(1, 0.24, 0.16, 0.11)
    c.set_source(fg); c.rectangle(0, 880, W, H - 880); c.fill()
    c.set_source_rgba(0, 0, 0, 0.18); c.rectangle(0, 878, W, 6); c.fill()
    # rug
    c.save(); c.translate(980, 1010); c.scale(1, 0.18); c.arc(0, 0, 640, 0, 2 * math.pi); c.restore(); c.set_source_rgb(0.55, 0.20, 0.18); c.fill()
    c.save(); c.translate(980, 1010); c.scale(1, 0.18); c.arc(0, 0, 590, 0, 2 * math.pi); c.restore(); c.set_source_rgba(*AMBER, 0.55); c.set_line_width(6); c.stroke()
    # sofa behind Anna
    c.set_source_rgb(0.60, 0.42, 0.30); rrect(c, 230, 600, 820, 170, 40); c.fill()
    c.set_source_rgb(0.52, 0.35, 0.24); rrect(c, 200, 700, 880, 200, 40); c.fill()
    c.set_source_rgba(0, 0, 0, 0.12); rrect(c, 200, 840, 880, 60, 30); c.fill()
    for x in (330, 900): c.set_source_rgb(0.85, 0.62, 0.30); rrect(c, x, 640, 120, 100, 24); c.fill()
    _BG = s; return s


def string_lights(c, t):
    for i in range(41):
        x = i * 48 + 10; y = 38 + 18 * math.sin(i * 0.55) + 6 * math.sin(i * 1.7)
        tw = 0.65 + 0.35 * math.sin(t * 2.2 + i * 1.3)
        col = (1.0, 0.70, 0.18) if i % 2 else (1.0, 0.55, 0.20)
        g = cairo.RadialGradient(x, y, 0, x, y, 30); g.add_color_stop_rgba(0, *col, 0.45 * tw); g.add_color_stop_rgba(1, *col, 0)
        c.set_source(g); c.arc(x, y, 30, 0, 2 * math.pi); c.fill()
        c.set_source_rgba(*col, 0.75 + 0.25 * tw); c.arc(x, y, 10, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.1, 0.07, 0.05, 0.6); c.set_line_width(2)
    c.move_to(10, 38)
    for i in range(41): c.line_to(i * 48 + 10, 38 + 18 * math.sin(i * 0.55) + 6 * math.sin(i * 1.7) - 10)
    c.stroke()


def diya(c, x, y, s, t, lit=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    if lit > 0:
        f = 1 + 0.08 * math.sin(t * 11 + x) + 0.05 * math.sin(t * 17)
        g = cairo.RadialGradient(0, -40, 0, 0, -40, 120); g.add_color_stop_rgba(0, 1, 0.75, 0.3, 0.5 * lit); g.add_color_stop_rgba(1, 1, 0.7, 0.3, 0)
        c.set_source(g); c.arc(0, -40, 120, 0, 2 * math.pi); c.fill()
        c.save(); c.translate(0, -18); c.scale(lit, f * lit)
        c.move_to(0, -52); c.curve_to(18, -26, 14, -4, 0, 0); c.curve_to(-14, -4, -18, -26, 0, -52); c.close_path()
        fg = cairo.LinearGradient(0, -52, 0, 0); fg.add_color_stop_rgb(0, 1, 0.95, 0.7); fg.add_color_stop_rgb(1, 1.0, 0.55, 0.1); c.set_source(fg); c.fill(); c.restore()
    c.move_to(-52, -14); c.curve_to(-40, 26, 40, 26, 52, -14); c.curve_to(30, -4, -30, -4, -52, -14); c.close_path()
    dg = cairo.LinearGradient(0, -14, 0, 24); dg.add_color_stop_rgb(0, 0.80, 0.42, 0.20); dg.add_color_stop_rgb(1, 0.52, 0.24, 0.10); c.set_source(dg); c.fill_preserve()
    c.set_source_rgb(*CH.OUT); c.set_line_width(4); c.stroke()
    c.restore()


def phone_tripod(c, x, y, t, rec_on, a=1.0):
    c.set_source_rgba(0.12, 0.10, 0.10, a); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx in (-60, 0, 60): c.move_to(x, y - 190); c.line_to(x + dx, y); c.stroke()
    c.set_source_rgba(0.08, 0.08, 0.09, a); rrect(c, x - 52, y - 300, 104, 180, 16); c.fill()
    c.set_source_rgba(0.22, 0.24, 0.28, a); rrect(c, x - 44, y - 290, 88, 160, 10); c.fill()
    if rec_on and int(t * 2) % 2 == 0:
        c.set_source_rgba(0.95, 0.2, 0.2, a); c.arc(x + 26, y - 270, 9, 0, 2 * math.pi); c.fill()


def qmark(c, x, y, size, t, a=1.0, pop=0.0):
    if a <= 0.01: return
    s = size * (1 + 0.25 * pop); yy = y + 6 * math.sin(t * 2.3)
    g = cairo.RadialGradient(x, yy, 0, x, yy, s * 0.9); g.add_color_stop_rgba(0, *AMBER, 0.35 * a); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.arc(x, yy, s * 0.9, 0, 2 * math.pi); c.fill()
    c.save(); c.translate(x, yy); c.rotate(math.radians(6 * math.sin(t * 1.7)))
    txt(c, '?', 0, 0, s, grad=True, a=a, stroke=s * 0.08); c.restore()


def blink_at(t, period, ph):
    k = (t + ph) % period
    return 1.0 if k < 0.07 else (0.5 if k < 0.12 else 0.0)


class Cast:
    """per-frame character state, set by render.py"""
    def __init__(self):
        self.anna = dict(x=AX, y=BY, s=SC, talk=0, gesture=0, look=(0.5, 0), tilt=0, a=1.0)
        self.chelli = dict(x=CX, y=BY, s=SC, talk=0, gesture=0, look=(-0.5, 0), tilt=0, a=1.0, q=1.0, qpop=0)


def draw_room(c, t, cast, cam=(1.0, W / 2, H / 2), rec=None, props=None, before_chars=None):
    z, fx, fy = cam
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    c.set_source_surface(room_bg(), 0, 0); c.paint()
    string_lights(c, t)
    phone_tripod(c, 975, 1000, t, rec is not None)
    for i, (x, s) in enumerate(((880, 0.55), (1100, 0.55))): diya(c, x, 1030, s, t)
    if before_chars: before_chars(c, t)
    A, Cc = cast.anna, cast.chelli
    CH.anna(c, A['x'], A['y'], A['s'], t=t, talk=A['talk'], blink=blink_at(t, 3.7, 0.3), gesture=A['gesture'], look=A['look'], tilt=A['tilt'])
    if Cc['a'] > 0:
        CH.chelli(c, Cc['x'], Cc['y'], Cc['s'], t=t, talk=Cc['talk'], blink=blink_at(t, 3.1, 1.1), gesture=Cc['gesture'], look=Cc['look'], tilt=Cc['tilt'], q=0)
        hx = Cc['x'] + 8; hy = Cc['y'] - (660 + 168) * Cc['s'] - 95
        qmark(c, hx, hy, 150 * Cc['s'], t, a=Cc['q'], pop=Cc['qpop'])
    if props: props(c, t)
    c.restore()


def rec_overlay(c, t, t_start, full=False, a=1.0):
    """phone viewfinder: small REC + timer (full=True adds corner brackets)."""
    el = max(0, t - t_start); mm, ss = int(el // 60), int(el % 60)
    x, y = W - 250, 92
    glass(c, x - 20, y - 24, 220, 48, 24, 0.85 * a, edge=False)
    if int(t * 2) % 2 == 0: c.set_source_rgba(0.95, 0.2, 0.2, a); c.arc(x + 8, y, 9, 0, 2 * math.pi); c.fill()
    txt(c, f'REC  {mm:02d}:{ss:02d}', x + 28, y, 22, CREAM, a, anchor='l', kind='monob')
    if full:
        c.set_source_rgba(*CREAM, 0.85 * a); c.set_line_width(5)
        for (px, py, dx, dy) in ((60, 60, 1, 1), (W - 60, 60, -1, 1), (60, H - 60, 1, -1), (W - 60, H - 60, -1, -1)):
            c.move_to(px, py + dy * 70); c.line_to(px, py); c.line_to(px + dx * 70, py); c.stroke()
        txt(c, '4K · 30', 90, H - 90, 20, CREAM, 0.7 * a, anchor='l', kind='monob')


# ---------------- props ----------------
def broom(c, x, y, ang, s=1.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgb(0.55, 0.38, 0.20); c.rectangle(-6, -260, 12, 260); c.fill()
    c.move_to(-10, 0); c.line_to(-60, 140); c.curve_to(-20, 155, 20, 155, 60, 140); c.line_to(10, 0); c.close_path()
    c.set_source_rgb(0.86, 0.72, 0.42); c.fill_preserve(); c.set_source_rgb(*CH.OUT); c.set_line_width(4); c.stroke()
    c.set_source_rgba(0.55, 0.42, 0.20, 0.8); c.set_line_width(2)
    for k in range(-4, 5): c.move_to(k * 2, 10); c.line_to(k * 13, 145); c.stroke()
    c.restore()


def dust(c, x, y, t, t0):
    u = prog(t, t0, t0 + 2.5)
    if u <= 0 or u >= 1: return
    rng = np.random.default_rng(7)
    for i in range(14):
        a = rng.uniform(math.pi, 2 * math.pi); r = 30 + 160 * u * rng.uniform(0.5, 1)
        px, py = x + math.cos(a) * r, y + math.sin(a) * r * 0.5 - 40 * u
        c.set_source_rgba(0.85, 0.78, 0.66, 0.35 * (1 - u)); c.arc(px, py, 18 + 30 * u * rng.uniform(0.5, 1), 0, 2 * math.pi); c.fill()


def bags(c, x, y, t, t0):
    u = e_back(prog(t, t0, t0 + 0.35))
    if u <= 0: return
    for k, (dx, col, lab) in enumerate(((-70, AMBER, ''), (10, TEAL, ''), (90, (0.85, 0.35, 0.45), ''))):
        c.save(); c.translate(x + dx, y); c.scale(u, u); c.rotate(math.radians(-6 + k * 6))
        c.set_source_rgb(*col); rrect(c, -45, -110, 90, 110, 8); c.fill_preserve(); c.set_source_rgb(*CH.OUT); c.set_line_width(4); c.stroke()
        c.set_line_width(5); c.arc(0, -110, 24, math.pi, 2 * math.pi); c.stroke(); c.restore()


def notebook(c, x, y, t, t0):
    u = e_back(prog(t, t0, t0 + 0.35))
    if u <= 0: return
    c.save(); c.translate(x, y); c.scale(u, u); c.rotate(-0.15)
    c.set_source_rgb(0.62, 0.12, 0.14); rrect(c, -70, -90, 140, 180, 8); c.fill_preserve(); c.set_source_rgb(*CH.OUT); c.set_line_width(4); c.stroke()
    c.set_source_rgb(*AMBER); c.rectangle(-70, -90, 18, 180); c.fill(); c.restore()
