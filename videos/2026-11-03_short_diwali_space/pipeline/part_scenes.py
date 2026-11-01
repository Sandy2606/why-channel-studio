
# ---------------- anchors ----------------
A = {
    'nasa1': AT('1', 'NASA', 'NASA'), 'itsnot': AT('1', 'not.', 'కాదు'),
    'raju': AT('2', 'Raju', 'రాజు'), 'fwd': AT('2', 'forwards', 'forward'),
    'y2003': AT('3', '2003', '2003'), 'elvidge': AT('3', 'Elvidge', 'Elvidge'), 'mil': AT('3', 'military', 'military'),
    'fire': AT('4', 'fireworks', 'బాణాసంచా'), 'years4': AT('4', 'years', 'సంవత్సరాలు'),
    'white': AT('5', 'White', 'తెలుపు'), 'blue': AT('5', 'Blue', 'నీలం'), 'green': AT('5', 'Green', 'ఆకుపచ్చ'), 'red': AT('5', 'Red', 'ఎరుపు'),
    'growing': AT('6', 'growing', 'పెరిగాయో'), 'onenight': AT('6', 'night', 'రాత్రి'),
    'clouds': AT('7', 'clouds', 'మేఘాలను'), 'city7': AT('7', 'city', 'నగరాల'),
    'real8': AT('8', "NASA's", 'NASA'),
    'rainbow': AT('9', 'rainbow', 'ఇంద్రధనుస్సు'),
    'subtle': AT('10', 'subtle', 'తక్కువ'),
    'k824': AT('11', '824', '824'), 'm750': AT('11', '750', '750'), 'hood': AT('11', 'neighbourhood', 'colony'),
    'street': AT('12', 'Street', 'Street'), 'blends': AT('12', 'blends', 'కలిసిపోతుంది'),
    'reply': AT('13', 'reply', 'reply'), 'wrong': AT('13', 'Wrong', 'తప్పు'),
    'tomorrow': S('14'), 'loop': S('L'),
}
A['end'] = DUR
"""HELPERS"""
# ---------------- 2/6 assets ----------------
IMGD = '/home/claude/why-channel-studio/videos/2026-11-01_long_diwali_explained/assets/images/'
VIRAL = IMGD + '09-india-diwali-rainbow-composite.jpg'
NASAIMG = IMGD + '10-nasa-suomi-npp-india-2012-11-12.jpg'
MASK = {}
def viral_mask(kind, w):
    key = (kind, w)
    if key not in MASK:
        im = Image.open(VIRAL).convert('RGB').resize((w, int(577 * w / 600)), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32) / 255
        hsv = np.asarray(im.convert('HSV')).astype(np.float32) / 255
        h, s_, v = hsv[..., 0] * 360, hsv[..., 1], hsv[..., 2]
        lit = v > 0.30
        sel = {'white': lit & (s_ < 0.28),
               'blue': lit & (s_ >= 0.28) & (h >= 180) & (h < 270),
               'green': lit & (s_ >= 0.28) & (h >= 75) & (h < 180),
               'red': lit & (s_ >= 0.28) & ((h < 40) | (h >= 300))}[kind]
        out = a * 0.12; out[sel] = a[sel] * 1.15
        MASK[key] = surf_from_pil(Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8)))[0]
    return MASK[key]

def burst_icon(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(12):
        an = k * math.pi / 6; c.set_source_rgba(*(AMBER if k % 2 else CREAM), a); c.set_line_width(8)
        c.move_to(math.cos(an) * 25, math.sin(an) * 25); c.line_to(math.cos(an) * 70, math.sin(an) * 70); c.stroke()
    c.restore()
def calendar_icon(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    rrect(c, -70, -60, 140, 130, 14); c.set_source_rgba(*CREAM, a); c.fill()
    rrect(c, -70, -60, 140, 36, 14); c.set_source_rgba(*AMBER, a); c.fill()
    for i in range(3):
        for j in range(3): c.set_source_rgba(*INK, 0.8 * a); c.rectangle(-48 + i * 36, -8 + j * 26, 22, 16); c.fill()
    c.restore()
def satellite(c, x, y, s, a=1.0, ang=0.0):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    for d in (-1, 1):
        c.set_source_rgba(0.25, 0.40, 0.75, a); c.rectangle(d * 40 - (90 if d < 0 else 0), -22, 90, 44); c.fill()
        c.set_source_rgba(1, 1, 1, 0.3 * a); c.set_line_width(2)
        for k in range(1, 4): c.move_to(d * 40 - (90 if d < 0 else 0) + k * 22, -22); c.line_to(d * 40 - (90 if d < 0 else 0) + k * 22, 22)
        c.stroke()
    rrect(c, -38, -30, 76, 60, 10); c.set_source_rgba(0.85, 0.85, 0.88, a); c.fill()
    c.set_source_rgba(*AMBER, a); c.arc(0, 34, 10, 0, 2 * math.pi); c.fill()
    c.restore()
def raju(c, x, y, s, t, a=1.0, react=0.0):
    person(c, x, y, s, (0.55, 0.22, 0.30), prop=None, a=a, t=t)
    bob = 3 * math.sin(t * 3.0)
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.1, 0.1, 0.1, a); c.set_line_width(4)               # glasses
    for d in (-1, 1): c.arc(d * 20, -345 + bob, 13, 0, 2 * math.pi); c.stroke()
    c.move_to(-7, -345 + bob); c.line_to(7, -345 + bob); c.stroke()
    c.set_source_rgba(0.85, 0.85, 0.85, a); c.arc(0, -400 + bob, 40, math.pi * 1.1, math.pi * 1.9); c.set_line_width(10); c.stroke()  # grey hair
    c.set_source_rgba(*SKIN, a); c.arc(70, -180 + bob, 18, 0, 2 * math.pi); c.fill()                   # hand + phone
    rrect(c, 60, -250 + bob, 44, 80, 8); c.set_source_rgba(0.12, 0.12, 0.14, a); c.fill()
    c.set_source_rgba(*AMBER, 0.8 * a); c.rectangle(65, -243 + bob, 34, 60); c.fill()
    c.restore()
    if react > 0:
        u = e_back(react); c.save(); c.translate(x + 120 * s, y - 470 * s); c.scale(max(0.01, u), max(0.01, u))
        c.set_source_rgba(*CREAM, a); c.arc(0, 0, 46, 0, 2 * math.pi); c.fill()
        font(c, 'head', 56); e = c.text_extents('!'); c.move_to(-e.width / 2 - e.x_bearing, 20); c.set_source_rgba(*INK, a); c.show_text('!'); c.restore()
def chat_panel(c, t, t0, x=470, y=330, w=560, h=760, count_t=None, reply_t=None, reply_full=None, a=1.0):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.35)) * a
    c.save(); c.translate(0, (1 - u) * 40)
    glass_dark(c, x, y, w, h, 34, u)
    c.set_source_rgba(*AMBER, u); c.arc(x + 50, y + 50, 18, 0, 2 * math.pi); c.fill()
    mono(c, 'FAMILY GROUP', x + 85, y + 50, 26, CREAM, a=u, anchor='l', kind='monob')
    # forwarded bubble with the photo
    bx, by = x + 30, y + 110
    rrect(c, bx, by, w - 110, 420, 22); c.set_source_rgba(0.16, 0.16, 0.19, u); c.fill()
    mono(c, 'Forwarded many times', bx + 22, by + 32, 18, CREAM, a=0.7 * u, anchor='l', kind='mono')
    sf = img(VIRAL, w - 150); c.save(); rrect(c, bx + 20, by + 60, w - 150, 340, 14); c.clip(); c.set_source_surface(sf, bx + 20, by + 40); c.paint_with_alpha(u); c.restore()
    if count_t is not None and t >= count_t:   # reactions count up
        k = prog(t, count_t, count_t + 1.3); n = int(52 * e_out(k))
        rrect(c, bx + 20, by + 395, 230, 54, 27); c.set_source_rgba(0.24, 0.24, 0.28, u); c.fill()
        for i, col in enumerate(((1.0, 0.35, 0.45), AMBER, (1.0, 0.85, 0.3))):
            c.set_source_rgba(*col, u); c.arc(bx + 50 + i * 30, by + 422, 12, 0, 2 * math.pi); c.fill()
        font(c, 'monob', 26); c.move_to(bx + 150, by + 432); c.set_source_rgba(*CREAM, u); c.show_text(f'{n}+')
    if reply_t is not None and t >= reply_t:   # the reply types out
        k = prog(t, reply_t, reply_t + 1.4); full = reply_full; n = max(1, int(len(full) * k))
        rx, ry = x + 90, y + h - 190
        rrect(c, rx, ry, w - 120, 120, 24); c.set_source_rgba(*AMBER, u); c.fill()
        txt_ = full[:n] + ('|' if k < 1 and int(t * 4) % 2 == 0 else '')
        if LANGV == 'te': TT.draw(c, txt_, rx + 24, ry + 60, 30, INK, u, 'l', 'Bold', maxw=w - 160)
        else:
            font(c, 'monob', 28); c.move_to(rx + 24, ry + 70); c.set_source_rgba(*INK, u); c.show_text(txt_)
    c.restore()

def sc_hook(c, t, frozen=False):
    sf = img(VIRAL, 900); w, h = sf.get_width(), sf.get_height()
    z = 1.0 if frozen else 1.0 + 0.05 * prog(t, 0, S('2'))
    c.save(); c.translate(W / 2, 680); c.scale(z, z)
    c.set_source_rgba(0, 0, 0, 0.5); rrect(c, -w / 2 + 10, -h / 2 + 16, w, h, 26); c.fill()
    rrect(c, -w / 2, -h / 2, w, h, 26); c.save(); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint(); c.restore()
    c.restore()
    pill(c, "NASA'S DIWALI PHOTO?", W / 2, 1210, 46, AMBER)
    if not frozen:
        for i, (lab, y, r) in enumerate((('NOT DIWALI', 470, -8), ('NOT FIREWORKS', 690, 6), ('NOT ONE NIGHT', 910, -5))):
            stamp_txt(c, lab, W / 2, y, t, A['itsnot'] - 0.05 + 0.28 * i, px=72, rot=r, col=AMBER)

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 Raju uncle
    elif t < S('3') - 0.05:
        raju(c, 250, 1180, 1.05, t, a=prog(t, A['raju'] - 0.2, A['raju'] + 0.1))
        mono(c, 'RAJU UNCLE', 250, 1235, 28, CREAM, a=prog(t, A['raju'], A['raju'] + 0.3), kind='monob')
        chat_panel(c, t, A['fwd'] - 0.3, count_t=A['fwd'] + 0.4)
    # 3 what it really is
    elif t < S('4') - 0.05:
        draw_clip(c, 'es_head', W / 2, 400, 900, t, S('3') - 0.05, rot=-1.0)
        draw_clip(c, 'es_cap', W / 2, 680, 1010, t, S('3') + 0.4, rot=0.8, hl_t0=S('3') + 0.8, hl_dur=1.3)
        source_tag(c, 'EARTHSKY · NOV 6, 2018', 90, 820, a=prog(t, S('3') + 0.3, S('3') + 0.6))
        if t >= A['y2003'] - 0.2:
            name_card(c, 230, 900, 'CHRIS ELVIDGE', 'NOAA SCIENTIST', '2003', t, A['y2003'] - 0.2, w=620)
        if t >= A['mil'] - 0.2:
            pill(c, 'DMSP · US DEFENSE METEOROLOGICAL SATELLITE PROGRAM', W / 2, 1150, 20, CREAM, s=e_back(prog(t, A['mil'] - 0.2, A['mil'] + 0.1)))
    # 4 colours are years
    elif t < S('5') - 0.05:
        sf = img(VIRAL, 700); w, h = sf.get_width(), sf.get_height()
        c.save(); c.translate(W / 2, 560); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint(); c.restore()
        cols = [CREAM, (0.35, 0.55, 1.0), (0.3, 0.9, 0.45), (1.0, 0.3, 0.25)]
        for i, col in enumerate(cols):
            k = e_back(prog(t, S('4') + 0.1 + 0.12 * i, S('4') + 0.4 + 0.12 * i))
            if k > 0: c.set_source_rgba(*col, 1); c.arc(300 + i * 160, 1000, 40 * min(k, 1.1), 0, 2 * math.pi); c.fill()
        if t < A['years4'] - 0.1:
            burst_icon(c, W / 2, 1180, 1.0, a=prog(t, A['fire'] - 0.2, A['fire']))
            if t >= A['fire'] + 0.3: cross(c, W / 2, 1180, 2.0, prog(t, A['fire'] + 0.3, A['fire'] + 0.6), CREAM)
        else:
            calendar_icon(c, W / 2, 1180, 1.0 * e_back(prog(t, A['years4'] - 0.1, A['years4'] + 0.2)))
            head(c, 'THEY\'RE YEARS', W / 2, 1300, 52, AMBER, a=prog(t, A['years4'], A['years4'] + 0.3))
    # 5 legend
    elif t < S('6') - 0.05:
        order = [('white', A['white'], 'BEFORE 1992', CREAM), ('blue', A['blue'], '1992', (0.35, 0.55, 1.0)),
                 ('green', A['green'], '1998', (0.3, 0.9, 0.45)), ('red', A['red'], '2003', (1.0, 0.3, 0.25))]
        cur = 0
        for i, (_, tt, _, _) in enumerate(order):
            if t >= tt - 0.15: cur = i
        sf = viral_mask(order[cur][0], 860); w, h = sf.get_width(), sf.get_height()
        c.save(); c.translate(W / 2, 640); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint(); c.restore()
        for i, (_, tt, lab, col) in enumerate(order):
            if t < tt - 0.15: continue
            x = 160 + i * 253; on = i == cur; u = e_out(prog(t, tt - 0.15, tt + 0.1))
            glass_dark(c, x - 115, 1110, 230, 150, 24, u)
            if on: c.set_source_rgba(*col, u); c.set_line_width(5); rrect(c, x - 115, 1110, 230, 150, 24); c.stroke()
            c.set_source_rgba(*col, u); c.arc(x, 1160, 22, 0, 2 * math.pi); c.fill()
            mono(c, lab, x, 1222, 24 if len(lab) < 6 else 19, col if on else CREAM, a=u, kind='monob')
    # 6 hero: 11 years vs 1 night
    elif t < S('7') - 0.05:
        mono(c, 'A MAP OF INDIA GROWING', W / 2, 300, 30, CREAM, a=prog(t, S('6'), S('6') + 0.3), kind='monob')
        if t >= A['growing'] - 0.2:
            mono(c, '1992 → 2003', W / 2, 430, 44, AMBER, a=prog(t, A['growing'] - 0.2, A['growing']), kind='monob')
            big_num(c, '11 YEARS', W / 2, 590, 170, t, A['growing'])
        if t >= A['onenight'] - 0.6:
            head(c, 'NOT', W / 2, 800, 60, CREAM, a=prog(t, A['onenight'] - 0.6, A['onenight'] - 0.4))
            head(c, '1 NIGHT', W / 2, 950, 150, CREAM, a=prog(t, A['onenight'] - 0.4, A['onenight'] - 0.1))
            cross(c, W / 2, 950, 4.0, prog(t, A['onenight'], A['onenight'] + 0.35), AMBER)
    # 7 satellites built for clouds by moonlight
    elif t < S('8') - 0.05:
        g = cairo.RadialGradient(W / 2, 2500, 900, W / 2, 2500, 1500); g.add_color_stop_rgba(0, 0.05, 0.12, 0.28, 1); g.add_color_stop_rgba(1, 0.02, 0.05, 0.12, 1)
        c.set_source(g); c.arc(W / 2, 2500, 1500, 0, 2 * math.pi); c.fill()
        mk = prog(t, A['clouds'] - 0.3, A['clouds'] + 0.4)
        c.set_source_rgba(0.95, 0.95, 0.85, 0.9); c.arc(880, 330, 55, 0, 2 * math.pi); c.fill()
        g2 = cairo.RadialGradient(880, 330, 50, 880, 330, 260); g2.add_color_stop_rgba(0, 1, 1, 0.9, 0.25 * mk); g2.add_color_stop_rgba(1, 1, 1, 0.9, 0); c.set_source(g2); c.paint()
        for i, (cx, cy) in enumerate(((260, 1110), (520, 1060), (790, 1120), (400, 1190), (680, 1200))):
            c.set_source_rgba(0.85, 0.88, 0.95, 0.15 + 0.55 * mk)
            for dx, dy, r in ((-40, 0, 40), (0, -18, 50), (45, 0, 38)): c.arc(cx + dx, cy + dy, r, 0, 2 * math.pi); c.fill()
        ck = prog(t, A['city7'] - 0.2, A['city7'] + 0.8)
        rng = np.random.default_rng(7)
        for i in range(60):
            x = rng.uniform(120, 960); y = rng.uniform(1020, 1320); k = clamp(ck * 60 - i)
            if k > 0: glowdot(c, x, y, 5 + 3 * rng.random(), a=k)
        satellite(c, 200 + 680 * prog(t, S('7'), S('8')), 520, 1.0, ang=0.15)
        if mk > 0: mono(c, 'CLOUDS BY MOONLIGHT', W / 2, 760, 30, CREAM, a=mk, kind='monob')
        if ck > 0: mono(c, '+ CITY LIGHTS', W / 2, 830, 34, AMBER, a=prog(t, A['city7'] - 0.2, A['city7'] + 0.1), kind='monob')
    # 8 NASA's real image
    elif t < S('9') - 0.05:
        head(c, "NASA'S REAL IMAGE", W / 2, 260, 56, CREAM, a=prog(t, A['real8'] - 0.3, A['real8']))
        if t >= A['real8'] - 0.3:
            sf = img(NASAIMG, 880); w, h = sf.get_width(), sf.get_height(); u = e_out(prog(t, A['real8'] - 0.3, A['real8'] + 0.2))
            z = 1.0 + 0.06 * prog(t, A['real8'], S('9'))
            c.save(); c.translate(W / 2, 760 + (1 - u) * 100); c.scale(z, z); rrect(c, -w / 2, -h / 2, w, h, 22); c.clip(); c.set_source_surface(sf, -w / 2, -h / 2); c.paint_with_alpha(u); c.restore()
            pill(c, 'NOV 12, 2012 · DIWALI WEEK', W / 2, 1250, 32, AMBER, s=e_back(prog(t, A['real8'] + 0.4, A['real8'] + 0.7)))
            mono(c, 'NASA EARTH OBSERVATORY · VIIRS / SUOMI NPP', W / 2, 1320, 18, CREAM, a=0.8 * u, kind='mono')
    # 9 fake vs real
    elif t < S('10') - 0.05:
        for j, (path, lab, ok) in enumerate(((VIRAL, 'VIRAL', False), (NASAIMG, 'REAL', True))):
            u = e_out(prog(t, S('9') - 0.05 + 0.15 * j, S('9') + 0.3 + 0.15 * j)); x = 90 + j * 470
            sf = img(path, 430); w, h = sf.get_width(), min(sf.get_height(), 430)
            c.save(); c.translate(0, (1 - u) * 50); rrect(c, x, 400, 430, 430, 22); c.clip(); c.set_source_surface(sf, x, 400); c.paint_with_alpha(u); c.restore()
            if ok: c.set_source_rgba(*AMBER, u); c.set_line_width(6); rrect(c, x, 400, 430, 430, 22); c.stroke()
            head(c, lab, x + 215, 900, 60, AMBER if ok else CREAM, a=u, shadow=False)
            k = prog(t, (S('9') + 0.6) if ok else A['rainbow'] - 0.2, (S('9') + 0.9) if ok else A['rainbow'] + 0.1)
            (tick if ok else cross)(c, x + 215, 1040, 1.6, k, AMBER if ok else CREAM)
        mono(c, 'ORANGE + WHITE = STREET LIGHTS', W / 2, 1200, 26, AMBER, a=prog(t, S('9') + 0.4, S('9') + 0.7), kind='monob')
    # 10 NASA proof card
    elif t < S('11') - 0.05:
        c.set_source_rgba(0, 0, 0, 0.35); c.paint()
        draw_clip(c, 'nasa_h1', W / 2, 560, 760, t, S('10') - 0.05, rot=-1.0)
        draw_clip(c, 'nasa_para', W / 2, 800, 1030, t, S('10') + 0.15, rot=0.6, hl_t0=A['subtle'] - 0.2, hl_dur=1.6)
        source_tag(c, 'NASA EARTH OBSERVATORY · SOUTH ASIAN NIGHT LIGHTS', 90, 960, a=prog(t, S('10') + 0.3, S('10') + 0.6))
    # 11 the pixel
    elif t < S('12') - 0.05:
        satellite(c, W / 2, 300, 0.9)
        k = prog(t, A['k824'] - 0.4, A['k824'] + 0.3)
        c.set_source_rgba(*AMBER, 0.8); c.set_line_width(4); c.set_dash([10, 10]); c.move_to(W / 2, 360); c.line_to(W / 2, 360 + 500 * k); c.stroke(); c.set_dash([])
        if t >= A['k824'] - 0.1: big_num(c, '824 KM', 790, 600, 90, t, A['k824'] - 0.1)
        # colony map
        gy = 900
        for i in range(9):
            for j in range(4):
                c.set_source_rgba(0.22, 0.22, 0.26, 1); c.rectangle(160 + i * 86, gy + j * 86, 70, 70); c.fill()
        if t >= A['m750'] - 0.3:
            u = e_out(prog(t, A['m750'] - 0.3, A['m750'] + 0.1)); yy = 360 + (gy - 20 - 360) * u
            c.set_source_rgba(*AMBER, 0.25); c.rectangle(300, yy, 480, 380); c.fill()
            c.set_source_rgba(*AMBER, 1); c.set_line_width(6); c.rectangle(300, yy, 480, 380); c.stroke()
            if u >= 1:
                pill(c, '1 PIXEL ≈ 750 m', W / 2, 820, 40, AMBER)
                mono(c, 'VIIRS DAY/NIGHT BAND · NOMINAL RESOLUTION', W / 2, 1300, 18, CREAM, a=0.8, kind='mono')
        if t >= A['hood'] - 0.2: head(c, 'A WHOLE NEIGHBOURHOOD', W / 2, 1240, 52, CREAM, a=prog(t, A['hood'] - 0.2, A['hood'] + 0.1))
    # 12 diyas blend in
    elif t < S('13') - 0.05:
        c.set_source_rgba(*AMBER, 1); c.set_line_width(6); c.rectangle(140, 330, 640, 640); c.stroke()
        mono(c, 'INSIDE 1 PIXEL', 460, 300, 24, AMBER, kind='monob')
        rng = np.random.default_rng(3)
        for i in range(70):
            x, y = 170 + rng.uniform(0, 580), 360 + rng.uniform(0, 580); fl = 0.6 + 0.4 * math.sin(t * 9 + i)
            c.set_source_rgba(1.0, 0.75, 0.3, 0.9 * fl * prog(t, S('12'), S('12') + 0.5)); c.arc(x, y, 3, 0, 2 * math.pi); c.fill()
        if t >= A['street'] - 0.2:
            k = prog(t, A['street'] - 0.2, A['street'] + 0.4)
            for i in range(6):
                for j in range(6): glowdot(c, 200 + i * 104, 390 + j * 104, 11, a=k)
        mono(c, 'DIYAS', 300, 1010, 26, CREAM, a=prog(t, S('12'), S('12') + 0.3), kind='monob')
        if t >= A['street'] - 0.2: mono(c, 'STREET LIGHTS · EVERY NIGHT', 520, 1060, 22, AMBER, a=prog(t, A['street'] - 0.2, A['street']), kind='monob')
        # brightness meter
        glass_dark(c, 840, 330, 140, 640, 30)
        lev = 0.72 + 0.04 * prog(t, A['blends'] - 0.4, A['blends'])
        rrect(c, 870, 330 + 610 - 580 * lev, 80, 580 * lev, 20); c.set_source(agrad(870, 0, 950, 0)); c.fill()
        mono(c, 'BRIGHTNESS', 910, 1000, 18, CREAM, kind='monob')
        if t >= A['blends'] - 0.2: head(c, 'DIWALI BLENDS IN', W / 2, 1200, 64, AMBER, a=prog(t, A['blends'] - 0.2, A['blends'] + 0.1))
    # 13 the reply
    elif t < S('14') - 0.05:
        full = 'Beautiful map. Wrong night.' if LANGV == 'en' else 'Map బాగుంది. రాత్రే తప్పు.'
        raju(c, 250, 1180, 1.05, t, react=prog(t, A['wrong'] + 0.4, A['wrong'] + 0.7))
        mono(c, 'RAJU UNCLE', 250, 1235, 28, CREAM, kind='monob')
        chat_panel(c, t, S('13') - 0.3, count_t=S('13') - 2.0, reply_t=A['reply'] + 0.1, reply_full=full)
    # 14 series slide + CTA
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('14') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        k = e_io(prog(t, S('L') - 0.05, S('L') + 0.7))
        c.push_group(); slide(c, t, S('14') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - k)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('14') - 0.05: tag(c)
    return s
