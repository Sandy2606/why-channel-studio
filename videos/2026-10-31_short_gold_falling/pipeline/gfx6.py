# ---------------- graphics ----------------
def big_num(c, txt, x, y, px, t, t0, anchor='c'):
    if t < t0: return
    u = e_back(prog(t, t0, t0 + 0.3)); font(c, 'head', px); e = c.text_extents(txt)
    c.save(); c.translate(x, y); c.scale(u, u)
    xx = -e.width / 2 - e.x_bearing if anchor == 'c' else 0
    c.move_to(xx, px * 0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgba(0, 0, 0, 0.85); c.set_line_width(px * 0.1); c.stroke_preserve(); c.set_source(agrad(xx, 0, xx + e.width, 0)); c.fill(); c.restore()
def share_bar(c, y, label, frac, t, t0, col_grad=True):
    x0, w, h = 120, 840, 90
    glass_dark(c, x0, y, w, h, 45)
    u = e_out(prog(t, t0, t0 + 0.8)); fw = max(h, w * frac * u)
    rrect(c, x0, y, fw, h, 45); c.set_source(agrad(x0, 0, x0 + w, 0) if col_grad else cairo.SolidPattern(0.55, 0.55, 0.6)); c.fill()
    mono(c, label, x0, y - 30, 26, CREAM, anchor='l', kind='monob')
    if u > 0.2:
        font(c, 'head', 60); s = f'{int(round(frac * 100 * u))}%'; e = c.text_extents(s)
        c.move_to(x0 + fw - e.width - 30, y + h / 2 + 22); c.set_source_rgb(*INK); c.show_text(s)
