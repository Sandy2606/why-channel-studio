import sys, cairo
sys.argv=sys.argv[:1]
sys.path.insert(0,'/home/claude/rv')
import render2 as K
for plat, word in (('yt','SUBSCRIBE'),('ig','FOLLOW')):
    for kind,(px,y) in {'nudge':(40,1525),'end':(54,1265)}.items():
        s=cairo.ImageSurface(cairo.FORMAT_ARGB32,1080,1920); c=cairo.Context(s)
        K.pill(c, word, 540, y, px, K.AMBER, K.INK); s.write_to_png(f'/home/claude/g3/ov3_{kind}_{plat}.png')
