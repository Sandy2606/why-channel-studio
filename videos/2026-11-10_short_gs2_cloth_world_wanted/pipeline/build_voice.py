import json, subprocess, numpy as np, scipy.io.wavfile as wf
SR=48000; VD='/home/claude/why-channel-studio/videos/2026-11-10_short_gs2_cloth_world_wanted/voice/'
SRC={l:f'/home/claude/gs/out/{l}/GS_S1_S2_{l.upper()}_voice.wav' for l in ('en','te')}
def load(f,ss=None,to=None):
    cmd=['ffmpeg','-v','error','-i',f]+(['-ss',str(ss)] if ss is not None else [])+(['-to',str(to)] if to is not None else [])+['-ac','1','-ar',str(SR),'-f','f32le','-']
    return np.frombuffer(subprocess.run(cmd,capture_output=True).stdout,np.float32).copy()
def rms(a):
    x=a[np.abs(a)>0.02]; return float(np.sqrt(np.mean(x**2))) if len(x) else 1e-3
SPLIT={'en':4.88,'te':4.67}
ORDER={'en':['0.1','Q1','B2','2.2','2.3','Q2','2.4','2.5','2.6','2.8','2.9','2.10','Q3','2.11','2.12','2.13','2.14','2.15','T','tease2','SLIDE','L'],
       'te':['0.1','Q1','B2','2.2','2.3','Q2','2.4','2.5','2.6','2.7','2.8','2.10','Q3','2.11','2.12','2.13','2.14','T','tease2','SLIDE','L']}
for l in ('en','te'):
    d=[x for x in json.load(open(f'/home/claude/gs/out/shorts_{l}.json')) if x['short']=='S2'][0]
    seg={s[0]:(s[1],s[2]) for s in d['segments']}; keys=[s[0] for s in d['segments']]
    ref=load(SRC[l]); R=rms(ref); out=[]; marks={}; t=0.0; order=ORDER[l]
    for i,k in enumerate(order):
        nxt=order[i+1] if i+1<len(order) else None
        if k=='SLIDE': a=np.zeros(int(2.0*SR),np.float32); g=0.0
        elif k in ('Q1','Q2','Q3','L'):
            a=load(VD+f'{l}_{k}_trim.wav'); a*=R/rms(a); f=int(.01*SR); a[:f]*=np.linspace(0,1,f); a[-f:]*=np.linspace(1,0,f); g=0.40 if k!='L' else 0.30
        elif k=='T': s,e=seg['S2_tease']; a=load(SRC[l],s,s+SPLIT[l]); g=0.0
        elif k=='tease2': s,e=seg['S2_tease']; a=load(SRC[l],s+SPLIT[l],e); g=0.20
        else:
            s,e=seg[k]; a=load(SRC[l],s,e)
            if nxt in ('Q1','Q2','Q3'): g=0.25
            else:
                j=keys.index(k); g=(seg[keys[j+1]][0]-e) if j+1<len(keys) else 0.3
                g=min(max(g,0.15),0.5)
        marks[k]=[round(t,3),round(t+len(a)/SR,3)]; out+= [a,np.zeros(int(g*SR),np.float32)]; t+=len(a)/SR+g
    v=np.clip(np.concatenate(out),-1,1); wf.write(f'voice_{l}.wav',SR,(v*32767).astype(np.int16)); json.dump(marks,open(f'marks_{l}.json','w'))
    print(l,round(t,2),'=',f'{int(t//60)}:{t%60:04.1f}')
