# Word-level caption timings for the Saturday Short
import json, numpy as np, scipy.io.wavfile as wf
ROOT = '/home/claude/sun/'
import os
PLAT = os.environ.get('PLAT', 'yt')
EN_FIX = {5: "Ravana's", 6: None, 7: 'effigy.', 23: 'Dussehra?', 31: 'Ramlila.', 32: None, 50: 'Ramcharitmanas,', 51: None, 65: 'Ramlila', 66: None,
          68: "world", 69: 'heritage.', 70: None, 73: 'Ramnagar,', 74: None, 90: 'Ravana', 117: 'together.', 121: 'heads?', 133: 'us:',
          134: 'anger,', 135: 'greed,', 136: 'ego,', 137: 'jealousy.', 144: 'burn', 146: 'year,', 147: 'remember,'}
EN_FIX_IG = {148: 'the Ravana', 159: 'us.', 164: 'Dussehra', 170: 'now.', 171: 'follow', 178: 'why', 180: 'day.', 193: 'below.'}
EN_FIX_YT = {148: 'the', 149: 'Ravana', 160: 'us.', 165: 'Dussehra', 171: 'now.', 179: 'why', 181: 'day.', 194: 'below.'}
TE_LINES = ["రామాయణంలో రావణుడి బొమ్మని కాల్చడం అనేది ఎక్కడా లేదు.", "ఒక్కసారి కూడా.", "తెలుసా మీకు?", "మరి ప్రతి దసరాకి మనం ఎందుకు కాలుస్తాం?",
    "తెలుసుకుందాం రండి.", "ఇదంతా రామ్‌లీలా నుంచే వచ్చింది.", "నార్త్ ఇండియా అంతా స్టేజ్‌ల మీద ఆడే రామాయణ నాటకం ఇది.", "చాలా రామ్‌లీలలు",
    "1500ల్లో తులసీదాస్ రాసిన", "రామచరితమానస్ ఆధారంగా జరుగుతాయి.", "ఇది ఎంత స్పెషల్ అంటే, UNESCO రామ్‌లీలాని వరల్డ్ హెరిటేజ్‌గా గుర్తించింది.",
    "వారణాసి దగ్గర రామ్‌నగర్‌లో అది నెల మొత్తం జరుగుతుంది.", "ఇప్పుడు ఆలోచించండి, ఆ నాటకం ఎలా ముగుస్తుంది?", "రావణుడి మరణంతో.",
    "అందుకే చివరి రాత్రి ఆ సీన్ నటించడమే కాదు,", "తగలబెడతారు.", "ఊరంతా కలిసి చెడు అంతమవడం చూడాలని.", "మరి ఆ పది తలలు?",
    "అవి మనలో ఉండే పది చెడు గుణాలు అని చాలా మంది చెప్తారు.", "కోపం,", "అత్యాశ, అహంకారం, అసూయ.", "అందుకే ఈసారి బొమ్మ కాలుతుంటే", "గుర్తుపెట్టుకోండి:",
    "మనం నిజంగా కాల్చాల్సింది మనలో ఉన్న రావణుణ్ణి.", "దసరా పూర్తి కథ మన ఛానెల్‌లో", "ఇప్పుడే ఉంది.",
    "రోజూ ఒక కొత్త 'ఎందుకు' కోసం FOLLOW చేయండి.",
    "ఇక మీకు 'ఎందుకు' అని మొదలయ్యే ఏ ప్రశ్న వచ్చినా కింద కామెంట్ చేయండి.", "మేము రీసెర్చ్ చేసి మీకు ఆన్సర్ చెప్తాం."]
TE_LINES[26] = TE_LINES[26].replace('FOLLOW', 'ఫాలో' if PLAT == 'ig' else 'సబ్‌స్క్రైబ్')

def words(lang):
    if lang == 'en':
        ws = json.load(open(ROOT + f'ven_{PLAT}.words.json')); fx = dict(EN_FIX); fx.update(EN_FIX_IG if PLAT == 'ig' else EN_FIX_YT)
        return [(s, e, fx.get(i, w)) for i, (s, e, w) in enumerate(ws) if fx.get(i, w) is not None]
    sr, a = wf.read(ROOT + f'voice_te_{PLAT}.wav'); a = a.astype(np.float32) / 32768
    if a.ndim > 1: a = a.mean(1)
    hop = sr // 100; n = len(a) // hop
    db = 20 * np.log10(np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, 1)) + 1e-9); vo = db > np.median(db) - 20
    mp = json.load(open(ROOT + f'voice_te_{PLAT}.wav.map.json')); starts = [m[0] for m in mp] + [n / 100]
    out = []
    for i, line in enumerate(TE_LINES):
        s, e = starts[i], starts[i + 1]
        fr = np.where(vo[int(s * 100):int(e * 100)])[0] / 100 + s          # voiced frames in this piece
        if len(fr) == 0: fr = np.array([s, e])
        ws = line.split(); L = np.array([max(2, len(w)) for w in ws], float); c = np.concatenate([[0], np.cumsum(L) / L.sum()])
        for j, w in enumerate(ws):
            t0 = fr[min(len(fr) - 1, int(c[j] * (len(fr) - 1)))]; t1 = fr[min(len(fr) - 1, int(c[j + 1] * (len(fr) - 1)))]
            out.append((float(t0), float(max(t1, t0 + .12)), w, j == len(ws) - 1))
    return out

def chunks(ws, maxw=3, maxc=20):
    """group words into on-screen caption chunks: (start, end, [(s,e,w)...])"""
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
