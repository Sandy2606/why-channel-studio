import sys, os, math, cairo
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
os.environ.setdefault('LANGV','en'); sys.argv=sys.argv[:1]
import render3 as R
W,H=1080,1920
def make(lang):
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    # hero: real gold ring frame, warmed + sharpened
    im=Image.open('hero_gold.png').convert('RGB').resize((W,H),Image.LANCZOS)
    sf,_=R.surf_from_pil(im); c.set_source_surface(sf,0,0); c.paint()
    g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgba(0,0,0,0,0.55); g.add_color_stop_rgba(0.35,0,0,0,0.05); g.add_color_stop_rgba(0.62,0,0,0,0.55); g.add_color_stop_rgba(1,0,0,0,0.95)
    c.set_source(g); c.paint()
    # Einstein taped print
    R.print_photo(c,'einstein.jpg',300,560,400,99,0,rot=-6)
    R.draw_clip(c,'bbc_q1',760,330,560,99,0,rot=4,hl_t0=0,hl_dur=0.01,guide=False)
    R.thread(c,420,760,640,420,99,0)
    R.glowdot(c,640,420,10)
    if lang=='en':
        for txt,y,px,grad in (('EINSTEIN',1240,170,False),('MADE GOLD',1400,150,False),('YELLOW',1560,190,True)):
            R.font(c,'head',px); e=c.text_extents(txt); x=W/2-e.width/2-e.x_bearing
            c.move_to(x,y+px*0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.set_source_rgba(0,0,0,0.85); c.set_line_width(px*0.12); c.stroke_preserve()
            c.set_source(R.agrad(x,0,x+e.width,0) if grad else cairo.SolidPattern(*R.CREAM)); c.fill()
        s.write_to_png('cover3_en.png')
    else:
        s.write_to_png('cover3_te_base.png')
        base=Image.open('cover3_te_base.png').convert('RGBA'); d=ImageDraw.Draw(base)
        def f(px,var='Black'):
            ft=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',px,layout_engine=ImageFont.Layout.RAQM)
            try: ft.set_variation_by_name(var)
            except Exception: pass
            return ft
        for txt,y,px,col in (('Gold పసుపు రంగు',1260,120,(244,241,234)),('Einstein',1430,170,(255,178,36)),('వల్లే!',1600,150,(255,178,36))):
            d.text((W/2,y),txt,font=f(px),fill=col,anchor='mm',stroke_width=10,stroke_fill=(0,0,0,230))
        base.save('cover3_te.png')
    sys.path.insert(0,'/home/claude/elnino'); sys.path.insert(0,'/home/claude/why-channel-studio/videos/2026-10-26_short_gold_stardust/pipeline')
    from thumbkit import logo
    from epic import font as efont
    n0='cover3_en.png' if lang=='en' else 'cover3_te.png'
    im=Image.open(n0).convert('RGBA')
    text='GOLD · 3/6' if lang=='en' else 'గోల్డ్ · 3/6'
    if lang=='en': f=efont('mono',38)
    else:
        f=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',38,layout_engine=ImageFont.Layout.RAQM)
        try: f.set_variation_by_name('Bold')
        except Exception: pass
    w=int(f.getlength(text)+(len(text)*6 if lang=='en' else 0)+70); h=74
    t=Image.new('RGBA',(w,h),(0,0,0,0)); d=ImageDraw.Draw(t)
    d.rounded_rectangle((1,1,w-2,h-2),radius=37,fill=(10,10,10,170),outline=(255,178,36,255),width=3)
    if lang=='en':
        x=35
        for ch in text: d.text((x,h/2),ch,font=f,fill=(255,178,36),anchor='lm'); x+=f.getlength(ch)+6
    else: d.text((w/2,h/2),text,font=f,fill=(255,178,36),anchor='mm')
    im.alpha_composite(t,(int((W-w)/2),1730-h//2))
    logo(im,50,50,64); im.save(n0)
    for n in [n0]:
        Image.open(n).convert('RGB').save(n.replace('.png','.jpg').replace('cover3','Gold3_cover').replace('_en','_EN').replace('_te','_TE'),quality=92)
make('en'); make('te')
