
# ---------------- anchors ----------------
A = {
    'trade1': AT('1', 'trade', 'వ్యాపారం'), 'where': AT('1', 'Where', 'ఎక్కడికి'),
    'notgold': AT('3', 'gold', 'కాదు'), 'groc': AT('3', 'Groceries', 'కిరాణా'),
    'gold4': AT('4', 'Gold', 'బంగారం'), 'elec': AT('4', 'Electronics', 'Electronics'),
    'appl': AT('5', 'appliances', 'appliances'),
    'decor': AT('6', 'décor', 'అలంకరణ'), 'sweets': AT('6', 'sweets', 'స్వీట్లకి'),
    'services': AT('7', 'Services', 'services'), 'k80': AT('7', '80,000', '80,000'),
    'lakshmi': AT('8', 'Lakshmi', 'లక్ష్మి'), 'busiest': AT('8', 'busiest', 'busy'),
    'p85': AT('9', '85', '85'),
    'j50': AT('10', '50', '50'),
    'small': AT('11', 'small', 'చిన్న'),
    'tomorrow': S('12'), 'loop': S('L'),
}
A['end'] = DUR
"""HELPERS"""
# ---------------- 5/6 drawings ----------------
NOTE = (540, 948)
GREEN = (0.30, 0.78, 0.45)
def note100(c, x, y, s, a=1.0, rot=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_source_rgba(0, 0, 0, 0.35 * a); rrect(c, -78, -34, 160, 72, 8); c.fill()
    c.set_source_rgba(0.72, 0.66, 0.86, a); rrect(c, -80, -36, 160, 72, 8); c.fill()
    c.set_source_rgba(0.55, 0.48, 0.72, a); c.set_line_width(3); rrect(c, -72, -28, 144, 56, 6); c.stroke()
    c.set_source_rgba(0.88, 0.84, 0.95, a); c.arc(30, 0, 20, 0, 2 * math.pi); c.fill()
    font(c, 'head', 26); c.set_source_rgba(0.30, 0.22, 0.45, a); c.move_to(-66, 10); c.show_text('₹100')
    c.restore()
def coin(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.95, 0.75, 0.25, a); c.arc(0, 0, 16, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.78, 0.56, 0.15, a); c.set_line_width(3); c.arc(0, 0, 11, 0, 2 * math.pi); c.stroke(); c.restore()
def market(c, t, a=1.0, note=True):
    c.save(); c.push_group()
    c.set_source_rgb(0.10, 0.09, 0.16); c.rectangle(60, 260, 960, 880); c.fill()
    for k in range(2):                                                     # string lights
        for i in range(20):
            x = 80 + i * 49; y = 300 + k * 60 + 26 * math.sin(i / 19 * math.pi)
            fl = 0.7 + 0.3 * math.sin(t * 3 + i * 1.7 + k)
            col = (1, 0.80, 0.35) if (i + k) % 3 else (1, 0.45, 0.35)
            g = cairo.RadialGradient(x, y, 0, x, y, 18); g.add_color_stop_rgba(0, *col, 0.9 * fl); g.add_color_stop_rgba(1, *col, 0); c.set_source(g); c.arc(x, y, 18, 0, 2 * math.pi); c.fill()
    for sx, col in ((120, (0.55, 0.20, 0.30)), (840, (0.20, 0.35, 0.55))):  # side stalls
        c.set_source_rgb(*col); c.rectangle(sx, 560, 120, 420); c.fill()
        for j in range(4): c.set_source_rgb(0.95, 0.85, 0.55) if j % 2 else c.set_source_rgb(*col); c.rectangle(sx - 10 + j * 35, 520, 35, 50); c.fill()
    c.set_source_rgb(0.32, 0.20, 0.14); c.rectangle(290, 500, 500, 460); c.fill()     # kirana shop
    for j in range(8):                                                     # awning
        c.set_source_rgb(0.90, 0.30, 0.20) if j % 2 == 0 else c.set_source_rgb(0.96, 0.92, 0.85)
        c.move_to(270 + j * 67.5, 440); c.line_to(270 + (j + 1) * 67.5, 440); c.line_to(270 + (j + 1) * 67.5, 510); c.curve_to(270 + (j + 0.5) * 67.5, 540, 270 + (j + 0.5) * 67.5, 540, 270 + j * 67.5, 510); c.close_path(); c.fill()
    font(c, 'head', 34); c.set_source_rgb(*AMBER); e = c.text_extents('KIRANA'); c.move_to(540 - e.width / 2 - e.x_bearing, 480); c.show_text('KIRANA')
    for r in range(3):                                                     # shelves with jars & packs
        y = 600 + r * 95; c.set_source_rgb(0.50, 0.34, 0.22); c.rectangle(310, y + 50, 460, 10); c.fill()
        for i in range(7):
            col = [(0.95, 0.75, 0.25), (0.35, 0.65, 0.40), (0.90, 0.35, 0.25), (0.40, 0.55, 0.85), (0.95, 0.90, 0.80), (0.80, 0.50, 0.25), (0.65, 0.40, 0.70)][(i + r) % 7]
            c.set_source_rgb(*col); rrect(c, 325 + i * 64, y, 44, 50, 6); c.fill()
    c.set_source_rgb(0.62, 0.42, 0.26); c.rectangle(250, 960, 580, 140); c.fill()     # counter
    c.set_source_rgb(0.75, 0.55, 0.35); c.rectangle(240, 950, 600, 18); c.fill()
    for i, col in enumerate(((0.95, 0.85, 0.6), (0.85, 0.75, 0.55))):      # sacks
        c.set_source_rgb(*col); c.move_to(300 + i * 80, 1100); c.curve_to(290 + i * 80, 1010, 370 + i * 80, 1010, 360 + i * 80, 1100); c.close_path(); c.fill()
    if note: note100(c, *NOTE, 1.0, rot=-0.06)
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
JARS = [  # key, label, amount, cx, cy, w, h
    ('groc', 'GROCERIES & FMCG', 12, 200, 560, 270, 220), ('gold', 'GOLD, SILVER & JEWELLERY', 10, 540, 560, 270, 220), ('elec', 'ELECTRONICS', 8, 880, 560, 270, 220),
    ('appl', 'APPLIANCES', 7, 200, 830, 270, 190), ('cloth', 'CLOTHES', 7, 540, 830, 270, 190), ('gift', 'GIFTS', 7, 880, 830, 270, 190),
    ('decor', 'HOME DÉCOR', 5, 200, 1070, 270, 170), ('furn', 'FURNITURE', 5, 540, 1070, 270, 170), ('sweet', 'SWEETS', 5, 880, 1070, 270, 170),
    ('else', 'EVERYTHING ELSE', 34, 540, 1300, 900, 110)]
def jar_t0(k):
    return {'groc': A['groc'], 'gold': A['gold4'], 'elec': A['elec'], 'appl': A['appl'], 'cloth': A['appl'], 'gift': A['appl'],
            'decor': A['decor'], 'furn': A['decor'], 'sweet': A['decor'], 'else': A['sweets'] + 0.4}[k]
def jars(c, t, a=1.0, only=None):
    tot = 0.0
    for k, lab, amt, cx, cy, w, h in JARS:
        if only and k not in only: continue
        t0 = jar_t0(k); f = e_out(prog(t, t0, t0 + 0.6)); tot += amt * f
        if k == 'else' and t < A['decor']: continue
        x0, y0 = cx - w / 2, cy - h / 2
        wob = 0.0
        if k == 'gold' and S('3') + 0.1 < t < A['groc']: wob = 0.06 * math.sin((t - S('3')) * 18)
        dim = 0.45 if (k == 'gold' and A['groc'] <= t < A['gold4']) else 1.0
        c.save(); c.translate(cx, cy); c.rotate(wob); c.translate(-cx, -cy)
        glass_dark(c, x0, y0, w, h, 20, a * dim)
        c.set_source_rgba(1, 1, 1, 0.25 * a * dim); c.set_line_width(3); rrect(c, x0, y0, w, h, 20); c.stroke()
        if f > 0:
            fh = (h - 112) * f * (min(1.0, amt / 12) if k != 'else' else 1.0) if k != 'else' else (h - 60) * f
            c.set_source_rgba(*(AMBER if k == 'groc' else (0.95, 0.75, 0.25)), 0.85 * a); rrect(c, x0 + 10, y0 + h - 10 - fh, w - 20, fh, 12); c.fill()
            if f < 1:
                for q in range(5): coin(c, cx - 60 + q * 30, y0 - 20 + ((t - t0) * 900 + q * 37) % (h - 20), 0.9, a=a)
            if k == 'else': head(c, f'₹{amt}', cx + 330, y0 + 28, 34, CREAM, a=a * prog(f, 0.3, 0.8), shadow=False)
            else: head(c, f'₹{amt}', cx, y0 + 70, 46, AMBER if k == 'groc' else CREAM, a=a * prog(f, 0.3, 0.8), shadow=False)
        mono(c, lab, cx, y0 + 26, 17 if k != 'else' else 20, CREAM, a=a * dim * 0.9, kind='monob')
        c.restore()
    return tot
def services_icons(c, t, t0, a=1.0):
    items = [('bike', 820, 560), ('cab', 820, 760), ('tent', 820, 950)]
    for i, (kind, x, y) in enumerate(items):
        u = e_back(prog(t, t0 + 0.2 * i, t0 + 0.2 * i + 0.3))
        if u <= 0: continue
        c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u))
        glass_dark(c, -150, -80, 300, 160, 30, a)
        if kind == 'bike':
            c.set_source_rgba(*CREAM, a); c.set_line_width(8)
            for wx in (-55, 55): c.new_path(); c.arc(wx, 30, 28, 0, 2 * math.pi); c.stroke()
            c.set_source_rgba(*AMBER, a); rrect(c, -50, -30, 90, 40, 10); c.fill(); rrect(c, 20, -60, 50, 44, 8); c.fill()
        elif kind == 'cab':
            c.set_source_rgba(0.98, 0.80, 0.20, a); rrect(c, -95, -20, 190, 55, 14); c.fill(); rrect(c, -55, -55, 110, 45, 12); c.fill()
            c.set_source_rgba(0.1, 0.1, 0.12, a)
            for wx in (-55, 55): c.new_path(); c.arc(wx, 38, 18, 0, 2 * math.pi); c.fill()
        else:
            for j in range(4):
                c.set_source_rgba(*((0.90, 0.30, 0.20) if j % 2 == 0 else CREAM), a)
                c.move_to(-90 + j * 45, 50); c.line_to(-90 + (j + 1) * 45, 50); c.line_to(0, -55); c.close_path(); c.fill()
        c.restore()
def aunty(c, x, y, s, t, a=1.0):
    person(c, x, y, s, (0.82, 0.20, 0.42), t=t, a=a)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.95, 0.75, 0.25, a); c.move_to(-72, -280); c.line_to(-40, -290); c.line_to(72, -120); c.line_to(40, -110); c.close_path(); c.fill()   # saree pallu
    c.set_source_rgba(*HAIR, a); c.arc(0, -410, 26, 0, 2 * math.pi); c.fill()                                                                   # bun
    c.set_source_rgba(0.85, 0.10, 0.10, a); c.arc(0, -372, 6, 0, 2 * math.pi); c.fill()                                                         # bindi
    c.restore()

def sc_hook(c, t, frozen=False):
    tt = 0.0 if frozen else t
    market(c, tt)
    mono(c, 'FESTIVE TRADE FORECAST · CAIT', W / 2, 1185, 28, CREAM, kind='monob')
    head(c, '₹7 LAKH CRORE', W / 2, 1265, 88, AMBER)
    if not frozen:
        draw_clip(c, 'bt', W / 2, 720, 780, t, A['trade1'] - 0.2, rot=-0.8, hl_t0=A['trade1'] + 0.1, hl_dur=0.9, t1=A['where'] - 0.35)
        if t < A['where'] - 0.1: source_tag(c, 'BUSINESS TODAY · 14 OCT 2026', 150, 900, a=prog(t, A['trade1'], A['trade1'] + 0.3) * (1 - prog(t, A['where'] - 0.4, A['where'] - 0.1)))
        if t >= A['where'] - 0.1: head(c, 'WHERE DOES IT GO?', W / 2, 1348, 60, CREAM, a=prog(t, A['where'] - 0.1, A['where'] + 0.15))

def heading(c, a=1.0):
    pill(c, '₹100 OF GOODS SALES · CAIT ESTIMATES', W / 2, 215, 22, CREAM, a=a)

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 follow 100 rupees
    elif t < S('3') - 0.05:
        heading(c, a=prog(t, S('2') + 0.2, S('2') + 0.5))
        k = e_io(prog(t, S('2'), S('2') + 1.0))
        x = NOTE[0]; y = NOTE[1] + (640 - NOTE[1]) * k; sc_ = 1.0 + 1.6 * k
        burst = prog(t, S('2') + 1.3, S('2') + 2.0)
        note100(c, x, y, sc_, a=1 - burst, rot=-0.06 * (1 - k))
        if burst > 0:
            rng = np.random.default_rng(3)
            for i in range(40):
                an = rng.uniform(0, 2 * math.pi); r = 40 + 380 * e_out(burst) * rng.uniform(0.4, 1)
                coin(c, 540 + r * math.cos(an), 640 + r * math.sin(an) * 0.8, 1.0, a=1 - prog(burst, 0.7, 1.0))
        if t >= S('2') + 1.7: jars(c, t, a=prog(t, S('2') + 1.7, S('2') + 2.2))
    # 3-6 the jars
    elif t < S('7') - 0.05:
        heading(c)
        tot = jars(c, t)
        if S('3') + 0.1 < t < A['groc']:
            mono(c, 'BIGGEST SLICE?', 540, 410, 24, AMBER, kind='monob')
        if A['groc'] + 0.5 <= t < S('4') - 0.1:
            draw_clip(c, 'caitcat', W / 2, 1230, 820, t, A['groc'] + 0.5, rot=0.7, hl_t0=A['groc'] + 0.8, hl_dur=0.8)
        pill(c, f'₹{int(round(tot))} / 100', W / 2, 300, 26, AMBER if tot > 99.5 else CREAM)
    # 7 services (part of the ₹7 lakh crore)
    elif t < S('8') - 0.05:
        k = e_io(prog(t, S('7') - 0.05, S('7') + 0.5))
        c.save(); c.translate(80 * k, 260 * k); c.scale(1 - 0.45 * k, 1 - 0.45 * k)
        c.push_group(); jars(c, t); c.pop_group_to_source(); c.paint_with_alpha(1 - 0.65 * k); c.restore()
        mono(c, 'GOODS', 330, 470, 24, CREAM, a=0.7 * k, kind='monob')
        services_icons(c, t, A['services'] - 0.2)
        if t >= A['k80'] - 0.2:
            pill(c, 'SERVICES · ≈ ₹80,000 CR+ · 2026 FORECAST', W / 2, 1150, 28, AMBER, s=e_back(prog(t, A['k80'] - 0.2, A['k80'] + 0.1)))
        if t >= A['services']:
            mono(c, 'SERVICES INCLUDED IN ₹7 LAKH CR FORECAST', W / 2, 1230, 22, CREAM, a=prog(t, A['services'], A['services'] + 0.3), kind='monob')
    # 8 Lakshmi aunty (grocery coins flow to her counter)
    elif t < S('9') - 0.05:
        market(c, t, note=False)
        aunty(c, 540, 960, 0.95, t, a=prog(t, S('8'), S('8') + 0.3))
        c.set_source_rgb(0.62, 0.42, 0.26); c.rectangle(250, 960, 580, 140); c.fill(); c.set_source_rgb(0.75, 0.55, 0.35); c.rectangle(240, 950, 600, 18); c.fill()
        for i in range(3): person(c, 920, 1180, 0.45 + 0.02 * i, [(0.3, 0.5, 0.8), (0.4, 0.7, 0.4), (0.8, 0.6, 0.3)][i], t=t + i)
        glass_dark(c, 80, 300, 220, 150, 20); c.set_source_rgba(*AMBER, 0.85); rrect(c, 95, 360, 190, 76, 12); c.fill()
        mono(c, 'GROCERIES ₹12', 190, 330, 18, CREAM, kind='monob')
        k = prog(t, S('8') + 0.2, S('8') + 2.2)
        if 0 < k < 1:
            for q in range(8):
                f = (k * 3 + q / 8) % 1.0
                coin(c, 190 + (500 - 190) * f, 420 + (930 - 420) * f - math.sin(f * math.pi) * 160, 1.0)
        name_card(c, 600, 300, 'LAKSHMI AUNTY', 'EXAMPLE', None, t, A['lakshmi'] - 0.2, w=420)
        if t >= A['busiest'] - 0.3:
            u = prog(t, A['busiest'] - 0.3, A['busiest'] + 0.3)
            for i in range(8):
                on = i in (4, 5, 6); x = 150 + i * 100
                glass_dark(c, x - 42, 1150, 84, 60, 12, u)
                if on: c.set_source_rgba(*AMBER, 0.9 * u); rrect(c, x - 42, 1150, 84, 60, 12); c.fill()
            mono(c, 'BUSIEST WEEKS', 690, 1250, 22, AMBER, a=u, kind='monob')
    # 9 85% mainline retail
    elif t < S('10') - 0.05:
        t0 = A['p85'] - 0.3
        for i in range(100):
            r_, q = divmod(i, 10); x = 306 + q * 52; y = 380 + r_ * 52
            on = i < int(85 * prog(t, t0, t0 + 1.0))
            c.set_source_rgba(*(AMBER if on else CREAM), 0.95 if on else 0.18); c.new_path(); c.arc(x, y, 18, 0, 2 * math.pi); c.fill()
        if t >= t0 + 1.0: big_num(c, '85%', W / 2, 960, 120, t, t0 + 1.0)
        pill(c, 'MAINLINE RETAIL · 2025 · CAIT ESTIMATE', W / 2, 1060, 24, CREAM, s=e_back(prog(t, S('9'), S('9') + 0.3)))
        draw_clip(c, 'cait85', W / 2, 1240, 880, t, A['p85'] + 1.0, rot=-0.6, hl_t0=A['p85'] + 1.3, hl_dur=1.4)
    # 10 50 lakh temporary jobs
    elif t < S('11') - 0.05:
        n = int(60 * e_out(prog(t, S('10'), A['j50'] + 0.8)))
        cols = [(0.95, 0.55, 0.2), (0.3, 0.6, 0.9), (0.4, 0.75, 0.45)]
        for i in range(n):
            r_, q = divmod(i, 10); person(c, 130 + q * 92, 470 + r_ * 100, 0.2, cols[i % 3], t=t + i)
        if t >= A['j50'] - 0.1: big_num(c, '≈ 50 LAKH', W / 2, 1120, 110, t, A['j50'] - 0.1)
        mono(c, 'TEMPORARY JOBS · 2025 · CAIT ESTIMATE', W / 2, 1230, 24, CREAM, a=prog(t, A['j50'], A['j50'] + 0.3), kind='monob')
    # 11 caveat + small shops
    elif t < S('12') - 0.05:
        if t < A['small'] - 0.3:
            stamp_txt(c, "TRADERS' ESTIMATES · NOT OFFICIAL", W / 2, 700, t, S('11') + 0.1, px=44, rot=-5, col=AMBER)
        else:
            k = prog(t, A['small'] - 0.3, A['small'] + 0.2)
            market(c, t, a=k, note=False); aunty(c, 540, 960, 0.95, t, a=k)
            c.set_source_rgba(0.62, 0.42, 0.26, k); c.rectangle(250, 960, 580, 140); c.fill()
            head(c, 'SMALL SHOPS', W / 2, 1230, 80, AMBER, a=k)
            mono(c, 'BIG PART OF THE STORY', W / 2, 1310, 28, CREAM, a=k, kind='monob')
    # 12 series slide
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('12') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        # a hand places the ₹100 note exactly where it lies in frame 0, then the market fades in around it
        ks = e_io(prog(t, S('L') - 0.05, S('L') + 0.45)); k = e_io(prog(t, S('L') + 0.8, S('L') + 1.5))
        c.push_group(); slide(c, t, S('12') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - ks)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
        if k < 1:
            u = e_out(prog(t, S('L') + 0.1, S('L') + 0.8)); y = 1500 + (NOTE[1] - 1500) * u
            note100(c, NOTE[0], y, 1.0, a=1 - k * 0, rot=-0.06)
            c.set_source_rgba(*SKIN, (1 - k) * (1 - prog(t, S('L') + 0.8, S('L') + 1.1))); rrect(c, NOTE[0] + 30, y + 10, 70, 160, 30); c.fill()
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('12') - 0.05: tag(c)
    return s
