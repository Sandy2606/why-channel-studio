# 2D motion-graphic explainers for the long video (1920x1080, brand: #0A0A0A / cream / amber)
import json, math, functools, sys
sys.path.insert(0, '/home/claude/elnino')
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from epic import prog, e_out, e_io, e_back, font, is_te
from modern import mono, text_plain, pill, paste_c, alpha_paste, CREAM, AMBER, GREY, RED

W, H = 1920, 1080
INK = (10, 10, 10); LAND = (34, 33, 31); LAND_HI = (52, 50, 46); GRID = (28, 28, 28)
GREEN = (120, 210, 120)

def T(lang, en, te): return te if lang == 'te' else en
def hfont(txt, px): return font('tesans', int(px * .82)) if is_te(txt) else font('archivo', px)

# ---------------- geography (land drawn as one mass, no political borders) ----------------
@functools.lru_cache(1)
def _polys():
    d = json.load(open('/home/claude/elnino/geo/countries.geojson')); out = []
    for f in d['features']:
        g = f['geometry']; cs = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in cs: out.append(poly[0])
    return out

class Map:
    def __init__(self, lon0, lon1, lat0, lat1, box):
        self.lon0, self.lon1, self.lat0, self.lat1 = lon0, lon1, lat0, lat1; self.box = box
    def xy(self, lon, lat):
        x0, y0, x1, y1 = self.box
        return x0 + (lon - self.lon0) / (self.lon1 - self.lon0) * (x1 - x0), y0 + (self.lat1 - lat) / (self.lat1 - self.lat0) * (y1 - y0)

@functools.lru_cache(4)
def map_base(key):
    m = MAPS[key]; im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
    # faint dot graticule
    for gx in range(40, W, 48):
        for gy in range(40, H, 48): d.ellipse((gx - 1.5, gy - 1.5, gx + 1.5, gy + 1.5), fill=GRID)
    big = Image.new('L', (W * 2, H * 2), 0); bd = ImageDraw.Draw(big)
    for ring in _polys():
        pts = [m.xy(lo, la) for lo, la in ring]
        if key == 'world': pts = [m.xy(lo if lo > -170 else lo + 360, la) for lo, la in ring]
        bd.polygon([(x * 2, y * 2) for x, y in pts], fill=255)
    mask = big.resize((W, H), Image.LANCZOS)
    land = Image.new('RGB', (W, H), LAND); im.paste(land, (0, 0), mask)
    edge = mask.filter(ImageFilter.FIND_EDGES).point(lambda p: min(255, p * 3))
    im.paste(Image.new('RGB', (W, H), LAND_HI), (0, 0), edge)
    return im

MAPS = {'india': Map(64.0, 100.0, 5.0, 35.0, (640, 20, 640 + 36 * 34.5, 20 + 30 * 34.5)),
        'world': Map(-95.0, 190.0, -45.0, 50.0, (40, 130, 1880, 130 + 95 * 6.456))}

def _pin(img, x, y, v, t, label, sub=None, side='r', col=AMBER, lang='en'):
    if v < t: return
    k = e_back(prog(v, t, t + .35)); a = prog(v, t, t + .15)
    d = ImageDraw.Draw(img)
    # pulse rings
    for ph in (0, .5):
        p = ((v - t) * .8 + ph) % 1.0
        R = 14 + 46 * p; d.ellipse((x - R, y - R, x + R, y + R), outline=col + (int(170 * (1 - p) * a),), width=3)
    r = 13 * k; d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,), outline=INK + (255,), width=3)
    lk = e_out(prog(v, t + .1, t + .45))
    if lk <= 0: return
    px = 40; f = hfont(label, px); tw = f.getlength(label)
    lx = x + 34 if side[0] == 'r' else x - 34 - tw - 40
    ly = y - 30 + (70 if 'd' in side else (-70 if 'u' in side else 0))
    box = Image.new('RGBA', (int(tw + 40), 62), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
    bd.rounded_rectangle((0, 0, tw + 39, 61), radius=12, fill=(12, 12, 12, 235), outline=col + (255,), width=3)
    bd.text((20, 31), label, font=f, fill=CREAM, anchor='lm')
    alpha_paste(img, box, lx + (20 if side[0] == 'r' else -20) * (1 - lk), ly, lk)
    if sub: mono(img, sub, lx + 12, ly + 88, 22, col, lk, anchor='l', track=2)

# 1) hook: one day, five places
def india_hook(img, v, t0, pins, lang='en', title=None):
    img.paste(map_base('india'), (0, 0)); m = MAPS['india']
    for (lab, lon, lat, t, sub, side) in pins:
        x, y = m.xy(lon, lat); _pin(img, x, y, v, t, lab, sub, side, lang=lang)
    if title:
        a = prog(v, t0, t0 + .4)
        mono(img, title[0], 110, 640, 30, AMBER, a, anchor='l', track=4)
        text_plain(img, title[1], 110, 720, 84 if not is_te(title[1]) else 76, CREAM, a, anchor='l')

# 9) nine nights: pins with day-count badges
def india_days(img, v, t0, pins, lang='en'):
    img.paste(map_base('india'), (0, 0)); m = MAPS['india']
    for (lab, lon, lat, t, badge, side) in pins:
        x, y = m.xy(lon, lat); _pin(img, x, y, v, t, lab, None, side, lang=lang)
        if badge and v >= t + .35:
            k = e_back(prog(v, t + .35, t + .7)); f = hfont(badge, 46); tw = f.getlength(badge)
            b = Image.new('RGBA', (int(tw + 44), 70), (0, 0, 0, 0)); bd = ImageDraw.Draw(b)
            bd.rounded_rectangle((0, 0, tw + 43, 69), radius=35, fill=AMBER + (255,)); bd.text((22, 35), badge, font=f, fill=INK, anchor='lm')
            off = 34 if side[0] == 'r' else -34 - tw - 44
            paste_c(img, b, x + off + (tw + 44) / 2, y + 62 + (70 if 'd' in side else (-70 if 'u' in side else 0)), prog(v, t + .35, t + .5), k)

# 7) Ramlila crosses the oceans
def diaspora(img, v, t0, dests, lang='en'):
    img.paste(map_base('world'), (0, 0)); m = MAPS['world']
    ox, oy = m.xy(80.0, 23.0)
    d = ImageDraw.Draw(img)
    _pin(img, ox, oy, v, t0, T(lang, 'INDIA', 'ఇండియా'), None, 'r', lang=lang)
    for i, (lab, lon, lat, t, side) in enumerate(dests):
        if lon < -170: lon += 360
        tx, ty = m.xy(lon, lat); k = e_io(prog(v, t, t + 1.1))
        if k <= 0: continue
        mx, my = (ox + tx) / 2, min(oy, ty) - 120 - abs(tx - ox) * .12
        pts = []
        for j in range(int(60 * k) + 1):
            u = j / 60; pts.append(((1 - u) ** 2 * ox + 2 * (1 - u) * u * mx + u * u * tx, (1 - u) ** 2 * oy + 2 * (1 - u) * u * my + u * u * ty))
        if len(pts) > 1:
            for j in range(0, len(pts) - 1, 2): d.line(pts[j:j + 2], fill=AMBER + (230,), width=4)
            hx, hy = pts[-1]; d.ellipse((hx - 8, hy - 8, hx + 8, hy + 8), fill=CREAM)
        if k >= 1: _pin(img, tx, ty, v, t + 1.1, lab, None, side, lang=lang)

# 2) the name: two words snap into one
def word_merge(img, v, t0, parts, result, sub=None, lang='en'):
    """parts=[(word, meaning, t)], result=(text, t)"""
    cx = W / 2; n = len(parts); rt = result[1]; mk = e_io(prog(v, rt, rt + .5))
    px = 150
    while px > 70 and sum(hfont(p[0], px).getlength(p[0]) for p in parts) + 260 > 1700: px -= 6
    ws_ = [hfont(p[0], px).getlength(p[0]) for p in parts]
    xs = [cx - 130 - ws_[1] / 2 * 0 - ws_[0] / 2, cx + 130 + ws_[1] / 2] if n == 2 else [cx]
    for i, (wd, mean, t) in enumerate(parts):
        if v < t: continue
        k = e_back(prog(v, t, t + .4)); a = prog(v, t, t + .15) * (1 - min(1.0, mk * 3))
        x = xs[i] + (cx - xs[i]) * mk
        text_plain(img, wd, x, 430 - 60 * (1 - k), px if not is_te(wd) else int(px * .8), CREAM, a)
        bk = e_out(prog(v, t + .35, t + .7))
        if bk > 0:
            pill(img, mean, x, 600, 44, AMBER, INK, a * bk, .9 + .1 * bk)
        if i == 0 and n == 2 and v >= parts[1][2]:
            text_plain(img, '+', cx, 430, 130, AMBER, prog(v, parts[1][2], parts[1][2] + .2) * (1 - min(1.0, mk * 3)))
    if mk > .33:
        k = e_back(prog(v, rt + .15, rt + .6))
        text_plain(img, result[0], cx, 450, int((170 if not is_te(result[0]) else 140) * max(.3, k)), AMBER, prog(v, rt + .15, rt + .3))
        if sub: mono(img, sub, cx, 600, 34, CREAM, prog(v, rt + .4, rt + .8), track=4)

# 3) three stories, one day
def three_lines(img, v, t0, lanes, day_lab, t_day, lang='en'):
    """lanes=[(label, sub, t_start, color)] lines draw left->right and hit the DAY 10 column"""
    d = ImageDraw.Draw(img); X0, X1 = 200, 1470; ys = [300, 500, 700]
    # day column
    dk = e_out(prog(v, t_day, t_day + .5))
    if dk > 0:
        glow = 0
        for (_, _, ts, _) in lanes: glow = max(glow, 1 - prog(v, ts + 1.6, ts + 2.4) if v > ts + 1.6 else 0)
        col = Image.new('RGBA', (300, 700), (0, 0, 0, 0)); cd = ImageDraw.Draw(col)
        cd.rounded_rectangle((0, 0, 299, 699), radius=26, fill=AMBER + (int(40 + 60 * glow),), outline=AMBER + (255,), width=5)
        alpha_paste(img, col, X1, 150 + 40 * (1 - dk), dk)
        text_plain(img, day_lab[0], X1 + 150, 220 + 40 * (1 - dk), 70 if not is_te(day_lab[0]) else 56, AMBER, dk)
        mono(img, day_lab[1], X1 + 150, 905 + 40 * (1 - dk), 22, CREAM, dk, track=2)
    for i, (lab, sub, ts, colr) in enumerate(lanes):
        if v < ts: continue
        y = ys[i]; a = prog(v, ts, ts + .2); k = e_io(prog(v, ts + .2, ts + 1.8))
        text_plain(img, lab, X0, y - 52, 52 if not is_te(lab) else 44, CREAM, a, anchor='l')
        mono(img, sub, X0, y + 46, 22, GREY, a, anchor='l', track=2)
        xe = X0 + (X1 - X0) * k
        d.line((X0, y, X1, y), fill=(50, 50, 50, int(255 * a)), width=6)
        d.line((X0, y, xe, y), fill=colr + (255,), width=10)
        d.ellipse((X0 - 12, y - 12, X0 + 12, y + 12), fill=colr + (255,))
        if k > 0: d.ellipse((xe - 16, y - 16, xe + 16, y + 16), fill=CREAM + (255,), outline=colr + (255,), width=5)
        if k >= 1:
            hk = prog(v, ts + 1.8, ts + 2.4)
            if hk < 1:
                R = 20 + 60 * hk; d.ellipse((X1 - R, y - R, X1 + R, y + R), outline=AMBER + (int(255 * (1 - hk)),), width=5)

# 4) the loophole
def loophole(img, v, t0, slots, lang='en'):
    """slots=[(text, ok, t)]"""
    n = len(slots); gap = 560; x0 = W / 2 - gap * (n - 1) / 2
    for i, (txt, ok, t) in enumerate(slots):
        if v < t: continue
        x = x0 + i * gap; k = e_back(prog(v, t, t + .4)); a = prog(v, t, t + .15)
        colr = AMBER if ok else RED
        card = Image.new('RGBA', (480, 420), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle((0, 0, 479, 419), radius=30, fill=(14, 14, 14, 235), outline=colr + (255,), width=6)
        paste_c(img, card, x, 470, a, .85 + .15 * k)
        mk = e_out(prog(v, t + .35, t + .7)); d = ImageDraw.Draw(img); cy = 380
        if mk > 0:
            if ok:
                p = [(x - 70, cy), (x - 20, cy + 50), (x + 80, cy - 60)]
                L = mk * 2
                d.line(p[:1] + [(p[0][0] + (p[1][0] - p[0][0]) * min(1, L), p[0][1] + (p[1][1] - p[0][1]) * min(1, L))], fill=AMBER, width=22)
                if L > 1: d.line([p[1], (p[1][0] + (p[2][0] - p[1][0]) * (L - 1), p[1][1] + (p[2][1] - p[1][1]) * (L - 1))], fill=AMBER, width=22)
            else:
                s = 65 * mk; d.line((x - s, cy - s, x + s, cy + s), fill=RED, width=22); d.line((x + s, cy - s, x - s, cy + s), fill=RED, width=22)
        text_plain(img, txt, x, 580, 58 if not is_te(txt) else 48, CREAM, a)

# 5) timeline 1520 -> 1610 -> today
def timeline(img, v, t0, nodes, lang='en'):
    """nodes=[(year, place, t)]"""
    d = ImageDraw.Draw(img); X0, X1, Y = 260, 1660, 560
    d.line((X0, Y, X1, Y), fill=(60, 60, 60), width=8)
    n = len(nodes); xs = [X0 + (X1 - X0) * i / (n - 1) for i in range(n)]
    last = None
    for i, (yr, place, t) in enumerate(nodes):
        if v < t: continue
        last = i; k = e_back(prog(v, t, t + .4)); a = prog(v, t, t + .15)
        if i > 0:
            pk = e_io(prog(v, t - .6, t)); d.line((xs[i - 1], Y, xs[i - 1] + (xs[i] - xs[i - 1]) * pk, Y), fill=AMBER, width=8)
        r = 26 * k; d.ellipse((xs[i] - r, Y - r, xs[i] + r, Y + r), fill=AMBER, outline=INK, width=4)
        text_plain(img, yr, xs[i], Y - 130 + 30 * (1 - k), 110 if not is_te(yr) else 84, AMBER if i == n - 1 else CREAM, a)
        pill(img, place, xs[i], Y + 110, 34, (30, 30, 30), CREAM, a)
    if last is not None and last < n - 1:   # travelling dot toward next node
        tn = nodes[last + 1][2]; u = e_io(prog(v, tn - .6, tn))
        if u > 0:
            x = xs[last] + (xs[last + 1] - xs[last]) * u; d.ellipse((x - 12, Y - 12, x + 12, Y + 12), fill=CREAM)

# 6) Ramnagar: the whole town is the stage
def town_stage(img, v, t0, spots, walk_t, lang='en'):
    """spots=[(label, (x,y), t)]; crowd dots walk between spots from walk_t"""
    d = ImageDraw.Draw(img); rng = np.random.default_rng(3)
    # town blocks
    for _ in range(150):
        x = rng.uniform(140, 1780); y = rng.uniform(140, 960); w = rng.uniform(30, 90); h = rng.uniform(24, 70)
        d.rounded_rectangle((x, y, x + w, y + h), radius=6, fill=(24, 24, 24))
    pts = [p for _, p, _ in spots]
    # road path
    path = []
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        for j in range(40): u = j / 40; path.append((ax + (bx - ax) * u, ay + (by - ay) * u - math.sin(u * math.pi) * 90))
    path.append(pts[-1])
    pk = prog(v, t0, t0 + 1.0)
    for j in range(0, int((len(path) - 1) * pk), 2): d.line(path[j:j + 2], fill=(90, 80, 60), width=6)
    for lab, (x, y), t in spots:
        if v < t: continue
        k = e_back(prog(v, t, t + .4)); a = prog(v, t, t + .15)
        r = 70 * k; d.ellipse((x - r, y - r, x + r, y + r), fill=(40, 32, 14), outline=AMBER, width=5); d.ellipse((x - 14 * k, y - 14 * k, x + 14 * k, y + 14 * k), fill=AMBER)
        pill(img, lab, x, y - 120, 40, AMBER, INK, a, .8 + .2 * k)
    if v > walk_t:   # audience walks with the story
        L = len(path)
        for q in range(60):
            u = ((v - walk_t) * .07 - q * .006) % 1.0
            if (v - walk_t) * .07 - q * .006 < 0: continue
            px, py = path[min(L - 1, int(u * (L - 1)))]
            jx = math.sin(q * 12.9) * 26; jy = math.cos(q * 7.3) * 18
            d.ellipse((px + jx - 7, py + jy - 7, px + jx + 7, py + jy + 7), fill=CREAM)

# 8) the clay cycle
def clay_cycle(img, v, t0, nodes, lang='en', center=None):
    """nodes=[(label, t)] placed clockwise on a circle; dot travels around"""
    d = ImageDraw.Draw(img); cx, cy, R = W / 2, 540, 330; n = len(nodes)
    ang = [(-90 + 360 * i / n) for i in range(n)]
    for i, (lab, t) in enumerate(nodes):
        if v < t: continue
        a0 = math.radians(ang[i]); k = e_io(prog(v, t, t + .9))
        if i > 0 or v > nodes[-1][1] + .9:
            pass
        # arc from node i to i+1
        a1 = math.radians(ang[i] + 360 / n * k)
        if i < n - 1 or True:
            d.arc((cx - R, cy - R, cx + R, cy + R), ang[i] + 12, ang[i] + 12 + (360 / n - 24) * k, fill=AMBER, width=8)
            if k > 0 and k < 1:
                aa = math.radians(ang[i] + 12 + (360 / n - 24) * k); hx, hy = cx + R * math.cos(aa), cy + R * math.sin(aa)
                d.ellipse((hx - 12, hy - 12, hx + 12, hy + 12), fill=CREAM)
    for i, (lab, t) in enumerate(nodes):
        if v < t: continue
        a0 = math.radians(ang[i]); x, y = cx + R * math.cos(a0), cy + R * math.sin(a0)
        k = e_back(prog(v, t, t + .4))
        d.ellipse((x - 22 * k, y - 22 * k, x + 22 * k, y + 22 * k), fill=AMBER, outline=INK, width=4)
        ox = 0 if abs(math.cos(a0)) < .3 else (1 if math.cos(a0) > 0 else -1)
        oy = -1 if math.sin(a0) < -.5 else (1 if math.sin(a0) > .5 else 0)
        pill(img, lab, x + ox * 200, y + oy * 70, 38, (24, 24, 24), CREAM, prog(v, t, t + .2), .85 + .15 * k)
    if center and v >= center[1]:
        k = e_back(prog(v, center[1], center[1] + .4))
        ws = center[0].split(); h = (len(ws) + 1) // 2
        for li, ln in enumerate([' '.join(ws[:h]), ' '.join(ws[h:])]):
            text_plain(img, ln, cx, cy - 40 + li * 80, int((64 if not is_te(ln) else 52) * max(.3, k)), AMBER, prog(v, center[1], center[1] + .2))

# villains: power -> what they did with it
def power_table(img, v, t0, rows, lang='en'):
    """rows=[(villain, power, t)]"""
    for i, (vil, pw, t) in enumerate(rows):
        if v < t: continue
        y = 330 + i * 190; k = e_out(prog(v, t, t + .4)); a = prog(v, t, t + .2)
        text_plain(img, vil, 620 - 40 * (1 - k), y, 72 if not is_te(vil) else 58, CREAM, a, anchor='r') if False else None
        f = hfont(vil, 72); tw = f.getlength(vil)
        text_plain(img, vil, 860 - tw - 40 * (1 - k), y, 72 if not is_te(vil) else 58, CREAM, a, anchor='l')
        d = ImageDraw.Draw(img); d.line((900, y, 900 + 140 * k, y), fill=AMBER, width=6)
        d.polygon([(1040 * 1, y - 14), (1062, y), (1040, y + 14)], fill=AMBER + (int(255 * k),))
        pw_w = hfont(pw, 44).getlength(pw) + 60
        pill(img, pw, 1090 + pw_w / 2, y, 44, AMBER, INK, prog(v, t + .25, t + .45))
