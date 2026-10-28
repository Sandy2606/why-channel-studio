"""Ravana new-style test Short: story-first, '?' host, evidence visuals. 1080x1920 @30."""
import json, math, os, sys, subprocess
import numpy as np, cairo
from PIL import Image, ImageFilter
import host

W, H, FPS = 1080, 1920, 30
LEAD, TAIL = 0.15, 0.7
VOICE_LEN = 54.96
DUR = LEAD + VOICE_LEN + TAIL
BLACK = (0.04, 0.04, 0.04); CREAM = host.CREAM; AMBER = host.AMBER; RED = (0.89, 0.16, 0.16)
ROOT = '/home/claude/rv/'

# ---------- timing helpers ----------
WORDS = json.load(open(ROOT + 'words.json'))
def T(word, n=1, after=0.0):
    """start time (video clock) of the n-th occurrence of word after `after` (voice clock)."""
    k = 0
    for s, e, w in WORDS:
        if s < after: continue
        if w.strip('.,?!').lower() == word.lower():
            k += 1
            if k == n: return s + LEAD
    raise KeyError(word)
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def prog(t, a, b): return clamp((t - a) / max(1e-6, b - a))
def e_out(x): return 1 - (1 - x) ** 3
def e_io(x): return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def e_back(x, s=1.7): x -= 1; return 1 + (s + 1) * x ** 3 + s * x ** 2

# ---------- scene anchors ----------
A = {}
A['hook'] = 0.0
A['35'] = T('35'); A['women'] = T('women'); A['just'] = T('just'); A['inlaws'] = T('front')
A['why'] = T('why?'.strip('?'))
A['people'] = T('people'); A['mandodari'] = T('mandodari'); A['son'] = T('son')
A['dasara1'] = T('on'); A['burn1'] = T('burn'); A['but'] = T('but'); A['pray1'] = T('pray')
A['jodhpur'] = T('jodhpur'); A['devgoda'] = T('devgoda'); A['descend'] = T('descendants')
A['dasara2'] = T('dasara', 2); A['city'] = T('city'); A['bath'] = T('bath'); A['funeral'] = T('funeral'); A['temple1'] = T('temple')
A['baijnath'] = T('baijnath'); A['penance'] = T('penance'); A['shiva'] = T('shiva')
A['so'] = T('so'); A['devotee'] = T('devotee'); A['stopped'] = T('stopped')
A['because'] = T('because'); A['villain'] = T('villain')
A['soyes'] = T('so', 2); A['family'] = T('family')
A['cta'] = T('whenever'); A['comment'] = T('comment'); A['research'] = T('research')

# ---------- images ----------
IMG = {}
def _surf_from_pil(im):
    im = im.convert('RGBA'); a = np.array(im)
    bgra = a[:, :, [2, 1, 0, 3]].copy()
    s = cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, im.width, im.height)
    return s, bgra
def photo(name):
    """returns (fill_surface, sharp_surface) both 1080 wide; fill is 1080x1920 blurred."""
    if name in IMG: return IMG[name]
    p = None
    for ext in ('.jpg', '.png', '.orig', '.jpeg'):
        if os.path.exists(ROOT + 'img/' + name + ext) and os.path.getsize(ROOT + 'img/' + name + ext) > 20000:
            p = ROOT + 'img/' + name + ext; break
    if p is None:
        im = Image.new('RGB', (1200, 900), (40, 36, 30))
    else:
        im = Image.open(p).convert('RGB')
    # fill
    s = max(W * 1.15 / im.width, H * 1.15 / im.height)
    f = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    f = f.crop(((f.width - int(W * 1.15)) // 2, (f.height - int(H * 1.15)) // 2,
                (f.width - int(W * 1.15)) // 2 + int(W * 1.15), (f.height - int(H * 1.15)) // 2 + int(H * 1.15)))
    f = f.filter(ImageFilter.GaussianBlur(38)).point(lambda v: int(v * 0.55))
    # sharp: scaled so its width covers 1080*1.12 (crop happens via clip)
    s2 = max(W * 1.18 / im.width, 1250 * 1.12 / im.height)
    sh = im.resize((int(im.width * s2), int(im.height * s2)), Image.LANCZOS)
    IMG[name] = (_surf_from_pil(f), _surf_from_pil(sh), p is None)
    return IMG[name]

def draw_photo(c, name, t, t0, t1, z=(1.0, 1.08), focus=(0.5, 0.5), box=(0, 230, W, 1260), dim=0.0, label=None, full=False):
    (fill, _), (sharp, _), missing = photo(name)
    u = prog(t, t0, t1)
    # fill
    c.save(); fs = 1.0 + 0.03 * u
    c.translate(W / 2, H / 2); c.scale(fs, fs); c.translate(-fill.get_width() / 2, -fill.get_height() / 2)
    c.set_source_surface(fill, 0, 0); c.paint(); c.restore()
    x, y, w, h = (0, 0, W, H) if full else box
    zz = z[0] + (z[1] - z[0]) * e_io(u)
    c.save(); c.rectangle(x, y, w, h); c.clip()
    sw, shh = sharp.get_width(), sharp.get_height()
    sc = max(w / sw, h / shh) * zz
    cx = x + w / 2 - (focus[0] - 0.5) * sw * sc * 0.3; cy = y + h / 2 - (focus[1] - 0.5) * shh * sc * 0.3
    c.translate(cx, cy); c.scale(sc, sc); c.translate(-sw / 2, -shh / 2)
    c.set_source_surface(sharp, 0, 0); c.get_source().set_filter(cairo.FILTER_GOOD); c.paint()
    c.restore()
    if dim: c.set_source_rgba(0, 0, 0, dim); c.rectangle(x, y, w, h); c.fill()
    if missing:
        mono(c, 'PHOTO: ' + name.upper(), W / 2, y + h / 2, 34, CREAM)
    if label:
        mono(c, label, W - 150, y + h - 26, 18, (1, 1, 1), a=0.75, anchor='r')

def draw_video(c, t, t0, off, label='Dussehra effigies · Swastik Arora · Pexels', dim=0.12):
    i = int((t - t0 + off) * FPS) + 1
    i = max(1, min(i, 762))
    im = Image.open(f'{ROOT}vid/f_{i:04d}.jpg').convert('RGBA')
    sf, keep = _surf_from_pil(im)
    u = prog(t, t0, t0 + 6); z = 1.0 + 0.06 * u
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    c.set_source_surface(sf, 0, 0); c.paint(); c.restore()
    if dim: c.set_source_rgba(0, 0, 0, dim); c.paint()
    mono(c, label, W - 150, 1240, 18, (1, 1, 1), a=0.75, anchor='r')

# ---------- text ----------
def font(c, kind, px):
    c.select_font_face('Archivo Black' if kind == 'head' else 'Space Mono',
                       cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if kind == 'monob' else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(px)
def mono(c, txt, x, y, px, col=AMBER, a=1.0, anchor='c', kind='monob'):
    font(c, kind, px); e = c.text_extents(txt)
    xx = x - e.width / 2 - e.x_bearing if anchor == 'c' else (x - e.width - e.x_bearing if anchor == 'r' else x)
    c.move_to(xx, y + px * 0.35); c.set_source_rgba(*col, a); c.show_text(txt)
    return e.width
def head(c, txt, x, y, px, col=CREAM, a=1.0, anchor='c', shadow=True):
    font(c, 'head', px); e = c.text_extents(txt)
    xx = x - e.width / 2 - e.x_bearing if anchor == 'c' else x
    if shadow:
        c.move_to(xx + 4, y + px * 0.36 + 5); c.set_source_rgba(0, 0, 0, 0.55 * a); c.show_text(txt)
    c.move_to(xx, y + px * 0.36); c.set_source_rgba(*col, a); c.show_text(txt)
    return e.width
def rrect(c, x, y, w, h, r):
    c.new_sub_path(); c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); c.close_path()
def pill(c, txt, cx, cy, px=34, fill=AMBER, col=BLACK, a=1.0, s=1.0, kind='head'):
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    font(c, kind, px); e = c.text_extents(txt); w = e.width + px * 1.3; h = px * 1.75
    rrect(c, -w / 2, -h / 2, w, h, h / 2); c.set_source_rgba(*fill, a); c.fill()
    c.move_to(-e.width / 2 - e.x_bearing, px * 0.36); c.set_source_rgba(*col, a); c.show_text(txt)
    c.restore()
def typed(c, txt, x, y, px, t, t0, cps=22, col=CREAM, kind='head', anchor='c', a=1.0):
    n = int(clamp((t - t0) * cps, 0, len(txt)))
    if n <= 0: return
    font(c, kind, px); full = c.text_extents(txt)
    xx = x - full.width / 2 - full.x_bearing if anchor == 'c' else x
    c.move_to(xx, y + px * 0.36); c.set_source_rgba(*col, a); c.show_text(txt[:n])
    if n < len(txt) and int(t * 6) % 2 == 0:
        e = c.text_extents(txt[:n]); c.rectangle(xx + e.x_advance + 4, y - px * 0.4, px * 0.08, px * 0.85); c.fill()

def card(c, cx, cy, w, h, t, t0, a=1.0, tilt=-1.5):
    """paper card slides up + settles; returns transform state saved — caller must restore."""
    u = e_back(prog(t, t0, t0 + 0.35)) if t >= t0 else 0
    c.save(); c.translate(cx, cy + (1 - u) * 160); c.rotate(math.radians(tilt * u))
    c.set_source_rgba(0, 0, 0, 0.35 * a); rrect(c, -w / 2 + 8, -h / 2 + 12, w, h, 22); c.fill()
    c.set_source_rgba(*CREAM, a); rrect(c, -w / 2, -h / 2, w, h, 22); c.fill()
    return u

def polaroid(c, name, cx, cy, w, t, t0, rot=6):
    if t < t0: return
    (_, _), (sharp, _), _ = photo(name)
    u = e_back(prog(t, t0, t0 + 0.35))
    h = w * 0.78
    c.save(); c.translate(cx, cy - (1 - u) * 300); c.rotate(math.radians(rot * u + (1 - u) * 20))
    c.set_source_rgba(0, 0, 0, 0.4); c.rectangle(-w / 2 - 14, -h / 2 - 6, w + 28, h + 80); c.fill()
    c.set_source_rgb(0.97, 0.96, 0.93); c.rectangle(-w / 2 - 20, -h / 2 - 20, w + 40, h + 90); c.fill()
    c.save(); c.rectangle(-w / 2, -h / 2, w, h); c.clip()
    sw, sh = sharp.get_width(), sharp.get_height(); sc = max(w / sw, h / sh)
    c.scale(sc, sc); c.translate(-sw / 2, -sh / 2); c.set_source_surface(sharp, 0, 0); c.paint(); c.restore()
    mono(c, 'MANDSAUR, MP', 0, h / 2 + 40, 22, (0.2, 0.2, 0.2))
    c.restore()

def marker_underline(c, x0, x1, y, t, t0, dur=0.35, col=AMBER, wdt=10):
    u = e_out(prog(t, t0, t0 + dur))
    if u <= 0: return
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(wdt); c.set_source_rgba(*col, 0.92)
    c.move_to(x0, y + 3); xe = x0 + (x1 - x0) * u
    c.curve_to(x0 + (xe - x0) * 0.3, y - 4, x0 + (xe - x0) * 0.7, y + 8, xe, y); c.stroke(); c.restore()

def marker_circle(c, cx, cy, rx, ry, t, t0, dur=0.45, col=AMBER):
    u = e_out(prog(t, t0, t0 + dur))
    if u <= 0: return
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(9); c.set_source_rgba(*col, 0.92)
    c.translate(cx, cy); c.scale(rx, ry)
    c.arc(0, 0, 1, math.radians(-100), math.radians(-100 + 380 * u)); c.restore(); c.stroke()

def stamp(c, txt, cx, cy, t, t0, col=AMBER, px=70, rot=-8):
    if t < t0: return
    u = prog(t, t0, t0 + 0.18); s = 1.6 - 0.6 * e_out(u)
    c.save(); c.translate(cx, cy); c.rotate(math.radians(rot)); c.scale(s, s)
    font(c, 'head', px); e = c.text_extents(txt); w = e.width + 50; h = px * 1.5
    c.set_line_width(8); c.set_source_rgba(*col, 0.95 * min(1, u * 2)); rrect(c, -w / 2, -h / 2, w, h, 12); c.stroke()
    c.move_to(-e.width / 2 - e.x_bearing, px * 0.36); c.show_text(txt); c.restore()

# ---------- map ----------
GEO = json.load(open('/home/claude/sandy2606/why-channel-studio/pipeline/lib/countries.geojson'))
POLYS = []
for f in GEO['features']:
    g = f['geometry']
    if g is None: continue
    ps = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for p in ps:
        ring = p[0]
        xs = [q[0] for q in ring]; ys = [q[1] for q in ring]
        if max(xs) < 40 or min(xs) > 115 or max(ys) < -5 or min(ys) > 50: continue
        POLYS.append(np.array(ring))
PLACES = {
    'Mandsaur': (75.07, 24.07, 'MADHYA PRADESH'),
    'Jodhpur': (73.02, 26.24, 'RAJASTHAN'),
    'Baijnath': (76.65, 32.05, 'HIMACHAL PRADESH'),
    'Bisrakh': (77.43, 28.57, 'UTTAR PRADESH'),
    'Kanpur': (80.33, 26.45, 'UTTAR PRADESH'),
}
KX = math.cos(math.radians(23))
REFS = [('DELHI', 77.21, 28.61), ('MUMBAI', 72.88, 19.08), ('JAIPUR', 75.79, 26.91), ('AHMEDABAD', 72.57, 23.02),
        ('BHOPAL', 77.41, 23.26), ('SHIMLA', 77.17, 31.10), ('AMRITSAR', 74.87, 31.63), ('UDAIPUR', 73.71, 24.59),
        ('KOLKATA', 88.36, 22.57), ('CHENNAI', 80.27, 13.08), ('HYDERABAD', 78.49, 17.39), ('BENGALURU', 77.59, 12.97)]
_G = None
def grain(c):
    global _G
    if _G is None:
        rng = np.random.default_rng(3); n = rng.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
        a = np.zeros((H // 2, W // 2, 4), np.uint8); m = (n.astype(np.uint16) * 16 // 255).astype(np.uint8); a[..., 0] = a[..., 1] = a[..., 2] = m; a[..., 3] = 16
        _G = (cairo.ImageSurface.create_for_data(memoryview(a), cairo.FORMAT_ARGB32, W // 2, H // 2), a)
    c.save(); c.scale(2, 2); c.set_source_surface(_G[0], 0, 0); c.paint(); c.restore()
def draw_map(c, clon, clat, zoom, t, glow=0.0):
    """zoom = pixels per degree."""
    c.set_source_rgb(0.055, 0.075, 0.095); c.paint()
    # graticule
    c.set_line_width(1.2); c.set_source_rgba(1, 1, 1, 0.05)
    for lon in range(40, 120, 5):
        x = W / 2 + (lon - clon) * zoom * KX; c.move_to(x, 0); c.line_to(x, H)
    for lat in range(-5, 50, 5):
        y = H / 2 - (lat - clat) * zoom; c.move_to(0, y); c.line_to(W, y)
    c.stroke()
    c.save()
    c.translate(W / 2, H / 2); c.scale(zoom * KX, -zoom); c.translate(-clon, -clat)
    for r in POLYS:
        c.move_to(*r[0])
        for q in r[1:]: c.line_to(*q)
        c.close_path()
    c.restore()
    c.set_source_rgb(0.165, 0.150, 0.128); c.fill_preserve()
    c.set_line_width(2.0); c.set_source_rgb(0.165, 0.150, 0.128); c.stroke()  # hides seams: no borders
    # reference cities for orientation (no borders)
    font(c, 'mono', 22)
    for nm, lo, la in REFS:
        x, y = lonlat_xy(lo, la, clon, clat, zoom)
        if -50 < x < W + 50 and -50 < y < H + 50:
            c.set_source_rgba(*CREAM, 0.45); c.arc(x, y, 5, 0, 2 * math.pi); c.fill()
            c.move_to(x + 12, y + 7); c.show_text(nm)
    grain(c)
ROUTE = ['Mandsaur', 'Jodhpur', 'Baijnath']
def others(c, clon, clat, z, t, cur, t_line=None):
    # earlier stops stay as small pins; dashed route draws from previous stop to current
    i = ROUTE.index(cur)
    for nm in ROUTE[:i]:
        p = PLACES[nm]; x, y = lonlat_xy(p[0], p[1], clon, clat, z)
        c.set_source_rgba(*AMBER, 0.55); c.arc(x, y, 10, 0, 2 * math.pi); c.fill()
    if i > 0 and t_line is not None:
        a = PLACES[ROUTE[i - 1]]; b = PLACES[cur]
        x0, y0 = lonlat_xy(a[0], a[1], clon, clat, z); x1, y1 = lonlat_xy(b[0], b[1], clon, clat, z)
        u = e_io(prog(t, t_line, t_line + 0.8))
        c.set_line_width(5); c.set_dash([14, 12]); c.set_source_rgba(*RED, 0.9)
        c.move_to(x0, y0); c.line_to(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u); c.stroke(); c.set_dash([])
def lonlat_xy(lon, lat, clon, clat, zoom):
    return W / 2 + (lon - clon) * zoom * KX, H / 2 - (lat - clat) * zoom
def pin(c, x, y, t, t0, big=True, col=AMBER):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3))
    pulse = (t - t0) % 1.6 / 1.6
    c.set_source_rgba(*col, 0.35 * (1 - pulse)); c.arc(x, y, 18 + 60 * pulse, 0, 2 * math.pi); c.fill()
    r = (17 if big else 11) * u
    c.set_source_rgb(*BLACK); c.arc(x, y, r + 5, 0, 2 * math.pi); c.fill()
    c.set_source_rgb(*col); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
def place_card(c, name, state, x, y, t, t0, side='r'):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.3))
    font(c, 'head', 54); e = c.text_extents(name.upper()); w = max(e.width, 300) + 60
    xx = x + 40 if side == 'r' else x - 40 - w
    c.save(); c.translate(0, (1 - u) * 30)
    c.set_source_rgba(*CREAM, u); rrect(c, xx, y - 62, w, 124, 16); c.fill()
    c.move_to(xx + 30, y + 4); c.set_source_rgba(*BLACK, u); c.show_text(name.upper())
    mono(c, state, xx + 30, y + 34, 22, (0.55, 0.42, 0.1), a=u, anchor='l')
    c.restore()

# camera path for map scenes: (time, lon, lat, zoom)
INDIA = (78.5, 22.5, 52)
def cam_at(t, keys):
    if t <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t0 <= t <= t1:
            u = e_io(prog(t, t0, t1)); return tuple(x + (y - x) * u for x, y in zip(a, b))
    return keys[-1][1:]

# ---------- icons ----------
def flame(c, x, y, s, a=1.0, t=0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fl = 1 + 0.06 * math.sin(t * 18 + x)
    c.scale(1, fl)
    c.move_to(0, -60); c.curve_to(30, -25, 38, 5, 24, 26); c.curve_to(14, 42, -14, 42, -24, 26)
    c.curve_to(-36, 6, -22, -18, -8, -30); c.curve_to(-6, -14, 4, -10, 0, -60); c.close_path()
    c.set_source_rgba(1.0, 0.45, 0.1, a); c.fill()
    c.move_to(0, -20); c.curve_to(14, 0, 16, 14, 8, 26); c.curve_to(2, 32, -8, 32, -12, 24); c.curve_to(-16, 12, -8, 0, 0, -20)
    c.set_source_rgba(1.0, 0.8, 0.25, a); c.fill(); c.restore()

# ---------- captions ----------
CAP = []
fix = {'him': 'him', 'Him.': 'him.', 'Him': 'him'}
for s, e, w in WORDS:
    w = fix.get(w, w)
    if w == 'pass': CAP.append([s, e, 'pass']); CAP.append([e - 0.05, e + 0.2, 'it,']); continue
    if w.startswith('-'): CAP[-1][2] += w; CAP[-1][1] = e; continue
    CAP.append([s, e, w])
GROUPS = []; g = []
for i, (s, e, w) in enumerate(CAP):
    g.append((s + LEAD, e + LEAD, w))
    nxt = CAP[i + 1][0] if i + 1 < len(CAP) else 99
    if len(g) >= 3 or w[-1] in '.,?!' or nxt - e > 0.35 or sum(len(x[2]) for x in g) > 16:
        GROUPS.append(g); g = []
if g: GROUPS.append(g)
def captions(c, t, y=1395):
    for gi, g in enumerate(GROUPS):
        end = GROUPS[gi + 1][0][0] if gi + 1 < len(GROUPS) else g[-1][1] + 0.6
        if g[0][0] - 0.02 <= t < min(end, g[-1][1] + 0.6):
            words = [x[2].upper().strip(',') for x in g]
            px = 82; font(c, 'head', px)
            sp = c.text_extents(' ').x_advance
            ws = [c.text_extents(w).x_advance for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
            if tot > 900: px = int(px * 900 / tot); font(c, 'head', px); ws = [c.text_extents(w).x_advance for w in words]; sp = c.text_extents(' ').x_advance; tot = sum(ws) + sp * (len(ws) - 1)
            x = W / 2 - tot / 2
            pop = e_back(prog(t, g[0][0], g[0][0] + 0.12));
            for (s, e, _), w, wd in zip(g, words, ws):
                act = s <= t < (e + 0.05)
                c.save(); sc = 0.9 + 0.1 * pop
                c.translate(x + wd / 2, y); c.scale(sc, sc)
                c.set_line_join(cairo.LINE_JOIN_ROUND)
                c.move_to(-wd / 2, px * 0.36); c.text_path(w)
                c.set_source_rgba(0, 0, 0, 0.9); c.set_line_width(px * 0.16); c.stroke_preserve()
                c.set_source_rgb(*(AMBER if act else CREAM)); c.fill()
                c.restore(); x += wd + sp
            break

# ---------- host cues: (time, pose, x, y, size, extra) ----------
def hk(t, pose, x, y, size, **kw): return (t, pose, x, y, size, kw)
HOST = [
    hk(0.0, 'idle', -200, 1230, 240),
    hk(A['women'] - 0.2, 'idle', -200, 1230, 240),
    hk(A['women'] + 0.25, 'curious', 175, 1230, 240),
    hk(A['inlaws'] - 0.3, 'curious', 175, 1230, 240),
    hk(A['inlaws'], 'shocked', 175, 1235, 250),
    hk(A['why'] - 0.32, 'shocked', 175, 1235, 250),
    hk(A['why'] - 0.08, 'curious', W / 2, 1180, 620),
    hk(A['people'] - 0.1, 'curious', W / 2, 1180, 620),
    hk(A['people'] + 0.35, 'point_r', 200, 1225, 230),
    hk(A['son'] - 0.1, 'point_r', 200, 1225, 230),
    hk(A['son'] + 0.15, 'shocked', 200, 1230, 240),
    hk(A['dasara1'] + 0.1, 'thinking', 175, 1230, 230),
    hk(A['but'], 'thinking', 175, 1230, 230),
    hk(A['but'] + 0.3, 'curious', 175, 1230, 230),
    hk(A['jodhpur'], 'point_r', 175, 1230, 230),
    hk(A['funeral'], 'point_r', 175, 1230, 230),
    hk(A['funeral'] + 0.2, 'shocked', 175, 1232, 236),
    hk(A['baijnath'] - 0.2, 'curious', 175, 1230, 230),
    hk(A['devotee'], 'thinking', 175, 1230, 230),
    hk(A['stopped'], 'happy', 175, 1230, 230),
    hk(A['because'] - 0.05, 'curious', 175, 1230, 230),
    hk(A['soyes'] - 0.4, 'curious', 175, 1230, 230),
    hk(A['soyes'] - 0.05, 'curious', W / 2, 1150, 560),
    hk(A['family'] - 0.15, 'shocked', W / 2, 1150, 560),
    hk(A['cta'] - 0.3, 'happy', W / 2, 1270, 360),
    hk(DUR, 'happy', W / 2, 1270, 360),
]
def host_state(t):
    ks = HOST
    if t <= ks[0][0]: a = b = ks[0]; u = 0
    else:
        a = b = ks[-1]; u = 0
        for k0, k1 in zip(ks, ks[1:]):
            if k0[0] <= t <= k1[0]: a, b = k0, k1; u = e_io(prog(t, k0[0], k1[0])); break
    pa, pb = host.POSES[a[1]], host.POSES[b[1]]
    st = dict(pb if u > 0.5 else pa)
    for key in ('tilt', 'sq', 'brow'):
        st[key] = pa[key] + (pb[key] - pa[key]) * u
    st['look'] = tuple(x + (y - x) * u for x, y in zip(pa['look'], pb['look']))
    x = a[2] + (b[2] - a[2]) * u; y = a[3] + (b[3] - a[3]) * u; sz = a[4] + (b[4] - a[4]) * u
    return st, x, y, sz

ENV = None
def voice_env():
    global ENV
    import scipy.io.wavfile as wf
    sr, v = wf.read(ROOT + 'voice.wav'); v = v.astype(np.float32) / 32768
    hop = sr // FPS; n = len(v) // hop
    e = np.sqrt((v[:n * hop].reshape(n, hop) ** 2).mean(1)); e = e / (np.percentile(e, 95) + 1e-9)
    ENV = np.clip(e, 0, 1)
def env_at(t):
    i = int((t - LEAD) * FPS)
    return float(ENV[i]) if 0 <= i < len(ENV) else 0.0

def draw_host(c, t, morph=0.0, glow=0.6):
    st, x, y, sz = host_state(t)
    if x < -100: return
    e = env_at(t)
    st['sq'] = st['sq'] * (1 + 0.05 * e) ; st['tilt'] += 3 * math.sin(t * 2.1) * (0.4 + e)
    yb = y - 6 * e
    # blink
    ph = (t + 0.7) % 3.3
    if ph < 0.12 and st['eye'] in ('open', 'wide'): st['eye'] = 'blink'
    if morph > 0.5: st['eye'] = 'wide'; st['brow'] = 1
    host.draw(c, x, yb, sz, morph=morph, glow=glow + 0.3 * e, **st)

# ---------- series tag ----------
def tag(c):
    font(c, 'monob', 26); txt = 'DUSSEHRA · 5/6'
    e = c.text_extents(txt)
    c.set_source_rgba(0, 0, 0, 0.55); rrect(c, 40, 92, e.x_advance + 84, 56, 12); c.fill()
    c.set_source_rgb(*AMBER); c.arc(68, 120, 9, 0, 2 * math.pi); c.fill()
    c.move_to(88, 129); c.set_source_rgb(*CREAM); c.show_text(txt)

# ---------- frame ----------
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    c.set_source_rgb(*BLACK); c.paint()
    morph = 0.0
    # ---- 1. HOOK: statue photo
    if t < A['why'] - 0.05:
        draw_photo(c, 'mandsaur', t, 0, A['why'], z=(1.12, 1.0) if t < A['women'] else (1.0, 1.10), box=(0, 0, W, 1250), label='Ravana statue, Mandsaur · Samwad India')
        g = cairo.LinearGradient(0, 700, 0, 1250); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.75)
        c.set_source(g); c.rectangle(0, 700, W, 550); c.fill()
        if t >= A['35']:
            u = e_out(prog(t, A['35'], A['35'] + 0.5))
            x = 930; y0, y1 = 220, 1180; yt = y1 - (y1 - y0) * u
            c.set_source_rgba(*AMBER, 0.9); c.set_line_width(4); c.move_to(x, y1); c.line_to(x, yt); c.stroke()
            for k in range(8):
                yy = y1 - (y1 - y0) * k / 7
                if yy >= yt: c.move_to(x - 16, yy); c.line_to(x, yy); c.stroke()
            glowdot(c, x, yt, 12)
            ub = e_back(prog(t, A['35'], A['35'] + 0.3))
            c.save(); c.translate(70, 1150); c.scale(ub, ub)
            font(c, 'head', 230); e = c.text_extents('35 FT'); c.move_to(0, 80); c.text_path('35 FT')
            c.set_source(agrad(0, -100, e.width, 80)); c.fill(); c.restore()
            mono(c, 'SEATED · TEN HEADS · MANDSAUR, MP', 76, 1215, 22, CREAM, a=0.9 * prog(t, A['35'] + 0.2, A['35'] + 0.5), anchor='l', kind='mono')
        if t >= A['women']:
            c.set_source_rgba(0, 0, 0, 0.25 * prog(t, A['women'], A['women'] + 0.2)); c.rectangle(0, 0, W, 1250); c.fill()
            u = card(c, W / 2, 620, 800, 220, t, A['women'], tilt=0)
            head(c, 'WOMEN COVER', 0, -48, 66, CREAM, shadow=False)
            head(c, 'THEIR HEADS', 0, 36, 66, CREAM, shadow=False); c.restore()
        if t >= A['just']:
            c.save(); c.translate(W / 2, 800); c.rotate(0)
            u = e_back(prog(t, A['just'], A['just'] + 0.3)); c.scale(u, u)
            pill(c, 'LIKE IN FRONT OF IN-LAWS', 0, 0, 40, RED, CREAM); c.restore()
    # ---- 2. WHY?
    elif t < A['people']:
        c.set_source_rgb(*BLACK); c.paint()
        g = cairo.RadialGradient(W / 2, 1000, 0, W / 2, 1000, 700); g.add_color_stop_rgba(0, *AMBER, 0.18); g.add_color_stop_rgba(1, *AMBER, 0)
        c.set_source(g); c.paint()
        head(c, 'WHY?', W / 2, 470, 150, CREAM)
    # ---- 3. MANDSAUR map
    elif t < A['dasara1']:
        p = PLACES['Mandsaur']
        clon, clat, z = cam_at(t, [(A['people'], *INDIA), (A['people'] + 1.0, p[0], p[1] - 180/78, 78)])
        draw_map(c, clon, clat, z, t)
        x, y = lonlat_xy(p[0], p[1], clon, clat, z)
        pin(c, x, y, t, A['people'] + 0.8)
        place_card(c, 'Mandsaur', p[2], x, y, t, A['people'] + 1.0, side='r' if x < W / 2 else 'l')
        # family link card
        if t >= A['mandodari']:
            u = card(c, W / 2, 400, 860, 300, t, A['mandodari'], tilt=-1.5)
            mono(c, 'TRADITION SAYS', 0, -105, 24, AMBER, anchor='c')
            head(c, "MANDODARI'S", 0, -32, 64, CREAM, shadow=False)
            head(c, 'HOMETOWN', 0, 46, 64, CREAM, shadow=False)
            c.restore()
        polaroid(c, 'mandsaur2', W - 300, 880, 360, t, T('was') - 0.05, rot=6)
        stamp(c, 'SON-IN-LAW', W / 2, 1150, t, A['son'] - 0.05, px=74)
    # ---- 4. "we burn him... but places pray"
    elif t < A['jodhpur']:
        if t < A['but']:
            draw_video(c, t, A['dasara1'], 1.0)
        else:
            clon, clat, z = INDIA
            draw_map(c, clon, clat, z, t)
            # flames across India for 'burn' then pins
            import random; rnd = random.Random(4)
            pts = [(rnd.uniform(70, 88), rnd.uniform(12, 30)) for _ in range(40)]
            pts = [p for p in pts if not (p[0] < 72 and p[1] < 20)]
            for i, (lo, la) in enumerate(pts):
                x, y = lonlat_xy(lo, la, clon, clat, z)
                fa = 1 - prog(t, A['pray1'] - 0.2, A['pray1'] + 0.3) * 0.75
                flame(c, x, y, 0.45, a=0.85 * fa * prog(t, A['but'] + i * 0.02, A['but'] + i * 0.02 + 0.2), t=t)
            for i, nm in enumerate(['Bisrakh', 'Mandsaur', 'Jodhpur', 'Baijnath', 'Kanpur']):
                p = PLACES[nm]; x, y = lonlat_xy(p[0], p[1], clon, clat, z)
                pin(c, x, y, t, A['pray1'] - 0.15 + i * 0.12, big=False)
            if t >= A['pray1']:
                u = card(c, W / 2, 420, 640, 150, t, A['pray1'], tilt=1.5)
                head(c, 'THEY PRAY', 0, 0, 72, CREAM, shadow=False); c.restore()
    # ---- 5. JODHPUR
    elif t < A['dasara2']:
        p = PLACES['Jodhpur']
        clon, clat, z = cam_at(t, [(A['jodhpur'], *INDIA), (A['jodhpur'] + 0.9, p[0] + 1.2, p[1] - 180/78, 78)])
        draw_map(c, clon, clat, z, t)
        others(c, clon, clat, z, t, 'Jodhpur', A['jodhpur'] + 0.1)
        x, y = lonlat_xy(p[0], p[1], clon, clat, z)
        pin(c, x, y, t, A['jodhpur'] + 0.6)
        place_card(c, 'Jodhpur', p[2], x, y, t, A['jodhpur'] + 0.8, side='l' if x > W / 2 else 'r')
        # lineage graphic
        if t >= A['devgoda'] - 0.1:
            u = card(c, W / 2, 420, 860, 470, t, A['devgoda'] - 0.1, tilt=-1)
            mono(c, 'THE DEVGODA CLAN', 0, -185, 30, AMBER)
            nodes = [('RAVANA', -120), ('...', 0), ('DEVGODA', 120)]
            for i, (nm, yy) in enumerate(nodes):
                tt = A['devgoda'] + 0.25 + i * 0.35 if nm != 'RAVANA' else A['descend'] - 0.6
                if nm == 'RAVANA': tt = A['devgoda'] + 0.1
                if t < tt: continue
                if nm == '...':
                    c.set_source_rgb(*BLACK); c.set_line_width(5); c.set_dash([10, 12])
                    c.move_to(0, -80); c.line_to(0, -80 + 160 * e_out(prog(t, tt, tt + 0.4))); c.stroke(); c.set_dash([])
                else:
                    pill(c, nm, 0, yy, 48, BLACK if nm == 'RAVANA' else AMBER, CREAM if nm == 'RAVANA' else BLACK, s=e_back(prog(t, tt, tt + 0.25)))
            c.restore()
            if t >= A['descend']:
                stamp(c, 'DESCENDANTS', W / 2, 700, t, A['descend'], col=AMBER, px=64, rot=6)
    # ---- 6. Funeral bath
    elif t < A['baijnath'] - 0.35:
        if t < A['bath'] - 0.1:
            draw_video(c, t, A['dasara2'], 12.0)
            if t >= A['city']:
                pill(c, 'THE CITY BURNS HIM', W / 2, 360, 46, CREAM, BLACK, s=e_back(prog(t, A['city'], A['city'] + 0.25)))
        else:
            tg = T('go') - 0.1
            if t < tg:
                draw_photo(c, 'jodhpur_idol', t, A['bath'] - 0.1, tg + 3, z=(1.0, 1.08), full=True, focus=(0.4, 0.4), label='Ravana idol, Mandore · Mediawala')
                c.set_source_rgba(0, 0, 0, 0.35); c.paint()
            else:
                draw_photo(c, 'jodhpur_worship', t, tg, A['baijnath'], z=(1.0, 1.1), full=True, label='Ravana temple, Mandore, Jodhpur · Mediawala')
                c.set_source_rgba(0, 0, 0, 0.3); c.paint()
            pill(c, 'ON DUSSEHRA · THE DEVGODA FAMILIES', W / 2, 260, 26, BLACK, AMBER, kind='monob')
            rows = [('1', 'BATH, LIKE AFTER', 'A FUNERAL', A['bath'] - 0.05), ('2', 'PRAY AT THEIR', 'OWN RAVANA TEMPLE', A['pray1'] + 0 if False else T('go', 1) - 0.1)]
            for i, (n, l1, l2, tt) in enumerate(rows):
                if t < tt: continue
                u = card(c, W / 2, 520 + i * 330, 900, 270, t, tt, tilt=(-1.2 if i == 0 else 1.2))
                c.set_source_rgb(*AMBER); c.arc(-350, 0, 54, 0, 2 * math.pi); c.fill()
                head(c, n, -350, 0, 64, BLACK, shadow=False)
                head(c, l1, 70, -38, 52, CREAM, shadow=False)
                head(c, l2, 70, 38, 52, CREAM, shadow=False)
                c.restore()
            if t >= A['funeral']:
                marker_underline(c, 470, 755, 566, t, A['funeral'] + 0.05, col=AMBER)
            if t >= A['temple1'] - 0.15:
                marker_circle(c, W / 2 + 70, 885, 330, 62, t, A['temple1'] - 0.15)
    # ---- 7. BAIJNATH
    elif t < A['so']:
        p = PLACES['Baijnath']
        if t < A['penance'] - 0.25:
            clon, clat, z = cam_at(t, [(A['baijnath'] - 0.35, *INDIA), (A['baijnath'] + 0.7, p[0] - 0.8, p[1] - 180/78, 78)])
            draw_map(c, clon, clat, z, t)
            others(c, clon, clat, z, t, 'Baijnath', A['baijnath'] - 0.2)
            x, y = lonlat_xy(p[0], p[1], clon, clat, z)
            pin(c, x, y, t, A['baijnath'] + 0.4)
            place_card(c, 'Baijnath', p[2], x, y, t, A['baijnath'] + 0.6, side='l' if x > W / 2 else 'r')
        else:
            draw_photo(c, 'baijnath', t, A['penance'] - 0.25, A['so'], z=(1.0, 1.1), full=True, label='Baijnath temple · Sachin Sonkusare · Wikimedia Commons')
            c.set_source_rgba(0, 0, 0, 0.2); c.paint()
            if t >= A['penance']:
                u = card(c, W / 2, 470, 820, 240, t, A['penance'], tilt=-1.5)
                mono(c, 'TRADITION SAYS', 0, -78, 24, AMBER)
                head(c, 'RAVANA PRAYED', 0, -10, 58, CREAM, shadow=False)
                head(c, 'TO SHIVA HERE', 0, 62, 58, CREAM, shadow=False)
                c.restore()
    # ---- 8. Shiva's devotee: Ellora relief, then no-burn verdict
    elif t < A['because']:
        draw_photo(c, 'baijnath', t, A['so'], A['because'], z=(1.25, 1.12), full=True, focus=(0.42, 0.4), label='Baijnath temple · Sachin Sonkusare · Wikimedia Commons')
        c.set_source_rgba(0, 0, 0, 0.25); c.paint()
        if t >= A['devotee'] - 0.2:
            pill(c, "SHIVA'S BIGGEST DEVOTEE", W / 2, 360, 44, AMBER, BLACK, s=e_back(prog(t, A['devotee'] - 0.2, A['devotee'] + 0.05)))
        if t >= A['stopped'] - 0.3:
            fx, fy = W / 2, 860
            flame(c, fx, fy, 2.4, a=0.95, t=t)
            stamp(c, 'NO BURNING', fx, fy + 40, t, A['stopped'], px=80, rot=-10)
    # ---- 9. not only a villain
    elif t < A['soyes'] - 0.1:
        draw_photo(c, 'ravivarma', t, A['because'], A['soyes'], z=(1.0, 1.08), full=True, focus=(0.5, 0.35), label='Jatayu Vadham, Raja Ravi Varma, 1895 · Public domain')
        c.set_source_rgba(0, 0, 0, 0.45); c.paint()
        tv = A['villain'] - 0.1
        if t >= T('ravana', 1, after=A['because'] - LEAD) - 0.05:
            head(c, 'VILLAIN', W / 2, 420, 120, CREAM)
        if t >= tv:
            c.set_line_width(10); c.set_source_rgba(*AMBER, 0.95); u = e_out(prog(t, tv, tv + 0.25))
            c.move_to(W / 2 - 290, 430); c.line_to(W / 2 - 290 + 580 * u, 410); c.stroke()
        for i, wd in enumerate(['SCHOLAR', 'SHIVA DEVOTEE', 'KING']):
            tt = A['villain'] + 0.25 + i * 0.22
            pill(c, wd, W / 2, 620 + i * 120, 44, CREAM, BLACK, s=e_back(prog(t, tt, tt + 0.25)), a=1.0 if t >= tt else 0)
    # ---- 10. PAYOFF
    elif t < A['cta'] - 0.3:
        c.set_source_rgb(*BLACK); c.paint()
        uf = prog(t, A['family'] - 0.1, A['family'] + 0.45)
        morph = e_io(uf)
        g = cairo.RadialGradient(W / 2, 950, 0, W / 2, 950, 900); g.add_color_stop_rgba(0, *AMBER, 0.12 + 0.25 * morph); g.add_color_stop_rgba(1, *AMBER, 0)
        c.set_source(g); c.paint()
        for i in range(14):
            ang = i / 14 * 2 * math.pi + t * 0.15
            c.set_source_rgba(*AMBER, 0.06 * morph); c.set_line_width(46)
            c.move_to(W / 2, 950); c.line_to(W / 2 + math.cos(ang) * 1500, 950 + math.sin(ang) * 1500); c.stroke()
        if t >= A['soyes']:
            mono(c, 'IN THESE PLACES, RAVANA IS', W / 2, 330, 30, CREAM, a=prog(t, A['soyes'], A['soyes'] + 0.3))
        if t >= A['family']:
            u = e_back(prog(t, A['family'], A['family'] + 0.3))
            c.save(); c.translate(W / 2, 470); c.scale(u, u)
            font(c, 'head', 180); e = c.text_extents('FAMILY'); c.move_to(-e.width / 2 - e.x_bearing, 65); c.text_path('FAMILY')
            c.set_source(agrad(-e.width / 2, -60, e.width / 2, 60)); c.fill(); c.restore()
    # ---- 11. CTA
    else:
        c.set_source_rgb(*BLACK); c.paint()
        morph = 1.0 - e_io(prog(t, A['cta'] - 0.3, A['cta'] + 0.3))
        g = cairo.RadialGradient(W / 2, 900, 0, W / 2, 900, 800); g.add_color_stop_rgba(0, *AMBER, 0.16); g.add_color_stop_rgba(1, *AMBER, 0)
        c.set_source(g); c.paint()
        typed(c, 'GOT A WHY?', W / 2, 330, 120, t, A['cta'] + 0.1, cps=16, col=CREAM)
        if t >= A['comment']:
            pill(c, 'COMMENT IT BELOW', W / 2, 520, 50, AMBER, BLACK, s=e_back(prog(t, A['comment'], A['comment'] + 0.25)))
        if t >= A['research']:
            mono(c, "WE'LL FIND THE ANSWER", W / 2, 640, 30, CREAM, a=prog(t, A['research'], A['research'] + 0.3))
    # host (not over full photo-only hook start)
    in_payoff = A['soyes'] - 0.1 <= t
    if (A['why'] - 0.1 <= t < A['people'] + 0.15) or t >= A['soyes'] - 0.1:
        draw_host(c, t, morph=morph, glow=0.6)
    guide(c, t)
    # captions band
    if t >= LEAD - 0.01 and not (A['why'] - 0.05 <= t < A['people']):
        captions(c, t, y=1450 if (A['soyes'] - 0.1 <= t) else 1395)
    tag(c)
    return s

# ================= STYLE v2 overrides: dark glass + amber light guide + highlighter =================
host._eye = lambda *a, **k: None
AMBER2 = (1.0, 0.52, 0.18); INK = (0.08, 0.08, 0.09)
def agrad(x0, y0, x1, y1):
    g = cairo.LinearGradient(x0, y0, x1, y1); g.add_color_stop_rgb(0, *AMBER); g.add_color_stop_rgb(1, *AMBER2); return g
def glowdot(c, x, y, r=14, a=1.0):
    g = cairo.RadialGradient(x, y, 0, x, y, r * 5); g.add_color_stop_rgba(0, *AMBER, 0.6 * a); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.arc(x, y, r * 5, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(*AMBER, a); c.arc(x, y, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(1, 1, 1, 0.9 * a); c.arc(x, y, r * 0.4, 0, 2 * math.pi); c.fill()
def glass_dark(c, x, y, w, h, r=28, a=1.0):
    rrect(c, x, y, w, h, r); c.set_source_rgba(0.06, 0.06, 0.08, 0.62 * a); c.fill_preserve()
    c.set_source_rgba(1, 1, 1, 0.22 * a); c.set_line_width(2); c.stroke()
def card(c, cx, cy, w, h, t, t0, a=1.0, tilt=0):
    u = e_out(prog(t, t0, t0 + 0.3)) if t >= t0 else 0
    c.save(); c.translate(cx, cy + (1 - u) * 50)
    glass_dark(c, -w / 2, -h / 2, w, h, 28, u)
    c.set_source_rgba(*AMBER, u); c.rectangle(-w / 2 + 22, -h / 2 + 22, 6, h - 44); c.fill()  # amber edge bar
    return u
def pill(c, txt, cx, cy, px=34, fill=AMBER, col=BLACK, a=1.0, s=1.0, kind='head'):
    if a <= 0: return
    c.save(); c.translate(cx, cy); c.scale(s, s)
    font(c, kind, px); e = c.text_extents(txt); w = e.width + px * 1.3; h = px * 1.75
    if fill == CREAM:
        glass_dark(c, -w / 2, -h / 2, w, h, h / 2, a); tc = CREAM
    elif fill in (RED, AMBER):
        g = cairo.RadialGradient(0, 0, 0, 0, 0, w * 0.75); g.add_color_stop_rgba(0, *AMBER, 0.3 * a); g.add_color_stop_rgba(1, *AMBER, 0)
        c.set_source(g); c.arc(0, 0, w * 0.75, 0, 2 * math.pi); c.fill()
        rrect(c, -w / 2, -h / 2, w, h, h / 2); c.set_source(agrad(-w / 2, 0, w / 2, 0)); c.fill(); tc = INK
    else:
        rrect(c, -w / 2, -h / 2, w, h, h / 2); c.set_source_rgba(*fill, a); c.fill(); tc = col
    c.move_to(-e.width / 2 - e.x_bearing, px * 0.36); c.set_source_rgba(*tc, a); c.show_text(txt)
    c.restore()
def stamp(c, txt, cx, cy, t, t0, col=AMBER, px=70, rot=0):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3))
    pill(c, txt, cx, cy, int(px * 0.8), AMBER, INK, s=u)
def marker_underline(c, x0, x1, y, t, t0, dur=0.35, col=AMBER, wdt=10):
    u = e_out(prog(t, t0, t0 + dur))
    if u <= 0: return
    xe = x0 + (x1 - x0) * u
    c.save(); c.set_source_rgba(*AMBER, 0.45)
    c.move_to(x0 - 6, y - 30); c.curve_to(x0 + (xe - x0) * 0.4, y - 34, x0 + (xe - x0) * 0.7, y - 27, xe + 8, y - 31)
    c.line_to(xe + 4, y + 6); c.curve_to(x0 + (xe - x0) * 0.6, y + 9, x0 + (xe - x0) * 0.3, y + 3, x0 - 2, y + 7); c.close_path(); c.fill()
    c.restore()
def marker_circle(c, cx, cy, rx, ry, t, t0, dur=0.45, col=AMBER):
    u = e_out(prog(t, t0, t0 + dur))
    if u <= 0: return
    c.save(); c.set_source_rgba(*AMBER, 0.28); c.translate(cx, cy); c.scale(rx, ry)
    c.rectangle(-1, -0.8, 2 * u, 1.6); c.restore(); c.fill()
def polaroid(c, name, cx, cy, w, t, t0, rot=0):
    if t < t0: return
    (_, _), (sharp, _), _ = photo(name)
    u = e_out(prog(t, t0, t0 + 0.35)); h = w * 0.72
    c.save(); c.translate(cx, cy + (1 - u) * 60)
    c.save(); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip()
    sw, sh = sharp.get_width(), sharp.get_height(); sc = max(w / sw, h / sh)
    c.save(); c.scale(sc, sc); c.translate(-sw / 2, -sh / 2); c.set_source_surface(sharp, 0, 0); c.paint_with_alpha(u); c.restore()
    g = cairo.LinearGradient(0, h * 0.1, 0, h / 2); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.7)
    c.set_source(g); c.paint_with_alpha(u); c.restore()
    rrect(c, -w / 2, -h / 2, w, h, 22); c.set_source_rgba(1, 1, 1, 0.4 * u); c.set_line_width(2); c.stroke()
    mono(c, 'THE STATUE · MANDSAUR', -w / 2 + 24, h / 2 - 30, 20, CREAM, a=u, anchor='l', kind='mono')
    c.restore()
def pin(c, x, y, t, t0, big=True, col=AMBER):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3)); pulse = (t - t0) % 1.8 / 1.8
    c.set_source_rgba(*AMBER, 0.25 * (1 - pulse)); c.arc(x, y, 20 + 90 * pulse, 0, 2 * math.pi); c.fill()
    glowdot(c, x, y, (15 if big else 9) * u)
def place_card(c, name, state, x, y, t, t0, side='r'):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.3))
    font(c, 'head', 60); e = c.text_extents(name.upper()); w = max(e.width, 330) + 64
    xx = x + 46 if side == 'r' else x - 46 - w
    c.save(); c.translate((1 - u) * (24 if side == 'r' else -24), 0)
    glass_dark(c, xx, y - 66, w, 132, 22, u)
    c.move_to(xx + 32, y + 6); c.set_source_rgba(*CREAM, u); c.show_text(name.upper())
    mono(c, state, xx + 32, y + 38, 20, AMBER, a=u, anchor='l', kind='mono')
    c.restore()
def others(c, clon, clat, z, t, cur, t_line=None):
    i = ROUTE.index(cur)
    for nm in ROUTE[:i]:
        p = PLACES[nm]; x, y = lonlat_xy(p[0], p[1], clon, clat, z); glowdot(c, x, y, 7, 0.6)
    if i > 0 and t_line is not None:
        a = PLACES[ROUTE[i - 1]]; b = PLACES[cur]
        x0, y0 = lonlat_xy(a[0], a[1], clon, clat, z); x1, y1 = lonlat_xy(b[0], b[1], clon, clat, z)
        u = e_io(prog(t, t_line, t_line + 0.8))
        c.set_line_width(4); c.set_dash([4, 12]); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgba(*AMBER, 0.9)
        c.move_to(x0, y0); c.line_to(x0 + (x1 - x0) * u, y0 + (y1 - y0) * u); c.stroke(); c.set_dash([]); c.set_line_cap(cairo.LINE_CAP_BUTT)
        glowdot(c, x0 + (x1 - x0) * u, y0 + (y1 - y0) * u, 8, 1 - prog(t, t_line + 0.8, t_line + 1.0))
def tag(c):
    font(c, 'monob', 24); txt = 'DUSSEHRA · 5/6'; e = c.text_extents(txt)
    glass_dark(c, 40, 92, e.x_advance + 80, 54, 27); glowdot(c, 68, 119, 7)
    c.move_to(88, 128); c.set_source_rgb(*CREAM); c.show_text(txt)
def captions(c, t, y=1395):
    for gi, g in enumerate(GROUPS):
        end = GROUPS[gi + 1][0][0] if gi + 1 < len(GROUPS) else g[-1][1] + 0.6
        if g[0][0] - 0.02 <= t < min(end, g[-1][1] + 0.6):
            words = [x[2].upper().strip(',') for x in g]
            px = 80; font(c, 'head', px); sp = c.text_extents(' ').x_advance
            ws = [c.text_extents(w).x_advance for w in words]; tot = sum(ws) + sp * (len(ws) - 1)
            if tot > 900:
                px = int(px * 900 / tot); font(c, 'head', px); ws = [c.text_extents(w).x_advance for w in words]; sp = c.text_extents(' ').x_advance; tot = sum(ws) + sp * (len(ws) - 1)
            x = W / 2 - tot / 2; pop = e_out(prog(t, g[0][0], g[0][0] + 0.12))
            for (s, e, _), w, wd in zip(g, words, ws):
                act = s <= t < (e + 0.05)
                c.save(); c.translate(x, y + (1 - pop) * 14)
                c.move_to(0, px * 0.36); c.text_path(w); c.set_line_join(cairo.LINE_JOIN_ROUND)
                c.set_source_rgba(0, 0, 0, 0.85); c.set_line_width(px * 0.15); c.stroke_preserve()
                if act: c.set_source(agrad(0, 0, wd, 0))
                else: c.set_source_rgb(*CREAM)
                c.fill(); c.restore(); x += wd + sp
            break

# guide: the amber dot that travels to whatever matters
def _guide_keys():
    a = A; Wc = W / 2
    return [
        (a['35'] + 0.5, None),
        (a['women'], (Wc - 440, 620)), (a['just'], (Wc - 395, 800)), (a['why'] - 0.25, (Wc, 1180)), (a['why'] + 0.1, None),
        (a['people'] + 0.15, (Wc, 1180)), (a['people'] + 0.6, (Wc, 780)), (a['people'] + 0.95, None),
        (a['mandodari'], (Wc - 470, 400)), (T('was') - 0.05, (Wc + 70, 880)), (a['son'] - 0.1, (Wc - 250, 1150)), (a['dasara1'] - 0.05, None),
        (a['pray1'], (Wc - 330, 420)), (a['jodhpur'] - 0.05, None),
        (a['devgoda'] - 0.1, (Wc - 470, 420)), (a['descend'], (Wc - 260, 700)), (a['dasara2'] - 0.05, None),
        (a['city'], (Wc - 300, 360)), (a['bath'] - 0.05, (Wc - 470, 520)), (T('go') - 0.1, (Wc - 470, 850)), (a['temple1'] + 0.4, None),
        (a['penance'], (Wc - 450, 470)), (a['so'] - 0.05, None),
        (a['devotee'] - 0.2, (Wc - 330, 360)), (a['stopped'] - 0.3, (Wc, 860)), (a['because'] - 0.05, None),
        (a['because'] + 0.2, (Wc - 330, 420)), (a['villain'] + 0.25, (Wc - 200, 620)), (a['villain'] + 0.47, (Wc - 260, 740)), (a['villain'] + 0.69, (Wc - 150, 860)),
        (a['soyes'] - 0.3, (Wc, 1150)), (a['soyes'] + 0.05, None),
    ]
GUIDE = None
def guide_pos(t):
    global GUIDE
    if GUIDE is None: GUIDE = _guide_keys()
    k = None
    for i, (tk, p) in enumerate(GUIDE):
        if tk <= t: k = i
    if k is None or GUIDE[k][1] is None: return None
    tk, p = GUIDE[k]
    prev = GUIDE[k - 1][1] if k > 0 else None
    if prev is not None and t - tk < 0.4:
        u = e_io(prog(t, tk, tk + 0.4)); x = prev[0] + (p[0] - prev[0]) * u; y = prev[1] + (p[1] - prev[1]) * u
        y -= math.sin(u * math.pi) * 60
        return x, y, 1.0
    a = prog(t, tk, tk + 0.2) if prev is None else 1.0
    return p[0], p[1] + 4 * math.sin(t * 3.0), a
def guide(c, t):
    for k in range(5, 0, -1):
        q = guide_pos(t - 0.025 * k)
        if q: c.set_source_rgba(*AMBER, 0.12 * (6 - k) / 5 * q[2]); c.arc(q[0], q[1], 13 - k, 0, 2 * math.pi); c.fill()
    q = guide_pos(t)
    if q: glowdot(c, q[0], q[1], 13, q[2])


def main(part=0, parts=1, out=None, still=None):
    voice_env()
    if still is not None:
        for tt in still:
            frame(tt).write_to_png(f'{ROOT}stills2/f_{tt:05.2f}.png')
        return
    n = int(DUR * FPS); a = n * part // parts; b = n * (part + 1) // parts
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        s = frame(i / FPS); s.flush()
        p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    if sys.argv[1] == 'still':
        os.makedirs(ROOT + 'stills2', exist_ok=True)
        main(still=[float(x) for x in sys.argv[2:]])
    else:
        main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
