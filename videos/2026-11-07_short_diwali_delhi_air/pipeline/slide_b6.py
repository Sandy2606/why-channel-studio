from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json
W,H=1080,1920; A=(255,178,36); CR=(244,241,234)
F=lambda p:ImageFont.truetype('/root/.fonts/ArchivoBlack-Regular.ttf',p)
M=lambda p,b=True:ImageFont.truetype('/root/.fonts/SpaceMono-Bold.ttf' if b else '/root/.fonts/SpaceMono-Regular.ttf',p)
def TF(p,w='Bold'):
    f=ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf',p,layout_engine=ImageFont.Layout.RAQM)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
VIRAL='/home/claude/why-channel-studio/videos/2026-11-01_long_diwali_explained/assets/images/09-india-diwali-rainbow-composite.jpg'
LONG={'en':'/home/claude/dl/thumb2_diwali_long_EN.jpg','te':'/home/claude/dl/thumb2_diwali_long_TE.jpg'}
TIT={'en':['Bonus: gift or law?','The space photo','Why we deep-clean','Market on Diwali','₹6 lakh crore','Delhi\'s air'],
     'te':['Bonus: బహుమతా?','Space photo','ఎందుకు శుభ్రం?','Diwali market','₹6 లక్షల కోట్లు','Delhi గాలి']}
DAY=['MON','TUE','WED','THU','FRI','SAT']
def layer(): return Image.new('RGBA',(W,H),(0,0,0,0))
def paste_round(L,im,box,r=22,outline=None,w=4):
    x0,y0,x1,y1=box; m=Image.new('L',(x1-x0,y1-y0),0); ImageDraw.Draw(m).rounded_rectangle((0,0,x1-x0-1,y1-y0-1),r,fill=255)
    im=im.convert('RGB'); s=max((x1-x0)/im.width,(y1-y0)/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1),Image.LANCZOS)
    l=(im.width-(x1-x0))//2; t=(im.height-(y1-y0))//2; im=im.crop((l,t,l+x1-x0,t+y1-y0))
    L.paste(im,(x0,y0),m)
    if outline: ImageDraw.Draw(L).rounded_rectangle(box,r,outline=outline,width=w)
for lang in ('en','te'):
    out=[]; meta=[]
    hd=layer(); d=ImageDraw.Draw(hd)
    d.text((W/2,120),'DIWALI WEEK',font=F(84),fill=A,anchor='mm')
    if lang=='en': d.text((W/2,192),'A NEW SHORT EVERY DAY',font=M(26),fill=CR,anchor='mm')
    else: d.text((W/2,192),'రోజుకో కొత్త Short',font=TF(34),fill=CR,anchor='mm')
    out.append(('header',hd,(W/2,150)))
    lw=820; lh=int(lw*720/1280); lx0=(W-lw)//2; ly0=240
    L=layer(); paste_round(L,Image.open(LONG[lang]),(lx0,ly0,lx0+lw,ly0+lh),26,A,5); d=ImageDraw.Draw(L)
    bx1,by1=lx0+lw-20,ly0+lh-20; bx0,by0=bx1-300,by1-56
    d.rounded_rectangle((bx0,by0,bx1,by1),28,fill=(10,10,10)); d.polygon([(bx0+30,by0+16),(bx0+30,by0+40),(bx0+50,by0+28)],fill=A)
    d.text((bx0+66,by0+28),'FULL VIDEO',font=M(26),fill=A,anchor='lm')
    if lang=='en': d.text((W/2,ly0+lh+40),'Diwali, Explained · on the channel',font=M(24,False),fill=CR,anchor='mm')
    else: d.text((W/2,ly0+lh+40),'దీపావళి వివరంగా · మన channel లో',font=TF(30),fill=CR,anchor='mm')
    out.append(('long',L,(W/2,ly0+lh/2)))
    cw=250; ch=444; gap=40; x0=(W-3*cw-2*gap)//2; gx=[x0+i*(cw+gap) for i in range(3)]; gy=[ly0+lh+90, ly0+lh+90+ch+80]
    for i,tt in enumerate(TIT[lang]):
        x=gx[i%3]; y=gy[i//3]; L=layer(); d=ImageDraw.Draw(L)
        if i==0: paste_round(L,Image.open(f'/home/claude/b1/Diwali1_cover_{lang.upper()}.jpg'),(x,y,x+cw,y+ch),18,CR,4)
        elif i==1: paste_round(L,Image.open(f'/home/claude/b2/Diwali2_cover_{lang.upper()}.jpg'),(x,y,x+cw,y+ch),18,CR,4)
        elif i==2: paste_round(L,Image.open(f'/home/claude/b3/Diwali3_cover_{lang.upper()}.jpg'),(x,y,x+cw,y+ch),18,CR,4)
        elif i==3: paste_round(L,Image.open(f'/home/claude/b4/Diwali4_cover_{lang.upper()}.jpg'),(x,y,x+cw,y+ch),18,CR,4)
        elif i==4: paste_round(L,Image.open(f'/home/claude/b5/Diwali5_cover_{lang.upper()}.jpg'),(x,y,x+cw,y+ch),18,CR,4)
        elif i==5: paste_round(L,Image.open(f'Diwali6_cover_{lang.upper()}.jpg'),(x,y,x+cw,y+ch),18,A,6)
        else:
            d.rounded_rectangle((x,y,x+cw,y+ch),18,fill=(22,22,26,235),outline=(80,80,90),width=2)
            d.text((x+cw/2,y+ch/2),DAY[i],font=M(40),fill=(150,150,158),anchor='mm')
        d.rounded_rectangle((x+10,y+10,x+92,y+54),22,fill=(10,10,10)); d.text((x+51,y+32),f'{i+1}/6',font=M(22),fill=A,anchor='mm')
        d.ellipse((x+cw-58,y+10,x+cw-12,y+56),fill=A); d.line([(x+cw-46,y+33),(x+cw-37,y+43),(x+cw-22,y+23)],fill=(10,10,10),width=5)
        if i==5:
            d.rounded_rectangle((x+cw/2-104,y+ch-58,x+cw/2+104,y+ch-14),22,fill=A); d.text((x+cw/2,y+ch-36),"YOU'RE HERE",font=M(21),fill=(10,10,10),anchor='mm')
        if False:
            d.rounded_rectangle((x+cw/2-90,y+ch-58,x+cw/2+90,y+ch-14),22,fill=(10,10,10),outline=A,width=3); d.text((x+cw/2,y+ch-36),"TOMORROW",font=M(21),fill=A,anchor='mm')
        if lang=='en': d.text((x+cw/2,y+ch+28),tt,font=M(20,False),fill=CR,anchor='mm')
        else: d.text((x+cw/2,y+ch+30),tt,font=TF(26),fill=CR,anchor='mm')
        out.append((f'c{i}',L,(x+cw/2,y+ch/2)))
    L=layer(); d=ImageDraw.Draw(L); txt='COMMENT YOUR WHY' if lang=='en' else 'మీ ఎందుకు? ని comment చేయండి'
    f=M(26) if lang=='en' else TF(32); tw=d.textlength(txt,font=f); y=gy[1]+ch+80
    d.rounded_rectangle((W/2-tw/2-34,y-34,W/2+tw/2+34,y+34),34,fill=(10,10,10),outline=A,width=3); d.text((W/2,y),txt,font=f,fill=A,anchor='mm')
    out.append(('next',L,(W/2,y)))
    for k,(name,L,c) in enumerate(out):
        L.save(f'slide_{lang}_{k}_{name}.png'); meta.append([f'slide_{lang}_{k}_{name}.png',c])
    json.dump(meta,open(f'slide_{lang}.json','w'))
    comp=Image.new('RGB',(W,H),(11,11,13))
    for name,L,c in out: comp.paste(L,(0,0),L)
    comp.save(f'slide_{lang}_preview.png'); print(lang, gy[1]+ch+80)
