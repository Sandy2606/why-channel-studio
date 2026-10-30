"""Series slide layers (EN/TE): bg + elements (RGBA, full-frame) for animated reveal."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
V='/home/claude/why-channel-studio/videos/'
W,H=1080,1920; A=(255,178,36); CR=(244,241,234)
F=lambda p:ImageFont.truetype('/root/.fonts/ArchivoBlack-Regular.ttf',p)
M=lambda p,b=True:ImageFont.truetype('/root/.fonts/SpaceMono-Bold.ttf' if b else '/root/.fonts/SpaceMono-Regular.ttf',p)
def TF(p,w='Bold'):
    f=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',p,layout_engine=ImageFont.Layout.RAQM)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
COV={'en':[V+'2026-10-26_short_gold_stardust/cover_gold1_EN.jpg',V+'2026-10-27_short_gold_never_rusts/cover_gold2_EN.jpg',V+'2026-10-28_short_gold_yellow/Gold3_cover_EN.jpg',V+'2026-10-29_short_gold_comes_home/Gold4_cover_EN.jpg',V+'2026-10-30_short_gold_dhanteras/covers/Gold5_cover_EN.jpg','Gold6_cover_EN.jpg'],
     'te':[V+'2026-10-26_short_gold_stardust/cover_gold1_TE.jpg',V+'2026-10-27_short_gold_never_rusts/cover_gold2_TE.jpg',V+'2026-10-28_short_gold_yellow/Gold3_cover_TE.jpg',V+'2026-10-29_short_gold_comes_home/Gold4_cover_TE.jpg',V+'2026-10-30_short_gold_dhanteras/covers/Gold5_cover_TE.jpg','Gold6_cover_TE.jpg']}
LONG={'en':V+'2026-10-28_long_why_gold_expensive/thumb_gold_long_EN.jpg','te':V+'2026-10-28_long_why_gold_expensive/thumb_gold_long_TE.jpg'}
TIT={'en':['Made in dead stars','Why it never rusts',"Why it's yellow",'Coming home','Gold vs banks','Why it\'s falling'],
     'te':['Dead stars నుంచి','తుప్పు ఎందుకు పట్టదు','పసుపు రంగు ఎందుకు','ఇంటికి వస్తోంది','Bank vs Gold','ఎందుకు పడుతోంది']}
def layer(): return Image.new('RGBA',(W,H),(0,0,0,0))
def paste_round(L,im,box,r=22,outline=None,w=4):
    x0,y0,x1,y1=box; m=Image.new('L',(x1-x0,y1-y0),0); ImageDraw.Draw(m).rounded_rectangle((0,0,x1-x0-1,y1-y0-1),r,fill=255)
    L.paste(im.convert('RGB').resize((x1-x0,y1-y0),Image.LANCZOS),(x0,y0),m)
    if outline: ImageDraw.Draw(L).rounded_rectangle(box,r,outline=outline,width=w)
for lang in ('en','te'):
    out=[]; meta=[]
    hd=layer(); d=ImageDraw.Draw(hd)
    d.text((W/2,120),'GOLD WEEK',font=F(84),fill=A,anchor='mm')
    if lang=='en': d.text((W/2,192),'EVERY VIDEO IN THIS SERIES',font=M(26),fill=CR,anchor='mm')
    else: d.text((W/2,192),'ఈ series లో అన్ని videos',font=TF(34),fill=CR,anchor='mm')
    out.append(('header',hd,(W/2,150)))
    lw=820; lh=int(lw*720/1280); lx0=(W-lw)//2; ly0=240
    L=layer(); paste_round(L,Image.open(LONG[lang]),(lx0,ly0,lx0+lw,ly0+lh),26,A,5); d=ImageDraw.Draw(L)
    bx1,by1=lx0+lw-20,ly0+lh-20; bx0,by0=bx1-300,by1-56
    d.rounded_rectangle((bx0,by0,bx1,by1),28,fill=(10,10,10)); d.polygon([(bx0+30,by0+16),(bx0+30,by0+40),(bx0+50,by0+28)],fill=A)
    d.text((bx0+66,by0+28),'FULL VIDEO',font=M(26),fill=A,anchor='lm')
    if lang=='en': d.text((W/2,ly0+lh+40),'Why Is Gold So Expensive? · on the channel',font=M(24,False),fill=CR,anchor='mm')
    else: d.text((W/2,ly0+lh+40),'Gold ఎందుకు ఇంత Costly? · మన channel లో',font=TF(30),fill=CR,anchor='mm')
    out.append(('long',L,(W/2,ly0+lh/2)))
    cw=250; ch=444; gap=40; x0=(W-3*cw-2*gap)//2; gx=[x0+i*(cw+gap) for i in range(3)]; gy=[ly0+lh+90, ly0+lh+90+ch+80]
    for i,(cv,tt) in enumerate(zip(COV[lang],TIT[lang])):
        x=gx[i%3]; y=gy[i//3]; L=layer(); paste_round(L,Image.open(cv),(x,y,x+cw,y+ch),18,A if i==5 else None,6); d=ImageDraw.Draw(L)
        d.rounded_rectangle((x+10,y+10,x+92,y+54),22,fill=(10,10,10)); d.text((x+51,y+32),f'{i+1}/6',font=M(22),fill=A,anchor='mm')
        if i==5:
            d.rounded_rectangle((x+cw/2-104,y+ch-58,x+cw/2+104,y+ch-14),22,fill=A); d.text((x+cw/2,y+ch-36),"YOU'RE HERE",font=M(21),fill=(10,10,10),anchor='mm')
        if lang=='en': d.text((x+cw/2,y+ch+28),tt,font=M(21,False),fill=CR,anchor='mm')
        else: d.text((x+cw/2,y+ch+30),tt,font=TF(26),fill=CR,anchor='mm')
        out.append((f'c{i}',L,(x+cw/2,y+ch/2)))
    L=layer(); d=ImageDraw.Draw(L); txt='NEXT · NEW SERIES THIS SUNDAY' if lang=='en' else 'తర్వాత · ఈ ఆదివారం కొత్త series'
    f=M(26) if lang=='en' else TF(32); tw=d.textlength(txt,font=f); y=gy[1]+ch+80
    d.rounded_rectangle((W/2-tw/2-34,y-34,W/2+tw/2+34,y+34),34,fill=(10,10,10),outline=A,width=3); d.text((W/2,y),txt,font=f,fill=A,anchor='mm')
    out.append(('next',L,(W/2,y)))
    for k,(name,L,c) in enumerate(out):
        L.save(f'slide_{lang}_{k}_{name}.png'); meta.append([f'slide_{lang}_{k}_{name}.png',c])
    json.dump(meta,open(f'slide_{lang}.json','w'))
    comp=Image.new('RGB',(W,H),(11,11,13))
    for name,L,c in out: comp.paste(L,(0,0),L)
    comp.save(f'slide_{lang}_preview.png'); print(lang, gy[1]+ch+80)
