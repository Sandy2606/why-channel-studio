import sys,json,numpy as np,scipy.io.wavfile as wf,subprocess
def load(name):
    sr,a=wf.read(f"/home/claude/long/rec/{name}.wav"); return sr,a.astype(np.float32)/32768
def env(a,sr):
    hop=sr//100; n=len(a)//hop
    db=20*np.log10(np.sqrt(np.mean(a[:n*hop].reshape(n,hop)**2,axis=1))+1e-9)
    return db, np.percentile(db,10)+14
def snap(db,thr,s,e,raw=False):
    v=db>thr; n=len(v)
    if raw: return s,e
    i=int(s*100); lo=max(0,i-30)
    # onset: walk back from s while voiced (max .3s), else walk forward to first voiced (max .25s)
    if v[min(i,n-1)]:
        while i>lo and v[i-1]: i-=1
    else:
        k=i
        while k<min(n,i+25) and not v[k]: k+=1
        if k<min(n,i+25): i=k
    j=int(e*100); hi=min(n,j+50)
    # end: walk forward until 12 consecutive silent frames
    while j<hi:
        if not v[j:j+12].any(): break
        j+=1
    return max(0,i/100-0.07), min(n/100,j/100+0.09)
def build(name,keep,out,gap=0.14,raw=False,chain=True):
    sr,a=load(name); db,thr=env(a,sr)
    parts=[];log=[]
    fade=int(0.012*sr)
    for k in keep:
        s,e=k[0],k[1]; r=raw or (len(k)>2 and k[2]=='raw')
        s2,e2=snap(db,thr,s,e,r)
        seg=a[int(s2*sr):int(e2*sr)].copy()
        seg[:fade]*=np.linspace(0,1,fade); seg[-fade:]*=np.linspace(1,0,fade)
        parts.append(seg); parts.append(np.zeros(int(gap*sr),np.float32)); log.append((s2,e2))
    y=np.concatenate(parts)
    wf.write(out+".raw.wav",sr,(y*32767).astype(np.int16))
    if chain:
        subprocess.run(["ffmpeg","-v","error","-y","-i",out+".raw.wav","-af","highpass=f=85,afftdn=nr=12:nf=-50,equalizer=f=3500:t=q:w=1.2:g=2,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=7","-ar","48000",out],check=True)
    t=0;mp=[]
    for (s2,e2) in log:
        mp.append((round(t,2),round(s2,2),round(e2,2))); t+=e2-s2+gap
    json.dump(mp,open(out+".map.json","w"))
    print(f"{out}: {t:.2f}s, {len(log)} pieces")
    return mp
