import json, difflib, re, subprocess, numpy as np
L=json.load(open('lines.json'))
def norm(w): return re.sub(r"[^a-z0-9%]","",w.lower().replace('percent','%'))
def voiced(l):
    a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f'voice_{l}.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
    hop=160; n=len(a)//hop; r=np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1)); return r>0.012
for l in ('en','te'):
    M=json.load(open(f'marks_{l}.json')); out=[]
    if l=='en':
        Wh=json.load(open('whisper_en.json'))
        for k,(s,e) in M.items():
            if k=="SLIDE": continue
            sw=L[l][k].split(); ww=[w for w in Wh if w[0]>=s-0.15 and w[1]<=e+0.15]
            a=[norm(w) for w in sw]; b=[norm(w[2]) for w in ww]; tm=[None]*len(sw)
            for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
                if tag=='equal':
                    for d in range(i2-i1): tm[i1+d]=(ww[j1+d][0],ww[j1+d][1])
            # interpolate gaps
            for i in range(len(sw)):
                if tm[i] is None:
                    p=next((tm[j][1] for j in range(i-1,-1,-1) if tm[j]),s); q=next((tm[j][0] for j in range(i+1,len(sw)) if tm[j]),e)
                    run=[j for j in range(i,len(sw)) if tm[j] is None]; run=run[:next((n for n,j in enumerate(run) if j!=i+n),len(run))]
                    st=(q-p)/len(run)
                    for n,j in enumerate(run): tm[j]=(p+n*st,p+(n+1)*st)
            out+=[[round(a_,3),round(b_,3),w,k] for (a_,b_),w in zip(tm,sw)]
    else:
        V=voiced(l)
        for k,(s,e) in M.items():
            if k=="SLIDE": continue
            sw=L[l][k].split(); fr=[i for i in range(int(s*100),int(e*100)) if i<len(V) and V[i]]
            if not fr: fr=list(range(int(s*100),int(e*100)))
            wl=np.array([len(w) for w in sw],float); cum=np.concatenate([[0],np.cumsum(wl)])/wl.sum()
            for i,w in enumerate(sw):
                a_=fr[min(len(fr)-1,int(cum[i]*len(fr)))]/100; b_=fr[min(len(fr)-1,max(0,int(cum[i+1]*len(fr))-1))]/100
                out.append([round(a_,3),round(b_+0.01,3),w,k])
    json.dump(out,open(f'words_{l}.json','w'),ensure_ascii=False); print(l,len(out),out[:3],out[-2:])
