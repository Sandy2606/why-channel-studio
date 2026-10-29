"""Animated subscribe / follow CTA card (YT + IG), cursor clicks, real UI SFX.

draw(c, t, t0, plat, lang, y=1180)  -> paints the card on a cairo context (1080 wide)
events(t0, plat)                    -> [(sfx_name, time, gain)] for the mixer
t0 = start of the CTA voice line ("If you like learning things like this, subscribe/follow ...").
"""
import math, os, cairo
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
W = 1080
ACC = {
    ('en', 'yt'): ('Why?', '@WhyEveryQuestionHasAStory', 'why_profile_2160.png'),
    ('te', 'yt'): ('why?telugu', '@WhyTeluguStories', 'why_telugu_profile_2160.png'),
    ('en', 'ig'): ('Why?', 'why_everyquestionhasastory', 'why_profile_2160.png'),
    ('te', 'ig'): ('Why? Telugu', 'whytelugu', 'why_telugu_profile_2160.png'),
}
# timeline (s after t0)
T_IN, T_CLICK, T_BELL = 0.0, 1.05, 2.05

def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / max(1e-6, b - a))
def e_out(x): return 1 - (1 - x) ** 3
def e_io(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def e_back(x, s=1.7): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

def rrect(c, x, y, w, h, r):
    r = min(r, h / 2, w / 2)
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()

def ui(c, px, bold=True):
    c.select_font_face('Inter', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL); c.set_font_size(px)

_AV = {}
def avatar(c, name, cx, cy, r):
    if name not in _AV:
        im = Image.open(os.path.join(REPO, 'brand', 'avatars', name)).convert('RGBA').resize((int(r * 2 * 1.5),) * 2, Image.LANCZOS)
        b = bytearray(im.tobytes('raw', 'BGRa')); s = cairo.ImageSurface.create_for_data(b, cairo.FORMAT_ARGB32, im.width, im.height)
        _AV[name] = (s, b)
    s = _AV[name][0]; sc = 2 * r / s.get_width()
    c.save(); c.arc(cx, cy, r, 0, 2 * math.pi); c.clip(); c.translate(cx - r, cy - r); c.scale(sc, sc); c.set_source_surface(s, 0, 0); c.paint(); c.restore()

def cursor(c, x, y, press=0.0, a=1.0):
    s = 1.0 - 0.12 * press
    c.save(); c.translate(x, y); c.scale(s * 1.6, s * 1.6)
    pts = [(0, 0), (0, 34), (8, 26), (14, 40), (20, 37), (14, 24), (25, 24)]
    c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path()
    c.set_source_rgba(0, 0, 0, 0.35 * a); c.save(); c.translate(2, 3); c.restore()
    c.set_source_rgba(1, 1, 1, a); c.fill_preserve(); c.set_line_width(2.2); c.set_source_rgba(0, 0, 0, a); c.stroke()
    c.restore()

def ripple(c, x, y, t, tc):
    u = prog(t, tc, tc + 0.45)
    if 0 < u < 1:
        c.set_source_rgba(1, 1, 1, 0.45 * (1 - u)); c.set_line_width(4); c.arc(x, y, 18 + 60 * e_out(u), 0, 2 * math.pi); c.stroke()

def bell_icon(c, x, y, s, ring=0.0, filled=False, col=(1, 1, 1)):
    c.save(); c.translate(x, y); c.rotate(math.radians(18 * math.sin(ring * math.pi * 6) * (1 - ring))); c.scale(s, s)
    c.move_to(-14, 8); c.curve_to(-14, -16, -10, -20, 0, -20); c.curve_to(10, -20, 14, -16, 14, 8); c.line_to(18, 12); c.line_to(-18, 12); c.close_path()
    c.set_source_rgb(*col)
    if filled: c.fill()
    else: c.set_line_width(3.2); c.stroke()
    c.arc(0, 16, 4.5, 0, 2 * math.pi); c.fill()
    if filled and ring > 0:
        c.set_line_width(3); a = 1 - ring
        for sgn in (-1, 1):
            c.set_source_rgba(*col, a); c.arc(0, -4, 26 + 8 * ring, math.radians(-90 + sgn * 35) - 0.35, math.radians(-90 + sgn * 35) + 0.35); c.stroke()
    c.restore()

def check(c, x, y, s, u, col=(1, 1, 1)):
    if u <= 0: return
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_width(4); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgb(*col); p = [(-9, 0), (-3, 7), (10, -8)]
    L1 = math.dist(p[0], p[1]); L2 = math.dist(p[1], p[2]); d = u * (L1 + L2)
    c.move_to(*p[0])
    if d <= L1: f = d / L1; c.line_to(p[0][0] + (p[1][0] - p[0][0]) * f, p[0][1] + (p[1][1] - p[0][1]) * f)
    else: c.line_to(*p[1]); f = (d - L1) / L2; c.line_to(p[1][0] + (p[2][0] - p[1][0]) * f, p[1][1] + (p[2][1] - p[1][1]) * f)
    c.stroke(); c.restore()

def draw(c, t, t0, plat, lang, y=1180, t_out=None):
    tt = t - t0
    if tt < 0: return
    name, handle, av = ACC[(lang, plat)]
    u = e_back(prog(tt, T_IN, T_IN + 0.4)); a = clamp(prog(tt, T_IN, T_IN + 0.2))
    if t_out is not None and t >= t_out:
        v = prog(t, t_out, t_out + 0.3); a *= 1 - v; u *= 1 - 0.15 * v
        if a <= 0.01: return
    cw, ch = 900, 200; x0 = (W - cw) / 2; y0 = y - ch / 2
    c.save(); c.translate(W / 2, y + (1 - min(1, u)) * 80); c.scale(0.9 + 0.1 * min(1.05, u), 0.9 + 0.1 * min(1.05, u)); c.translate(-W / 2, -y)
    c.push_group()
    # card
    c.set_source_rgba(0, 0, 0, 0.45); rrect(c, x0 + 6, y0 + 14, cw, ch, 40); c.fill()
    c.set_source_rgb(0.09, 0.09, 0.095); rrect(c, x0, y0, cw, ch, 40); c.fill()
    c.set_source_rgba(1, 1, 1, 0.08); c.set_line_width(2); rrect(c, x0, y0, cw, ch, 40); c.stroke()
    ax, ay, ar = x0 + 104, y, 66
    if plat == 'ig':  # story ring
        g = cairo.LinearGradient(ax - ar, ay + ar, ax + ar, ay - ar)
        for s_, col in ((0, (1.0, 0.78, 0.2)), (0.5, (0.98, 0.33, 0.4)), (1, (0.75, 0.2, 0.8))): g.add_color_stop_rgb(s_, *col)
        c.set_source(g); c.arc(ax, ay, ar + 9, 0, 2 * math.pi); c.fill(); c.set_source_rgb(0.09, 0.09, 0.095); c.arc(ax, ay, ar + 4, 0, 2 * math.pi); c.fill()
    avatar(c, av, ax, ay, ar)
    tx = x0 + 196
    ui(c, 44); c.set_source_rgb(1, 1, 1); c.move_to(tx, y - 8); c.show_text(name)
    ui(c, 26, bold=False); e = c.text_extents(handle); hs = min(1.0, 330 / max(1, e.x_advance))
    c.save(); c.move_to(tx, y + 36); c.set_font_size(26 * hs); c.set_source_rgb(0.67, 0.67, 0.69); c.show_text(handle); c.restore()
    # button
    clicked = tt >= T_CLICK + 0.05
    bw, bh = (250, 84) if plat == 'yt' else (240, 84); bx = x0 + cw - bw - 36; by = y - bh / 2
    press = 1 - abs(prog(tt, T_CLICK - 0.06, T_CLICK + 0.14) * 2 - 1) if T_CLICK - 0.06 < tt < T_CLICK + 0.14 else 0
    c.save(); c.translate(bx + bw / 2, y); c.scale(1 - 0.06 * press, 1 - 0.06 * press); c.translate(-(bx + bw / 2), -y)
    if plat == 'yt':
        if not clicked:
            c.set_source_rgb(0.95, 0.95, 0.95); rrect(c, bx, by, bw, bh, 42); c.fill()
            ui(c, 32); e = c.text_extents('Subscribe'); c.set_source_rgb(0.06, 0.06, 0.06); c.move_to(bx + bw / 2 - e.x_advance / 2, y + 11); c.show_text('Subscribe')
        else:
            c.set_source_rgb(0.2, 0.2, 0.21); rrect(c, bx, by, bw, bh, 42); c.fill()
            ring = prog(tt, T_BELL, T_BELL + 0.9)
            bell_icon(c, bx + 44, y - 2, 0.95, ring=ring, filled=tt >= T_BELL, col=(1, 1, 1))
            ui(c, 28); c.set_source_rgb(1, 1, 1); c.move_to(bx + 78, y + 10); c.show_text('Subscribed')
    else:
        if not clicked:
            c.set_source_rgb(0.0, 0.584, 0.965); rrect(c, bx, by, bw, bh, 20); c.fill()
            ui(c, 32); e = c.text_extents('Follow'); c.set_source_rgb(1, 1, 1); c.move_to(bx + bw / 2 - e.x_advance / 2, y + 11); c.show_text('Follow')
        else:
            c.set_source_rgb(0.2, 0.2, 0.21); rrect(c, bx, by, bw, bh, 20); c.fill()
            ui(c, 30); e = c.text_extents('Following'); c.set_source_rgb(1, 1, 1); c.move_to(bx + bw / 2 - e.x_advance / 2 + 16, y + 10); c.show_text('Following')
            check(c, bx + bw / 2 - e.x_advance / 2 - 14, y - 1, 1.0, e_out(prog(tt, T_CLICK + 0.1, T_CLICK + 0.35)))
    c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
    # toast under card after bell (YT) / after follow (IG)
    tt2 = T_BELL + 0.1 if plat == 'yt' else T_CLICK + 0.35
    if tt >= tt2:
        v = e_back(prog(tt, tt2, tt2 + 0.3)) * a
        msg = 'All notifications on' if plat == 'yt' else "You're following"
        ui(c, 26); e = c.text_extents(msg); w = e.x_advance + 110; px = W / 2 - w / 2; py = y0 + ch + 34
        c.save(); c.translate(W / 2, py + 30); c.scale(max(0.01, v), max(0.01, v)); c.translate(-W / 2, -(py + 30))
        c.set_source_rgba(0.09, 0.09, 0.095, 0.95); rrect(c, px, py, w, 60, 30); c.fill()
        c.set_source_rgb(1.0, 0.70, 0.14); c.arc(px + 40, py + 30, 15, 0, 2 * math.pi); c.fill()
        check(c, px + 40, py + 30, 0.75, 1.0, col=(0.05, 0.05, 0.05))
        c.set_source_rgb(1, 1, 1); c.move_to(px + 70, py + 39); c.show_text(msg); c.restore()
    # cursor path
    btn = (bx + bw * 0.55, y + 12); bell = (bx + 44, y + 6); start = (W + 60, y + 330)
    if tt < T_CLICK:
        k = e_io(prog(tt, 0.25, T_CLICK - 0.05)); p = (start[0] + (btn[0] - start[0]) * k, start[1] + (btn[1] - start[1]) * k + math.sin(k * math.pi) * -40)
    elif plat == 'yt' and tt < T_BELL:
        k = e_io(prog(tt, T_CLICK + 0.35, T_BELL - 0.05)); p = (btn[0] + (bell[0] - btn[0]) * k, btn[1] + (bell[1] - btn[1]) * k)
    else:
        last = bell if plat == 'yt' else btn; tc = T_BELL if plat == 'yt' else T_CLICK
        k = e_io(prog(tt, tc + 0.5, tc + 1.1)); p = (last[0] + 90 * k, last[1] + 160 * k)
    tc_list = [T_CLICK] + ([T_BELL] if plat == 'yt' else [])
    for tc in tc_list: ripple(c, p[0], p[1], tt, tc)
    pr = max([1 - abs(prog(tt, tc - 0.06, tc + 0.14) * 2 - 1) if tc - 0.06 < tt < tc + 0.14 else 0 for tc in tc_list])
    ca = clamp(prog(tt, 0.25, 0.45)) * (1 - prog(tt, (T_BELL if plat == 'yt' else T_CLICK) + 1.0, (T_BELL if plat == 'yt' else T_CLICK) + 1.3)) * a
    if ca > 0: cursor(c, p[0], p[1], pr, ca)

def events(t0, plat):
    ev = [('woosh_air', t0 - 0.1, 0.22), ('ui_click', t0 + T_CLICK - 0.02, 0.9), ('ui_pop', t0 + T_CLICK + 0.1, 0.5)]
    if plat == 'yt': ev += [('ui_click', t0 + T_BELL - 0.02, 0.9), ('ui_bell', t0 + T_BELL + 0.03, 0.45)]
    return ev
