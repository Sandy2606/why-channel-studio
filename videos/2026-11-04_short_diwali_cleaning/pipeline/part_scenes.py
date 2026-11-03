
# ---------------- anchors ----------------
A = {
    'cupboards': AT('1', 'Cupboards', 'బీరువాలు'), 'fans': AT('1', 'Fans', 'Fans'), 'walls': AT('1', 'Walls', 'గోడలకి'), 'why1': AT('1', 'Why', 'ఎందుకు'),
    'lakshmi': AT('2', 'Lakshmi', 'లక్ష్మీదేవి'), 'timing2': AT('2', 'timing', 'timing'),
    'oct15': AT('3', 'October', 'October'), 'nov8': AT('3', 'November', 'November'),
    'damp': AT('4', 'Damp', 'తడి', n=2 if LANGV == 'en' else 1), 'black': AT('4', 'Black', 'నల్ల'), 'smell': AT('4', 'smell', 'వాసన'),
    'epa': AT('5', 'EPA', 'EPA'), 'sixty': AT('5', '60', '60'), 'hard': AT('5', 'hard', 'కష్టం'),
    'clean6': AT('6', 'clean', 'శుభ్రం'),
    'lime7': AT('7', 'Lime', 'సున్నం'),
    'ph': AT('8', '12.4', '12.4'), 'germs8': AT('8', 'germs', 'క్రిములను'),
    'white9': AT('9', 'white', 'తెలుపు'), 'while9': AT('9', 'while', 'కాలం'),
    'co2': AT('10', 'carbon', 'carbon'), 'caco3': AT('10', 'calcium', 'calcium'), 'limestone': AT('10', 'limestone', 'సున్నపురాయిలో'),
    'practical': AT('11', 'practical', 'practical'),
    'tomorrow': S('12'), 'loop': S('L'),
}
A['end'] = DUR
"""HELPERS"""
# ---------------- 3/6 drawings ----------------
WALL = (0.80, 0.74, 0.62); FLOOR = (0.30, 0.24, 0.20)
def room(c, t, chaos=1.0, painted=0.5, a=1.0):
    """drawn living room, wall area y 260..1180"""
    c.save(); c.push_group()
    c.set_source_rgb(*WALL); c.rectangle(60, 260, 960, 820); c.fill()
    c.set_source_rgb(0.92, 0.90, 0.84); c.rectangle(60, 260, 960 * painted, 820); c.fill()           # fresh paint part
    c.set_source_rgb(*FLOOR); c.rectangle(60, 1080, 960, 100); c.fill()
    # cupboard (left)
    c.set_source_rgb(0.45, 0.30, 0.20); c.rectangle(110, 560, 260, 520); c.fill()
    if chaos > 0:
        c.save(); c.translate(110, 560); c.rotate(-0.6 * chaos); c.set_source_rgb(0.55, 0.37, 0.24); c.rectangle(-120, 0, 120, 520); c.fill(); c.restore()
        for i, col in enumerate(((0.9, 0.4, 0.4), (0.4, 0.6, 0.9), (0.95, 0.8, 0.3), (0.5, 0.8, 0.5))):
            c.set_source_rgba(*col, chaos); rrect(c, 140 + i * 50, 1000 - (i % 2) * 30, 120, 60, 18); c.fill()
    # ceiling fan + stepladder (middle)
    c.set_source_rgb(0.25, 0.25, 0.28); c.rectangle(535, 260, 10, 80); c.fill()
    for k in range(3):
        an = k * 2 * math.pi / 3 + (0 if chaos > 0 else t * 4)
        c.save(); c.translate(540, 345); c.rotate(an); c.set_source_rgb(0.55, 0.55, 0.58); rrect(c, 10, -14, 150, 28, 12); c.fill(); c.restore()
    if chaos > 0:
        c.set_source_rgba(0.75, 0.6, 0.3, chaos); c.set_line_width(12)
        c.move_to(470, 1080); c.line_to(520, 640); c.move_to(610, 1080); c.line_to(560, 640); c.stroke()
        for y in range(700, 1080, 90): c.move_to(500 - (y - 700) * 0.0, y); c.line_to(580, y)
        c.stroke()
    # paint roller on the wall (right)
    if chaos > 0:
        rx = 60 + 960 * painted
        c.set_source_rgba(0.3, 0.3, 0.32, chaos); c.set_line_width(10); c.move_to(rx + 30, 760); c.line_to(rx + 30, 980); c.stroke()
        rrect(c, rx, 700, 70, 70, 14); c.set_source_rgba(0.95, 0.93, 0.88, chaos); c.fill()
    # broom leaning (right corner) — same spot as the loop line
    broom(c, 900, 1080, 1.0, a=1.0)
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
def broom(c, x, y, s, a=1.0, ang=-0.18):
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    c.set_source_rgba(0.55, 0.38, 0.22, a); c.rectangle(-6, -560, 12, 460); c.fill()
    c.set_source_rgba(0.82, 0.68, 0.36, a)
    c.move_to(-14, -110); c.line_to(14, -110); c.line_to(60, 0); c.line_to(-60, 0); c.close_path(); c.fill()
    c.set_source_rgba(0.6, 0.45, 0.2, a); c.set_line_width(3)
    for k in range(-50, 60, 12): c.move_to(k * 0.25, -105); c.line_to(k, 0)
    c.stroke(); c.restore()
def diya(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    fl = 0.8 + 0.2 * math.sin(t * 9 + x)
    g = cairo.RadialGradient(0, -30, 0, 0, -30, 70); g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.5 * a * fl); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0); c.set_source(g); c.arc(0, -30, 70, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0.78, 0.40, 0.18, a); c.move_to(-40, 0); c.curve_to(-30, 30, 30, 30, 40, 0); c.close_path(); c.fill()
    c.set_source_rgba(1.0, 0.75, 0.25, a); c.move_to(0, -10); c.curve_to(-10, -25, -4, -40, 0, -55 * fl); c.curve_to(4, -40, 10, -25, 0, -10); c.fill()
    c.restore()
CHAIN = ['MONSOON', 'MOISTURE', 'MOULD', 'DRY', 'LIME']
def chain(c, t, active, a=1.0):
    """subdued chain across the top; current word glows amber"""
    if a <= 0: return
    xs = [130, 330, 540, 730, 920]
    for i, (w_, x) in enumerate(zip(CHAIN, xs)):
        on = i == active; past = i < active
        if on: pill(c, w_, x, 215, 24, AMBER, a=a)
        else: mono(c, w_, x, 215, 20, AMBER if past else CREAM, a=a * (0.75 if past else 0.35), kind='monob')
        if i < 4: mono(c, '→', (x + xs[i + 1]) / 2 + 8, 215, 20, CREAM, a=0.35 * a, kind='monob')
def germ(c, x, y, r, a=1.0, kind=0):
    if a <= 0.01: return
    c.save(); c.translate(x, y)
    col = (0.45, 0.75, 0.40) if kind == 0 else (0.70, 0.45, 0.85)
    c.set_source_rgba(*col, a); c.set_line_width(4)
    for k in range(8):
        an = k * math.pi / 4; c.move_to(math.cos(an) * r, math.sin(an) * r); c.line_to(math.cos(an) * r * 1.4, math.sin(an) * r * 1.4)
    c.stroke(); c.arc(0, 0, r, 0, 2 * math.pi); c.fill()
    c.set_source_rgba(0, 0, 0, 0.4 * a); c.arc(-r * 0.3, -r * 0.2, r * 0.18, 0, 2 * math.pi); c.fill(); c.arc(r * 0.3, -r * 0.2, r * 0.18, 0, 2 * math.pi); c.fill()
    c.restore()
def meter(c, cx, cy, val, a=1.0):
    """semicircle humidity meter, val 0..1 (0.6 = the EPA line)"""
    c.save(); c.translate(cx, cy)
    for k in range(60):
        f0, f1 = k / 60, (k + 1) / 60; col = (0.35, 0.8, 0.45) if f0 < 0.6 else (0.95, 0.55, 0.2)
        c.set_source_rgba(*col, a); c.set_line_width(36); c.new_path(); c.arc(0, 0, 260, math.pi + f0 * math.pi, math.pi + f1 * math.pi + 0.005); c.stroke()
    an = math.pi + val * math.pi
    c.set_source_rgba(*CREAM, a); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); c.move_to(0, 0); c.line_to(math.cos(an) * 230, math.sin(an) * 230); c.stroke()
    c.arc(0, 0, 18, 0, 2 * math.pi); c.fill()
    an6 = math.pi + 0.6 * math.pi; c.set_source_rgba(*CREAM, a); c.set_line_width(4); c.move_to(math.cos(an6) * 200, math.sin(an6) * 200); c.line_to(math.cos(an6) * 300, math.sin(an6) * 300); c.stroke()
    mono(c, '60%', math.cos(an6) * 335, math.sin(an6) * 335, 26, CREAM, a=a, kind='monob')
    c.restore()

def chem(c, x, y, px):
    """Ca(OH)2 -> CaCO3 with real subscripts"""
    parts = [('Ca(OH)', 0), ('2', 1), ('CaCO', 0), ('3', 1)]
    font(c, 'head', px); tot = 0
    for txt_, sub in parts: font(c, 'head', px * (0.6 if sub else 1)); tot += c.text_extents(txt_).x_advance
    tot += px * 1.75; xx = x - tot / 2
    for i, (txt_, sub) in enumerate(parts):
        font(c, 'head', px * (0.6 if sub else 1)); c.move_to(xx, y + px * 0.35 + (px * 0.18 if sub else 0)); c.set_source_rgb(*AMBER); c.show_text(txt_); xx += c.text_extents(txt_).x_advance
        if i == 1:
            xx += px * 0.4; c.set_line_width(6); c.move_to(xx, y); c.line_to(xx + px * 0.75, y); c.stroke()
            c.move_to(xx + px * 0.85, y); c.line_to(xx + px * 0.55, y - px * 0.22); c.line_to(xx + px * 0.55, y + px * 0.22); c.close_path(); c.fill(); xx += px * 1.25
def sc_hook(c, t, frozen=False):
    tt = 0.0 if frozen else t
    chaos = 1.0
    room(c, tt, chaos=chaos, painted=0.45)
    mono(c, 'DIWALI CLEANING', W / 2, 1230, 30, CREAM, kind='monob')
    head(c, 'WHY RIGHT NOW?', W / 2, 1320, 84, AMBER)
    if not frozen:
        for i, (lab, key, x, y) in enumerate((('CUPBOARDS OUT', 'cupboards', 240, 480), ('FANS DOWN', 'fans', 540, 470), ('WALLS PAINTED', 'walls', 830, 600))):
            if t >= A[key] - 0.1: pill(c, lab, x, y, 26, AMBER, s=e_back(prog(t, A[key] - 0.1, A[key] + 0.15)))

def frame(t):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
    board_bg(c, t)
    caps = True
    if t < S('2') - 0.05:
        sc_hook(c, t)
    # 2 belief + timing
    elif t < S('3') - 0.05:
        c.set_source_rgb(0.35, 0.18, 0.12); c.rectangle(300, 330, 480, 700); c.fill()            # doorway
        c.set_source_rgb(0.08, 0.06, 0.06); c.rectangle(340, 370, 400, 660); c.fill()
        for i in range(5): diya(c, 260 + i * 140, 1110, 0.8, t, a=prog(t, S('2') + 0.1 * i, S('2') + 0.3 + 0.1 * i))
        for r_, col in ((150, (0.95, 0.3, 0.35)), (110, AMBER), (70, (0.3, 0.7, 0.9)), (30, CREAM)):     # rangoli
            c.set_source_rgba(*col, 0.85); c.save(); c.translate(W / 2, 1180); c.scale(1, 0.35); c.arc(0, 0, r_, 0, 2 * math.pi); c.restore(); c.fill()
        for j, (lab, t0) in enumerate((('BELIEF', A['lakshmi'] - 0.2), ('TIMING', A['timing2'] - 0.2))):
            if t < t0: continue
            u = e_back(prog(t, t0, t0 + 0.3)); x = 290 + j * 500
            c.save(); c.translate(x, 520); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -200, -70, 400, 140, 30)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(4); rrect(c, -200, -70, 400, 140, 30); c.stroke()
            head(c, lab, 0, 0, 60, AMBER, shadow=False); c.restore()
    # 3 calendar + IMD
    elif t < S('4') - 0.05:
        chain(c, t, 0)
        u = e_out(prog(t, S('3'), S('3') + 0.4))
        for j, (lab, sub, t0) in enumerate((('OCT 15', 'MONSOON GONE', A['oct15'] - 0.2), ('NOV 8', 'DIWALI', A['nov8'] - 0.2))):
            if t < t0: continue
            k = e_out(prog(t, t0, t0 + 0.3)); x = 110 + j * 560
            glass_dark(c, x, 330, 300, 230, 30, k); c.set_source_rgba(*AMBER, k); c.rectangle(x, 330, 300, 56); c.fill()
            mono(c, sub, x + 150, 358, 20, INK, a=k, kind='monob'); head(c, lab, x + 150, 470, 66, CREAM, a=k, shadow=False)
        if t >= A['nov8']:
            k = prog(t, A['nov8'], A['nov8'] + 0.8); n = int(round(24 * e_out(k)))
            c.set_source_rgba(*AMBER, 0.9); c.set_line_width(6); c.set_dash([12, 10]); c.move_to(420, 445); c.line_to(420 + 250 * k, 445); c.stroke(); c.set_dash([])
            big_num(c, str(n), W / 2 - 90, 650, 110, t, A['nov8']); head(c, 'DAYS', W / 2 + 90, 655, 70, AMBER, a=prog(t, A['nov8'], A['nov8'] + 0.3))
        t1 = A['oct15'] + 0.2
        draw_clip(c, 'imd', 644, 900, 1250, t, t1, rot=-0.8, hl_t0=t1 + 0.4, hl_dur=1.1)
        source_tag(c, 'IMD PRESS RELEASE · 15 OCT 2026', 90, 1010, a=prog(t, t1 + 0.2, t1 + 0.5))
    # 4 damp walls
    elif t < A['damp'] - 0.4:
        # "across much of India": the same IMD release, highlight shifts to the south (NE monsoon)
        chain(c, t, 1)
        draw_clip(c, 'imd2', 515, 700, 1250, t, S('4') - 0.3, rot=0.6, hl_t0=S('4') + 0.1, hl_dur=1.3)
        source_tag(c, 'IMD PRESS RELEASE · 15 OCT 2026', 90, 810, a=1.0)
        pill(c, 'SOUTH INDIA DIFFERS · NE MONSOON OCT–DEC', W / 2, 960, 26, AMBER, s=e_back(prog(t, S('4') + 0.6, S('4') + 0.9)))
    elif t < S('5') - 0.05:
        chain(c, t, 1)
        c.set_source_rgb(*WALL); c.rectangle(90, 300, 900, 900); c.fill()
        k = prog(t, A['damp'] - 0.3, A['damp'] + 1.2)
        for i in range(5):
            g = cairo.RadialGradient(200 + i * 170, 420 + (i % 2) * 300, 0, 200 + i * 170, 420 + (i % 2) * 300, 180 * k)
            g.add_color_stop_rgba(0, 0.45, 0.42, 0.35, 0.6 * k); g.add_color_stop_rgba(1, 0.45, 0.42, 0.35, 0); c.set_source(g); c.paint()
        rng = np.random.default_rng(5)
        for i in range(60):
            x, y = 110 + rng.uniform(0, 300), 320 + rng.uniform(0, 400); k2 = clamp((t - A['black'] + 0.3) * 30 - i)
            if k2 > 0: c.set_source_rgba(0.08, 0.08, 0.06, 0.85 * min(1, k2)); c.arc(x, y, rng.uniform(4, 16), 0, 2 * math.pi); c.fill()
        if t >= A['smell'] - 0.3:        # cupboard + smell lines
            kk = prog(t, A['smell'] - 0.3, A['smell'])
            c.set_source_rgba(0.45, 0.30, 0.20, kk); c.rectangle(640, 700, 300, 480); c.fill()
            c.set_source_rgba(0.55, 0.65, 0.35, kk); c.set_line_width(7)
            for j in range(3):
                x0 = 720 + j * 70; c.move_to(x0, 680)
                for yy in range(680, 480, -20): c.line_to(x0 + 14 * math.sin(yy / 18 + t * 4), yy)
                c.stroke()
        cur = None
        for lab, key in (('DAMP WALLS', 'damp'), ('BLACK SPOTS', 'black'), ('THAT SMELL', 'smell')):
            if t >= A[key] - 0.1: cur = (lab, key)
        if cur: pill(c, cur[0], W / 2, 1270, 34, AMBER, s=e_back(prog(t, A[cur[1]] - 0.1, A[cur[1]] + 0.2)))
    # 5 humidity meter + EPA
    elif t < S('6') - 0.05:
        chain(c, t, 2)
        v = 0.25 + 0.6 * e_io(prog(t, S('5'), A['sixty']))
        meter(c, W / 2, 700, v)
        mono(c, 'INDOOR HUMIDITY', W / 2, 760, 26, CREAM, kind='monob')
        if v > 0.65: pill(c, 'MOULD ZONE', W / 2, 340, 30, AMBER)
        ct0 = min(A['epa'], A['sixty']) - 0.4
        draw_clip(c, 'epa', W / 2, 1000, 900, t, ct0, rot=0.8, hl_t0=max(A['sixty'] - 0.3, ct0 + 0.5), hl_dur=1.3)
        source_tag(c, 'US EPA · MOLD COURSE', 90, 1250, a=prog(t, ct0 + 0.2, ct0 + 0.5))
    # 6 dry weeks
    elif t < S('7') - 0.05:
        chain(c, t, 3)
        k = e_io(prog(t, S('6'), S('6') + 1.6))
        g = cairo.RadialGradient(W / 2, 300, 0, W / 2, 300, 700); g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.45 * k); g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0); c.set_source(g); c.paint()
        c.set_source_rgba(0.55, 0.75, 0.95, 0.35 + 0.4 * k); c.rectangle(340, 300, 400, 300); c.fill()
        c.set_source_rgba(0.45, 0.30, 0.20, 1); c.set_line_width(14); c.rectangle(340, 300, 400, 300); c.stroke(); c.move_to(540, 300); c.line_to(540, 600); c.stroke()
        c.set_source_rgba(1, 0.9, 0.5, k); c.arc(640, 380, 50, 0, 2 * math.pi); c.fill()
        meter(c, W / 2, 1000, 0.85 - 0.55 * k)
        if k > 0.6: pill(c, 'DRY', W / 2, 1110, 40, AMBER, s=e_back(prog(t, S('6') + 1.0, S('6') + 1.3)))
        if t >= A['clean6'] - 0.2: mono(c, 'CLEAN · DRY · PAINT', W / 2, 1220, 34, CREAM, a=prog(t, A['clean6'] - 0.2, A['clean6'] + 0.2), kind='monob')
    # 7 lime
    elif t < S('8') - 0.05:
        chain(c, t, 4)
        c.set_source_rgb(0.55, 0.42, 0.30); c.move_to(160, 560); c.line_to(540, 360); c.line_to(920, 560); c.close_path(); c.fill()   # roof
        k = prog(t, A['lime7'] - 0.3, A['lime7'] + 0.6)
        c.set_source_rgb(0.62, 0.55, 0.45); c.rectangle(220, 560, 640, 460); c.fill()
        c.set_source_rgba(0.97, 0.96, 0.92, 1); c.rectangle(220, 560, 640 * k, 460); c.fill()
        c.set_source_rgb(0.35, 0.22, 0.14); c.rectangle(480, 760, 120, 260); c.fill()
        c.set_source_rgb(0.5, 0.5, 0.55); c.move_to(200, 1060); c.line_to(320, 1060); c.line_to(300, 1180); c.line_to(220, 1180); c.close_path(); c.fill()  # bucket
        c.set_source_rgb(0.97, 0.96, 0.92); c.save(); c.translate(260, 1065); c.scale(1, 0.25); c.arc(0, 0, 58, 0, 2 * math.pi); c.restore(); c.fill()
        if t >= A['lime7'] - 0.1: head(c, 'LIME · SUNNAM', W / 2, 1270, 60, AMBER, a=prog(t, A['lime7'] - 0.1, A['lime7'] + 0.2))
    # 8 pH
    elif t < S('9') - 0.05:
        chain(c, t, 4)
        x0, x1, y = 120, 960, 420
        for i in range(15):
            f = i / 14; col = (0.95 - 0.5 * f, 0.35 + 0.4 * (1 - abs(f - 0.5) * 2), 0.3 + 0.6 * f)
            c.set_source_rgba(*col, 1); c.rectangle(x0 + (x1 - x0) * i / 15, y, (x1 - x0) / 15 + 1, 70); c.fill()
            mono(c, str(i), x0 + (x1 - x0) * (i + 0.5) / 15, y + 105, 18, CREAM, a=0.8, kind='mono')
        mono(c, 'ACID', x0, y - 30, 20, CREAM, anchor='l', kind='monob'); mono(c, 'NEUTRAL', (x0 + x1) / 2, y - 30, 20, CREAM, kind='monob'); mono(c, 'ALKALINE', x1, y - 30, 20, CREAM, anchor='r', kind='monob')
        k = e_io(prog(t, S('8'), A['ph'])); px = x0 + (x1 - x0) * (7 + 5.4 * k) / 15
        c.set_source_rgba(*AMBER, 1); c.move_to(px, y - 8); c.line_to(px - 18, y - 40); c.line_to(px + 18, y - 40); c.close_path(); c.fill()
        if t >= A['ph'] - 0.1:
            big_num(c, 'pH 12.4', W / 2, 660, 120, t, A['ph'] - 0.1)
            mono(c, 'STRONGLY ALKALINE', W / 2, 760, 28, AMBER, a=prog(t, A['ph'], A['ph'] + 0.3), kind='monob')
        rng = np.random.default_rng(9)
        for i in range(8):
            gx, gy = 150 + i * 110, 870 + (i % 2) * 70; tf = A['germs8'] - 0.2 + 0.15 * i
            al = 1 - prog(t, tf, tf + 0.6)
            if i in (2, 6): al = max(al, 0.55)   # not everything vanishes
            germ(c, gx, gy, 26, a=al * prog(t, S('8'), S('8') + 0.4), kind=i % 2)
        if t >= A['germs8'] - 0.2: mono(c, 'CAN INACTIVATE MANY PATHOGENS', W / 2, 1010, 24, CREAM, a=prog(t, A['germs8'], A['germs8'] + 0.3), kind='monob')
        draw_clip(c, 'sr_ph', 38, 1150, 1700, t, A['ph'] + 0.3, rot=-0.6, hl_t0=A['ph'] + 0.6, hl_dur=1.0)
        source_tag(c, 'SCIENTIFIC REPORTS · 2021', 90, 1250, a=prog(t, A['ph'] + 0.5, A['ph'] + 0.8))
    # 9 fresh coat, for a while
    elif t < S('10') - 0.05:
        chain(c, t, 4)
        c.set_source_rgb(0.62, 0.55, 0.45); c.rectangle(140, 320, 800, 640); c.fill()
        k = e_io(prog(t, S('9'), A['white9'] + 0.3))
        c.set_source_rgba(0.98, 0.97, 0.93, 1); c.rectangle(140, 320, 800 * k, 640); c.fill()
        broom_x = 140 + 800 * k
        c.set_source_rgba(0.82, 0.68, 0.36, 1); c.rectangle(broom_x - 20, 600, 40, 120); c.fill()
        if t >= A['while9'] - 0.3:
            kk = prog(t, A['while9'] - 0.3, S('10'))
            c.set_source_rgba(1, 1, 1, 0.15); c.set_line_width(18); c.arc(W / 2, 1110, 90, 0, 2 * math.pi); c.stroke()
            c.set_source_rgba(*AMBER, 1); c.arc(W / 2, 1110, 90, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (1 - kk * 0.6)); c.stroke()
            mono(c, 'FOR A WHILE', W / 2, 1110, 24, CREAM, kind='monob')
            for i in range(4): germ(c, 260 + i * 180, 640, 24, a=0.7 * (1 - prog(t, A['while9'] + 0.1 * i, A['while9'] + 0.5 + 0.1 * i)), kind=i % 2)
    # 10 carbonation
    elif t < S('11') - 0.05:
        chain(c, t, 4)
        c.set_source_rgba(0.98, 0.97, 0.93, 1); c.rectangle(140, 320, 800, 520); c.fill()
        k = prog(t, A['co2'] - 0.2, A['caco3'] + 0.8)
        c.set_source_rgba(0.75, 0.72, 0.65, 0.6 * k); c.rectangle(140, 320, 800, 520); c.fill()
        rng = np.random.default_rng(2)
        for i in range(16):
            x = 180 + rng.uniform(0, 720); y = 900 - ((t - A['co2'] + i * 0.2) * 160) % 560
            if t >= A['co2'] - 0.2:
                c.set_source_rgba(0.6, 0.8, 1.0, 0.7); c.set_line_width(3); c.new_path(); c.arc(x, y, 18, 0, 2 * math.pi); c.stroke()
                font(c, 'monob', 14); c.move_to(x - 15, y + 5); c.set_source_rgba(0.6, 0.8, 1.0, 0.9); c.show_text('CO₂')
        if t >= A['caco3'] - 0.2:
            u = e_back(prog(t, A['caco3'] - 0.2, A['caco3'] + 0.1))
            c.save(); c.translate(W / 2, 960); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -420, -70, 840, 140, 30)
            chem(c, 0, 0, 58); c.restore()
        if t >= A['limestone'] - 0.3:
            pill(c, 'LIME → LIMESTONE MINERAL', W / 2, 1140, 34, CREAM, s=e_back(prog(t, A['limestone'] - 0.3, A['limestone'])))
            c.set_source_rgba(0.6, 0.58, 0.52, 1); c.move_to(470, 1290); c.line_to(510, 1220); c.line_to(580, 1210); c.line_to(620, 1260); c.line_to(600, 1300); c.close_path(); c.fill()
    # 11 belief + timing, equal
    elif t < S('12') - 0.05:
        for j, (lab, col) in enumerate((('OLD HOME', (0.97, 0.96, 0.92)), ('TODAY', (0.80, 0.82, 0.86)))):
            x = 90 + j * 470
            c.set_source_rgb(*col); c.rectangle(x, 360, 430, 420); c.fill()
            c.set_source_rgb(0.45, 0.32, 0.22) if j == 0 else c.set_source_rgb(0.35, 0.38, 0.45)
            c.rectangle(x, 780, 430, 50); c.fill()
            broom(c, x + 330, 820, 0.6)
            mono(c, lab, x + 215, 880, 24, CREAM, kind='monob')
        for j, lab in enumerate(('BELIEF', 'TIMING')):
            x = 320 + j * 440; u = e_back(prog(t, S('11') + 0.2 * j, S('11') + 0.3 + 0.2 * j))
            c.save(); c.translate(x, 1050); c.scale(max(0.01, u), max(0.01, u)); glass_dark(c, -190, -65, 380, 130, 30)
            c.set_source_rgba(*AMBER, 1); c.set_line_width(4); rrect(c, -190, -65, 380, 130, 30); c.stroke()
            head(c, lab, 0, 0, 56, AMBER, shadow=False); c.restore()
        if t >= A['practical']: head(c, '+', W / 2, 1050, 70, CREAM, a=prog(t, A['practical'], A['practical'] + 0.2), shadow=False)
    # 12 series slide
    elif t < S('L') - 0.05:
        caps = t < END_T0 - 0.3
        sc_ = 1.0 - 0.14 * e_io(prog(t, END_T0 - 0.5, END_T0))
        slide(c, t, S('12') - 0.05, scale=sc_)
        CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745)
    else:
        # broom slides in to the exact spot it leans in frame 0, then the chaos room fades in around it
        k = e_io(prog(t, S('L') + 0.35, S('L') + 1.1)); ks = e_io(prog(t, S('L') - 0.05, S('L') + 0.45))
        c.push_group(); slide(c, t, S('12') - 0.05, scale=0.86); CTA.draw(c, t, END_T0, PLAT, LANGV, y=1745); c.pop_group_to_source(); c.paint_with_alpha(1 - ks)
        c.push_group(); board_bg(c, 0.0); sc_hook(c, 0.0, frozen=True); tag(c); c.pop_group_to_source(); c.paint_with_alpha(k)
        if k < 1:
            u = e_out(prog(t, S('L') - 0.05, S('L') + 0.6))
            broom(c, 900 + (1 - u) * 420, 1080, 1.0, a=1 - k)
    if caps: (K.captions(c, t, y=1440) if LANGV == 'en' else R3.te_captions(c, t, y=1440))
    if t < S('12') - 0.05: tag(c)
    return s
