import sys, json; sys.path.insert(0,'/home/claude/g4'); import clipkit as C
C.Z='/home/claude/g6/z/'
_pi=C.page_img
def page_img(pdf,page):
    import subprocess
    from PIL import Image
    k=(pdf,page)
    if k not in C._pages:
        base=f'/home/claude/g6/pg/hi_{pdf[:-4]}_{page}'
        subprocess.run(['pdftoppm','-r','300','-f',str(page),'-l',str(page),'-singlefile','-png',C.Z+pdf,base],check=True,capture_output=True)
        C._pages[k]=Image.open(base+'.png').convert('RGB')
    return C._pages[k]
C.page_img=page_img
_f=C.find
def find(pdf,page,phrase,nth=1):
    if '@@' in phrase: phrase,nth=phrase.split('@@'); nth=int(nth)
    return _f(pdf,page,phrase,nth)
C.find=find
P={'sed':[('sedaily-oct24-gold.pdf',1,(36,170,600,236),[]),('sedaily-oct24-gold.pdf',1,(36,684,600,742),['fell below $4,000 an ounce','roughly 29%'])],
   'sedm':[('sedaily-oct24-gold.pdf',2,(36,327,600,402),['investors sell gold to meet margin calls when risk assets tumble,'])],
   'yah':[('yahoo-oct27-gold.pdf',1,(6,31,600,152),[]),('yahoo-oct27-gold.pdf',2,(6,22,600,150),['increase interest rates for the first time since 2023.'])],
   'bt63':[('bt-oct16-gold-2028.pdf',1,(36,112,340,187),[]),('bt-oct16-gold-2028.pdf',3,(36,415,330,524),['central banks purchased around 63 tonnes of gold in September,','the highest monthly level since November 2024.'])],
   'mcath':[('metalcharts-gold-ath.pdf',1,(122,140,600,159.5),['$5,590 per troy ounce, set on January 28, 2026.'])],
   'mctab':[('metalcharts-gold-ath.pdf',2,(42,465,600,612),['Sep 6, 2011','$1,921','Aug 7, 2020','~$2,075'])],
   'cern':[('cern-alice-substitute-home-cern.pdf',1,(34,145,600,284),['ALICE detects the conversion of lead into gold at the LHC'])],
   'andhra':[('bt-andhra-gold-rush-apr19-2026.pdf',1,(28,98,600,172),["India’s first private new mine@@2"])]}
out={}
for k,parts in P.items():
    im,h=C.build(parts)
    if k=='yah': h=[(a,d-0.47*(d-b),c,d+0.02*(d-b)) for a,b,c,d in h]
    im.save(f'clip_{k}.png'); out[k]={'hl':h}; print(k,im.size,len(h))
json.dump(out,open('clips.json','w'))
