# TE word timing from ASR chunks: align script characters to ASR characters, each script word inherits its chunk; distribute inside chunk by voiced frames
import json, difflib, subprocess, numpy as np, re
L=json.load(open('lines.json'))['te']; M=json.load(open('marks_te.json')); C=json.load(open('asr_te_chunks.json'))
a=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i','voice_te.wav','-ac','1','-ar','16000','-f','f32le','-'],capture_output=True).stdout,np.float32)
hop=160; n=len(a)//hop; V=np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1))>0.012
keep=lambda s: re.sub(r'[^ఀ-౿0-9]','',s)
# ASR char stream with chunk ids
asr=''; aid=[]
for i,(s,e,t) in enumerate(C):
    k=keep(t); asr+=k; aid+=[i]*len(k)
words=[]   # (key, word, s_line, e_line)
for k,(s,e) in M.items():
    if k=='SLIDE': continue
    for w in L[k].split(): words.append((k,w,s,e))
scr=''; sid=[]
for j,(k,w,s,e) in enumerate(words):
    kk=keep(w) or 'x'; scr+=kk; sid+=[j]*len(kk)
sm=difflib.SequenceMatcher(None,scr,asr,autojunk=False); chunk_of=[None]*len(words)
votes=[dict() for _ in words]
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal' or tag=='replace':
        for d in range(min(i2-i1,j2-j1)):
            wj=sid[i1+d]; c=aid[j1+d]; votes[wj][c]=votes[wj].get(c,0)+1
for j,v in enumerate(votes):
    if v: chunk_of[j]=max(v,key=v.get)
# fill gaps; keep monotonic; clamp chunk inside the word's own line span
for j in range(len(words)):
    if chunk_of[j] is None: chunk_of[j]=chunk_of[j-1] if j else 0
for j in range(1,len(words)):
    if chunk_of[j]<chunk_of[j-1]: chunk_of[j]=chunk_of[j-1]
out=[]
groups={}
for j,(k,w,s,e) in enumerate(words): groups.setdefault((k,chunk_of[j]),[]).append(j)
for (k,c),js in sorted(groups.items(),key=lambda x:x[1][0]):
    s,e=M[k]; cs,ce=C[c][0],C[c][1]; s2,e2=max(s,cs),min(e,ce)
    if e2-s2<0.15: s2,e2=s,e
    fr=[i for i in range(int(s2*100),int(e2*100)) if i<len(V) and V[i]] or list(range(int(s2*100),int(e2*100)))
    wl=np.array([len(words[j][1]) for j in js],float); cum=np.concatenate([[0],np.cumsum(wl)])/wl.sum()
    for i,j in enumerate(js):
        a_=fr[min(len(fr)-1,int(cum[i]*len(fr)))]/100; b_=fr[min(len(fr)-1,max(0,int(cum[i+1]*len(fr))-1))]/100
        out.append([round(a_,3),round(b_+.01,3),words[j][1],k])
out.sort(key=lambda x:x[0]); json.dump(out,open('words_te.json','w'),ensure_ascii=False)
s=M['PILOT'][0]; print([(round(a-s,1),x) for a,b,x,k in out if k=='PILOT'][::3])
