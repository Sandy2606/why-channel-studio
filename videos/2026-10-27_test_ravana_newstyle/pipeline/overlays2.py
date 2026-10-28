import cairo, math, sys
sys.argv=sys.argv[:1]
import render2 as R
for plat, word in (('yt','SUBSCRIBE'),('ig','FOLLOW')):
    for kind,(px,y) in {'nudge':(40,1525),'end':(58,770)}.items():
        s=cairo.ImageSurface(cairo.FORMAT_ARGB32,R.W,R.H); c=cairo.Context(s)
        R.pill(c, word, R.W/2, y, px, R.AMBER, R.INK)
        if kind=='end':
            # small hand-tap ring
            pass
        s.write_to_png(f'ov_{kind}_{plat}.png')
print('ok')
