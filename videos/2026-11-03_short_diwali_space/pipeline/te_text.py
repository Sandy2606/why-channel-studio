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
