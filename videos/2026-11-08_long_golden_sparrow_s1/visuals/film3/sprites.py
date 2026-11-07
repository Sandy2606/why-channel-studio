"""Flat 2D cutout sprites (rigid; moved only by translation/rotation, never warped)."""
import math
from PIL import ImageDraw
COMPANY = (200, 56, 48); MUGHAL = (58, 140, 92); FRENCH = (72, 112, 214); NAWAB = (214, 172, 84); PORT = (226, 226, 232)
INKC = (24, 20, 26); CLOTHC = (214, 186, 120)

def A(col, a): return tuple(col[:3]) + (int(max(0, min(1, a)) * 255),)

def man(d, x, y, s, col, a=1.0, hat='turban', musket=True, kneel=False, crown=False, bow=0.0):
    """y = feet. s = height in px."""
    c = A(col, a); k = s / 100
    if kneel:
        d.polygon([(x - 18 * k, y), (x + 20 * k, y), (x + 14 * k, y - 30 * k), (x - 4 * k, y - 34 * k)], fill=c)           # legs folded
        d.polygon([(x - 6 * k, y - 30 * k), (x + 14 * k, y - 32 * k), (x + 22 * k, y - 62 * k), (x + 4 * k, y - 66 * k)], fill=c)  # bent torso
        hx, hy = x + 20 * k, y - 72 * k
    else:
        lean = bow * 25 * k
        d.polygon([(x - 12 * k, y), (x - 4 * k, y), (x - 2 * k, y - 45 * k), (x - 10 * k, y - 45 * k)], fill=c)
        d.polygon([(x + 4 * k, y), (x + 12 * k, y), (x + 10 * k, y - 45 * k), (x + 2 * k, y - 45 * k)], fill=c)
        d.polygon([(x - 14 * k, y - 42 * k), (x + 14 * k, y - 42 * k), (x + 12 * k + lean, y - 80 * k), (x - 12 * k + lean, y - 80 * k)], fill=c)
        hx, hy = x + lean, y - 90 * k
    d.ellipse((hx - 10 * k, hy - 10 * k, hx + 10 * k, hy + 10 * k), fill=c)
    if hat == 'turban': d.ellipse((hx - 12 * k, hy - 16 * k, hx + 12 * k, hy - 2 * k), fill=c)
    elif hat == 'tricorn': d.polygon([(hx - 16 * k, hy - 6 * k), (hx + 16 * k, hy - 6 * k), (hx + 8 * k, hy - 18 * k), (hx - 8 * k, hy - 18 * k)], fill=c)
    elif hat == 'helmet': d.pieslice((hx - 13 * k, hy - 22 * k, hx + 13 * k, hy + 2 * k), 180, 360, fill=c)
    if crown:
        g = A((236, 196, 90), a); d.polygon([(hx - 11 * k, hy - 14 * k), (hx + 11 * k, hy - 14 * k), (hx + 11 * k, hy - 26 * k), (hx + 5 * k, hy - 19 * k), (hx, hy - 28 * k), (hx - 5 * k, hy - 19 * k), (hx - 11 * k, hy - 26 * k)], fill=g)
    if musket and not kneel: d.line((x + 16 * k, y - 20 * k, x + 22 * k, y - 105 * k), fill=c, width=max(1, int(3 * k)))

def rider(d, x, y, s, col, a=1.0):
    c = A(col, a); k = s / 100
    d.ellipse((x - 34 * k, y - 46 * k, x + 30 * k, y - 22 * k), fill=c)                      # horse body
    for dx in (-26, -12, 10, 22): d.line((x + dx * k, y - 26 * k, x + dx * k, y), fill=c, width=max(1, int(5 * k)))
    d.polygon([(x + 24 * k, y - 40 * k), (x + 46 * k, y - 62 * k), (x + 52 * k, y - 54 * k), (x + 32 * k, y - 30 * k)], fill=c)  # neck/head
    d.polygon([(x - 8 * k, y - 46 * k), (x + 6 * k, y - 46 * k), (x + 4 * k, y - 78 * k), (x - 6 * k, y - 78 * k)], fill=c)  # rider
    d.ellipse((x - 8 * k, y - 94 * k, x + 8 * k, y - 78 * k), fill=c)
    d.line((x + 6 * k, y - 70 * k, x + 30 * k, y - 104 * k), fill=c, width=max(1, int(3 * k)))  # lance

def elephant(d, x, y, s, col, a=1.0):
    c = A(col, a); k = s / 100
    d.ellipse((x - 44 * k, y - 70 * k, x + 34 * k, y - 22 * k), fill=c)
    for dx in (-32, -14, 8, 22): d.rectangle((x + dx * k, y - 30 * k, x + (dx + 10) * k, y), fill=c)
    d.ellipse((x + 22 * k, y - 76 * k, x + 54 * k, y - 44 * k), fill=c)
    d.line((x + 50 * k, y - 52 * k, x + 58 * k, y - 10 * k), fill=c, width=max(1, int(7 * k)))
    d.rectangle((x - 20 * k, y - 92 * k, x + 10 * k, y - 70 * k), fill=c)                       # howdah

def cannon(d, x, y, s, col, a=1.0, ang=-8):
    c = A(col, a); k = s / 100; r = math.radians(ang)
    L = 60 * k; d.line((x, y - 18 * k, x + L * math.cos(r), y - 18 * k + L * math.sin(r)), fill=c, width=max(2, int(12 * k)))
    d.ellipse((x - 18 * k, y - 22 * k, x + 4 * k, y), outline=c, width=max(1, int(4 * k)))

def flag(d, x, y, s, col, a=1.0, t=0.0, cross=False):
    k = s / 100; c = A(col, a)
    d.line((x, y, x, y - 100 * k), fill=A(INKC if col != INKC else (200, 200, 200), a), width=max(1, int(3 * k)))
    w = [(x, y - 100 * k)] + [(x + i * 12 * k, y - 100 * k + 4 * k * math.sin(t * 5 + i)) for i in range(1, 6)] + \
        [(x + i * 12 * k, y - 66 * k + 4 * k * math.sin(t * 5 + i)) for i in range(5, 0, -1)] + [(x, y - 66 * k)]
    d.polygon(w, fill=c)
    if cross: d.line((x + 30 * k, y - 99 * k, x + 30 * k, y - 67 * k), fill=A((240, 240, 240), a), width=max(1, int(4 * k)))

def ship(d, x, y, s, sail=(246, 238, 220), hull=(120, 80, 46), a=1.0, flagcol=None, cargo=None):
    k = s / 100
    d.polygon([(x - 50 * k, y - 18 * k), (x + 50 * k, y - 18 * k), (x + 38 * k, y), (x - 40 * k, y)], fill=A(hull, a))
    for mx, h in ((-18, 70), (12, 84)):
        d.line((x + mx * k, y - 18 * k, x + mx * k, y - (18 + h) * k), fill=A(INKC, a), width=max(1, int(3 * k)))
        d.polygon([(x + (mx - 16) * k, y - (26 + h * 0.85) * k), (x + (mx + 16) * k, y - (26 + h * 0.85) * k), (x + (mx + 18) * k, y - 26 * k), (x + (mx - 18) * k, y - 26 * k)], fill=A(sail, a))
    if flagcol: d.rectangle((x + 12 * k, y - 112 * k, x + 30 * k, y - 100 * k), fill=A(flagcol, a))
    if cargo == 'bale': d.rounded_rectangle((x - 8 * k, y - 34 * k, x + 8 * k, y - 20 * k), 3, fill=A(CLOTHC, a))
    if cargo == 'silver':
        for i in range(3): d.ellipse((x - 14 * k + i * 9 * k, y - 32 * k, x - 6 * k + i * 9 * k, y - 24 * k), fill=A((214, 214, 222), a))

def boat(d, x, y, s, a=1.0, rowers=2, t=0.0):
    k = s / 100; c = A((96, 66, 40), a)
    d.pieslice((x - 60 * k, y - 40 * k, x + 60 * k, y + 20 * k), 0, 180, fill=c)
    for i in range(rowers):
        rx = x - 20 * k + i * 40 * k; man(d, rx, y - 10 * k, 40 * k, INKC, a, hat='turban', musket=False)
        ang = 0.6 * math.sin(t * 6 + i); d.line((rx, y - 26 * k, rx + 40 * k * math.cos(1.2 + ang), y - 26 * k + 40 * k * math.sin(1.2 + ang)), fill=c, width=max(1, int(3 * k)))

def fort(d, x, y, s, col, a=1.0, build=1.0, ruined=False):
    k = s / 100; h = 46 * k * build; c = A((70, 64, 60) if ruined else (176, 160, 130), a); o = A(INKC, a)
    d.rectangle((x - 50 * k, y - h, x + 50 * k, y), fill=c, outline=o)
    for i in range(6):
        if build > 0.6: d.rectangle((x - 50 * k + i * 18 * k, y - h - 8 * k, x - 40 * k + i * 18 * k, y - h), fill=c)
    if build >= 1 and not ruined: flag(d, x, y - h, 60 * k, col, a)

def factory(d, x, y, s, col, a=1.0, seized=False):
    k = s / 100; c = A((90, 90, 96) if seized else (200, 184, 150), a)
    d.rectangle((x - 22 * k, y - 26 * k, x + 22 * k, y), fill=c, outline=A(INKC, a))
    d.polygon([(x - 26 * k, y - 26 * k), (x, y - 42 * k), (x + 26 * k, y - 26 * k)], fill=c, outline=A(INKC, a))
    flag(d, x + 18 * k, y - 26 * k, 50 * k, (110, 110, 116) if seized else col, a)

def throne(d, x, y, s, a=1.0, seated=True, col=(236, 196, 90)):
    k = s / 100; g = A(col, a)
    d.polygon([(x - 70 * k, y - 170 * k), (x + 70 * k, y - 170 * k), (x + 50 * k, y - 196 * k), (x - 50 * k, y - 196 * k)], fill=g)   # canopy
    for px in (-62, 58): d.rectangle((x + px * k, y - 170 * k, x + (px + 4) * k, y), fill=g)
    d.rectangle((x - 46 * k, y - 30 * k, x + 46 * k, y), fill=g)                         # dais
    if seated:
        c = A(INKC, a); d.polygon([(x - 22 * k, y - 30 * k), (x + 22 * k, y - 30 * k), (x + 16 * k, y - 92 * k), (x - 16 * k, y - 92 * k)], fill=c)
        d.ellipse((x - 11 * k, y - 116 * k, x + 11 * k, y - 94 * k), fill=c); d.ellipse((x - 14 * k, y - 124 * k, x + 14 * k, y - 106 * k), fill=c)

def scroll(d, x, y, s, a=1.0, seals=1):
    k = s / 100
    d.rounded_rectangle((x - 40 * k, y - 26 * k, x + 40 * k, y + 26 * k), int(6 * k) + 1, fill=A((232, 216, 180), a), outline=A((120, 90, 50), a), width=2)
    for i in range(4): d.line((x - 28 * k, y - 14 * k + i * 9 * k, x + 28 * k, y - 14 * k + i * 9 * k), fill=A((140, 110, 80), a), width=1)
    for j in range(seals): d.ellipse((x + 14 * k - j * 24 * k, y + 10 * k, x + 28 * k - j * 24 * k, y + 24 * k), fill=A((170, 40, 34), a))

def coin(d, x, y, r=10, a=1.0, silver=False):
    col = (214, 214, 222) if silver else (232, 190, 90)
    d.ellipse((x - r, y - r, x + r, y + r), fill=A(col, a), outline=A((120, 100, 60), a), width=2)

def bale(d, x, y, s, a=1.0):
    k = s / 100; d.rounded_rectangle((x - 30 * k, y - 40 * k, x + 30 * k, y), int(8 * k) + 1, fill=A(CLOTHC, a), outline=A((110, 86, 44), a), width=2)
    d.line((x - 30 * k, y - 20 * k, x + 30 * k, y - 20 * k), fill=A((110, 86, 44), a), width=2); d.line((x, y - 40 * k, x, y), fill=A((110, 86, 44), a), width=2)

def puff(d, x, y, r, a=1.0):
    for i in range(4):
        dx, dy = (i - 1.5) * r * 0.5, -abs(i - 1.5) * r * 0.2
        d.ellipse((x + dx - r * 0.6, y + dy - r * 0.6, x + dx + r * 0.6, y + dy + r * 0.6), fill=A((220, 214, 200), a * 0.7))

def swords(d, x, y, s, a=1.0, col=(240, 230, 210)):
    k = s / 100; c = A(col, a)
    d.line((x - 30 * k, y - 30 * k, x + 30 * k, y + 30 * k), fill=c, width=max(2, int(6 * k))); d.line((x + 30 * k, y - 30 * k, x - 30 * k, y + 30 * k), fill=c, width=max(2, int(6 * k)))
    d.line((x - 22 * k, y + 8 * k, x - 8 * k, y + 22 * k), fill=c, width=max(2, int(6 * k))); d.line((x + 22 * k, y + 8 * k, x + 8 * k, y + 22 * k), fill=c, width=max(2, int(6 * k)))

def formation(d, x, y, cols, rows, s, col, a=1.0, kind='man', hat='turban', gap=None, jitter=0.0, t=0.0, mix=None):
    """block of rigid figures; mix=(fraction, col2, hat2) recolours a share (e.g. Europeans within a sepoy army)."""
    gx = gap or s * 0.42; gy = s * 0.55
    for r in range(rows):
        for c_ in range(cols):
            px = x + c_ * gx + (r % 2) * gx * 0.5; py = y + r * gy
            cc, hh = col, hat
            if mix and ((r * cols + c_) * 7919 % 100) / 100 < mix[0]: cc, hh = mix[1], mix[2]
            if kind == 'man': man(d, px, py, s, cc, a, hat=hh)
            elif kind == 'rider': rider(d, px, py, s, cc, a)
            elif kind == 'elephant': elephant(d, px, py, s, cc, a)
