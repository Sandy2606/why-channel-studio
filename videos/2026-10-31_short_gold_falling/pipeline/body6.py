
# ---------------- extras ----------------
sys.path.insert(0, '/home/claude/why-channel-studio/pipeline/style_v2')
import cta_card as CTA
MID_T0 = A['buying'] + 0.6
END_T0 = A['sub'] - CTA.T_CLICK

def fmt_inr(v):
    s_ = str(int(round(v)))
    if len(s_) <= 3: return s_
    last = s_[-3:]; rest = s_[:-3]; parts = []
    while len(rest) > 2: parts.insert(0, rest[-2:]); rest = rest[:-2]
    if rest: parts.insert(0, rest)
    return ','.join(parts) + ',' + last

def arrow(c, x, y, s, up=True, col=AMBER, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s if up else -s)
    c.move_to(0, -40); c.line_to(30, -5); c.line_to(12, -5); c.line_to(12, 40); c.line_to(-12, 40); c.line_to(-12, -5); c.line_to(-30, -5); c.close_path()
    c.set_source_rgba(*col, a); c.fill(); c.restore()

def tagpill(c, txt_, y, t, t0, col=CREAM):
    if t >= t0: pill(c, txt_, W / 2, y, 34, col, s=e_back(prog(t, t0, t0 + 0.25)))

def chain_row(c, label, y, t, t0, up):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.3))
    c.save(); c.translate((1 - u) * 80, 0)
    glass_dark(c, 190, y - 60, 700, 120, 60, u)
    head(c, label, 260, y + 22, 62, CREAM, a=u, anchor='l', shadow=False)
    arrow(c, 800, y, 1.05, up=up, col=AMBER if up else CREAM, a=u)
    c.restore()

def down_link(c, y0, y1, t, t0):
    if t < t0: return
    u = e_io(prog(t, t0, t0 + 0.25)); c.set_source_rgba(*AMBER, 0.8); c.set_line_width(5); c.set_dash([4, 10])
    c.move_to(W / 2, y0); c.line_to(W / 2, y0 + (y1 - y0) * u); c.stroke(); c.set_dash([])

def stamp_txt(c, txt_, x, y, t, t0, px=96, rot=-10, col=CREAM):
    if t < t0: return
    u = prog(t, t0, t0 + 0.18); sc = 1.8 - 0.8 * e_out(u)
    c.save(); c.translate(x, y); c.rotate(math.radians(rot)); c.scale(sc, sc)
    font(c, 'head', px); e = c.text_extents(txt_); w, h = e.width + 60, px + 40
    c.set_source_rgba(*col, u); c.set_line_width(8); rrect(c, -w / 2, -h / 2, w, h, 16); c.stroke()
    c.move_to(-e.width / 2 - e.x_bearing, px * 0.36); c.show_text(txt_); c.restore()

def coin_card(c, x, y, w, h, title, sub, t, t0, glow=True, val=None):
    if t < t0: return
    u = e_out(prog(t, t0, t0 + 0.35))
    c.save(); c.translate(0, (1 - u) * 60); glass_dark(c, x, y, w, h, 36, u)
    mono(c, title, x + w / 2, y + 70, 30, AMBER if glow else CREAM, a=u, kind='monob')
    if val: head(c, val, x + w / 2, y + 190, 66, CREAM, a=u, shadow=False)
    mono(c, sub, x + w / 2, y + h - 50, 24, CREAM, a=0.8 * u, kind='mono')
    c.restore()

SL = {}
def slide(c, t, t0, scale=1.0):
    if LANGV not in SL:
        SL[LANGV] = [(surf_from_pil(Image.open(ROOT + f).convert('RGBA'))[0], cxy) for f, cxy in json.load(open(ROOT + f'slide_{LANGV}.json'))]
    c.save(); c.translate(W / 2, 40); c.scale(scale, scale); c.translate(-W / 2, -40)
    starts = [0.0, 0.25] + [0.6 + 0.15 * i for i in range(6)] + [1.7]
    for (sf, (cx, cy)), st in zip(SL[LANGV], starts):
        tt = t - (t0 + st)
        if tt < 0: continue
        u = e_back(prog(tt, 0, 0.35)); a = prog(tt, 0, 0.2)
        c.save(); c.translate(cx, cy + (1 - min(u, 1)) * 60); c.scale(0.85 + 0.15 * min(u, 1.03), 0.85 + 0.15 * min(u, 1.03)); c.translate(-cx, -cy)
        c.set_source_surface(sf, 0, 0); c.paint_with_alpha(a); c.restore()
    # glow dot travels to YOU'RE HERE (6/6 card)
    k = prog(t, t0 + 1.5, t0 + 2.3)
    if 0 < k:
        sx, sy = W / 2, 560; ex, ey = SL[LANGV][7][1]; ey += 190
        x = sx + (ex - sx) * e_io(k); y = sy + (ey - sy) * e_io(k) - math.sin(k * math.pi) * 120
        glowdot(c, x, y, 13 if k < 1 else 10 + 2 * math.sin(t * 6))
    c.restore()

def bubble(c, t, t0, y=1230):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3)); msg = 'Part 2 please!'
    n = int(clamp((t - t0 - 0.3) / 0.9) * len(msg))
    c.save(); c.translate(W / 2, y); c.scale(u, u)
    glass_dark(c, -330, -70, 660, 140, 40)
    c.set_source_rgba(*AMBER, 1); c.arc(-260, 0, 34, 0, 2 * math.pi); c.fill()
    font(c, 'head', 34); c.set_source_rgb(*INK); e = c.text_extents('?'); c.move_to(-260 - e.width / 2 - e.x_bearing, 13); c.show_text('?')
    font(c, 'monob', 34); c.set_source_rgb(*CREAM); c.move_to(-200, 12); c.show_text(msg[:n] + ('|' if int(t * 3) % 2 == 0 else ''))
    c.restore()

def qcard(c, label, y, t, t0, t1):
    if not (t0 <= t < t1): return
    u = e_out(prog(t, t0, t0 + 0.3)); v = 1 - prog(t, t1 - 0.2, t1)
    c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 90, y - 70, 900, 140, 40, u * v)
    c.set_source_rgba(*AMBER, u * v); c.arc(160, y, 40, 0, 2 * math.pi); c.fill()
    font(c, 'head', 52); c.set_source_rgba(*INK, u * v); e = c.text_extents('?'); c.move_to(160 - e.width / 2 - e.x_bearing, y + 19); c.show_text('?')
    mono(c, label, 230, y + 12, 30, CREAM, a=u * v, anchor='l', kind='monob'); c.restore()

# ---------------- frame ----------------
def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    # 1. peak -> now
    if t < A['thirty'] - 0.05:
        mono(c, 'GOLD · US$ PER OUNCE', W / 2, 250, 28, AMBER, kind='monob')
        X0, Y0, CW, CH = 130, 560, 820, 420
        glass_dark(c, X0 - 30, Y0 - 40, CW + 60, CH + 100, 30)
        def yv(v): return Y0 + CH - CH * (v - 3600) / (5800 - 3600)
        p0 = (X0 + 60, yv(5590)); p1 = (X0 + CW - 60, yv(3986))
        u = e_io(prog(t, 0.6, A['below'] + 0.2))
        c.set_source_rgba(1, 1, 1, 0.25); c.set_dash([6, 10]); c.set_line_width(2); c.move_to(X0, yv(4000)); c.line_to(X0 + CW, yv(4000)); c.stroke(); c.set_dash([])
        mono(c, '$4,000', X0 + CW - 10, yv(4000) - 14, 20, CREAM, a=0.6, anchor='r', kind='mono')
        if u > 0:
            c.set_source(agrad(p0[0], 0, p1[0], 0)); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.move_to(*p0); c.line_to(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u); c.stroke(); c.set_line_cap(cairo.LINE_CAP_BUTT)
            glowdot(c, p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u, 13)
        glowdot(c, *p0, 11); mono(c, 'JAN 28 · ALL-TIME HIGH', p0[0] - 10, p0[1] - 30, 22, AMBER, anchor='l', kind='monob')
        if t >= A['below'] - 0.1: mono(c, 'OCT 23', p1[0], p1[1] + 50, 22, CREAM, anchor='r', kind='monob')
        val = 5590 - (5590 - 3986) * u
        big_num(c, f'${int(round(val)):,}', W / 2, 400, 170, t, -0.3)
        draw_clip(c, 'mcath', W / 2, 1180, 1000, t, 1.0, rot=-1.0, hl_t0=1.4, hl_dur=1.2)
        if t >= 1.2: source_tag(c, 'METALCHARTS · GOLD ALL-TIME HIGH', 90, 1290, a=prog(t, 1.2, 1.5))
    # 2. -29% + Seoul Economic Daily
    elif t < A['r1'] - 0.05:
        big_num(c, '−29%', W / 2, 400, 230, t, A['thirty'] - 0.05)
        mono(c, 'FROM THE JANUARY HIGH', W / 2, 560, 28, CREAM, a=prog(t, A['thirty'] + 0.2, A['thirty'] + 0.5), kind='monob')
        draw_clip(c, 'sed', W / 2, 870, 1000, t, A['thirty'] + 0.1, rot=1.0, hl_t0=A['thirty'] + 0.5, hl_dur=1.4)
        if t >= A['thirty'] + 0.3: source_tag(c, 'SEOUL ECONOMIC DAILY · OCT 24, 2026', 90, 1110, a=prog(t, A['thirty'] + 0.3, A['thirty'] + 0.6))
        if t >= A['safest'] - 0.1: pill(c, 'THE "SAFEST" THING?', W / 2, 1250, 44, AMBER, s=e_back(prog(t, A['safest'] - 0.1, A['safest'] + 0.2)))
    # 3. reason one: gold pays nothing
    elif t < A['rates'] - 0.05:
        tagpill(c, 'REASON 1', 250, t, A['r1'] - 0.05, AMBER)
        k = prog(t, A['fd'], A['fd'] + 1.6)
        coin_card(c, 100, 420, 420, 520, 'BANK FD', 'PAYS YOU INTEREST', t, A['fd'] - 0.1, glow=True, val='₹' + fmt_inr(10000 + 700 * k))
        if t >= A['fd'] + 0.2: arrow(c, 310, 760, 0.8, up=True, col=AMBER, a=prog(t, A['fd'] + 0.2, A['fd'] + 0.4))
        coin_card(c, 560, 420, 420, 520, 'GOLD', 'PAYS YOU ₹0', t, A['r1'] + 0.4, glow=False)
        if t >= A['r1'] + 0.4:
            dim = 1 - 0.6 * prog(t, A['sits'], A['sits'] + 0.5)
            R3.gold_bar(c, 770, 650, 0.42, glow=0.6 * dim, a=prog(t, A['r1'] + 0.4, A['r1'] + 0.7))
        if t >= A['sits']: mono(c, '…IT JUST SITS THERE', 770, 1010, 24, CREAM, a=prog(t, A['sits'], A['sits'] + 0.3), kind='monob')
    # 4. rates up -> Yahoo clipping
    elif t < A['r2'] - 0.05:
        u = e_back(prog(t, A['rates'] - 0.05, A['rates'] + 0.3))
        arrow(c, 220, 380, 1.6 * max(0.01, u), up=True, col=AMBER)
        head(c, 'INTEREST', 330, 360, 70, CREAM, a=prog(t, A['rates'] - 0.05, A['rates'] + 0.2), anchor='l', shadow=False)
        head(c, 'RATES UP', 330, 440, 70, AMBER, a=prog(t, A['rates'] - 0.05, A['rates'] + 0.2), anchor='l', shadow=False)
        mono(c, '= GOLD LOOKS LESS ATTRACTIVE', W / 2, 560, 26, CREAM, a=prog(t, A['rates'] + 0.8, A['rates'] + 1.1), kind='monob')
        draw_clip(c, 'yah', W / 2, 950, 1000, t, A['fed'] - 0.4, rot=-1.0, hl_t0=A['y2023'] - 0.8, hl_dur=1.3)
        if t >= A['fed'] - 0.2: source_tag(c, 'YAHOO FINANCE · OCT 27, 2026', 90, 1250, a=prog(t, A['fed'] - 0.2, A['fed'] + 0.1))
    # 5. oil -> prices -> rates -> gold
    elif t < A['r3'] - 0.05:
        full_photo(c, 'ph/oil_g.jpg', t, A['r2'], A['r3'], z=(1.05, 1.15), focus=(0.5, 0.55), dim=0.62, label='Zbynek Burival · Unsplash')
        tagpill(c, 'REASON 2', 250, t, A['r2'] - 0.05, AMBER)
        chain_row(c, 'OIL', 470, t, A['oil'] - 0.1, True)
        down_link(c, 535, 595, t, A['oil'] + 0.6)
        chain_row(c, 'PRICES', 660, t, A['hikes'] - 1.8, True)
        down_link(c, 725, 785, t, A['hikes'] - 1.2)
        chain_row(c, 'RATES', 850, t, A['hikes'] - 0.7, True)
        down_link(c, 915, 975, t, A['hikes'] - 0.1)
        chain_row(c, 'GOLD', 1040, t, A['hikes'] + 0.2, False)
        if t >= A['oil'] + 0.2: mono(c, 'US–IRAN TENSION', W / 2, 345, 24, CREAM, a=0.8 * prog(t, A['oil'] + 0.2, A['oil'] + 0.5), kind='monob')
    # 6. reason three: cash scramble
    elif t < A['nobody'] - 0.05:
        full_photo(c, 'ph/stocks.jpg', t, A['r3'], A['nobody'], z=(1.05, 1.15), focus=(0.5, 0.45), dim=0.7, label='Jakub Żerdzicki · Unsplash')
        tagpill(c, 'REASON 3', 250, t, A['r3'] - 0.05, AMBER)
        if t >= A['r3'] + 0.4: pill(c, 'STOCKS FALL → NEED CASH', W / 2, 360, 32, CREAM, s=e_back(prog(t, A['r3'] + 0.4, A['r3'] + 0.7)))
        if t >= A['easiest'] - 0.2:
            R3.gold_bar(c, W / 2, 620, 0.7, glow=0.8, a=prog(t, A['easiest'] - 0.2, A['easiest'] + 0.1))
            stamp_txt(c, 'SOLD', W / 2 + 40, 600, t, A['sold'], px=110)
        draw_clip(c, 'sedm', W / 2, 960, 1000, t, A['cash'] - 0.2, rot=1.2, hl_t0=A['cash'] + 0.2, hl_dur=1.6)
        if t >= A['rushed'] - 0.2:
            u = e_out(prog(t, A['rushed'] - 0.2, A['rushed'] + 0.3)); v = e_io(prog(t, A['out'] - 0.3, A['out'] + 0.3))
            glass_dark(c, 140, 1130, 800, 170, 40, u)
            mono(c, 'FAST MONEY', W / 2, 1185, 30, AMBER, a=u, kind='monob')
            head(c, 'IN  →  OUT' if v > 0.5 else 'JANUARY: IN', W / 2, 1262, 56, CREAM, a=u, shadow=False)
    # 7. central banks bought 63 t; traders sell / banks buy
    elif t < A['y2011'] - 0.05:
        if t < A['traders'] - 0.1:
            draw_clip(c, 'bt63', W / 2, 640, 860, t, A['nobody'], rot=-1.2, hl_t0=A['t63'] - 0.2, hl_dur=1.8)
            if t >= A['nobody'] + 0.2: source_tag(c, 'BUSINESS TODAY · OCT 16, 2026 (WGC DATA)', 90, 330, a=prog(t, A['nobody'] + 0.2, A['nobody'] + 0.5))
            big_num(c, '63 TONNES', W / 2, 1050, 120, t, A['t63'])
            if t >= A['most']: mono(c, 'MOST IN ALMOST TWO YEARS', W / 2, 1180, 28, CREAM, a=prog(t, A['most'], A['most'] + 0.3), kind='monob')
        else:
            for j, (lab, sub, up, t0, col) in enumerate((('TRADERS', 'SELLING', False, A['traders'] - 0.1, CREAM), ('CENTRAL BANKS', 'BUYING', True, A['buying'] - 0.2, AMBER))):
                if t < t0: continue
                u = e_out(prog(t, t0, t0 + 0.35)); x = 90 + j * 470
                c.save(); c.translate(0, (1 - u) * 60); glass_dark(c, x, 420, 430, 600, 40, u)
                mono(c, lab, x + 215, 500, 30, col, a=u, kind='monob')
                arrow(c, x + 215, 720, 2.0, up=up, col=col, a=u)
                head(c, sub, x + 215, 950, 58, col, a=u, shadow=False); c.restore()
    # 8. 2011 record took 9 years; still 17x
    elif t < A['updown'] - 0.05:
        draw_clip(c, 'mctab', W / 2, 520, 1000, t, A['y2011'] - 0.1, rot=-0.8, hl_t0=A['y2011'] + 0.1, hl_dur=max(1.0, A['y2020'] - A['y2011']))
        if t >= A['y2011']: source_tag(c, 'METALCHARTS · EVERY GOLD ALL-TIME HIGH', 90, 330, a=prog(t, A['y2011'], A['y2011'] + 0.3))
        big_num(c, '9 YEARS', W / 2, 820, 150, t, A['nine'])
        if t >= A['nine'] + 0.3: mono(c, '2011 RECORD → BEATEN ONLY IN 2020', W / 2, 950, 26, CREAM, a=prog(t, A['nine'] + 0.3, A['nine'] + 0.6), kind='monob')
        if t >= A['x17'] - 0.6:
            u = e_back(prog(t, A['x17'] - 0.6, A['x17'] - 0.3))
            pill(c, '₹8,400 → ₹1,42,300 · ~17×', W / 2, 1110, 40, AMBER, s=u)
            mono(c, '24K /10 G · 2006 → OCT 28, 2026 (ADITYA BIRLA CAPITAL · CLEARTAX)', W / 2, 1200, 17, CREAM, a=0.7 * prog(t, A['x17'] - 0.3, A['x17']), kind='mono')
    # 9. years, not weeks
    elif t < A['secrets'] - 0.05:
        u = e_out(prog(t, A['updown'] - 0.1, A['updown'] + 0.3))
        c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 90, 360, 900, 230, 34, u)
        c.set_source_rgba(*AMBER, u); c.rectangle(112, 385, 6, 180); c.fill()
        head(c, 'GOLD GOES UP', 150, 450, 60, CREAM, a=u, anchor='l', shadow=False)
        head(c, 'AND DOWN.', 150, 535, 60, CREAM, a=u, anchor='l', shadow=False); c.restore()
        if t >= A['years'] - 0.9:
            big_num(c, 'YEARS,', W / 2, 760, 150, t, A['years'] - 0.9)
            if t >= A['years'] - 0.3: head(c, 'NOT WEEKS', W / 2, 900, 80, CREAM, a=prog(t, A['years'] - 0.3, A['years']), shadow=False)
        qmark(c, t, W / 2, 1180, 240, morph=e_io(prog(t, A['years'], A['years'] + 0.5)))
    # 10. open questions
    elif t < A['wrap'] - 0.05:
        if t >= A['secrets'] - 0.05: pill(c, 'GOLD STILL HAS SECRETS', W / 2, 250, 40, AMBER, s=e_back(prog(t, A['secrets'] - 0.05, A['secrets'] + 0.25)))
        if t < A['q2'] - 0.05:
            print_photo(c, 'ph/medal.jpg', W / 2, 640, 420, t, A['q1'] - 0.2, rot=-3)
            qcard(c, 'OLYMPIC GOLD = MOSTLY SILVER?', 1110, t, A['q1'] + 0.2, A['q2'] - 0.05)
        elif t < A['q3'] - 0.05:
            draw_clip(c, 'andhra', W / 2, 620, 1000, t, A['q2'] - 0.05, rot=1.0, hl_t0=A['q2'] + 0.3, hl_dur=0.8)
            if t >= A['q2'] + 0.1: source_tag(c, 'BUSINESS TODAY · APR 19, 2026', 90, 760, a=prog(t, A['q2'] + 0.1, A['q2'] + 0.4))
            qcard(c, 'SO WHY DOES INDIA STILL IMPORT?', 1110, t, A['q2'] + 0.8, A['q3'] - 0.05)
        elif t < A['another'] - 0.05:
            print_photo(c, 'ph/cern_lhc.jpg', W / 2, 560, 640, t, A['q3'] - 0.2, rot=2, caption='CERN · LHC')
            draw_clip(c, 'cern', W / 2, 930, 920, t, A['q3'] + 0.5, rot=-1.0, hl_t0=A['q3'] + 0.9, hl_dur=1.0)
            if t >= A['q3'] + 0.7: source_tag(c, 'CERN · 08 MAY 2025', 90, 1080, a=prog(t, A['q3'] + 0.7, A['q3'] + 1.0))
            qcard(c, "SO WHY CAN'T WE MAKE MORE?", 1190, t, A['q3'] + 1.6, A['another'] - 0.05)
        else:
            u = e_out(prog(t, A['another'] - 0.05, A['another'] + 0.3))
            c.save(); c.translate(0, (1 - u) * 40); glass_dark(c, 90, 500, 900, 260, 34, u)
            c.set_source_rgba(*AMBER, u); c.rectangle(112, 525, 6, 210); c.fill()
            head(c, "THAT'S A WHY", 150, 600, 62, CREAM, a=u, anchor='l', shadow=False)
            head(c, 'FOR ANOTHER DAY', 150, 690, 62, AMBER, a=u, anchor='l', shadow=False); c.restore()
            bubble(c, t, A['comment'] - 0.2, y=1000)
            if t >= A['comment'] + 0.2: mono(c, 'COMMENT BELOW', W / 2, 1120, 28, AMBER, a=prog(t, A['comment'] + 0.2, A['comment'] + 0.5), kind='monob')
    # 11. series slide + end CTA
    else:
        caps = False
        sc = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, A['wrap'] - 0.05, scale=sc)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    # mid-video CTA (smaller)
    if MID_T0 <= t < MID_T0 + 3.2:
        c.save(); c.translate(W / 2, 1255); c.scale(0.85, 0.85); c.translate(-W / 2, -1255)
        CTA.draw(c, t, MID_T0, PLAT, LANGV, y=1255, t_out=MID_T0 + 2.9); c.restore()
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if caps: tag(c)
    return s

def main(part=0, parts=1, out=None, still=None):
    if still is not None:
        os.makedirs(ROOT + 'stills', exist_ok=True)
        for tt in still: frame(tt).write_to_png(f'{ROOT}stills/{LANGV}_{PLAT}_{tt:05.2f}.png')
        return
    n = int(DUR * FPS); a = n * part // parts; b = n * (part + 1) // parts
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    for i in range(a, b):
        s = frame(i / FPS); s.flush(); p.stdin.write(bytes(s.get_data()))
    p.stdin.close(); p.wait()

if __name__ == '__main__':
    if sys.argv[1] == 'still': main(still=[float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == 'anchors': print({k: round(v, 2) for k, v in A.items()})
    else: main(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
