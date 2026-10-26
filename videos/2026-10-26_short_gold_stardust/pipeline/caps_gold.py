# Word-level caption timings for Gold Short 1
import json, os, numpy as np, scipy.io.wavfile as wf
ROOT = '/home/claude/gold1/'
PLAT = os.environ.get('PLAT', 'yt')

EN_FIX = {'can': "can't", 'mined': 'mine', 'everyday.': 'every day.', 'your': None}

TE_A = ["మీ ఉంగరంలో ఉన్న గోల్డ్", "అసలు భూమ్మీద పుట్టలేదు", "మన సూర్యుడిలో కూడా కాదు", "తెలుసుకుందాం రండి",
        "స్టార్స్ ఏం చేస్తాయంటే", "చిన్న చిన్న ఆటమ్స్‌ని నొక్కి కలిపేసి", "కొత్తవి తయారు చేస్తాయి", "హైడ్రోజన్ నుంచి హీలియం",
        "హీలియం నుంచి కార్బన్", "అలా ఐరన్ వరకు వెళ్తాయి", "అక్కడితో ఆగిపోతాయి", "గోల్డ్ ఐరన్ కంటే చాలా హెవీ",
        "అందుకే మన సూర్యుడు ఒక చిన్న ముక్క గోల్డ్ కూడా తయారు చేయలేడు", "మరి గోల్డ్ ఎక్కడి నుంచి వచ్చింది?",
        "ఒక పెద్ద స్టార్ చనిపోయినప్పుడు అది న్యూట్రాన్ స్టార్‌గా మారిపోతుంది", "అది ఎంత డెన్స్ అంటే", "ఒక చక్కెర ముక్క అంత దాని బరువు",
        "వంద కోట్ల టన్నుల కంటే ఎక్కువ", "ఇప్పుడు ఇలాంటి రెండు చనిపోయిన స్టార్స్", "ఒకదాని చుట్టూ ఒకటి తిరుగుతూ",
        "ఇంకా ఫాస్ట్‌గా ఇంకా ఫాస్ట్‌గా చివరికి ఢీ కొట్టుకుంటాయి", "2017లో సైంటిస్ట్స్ నిజంగా అలాంటిది ఒకటి పట్టుకున్నారు",
        "మనకి పదమూడు కోట్ల లైట్ ఇయర్స్ దూరంలో",
        "ఆ పేలుడు వెలుగు చూసి వాళ్ళకి అర్థమైంది అప్పుడే అక్కడ గోల్డ్ ప్లాటినం లాంటి హెవీ మెటల్స్ పుట్టాయని",
        "కానీ ఇక్కడే ట్విస్ట్ ఉంది", "భూమి కొత్తగా పుట్టినప్పుడు దాని గోల్డ్ దాదాపు అంతా లోపల కోర్‌లోకి మునిగిపోయింది",
        "మరి మనం ఇప్పుడు తవ్వుతున్న గోల్డ్", "అది తర్వాత ఆకాశం నుంచి మీటియోరైట్స్‌తో పడింది", "అంటే మీ ఉంగరంలో ఉన్న గోల్డ్",
        "మన భూమి కంటే పాతది", "అది నిజంగా", "స్టార్స్ నుంచి వచ్చిన ధూళి", "కానీ స్పేస్‌లో ఇంత గోల్డ్ పుడితే",
        "ఇక్కడ ఎందుకింత కాస్ట్లీ?", "ఫుల్ వీడియో బుధవారం వస్తుంది"]
TE_F = ["ఇలాంటి విషయాలు నచ్చితే", "రోజుకో కొత్త why కోసం ఫాలో అవ్వండి"]
TE_S = ["ఇలాంటి కొత్త విషయాలు నచ్చితే రోజుకో కొత్త why కోసం సబ్‌స్క్రైబ్ చేసుకోండి"]
TE_C = ["మీకు ఏదైనా 'ఎందుకు' అనే ప్రశ్న ఉంటే కింద కామెంట్ చేయండి", "ఆన్సర్ మేము వెతికి చెప్తాం"]
TE_LINES = TE_A + (TE_F if PLAT == 'ig' else TE_S) + TE_C

def piece_starts(lang):
    return [m[0] for m in json.load(open(ROOT + f'voice_{lang}_{PLAT}.wav.map.json'))]

def words(lang):
    if lang == 'en':
        ws = json.load(open(ROOT + f'ven_{PLAT}.words.json')); out = []
        for i, (s, e, w) in enumerate(ws):
            nx = ws[i + 1][2] if i + 1 < len(ws) else ''
            if w == 'your' and nx == 'new': w = 'a'
            elif w == 'can' and nx != 'make': pass
            elif w in EN_FIX and w != 'your': w = EN_FIX[w]
            out.append((s, e, w))
        return out
    sr, a = wf.read(ROOT + f'voice_te_{PLAT}.wav'); a = a.astype(np.float32) / 32768
    if a.ndim > 1: a = a.mean(1)
    hop = sr // 100; n = len(a) // hop
    db = 20 * np.log10(np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-9); vo = db > np.median(db) - 20
    starts = piece_starts('te') + [n / 100]
    assert len(starts) - 1 == len(TE_LINES), (len(starts), len(TE_LINES))
    out = []
    for i, line in enumerate(TE_LINES):
        s, e = starts[i], starts[i + 1]
        fr = np.where(vo[int(s * 100):int(e * 100)])[0] / 100 + s
        if len(fr) == 0: fr = np.array([s, e])
        ws = line.split(); L = np.array([max(2, len(w)) for w in ws], float); c = np.concatenate([[0], np.cumsum(L) / L.sum()])
        for j, w in enumerate(ws):
            t0 = fr[min(len(fr) - 1, int(c[j] * (len(fr) - 1)))]; t1 = fr[min(len(fr) - 1, int(c[j + 1] * (len(fr) - 1)))]
            out.append((float(t0), float(max(t1, t0 + .12)), w, j == len(ws) - 1))
    return out

def chunks(ws, maxw=3, maxc=20):
    C = []; cur = []
    for k, x in enumerate(ws):
        cur.append(x); txt = ' '.join(y[2] for y in cur)
        nxt = ws[k + 1] if k + 1 < len(ws) else None
        brk = (len(x) > 3 and x[3]) or len(cur) >= maxw or len(txt) >= maxc or x[2][-1] in '.,?!' or (nxt and nxt[0] - x[1] > .35)
        if nxt and len(txt + ' ' + nxt[2]) > maxc + 4: brk = True
        if brk or not nxt: C.append(cur); cur = []
    out = []
    for i, c in enumerate(C):
        s = c[0][0]; e = C[i + 1][0][0] if i + 1 < len(C) else c[-1][1] + .4
        out.append((s, min(e, c[-1][1] + .6), c))
    return out
