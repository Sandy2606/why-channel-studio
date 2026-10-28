"""Three style directions, same three moments (hook, map, payoff). No red, no character eye."""
import sys, math, cairo, numpy as np
sys.argv = sys.argv[:1]
import render as R, host
from PIL import Image, ImageFilter
host._eye = lambda *a, **k: None   # plain logo glyph, no face
W, H = R.W, R.H
AMBER, CREAM, BLACK = R.AMBER, R.CREAM, R.BLACK
AMBER2 = (1.0, 0.52, 0.18)   # warm orange for gradients
INK = (0.08, 0.08, 0.09)

def surf():
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); return s, cairo.Context(s)

def amber_grad(c, x0, y0, x1, y1):
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgb(0, *AMBER); g.add_color_stop_rgb(1, *AMBER2); return g

def glass(c, name, x, y, w, h, r=28):
    """frosted card: paint the blurred photo fill clipped + light tint + hairline."""
    (fill, _), _, _ = R.photo(name)
    c.save(); R.rrect(c, x, y, w, h, r); c.clip()
    c.translate(W / 2, H / 2); c.translate(-fill.get_width() / 2, -fill.get_height() / 2)
    c.set_source_surface(fill, 0, 0); c.paint(); c.restore()
    c.save(); R.rrect(c, x, y, w, h, r); c.set_source_rgba(1, 1, 1, 0.12); c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(2); c.stroke(); c.restore()

def glass_dark(c, x, y, w, h, r=28):
    c.save(); R.rrect(c, x, y, w, h, r); c.set_source_rgba(0.08, 0.08, 0.1, 0.55); c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 0.22); c.set_line_width(2); c.stroke(); c.restore()

def glowdot(c, x, y, r=14, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 5); g.add_color_stop_rgba(0, *AMBER, 0.6 * a); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.arc(x, y, r * 5, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*AMBER, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1, 1, 1, 0.9 * a); c.arc(x, y, r * 0.4, 0, 2 * math.pi); c.fill()

def capA(c, words, act, y=1430, px=74, col=CREAM, actcol=AMBER, band=True):
    R.font(c, 'head', px); sp = c.text_extents(' ').x_advance
    ws = [c.text_extents(w).x_advance for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
    if tot > 920:
        px = int(px * 920 / tot); R.font(c, 'head', px); sp = c.text_extents(' ').x_advance
        ws = [c.text_extents(w).x_advance for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
    x = W / 2 - tot / 2
    for i, (w, wd) in enumerate(zip(words, ws)):
        c.move_to(x, y + px * 0.36); c.text_path(w)
        if band: c.set_source_rgba(0, 0, 0, 0.75); c.set_line_width(px * 0.14); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        if i == act and actcol == 'grad': c.set_source(amber_grad(c, x, 0, x + wd, 0))
        else: c.set_source_rgb(*(actcol if i == act else col))
        c.fill(); x += wd + sp

def label(c, txt, x, y, px=22, col=(1, 1, 1), a=0.8, anchor='l'):
    R.mono(c, txt, x, y, px, col, a=a, anchor=anchor, kind='mono')

def tagA(c):
    R.font(c, 'monob', 24); t = 'DUSSEHRA · 5/6'; e = c.text_extents(t)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7)
    c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(t)

# ====================== A. GLOW (dark glass + amber light guide) ======================
def A_hook():
    s, c = surf()
    R.draw_photo(c, 'mandsaur', 0.6, 0, 1, z=(1.02, 1.02), full=True, focus=(0.5, 0.42))
    g = cairo.LinearGradient(0, 1000, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(0.55, 0, 0, 0, 0.8); g.add_color_stop_rgba(1, 0, 0, 0, 0.92)
    c.set_source(g); c.paint()
    # measuring line with ticks, glowing
    x = 930; y0, y1 = 210, 1180
    c.set_source_rgba(*AMBER, 0.9); c.set_line_width(4); c.move_to(x, y0); c.line_to(x, y1); c.stroke()
    for k in range(8):
        yy = y0 + (y1 - y0) * k / 7; c.move_to(x - 16, yy); c.line_to(x, yy); c.stroke()
    glowdot(c, x, y0, 12)
    # 35 FT gradient numerals
    R.font(c, 'head', 230); t = '35 FT'; e = c.text_extents(t); tx = 70
    c.move_to(tx, 1290); c.text_path(t); c.set_source(amber_grad(c, tx, 1100, tx + e.width, 1300)); c.fill()
    label(c, 'SEATED · TEN HEADS · MANDSAUR, MP', 76, 1340, 24, CREAM, 0.9, 'l')
    # glass fact card
    glass(c, 'mandsaur', 70, 760, 760, 190, 30)
    label(c, 'WHEN WOMEN PASS IT', 110, 810, 24, AMBER, 1)
    R.head(c, 'THEY COVER THEIR HEADS', 110, 885, 46, CREAM, anchor='l', shadow=False)
    capA(c, ['JUST', 'LIKE', 'IN-LAWS'], 2, y=1480, actcol='grad')
    tagA(c); return s

def A_map():
    s, c = surf()
    p = R.PLACES['Mandsaur']; clon, clat, z = p[0] + 1.5, p[1] - 1.2, 95
    R.draw_map(c, clon, clat, z, 0)
    c.set_source_rgba(0.02, 0.03, 0.05, 0.35); c.paint()
    x, y = R.lonlat_xy(p[0], p[1], clon, clat, z)
    # halo
    for r, a in ((260, 0.05), (160, 0.08), (90, 0.12)):
        c.set_source_rgba(*AMBER, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    glowdot(c, x, y, 16)
    # place label: clean, no card
    R.head(c, 'MANDSAUR', x + 40, y - 30, 62, CREAM, anchor='l')
    label(c, 'MADHYA PRADESH  ·  24.07°N 75.07°E', x + 42, y + 26, 20, AMBER, 1)
    # connector line to glass photo
    c.set_source_rgba(*AMBER, 0.8); c.set_line_width(3); c.move_to(x, y); c.line_to(x + 60, y + 90); c.line_to(x + 60, 1040); c.stroke()
    px, py, pw, ph = 380, 1180, 600, 280
    c.save(); R.rrect(c, px, py - 140, pw, ph, 26); c.clip()
    (_, _), (sh, _), _ = R.photo('mandsaur2'); sc = max(pw / sh.get_width(), ph / sh.get_height())
    c.translate(px + pw / 2, py - 140 + ph / 2); c.scale(sc, sc); c.translate(-sh.get_width() / 2, -sh.get_height() / 2)
    c.set_source_surface(sh, 0, 0); c.paint(); c.restore()
    c.save(); R.rrect(c, px, py - 140, pw, ph, 26); c.set_source_rgba(1, 1, 1, 0.4); c.set_line_width(2); c.stroke(); c.restore()
    # top glass card
    glass_dark(c, 70, 230, 940, 270, 30)
    label(c, 'TRADITION SAYS', 110, 290, 22, AMBER, 1)
    R.head(c, "MANDODARI WAS", 110, 360, 58, CREAM, anchor='l', shadow=False)
    R.head(c, "FROM HERE", 110, 435, 58, CREAM, anchor='l', shadow=False)
    # relation tag: gradient pill with glow
    c.save(); c.translate(700, 560)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 260); g.add_color_stop_rgba(0, *AMBER, 0.35); g.add_color_stop_rgba(1, *AMBER, 0); c.set_source(g); c.arc(0, 0, 260, 0, 2 * math.pi); c.fill()
    R.font(c, 'head', 46); e = c.text_extents('= SON-IN-LAW'); w = e.width + 70
    R.rrect(c, -w / 2, -42, w, 84, 42); c.set_source(amber_grad(c, -w / 2, 0, w / 2, 0)); c.fill()
    c.move_to(-e.width / 2 - e.x_bearing, 17); c.set_source_rgb(*INK); c.show_text('= SON-IN-LAW'); c.restore()
    capA(c, ['RAVANA', 'THEIR', 'SON-IN-LAW'], 2, y=1470, actcol='grad')
    tagA(c); return s

def A_pay():
    s, c = surf()
    c.set_source_rgb(0.03, 0.03, 0.04); c.paint()
    g = cairo.RadialGradient(W / 2, 950, 0, W / 2, 950, 900); g.add_color_stop_rgba(0, *AMBER2, 0.32); g.add_color_stop_rgba(0.5, *AMBER, 0.08); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    c.set_source(g); c.paint()
    # light streaks
    for i in range(14):
        a = i / 14 * 2 * math.pi
        c.set_source_rgba(*AMBER, 0.05); c.set_line_width(40)
        c.move_to(W / 2, 950); c.line_to(W / 2 + math.cos(a) * 1400, 950 + math.sin(a) * 1400); c.stroke()
    host.draw(c, W / 2, 1150, 620, morph=1.0, glow=1.0, stroke=0.15)
    label(c, 'IN THESE PLACES, RAVANA IS', W / 2, 300, 28, CREAM, 0.85, 'c')
    R.font(c, 'head', 190); t = 'FAMILY'; e = c.text_extents(t); tx = W / 2 - e.width / 2 - e.x_bearing
    c.move_to(tx, 470); c.text_path(t); c.set_source(amber_grad(c, tx, 330, tx + e.width, 470)); c.fill()
    capA(c, ['RAVANA', 'IS', 'FAMILY.'], 2, y=1470, actcol='grad')
    tagA(c); return s

# ====================== B. PAPER (editorial, Johnny-Harris desk) ======================
PAPER = (0.957, 0.941, 0.906)
def paper(c):
    c.set_source_rgb(*PAPER); c.paint()
    rng = np.random.default_rng(7); n = rng.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
    a = np.zeros((H // 2, W // 2, 4), np.uint8); m = (n.astype(np.uint16) * 22 // 255).astype(np.uint8); a[..., 3] = m
    sf = cairo.ImageSurface.create_for_data(memoryview(a), cairo.FORMAT_ARGB32, W // 2, H // 2)
    c.save(); c.scale(2, 2); c.set_source_surface(sf, 0, 0); c.paint(); c.restore(); paper.keep = a
def highlighter(c, x, y, w, h=58):
    c.save(); c.set_source_rgba(*AMBER, 0.75)
    c.move_to(x - 8, y - h / 2 + 4); c.curve_to(x + w * 0.3, y - h / 2 - 3, x + w * 0.7, y - h / 2 + 6, x + w + 10, y - h / 2)
    c.line_to(x + w + 6, y + h / 2); c.curve_to(x + w * 0.6, y + h / 2 + 4, x + w * 0.3, y + h / 2 - 4, x - 4, y + h / 2 + 2); c.close_path(); c.fill(); c.restore()
def ink(c, txt, x, y, px, anchor='l', hl=False, col=INK):
    R.font(c, 'head', px); e = c.text_extents(txt)
    xx = x if anchor == 'l' else x - e.width / 2 - e.x_bearing
    if hl: highlighter(c, xx, y, e.width)
    c.move_to(xx, y + px * 0.36); c.set_source_rgb(*col); c.show_text(txt); return e.width
def print_photo(c, name, cx, cy, w, h, rot, tape=True, caption=None):
    (_, _), (sh, _), _ = R.photo(name)
    c.save(); c.translate(cx, cy); c.rotate(math.radians(rot))
    c.set_source_rgba(0, 0, 0, 0.22); c.rectangle(-w / 2 + 10, -h / 2 + 16, w, h + (60 if caption else 0)); c.fill()
    c.set_source_rgb(1, 1, 1); c.rectangle(-w / 2 - 14, -h / 2 - 14, w + 28, h + 28 + (60 if caption else 0)); c.fill()
    c.save(); c.rectangle(-w / 2, -h / 2, w, h); c.clip()
    sc = max(w / sh.get_width(), h / sh.get_height()); c.scale(sc, sc); c.translate(-sh.get_width() / 2, -sh.get_height() / 2)
    c.set_source_surface(sh, 0, 0); c.paint(); c.restore()
    if caption: R.mono(c, caption, 0, h / 2 + 32, 22, (0.25, 0.25, 0.25), kind='mono')
    if tape:
        for tx in (-w / 2 + 40, w / 2 - 40):
            c.save(); c.translate(tx, -h / 2 - 6); c.rotate(math.radians(-35 if tx < 0 else 35))
            c.set_source_rgba(0.93, 0.88, 0.72, 0.85); c.rectangle(-60, -18, 120, 36); c.fill(); c.restore()
    c.restore()
def tagB(c):
    R.font(c, 'monob', 24); t = 'DUSSEHRA · 5/6'
    c.move_to(48, 128); c.set_source_rgb(*INK); c.show_text(t)
    c.set_source_rgb(*AMBER); c.arc(40 - 12 + 0, 119, 0, 0, 0); c.fill()

def B_hook():
    s, c = surf(); paper(c)
    print_photo(c, 'mandsaur', W / 2 + 10, 720, 900, 700, -2.5, caption='MANDSAUR, MADHYA PRADESH')
    # hand-drawn measure
    c.set_source_rgb(*INK); c.set_line_width(5); c.move_to(60, 330); c.line_to(60, 1110); c.stroke()
    for yy in (330, 1110): c.move_to(40, yy); c.line_to(80, yy); c.stroke()
    c.save(); c.translate(120, 720); c.rotate(-math.pi / 2); ink(c, '35 FT TALL', 0, 0, 64, 'c', hl=True); c.restore()
    ink(c, 'WOMEN COVER', 90, 1290, 72)
    ink(c, 'THEIR HEADS', 90, 1380, 72, hl=True)
    capA(c, ['JUST', 'LIKE', 'IN-LAWS'], 2, y=1520, px=60, col=INK, actcol=(0.75, 0.45, 0.0), band=False)
    tagB(c); return s

def B_map():
    s, c = surf(); paper(c)
    p = R.PLACES['Mandsaur']; clon, clat, z = p[0] + 1.0, p[1] - 0.8, 80
    # printed map: pale ocean with hatch, land paper
    c.save(); c.rectangle(60, 200, W - 120, 1150); c.clip()
    c.set_source_rgb(0.80, 0.85, 0.87); c.paint()
    c.set_source_rgba(0.55, 0.65, 0.70, 0.35); c.set_line_width(1.5)
    for k in range(-60, 120): c.move_to(k * 22, 200); c.line_to(k * 22 + 900, 1400); c.stroke()
    c.translate(W / 2, H / 2); c.scale(z * R.KX, -z); c.translate(-clon, -clat)
    for r in R.POLYS:
        c.move_to(*r[0])
        for q in r[1:]: c.line_to(*q)
        c.close_path()
    c.restore()
    c.save(); c.rectangle(60, 200, W - 120, 1150); c.clip(); c.set_source_rgb(0.93, 0.90, 0.83); c.fill_preserve()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(3); c.rectangle(60, 200, W - 120, 1150); c.stroke()
    R.font(c, 'mono', 22)
    for nm, lo, la in R.REFS:
        x, y = R.lonlat_xy(lo, la, clon, clat, z)
        if 80 < x < W - 160 and 220 < y < 1330:
            c.set_source_rgb(*INK); c.arc(x, y, 4, 0, 2 * math.pi); c.fill(); c.move_to(x + 10, y + 7); c.show_text(nm.title())
    x, y = R.lonlat_xy(p[0], p[1], clon, clat, z)
    c.set_source_rgb(*INK); c.arc(x, y, 12, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*AMBER, 1); c.set_line_width(7); c.arc(x, y, 46, 0, 2 * math.pi); c.stroke()
    ink(c, 'Mandsaur', x - 60, y - 90, 60, 'l')
    print_photo(c, 'mandsaur2', 760, 1060, 380, 280, 5, caption='THE STATUE')
    ink(c, "MANDODARI'S", 80, 1440, 64)
    ink(c, 'HOMETOWN.', 80, 1525, 64, hl=True)
    tagB(c); return s

def B_pay():
    s, c = surf(); paper(c)
    host.draw(c, W / 2, 1330, 520, morph=1.0, glow=0.0, color=INK)
    ink(c, 'IN THESE PLACES,', W / 2, 300, 60, 'c')
    ink(c, 'RAVANA IS', W / 2, 390, 60, 'c')
    ink(c, 'FAMILY.', W / 2, 520, 150, 'c', hl=True)
    tagB(c); return s

# ====================== C. KINETIC (type-as-window) ======================
def knock(c, name, txt, cx, cy, px, focus=(0.5, 0.5)):
    R.font(c, 'head', px); e = c.text_extents(txt)
    c.save(); c.move_to(cx - e.width / 2 - e.x_bearing, cy + px * 0.36); c.text_path(txt); c.clip()
    (_, _), (sh, _), _ = R.photo(name); sc = max(W / sh.get_width(), H * 0.9 / sh.get_height())
    c.translate(W / 2, cy); c.scale(sc, sc); c.translate(-sh.get_width() * focus[0], -sh.get_height() * focus[1])
    c.set_source_surface(sh, 0, 0); c.paint(); c.restore()
def C_hook():
    s, c = surf(); c.set_source_rgb(0.03, 0.03, 0.04); c.paint()
    knock(c, 'mandsaur', '35', W / 2, 560, 720, focus=(0.5, 0.35))
    R.head(c, 'FEET OF RAVANA', W / 2, 1000, 84, CREAM, shadow=False)
    c.set_source_rgba(*AMBER, 1); c.rectangle(W / 2 - 60, 1080, 120, 8); c.fill()
    R.head(c, 'AND WOMEN COVER', W / 2, 1180, 64, (0.6, 0.6, 0.6), shadow=False)
    R.head(c, 'THEIR HEADS', W / 2, 1260, 64, AMBER, shadow=False)
    capA(c, ['JUST', 'LIKE', 'IN-LAWS'], 2, y=1440, actcol=AMBER)
    R.tag(c); return s
def C_map():
    s, c = surf()
    p = R.PLACES['Mandsaur']; R.draw_map(c, p[0], p[1] - 0.5, 70, 0); c.set_source_rgba(0, 0, 0, 0.55); c.paint()
    x, y = R.lonlat_xy(p[0], p[1], p[0], p[1] - 0.5, 70)
    for r, a in ((120, 0.10), (60, 0.2)): c.set_source_rgba(*AMBER, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*AMBER); c.arc(x, y, 16, 0, 2 * math.pi); c.fill()
    R.head(c, 'MANDODARI\'S HOMETOWN', W / 2, 330, 46, CREAM, shadow=False)
    knock(c, 'mandsaur2', 'SON-IN', W / 2, 560, 250, focus=(0.5, 0.45))
    knock(c, 'mandsaur2', '-LAW', W / 2, 780, 250, focus=(0.5, 0.6))
    R.head(c, 'MANDSAUR · MP', x, y + 80, 40, AMBER, shadow=False)
    capA(c, ['RAVANA', 'THEIR', 'SON-IN-LAW'], 2, y=1440, actcol=AMBER)
    R.tag(c); return s
def C_map_old():
    s, c = surf(); c.set_source_rgb(0.03, 0.03, 0.04); c.paint()
    p = R.PLACES['Mandsaur']; clon, clat, z = 79.0, 22.0, 52
    # India landmass as a window onto the statue photo
    c.save(); c.translate(W / 2, H / 2 - 120); c.scale(z * R.KX, -z); c.translate(-clon, -clat)
    for r in R.POLYS:
        xs = r[:, 0]
        if xs.min() < 66 or xs.max() > 98: continue
        c.move_to(*r[0])
        for q in r[1:]: c.line_to(*q)
        c.close_path()
    c.restore(); c.save(); c.clip()
    (_, _), (sh, _), _ = R.photo('mandsaur2'); sc = H / sh.get_height()
    c.translate(W / 2, H / 2 - 200); c.scale(sc, sc); c.translate(-sh.get_width() / 2, -sh.get_height() / 2); c.set_source_surface(sh, 0, 0); c.paint()
    c.restore()
    x, y = R.lonlat_xy(p[0], p[1], clon, clat, z); y -= 120
    c.set_source_rgb(*AMBER); c.arc(x, y, 18, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*AMBER, 1); c.set_line_width(4); c.move_to(x, y); c.line_to(80, 300); c.stroke()
    R.head(c, 'MANDSAUR', 80, 260, 72, CREAM, anchor='l', shadow=False)
    R.head(c, 'SON-IN-LAW', W / 2, 1290, 120, AMBER, shadow=False)
    R.head(c, "MANDODARI'S HOMETOWN", W / 2, 1170, 48, CREAM, shadow=False)
    capA(c, ['RAVANA', 'THEIR', 'SON-IN-LAW'], 2, y=1440, actcol=AMBER)
    R.tag(c); return s
def C_pay():
    s, c = surf(); c.set_source_rgb(0.03, 0.03, 0.04); c.paint()
    R.head(c, 'IN THESE PLACES, RAVANA IS', W / 2, 330, 40, (0.65, 0.65, 0.65), shadow=False)
    knock(c, 'mandsaur', 'FAMILY', W / 2, 640, 250, focus=(0.5, 0.4))
    host.draw(c, W / 2, 1250, 420, morph=1.0, glow=0.8)
    capA(c, ['RAVANA', 'IS', 'FAMILY.'], 2, y=1450, actcol=AMBER)
    R.tag(c); return s

if __name__ == '__main__':
    R.voice_env()
    rows = {'A · GLOW': (A_hook, A_map, A_pay), 'B · PAPER': (B_hook, B_map, B_pay), 'C · KINETIC': (C_hook, C_map, C_pay)}
    for k, fs in rows.items():
        for i, f in enumerate(fs):
            f().write_to_png(f'/home/claude/rv/sb_{k[0]}{i}.png')
    print('ok')
