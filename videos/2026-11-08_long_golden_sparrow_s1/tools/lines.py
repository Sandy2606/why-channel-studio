# Golden Sparrow S1 - recording script data (EN + TE). One row per recorded line.
# fields: id, spk (NAR/ANNA/CHELLI), role, en_mood, en, te_mood, te, src (claim ids), sh (Short reuse), vis, only ('en'/'te'/None)
L = []
def a(id, spk, role, em, en, tm, te, src='', sh='', vis='', only=None):
    L.append(dict(id=id, spk=spk, role=role, em=em, en=en, tm=tm, te=te, src=src, sh=sh, vis=vis, only=only))

# ---------------- COLD OPEN ----------------
a('0.1','NAR','HOOK','HOOK · intrigued, low',
  "In **1721**, Britain passed a law banning people from wearing certain **printed cotton** fabrics. ⏸ **Why?**",
  'HOOK · ఆశ్చర్యంగా',
  "**1721**లో బ్రిటన్ ఒక చట్టం చేసింది: కొన్ని రకాల **అచ్చు cotton** గుడ్డలు వేసుకోవడమే నిషేధం. ⏸ **ఎందుకు?**",
  'C1','S2-hook','Black → loom sound → macro of a painted flower on Met 1982.66 (caption "Coromandel Coast, 18th c. · The Met"); chip "ENACTED 1721 · IN FORCE 25 DEC 1722 · CERTAIN PRINTED, PAINTED, STAINED OR DYED CALICOES · SOME EXCEPTIONS"')
a('0.2','NAR','HOOK','fast, pointed',
  "Printed here or abroad, it didn't matter. ⏸ **Indian cotton** was beating Britain's **wool** and **silk**.",
  'వేగంగా',
  "అచ్చు ఎక్కడ వేసినా నిషేధమే. ⏸ మన **cotton** తో బ్రిటన్ **ఉన్ని**, **పట్టు** పోటీ పడలేకపోయాయి.",
  'C1,C2,C5','','Pull back to the full palampore; wool and silk bolts dim beside it')
a('0.3','NAR','HOOK','rising, wonder',
  "For centuries, the world sailed to India: for **pepper**, for **diamonds**… and above all, for **cloth**.",
  'ఆశ్చర్యంగా',
  "శతాబ్దాలుగా ప్రపంచం మన దగ్గరికి వచ్చేది: **మిరియాల** కోసం, **గోల్కొండ వజ్రాల** కోసం… అన్నిటికంటే ఎక్కువగా, **మచిలీపట్నం** లాంటి మన రేవుల **గుడ్డ** కోసం.",
  'C30','','1 s cuts: Indus beads (Met) → monsoon sea → Calicut coast → Golconda fort → Tavernier diamond plate → ship under sail')
a('0.4','NAR','HOOK','confident',
  "By one estimate, in **1700**, India made almost **a quarter** of the world's output.",
  'నమ్మకంగా',
  "ఒక అంచనా ప్రకారం, **1700**లో ప్రపంచ ఉత్పత్తిలో దాదాపు **నాలుగో వంతు** భారతదేశానిదే.",
  'C8','','World map, India glows; chip "≈24% OF WORLD GDP · c.1700 · MADDISON EST."')
a('0.5','NAR','HOOK','slow, heavy question',
  "So how did the land the whole world came to… fall under a company that came only to **trade**?",
  'నెమ్మదిగా · ప్రశ్నగా',
  "మరి ప్రపంచమంతా వెతుక్కుంటూ వచ్చిన ఈ నేల… **వ్యాపారం** కోసం వచ్చిన ఒక కంపెనీ చేతుల్లోకి ఎలా వెళ్లింది?",
  '','','Company sail fills the frame → black → title card THE GOLDEN SPARROW · SEASON 1 (TE: బంగారు పిచ్చుక · సీజన్ 1)')

# ---------------- TRUNK ----------------
a('F1.1','CHELLI','DLG','delighted',
  "Anna! It's Ammamma's **Ramayana** cloth!",
  'సంతోషంగా',
  "అన్నా! ఇది అమ్మమ్మ **రామాయణం** గుడ్డ కదా!",
  'C50','','[DRAM] Anna & Chelli open Ammamma\'s trunk; kalamkari of Rama, Sita, Lakshmana on top; coin and folded map beneath')
a('F1.2','ANNA','DLG','warm',
  "Stories like the **Ramayana** and **Mahabharata** are still painted on cloth like this. ⏸ More than three hundred years ago, hands like these made a cloth that travelled all the way to **London**… and the world went crazy for it.",
  'ఆప్యాయంగా',
  "రామాయణం, మహాభారతం కథలను ఇప్పటికీ ఇలా గుడ్డ మీద **చిత్రిస్తారు**. ⏸ మూడు వందల ఏళ్లకు పైగా క్రితం, ఇలాంటి చేతులే చేసిన ఒక గుడ్డ… మన తీరం నుంచి **లండన్** దాకా వెళ్లింది.",
  'C50','','Anna\'s finger traces the painted border; Chelli leans in')
a('F1.3','NAR','EXP','storytelling',
  "That cloth is our **reconstruction**. But every step of its journey is **real**. ⏸ Let's follow it.",
  'కథ చెప్తూ',
  "ఆ గుడ్డ మా **ఊహ**. కానీ దాని ప్రయాణంలో ప్రతి అడుగూ **నిజం**. ⏸ పదండి, దాని వెనకే వెళ్దాం.",
  'C49','','Tag "DRAMATIZED RECONSTRUCTION · BASED ON SURVIVING MUSEUM CHINTZ"; match cut: painted cotton plant on the cloth → real field')

# ---------------- CH1 ----------------
a('1.0','NAR','CHAP','chapter',
  "Chapter one. **Was India really that rich?**", 'అధ్యాయం',
  "మొదటి అధ్యాయం. **భారతదేశం నిజంగా అంత ధనికమా?**", '','','Chapter card; year chip "c.1680 / 1700"; progress bar 1/6')
a('1.1','NAR','Q','curious, a little teasing',
  "They called India the **golden sparrow**. ⏸ Was it true… or is it just a story we like to tell?",
  'ఆసక్తిగా',
  "మనల్ని **బంగారు పిచ్చుక** అనేవారు. ⏸ అది నిజమా… లేక మనం చెప్పుకునే కథా?",
  '','','Golden sparrow motif dissolves into dawn light over a field')
a('1.2','NAR','EXP','storytelling, calm',
  "Let's start where our cloth starts. ⏸ Around **1680**, somewhere in the Deccan, a family is picking **cotton** at dawn.",
  'కథ చెప్తూ',
  "మన గుడ్డ మొదలయ్యే చోటు నుంచే మొదలుపెడదాం. ⏸ దాదాపు **1680**. దక్కన్‌లో ఒక **నల్లరేగడి** పొలం. తెల్లవారుజామునే ఒక కుటుంబం **పత్తి** ఏరుతోంది.",
  'C49','','[DRAM] AI still: family picking cotton, black soil, ox; chip "OUR CLOTH · c.1680"')
a('1.3','NAR','EXP','steady',
  "People here had been growing and weaving cotton for **thousands of years**.",
  'స్థిరంగా',
  "ఈ నేలపై **వేల ఏళ్లుగా** పత్తి పండిస్తున్నారు, నేస్తున్నారు.",
  'C7','','Archaeological cotton evidence (Mehrgarh) or Indus textile impression (licence-confirmed image only)')
a('1.4','NAR','EXP','clear, numbers slower',
  "Now, the big number. ⏸ The economic historian **Angus Maddison** estimated that in 1700, India produced about **24 percent** of the world's output. ⏸ Britain? About **3**. ⏸ By 1950, the Republic of India's share was about **4**.",
  'స్పష్టంగా · అంకెలు నెమ్మదిగా',
  "ఇప్పుడు అసలు లెక్క. ⏸ ఆర్థిక చరిత్రకారుడు **Angus Maddison** అంచనా ప్రకారం, 1700లో ప్రపంచ ఉత్పత్తిలో మన వాటా దాదాపు **24 శాతం**. ⏸ బ్రిటన్? దాదాపు **3 శాతం**. ⏸ 1950 నాటికి, స్వతంత్ర భారతదేశం వాటా దాదాపు **4 శాతం**.",
  'C8','S1 (from "The economic historian")','Animated bars on the master map: India 24 / Britain 3 → 1950 India 4; source note "MADDISON ESTIMATES (OECD 2001) · 1700 = UNDIVIDED SUBCONTINENT · 1950 = REPUBLIC OF INDIA ONLY (EXCL. PAKISTAN & BANGLADESH) · AREAS DIFFER"')
a('1.4e','NAR','EXP','light',
  "China made about **22**. ⏸ Together, India and China made almost **half** of everything on Earth.",
  '', '', 'C8','S1','China bar joins; "≈ HALF" bracket', only='en')
a('1.5','NAR','PUNCH','honest, slower',
  "But here's the **catch**. ⏸ That doesn't mean every Indian was **rich**.",
  'నిజాయితీగా',
  "కానీ ఇక్కడే అసలు **విషయం**. ⏸ అంటే ప్రతి భారతీయుడూ **ధనికుడని** కాదు.",
  'C9','S1','Bars freeze; one gold coin among many plain ones')
a('1.6','NAR','EXP','explaining',
  "India had roughly **a quarter** of the world's people. ⏸ Its share was huge because India was **huge**… and because it **made things**. ⏸ Income per person was probably close to the **world average**, and below Western Europe's.",
  'వివరిస్తూ',
  "ప్రపంచ జనాభాలో దాదాపు **నాలుగో వంతు** ఇక్కడే ఉండేవారు. ⏸ దేశం **పెద్దది**, పైగా ఎన్నో వస్తువులు **తయారుచేసేది**. అందుకే వాటా అంత పెద్దది. ⏸ ఒక్కొక్కరి సగటు ఆదాయం మాత్రం **ప్రపంచ సగటుకు** దగ్గరగా, పశ్చిమ యూరప్ కంటే తక్కువగా ఉండేదని అంచనా.",
  'C9','S1','Population dots fill the India shape; per-person bar sits near the world line, below W. Europe; chip "ESTIMATES"')
a('1.7','NAR','EXP','serious, fair',
  "And the harvest was **split**. The farmer, the landlord and the state each took a share, rarely an equal one. ⏸ **Caste** decided many people's work from birth. ⏸ And schooling reached only a **few**.",
  'గంభీరంగా · న్యాయంగా',
  "పంట కూడా **సమానంగా** పంచుకోలేదు. రైతు, భూస్వామి, రాజ్యం… ఒక్కొక్కరూ తమ వాటా తీసుకునేవారు. ⏸ ప్రతి ఊరిలో **కరణం** భూమి లెక్కలన్నీ రాసేవాడు. ⏸ చాలామంది చేసే పని పుట్టుకతోనే, **కులంతోనే** నిర్ణయమయ్యేది. ⏸ **చదువు** కొంతమందికే దక్కేది.",
  'C25','S1','[DRAM] Village scene: grain heaps divided three ways; a village accountant\'s palm-leaf ledger; a pathshala with few children')
a('1.8','NAR','Q','intrigue',
  "So what made this land so **productive**? ⏸ The world didn't come for India's gold. It came for something **humbler**… and it's right here, in this field.",
  'ఆసక్తి రేపుతూ',
  "మరి ఈ నేల ఇంత సంపద ఎలా **సృష్టించింది**? ⏸ ప్రపంచం మన బంగారం కోసం రాలేదు. ఇంకా **సాధారణమైన** దాని కోసం వచ్చింది… అది ఇక్కడే, ఈ పొలంలోనే ఉంది.",
  '','','A hand closes on a cotton boll; macro; spinning wheel turns in the dark')

# ---------------- CH2 ----------------
a('2.0','NAR','CHAP','chapter',
  "Chapter two. **The cloth the world wanted.**", 'అధ్యాయం',
  "రెండో అధ్యాయం. **ప్రపంచం కోరుకున్న గుడ్డ.**", '','','Chapter card; progress 2/6')
a('2.1','NAR','Q','curious',
  "Why would a country **ban** a fabric? ⏸ To understand that, follow the **hands**.",
  'ఆసక్తిగా',
  "ఒక దేశం ఒక గుడ్డను ఎందుకు **నిషేధిస్తుంది**? ⏸ అది తెలియాలంటే, ఈ **చేతుల** వెనకే వెళ్లాలి.",
  '','','Montage of hands: spinning, weaving, painting')
a('2.2','NAR','EXP','gentle',
  "First, the **spinner**. Usually a woman, spinning at home between her other work. ⏸ It took **many** spinners to keep one loom busy.",
  'మృదువుగా',
  "మొదట **వడికేవాళ్లు**. ఎక్కువగా ఆడవాళ్లే, ఇంటి పనుల మధ్యలో రాట్నం మీద నూలు వడికేవారు. ⏸ ఒక్క మగ్గం నడవాలంటే **ఎంతోమంది** వడికేవాళ్లు కావాలి.",
  'C10','','[DRAM] Courtyard charkha at oil-lamp light')
a('2.3','NAR','EXP','explaining, fair',
  "Then the **weaver**. A pit loom, the whole family working. ⏸ Weavers were often paid **in advance** by brokers… and the broker usually set the **price**. ⏸ World-class skill. Very little **bargaining power**.",
  'వివరిస్తూ',
  "తర్వాత **నేతగాళ్లు**. గుంట మగ్గం, కుటుంబం మొత్తం పనిలో. ⏸ దళారులు **ముందుగానే** డబ్బు ఇచ్చేవారు… ధర కూడా చాలావరకు **వాళ్లే** నిర్ణయించేవారు. ⏸ ప్రపంచస్థాయి నైపుణ్యం. కానీ బేరమాడే శక్తి **చాలా తక్కువ**.",
  'C10','S2','[DRAM] Pit loom; broker counting coins into a weaver\'s hand')
a('2.4','NAR','PUNCH','reveal',
  "Then came the real secret: the **dyer**.",
  'రహస్యం చెప్తూ',
  "తర్వాత అసలు **రహస్యం**: రంగులు అద్దేవాళ్లు.",
  '','S2','Hard cut to river, vats of red and indigo')
a('2.5','NAR','EXP','admiring',
  "European dyers could colour cloth. ⏸ Indian dyers made colours that **didn't wash out**.",
  'మెచ్చుకుంటూ',
  "మన తీరంలో, **మచిలీపట్నం**, **పాలకొల్లు** చుట్టుపక్కల ఊళ్లలో, రంగు అద్దేవాళ్లు **ఉతికినా పోని** రంగులు తయారుచేసేవారు.",
  'C11,C15','S2','Split screen: faded European print vs bright chintz after washing (illustrative)')
a('2.6','NAR','EXP','explaining, rhythmic',
  "With a pen called a **kalam**, they drew the design in mordants, substances that fix dye to cotton. ⏸ Then came reds from the **chay root**, blue from **indigo**, and wax to protect some areas. Step after step, for **weeks**.",
  'వివరిస్తూ · లయగా',
  "**కలం** అనే పెన్నుతో, రంగును cotton కి పట్టించే పదార్థాలతో design గీసేవారు. ⏸ తర్వాత **చిరివేరు** నుంచి ఎరుపు, **నీలిమందు** నుంచి నీలం, కొన్ని భాగాలను కాపాడటానికి మైనం. అడుగు తర్వాత అడుగు, **వారాల** తరబడి.",
  'C11','S2','[DRAM] Dyer\'s hand with kalam; diagram: mordant → madder/chay red → indigo → wax resist; Met chintz detail')
a('2.7','NAR','EXP','light',
  "", 'గర్వంగా',
  "కలంతో గీసే ఈ పనినే మనం ఇప్పుడు **కలంకారి** అంటాం. ⏸ ఈరోజుకీ **శ్రీకాళహస్తిలో** కలంతో, **మచిలీపట్నం**, **పెడనలో** అచ్చులతో ఈ కళ బతికే ఉంది.",
  'C11','','Map pins Srikalahasti, Machilipatnam, Pedana; tag "TODAY"', only='te')
a('2.8','NAR','EXP','storytelling',
  "Europe tried for **decades** to copy it. ⏸ In the 1740s, a French Jesuit priest named **Coeurdoux** sent home detailed descriptions of how it was done.",
  'కథ చెప్తూ',
  "యూరప్ **దశాబ్దాల** పాటు దీన్ని కాపీ చేయాలని ప్రయత్నించింది. ⏸ 1740లలో, **Coeurdoux** అనే ఒక ఫ్రెంచ్ Jesuit priest, ఇక్కడి పద్ధతిని వివరంగా రాసి తన దేశానికి పంపాడు.",
  'C12','S2','Letter with quill; period engraving of a Pondicherry street (PD)')
a('2.9','NAR','EXP','wonder',
  "And in Bengal, weavers made **muslin** so fine, people called it **woven air**.",
  'ఆశ్చర్యంగా',
  "బెంగాల్‌లో అయితే, **మస్లిన్** ఎంత పల్చగా ఉండేదంటే, దాన్ని **నేసిన గాలి** అనేవారు.",
  'C13','','Muslin held to light (V&A/Met, licence-confirmed)')
a('2.10','NAR','EXP','building',
  "In Europe, people went **crazy** for it: bright, light, **washable** cotton. ⏸ And that's when the **bans** began.",
  'పెరుగుతున్న ఉత్సాహంతో',
  "యూరప్‌లో జనం దీని కోసం **ఎగబడ్డారు**: రంగురంగుల, తేలికైన, **ఉతకగలిగే** cotton. ⏸ అప్పుడే **నిషేధాలు** మొదలయ్యాయి.",
  'C1','S2','18th-c. fashion plate in chintz (PD); stamp "BANNED"')
a('2.11','NAR','EXP','precise, steady',
  "France banned printed calicoes in **1686**. ⏸ England's **1700** Act stopped printed and painted calicoes from Asia being used at home. They could still be **re-exported**.",
  'ఖచ్చితంగా',
  "**1686**లో ఫ్రాన్స్ అచ్చు cotton గుడ్డలను నిషేధించింది. ⏸ **1700** చట్టంతో ఇంగ్లాండ్, ఆసియా నుంచి వచ్చే అచ్చు, రంగుల calico లను దేశంలో **వాడకుండా** ఆపింది. వేరే దేశాలకు మళ్లీ **పంపొచ్చు**.",
  'C2,C3','S2','Timeline: our cloth c.1680 → France 1686 → England 1700 (customs warehouse, bales stamped RE-EXPORT)')
a('2.12','NAR','EXP','precise, weighty',
  "Then the **1721** Act went further. ⏸ From Christmas **1722**, it banned **wearing** or **using** printed, painted, stained or dyed calicoes, whether printed abroad or in **Britain**, with a few exceptions.",
  'ఖచ్చితంగా · బరువుగా',
  "**1721** చట్టం ఇంకా ముందుకెళ్లింది. ⏸ **1722** క్రిస్మస్ నుంచి, అచ్చు వేసిన, రంగు అద్దిన calico లను **వేసుకోవడం**, **వాడటం** నిషేధం. అచ్చు బయట వేసినా, **బ్రిటన్‌లోనే** వేసినా సరే. కొన్ని మినహాయింపులు మాత్రం ఉండేవి.",
  'C1','S2','Act title page (7 Geo. I c.7, PD); chip "EXCEPTIONS: MUSLINS, NECKCLOTHS, FUSTIANS, ALL-BLUE CALICO"')
a('2.13','NAR','EXP','plain',
  "It stayed in force until **1774**.",
  'సాదాగా',
  "ఈ నిషేధం **1774** వరకు అమల్లో ఉంది.",
  'C4','S2','Timeline extends to 1774')
a('2.14','NAR','PUNCH','pointed',
  "These laws protected Britain's **wool** and **silk** weavers. ⏸ And they tell you how good **Indian cotton** was.",
  'సూటిగా',
  "ఎందుకంటే మన cotton తో, బ్రిటన్ **ఉన్ని**, **పట్టు** నేతగాళ్లు పోటీ పడలేకపోయారు. ⏸ ఆ చట్టాలే చెప్తాయి, మన గుడ్డ **ఎంత గొప్పదో**.",
  'C1','S2','Wool and silk weavers\' petition print (PD) beside the chintz')
a('2.15','NAR','EXP','worldly',
  "Indian cloth also bought **spices** in Southeast Asia and travelled into **West Africa**. ⏸ Even the English words **calico**, from Calicut, and **chintz** came from India.",
  '', '', 'C30','','Cloth-route lines across the master map; word cards CALICO ← Calicut, CHINTZ ← chheent', only='en')
a('2.16','NAR','EXP','transition',
  "Our cloth is finished. Now it needs a **buyer**. ⏸ And on the Deccan coast, there was a port where the whole world came **shopping**.",
  'కథ చెప్తూ',
  "మన గుడ్డ సిద్ధమైంది. ఇప్పుడు దానికి **కొనేవాళ్లు** కావాలి. ⏸ దక్కన్ తీరంలో ఒక రేవు ఉండేది… అక్కడికి ప్రపంచమంతా **షాపింగ్‌కి** వచ్చేది.",
  'C49','','[DRAM] Broker\'s stamp pressed on the bundle → sea horizon')

# ---------------- CH3 ----------------
a('3.0','NAR','CHAP','chapter',
  "Chapter three. **Golconda and Machilipatnam.**", 'అధ్యాయం',
  "మూడో అధ్యాయం. **గోల్కొండ, మచిలీపట్నం.**", '','','Chapter card; progress 3/6; chip "c.1680"')
a('3.1','NAR','Q','intrigue',
  "Golconda is famous for **diamonds**. ⏸ So why did merchants from Persia to the Netherlands really crowd its **port**?",
  'ఆసక్తి రేపుతూ',
  "గోల్కొండ అంటే మనకు **వజ్రాలే** గుర్తొస్తాయి. ⏸ మరి Persia నుంచి Netherlands వరకు వ్యాపారులు అసలు దేని కోసం ఆ **రేవుకి** వచ్చేవారు?",
  '','','Golconda fort at dusk (licensed photo)')
a('3.2','NAR','EXP','storytelling',
  "Around 1680, much of today's Telangana and Andhra was ruled by the **Qutb Shahi** kings of Golconda. ⏸ Their sea gate was **Machilipatnam**, on the Krishna delta.",
  'కథ చెప్తూ · గర్వంగా',
  "1680 ప్రాంతంలో, ఇప్పటి తెలంగాణ, ఆంధ్రలో చాలా భాగాన్ని గోల్కొండ **కుతుబ్‌షాహీ** రాజులు పాలించేవారు. ⏸ వాళ్ల సముద్ర ద్వారం… కృష్ణా డెల్టాలోని మన **మచిలీపట్నం**.",
  'C14','S3','Master map: Golconda kingdom fill, road to Machilipatnam (TE: Telugu labels, zoom 1)')
a('3.3','NAR','EXP','busy, vivid',
  "Ships came here from **Persia**, **Arabia**, **Burma** and **Southeast Asia**. ⏸ The Dutch set up trade here in the early 1600s, the English in **1611**. ⏸ Local brokers and interpreters connected these foreign buyers with weaving villages along the coast.",
  'సందడిగా',
  "ఇక్కడికి **Persia**, **అరేబియా**, **బర్మా**, **ఆగ్నేయాసియా** నుంచి ఓడలు వచ్చేవి. ⏸ 1600ల మొదట్లో డచ్ వాళ్లు, **1611**లో ఇంగ్లీష్ వాళ్లు ఇక్కడ వ్యాపారం మొదలుపెట్టారు. ⏸ మన దళారులు, **దుబాసీలు** ఈ విదేశీ కొనుగోలుదారులను తీరంలోని నేత గ్రామాలతో కలిపేవారు.",
  'C15','S3','[DRAM] Harbour reconstruction; Rijksmuseum CC0 view of Masulipatnam if located; route lines to Persia/Arakan/Aceh')
a('3.4','NAR','EXP','proud',
  "", 'గర్వంగా',
  "ఒక శతాబ్దం ముందే, గోల్కొండ రాజు **ఇబ్రహీం కుతుబ్ షా**, తన పత్రాల్లో **మల్కిభరాముడు** అనే తెలుగు పేరు వాడాడు. తెలుగు కవులను పోషించాడు.",
  'C22','S3','Qutb Shahi tombs (licensed photo); Telugu manuscript (licence-confirmed)', only='te')
a('3.5','NAR','EXP','light turn',
  "And yes… the **diamonds**.",
  'తేలికగా',
  "ఇక **వజ్రాలు**.",
  '','S3','Diamond glints in candlelight')
a('3.6','NAR','EXP','explaining',
  "On the Krishna river, near today's **Pulichintala**, lay the **Kollur** mines. ⏸ Until Brazil's diamond finds in the **1720s**, India was the world's **major** source of diamonds. A few also came from **Borneo**.",
  'వివరిస్తూ',
  "కృష్ణా నది ఒడ్డున, ఇప్పటి **పులిచింతల** దగ్గర, **కొల్లూరు** గనులు ఉండేవి. ⏸ **1720లలో** బ్రెజిల్‌లో వజ్రాలు దొరికే వరకు, ప్రపంచానికి వజ్రాలు **ప్రధానంగా** భారతదేశం నుంచే వచ్చేవి. **బోర్నియో** నుంచి కొన్ని మాత్రమే.",
  'C16,C19','S3','Map: Kollur pin "KOLLUR MINES · NEAR PULICHINTALA, KRISHNA RIVER" (no district label); inset world: India large, Borneo small, Brazil "1720s"')
a('3.7','NAR','EXP','vivid',
  "Visitors in the early 1620s counted **tens of thousands** of workers here: men, women and children. ⏸ Later, the French jeweller **Tavernier** acquired a remarkable **blue** diamond in India, possibly from the Golconda region. It eventually became the **Hope diamond**.",
  'వర్ణిస్తూ',
  "1620ల మొదట్లో ఇక్కడికి వచ్చిన విదేశీయులు, **పదుల వేల** మంది కూలీలను చూశారు: మగవాళ్లు, ఆడవాళ్లు, పిల్లలు కూడా. ⏸ తర్వాత ఫ్రెంచ్ నగల వ్యాపారి **Tavernier**, భారతదేశంలో ఒక అరుదైన **నీలి** వజ్రం కొన్నాడు, బహుశా గోల్కొండ ప్రాంతం నుంచి. చివరికి అదే ప్రసిద్ధ **Hope diamond** అయింది.",
  'C17,C18','S3','[DRAM] Mine pits with crowds; Tavernier\'s engraved diamond plate (PD, 1676); chip "EXACT MINE UNKNOWN"')
a('3.8','NAR','EXP','careful',
  "Where the **Kohinoor** was mined… historians still **debate**.",
  'జాగ్రత్తగా',
  "**కోహినూర్** ఏ గనిలో దొరికిందో… చరిత్రకారులు ఇప్పటికీ **చర్చిస్తున్నారు**.",
  'C20','S3','Kohinoor silhouette with "?"; tag "DEBATED"')
a('3.9','NAR','PUNCH','reveal',
  "But here's the **surprise**. ⏸ Diamonds made the legends. **Cloth** filled the ships. ⏸ A diamond fits in your **fist**. Cloth filled whole **fleets**, year after year.",
  'ఆశ్చర్యం చెప్తూ',
  "కానీ అసలు **ఆశ్చర్యం** ఇది. ⏸ వజ్రాలు కథలు సృష్టించాయి. ఓడలు నింపింది మాత్రం **గుడ్డే**. ⏸ ఒక వజ్రం **గుప్పిట్లో** పడుతుంది. గుడ్డ మాత్రం ఏటా **ఓడలకు ఓడలు** నింపేది.",
  'C21','S3','Split: a diamond in a palm vs a ship\'s hold packed with bales')
a('3.10','NAR','EXP','wistful',
  "", 'బాధగా',
  "**1687**లో మొఘలులు గోల్కొండను జయించాక, మచిలీపట్నం వైభవం నెమ్మదిగా **తగ్గిపోయింది**.",
  'C14','','Map: Mughal colour floods Golconda; harbour fades', only='te')
a('3.11','NAR','Q','turn',
  "At the port gate, a clerk writes down our cloth and the **duty** it owes. ⏸ Every time it changed hands, someone took a **share**. ⏸ **Who?**",
  'ప్రశ్నగా',
  "రేవు ద్వారం దగ్గర, ఒక గుమాస్తా మన గుడ్డను, దానికి కట్టాల్సిన **సుంకాన్ని** రాసుకుంటున్నాడు. ⏸ అది చేతులు మారిన ప్రతిసారీ, ఎవరో ఒకరు **వాటా** తీసుకున్నారు. ⏸ **ఎవరు?**",
  'C49','','[DRAM] Clerk\'s ledger macro, our cloth\'s stamp')
a('3.12','NAR','ASK','warm, quick',
  "By the way, if this story is new to you too, **subscribe**. ⏸ Season 2 picks up exactly where this one ends.",
  'ఆప్యాయంగా · వేగంగా',
  "ఈ కథ మీకూ కొత్తగా ఉంటే, **subscribe** చేయండి. ⏸ ఇది ఎక్కడ ముగుస్తుందో, సీజన్ 2 అక్కడి నుంచే మొదలవుతుంది.",
  '','','Subscribe chip, light')

# ---------------- COIN ----------------
a('F2.1','CHELLI','DLG','curious',
  "Anna, whose **face** is on this coin?",
  'ఆసక్తిగా',
  "అన్నా, ఈ నాణెం మీద ఎవరి **ముఖం**?",
  '','','[DRAM] Chelli lifts the coin (EN: Mughal silver rupee · TE: Golconda gold pagoda/hun)')
a('F2.2','ANNA','DLG','thoughtful',
  "No face. Just a **king's name**. ⏸ But a name on a coin doesn't tell you who really held the **wealth**.",
  'ఆలోచనగా',
  "ముఖం లేదు, ఒక **రాజు పేరు** మాత్రమే. ⏸ కానీ నాణెం మీద పేరు ఉన్నంతమాత్రాన, అసలు **సంపద** ఎవరి చేతిలో ఉందో తెలియదు.",
  '','','Coin macro, Persian script')

# ---------------- CH4 ----------------
a('4.0','NAR','CHAP','chapter',
  "Chapter four. **Who controlled the wealth?**", 'అధ్యాయం',
  "నాలుగో అధ్యాయం. **సంపద ఎవరి చేతిలో?**", '','','Chapter card; progress 4/6')
a('4.1','NAR','Q','pointed',
  "If India made so much… why were the people who made it often so **poor**?",
  'సూటిగా',
  "దేశం ఇంత తయారుచేస్తే… దాన్ని తయారుచేసిన వాళ్లే ఎందుకు ఇంత **పేదవాళ్లుగా** ఉండేవారు?",
  '','','Weaver\'s empty bowl beside a bale of chintz')
a('4.2','NAR','EXP','explaining, map',
  "First, there was no single India. ⏸ Kingdoms rose and fell. ⏸ In the south, **Vijayanagara**'s great capital was sacked after the battle of **Talikota** in 1565, but its **Aravidu** kings ruled on from other forts for decades. ⏸ The Deccan sultanates, like Golconda, held the middle. ⏸ And the **Mughal** empire kept pushing south.",
  'వివరిస్తూ',
  "మొదట, అప్పుడు **ఒకే భారతదేశం** లేదు. ⏸ రాజ్యాలు పుట్టాయి, పడిపోయాయి. ⏸ దక్షిణాన, 1565 **తళ్లికోట** యుద్ధం తర్వాత **విజయనగరం** రాజధాని దోపిడీకి గురైంది. కానీ **ఆరవీడు** రాజులు పెనుగొండ, చంద్రగిరి, వెల్లూరు నుంచి దశాబ్దాల పాటు పాలన కొనసాగించారు. ⏸ మధ్యలో గోల్కొండ లాంటి దక్కన్ సుల్తానుల రాజ్యాలు. ⏸ ఉత్తరం నుంచి **మొఘల్** సామ్రాజ్యం దక్షిణానికి విస్తరిస్తూనే ఉంది.",
  'C23','S4','Master map animates 1500→1690: Vijayanagara → Aravidu seats (Penukonda, Chandragiri, Vellore); sultanates; Mughal advance')
a('4.3','NAR','EXP','proud',
  "", 'గర్వంగా',
  "అంతకుముందే, విజయనగర రాజు **శ్రీకృష్ణదేవరాయలు** తెలుగులో **ఆముక్తమాల్యద** రాశాడు. అందులో విష్ణువు నోట వచ్చే ప్రసిద్ధ మాట: **దేశ భాషలందు తెలుగు లెస్స**.",
  'C24','S4','Hampi ruins (licensed photo); verse in Telugu script on screen', only='te')
a('4.4','NAR','EXP','authoritative',
  "The Mughal empire was one of the **largest states** on Earth. ⏸ Under **Akbar**, his minister **Todar Mal** measured the land and set revenue by survey.",
  '', '', 'C26','S4','Mughal miniature of a land survey (Met OA, to select)', only='en')
a('4.5','NAR','EXP','turn',
  "But kings come and go. The **system** lasted. ⏸ Follow the **money**.",
  'మలుపు',
  "కానీ రాజులు వస్తారు, పోతారు. **వ్యవస్థ** మాత్రం నిలిచింది. ⏸ **డబ్బు** వెనకే వెళ్దాం.",
  '','S4','A single coin rolls from a field toward a palace')
a('4.6','NAR','LIST','brisk list',
  "The farmer paid **land revenue**. Historians estimate it was often **a third to a half** of the crop. ⏸ Collectors and local lords took their **cut**. ⏸ The state spent it on **armies** and **courts**. ⏸ Bankers lent to **everyone**. ⏸ And a foreign merchant needed a **farman**, a royal permission, just to trade.",
  'వేగంగా · జాబితాగా',
  "రైతు **భూమి శిస్తు** కట్టేవాడు. అది తరచుగా పంటలో **మూడో వంతు నుంచి సగం** వరకు ఉండేదని చరిత్రకారుల అంచనా. ⏸ వసూలు చేసేవాళ్లు, స్థానిక పెద్దలు తమ **వాటా** తీసుకునేవారు. ⏸ రాజ్యం ఆ డబ్బును **సైన్యాలకు**, **దర్బార్లకు** ఖర్చుపెట్టేది. ⏸ వడ్డీ వ్యాపారులు **అందరికీ** అప్పులిచ్చేవారు. ⏸ విదేశీ వ్యాపారి వ్యాపారం చేయాలంటే, రాజు ఇచ్చే అనుమతి పత్రం, **ఫర్మానా** కావాలి.",
  'C25','S4','Flow diagram: field → collector/zamindar → treasury → army & court; banker arrows to all; farman scroll')
a('4.7','NAR','EXP','storytelling',
  "", 'కథ చెప్తూ',
  "గోల్కొండలో, **మాదన్న**, **అక్కన్న** అనే తెలుగు సోదరులు, అబుల్ హసన్ కుతుబ్ షా దగ్గర మంత్రులుగా రాజ్య పాలన, ఆదాయ వ్యవహారాలు నడిపారు.",
  'C27','S4','[DRAM] Two ministers over revenue ledgers', only='te')
a('4.8','NAR','EXP','impressed',
  "Bankers could be enormously powerful. ⏸ In Surat, **Virji Vora** lent money to the English company again and again. Its own records called him the **richest merchant** of his time. ⏸ But even he lived by the ruler's **permission**.",
  'ఆశ్చర్యంగా',
  "సూరత్‌లో **విర్జీ వోరా** అనే వ్యాపారి, ఇంగ్లీష్ కంపెనీకి పదే పదే అప్పులిచ్చాడు. కంపెనీ రికార్డులే అతన్ని ఆ కాలంలో **అత్యంత ధనిక** వ్యాపారిగా వర్ణించాయి. ⏸ కానీ అతను కూడా రాజు **అనుమతితోనే** బతికాడు.",
  'C28','S4','[DRAM] Surat counting-house; Company factory-record page (BL, licence-confirmed) or reconstruction')
a('4.9','NAR','PUNCH','serious, slower',
  "And when the rains failed… wealth at the top did not protect the people at the **bottom**.",
  'గంభీరంగా · నెమ్మదిగా',
  "వానలు పడకపోతే… పైనున్న సంపద కిందున్నవాళ్లను **కాపాడలేదు**.",
  '','S4','Cracked earth; music drops out')
a('4.10','NAR','EXP','serious',
  "From **1630 to 1632**, famine struck Gujarat and the Deccan. An English traveller, **Peter Mundy**, described roads lined with the dead. ⏸ Estimates run into the **millions**. ⏸ Many weavers died… or fled.",
  'గంభీరంగా',
  "**1630 నుంచి 1632** వరకు, గుజరాత్‌లో, దక్కన్‌లో కరువు వచ్చింది. **Peter Mundy** అనే ఇంగ్లీష్ యాత్రికుడు, దారుల నిండా శవాలు ఉన్నాయని రాశాడు. ⏸ చనిపోయినవాళ్లు **పదుల లక్షల్లో** ఉంటారని అంచనా. ⏸ ఎంతోమంది నేతగాళ్లు చనిపోయారు… లేదా ఊళ్లు వదిలి వెళ్లిపోయారు.",
  'C29','S4','Restrained: empty loom, dust road, Mundy journal page (PD); no graphic imagery; chip "ESTIMATES"')
a('4.11','NAR','EXP','transition',
  "Every ruler wanted one thing: **trade**. Because trade meant **taxes**. ⏸ And the richest trade… came by **sea**.",
  'కథ చెప్తూ',
  "ప్రతి రాజూ ఒక్కటే కోరుకున్నాడు: **వ్యాపారం**. ఎందుకంటే వ్యాపారం అంటే **పన్నులు**. ⏸ అతి ధనిక వ్యాపారం… **సముద్రం** మీదుగా వచ్చేది.",
  '','','[DRAM] Our bale hoisted aboard a ship at Machilipatnam')

# ---------------- CH5 ----------------
a('5.0','NAR','CHAP','chapter',
  "Chapter five. **Europe didn't discover India.**", 'అధ్యాయం',
  "ఐదో అధ్యాయం. **యూరప్ భారత్‌ను కనిపెట్టలేదు.**", '','','Chapter card; progress 5/6; chip "1498 · the sea before our ship"')
a('5.1','NAR','Q','provocative',
  "In **1498**, Vasco da Gama reached India. ⏸ So who showed him the **way**?",
  'ప్రశ్నగా',
  "**1498**లో వాస్కో డ గామా భారతదేశం చేరాడు. ⏸ మరి అతనికి **దారి** చూపించింది ఎవరు?",
  '','','Cantino planisphere 1502 (PD), slow push')
a('5.2','NAR','EXP','storytelling',
  "Our cloth's ship sails out of Machilipatnam onto an ocean that had been busy for **centuries**.",
  'కథ చెప్తూ',
  "మచిలీపట్నం నుంచి బయల్దేరిన మన గుడ్డ ఓడ, **శతాబ్దాలుగా** రద్దీగా ఉన్న సముద్రంలోకి వెళ్తోంది.",
  'C49','','[DRAM] Ship clears the harbour; master map pulls out to the Indian Ocean')
a('5.3','NAR','EXP','sweeping',
  "**Indian**, **Arab**, **Persian**, **African**, **Chinese** and **Malay** traders crossed it long before any European. ⏸ At **Malacca**, Gujarati merchants were among the biggest traders.",
  'విస్తృతంగా',
  "ఏ యూరోపియన్ రాకముందే, **భారతీయులు**, **అరబ్బులు**, **పర్షియన్లు**, **ఆఫ్రికన్లు**, **చైనీయులు**, **మలయా** వ్యాపారులు ఈ సముద్రాన్ని దాటేవారు. ⏸ **మలక్కాలో** అతిపెద్ద వ్యాపారుల్లో గుజరాతీలు కూడా ఉండేవారు.",
  'C30','S5','Route lines light up port by port')
a('5.4','NAR','EXP','proud',
  "", 'గర్వంగా',
  "మన తీరం అంతకంటే ఎంతో ముందే సముద్ర వ్యాపారం చేసింది. ⏸ తెలుగు నేలలో **రోమన్ నాణేలు** కూడా దొరికాయి.",
  'C34','','Roman coin (museum OA image); map pin on the Telugu region', only='te')
a('5.5','NAR','EXP','explaining',
  "Their secret was the **wind**. ⏸ The **monsoon** blows one way for half the year, and back the other way for the rest. ⏸ Sailors timed whole voyages around it.",
  'వివరిస్తూ',
  "వాళ్ల రహస్యం **గాలి**. ⏸ **రుతుపవనాలు** సగం సంవత్సరం ఒక వైపు, మిగతా సగం మరో వైపు వీస్తాయి. ⏸ నావికులు తమ ప్రయాణాలన్నీ దాని ప్రకారమే ప్లాన్ చేసేవారు.",
  'C30','S5','Wind arrows reverse across the map; dhow sail fills (DRAM)')
a('5.6','NAR','EXP','storytelling',
  "So in 1498, when da Gama reached **Malindi** in East Africa, he took on an experienced **pilot**… who guided his ships across to **Calicut**. ⏸ Who that pilot was, historians still **debate**.",
  'కథ చెప్తూ',
  "1498లో డ గామా తూర్పు ఆఫ్రికాలోని **మాలిండి** చేరినప్పుడు, అక్కడ అనుభవం ఉన్న ఒక **దారిచూపే నావికుడిని** ఎక్కించుకున్నాడు. అతనే ఓడలను **కాలికట్** వరకు తీసుకొచ్చాడు. ⏸ ఆ నావికుడు ఎవరనేది… చరిత్రకారులు ఇప్పటికీ **చర్చిస్తున్నారు**.",
  'C31,C32','S5','Route Malindi → Calicut; silhouette pilot with "?"; tag "DEBATED"')
a('5.7','NAR','EXP','vivid, with a smile',
  "His crew's own journal records a strange welcome. ⏸ Two merchants from **Tunis**, who spoke Spanish and Italian, asked the first Portuguese man ashore: 'What brought you **here**?' ⏸ The answer: '**Christians**… and **spices**.'",
  'వర్ణిస్తూ · చిరునవ్వుతో',
  "డ గామా సిబ్బంది డైరీలో ఒక విచిత్రమైన స్వాగతం ఉంది. ⏸ **ట్యూనిస్** నుంచి వచ్చిన ఇద్దరు వ్యాపారులు, ఒడ్డుకి వచ్చిన మొదటి పోర్చుగీస్ మనిషిని అడిగారు: 'ఇంత దూరం **ఎందుకొచ్చారు**?' ⏸ జవాబు: '**క్రైస్తవుల** కోసం… **సుగంధ ద్రవ్యాల** కోసం.'",
  'C33','S5','[DRAM] Calicut shore 1498; Roteiro page (PD) with the line highlighted')
a('5.8','NAR','PUNCH','amused',
  "And da Gama's gifts for the king? **Hats**, **coral**, **sugar**, **honey**. ⏸ The king's officials **laughed**. They said the poorest merchant from Mecca gave more.",
  'నవ్వుతూ',
  "రాజు కోసం డ గామా తెచ్చిన కానుకలు? **టోపీలు**, **పగడాలు**, **చక్కెర**, **తేనె**. ⏸ రాజు అధికారులు **నవ్వారు**. మక్కా నుంచి వచ్చే అతి పేద వ్యాపారి కూడా ఇంతకంటే ఎక్కువ ఇస్తాడన్నారు.",
  'C33','S5','[DRAM] Gifts laid out; courtiers smiling')
a('5.9','NAR','EXP','worldly',
  "Europe hadn't found a **new** world here. It had joined an **old** one… and it wanted to get past the middlemen who controlled the spice trade to Europe.",
  '', '', 'C30','S5','Spice route via Red Sea/Gulf to Venice dims; Cape route lights', only='en')
a('5.10','NAR','PUNCH','turn',
  "The Portuguese came with **cannons**. ⏸ A century later, the English came asking **politely**.",
  'మలుపు',
  "పోర్చుగీసులు **ఫిరంగులతో** వచ్చారు. ⏸ ఒక శతాబ్దం తర్వాత, ఇంగ్లీష్ వాళ్లు **మర్యాదగా** అనుమతి అడుగుతూ వచ్చారు.",
  '','S5','Portuguese cannon → English bow')

# ---------------- CH6 ----------------
a('6.0','NAR','CHAP','chapter',
  "Chapter six. **The company that came to trade.**", 'అధ్యాయం',
  "ఆరో అధ్యాయం. **వ్యాపారం కోసం వచ్చిన కంపెనీ.**", '','','Chapter card; progress 6/6; chip "1600 → 1757"')
a('6.1','NAR','Q','intrigue',
  "The East India Company arrived asking for **permission**. ⏸ How did it end up giving **orders**?",
  'ఆసక్తి రేపుతూ',
  "East India Company **అనుమతి** అడుగుతూ వచ్చింది. ⏸ మరి చివరికి **ఆజ్ఞలు** ఇచ్చే స్థాయికి ఎలా చేరింది?",
  '','S6','Company coat of arms (PD)')
a('6.2','NAR','EXP','storytelling',
  "It began as a **business**, not a country. ⏸ On the last day of **1600**, a group of London merchants received a royal **charter**. Two years later, the Dutch formed their own company.",
  'కథ చెప్తూ',
  "అది ఒక దేశం కాదు, ఒక **వ్యాపారం**. ⏸ **1600** చివరి రోజున, లండన్ వ్యాపారుల బృందానికి రాణి **charter** ఇచ్చింది. రెండేళ్ల తర్వాత డచ్ వాళ్లు తమ కంపెనీ పెట్టారు.",
  'C35','S6','[DRAM] London street 1600; charter document')
a('6.3','NAR','EXP','steady, dates clear',
  "In **1608**, William Hawkins reached **Surat** and travelled to the court of the emperor **Jahangir**. ⏸ In **1612**, English ships beat a Portuguese fleet off Swally, near Surat, and Mughal officials took notice. ⏸ A deal with Surat's governor was confirmed by the emperor in early **1613**. ⏸ And from 1615 to 1619, King James's ambassador, Sir **Thomas Roe**, stayed at the court, pressing for better terms.",
  'స్థిరంగా · తేదీలు స్పష్టంగా',
  "**1608**లో William Hawkins **సూరత్** చేరి, **జహంగీర్** దర్బారుకి వెళ్లాడు. ⏸ **1612**లో, సూరత్ దగ్గర Swally వద్ద ఇంగ్లీష్ ఓడలు పోర్చుగీస్ నౌకాదళాన్ని ఓడించాయి. మొఘల్ అధికారులు గమనించారు. ⏸ **1613** మొదట్లో, సూరత్ గవర్నర్‌తో చేసుకున్న ఒప్పందాన్ని చక్రవర్తి ఆమోదించాడు.",
  'C36,C37,C38','S6','Surat on the master map; naval engraving (PD); Mughal court painting (Met OA, to select — NOT the Freer Bichitr, restricted)')
a('6.4','NAR','PUNCH','quiet',
  "Step by step. **Permission** by permission.",
  'నెమ్మదిగా',
  "అడుగు తర్వాత అడుగు. **అనుమతి** తర్వాత అనుమతి.",
  '','S6','Stamps land one after another on a ledger')
a('6.5','NAR','EXP','storytelling',
  "On the east coast, the English traded at **Machilipatnam** from 1611. ⏸ And in **1639**, the **Damarla** Nayakas, local rulers of this coast under the Vijayanagara king, granted them a strip of land by the sea. ⏸ It would become **Madras**.",
  'కథ చెప్తూ · గర్వంగా',
  "తూర్పు తీరంలో, **1611** నుంచే ఇంగ్లీష్ వాళ్లు మన **మచిలీపట్నంలో** వ్యాపారం చేశారు. ⏸ **1639**లో, ఈ తీరాన్ని విజయనగర రాజు కింద పాలించిన **దామెర్ల నాయకులు**, వాళ్లకు సముద్రతీరంలో ఒక చిన్న భూమి ఇచ్చారు. ⏸ అదే తర్వాత **మద్రాసు** అయింది.",
  'C15,C39','S6','Master map: Machilipatnam → Madras pins (TE zoom 2); Fort St George early view (PD print, date to confirm)')
a('6.6','NAR','EXP','explaining',
  "There was one **problem**. ⏸ Europe made very little that India wanted. So the Company paid mostly in **silver**.",
  'వివరిస్తూ',
  "కానీ ఒక **సమస్య**. ⏸ భారతదేశానికి కావాల్సినవి యూరప్ పెద్దగా తయారుచేసేది కాదు. అందుకే కంపెనీ ఎక్కువగా **వెండితోనే** చెల్లించేది.",
  'C40','S6','Silver bars and coins pour into a chest at the dock')
a('6.7','NAR','EXP','storytelling, warm',
  "And around **1680**, a Company ship like this one carried **our cloth** to London. ⏸ In a warehouse by the Thames, the bales were cut open… and our cloth was sold at the Company's **sale**.",
  'కథ చెప్తూ · ఆప్యాయంగా',
  "దాదాపు **1680**లో, ఇలాంటి ఒక కంపెనీ ఓడ **మన గుడ్డను** లండన్‌కి తీసుకెళ్లింది. ⏸ థేమ్స్ నది పక్కన ఒక గోదాములో మూటలు విప్పారు… మన గుడ్డను కంపెనీ **వేలంలో** అమ్మేశారు.",
  'C49','','[DRAM] chip "OUR CLOTH · LONDON · c.1680"; warehouse, bale cut open, gavel; East India House print (PD)')
a('6.8','NAR','EXP','turn',
  "Our cloth's journey ends there. ⏸ The **Company's** story doesn't.",
  'మలుపు',
  "మన గుడ్డ ప్రయాణం అక్కడితో ముగిసింది. ⏸ కానీ **కంపెనీ** కథ ఆగలేదు.",
  '','','Year chip spins c.1680 → 1717')
a('6.8b','NAR','EXP','storytelling, a little wry',
  "And the Company had already tried **force** once. ⏸ In **1686**, it went to war against the Mughal emperor **Aurangzeb**… and **lost**. ⏸ Its envoys had to beg the emperor's **pardon**, pay a heavy **fine**, and promise to behave. ⏸ Only then could it trade again. And in **1690**, it set up a new base in Bengal: **Calcutta**.",
  'కథ చెప్తూ',
  "నిజానికి కంపెనీ ఒకసారి **బలప్రయోగానికి** ప్రయత్నించింది. ⏸ **1686**లో మొఘల్ చక్రవర్తి **ఔరంగజేబుతో** యుద్ధానికి దిగి… **ఓడిపోయింది**. ⏸ దాని దూతలు చక్రవర్తిని **క్షమాపణ** వేడుకున్నారు, భారీ **జరిమానా** కట్టారు, ఇక బుద్ధిగా ఉంటామని మాటిచ్చారు. ⏸ అప్పుడే మళ్లీ వ్యాపారానికి అనుమతి దొరికింది. **1690**లో బెంగాల్‌లో కొత్త స్థావరం పెట్టింది: **కలకత్తా**.",
  'C51','S6','Mughal fleet blockading Bombay (period print or AI); chip "ANGLO-MUGHAL WAR 1686–90 · MUGHAL VICTORY" (fine amount shown only if verified in Keay, India: A History, p. 372)')
a('6.9','NAR','EXP','precise',
  "In **1717**, Emperor **Farrukhsiyar** granted it a farman: duty-free trade in **Bengal**, for a fixed **3,000 rupees** a year, with passes called **dastaks**. ⏸ Company men soon **misused** those passes for their own private trade.",
  'ఖచ్చితంగా',
  "**1717**లో చక్రవర్తి **ఫరూఖ్‌సియర్** ఒక ఫర్మానా ఇచ్చాడు: ఏటా **3,000 రూపాయలు** కడితే, **బెంగాల్‌లో** సుంకం లేని వ్యాపారం, **దస్తక్** అనే పాసులు. ⏸ కంపెనీ ఉద్యోగులు త్వరలోనే ఆ పాసులను తమ సొంత వ్యాపారానికి **దుర్వినియోగం** చేశారు.",
  'C41','S6','Farman scroll (reconstruction); dastak pass; private boats slipping past a toll post')
a('6.10','NAR','EXP','darker',
  "Then came the **wars**. ⏸ In the 1740s and 50s, the French and English companies fought each other in South India. They trained Indian soldiers, called **sepoys**, in European drill. ⏸ And they backed rival claimants to the thrones of the **Carnatic** and **Hyderabad**. The **French** did it first.",
  'గంభీరంగా',
  "తర్వాత **యుద్ధాలు**. ⏸ 1740, 50లలో, దక్షిణ భారతదేశంలో ఫ్రెంచ్, ఇంగ్లీష్ కంపెనీలు ఒకదానితో ఒకటి పోరాడాయి. **సిపాయిలు** అనే భారతీయ సైనికులకు యూరోపియన్ పద్ధతిలో శిక్షణ ఇచ్చాయి. ⏸ **కర్ణాటక**, **హైదరాబాద్** సింహాసనాల కోసం పోటీపడుతున్న వారసుల్లో, తమకు నచ్చినవాళ్లకు మద్దతిచ్చాయి. మొదట ఈ పని చేసింది **ఫ్రెంచ్** వాళ్లే.",
  'C42','S6','[DRAM] Sepoy drill; map: rival claimants with French/English flags (Arcot, Hyderabad)')
a('6.11','NAR','EXP','regional',
  "", 'కథ చెప్తూ',
  "1750లలో, మచిలీపట్నంతో సహా మన **తీర ప్రాంతాలపై** ఫ్రెంచ్ వాళ్లకు పట్టు దొరికింది.",
  'C43','','Map: coastal Andhra shaded French blue (TE zoom 3)', only='te')
a('6.12','NAR','PUNCH','ominous, slow',
  "The traders had learned something **dangerous**. ⏸ Fighting the Mughals had failed. But choosing rulers… **paid**.",
  'భయం కలిగించేలా · నెమ్మదిగా',
  "వ్యాపారులు ఒక **ప్రమాదకరమైన** విషయం నేర్చుకున్నారు. ⏸ మొఘలులతో యుద్ధం ఓడిపోయింది. కానీ రాజులను ఎంచుకోవడం… **లాభం**.",
  'C42','S6','Chess-piece king lifted by a merchant\'s hand')
a('6.13','NAR','EXP','tense',
  "In Bengal, the young Nawab **Siraj-ud-Daulah** was angry: the Company was building **fortifications** and abusing its passes. ⏸ In **1756**, he seized **Calcutta**. ⏸ The Company sent an army from Madras.",
  'ఉద్విగ్నంగా',
  "బెంగాల్‌లో యువ నవాబు **సిరాజ్-ఉద్-దౌలా** కోపంగా ఉన్నాడు: కంపెనీ **కోటలు** కడుతోంది, పాసులను దుర్వినియోగం చేస్తోంది. ⏸ **1756**లో అతను **కలకత్తాను** స్వాధీనం చేసుకున్నాడు. ⏸ కంపెనీ మద్రాసు నుంచి సైన్యాన్ని పంపింది.",
  'C44','S6','Calcutta 1750s print (PD); ships sailing north from Madras on the map')

# ---------------- FINAL 60 ----------------
a('7.1','NAR','EXP','warm, reflective',
  "For a hundred and fifty years, the Company asked **permission**, paid in **silver**, and traded. ⏸ Then came **Plassey**.",
  'ఆలోచనగా',
  "నూట యాభై ఏళ్లు కంపెనీ **అనుమతి** అడిగింది, **వెండి** ఇచ్చింది, వ్యాపారం చేసింది. ⏸ తర్వాత వచ్చింది **ప్లాసీ**.",
  'C40','','Callback: our cloth in lamplight → mist over a mango grove')
a('7.2','NAR','EXP','dramatic',
  "On **23 June 1757**, in Bengal, about **three thousand** Company troops faced an army of around **fifty thousand**.",
  'నాటకీయంగా',
  "**1757 జూన్ 23**, బెంగాల్. దాదాపు **మూడు వేల** మంది కంపెనీ సైనికులు… ఎదురుగా దాదాపు **యాభై వేల** సైన్యం.",
  'C45','S6','[DRAM] Plassey lines in mist (AI reconstruction; Hayman/NPG painting NOT used — commercial licence)')
a('7.3','NAR','PUNCH','low, deliberate',
  "Much of that army never **fought**. ⏸ Its commander, **Mir Jafar**, had made a secret deal… and the Company helped put him on Bengal's **throne**.",
  'నెమ్మదిగా · బరువుగా',
  "కానీ ఆ సైన్యంలో చాలామంది యుద్ధమే **చేయలేదు**. ⏸ సేనాని **మీర్ జాఫర్** ముందే రహస్య ఒప్పందం చేసుకున్నాడు… కంపెనీ అతన్నే బెంగాల్ **నవాబుగా** కూర్చోబెట్టింది.",
  'C45','S6','Still ranks on one flank; a throne cushion')
a('7.4','NAR','EXP','regional, quick',
  "", 'వేగంగా',
  "రెండేళ్లకే, **1759**లో, కంపెనీ సైన్యం ఫ్రెంచ్ వాళ్ల నుంచి మన **మచిలీపట్నాన్ని** స్వాధీనం చేసుకుంది.",
  'C46','','Map zoom to Machilipatnam, cannon smoke', only='te')
a('7.5','NAR','EXP','building',
  "Plassey didn't conquer **India**. ⏸ But at **Buxar** in 1764, the Company won again. ⏸ And in **1765**, the Mughal emperor granted it the right to collect the **revenue** of Bengal, Bihar and Orissa.",
  'పెరుగుతూ',
  "ప్లాసీ భారతదేశాన్ని **జయించలేదు**. ⏸ కానీ **1764**లో **బక్సర్‌లో** కంపెనీ మళ్లీ గెలిచింది. ⏸ **1765**లో బెంగాల్, బీహార్, ఒరిస్సాల **ఆదాయం** వసూలు చేసే హక్కు, మొఘల్ చక్రవర్తి నుంచి కంపెనీకి వచ్చింది.",
  'C45,C47','S6','Map: Bengal only changes colour; Buxar marker 1764; diwani scroll 1765 (EN also shows Madras/Bombay footholds)')
a('7.6','ANNA','DLG','quiet, heavy',
  "Think about our cloth. ⏸ For a hundred and fifty years, they brought **silver** from across the world to buy cloth like it. ⏸ Now… they could increasingly pay with **taxes** collected in India itself.",
  'నెమ్మదిగా · బరువుగా',
  "మన గుడ్డ గురించి ఆలోచించు. ⏸ నూట యాభై ఏళ్లు, సముద్రాల అవతల నుంచి **వెండి** తెచ్చి ఇలాంటి గుడ్డ కొన్నారు. ⏸ ఇప్పుడు… ఇక్కడే వసూలు చేసిన **పన్నులతోనే** ఎక్కువగా కొనగలరు.",
  'C48','S6','[DRAM] Trunk: Chelli holds Ammamma\'s cloth, Anna holds the coin')
a('7.7','CHELLI','DLG','small, uneasy',
  "So the traders became **kings**?",
  'అయోమయంగా',
  "అంటే వ్యాపారులు **రాజులైపోయారా**?",
  '','','Chelli looks up')
a('7.8','ANNA','DLG','quiet',
  "Not **yet**.",
  'నెమ్మదిగా',
  "**ఇంకా** కాదు.",
  '','','Anna folds the cloth into the trunk')
a('7.9','NAR','Q','final question, slow',
  "What happens when a company that once needed permission to trade… starts collecting the **taxes**?",
  'చివరి ప్రశ్న · నెమ్మదిగా',
  "ఒకప్పుడు వ్యాపారానికి అనుమతి అడిగిన కంపెనీ… **పన్నులే** వసూలు చేయడం మొదలుపెడితే ఏమవుతుంది?",
  'C48','S6-end','Lid closes → card THE GOLDEN SPARROW · SEASON 2 · HOW A COMPANY BECAME AN EMPIRE (TE: బంగారు పిచ్చుక · సీజన్ 2 · ఒక కంపెనీ సామ్రాజ్యం ఎలా అయింది); end screen')

L = [x for x in L if x]
