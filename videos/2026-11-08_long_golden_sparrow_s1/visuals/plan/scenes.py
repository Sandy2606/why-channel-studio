# Scene-by-scene visual plan. One entry per recorded line (film order). Fields:
# id, style, picture (what is on screen + how it moves), camera, sync (narration cues), en (on-screen text EN), te (TE),
# assets, vert (9:16 recomposition), sens (sensitive-scene rule, optional)
# style: CIN = cinematic reconstruction (parallax, atmosphere) · MAP = animated map · EVID = evidence (documents, museum objects)
#        DATA = data graphic · TITLE = title / chapter card · DLG = Anna-Chelli frame story
S = []
def s(id, style, picture, camera, sync, en='', te='', assets=(), vert='', sens=''):
    S.append(dict(id=id, style=style, picture=picture, camera=camera, sync=sync, en=en, te=te, assets=list(assets), vert=vert, sens=sens))

# ================= COLD OPEN
s('0.1', 'EVID', 'Black, loom-shuttle sound, then a macro of a painted flower on the palampore; the frame darkens as "WHY?" lands.',
  'Slow push-in on the flower (2.0x → 2.2x).', '"1721" chip on "1721"; "WHY?" on "Why?".',
  '1721 · BRITAIN BANS PRINTED COTTON → WHY?', '1721 · అచ్చు గుడ్డలపై బ్రిటన్ నిషేధం → ఎందుకు?', ['MET1', 'GX-TEXT'],
  'Same macro, centred; chip at y≈1250, "WHY?" centre, 150 px.')
s('0.2', 'EVID', 'Pull back to reveal the whole palampore; wool and silk swatches slide in dimmed at the sides.',
  'Pull-out from macro to the full cloth on a blurred fill.', 'Swatches on "wool" / "silk"; cloth glows on "Indian cotton".',
  'small caption: Palampore · Coromandel Coast · The Met', 'పలంపోర్ · కోరమాండల్ తీరం · The Met', ['MET1', 'GX-TEXT'],
  'Cloth fills the height; swatches above and below instead of left and right.')
s('0.3', 'CIN', 'Three cuts timed to the three nouns: monsoon ship (pepper) → Tavernier diamond plate (diamonds) → back to the cloth (cloth).',
  'Each shot drifts in the direction of the next.', 'Cut on "pepper", "diamonds", "cloth" (TE: మిరియాల, వజ్రాల, గుడ్డ).',
  '', '', ['T1', 'PD02', 'MET1'], 'Same cuts, recentred.')
s('0.4', 'MAP', 'World map draws in; the undivided subcontinent fills gold; one chip.', 'Slow push toward South Asia.',
  'Fill starts on "India" / "భారతదేశానిదే"; chip on "a quarter".',
  'c.1700 · ABOUT A QUARTER OF WORLD OUTPUT · MADDISON ESTIMATE', 'సుమారు 1700 · ప్రపంచ ఉత్పత్తిలో నాలుగో వంతు · మాడిసన్ అంచనా', ['M-WORLD', 'GX-TEXT'],
  'Map in the upper 60%, chip below.')
s('0.5', 'TITLE', 'The Company sail fills the frame, fades to black; title card lands on the impact.',
  'Slow push into the sail.', 'Fade begins after "trade?" / "వెళ్లింది?"; title on the boom.',
  'THE GOLDEN SPARROW · SEASON 1', 'బంగారు పిచ్చుక · సీజన్ 1', ['T2', 'GX-CARD'], 'Title stacked on two lines.')

# ================= TRUNK
s('F1.1', 'DLG', 'Anna and Chelli open the trunk.', 'Gentle push toward the cloth.', 'Chelli\'s line starts the shot.', '', '', ['T3'],
  '9:16 starts on Chelli (she speaks), drifts to the trunk.')
s('F1.2', 'DLG', 'Close-up: Anna traces the painted border; on "London" the cloth\'s border is masked and a thin gold route line runs from the coast to London on a small map inset.',
  '2.5D parallax: hands and cloth move against the soft background.', 'Map inset on "London" / "లండన్".', '', '', ['T4', 'GX-PARALLAX', 'M-WORLD'],
  'Close on Chelli\'s face and the finger; inset at top.')
s('F1.3', 'DLG', 'Tag appears; match-cut from the painted cotton plant on the museum cloth to a real cotton field at dawn.',
  'Match-cut on shape.', 'Tag on "reconstruction" / "ఊహ"; cut on "Let\'s follow it" / "వెళ్దాం".',
  'DRAMATIZED RECONSTRUCTION · BASED ON SURVIVING MUSEUM CHINTZ', 'నాటకీయ పునఃసృష్టి · మ్యూజియంలోని అసలు చింట్జ్ ఆధారంగా', ['T4', 'MET1', 'G01'],
  'Tag at top (y≈220), 2 lines.')

# ================= CH 1
s('1.0', 'TITLE', 'Chapter card over the dawn field.', 'Static card, field drifts.', 'Card on the boom.',
  'CHAPTER 1 · WAS INDIA REALLY THAT RICH? · c.1680', 'మొదటి అధ్యాయం · భారతదేశం నిజంగా అంత ధనికమా? · సుమారు 1680', ['GX-CARD', 'G01'], '')
s('1.1', 'CIN', 'A gold sparrow line-drawing traces itself and dissolves into the dawn field.', 'Parallax on the field.',
  '"golden sparrow" draws the bird; dissolve on "story".', '', '', ['G01', 'GX-PARALLAX'], '')
s('1.2', 'CIN', 'The family picks cotton at dawn.', 'Parallax dolly through the plants (foreground bolls slide past).',
  'Chip on "1680".', 'OUR CLOTH · c.1680', 'మన గుడ్డ · సుమారు 1680', ['G02', 'GX-PARALLAX'], 'Crop on the mother and grandmother.')
s('1.3', 'EVID', 'Timeline card: "Mehrgarh · c. 5000 BCE · earliest cotton threads found" with a map pin; field behind, dimmed.',
  'Timeline slides from right.', 'Pin on "thousands of years".', 'MEHRGARH · c.5000 BCE · EARLIEST KNOWN COTTON', 'మెహర్‌గఢ్ · సుమారు క్రీ.పూ. 5000 · తొలి పత్తి ఆనవాళ్లు',
  ['GX-DOC', 'M-SA', 'G01'], '')
s('1.4', 'DATA', 'APPROVED POC: world map, 100-square grid, India 24 → Britain 3 → 1950 India 4 with the border change.',
  'Map camera: wide → 1950 zoom.', 'Squares on "24", "three", "four" (TE: phrase ends).',
  'INDIAN SUBCONTINENT · c.1700 | INDIA · 1950 (DIFFERENT TERRITORY)', 'భారత ఉపఖండం · సుమారు 1700 | భారతదేశం · 1950 (వేరే భూభాగం)',
  ['M-WORLD', 'M-SA', 'GX-DATA'], 'Approved 9:16 layout; territory labels enlarged to 40 px and moved above the map.')
s('1.4e', 'DATA', 'EN only: China fills teal, 22 squares; bracket "INDIA + CHINA: ALMOST HALF".', 'Map back to wide.', 'On "22" and "half".',
  'INDIA + CHINA: ALMOST HALF', '', ['M-WORLD', 'GX-DATA'], '')
s('1.5', 'DATA', 'APPROVED POC: rows of dull coins, one glows gold.', 'Static, coins drop in.', 'Coins on "every"; gold coin on "rich".',
  'A BIG SHARE, BUT NOT EVERYONE RICH', 'పెద్ద వాటా, కానీ అందరూ ధనికులు కాదు', ['GX-DATA', 'GX-PART'], '')
s('1.6', 'DATA', 'APPROVED POC: 100 people, 27 light gold; loom parallax with the equation; income bars against the world-average line.',
  'Parallax dolly on T6.', 'People on "quarter"; equation on "huge" / "made things"; bars on "world average", "Western Europe".',
  'ABOUT 1 IN 4 PEOPLE LIVED HERE · MANY PEOPLE + MAKING THINGS = A BIG SHARE', 'ప్రతి 4 మందిలో ఒకరు ఇక్కడే · ఎక్కువ మంది + ఎన్నో తయారీలు = పెద్ద వాటా',
  ['GX-DATA', 'T6', 'GX-PARALLAX'], '')
s('1.7', 'DATA', 'APPROVED POC harvest split (illustrative), then the village: the karanam writing on palm leaves (TE line), a pathshala with only a few boys.',
  'Grain particles; then slow parallax on the village.', 'Piles on "farmer / landlord / state"; village on "Caste" / "కరణం"; pathshala on "schooling" / "చదువు".',
  'ILLUSTRATIVE · SHARES VARIED BY REGION AND RULER', 'ఉదాహరణ మాత్రమే · వాటాలు ప్రాంతాన్ని, పాలకుడిని బట్టి మారేవి', ['GX-PART', 'G03', 'GX-PARALLAX'], '',
  'Caste: no caste markers, uniforms or stereotypes on screen; show the system (who writes, who learns), not people ranked.')
s('1.8', 'CIN', 'Macro: a hand closes on an open cotton boll; cut to the spinning wheel turning in the dark.', 'Macro push.',
  'Boll on "something humbler"; wheel on "this field".', '', '', ['G04', 'T5'], '')

# ================= CH 2
s('2.0', 'TITLE', 'Chapter card.', '', '', 'CHAPTER 2 · THE CLOTH THE WORLD WANTED', 'రెండో అధ్యాయం · ప్రపంచం కోరుకున్న గుడ్డ', ['GX-CARD'], '')
s('2.1', 'CIN', 'Three hand close-ups: spinning, weaving, painting.', 'Quick drifts.', 'One per beat after "follow the hands" / చేతుల.', '', '', ['T5', 'T6', 'G05'], '')
s('2.2', 'CIN', 'The spinner by lamplight; on "many spinners" a small counter of spinner icons fills beside the loom icon.',
  'Parallax push on T5.', 'Icons on "many".', 'MANY SPINNERS → ONE LOOM', 'ఎంతోమంది వడికేవాళ్లు → ఒక్క మగ్గం', ['T5', 'GX-PARALLAX', 'GX-DATA'], 'Crop on the woman and wheel.')
s('2.3', 'CIN', 'The pit loom; a small flow sketch: broker → advance → weaver, broker → sets price.',
  'Parallax dolly (approved).', 'Flow arrows on "advance" and "price"; hold on "bargaining power".',
  'PAID IN ADVANCE · THE BROKER SET THE PRICE', 'ముందే డబ్బు · ధర దళారిదే', ['T6', 'GX-PARALLAX', 'GX-DATA'], '9:16 pans broker → weaver (approved).')
s('2.4', 'CIN', 'Hard cut to the river: madder-red and indigo vats, cloth on poles.', 'Parallax drift along the poles.', 'Cut on "dyer".', '', '', ['G06', 'GX-PARALLAX'], '')
s('2.5', 'EVID', 'Split screen: the same chintz detail, left half desaturated and washed out, right half bright.', 'Wipe left → right.',
  'Wipe on "didn\'t wash out".', 'ILLUSTRATIVE COMPARISON', 'ఉదాహరణ పోలిక', ['PD20', 'GX-DOC'], 'Top / bottom split.')
s('2.6', 'EVID', 'Kalam on cloth; process strip builds step by step: mordant → chay red → indigo → wax resist; museum chintz detail.',
  'Macro on G05, then strip.', 'Each step on its word.', 'MORDANT → RED (CHAY ROOT) → BLUE (INDIGO) → WAX', 'మోర్డెంట్ → ఎరుపు (చాయ్ వేరు) → నీలం (నీలిమందు) → మైనం',
  ['G05', 'PD20', 'GX-DATA'], 'Strip vertical.')
s('2.7', 'MAP', 'TE only: coast map pins Srikalahasti (kalam), Machilipatnam and Pedana (blocks); today\'s artisans.', 'Map push.',
  'Pins on each town name.', '', 'ఈరోజుకీ · శ్రీకాళహస్తి (కలం) · మచిలీపట్నం, పెడన (అచ్చు)', ['M-COAST', 'CC06'], '')
s('2.8', 'EVID', 'Document card: a letter with quill; period engraving of Pondicherry if found.', 'Highlight sweep on "detailed descriptions".',
  'Card on "Coeurdoux".', 'COEURDOUX · LETTERS, 1740s', 'కర్డూ · ఉత్తరాలు, 1740లు', ['GX-DOC'], '')
s('2.9', 'CIN', 'Muslin held to the light.', 'Slow tilt; light flickers through.', 'On "woven air".', '"WOVEN AIR"', '"నేసిన గాలి"', ['G07'], '')
s('2.10', 'EVID', '18th-c. dress in Indian chintz; "BANNED" stamp lands.', 'Push-in.', 'Stamp on "bans".', 'BANNED', 'నిషేధం', ['PD04', 'GX-TEXT'], '')
s('2.11', 'EVID', 'Timeline: our cloth c.1680 → France 1686 → England 1700 (bales stamped RE-EXPORT in a warehouse).', 'Timeline tracks right.',
  'Each date on its word.', 'FRANCE 1686 · ENGLAND 1700 · RE-EXPORT ALLOWED', 'ఫ్రాన్స్ 1686 · ఇంగ్లాండ్ 1700 · మళ్లీ ఎగుమతికి అనుమతి', ['GX-DATA', 'G08'], '')
s('2.12', 'EVID', 'The Act\'s title page; exact dates and exceptions shown here (moved from the cold open).', 'Highlight sweep across the title.',
  'Dates on "Christmas 1722"; exceptions on "few exceptions".', 'ENACTED 1721 · IN FORCE 25 DEC 1722 · EXCEPTIONS: MUSLINS, NECKCLOTHS, FUSTIANS, ALL-BLUE CALICO',
  'చట్టం 1721 · అమలు 25 డిసెంబర్ 1722 · మినహాయింపులు: మస్లిన్, మెడగుడ్డలు, ఫస్టియన్, పూర్తి నీలం calico', ['PD03', 'GX-DOC'], '')
s('2.13', 'EVID', 'Timeline extends to 1774.', '', 'On "1774".', 'IN FORCE UNTIL 1774', '1774 వరకు అమల్లో', ['GX-DATA'], '')
s('2.14', 'EVID', 'Protest print or document card beside the palampore.', 'Slow push.', 'On "wool and silk".', 'PROTECTING WOOL AND SILK', 'ఉన్ని, పట్టు రక్షణ కోసం', ['PD05', 'MET1'], '')
s('2.15', 'MAP', 'EN only: cloth routes to Southeast Asia and West Africa; word cards CALICO ← Calicut, CHINTZ ← chheent.', 'Map pull-out.',
  'Routes on "Southeast Asia", "West Africa"; cards on "calico", "chintz".', 'CALICO ← CALICUT · CHINTZ ← CHHEENT', '', ['M-OCEAN', 'GX-TEXT'], '')
s('2.16', 'CIN', 'Broker stamps the bundle; cut to the sea horizon.', 'Push on the stamp, then wide.', 'Stamp on "finished"; horizon on "port".', '', '', ['T6', 'GX-TEXT', 'T1'], '')

# ================= CH 3
s('3.0', 'TITLE', 'Chapter card.', '', '', 'CHAPTER 3 · GOLCONDA AND MACHILIPATNAM · c.1680', 'మూడో అధ్యాయం · గోల్కొండ, మచిలీపట్నం · సుమారు 1680', ['GX-CARD'], '')
s('3.1', 'CIN', 'Golconda fort at dusk.', 'Slow parallax.', 'Cut to map on "port".', '', '', ['CC01', 'GX-PARALLAX'], '')
s('3.2', 'MAP', 'Coast map: Golconda kingdom fills; road animates to Machilipatnam on the Krishna delta.', 'Map push, then follow the road.',
  'Fill on "Qutb Shahi"; road on "sea gate".', 'QUTB SHAHI GOLCONDA · c.1680', 'కుతుబ్‌షాహీ గోల్కొండ · సుమారు 1680', ['M-COAST'], 'Map tilted to portrait.')
s('3.3', 'CIN', 'Harbour reconstruction; route lines from Persia, Arabia, Burma, SE Asia; Dutch / English flags appear with years; waterfront market.',
  'Parallax over the harbour, then market close.', 'Each region on its word; flags on "Dutch" / "English 1611"; market on "brokers".',
  'DUTCH early 1600s · ENGLISH 1611', 'డచ్ 1600ల మొదట్లో · ఇంగ్లీష్ 1611', ['G09', 'G10', 'M-OCEAN', 'PD06'], '')
s('3.4', 'EVID', 'TE only: Qutb Shahi tombs, Telugu manuscript; name card "మల్కిభరాముడు".', 'Slow pans.', 'Card on the name.', '',
  'ఇబ్రహీం కుతుబ్ షా = మల్కిభరాముడు', ['CC02', 'PD07', 'GX-TEXT'], '')
s('3.5', 'CIN', 'One rough diamond in candlelight.', 'Macro, glint.', 'On "diamonds".', '', '', ['G11'], '')
s('3.6', 'MAP', 'Kollur pin on the Krishna near Pulichintala; world inset: India large, Borneo small, Brazil "1720s".', 'Map push to the pin.',
  'Pin on "Kollur"; inset on "Brazil".', 'KOLLUR MINES · NEAR PULICHINTALA, KRISHNA RIVER', 'కొల్లూరు గనులు · పులిచింతల దగ్గర, కృష్ణా నది', ['M-COAST', 'M-WORLD'], '')
s('3.7', 'CIN', 'The diggings, wide and distant; then Tavernier\'s engraved plate with the blue diamond; chip.', 'Slow parallax; plate push.',
  'Plate on "Tavernier"; chip on "possibly".', 'EXACT MINE UNKNOWN', 'అసలు గని తెలియదు', ['G12', 'PD02', 'GX-PARALLAX'], '',
  'Child labour mentioned: keep figures distant; no close-ups of children.')
s('3.8', 'EVID', 'Koh-i-Noor silhouette graphic with "?".', 'Static.', 'On "debate".', 'MINE OF ORIGIN · DEBATED', 'ఏ గని? · చర్చనీయాంశం', ['GX-TEXT'], '')
s('3.9', 'CIN', 'Split: a diamond in a fist vs a ship\'s hold packed with bales.', 'Split opens.', 'Split on "Cloth filled the ships".', '', '', ['G11', 'G13'], 'Top / bottom split.')
s('3.10', 'MAP', 'TE only: Mughal colour floods Golconda (1687); the harbour fades.', 'Map.', 'On "1687".', '', '1687 · మొఘల్ ఆక్రమణ', ['M-COAST', 'M-DECCAN'], '')
s('3.11', 'CIN', 'Port-gate clerk writes our bale\'s duty; coins split off at each hand.', 'Macro on the ledger.', 'Coin icons on "someone took a share"; hold on "Who?".',
  '', '', ['G14', 'GX-PART'], '')
s('3.12', 'TITLE', 'Subscribe chip over the ledger close-up.', '', 'On "subscribe".', 'SUBSCRIBE', 'SUBSCRIBE', ['GX-TEXT'], '')
s('F2.1', 'DLG', 'Chelli lifts the coin.', 'Push toward the coin.', '', '', '', ['G15'], '')
s('F2.2', 'DLG', 'Coin macro: EN Mughal silver rupee, TE Golconda gold pagoda (hun).', 'Slow rotation.', 'Name on "king\'s name".', 'MUGHAL SILVER RUPEE', 'గోల్కొండ బంగారు వరహా', ['PD18'], 'Coin centred, large.')

# ================= CH 4
s('4.0', 'TITLE', 'Chapter card.', '', '', 'CHAPTER 4 · WHO CONTROLLED THE WEALTH?', 'నాలుగో అధ్యాయం · సంపద ఎవరి చేతిలో?', ['GX-CARD'], '')
s('4.1', 'CIN', 'Still life: the empty bowl beside a bale of bright chintz.', 'Very slow push.', 'Hold on "so poor".', '', '', ['G16'], '')
s('4.2', 'MAP', 'Deccan map animates 1500 → 1690: Vijayanagara, Talikota 1565, Aravidu seats (Penukonda, Chandragiri, Vellore), sultanates, Mughal advance.',
  'Map moves with the story.', 'Each place on its word.', 'TALIKOTA 1565', 'తళ్లికోట 1565', ['M-DECCAN'], '')
s('4.3', 'EVID', 'TE only: Hampi; the verse in Telugu script.', 'Parallax on Hampi.', 'Verse on "దేశ భాషలందు".', '', 'దేశ భాషలందు తెలుగు లెస్స · ఆముక్తమాల్యద', ['CC03', 'GX-TEXT'], '')
s('4.4', 'EVID', 'EN only: Mughal miniature of a land survey.', 'Slow pan.', 'On "Todar Mal".', 'TODAR MAL · LAND SURVEY', '', ['PD08'], '')
s('4.5', 'DATA', 'A coin rolls from a field toward a palace.', 'Track with the coin.', 'On "Follow the money".', 'FOLLOW THE MONEY', 'డబ్బు వెనకే', ['GX-PART'], '')
s('4.6', 'DATA', 'Flow diagram builds step by step: field → collector/zamindar → treasury → army & court; bankers link to all; farman scroll for the foreign merchant. Coins actually flow along the arrows.',
  'Diagram pans as it grows.', 'Each node on its phrase; "a third to a half" bar on "third".', 'OFTEN 1/3 TO 1/2 OF THE CROP · HISTORIANS\' ESTIMATE', 'తరచుగా పంటలో 1/3 నుంచి 1/2 · చరిత్రకారుల అంచనా',
  ['GX-DATA', 'GX-PART', 'G17'], 'Diagram vertical (top → bottom).')
s('4.7', 'CIN', 'TE only: two ministers over revenue books.', 'Parallax.', 'Names card.', '', 'మాదన్న, అక్కన్న · పన్నులు, ఖజానా', ['G18'], '')
s('4.8', 'CIN', 'Surat counting-house; record card "the richest merchant of his time" (Company records).', 'Parallax; card highlight.',
  'Card on "records".', 'VIRJI VORA · SURAT · "THE RICHEST MERCHANT" (COMPANY RECORDS)', 'విర్జీ వోరా · సూరత్', ['G19', 'GX-DOC'], '')
s('4.9', 'CIN', 'Cracked earth; music drops out.', 'Static.', 'Silence after "rains failed".', '', '', ['CC04'], '', 'Famine: restrained.')
s('4.10', 'EVID', 'Empty loom, dust road, Mundy journal page; chip.', 'Slow fades only.', 'Page on "Peter Mundy"; chip on "Estimates".', 'ESTIMATES', 'అంచనాలు',
  ['G20', 'PD09'], '', 'No bodies, no graphic imagery; slow dissolves, no SFX hits.')
s('4.11', 'CIN', 'Our bale hoisted aboard at Machilipatnam.', 'Tilt up with the rope.', 'On "by sea".', '', '', ['G21'], '')

# ================= CH 5
s('5.0', 'TITLE', 'Chapter card.', '', '', 'CHAPTER 5 · EUROPE DIDN\'T DISCOVER INDIA · 1498', 'ఐదో అధ్యాయం · యూరప్ భారత్‌ను కనిపెట్టలేదు · 1498', ['GX-CARD'], '')
s('5.1', 'EVID', 'Cantino planisphere 1502.', 'Slow push to India.', 'On "who showed him the way?".', 'CANTINO PLANISPHERE · 1502', 'కాంటినో ప్రపంచ పటం · 1502', ['PD10'], '')
s('5.2', 'MAP', 'Ship leaves Machilipatnam; the map pulls out to a busy ocean.', 'Ship parallax → map pull-out.', 'Pull-out on "busy".', '', '', ['T1', 'M-OCEAN'], '')
s('5.3', 'MAP', 'Route lines light up port by port; Malacca highlighted.', 'Map tracks the routes.', 'Each people on its word; Malacca on "Malacca".',
  'MALACCA · GUJARATI MERCHANTS', 'మలక్కా · గుజరాతీ వ్యాపారులు', ['M-OCEAN'], '')
s('5.4', 'EVID', 'TE only: Roman coin; pin on the Telugu region.', 'Coin rotates; map pin.', 'On "రోమన్ నాణేలు".', '', 'రోమన్ నాణేలు · తెలుగు నేల', ['PD19', 'M-COAST'], '')
s('5.5', 'MAP', 'Monsoon wind arrows reverse across the ocean; a dhow sail fills.', 'Map; then sail.', 'Arrows reverse on "back the other way".',
  'SW MONSOON · NE MONSOON', 'నైరుతి రుతుపవనాలు · ఈశాన్య రుతుపవనాలు', ['M-OCEAN', 'T1'], '')
s('5.6', 'MAP', 'Route Malindi → Calicut; pilot silhouette with "?".', 'Follow the route.', '"?" on "debate".', 'PILOT\'S IDENTITY · DEBATED', 'ఆ నావికుడు ఎవరు? · చర్చనీయాంశం', ['M-OCEAN', 'GX-TEXT'], '')
s('5.7', 'CIN', 'Calicut shore 1498; the journal page with the line highlighted.', 'Parallax; highlight sweep.', 'Quote card on "Christians… and spices".',
  '"CHRISTIANS AND SPICES" · ROTEIRO, 1498', '"క్రైస్తవుల కోసం, సుగంధ ద్రవ్యాల కోసం" · రోటీరో, 1498', ['G22', 'PD11', 'GX-DOC'], '')
s('5.8', 'CIN', 'Gifts on a mat; courtiers amused.', 'Push.', 'Cut on "laughed".', '', '', ['G23'], '')
s('5.9', 'MAP', 'EN only: Red Sea / Gulf route to Venice dims; Cape route lights.', 'Map.', 'On "middlemen".', '', '', ['M-OCEAN'], '')
s('5.10', 'EVID', 'Graphic transition: cannon icon → bowing figure icon.', '', 'On "cannons" / "politely".', '', '', ['GX-TEXT'], '')

# ================= CH 6
s('6.0', 'TITLE', 'Chapter card.', '', '', 'CHAPTER 6 · THE COMPANY THAT CAME TO TRADE · 1600 → 1757', 'ఆరో అధ్యాయం · వ్యాపారం కోసం వచ్చిన కంపెనీ · 1600 → 1757', ['GX-CARD'], '')
s('6.1', 'EVID', 'Company coat of arms.', 'Slow push.', 'On "giving orders".', '', '', ['PD12'], '')
s('6.2', 'CIN', 'London merchants and the charter; Dutch VOC year chip.', 'Parallax.', 'Chip on "1600" and "two years later".', '31 DEC 1600 · VOC 1602', '31 డిసెంబర్ 1600 · డచ్ కంపెనీ 1602', ['G24'], '')
s('6.3', 'MAP', 'Surat on the Company map; Jahangir court painting; Swally 1612 marker; 1613 deal chip.', 'Map ↔ painting.', 'Each date on its word.',
  '1608 · 1612 SWALLY · 1613', '1608 · 1612 స్వాలీ · 1613', ['M-COMPANY', 'PD13'], '')
s('6.4', 'EVID', 'Stamps land one after another on a ledger.', '', 'Stamps on the beats.', '', '', ['GX-DOC'], '')
s('6.5', 'MAP', 'Machilipatnam 1611 → Madras 1639; Fort St George print.', 'Map.', 'Pins on dates.', 'MACHILIPATNAM 1611 · MADRAS 1639', 'మచిలీపట్నం 1611 · మద్రాసు 1639', ['M-COMPANY', 'PD14'], '')
s('6.6', 'CIN', 'Silver chests unloaded at the dock.', 'Parallax.', 'On "silver".', 'PAID MOSTLY IN SILVER', 'ఎక్కువగా వెండితో', ['G25'], '')
s('6.7', 'CIN', 'London warehouse sale; East India House print.', 'Push.', 'Chip on "London".', 'OUR CLOTH · LONDON · c.1680', 'మన గుడ్డ · లండన్ · సుమారు 1680', ['G26', 'PD15'], '')
s('6.8', 'EVID', 'Year chip spins c.1680 → 1717.', '', '', '', '', ['GX-TEXT'], '')
s('6.8b', 'MAP', 'Anglo-Mughal war 1686–90 on the map; Mughal victory; Calcutta 1690 pin. No fine amount on screen.', 'Map.', 'On "lost"; pin on "Calcutta".',
  'ANGLO-MUGHAL WAR 1686–90 · MUGHAL VICTORY', 'ఆంగ్లో-మొఘల్ యుద్ధం 1686–90 · మొఘలుల విజయం', ['M-COMPANY'], '')
s('6.9', 'EVID', 'Farman scroll; dastak pass card; boats slip past a toll post.', 'Doc highlight; then parallax.', 'On "3,000 rupees"; boats on "misused".',
  '1717 FARMAN · ₹3,000 A YEAR · DUTY-FREE IN BENGAL', '1717 ఫర్మానా · ఏటా ₹3,000 · బెంగాల్‌లో సుంకం లేదు', ['G17', 'G27', 'GX-DOC'], '')
s('6.10', 'CIN', 'Sepoy drill; map: rival claimants (Arcot, Hyderabad) with French / English flags.', 'Parallax → map.', 'Map on "rival claimants".', '', '', ['G28', 'M-COMPANY'], '')
s('6.11', 'MAP', 'TE only: coastal Andhra turns French blue (1753).', 'Map.', 'On "1753".', '', '1753 · ఉత్తర సర్కారులు ఫ్రెంచ్ చేతికి', ['M-COMPANY'], '')
s('6.12', 'EVID', 'A merchant\'s hand lifts a chess king.', 'Macro.', 'On "choosing rulers".', '', '', ['GX-PART'], '')
s('6.13', 'MAP', 'Calcutta 1750s print; 1756 marker; ships sail north from Madras.', 'Print → map.', 'Marker on "1756"; ships on "army".', '1756', '1756', ['PD16', 'M-COMPANY'], '')

# ================= ENDING
s('7.1', 'CIN', 'Callback: our cloth in lamplight → mist over the mango grove.', 'Slow dissolve.', 'Grove on "Plassey".', '', '', ['T7', 'G29'], '')
s('7.2', 'CIN', 'Plassey lines in heavy air; numbers chip.', 'Very slow parallax.', 'Chip on the numbers.', '23 JUNE 1757 · ~3,000 vs ~50,000', '23 జూన్ 1757 · ~3,000 vs ~50,000', ['G30', 'GX-PARALLAX'], '',
  'Battle: no gore, no fake heroics; label DRAMATIZED.')
s('7.3', 'CIN', 'One flank stands still; the throne cushion.', 'Push.', 'On "never fought".', '', '', ['G30', 'GX-TEXT'], '')
s('7.4', 'MAP', 'TE only: zoom to Machilipatnam, 1759; smoke puff.', 'Map.', 'On "1759".', '', '1759 · మచిలీపట్నం', ['M-COMPANY'], '')
s('7.5', 'MAP', 'Bengal changes colour; Buxar 1764 marker; the diwani painting (1765).', 'Map → painting.', 'Each year on its word.',
  'BUXAR 1764 · DIWANI 1765', 'బక్సర్ 1764 · దివానీ 1765', ['M-COMPANY', 'PD17'], '')
s('7.6', 'DLG', 'Anna and Chelli with the coin and cloth; silver → taxes inset.', 'Approved crops (Anna speaks).', 'Inset on "taxes".', '', '', ['T7'], '')
s('7.7', 'DLG', 'Chelli looks up.', 'Push to Chelli.', '', '', '', ['T7'], '')
s('7.8', 'DLG', 'Anna answers.', 'Push to Anna.', '', '', '', ['T7'], '')
s('7.9', 'TITLE', 'The lid closes (approved); Season 2 card on the impact.', 'Slow push.', 'Card on the boom.',
  'THE GOLDEN SPARROW · SEASON 2 · HOW A COMPANY BECAME AN EMPIRE', 'బంగారు పిచ్చుక · సీజన్ 2 · ఒక కంపెనీ సామ్రాజ్యం ఎలా అయింది', ['T8', 'GX-CARD'], '')
