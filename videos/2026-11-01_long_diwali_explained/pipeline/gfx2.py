"""Explainer graphics: chapters 4-6, ending, series slide."""
from base import *
from gfx1 import moon, sun, cal_page, title_label, qcard, QCARDS, ledger, person, sparkle
import room as RM

VIRAL = ASSET + 'images/09-india-diwali-rainbow-composite.jpg'
NASA = ASSET + 'images/10-nasa-suomi-npp-india-2012-11-12.jpg'
NASA_CR = 'NASA Earth Observatory · Jesse Allen & Robert Simmon · VIIRS/Suomi NPP · Nov 12, 2012'


def fill_img(c, path, t, t0, dim=1.0):
    sf = blur_fill(path); c.set_source_surface(sf, (W - sf.get_width()) / 2, (H - sf.get_height()) / 2); c.paint()


def g_viral(c, t, t0, tstamp=None, legend_t=None):
    fill_img(c, VIRAL, t, t0)
    x = W / 2 if legend_t is None else lerp(W / 2, 640, e_io(prog(t, legend_t, legend_t + 0.6)))
    photo_panel(c, VIRAL, x, 520, 860, t, t0, zoom=(1.0, 1.06), dur=8, credit=L('Colour composite · NOAA / Chris Elvidge', 'Colour composite · NOAA / Chris Elvidge'))
    if tstamp: stamp(c, L('NOT DIWALI', 'దీపావళి కాదు'), x, 520, t, tstamp, 120, rot=-10)
    if legend_t is not None and t >= legend_t + 0.3:
        rows = [((1, 1, 1), L('lights seen before 1992', '1992 కి ముందు లైట్లు')), ((0.35, 0.55, 1.0), L('new in 1992', '1992 లో కొత్తవి')),
                ((0.35, 0.85, 0.40), L('new in 1998', '1998 లో కొత్తవి')), ((1.0, 0.30, 0.25), L('new in 2003', '2003 లో కొత్తవి'))]
        glass(c, 1150, 230, 640, 480, 30, prog(t, legend_t + 0.3, legend_t + 0.6))
        txt(c, L('MADE IN 2003 · CHRIS ELVIDGE', '2003 · CHRIS ELVIDGE'), 1470, 290, 30, grad=True, a=prog(t, legend_t + 0.3, legend_t + 0.6), maxw=580)
        for i, (col, lab) in enumerate(rows):
            tt = legend_t + 0.6 + i * 0.3; a = prog(t, tt, tt + 0.25)
            c.set_source_rgba(*col, a); c.arc(1220, 380 + i * 85, 20, 0, 2 * math.pi); c.fill()
            txt(c, lab, 1265, 380 + i * 85, 32, CREAM, a, anchor='l')
        pill(c, L('= HOW CITIES GREW', '= నగరాలు ఎలా పెరిగాయో'), 1470, 790, 30, a=prog(t, legend_t + 2.0, legend_t + 2.3), outline=True)


def nasa_panel(c, t, t0):
    photo_panel(c, NASA, 1440, 470, 760, t, t0, rot=2, caption=L('REAL · NASA · DIWALI 2012', 'నిజమైనది · NASA · దీపావళి 2012'), zoom=(1.12, 1.2), dur=8)
    if t >= t0: txt(c, NASA_CR, 1440, 900, 15, CREAM, 0.75 * prog(t, t0, t0 + 0.4), kind='mono')


def g_earthk(c, t, t0):
    board_bg(c)
    photo_panel(c, NASA, 1500, 470, 560, t, t0, rot=3, zoom=(1.2, 1.25), dur=8)
    draw_clip(c, 'earth_h', 620, 300, 760, t, t0 + 0.1, rot=-2, src='EARTHSKY')
    draw_clip(c, 'earth_k', 700, 650, 1000, t, t0 + 0.4, rot=1, hl_t0=t0 + 1.0, hl_dur=1.6)


def g_compare(c, t, t0):
    board_bg(c)
    photo_panel(c, VIRAL, 520, 500, 680, t, t0, rot=-2)
    photo_panel(c, NASA, 1400, 500, 620, t, t0 + 0.3, rot=2, zoom=(1.15, 1.15))
    stamp(c, L('RAINBOW = COMPOSITE', 'రంగులు = composite'), 520, 900, t, t0 + 1.2, 44, rot=-4, col=CREAM)
    stamp(c, L('ORANGE + WHITE = REAL', 'Orange + తెలుపు = నిజం'), 1400, 900, t, t0 + 2.0, 44, rot=3)
    txt(c, NASA_CR, 1400, 830, 13, CREAM, 0.7 * prog(t, t0 + 0.3, t0 + 0.6), kind='mono')


# ---------- chapter 5 ----------
def g_ticker(c, t, t0, tbell):
    c.set_source_rgb(0.03, 0.03, 0.05); c.paint()
    rng = np.random.default_rng(2)
    for i in range(60):
        c.set_source_rgba(1, 1, 1, 0.4 * (0.5 + 0.5 * math.sin(t * 2 + i))); c.arc(rng.uniform(0, W), rng.uniform(0, 300), 1.5, 0, 2 * math.pi); c.fill()
    on = e_out(prog(t, tbell, tbell + 0.5))
    bx, by, bw, bh = 220, 330, 1480, 420
    c.set_source_rgb(0.08, 0.08, 0.10); rrect(c, bx, by, bw, bh, 20); c.fill()
    names = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ITC', 'SBIN', 'LT', 'BHARTIARTL', 'HINDUNILVR', 'ICICIBANK']
    for row in range(3):
        y = by + 80 + row * 130; off = (t * (60 + row * 15)) % 600
        c.save(); c.rectangle(bx + 20, y - 50, bw - 40, 100); c.clip()
        for k in range(10):
            x = bx + bw - off - 0 + k * 300 - 600 if row % 2 else bx + 40 + k * 300 - off
            nm = names[(k + row * 3) % len(names)]; up = (k + row) % 3 != 0
            col = (0.35, 0.95, 0.5) if up else (1.0, 0.45, 0.35)
            txt(c, nm, x, y - 14, 28, (1, 0.8, 0.4), 0.15 + 0.85 * on, anchor='l', kind='monob')
            txt(c, ('▲ ' if False else '+' if up else '−') + f'{0.4 + (k % 5) * 0.37:.2f}%', x, y + 24, 24, col, 0.15 + 0.85 * on, anchor='l', kind='monob')
        c.restore()
    g = cairo.RadialGradient(W / 2, by + bh / 2, 0, W / 2, by + bh / 2, 900); g.add_color_stop_rgba(0, *AMBER, 0.18 * on); g.add_color_stop_rgba(1, *AMBER, 0)
    c.set_source(g); c.paint()
    txt(c, L('MUHURAT TRADING', 'ముహూర్త trading'), W / 2, 200, 80, grad=True, a=prog(t, tbell, tbell + 0.4), stroke=5)
    pill(c, L('ABOUT 1 HOUR', 'దాదాపు 1 గంట'), W / 2, 850, 32, a=prog(t, t0 + 0.6, t0 + 0.9), outline=True)


def g_datecard(c, t, t0):
    board_bg(c)
    cal_page(c, 470, 400, 330, L('SUNDAY', 'ఆదివారం'), '8', L('NOV · 2026', 'నవం · 2026'), t, t0, rot=-3, hl=True)
    u = e_out(prog(t, t0 + 0.6, t0 + 1.0))
    glass(c, 860, 260, 860, 260, 30, u)
    txt(c, '2:20 – 3:30 PM', 1290, 360, 84, grad=True, a=u, stroke=4)
    txt(c, L('IST · NORMAL MARKET', 'IST · సాధారణ market'), 1290, 450, 26, CREAM, u, kind='monob')
    draw_clip(c, 'zer', W / 2, 820, 1500, t, t0 + 1.0, rot=-0.8, hl_t0=t0 + 1.4, hl_dur=1.0, src='ZERODHA BULLETIN (NSE/BSE CIRCULARS) · OCT 27, 2026')


def g_trade(c, t, t0, tclick):
    board_bg(c)
    u = e_out(prog(t, t0, t0 + 0.4))
    c.save(); c.translate(W / 2, 540 + (1 - u) * 80)
    c.set_source_rgb(0.06, 0.06, 0.07); rrect(c, -260, -420, 520, 840, 60); c.fill()
    c.set_source_rgb(0.12, 0.12, 0.14); rrect(c, -240, -400, 480, 800, 44); c.fill()
    txt(c, L('FIRST TRADE OF THE YEAR', 'ఏడాది మొదటి trade'), 0, -320, 24, CREAM, kind='monob')
    txt(c, 'SHARE · 1 qty', 0, -220, 40, CREAM)
    # mini chart
    c.set_source_rgba(0.35, 0.95, 0.5, 0.9); c.set_line_width(5); c.move_to(-180, -40)
    for i in range(1, 13): c.line_to(-180 + i * 30, -40 - 12 * math.sin(i * 0.9) - i * 6)
    c.stroke()
    clicked = t >= tclick
    pr = 1 - abs(prog(t, tclick - 0.08, tclick + 0.12) * 2 - 1) if tclick - 0.08 < t < tclick + 0.12 else 0
    c.save(); c.translate(0, 180); c.scale(1 - 0.06 * pr, 1 - 0.06 * pr)
    c.set_source_rgb(*((0.25, 0.75, 0.45) if not clicked else (0.2, 0.2, 0.22))); rrect(c, -180, -50, 360, 100, 50); c.fill()
    txt(c, 'BUY' if not clicked else 'ORDER PLACED', 0, 0, 34, CREAM)
    c.restore()
    c.restore()
    if clicked: pill(c, L('FOR GOOD LUCK', 'శుభం కోసం'), 1450, 540, 40, sc=e_back(prog(t, tclick + 0.2, tclick + 0.5)))
    # cursor
    if t < tclick + 0.8:
        k = e_io(prog(t, t0 + 0.4, tclick - 0.05)); px, py = lerp(1500, W / 2 + 40, k), lerp(950, 540 + 190, k)
        c.save(); c.translate(px, py); c.move_to(0, 0); c.line_to(0, 44); c.line_to(12, 33); c.line_to(22, 54); c.line_to(30, 50); c.line_to(20, 30); c.line_to(36, 30); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(0, 0, 0); c.set_line_width(2.5); c.stroke(); c.restore()


def g_history(c, t, t0, t57, t92):
    board_bg(c)
    x0, x1, y = 300, 1620, 380
    c.set_source_rgba(1, 1, 1, 0.15); c.set_line_width(6); c.move_to(x0, y); c.line_to(x1, y); c.stroke()
    for yr, tt, lab in ((1957, t57, 'BSE'), (1992, t92, 'NSE')):
        x = x0 + (x1 - x0) * (yr - 1950) / 80
        if t >= tt:
            glowdot(c, x, y, 14); big_num(c, str(yr), x, y - 100, 90, t, tt)
            pill(c, lab, x, y + 80, 32, sc=e_back(prog(t, tt + 0.1, tt + 0.4)))
    txt(c, '2026', x1, y - 60, 30, CREAM, 0.5, kind='monob')
    draw_clip(c, 'icici', W / 2, 800, 1600, t, t0 + 0.3, rot=-0.6, hl_t0=t57 - 0.2, hl_dur=max(0.8, t92 - t57 + 0.6), src='ICICI DIRECT · DIWALI MUHURAT TRADING')


# ---------- chapter 6 ----------
_LAND = None


def land_paths():
    global _LAND
    if _LAND is None:
        import json as _j
        from shapely.geometry import shape, box
        from shapely.ops import unary_union
        G = _j.load(open('/home/claude/why-channel-studio/pipeline/lib/countries.geojson'))
        bb = box(60, 5, 100, 40); geoms = []
        for f in G['features']:
            g = shape(f['geometry'])
            if g.intersects(bb): geoms.append(g.intersection(bb.buffer(2)))
        u = unary_union(geoms).buffer(0.02).buffer(-0.02)
        polys = list(u.geoms) if hasattr(u, 'geoms') else [u]
        _LAND = [list(p.exterior.coords) for p in polys if p.area > 0.3]
    return _LAND


def proj(lon, lat, clon=79.0, clat=23.5, z=48.0):
    return W / 2 + (lon - clon) * z, H / 2 - (lat - clat) * z * 1.08


def g_map(c, t, t0):
    c.set_source_rgb(0.07, 0.15, 0.25); c.paint()
    zz = lerp(38, 46, e_io(prog(t, t0, t0 + 8)))
    for poly in land_paths():
        c.move_to(*proj(*poly[0], z=zz))
        for p in poly[1:]: c.line_to(*proj(*p, z=zz))
        c.close_path()
    c.set_source_rgb(0.34, 0.31, 0.26); c.fill_preserve(); c.set_source_rgba(1, 1, 1, 0.25); c.set_line_width(2); c.stroke()
    dl = proj(77.21, 28.61, z=zz)
    fires = [(74.9, 30.9), (75.8, 30.3), (74.3, 31.3), (76.4, 29.6), (75.3, 30.0), (76.0, 29.2), (74.6, 30.3), (76.8, 30.4)]
    u = prog(t, t0 + 0.5, t0 + 1.4)
    for i, (lo, la) in enumerate(fires):
        x, y = proj(lo, la, z=zz); f = 0.6 + 0.4 * math.sin(t * 8 + i)
        g = cairo.RadialGradient(x, y, 0, x, y, 40); g.add_color_stop_rgba(0, 1, 0.5, 0.1, 0.9 * u * f); g.add_color_stop_rgba(1, 1, 0.4, 0.1, 0)
        c.set_source(g); c.arc(x, y, 40, 0, 2 * math.pi); c.fill()
    # smoke drifting to Delhi
    for i in range(26):
        ph = (t * 0.25 + i * 0.137) % 1; s0 = fires[i % len(fires)]; x0, y0 = proj(*s0, z=zz)
        x = lerp(x0, dl[0], ph) + 30 * math.sin(i + t); y = lerp(y0, dl[1], ph) + 20 * math.cos(i * 2 + t)
        c.set_source_rgba(0.70, 0.68, 0.64, 0.30 * u * math.sin(ph * math.pi)); c.arc(x, y, 30 + 30 * ph, 0, 2 * math.pi); c.fill()
    for (lo, la) in ((75.2, 31.6), (76.0, 30.6)):
        x0, y0 = proj(lo, la, z=zz); k = e_io(prog(t, t0 + 1.2, t0 + 2.2))
        c.set_source_rgba(*AMBER, 0.9); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(x0, y0); c.line_to(lerp(x0, dl[0] - 30, k), lerp(y0, dl[1] - 20, k)); c.stroke()
        if k > 0.05: arrow_head(c, lerp(x0, dl[0] - 30, k), lerp(y0, dl[1] - 20, k), math.atan2(dl[1] - y0, dl[0] - x0), 26)
    glowdot(c, *dl, 14); pill(c, 'DELHI' if LANG == 'en' else 'ఢిల్లీ', dl[0] + 120, dl[1] + 40, 30)
    pp = proj(75.5, 31.7, z=zz); pill(c, L('PUNJAB & HARYANA · CROP STUBBLE FIRES', 'Punjab & Haryana · పంట వ్యర్థాల మంటలు'), pp[0] - 330, pp[1] + 10, 26, a=prog(t, t0 + 0.6, t0 + 1.0), outline=True)
    txt(c, L('Map: land only, no borders', 'Map: భూభాగం మాత్రమే'), 60, H - 40, 15, CREAM, 0.5, anchor='l', kind='mono')


def skyline(c, y, col=(0.10, 0.10, 0.13), a=1.0, x0=0, x1=W):
    rng = np.random.default_rng(4); x = x0
    while x < x1:
        w = rng.uniform(60, 140); h = rng.uniform(80, 300)
        c.set_source_rgba(*col, a); c.rectangle(x, y - h, w - 6, h); c.fill()
        for k in range(int(h // 40)):
            if rng.uniform() < 0.5: c.set_source_rgba(1, 0.8, 0.45, 0.5 * a); c.rectangle(x + 12, y - h + 15 + k * 40, 12, 14); c.fill()
        x += w


def smoke(c, x, y, t, i, top, a=1.0):
    ph = (t * 0.3 + i * 0.173) % 1; yy = lerp(y, top, ph) + 10 * math.sin(t + i)
    xx = x + 60 * math.sin(i * 1.7 + ph * 3)
    c.set_source_rgba(0.62, 0.60, 0.56, 0.35 * a * (1 - abs(ph - 0.6))); c.arc(xx, yy, 36 + 50 * ph, 0, 2 * math.pi); c.fill()


def g_lid(c, t, t0):
    sky = cairo.LinearGradient(0, 0, 0, H); sky.add_color_stop_rgb(0, 0.32, 0.36, 0.42); sky.add_color_stop_rgb(1, 0.55, 0.52, 0.48)
    c.set_source(sky); c.paint()
    k = e_io(prog(t, t0 + 0.3, t0 + 1.6)); lid_y = lerp(-120, 330, k)
    for i in range(40): smoke(c, 100 + (i * 47) % 1720, 900, t, i, max(lid_y + 90, 380))
    skyline(c, 1000)
    c.set_source_rgb(0.12, 0.12, 0.14); c.rectangle(0, 990, W, 90); c.fill()
    c.set_source_rgba(0.55, 0.75, 1.0, 0.35); rrect(c, 80, lid_y - 70, W - 160, 140, 30); c.fill()
    c.set_source_rgba(0.75, 0.88, 1.0, 0.8); c.set_line_width(4); rrect(c, 80, lid_y - 70, W - 160, 140, 30); c.stroke()
    txt(c, L('COLD, STILL AIR = A LID', 'చల్లని, కదలని గాలి = మూత'), W / 2, lid_y, 44, CREAM, stroke=5)
    for x in (400, 960, 1520):
        c.set_source_rgba(0.75, 0.88, 1.0, 0.8 * k); c.set_line_width(6); c.move_to(x, lid_y + 80); c.line_to(x, lid_y + 140); c.stroke()
        arrow_head(c, x, lid_y + 150, math.pi / 2, 22, col=(0.75, 0.88, 1.0), a=k)


def g_mumdel(c, t, t0):
    c.set_source_rgb(0.06, 0.07, 0.09); c.paint()
    # left: Mumbai with sea
    c.save(); c.rectangle(0, 0, W / 2, H); c.clip()
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.45, 0.62, 0.80); g.add_color_stop_rgb(1, 0.70, 0.80, 0.88); c.set_source(g); c.paint()
    c.set_source_rgb(0.12, 0.35, 0.55); c.rectangle(0, 760, W / 2, 320); c.fill()
    for i in range(6):
        c.set_source_rgba(1, 1, 1, 0.3); c.set_line_width(3); y = 800 + i * 45; off = (t * 40 + i * 30) % 120
        for x in range(-120, W // 2, 120): c.move_to(x + off, y); c.curve_to(x + off + 30, y - 10, x + off + 60, y + 10, x + off + 90, y); c.stroke()
    skyline(c, 760, x0=480, x1=W / 2)
    for i in range(4):
        y = 420 + i * 80; ph = (t * 0.6 + i * 0.25) % 1; x = lerp(860, 120, ph)
        c.set_source_rgba(1, 1, 1, 0.9 * math.sin(ph * math.pi)); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(x + 160, y); c.line_to(x, y); c.stroke()
        arrow_head(c, x - 4, y, math.pi, 24, col=(1, 1, 1), a=math.sin(ph * math.pi))
    pill(c, 'MUMBAI' if LANG == 'en' else 'ముంబై', W / 4, 150, 36)
    pill(c, L('SEA BREEZE CARRIES AIR OUT', 'సముద్రపు గాలి బయటకు తీసుకెళ్తుంది'), W / 4, 240, 26, outline=True)
    c.restore()
    # right: Delhi still
    c.save(); c.rectangle(W / 2, 0, W / 2, H); c.clip()
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.42, 0.42, 0.42); g.add_color_stop_rgb(1, 0.62, 0.58, 0.52); c.set_source(g); c.paint()
    for i in range(24): smoke(c, W / 2 + 60 + (i * 43) % 860, 800, t, i, 420)
    skyline(c, 860, x0=W / 2, x1=W)
    c.set_source_rgb(0.14, 0.13, 0.12); c.rectangle(W / 2, 850, W / 2, 230); c.fill()
    pill(c, 'DELHI' if LANG == 'en' else 'ఢిల్లీ', W * 3 / 4, 150, 36)
    pill(c, L('FAR FROM THE SEA · WIND ALMOST STOPS', 'సముద్రానికి దూరం · గాలి దాదాపు ఆగుతుంది'), W * 3 / 4, 240, 26, outline=True)
    c.restore()
    c.set_source_rgb(*AMBER); c.rectangle(W / 2 - 3, 0, 6, H); c.fill()


def g_iit(c, t, t0, t12):
    board_bg(c)
    draw_clip(c, 'iit', W / 2, 250, 1560, t, t0, rot=-0.6, hl_t0=t0 + 0.6, hl_dur=1.8, src='SHIKSHA · IIT DELHI STUDY RELEASE')
    # graph
    gx, gy, gw, gh = 650, 520, 620, 290
    u = e_out(prog(t, t0 + 0.4, t0 + 0.8)); glass(c, gx - 30, gy - 40, gw + 60, gh + 110, 26, u)
    k = prog(t, t0 + 0.8, t12 + 1.5)
    c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgba(1.0, 0.55, 0.25, u); c.move_to(gx, gy + gh)
    for i in range(int(60 * k) + 1):
        x = i / 60; v = math.exp(-((x - 0.12) / 0.03) ** 2) * 0.95 if x < 0.12 else 0.95 * math.exp(-(x - 0.12) * 14)
        c.line_to(gx + x * gw, gy + gh - v * gh)
    c.stroke()
    c.set_source_rgba(0.75, 0.75, 0.78, u); c.move_to(gx, gy + gh * 0.55)
    for i in range(int(60 * k) + 1): c.line_to(gx + i / 60 * gw, gy + gh * (0.55 - 0.1 * math.sin(i / 60 * 3)))
    c.stroke()
    txt(c, L('crackers', 'బాణసంచా'), gx + 120, gy - 5, 22, (1.0, 0.6, 0.3), u, anchor='l', kind='monob')
    txt(c, L('crop fires + winter heating', 'పంట మంటలు + చలి వేడి'), gx + gw, gy + gh * 0.35, 22, CREAM, u * prog(t, t0 + 2, t0 + 2.4), anchor='r', kind='monob')
    if t >= t12: pill(c, L('~12 HOURS', '~12 గంటలు'), gx + gw * 0.2, gy + gh + 40, 26, sc=e_back(prog(t, t12, t12 + 0.3)))
    txt(c, L('illustrative', 'ఉదాహరణ మాత్రమే'), gx + gw, gy + gh + 50, 16, CREAM, 0.5 * u, anchor='r', kind='mono')


def g_sc(c, t, t0):
    board_bg(c)
    draw_clip(c, 'sc', W / 2, 470, 1300, t, t0, rot=-1)
    pill(c, L('SUPREME COURT HEARING · OCT 29, 2026', 'Supreme Court విచారణ · OCT 29, 2026'), W / 2, 870, 30, a=prog(t, t0 + 0.6, t0 + 0.9), outline=True)
    txt(c, 'DEVDISCOURSE / ANI', W / 2, 940, 20, CREAM, 0.7 * prog(t, t0 + 0.6, t0 + 0.9), kind='monob')
    if t > t0 + 1.0: marker_line(c, W / 2 - 560, 405, W / 2 + 160, 405, t, t0 + 1.0, 0.5, 6)


# ---------- ending ----------
DONE = [('Moon moves the date', 'చంద్రుడు తేదీ మారుస్తాడు'), ('Monsoon → we clean', 'వర్షాకాలం → శుభ్రం'), ('Bonus is the law', 'Bonus చట్టం'),
        ('That photo is fake', 'ఆ photo fake'), ('New financial year', 'కొత్త ఆర్థిక సంవత్సరం'), ("Delhi's air: a winter problem", 'Delhi గాలి: చలికాలం సమస్య')]


def g_board(c, t, t0, ts):
    board_bg(c, 0.1)
    for i, (lab, tt) in enumerate(zip(DONE, ts)):
        x = 380 + (i % 3) * 580; y = 330 + (i // 3) * 330
        u = e_back(prog(t, t0 + i * 0.06, t0 + i * 0.06 + 0.3))
        if u <= 0: continue
        flip = prog(t, tt, tt + 0.3); sx = abs(math.cos(flip * math.pi)); front = flip < 0.5
        c.save(); c.translate(x, y); c.scale(max(0.02, sx) * u, u)
        glass(c, -250, -110, 500, 220, 26)
        if front:
            txt(c, L(*QCARDS[i]), 0, 0, 34, CREAM, maxw=440)
        else:
            c.set_source(agrad(-40, -40, 40, 40)); c.arc(0, -40, 40, 0, 2 * math.pi); c.fill()
            c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(-16, -40); c.line_to(-4, -28); c.line_to(18, -54); c.stroke()
            txt(c, L(*lab), 0, 50, 32, CREAM, maxw=450)
        c.restore()


def g_locked(c, t, t0, ts):
    board_bg(c, 0.12)
    for k, i in enumerate((6, 7, 8)):
        tt = ts[k]; x = 400 + k * 560; y = 520
        u = e_back(prog(t, t0 + k * 0.1, t0 + k * 0.1 + 0.3))
        if u <= 0: continue
        sh = 8 * math.sin(t * 30) * (1 - prog(t, tt, tt + 0.6)) if t >= tt else 0
        c.save(); c.translate(x + sh, y); c.scale(u, u); glass(c, -240, -170, 480, 340, 30)
        act = t >= tt
        c.set_source_rgba(*(AMBER if act else CREAM), 0.9); c.set_line_width(10); c.arc(0, -60, 40, math.pi, 2 * math.pi); c.stroke(); rrect(c, -55, -60, 110, 85, 12); c.fill()
        txt(c, L(*QCARDS[i]), 0, 90, 36, CREAM if act else (0.6, 0.6, 0.6), maxw=430)
        c.restore()
    pill(c, L('NEXT DIWALI', 'వచ్చే దీపావళి'), W / 2, 880, 34, a=prog(t, ts[-1] + 0.6, ts[-1] + 1.0), outline=True)


def like_comment(c, t, t0, ttype):
    u = e_back(prog(t, t0, t0 + 0.35))
    if u > 0.01:
        c.save(); c.translate(1520, 330); c.scale(u, u)
        glass(c, -130, -110, 260, 220, 40, edge=False)
        k = prog(t, t0 + 0.5, t0 + 0.8); col = AMBER if k > 0.5 else CREAM
        c.save(); c.scale(1 + 0.2 * math.sin(k * math.pi), 1 + 0.2 * math.sin(k * math.pi)); c.set_source_rgb(*col)
        c.move_to(-50, 0); c.line_to(-50, 60); c.line_to(-20, 60); c.line_to(-20, 0); c.close_path(); c.fill()
        c.move_to(-10, 0); c.line_to(10, -60); c.curve_to(30, -60, 30, -30, 26, -10); c.line_to(60, -10); c.curve_to(72, -10, 72, 10, 62, 14)
        c.line_to(54, 56); c.curve_to(50, 62, 46, 64, 40, 64); c.line_to(-10, 64); c.close_path(); c.fill(); c.restore(); c.restore()
    if t >= ttype:
        v = e_back(prog(t, ttype, ttype + 0.3)); s = L('make it!', 'చేయండి!'); n = int(len(s) * prog(t, ttype + 0.3, ttype + 1.2))
        c.save(); c.translate(1520, 600); c.scale(v, v); glass(c, -230, -60, 460, 120, 30, edge=False)
        txt(c, s[:max(0, n)] + ('|' if int(t * 3) % 2 else ''), -190, 0, 40, CREAM, anchor='l'); c.restore()


SERIES = [('Your Diwali bonus is the law', 'Diwali bonus చట్టం'), ('The fake space photo', 'Fake space photo'), ('Why we deep-clean', 'ఎందుకు శుభ్రం చేస్తాం'),
          ('Market opens on Diwali', 'దీపావళికి market'), ('₹6 lakh crore in one Diwali', 'ఒక్క దీపావళికి ₹6 లక్షల కోట్లు'), ("Delhi's air after Diwali", 'దీపావళి తర్వాత Delhi గాలి')]
DAYS = [('MON', 'సోమ'), ('TUE', 'మంగళ'), ('WED', 'బుధ'), ('THU', 'గురు'), ('FRI', 'శుక్ర'), ('SAT', 'శని')]
ICONS = ['₹', '◐', '✦', '▲', '₹', '≋']


def g_series(c, t, t0, sub_t=None):
    board_bg(c, 0.12)
    txt(c, L('DIWALI WEEK', 'దీపావళి వారం'), W / 2, 95, 56, grad=True, a=prog(t, t0, t0 + 0.3))
    # full video card
    u = e_back(prog(t, t0 + 0.1, t0 + 0.4)); c.save(); c.translate(360, 410); c.scale(u, u)
    glass(c, -260, -200, 520, 400, 30)
    RM.diya(c, 0, -10, 1.3, t); txt(c, L('FULL VIDEO', 'FULL VIDEO'), 0, 110, 34, grad=True)
    pill(c, L("YOU'RE HERE", 'మీరు ఇక్కడ'), 0, 165, 22, outline=True); c.restore()
    for i, ((en, te), day) in enumerate(zip(SERIES, DAYS)):
        x = 820 + (i % 3) * 390; y = 290 + (i // 3) * 250; tt = t0 + 0.3 + i * 0.12
        v = e_back(prog(t, tt, tt + 0.3))
        if v <= 0: continue
        c.save(); c.translate(x, y); c.scale(v, v)
        glass(c, -175, -115, 350, 230, 24, edge=(i == 0))
        txt(c, f'{L(*day)} · {i + 1}/6', -150, -80, 22, AMBER, anchor='l', kind='monob')
        txt(c, L(en, te), 0, 0, 30, CREAM, maxw=320)
        if i == 0: pill(c, L('TOMORROW', 'రేపు'), 0, 75, 22)
        c.restore()
    if sub_t is not None:
        import importlib, sys as _s
        _s.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2'); import cta_card as CT
        c.save(); c.translate((W - 1080) / 2, 0); CT.draw(c, t, sub_t - 1.05, 'yt', LANG, y=790); c.restore()


def end_card(c, t, t0):
    board_bg(c, 0.14)
    u = e_back(prog(t, t0, t0 + 0.4))
    c.save(); c.translate(W / 2 - 420, 430); c.scale(u, u); txt(c, 'WHY?', 0, 0, 170, grad=True, stroke=6); c.restore()
    txt(c, L('GOT A WHY? COMMENT IT', 'మీ WHY? comment చేయండి'), W / 2 - 420, 600, 40, CREAM, prog(t, t0 + 0.3, t0 + 0.6))
