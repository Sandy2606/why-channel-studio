import sys, os, math, numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageFilter, ImageEnhance
sys.path.insert(0,'/home/claude/elnino'); sys.path.insert(0,'/home/claude/why-channel-studio/videos/2026-10-26_short_gold_stardust/pipeline')
from thumbkit import logo
from epic import font as efont
W,H=1080,1920; AMB=(255,178,36); CR=(244,241,234)
def TF(px,w='Black'):
    f=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',px,layout_engine=ImageFont.Layout.RAQM)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
def make(lang):
    im=Image.open('real/gate.jpg').convert('RGB'); sc=H/im.height*1.0
    im=im.resize((int(im.width*sc),int(im.height*sc)),Image.LANCZOS)
    cx=int(0.505*im.width); top=0
    bg=im.crop((cx-W//2,top,cx+W//2,top+H)).convert('RGBA')
    bg=ImageEnhance.Contrast(bg).enhance(1.08)
    # thicker smog: warm grey veil, stronger in the sky
    a=np.zeros((H,W),np.float32); y=np.linspace(1,0,H)[:,None]; a[:]=0.42*y**1.3+0.08
    veil=Image.new('RGBA',(W,H),(150,128,104,0)); veil.putalpha(Image.fromarray((a*255).astype(np.uint8)))
    bg=Image.alpha_composite(bg,veil)
    rng=np.random.default_rng(3); d=ImageDraw.Draw(bg)
    for _ in range(320):     # floating particles in the lamp light
        x,yy=rng.uniform(0,W),rng.uniform(0,H*0.75); r=rng.uniform(0.6,1.8)
        d.ellipse((x-r,yy-r,x+r,yy+r),fill=(255,236,200,int(rng.uniform(25,90))))
    # dark fade at the bottom for the title
    g=np.zeros((H,W),np.float32); yy=np.linspace(0,1,H)[:,None]; g[:]=np.clip((yy-0.55)/0.4,0,1)**1.4*0.92
    sh=Image.new('RGBA',(W,H),(8,6,5,0)); sh.putalpha(Image.fromarray((g*255).astype(np.uint8))); bg=Image.alpha_composite(bg,sh)
    # magnifier lens over the haze: what you are breathing
    lx,ly,lr=800,560,150
    lens=Image.new('RGBA',(2*lr,2*lr),(0,0,0,0)); ld=ImageDraw.Draw(lens)
    ld.ellipse((0,0,2*lr-1,2*lr-1),fill=(70,58,48,235))
    r2=np.random.default_rng(9)
    for _ in range(46):
        x,y=r2.uniform(25,2*lr-25),r2.uniform(25,2*lr-25)
        if (x-lr)**2+(y-lr)**2>(lr-22)**2: continue
        rr=r2.uniform(4,11); col=(255,178,36,235) if r2.random()<0.35 else (30,26,24,240)
        ld.ellipse((x-rr,y-rr,x+rr,y+rr),fill=col)
    lens=lens.filter(ImageFilter.GaussianBlur(0.6))
    m=Image.new('L',(2*lr,2*lr),0); ImageDraw.Draw(m).ellipse((0,0,2*lr-1,2*lr-1),fill=255); bg.paste(lens,(lx-lr,ly-lr),m)
    d=ImageDraw.Draw(bg)
    d.ellipse((lx-lr-6,ly-lr-6,lx+lr+6,ly+lr+6),outline=(235,230,220,255),width=12)
    d.line((lx-lr*0.72,ly+lr*0.72,lx-lr*1.35,ly+lr*1.35),fill=(235,230,220,255),width=26)
    f=efont('mono',30) if lang=='en' else TF(32,'Bold')
    d.text((lx,ly+lr+44),'PM2.5' if lang=='en' else 'PM2.5 కణాలు',font=f,fill=AMB,anchor='mm',stroke_width=4,stroke_fill=(0,0,0,200))
    # big number
    fh=efont('archivo',250)
    d.text((80,330),'488',font=fh,fill=AMB,anchor='lm',stroke_width=10,stroke_fill=(20,12,6,255))
    sub='µg/m³ · DIWALI 2025' if lang=='en' else 'మైక్రోగ్రాములు · Diwali 2025'
    d.text((92,500),sub,font=efont('mono',34) if lang=='en' else TF(34,'Bold'),fill=CR,anchor='lm',stroke_width=4,stroke_fill=(0,0,0,200))
    pill='8× THE SAFE LIMIT' if lang=='en' else 'సురక్షిత పరిమితికి 8 రెట్లు'
    pf=efont('archivo',40) if lang=='en' else TF(40,'Bold'); pw=int(pf.getlength(pill))+60
    d.rounded_rectangle((86,560,86+pw,630),radius=35,fill=(220,60,50,255)); d.text((86+pw/2,595),pill,font=pf,fill=CR,anchor='mm')
    # title
    if lang=='en':
        d.text((W/2,1440),'WHY DELHI',font=efont('archivo',128),fill=CR,anchor='mm',stroke_width=10,stroke_fill=(0,0,0,230))
        d.text((W/2,1590),'CHOKES',font=efont('archivo',190),fill=AMB,anchor='mm',stroke_width=12,stroke_fill=(0,0,0,230))
    else:
        d.text((W/2,1430),'Delhi ఎందుకు',font=TF(120),fill=CR,anchor='mm',stroke_width=10,stroke_fill=(0,0,0,230))
        d.text((W/2,1590),'ఉక్కిరిబిక్కిరి?',font=TF(132),fill=AMB,anchor='mm',stroke_width=11,stroke_fill=(0,0,0,230))
    # series tag
    t='DIWALI · 6/6' if lang=='en' else 'దీపావళి · 6/6'; tf=efont('mono',38) if lang=='en' else TF(38,'Bold'); tw=int(tf.getlength(t))+(len(t)*6 if lang=='en' else 0)+70
    d.rounded_rectangle(((W-tw)/2,1740,(W+tw)/2,1814),radius=37,fill=(10,10,10,190),outline=AMB,width=3)
    if lang=='en':
        x=(W-tw)/2+35
        for ch in t: d.text((x,1777),ch,font=tf,fill=AMB,anchor='lm'); x+=tf.getlength(ch)+6
    else: d.text((W/2,1777),t,font=tf,fill=AMB,anchor='mm')
    logo(bg,50,50,64)
    bg.convert('RGB').save(f'Diwali6_cover_{lang.upper()}.jpg',quality=92)
for L in ('en','te'): make(L)
