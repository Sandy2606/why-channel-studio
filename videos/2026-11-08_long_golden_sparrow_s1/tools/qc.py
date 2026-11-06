import json,subprocess,numpy as np,sys
sys.path.insert(0,'/home/claude/gs')
from timing import *
SR=16000
def load(p):
    return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar',str(SR),'-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32)
def sil(x,thr=-45):
    hop=160;n=len(x)//hop;db=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9);v=db>thr
    idx=np.where(v)[0]; s,e=idx[0],idx[-1]
    # longest internal silence
    run=0;mx=0
    for b in v[s:e]:
        run=0 if b else run+1; mx=max(mx,run)
    return (e-s)*hop/SR, mx*hop/SR
jobs=json.load(open('jobs.json'))
rows={r['id']:r for r in L}
from shorts import NEW,BRIDGE
res=[]
for lang in ('en','te'):
    ids=[x['id'] for x in L if x['only'] in (None,lang) and (x['en'] if lang=='en' else x['te'])]
    ids+= [j['id'] for j in jobs if j['lang']==lang and j['id'] not in ids]
    for i in ids:
        x=load(f'rec/take/{lang}_{i}.mp3'); d,mx=sil(x)
        if i in rows: t=rows[i][lang]; role=rows[i]['role']
        else: t=next(j['text'] for j in jobs if j['lang']==lang and j['id']==i); role='EXP'
        est=spoken(t,lang,role)*TEMPO
        res.append(dict(lang=lang,id=i,dur=round(d,2),est=round(est,2),ratio=round(d/est,2),maxgap=round(mx,2)))
json.dump(res,open('rec/qc.json','w'),indent=0)
for r in res:
    if r['ratio']<0.8 or r['ratio']>1.3 or r['maxgap']>1.3: print(r)
for lang in ('en','te'):
    rr=[r for r in res if r['lang']==lang]; print(lang,'total speech',round(sum(r['dur'] for r in rr),1),'est',round(sum(r['est'] for r in rr),1))
