# Prompt pack v2: G01-G30 + R1 (master cloth reference). One complete, self-contained prompt per image.
STYLE = ("STYLE (same as the approved T1-T8 images): never add Anna, Chelli or Ammamma's trunk unless the prompt asks for them; painterly documentary realism, like a museum-quality oil painting with soft visible brushwork; "
         "warm natural light and deep soft shadows; colour accents of madder red, indigo and turmeric over earthy black-soil tones; historically accurate clothing, tools and architecture; "
         "no text, letters, captions, logos or watermarks; no modern objects.")
LAYERS = ("COMPOSITION FOR ANIMATION: landscape 16:9 at the highest resolution. Build the picture in three clear depth layers (a distinct foreground element, the subject in the middle ground, "
          "a separate background) so it can be animated with parallax. Keep the main subject inside the central third, so a vertical 9:16 crop from the centre still contains it. "
          "Leave about 10% breathing room on every side for camera movement, and avoid important details touching the frame edges.")
CLOTH = ("OUR CLOTH (keep exactly as in the attached cloth reference): a cream cotton chintz with a flowering-tree pattern - large madder-red blossoms, indigo-blue leaves, small turmeric-yellow buds, fine brown-black outlines - "
         "and a border of a running red-and-indigo vine on a narrow indigo band. When baled: folded cloth wrapped in coarse off-white sacking, tied with brown rope in a cross, "
         "stamped in black with a circle containing a small fish above three wavy lines and the numeral 7 below.")
CHARS = ("Use the attached character sheet and the attached T3 image: keep Anna's and Chelli's faces, hair, clothes and proportions, Ammamma's room (tiled roof, barred wooden window, red-oxide floor) and the trunk with brass corners exactly as they are. Do not redesign them.")

P = []
def p(id, title, scene, purpose, prompt, refs, history, art, comp, batch=2):
    P.append(dict(id=id, title=title, scene=scene, purpose=purpose, prompt=prompt, refs=refs, history=history, art=art, comp=comp, batch=batch))

p('R1', 'Master cloth reference ("our cloth")', 'reference only', 'Fixes the look of the fictional 1680 chintz and its bale so every scene shows the same cloth.',
  'Reference sheet on a plain warm-grey background, same painterly style as the character sheet. Show four views of ONE fictional 1680 Coromandel chintz: '
  '(1) the whole cloth laid flat - cream cotton ground, a central flowering-tree pattern with large madder-red blossoms, indigo-blue leaves and small turmeric-yellow buds, fine brown-black outlines; '
  '(2) a close-up of its border: a running red-and-indigo vine on a narrow indigo band; (3) the cloth folded into a neat stack with the border showing along one edge; '
  '(4) a merchant\'s bale: folded cloths wrapped in coarse off-white sacking, tied with brown rope in a cross, stamped in black with a circle containing a small fish above three wavy lines and the numeral 7 below. '
  'Evenly lit, no other text or labels, 16:9.',
  [], 'Pattern follows surviving 17th-18th c. Coromandel chintz (tree-of-life style, madder red + indigo, mordant-painted). The bale mark is fictional: brokers and companies did mark bales, but we invent ours rather than copy a real company mark.',
  'Flat, evenly lit reference; the same palette as the film.', 'Reference only; not used on screen.', batch=1)

p('G01', 'Cotton field at dawn', '1.0, 1.1, F1.3 match cut', 'Opens Chapter 1; the place where our cloth begins.',
  'A cotton field on black Deccan soil at first light, c.1680, no people. Rows of cotton plants with open white bolls in the foreground (close to camera, some slightly out of focus), '
  'the field stretching to a line of neem and palmyra trees in the middle distance, low mist, a soft orange sun just above the horizon, a simple thatched field hut far away. ',
  [], 'Deccan black cotton soil (regur); hand-cultivated plots; neem and palmyra are native to the region.', 'Calm, golden, quiet; the "establishing shot" of the season.',
  'Foreground bolls / mid field / background trees and sun give clean parallax; horizon in the upper third; the hut near centre for the 9:16 crop.', batch=1)
p('G02', 'Family picking cotton', '1.2', '"Around 1680, somewhere in the Deccan, a family is picking cotton at dawn."',
  'Same field and dawn light as G01. A farming family picks cotton: the mother and grandmother in plain, faded unbleached-cotton saris worn without stitched blouses or festive borders (simple everyday 17th-century village dress, not a langa-voni or half-saree, and NOT the colours of Chelli\'s outfit), the father in a dhoti and head cloth, '
  'cloth bags slung at the hip filling with cotton; a white ox stands at the field edge. Bare feet, simple brass bangles, no shoes. ',
  [], 'Late-17th c. rural Deccan dress: unstitched cotton (sari, dhoti), head cloths; hand picking into slung bags.', 'Dignified, unhurried work; faces lit by the low sun.',
  'Foreground cotton plants, family in the middle ground, ox and trees behind; mother and grandmother close to the centre for the 9:16 crop.', batch=1)
p('G03', 'Karanam and the pathshala', '1.7', 'The village system: who writes the records, who gets schooling.',
  'A village under a large banyan tree, c.1680. In the middle ground, the village accountant (karanam) sits cross-legged writing with a stylus on palm-leaf strips, a bundle of palm-leaf records beside him; '
  'behind him, a small open-air pathshala where a teacher sits with only four boys writing on sand; the rest of the village goes about its work further back. ',
  [], 'Telugu villages kept land records with the karanam on palm leaf; schooling was limited to a few. Show no caste markers or ranking of people.',
  'Neutral, observational; nobody is shamed or ranked.', 'Banyan roots in the foreground, karanam middle, pathshala behind; karanam in the centre third.')
p('G04', 'Hand on a cotton boll (macro)', '1.8', '"It came for something humbler… and it\'s right here, in this field."',
  'Extreme close-up at dawn: a farmer\'s weathered hand gently closing around one open cotton boll on the plant, dew drops, soft rim light; field softly blurred behind. ',
  [], 'Desi (Gossypium arboreum) cotton bolls, smaller than modern varieties.', 'Intimate, tactile.', 'Hand and boll centred; shallow depth (foreground leaf, hand, blurred field).')
p('G05', 'The kalam on cloth', '2.1, 2.6', 'The painter draws the design in mordant with a bamboo kalam.',
  'Close-up: an artisan\'s hand holds a bamboo kalam (pen) wrapped with a small wool pad, drawing fine black outlines of OUR CLOTH\'s flowering-tree design on cream cotton stretched on a low board; '
  'a small clay pot of mordant beside it; part of the design already painted in madder red. Soft daylight from the left. ' + CLOTH + ' ',
  ['R1'], 'Kalamkari of the Coromandel coast: kalam drawing, mordants (alum/iron), chay-root red, indigo, wax resist.', 'Craft, concentration, beauty.',
  'Pot in the foreground, hand and cloth mid, workshop wall behind; the pen tip near the centre.', batch=1)
p('G06', 'Dyers at the river', '2.4', '"Then came the real secret: the dyer."',
  'A riverbank dye works, c.1680: large clay vats of madder red and deep indigo, dyers with dyed forearms lifting a long cloth from a vat, rows of cloths drying on bamboo poles in the sun, '
  'some of them OUR CLOTH in progress. River and palms behind. ' + CLOTH + ' ',
  ['R1'], 'Washing and dyeing near running water was typical of Coromandel dye centres.', 'Colour and energy, still documentary.',
  'Vats foreground, dyers and poles middle, river behind; one dyer near the centre.')
p('G07', 'Muslin held to the light', '2.9', '"…so fine, people called it woven air."',
  'A Bengal weaver\'s hands hold up a length of very fine white muslin against the morning sun in a doorway; the light passes through the cloth, showing the faint grid of the weave. Interior dark, doorway bright. ',
  [], 'Dhaka muslin, early 18th c.; plain, translucent.', 'Luminous, delicate.', 'Hands lower foreground, cloth in the centre, doorway light behind.')
p('G08', 'London customs warehouse', '2.11', 'England 1700: Asian calicoes stopped for home use, re-export allowed.',
  'Interior of a London customs warehouse, c.1700: timber beams, high windows, bales of Indian calico stacked high, a customs clerk in a long coat and wig writing in a ledger, '
  'a porter chalking a mark on a bale for re-export. Cool grey daylight. ',
  [], 'Late-Stuart London: coats, cravats, periwigs; customs officers recorded goods for re-export under the 1700 Act.', 'Bureaucratic, cooler palette than India scenes.',
  'Bales foreground, clerk middle, windows behind; clerk centred.')
p('G09', 'Machilipatnam harbour, c.1680', '3.3, 4.11 (alt)', 'The Golconda port where the world came to buy cloth.',
  'Wide view of Machilipatnam harbour at the Krishna delta, c.1680: large ocean-going ships (Dutch and English East Indiamen and Persian/Arab vessels) at anchor offshore, small masula surf boats ferrying bales (wrapped in sacking, rope tied in a cross, stamped with the fish-and-7 mark) to the shore, '
  'warehouses with tiled roofs and a wooden jetty, palm-lined beach, morning haze. Only 17th-century people: do NOT include Anna, Chelli, any present-day children or Ammamma\'s trunk. ',
  [], 'Masulipatnam: Golconda\'s main port; Dutch (from 1605/06) and English (1611) factories; masula boats carried cargo through the surf.',
  'Grand, busy, international.', 'Jetty and boats foreground, beach and warehouses middle, ships at anchor behind; a central ship for the 9:16 crop.', batch=1)
p('G10', 'Waterfront cloth market', '3.3', 'Brokers and interpreters connect foreign buyers with weaving villages.',
  'A busy waterfront market at Machilipatnam, c.1680: a Telugu broker unfolds OUR CLOTH for inspection; a Persian merchant in a turban and robe, a Dutch merchant in a dark coat and broad hat, and an interpreter between them; '
  'bales with our mark stacked nearby, shade awnings, ships\' masts beyond. ' + CLOTH + ' ',
  ['R1'], 'Coromandel ports relied on local brokers and dubashes (interpreters); Persian, Dutch and English buyers traded side by side.', 'Lively but readable; the cloth is the hero.',
  'Bales foreground, the unfolded cloth and three merchants middle, masts behind; the cloth in the centre.', batch=1)
p('G11', 'Rough diamond in candlelight', '3.5, 3.9', '"And yes… the diamonds."',
  'Macro: a single rough, uncut octahedral diamond on dark indigo cloth, lit by one candle, a soft sparkle; deep black background. ',
  [], 'Golconda diamonds were traded rough or simply cut.', 'Jewel-like, minimal.', 'Diamond centred; candle glow at one side, out of focus.')
p('G12', 'Kollur diggings (wide)', '3.7', 'Visitors in the 1620s counted tens of thousands of workers.',
  'A very wide, distant view of the Kollur diamond diggings on the Krishna river, early 1600s: a landscape of shallow pits and earth heaps, many small workers carrying baskets, a supervisor\'s shade tent, the river beyond. '
  'Everyone is small in the frame; no close-ups. ',
  [], 'Methwold described tens of thousands of workers (men, women, children). Keep children distant and unidentifiable.', 'Scale and toil, restrained.',
  'Pit rims foreground, workers middle, river and hills behind.')
p('G13', 'Ship\'s hold full of bales', '3.9', '"Cloth filled the ships."',
  'Inside a wooden ship\'s hold, lantern light: bales of cloth stacked to the beams, each wrapped and marked like OUR CLOTH\'s bale, a narrow walkway between them, a sailor\'s silhouette at the hatch above. ' + CLOTH + ' ',
  ['R1'], 'East Indiamen and Asian ships carried mostly textiles from Coromandel.', 'Warm, enclosed, abundant.', 'Bales on both sides, walkway leading to the centre.')
p('G14', 'Port-gate clerk and our bale', '3.11, S3 tease', '"A clerk writes down our cloth and the duty it owes."',
  'Close shot at the Machilipatnam port gate: a clerk\'s hand writes with a reed pen in a cloth-bound ledger; OUR CLOTH\'s bale with its mark sits beside him; a few coins on a small tray. ' + CLOTH + ' ',
  ['R1'], 'Customs duties were levied at port; records kept in ledgers.', 'Precise, quietly tense ("who took a share?").', 'Ledger and hand centre, bale side, gate behind.')
p('G15', 'Chelli lifts the coin', 'F2.1', 'Frame story: "Anna, whose face is on this coin?"',
  CHARS + ' Late afternoon in Ammamma\'s room, the trunk open. Chelli kneels and lifts a small old coin up to the window light, curious; Anna leans in beside her. The kalamkari cloth lies folded in the trunk. ',
  ['CHAR', 'T3'], '', 'Warm, curious; consistent with T3/T4.', 'Trunk foreground, children middle, window behind; Chelli and the coin near the centre.')
p('G16', 'Empty bowl beside the chintz', '4.1, S4 hook', '"Why were the people who made it often so poor?"',
  'Still life on an earthen floor: a weaver\'s empty, dented brass bowl beside a finished, folded bale of OUR CLOTH, bright and beautiful; a shaft of light falls on the cloth, the bowl in shadow. ' + CLOTH + ' ',
  ['R1'], '', 'Quiet contrast, no people.', 'Bowl foreground, cloth middle, dim wall behind; both objects within the centre third.')
p('G17', 'Farman scroll', '4.6, 6.9', 'Royal permission to trade.',
  'A Mughal farman scroll partly unrolled on a low wooden desk, red-brown paper with gold-flecked margins, a large round seal impression at the top, lines of Persian calligraphy rendered as illegible decorative strokes, an inkpot and reed pen. ',
  [], 'Farmans carried the imperial seal (tughra) and were written in Persian. Do not render readable text.', 'Formal, archival.', 'Scroll diagonal through the centre; desk edge foreground.')
p('G18', 'Golconda revenue office', '4.7 (TE)', 'Madanna and Akkanna oversaw revenue and the treasury.',
  'Interior of a Golconda revenue office, c.1680: two ministers in white jamas and turbans seen from behind and three-quarter, studying account books with a scribe; arched niche windows, stacked ledgers. No portrait likeness. ',
  [], 'Qutb Shahi court dress; no authentic portraits of the brothers exist, so faces stay turned away.', 'Authority, paperwork.', 'Ledgers foreground, ministers middle, arches behind.')
p('G19', 'Surat counting-house', '4.8', 'Virji Vora, the merchant-banker the English borrowed from.',
  'A Surat merchant-banker\'s counting-house, c.1620s: a wealthy Gujarati merchant in a white angarkha seated on a cushion, scales weighing silver coins, ledgers, clerks; through the window, river ships on the Tapti. ',
  [], 'Surat was the Mughal empire\'s chief port; Virji Vora lent to the English Company. No portrait of him survives, so make him generic.', 'Wealth, calm power.', 'Scales foreground, merchant middle, window behind.')
p('G20', 'Empty pit loom', '4.10', 'Famine: many weavers died or fled. Restrained.',
  'An empty pit loom in a dark mud hut, no people; the loom frame and an unfinished white cloth, a broken thread hanging; dust in a single shaft of light from the doorway. ',
  [], '1630-32 Deccan famine. No bodies, no suffering imagery.', 'Silent, mournful, very restrained.', 'Loom centre, doorway light behind.')
p('G21', 'Our bale goes aboard', '4.11', '"And the richest trade… came by sea."',
  'At Machilipatnam, a bale of OUR CLOTH is hoisted by rope and wooden pulley from a masula boat up the side of a large ship; sailors hauling, the sea glittering. ' + CLOTH + ' ',
  ['R1'], 'Masula boats ferried cargo through the surf to ships at anchor.', 'Movement upward, hopeful.', 'Bale in the upper centre, boat foreground, ship side behind.')
p('G22', 'Calicut shore, May 1498', '5.7', 'Da Gama\'s crew records a strange welcome.',
  'The beach at Calicut, May 1498: three Portuguese ships offshore, a small rowing boat landing, a few local traders and onlookers on the shore in white mundus, palm trees, monsoon clouds building. ',
  [], 'Late-15th c. Malabar dress; Portuguese carracks/naus.', 'Arrival, curiosity, scale of the existing trade world.', 'Boat foreground, traders middle, ships behind.')
p('G23', 'Da Gama\'s gifts', '5.8', 'The king\'s officials laughed at the gifts.',
  'Inside a hall of the Zamorin\'s palace, 1498: on a mat lie da Gama\'s gifts - striped cloth, a few hats, strings of coral, basins of sugar, jars of honey; courtiers in white with gold ornaments look on, amused. ',
  [], 'The Roteiro lists hats, coral, sugar, honey, wash basins and cloth; officials (not the Zamorin) laughed.', 'Gentle irony.', 'Gifts foreground, courtiers middle, carved pillars behind.')
p('G24', 'London charter, 1600', '6.2', 'A group of London merchants receives a royal charter.',
  'A panelled London hall, 31 December 1600: merchants in Elizabethan ruffs and doublets gather round a table where a large parchment charter with a hanging wax seal is unrolled; candlelight. ',
  [], 'Elizabethan dress; royal charter with Great Seal.', 'Ambition, a "business" beginning.', 'Charter centre, merchants around, panelling behind.')
p('G25', 'Silver at the dock', '6.6, S6 B6', 'Europe paid mostly in silver.',
  'At an Indian dock, c.1680: wooden chests of silver coins and bars being unloaded from a boat, one chest open and gleaming, an English factor checking a list, Indian porters carrying. ',
  [], 'Bullion (much of it Spanish-American silver) was the main Company export to India.', 'Glint of silver against warm dock.', 'Open chest foreground centre, porters middle, boats behind.')
p('G26', 'London sale, c.1680', '6.7', 'In a warehouse by the Thames, our cloth is sold.',
  'A Company warehouse sale by the Thames, c.1680: OUR CLOTH\'s bale cut open on a table, the chintz spread out, London buyers in periwigs examining it, an auctioneer with a burning candle (sale "by the candle"). ' + CLOTH + ' ',
  ['R1'], 'Company sales in London were held "by the candle"; late-Stuart dress.', 'Our cloth\'s journey ends in admiration.', 'Spread cloth foreground centre, buyers middle, windows on the river behind.')
p('G27', 'Boats past the toll post', '6.9', 'Company men misused their passes for private trade.',
  'A riverside toll post in Bengal, 1720s-50s: a Company budgerow boat glides past, its men holding up a pass, while the Nawab\'s toll officer looks on, frustrated; other boats wait to pay. ',
  [], 'Dastaks exempted Company goods from duties; private abuse angered Bengal\'s rulers.', 'Quiet tension.', 'Toll officer foreground, boats middle, river bank behind.')
p('G28', 'Sepoys drilling', '6.10', 'The companies trained Indian soldiers in European drill.',
  'South India, 1750s: a line of Indian sepoys drilling with muskets in European formation under a European officer (any flag: the striped Company ensign or the French white flag, never the modern Union Jack); red coats over Indian dress, turbans, dust; a fort wall behind. ',
  [], 'Early sepoy units (French and English) wore European-style coats with Indian turbans and dress.', 'Disciplined, ominous.', 'Officer foreground, line middle, fort behind.')
p('G29', 'Mango grove at Plassey', '7.1', 'The calm before Plassey.',
  'A mango grove near Plassey before dawn, June 1757: heavy humid mist between dark mango trees, distant camp fires, a river bend glimpsed; no people close. ',
  [], 'The Company army camped in the Lakshabag mango grove by the Bhagirathi.', 'Still, heavy, foreboding.', 'Trees foreground, mist middle, fires behind.')
p('G30', 'Plassey, 23 June 1757', '7.2, 7.3', 'Two armies; much of one never fought.',
  'Very wide view across rain-wet fields, 23 June 1757: a small Company army in a line near the mango grove - mostly Indian sepoys in turbans and red coats, with a smaller group of European soldiers in tricorne hats and a few field guns; if any flag is shown it must be the red-and-white striped East India Company ensign (NOT the modern Union Jack, which did not exist until 1801); facing it, a far larger army with elephants and cavalry, much of one flank standing still; heavy grey sky, distant smoke. '
  'No close combat, no blood. ',
  [], 'Roughly 3,000 Company troops faced about 50,000; a heavy rain fell that afternoon; Mir Jafar\'s troops stood aside.', 'Restrained, documentary, no heroics.',
  'Company line foreground-left, open field middle, large army behind; the still flank near the centre.', batch=1)
