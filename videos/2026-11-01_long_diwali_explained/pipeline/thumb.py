import os, sys, numpy as np, cairo
from PIL import Image
LANG = os.environ.get('LANGV', 'en')
import render as R
from base import *
import room as RM, gfx1 as G1, gfx2 as G2

s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(s)
cast = RM.Cast(); cast.anna['talk'] = 0.0; cast.chelli['talk'] = 0.6; cast.chelli['gesture'] = 0.8; cast.anna['gesture'] = 0.5
cast.anna['look'] = (0.55, 0); cast.chelli['look'] = (-0.3, 0)
c.save(); c.translate(-330, 0); RM.draw_room(c, 2.5, cast, cam=(1.06, 960, 520)); c.restore()
# right: evidence board panel
g = cairo.LinearGradient(1080, 0, 1300, 0); g.add_color_stop_rgba(0, 0.05, 0.05, 0.05, 0); g.add_color_stop_rgba(1, 0.05, 0.05, 0.05, 0.96)
c.set_source(g); c.rectangle(1080, 0, 840, H); c.fill()
c.set_source_rgba(0.05, 0.05, 0.05, 0.96); c.rectangle(1300, 0, 620, H); c.fill()
photo_panel(c, G2.VIRAL, 1570, 330, 560, 99, 0, rot=4)
stamp(c, L('NOT DIWALI', 'దీపావళి కాదు'), 1570, 330, 99, 0, 70, rot=-10)
G1.cal_page(c, 1330, 690, 220, L('THIS YEAR', 'ఈ ఏడాది'), '8', L('NOV · 2026', 'నవం · 2026'), 99, 0, rot=-8)
stamp(c, '₹ = ' + L('LAW', 'చట్టం'), 1680, 700, 99, 0, 64, rot=6)
# headline lower third
g = cairo.LinearGradient(0, 640, 0, H); g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, 0.92); c.set_source(g); c.rectangle(0, 640, W, H - 640); c.fill()
txt(c, L('DIWALI,', 'దీపావళి,'), 70, 880, 130, CREAM, anchor='l', stroke=8)
txt(c, L('EXPLAINED', 'వివరంగా'), 70, 1005, 130, grad=True, anchor='l', stroke=8)
txt(c, 'WHY?', 1330, 905, 60, grad=True, anchor='l', stroke=4)
pill(c, L('DIWALI · FULL STORY', 'దీపావళి · FULL STORY'), 1560, 1010, 30, outline=True, kind='monob')
a = np.ndarray((H, W, 4), np.uint8, s.get_data())[:, :, [2, 1, 0]].copy()
Image.fromarray(a).resize((1280, 720), Image.LANCZOS).save(f'/home/claude/dl/thumb_diwali_long_{LANG.upper()}.jpg', quality=92)
print('ok')
