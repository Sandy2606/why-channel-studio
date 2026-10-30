"""Anna & Chelli v2 — detailed 2D (Pixar-ish proportions, outlines, soft shading). Cairo."""
import math, cairo
OUT = (0.17, 0.10, 0.07); OW = 5
SKIN = (0.76, 0.53, 0.37); SKIN_L = (0.86, 0.64, 0.47); SKIN_D = (0.62, 0.40, 0.27)
HAIR = (0.11, 0.07, 0.06); HAIR_L = (0.30, 0.19, 0.13)
CREAM = (0.957, 0.945, 0.918); AMBER = (1.0, 0.698, 0.141); INK = (0.08, 0.05, 0.04)
KURTA = (0.93, 0.63, 0.22); KURTA_D = (0.78, 0.48, 0.14); PANT = (0.93, 0.89, 0.80); PANT_D = (0.78, 0.73, 0.64)
TEAL = (0.15, 0.55, 0.55); TEAL_D = (0.09, 0.39, 0.40); DUP = (1.0, 0.76, 0.30); DUP_D = (0.86, 0.58, 0.16)

def vgrad(y0, y1, c0, c1):
    g = cairo.LinearGradient(0, y0, 0, y1); g.add_color_stop_rgb(0, *c0); g.add_color_stop_rgb(1, *c1); return g

def paint(c, src, outline=True, w=OW):
    if isinstance(src, tuple): c.set_source_rgb(*src)
    else: c.set_source(src)
    if outline:
        c.fill_preserve(); c.set_source_rgb(*OUT); c.set_line_width(w); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    else: c.fill()

def blob(c, pts):
    """smooth closed shape through points (Catmull-Rom)."""
    n = len(pts); c.move_to(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6, p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6, *p2)
    c.close_path()

def limb(c, x0, y0, x1, y1, w, col, col_d):
    ang = math.atan2(y1 - y0, x1 - x0); nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
    c.move_to(x0 + nx, y0 + ny); c.line_to(x1 + nx * 0.85, y1 + ny * 0.85); c.line_to(x1 - nx * 0.85, y1 - ny * 0.85); c.line_to(x0 - nx, y0 - ny); c.close_path()
    g = cairo.LinearGradient(x0 + nx, y0 + ny, x0 - nx, y0 - ny); g.add_color_stop_rgb(0, *col); g.add_color_stop_rgb(1, *col_d); paint(c, g)

def hand(c, x, y, r):
    c.arc(x, y, r, 0, 2 * math.pi); g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, 0, x, y, r); g.add_color_stop_rgb(0, *SKIN_L); g.add_color_stop_rgb(1, *SKIN); paint(c, g)
    c.arc(x + r * 0.55, y - r * 0.35, r * 0.38, 0, 2 * math.pi); paint(c, SKIN)

def face(c, r, blink, look, talk, smile, brow_lift, lashes=False, iris=(0.33, 0.20, 0.11)):
    # head
    c.arc(0, 0, r, 0, 2 * math.pi)
    g = cairo.RadialGradient(-r * 0.3, -r * 0.35, r * 0.1, 0, 0, r * 1.05); g.add_color_stop_rgb(0, *SKIN_L); g.add_color_stop_rgb(0.7, *SKIN); g.add_color_stop_rgb(1, *SKIN_D); paint(c, g)
    # cheeks
    for d in (-1, 1):
        gg = cairo.RadialGradient(d * r * 0.52, r * 0.28, 0, d * r * 0.52, r * 0.28, r * 0.25); gg.add_color_stop_rgba(0, 0.90, 0.45, 0.40, 0.35); gg.add_color_stop_rgba(1, 0.90, 0.45, 0.40, 0)
        c.set_source(gg); c.arc(d * r * 0.52, r * 0.28, r * 0.25, 0, 2 * math.pi); c.fill()
    # eyes
    ex, ey, ew, eh = r * 0.36, -r * 0.02, r * 0.21, r * 0.25
    for d in (-1, 1):
        cx = d * ex; open_ = max(0.06, 1 - blink)
        c.save(); c.translate(cx, ey); c.scale(1, open_)
        c.save(); c.scale(ew / eh, 1); c.arc(0, 0, eh, 0, 2 * math.pi); c.restore(); paint(c, (1, 1, 1), w=4)
        ix, iy = look[0] * ew * 0.35, look[1] * eh * 0.25
        c.arc(ix, iy + eh * 0.08, eh * 0.66, 0, 2 * math.pi); gi = cairo.RadialGradient(ix, iy, 0, ix, iy + eh * 0.08, eh * 0.66); gi.add_color_stop_rgb(0, 0.55, 0.36, 0.20); gi.add_color_stop_rgb(1, *iris); c.set_source(gi); c.fill()
        c.arc(ix, iy + eh * 0.1, eh * 0.33, 0, 2 * math.pi); c.set_source_rgb(*INK); c.fill()
        c.arc(ix + eh * 0.25, iy - eh * 0.18, eh * 0.17, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
        c.arc(ix - eh * 0.2, iy + eh * 0.3, eh * 0.08, 0, 2 * math.pi); c.fill()
        c.restore()
        # upper lid line + lashes
        c.set_source_rgb(*OUT); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.save(); c.translate(cx, ey); c.scale(1, open_); c.arc(0, 0, eh * 1.0, math.pi * 1.1, math.pi * 1.9); c.restore(); c.stroke()
        if lashes:
            for k in range(3):
                a = math.pi * (1.65 + 0.12 * k) if d > 0 else math.pi * (1.35 - 0.12 * k)
                px, py = cx + math.cos(a) * ew, ey + math.sin(a) * eh * open_
                c.move_to(px, py); c.line_to(px + math.cos(a) * 12, py + math.sin(a) * 12); c.stroke()
        # brow
        c.set_line_width(9); c.set_source_rgb(*HAIR)
        by = ey - eh * 1.45 - brow_lift * 10
        c.move_to(cx - d * ew * 0.9, by + 6); c.curve_to(cx - d * ew * 0.3, by - 6, cx + d * ew * 0.4, by - 6, cx + d * ew * 1.0, by + 2); c.stroke()
    # nose
    c.set_line_width(5); c.set_source_rgba(*SKIN_D, 1); c.move_to(r * 0.02, r * 0.14); c.curve_to(-r * 0.07, r * 0.30, r * 0.05, r * 0.33, r * 0.1, r * 0.28); c.stroke()
    # mouth
    my = r * 0.52; mw = r * 0.36
    if talk > 0.08:
        c.save(); c.translate(0, my - 4); c.move_to(-mw / 2, 0); c.curve_to(-mw / 3, mw * (0.3 + talk * 0.6), mw / 3, mw * (0.3 + talk * 0.6), mw / 2, 0); c.curve_to(mw / 4, -4, -mw / 4, -4, -mw / 2, 0); c.close_path()
        paint(c, (0.42, 0.12, 0.12), w=4)
        c.move_to(-mw / 3, 2); c.curve_to(-mw / 6, 10, mw / 6, 10, mw / 3, 2); c.set_source_rgb(1, 1, 1); c.set_line_width(6); c.stroke()
        c.arc(0, mw * (0.22 + talk * 0.45), mw * 0.18, 0, math.pi); c.set_source_rgb(0.85, 0.45, 0.45); c.fill(); c.restore()
    else:
        c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgb(*OUT)
        c.move_to(-mw / 2, my); c.curve_to(-mw / 4, my + 18 * smile, mw / 4, my + 18 * smile, mw / 2, my); c.stroke()

def ears(c, r, earring=False):
    for d in (-1, 1):
        c.save(); c.translate(d * r * 0.97, r * 0.05); c.scale(0.6, 1); c.arc(0, 0, r * 0.18, 0, 2 * math.pi); c.restore(); paint(c, SKIN, w=4)
        if earring:
            c.arc(d * r * 0.98, r * 0.28, 9, 0, 2 * math.pi); paint(c, AMBER, w=3)
            c.arc(d * r * 0.98, r * 0.40, 6, 0, 2 * math.pi); paint(c, AMBER, w=3)

def backglow(c, x, y, s):
    g = cairo.RadialGradient(x, y - 560 * s, 0, x, y - 560 * s, 560 * s); g.add_color_stop_rgba(0, 1.0, 0.70, 0.30, 0.16); g.add_color_stop_rgba(1, 1.0, 0.70, 0.30, 0)
    c.set_source(g); c.arc(x, y - 560 * s, 560 * s, 0, 2 * math.pi); c.fill()

def shadow(c):
    c.save(); c.scale(1, 0.16); c.arc(0, 0, 150, 0, 2 * math.pi); c.restore(); c.set_source_rgba(0, 0, 0, 0.4); c.fill()

def anna(c, x, y, s=1.0, t=0.0, talk=0.0, blink=0.0, gesture=0.0, look=(0, 0), tilt=0.0):
    backglow(c, x, y, s)
    c.save(); c.translate(x, y); c.scale(s, s); shadow(c)
    breath = math.sin(t * 2.0); c.translate(0, breath * 2)
    # legs (pyjama) + feet
    for d in (-1, 1):
        c.move_to(d * 12, -300); c.line_to(d * 70, -300); c.line_to(d * 62, -30); c.line_to(d * 18, -30); c.close_path(); paint(c, vgrad(-300, -30, PANT, PANT_D))
        c.save(); c.translate(d * 46, -16); c.scale(1.5, 0.7); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore(); paint(c, (0.36, 0.22, 0.14))
    # kurta
    c.move_to(-110, -560); c.curve_to(-135, -470, -140, -330, -128, -250); c.line_to(128, -250); c.curve_to(140, -330, 135, -470, 110, -560); c.curve_to(60, -585, -60, -585, -110, -560); c.close_path()
    paint(c, vgrad(-585, -250, KURTA, KURTA_D))
    c.set_source_rgba(*KURTA_D, 0.8); c.set_line_width(4)
    for fx in (-60, 55): c.move_to(fx, -420); c.curve_to(fx + 8, -360, fx - 6, -300, fx + 4, -262); c.stroke()
    # placket
    c.move_to(-16, -585); c.line_to(16, -585); c.line_to(10, -470); c.line_to(-10, -470); c.close_path(); paint(c, KURTA_D, w=3)
    for yy in (-560, -530, -500): c.arc(0, yy, 5, 0, 2 * math.pi); paint(c, CREAM, w=2)
    # arms
    lx1, ly1 = -150, -330
    limb(c, -105, -545, lx1, ly1, 46, KURTA, KURTA_D); hand(c, lx1 - 2, ly1 + 14, 24)
    rx1, ry1 = 150 + 50 * gesture, -330 - 250 * gesture
    limb(c, 105, -545, rx1, ry1, 46, KURTA, KURTA_D); hand(c, rx1 + 2, ry1 - 8 * gesture + 14 * (1 - gesture), 24)
    # neck
    c.move_to(-26, -600); c.line_to(26, -600); c.line_to(22, -565); c.line_to(-22, -565); c.close_path(); paint(c, SKIN_D, w=4)
    # head
    hr = 150; c.save(); c.translate(0, -735); c.rotate(math.radians(tilt + 2 * math.sin(t * 1.3)))
    # hair back
    blob(c, [(-150, 10), (-160, -90), (-110, -165), (-20, -190), (80, -180), (150, -120), (155, -10)]); paint(c, HAIR)
    ears(c, hr)
    face(c, hr, blink, look, talk, 0.7, 0.3 * gesture)
    # hair front (side-swept fringe)
    blob(c, [(-150, -40), (-140, -120), (-70, -175), (30, -182), (120, -150), (152, -70), (120, -95), (60, -118), (0, -108), (-60, -120), (-115, -85)]); paint(c, vgrad(-185, -40, HAIR_L, HAIR))
    c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(5); c.move_to(-40, -160); c.curve_to(0, -172, 50, -168, 90, -150); c.stroke()
    c.restore(); c.restore()

def chelli(c, x, y, s=1.0, t=0.0, talk=0.0, blink=0.0, gesture=0.0, look=(0, 0), tilt=0.0, q=1.0, qpop=0.0, qdraw=None):
    backglow(c, x, y, s)
    c.save(); c.translate(x, y); c.scale(s, s); shadow(c)
    breath = math.sin(t * 2.3 + 1); c.translate(0, breath * 2)
    # langa (long skirt) with border
    c.move_to(-85, -300); c.curve_to(-110, -200, -130, -80, -135, -12); c.curve_to(-40, 2, 40, 2, 135, -12); c.curve_to(130, -80, 110, -200, 85, -300); c.close_path()
    paint(c, vgrad(-300, -12, TEAL, TEAL_D))
    c.set_source_rgb(*AMBER); c.set_line_width(14); c.move_to(-132, -40); c.curve_to(-40, -28, 40, -28, 132, -40); c.stroke()
    c.set_source_rgba(*TEAL_D, 0.9); c.set_line_width(4)
    for fx in (-50, 0, 50): c.move_to(fx * 0.6, -280); c.curve_to(fx * 0.8, -180, fx * 1.1, -100, fx * 1.4, -50); c.stroke()
    for d in (-1, 1): c.save(); c.translate(d * 40, -6); c.scale(1.4, 0.6); c.arc(0, 0, 22, 0, 2 * math.pi); c.restore(); paint(c, (0.55, 0.30, 0.15))
    # blouse
    c.move_to(-88, -500); c.curve_to(-100, -430, -96, -350, -86, -295); c.line_to(86, -295); c.curve_to(96, -350, 100, -430, 88, -500); c.curve_to(45, -520, -45, -520, -88, -500); c.close_path()
    paint(c, vgrad(-520, -295, TEAL, TEAL_D))
    # dupatta (half-saree drape)
    c.move_to(-80, -505); c.curve_to(-40, -520, -10, -512, 10, -500); c.line_to(105, -300); c.curve_to(80, -280, 50, -280, 40, -295); c.close_path(); paint(c, vgrad(-520, -280, DUP, DUP_D))
    c.set_source_rgb(*DUP_D); c.set_line_width(3)
    for k in range(3): c.move_to(-40 + k * 14, -508); c.line_to(55 + k * 14, -300); c.stroke()
    # arms
    limb(c, -82, -490, -122, -310, 38, TEAL, TEAL_D); hand(c, -124, -296, 20)
    rx1, ry1 = 122 + 40 * gesture, -310 - 230 * gesture
    limb(c, 82, -490, rx1, ry1, 38, TEAL, TEAL_D); hand(c, rx1 + 2, ry1 + 10 * (1 - gesture), 20)
    c.set_source_rgb(*AMBER); c.set_line_width(6)
    for d, (hx, hy) in ((-1, (-124, -296)), (1, (rx1, ry1))): c.arc(hx, hy - 22, 14, math.pi * 0.9, math.pi * 2.1); c.stroke()  # bangles
    c.move_to(-22, -540); c.line_to(22, -540); c.line_to(18, -505); c.line_to(-18, -505); c.close_path(); paint(c, SKIN_D, w=4)
    hr = 132; c.save(); c.translate(0, -660); c.rotate(math.radians(tilt + 2.5 * math.sin(t * 1.5 + 0.5)))
    # ponytail + back hair
    sw = 8 * math.sin(t * 2.5)
    blob(c, [(90, -60), (175, -20), (195, 80 + sw), (170, 190 + sw), (140, 120), (120, 20)]); paint(c, vgrad(-60, 190, HAIR_L, HAIR))
    blob(c, [(-135, 30), (-140, -80), (-90, -150), (0, -168), (90, -150), (140, -80), (135, 30)]); paint(c, HAIR)
    ears(c, hr, earring=True)
    face(c, hr, blink, look, talk, 0.85, 0.6 + 0.4 * gesture, lashes=True)
    # front hair with middle parting
    blob(c, [(-136, -10), (-128, -100), (-70, -155), (0, -150), (70, -155), (128, -100), (136, -10), (105, -70), (40, -108), (0, -112), (-40, -108), (-105, -70)]); paint(c, vgrad(-160, -10, HAIR_L, HAIR))
    c.set_source_rgb(*SKIN); c.set_line_width(4); c.move_to(0, -150); c.line_to(0, -112); c.stroke()
    c.arc(72, -118, 13, 0, 2 * math.pi); paint(c, AMBER, w=3)  # clip
    c.arc(0, -78, 8, 0, 2 * math.pi); paint(c, (0.80, 0.22, 0.35), w=2)  # bindi
    c.restore(); c.restore()
    if q > 0 and qdraw:
        qdraw(c, x + 20 * s, y - (960 + 10 * math.sin(t * 2.3 + 1)) * s, 230 * s * (1 + 0.25 * qpop), q)
