import sys, json; sys.path.insert(0, '/home/claude/long'); sys.path.insert(0, '/home/claude/goldL')
from proasm import build_long
import pacing
R = 'raw'
P = [
 ((1.57, 2.88), "Okay, this is crazy."), ((3.95, 4.95), "In January this year,"), ((5.21, 6.08), "one ounce of gold,"),
 ((6.28, 7.45), "that's about 31 grams,"), ((10.30, 11.95), "a little bar that fits in your palm,"), ((12.51, 13.74), "crossed 5,000 dollars."),
 ((14.39, 15.57), "For the first time in history."), ((17.30, 18.22), "And think about it."), ((19.19, 20.17), "Gold is just a metal."),
 ((20.65, 21.40), "We can't eat it."), ((23.70, 25.20), "We can't run our cars on it."), ((33.18, 38.74), "And yet the whole world keeps paying more and more for it."),
 ((39.30, 40.57), "So why is gold so expensive?"), ((45.73, 47.30), "I went really deep on this one."),
 ((48.00, 50.33), "And the answer starts somewhere you'd never expect."), ((51.58, 52.03), "Let's go."),
 ((52.60, 53.14), "Chapter one."), ((53.50, 54.56, R), "It came from the stars."), ((54.56, 57.57, R), "So, first, where does gold even come from?"),
 ((58.00, 60.45), "Not from Earth, not even from our Sun."), ((63.30, 66.22), "Stars make new elements by squeezing atoms together,"),
 ((66.67, 70.40), "hydrogen into helium, helium into carbon, all the way up to iron."), ((71.96, 72.88), "And there, it stops."),
 ((73.75, 77.68), "Gold is way heavier than iron, so a normal star just can't make it."),
 ((90.90, 95.66), "Gold is made when two dead stars called neutron stars smash into each other."),
 ((104.57, 108.37), "And in 2017, scientists actually watched one of those crashes happen,"), ((111.55, 113.24), "130 million light years away."),
 ((113.56, 114.43), "And here's the twist."), ((115.03, 119.28), "When Earth was young and molten, almost all of its gold sank into the core."),
 ((123.30, 126.55, R), "The gold we dig up today arrived later, on meteorites."),
 ((134.20, 138.54), "So, the gold we can actually reach is like a thin dusting left near the surface."),
 ((142.05, 143.91), "That's reason number one, it's rare."), ((148.86, 149.37), "How rare?"),
 ((145.41, 148.05), "Every bit of gold humans have ever mined,"), ((154.50, 158.85, R), "in all of history, is about 222,000 tonnes."),
 ((160.27, 164.42), "Melt it into one block and you'd get a cube about 22 metres on each side."),
 ((165.07, 167.09), "Roughly the height of a seven-storey building."), ((167.55, 169.20), "That's it. That's all of it."),
 ((180.73, 183.01), "Chapter two. It lasts forever."), ((183.85, 184.71), "Now, reason number two."), ((187.28, 188.69), "Gold basically never dies."),
 ((189.01, 192.12), "Iron rusts. Silver turns black. Copper goes green."),
 ((193.04, 197.20), "But gold holds on to its electrons so tightly that oxygen just can't grab it."),
 ((215.19, 220.20, R), "That's why King Tut's gold mask still shines after more than 3,300 years."),
 ((220.85, 222.76), "And this matters for the price, big time."), ((223.46, 224.86), "Because gold doesn't rot,"),
 ((229.00, 232.04), "almost all the gold ever mined is still around today."), ((232.35, 233.79), "It just keeps changing hands."),
 ((234.28, 236.08), "Coin, to necklace, to bar, to ring."), ((236.61, 238.42), "So the gold chain your mom wears?"),
 ((250.21, 255.45), "Some of that gold could have been a king's coin once."),
 ((256.35, 261.37), "Nobody can say for sure, but that's how gold works. It just keeps coming back."),
 ((263.42, 265.26), "Chapter three. Why gold became money."), ((267.25, 269.58), "Okay, but here's a question I never thought about."),
 ((270.79, 272.03), "Out of everything on Earth,"), ((273.12, 274.74), "why did humans pick gold as money?"),
 ((275.42, 278.06), "A chemist actually answered this using the periodic table."), ((278.77, 281.66), "Imagine you're choosing what to use as money."),
 ((282.38, 283.96), "Gases? You can't carry them."), ((284.96, 288.69), "Liquids, like mercury? No."),
 ((289.47, 292.97), "Metals that catch fire, or react with water? Gone."), ((299.84, 302.51), "Radioactive ones? Obviously not. They'd poison you."),
 ((303.33, 306.11), "Then you cut the common ones, like iron and copper."), ((306.64, 308.10), "Too easy to find, and they corrode."),
 ((308.72, 310.37), "And you cut the super rare ones."), ((310.79, 311.90, R), "You can't make enough coins."), ((311.92, 313.14, R), "What's left?"),
 ((313.34, 314.95), "Basically silver, platinum and gold."), ((315.69, 316.81), "Silver tarnishes."),
 ((317.12, 319.26), "Platinum was too hard to melt for ancient people."), ((319.59, 320.52), "So gold wins."),
 ((320.85, 322.09), "Rare, but not too rare."), ((322.44, 325.42), "Easy to melt, easy to shape, and it never rots."),
 ((327.24, 334.08), "That's why for thousands of years, from Egyptian kings to our own grandmothers, people trusted gold."),
 ((339.02, 340.88), "Chapter four. So hard to get."), ((341.52, 342.34), "Reason number three."),
 ((356.10, 358.14, R), "Getting gold out of the ground is brutal."),
 ((358.14, 366.64, R), "In a typical gold mine today, they dig and crush about one tonne of rock to get roughly one and a half grams of gold."),
 ((394.70, 395.80), "A whole tonne of rock for"), ((400.60, 402.70), "a piece of gold smaller than a peppercorn."),
 ((410.92, 415.73), "And even with giant machines, the whole world mines only about 3,600 tonnes a year."),
 ((416.64, 422.47), "That adds less than 2% to all the gold that exists."), ((423.53, 424.91), "You can't just print more gold."),
 ((427.28, 430.35, R), "Chapter five. Why the price keeps climbing."), ((431.85, 434.93), "So gold is rare, it lasts forever, it's hard to mine."),
 ((435.74, 436.87), "But that was always true."), ((442.48, 445.29), "So why has the price gone crazy in the last few years?"),
 ((445.72, 446.40), "Here's the big one."), ((447.04, 448.11), "Countries are buying it."),
 ((456.02, 459.16), "Central banks, the banks that run a country's money,"), ((463.26, 466.77), "used to buy around 470 tonnes of gold a year."),
 ((467.07, 473.02), "Then from 2022 to 2024, they bought more than 1,000 tonnes every single year."),
 ((477.62, 479.96), "And in 2025, still about 860."), ((480.30, 480.70, R), "Why?"),
 ((481.30, 483.80, R), "Because when the world feels scary,"), ((499.44, 504.48), "wars, rising prices, countries not trusting each other,"),
 ((509.90, 513.55), "gold is the one thing that isn't anybody's promise."),
 ((513.86, 517.36), "A government can print more money. Nobody can print more gold."), ((517.60, 518.62), "So the price took off."),
 ((518.92, 522.43), "In 2019, one ounce was around 1,400 dollars."), ((522.76, 526.27), "In January 2026, it crossed 5,000."),
 ((528.26, 531.07), "It's come down since then. It's around 4,000 right now."),
 ((541.17, 544.62), "But that's still almost three times what it was in 2019."),
 ((545.81, 548.93), "Chapter six. And then there's India."), ((551.80, 555.97), "And for us in India, gold isn't just an investment. It's family."),
 ((556.31, 561.58, R), "Weddings. Akshaya Tritiya. Dhanteras, which is coming up on November 6th."),
 ((562.10, 565.87), "Gold gets passed from mothers to daughters, from one generation to the next."),
 ((567.13, 572.39), "India is one of the two biggest gold buyers in the whole world, along with China."),
 ((580.20, 582.53), "So when you see gold prices jump in the news,"), ((591.40, 594.28), "part of that story is happening in our homes."),
 ((610.89, 612.15), "So, why is gold so expensive?"), ((612.62, 614.17), "It was made in exploding stars."), ((615.10, 616.33), "There's very little of it."),
 ((616.36, 617.50), "It never rots."), ((618.92, 619.85), "It's brutal to dig up."), ((620.00, 622.17), "And the moment the world gets scary,"),
 ((622.66, 624.28), "everyone wants it, at the same time."), ((625.56, 626.79), "That combination?"), ((627.26, 630.45), "Nothing else on Earth has it."),
 ((639.20, 641.75), "If you like learning things like this, subscribe."), ((642.48, 643.89), "There's a new why every day."),
 ((643.90, 647.21), "And whenever you get a question that starts with why, comment it below."),
 ((647.36, 648.92), "We'll do the research and get you the answer."),
]
texts = [t for _, t in P]; keep = [k for k, _ in P]
idx = lambda s: next(i for i, t in enumerate(texts) if t.startswith(s))
chap = [idx('Chapter one'), idx('Chapter two'), idx('Chapter three'), idx('Chapter four'), idx('Chapter five'), idx('Chapter six'), idx('So, why is gold so expensive')]
marks = dict(hook_end=idx('So why is gold so expensive'), ask=idx('So why is gold so expensive'), ask_end=chap[0], cta=idx('If you like'),
             chapters=chap, tease=[], lists=[(idx('Gases?'), idx('Then you cut')), (idx('It was made in exploding'), idx('That combination'))],
             reveal=[idx("That's it."), idx('Countries are buying'), idx('So gold wins'), idx('Nothing else on Earth')])
json.dump(texts, open('/home/claude/goldL/pieces_en.json', 'w'))
role, gaps, intra = pacing.plan(texts, marks, None)
gaps[idx('Chapter one') - 1] = 6.6   # room for the title sequence
json.dump(role, open('/home/claude/goldL/roles_en.json', 'w'))
build_long('en', keep, '/home/claude/goldL/voice_en.wav', gaps, intra=intra)
import scipy.io.wavfile as wf
sr, a = wf.read('/home/claude/goldL/voice_en.wav'); total = len(a) / sr
om = json.load(open('/home/claude/goldL/voice_en.wav.map.json'))
print('report', pacing.report(texts, role, om, total), 'total', round(total, 1))
