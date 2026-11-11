import sys,re,difflib,json,subprocess,numpy as np
from faster_whisper import WhisperModel
def load(p): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',p,'-ar','16000','-ac','1','-f','f32le','-'],capture_output=True).stdout,np.float32).copy()
REF={
'en_53A':"Indian, Arab, Persian, African, Chinese and Malay traders were crossing it long before Vasco da Gama arrived.",
'en_PILOT':"His crew's journal calls him a Christian, but they called the Hindus of Calicut Christians too, so that word tells us little about his faith. Later Portuguese chroniclers describe a navigator from Gujarat: Malemo Canaqua. Malemo is a title, not a name. It means master navigator. The famous story that it was the Arab navigator Ibn Majid? Most historians think that's unlikely. So the navigator who guided Vasco da Gama to Calicut was most likely from Gujarat, in India.",
'en_FORCE':"The Portuguese used treaties and cannons: they allied with some rulers and bombarded others. A century later, the English came seeking trading permissions, and they used force too.",
'en_L':"So next time someone says Europe discovered India",
'en_Q1':"Wait, so who was already out on that ocean?",
'en_Q2':"Okay, so who showed him the way?",
'en_Q3':"And when he finally got there?",
'te_53A':"వాస్కో డ గామా రాకముందే ఎంతో కాలంగా, భారతీయులు, అరబ్బులు, పర్షియన్లు, ఆఫ్రికన్లు, చైనీయులు, మలయా వ్యాపారులు ఈ సముద్రాన్ని దాటుతున్నారు.",
'te_PILOT':"డ గామా సిబ్బంది డైరీ అతన్ని క్రైస్తవుడు అని రాసింది కానీ కాలికట్‌లోని హిందువులను కూడా వాళ్లు అలాగే పిలిచారు. అందుకే ఆ మాట అతని మతాన్ని చెప్పదు. తర్వాతి పోర్చుగీస్ చరిత్రకారులు, గుజరాత్‌కు చెందిన ఒక నావికుడిని మాలెమో కనాక్వా అని రాశారు. మాలెమో పేరు కాదు, బిరుదు: నావికుల నాయకుడు అని అర్థం. అతను అరబ్ నావికుడు ఇబ్న్ మాజిద్ అనే ప్రసిద్ధ కథ కూడా ఉంది కానీ అది నిజం కాకపోవచ్చని చాలామంది చరిత్రకారులు అంటారు. అంటే వాస్కో డ గామా ఓడలకు కాలికట్ దారి చూపించిన నావికుడు బహుశా మన గుజరాత్‌కు చెందినవాడే.",
'te_OLD':"యూరప్ కొత్త ప్రపంచాన్ని కనుక్కోలేదు. అప్పటికే నడుస్తున్న సముద్ర వాణిజ్య ప్రపంచంలోకి అడుగుపెట్టింది.",
'te_FORCE':"పోర్చుగీసులు కొందరు రాజులతో ఒప్పందాలు చేసుకున్నారు, మరికొందరిపై ఫిరంగులు పేల్చారు. ఒక శతాబ్దం తర్వాత, ఇంగ్లీష్ వాళ్లు వ్యాపార అనుమతులు అడుగుతూ వచ్చారు కానీ వాళ్లు కూడా బలాన్ని ప్రయోగించారు.",
'te_L':"కాబట్టి ఈసారి ఎవరైనా యూరప్ భారత్‌ను కనిపెట్టింది అంటే",
'te_Q1':"ఆగు అన్నా మరి అతనికంటే ముందే ఆ సముద్రంలో ఎవరున్నారు?",
'te_Q2':"సరే మరి అతనికి దారి చూపించింది ఎవరు?",
'te_Q3':"మరి చివరికి అక్కడికి చేరాక?",
}
lang=sys.argv[1]
m=WhisperModel('small' if lang=='en' else '/home/claude/models/te_med',device='cpu',compute_type='int8')
tok=(lambda s: re.sub(r"[^a-z0-9 ]"," ",s.lower()).split()) if lang=='en' else (lambda s: re.sub(r"[^ఀ-౿ ]"," ",s).split())
res={}
for k,ref in REF.items():
    if not k.startswith(lang): continue
    segs,_=m.transcribe(load(k+'.mp3'),language=lang,beam_size=1 if lang=='en' else 3)
    hyp=' '.join(s.text.strip() for s in segs)
    r=difflib.SequenceMatcher(None,tok(ref),tok(hyp)).ratio()
    cr=difflib.SequenceMatcher(None,ref.replace(' ',''),hyp.replace(' ','')).ratio()
    res[k]=dict(word_match=round(r,2),char_match=round(cr,2),hyp=hyp)
    print(k,round(r,2),round(cr,2),'|',hyp,flush=True)
json.dump(res,open(f'../asr_{lang}.json','w'),ensure_ascii=False,indent=1)
