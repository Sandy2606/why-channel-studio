import re, json, numpy as np, scipy.io.wavfile as wf
SR=48000
sr,a=wf.read('take2.wav'); a=a.astype(np.float32)/32768
hop=480; n=len(a)//hop; db=20*np.log10(np.sqrt((a[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
thr=np.percentile(db,12)+12; v=db>thr
# pauses >= 0.18s inside body
pauses=[]; i=0
while i<n:
    if not v[i]:
        j=i
        while j<n and not v[j]: j+=1
        if (j-i)/100>=0.18 and i>0 and j<n and i/100<75.0: pauses.append(((i+j)/200,(j-i)/100))
        i=j
    else: i+=1
t=open('tts_body.txt').read().strip()
S=[x.strip() for x in re.split(r'(?<=[.?!])\s+|(?<=\.\.\.)\s*',t) if x.strip()]
L=np.array([len(x) for x in S],float); tot_end=75.0
# speech start/end
st=np.argmax(v)/100
# DP: choose len(S)-1 pauses (ordered) to make segment durations ~ proportional to chars, rewarding long pauses
P=[p[0] for p in pauses]; Wt=[p[1] for p in pauses]; K=len(S)-1; M=len(P)
rate=(tot_end-st)/L.sum()
INF=1e18; dp=np.full((K+1,M+1),INF); bk=np.zeros((K+1,M+1),int)
# dp[k][m]: k boundaries placed, last at pause m-1 (m=0 means start)
dp[0][0]=0
bounds=[st]+P
for k in range(1,K+1):
    for m in range(1,M+1):
        best=INF
        for pm in range(0,m):
            if dp[k-1][pm]>=INF: continue
            d=bounds[m]-bounds[pm]; exp=L[k-1]*rate
            cost=dp[k-1][pm]+((d-exp)/max(exp,0.5))**2 - 0.8*Wt[m-1]
            if cost<best: best=cost; bk[k][m]=pm
        dp[k][m]=best
# close last segment
bestm=None;best=INF
for m in range(1,M+1):
    d=tot_end-bounds[m]; exp=L[K]*rate; c=dp[K][m]+((d-exp)/exp)**2
    if c<best: best=c; bestm=m
seq=[]; m=bestm
for k in range(K,0,-1): seq.append(bounds[m]); m=bk[k][m]
seq=seq[::-1]
starts=[st]+seq
for i,(x,s) in enumerate(zip(S,starts)): print(i,round(s,2),x[:40])
json.dump({'sent':S,'starts':starts},open('align.json','w'),ensure_ascii=False)
