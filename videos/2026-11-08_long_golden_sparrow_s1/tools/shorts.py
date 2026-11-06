import sys; sys.path.insert(0, '/home/claude/gs')
from timing import *

# New pick-up lines recorded only for Shorts (hook / bridge / tease). 'REUSE:<id>' = no new recording.
NEW = {
 'S1': dict(
   hook=('REUSE:1.1', 'REUSE:1.1'),
   reuse=['1.3', '1.4', '1.4e', '1.5', '1.6', '1.7', '1.8'],
   tease=("The answer: a cloth so good that Britain **banned** it. ⏸ That's the next episode. The full film is linked.",
          "దానికి జవాబు: బ్రిటన్ **నిషేధించేంత** గొప్ప గుడ్డ. ⏸ అది తర్వాతి ఎపిసోడ్‌లో. పూర్తి సినిమా link లో ఉంది.")),
 'S2': dict(
   hook=('REUSE:0.1', 'REUSE:0.1'),
   reuse=['B2', '2.2', '2.3', '2.4', '2.5', '2.6', '2.7', '2.8', '2.9', '2.10', '2.11', '2.12', '2.13', '2.14', '2.15'],
   tease=("Where did the world come to **buy** this cloth? ⏸ A port on India's east coast. ⏸ Next episode. The full film is linked.",
          "ఈ గుడ్డ కొనడానికి ప్రపంచం ఎక్కడికి వచ్చేది? ⏸ మన **మచిలీపట్నం**. ⏸ తర్వాతి ఎపిసోడ్. పూర్తి సినిమా link లో ఉంది.")),
 'S3': dict(
   hook=("One Indian kingdom supplied many of the world's most **famous diamonds**. ⏸ But its biggest business was something **else**.",
         "ప్రపంచ ప్రసిద్ధ వజ్రాలు ఎన్నో **గోల్కొండ** నుంచే. ⏸ కానీ అసలు సంపద **వేరే**."),
   reuse=['3.2', '3.3', '3.4', '3.5', '3.6', '3.7', '3.8', '3.9', '3.10', 'B3'],
   tease=("And with every bale, someone took a **cut**. ⏸ Who really controlled the wealth? ⏸ Next episode. The full film is linked.",
          "మరి ప్రతి మూటలో ఎవరో ఒకరు **వాటా** తీసుకున్నారు. ⏸ సంపద అసలు ఎవరి చేతిలో? ⏸ తర్వాతి ఎపిసోడ్. పూర్తి సినిమా link లో ఉంది.")),
 'S4': dict(
   hook=("India made almost a quarter of the world's output. ⏸ So why did so many of the people who made it stay **poor**?",
         "ప్రపంచ ఉత్పత్తిలో దాదాపు నాలుగో వంతు మనదే. ⏸ మరి దాన్ని తయారుచేసినవాళ్లలో ఎంతోమంది ఎందుకు **పేదవాళ్లుగానే** ఉండిపోయారు?"),
   reuse=['4.2', '4.3', '4.4', '4.5', '4.6', '4.7', '4.8', '4.9', '4.10', '4.11'],
   tease=("And the richest trade of all came by **sea**. ⏸ Next: who showed **Vasco da Gama** the way? ⏸ The full film is linked.",
          "అతి ధనిక వ్యాపారం **సముద్రం** మీదుగా వచ్చేది. ⏸ తర్వాత: వాస్కో డ గామాకి **దారి** చూపించింది ఎవరు? ⏸ పూర్తి సినిమా link లో ఉంది.")),
 'S5': dict(
   hook=("Vasco da Gama didn't **discover** India. ⏸ The ocean he sailed into had been busy for **centuries**… and someone had to show him the **way**.",
         "వాస్కో డ గామా భారత్‌ను **కనిపెట్టలేదు**. ⏸ ఎవరో **దారి** చూపించారు."),
   reuse=['5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9', '5.10'],
   tease=("Next: the company that came asking **permission**… and ended up giving **orders**. ⏸ The full film is linked.",
          "తర్వాత: **అనుమతి** అడిగి వచ్చిన కంపెనీ… **ఆజ్ఞలు** ఇచ్చే స్థాయికి ఎలా చేరింది? ⏸ పూర్తి సినిమా link లో ఉంది.")),
 'S6': dict(
   hook=("It came to India asking **permission**. ⏸ A hundred and fifty years later, it helped put a **Nawab** on Bengal's throne.",
         "**అనుమతి** అడిగి వచ్చిన కంపెనీ… నూట యాభై ఏళ్ల తర్వాత బెంగాల్ **నవాబునే** మార్చేసింది."),
   reuse=['6.3:en', '6.8b', '6.9', '6.10', '6.12', '6.13', '7.2', '7.3', '7.4', '7.5', 'B6', '7.9'],
   tease=("That's where **Season 2** begins. ⏸ The full film is linked.",
          "అక్కడి నుంచే **సీజన్ 2** మొదలవుతుంది. ⏸ పూర్తి సినిమా link లో ఉంది.")),
}

BRIDGE = {'B2': ("The answer starts in India's **weaving villages**, with the hands that made the cloth.",
                 "దానికి జవాబు మన **నేత గ్రామాల్లోనే** ఉంది… ఆ గుడ్డ తయారుచేసిన చేతుల్లో."),
          'B6': ("For a century and a half, the Company had shipped **silver** to India to pay for its cloth. ⏸ After 1765, it could increasingly pay with **revenue** collected in India itself.",
                 "నూట యాభై ఏళ్లు కంపెనీ సముద్రాల అవతల నుంచి **వెండి** తెచ్చి మన గుడ్డ కొన్నది. ⏸ 1765 తర్వాత, ఇక్కడే వసూలు చేసిన **పన్నులతోనే** ఎక్కువగా కొనగలిగింది."),
          'B3': ("Golconda's real wealth wasn't buried in its **mines**. ⏸ It was woven in its **villages**.",
                 "గోల్కొండ అసలు సంపద గనుల్లో దాగి లేదు. ⏸ అది ఊళ్లలోని **మగ్గాల** మీద నేయబడింది.")}

def short_plan(lang):
    tl, _ = timeline(lang); d = {x['id']: x for x in tl}
    rows = {r['id']: r for r in L}
    out = {}
    for k, p in NEW.items():
        i = 0 if lang == 'en' else 1
        segs = []
        h = p['hook'][i]
        if h.startswith('REUSE:'):
            rid = h[6:]; segs.append(('reuse', rid, d[rid]['start'], d[rid]['dur']))
        else:
            segs.append(('new-hook', h, None, spoken(h, lang, 'HOOK')))
        for rid in p['reuse']:
            if ':' in rid:
                rid, only = rid.split(':')
                if only != lang: continue
            if rid in BRIDGE:
                bt = BRIDGE[rid][i]; segs.append(('new-bridge', bt, None, spoken(bt, lang, 'PUNCH'))); continue
            if rid in d: segs.append(('reuse', rid, d[rid]['start'], d[rid]['dur']))
        segs.append(('new-tease', p['tease'][i], None, spoken(p['tease'][i], lang, 'EXP')))
        total = sum(s[3] for s in segs) + 0.22 * (len(segs) - 1)
        out[k] = (segs, total)
    return out

if __name__ == '__main__':
    for lang in ('en', 'te'):
        for k, (segs, tot) in short_plan(lang).items():
            print(lang, k, round(tot, 1), 's', [s[1] if s[0] == 'reuse' else s[0] for s in segs])
