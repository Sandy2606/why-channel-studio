import sys; sys.path.insert(0,'/home/claude/elnino'); sys.path.insert(0,'/home/claude/gold1')
from thumbkit import logo
from epic import font, is_te
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
W,H=1280,720
def gold_text(im,text,x,y,px,kind=None):
    f=font(kind or ('tesans' if is_te(text) else 'archivo'),px); b=f.getbbox(text); w,h=b[2]-b[0],b[3]-b[1]
    m=Image.new('L',(w+40,h+40),0); ImageDraw.Draw(m).text((20-b[0],20-b[1]),text,font=f,fill=255)
    yy=np.linspace(0,1,h+40)[:,None]; c0=np.array([255,236,160]); c1=np.array([214,140,20])
    g=Image.fromarray(np.repeat(c0*(1-yy[...,None])+c1*yy[...,None],w+40,1).astype(np.uint8),'RGB').convert('RGBA'); g.putalpha(m)
    gl=Image.new('RGBA',g.size,(255,190,60,0)); gl.putalpha(m.filter(ImageFilter.GaussianBlur(14)).point(lambda p:int(p*.7)))
    sh=Image.new('RGBA',g.size,(0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(6)))
    im.alpha_composite(sh,(x+4,y+6)); im.alpha_composite(gl,(x,y)); im.alpha_composite(g,(x,y))
def white_text(im,text,x,y,px,col=(255,255,255)):
    f=font('tesans' if is_te(text) else 'archivo',px); b=f.getbbox(text)
    t=Image.new('RGBA',(b[2]-b[0]+40,b[3]-b[1]+40),(0,0,0,0)); ImageDraw.Draw(t).text((20-b[0],20-b[1]),text,font=f,fill=col)
    sh=Image.new('RGBA',t.size,(0,0,0,0)); sh.putalpha(t.split()[3].filter(ImageFilter.GaussianBlur(7)))
    im.alpha_composite(sh,(x+3,y+5)); im.alpha_composite(t,(x,y))
def chip(im,text,x,y,px):
    f=font('mono',px); w=f.getlength(text)+len(text)*4+56; h=int(px*1.9)
    t=Image.new('RGBA',(int(w),h),(0,0,0,0)); d=ImageDraw.Draw(t); d.rounded_rectangle((1,1,w-2,h-2),radius=h//2,fill=(10,10,10,190),outline=(255,178,36,255),width=3)
    xx=28
    for c in text: d.text((xx,h/2),c,font=f,fill=(255,178,36),anchor='lm'); xx+=f.getlength(c)+4
    im.alpha_composite(t,(x,y))
def base():
    sp=Image.open('cf/N/0300.jpg').convert('RGB').resize((W,H)); sp=ImageEnhance.Brightness(sp).enhance(1.05)
    bars=Image.open('cf/B/0030.jpg').convert('RGB').resize((W,H)); bars=ImageEnhance.Brightness(bars).enhance(1.2)
    yy,xx=np.mgrid[0:H,0:W]; m=np.clip((yy/H-.6)/.16,0,1)*np.clip((xx/W-.18)/.2,0,1)          # bars bottom-left, stars top-right
    im=Image.composite(bars,sp,Image.fromarray((m*255).astype(np.uint8))).convert('RGBA')
    g=np.zeros((H,W,4),np.uint8); g[...,3]=(np.clip((.62-xx/W)/.62,0,1)**1.3*200).astype(np.uint8); im.alpha_composite(Image.fromarray(g))
    return im
def thumb(lang,out):
    im=base()
    if lang=='en':
        white_text(im,'GOLD',48,40,140); gold_text(im,'CAME FROM',48,205,86); gold_text(im,'SPACE',48,305,140)
    else:
        white_text(im,'Gold',48,30,130); gold_text(im,'Space నుంచి',48,195,96); gold_text(im,'వచ్చింది!',48,340,96)
    chip(im,'$5,000/oz · WHY?',52,500,28); logo(im,1150,30,40); im.convert('RGB').save(out,quality=93)
thumb('en','share/thumb_gold_long_EN.jpg'); thumb('te','share/thumb_gold_long_TE.jpg')
