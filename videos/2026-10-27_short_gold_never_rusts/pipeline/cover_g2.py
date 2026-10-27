import sys; sys.path.insert(0,'/home/claude/elnino'); sys.path.insert(0,'/home/claude/gold2')
from thumbkit import logo
from epic import font, is_te
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
W,H=1080,1920
def feather(h0,h1,top=True):
    y=np.arange(H,dtype=np.float32); m=np.clip((h1-y)/(h1-h0),0,1) if top else np.clip((y-h0)/(h1-h0),0,1)
    return Image.fromarray((np.repeat(m[:,None],W,1)*255).astype(np.uint8),'L')
def base_old():
    neb=Image.open('cf/N/0300.jpg').convert('RGB').crop((0,330,1080,1320)).resize((1300,1192)).crop((110,0,1190,1192))
    top=Image.new('RGB',(W,H),(6,7,12)); top.paste(neb,(0,0))
    bars=Image.open('cf/B/0011.jpg').convert('RGB'); bars=ImageEnhance.Brightness(bars).enhance(1.25)
    bot=Image.new('RGB',(W,H),(6,7,12)); bot.paste(bars.resize((1080,1920)).crop((0,500,1080,1720)),(0,700))
    im=Image.composite(top,bot,feather(820,1180,True)).convert('RGBA')
    y=np.arange(H); a=np.exp(-((y-1230)/330.)**2)*215                      # dark band behind the words
    g=np.zeros((H,W,4),np.uint8); g[...,3]=a[:,None].astype(np.uint8); im.alpha_composite(Image.fromarray(g))
    return im
def gold_text(im,text,cy,px):
    f=font('tesans' if is_te(text) else 'archivo',px); b=f.getbbox(text); w,h=b[2]-b[0],b[3]-b[1]
    m=Image.new('L',(w+40,h+40),0); ImageDraw.Draw(m).text((20-b[0],20-b[1]),text,font=f,fill=255)
    yy=np.linspace(0,1,h+40)[:,None]; c0=np.array([255,236,160]); c1=np.array([214,140,20])
    grad=(c0*(1-yy[...,None])+c1*yy[...,None]); grad=np.repeat(grad,w+40,1)
    g=Image.fromarray(grad.astype(np.uint8),'RGB').convert('RGBA'); g.putalpha(m)
    glow=Image.new('RGBA',g.size,(255,190,60,0)); glow.putalpha(m.filter(ImageFilter.GaussianBlur(18)).point(lambda p:int(p*.75)))
    sh=Image.new('RGBA',g.size,(0,0,0,0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(6)))
    x=(W-g.width)//2; y=int(cy-g.height/2)
    im.alpha_composite(sh,(x+4,y+6)); im.alpha_composite(glow,(x,y)); im.alpha_composite(g,(x,y))
def white_text(im,text,cy,px,col=(255,255,255)):
    f=font('tesans' if is_te(text) else 'archivo',px); b=f.getbbox(text)
    t=Image.new('RGBA',(b[2]-b[0]+40,b[3]-b[1]+40),(0,0,0,0)); ImageDraw.Draw(t).text((20-b[0],20-b[1]),text,font=f,fill=col)
    sh=Image.new('RGBA',t.size,(0,0,0,0)); sh.putalpha(t.split()[3].filter(ImageFilter.GaussianBlur(8)))
    x=(W-t.width)//2; y=int(cy-t.height/2); im.alpha_composite(sh,(x+3,y+5)); im.alpha_composite(t,(x,y))
def tag(im,text,cy):
    f=font('mono',38); w=f.getlength(text)+len(text)*6+70; h=74
    t=Image.new('RGBA',(int(w),h),(0,0,0,0)); d=ImageDraw.Draw(t)
    d.rounded_rectangle((1,1,w-2,h-2),radius=37,fill=(10,10,10,170),outline=(255,178,36,255),width=3)
    x=35
    for c in text: d.text((x,h/2),c,font=f,fill=(255,178,36),anchor='lm'); x+=f.getlength(c)+6
    im.alpha_composite(t,(int((W-w)/2),int(cy-h/2)))
def cover(lang,out):
    im=base()
    if lang=='en':
        white_text(im,'YOUR GOLD',1080,150); white_text(im,'CAME FROM',1225,96,(244,241,234)); gold_text(im,'DEAD STARS',1375,140)
    else:
        white_text(im,'మీ గోల్డ్',1070,170); gold_text(im,'చనిపోయిన స్టార్స్',1250,118); white_text(im,'నుంచి వచ్చింది',1405,92,(244,241,234))
    tag(im,'GOLD',1590)
    logo(im,50,50,64); im.convert('RGB').save(out,quality=93)


def base():
    im=Image.open('media/tut.jpg').convert('RGB'); s=max(W/im.width,H/im.height)*1.02
    im=im.resize((int(im.width*s),int(im.height*s))); x0=(im.width-W)//2; im=im.crop((x0,0,x0+W,H)).convert('RGBA')
    y=np.arange(H); g=np.zeros((H,W,4),np.uint8); g[...,3]=(np.clip((y-860)/420,0,1)**1.1*240)[:,None]; im.alpha_composite(Image.fromarray(g))
    return im
def cover2(lang,out):
    im=base()
    if lang=='en': white_text(im,'WHY GOLD',1250,150); gold_text(im,'NEVER RUSTS',1410,118)
    else: white_text(im,'గోల్డ్‌కి తుప్పు',1240,150); gold_text(im,'ఎందుకు పట్టదు?',1420,120)
    tag(im,'GOLD',1640); logo(im,50,50,64); im.convert('RGB').save(out,quality=93)
cover2('en','share/cover_gold2_EN.jpg'); cover2('te','share/cover_gold2_TE.jpg')
