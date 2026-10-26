import sys,numpy as np
from scipy.fftpack import dct
sys.path.insert(0,'/home/claude/long')
from asm import load,env
import scipy.io.wavfile as wf
def mfcc(x,sr=16000):
    x=np.append(x[0],x[1:]-0.97*x[:-1]); fl=400;hop=160
    n=1+(len(x)-fl)//hop
    idx=np.arange(fl)[None,:]+hop*np.arange(n)[:,None]
    fr=x[idx]*np.hamming(fl); P=np.abs(np.fft.rfft(fr,512))**2/512
    nf=26; mel=lambda f:2595*np.log10(1+f/700); imel=lambda m:700*(10**(m/2595)-1)
    pts=imel(np.linspace(mel(80),mel(7600),nf+2)); b=np.floor(513*pts/sr).astype(int)
    fb=np.zeros((nf,257))
    for m in range(1,nf+1):
        for k in range(b[m-1],b[m]): fb[m-1,k]=(k-b[m-1])/max(1,b[m]-b[m-1])
        for k in range(b[m],b[m+1]): fb[m-1,k]=(b[m+1]-k)/max(1,b[m+1]-b[m])
    E=np.log(P@fb.T+1e-10); C=dct(E,type=2,axis=1,norm='ortho')[:,1:14]
    return C
def norm(C): C=C-C.mean(0); return C/(C.std(0)+1e-6)
def dtw_prefix(A,B):
    n,m=len(A),len(B)
    d=np.sqrt(((A[:,None,:]-B[None,:,:])**2).sum(-1))
    D=np.full((n+1,m+1),np.inf); D[0,0]=0
    for i in range(1,n+1):
        r=D[i-1]; x=np.minimum(r[:-1],r[1:])+d[i-1]   # diag or vertical
        row=np.full(m+1,np.inf)
        acc=np.inf
        for j in range(1,m+1):
            acc=min(x[j-1],acc)+0 if False else min(x[j-1],(row[j-1]+d[i-1,j-1]))
            row[j]=acc
        D[i]=row
    j0=max(1,int(0.6*n)); j1=min(m,int(1.6*n)+1)
    if j0>j1: return 9e9,0
    c=D[n,j0:j1+1]/(n+np.arange(j0,j1+1)); k=int(np.argmin(c))
    return float(c[k]),j0+k
def segs(name,gap,minlen=0.2):
    sr,a=load(name); db,thr=env(a,sr); v=db>thr; n=len(v); G=int(gap*100); out=[];i=0
    while i<n:
        if v[i]:
            j=i
            while j<n and (v[j] or v[j:j+G].any()): j+=1
            if (j-i)/100>=minlen: out.append((i/100,j/100))
            i=j
        else: i+=1
    return out
if __name__=='__main__':
    name=sys.argv[1]; gap=float(sys.argv[2])
    _,a=wf.read(f"/home/claude/long/rec/{name}_16k.wav"); a=a.astype(np.float32)/32768
    S=segs(name,gap); M=norm(mfcc(a))
    feats=[M[int(s*100):int(e*100)] for s,e in S]
    for i,(s,e) in enumerate(S):
        best=[]
        for j in range(i+1,min(len(S),i+5)):
            A=feats[i][::2];B=feats[j][::2]
            if len(A)<5 or len(B)<5: continue
            c,k=dtw_prefix(A,B); best.append((c,j,k*2/100))
        tag=''
        if best:
            c,j,l=min(best); tag=f"-> best match seg{j} cost {c:.2f} (covers {l:.1f}s)"
        print(f"{i:3d} {s:7.2f}-{e:7.2f} ({e-s:4.1f}) {tag}",flush=True)
