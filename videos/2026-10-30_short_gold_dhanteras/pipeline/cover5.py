import sys, os, cairo
from PIL import Image, ImageFont, ImageDraw
sys.argv=sys.argv[:1]
import render5 as R
sys.path.insert(0,'/home/claude/elnino'); sys.path.insert(0,'/home/claude/why-channel-studio/videos/2026-10-26_short_gold_stardust/pipeline')
from thumbkit import logo
from epic import font as efont
W,H=1080,1920
def tagpill(im,text,lang,cy=1730):
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
    im.alpha_composite(t,(int((W-w)/2),cy-h//2))
def make(lang):
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
    im=Image.open('hero_blue.png').convert('RGB').resize((W,H),Image.LANCZOS)
    sf,_=R.surf_from_pil(im); c.set_source_surface(sf,0,0); c.paint()
    g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgba(0.42,0,0,0,0.0); g.add_color_stop_rgba(0.62,0,0,0,0.6); g.add_color_stop_rgba(1,0,0,0,0.92); c.set_source(g); c.paint()
    R.print_photo(c,'mother.jpg',270,960,400,99,0,rot=-5)
    R.draw_clip(c,'bs',730,880,620,99,0,rot=4,hl_t0=0,hl_dur=0.01,guide=False)
    R.thread(c,380,1080,620,960,99,0); R.glowdot(c,620,960,10)
    if lang=='en':
        for txt,y,px,grad in (('WHY INDIANS',1270,120,False),('TRUST GOLD',1410,134,True),('OVER BANKS',1565,130,False)):
            R.font(c,'head',px); e=c.text_extents(txt); x=W/2-e.width/2-e.x_bearing
            c.move_to(x,y+px*0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
            c.set_source_rgba(0,0,0,0.85); c.set_line_width(px*0.12); c.stroke_preserve()
            c.set_source(R.agrad(x,0,x+e.width,0) if grad else cairo.SolidPattern(*R.CREAM)); c.fill()
    s.write_to_png(f'c5_{lang}.png'); base=Image.open(f'c5_{lang}.png').convert('RGBA')
    if lang=='te':
        d=ImageDraw.Draw(base)
        def f(px):
            ft=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',px,layout_engine=ImageFont.Layout.RAQM)
            try: ft.set_variation_by_name('Black')
            except Exception: pass
            return ft
        for txt,y,px,col in (('Bank కంటే',1270,130,(244,241,234)),('Gold మీదే',1430,160,(255,178,36)),('నమ్మకం ఎందుకు?',1590,120,(244,241,234))):
            d.text((W/2,y),txt,font=f(px),fill=col,anchor='mm',stroke_width=10,stroke_fill=(0,0,0,230))
    tagpill(base,'GOLD · 5/6' if lang=='en' else 'గోల్డ్ · 5/6',lang); logo(base,50,50,64)
    base.convert('RGB').save(f'Gold5_cover_{lang.upper()}.jpg',quality=92)
make('en'); make('te')
