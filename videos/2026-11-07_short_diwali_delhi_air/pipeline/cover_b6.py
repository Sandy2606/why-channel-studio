import sys, os, cairo
from PIL import Image, ImageFont, ImageDraw
sys.argv=sys.argv[:1]
import render_b6 as R
sys.path.insert(0,'/home/claude/elnino'); sys.path.insert(0,'/home/claude/why-channel-studio/videos/2026-10-26_short_gold_stardust/pipeline')
from thumbkit import logo
from epic import font as efont
W,H=1080,1920
def TF(px,w='Black'):
    f=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',px,layout_engine=ImageFont.Layout.RAQM)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
def tagpill(im,text,lang,cy=1760):
    f=efont('mono',38) if lang=='en' else TF(38,'Bold')
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
    R.board_bg(c,0)
    R.home_draw(c,0,curtain=0.95)
    R.big_num(c,'488',W/2,700,190,1,0)
    def gtext(txt,y,px,grad):
        R.font(c,'head',px); e=c.text_extents(txt); x=W/2-e.width/2-e.x_bearing
        c.move_to(x,y+px*0.36); c.text_path(txt); c.set_line_join(cairo.LINE_JOIN_ROUND)
        c.set_source_rgba(0,0,0,0.85); c.set_line_width(px*0.12); c.stroke_preserve()
        c.set_source(R.agrad(x,0,x+e.width,0) if grad else cairo.SolidPattern(*R.CREAM)); c.fill()
    if lang=='en':
        gtext("WHY DELHI",1300,110,False); gtext('CHOKES',1440,150,True)
    s.write_to_png(f'cv6_{lang}.png'); base=Image.open(f'cv6_{lang}.png').convert('RGBA')
    if lang=='te':
        d=ImageDraw.Draw(base)
        d.text((W/2,1290),'Delhi ఎందుకు',font=TF(110),fill=(244,241,234),anchor='mm',stroke_width=10,stroke_fill=(0,0,0,230))
        d.text((W/2,1450),'ఉక్కిరిబిక్కిరి?',font=TF(120),fill=(255,178,36),anchor='mm',stroke_width=10,stroke_fill=(0,0,0,230))
    tagpill(base,'DIWALI · 6/6' if lang=='en' else 'దీపావళి · 6/6',lang); logo(base,50,50,64)
    base.convert('RGB').save(f'Diwali6_cover_{lang.upper()}.jpg',quality=92)
import os; make(os.environ.get('LANGV','en'))
