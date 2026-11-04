"""Telugu on-screen text for the TE version (PIL + RAQM, cached as cairo surfaces)."""
import cairo
from PIL import Image, ImageDraw, ImageFont
TR = {
'NASA\'S DIWALI PHOTO?':'NASA తీసిన Diwali photo?','NOT DIWALI':'Diwali కాదు','NOT FIREWORKS':'బాణాసంచా కాదు','NOT ONE NIGHT':'ఒక్క రాత్రి కాదు',
'RAJU UNCLE':'రాజు బాబాయ్','FAMILY GROUP':'Family group','Forwarded many times':'చాలాసార్లు forward అయింది','CHRIS ELVIDGE':'Chris Elvidge','NOAA SCIENTIST':'NOAA scientist',
'DMSP · US DEFENSE METEOROLOGICAL SATELLITE PROGRAM':'DMSP · US military వాతావరణ satellites',"THEY'RE YEARS":'అవి సంవత్సరాలు','BEFORE 1992':'1992 కి ముందు',
'A MAP OF INDIA GROWING':'India పెరుగుదల map','11 YEARS':'11 సంవత్సరాలు','NOT':'కాదు','1 NIGHT':'1 రాత్రి','CLOUDS BY MOONLIGHT':'వెన్నెలలో మేఘాలు','+ CITY LIGHTS':'+ నగరాల వెలుగు',
"NASA'S REAL IMAGE":'NASA నిజమైన photo','NOV 12, 2012 · DIWALI WEEK':'NOV 12, 2012 · Diwali వారం','VIRAL':'Viral','REAL':'నిజం','ORANGE + WHITE = STREET LIGHTS':'Orange + తెలుపు = street lights',
'1 PIXEL ≈ 750 m':'1 pixel ≈ 750 మీటర్లు','A WHOLE NEIGHBOURHOOD':'ఒక పూర్తి colony','INSIDE 1 PIXEL':'1 pixel లోపల','DIYAS':'దీపాలు','STREET LIGHTS · EVERY NIGHT':'Street lights · ప్రతి రాత్రీ',
'BRIGHTNESS':'వెలుగు','DIWALI BLENDS IN':'Diwali కలిసిపోతుంది',
'DECIDES WHICH ONE':'ఏదో ఇదే నిర్ణయిస్తుంది','EXAMPLE JOB':'ఉదాహరణ పని','WAREHOUSE PACKER':'Warehouse packer','MORE SKILL = HIGHER MINIMUM':'ఎక్కువ skill = ఎక్కువ minimum',
'YOUR DIWALI BONUS:':'మీ Diwali bonus:','GIFT… OR LAW?':'బహుమతా… చట్టమా?','GIFT?':'బహుమతా?','LAW?':'చట్టమా?','COMPANY CHOICE':'company ఇష్టం','FOR MILLIONS':'లక్షల మందికి',
'A MONTH · DECIDES WHICH ONE':'నెలకు · ఏదో ఇదే నిర్ణయిస్తుంది','OUR FULL VIDEO · SUNDAY':'మా full video · ఆదివారం','CORRECTION':'సవరణ','OUT OF DATE':'అది పాతది',
'IN FORCE SINCE 21 NOV 2025':'21 Nov 2025 నుంచి అమల్లో','WAGES ACT':'జీతాల చట్టం','MINIMUM WAGES':'కనీస వేతనాల చట్టం','BONUS ACT':'Bonus చట్టం','EQUAL PAY':'సమాన వేతన చట్టం',
'4 OLD LAWS → 1':'4 పాత చట్టాలు → 1','THE LAW NEVER SAYS':'చట్టంలో ఎక్కడా లేని మాట',"IT'S AN ANNUAL BONUS":'సంవత్సరానికి ఒకసారి ఇచ్చే bonus',
'MANY COMPANIES JUST PAY IT AROUND DIWALI':'చాలా companies Diwali టైంలో ఇస్తాయి అంతే','THE ₹21,000 TEST':'₹21,000 test','RAVI':'రవి',
'WAREHOUSE PACKER · 50 WORKERS':'Warehouse packer · 50 మంది','₹18,000 / MONTH':'నెలకు ₹18,000','WAGES, AS THE LAW COUNTS THEM:':'చట్టం లెక్కించే జీతం:',
'(+ RETAINING ALLOWANCE)':'(+ retaining allowance)','₹21,000 / MONTH':'నెలకు ₹21,000','RAVI · ₹18,000':'రవి · ₹18,000','BELOW THE LINE':'line కంటే కింద',
'30+ DAYS WORKED THIS YEAR':'ఈ ఏడాది 30+ రోజులు పని','LAW: MUST PAY':'చట్టం: ఇవ్వాల్సిందే','SAME ANSWER':'పాతదైనా, కొత్తదైనా · ఇదే answer',
'OLD LAW · 1965':'పాత చట్టం · 1965','NEW LAW · 2025':'కొత్త చట్టం · 2025','ARJUN · ₹45,000':'అర్జున్ · ₹45,000','SOFTWARE ENGINEER · ABOVE THE LINE':'Software engineer · line కంటే పైన',
"THE BONUS RULE DOESN'T COVER HIM":'ఈ bonus rule అతనికి వర్తించదు','HIS BONUS COMES FROM':'అతని bonus వచ్చేది','CONTRACT /':'Contract /','COMPANY POLICY':'Company policy',
'NOT FROM THIS LAW':'ఈ చట్టం నుంచి కాదు','ELIGIBILITY ₹21,000 OR LESS · S.O. 4711(E), 25 AUG 2026':'అర్హత: ₹21,000 లేదా తక్కువ · S.O. 4711(E), 25 Aug 2026',
'BUILT FOR LOWER-PAID WORKERS':'తక్కువ జీతం వాళ్ళ కోసం','SURPRISED?':'ఆశ్చర్యంగా ఉందా?','HOW MUCH DOES RAVI GET?':'రవికి ఎంత వస్తుంది?',
'NOT COUNTED ON THE FULL SALARY':'పూర్తి జీతం మీద కాదు','MINIMUM WAGE':'Minimum wage','THE LOWEST PAY THE LAW ALLOWS FOR A JOB':'ఒక పనికి చట్టం ఒప్పుకునే అతి తక్కువ జీతం',
'UNSKILLED':'నైపుణ్యం లేని','SEMI-SKILLED':'కొంత నైపుణ్యం','SKILLED':'నైపుణ్యం','HIGHLY SKILLED':'అధిక నైపుణ్యం','MORE SKILL → HIGHER MINIMUM':'ఎక్కువ skill → ఎక్కువ minimum',
'SAME JOB · DIFFERENT PLACE':'అదే పని · వేరే చోటు','CITY':'City','VILLAGE':'పల్లె','CAN DIFFER':'వేరుగా ఉండొచ్చు','WHO GETS A MINIMUM WAGE?':'Minimum wage ఎవరికి?',
'OLD: LISTED JOBS ONLY':'ఇంతకు ముందు: list లో ఉన్న పనులకే','NOW: EVERY JOB':'ఇప్పుడు: ప్రతి పనికీ',"RAVI'S JOB · MINIMUM WAGE (EXAMPLE)":'రవి పని · minimum wage (ఉదాహరణ)',
'BONUS IS COUNTED ON THIS':'Bonus లెక్క దీని మీదే','BASE = YOUR WAGE, CAPPED AT ₹7,000 OR THE MINIMUM WAGE (WHICHEVER IS HIGHER)':'లెక్క = మీ జీతం, ₹7,000 లేదా minimum wage (ఏది ఎక్కువైతే అది) వరకే',
'× 12 MONTHS':'× 12 నెలలు','MINIMUM · 8.33%':'కనీసం · 8.33%','MIN 8.33%':'కనీసం 8.33%','MAX 20%':'గరిష్టం 20%','₹28,800 MAX':'గరిష్టం ₹28,800',
'MAX NEEDS ENOUGH ALLOCABLE SURPLUS · EXCEPTIONS, E.G. NEW ESTABLISHMENTS':'గరిష్టానికి సరిపడా surplus కావాలి · కొత్త సంస్థలకు మినహాయింపులు',
'WHAT CHANGED':'ఏం మారింది?','IN THE NEW LAW?':'కొత్త చట్టంలో','4 THINGS':'4 విషయాలు','PAID INTO YOUR BANK':'Bonus bank account లోనే','CREDITED':'Credited','BONUS':'Bonus',
'CASH':'Cash','BANK':'Bank','SMALL FACTORIES':'చిన్న factories','WORKERS':'మంది','RULE STARTS AT 20+':'Rule 20+ మంది నుంచే','SURESH':'సురేష్','COULD BE':'వర్తించొచ్చు',
'WHO SETS ₹21,000?':'₹21,000 ఎవరు నిర్ణయిస్తారు?','OLD LAW':'పాత చట్టం','₹21,000 · IN THE ACT':'₹21,000 · చట్టంలోనే',
'CENTRAL NOTIFICATION · STATES NOTIFY FOR THEIR OWN ESTABLISHMENTS':'Centre notification · రాష్ట్రాలు వాటి సంస్థలకు విడిగా notify చేస్తాయి',
'YOU LOSE THE BONUS IF':'Bonus ఎప్పుడు పోతుంది?','DISMISSED FOR…':'ఈ కారణాలతో ఉద్యోగం పోతే…','FRAUD':'Fraud','VIOLENCE':'హింస','THEFT':'దొంగతనం','NEW':'కొత్త',
'SEXUAL-HARASSMENT':'Sexual harassment','CONVICTION':'కేసులో శిక్ష','WHEN MUST THEY PAY?':'ఎప్పటిలోగా ఇవ్వాలి?','YEAR ENDS 31 MAR → 8 MONTHS':'సంవత్సరం 31 Mar కి ముగిశాక → 8 నెలలు',
"DIDN'T GET IT?":'రాలేదా?','FILE A CLAIM':'Claim చేయండి','LABOUR AUTHORITY · CLAIM PERIOD GENERALLY 3 YEARS (SEC. 45(6))':'Labour authority · సాధారణంగా 3 ఏళ్లలోపు (Sec. 45(6))',
}
TR.update({
'DIWALI · DELHI':'దీపావళి · Delhi','WHY DELHI CHOKES':'Delhi ఎందుకు ఉక్కిరిబిక్కిరి?','HOME · DELHI':'ఇల్లు · Delhi','DELHI':'Delhi','SKY ABOVE DELHI':'Delhi పైన ఆకాశం',
'PUNJAB · HARYANA':'Punjab · Haryana','STREET · DELHI':'వీధి · Delhi','INDIA':'India','NORTH INDIA':'ఉత్తర భారతం','BEIJING':'Beijing',
'PROBLEM':'సమస్య','WHY':'ఎందుకు','EFFECTS':'ప్రభావం','ACTION':'చర్యలు','FIX':'పరిష్కారం',
'BEFORE':'ముందు','AFTER':'తర్వాత',"INDIA'S 24-HR LIMIT · 60":'India 24 గంటల పరిమితి · 60','PM2.5 · µg/m³ · DIWALI 2025 · CPCB DATA (CLIMATE TRENDS)':'PM2.5 · µg/m³ · Diwali 2025 · CPCB data (Climate Trends)',
'≈ 8× THE LIMIT':'పరిమితికి 8 రెట్లు','SPIKE':'పెరుగుదల','TRAP':'బంధించడం','BUILD':'పేరుకుపోవడం',
'TEMPERATURE INVERSION':'Temperature inversion','WIND < 1 m/s · DIWALI 2025':'గాలి < 1 m/s · Diwali 2025','WARM AIR':'వెచ్చని గాలి','COOL AIR':'చల్లని గాలి',
'VEHICLES':'వాహనాలు','DUST':'దుమ్ము','INDUSTRY':'పరిశ్రమలు','GARBAGE':'చెత్త','FARM FIRES · SOME DAYS':'పంట మంటలు · కొన్ని రోజులు',
'PUNJAB':'Punjab','HARYANA':'Haryana','UTTAR PRADESH':'Uttar Pradesh','INDIA GATE':'India Gate','YAMUNA':'యమున',
'MODELED LOCAL PM2.5 ONLY · NOV 10–20, 2023–25':'నమూనా అంచనా · స్థానిక PM2.5 మాత్రమే · Nov 10–20, 2023–25','CSE ANALYSIS OF IITM DSS':'IITM DSS పై CSE విశ్లేషణ',
'EVERY WEEK':'ప్రతి వారం','SUN':'ఆది','FULL VIDEO':'Full video','MON–SAT':'సోమ–శని','SHORTS':'Shorts',
'+8.2 YEARS':'+8.2 సంవత్సరాలు','POTENTIAL GAIN · AQLI 2025 · 2023 DATA':'పొందగలిగే జీవితకాలం · AQLI 2025 · 2023 data','IF PM2.5 MET THE WHO GUIDELINE':'PM2.5 WHO ప్రమాణానికి తగ్గితే',
'CONSTRUCTION PAUSED':'నిర్మాణాలు ఆగాయి','SOME OLD CARS RESTRICTED':'కొన్ని పాత కార్లపై ఆంక్షలు','PRIMARY CLASSES: HYBRID':'చిన్న తరగతులు: hybrid','SCHOOL':'బడి',
'STAGE I':'దశ I','STAGE II':'దశ II','STAGE III':'దశ III','STAGE IV':'దశ IV','GRAP · CAQM · STRICTER IN STAGES':'GRAP · CAQM · దశల వారీగా కఠినం',
'NCAP · PM10 TARGET':'NCAP · PM10 లక్ష్యం','BY 2025–26 vs 2017–18':'2025–26 నాటికి · 2017–18 తో పోలిస్తే',
'ANNUAL LIMIT 40':'సంవత్సర పరిమితి 40','DELHI · 2025 · µg/m³':'Delhi · 2025 · µg/m³','CAQM · FULL YEAR':'CAQM · పూర్తి సంవత్సరం','≈ 2.5×':'≈ 2.5 రెట్లు',
'DELHI: NOT IN THE 23':'Delhi: ఆ 23 లో లేదు','COAL PLANTS SHUT':'బొగ్గు plants మూత','HOMES: GAS + POWER':'ఇళ్లకు gas + కరెంటు','VEHICLE RULES':'వాహన నియమాలు','REGIONAL TEAMWORK':'ప్రాంతీయ సహకారం',
'TIANJIN':'Tianjin','HEBEI':'Hebei','FIRECRACKERS':'బాణాసంచా','WINTER CONDITIONS':'చలికాలం వాతావరణం','ONGOING EMISSIONS':'రోజువారీ కాలుష్యం','YEAR-ROUND + REGION-WIDE':'సంవత్సరమంతా + ప్రాంతమంతా',
'BEIJING ECOLOGY BUREAU via CHINA DAILY':'Beijing ecology bureau · China Daily ద్వారా',
})
TR.update({
'₹7 LAKH CR':'₹7 లక్షల కోట్లు','FESTIVE TRADE FORECAST · CAIT':'పండగ వ్యాపారం అంచనా · CAIT','₹7 LAKH CRORE':'₹7 లక్షల కోట్లు','WHERE DOES IT GO?':'అదంతా ఎక్కడికి?',
'₹100 OF GOODS SALES · CAIT ESTIMATES':'వస్తువుల అమ్మకాల్లో ₹100 · CAIT అంచనాలు','BIGGEST SLICE?':'అతిపెద్ద వాటా?',
'GROCERIES & FMCG':'కిరాణా & FMCG','GOLD, SILVER & JEWELLERY':'బంగారం, వెండి, నగలు','ELECTRONICS':'Electronics','APPLIANCES':'Appliances','CLOTHES':'బట్టలు','GIFTS':'Gifts',
'HOME DÉCOR':'ఇంటి అలంకరణ','FURNITURE':'Furniture','SWEETS':'స్వీట్లు','EVERYTHING ELSE':'మిగతావన్నీ','GOODS':'వస్తువులు',
'SERVICES · ≈ ₹80,000 CR+ · 2026 FORECAST':'Services · దాదాపు ₹80,000 కోట్లు+ · 2026 అంచనా','SERVICES INCLUDED IN ₹7 LAKH CR FORECAST':'₹7 లక్షల కోట్ల అంచనాలోనే services కూడా',
'GROCERIES ₹12':'కిరాణా ₹12','LAKSHMI AUNTY':'లక్ష్మి ఆంటీ','EXAMPLE':'ఉదాహరణ','BUSIEST WEEKS':'అత్యంత busy వారాలు',
'MAINLINE RETAIL · 2025 · CAIT ESTIMATE':'Mainline retail · 2025 · CAIT అంచనా','85%':'85%','≈ 50 LAKH':'దాదాపు 50 లక్షలు','TEMPORARY JOBS · 2025 · CAIT ESTIMATE':'తాత్కాలిక ఉద్యోగాలు · 2025 · CAIT అంచనా',
"TRADERS' ESTIMATES · NOT OFFICIAL":'వ్యాపారుల అంచనాలు · అధికారికం కాదు','SMALL SHOPS':'చిన్న దుకాణాలు','BIG PART OF THE STORY':'ఈ కథలో పెద్ద పాత్ర',
})
TR.update({
'DIWALI · SUNDAY':'Diwali · ఆదివారం','MARKET OPEN…':'Market తెరిచి…','ON DIWALI?':'Diwali రోజునా?','70 MIN':'70 నిమిషాలు',
'MAIN CASH-EQUITY WINDOW · OTHER SEGMENTS DIFFER':'ముఖ్య cash-equity సమయం · ఇతర segments వేరు',
'MUHURAT':'ముహూర్తం','NEW YEAR':'కొత్త ఏడాది','NEW BOOKS':'కొత్త పుస్తకాలు','FIRST DEAL':'మొదటి deal','AUSPICIOUS TIME':'శుభ సమయం',
'SAMVAT':'Samvat','NEW ACCOUNTING YEAR':'కొత్త లెక్కల సంవత్సరం','OLD BOOKS · 2082':'పాత పుస్తకాలు · 2082','CHOPDA PUJAN':'Chopda Pujan',
'WORSHIP OF ACCOUNT BOOKS':'లెక్కల పుస్తకాలకు పూజ','FIRST INVESTMENT · AUSPICIOUS TIME':'మొదటి పెట్టుబడి · శుభ ముహూర్తం',
'BSE BEGINS':'BSE మొదలు','MUHURAT TRADING':'Muhurat trading','NSE EQUITY':'NSE equity','TRADING BEGINS':'trading మొదలు','THIS SUNDAY':'ఈ ఆదివారం',
'2025 · 60 MIN':'2025 · 60 నిమి.','2026 · 70 MIN':'2026 · 70 నిమి.','SURESH UNCLE':'సురేష్ మామయ్య','EXAMPLE':'ఉదాహరణ','MUHURAT SESSION':'Muhurat session',
'NIFTY 50 STOCK':'Nifty 50 share','BUY × 1':'కొను × 1','SHAGUN':'శుభం','NIFTY 50 · CHANGE VS PREVIOUS CLOSE':'Nifty 50 · ముందు రోజు ముగింపుతో పోలిస్తే మార్పు',
'9 / 11 UP':'11 లో 9 సార్లు పైకి','EVERY MOVE UNDER 1%':'ప్రతి మార్పు 1% కంటే తక్కువ','RITUAL, NOT FORECAST':'ఆచారం, అంచనా కాదు',
'CONTRACT NOTE':'Contract note','TRADE DATE':'Trade తేదీ','SESSION':'Session','BUY':'కొనుగోలు','1 SHARE':'1 share','NORMAL SETTLEMENT':'మామూలు settlement',
})
TR.update({
'DIWALI CLEANING':'Diwali శుభ్రత','WHY RIGHT NOW?':'సరిగ్గా ఇప్పుడే ఎందుకు?','CUPBOARDS OUT':'బీరువాలు బయటికి','FANS DOWN':'Fans కిందికి','WALLS PAINTED':'గోడలకి paint',
'BELIEF':'నమ్మకం','TIMING':'Timing','MONSOON GONE':'రుతుపవనాలు వెళ్ళాయి','DIWALI':'Diwali','OCT 15':'OCT 15','NOV 8':'NOV 8','DAYS':'రోజులు',
'SOUTH INDIA DIFFERS · NE MONSOON OCT–DEC':'దక్షిణ భారతం వేరు · ఈశాన్య రుతుపవనాలు OCT–DEC',
'MONSOON':'వర్షాలు','MOISTURE':'తేమ','MOULD':'బూజు','DRY':'ఆరబెట్టు','LIME':'సున్నం',
'DAMP WALLS':'తడి గోడలు','BLACK SPOTS':'నల్ల మచ్చలు','THAT SMELL':'ఆ వాసన','INDOOR HUMIDITY':'ఇంట్లో తేమ','MOULD ZONE':'బూజు zone','60%':'60%',
'CLEAN · DRY · PAINT':'శుభ్రం · ఆరబెట్టు · Paint','LIME · SUNNAM':'సున్నం','ACID':'ఆమ్లం','NEUTRAL':'తటస్థం','ALKALINE':'క్షారం',
'pH 12.4':'pH 12.4','STRONGLY ALKALINE':'చాలా క్షారం','CAN INACTIVATE MANY PATHOGENS':'చాలా క్రిములను నిర్వీర్యం చేయగలదు','FOR A WHILE':'కొంత కాలం',
'LIME → LIMESTONE MINERAL':'సున్నం - సున్నపురాయి ఖనిజం','OLD HOME':'పాత ఇల్లు','TODAY':'ఈ రోజు',
})
_F = {}; _S = {}
def _font(px, w):
    k = (px, w)
    if k not in _F:
        f = ImageFont.truetype('/home/claude/fonts/NotoSansTelugu.ttf', px, layout_engine=ImageFont.Layout.RAQM)
        try: f.set_variation_by_name(w)
        except Exception: pass
        _F[k] = f
    return _F[k]
def surf(txt, px, col, w='Bold', stroke=0, maxw=980):
    txt = txt.replace(' → ', ' - ').replace('→', '-'); key = (txt, px, col, w, stroke, maxw)
    if key in _S: return _S[key]
    px = int(round(px)); f = _font(px, w)
    while f.getlength(txt) + 2 * stroke > maxw and px > 12: px -= 2; f = _font(px, w)
    l, t, r, b = f.getbbox(txt, stroke_width=stroke); pad = 4
    im = Image.new('RGBA', (r - l + 2 * pad, int(px * 1.55) + 2 * stroke + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad - l, im.height / 2), txt, font=f, fill=tuple(int(v * 255) for v in col) + (255,), anchor='lm',
                            stroke_width=stroke, stroke_fill=(0, 0, 0, 220))
    b_ = bytearray(im.tobytes('raw', 'BGRa')); s = cairo.ImageSurface.create_for_data(b_, cairo.FORMAT_ARGB32, im.width, im.height)
    _S[key] = (s, b_); return _S[key]
def draw(c, txt, x, y, px, col, a=1.0, anchor='c', w='Bold', stroke=0, maxw=980):
    if a <= 0.01: return 0
    s, _ = surf(txt, px, tuple(col), w, stroke, maxw); sw, sh = s.get_width(), s.get_height()
    x0 = x - sw / 2 if anchor == 'c' else (x - sw if anchor == 'r' else x)
    c.save(); c.set_source_surface(s, x0, y - sh / 2); c.paint_with_alpha(a); c.restore()
    return sw
