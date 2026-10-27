import sys, json; sys.path.insert(0, '/home/claude/long'); sys.path.insert(0, '/home/claude/goldL')
from proasm import build_long
import pacing
from voice_te_part1 import P1, R
P2 = [
 ((424.57, 430.24), "That's why for thousands", "అందుకే వేల ఏళ్ళుగా, Egypt రాజుల నుంచి మన నానమ్మల దాకా, అందరూ gold నే నమ్మారు."),
 ((432.14, 434.43), 'Chapter four', "చాప్టర్ ఫోర్. తవ్వడం చాలా కష్టం."),
 ((438.07, 440.21), 'Reason number three', "Gold ని భూమి నుంచి బయటికి తీయడం"),
 ((440.45, 441.11), 'Getting gold out', "చాలా కష్టం."),
 ((449.14, 457.20), 'In a typical gold mine', "ఈ రోజుల్లో ఒక మామూలు gold mine లో, సుమారు ఒక టన్ను రాళ్ళను తవ్వి పిండి చేస్తే, వచ్చేది సుమారు ఒకటిన్నర గ్రాము gold."),
 ((472.49, 473.45), 'A whole tonne', "ఒక టన్ను రాళ్ళకి,"),
 ((473.63, 475.78), 'a piece of gold smaller', "ఒక మిరియం గింజ కంటే చిన్న gold ముక్క."),
 ((476.73, 482.66), 'And even with giant', "పెద్ద పెద్ద machines ఉన్నా, ప్రపంచం మొత్తం ఏడాదికి తవ్వేది సుమారు 3,600 టన్నులు మాత్రమే."),
 ((485.00, 487.24), 'That adds less', "ఉన్న gold కి అది 2 శాతం కంటే తక్కువ."),
 ((487.87, 489.79), "You can't just print", "Gold ని డబ్బులాగా print చేయలేం."),
 ((494.48, 496.98), 'Chapter five', "చాప్టర్ ఫైవ్. Price ఎందుకు పెరుగుతూనే ఉంది."),
 ((500.15, 503.66), 'So gold is rare', "సరే, gold అరుదు, ఎప్పటికీ ఉంటుంది, తవ్వడం కష్టం."),
 ((507.01, 508.50), 'But that was always', "కానీ ఇవన్నీ ఎప్పుడూ ఉన్నవే."),
 ((517.24, 520.53), 'So why has the price', "మరి ఈ మధ్య కొన్నేళ్ళలో price ఎందుకు ఇంతగా పెరిగింది?"),
 ((521.06, 522.07), "Here's the big one", "అసలు కారణం ఇదే."),
 ((524.04, 525.47), 'Countries are buying', "దేశాలే gold కొంటున్నాయి."),
 ((525.87, 528.95), 'Central banks', "Central banks, అంటే ఒక దేశం డబ్బుని నడిపే banks,"),
 ((530.23, 533.92), 'used to buy around', "ఒకప్పుడు ఏడాదికి సుమారు 470 టన్నుల gold కొనేవి."),
 ((543.50, 551.04), 'Then from 2022', "కానీ 2022 నుంచి 2024 వరకు, ప్రతి ఏడాది 1,000 టన్నులకు పైగా కొన్నాయి. ప్రతి ఒక్క ఏడాది."),
 ((552.05, 555.76), 'And in 2025', "2025లో కూడా సుమారు 860 టన్నులు కొన్నాయి."),
 ((556.74, 557.61), 'Why?', "ఎందుకు?"),
 ((571.23, 572.83), 'Because when', "ప్రపంచం భయంగా అనిపించినప్పుడు,"),
 ((573.06, 577.06), 'wars, rising', "యుద్ధాలు, పెరిగే ధరలు, దేశాలు ఒకదాన్ని ఒకటి నమ్మకపోవడం,"),
 ((577.45, 580.26), 'gold is the one thing', "gold మాత్రమే ఎవరి promise మీదా ఆధారపడదు."),
 ((581.27, 585.37), 'A government can print', "ప్రభుత్వం డబ్బులు print చేయగలదు. కానీ gold ని ఎవరూ print చేయలేరు."),
 ((586.38, 588.57), 'So the price took off', "అందుకే price దూసుకెళ్ళింది."),
 ((589.09, 592.77), 'In 2019', "2019లో ఒక ounce సుమారు 1,400 డాలర్లు."),
 ((596.23, 599.20), 'In January 2026', "2026 జనవరిలో 5,000 దాటింది."),
 ((604.21, 608.06), "It's come down", "అప్పటి నుంచి కొంచెం తగ్గి, ఇప్పుడు సుమారు 4,000 డాలర్ల దగ్గర ఉంది."),
 ((608.55, 611.74), "But that's still almost", "అయినా 2019 కంటే దాదాపు మూడు రెట్లు ఎక్కువ."),
 ((613.64, 615.86), 'Chapter six', "చాప్టర్ సిక్స్. ఇక మన India."),
 ((616.80, 620.72), 'And for us in India', "ఇక మన India లో gold అంటే కేవలం investment కాదు. అది కుటుంబం."),
 ((626.76, 629.07), 'Weddings', "పెళ్ళిళ్ళు, అక్షయ తృతీయ, ధన్‌తేరస్,"),
 ((632.13, 633.75), 'te:nov6', "అది నవంబర్ 6న వస్తుంది."),
 ((634.49, 639.00), 'Gold gets passed', "Gold అమ్మల నుంచి కూతుళ్ళకి, ఒక తరం నుంచి ఇంకో తరానికి వెళ్తుంది."),
 ((639.44, 643.71), 'India is one of the two', "ప్రపంచంలో gold ఎక్కువగా కొనే రెండు దేశాల్లో India ఒకటి, China తో పాటు."),
 ((646.33, 648.53), 'So when you see gold', "అందుకే news లో gold price పెరిగిందంటే,"),
 ((649.04, 651.47), 'part of that story', "ఆ story లో ఒక భాగం మన ఇళ్ళలోనే జరుగుతోంది."),
 ((653.72, 655.45), 'So, why is gold so expensive', "మరి gold ఎందుకు ఇంత costly?"),
 ((662.57, 664.37), 'It was made in exploding', "అది పేలిన stars లో పుట్టింది."),
 ((664.79, 665.84), "There's very little", "చాలా తక్కువగా ఉంది."),
 ((666.25, 667.34), 'It never rots', "ఎప్పటికీ పాడవదు."),
 ((667.76, 668.73), "It's brutal to dig", "తవ్వడం చాలా కష్టం."),
 ((674.59, 679.21), 'And the moment the world', "ఇంకా ప్రపంచం భయపడిన ప్రతిసారీ, అందరూ ఒకేసారి దాన్నే కావాలనుకుంటారు."),
 ((679.94, 680.76), 'That combination', "ఈ combination?"),
 ((681.13, 682.87), 'Nothing else on Earth', "భూమ్మీద ఇంకే వస్తువుకీ లేదు."),
 ((684.26, 688.27), 'If you like learning', "ఇలాంటి విషయాలు నచ్చితే subscribe చేయండి. రోజుకో కొత్త why."),
 ((696.16, 699.47), 'te:comment', "మీకు 'ఎందుకు' అని మొదలయ్యే ఏ ప్రశ్న వచ్చినా కింద comment చేయండి."),
 ((699.80, 701.50), 'te:answer', "మేము research చేసి answer చెప్తాం."),
]
P = P1 + P2
keep = [p[0] for p in P]; keys = [p[1] for p in P]; texts = [p[2] for p in P]
idx = lambda k: keys.index(k)
chap = [idx(k) for k in ['Chapter one', 'Chapter two', 'Chapter three', 'Chapter four', 'Chapter five', 'Chapter six', 'So, why is gold so expensive']]
marks = dict(hook_end=idx('So why is gold so expensive'), ask=idx('So why is gold so expensive'), ask_end=chap[0], cta=idx('If you like learning'),
             chapters=chap, tease=[], lists=[(idx('Gases?'), idx('Then you cut the common')), (idx('It was made in exploding'), idx('That combination'))],
             reveal=[idx("That's it."), idx('Countries are buying'), idx('So gold wins'), idx('Nothing else on Earth')])
json.dump(texts, open('/home/claude/goldL/pieces_te.json', 'w'), ensure_ascii=False); json.dump(keys, open('/home/claude/goldL/keys_te.json', 'w'), ensure_ascii=False)
role, gaps, intra = pacing.plan(texts, marks, None)
gaps[idx('Chapter one') - 1] = 6.6
build_long('te', keep, '/home/claude/goldL/voice_te.wav', gaps, intra=intra)
import scipy.io.wavfile as wf
sr, a = wf.read('/home/claude/goldL/voice_te.wav'); print('total', round(len(a) / sr, 1), 'pieces', len(P))
