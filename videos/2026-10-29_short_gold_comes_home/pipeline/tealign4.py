import json, re, numpy as np
SR=48000
TEXT=open('/home/claude/why-channel-studio/videos/2026-10-29_short_gold_comes_home/te.txt').read().strip().split('\n')
# caption units: script lines split at '...' and sentence ends, matched to TTS pieces
L1=['1991 లో India దాదాపు దివాలా అంచున ఉంది.','కొన్ని వారాల imports కి సరిపడా foreign money మాత్రమే మిగిలింది.']
BODY=['అప్పుడు government రహస్యంగా దాదాపు 47 టన్నుల gold ని విదేశాలకు పంపింది...','ఒక loan కి హామీగా.',
 'అది పనిచేసింది.','India గట్టెక్కింది.','ఇప్పుడు 2024 కి వద్దాం...','India సరిగ్గా రివర్స్ చేయడం మొదలుపెట్టింది.',
 'London నుంచి 100 టన్నులకు పైగా gold తిరిగి వచ్చింది...','దీపావళికి ముందు ఇంకో 102 టన్నులు.',
 '2023 లో RBI gold లో 38% మాత్రమే India లో ఉండేది...','March 2026 కి? దాదాపు 77.','మరి ఎందుకు ఇంటికి తెస్తున్నారు?',
 '2022 లో Western countries, వేరే దేశాల vaults లో ఉన్న','Russia కి చెందిన దాదాపు 300 billion dollars ని ఫ్రీజ్ చేశాయి.',
 'దాంతో చాలా దేశాలు ఒక పాఠం నేర్చుకున్నాయి...','మీ gold మీకు అందే చోటే ఉంచుకోండి.',
 '1991 లో దేశాన్ని కాపాడటానికి gold బయటికి వెళ్ళింది...','ఇప్పుడు దేశాన్ని రక్షించడానికి తిరిగి వస్తోంది.',
 'Gold full story మన channel లో ఇప్పుడే వచ్చింది.']
SPOKEN_LEN={'47':'నలభై ఏడు','100':'వంద','102':'నూట రెండు','38%':'ముప్పై ఎనిమిది శాతం','77.':'డెబ్బై ఏడు','300':'మూడు వందల'}
def splen(s):
    for k,v in SPOKEN_LEN.items(): s=s.replace(k,v)
    return len(s)
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
CTA={'yt':'ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం subscribe చేయండి.','ig':'ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం follow అవ్వండి.'}
COM='మీకు ఏదైనా why ఉంటే comment చేయండి, answer మేము వెతికి చెప్తాం.'
for plat in ('yt','ig'):
    M=json.load(open(f'map_te_{plat}.json')); raw=np.load(f'raw_te_{plat}.npy'); offs=M['offs']; cuts=M['cuts']; f8=int(.008*SR)
    def o(samp): return (samp-sum(min(b,samp)-a for a,b in cuts if a<samp)-f8*sum(1 for a,b in cuts if b<=samp))/SR/M['tempo']
    segs=[]
    for pi,units in ((0,L1),(2,BODY)):
        x=raw[offs[pi]:offs[pi+1]]; starts,en=align(x,units)
        ends=starts[1:]+[en]
        for u,s,e in zip(units,starts,ends): segs.append((offs[pi]+s*SR, offs[pi]+e*SR, u))
    segs.append((offs[4],offs[5],CTA[plat])); segs.append((offs[6],offs[7],COM))
    words=[]; sent=[]
    for a,b,t in segs:
        t0,t1=o(a),o(b); tk=t.replace('...','…').split(); Lw=np.array([max(2,len(w)) for w in tk],float); cum=np.concatenate([[0],np.cumsum(Lw)])/Lw.sum()
        sent.append(round(t0,3))
        for i,w in enumerate(tk): words.append([round(t0+(t1-t0)*cum[i],3),round(t0+(t1-t0)*cum[i+1],3),w])
    json.dump({'words':words,'sent':sent,'units':[s[2] for s in segs]},open(f'words_te_{plat}.json','w'),ensure_ascii=False)
    print(plat,len(sent),sent)
