import sys, json; sys.path.insert(0,'/home/claude/g4'); import clipkit as C
C.Z='/home/claude/dl/z/'
import subprocess
from PIL import Image
def page_img(pdf,page):
    k=(pdf,page)
    if k not in C._pages:
        base=f'/home/claude/dl/pg/hi_{pdf[:-4]}_{page}'
        subprocess.run(['pdftoppm','-r','300','-f',str(page),'-l',str(page),'-singlefile','-png',C.Z+pdf,base],check=True,capture_output=True)
        C._pages[k]=Image.open(base+'.png').convert('RGB')
    return C._pages[k]
C.page_img=page_img
_f=C.find
def find(pdf,page,phrase,nth=1):
    if '@@' in phrase: phrase,nn=phrase.split('@@'); nth=int(nn)
    return _f(pdf,page,phrase,nth)
C.find=find
B='01-bonus-act-ezylegal.pdf'; CA='02-cait-diwali-businesstoday.pdf'; E='03-earthsky-fake-diwali.pdf'; Z='04-muhurat-2026-zerodha.pdf'
I='05-muhurat-history-icicidirect.pdf'; T='06-iit-delhi-shiksha.pdf'; S='07-supreme-court-devdiscourse.pdf'; D='08-diwali-dates-publicholidays.pdf'
def R(pdf,pg,a,b,pad=3):
    A=C.find(pdf,pg,a); ws=C.words(pdf,pg)
    y0=min(w[1] for w in A); k=1
    while True:
        Bx=C.find(pdf,pg,b,k)
        if min(w[1] for w in Bx)>=y0-1: break
        k+=1
    y1=max(w[3] for w in Bx)
    inside=[w for w in ws if w[1]>=y0-1 and w[3]<=y1+1]
    return (min(w[0] for w in inside)-pad, y0-pad, max(w[2] for w in inside)+pad, y1+pad)
P={'bonus_h':[(B,1,R(B,1,'Understanding the Payment@@2','Act 1965',6),[])],
   'bonus_k':[(B,2,R(B,2,'The employee must be paid a monthly','(By the Amendment of 2015)'),['Rs. 21,000/-.']),(B,2,R(B,2,'The legislation provides a minimum','(Section 11 of the Payment of Bonus Act 1965).'),['minimum bonus of 8.33%','not exceed 20%'])],
   'bonus_8':[(B,2,R(B,2,'The bonus must be paid within','within one month of the act’s'),['within eight months after the end of the fiscal year'])],
   'cait':[(CA,1,R(CA,1,'Diwali 2025 sales hit Rs 6.05 lakh@@2','report'),['Rs 6.05 lakh']),(CA,6,R(CA,6,'The Diwali trade boom created 50 lakh','transport, and retail.'),['created 50 lakh','temporary jobs'])],
   'earth_h':[(E,1,R(E,1,'Fake image of Diwali','circulating',5),[])],
   'earth_k':[(E,3,R(E,3,'NASA, the extra light','subtle that space images'),['subtle that space images don’t show it.'])],
   'zer':[(Z,1,R(Z,1,'Muhurat Trading session on account','on Sunday, November 08, 2026.'),['Sunday, November 08, 2026.'])],
   'icici':[(I,3,R(I,3,'History of Muhurat Trading in India','BSE began the Muhurat'),['BSE began the Muhurat Trading tradition in 1957,','NSE adopted it in 1992.'])],
   'iit':[(T,1,R(T,1,"Delhi's poor air quality after Diwali is because of Biomass burning, not fireworks: IIT Delhi Study@@1","Delhi's poor air quality after Diwali is because of Biomass burning, not fireworks: IIT Delhi Study@@1"),[]),(T,1,R(T,1,'accounted for 95 per cent','around 12 hours following'),['plummets within','around 12 hours following Diwali”,'])],
   'sc':[(S,1,R(S,1,'Festive enthusiasm high','of our orders'),[]),(S,1,R(S,1,'A bench of Justices','A bench of Justices'),[])],
   'dates':[(D,1,R(D,1,'In 2025, Diwali will be','In 2026, Diwali falls'),['In 2026, Diwali falls on Sunday 8 November.'])]}
out={}
for k,parts in P.items():
    im,h=C.build(parts); im.save(f'clip_{k}.png'); out[k]={'hl':h}; print(k,im.size,len(h))
json.dump(out,open('clips.json','w'))
