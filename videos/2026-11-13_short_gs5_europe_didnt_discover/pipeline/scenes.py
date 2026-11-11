# ------------------------------------------------------------------ GS 5/6 scenes ("Europe didn't discover India")
# Sharp-pictures rule: every source image is shown at <= 1.0 source px per output px; maps and graphics are drawn at output size.
ARC = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/archive/'
EV = '/home/claude/gs5/src/'
DUSK = (16, 16, 15); MUTED = (170, 164, 150); PARCH = (226, 210, 172); GOLD_A = (196, 160, 92)
def sm_(x): x = clamp(x); return x * x * (3 - 2 * x)

SRC = {'ROTEIRO': (ARC + '09_PD11_Roteiro_da_primeira_viagem_de_Vasco_da_Gama.jpg', None),
       'COIN': (ARC + '12_PD19_Gold_Aureus_of_Nerva_MANTIS.jpg', None),
       'BARROS': (EV + 'barros_p1.jpg', None)}
@functools.lru_cache(8)
def NAT(key):
    p, cr = SRC[key]; im = Image.open(p).convert('RGB')
    if cr: im = im.crop(cr)
    return im

def panel_nat(img, key, box, u, f0, f1, sc=1.0, radius=18, a=1.0, border=None, tint=None):
    """native-pixel window: a box-sized region of the source at scale sc (<= 1), panning f0 -> f1"""
    assert sc <= 1.0001, (key, sc)
    im = NAT(key); x0, y0, x1, y1 = [int(v) for v in box]; bw, bh = x1 - x0, y1 - y0; sw, sh = bw / sc, bh / sc
    k = e_io(clamp(u)); fx, fy = lerp(f0[0], f1[0], k), lerp(f0[1], f1[1], k)
    cx = min(max(fx * im.width, sw / 2), im.width - sw / 2); cy = min(max(fy * im.height, sh / 2), im.height - sh / 2)
    crop = im.resize((bw, bh), Image.LANCZOS, box=(cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2))
    if tint: crop = Image.fromarray(np.clip(np.asarray(crop).astype(np.float32) * np.array(tint) / 255, 0, 255).astype(np.uint8))
    shadow(img, box, a)
    if border:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0 - 3, y0 - 3, x1 + 3, y1 + 3), radius + 3, fill=border + (int(255 * a),)); img.paste(lay, (0, 0), lay)
    m = Image.new('L', (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), radius, fill=int(255 * a))
    img.paste(crop, (x0, y0), m); LY.reg('image', (x0, y0, x1, y1), owner=key)

def shadow(img, box, a=1.0, r=22, o=12):
    if a <= .02: return
    x0, y0, x1, y1 = box; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(lay).rounded_rectangle((x0 + 4, y0 + o, x1 + 4, y1 + o), 18, fill=(0, 0, 0, int(150 * a)))
    lay = lay.filter(ImageFilter.GaussianBlur(r)); img.paste(lay, (0, 0), lay)

def small(img, s, x, y, px=24, col=MUTED, anchor='mm', a=1.0, maxw=None):
    text(img, s, x, y, px, col, anchor, 'monob', a, maxw or ST.sw, None)

def rule_frame(d, box, a):
    x0, y0, x1, y1 = box; c1 = GOLD_A + (int(230 * a),); c2 = GOLD_A + (int(140 * a),)
    d.rectangle(box, outline=c1, width=2); d.rectangle((x0 + 9, y0 + 9, x1 - 9, y1 - 9), outline=c2, width=1)
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):
        d.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)], fill=GOLD_A + (int(255 * a),))

def plate(img, box, a=1.0, rule=True, fill=INK, alpha=222):
    if a <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rectangle(box, fill=fill + (int(alpha * a),))
    if rule: rule_frame(d, box, a)
    img.paste(lay, (0, 0), lay)

def plate_text(img, box, kicker, title, a=1.0, px=44, owner=None, sub=None, tcol=CREAM, kcol=AMBER):
    """ink plate: kicker (mono, amber) + title (head, cream) + sub (mono, muted); registers box and ink"""
    if a <= .01: return
    plate(img, box, a); x0, y0, x1, y1 = box; inner = x1 - x0 - 70; cx = (x0 + x1) / 2
    lines = wrap(title, 'head', px, inner); f = pick(title, 'head', px); lh = px + 12
    kpx = 24 if not TE else 27; spx = 22 if not TE else 24
    block = (kpx + 16 if kicker else 0) + len(lines) * lh + (spx + 18 if sub else 0); y = (y0 + y1) / 2 - block / 2
    if kicker: small(img, kicker, cx, y + kpx / 2, kpx, kcol, 'mm', a, inner); y += kpx + 16
    ink = None
    for ln in lines:
        yy = y + lh / 2; text(img, ln, cx, yy, px, tcol, 'mm', 'head', a, None, None)
        bb = f.getbbox(ln, anchor='mm'); r = (cx + bb[0], yy + bb[1], cx + bb[2], yy + bb[3]); y += lh
        ink = r if ink is None else (min(ink[0], r[0]), min(ink[1], r[1]), max(ink[2], r[2]), max(ink[3], r[3]))
    if sub: small(img, sub, cx, y + 8 + spx / 2, spx, MUTED, 'mm', a, inner)
    LY.reg('card', box, ink, owner=owner or title)

def map_label(img, s, x, y, px=28, col=INK, a=1.0, bg=(244, 236, 214)):
    if a <= .01: return
    f = pick(s, 'monob', px); w = f.getlength(s) + 26; x0 = min(max(x - w / 2, 48), W - 48 - w)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0, y - px * .85, x0 + w, y + px * .85), 9, fill=bg + (int(232 * a),))
    img.paste(lay, (0, 0), lay); text(img, s, x0 + w / 2, y, px, col, 'mm', 'monob', a, None, None)
    LY.reg('label', (x0, y - px * .85, x0 + w, y + px * .85), owner=s)

def pin(img, x, y, k, col=AMBER, r=13, pulse=None):
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if pulse is not None:
        pr = r + 34 * (pulse % 1.0); d.ellipse((x - pr, y - pr, x + pr, y + pr), outline=col + (int(170 * (1 - pulse % 1.0) * k),), width=3)
    rr = r * e_back(min(1, k)); d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=col + (int(255 * min(1, k)),), outline=(20, 16, 10, int(255 * min(1, k))), width=3)
    img.paste(lay, (0, 0), lay)

# ------------------------------------------------------------------ the map (real coastlines, drawn at output size)
def _smooth(pts, n=10):
    """Catmull-Rom through the points (screen space)"""
    if len(pts) < 3: return pts
    P = [pts[0]] + pts + [pts[-1]]; out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for j in range(n):
            t = j / n; t2, t3 = t * t, t * t * t
            out.append(tuple(.5 * ((2 * p1[c]) + (-p0[c] + p2[c]) * t + (2 * p0[c] - 5 * p1[c] + 4 * p2[c] - p3[c]) * t2 + (-p0[c] + 3 * p1[c] - 3 * p2[c] + p3[c]) * t3) for c in (0, 1)))
    out.append(pts[-1]); return out

def poly_len(pts): return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
def poly_at(pts, f):
    """point and direction at fraction f of the polyline length"""
    tot = poly_len(pts) * clamp(f)
    for a, b in zip(pts, pts[1:]):
        s = math.dist(a, b)
        if tot <= s or b == pts[-1]:
            q = 0 if s == 0 else min(1, tot / s); return (lerp(a[0], b[0], q), lerp(a[1], b[1], q)), math.atan2(b[1] - a[1], b[0] - a[0])
        tot -= s
    return pts[-1], 0.0
def poly_part(pts, k):
    if k <= 0: return []
    tot = poly_len(pts) * min(1, k); out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        s = math.dist(a, b)
        if tot <= 0: break
        q = min(1, tot / s) if s else 1; out.append((lerp(a[0], b[0], q), lerp(a[1], b[1], q))); tot -= s
    return out

class OMap:
    """Indian Ocean map at output size: all coastlines, muted sea/land; land mask for the wind field"""
    def __init__(self, lon0, lon1, latc):
        self.s = W / ((lon1 - lon0) * gsmap.AX); self.x0 = gsmap.to_svg(lon0, 0)[0]; self.yc = gsmap.to_svg(0, latc)[1]
        SS = 2; im = Image.new('RGB', (W * SS, H * SS), (108, 128, 130)); d = ImageDraw.Draw(im); lm = Image.new('L', (W * SS, H * SS), 0); dl = ImageDraw.Draw(lm)
        for f in gsmap.GEO['features']:
            for q in gsmap.polys(f['properties']['name']):
                if len(q) > 2:
                    pts = [(x * SS, y * SS) for x, y in self._tr(q)]; d.polygon(pts, fill=(170, 156, 124), outline=(128, 114, 88)); dl.polygon(pts, fill=255)
        im = im.resize((W, H), Image.LANCZOS); a = np.asarray(im).astype(np.float32)
        yy, xx = np.mgrid[0:H, 0:W]; r = np.sqrt(((xx - W / 2) / (W * .8)) ** 2 + ((yy - H * .48) / (H * .62)) ** 2); a *= np.clip(1.12 - .5 * r, .4, 1)[..., None]
        self.base = Image.fromarray(np.clip(a * .9, 0, 255).astype(np.uint8)); self.land = np.asarray(lm.resize((W, H), Image.BILINEAR)) > 100
    def _tr(self, q): return [((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s) for x, y in q]
    def P(self, lon, lat):
        x, y = gsmap.to_svg(lon, lat); return ((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s)
    def path(self, ll, n=10): return _smooth([self.P(*p) for p in ll], n)

MAP_A = (34.0, 102.0, 5.0)      # the whole ocean
MAP_B = (34.0, 90.0, 7.0)        # Malindi -> Calicut -> Gujarat
@functools.lru_cache(64)
def OM(lon0, lon1, latc): return OMap(lon0, lon1, latc)
def om_lerp(k, steps=24):
    q = round(clamp(k) * steps) / steps
    return OM(*(round(lerp(a, b, q), 3) for a, b in zip(MAP_A, MAP_B)))

# trade routes (lon, lat) – illustrative examples of documented routes c. 1400–1500; drawn over water
ROUTES = {
 'INDIAN':  [[(72.5, 21.6), (70.6, 17.5), (73.2, 9.5), (77.5, 5.6), (82.0, 5.4), (92.0, 6.2), (98.0, 4.6), (102.2, 2.2)],
             [(75.7, 11.2), (66.0, 12.6), (55.0, 13.2), (45.3, 12.3)], [(72.5, 21.6), (66.5, 22.6), (60.0, 24.2), (56.6, 26.4)]],
 'ARAB':    [[(45.0, 12.6), (52.0, 11.5), (62.0, 10.5), (70.0, 10.8), (75.6, 11.2)], [(45.0, 12.6), (49.0, 10.8), (51.5, 7.0), (47.0, 1.0), (41.5, -2.6)],
             [(39.2, 21.4), (41.0, 17.0), (43.3, 12.9), (45.0, 12.6)]],
 'PERSIAN': [[(56.5, 26.5), (58.5, 24.0), (62.0, 22.6), (66.6, 21.6), (70.4, 20.6), (72.4, 21.4)], [(56.5, 26.5), (59.5, 22.5), (64.0, 17.0), (70.5, 12.6), (75.6, 11.3)]],
 'AFRICAN': [[(39.6, -8.8), (40.1, -6.2), (39.9, -4.2), (40.3, -3.0), (42.5, -0.4), (45.5, 2.0), (49.6, 7.6), (51.6, 11.4), (46.0, 12.4)]],
 'CHINESE': [[(110.0, 9.0), (106.5, 5.5), (104.5, 2.5), (102.3, 2.3)], [(102.0, 2.3), (97.0, 5.6), (88.0, 6.0), (80.6, 5.6), (77.2, 7.4), (75.7, 11.2)]],
 'MALAY':   [[(102.2, 2.1), (104.0, -1.0), (106.5, -4.5)], [(102.0, 2.4), (96.0, 6.6), (86.0, 8.6), (81.5, 7.0)]],
}
RCOL = {'INDIAN': (222, 178, 96), 'ARAB': (188, 128, 92), 'PERSIAN': (124, 156, 176), 'AFRICAN': (176, 140, 92), 'CHINESE': (196, 132, 110), 'MALAY': (128, 160, 112)}
RLAB = {'INDIAN': (L('INDIAN', 'భారతీయులు'), (78.5, 19.5)), 'ARAB': (L('ARAB', 'అరబ్బులు'), (46.5, 19.0)), 'PERSIAN': (L('PERSIAN', 'పర్షియన్లు'), (58.0, 31.0)),
        'AFRICAN': (L('AFRICAN', 'ఆఫ్రికన్లు'), (35.0, -1.0)), 'CHINESE': (L('CHINESE', 'చైనీయులు'), (100.5, 15.5)), 'MALAY': (L('MALAY', 'మలయా'), (98.5, -4.6))}
RWORD = {'INDIAN': ('Indian,', 'భారతీయులు,'), 'ARAB': ('Arab,', 'అరబ్బులు,'), 'PERSIAN': ('Persian,', 'పర్షియన్లు,'),
         'AFRICAN': ('African,', 'ఆఫ్రికన్లు,'), 'CHINESE': ('Chinese', 'చైనీయులు,'), 'MALAY': ('Malay', 'మలయా')}
PORTS = {'MALINDI': (40.12, -3.22), 'CALICUT': (75.78, 11.25), 'MALACCA': (102.25, 2.19), 'GUJARAT': (72.4, 22.2), 'PHANIGIRI': (79.53, 17.29)}
PNAME = {'MALINDI': L('MALINDI', 'మాలిండి'), 'CALICUT': L('CALICUT', 'కాలికట్'), 'MALACCA': L('MALACCA', 'మలక్కా'), 'GUJARAT': L('GUJARAT', 'గుజరాత్'), 'PHANIGIRI': L('PHANIGIRI', 'ఫణిగిరి')}

def draw_routes(img, m, t, lit, glow_k=None, thick=None, alpha=1.0):
    """lit: {group: 0..1 draw-on}. Moving lantern dots show traffic on every lit route."""
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    dots = []
    for g, segs in ROUTES.items():
        k = lit.get(g, 0)
        if k <= .01: continue
        col = RCOL[g]; wd = (thick or {}).get(g, 4)
        for si, seg in enumerate(segs):
            pts = m.path(seg); part = poly_part(pts, k)
            if len(part) > 1: d.line([(x * 2, y * 2) for x, y in part], fill=col + (int(225 * alpha),), width=wd * 2, joint='curve')
            if k >= .999:
                L_ = poly_len(pts); n = max(1, int(L_ / 170))
                for j in range(n):
                    f = ((t * 46 / max(L_, 1)) + j / n + si * .37) % 1.0
                    if si % 2: f = 1 - f
                    (x, y), _ = poly_at(pts, f); dots.append((x, y, col))
    for x, y, col in dots:
        d.ellipse((x * 2 - 9, y * 2 - 9, x * 2 + 9, y * 2 + 9), fill=(250, 238, 210, int(235 * alpha)), outline=col + (int(255 * alpha),), width=3)
    lay = lay.resize((W, H), Image.LANCZOS)
    g_ = lay.filter(ImageFilter.GaussianBlur(5)); img.paste(g_, (0, 0), g_); img.paste(lay, (0, 0), lay)

def time_rail(img, k_in, k_fill, k_end, y=372):
    """1st c. CE (Roman coins in India) ... 1498 (da Gama): da Gama arrives last"""
    if k_in <= .01: return
    box = (70, y - 64, W - 70, y + 70); plate(img, box, k_in, alpha=210)
    x0, x1 = 150, W - 150; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((x0, y + 4, x1, y + 4), fill=(110, 100, 80, int(255 * k_in)), width=4)
    xf = lerp(x0, x1, e_io(k_fill)); d.line((x0, y + 4, xf, y + 4), fill=GOLD_A + (int(255 * k_in),), width=6)
    d.ellipse((x0 - 10, y - 6, x0 + 10, y + 14), fill=GOLD_A + (int(255 * k_in),))
    img.paste(lay, (0, 0), lay)
    small(img, L('1st c. CE · ROMAN COINS IN INDIA', 'క్రీ.శ. 1వ శతాబ్దం · భారత్‌లో రోమన్ నాణేలు'), x0 - 30, y - 32, 27 if not TE else 28, PARCH, 'lm', k_in, 600)
    small(img, L('CENTURIES OF TRADE', 'శతాబ్దాల వ్యాపారం'), W / 2, y + 40, 25 if not TE else 26, MUTED, 'mm', k_in * clamp(k_fill * 2))
    if k_end > .01:
        pin(img, x1, y + 4, k_end, AMBER, 12)
        small(img, L('1498 · DA GAMA', '1498 · డ గామా'), x1 + 30, y + 40, 28 if not TE else 28, AMBER, 'rm', k_end, 400)
    LY.reg('card', box, owner='time rail')

def wind(img, m, t, dirk, strength=1.0, n=700, seed=3, col=(236, 230, 214)):
    """wind streaks over the sea; dirk = +1 south-west monsoon (blows towards the NE), -1 north-east monsoon"""
    if strength <= .01: return
    n = int(n * .6); rng = np.random.default_rng(seed); xs = rng.uniform(0, W, n); ys = rng.uniform(600, 1560, n); ph = rng.uniform(0, 1, n); sp = rng.uniform(.6, 1.2, n)
    vx, vy = .77, -.64
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    pos = t * 70
    for i in range(n):
        f = (ph[i] + t * .35 * sp[i]) % 1.0; life = math.sin(math.pi * f)
        x = (xs[i] + dirk * vx * (pos * sp[i] + 90 * f)) % W; y = 600 + ((ys[i] - 600 + dirk * vy * (pos * sp[i] + 90 * f)) % 960)
        xi, yi = int(x), int(y)
        if m.land[min(H - 1, yi), min(W - 1, xi)]: continue
        ln = 26 * sp[i] * abs(dirk) + 4
        d.line((x - dirk * vx * ln * 1.6, y - dirk * vy * ln * 1.6, x, y), fill=col + (int(118 * life * strength),), width=3)
    img.paste(lay, (0, 0), lay)

def dhow(img, x, y, ang, k=1.0, s=1.0):
    """small lateen-sail ship icon in ink with a cream sail"""
    if k <= .01: return
    sz = 64 * s; lay = Image.new('RGBA', (int(sz * 2), int(sz * 2)), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = sz
    d.polygon([(c - sz * .55, c + sz * .18), (c + sz * .6, c + sz * .18), (c + sz * .38, c + sz * .42), (c - sz * .38, c + sz * .42)], fill=(30, 24, 18, int(255 * k)))
    d.line((c - sz * .05, c + sz * .2, c + sz * .02, c - sz * .62), fill=(30, 24, 18, int(255 * k)), width=4)
    d.polygon([(c + sz * .02, c - sz * .62), (c + sz * .52, c + sz * .12), (c - sz * .42, c + sz * .12)], fill=(244, 236, 214, int(255 * k)), outline=(30, 24, 18, int(255 * k)))
    if math.cos(ang) < 0: lay = lay.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(lay, (int(x - c), int(y - c)), lay)

# ------------------------------------------------------------------ PREVIEW A: the busy ocean (53A + 5.3b [+ TE 5.4]) and the monsoon (5.5)
def ocean_lit(t):
    lit = {}
    for g, (en, te) in RWORD.items():
        c = AT('53A', en, te) - .12; lit[g] = e_io(prog(t, c, c + 1.1))
    return lit

def s_ocean(t, s0, s1):
    m = OM(*MAP_A); img = m.base.copy()
    lit = ocean_lit(t); thick = {}
    c_long = AT('53A', 'long', 'ఎంతో') - .1; c_arr = AT('53A', 'arrived.', 'రాకముందే', end=True) - (.2 if not TE else 0)
    c_mal = S('5.3b') - .05
    # INDIAN route to Malacca thickens once Malacca is named
    km = e_io(prog(t, c_mal + .2, c_mal + 1.0))
    if km > 0: thick['INDIAN'] = int(4 + 4 * km)
    draw_routes(img, m, t, lit, thick=thick)
    for g, (lab, ll) in RLAB.items():
        k = e_out(prog(t, AT('53A', *RWORD[g]) - .05, AT('53A', *RWORD[g]) + .45))
        if k > .01: x, y = m.P(*ll); map_label(img, lab, x, y, 30 if not TE else 30, INK, k * (1 - .35 * km if g != 'INDIAN' else 1), bg=(244, 236, 214))
    # the time rail: Roman trade ... 1498, da Gama arrives last
    k_in = e_out(prog(t, s0 + .1, s0 + .7))
    if TE: k_fill = prog(t, s0 + .4, c_arr + .6); k_end = e_out(prog(t, s0 + .3, s0 + .9))
    else: k_fill = prog(t, c_long, c_arr); k_end = e_out(prog(t, c_arr - .1, c_arr + .4))
    k_out = 1 - e_io(prog(t, c_mal, c_mal + .6))
    time_rail(img, k_in * k_out, k_fill, k_end * k_out)
    # Malacca: the Gujarati merchants (museum label tied to the pin)
    if km > 0:
        x, y = m.P(*PORTS['MALACCA']); pin(img, x, y, km, AMBER, 13, pulse=(t - c_mal) * .8)
        map_label(img, PNAME['MALACCA'], x - 40, y - 52, 26 if not TE else 28, INK, km)
        box = (90, 1150, W - 90, 1330); k2 = e_out(prog(t, c_mal + .5, c_mal + 1.1)) * (1 - (e_io(prog(t, S('5.4') - .2, S('5.4') + .3)) if TE and has('5.4') else 0))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line((x, y + 16, x - 40, 1150), fill=GOLD_A + (int(220 * k2),), width=2); img.paste(lay, (0, 0), lay)
        plate_text(img, box, L('TOMÉ PIRES · SUMA ORIENTAL · c. 1515', 'టోమే పిరెస్ · సుమా ఓరియెంటల్ · c. 1515'),
                   L('GUJARATI MERCHANTS: AMONG THE BIGGEST AT MALACCA', 'మలక్కాలో అతిపెద్ద వ్యాపారుల్లో గుజరాతీలు'), k2, 40 if not TE else 40, owner='pires')
    small(img, L('PORTS AND ROUTES SHOWN ARE EXAMPLES · c. 1400–1500', 'చూపిన రేవులు, మార్గాలు ఉదాహరణలు · c. 1400–1500'), W / 2, 1360, 22 if not TE else 24, (226, 220, 204), 'mm', e_out(prog(t, s0 + .6, s0 + 1.2)) * (1 - km))
    if TE and has('5.4') and t >= S('5.4') - .1: s_coin(img, m, t)
    return img

def s_coin(img, m, t):
    """TE 5.4: our coast traded long before; a Roman gold coin found at Phanigiri (the coin shown is an illustrative example)"""
    c0 = S('5.4') - .1; c_coin = AT('5.4', 'తెలుగు', 'తెలుగు') - .15
    k = e_out(prog(t, c0, c0 + .6))
    # India's coastline glows (the Malacca label leaves)
    x, y = m.P(*PORTS['PHANIGIRI']); kp = e_out(prog(t, c_coin, c_coin + .5))
    pin(img, x, y, kp, AMBER, 12, pulse=(t - c_coin) * .8 if kp > 0 else None)
    if kp > 0: map_label(img, PNAME['PHANIGIRI'] + ' · తెలంగాణ', x + 10, y - 50, 26, INK, kp)
    kc = e_out(prog(t, c_coin + .35, c_coin + 1.0))
    if kc <= .01: return
    box = (70, 1040, W - 70, 1340); plate(img, box, kc, alpha=230)
    # coin photo: native pixels at 0.18 (1747 px -> 314 px), clearly marked as an illustrative example
    panel_nat(img, 'COIN', (100, 1066, 100 + 250, 1066 + 250), 1.0, (.5, .5), (.5, .5), sc=250 / 1747 * 1.0, radius=125, a=kc)
    tx_ = 385; text(img, 'రోమన్ బంగారు నాణెం', tx_, 1105, 44, CREAM, 'lm', 'head', kc, W - 120 - tx_, None)
    small(img, 'క్రీ.శ. 1వ శతాబ్దం · ఫణిగిరిలో దొరికింది', tx_, 1168, 28, AMBER, 'lm', kc, W - 120 - tx_)
    small(img, 'చిత్రం: ఉదాహరణ మాత్రమే', tx_, 1228, 27, PARCH, 'lm', kc, W - 120 - tx_)
    small(img, 'ఫణిగిరి నాణెం కాదు · ANS (MANTIS) · CC0', tx_, 1272, 23, MUTED, 'lm', kc, W - 120 - tx_)
    LY.reg('card', box, owner='coin')

def s_monsoon(t, s0, s1):
    m = OM(*MAP_A); img = m.base.copy()
    c_back = AT('5.5', 'back', 'మిగతా') - .1; c_sail = AT('5.5', 'Sailors', 'నావికులు') - .15
    # the network stays, quieter, under the wind
    draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.45)
    rev = e_io(prog(t, c_back, c_back + 1.1)); dirk = 1 - 2 * rev; dirk = dirk if abs(dirk) > .08 else .08 * (1 if dirk >= 0 else -1)
    k_in = e_out(prog(t, s0, s0 + .8))
    wind(img, m, t, dirk, k_in * (1 - .7 * (1 - abs(dirk))))
    # a ship rides the wind: Arabia -> Calicut, then home again
    pts = m.path(ROUTES['ARAB'][0])
    if t < c_back + .4: f = e_io(prog(t, s0 + .4, c_back + .2)); (x, y), ang = poly_at(pts, f)
    else: f = e_io(prog(t, c_back + .6, c_sail + 1.2)); (x, y), ang = poly_at(pts, 1 - f); ang += math.pi
    dhow(img, x, y - 22, ang, k_in, .9)
    # the season plate at the top
    swk = 1 - rev
    for txt_, kk in ((L('JUN – SEP · SOUTH-WEST MONSOON', 'జూన్ – సెప్టెంబర్ · నైరుతి రుతుపవనాలు'), swk), (L('NOV – FEB · NORTH-EAST MONSOON', 'నవంబర్ – ఫిబ్రవరి · ఈశాన్య రుతుపవనాలు'), rev)):
        if kk > .02: plate_text(img, (90, 306, W - 90, 436), L('THE WIND', 'గాలి'), txt_, k_in * kk, 38 if not TE else 36, owner='season')
    # sailing calendar: the year split by the two winds (simplified)
    kc = e_out(prog(t, c_sail, c_sail + .7))
    if kc > .01:
        box = (70, 1120, W - 70, 1335); plate(img, box, kc, alpha=232)
        ms = L(list('JFMAMJJASOND'), ['జన', 'ఫి', 'మా', 'ఏ', 'మే', 'జూ', 'జు', 'ఆ', 'సె', 'అ', 'న', 'డి'])
        cw = (W - 200) / 12; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i in range(12):
            x0 = 100 + i * cw; sw_ = 5 <= i <= 8; ne = i in (10, 11, 0, 1)
            col = RCOL['INDIAN'] if sw_ else ((124, 156, 176) if ne else (60, 56, 50))
            d.rounded_rectangle((x0 + 4, 1180, x0 + cw - 4, 1238), 8, fill=col + (int(235 * kc),))
        img.paste(lay, (0, 0), lay)
        for i, ch in enumerate(ms): small(img, ch, 100 + i * cw + cw / 2, 1209, 28 if not TE else 24, INK, 'mm', kc)
        small(img, L('→ TOWARDS INDIA', '→ భారత్ వైపు'), 100 + 6.5 * cw, 1278, 27 if not TE else 27, RCOL['INDIAN'], 'mm', kc)
        small(img, L('← HOME', '← తిరుగు'), 100 + 11 * cw - 10, 1278, 27 if not TE else 27, (150, 180, 200), 'mm', kc)
        small(img, L('SAILING SEASONS FOLLOWED THE WINDS · SIMPLIFIED', 'గాలుల ప్రకారమే ప్రయాణాలు · సరళీకృతం'), W / 2, 1150, 24 if not TE else 25, MUTED, 'mm', kc)
        LY.reg('card', box, owner='calendar')
    return img

# ------------------------------------------------------------------ PREVIEW B: Malindi -> Calicut, the pilot evidence trail, the Gujarat conclusion
TRACK = [(33.5, -30.0), (36.5, -24.5), (40.6, -16.0), (40.9, -10.0), (40.3, -5.2), (40.12, -3.22)]
ARCLL = [(40.12, -3.22), (47.0, 0.8), (56.0, 5.4), (66.0, 9.0), (72.5, 10.8), (75.78, 11.25)]

def dates_plate(img, t, c0, c1, a):
    import datetime as dt
    d0 = dt.date(1498, 4, 24); d1 = dt.date(1498, 5, 20); n = (d1 - d0).days; dd = d0 + dt.timedelta(days=int(round(n * e_io(prog(t, c0, c1)))))
    mo = L(['', '', '', '', 'APR', 'MAY'][dd.month], ['', '', '', '', 'ఏప్రిల్', 'మే'][dd.month])
    plate_text(img, (170, 306, W - 170, 440), L("DATES FROM THE CREW'S JOURNAL", 'తేదీలు: సిబ్బంది డైరీ నుంచి'), f'{dd.day} {mo} 1498', a, 50, owner='dates')

def pilot_icon(img, x, y, k, q=1.0):
    """an ink silhouette (not a portrait) with an amber question mark"""
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * k)
    d.ellipse((x - 17, y - 66, x + 17, y - 32), fill=(24, 20, 16, a), outline=PARCH + (a,), width=3)
    d.polygon([(x - 30, y + 18), (x + 30, y + 18), (x + 20, y - 28), (x - 20, y - 28)], fill=(24, 20, 16, a), outline=PARCH + (a,))
    img.paste(lay, (0, 0), lay)
    if q > .01: text(img, '?', x, y - 108, 64, AMBER, 'mm', 'head', k * q, None, (0, 0, 0))

def route_layer(img, m, t, k_track, k_arc, ship_f=None, a=1.0, w=7):
    lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    tr = poly_part(m.path(TRACK), k_track)
    for i in range(0, len(tr) - 1, 2): d.line([(tr[i][0] * 2, tr[i][1] * 2), (tr[i + 1][0] * 2, tr[i + 1][1] * 2)], fill=CREAM + (int(210 * a),), width=6)
    arc = poly_part(m.path(ARCLL, 14), k_arc)
    if len(arc) > 1: d.line([(x * 2, y * 2) for x, y in arc], fill=AMBER + (int(255 * a),), width=w * 2, joint='curve')
    lay = lay.resize((W, H), Image.LANCZOS); g_ = lay.filter(ImageFilter.GaussianBlur(9)); img.paste(g_, (0, 0), g_); img.paste(lay, (0, 0), lay)
    if ship_f is not None:
        (x, y), ang = poly_at(m.path(ARCLL, 14), ship_f); dhow(img, x, y - 24, ang, a, .8)

def s_route(t, s0, s1):
    c_mal = AT('5.6a', 'Malindi', 'మాలిండి') - .15; c_pil = AT('5.6a', 'pilot…', 'దారిచూపే') - .15
    c_gui = AT('5.6a', 'guided', 'అతనే') - .15; c_cal = AT('5.6a', 'Calicut.', 'కాలికట్') - .1
    kz = e_io(prog(t, s0, s0 + 1.4)); m = om_lerp(kz); img = m.base.copy()
    draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.38 * (1 - .4 * kz))
    if kz >= 1: wind(img, m, t, 1, .45, n=380)
    route_layer(img, m, t, e_io(prog(t, s0 + .6, c_mal + .2)), e_io(prog(t, c_gui, c_cal + .3)), ship_f=e_io(prog(t, c_gui, c_cal + .3)) if t >= c_gui else None)
    small(img, L('APPROXIMATE ROUTE', 'సుమారు మార్గం'), 210, 1250, 22 if not TE else 24, PARCH, 'mm', e_out(prog(t, s0 + 1.0, s0 + 1.6)))
    xm, ym = m.P(*PORTS['MALINDI']); km = e_out(prog(t, c_mal, c_mal + .5))
    pin(img, xm, ym, km, CREAM, 12); map_label(img, PNAME['MALINDI'], xm + 30, ym + 50, 28 if not TE else 30, INK, km)
    kp = e_out(prog(t, c_pil, c_pil + .5)); pilot_icon(img, xm + 95, ym - 10, kp * (1 - e_io(prog(t, c_gui, c_gui + .6))), 1.0)
    if kp > 0: map_label(img, L('A LOCAL PILOT', 'స్థానిక దారిచూపే నావికుడు'), xm + 110, ym + 110, 24 if not TE else 26, INK, kp * (1 - e_io(prog(t, c_gui, c_gui + .6))))
    xc, yc = m.P(*PORTS['CALICUT']); kc = e_out(prog(t, c_cal, c_cal + .5))
    pin(img, xc, yc, kc, AMBER, 13, pulse=(t - c_cal) * .8 if kc > 0 else None)
    if kc > 0: map_label(img, PNAME['CALICUT'], xc - 10, yc + 54, 28 if not TE else 30, INK, kc)
    if t >= c_gui - .3: dates_plate(img, t, c_gui, c_cal + .3, e_out(prog(t, c_gui - .3, c_gui + .2)))
    return img

# ---- evidence cards: real screenshots of the 1898 English translation (Project Gutenberg), cropped to the quoted lines
CLIPS = json.load(open(EV + 'clips.json'))
@functools.lru_cache(8)
def CLIP(key, lines_before=1, lines_after=1):
    """crop the screenshot to whole text lines around the highlighted words (cuts in the gaps between lines)"""
    im = Image.open(EV + key + '.png').convert('RGB'); r = CLIPS[key]['rects']
    g = np.asarray(im.convert('L')); ink = (g < 140).sum(1) > 2
    bands = []; i = 0
    while i < len(ink):
        if ink[i]:
            j = i
            while j < len(ink) and ink[j]: j += 1
            bands.append([i, j]); i = j
        else: i += 1
    merged = []                                   # join tiny bands (dots, superscripts) to their line
    for b_ in bands:
        if merged and (b_[0] - merged[-1][1] < 6 or b_[1] - b_[0] < 10): merged[-1][1] = max(merged[-1][1], b_[1])
        else: merged.append(b_)
    ys = [q['y'] + q['h'] / 2 for q in r]
    hit = [n for n, (a_, b2) in enumerate(merged) if any(a_ - 8 <= y <= b2 + 8 for y in ys)]
    n0 = max(0, min(hit) - lines_before); n1 = min(len(merged) - 1, max(hit) + lines_after)
    y0 = (merged[n0][0] + (merged[n0 - 1][1] if n0 > 0 else 0)) / 2 if n0 > 0 else max(0, merged[0][0] - 14)
    y1 = (merged[n1][1] + merged[n1 + 1][0]) / 2 if n1 + 1 < len(merged) else min(im.height, merged[n1][1] + 14)
    im = im.crop((0, int(y0), im.width, int(y1)))
    a = np.asarray(im).astype(np.float32); a = a * (np.array([246, 238, 220]) / 255.0)          # paper tone
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)), [(q['x'], q['y'] - y0, q['w'], q['h']) for q in r]

def clip_card(img, key, cx, cy, wd, a=1.0, hl=0.0, lb=1, la=1, owner=None):
    """paper clipping at <= 1.0 scale with an animated highlighter on the quoted words; returns its box"""
    if a <= .01: return None
    im, rects = CLIP(key, lb, la); sc = min(1.0, wd / im.width); w_, h_ = int(im.width * sc), int(im.height * sc)
    x0, y0 = int(cx - w_ / 2), int(cy - h_ / 2); box = (x0, y0, x0 + w_, y0 + h_)
    shadow(img, box, a, 18, 10)
    pic = im.resize((w_, h_), Image.LANCZOS).convert('RGBA')
    if hl > 0:
        lay = Image.new('RGBA', pic.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay); tot = sum(r[2] for r in rects) * hl
        for rx, ry, rw, rh in rects:
            if tot <= 0: break
            ww = min(rw, tot); d.rectangle((rx * sc - 3, ry * sc + rh * sc * .12, (rx + ww) * sc + 3, (ry + rh) * sc - rh * sc * .02), fill=(255, 196, 60, 110)); tot -= ww
        pic = Image.alpha_composite(pic, lay)
    m = Image.new('L', pic.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w_ - 1, h_ - 1), 10, fill=int(255 * a)); img.paste(pic.convert('RGB'), (x0, y0), m)
    LY.reg('image', box, owner=owner or key); return box

def case_strip(img, m_unused, t, a, q=1.0, gujarat=0.0):
    """the case file: a small, subordinate schematic of the route that stays at the top while documents are shown"""
    if a <= .01: return
    y = 300; x0, x1 = 180, W - 180; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(200 * a)
    d.line((x0, y, x1, y), fill=AMBER + (al,), width=4)
    for x in (x0, x1): d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=CREAM + (al,))
    img.paste(lay, (0, 0), lay)
    small(img, PNAME['MALINDI'], x0, y + 34, 25 if not TE else 26, PARCH, 'mm', a * .9)
    small(img, PNAME['CALICUT'], x1, y + 34, 25 if not TE else 26, PARCH, 'mm', a * .9)
    dhow(img, W / 2, y - 22, 0, a * .9, .55)
    small(img, L('THE PILOT · 1498', 'దారిచూపే నావికుడు · 1498'), W / 2, y + 34, 25 if not TE else 26, AMBER, 'mm', a * .9)
    LY.reg('card', (x0 - 30, y - 50, x1 + 30, y + 52), owner='case strip')

def ex_head(img, n, title, a):
    """exhibit heading above the document: EXHIBIT n · title"""
    if a <= .01: return
    small(img, L(f'EXHIBIT {n} OF 3', f'ఆధారం {n} / 3'), W / 2, 404, 28 if not TE else 28, AMBER, 'mm', a)
    text(img, title, W / 2, 458, 46 if not TE else 42, CREAM, 'mm', 'head', a, ST.sw - 60, None)

def doc_label(img, y, kicker, sub, a, w=None):
    if a <= .01: return
    small(img, kicker, W / 2, y, 26 if not TE else 27, PARCH, 'mm', a, w or ST.sw - 60)
    if sub: small(img, sub, W / 2, y + 38, 23 if not TE else 24, MUTED, 'mm', a, w or ST.sw - 60)

def s_pilot(t, s0, s1):
    # cues on the actual voice (EN: Whisper word times; TE: script words aligned to ASR chunks)
    c_x = AT('PILOT', "'Christian'…", "'క్రైస్తవుడు'") - .25
    c_h = AT('PILOT', 'but', 'కానీ') - .15; c_so = AT('PILOT', 'so', 'అందుకే') - .1
    c_lat = AT('PILOT', 'Later', 'తర్వాతి') - .2; c_name = AT('PILOT', 'Malemo', 'మాలెమో') - .15
    c_tit = AT('PILOT', 'title,', 'బిరుదు:') - .3; c_fam = AT('PILOT', 'famous', 'అతను') - .2
    c_unl = AT('PILOT', 'unlikely.', 'కానీ', n=1 if not TE else 2) - .2; c_ver = AT('PILOT', 'So', 'అంటే', n=2 if not TE else 1) - .2
    c_guj = AT('PILOT', 'Gujarat,', 'గుజరాత్‌కు', n=2) - .2
    if t >= c_ver - .25: return s_verdict(t, c_ver, c_guj, s1)
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9), cy=.45, reach=.85).copy()
    k_in = e_out(prog(t, s0 - .1, s0 + .5)); case_strip(img, None, t, .75 * k_in)
    slide = lambda c, d=.45: e_io(prog(t, c, c + d))
    # ---- EXHIBIT 1 · the voyage journal and the problem with "Christian"
    if t < c_lat - .05:
        out_ = e_io(prog(t, c_lat - .4, c_lat - .05)); a1 = k_in * (1 - out_); dx = -60 * out_
        ex_head(img, 1, L("THE CREW'S JOURNAL, 1498", 'సిబ్బంది డైరీ, 1498'), a1)
        # (a) the journal itself: a surviving manuscript copy (shown alone first, so no quotation sits on it)
        k_ms = 1 - slide(c_x)
        if k_ms > .01:
            panel_nat(img, 'ROTEIRO', (170 + dx, 520, W - 170 + dx, 1110), 1.0, (.5, .30), (.5, .36), sc=.62, radius=10, a=a1 * k_ms)
            doc_label(img, 1170, L('THE JOURNAL · A SURVIVING MANUSCRIPT COPY · EARLY 1500s', 'డైరీ · మిగిలిన చేతిరాత ప్రతి · 1500ల మొదట్లో'),
                      L('PORTO MUNICIPAL LIBRARY, MS 804 · PUBLIC DOMAIN', 'పోర్టో మునిసిపల్ లైబ్రరీ, MS 804 · పబ్లిక్ డొమైన్'), a1 * k_ms)
        # (b) the English translation (1898): "sent a Christian pilot"
        k_tr = slide(c_x)
        if k_tr > .01:
            a_tr = a1 * k_tr; sw_ = slide(c_h); y1 = 690
            small(img, L('ENGLISH TRANSLATION · E. G. RAVENSTEIN · 1898', 'ఆంగ్ల అనువాదం · E. G. RAVENSTEIN · 1898'), W / 2 + dx, 548, 23 if not TE else 25, AMBER, 'mm', a_tr)
            b1 = clip_card(img, 'A1_christian_pilot', W / 2 + dx, y1 - 40 * sw_, 940, a_tr * (1 - .45 * sw_), e_io(prog(t, c_x + .5, c_x + 1.3)), 2, 0, 'A1')
            if TE and sw_ < .5: small(img, "'రాజు ఒక క్రైస్తవ నావికుడిని పంపాడు'", W / 2 + dx, (b1[3] if b1 else 900) + 40, 25, PARCH, 'mm', a_tr * (1 - 2 * sw_))
            # (c) the same journal on Calicut: "inhabited by Christians"
            if sw_ > .01:
                b2 = clip_card(img, 'A2_calecut_christians', W / 2 + dx + (1 - sw_) * 300, 930, 940, a1 * sw_, e_io(prog(t, c_h + .5, c_h + 1.4)), 0, 0, 'A2')
                small(img, L('THE SAME JOURNAL, ON CALICUT', 'అదే డైరీ, కాలికట్ గురించి'), W / 2 + dx, (b2[1] if b2 else 840) - 34, 26 if not TE else 27, PARCH, 'mm', a1 * sw_)
                if TE: small(img, "'కాలికట్ నగరంలో క్రైస్తవులు ఉంటారు'", W / 2 + dx, (b2[3] if b2 else 920) + 38, 25, PARCH, 'mm', a1 * sw_)
            # what it shows (one short museum label)
            ks = e_out(prog(t, c_so, c_so + .5))
            if ks > .01:
                plate_text(img, (110 + dx, 1090, W - 110 + dx, 1290), L('WHAT THIS SHOWS', 'దీని అర్థం'),
                           L("'CHRISTIAN' DOESN'T TELL US HIS FAITH", "'క్రైస్తవుడు' అనే మాట అతని మతాన్ని చెప్పదు"), a1 * ks, 42 if not TE else 40, owner='ex1 label',
                           sub=L("THE CREW CALLED CALICUT'S HINDUS 'CHRISTIANS' TOO", 'కాలికట్ హిందువులనూ వాళ్లు అలాగే పిలిచారు'))
            small(img, L('HAKLUYT SOCIETY · VIA PROJECT GUTENBERG · PUBLIC DOMAIN', 'HAKLUYT SOCIETY · PROJECT GUTENBERG · పబ్లిక్ డొమైన్'), W / 2 + dx, 1330, 20 if not TE else 22, MUTED, 'mm', a_tr * (1 - e_out(prog(t, c_so, c_so + .5))))
        if t < c_lat - .15: return img
    # ---- EXHIBIT 2 · later Portuguese chroniclers: a Gujarati navigator, "Malemo" a title
    if t < c_fam - .05:
        kin = e_io(prog(t, c_lat - .15, c_lat + .25)); out_ = e_io(prog(t, c_fam - .4, c_fam - .05)); a2 = kin * (1 - out_); dx = 60 * (1 - kin) - 60 * out_
        ex_head(img, 2, L('LATER PORTUGUESE CHRONICLERS', 'తర్వాతి పోర్చుగీస్ చరిత్రకారులు'), a2)
        up = e_io(prog(t, c_name, c_name + .6))          # the title page steps back to make room for the name
        ph = int(lerp(560, 400, up)); pw = int(ph * 700 / 640)
        panel_nat(img, 'BARROS', (W / 2 - pw / 2 + dx, 510, W / 2 + pw / 2 + dx, 510 + ph), 1.0, (.47, .245), (.47, .245), sc=ph / 640, radius=8, a=a2, tint=(246, 238, 220))
        doc_label(img, 510 + ph + 34, L('JOÃO DE BARROS · DÉCADAS DA ÁSIA · LISBON 1552', 'జోవో డి బారోస్ · DÉCADAS DA ÁSIA · లిస్బన్ 1552'),
                  L('ALSO GÓIS AND CASTANHEDA · TITLE PAGE · PUBLIC DOMAIN', 'గోయిస్, కాస్టన్హెడా కూడా · టైటిల్ పేజీ · పబ్లిక్ డొమైన్'), a2 * (1 - e_io(prog(t, c_name - .1, c_name + .25))))
        kn = e_out(prog(t, c_name + .3, c_name + .8))
        if kn > .01:
            kt = e_io(prog(t, c_tit, c_tit + .6)); box = (110 + dx, 1030, W - 110 + dx, 1310)
            if kt < 1:
                plate_text(img, box, L('A NAVIGATOR FROM GUJARAT', 'గుజరాత్‌కు చెందిన నావికుడు'), 'MALEMO CANAQUA', a2 * kn * (1 - kt), 66, owner='name',
                           sub=L('RAVENSTEIN 1898, NOTE 132 · CITING BARROS, GÓIS', 'RAVENSTEIN 1898, NOTE 132 · బారోస్, గోయిస్ ఆధారంగా'))
            if kt > 0:
                plate_text(img, box, L("'MALEMO' ← MU'ALLIM", "'మాలెమో' ← ముఅల్లిమ్"), L('MASTER NAVIGATOR · A TITLE, NOT A NAME', 'నావికుల నాయకుడు · పేరు కాదు, బిరుదు'), a2 * kt, 46 if not TE else 44, owner='title',
                           sub=L('RAVENSTEIN 1898, NOTE 132', 'RAVENSTEIN 1898, NOTE 132'))
        if t < c_fam - .15: return img
    # ---- EXHIBIT 3 · the Ibn Majid identification, and why it is questioned
    kin = e_io(prog(t, c_fam - .15, c_fam + .25)); a3 = kin; dx = 60 * (1 - kin)
    ex_head(img, 3, L('A LATER, FAMOUS STORY', 'తర్వాత వచ్చిన ఒక ప్రసిద్ధ కథ'), a3)
    ku = e_io(prog(t, c_unl, c_unl + .6))
    plate_text(img, (110 + dx, 560, W - 110 + dx, 860), L('THE STORY SAYS THE PILOT WAS', 'ఆ కథ ప్రకారం నావికుడు'), L('IBN MAJID, THE FAMOUS ARAB NAVIGATOR', 'ప్రసిద్ధ అరబ్ నావికుడు ఇబ్న్ మాజిద్'), a3 * (1 - .45 * ku), 48 if not TE else 44, owner='ibn majid')
    if ku > .01:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line((190 + dx, 710, 190 + dx + (W - 380) * ku, 710), fill=PARCH + (int(200 * ku),), width=3); img.paste(lay, (0, 0), lay)
        plate_text(img, (110 + dx, 960, W - 110 + dx, 1230), L('HISTORIANS TODAY', 'ఈ రోజు చరిత్రకారులు'), L('MOST THINK IT UNLIKELY', 'చాలామంది ఇది నిజం కాకపోవచ్చు అంటారు'), a3 * ku, 52 if not TE else 44, owner='unlikely',
                   sub='TIBBETTS 1971 · SUBRAHMANYAM 1997')
    return img

def s_verdict(t, c_ver, c_guj, s1):
    """back to the map: the Malindi -> Calicut arc, and a thread to Gujarat (hedged)"""
    m = OM(*MAP_B); img = m.base.copy(); kin = e_io(prog(t, c_ver - .25, c_ver + .35))
    draw_routes(img, m, t, {g: 1.0 for g in ROUTES}, alpha=.3)
    route_layer(img, m, t, 1.0, 1.0, a=1.0, w=8)
    xm, ym = m.P(*PORTS['MALINDI']); xc, yc = m.P(*PORTS['CALICUT']); xg, yg = m.P(*PORTS['GUJARAT'])
    pin(img, xm, ym, 1, CREAM, 11); pin(img, xc, yc, 1, AMBER, 12)
    map_label(img, PNAME['MALINDI'], xm + 30, ym + 50, 26 if not TE else 28, INK, 1); map_label(img, PNAME['CALICUT'], xc - 10, yc + 52, 26 if not TE else 28, INK, 1)
    # the pilot icon rides the arc; its thread rises to Gujarat
    (px_, py_), _ = poly_at(m.path(ARCLL, 14), .55)
    kq = 1 - e_io(prog(t, c_guj, c_guj + .5)); pilot_icon(img, px_, py_ - 20, kin, kq)
    kt = e_io(prog(t, c_guj - .1, c_guj + 1.0))
    if kt > 0:
        pts = _smooth([(px_, py_ - 50), (lerp(px_, xg, .5) - 40, lerp(py_, yg, .5) - 30), (xg, yg)], 12)
        lay = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); ImageDraw.Draw(lay).line([(x * 2, y * 2) for x, y in poly_part(pts, kt)], fill=AMBER + (240,), width=10, joint='curve')
        lay = lay.resize((W, H), Image.LANCZOS); g_ = lay.filter(ImageFilter.GaussianBlur(7)); img.paste(g_, (0, 0), g_); img.paste(lay, (0, 0), lay)
        kg = e_out(prog(t, c_guj + .7, c_guj + 1.2)); pin(img, xg, yg, kg, AMBER, 15, pulse=(t - c_guj) * .8)
        map_label(img, PNAME['GUJARAT'], xg - 70, yg - 50, 30 if not TE else 32, INK, kg)
    # the conclusion, clearly hedged
    kc = e_out(prog(t, c_guj + .3, c_guj + .9))
    if kc > .01:
        plate_text(img, (90, 296, W - 90, 520), L('MOST LIKELY', 'బహుశా'), L('FROM GUJARAT, INDIA', 'గుజరాత్ నుంచి · భారత్'), kc, 60 if not TE else 56, owner='verdict',
                   sub=L('BASED ON 16th-CENTURY PORTUGUESE CHRONICLES', '16వ శతాబ్దపు పోర్చుగీస్ చరిత్రకారుల ఆధారంగా'))
    # the case strip fades back into the full map
    case_strip(img, None, t, .75 * (1 - kin))
    return img

# ------------------------------------------------------------------ dispatch (other scenes are built after the previews are approved)
def s_todo(t, s0, s1, name):
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9)).copy(); text(img, f'[{name}] · after preview approval', W / 2, H / 2, 40, MUTED, 'mm', 'head'); return img

def render(t):
    LY.reset(); name, s0, s1 = scene_at(t)
    if name == 'ocean': img = s_ocean(t, s0, s1)
    elif name == 'monsoon': img = s_monsoon(t, s0, s1)
    elif name == 'route': img = s_route(t, s0, s1)
    elif name == 'pilot': img = s_pilot(t, s0, s1)
    elif name.startswith('cartoon'):
        k = {'cartoon1': 'Q1', 'cartoon2': 'Q2', 'cartoon3': 'Q3'}[name]; img = cartoon(t, s0, [('CHELLI', k)])
    else: img = s_todo(t, s0, s1, name)
    # short cross-fades between scenes
    for n_, st_ in SC:
        if 0 < t - st_ < .3 and n_ in ('monsoon', 'pilot') and n_ == name:
            prev = SC[[x[0] for x in SC].index(n_) - 1]
            pimg = {'ocean': s_ocean, 'route': s_route}.get(prev[0])
            if pimg: img = Image.blend(pimg(st_ - .001, prev[1], st_), img, e_io((t - st_) / .3))
    overlays(img, t, name); captions(img, t, name); return img
