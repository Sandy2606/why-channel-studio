
# ---------------- anchors ----------------
A = {
    'm70': AT('1', '70', '70'), 'why1': AT('1', 'Why', 'ఎందుకు'),
    'means': AT('2', 'means', 'అంటే'),
    'samvat': AT('3', 'Samvat', 'Samvat'),
    'closed': AT('4', 'closed', 'మూసేసి'), 'chopda': AT('4', 'Chopda', 'Chopda'),
    'first': AT('5', 'first', 'మొదటి'),
    'y1957': AT('6', '1957', '1957'), 'y1994': AT('6', '1994', '1994'),
    'preopen': AT('7', 'pre-open', 'pre-open'), 'trading7': AT('7', 'Trading', 'trading') if LANGV == 'en' else AT('7', None, 'రెండు', n=2), 'last': AT('7', 'Last', 'పోయిన'),
    'suresh': AT('8', 'Suresh', 'సురేష్'), 'one': AT('8', 'one', 'ఒక్క'), 'shagun': AT('8', 'shagun', 'శుభం'),
    'eleven': AT('9', '11', '11'), 'nine': AT('9', '9', '9'),
    'tiny': AT('10', 'tiny', 'చిన్నది'), 'ritual': AT('10', 'ritual', 'ఆచారం'),
    'real': AT('11', 'real', 'నిజమైనవే'), 'settle': AT('11', 'settle', 'settle'),
    'tomorrow': S('12'), 'loop': S('L'),
}
A['end'] = DUR
"""HELPERS"""
# ---------------- 4/6 drawings ----------------
LOOPDIYA = (540, 1062)
NIFTY = [(2015, 0.53), (2016, -0.14), (2017, -0.63), (2018, 0.65), (2019, 0.37), (2020, 0.47), (2021, 0.49), (2022, 0.87), (2023, 0.51), (2024, 0.40), (2025, 0.10)]
RED = (0.86, 0.22, 0.12); GREEN = (0.30, 0.78, 0.45)
def diya(c, x, y, s, t, a=1.0, lit=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fl = 0.85 + 0.15 * math.sin(t * 9 + x)
    if lit > 0:
        g = cairo.RadialGradient(0, -30, 0, 0, -30, 90); g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.55 * a * fl * lit); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0); c.set_source(g); c.arc(0, -30, 90, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.78, 0.40, 0.18, a); c.move_to(-42, 0); c.curve_to(-32, 32, 32, 32, 42, 0); c.close_path(); c.fill()
    c.set_source_rgba(0.95, 0.62, 0.25, a); c.save(); c.scale(1, 0.25); c.arc(0, 0, 42, 0, 2 * math.pi); c.restore(); c.fill()
    if lit > 0:
        h = 55 * fl * lit
        c.set_source_rgba(1.0, 0.75, 0.25, a * min(1, lit * 1.5)); c.move_to(0, -6); c.curve_to(-11, -22, -4, -h * 0.75, 0, -h); c.curve_to(4, -h * 0.75, 11, -22, 0, -6); c.fill()
        c.set_source_rgba(1, 0.95, 0.75, a * lit); c.move_to(0, -8); c.curve_to(-5, -16, -2, -h * 0.45, 0, -h * 0.55); c.curve_to(2, -h * 0.45, 5, -16, 0, -8); c.fill()
    c.restore()
def room(c, t, a=1.0, loop_diya=True):
    c.save(); c.push_group()
    c.set_source_rgb(0.17, 0.14, 0.22); c.rectangle(60, 260, 960, 840); c.fill()                       # dusk wall
    c.set_source_rgb(0.12, 0.10, 0.16); c.rectangle(60, 1100, 960, 90); c.fill()                       # floor
    for i in range(17):                                                                                  # marigold toran
        x = 90 + i * 57; y = 290 + 22 * math.sin(i / 16 * math.pi)
        c.set_source_rgb(0.98, 0.55 + 0.15 * (i % 2), 0.12); c.arc(x, y, 18, 0, 2 * math.pi); c.fill()
        if i % 3 == 1: c.set_source_rgb(0.25, 0.55, 0.25); c.move_to(x, y + 14); c.line_to(x - 10, y + 50); c.line_to(x + 10, y + 50); c.close_path(); c.fill()
    c.set_source_rgb(0.92, 0.90, 0.84); c.arc(890, 430, 70, 0, 2 * math.pi); c.fill()                  # wall clock 2:20
    c.set_source_rgb(0.12, 0.12, 0.14)
    for hk in range(12):
        an = hk * math.pi / 6; r0 = 52 if hk % 3 else 46
        c.set_line_width(6 if hk % 3 == 0 else 3); c.move_to(890 + r0 * math.sin(an), 430 - r0 * math.cos(an)); c.line_to(890 + 62 * math.sin(an), 430 - 62 * math.cos(an)); c.stroke()
    c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for an, ln in ((2 * math.pi * (2 + 20 / 60) / 12, 34), (2 * math.pi * 20 / 60, 54)):
        c.move_to(890, 430); c.line_to(890 + ln * math.sin(an), 430 - ln * math.cos(an)); c.stroke()
    c.set_source_rgb(0.40, 0.27, 0.18); c.rectangle(150, 940, 780, 40); c.fill()                       # table
    c.rectangle(190, 980, 30, 120); c.fill(); c.rectangle(860, 980, 30, 120); c.fill()
    c.set_source_rgb(0.55, 0.56, 0.60); rrect(c, 290, 560, 500, 330, 18); c.fill()                     # laptop
    c.set_source_rgb(0.05, 0.07, 0.08); rrect(c, 306, 576, 468, 298, 10); c.fill()
    c.set_source_rgb(0.62, 0.63, 0.67); c.move_to(250, 940); c.line_to(830, 940); c.line_to(790, 890); c.line_to(290, 890); c.close_path(); c.fill()
    vals = [0, 12, 6, 22, 16, 30, 24, 40, 34, 48, 42, 58, 52, 66, 60, 74]
    for i, v in enumerate(vals[1:]):                                                                     # green candles
        x = 330 + i * 28; up = v > vals[i]; col = GREEN if up else RED
        y0 = 820 - vals[i] * 3; y1 = 820 - v * 3
        c.set_source_rgb(*col); c.rectangle(x, min(y0, y1), 16, max(6, abs(y1 - y0))); c.fill()
        c.set_line_width(2); c.move_to(x + 8, min(y0, y1) - 10); c.line_to(x + 8, max(y0, y1) + 10); c.stroke()
    font(c, 'monob', 18); c.set_source_rgb(*GREEN); c.move_to(326, 606); c.show_text('NIFTY 50  ▲')
    for x in (360, 720):
        diya(c, x, 1062, 0.85, t)
    if loop_diya: diya(c, *LOOPDIYA, 0.85, t)
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
CHAIN = ['MUHURAT', 'NEW YEAR', 'NEW BOOKS', 'FIRST DEAL', '70 MIN']
def chain(c, t, active, a=1.0):
    xs = [130, 330, 540, 750, 950]
    for i, (w_, x) in enumerate(zip(CHAIN, xs)):
        if i == active: pill(c, w_, x, 215, 22, AMBER, a=a)
        else: mono(c, w_, x, 215, 18, AMBER if i < active else CREAM, a=a * (0.6 if i < active else 0.28), kind='monob')
def swastika(c, x, y, s, a=1.0):
    """traditional Chopda Pujan mark: upright, right-facing, kumkum red-orange, with four dots"""
    c.save(); c.translate(x, y); c.scale(s, s)
    col = (0.88, 0.28, 0.10)
    c.set_source_rgba(*col, a); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(0, -60); c.line_to(0, 60); c.move_to(-60, 0); c.line_to(60, 0)
    c.move_to(0, -60); c.line_to(60, -60); c.move_to(60, 0); c.line_to(60, 60); c.move_to(0, 60); c.line_to(-60, 60); c.move_to(-60, 0); c.line_to(-60, -60)
    c.stroke()
    for dx, dy in ((30, -30), (30, 30), (-30, 30), (-30, -30)): c.arc(dx, dy, 9, 0, 2 * math.pi); c.fill()
    c.restore()
DEV = {}
def dev_text(c, txt, x, y, px, col, a=1.0):
    key = (txt, px)
    if key not in DEV:
        f = ImageFont.truetype('/home/claude/fonts/NotoSansDevanagari-Bold.ttf', int(px), layout_engine=ImageFont.Layout.RAQM)
        w = int(f.getlength(txt)) + 20; im = Image.new('RGBA', (w, int(px * 1.6)), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, px * 0.8), txt, font=f, fill=tuple(int(v * 255) for v in col) + (255,), anchor='lm'); DEV[key] = surf_from_pil(im)[0]
    sf = DEV[key]; c.set_source_surface(sf, x - sf.get_width() / 2, y - sf.get_height() / 2); c.paint_with_alpha(a)
def ledger(c, cx, cy, t, open_k, a=1.0, first_glow=0.0, marks=True):
    c.save(); c.translate(cx, cy)
    w, h = 380, 470
    c.set_source_rgba(0.62, 0.08, 0.08, a); rrect(c, -w - 16, -h / 2 - 14, 2 * w + 32, h + 28, 18); c.fill()            # red cloth cover
    for side in (-1, 1):
        c.save(); c.scale(side if side > 0 else -1 * max(0.02, open_k), 1)
        c.set_source_rgba(0.97, 0.93, 0.82, a); c.rectangle(0, -h / 2, w, h); c.fill()
        c.set_source_rgba(0.75, 0.30, 0.25, 0.35 * a); c.set_line_width(2)
        for k in range(1, 11): c.move_to(20, -h / 2 + k * 42); c.line_to(w - 20, -h / 2 + k * 42)
        c.stroke(); c.restore()
    c.set_source_rgba(0.45, 0.05, 0.05, a); c.rectangle(-4, -h / 2, 8, h); c.fill()
    if marks and open_k > 0.9:
        k = prog(open_k, 0.9, 1.0)
        swastika(c, -w / 2, -60, 1.15, a=a * k)
        dev_text(c, 'शुभ लाभ', w / 2, -90, 64, (0.80, 0.12, 0.08), a=a * k)
        c.set_source_rgba(0.80, 0.12, 0.08, a * k); c.set_line_width(4); c.move_to(w / 2 - 110, -30); c.line_to(w / 2 + 110, -30); c.stroke()
    if first_glow > 0:
        c.set_source_rgba(*AMBER, 0.55 * first_glow * a); c.rectangle(20, -h / 2 + 302, w - 40, 36); c.fill()
    c.restore()
def coin(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.set_source_rgba(0.95, 0.75, 0.25, a); c.arc(0, 0, 34, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.80, 0.58, 0.15, a); c.set_line_width(5); c.arc(0, 0, 25, 0, 2 * math.pi); c.stroke()
    font(c, 'head', 30); e = c.text_extents('₹'); c.move_to(-e.width / 2 - e.x_bearing, 11); c.show_text('₹'); c.restore()
def node(c, x, y, year, l1, l2, t, t0, cur=False):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3))
    c.save(); c.translate(x, y); c.scale(max(0.01, u), max(0.01, u))
    c.set_source_rgb(*AMBER) if cur else c.set_source_rgb(*CREAM); c.arc(0, 0, 22, 0, 2 * math.pi); c.fill()
    c.restore()
    k = prog(t, t0 + 0.1, t0 + 0.4)
    head(c, year, x, y - 70, 62, AMBER, a=k)
    mono(c, l1, x, y + 62, 20, CREAM, a=k, kind='monob'); mono(c, l2, x, y + 92, 20, CREAM, a=k, kind='monob')

def sc_hook(c, t, frozen=False):
    tt = 0.0 if frozen else t
    room(c, tt)
    mono(c, 'DIWALI · SUNDAY', W / 2, 1185, 30, CREAM, kind='monob')
    head(c, 'MARKET OPEN…', W / 2, 1262, 76, CREAM)
    head(c, 'ON DIWALI?', W / 2, 1346, 76, AMBER)
    if not frozen and t >= A['m70'] - 0.15:
        u = e_back(prog(t, A['m70'] - 0.15, A['m70'] + 0.15))
        c.save(); c.translate(W / 2, 700); c.scale(max(0.01, u), max(0.01, u)); hw = 260 if LANGV == 'en' else 340; glass_dark(c, -hw, -110, 2 * hw, 220, 36)
        c.set_source_rgba(*AMBER, 1); c.set_line_width(5); rrect(c, -hw, -110, 2 * hw, 220, 36); c.stroke(); c.restore()
        big_num(c, '70 MIN', W / 2, 690, 130 if LANGV == 'en' else 110, t, A['m70'] - 0.15)
        pill(c, 'MAIN CASH-EQUITY WINDOW · OTHER SEGMENTS DIFFER', W / 2, 860, 18, CREAM, s=e_back(prog(t, A['m70'] + 0.4, A['m70'] + 0.7)))

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 muhurat = auspicious time
    elif t < S('3') - 0.05:
        chain(c, t, 0)
        diya(c, W / 2, 470, 1.3, t, a=prog(t, S('2'), S('2') + 0.3))
        big_num(c, 'MUHURAT', W / 2, 640, 120, t, S('2') + 0.05)
        if t >= A['means'] - 0.1:
            head(c, '=', W / 2, 790, 80, CREAM, a=prog(t, A['means'] - 0.1, A['means'] + 0.1))
            pill(c, 'AUSPICIOUS TIME', W / 2, 920, 46, AMBER, s=e_back(prog(t, A['means'], A['means'] + 0.3)))
    # 3 new accounting year
    elif t < S('4') - 0.05:
        chain(c, t, 1)
        u = e_out(prog(t, S('3'), S('3') + 0.35))
        x0, y0, w, h = 280, 380, 520, 600
        c.save(); c.translate(0, (1 - u) * 80)
        c.set_source_rgba(0.97, 0.95, 0.90, u); rrect(c, x0, y0, w, h, 26); c.fill()
        c.set_source_rgba(0.80, 0.15, 0.10, u); rrect(c, x0, y0, w, 120, 26); c.fill(); c.rectangle(x0, y0 + 80, w, 40); c.fill()
        for rx in (x0 + 120, x0 + w - 120):
            c.set_source_rgba(0.3, 0.3, 0.32, u); c.arc(rx, y0 + 10, 14, 0, 2 * math.pi); c.fill()
        mono(c, 'SAMVAT', W / 2, y0 + 62, 40, CREAM, a=u, kind='monob')
        tf = A['samvat'] + 0.25; k = prog(t, tf, tf + 0.35)
        yr = '2082' if k < 0.5 else '2083'; sq = abs(math.cos(k * math.pi))
        c.save(); c.translate(W / 2, y0 + 340); c.scale(1, max(0.02, sq))
        font(c, 'head', 150); e = c.text_extents(yr); c.move_to(-e.width / 2 - e.x_bearing, 54)
        c.set_source_rgba(*(INK if k < 0.5 else (0.80, 0.15, 0.10)), u); c.show_text(yr); c.restore()
        c.restore()
        if t >= tf + 0.35: pill(c, 'NEW ACCOUNTING YEAR', W / 2, 1100, 34, AMBER, s=e_back(prog(t, tf + 0.35, tf + 0.6)))
    # 4 chopda pujan
    elif t < S('5') - 0.05:
        chain(c, t, 2)
        k_old = prog(t, A['closed'] - 0.3, A['closed'] + 0.6)
        if k_old < 1:
            c.save(); c.translate(-700 * e_io(prog(t, A['closed'] + 0.1, A['closed'] + 0.7)), 0)
            c.set_source_rgba(0.45, 0.33, 0.22, 1); rrect(c, 360, 420, 360, 460, 14); c.fill()
            c.set_source_rgba(0.62, 0.50, 0.36, 1); rrect(c, 380, 440, 320, 420, 10); c.fill()
            mono(c, 'OLD BOOKS · 2082', 540, 650, 24, INK, kind='monob'); c.restore()
        if t >= A['closed'] + 0.3:
            ok = e_io(prog(t, A['closed'] + 0.3, A['closed'] + 1.0))
            ledger(c, W / 2, 680, t, ok)
            diya(c, 900, 1010, 0.8, t, a=ok)
        if t >= A['chopda'] - 0.2:
            head(c, 'CHOPDA PUJAN', W / 2, 1060, 70, AMBER, a=prog(t, A['chopda'] - 0.2, A['chopda'] + 0.1))
            mono(c, 'WORSHIP OF ACCOUNT BOOKS', W / 2, 1135, 24, CREAM, a=prog(t, A['chopda'], A['chopda'] + 0.3), kind='monob')
    # 5 first investment
    elif t < S('6') - 0.05:
        chain(c, t, 3)
        gl = e_io(prog(t, A['first'] - 0.4, A['first'] + 0.2))
        ledger(c, W / 2, 680, t, 1.0, first_glow=gl)
        ky = e_out(prog(t, A['first'] - 0.1, A['first'] + 0.35))
        if t >= A['first'] - 0.1: coin(c, W / 2 + 190, 200 + (765 - 200) * ky, 1.0)
        if t >= A['first'] + 0.4: pill(c, 'FIRST INVESTMENT · AUSPICIOUS TIME', W / 2, 1100, 30, AMBER, s=e_back(prog(t, A['first'] + 0.4, A['first'] + 0.7)))
    # 6 timeline
    elif t < S('7') - 0.05:
        chain(c, t, 3)
        k = e_io(prog(t, S('6'), A['y1994'] + 1.2))
        c.set_source_rgba(*CREAM, 0.4); c.set_line_width(6); c.move_to(160, 560); c.line_to(160 + 760 * k, 560); c.stroke()
        node(c, 180, 560, '1957', 'BSE BEGINS', 'MUHURAT TRADING', t, A['y1957'] - 0.3)
        node(c, 540, 560, '1994', 'NSE EQUITY', 'TRADING BEGINS', t, A['y1994'] - 0.3)
        node(c, 900, 560, '2026', 'THIS SUNDAY', '70 MIN', t, A['y1994'] + 1.1, cur=True)
        draw_clip(c, 'ao', W / 2, 930, 940, t, A['y1957'] + 0.1, rot=-0.8, hl_t0=A['y1957'] + 0.4, hl_dur=1.0)
        source_tag(c, 'ANGEL ONE · MUHURAT TRADING 2026', 90, 1040, a=prog(t, A['y1957'] + 0.3, A['y1957'] + 0.6))
        source_tag(c, 'BUSINESS STANDARD · NSE EQUITIES BEGAN 3 NOV 1994', 90, 1100, a=prog(t, A['y1994'], A['y1994'] + 0.3))
    # 7 the schedule
    elif t < S('8') - 0.05:
        chain(c, t, 4)
        name = 'zd' if t < A['trading7'] - 0.2 else 'zd2'
        draw_clip(c, name, W / 2, 690, 760, t, S('7') - 0.3 if name == 'zd' else -1, rot=-0.6,
                  hl_t0=(A['preopen'] - 0.1) if name == 'zd' else A['trading7'] - 0.15, hl_dur=0.9)
        source_tag(c, 'ZERODHA · NSE/BSE MUHURAT SCHEDULE · 27 OCT 2026', 90, 1085)
        if t >= A['last'] - 0.3:
            for j, (lab, mins, col) in enumerate((('2025 · 60 MIN', 60, CREAM), ('2026 · 70 MIN', 70, AMBER))):
                kk = e_out(prog(t, A['last'] - 0.3 + 0.35 * j, A['last'] + 0.3 + 0.35 * j)); y = 1170 + j * 80
                c.set_source_rgba(1, 1, 1, 0.12); rrect(c, 330, y - 24, 640, 48, 24); c.fill()
                c.set_source_rgba(*col, 0.9 if j else 0.55); rrect(c, 330, y - 24, max(48, 640 * mins / 70 * kk), 48, 24); c.fill()
                mono(c, lab, 310, y, 26, col, anchor='r', kind='monob')
    # 8 Suresh uncle
    elif t < S('9') - 0.05:
        person(c, 290, 1180, 1.25, (0.95, 0.55, 0.15), t=t, a=prog(t, S('8'), S('8') + 0.3))
        c.set_source_rgba(0.85, 0.10, 0.10, prog(t, S('8'), S('8') + 0.3)); rrect(c, 285, 1180 - 1.25 * 392, 10, 26, 4); c.fill()   # tilak
        name_card(c, 70, 330, 'SURESH UNCLE', 'EXAMPLE', None, t, A['suresh'] - 0.2, w=440)
        u = e_out(prog(t, A['suresh'], A['suresh'] + 0.35))
        c.save(); c.translate(0, (1 - u) * 80)
        glass_dark(c, 580, 470, 400, 640, 40, u); c.set_source_rgba(0.08, 0.09, 0.10, u); rrect(c, 600, 490, 360, 600, 28); c.fill()
        mono(c, 'MUHURAT SESSION', 780, 540, 20, CREAM, a=0.7 * u, kind='monob')
        mono(c, 'NIFTY 50 STOCK', 780, 610, 26, CREAM, a=u, kind='monob')
        head(c, 'QTY  1', 780, 720, 64, CREAM, a=u, shadow=False)
        if t >= A['one'] - 0.1:
            kb = e_back(prog(t, A['one'] - 0.1, A['one'] + 0.2))
            c.save(); c.translate(780, 880); c.scale(max(0.01, kb), max(0.01, kb)); rrect(c, -150, -50, 300, 100, 50); c.set_source_rgb(*GREEN); c.fill()
            head(c, 'BUY × 1', 0, 0, 44, INK, shadow=False); c.restore()
        c.restore()
        if t >= A['shagun'] - 0.1: stamp_txt(c, 'SHAGUN', 780, 1010, t, A['shagun'] - 0.1, px=64, rot=-8, col=AMBER)
    # 9 11 sessions
    elif t < S('10') - 0.05:
        pill(c, 'NIFTY 50 · CHANGE VS PREVIOUS CLOSE', W / 2, 400, 24, CREAM, s=e_back(prog(t, S('9'), S('9') + 0.3)))
        t0 = A['eleven'] - 0.1
        for i, (yr, v) in enumerate(NIFTY):
            x = 34 + i * 93; tt = t0 + 0.14 * i; on = t >= tt
            glass_dark(c, x, 560, 84, 150, 16)
            if on:
                k = prog(t, tt, tt + 0.15); col = GREEN if v > 0 else RED
                c.set_source_rgba(*col, 0.9 * k); rrect(c, x, 560, 84, 150, 16); c.fill()
                mono(c, ('+' if v > 0 else '') + f'{v:.2f}%', x + 42, 635, 18, INK, a=k, kind='monob')
            mono(c, str(yr), x + 42, 740, 18, CREAM, a=0.8, kind='monob')
        if t >= A['nine'] - 0.15:
            big_num(c, '9 / 11 UP', W / 2, 920, 110, t, A['nine'] - 0.15)
    # 10 ritual, not forecast
    elif t < S('11') - 0.05:
        z = e_io(prog(t, A['tiny'] - 0.2, A['tiny'] + 0.8)); sc_ = 420 * (1 - z) + 52 * z      # px per 1 %
        cy = 760
        c.set_source_rgba(*CREAM, 0.5); c.set_line_width(2); c.move_to(90, cy); c.line_to(1000, cy); c.stroke()
        if z > 0.3:
            a_ = prog(z, 0.3, 0.8)
            for p_ in (5, -5):
                yy = cy - p_ * 52; c.set_source_rgba(*CREAM, 0.25 * a_); c.set_dash([10, 10]); c.move_to(150, yy); c.line_to(1000, yy); c.stroke(); c.set_dash([])
                mono(c, f'{p_:+d}%', 120, yy, 20, CREAM, a=0.7 * a_, kind='monob')
        for i, (yr, v) in enumerate(NIFTY):
            x = 175 + i * 75; hh = v * sc_; col = GREEN if v > 0 else RED
            c.set_source_rgba(*col, 0.95); c.rectangle(x, cy - max(hh, 0), 44, max(3, abs(hh))); c.fill()
        if z > 0.6: mono(c, 'EVERY MOVE UNDER 1%', W / 2, 1100, 28, CREAM, a=prog(z, 0.6, 1.0), kind='monob')
        if t >= A['ritual'] - 0.1: stamp_txt(c, 'RITUAL, NOT FORECAST', W / 2, 1220, t, A['ritual'] - 0.1, px=60, rot=-6, col=AMBER)
    # 11 normal settlement
    elif t < S('12') - 0.05:
        u = e_out(prog(t, S('11'), S('11') + 0.35))
        c.save(); c.translate(0, (1 - u) * 90)
        c.set_source_rgba(0.97, 0.96, 0.92, u); rrect(c, 190, 420, 700, 560, 24); c.fill()
        mono(c, 'CONTRACT NOTE', 540, 490, 34, INK, a=u, kind='monob')
        c.set_source_rgba(*INK, 0.3 * u); c.set_line_width(2); c.move_to(230, 530); c.line_to(850, 530); c.stroke()
        for j, (l, r) in enumerate((('TRADE DATE', '08 NOV 2026'), ('SESSION', 'MUHURAT'), ('BUY', '1 SHARE'))):
            mono(c, l, 240, 600 + j * 70, 24, INK, a=0.6 * u, anchor='l', kind='mono'); mono(c, r, 840, 600 + j * 70, 24, INK, a=u, anchor='r', kind='monob')
        c.restore()
        if t >= A['settle'] - 0.2:
            kk = e_back(prog(t, A['settle'] - 0.2, A['settle'] + 0.1))
            pill(c, 'NORMAL SETTLEMENT', W / 2 - 30, 900, 34, GREEN, s=kk)
            tick(c, W / 2 + 265, 900, 0.9, u=prog(t, A['settle'], A['settle'] + 0.3), col=GREEN)
    # 12 series slide
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('12') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        # one diya is lit in the exact spot it sits in frame 0, then the room fades in around it
        ks = e_io(prog(t, S('L') - 0.05, S('L') + 0.45)); k = e_io(prog(t, S('L') + 0.7, S('L') + 1.4))
        c.push_group(); slide(c, t, S('12') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - ks)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
        if k < 1:
            lit = e_out(prog(t, S('L') + 0.3, S('L') + 0.6))
            diya(c, *LOOPDIYA, 0.85, 0.0, a=(1 - k) * prog(t, S('L'), S('L') + 0.3), lit=lit)
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('12') - 0.05: tag(c)
    return s
