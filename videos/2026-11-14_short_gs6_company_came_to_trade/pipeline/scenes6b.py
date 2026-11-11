
# ------------------------------------------------------------------ GS 6/6 · remaining scenes (full-frame direction, approved Nov 11)
# Composition rule for this file: the whole 1080x1920 frame is the canvas. Maps run edge to edge; archive pictures sit on a blurred,
# darkened backdrop of themselves (texture only) and are never shown above native resolution. Essential text stays above y 1540,
# clear of the caption line (y 1405-1490) and of the right-hand button column in the lower half.
SRC.update({'JAHANGIR': (ARC + '19_PD13_Jahangir_Darbar_David_Collection.jpg', None),
            'FORTW': (ARC + '05_PD16_A_Perspective_View_of_Fort_William_by_Jan_Van_Ryne_1754.jpg', None),
            'DIWANI': (ARC + '02_PD17_Shah_Alam_conveying_the_grant_of_the_Diwani_to_Lord_Clive.jpg', None),
            'FSG': (ARC + '06_PD14_Fort_of_St.George_on_the_Coromandel_Coast_by_Jan_van_Ryne.jpg', (0, 0, 720, 516)),
            'FARMAN': (ARC + '08_NEW_Farman_of_Aurangzeb_National_Museum_New_Delhi_62.5.jpg', None)})
INDIA = (66.0, 94.0, 21.0); WEST = (68.6, 80.6, 23.0); SOUTH = (73.5, 85.5, 15.2); BAY = (76.0, 96.0, 23.4)
PL = {'SURAT': (72.83, 21.17), 'SWALLY': (72.62, 21.08), 'AGRA': (78.01, 27.18), 'DELHI': (77.2, 28.6), 'CALCUTTA': (88.36, 22.57), 'MADRAS': (80.27, 13.08),
      'PONDICHERRY': (79.83, 11.93), 'BOMBAY': (72.88, 19.08), 'BUXAR': (83.98, 25.56), 'PLASSEY': (88.25, 23.8), 'HYDERABAD': (78.47, 17.36), 'ARCOT': (79.32, 12.9)}
def OMV(v0, v1, u, steps=20):
    q = round(clamp(u) * steps) / steps; return OM(*(round(lerp(a, b, q), 3) for a, b in zip(v0, v1)))
def zoomv(v, z):
    """the same map view, zoomed in by z around its centre (z > 1)"""
    c = (v[0] + v[1]) / 2; h = (v[1] - v[0]) / 2 / z; return (c - h, c + h, v[2])

@functools.lru_cache(8)
def BACKDROP(key):
    im = NAT(key).copy(); im.thumbnail((360, 360)); bw = max(W / im.width, H / im.height)
    b = im.resize((int(im.width * bw) + 2, int(im.height * bw) + 2), Image.BILINEAR).filter(ImageFilter.GaussianBlur(26))
    b = b.crop(((b.width - W) // 2, (b.height - H) // 2, (b.width - W) // 2 + W, (b.height - H) // 2 + H))
    return Image.fromarray((np.asarray(b).astype(np.float32) * .34).astype(np.uint8))
def backdrop(key, k=1.0):
    """soft texture behind an archive panel: the same picture, heavily blurred and darkened (never the sharp content)"""
    b = BACKDROP(key).copy()
    if k < 1: b = Image.blend(Image.new('RGB', (W, H), (12, 11, 9)), b, k)
    return b
def cover_zoom(key, u, c0, c1, sc0, sc1):
    """full-frame crop of a large archive picture at sc <= 1.0 (output px per source px), panning c0 -> c1 and easing sc0 -> sc1"""
    im = NAT(key); kk = e_io(clamp(u)); sc = lerp(sc0, sc1, kk); assert sc <= 1.0001
    hw, hh = W / 2 / sc, H / 2 / sc; assert hw * 2 <= im.width + 1 and hh * 2 <= im.height + 1, (key, sc)
    cx = min(max(lerp(c0[0], c1[0], kk) * im.width, hw), im.width - hw); cy = min(max(lerp(c0[1], c1[1], kk) * im.height, hh), im.height - hh)
    return im.resize((W, H), Image.LANCZOS, box=(cx - hw, cy - hh, cx + hw, cy + hh))
def tag(img, s, x, y, px=30, col=CREAM, a=1.0, anchor='mm', bg=(14, 13, 11), maxw=None):
    """a small ink pill for map and picture labels (readable over any background)"""
    if a <= .01: return
    if _tel(s): px = int(px * 1.15)
    f = pick(s, 'monob', px); w = min(f.getlength(s), maxw or 2000) + 30; hh = px * .95
    x0 = x - w / 2 if anchor == 'mm' else (x if anchor == 'lm' else x - w); x0 = min(max(x0, 44), W - 44 - w)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).rounded_rectangle((x0, y - hh, x0 + w, y + hh), 10, fill=bg + (int(225 * a),), outline=GOLD_A + (int(140 * a),), width=2)
    img.paste(lay, (0, 0), lay); text(img, s, x0 + w / 2, y, px, col, 'mm', 'monob', a, maxw, None); LY.reg('label', (x0, y - hh, x0 + w, y + hh), owner=s[:24])
def ink(img, pts, k, col=INK, w=6, a=1.0, dash=None, phase=0.0):
    if k <= .01 or a <= .01: return
    pp = poly_part(pts, clamp(k)); lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    if dash:
        L_ = poly_len(pp); n = int(L_ / dash)
        for i in range(n):
            f0 = (i + phase % 1) / max(n, 1); f1 = f0 + .5 / max(n, 1)
            if f1 <= 1: d.line((poly_at(pp, f0)[0], poly_at(pp, f1)[0]), fill=col + (int(255 * a),), width=w)
    else: d.line(pp, fill=col + (int(255 * a),), width=w, joint='curve')
    img.paste(lay, (0, 0), lay)
def eship(img, x, y, k=1.0, s=1.0, col=CREAM, flip=False):
    """a small European sailing ship (hull, three masts, square sails): a drawn icon, not a portrait of any vessel"""
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); f = -1 if flip else 1; a = int(255 * k)
    hull = [(x - 46 * s * f, y), (x + 46 * s * f, y), (x + 34 * s * f, y + 16 * s), (x - 38 * s * f, y + 16 * s)]
    d.polygon(hull, fill=(54, 40, 28, a), outline=(20, 16, 12, a))
    for mx, mh in ((-22, 54), (4, 66), (28, 46)):
        X = x + mx * s * f; d.line((X, y, X, y - mh * s), fill=(40, 30, 22, a), width=max(2, int(3 * s)))
        for j in (0, 1):
            sy = y - mh * s + 8 * s + j * 22 * s; d.polygon([(X - 13 * s, sy), (X + 13 * s, sy), (X + 15 * s, sy + 18 * s), (X - 15 * s, sy + 18 * s)], fill=col + (a,), outline=(60, 50, 36, a))
    img.paste(lay, (0, 0), lay)
def smoke(img, x, y, t, t0, k=1.0):
    if k <= .01 or t < t0: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for i in range(6):
        v = (t - t0) * .8 + i * .17; f = v % 1.0; r = 10 + 30 * f; al = int(140 * k * (1 - f))
        d.ellipse((x + 40 * f - r + i * 6, y - 60 * f - r, x + 40 * f + r + i * 6, y - 60 * f + r), fill=(214, 206, 188, al))
    img.paste(lay.filter(ImageFilter.GaussianBlur(4)), (0, 0), lay.filter(ImageFilter.GaussianBlur(4)))
def person(d, x, y, s, col, a):
    d.ellipse((x - 9 * s, y - 40 * s, x + 9 * s, y - 22 * s), fill=col + (a,)); d.rounded_rectangle((x - 11 * s, y - 20 * s, x + 11 * s, y + 18 * s), int(6 * s), fill=col + (a,))
def throne(img, x, y, k, lab, chips, kc):
    """a throne with two rival claimants; the companies' chips slide in behind their choices"""
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * k)
    d.rounded_rectangle((x - 34, y - 70, x + 34, y + 10), 10, fill=GOLD_A + (a,), outline=(40, 30, 16, a), width=3); d.rectangle((x - 46, y + 10, x + 46, y + 26), fill=(150, 116, 62, a))
    for j, dx in enumerate((-110, 110)): person(d, x + dx, y + 10, 1.6, (214, 200, 170), a)
    img.paste(lay, (0, 0), lay)
    tag(img, lab, x, y + 72, 30, AMBER, k)
    for j, (dx, c) in enumerate(zip((-110, 110), chips)):
        kk = e_out(clamp(kc * 2 - j * .4))
        if kk > .01: tag(img, c, x + dx, y - 108 - 20 * (1 - kk), 22, INK, kk, bg=(236, 228, 208))
def region_word(img, m, s, ll, k):
    """a large faint region name across the land (context, not a border claim)"""
    if k <= .01: return
    x, y = m.P(*ll); text(img, s, x, y, 64 if not TE else 56, (120, 104, 76), 'mm', 'head', .55 * k, W - 160, None)
def hatch_region(img, m, ll, k, t):
    if k <= .01: return
    pts = [m.P(*p) for p in ll]; mask = Image.new('L', (W, H), 0); ImageDraw.Draw(mask).polygon(pts, fill=255)
    lay = Image.new('RGBA', (W, H), AMBER + (int(40 * k),)); d = ImageDraw.Draw(lay)
    off = (t * 20) % 26
    for i in range(-H, W + H, 26): d.line((i + off, 0, i + off + H, H), fill=AMBER + (int(120 * k),), width=3)
    lay.putalpha(ImageChops.multiply(lay.getchannel('A'), mask)); img.paste(lay, (0, 0), lay); ol = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ol).line(pts + [pts[0]], fill=AMBER + (int(255 * k),), width=5); img.paste(ol, (0, 0), ol)
BBO = [(83.3, 27.3), (84.6, 27.4), (86.0, 26.7), (88.0, 26.5), (89.8, 26.2), (92.2, 25.0), (92.4, 22.4), (91.6, 22.0), (89.0, 21.7), (87.5, 21.4),
       (86.6, 20.4), (85.4, 19.9), (85.0, 21.0), (84.2, 22.4), (83.4, 23.8), (83.3, 25.4)]     # Bengal, Bihar and Orissa (approximate area)

# ---- 1 · hook: Jahangir's court -> 150 years -> Fort William, Bengal
def s_hook(t, s0, s1, frame0=False):
    c150 = AT('A', 'hundred', 'నూట') - .15; chelp = AT('A', 'helped', 'బెంగాల్') - .15
    if frame0: t = 0.0
    if t < c150:
        img = cover_zoom('JAHANGIR', prog(t, 0, c150 + 2), (.55, .52), (.6, .5), .62, .7)
        plate(img, (90, 260, W - 90, 560), 1.0)
        text(img, '1608', W / 2, 345, 110, AMBER, 'mm', 'head', 1.0, None, None)
        text(img, L('IT CAME ASKING PERMISSION', 'అనుమతి అడిగి వచ్చింది'), W / 2, 470, 54 if not TE else 50, CREAM, 'mm', 'head', 1.0, W - 260, None); LY.reg('card', (90, 260, W - 90, 560), owner='hook')
        tag(img, L("JAHANGIR'S COURT · c. 1620 · DAVID COLLECTION · PD", 'జహంగీర్ దర్బార్ · c. 1620 · పబ్లిక్ డొమైన్'), W / 2, 1340, 26, PARCH)
        return img
    if t < chelp:
        u = e_io(prog(t, c150, chelp - .1)); yr = int(round(lerp(1608, 1757, u)))
        img = Image.blend(cover_zoom('JAHANGIR', 1.0, (.6, .5), (.6, .5), .7, .7), Image.new('RGB', (W, H), (12, 11, 9)), .78)
        text(img, str(yr), W / 2, 820, 230, CREAM, 'mm', 'head', 1.0, None, (0, 0, 0))
        small(img, L('150 YEARS LATER', '150 ఏళ్ల తర్వాత'), W / 2, 1000, 40, AMBER, 'mm', e_out(prog(t, c150, c150 + .4)))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); d.line((110, 1180, W - 110, 1180), fill=(110, 100, 80, 230), width=6)
        d.line((110, 1180, lerp(110, W - 110, u), 1180), fill=GOLD_A + (255,), width=10); img.paste(lay, (0, 0), lay)
        small(img, '1608', 110, 1230, 32, PARCH, 'lm'); small(img, '1757', W - 110, 1230, 32, AMBER, 'rm')
        return img
    img = backdrop('FORTW'); k = 1.0
    panel_nat(img, 'FORTW', (0, 560, W, 560 + 669), prog(t, chelp, s1 + 1), (.42, .5), (.5, .5), sc=W / 1629 * 1.0, radius=0, a=k)
    plate_text(img, (90, 290, W - 90, 500), L('1757 · THE COMPANY HELPED', '1757 · కంపెనీ'), L("A NAWAB ON BENGAL'S THRONE", 'బెంగాల్ నవాబునే మార్చేసింది'), k, 56 if not TE else 50, owner='hook2')
    tag(img, L('FORT WILLIAM, CALCUTTA · VAN RYNE, 1754 · PD', 'ఫోర్ట్ విలియం, కలకత్తా · 1754 · పబ్లిక్ డొమైన్'), W / 2, 1290, 26, PARCH)
    return img

# ---- 2 · EN only: Hawkins, Swally, 1613 approval, Roe (west India map, full frame)
def s_perm(t, s0, s1):
    ch = AT('A', 'Hawkins', '') - .15; ctr = AT('A', 'travelled', ''); cj = AT('A', 'Jahangir.', '')
    c12 = AT('A', '1612,', '') - .15; csw = AT('A', 'Swally,', '') - .2; cof = AT('A', 'officials', '') - .1
    cdl = AT('A', 'deal', '') - .15; ccf = AT('A', 'confirmed', '') - .15; c15 = AT('A', '1615', '') - .2
    if t >= c15: return s_roe(t, c15, s1)
    m = OMV(WEST, zoomv(WEST, 1.08), prog(t, s0, c15)); img = m.base.copy(); k = e_out(prog(t, s0, s0 + .4))
    region_word(img, m, L('MUGHAL EMPIRE', 'మొఘల్ సామ్రాజ్యం'), (76.6, 24.6), k)
    rail_strip(img, 1 if t >= ccf else 0, k, 300, k_last=e_io(prog(t, ccf, ccf + .8)) if t >= ccf else 1.0)
    sx, sy = m.P(*PL['SURAT']); ax, ay = m.P(*PL['AGRA'])
    road = [m.P(72.83, 21.17), m.P(74.6, 23.4), m.P(75.9, 25.2), m.P(78.01, 27.18)]
    kr = e_io(prog(t, ctr - .2, cj + .4)); ink(img, road, kr, (60, 46, 30), 6, 1.0, dash=34, phase=t * .6)
    pin(img, sx, sy, e_out(prog(t, ch, ch + .4))); tag(img, L('SURAT · 1608 · HAWKINS', ''), sx + 30, sy - 70, 32, CREAM, e_out(prog(t, ch, ch + .4)), 'lm')
    ka = e_out(prog(t, cj - .3, cj + .1)); pin(img, ax, ay, ka); tag(img, L("AGRA · JAHANGIR'S COURT", ''), ax, ay - 66, 32, CREAM, ka)
    # Swally, 1612: English ships (cream sails) and a Portuguese fleet (grey sails) off the coast near Surat
    kw = e_out(prog(t, c12, c12 + .6)) * (1 - e_io(prog(t, cdl, cdl + .5)))
    if kw > .01:
        wx, wy = m.P(*PL['SWALLY']); u = prog(t, c12, csw + 1.5)
        for j, (ox, oy) in enumerate(((-250, 60), (-200, 150))): eship(img, wx + ox + 60 * u, wy + oy, kw, 1.25, CREAM)
        for j, (ox, oy) in enumerate(((-90, 210), (-20, 290))): eship(img, wx + ox - 120 * e_io(prog(t, csw + 1.0, cof + 1.0)), wy + oy, kw * (1 - .5 * prog(t, cof, cof + 1)), 1.15, (150, 146, 140), True)
        smoke(img, wx - 140, wy + 110, t, csw, kw); smoke(img, wx - 40, wy + 230, t + .4, csw + .3, kw)
        tag(img, L('SWALLY · 1612 · ENGLISH vs PORTUGUESE', ''), W / 2, min(wy + 360, 1340), 30, CREAM, kw)
        tag(img, L('MUGHAL OFFICIALS TOOK NOTICE', ''), sx + 20, sy - 140, 30, AMBER, kw * e_out(prog(t, cof, cof + .4)), 'lm')
    # 1613: the deal with Surat's governor, confirmed by the emperor
    kd = e_out(prog(t, cdl + .45, cdl + .85))
    if kd > .01:
        ink(img, road, 1.0, AMBER, 8, e_out(prog(t, ccf, ccf + .6)))
        plate_text(img, (90, 1150, W - 90, 1370), L("A DEAL WITH SURAT'S GOVERNOR", ''), L('1613 · CONFIRMED BY THE EMPEROR', ''), kd, 46, owner='1613',
                   sub=L('TRADING APPROVAL · THE ENGLISH COULD TRADE AT SURAT', '') if t >= ccf else None)
    return img
def s_roe(t, c0, s1):
    img = cover_zoom('JAHANGIR', prog(t, c0, s1 + .5), (.62, .62), (.64, .55), .78, .9); k = e_out(prog(t, c0, c0 + .3))
    plate_text(img, (90, 270, W - 90, 470), L('1615–19 · SIR THOMAS ROE AT COURT', ''), L('PRESSING FOR BETTER TERMS', ''), k, 50, owner='roe', sub=L("KING JAMES'S AMBASSADOR", ''))
    tag(img, L("JAHANGIR'S COURT, c. 1620 · ROE IS NOT SHOWN", ''), W / 2, 1340, 28, PARCH, k)
    return img

# ---- 3 · the 1686 war, lost; the terms; Calcutta 1690 (India map, full frame). TE opens with the simplified 1608 -> 1613 marks.
def te_permission(img, t, s0):
    """TE only: two big marks a phone can read (1608 asked -> 1613 approved), Roe as a small secondary tick"""
    k = e_out(prog(t, s0, s0 + .4)) * (1 - e_io(prog(t, AT('A', '', '1686లో') - .5, AT('A', '', '1686లో') - .1)))
    if k <= .01: return
    plate(img, (70, 520, W - 70, 1320), k)
    for i, (yr, lab, y, c) in enumerate((('1608', 'అనుమతి కోరారు', 700, CREAM), ('1613', 'ఆమోదం', 1060, AMBER))):
        kk = k * e_out(prog(t, s0 + .1 + i * 1.1, s0 + .5 + i * 1.1))
        text(img, yr, W / 2, y - 50, 96, c, 'mm', 'head', kk, None, None); text(img, lab, W / 2, y + 60, 66, c, 'mm', 'head', kk, ST.sw - 120, None)
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); ka = int(255 * k * e_out(prog(t, s0 + .6, s0 + 1.2)))
    d.line((W / 2, 830, W / 2, 940), fill=GOLD_A + (ka,), width=6); d.polygon([(W / 2 - 18, 930), (W / 2 + 18, 930), (W / 2, 960)], fill=GOLD_A + (ka,)); img.paste(lay, (0, 0), lay)
    small(img, 'రో 1615–19 · ఆస్థానంలో రాయబారి', W / 2, 1240, 26, MUTED, 'mm', k * e_out(prog(t, s0 + 1.6, s0 + 2.0)))
def s_war(t, s0, s1):
    c86 = AT('A', '1686,', '1686లో') - .15; cwar = AT('A', 'war', 'యుద్ధానికి') - .1; clost = AT('A', 'lost.', 'ఓడిపోయింది.') - .15
    cpar = AT('A', 'pardon,', 'క్షమాపణ') - .2; cfin = AT('A', 'fine,', 'జరిమానా') - .2; cbeh = AT('A', 'promise', 'ఉంటామని') - .2
    ctr = AT('A', 'trade', 'వ్యాపారానికి') - .15; c90 = AT('A', '1690,', '1690లో') - .15; ccal = AT('A', 'Calcutta.', 'కలకత్తా.') - .2
    m = OMV(INDIA, zoomv(INDIA, 1.08), prog(t, s0, s1)); img = m.base.copy(); k = e_out(prog(t, s0, s0 + .4))
    region_word(img, m, L('MUGHAL EMPIRE', 'మొఘల్ సామ్రాజ్యం'), (79.5, 25.0), k)
    if TE and t < c86: te_permission(img, t, s0); rail_strip(img, 1, k * .6, 300); return img
    rail_strip(img, 2, k, 300, k_last=e_io(prog(t, clost, clost + .8)))
    dx, dy = m.P(*PL['DELHI']); bx, by = m.P(*PL['BOMBAY']); hx, hy = m.P(*PL['CALCUTTA'])
    km = e_out(prog(t, s0, s0 + .5)); pin(img, dx, dy, km, CREAM); tag(img, L('MUGHAL EMPIRE · AURANGZEB', 'మొఘల్ సామ్రాజ్యం · ఔరంగజేబు'), dx, dy - 70, 30, CREAM, km)
    kw = e_io(prog(t, cwar, cwar + 1.2)); back = e_io(prog(t, clost, clost + 1.0))
    for (x0, y0) in ((bx, by), (hx, hy)):
        tip = (lerp(x0, dx, .62 * kw * (1 - .5 * back)), lerp(y0, dy, .62 * kw * (1 - .5 * back)))
        ink(img, [(x0, y0), tip], 1.0 if kw > .01 else 0, (130, 38, 28) if not back else (90, 70, 56), 9, 1 - .5 * back)
    tag(img, L('1686 · THE COMPANY WENT TO WAR', '1686 · కంపెనీ యుద్ధానికి దిగింది'), W / 2, 470, 32, CREAM, e_out(prog(t, cwar - .3, cwar + .2)))
    kl = e_out(prog(t, clost, clost + .35))
    if kl > .01 and t < c90: text(img, L('LOST', 'ఓటమి'), W / 2, 980, 150 if not TE else 120, (230, 214, 180), 'mm', 'head', kl * (1 - e_io(prog(t, cpar - .3, cpar))), None, (20, 14, 10))
    # the terms, as the narrator states them (a separate cartouche; no document is shown here)
    if cpar - .2 <= t < c90:
        ka = e_out(prog(t, cpar - .2, cpar + .2)) * (1 - e_io(prog(t, c90 - .3, c90)))
        plate(img, (80, 820, W - 80, 1370), ka)
        small(img, L('TO TRADE AGAIN, THE COMPANY HAD TO:', 'మళ్లీ వ్యాపారం చేయాలంటే:'), W / 2, 880, 30, AMBER, 'mm', ka)
        for i, (c_, s_) in enumerate(((cpar, L("BEG THE EMPEROR'S PARDON", 'క్షమాపణ వేడుకోవాలి')), (cfin, L('PAY A HEAVY FINE', 'భారీ జరిమానా కట్టాలి')), (cbeh, L('PROMISE TO BEHAVE', 'బుద్ధిగా ఉంటామని మాటివ్వాలి')))):
            kk = ka * e_out(prog(t, c_, c_ + .35)); y = 990 + i * 110
            text(img, f'{i + 1}', 170, y, 54, AMBER, 'mm', 'head', kk, None, None); text(img, s_, 230, y, 50 if not TE else 44, CREAM, 'lm', 'head', kk, W - 330, None)
        kt = ka * e_out(prog(t, ctr, ctr + .3)); small(img, L('ONLY THEN COULD IT TRADE AGAIN', 'అప్పుడే మళ్లీ వ్యాపారం'), W / 2, 1320, 30, PARCH, 'mm', kt)
        LY.reg('card', (80, 820, W - 80, 1370), owner='terms')
    kc = e_out(prog(t, c90, c90 + .4))
    if kc > .01:
        pin(img, hx, hy, kc, AMBER, 16); tag(img, L('1690 · CALCUTTA · A NEW BASE IN BENGAL', '1690 · కలకత్తా · బెంగాల్‌లో కొత్త స్థావరం'), W / 2, hy + 300, 32, AMBER, kc * e_out(prog(t, ccal - .4, ccal)) if False else kc)
    return img

# ---- 4 · the 1717 farman (example document) -> the passes misused on Bengal's rivers
def s_farman(t, s0, s1):
    cfa = AT('A', 'farman:', 'ఫర్మానా') - .3; cdf = AT('A', 'duty-free', 'సుంకం') - .15; c3k = AT('A', '3,000', '3,000') - .15; cps = AT('A', 'passes', 'దస్తక్') - .15
    cco = AT('A', 'men', 'కంపెనీ', n=1 if not TE else 3) - (.5 if not TE else .15)
    if t >= cco: return s_passes(t, cco, s1)
    img = backdrop('FARMAN'); k = e_out(prog(t, s0, s0 + .4))
    rail_strip(img, 3, k, 300, k_last=e_io(prog(t, s0, s0 + .8)))
    # left: an example of a Mughal farman (Aurangzeb's, National Museum, New Delhi); NOT the 1717 grant
    ke = e_out(prog(t, s0 + .2, s0 + .7)); fb = (40, 470, 560, 1380)
    panel_nat(img, 'FARMAN', fb, prog(t, cfa, cco), (.5, .38), (.5, .55), sc=.64, radius=10, a=ke, border=GOLD_A)
    tag(img, L("EXAMPLE: A FARMAN OF AURANGZEB · NOT THE 1717 GRANT", 'ఉదాహరణ: ఔరంగజేబు ఫర్మానా · 1717 ఫర్మానా కాదు'), W / 2, 412, 28, AMBER, ke)
    # right: what the 1717 farman gave
    x0 = 600; rows = [(s0, L('1717', '1717'), L("FARRUKHSIYAR'S FARMAN", 'ఫరూఖ్‌సియర్ ఫర్మానా')), (cdf, L('DUTY-FREE', 'సుంకం లేదు'), L('TRADE IN BENGAL', 'బెంగాల్ వ్యాపారం')),
                      (c3k, L('3,000', '3,000'), L('RUPEES A YEAR', 'రూపాయలు ఏటా')), (cps, L('PASSES', 'పాసులు'), L('CALLED DASTAKS', 'దస్తక్‌లు'))]
    for i, (c_, big, sm) in enumerate(rows):
        kk = e_out(prog(t, c_, c_ + .35)); y = 560 + i * 205
        if kk <= .01: continue
        plate(img, (x0, y - 80, W - 40, y + 90), kk)
        text(img, big, x0 + 30, y - 20, 62 if not TE else 56, AMBER if i else CREAM, 'lm', 'head', kk, W - x0 - 100, None)
        small(img, sm, x0 + 30, y + 45, 28, CREAM, 'lm', kk, W - x0 - 100); LY.reg('card', (x0, y - 80, W - 40, y + 90), owner=f'farman{i}')
    tag(img, L('NATIONAL MUSEUM, NEW DELHI', 'నేషనల్ మ్యూజియం, న్యూఢిల్లీ'), 300, 1340, 24, PARCH, ke)
    return img
def river_scene(img, t, k):
    """Bengal's river as a broad band down the whole frame, with a toll post on the bank"""
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    xs = lambda y: 470 + 90 * math.sin(y / 420 + .6)
    pts = [(xs(y) - 230, y) for y in range(-40, H + 80, 40)] + [(xs(y) + 230, y) for y in range(H + 40, -80, -40)]
    d.polygon(pts, fill=(96, 118, 122, int(255 * k)))
    for i in range(16):
        y = ((i * 140 + t * 70) % (H + 200)) - 100; d.line((xs(y) - 90, y, xs(y) - 30, y + 6), fill=(150, 170, 172, int(120 * k)), width=3)
    img.paste(lay, (0, 0), lay); return xs
def boat(img, x, y, k, col, s=1.0, flag=None, pass_k=0.0):
    if k <= .01: return
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); a = int(255 * k)
    d.polygon([(x - 50 * s, y), (x + 50 * s, y), (x + 34 * s, y + 22 * s), (x - 34 * s, y + 22 * s)], fill=col + (a,), outline=(20, 16, 12, a))
    d.rectangle((x - 22 * s, y - 26 * s, x + 22 * s, y), fill=(196, 170, 120, a))
    if flag: d.line((x + 30 * s, y, x + 30 * s, y - 60 * s), fill=(30, 24, 18, a), width=3); d.rectangle((x + 30 * s, y - 60 * s, x + 62 * s, y - 40 * s), fill=flag + (a,))
    if pass_k > .01: d.rounded_rectangle((x - 70 * s, y - 80 * s, x - 18 * s, y - 40 * s), 4, fill=(236, 228, 208, int(a * pass_k)), outline=AMBER + (int(a * pass_k),), width=3)
    img.paste(lay, (0, 0), lay)
def s_passes(t, c0, s1):
    cmis = AT('A', 'misused', 'దుర్వినియోగం') - .2; cpri = AT('A', 'private', 'సొంత') - .15
    img = radial_bg(W, H, (64, 56, 40), (30, 26, 20), cy=.5, reach=1.0).copy(); k = e_out(prog(t, c0, c0 + .35))
    xs = river_scene(img, t, k); rail_strip(img, 3, k, 300)
    # toll post (chowki) on the right bank, with its lamp
    px, py = 880, 1000; lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((px - 90, py - 100, px + 90, py + 60), fill=(120, 92, 60, int(255 * k)), outline=(30, 22, 14, int(255 * k)), width=3); d.polygon([(px - 115, py - 100), (px + 115, py - 100), (px, py - 190)], fill=(90, 66, 42, int(255 * k)))
    lamp = 1 - .75 * e_io(prog(t, cmis, cmis + 1.0)); d.ellipse((px - 24, py - 46, px + 24, py + 2), fill=AMBER + (int(255 * k * lamp),)); img.paste(lay, (0, 0), lay)
    tag(img, L('TOLL POST', 'సుంకం చౌకీ'), px - 20, py + 110, 30, CREAM, k)
    # the Company's own boat shows its pass and goes through duty-free
    u = ((t - c0) / 4.0) % 1.0; y = lerp(-80, H + 80, u); boat(img, xs(y), y, k, (70, 52, 34), 2.0, flag=(236, 228, 208), pass_k=1.0)
    plate_text(img, (80, 470, W - 80, 650), L('THE FARMAN AT WORK', 'ఫర్మానా పని తీరు'), L('COMPANY BOAT + PASS = NO DUTY', 'కంపెనీ పడవ + పాసు = సుంకం లేదు'), k * (1 - e_io(prog(t, cmis - .3, cmis))), 44 if not TE else 40, owner='pass')
    # private boats of Company men show the same pass
    kp = e_out(prog(t, cmis, cmis + .5))
    if kp > .01:
        for j in range(4):
            uj = ((t - cmis) / 3.2 + j * .25) % 1.0; yj = lerp(-80, H + 80, uj); boat(img, xs(yj) + (-80 if j % 2 else 80), yj, kp, (110, 84, 60), 1.4, pass_k=1.0)
        plate_text(img, (80, 470, W - 80, 690), L("COMPANY MEN'S PRIVATE TRADE", 'ఉద్యోగుల సొంత వ్యాపారం'), L('PASSES MISUSED', 'పాసుల దుర్వినియోగం'), kp, 60 if not TE else 54, owner='misuse')
    return img

# ---- 6 · the wars in the south (south India map, full frame)
def s_wars(t, s0, s1):
    c40 = AT('B', '1740s', '1740,') - .15; cfr = AT('B', 'French', 'ఫ్రెంచ్,') - .15; cen = AT('B', 'English', 'ఇంగ్లీష్') - .15; cfo = AT('B', 'fought', 'పోరాడాయి.') - .2
    csp = AT('B', 'sepoys,', 'సిపాయిలు') - .2; cdr = AT('B', 'drill.', 'శిక్షణ') - .15; cba = AT('B', 'backed', 'కర్ణాటక,') - .3
    cca = AT('B', 'Carnatic', 'కర్ణాటక,') - .15; chy = AT('B', 'Hyderabad.', 'హైదరాబాద్') - .15; cff = AT('B', 'French', 'మొదట', n=2 if not TE else 1) - .15
    m = OMV(SOUTH, zoomv(SOUTH, 1.1), prog(t, s0, s1)); img = m.base.copy(); k = e_out(prog(t, s0, s0 + .4))
    rail_strip(img, 4, k, 300, k_last=e_io(prog(t, c40, c40 + .8)))
    tag(img, L('SOUTH INDIA', 'దక్షిణ భారతం'), W / 2, 420, 32, CREAM, k * (1 - e_io(prog(t, cen, cen + .3))))
    mx, my = m.P(*PL['MADRAS']); px_, py_ = m.P(*PL['PONDICHERRY'])
    kdec = e_out(prog(t, s0 + .2, s0 + .8)) * (1 - e_io(prog(t, cfr - .2, cfr + .4)))     # the decades, large and drifting, until the first pin lands
    if kdec > .01: text(img, L('1740s–50s', '1740–50లు'), W / 2 - 60 + 120 * prog(t, s0, cfr + .4), 760, 150 if not TE else 130, (236, 228, 208), 'mm', 'head', .55 * kdec, None, None)
    ko = e_io(prog(t, s0 + .3, cfr + .3)) * (1 - e_io(prog(t, csp - .4, csp)))     # the Coromandel coast is ringed slowly while the decade is named
    if ko > .01:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); cxo, cyo = (mx + px_) / 2, (my + py_) / 2
        n = int(72 * ko); pts_ = [(cxo + 190 * math.cos(-math.pi / 2 + 2 * math.pi * i / 72), cyo + 260 * math.sin(-math.pi / 2 + 2 * math.pi * i / 72)) for i in range(n + 1)]
        for i in range(0, len(pts_) - 1, 2): d.line((pts_[i], pts_[i + 1]), fill=GOLD_A + (230,), width=5)
        img.paste(lay, (0, 0), lay)
    kpl = 1 - e_io(prog(t, csp - .4, csp))
    kf = e_out(prog(t, cfr, cfr + .4)); ke = e_out(prog(t, cen, cen + .4))
    pin(img, px_, py_, kf, (150, 146, 140)); pin(img, mx, my, ke, CREAM)
    tag(img, L('PONDICHERRY · FRENCH', 'పాండిచ్చేరి · ఫ్రెంచ్'), px_ - 40, py_ + 60, 30, CREAM, kf * kpl, 'rm')
    tag(img, L('MADRAS · ENGLISH', 'మద్రాసు · ఇంగ్లీష్'), mx + 40, my - 64, 30, CREAM, ke * kpl, 'lm')
    kx = e_out(prog(t, cfo, cfo + .5))
    if kx > .01:
        for j in range(5):
            ph = (t * 1.3 + j * .2) % 1.0; ax_ = lerp(px_, mx, ph); ay_ = lerp(py_, my, ph)
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(lay).ellipse((ax_ - 8, ay_ - 8, ax_ + 8, ay_ + 8), fill=AMBER + (int(200 * kx * math.sin(math.pi * ph)),)); img.paste(lay, (0, 0), lay)
    # Fort St George (Madras) engraving, native pixels, high in the frame until the sepoys arrive
    kg = e_out(prog(t, cen, cen + .4)) * (1 - e_io(prog(t, csp - .3, csp)))
    if kg > .01:
        panel_nat(img, 'FSG', (60, 380, 60 + 700, 380 + 502), prog(t, cen, csp), (.45, .5), (.55, .5), sc=700 / 720, radius=10, a=kg, border=GOLD_A)
        tag(img, L('FORT ST GEORGE, MADRAS · VAN RYNE · PD', 'ఫోర్ట్ సెయింట్ జార్జ్, మద్రాసు · పబ్లిక్ డొమైన్'), 410, 920, 26, PARCH, kg)
    # sepoys: rows of Indian soldiers drilled in the European way, marching up from the bottom edge
    ks = e_out(prog(t, csp, csp + .5)) * (1 - e_io(prog(t, cba - .2, cba + .2)))
    if ks > .01:
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); dr = e_io(prog(t, cdr, cdr + 1.2))
        d.rectangle((0, 1180, W, H), fill=(40, 34, 26, int(200 * ks)))
        d.rectangle((0, 1395, W, 1505), fill=(24, 20, 16, int(150 * ks)))
        for r, yr_ in enumerate((1330, 1560, 1672, 1784, 1896)):      # rows skip the caption line (y 1405-1490)
            for c in range(7):
                kk = e_out(clamp((prog(t, csp, csp + 1.4) * 1.6 - r / 8 - c / 30) * 2))
                x = 140 + c * 133 + (1 - dr) * (((r * 7 + c * 3) % 5) - 2) * 14; y = yr_ + (1 - kk) * 300
                person(d, x, y, 2.0, SEPOY if (r + c) % 3 else (226, 166, 60), int(255 * ks * kk))
                d.line((x + 16, y - 46, x + 16, y + 10), fill=(60, 50, 40, int(255 * ks * kk)), width=4)
        img.paste(lay, (0, 0), lay)
        plate_text(img, (80, 1080, W - 80, 1270), L('SEPOYS', 'సిపాయిలు'), L('INDIAN SOLDIERS · EUROPEAN DRILL', 'భారతీయ సైనికులు · యూరోపియన్ శిక్షణ'), ks, 44 if not TE else 40, owner='sepoys')
    # rival claimants: two thrones, the companies back their choices
    kt = e_out(prog(t, cba, cba + .5))
    if kt > .01:
        hx, hy = m.P(*PL['HYDERABAD']); cx_, cy_ = m.P(*PL['ARCOT'])
        kt = kt * (1 - e_io(prog(t, cff - .3, cff)))
        throne(img, hx + 60, hy - 30, kt * e_out(prog(t, chy - .6, chy)) if not TE else kt * e_out(prog(t, chy, chy + .4)), L('HYDERABAD', 'హైదరాబాద్'), (L('FRENCH', 'ఫ్రెంచ్'), L('ENGLISH', 'ఇంగ్లీష్')), prog(t, chy, chy + 1.2))
        throne(img, cx_ - 150, cy_ - 60, kt * e_out(prog(t, cca - .3, cca + .2)), L('CARNATIC', 'కర్ణాటక'), (L('ENGLISH', 'ఇంగ్లీష్'), L('FRENCH', 'ఫ్రెంచ్')), prog(t, cca + .3, cca + 1.5))
        tag(img, L('RIVAL CLAIMANTS TO THE THRONES', 'సింహాసనాల కోసం పోటీ వారసులు'), W / 2, 470, 30, CREAM, kt)
    kff = e_out(prog(t, cff, cff + .4))
    if kff > .01: plate_text(img, (90, 1160, W - 90, 1340), '1749', L('THE FRENCH DID IT FIRST', 'మొదట ఫ్రెంచ్ వాళ్లే'), kff, 54 if not TE else 50, owner='first')
    return img

# ---- 7 · the dangerous lesson: two halves of the frame
def s_lesson(t, s0, s1):
    cf = AT('B', 'Fighting', 'మొఘలులతో') - .15; cfa = AT('B', 'failed.', 'ఓడిపోయింది.') - .15; cc = AT('B', 'choosing', 'రాజులను') - .15; cp = AT('B', 'paid.', 'లాభం.') - .15
    img = radial_bg(W, H, (30, 26, 20), (9, 9, 9)).copy(); k = e_out(prog(t, s0, s0 + .4))
    kL = e_out(prog(t, cf, cf + .5)); kR = e_io(prog(t, cc, cc + .7))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle((0, 0, W / 2 - 4, H), fill=(58, 56, 52, int(150 * kL))); d.rectangle((W / 2 + 4, H - H * kR, W, H), fill=(120, 84, 30, int(150 * kR)))
    d.line((W / 2, 260, W / 2, H), fill=GOLD_A + (int(200 * k),), width=4); img.paste(lay, (0, 0), lay)
    plate_text(img, (90, 270, W - 90, 440), L("THE TRADERS' LESSON", 'వ్యాపారులు నేర్చుకున్నది'), L('SOMETHING DANGEROUS', 'ఒక ప్రమాదకరమైన విషయం'), k, 54 if not TE else 50, owner='lesson', sub=L("NARRATOR'S READING", 'కథకుడి విశ్లేషణ'))
    for side, kk, big, s1_, s2_, col in ((0, kL, L('FIGHTING', 'యుద్ధం'), L('THE MUGHALS', 'మొఘలులతో'), '1686', (196, 190, 178)), (1, kR, L('CHOOSING', 'రాజులను'), L('RULERS', 'ఎంచుకోవడం'), '1740s', AMBER)):
        if kk <= .01: continue
        cx = W / 4 if side == 0 else 3 * W / 4
        small(img, s2_, cx, 620, 40, PARCH, 'mm', kk); text(img, big, cx, 760, 76 if not TE else 64, col, 'mm', 'head', kk, W / 2 - 50, None)
        text(img, s1_, cx, 860, 50 if not TE else 46, col, 'mm', 'head', kk, W / 2 - 50, None)
    kf_ = e_out(prog(t, cfa, cfa + .3)); kp_ = e_out(prog(t, cp, cp + .3))
    if kf_ > .01: text(img, L('FAILED', 'ఓటమి'), W / 4, 1120, 92 if not TE else 80, (150, 146, 140), 'mm', 'head', kf_, W / 2 - 40, None)
    if kp_ > .01: text(img, L('PAID', 'లాభం'), 3 * W / 4, 1120 - 20 * (1 - kp_), 120 if not TE else 96, AMBER, 'mm', 'head', kp_, W / 2 - 40, (20, 12, 4))
    return img

# ---- 8 · Siraj-ud-Daulah, 1756 (Fort William high, the Bay of Bengal below)
def s_siraj(t, s0, s1):
    cs = AT('B', 'Siraj-ud-Daulah', 'సిరాజ్-ఉద్-దౌలా') - .2; cfo = AT('B', 'fortifications', 'కోటలు') - .2; cpa = AT('B', 'passes.', 'పాసులను') - .2
    c56 = AT('B', '1756,', '1756లో') - .15; cse = AT('B', 'seized', 'కలకత్తాను') - .15; carm = AT('B', 'army', 'సైన్యాన్ని') - .3; cma = AT('B', 'Madras.', 'మద్రాసు') - .2
    m = OMV(BAY, zoomv(BAY, 1.06), prog(t, s0, s1)); img = m.base.copy(); k = e_out(prog(t, s0, s0 + .4))
    rail_strip(img, 4, k * .9, 300)
    hx, hy = m.P(*PL['CALCUTTA']); mx, my = m.P(*PL['MADRAS'])
    # Fort William, 1754 (native pixels), with museum labels; it gives way to the map at 1756
    kp = k * (1 - e_io(prog(t, c56 - .3, c56 + .1)))
    if kp > .01:
        img.paste(Image.blend(img, Image.new('RGB', (W, H), (12, 11, 9)), .5 * kp))
        panel_nat(img, 'FORTW', (0, 420, W, 420 + 669), prog(t, s0, c56), (.42, .5), (.5, .5), sc=W / 1629, radius=0, a=kp)
        tag(img, L('FORT WILLIAM, CALCUTTA · 1754 · PD', 'ఫోర్ట్ విలియం, కలకత్తా · 1754'), W / 2, 1140, 26, PARCH, kp)
        plate_text(img, (80, 1190, W - 80, 1370), L('BENGAL · THE YOUNG NAWAB', 'బెంగాల్ · యువ నవాబు'), L('SIRAJ-UD-DAULAH WAS ANGRY', 'సిరాజ్-ఉద్-దౌలా కోపంగా ఉన్నాడు'), kp * e_out(prog(t, cs, cs + .4)), 48 if not TE else 44, owner='siraj')
        k1 = kp * e_out(prog(t, cfo, cfo + .35)); k2 = kp * e_out(prog(t, cpa, cpa + .35))
        if k1 > .01: ink(img, [(300, 560), (440, 700)], 1.0, CREAM, 4, k1); tag(img, L('FORTIFICATIONS', 'కోటలు'), 300, 540, 32, CREAM, k1)
        if k2 > .01: tag(img, L('PASSES ABUSED', 'పాసుల దుర్వినియోగం'), 760, 1000, 32, AMBER, k2)
        return img
    kc = e_out(prog(t, c56, c56 + .4)); pin(img, hx, hy, kc, AMBER, 18)
    if kc > .01:      # Calcutta taken: a slow ink ring keeps pulsing out from the pin
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        hr = 260; hal = int(kc * (28 + 26 * math.sin((t - c56) * 2.6)))      # a slow amber halo breathes over Calcutta
        d.ellipse((hx - hr, hy - hr, hx + hr, hy + hr), fill=AMBER + (hal,))
        for j in range(2):
            f = ((t - c56) / 1.8 + j * .5) % 1.0; r = 30 + 150 * f; d.ellipse((hx - r, hy - r, hx + r, hy + r), outline=AMBER + (int(200 * kc * (1 - f)),), width=5)
        img.paste(lay, (0, 0), lay)
    plate_text(img, (80, 420, W - 80, 640), '1756', L('SIRAJ-UD-DAULAH TAKES CALCUTTA', 'కలకత్తాను సిరాజ్ స్వాధీనం చేసుకున్నాడు'), kc * e_out(prog(t, cse - .2, cse + .2)), 50 if not TE else 44, owner='1756')
    tag(img, L('CALCUTTA', 'కలకత్తా'), hx - 30, hy - 60, 30, CREAM, kc, 'rm')
    ka = e_out(prog(t, carm - .2, carm + .3))
    if ka > .01:
        route = m.path([PL['MADRAS'], (82.6, 15.4), (86.0, 18.6), (88.0, 21.0), PL['CALCUTTA']], 8); u = e_io(prog(t, carm, carm + 2.4))
        pin(img, mx, my, ka, CREAM); ink(img, route, u, AMBER, 7, ka, dash=26, phase=-t)
        (sx, sy), _a = poly_at(route, u); eship(img, sx, sy - 10, ka, 1.1)
        tag(img, L('AN ARMY SENT FROM MADRAS', 'మద్రాసు నుంచి సైన్యం'), 700, 1250, 32, AMBER, ka)
    return img

# ---- 12 · Buxar 1764, the diwani 1765 (India map, full frame; West's later painting as an inset)
def s_buxar(t, s0, s1):
    cpl = AT(KC, 'Plassey', 'ప్లాసీ') - .1; cbx = AT(KC, 'Buxar', 'బక్సర్‌లో') - .2; c65 = AT(KC, '1765,', '1765లో') - .2
    crt = AT(KC, 'right', 'బెంగాల్,') - .2; cem = AT(KC, 'emperor', 'మొఘల్') - .2
    m = OMV(INDIA, zoomv(INDIA, 1.08), prog(t, s0, s1)); img = m.base.copy(); k = e_out(prog(t, s0, s0 + .4))
    rail_strip(img, 6 if t >= c65 else 5, k, 300, k_last=e_io(prog(t, c65, c65 + .8)) if t >= c65 else 1.0)
    plx, ply = m.P(*PL['PLASSEY']); bx, by = m.P(*PL['BUXAR'])
    kp = e_out(prog(t, cpl, cpl + .4)) * (1 - e_io(prog(t, c65 - .3, c65)))
    if kp > .01:
        pin(img, plx, ply, kp, AMBER, 14, pulse=t)
        plate_text(img, (90, 420, W - 90, 590), L('1757', '1757'), L("PLASSEY DIDN'T CONQUER INDIA", 'ప్లాసీ భారతదేశాన్ని జయించలేదు'), kp, 50 if not TE else 46, owner='not india')
    kb = e_out(prog(t, cbx, cbx + .4)); pin(img, bx, by, kb, CREAM, 16)
    tag(img, L('BUXAR · 1764 · THE COMPANY WINS AGAIN', 'బక్సర్ · 1764 · కంపెనీ మళ్లీ గెలిచింది'), bx, by + 70, 30, CREAM, kb * (1 - e_io(prog(t, crt - .4, crt))))
    kr = e_out(prog(t, crt, crt + .6))
    if kr > .01:
        hatch_region(img, m, BBO, kr, t)
        plate_text(img, (90, 420, W - 90, 640), L('1765 · BENGAL · BIHAR · ORISSA', '1765 · బెంగాల్ · బీహార్ · ఒరిస్సా'), L('DIWANI · REVENUE-COLLECTION RIGHTS', 'దివానీ · ఆదాయం వసూలు చేసే హక్కు'), kr, 50 if not TE else 46, owner='diwani',
                   sub=L('NOT A CONQUEST · AREA APPROXIMATE', 'జయించడం కాదు · ప్రాంతం సుమారుగా'))
    ke = e_out(prog(t, cem, cem + .4))
    if ke > .01:
        panel_nat(img, 'DIWANI', (40, 940, 40 + 640, 940 + 452), prog(t, cem, s1), (.45, .5), (.55, .5), sc=640 / 1999 * 1.0, radius=10, a=ke, border=GOLD_A)
        tag(img, L('BENJAMIN WEST · PAINTED c. 1818', 'బెంజమిన్ వెస్ట్ · c. 1818 నాటి చిత్రం'), 360, 890, 28, CREAM, ke)
        tag(img, L('A LATER, IDEALISED IMAGE', 'తర్వాతి కాలపు ఊహాచిత్రం'), 360, 1360, 26, AMBER, ke)
    return img

# ---- 15 · tease: Season 2 (the season line runs on, into the Company's arms)
@functools.lru_cache(1)
def ARMS():
    im = Image.fromarray(FL.img('PD12')).convert('RGB'); im.thumbnail((620, 620), Image.LANCZOS); return im
def s_tease(t, s0, s1):
    img = radial_bg(W, H, (40, 34, 24), (9, 9, 9), cy=.5, reach=.9).copy(); k = e_out(prog(t, s0, s0 + .4))
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for yy_ in range(0, H, 36): d.line((W / 2, yy_ + (t * 60) % 36, W / 2, yy_ + (t * 60) % 36 + 18), fill=AMBER + (int(110 * k),), width=5)
    img.paste(lay, (0, 0), lay)
    a = ARMS(); m_ = Image.new('L', a.size, 0); ImageDraw.Draw(m_).rounded_rectangle((0, 0, a.width - 1, a.height - 1), 18, fill=int(255 * k))
    x0, y0 = int(W / 2 - a.width / 2), int(620 - 30 * e_io(prog(t, s0, s1))); shadow(img, (x0, y0, x0 + a.width, y0 + a.height), k); img.paste(a, (x0, y0), m_)
    tag(img, L('EAST INDIA COMPANY ARMS · PD', 'ఈస్ట్ ఇండియా కంపెనీ చిహ్నం · పబ్లిక్ డొమైన్'), W / 2, y0 + a.height + 40, 26, PARCH, k)
    plate_text(img, (90, 290, W - 90, 520), L('SEASON 2', 'సీజన్ 2'), L('WHERE THIS STORY GOES NEXT', 'ఈ కథ ఇక్కడి నుంచే'), k, 56 if not TE else 52, owner='tease')
    kf = e_out(prog(t, AT(KC, 'film', 'సినిమా') - .3, AT(KC, 'film', 'సినిమా') + .1)); chip(img, L('THE FULL FILM IS LINKED', 'పూర్తి సినిమా లింక్‌లో'), W / 2, 1340, 40, AMBER, INK, a=kf, scale=max(kf, .01))
    return img

FUNCS = {'hook': s_hook, 'perm': s_perm, 'war': s_war, 'farman': s_farman, 'wars': s_wars, 'lesson': s_lesson, 'siraj': s_siraj,
         'plassey': s_plassey, 'buxar': s_buxar, 'payoff': s_payoff, 'question': s_question, 'tease': s_tease}
def render(t):
    LY.reset(); name, s0, s1 = scene_at(t)
    if name.startswith('cartoon'): img = cartoon(t, s0, [('CHELLI', 'Q1')])
    elif name == 'plassey' and S('Q2') - .15 <= t < E('Q2') + .2: img = cartoon(t, S('Q2') - .15, [('CHELLI', 'Q2')]); name = 'cartoon2'
    elif name == 'slide': img = s_slide(t, s0, s1)
    else: img = FUNCS[name](t, s0, s1)
    overlays(img, t, name); captions(img, t, name); return img
