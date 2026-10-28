import json, re, numpy as np, scipy.io.wavfile as wf
SR=48000; TEMPO=1.06
S=json.load(open('align.json'))['sent']
ST=[0.0,2.89,5.48,8.0,11.24,14.43,16.44,17.46,19.41,28.51,32.04,35.49,39.17,41.68,45.69,47.67,51.56,54.56,55.32,60.06,61.84,67.72,72.38]
EN=[2.45,5.06,7.63,10.66,14.02,16.01,17.0,18.95,27.93,31.47,35.01,38.68,41.09,45.17,47.27,51.09,54.05,54.96,59.57,61.39,67.21,71.87,75.0]
REPL=[('డెబ్బై తొమ్మిది','79'),('రెండు వేల పదమూడులో','2013లో'),('నూట ఐదు','105')]
def toks(s):
    for a,b in REPL: s=s.replace(a,b)
    s=s.replace('...','…')
    return s.split()
CTA_SUB='ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం subscribe చేయండి.'
CTA_FOL='ఇలాంటి విషయాలు నచ్చితే, రోజుకో కొత్త why కోసం follow అవ్వండి.'
COMT='మీకు ఏదైనా why ఉంటే comment చేయండి, answer మేము వెతికి చెప్తాం.'
for plat in ('yt','ig'):
    M=json.load(open(f'map_{plat}.json')); cuts=M['cuts']; f8=int(.008*SR)
    def o(samp): return (samp - sum(min(b,samp)-a for a,b in cuts if a<samp) - f8*sum(1 for a,b in cuts if b<=samp))/SR/TEMPO
    segs=[(ST[i]*SR,EN[i]*SR,S[i]) for i in range(len(S))]
    c=M['cta']; segs.append((M['off_cta'], M['off_cta']+(c[1]-c[0])*SR, CTA_SUB if plat=='yt' else CTA_FOL))
    m=M['com']; segs.append((M['off_com'], M['off_com']+(m[1]-m[0])*SR, COMT))
    words=[]; sent_starts=[]
    for a,b,txt in segs:
        t0,t1=o(a),o(b); tk=toks(txt); L=np.array([max(2,len(w)) for w in tk],float); cum=np.concatenate([[0],np.cumsum(L)])/L.sum()
        sent_starts.append(round(t0,3))
        for i,w in enumerate(tk): words.append([round(t0+(t1-t0)*cum[i],3), round(t0+(t1-t0)*cum[i+1],3), w])
    json.dump({'words':words,'sent':sent_starts},open(f'/home/claude/g3/words_te_{plat}.json','w'),ensure_ascii=False)
    print(plat, len(words), sent_starts[:5], sent_starts[-3:])
