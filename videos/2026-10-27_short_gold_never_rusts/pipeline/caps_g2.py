# Word-level caption timings for Gold Short 1
import json, os, numpy as np, scipy.io.wavfile as wf
ROOT = '/home/claude/gold2/'
PLAT = os.environ.get('PLAT', 'yt')

EN_FIX = {'rusty': 'rust', 'way': 'why', 'Gold': "Gold's", 'packed': 'pack', 'lap': 'lab', 'right.': 'right?', 'trust,': 'rust,', 'medals': 'medals'}

TE_A = ["ఒక్కసారి గోల్డ్ మాస్క్ చూడండి", "దీని వయసు 3,300 ఏళ్ళకి పైనే", "కానీ ఇప్పుడే పాలిష్ చేసినట్టు మెరిసిపోతోంది",
        "ఒక ఐరన్ మేకుని బయట కొన్ని నెలలు వదిలేస్తే చాలు", "తుప్పు పట్టేస్తుంది", "గోల్డ్‌కి మాత్రం ఎప్పటికీ పట్టదు",
        "దీని వెనక రీజన్ చాలా ఇంట్రెస్టింగ్", "తుప్పు అంటే సింపుల్‌గా ఆక్సిజన్ ఒక మెటల్‌ని పట్టుకుని నెమ్మదిగా తినేయడం",
        "ఐరన్ వెంటనే లొంగిపోతుంది", "కానీ గోల్డ్ తన ఎలక్ట్రాన్స్‌ని గట్టిగా పట్టుకుని ఉంటుంది", "ఆక్సిజన్‌కి అసలు పట్టు దొరకదు",
        "ఇంకా నాకు షాకింగ్ అనిపించింది ఏంటంటే", "ఈ సంవత్సరమే సైంటిస్ట్స్ ఇంకో ట్రిక్ కనిపెట్టారు", "గోల్డ్ పైన ఆటమ్స్",
        "ఒక టైట్ హెక్సాగన్ లాగా దగ్గరగా అతుక్కుని ఉంటాయి", "ఎంత టైట్ అంటే ఆక్సిజన్ విడిపోయి దాడి చేయడానికి కూడా ఛాన్స్ ఉండదు",
        "అలా అని గోల్డ్‌ని ఏదీ ఏమీ చేయలేదని కాదు", "ఒక ద్రవం దాన్ని కరిగించగలదు", "దాని పేరు ఆక్వా రేజియా", "అంటే రాజ ద్రవం",
        "రెండు స్ట్రాంగ్ యాసిడ్స్ కలిపిన మిశ్రమం", "ఇక్కడ నాకు బాగా నచ్చిన స్టోరీ వస్తుంది", "1940లో", "నాజీస్", "డెన్మార్క్ మీద దాడి చేశారు",
        "కోపెన్‌హాగెన్‌లో సైంటిస్ట్స్ దగ్గర రెండు గోల్డ్ మెడల్స్ ఉన్నాయి", "వాటిని దాచాలి", "వాళ్ళేం చేశారో తెలుసా?",
        "వాటిని ఆక్వా రేజియాలో కరిగించేసి", "ఆ జార్‌ని అలాగే ల్యాబ్ షెల్ఫ్ మీద పెట్టేశారు", "యుద్ధం మొత్తం అది అక్కడే ఉంది",
        "ఎవరూ పట్టించుకోలేదు", "యుద్ధం అయిపోయాక ఆ గోల్డ్‌ని మళ్ళీ బయటికి తీసి", "మెడల్స్‌ని మళ్ళీ తయారు చేశారు",
        "గోల్డ్ నిజంగానే తిరిగి వచ్చింది", "తుప్పు పట్టదు", "రంగు పోదు", "కరిగించినా తిరిగి వస్తుంది",
        "ఇంత కాస్ట్లీగా ఉండడంలో ఆశ్చర్యం లేదు కదా", "గోల్డ్ ఫుల్ స్టోరీ రేపు వీడియోలో చెప్తా", "మిస్ అవ్వకండి"]
TE_F = ["ఇలాంటి విషయాలు నచ్చితే", "రోజుకో కొత్త why కోసం ఫాలో అవ్వండి"]
TE_S = ["ఇలాంటి విషయాలు నచ్చితే రోజుకో కొత్త why కోసం సబ్‌స్క్రైబ్ అవ్వండి"]
TE_C = ["మీకు ఏదైనా why ఉంటే కామెంట్ చేయండి", "ఆన్సర్ మేము వెతికి చెప్తాం"]
TE_LINES = TE_A + (TE_F if PLAT == 'ig' else TE_S) + TE_C

def piece_starts(lang):
    return [m[0] for m in json.load(open(ROOT + f'voice_{lang}_{PLAT}.wav.map.json'))]

def words(lang):
    if lang == 'en':
        ws = json.load(open(ROOT + f'ven_{PLAT}.words.json')); out = []
        for i, (s, e, w) in enumerate(ws):
            nx = ws[i + 1][2] if i + 1 < len(ws) else ''
            if w == 'your' and nx == 'new': w = 'a'
            elif w == 'your' and nx == 'lap': w = 'the'
            elif w == 'Gold' and nx != 'surface': pass
            elif w in EN_FIX and w != 'your': w = EN_FIX[w]
            if w == 'video' and nx == 'every': w = 'why'
            if w == 'cold.': w = 'cool.'
            if w.startswith(',') and out: ps, pe, pw = out.pop(); out.append((ps, e, pw + w)); continue
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
