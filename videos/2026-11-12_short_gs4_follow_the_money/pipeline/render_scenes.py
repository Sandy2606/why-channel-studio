# ------------------------------------------------------------------ GS 4/6 scenes  ("Follow the money")
# Sharp-pictures rule: every source image is shown at <= 1.0 source px per output px (NAT/cover_nat assert it);
# diagrams, maps and the isometric chain are drawn at output size.
import cv2
from core import shade
ARC = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/archive/'
PK2 = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1/visuals/pack2/'
SRC = {'FARMAN': (ARC + '08_NEW_Farman_of_Aurangzeb_National_Museum_New_Delhi_62.5.jpg', (0, 0, 815, 1390)),
       'MUNDY': (ARC + '14_PD09_Mundy_famine_p236.jpg', None), 'CRACK': (ARC + '26_CC04_Cracked_dry_earth_Pexels_9692860.jpg', None),
       'MASU': (ARC + '16_PD06_Masulipatnam_Rijksmuseum.jpg', None), 'CANTINO': (ARC + '01_PD10_Cantino_planisphere_(1502).jpg', (4700, 0, 8550, 4998)),
       'AKBAR': (ARC + '20_PD08_Abul_Fazl_presenting_Akbarnama.jpg', None), 'G20': (PK2 + 'G20_v1.png', None), 'G16': (PK2 + 'G16_v1.png', None), 'G18': (PK2 + 'G18_v1.png', None), 'G19': (PK2 + 'G19_v1.png', None)}
DUSK = (16, 16, 15); TILE = (26, 25, 23); TILE2 = (21, 20, 19); ROAD = (70, 64, 52); BODY = (112, 106, 96)
FIELD = (104, 128, 72); RED = (168, 62, 50); TEAL = (66, 132, 120); MUTED = (170, 164, 150); STAMP = (196, 54, 40)
def sm_(x): x = clamp(x); return x * x * (3 - 2 * x)

@functools.lru_cache(12)
def NAT(key, prescale=1.0):
    """original pixels, graded like the film; optional pre-reduction (never enlargement)"""
    p, cr = SRC[key]; im = Image.open(p).convert('RGB')
    if cr: im = im.crop(cr)
    if prescale < 1: im = im.resize((int(im.width * prescale), int(im.height * prescale)), Image.LANCZOS)
    return Image.fromarray(FL.grade(np.asarray(im)))

def cover_nat(key, u, c0, c1, z0, z1, prescale=1.0, k=0.95):
    """full-screen camera move that never enlarges the source (scale <= 1.0)"""
    im = NAT(key, prescale); w, h = im.size; base = max(W / w, H / h)
    zz = lerp(z0, z1, e_io(clamp(u))); sc = min(base * zz, 1.0); assert base <= 1.0001, (key, base)
    fx, fy = lerp(c0[0], c1[0], e_io(clamp(u))), lerp(c0[1], c1[1], e_io(clamp(u))); hw, hh = W / 2 / sc, H / 2 / sc
    cx = min(max(fx * w, hw), w - hw); cy = min(max(fy * h, hh), h - hh)
    return grade(im.resize((W, H), Image.LANCZOS, box=(cx - hw, cy - hh, cx + hw, cy + hh)), k)

def panel_nat(img, key, box, u, f0, f1, sc=1.0, radius=26, a=1.0, border=None):
    """native-pixel window: shows a box-sized region of the source at scale sc (<=1), panning f0->f1 (fractions)"""
    assert sc <= 1.0001
    im = NAT(key); x0, y0, x1, y1 = [int(v) for v in box]; bw, bh = x1 - x0, y1 - y0; sw, sh = bw / sc, bh / sc
    k = e_io(clamp(u)); fx, fy = lerp(f0[0], f1[0], k), lerp(f0[1], f1[1], k)
    cx = min(max(fx * im.width, sw / 2), im.width - sw / 2); cy = min(max(fy * im.height, sh / 2), im.height - sh / 2)
    crop = im.resize((bw, bh), Image.LANCZOS, box=(cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2))
    m = Image.new('L', (bw, bh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, bw - 1, bh - 1), radius, fill=int(255 * a))
    if border:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), radius + 4, fill=border + (int(255 * a),)); img.paste(lay, (0, 0), lay)
    img.paste(crop, (x0, y0), m); LY.reg('image', (x0, y0, x1, y1), owner=key)

def small(img, s, x, y, px=24, col=MUTED, anchor='mm', a=1.0, maxw=None):
    text(img, s, x, y, px, col, anchor, 'monob', a, maxw or ST.sw, None)

CREDIT_Y = 1330   # credits sit above the caption lane, with the picture they describe
def credit(img, s, y=CREDIT_Y, a=1.0):
    ls = s.split('\n'); w = min(ST.sw, max(pick(x, 'monob', 22).getlength(x) for x in ls) + 30); hh = 22 + 15 * (len(ls) - 1)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((W / 2 - w / 2, y - hh, W / 2 + w / 2, y + hh), 14, fill=(8, 8, 8, int(170 * a)))
    img.paste(lay, (0, 0), lay)
    for i, x in enumerate(ls): text(img, x, W / 2, y - 15 * (len(ls) - 1) + 30 * i, 22, (200, 194, 180), 'mm', 'monob', a, ST.sw - 20, None)
    LY.reg('credit', (W / 2 - w / 2, y - hh, W / 2 + w / 2, y + hh), owner=ls[0][:30])

def dramatized(img, a=1.0):
    s = L('DRAMATIZED · ILLUSTRATION', 'నాటకీకరణ · చిత్రణ'); chip(img, s, W - 70 - pick(s, 'head', 22).getlength(s) / 2 - 18, 262, 22, (40, 38, 34), CREAM, a=a)

def coin(d, x, y, r, frac=1.0, a=255, ss=1):
    """gold coin; frac < 1 draws it with a wedge missing (the cut taken)"""
    x, y, r = x * ss, y * ss, r * ss
    d.ellipse((x - r * 1.04, y - r * .9, x + r * 1.04, y + r * 1.2), fill=(0, 0, 0, int(a * .45)))
    if frac >= .999:
        d.ellipse((x - r, y - r, x + r, y + r), fill=(232, 168, 48, a), outline=(140, 92, 16, a), width=int(3 * ss))
        d.ellipse((x - r * .68, y - r * .68, x + r * .68, y + r * .68), outline=(255, 214, 120, a), width=int(3 * ss))
    else:
        st = -90 + 360 * (1 - frac); d.pieslice((x - r, y - r, x + r, y + r), st, 270, fill=(232, 168, 48, a), outline=(140, 92, 16, a), width=int(3 * ss))

# ------------------------------------------------------------------ the isometric money chain (drawn at 2x, output size)
import isometric as ISO
def P_iso(U, ox, oy): return lambda x, y, z=0: ISO._iso(ST, U, ox, oy, x, y, z)
def floor(d, p, Wd, Hd, lit=1.0, R=16):
    for i in range(-R, R):
        for j in range(-R, R):
            q = [p(i, j), p(i + 1, j), p(i + 1, j + 1), p(i, j + 1)]
            if max(x for x, _ in q) < 0 or min(x for x, _ in q) > Wd or max(y for _, y in q) < 0 or min(y for _, y in q) > Hd: continue
            d.polygon(q, fill=shade(TILE if (i + j) % 2 == 0 else TILE2, lit))
def road(d, p, a, b, k, col=ROAD):
    e = (lerp(a[0], b[0], k), lerp(a[1], b[1], k)); hw = .22
    d.polygon([p(a[0] + hw, a[1] - hw), p(e[0] + hw, e[1] - hw), p(e[0] - hw, e[1] + hw), p(a[0] - hw, a[1] + hw)], fill=col)
def field(d, p, x, y, k, lit=1.0):
    w = 2.6 * k
    if w < .05: return
    ISO._box(d, p, x, y, w, .12, shade(FIELD, lit))
    for r in range(6):   # crop rows on the field
        f = -w / 2 + (r + .5) * w / 6; d.line([p(x + f, y - w / 2 + .1, .12), p(x + f, y + w / 2 - .1, .12)], fill=shade((70, 96, 46), lit), width=4)
    ISO._box(d, p, x - .6, y - .7, .7 * k, .55 * k, shade((150, 120, 80), lit))   # the farmer's hut
def building(kind, d, p, x, y, k, lit=1.0):
    if k <= .01: return
    if kind == 'farmer': field(d, p, x, y, k, lit)
    elif kind == 'coll': ISO._box(d, p, x, y, 1.6, 1.3 * k, shade(BODY, lit), win=True, dark=shade((60, 56, 50), lit))
    elif kind == 'state': ISO._box(d, p, x, y, 2.0, 2.2 * k, shade(AMBER, lit), win=True, dark=shade((150, 96, 14), lit))
    elif kind == 'army':
        ISO._box(d, p, x - .55, y + .55, .9, .8 * k, shade(RED, lit)); ISO._box(d, p, x + .6, y - .5, 1.3, 1.5 * k, shade((150, 130, 104), lit), win=True)
    elif kind == 'bank': ISO._box(d, p, x, y, 1.5, 1.1 * k, shade(TEAL, lit), win=True, dark=shade((30, 70, 64), lit))
    elif kind == 'weaver': ISO._box(d, p, x, y, 1.3, .8 * k, shade((176, 146, 104), lit), win=False)

KINDS = ['farmer', 'coll', 'state', 'army', 'bank']
NAMES = {'farmer': L('FARMER', 'రైతు'), 'coll': L('COLLECTORS · LOCAL LORDS', 'వసూలుదారులు · స్థానిక పెద్దలు'), 'state': L('STATE TREASURY', 'రాజ్య ఖజానా'),
         'army': L('ARMIES · COURTS', 'సైన్యాలు · దర్బార్లు'), 'bank': L('BANKERS', 'వడ్డీ వ్యాపారులు'), 'weaver': L('WEAVERS', 'నేతగాళ్లు')}
ROLES = {'farmer': L('PAYS LAND REVENUE', 'భూమి శిస్తు కడతాడు'), 'coll': L('KEEP A CUT', 'తమ వాటా'), 'state': L('RECEIVES', 'అందుకుంటుంది'),
         'army': L('SPENDS', 'ఖర్చు'), 'bank': L('LEND TO EVERYONE', 'అందరికీ అప్పు')}
GAP = 6.0

@functools.lru_cache(1)
def CHAIN_CUES():
    a = S('MONEY')
    c = dict(drop=a + .05, farmer=AT('4.6a', 'farmer', 'రైతు') - .1, third=AT('4.6a', 'third', 'మూడో') - .1, coll=AT('4.6a', 'Collectors', 'వసూలు') - .15,
             cut=AT('4.6a', 'cut.', 'వాటా') - .1, state=AT('4.6a', 'state', 'రాజ్యం') - .15, army=AT('4.6a', 'armies', 'సైన్యాలకు,') - .15,
             bank=AT('4.6a', 'Bankers', 'వడ్డీ') - .15, every=AT('4.6a', 'everyone.', 'అందరికీ') - .1)
    c['farmer'] = max(c['farmer'], c['drop'] + 1.0); return c

def focus_at(t, c):
    """camera focus index (float) along the chain, and the zoom-out k at the end"""
    pts = [(c['drop'], 0.0), (c['coll'], 0.0), (c['coll'] + .9, 1.0), (c['state'], 1.0), (c['state'] + .9, 2.0), (c['army'], 2.0), (c['army'] + .9, 3.0),
           (c['bank'], 3.0), (c['bank'] + .9, 4.0)]
    f = 0.0
    for (t0, f0), (t1, f1) in zip(pts, pts[1:]):
        if t >= t0: f = f0 + (f1 - f0) * e_io(prog(t, t0, t1))
    return f, e_io(prog(t, c['every'] - .2, c['every'] + 1.1))

def coin_pos(t, c):
    """index position of the coin along the chain (it leads the camera slightly)"""
    pts = [(c['coll'] - .05, 0.0), (c['coll'] + .75, 1.0), (c['state'] - .05, 1.0), (c['state'] + .75, 2.0), (c['army'] - .05, 2.0), (c['army'] + .75, 3.0)]
    f = 0.0
    for (t0, f0), (t1, f1) in zip(pts, pts[1:]):
        if t >= t0: f = f0 + (f1 - f0) * e_io(prog(t, t0, t1))
    return f

def chain_frame(t, c, lit_override=None, show_labels=True, zoom_k=None, upto=None, Uz=40, Yz=800):
    """draws the chain; returns (img, screen-point function)"""
    f, zk = focus_at(t, c)
    if zoom_k is not None: zk = zoom_k
    SS = 2; Wd, Hd = W * SS, H * SS
    U = lerp(112, Uz, zk) * SS; fc = lerp(f, 2.0, zk); Yc = lerp(930, Yz, zk) * SS
    ox = Wd / 2 - 150 * SS * zk + math.sin(t * .7) * 6 * SS; oy = Yc - fc * GAP * U + math.sin(t * .5) * 8 * SS   # slow living drift (vector, stays sharp)
    p = P_iso(U, ox, oy); im = Image.new('RGBA', (Wd, Hd), DUSK + (255,)); d = ImageDraw.Draw(im)
    floor(d, p, Wd, Hd, R=int(16 * 112 * SS / U) + 8)
    born = [c['farmer'] - .4, c['coll'] - .2, c['state'] - .2, c['army'] - .2, c['bank'] - .2]
    n = 5 if upto is None else upto
    for i in range(1, n):
        k = e_io(prog(t, born[i] - .1, born[i] + .7)); road(d, p, ((i - 1) * GAP, (i - 1) * GAP), (i * GAP, i * GAP), k)
    for i in range(n):
        k = e_back(prog(t, born[i], born[i] + .55)); lit = 1.0 if lit_override is None else lit_override.get(KINDS[i], 1.0)
        building(KINDS[i], d, p, i * GAP, i * GAP, k, lit)
    out = im.resize((W, H), Image.LANCZOS)
    fade = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fade)
    for yy in range(0, 460, 4): fd.rectangle((0, yy, W, yy + 4), fill=DUSK + (int(255 * clamp(1.15 - yy / 460) * (1 - zk)),))
    out.paste(fade, (0, 0), fade)
    scr = lambda i, z=0: tuple(v / SS for v in p(i * GAP, i * GAP, z))
    if show_labels:
        for i in range(n):
            if t < born[i] + .2: continue
            x, y = scr(i); y += 175 * lerp(1, .45, zk)
            if y > 1300 and zk < .5: continue   # never draw a station label into the caption lane
            near = abs(i - fc) < .6 and zk < .5; a = e_out(prog(t, born[i] + .2, born[i] + .6))
            if zk > .5:
                text(out, NAMES[KINDS[i]], x + 110, y - 85, 30, CREAM, 'lm', 'head', a * e_out(prog(zk, .5, 1)), W - 90 - (x + 110), (0, 0, 0))
            elif near:
                text(out, NAMES[KINDS[i]], x, y, 46, CREAM, 'mm', 'head', a, ST.sw, (0, 0, 0))
                text(out, ROLES[KINDS[i]], x, y + 58, 30, AMBER, 'mm', 'head', a, ST.sw, (0, 0, 0))
            else:
                text(out, NAMES[KINDS[i]], x, y, 30, (150, 146, 136), 'mm', 'head', a * .8, ST.sw, None)
    return out, scr, f, zk

def s_chain(t, s0, s1):
    c = CHAIN_CUES(); img, scr, f, zk = chain_frame(t, c)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    # the one coin: drops from the top onto the field, then rides the chain
    if t < c['coll'] - .05:
        x, y = scr(0, 1.2); k = e_out(prog(t, c['drop'], c['drop'] + .7)); y = lerp(-80, y, k); bounce = math.sin(prog(t, c['drop'] + .7, c['drop'] + 1.1) * math.pi) * 18
        coin(d, x, y - bounce, 40, 1.0)
    else:
        q = coin_pos(t, c); i0 = int(q); fr = q - i0; a = scr(i0, 1.2); b = scr(min(4, i0 + 1), 1.2)
        x, y = lerp(a[0], b[0], fr), lerp(a[1], b[1], fr) - math.sin(fr * math.pi) * 60
        frac = 1.0 if t < c['cut'] else lerp(1.0, .67, e_io(prog(t, c['cut'], c['cut'] + .5)))
        if t >= c['every'] - .2: frac = .67
        r = 40 * lerp(1, .6, zk)
        if q >= 2.999 and t >= c['army'] + .75:   # spent: the coin settles on the armies/courts tile
            pass
        coin(d, x, y, r, frac)
        if t >= c['cut']:   # the wedge stays with the collectors
            cx_, cy_ = scr(1, 1.25); cx_ += 120 * (1 - zk); cy_ -= 30 * (1 - zk); k = e_out(prog(t, c['cut'], c['cut'] + .5)); r2 = 40 * lerp(1, .6, zk)
            d.pieslice((cx_ - r2 + 30 * k, cy_ - r2 - 10 * k, cx_ + r2 + 30 * k, cy_ + r2 - 10 * k), -90, -90 + 360 * .33, fill=(232, 168, 48, 255), outline=(140, 92, 16, 255), width=3)
    img.paste(lay, (0, 0), lay)
    # the revenue share: small, careful, beside the field
    if c['third'] <= t < c['coll'] + .4:
        a = e_out(prog(t, c['third'], c['third'] + .4)) * (1 - prog(t, c['coll'], c['coll'] + .4)); x0, y0 = 300, 560
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rounded_rectangle((x0 - 30, y0 - 70, x0 + 510, y0 + 130), 22, fill=(10, 10, 10, int(200 * a)))
        k1 = e_io(prog(t, c['third'] + .1, c['third'] + .7)); k2 = e_io(prog(t, c['third'] + .9, c['third'] + 1.6))
        d.rounded_rectangle((x0, y0, x0 + 450, y0 + 30), 15, fill=(60, 58, 52, int(255 * a)))
        d.rounded_rectangle((x0, y0, x0 + 450 * lerp(0, 1 / 3, k1) + 1, y0 + 30), 15, fill=(232, 168, 48, int(255 * a)))
        if k2 > 0: d.rectangle((x0 + 150, y0 + 4, x0 + 150 + 75 * k2, y0 + 26), fill=(232, 168, 48, int(140 * a)))
        img.paste(lay, (0, 0), lay)
        text(img, L('1/3 – 1/2 OF THE CROP', 'పంటలో 1/3 – 1/2'), x0, y0 - 34, 36, AMBER, 'lm', 'head', a, 480, None)
        small(img, L('ASSESSED DEMAND · VARIED · OFTEN PAID IN CASH', 'అంచనా శిస్తు · చోటును బట్టి మారేది · తరచుగా నగదులో'), x0, y0 + 70, 21, MUTED, 'lm', a, 480)
        small(img, L("HISTORIANS' ESTIMATE", 'చరిత్రకారుల అంచనా'), x0, y0 + 102, 21, MUTED, 'lm', a, 480)
    # bankers lend to everyone: thin dotted arcs on the zoomed-out view
    if t >= c['every'] - .1:
        k = e_out(prog(t, c['every'], c['every'] + 1.2)); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); bx, by = scr(4, 1.0)
        for i in range(4):
            tx_, ty_ = scr(i, .6); kk = clamp(k * 1.6 - i * .18)
            if kk <= 0: continue
            mx = max(bx, tx_) + 170
            for s_ in range(0, int(26 * kk)):
                u = s_ / 26; x = (1 - u) ** 2 * bx + 2 * (1 - u) * u * mx + u * u * tx_; y = (1 - u) ** 2 * by + 2 * (1 - u) * u * ((by + ty_) / 2) + u * u * ty_
                d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=TEAL + (230,))
        img.paste(lay, (0, 0), lay)
    # header + accuracy chip
    kh = e_out(prog(t, s0, s0 + .4)) * (1 - zk)
    text(img, L('FOLLOW THE MONEY', 'డబ్బు వెనకే'), W / 2, 300, 54, CREAM, 'mm', 'head', kh, ST.sw, (0, 0, 0))
    small(img, L('ILLUSTRATIVE · NOT EVERY PAYMENT TOOK THIS PATH', 'ఉదాహరణ మాత్రమే · ప్రతి చెల్లింపు ఇలానే కాదు'), W / 2, 352, 21, MUTED, 'mm', e_out(prog(t, c['farmer'], c['farmer'] + .5)) * (1 - zk))
    small(img, L('ILLUSTRATIVE', 'ఉదాహరణ మాత్రమే'), W / 2, 262, 21, MUTED, 'mm', zk)
    return img

# ------------------------------------------------------------------ farman: the meaning, not just the document
@functools.lru_cache(1)
def ARMS():
    im = Image.fromarray(FL.img('PD12')).convert('RGB'); im.thumbnail((300, 300), Image.LANCZOS); return im
def stamp(img, s, cx, cy, k, rot, px=58):
    if k <= .01: return
    f = pick(s, 'head', px); w = int(f.getlength(s)) + 60; h = int(px * 1.6)
    lay = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rounded_rectangle((10, 10, w + 10, h + 10), 12, outline=STAMP + (235,), width=7); d.rounded_rectangle((20, 20, w, h), 8, outline=STAMP + (150,), width=2)
    text(lay, s, (w + 20) / 2, (h + 20) / 2, px, STAMP, 'mm', 'head', .95, None, None)
    sc = lerp(1.7, 1.0, e_out(clamp(k * 1.3))); lay = lay.rotate(rot, expand=True, resample=Image.BICUBIC)
    paste_c(img, lay, cx, cy, min(1, k * 2.2), sc)

def s_farman(t, s0, s1):
    img = radial_bg(W, H, (40, 34, 24), (10, 10, 10), cy=.45, reach=.85).copy()
    c_doc = S('FARMAN') + .5; c_f = AT('FARMAN', 'farmans,', 'ఫర్మానాలు') - .1
    c_r = AT('FARMAN', 'trading', 'హక్కులు,', n=2 if not TE else 1) - .1; c_p = AT('FARMAN', 'privileges.', 'ప్రత్యేక') - .1
    # who: foreign trading companies (Company arms as the example)
    ka = e_out(prog(t, s0, s0 + .5)); arm = ARMS(); sc = lerp(1.0, .55, e_io(prog(t, c_doc, c_doc + .7)))
    sc = lerp(1.0, .42, e_io(prog(t, c_doc, c_doc + .7))); ax, ay = lerp(W / 2, 835, e_io(prog(t, c_doc, c_doc + .7))), lerp(640, 360, e_io(prog(t, c_doc, c_doc + .7)))
    lay = Image.new('RGBA', (arm.width + 8, arm.height + 8), (196, 160, 92, 255)); lay.paste(arm, (4, 4)); paste_c(img, lay, ax, ay, ka, sc)
    kt = 1 - e_io(prog(t, c_doc - .15, c_doc + .2))
    text(img, L('FOREIGN TRADING COMPANIES', 'విదేశీ వ్యాపార కంపెనీలు'), W / 2, 880, 56, CREAM, 'mm', 'head', ka * kt, ST.sw, (0, 0, 0))
    small(img, L('e.g. THE ENGLISH EAST INDIA COMPANY', 'ఉదా: ఇంగ్లీష్ ఈస్ట్ ఇండియా కంపెనీ'), W / 2, 950, 24, MUTED, 'mm', ka * kt)
    # the real document (downscaled only), left; museum-style annotations, right
    kd = e_out(prog(t, c_doc, c_doc + .8))
    if kd > .01:
        doc = NAT('FARMAN'); s = .70; dw, dh = int(doc.width * s), int(doc.height * s); x0 = 56; y0 = int(lerp(336, 296, kd))
        sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle((x0 + 12, y0 + 18, x0 + dw + 12, y0 + dh + 18), fill=(0, 0, 0, 150)); sh = sh.filter(ImageFilter.GaussianBlur(14)); img.paste(sh, (0, 0), sh)
        img.paste(doc.resize((dw, dh), Image.LANCZOS), (x0, y0), Image.new('L', (dw, dh), int(255 * kd))); LY.reg('image', (x0, y0, x0 + dw, y0 + dh), owner='farman')
        P_ = lambda x, y: (x0 + x * s, y0 + y * s)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        kf = e_out(prog(t, c_f, c_f + .5))
        if kf > 0:   # the royal seal, ringed
            cx, cy = P_(515, 255); r = 92 * s * lerp(1.35, 1.0, kf); d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 200, 80, int(255 * kf)), width=5)
        for c_, yy in ((c_r, 650), (c_p, 1080)):   # soft highlighter across the relevant lines
            kk = e_io(prog(t, c_ + .05, c_ + .6))
            if kk > 0:
                a_, b_ = P_(80, yy - 6), P_(80 + 650 * kk, yy + 52); d.rounded_rectangle((a_[0], a_[1], b_[0], b_[1]), 8, fill=(255, 204, 90, 70))
        img.paste(lay, (0, 0), lay)
        def note(c_, yy, kicker, title, anchor_pt):
            k = e_out(prog(t, c_ + .25, c_ + .8))
            if k <= .01: return
            cx0 = 648; cx1 = W - LY.EDGE; cy = yy; ax_, ay_ = anchor_pt; inner = cx1 - cx0 - 30 - 24     # fixed geometry: fade only
            px = 38 if not TE else 36; f = pick(title, 'head', px)
            lines = [title] if f.getlength(title) <= inner else wrap(title, 'head', px, inner)
            hh = 78 if len(lines) == 1 else 96
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            kl = e_io(prog(t, c_ + .15, c_ + .55)); ex = lerp(ax_, cx0, kl)
            d.line((ax_, ay_, ex, lerp(ay_, cy, kl)), fill=(255, 200, 80, 230), width=3); d.ellipse((ax_ - 7, ay_ - 7, ax_ + 7, ay_ + 7), fill=(255, 200, 80, 255))
            d.rounded_rectangle((cx0, cy - hh, cx1, cy + hh), 16, fill=(14, 13, 12, int(225 * k)), outline=(120, 96, 50, int(255 * k)), width=2)
            d.rectangle((cx0 + 2, cy - hh + 18, cx0 + 8, cy + hh - 18), fill=(255, 200, 80, int(255 * k)))
            img.paste(lay, (0, 0), lay)
            ty0 = cy - hh + 40; small(img, kicker, cx0 + 30, ty0, 22 if not TE else 27, AMBER, 'lm', k, inner)
            ink = None
            for i, ln in enumerate(lines):
                yy_ = ty0 + 54 + i * (px + 8); text(img, ln, cx0 + 30, yy_, px, CREAM, 'lm', 'head', k, None, None)
                bb = f.getbbox(ln, anchor='lm'); r = (cx0 + 30 + bb[0], yy_ + bb[1], cx0 + 30 + bb[2], yy_ + bb[3])
                ink = r if ink is None else (min(ink[0], r[0]), min(ink[1], r[1]), max(ink[2], r[2]), max(ink[3], r[3]))
            LY.reg('card', (cx0, cy - hh, cx1, cy + hh), ink, owner=title)
        note(c_f, P_(0, 255)[1], L('A ROYAL ORDER', 'రాజాజ్ఞ'), L('FARMAN', 'ఫర్మానా'), P_(515 + 92, 255))
        note(c_r, P_(0, 676)[1], L('SOUGHT FOR', 'దేని కోసం'), L('TRADING RIGHTS', 'వ్యాపార హక్కులు'), P_(730, 676))
        note(c_p, P_(0, 1106)[1], L('AND', 'ఇంకా'), L('PRIVILEGES', 'ప్రత్యేక అనుమతులు'), P_(730, 1106))
        credit(img, L('A MUGHAL FARMAN (AURANGZEB) · NATIONAL MUSEUM, NEW DELHI\nEXAMPLE OF THE DOCUMENT TYPE', 'మొఘల్ ఫర్మానా (ఔరంగజేబు) · నేషనల్ మ్యూజియం, న్యూఢిల్లీ\nఈ రకం పత్రానికి ఉదాహరణ'), CREDIT_Y, kd)
    return img

# ------------------------------------------------------------------ 4.9 the rains fail (restrained; no collector in this section)
def rain(img, t, k):
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); rng = np.random.default_rng(11)
    for i in range(220):
        x = rng.uniform(-100, W + 100); sp = rng.uniform(900, 1400); y = (rng.uniform(0, H) + t * sp) % (H + 200) - 100
        d.line((x, y, x - 14, y + 46), fill=(200, 210, 220, int(110 * k)), width=2)
    img.paste(lay, (0, 0), lay)

def s_rains(t, s0, s1):
    c_fail = AT('4.9', 'failed…', 'పడకపోతే…') + .1; c_top = AT('4.9', 'wealth', 'పైనున్న') - .2; c_bot = AT('4.9', 'bottom.', 'కాపాడలేదు.') - .2
    if t < c_top + .5:
        u = (t - s0) / max(.1, c_top + .5 - s0)
        im = cover_nat('CRACK', u, (.45, .5), (.55, .5), 1.0, 1.08, prescale=.62, k=lerp(.75, .95, e_io(prog(t, c_fail - .5, c_fail + .8))))
        dry = e_io(prog(t, c_fail - .4, c_fail + .9)); im = Image.blend(im.convert('L').convert('RGB'), im, .45 + .55 * dry)
        rain(im, t, 1 - dry)
        kr = e_out(prog(t, c_fail, c_fail + .5)) * (1 - prog(t, c_top - .3, c_top))
        text(im, L('THE RAINS FAIL', 'వానలు పడవు'), W / 2, 330, 54, CREAM, 'mm', 'head', kr, ST.sw, (0, 0, 0))
        small(im, L('FAILED RAINS · SCARCITY', 'వర్షాభావం · కొరత'), W / 2, 392, 24, (220, 210, 190), 'mm', e_out(prog(t, c_fail + .3, c_fail + .8)) * (1 - prog(t, c_top - .3, c_top)))
        if t < c_top: return im
        base = im
    else: base = None
    # split: the treasury at the top stays lit; farmers and weavers at the bottom go grey
    SS = 2; Wd, Hd = W * SS, H * SS; U = 92 * SS; img = Image.new('RGBA', (Wd, Hd), DUSK + (255,)); d = ImageDraw.Draw(img)
    p_top = P_iso(U, Wd / 2, 720 * SS); p_bot = P_iso(U, Wd / 2, 1100 * SS)
    floor(d, P_iso(U, Wd / 2, 900 * SS), Wd, Hd, .9)
    grey = e_io(prog(t, c_bot, c_bot + 1.0))
    building('state', d, p_top, 0, 0, e_back(prog(t, c_top, c_top + .5)))
    lit = lerp(1.0, .42, grey)
    building('farmer', d, p_bot, -1.4, 1.4, e_back(prog(t, c_top + .3, c_top + .8)), lit); building('weaver', d, p_bot, 1.6, -1.6, e_back(prog(t, c_top + .4, c_top + .9)), lit)
    out = img.resize((W, H), Image.LANCZOS)
    if grey > 0:
        a = np.asarray(out).astype(np.float32); g = a.mean(2, keepdims=True); m = np.zeros((H, W, 1), np.float32); m[1000:] = grey; a = a * (1 - m * .8) + g * .7 * m * .8
        out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line((120, 930, W - 120, 930), fill=(120, 116, 106, 160), width=3); out.paste(lay, (0, 0), lay)
    ka = e_out(prog(t, c_top, c_top + .5))
    text(out, L('WEALTH AT THE TOP', 'పైన సంపద'), W / 2, 330, 46, AMBER, 'mm', 'head', ka, ST.sw, (0, 0, 0))
    text(out, L('FARMERS · WEAVERS', 'రైతులు · నేతగాళ్లు'), W / 2, 1250, 42, CREAM, 'mm', 'head', e_out(prog(t, c_top + .4, c_top + .9)) * lerp(1, .7, grey), ST.sw, (0, 0, 0))
    if base is not None: out = Image.blend(base, out.convert('RGB'), e_io(prog(t, c_top, c_top + .5)))
    return out

# ------------------------------------------------------------------ 4.10 famine 1630–32: map -> Mundy's page -> estimates -> the empty loom
def map_label(img, s, x, y, px=30, col=INK, a=1.0, anchor='mm'):
    if a <= .01: return
    f = pick(s, 'monob', px); w = f.getlength(s) + 28; x0 = min(max(x - w / 2, 48), W - 48 - w)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0, y - px * .85, x0 + w, y + px * .85), 10, fill=(244, 236, 214, int(230 * a)))
    img.paste(lay, (0, 0), lay); text(img, s, x0 + w / 2, y, px, col, 'mm', 'monob', a, None, None)
    LY.reg('label', (x0, y - px * .85, x0 + w, y + px * .85), owner=s)
class AMap:
    def __init__(self, lon0, lon1, latc):
        self.s = W / ((lon1 - lon0) * gsmap.AX); self.x0 = gsmap.to_svg(lon0, 0)[0]; self.yc = gsmap.to_svg(0, latc)[1]; self.base = self._render()
    def P(self, lon, lat):
        x, y = gsmap.to_svg(lon, lat); return ((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s)
    def _tr(self, q): return [((x - self.x0) * self.s, H / 2 + (y - self.yc) * self.s) for x, y in q]
    def _render(self):
        SS = 2; im = Image.new('RGB', (W * SS, H * SS), (150, 160, 156)); d = ImageDraw.Draw(im)
        for f in gsmap.GEO['features']:
            n = f['properties']['name']
            if n == 'India': continue
            for q in gsmap.polys(n):
                if len(q) > 2: d.polygon([(x * SS, y * SS) for x, y in self._tr(q)], fill=(176, 164, 136), outline=(120, 108, 84))
        for q in list(gsmap.india_polys()) + [q for n in ('Pakistan', 'Bangladesh') for q in gsmap.polys(n)]:
            if len(q) > 2: d.polygon([(x * SS, y * SS) for x, y in self._tr([tuple(z) for z in q])], fill=(190, 174, 138), outline=(190, 174, 138), width=5)
        lm = Image.new('L', (W * SS, H * SS), 0); dl = ImageDraw.Draw(lm)
        for q in list(gsmap.india_polys()) + [q for n in ('Pakistan', 'Bangladesh', 'Nepal', 'Bhutan', 'Sri Lanka') for q in gsmap.polys(n)]:
            if len(q) > 2: dl.polygon([(x * SS, y * SS) for x, y in self._tr([tuple(z) for z in q])], fill=255)
        self.land = lm.resize((W, H), Image.LANCZOS)
        im = im.resize((W, H), Image.LANCZOS); a = np.asarray(im).astype(np.float32) * VIG() * .85
        return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
@functools.lru_cache(2)
def FMAP(): return AMap(62.0, 92.0, 21.0)
FAMINE = [(L('GUJARAT', 'గుజరాత్'), 72.0, 22.6, 150), (L('DECCAN', 'దక్కన్'), 76.5, 18.6, 190)]

def s_famine(t, s0, s1):
    c_yr = AT('4.10', '1630', '1630') - .1; c_m = AT('4.10', 'Peter', 'Peter') - .25; c_e = AT('4.10', 'Estimates', 'చనిపోయినవాళ్లు') - .2; c_w = AT('4.10', 'Many', 'ఎంతోమంది') - .2
    if t < c_m:
        m = FMAP(); img = m.base.copy(); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        for k_, (n, lo, la, r) in enumerate(FAMINE):
            kk = e_io(prog(t, c_yr + .2 + k_ * .7, c_yr + 1.6 + k_ * .7))
            if kk <= 0: continue
            x, y = m.P(lo, la); g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse((x - r, y - r * .9, x + r, y + r * .9), fill=(120, 24, 20, int(170 * kk)))
            lay.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
        img.paste(lay, (0, 0), lay)
        for k_, (n, lo, la, r) in enumerate(FAMINE):
            kk = e_out(prog(t, c_yr + .5 + k_ * .7, c_yr + 1.0 + k_ * .7)); x, y = m.P(lo, la); text(img, n, x, y, 40, CREAM, 'mm', 'head', kk, 400, (0, 0, 0))
        text(img, '1630 – 1632', W / 2, 330, 70, CREAM, 'mm', 'head', e_out(prog(t, c_yr, c_yr + .5)), ST.sw, (0, 0, 0))
        small(img, L('FAMINE · APPROXIMATE REGIONS', 'కరువు · సుమారు ప్రాంతాలు'), W / 2, 398, 24, (220, 210, 190), 'mm', e_out(prog(t, c_yr + .3, c_yr + .8)))
        return img
    if t < c_e:
        # Peter Mundy's own page, never enlarged: fit-width (0.56x) -> push towards the passage (0.9x)
        u = prog(t, c_m, c_e); doc = NAT('MUNDY'); s = lerp(max(W / doc.width, H / doc.height), .9, e_io(prog(t, c_m + .6, c_e - .2))); sw, sh = W / s, H / s
        cx = lerp(doc.width / 2, 520, e_io(prog(t, c_m + .6, c_e - .2))); cy = lerp(doc.height * .42, 1030, e_io(prog(t, c_m + .6, c_e - .2)))
        cx = min(max(cx, sw / 2), doc.width - sw / 2); cy = min(max(cy, sh / 2), doc.height - sh / 2)
        img = grade(doc.resize((W, H), Image.LANCZOS, box=(cx - sw / 2, cy - sh / 2, cx + sw / 2, cy + sh / 2)), .92)
        k = e_io(prog(t, c_m + 1.6, c_m + 2.4))
        if k > 0:   # underline "great dearth" in the page's own coordinates
            X = lambda x: (x - (cx - sw / 2)) * s; Y = lambda y: (y - (cy - sh / 2)) * s
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rectangle((X(232), Y(1003), X(232 + (602 - 232) * k), Y(1062)), fill=(255, 196, 60, 80))
            d.line((X(232), Y(1066), X(232 + (602 - 232) * k), Y(1066)), fill=(190, 60, 40, 230), width=6); img.paste(lay, (0, 0), lay)
        credit(img, L("PETER MUNDY · TRAVELS, VOL. II, p.236 (HAKLUYT, 1914)\n'THAT GREAT DEARTH'", "పీటర్ మండీ · TRAVELS, VOL. II, p.236\n'THAT GREAT DEARTH' · 'ఆ మహా కరువు'"), CREDIT_Y, e_out(prog(t, c_m, c_m + .5)))
        chip(img, L('EYEWITNESS · 1630s', 'ప్రత్యక్ష సాక్షి · 1630లు'), W / 2, 330, 40, INK, CREAM, a=e_out(prog(t, c_m + .2, c_m + .7)))
        return img
    if t < c_w:
        img = radial_bg(W, H, (30, 26, 22), (8, 8, 8), cy=.42, reach=.8).copy(); k = e_out(prog(t, c_e, c_e + .6))
        small(img, L('DEATHS · FAMINE OF 1630–32', 'మరణాలు · 1630–32 కరువు'), W / 2, 700, 28, MUTED, 'mm', k)
        text(img, L('ESTIMATES RUN INTO THE MILLIONS', 'పదుల లక్షల్లో · అంచనా'), W / 2, 820, 76, CREAM, 'mm', 'head', k, ST.sw - 40, None)
        kc = e_out(prog(t, c_e + .6, c_e + 1.1)); s = L('HISTORICAL ESTIMATES · UNCERTAIN', 'చారిత్రక అంచనాలు · కచ్చితం కాదు')
        chip(img, s, W / 2, 960, 30, (58, 54, 48), CREAM, a=kc)
        return img
    # the empty loom, at native pixels (1.0), slow pan; dust in the light
    img = Image.new('RGB', (W, H), (8, 8, 8)); u = prog(t, c_w, s1 + 2.5)
    panel_nat(img, 'G20', (0, 352, W, 1310), u, (.40, .52), (.58, .50), sc=1.0, radius=0, a=e_out(prog(t, c_w, c_w + .6)))
    a = np.asarray(img).astype(np.float32)
    rng = np.random.default_rng(4)
    for i in range(50):
        x = (rng.uniform(300, 900) + t * rng.uniform(-6, 6)) % W; y = (rng.uniform(400, 1400) - t * rng.uniform(4, 14)) % H
        cv2.circle(a, (int(x), int(y)), int(rng.uniform(1, 3)), (230, 220, 190), -1)
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    text(img, L('WEAVERS DIED… OR FLED', 'నేతగాళ్లు చనిపోయారు… లేదా వెళ్లిపోయారు'), W / 2, 282, 44 if not TE else 40, CREAM, 'mm', 'head', e_out(prog(t, c_w + .4, c_w + 1.0)), ST.sw, (0, 0, 0))
    s_ = L('DRAMATIZED · ILLUSTRATION', 'నాటకీకరణ · చిత్రణ'); chip(img, s_, W - 112 - pick(s_, 'head', 22).getlength(s_) / 2, 1278, 22, (20, 19, 17), CREAM, a=e_out(prog(t, c_w, c_w + .6)))
    return img

# ------------------------------------------------------------------ TURN: the thread lifts from the loom -> land revenue -> the port -> sea routes
def thread_line(img, pts, k, col=AMBER, w=7):
    if k <= 0 or len(pts) < 2: return
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; tot = sum(seg) * k; out = [pts[0]]
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if tot <= 0: break
        f = min(1, tot / s); out.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f))); tot -= s
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line(out, fill=col + (255,), width=w, joint='curve')
    glw = lay.filter(ImageFilter.GaussianBlur(8)); img.paste(glw, (0, 0), glw); img.paste(lay, (0, 0), lay)

def clip_frame(name, t0, t):
    """frame of a silent Remotion clip (rendered at 1080x1920)"""
    i = max(0, int((t - t0) * FPS)); p = ROOT + f'rem/{name}_{LANGV}.mp4'
    cache = ROOT + f'rem/{name}_{LANGV}_frames/'
    if not os.path.isdir(cache):
        os.makedirs(cache, exist_ok=True); subprocess.run(['ffmpeg', '-v', 'error', '-i', p, cache + '%04d.png'], check=True)
    n = len(os.listdir(cache)); return Image.open(cache + f'{min(n, i + 1):04d}.png').convert('RGB')

def globe_frame(t0, t):
    """Remotion globe with its bottom source line replaced by our credit above the caption lane"""
    img = clip_frame('globe', t0, t); a = np.asarray(img).astype(np.float32); yy = np.arange(H, dtype=np.float32)
    m = np.clip((yy - 1372) / 40, 0, 1)[:, None, None]; a = a * (1 - m) + np.array([10, 12, 18], np.float32) * m
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    credit(img, L('SEA ROUTES · CHAUDHURI 1985 · DAS GUPTA 1979', 'సముద్ర మార్గాలు · CHAUDHURI 1985 · DAS GUPTA 1979'), CREDIT_Y, e_out(prog(t, t0, t0 + .5)))
    return img
def s_turn(t, s0, s1):
    c_but = AT('TURN', 'But', 'కానీ') - .15; c_tr = AT('TURN', 'trade', 'సముద్రాల') - .25
    if t < c_but:   # land -> treasury, once more, quickly; the thread rises from the loom
        kx = e_io(prog(t, s0, s0 + .6))
        if kx < 1:
            img = Image.new('RGB', (W, H), (8, 8, 8)); panel_nat(img, 'G20', (0, 352, W, 1310), 1.0, (.58, .50), (.58, .50), sc=1.0, radius=0, a=1 - kx)
            thread_line(img, [(540, 1100), (560, 800), (540, 400), (540, -40)], e_io(prog(t, s0 - .2, s0 + .6)))
            return img
        c = dict(drop=s0, farmer=s0 + .2, third=1e9, coll=1e9, cut=1e9, state=s0 + .6, army=1e9, bank=1e9, every=1e9)
        SS = 2; Wd, Hd = W * SS, H * SS; U = 92 * SS; im = Image.new('RGBA', (Wd, Hd), DUSK + (255,)); d = ImageDraw.Draw(im)
        p = P_iso(U, Wd / 2, 600 * SS); floor(d, p, Wd, Hd)
        road(d, p, (0, 0), (GAP, GAP), e_io(prog(t, s0 + .4, s0 + 1.0))); building('farmer', d, p, 0, 0, 1.0); building('state', d, p, GAP, GAP, e_back(prog(t, s0 + .6, s0 + 1.1)))
        img = im.resize((W, H), Image.LANCZOS); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
        a_ = [v / SS for v in p(0, 0, 1.2)]; b_ = [v / SS for v in p(GAP, GAP, 2.6)]; k = e_io(prog(t, s0 + .7, s0 + 1.6))
        coin(dd, lerp(a_[0], b_[0], k), lerp(a_[1], b_[1], k) - math.sin(k * math.pi) * 60, 36); img.paste(lay, (0, 0), lay)
        text(img, L('LAND → REVENUE', 'భూమి నుంచి ఆదాయం'), W / 2, 330, 52, CREAM, 'mm', 'head', e_out(prog(t, s0 + .3, s0 + .8)), ST.sw, (0, 0, 0))
        thread_line(img, [(80, 1290), (300, 1268), (560, 1258), (1000, 1236)], e_io(prog(t, s0 + .6, c_but)))
        return img
    if t < c_tr + .5:   # the port: a real engraving, never enlarged
        u = prog(t, c_but, c_tr + 2.0)
        img = cover_nat('MASU', u, (.36, .5), (.50, .5), 1.0, 1.0, prescale=.62, k=.98)
        ka = e_out(prog(t, c_but + .2, c_but + .7))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((540 - 16, 860 - 16, 540 + 16, 860 + 16), fill=AMBER + (int(255 * ka),)); img.paste(lay, (0, 0), lay)
        text(img, L('MACHILIPATNAM', 'మచిలీపట్నం'), W / 2, 800, 50, INK, 'mm', 'head', ka, ST.sw, None)
        text(img, L("INDIA'S PORTS", 'మన రేవులు'), W / 2, 330, 54, INK, 'mm', 'head', ka, ST.sw, None)
        thread_line(img, [(1060, 1290), (820, 1150), (620, 980), (540, 880)], e_io(prog(t, c_but, c_tr)))
        if t < c_tr: credit(img, L('MASULIPATAM · ENGRAVING, c.1750 · RIJKSMUSEUM', 'మచిలీపట్నం · చెక్కడపు చిత్రం, c.1750 · RIJKSMUSEUM'), CREDIT_Y, ka)
        if t >= c_tr: img = Image.blend(img, globe_frame(c_tr, t), e_io(prog(t, c_tr, c_tr + .3)))
        return img
    return globe_frame(c_tr, t)

# ------------------------------------------------------------------ tease: clearly EARLIER · 1498
PARCH = (226, 210, 172); GOLD_A = (196, 160, 92)        # restrained parchment / antique gold (with INK, CREAM, AMBER)
def cantino_bg(t, t0, k=.62):
    return cover_nat('CANTINO', prog(t, t0, t0 + 6.5), (.40, .5), (.60, .5), 1.0, 1.0, prescale=.5, k=k)
def rule_frame(d, box, a):
    x0, y0, x1, y1 = box; c1 = GOLD_A + (int(230 * a),); c2 = GOLD_A + (int(140 * a),)
    d.rectangle(box, outline=c1, width=2); d.rectangle((x0 + 9, y0 + 9, x1 - 9, y1 - 9), outline=c2, width=1)
    for cx, cy in ((x0, y0), (x1, y0), (x0, y1), (x1, y1)):      # small lozenges at the corners
        d.polygon([(cx, cy - 9), (cx + 9, cy), (cx, cy + 9), (cx - 9, cy)], fill=GOLD_A + (int(255 * a),))
def s_tease(t, s0, s1):
    """archival date reveal on the 1502 map: the year rolls back 1632 -> 1498 while the cotton thread rewinds"""
    c_q = AT('tease2', 'who', 'వాస్కో') - .2; t_roll0, t_roll1 = s0 + .1, c_q + .35
    img = cantino_bg(t, s0, lerp(.62, .78, e_io(prog(t, c_q, c_q + .6))))
    a_ = np.asarray(img).astype(np.float32); img = Image.fromarray(np.clip(a_ * np.array([1.0, .97, .90]) + np.array([6, 4, 0]), 0, 255).astype(np.uint8))   # parchment warmth
    # the thread rewinds across the map towards the Indian coast (thin, no glow)
    u = e_io(prog(t, t_roll0, t_roll1)); path = [(540, 912), (600, 1060), (720, 1230), (860, 1420), (1000, 1640)]   # winds back into the date
    thread_line_plain(img, path, 1 - u)
    # cartouche: ink plate, antique-gold double rule
    up = e_io(prog(t, c_q + .1, c_q + .8)); cy = lerp(760, 470, up); sc = lerp(1.0, .78, up)
    bw, bh = 600 * sc, 300 * sc; box = (W / 2 - bw / 2, cy - bh / 2, W / 2 + bw / 2, cy + bh / 2); ka = e_out(prog(t, s0, s0 + .5))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rectangle(box, fill=INK + (int(215 * ka),)); rule_frame(d, box, ka); img.paste(lay, (0, 0), lay)
    LY.reg('card', box, owner='EARLIER 1498')
    kick = L('EARLIER', 'ఇంకా ముందు'); text(img, kick, W / 2, cy - 92 * sc, int(28 * sc) if not TE else int(34 * sc), AMBER, 'mm', 'monob', ka, None, None, track=0 if TE else int(8 * sc))
    yr = int(round(lerp(1632, 1498, e_out(prog(t, t_roll0, t_roll1)))))
    text(img, str(yr), W / 2, cy + 22 * sc, int(132 * sc), CREAM, 'mm', 'head', ka, None, None)
    kl = e_out(prog(t, t_roll1 - .1, t_roll1 + .4)); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.line((W / 2 - 150 * sc * kl, cy + 105 * sc, W / 2 + 150 * sc * kl, cy + 105 * sc), fill=GOLD_A + (int(230 * kl),), width=2); img.paste(lay, (0, 0), lay)
    # the question, on the same ink plate language
    kq = e_out(prog(t, c_q + .4, c_q + .9))
    if kq > .01:
        qb = (90, 1080, W - 90, 1290); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rectangle(qb, fill=INK + (int(215 * kq),)); rule_frame(d, qb, kq); img.paste(lay, (0, 0), lay)
        q = L('WHO SHOWED VASCO DA GAMA THE WAY?', 'వాస్కో డ గామాకి దారి చూపించింది ఎవరు?')
        ls = wrap(q, 'head', 52, qb[2] - qb[0] - 90)
        for i, ln in enumerate(ls): text(img, ln, W / 2, (qb[1] + qb[3]) / 2 + (i - (len(ls) - 1) / 2) * 64, 52, CREAM, 'mm', 'head', kq, qb[2] - qb[0] - 90, None)
        LY.reg('card', qb, owner='question')
    credit(img, L('CANTINO PLANISPHERE · 1502', 'కాంటినో ప్రపంచ పటం · 1502'), CREDIT_Y, ka)
    return img
def thread_line_plain(img, pts, k, col=AMBER, w=5):
    if k <= 0: return
    seg = [math.dist(a, b) for a, b in zip(pts, pts[1:])]; tot = sum(seg) * k; out = [pts[0]]
    for (a, b), s in zip(zip(pts, pts[1:]), seg):
        if tot <= 0: break
        f = min(1, tot / s); out.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f))); tot -= s
    big = Image.new('RGBA', (W * 2, H * 2), (0, 0, 0, 0)); ImageDraw.Draw(big).line([(x * 2, y * 2) for x, y in out], fill=col + (235,), width=w * 2, joint='curve')
    lay = big.resize((W, H), Image.LANCZOS); img.paste(lay, (0, 0), lay)

# ------------------------------------------------------------------ shared ink-plate card (same language as the farman notes and the 1498 cartouche)
def plate(img, box, a=1.0, rule=True, fill=INK, alpha=215):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.rectangle(box, fill=fill + (int(alpha * a),))
    if rule: rule_frame(d, box, a)
    img.paste(lay, (0, 0), lay)

def plate_text(img, box, kicker, title, a=1.0, px=44, owner=None, sub=None):
    """kicker (mono, amber) + title (head, cream) centred in an ink plate; registers the box and text ink"""
    if a <= .01: return
    plate(img, box, a); x0, y0, x1, y1 = box; inner = x1 - x0 - 60; cx = (x0 + x1) / 2
    lines = wrap(title, 'head', px, inner); f = pick(title, 'head', px); lh = px + 10
    block = (34 if kicker else 0) + len(lines) * lh + (34 if sub else 0); y = (y0 + y1) / 2 - block / 2
    if kicker: small(img, kicker, cx, y + 12, 22 if not TE else 26, AMBER, 'mm', a, inner); y += 34
    ink = None
    for ln in lines:
        yy = y + lh / 2; text(img, ln, cx, yy, px, CREAM, 'mm', 'head', a, None, None)
        bb = f.getbbox(ln, anchor='mm'); r = (cx + bb[0], yy + bb[1], cx + bb[2], yy + bb[3]); y += lh
        ink = r if ink is None else (min(ink[0], r[0]), min(ink[1], r[1]), max(ink[2], r[2]), max(ink[3], r[3]))
    if sub: small(img, sub, cx, y + 16, 21 if not TE else 24, MUTED, 'mm', a, inner)
    LY.reg('card', box, ink, owner=owner or title)

def arrow(d, a_, b_, col, k=1.0, w=4, head=16):
    if k <= 0: return
    x = lerp(a_[0], b_[0], k); y = lerp(a_[1], b_[1], k); d.line((a_[0], a_[1], x, y), fill=col, width=w)
    ang = math.atan2(y - a_[1], x - a_[0])
    d.polygon([(x, y), (x - head * math.cos(ang - .45), y - head * math.sin(ang - .45)), (x - head * math.cos(ang + .45), y - head * math.sin(ang + .45))], fill=col)

# ------------------------------------------------------------------ 0:00 hook: ~1/4 of world output -> the maker's empty bowl
def s_hook(t, s0, s1, frame0=False):
    c_made = AT('S4_hook', 'made', 'తయారుచేసినవాళ్లలో', n=2 if not TE else 1) - .15; c_poor = AT('S4_hook', 'poor?', 'పేదవాళ్లుగానే') - .2
    if frame0: t = 0.0
    img = radial_bg(W, H, (238, 226, 196), (206, 188, 150), cy=.42, reach=.9).copy()
    k_bowl = e_io(prog(t, c_made, c_made + .7))
    # 10 x 10 squares, ~24 lit (Maddison, c.1700); all lit at frame 0 so the first frame already carries the fact
    n_lit = 24   # constant: frame 1 already carries the fact, no refill flicker
    gx, gy, cs = 190, lerp(420, 330, k_bowl), 70; sc = lerp(1.0, .52, k_bowl); cs_ = cs * sc; gx = W / 2 - 5 * cs_
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(100):
        r_, c_ = divmod(i, 10); x = gx + c_ * cs_; y = gy + r_ * cs_
        sh_ = math.exp(-(((c_ + r_ * .5) - ((t * 4.0) % 16 - 3)) ** 2) / 2.0) if i < n_lit else 0   # a slow light passing over the lit squares
        col_ = mix(AMBER, (255, 226, 150), .55 * sh_) if i < n_lit else (90, 80, 62)
        d.rounded_rectangle((x + 4 * sc, y + 4 * sc, x + cs_ - 4 * sc, y + cs_ - 4 * sc), 6 * sc, fill=col_ + (255,))
    img.paste(lay, (0, 0), lay); LY.reg('label', (gx, gy, gx + 10 * cs_, gy + 10 * cs_), owner='grid')
    ky = 1 - k_bowl
    text(img, L("~1/4 OF THE WORLD'S OUTPUT", 'ప్రపంచ ఉత్పత్తిలో ~1/4'), W / 2, gy + 10 * cs_ + 70, 54, INK, 'mm', 'head', ky, ST.sw, None)
    small(img, L('c.1700 · MADDISON ESTIMATE', 'c.1700 · మాడిసన్ అంచనా'), W / 2, gy + 10 * cs_ + 128, 24, (90, 80, 62), 'mm', ky)
    if k_bowl > .01:   # the maker's empty bowl beside a finished bale (own illustration, native pixels)
        dark = Image.new('RGB', (W, H), (14, 13, 12)); m = Image.new('L', (W, H), int(255 * k_bowl)); img.paste(dark, (0, 0), m)
        gx2 = W / 2 - 5 * cs * .52; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i in range(100):
            r_, c_ = divmod(i, 10); x = gx2 + c_ * cs * .52; y = 330 + r_ * cs * .52
            d.rounded_rectangle((x + 2, y + 2, x + cs * .52 - 2, y + cs * .52 - 2), 3, fill=(AMBER if i < 24 else (60, 56, 48)) + (int(255 * k_bowl),))
        img.paste(lay, (0, 0), lay)
        panel_nat(img, 'G16', (60, 760, W - 60, 1286), prog(t, c_made, s1 + 1), (.48, .53), (.52, .53), sc=.52, radius=18, a=k_bowl, border=GOLD_A)
        kq = e_out(prog(t, c_poor, c_poor + .5))
        text(img, L('WHY DID THE MAKERS STAY POOR?', 'చేసినవాళ్లు పేదవాళ్లుగా ఎందుకు?'), W / 2, 1335, 44, CREAM, 'mm', 'head', kq, ST.sw, None)
        s_ = L('DRAMATIZED · ILLUSTRATION', 'నాటకీకరణ · చిత్రణ'); chip(img, s_, W - 112 - pick(s_, 'head', 22).getlength(s_) / 2, 1268, 22, (20, 19, 17), CREAM, a=k_bowl)
    return img

# ------------------------------------------------------------------ TE only: Madanna & Akkanna as role cards (not portraits)
@functools.lru_cache(4)
def DMAP(dl=0.0): return AMap(73.5 + dl, 85.5 + dl, 17.6 - dl * .5)
def s_madanna(t, s0, s1):
    c_hk = AT('MADANNA', 'హనుమకొండకు', 'హనుమకొండకు') - .1; c_gk = AT('MADANNA', 'గోల్కొండలో', 'గోల్కొండలో') - .1
    c_m = AT('MADANNA', 'మాదన్న', 'మాదన్న', n=2) - .15; c_a = AT('MADANNA', 'అక్కన్న', 'అక్కన్న', n=2) - .15
    if t < c_m:
        m = DMAP(round(.8 * e_io(prog(t, s0, c_m)), 3)); img = m.base.copy(); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        hk = m.P(79.56, 18.00); gk = m.P(78.40, 17.38); k1 = e_out(prog(t, c_hk, c_hk + .4)); k2 = e_io(prog(t, c_gk - .2, c_gk + .6))
        if k2 > 0: d.line((hk[0], hk[1], lerp(hk[0], gk[0], k2), lerp(hk[1], gk[1], k2)), fill=AMBER + (255,), width=5)
        for p_, k_ in ((hk, k1), (gk, e_out(prog(t, c_gk + .3, c_gk + .7)))):
            if k_ > 0: d.ellipse((p_[0] - 11, p_[1] - 11, p_[0] + 11, p_[1] + 11), fill=INK + (int(255 * k_),), outline=AMBER + (int(255 * k_),), width=4)
        img.paste(lay, (0, 0), lay)
        if k2 >= 1:   # a slow pulse on Golconda while the line is read (no static hold)
            ph = ((t - c_gk) * .6) % 1.0; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); r = 14 + 70 * ph
            ImageDraw.Draw(lay).ellipse((gk[0] - r, gk[1] - r, gk[0] + r, gk[1] + r), outline=AMBER + (int(200 * (1 - ph)),), width=3); img.paste(lay, (0, 0), lay)
        map_label(img, 'హనుమకొండ', hk[0] + 20, hk[1] - 60, 32, INK, k1); map_label(img, 'గోల్కొండ', gk[0] - 20, gk[1] + 60, 32, INK, e_out(prog(t, c_gk + .3, c_gk + .7)))
        plate_text(img, (90, 300, W - 90, 440), 'గోల్కొండ · 1670s–1680s', 'అబుల్ హసన్ కుతుబ్ షా పాలన', e_out(prog(t, c_gk, c_gk + .5)), 40)
        credit(img, 'సుమారు స్థానాలు', CREDIT_Y, k1)
        return img
    img = radial_bg(W, H, (34, 30, 24), (10, 10, 10), cy=.45, reach=.85).copy()
    km = e_out(prog(t, c_m, c_m + .5)); ka = e_out(prog(t, c_a, c_a + .5))
    # card 1: Madanna, chief minister, revenue (the revenue-office illustration, native pixels downscaled)
    b1 = (90, 330, W - 90, 760); plate(img, b1, km)
    if km > .01: panel_nat(img, 'G18', (120, 380, 480, 710), prog(t, c_m, s1), (.36, .5), (.50, .5), sc=.33, radius=6, a=km)
    text(img, 'మాదన్న', 520, 450, 54, CREAM, 'lm', 'head', km, b1[2] - 560, None)
    small(img, 'ప్రధానమంత్రి', 520, 530, 30, AMBER, 'lm', km, b1[2] - 560); small(img, 'ఆదాయ వ్యవహారాలు', 520, 584, 28, MUTED, 'lm', km, b1[2] - 560)
    LY.reg('card', b1, owner='madanna')
    # card 2: Akkanna, commander-in-chief (a drawn banner; no account books)
    b2 = (90, 820, W - 90, 1250); plate(img, b2, ka)
    if ka > .01:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); al = int(255 * ka)
        d.rectangle((120, 852, 480, 1218), fill=(26, 24, 21, al)); d.line((230, 880, 230, 1190), fill=GOLD_A + (al,), width=8)
        wv = math.sin(t * 3.0) * 10; d.polygon([(234, 890), (420, 935 + wv), (234, 985)], fill=(150, 70, 50, al)); d.polygon([(234, 990), (380, 1020), (234, 1050)], fill=GOLD_A + (al,))
        d.ellipse((222, 868, 238, 884), fill=GOLD_A + (al,)); img.paste(lay, (0, 0), lay)
    text(img, 'అక్కన్న', 520, 940, 54, CREAM, 'lm', 'head', ka, b2[2] - 560, None)
    small(img, 'సైన్యాధిపతి', 520, 1020, 30, AMBER, 'lm', ka, b2[2] - 560)
    LY.reg('card', b2, owner='akkanna')
    credit(img, 'చిత్రణ · చిత్తరువులు కావు', CREDIT_Y, km)
    return img

# ------------------------------------------------------------------ 4.8 Virji Vora and the English Company
def s_virji(t, s0, s1):
    c_s = AT('4.8a', 'Surat,', 'సూరత్‌లో') - .15; c_v = AT('4.8a', 'Virji', 'విర్జీ') - .15
    c_l = AT('4.8a', 'lent', 'ఇంగ్లీష్') - .1; c_ag = AT('4.8a', 'again', 'పదే') - .1; c_r = AT('4.8a', 'records', 'రికార్డులే') - .15
    img = radial_bg(W, H, (34, 30, 24), (10, 10, 10), cy=.45, reach=.85).copy()
    kp = e_out(prog(t, s0, s0 + .5))
    panel_nat(img, 'G19', (60, 322, W - 60, 1000), prog(t, s0, s1), (.40, .5), (.58, .5), sc=1.0, radius=18, a=kp, border=GOLD_A)
    text(img, L('BANKERS COULD BE POWERFUL', 'వడ్డీ వ్యాపారుల శక్తి'), W / 2, 260, 40, CREAM, 'mm', 'head', kp * (1 - prog(t, c_s - .2, c_s)), ST.sw, None)
    ks = e_out(prog(t, c_s, c_s + .4))
    if ks > 0: chip(img, L('SURAT · 1600s', 'సూరత్ · 1600లు'), W / 2, 262, 32, CREAM, INK, a=ks)
    s_ = L('DRAMATIZED · ILLUSTRATION', 'నాటకీకరణ · చిత్రణ'); chip(img, s_, W - 112 - pick(s_, 'head', 22).getlength(s_) / 2, 968, 22, (20, 19, 17), CREAM, a=kp)
    # loans: Virji Vora -> the English Company, again and again (three coins, one after another)
    kn = e_out(prog(t, c_v, c_v + .5)) * (1 - e_io(prog(t, c_r - .35, c_r - .05)))
    if kn > .01:
        bA = (70, 1060, 450, 1260); bB = (630, 1060, W - 70, 1260)
        plate_text(img, bA, L('MERCHANT · BANKER', 'వ్యాపారి · వడ్డీ వ్యాపారి'), L('VIRJI VORA', 'విర్జీ వోరా'), kn, 40)
        plate_text(img, bB, L('BORROWER', 'అప్పు తీసుకుంది'), L('ENGLISH COMPANY', 'ఇంగ్లీష్ కంపెనీ'), e_out(prog(t, c_l, c_l + .4)) * kn, 34)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        arrow(d, (462, 1160), (618, 1160), GOLD_A + (int(255 * kn),), e_io(prog(t, c_l, c_l + .5)))
        for j, c_ in enumerate((c_l + .4, c_ag, c_ag + .7)):
            u = prog(t, c_, c_ + .7)
            if 0 < u < 1: coin(d, lerp(470, 610, e_io(u)), 1110 - math.sin(u * math.pi) * 30, 18, a=int(255 * kn))
        img.paste(lay, (0, 0), lay)
        nloan = sum(1 for c_ in (c_l + .4, c_ag, c_ag + .7) if t >= c_ + .7)
        if nloan: small(img, L(f'LOANS: {nloan}' + (' …' if nloan == 3 else ''), f'అప్పులు: {nloan}' + (' …' if nloan == 3 else '')), W / 2, 1300, 24, AMBER, 'mm', kn)
    kr = e_out(prog(t, c_r - .05, c_r + .4))
    if kr > .01 and kn <= .01: plate_text(img, (90, 1060, W - 90, 1270), L("THE COMPANY'S OWN RECORDS", 'కంపెనీ రికార్డుల్లోనే'), L('THE RICHEST MERCHANT OF HIS TIME', 'ఆ కాలంలో అత్యంత ధనిక వ్యాపారి'), kr, 40)
    return img

# ------------------------------------------------------------------ "merchants and rulers needed each other"
def s_needeach(t, s0, s1):
    img = radial_bg(W, H, (34, 30, 24), (10, 10, 10), cy=.45, reach=.85).copy(); k = e_out(prog(t, s0, s0 + .4))
    bM = (70, 760, 450, 940); bR = (630, 760, W - 70, 940)
    plate_text(img, bM, None, L('MERCHANTS', 'వ్యాపారులు'), k, 40); plate_text(img, bR, None, L('RULERS', 'పాలకులు'), e_out(prog(t, s0 + .25, s0 + .65)), 40)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    k1 = e_io(prog(t, s0 + .5, s0 + 1.1)); k2 = e_io(prog(t, s0 + 1.1, s0 + 1.7))
    arrow(d, (462, 800), (618, 800), AMBER + (255,), k1); arrow(d, (618, 900), (462, 900), GOLD_A + (255,), k2)
    img.paste(lay, (0, 0), lay)
    small(img, L('CREDIT · TRADE · CUSTOMS REVENUE', 'అప్పులు · వ్యాపారం · సుంకాల ఆదాయం'), W / 2, 690, 24, AMBER, 'mm', k1, ST.sw)
    small(img, L('PROTECTION · PERMISSIONS', 'రక్షణ · అనుమతులు'), W / 2, 1010, 24, (210, 186, 130), 'mm', k2, ST.sw)
    text(img, L('THEY NEEDED EACH OTHER', 'ఒకరికొకరు అవసరం'), W / 2, 420, 52, CREAM, 'mm', 'head', e_out(prog(t, s0 + 1.4, s0 + 1.9)), ST.sw, None)
    return img

# ------------------------------------------------------------------ 4.2 kingdoms: approximate extents on a map drawn at output size
@functools.lru_cache(1)
def KMAP(): return AMap(64.0, 92.0, 21.0)
def region(m, lon0, lon1, lat0, lat1, col, a, shape='ellipse', op=.55):
    if a <= .01: return None
    x0, y0 = m.P(lon0, lat1); x1, y1 = m.P(lon1, lat0)
    r = Image.new('L', (W, H), 0); dr = ImageDraw.Draw(r)
    if shape == 'ellipse': dr.ellipse((x0, y0, x1, y1), fill=int(255 * a))
    else: dr.rectangle((x0, y0, x1, y1), fill=int(255 * a))
    r = ImageChops.multiply(r.filter(ImageFilter.GaussianBlur(28 if shape == 'ellipse' else 6)), m.land); lay = Image.new('RGBA', (W, H), col + (0,)); lay.putalpha(r.point(lambda p: int(p * op))); return lay
def s_kingdoms(t, s0, s1):
    c_d = AT('4.2t', 'Deccan', 'మధ్యలో') - .15; c_g = AT('4.2t', 'Golconda,', 'గోల్కొండ') - .1; c_mu = AT('4.2t', 'Mughal', 'ఉత్తరం') - .15
    m = KMAP(); img = m.base.copy()
    # "rose and fell": three regional glows appear and fade in turn (illustrative, unnamed)
    for j, (lo, la) in enumerate(((76.5, 14.5), (73.5, 22.5), (85.0, 24.0))):
        tt = s0 + .2 + j * .45; a = e_io(prog(t, tt, tt + .35)) * (1 - e_io(prog(t, tt + .55, tt + .95)))
        lay = region(m, lo - 2.4, lo + 2.4, la - 2.2, la + 2.2, (196, 160, 92), a)
        if lay: img.paste(lay, (0, 0), lay)
    kd = e_io(prog(t, c_d, c_d + .7))
    steps = [(c_mu, 23.6, 'c.1600'), (c_mu + 1.0, 20.8, '1636'), (c_mu + 2.0, 17.0, '1680s')]
    front = None; lab = None
    for tt, la, yr in steps:
        k_ = e_io(prog(t, tt, tt + .8))
        if k_ > 0: front = lerp(front if front is not None else 30.0, la, k_); lab = yr
    if front is not None:
        lay = region(m, 64.0, 92.0, front, 36.0, (150, 70, 50), 1.0, 'rect', .42)
        if lay: img.paste(lay, (0, 0), lay)
        x0, yF = m.P(66, front); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).line((60, yF, W - 60, yF), fill=(150, 70, 50, 220), width=3); img.paste(lay, (0, 0), lay)
        map_label(img, L('MUGHAL FRONT · ', 'మొఘల్ సరిహద్దు · ') + lab, W - 300, yF - 34, 26, INK, 1.0)
    if front is not None: kd = kd * clamp((front - 17.6) / 2.4)   # the Deccan sultanates fold into the advancing empire
    lay = region(m, 73.3, 81.8, 14.8, 20.6, (66, 120, 110), kd)
    if lay: img.paste(lay, (0, 0), lay)
    if kd > .01:
        x, y = m.P(77.0, 17.8); map_label(img, L('DECCAN SULTANATES', 'దక్కన్ సుల్తానుల రాజ్యాలు'), x, y + 40, 28, INK, kd)
        kg = e_out(prog(t, c_g, c_g + .4)); gx, gy = m.P(78.40, 17.38); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(lay).ellipse((gx - 10, gy - 10, gx + 10, gy + 10), fill=INK + (int(255 * kg),), outline=AMBER + (int(255 * kg),), width=4); img.paste(lay, (0, 0), lay)
        map_label(img, L('GOLCONDA', 'గోల్కొండ'), gx + 110, gy - 30, 26, INK, kg)
    text(img, L('KINGDOMS ROSE AND FELL', 'రాజ్యాలు పుట్టాయి, పడిపోయాయి'), W / 2, 300, 48, CREAM, 'mm', 'head', e_out(prog(t, s0, s0 + .4)), ST.sw, (0, 0, 0))
    credit(img, L('APPROXIMATE EXTENTS · ILLUSTRATIVE', 'సుమారు సరిహద్దులు · ఉదాహరణ'), CREDIT_Y, e_out(prog(t, s0, s0 + .5)))
    return img

# ------------------------------------------------------------------ 4.4 (EN only) Akbar's court -> the survey drawn on a field
def s_akbar(t, s0, s1):
    c_ak = AT('4.4', 'Under', 'Under') - .1; c_tm = AT('4.4', 'measured', 'measured') - .2; c_sv = AT('4.4', 'survey.', 'survey.') - .2
    if t < c_tm - .2:
        img = cover_nat('AKBAR', prog(t, s0, c_tm), (.5, .38), (.5, .46), 1.0, 1.0, prescale=.75, k=.92)
        plate_text(img, (90, 260, W - 90, 400), None, L('ONE OF THE LARGEST STATES ON EARTH', ''), e_out(prog(t, s0 + .3, s0 + .8)) * (1 - prog(t, c_ak - .3, c_ak)), 38)
        if t >= c_ak: plate_text(img, (90, 260, W - 90, 400), L('MUGHAL EMPEROR · r.1556–1605', ''), 'AKBAR', e_out(prog(t, c_ak, c_ak + .4)), 48)
        credit(img, 'ABUL FAZL PRESENTING THE AKBARNAMA · c.1600', CREDIT_Y, 1.0)
        return img
    # the survey shown happening on the field: rope lines draw plot by plot, then each plot gets its assessment
    SS = 2; Wd, Hd = W * SS, H * SS; U = 120 * SS; im = Image.new('RGBA', (Wd, Hd), DUSK + (255,)); d = ImageDraw.Draw(im)
    p = P_iso(U, Wd / 2, 880 * SS); floor(d, p, Wd, Hd); ISO._box(d, p, 0, 0, 5.4, .12, FIELD)
    n = 3; kg = e_io(prog(t, c_tm, c_tm + 1.6))
    for i in range(1, n):
        f = -2.7 + i * 5.4 / n; e = lerp(-2.7, 2.7, clamp(kg * 2)); d.line([p(f, -2.7, .13), p(f, e, .13)], fill=(240, 228, 196), width=5)
        e2 = lerp(-2.7, 2.7, clamp(kg * 2 - 1)); d.line([p(-2.7, f, .13), p(e2, f, .13)], fill=(240, 228, 196), width=5)
    img = im.resize((W, H), Image.LANCZOS); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dd = ImageDraw.Draw(lay)
    for i in range(n):
        for j in range(n):
            tt = c_sv - .6 + (i * n + j) * .12; k_ = e_back(prog(t, tt, tt + .3))
            if k_ > .01:
                cx_, cy_ = [v / SS for v in p(-2.7 + (i + .5) * 5.4 / n, -2.7 + (j + .5) * 5.4 / n, .3)]; coin(dd, cx_, cy_, 16 * k_)
    img.paste(lay, (0, 0), lay)
    plate_text(img, (90, 260, W - 90, 420), L('MINISTER TODAR MAL', ''), L('LAND MEASURED · REVENUE SET BY SURVEY', ''), e_out(prog(t, c_tm, c_tm + .5)), 36)
    small(img, L('ZABT SYSTEM · ILLUSTRATIVE', ''), W / 2, 1330, 22, MUTED, 'mm', e_out(prog(t, c_tm + .5, c_tm + 1.0)))
    return img

# ------------------------------------------------------------------ "kings come and go. The system lasted."
def crown(d, cx, cy, s, a):
    al = int(255 * a); pts = [(-1, .5), (-1, -.4), (-.5, .05), (0, -.6), (.5, .05), (1, -.4), (1, .5)]
    d.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=GOLD_A + (al,), outline=(120, 96, 50, al))
    d.rectangle((cx - s, cy + .5 * s, cx + s, cy + .72 * s), fill=GOLD_A + (al,))
def s_system(t, s0, s1):
    c_sys = AT('SYSTEM', 'system', 'వ్యవస్థ') - .15
    c = dict(drop=-9, farmer=-8, third=1e9, coll=-7, cut=-7, state=-6, army=-5, bank=-4, every=-3)
    img, scr, f, zk = chain_frame(t, c, zoom_k=1.0, Uz=34, Yz=880)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for m_ in range(4):   # coins keep moving along the chain, regardless of the king
        u = ((t - s0) * .35 + m_ / 4) % 1.0; q = u * 3; i0 = int(q); fr = q - i0; a_ = scr(i0, 1.0); b_ = scr(i0 + 1, 1.0)
        coin(d, lerp(a_[0], b_[0], fr), lerp(a_[1], b_[1], fr), 14)
    for j in range(3):    # three crowns, one after another
        tt = s0 + .1 + j * .7; a = e_io(prog(t, tt, tt + .25)) * (1 - (e_io(prog(t, tt + .6, tt + .85)) if j < 2 else 0))
        if a > .01: crown(d, W / 2 + 330, 360, 46, a)
    img.paste(lay, (0, 0), lay)
    text(img, L('KINGS COME AND GO', 'రాజులు వస్తారు, పోతారు'), W / 2 - 60, 360, 40, CREAM, 'mm', 'head', e_out(prog(t, s0, s0 + .4)) * (1 - prog(t, c_sys - .2, c_sys)), 620, None)
    text(img, L('THE SYSTEM LASTED', 'వ్యవస్థ నిలిచింది'), W / 2 - 60, 360, 46, AMBER, 'mm', 'head', e_out(prog(t, c_sys, c_sys + .4)), 620, None)
    return img

ZOOM = set()

def render(t):
    LY.reset(); scn, s0, s1 = scene_at(t)
    if scn == 'loop':
        img = s_loop(t, s0, s1); captions(img, t, 'loop'); return img
    if scn.startswith('cartoon'):
        q = {'cartoon1': 'Q1', 'cartoon2': 'Q2', 'cartoon3': 'Q3'}[scn]; img = cartoon(t, s0, [('CHELLI', q)])
    elif scn == 'slide': img = s_slide(t, s0, s1)
    else: img = globals()['s_' + scn](t, s0, s1)
    img = img.convert('RGB'); overlays(img, t, scn); captions(img, t, scn); return img
