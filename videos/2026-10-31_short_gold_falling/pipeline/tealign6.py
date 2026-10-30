import json, numpy as np, subprocess
import tealign5 as TA
SR=48000; B=json.load(open('bounds.json')); U=B['teu']
SP={'5,590':'ఐదు వేల ఐదు వందల తొంభై','4,000':'నాలుగు వేల','30':'ముప్పై','2023':'రెండు వేల ఇరవై మూడు','63':'అరవై మూడు','2011':'రెండు వేల పదకొండు','2020':'రెండు వేల ఇరవై','2006':'రెండు వేల ఆరు','17':'పదిహేడు'}
TA.SPOKEN_LEN.update(SP)
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar',str(SR),'-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
for plat in ('yt','ig'):
    x=load(f'voice_te_{plat}.wav'); mk=json.load(open(f'marks_te_{plat}.json')); words=[]; sent=[]; units=[]
    for k,(a,b) in mk.items():
        us=U[k]; seg=x[int(a*SR):int(b*SR)]
        if len(us)>1: st,en=TA.align(seg,us); ends=st[1:]+[en]
        else: st,ends=[0.0],[len(seg)/SR]
        for u,s,e in zip(us,st,ends):
            t0,t1=a+s,a+e; tk=u.replace('...','…').split(); Lw=np.array([max(2,len(w)) for w in tk],float); cum=np.concatenate([[0],np.cumsum(Lw)])/Lw.sum()
            sent.append(round(t0,3)); units.append(u)
            for i,w in enumerate(tk): words.append([round(t0+(t1-t0)*cum[i],3),round(t0+(t1-t0)*cum[i+1],3),w])
    json.dump({'words':words,'sent':sent,'units':units},open(f'words_te_{plat}.json','w'),ensure_ascii=False)
    print(plat,len(sent),[round(s,1) for s in sent])
