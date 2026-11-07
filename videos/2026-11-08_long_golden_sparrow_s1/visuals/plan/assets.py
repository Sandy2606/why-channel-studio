# Asset register for THE GOLDEN SPARROW S1.
# kind: EXIST (have it) | GEN (new illustration, generated free by Sandeep in ChatGPT from the prompt pack) |
#       PD (public-domain / open-access archive, download + log URL) | CC (Creative Commons photo, attribution in credits) |
#       BUILD (made in-house in the motion-graphics pipeline, no outside rights)
A = {}
def a(id, kind, desc, source, status, ref=False):
    A[id] = dict(id=id, kind=kind, desc=desc, source=source, status=status, ref=ref)

# ---- existing (approved test batch + museum image)
a('T1', 'EXIST', 'Indian Ocean trading ship under sail, monsoon sea, c.1680', 'ChatGPT (own generation)', 'have it')
a('T2', 'EXIST', 'Company mainsail backlit at dusk, striped Company ensign', 'ChatGPT (own generation)', 'have it')
a('T3', 'EXIST', 'Anna and Chelli open Ammamma\'s trunk (afternoon)', 'ChatGPT (own generation)', 'have it')
a('T4', 'EXIST', 'Close-up: Anna traces the kalamkari border, Chelli amazed', 'ChatGPT (own generation)', 'have it')
a('T5', 'EXIST', 'Spinner at the charkha by oil lamp, child asleep', 'ChatGPT (own generation)', 'have it')
a('T6', 'EXIST', 'Pit-loom weaver paid by a broker (true pit loom)', 'ChatGPT (own generation)', 'have it')
a('T7', 'EXIST', 'Evening: Anna holds the coin, Chelli the cloth', 'ChatGPT (own generation)', 'have it')
a('T8', 'EXIST', 'Night: the children\'s hands close the trunk lid', 'ChatGPT (own generation)', 'have it')
a('MET1', 'PD', 'Palampore, Coromandel Coast, 18th c. (Met 1982.66)', 'The Met Open Access', '✅ downloaded, public domain')
a('CHAR', 'EXIST', 'Character + prop reference sheet v1', 'ElevenLabs (paid, done)', 'have it')

# ---- new illustrations to generate (free, ChatGPT, prompt pack v2). ref=True: attach the character sheet
G = [
 ('G01', 'Cotton field at dawn, black-soil Deccan, mist, no people (wide)', False),
 ('G02', 'Family picking cotton at dawn c.1680: father, mother, grandmother, an ox at the field edge', False),
 ('G03', 'Village accountant (karanam) writing on palm leaves under a tree; a small pathshala with only a few boys in the background', False),
 ('G04', 'Macro: a farmer\'s hand closing around an open cotton boll, dew, first light', False),
 ('G05', 'Kalamkari artist\'s hand drawing with a bamboo kalam on cotton, mordant pot, half-finished floral design', False),
 ('G06', 'Dyers at a riverbank: vats of madder red and indigo, long cloths drying on poles', False),
 ('G07', 'Bengal muslin held up to sunlight, so fine the light passes through (weaver\'s hands only)', False),
 ('G08', 'London customs warehouse c.1700: bales of Indian calico stamped for re-export, clerk with ledger', False),
 ('G09', 'Machilipatnam harbour c.1680, wide: ocean ships at anchor, small boats ferrying bales, warehouses, palm-lined shore', False),
 ('G10', 'Market at the Machilipatnam waterfront: brokers, interpreters and foreign buyers (Persian, Dutch, English) inspecting cloth', False),
 ('G11', 'Macro: one rough uncut diamond on a dark cloth in candlelight', False),
 ('G12', 'Kollur diamond diggings on the Krishna, early 1600s, wide and distant: pits, many workers, river beyond (no close-ups of children)', False),
 ('G13', 'Ship\'s hold packed with cloth bales, lantern light', False),
 ('G14', 'Port-gate clerk writing duties in a ledger, our stamped bale beside him (macro on hands + ledger)', False),
 ('G15', 'Chelli lifts the old coin from the trunk, Anna leans in (same room as T3, late afternoon)', True),
 ('G16', 'A weaver\'s empty brass bowl beside a finished bale of bright chintz (still life, restrained)', False),
 ('G17', 'A Mughal farman scroll with seal on a low desk (reconstruction, no readable text)', False),
 ('G18', 'Two Golconda ministers in a revenue office over account books (backs/three-quarter, no portrait claim)', False),
 ('G19', 'Surat counting-house c.1620s: a merchant-banker\'s office, coins weighed, ledgers, river ships beyond', False),
 ('G20', 'An empty pit loom in a dark hut, dust in a shaft of light (restrained, no people)', False),
 ('G21', 'Our bale hoisted aboard a ship at Machilipatnam by rope and pulley', False),
 ('G22', 'Calicut shore, May 1498: Portuguese ships offshore, a small boat landing, local traders watching', False),
 ('G23', 'Da Gama\'s gifts laid on a mat (hats, coral, sugar, honey) before amused courtiers of the Zamorin\'s court', False),
 ('G24', 'London 1600: merchants in a panelled hall around a sealed charter document', False),
 ('G25', 'Company silver: chests of silver coins and bars unloaded at an Indian dock', False),
 ('G26', 'London warehouse sale c.1680: a bale cut open, buyers, an auctioneer\'s candle', False),
 ('G27', 'Company boats slipping past a riverside toll post in Bengal with passes in hand', False),
 ('G28', 'Sepoys drilling in European formation, 1750s, red coats, South Indian landscape', False),
 ('G29', 'Mango grove at Plassey before dawn, mist, distant camp fires (no fighting)', False),
 ('G30', 'Plassey 23 June 1757: armies facing each other in rain-heavy air, much of one flank standing still (wide, no gore)', False),
]
for gid, d, ref in G: a(gid, 'GEN', d, 'ChatGPT (free, Sandeep) · prompt pack v2', 'to generate', ref)

# ---- public domain / open access (download, log URL in credits)
P = [
 ('PD01', 'Indus carnelian beads (Met Open Access, to select)', 'The Met OA', 'to select'),
 ('PD02', 'Tavernier\'s diamond plate, Les Six Voyages (1676)', 'Wikimedia Commons (PD)', 'to download'),
 ('PD03', 'Act 7 Geo. I c.7 (1721) title page', 'Wellcome Collection / Google Books scan (PD)', 'to locate'),
 ('PD04', '18th-c. dress or fashion plate in Indian chintz', 'The Met / Rijksmuseum OA', 'to select'),
 ('PD05', 'Period print on the calico controversy / weavers\' protest (1719–21)', 'British Museum? (check licence) / Wikimedia', 'to locate; fallback: BUILD a document card'),
 ('PD06', 'Rijksmuseum CC0 view of Masulipatnam (17th c.)', 'Rijksmuseum (CC0)', 'to locate; fallback: G09'),
 ('PD07', 'Telugu palm-leaf or paper manuscript (TE 3.4)', 'Wikimedia Commons (PD)', 'to locate'),
 ('PD08', 'Mughal miniature: land measurement / revenue survey (EN 4.4)', 'The Met / Wikimedia (PD)', 'to select'),
 ('PD09', 'Peter Mundy\'s Travels page (Hakluyt edition, PD)', 'Internet Archive / Wikimedia', 'to locate'),
 ('PD10', 'Cantino planisphere, 1502', 'Wikimedia Commons (PD)', 'to download'),
 ('PD11', 'Roteiro of da Gama\'s first voyage, page facsimile', 'Wikimedia / BNP (PD)', 'to locate; fallback: BUILD a quote card'),
 ('PD12', 'East India Company coat of arms', 'Wikimedia Commons (PD)', 'to download'),
 ('PD13', 'Jahangir court painting (Met Open Access; NOT the Freer Bichitr)', 'The Met OA', 'to select'),
 ('PD14', 'Fort St George, Madras, early print (date to confirm)', 'Wikimedia / BL (PD)', 'to locate'),
 ('PD15', 'East India House, London, print', 'Wikimedia (PD)', 'to download'),
 ('PD16', 'Calcutta / Fort William 1750s print', 'Wikimedia (PD)', 'to locate'),
 ('PD17', 'Benjamin West, Shah Alam conveying the grant of the Diwani (1818)', 'British Library via Wikimedia (PD)', 'to download'),
 ('PD18', 'Coins: Mughal silver rupee (EN F2.1) and Golconda gold pagoda (TE F2.1)', 'Wikimedia (CNG photos, CC BY-SA)', 'to download, credit CNG'),
 ('PD19', 'Roman gold coin (aureus) for TE 5.4', 'Wikimedia (CC BY-SA / PD)', 'to download'),
 ('PD20', 'Met chintz details for the dye-process diagram (2.6) and the faded/bright split (2.5)', 'The Met OA', 'to select'),
]
for pid, d, s, st in P: a(pid, 'PD', d, s, st)
C = [
 ('CC01', 'Golconda fort at dusk', 'Wikimedia Commons (CC BY-SA, attribution)'),
 ('CC02', 'Qutb Shahi tombs, Hyderabad', 'Wikimedia Commons (CC BY-SA)'),
 ('CC03', 'Hampi ruins (Vittala temple / Virupaksha)', 'Wikimedia Commons (CC BY-SA)'),
 ('CC04', 'Cracked dry earth (drought)', 'Pexels (free licence)'),
 ('CC05', 'Monsoon sea / rain over ocean (b-roll)', 'Pexels (free licence)'),
 ('CC06', 'Kalamkari artisans at work today, Srikalahasti / Pedana (TE 2.7)', 'Wikimedia (CC BY-SA) or Pexels', ),
]
for c in C: a(c[0], 'CC', c[1], c[2], 'to select and check licence')

# ---- in-house builds (motion-graphics system approved in the POC)
B = [
 ('M-WORLD', 'Equal Earth world map, official India outline, layer masks (built)'),
 ('M-SA', 'South Asia map: subcontinent / Republic of India / Pakistan + Bangladesh layers (built)'),
 ('M-COAST', 'Coromandel coast map: Machilipatnam, Golconda, Kollur (Pulichintala), Srikalahasti, Pedana, Palakollu, Madras; Telugu labels for TE'),
 ('M-OCEAN', 'Indian Ocean map: ports (Aden, Hormuz, Malindi, Calicut, Malacca, Aceh, Arakan), animated route lines, monsoon wind arrows'),
 ('M-DECCAN', 'Deccan politics 1500→1690: Vijayanagara/Aravidu seats, sultanates, Mughal advance (animated colour fields)'),
 ('M-COMPANY', 'Company map: Surat, Swally, Machilipatnam, Madras, Bombay, Calcutta pins; 1686–90 war; Northern Circars 1753; Bengal 1757–65'),
 ('GX-CARD', 'Chapter card template (number, title, progress 1/6…6/6, year chip)'),
 ('GX-TEXT', 'Typography kit: headline + gold rule, year roll, lower third (source), evidence highlight, DRAMATIZED tag'),
 ('GX-DATA', 'Data kit: 100-square grid, counters, bars with reference line, people grid, flow diagram, timeline'),
 ('GX-DOC', 'Document card: paper texture, highlight sweep on one phrase, citation chip'),
 ('GX-PARALLAX', '2.5D depth parallax from depth maps (Depth Anything V2, local) for any still'),
 ('GX-PART', 'Particle kit: grain, coins, dust motes, mist, rain, smoke (restrained)'),
]
for b_ in B: a(b_[0], 'BUILD', b_[1], 'in-house pipeline', 'built' if b_[0] in ('M-WORLD', 'M-SA', 'GX-DATA', 'GX-TEXT', 'GX-PARALLAX', 'GX-PART') else 'to build')
