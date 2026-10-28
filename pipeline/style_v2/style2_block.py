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
def _G():
    a = A; Wc = W / 2
    return [
        (a['35'] + 0.5, None),
        (a['women'], (Wc - 440, 620)), (a['just'], (Wc - 300, 800)), (a['why'] - 0.25, (Wc, 1180)), (a['why'] + 0.1, None),
        (a['people'] + 0.15, (Wc, 1180)), (a['people'] + 0.6, (Wc, 780)), (a['people'] + 0.95, None),
        (a['mandodari'], (Wc - 470, 400)), (T('was') - 0.05, (Wc + 70, 880)), (a['son'] - 0.1, (Wc - 220, 1010)), (a['dasara1'] - 0.05, None),
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
    if GUIDE is None: GUIDE = _G()
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
