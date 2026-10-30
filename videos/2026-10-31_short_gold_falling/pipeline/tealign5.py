import json, re, numpy as np
SR=48000
SPOKEN_LEN={}
def splen(s):
    for k,v in SPOKEN_LEN.items(): s=s.replace(k,v)
    return len(s)
CAPMAP=[('ఇరవై ఐదు వేల','25,000'),('టాప్ పది','టాప్ 10'),('పది వేలు','10,000'),('పది వేల','10,000'),('ఒక లక్ష డెబ్బై ఏడు వేలు','₹1.77 లక్షలు'),('పద్దెనిమిది','18'),('ఏడు శాతం','7%'),('ముప్పై ఎనిమిది వేలు','₹38,000'),('ఒక dollar','$1'),('నలభై ఐదు రూపాయలు','₹45'),('తొంభై ఐదు','₹95'),('పదహారు లక్షల కోట్ల రూపాయలు','₹16 లక్షల కోట్లు')]
def cap(t):
    for k,v in CAPMAP: t=t.replace(k,v)
    return t
def align(x, units):
    hop=480; n=len(x)//hop; db=20*np.log10(np.sqrt((x[:n*hop].reshape(n,hop)**2).mean(1))+1e-9)
    v=db>np.percentile(db,15)+12; P=[];W=[];i=0
    while i<n:
        if not v[i]:
            j=i
            while j<n and not v[j]: j+=1
            if (j-i)/100>=0.12 and i>0 and j<n: P.append((i+j)/200); W.append((j-i)/100)
            i=j
        else: i+=1
    st=np.argmax(v)/100; en=(n-np.argmax(v[::-1]))/100
    L=np.array([splen(u) for u in units],float); K=len(units)-1; M=len(P); rate=(en-st)/L.sum()
    INF=1e18; dp=np.full((K+1,M+1),INF); bk=np.zeros((K+1,M+1),int); dp[0][0]=0; B=[st]+P
    for k in range(1,K+1):
        for m in range(1,M+1):
            for pm in range(0,m):
                if dp[k-1][pm]>=INF: continue
                d=B[m]-B[pm]; e=L[k-1]*rate; c=dp[k-1][pm]+((d-e)/max(e,.4))**2-1.2*W[m-1]
                if c<dp[k][m]: dp[k][m]=c; bk[k][m]=pm
    best=INF; bm=0
    for m in range(1,M+1):
        c=dp[K][m]+((en-B[m]-L[K]*rate)/(L[K]*rate))**2
        if c<best: best=c; bm=m
    seq=[]; m=bm
    for k in range(K,0,-1): seq.append(B[m]); m=bk[k][m]
    return [st]+seq[::-1], en
