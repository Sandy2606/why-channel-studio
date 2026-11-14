# Cinematic evidence-driven storytelling (optional treatment)

**Status:** an optional production capability, approved by the user on Nov 14, 2026 for Delhi Rain 1/6 v2. It is **not a compulsory template.** Combine it freely with Golden Sparrow-style historical storytelling, character scenes, the host-led method (`host_led.md`) and the animation styles in `pipeline/styles` and `pipeline/remotion_effects`. The story decides.

**Goal (unchanged):** curiosity, understanding, emotional connection and retention. The finished video should feel like a professionally directed documentary, not a fast slideshow.

## What it combines
- **Human story in painterly documentary scenes.** Real people or clearly labelled illustrative characters, shown on native pixels (LAY-05) with slow camera moves: pans, pushes and match cuts. Example: the 1957 lawn → the boy → the grandfather → Anu.
- **Genuine evidence, shown as evidence.**
  - Original SOURCE cards in our own layout carry only verified fields: authors, journal and issue, report and agency, date. A real headline is quoted only after its wording has been checked against the article, with the publication and date as a source line.
  - Never imitate a masthead or logo, never fabricate an authentic-looking historical document, and never reproduce a page we don't have rights to.
- **Continuous explanatory animation.** One camera move carries the idea from step to step instead of cutting between cards, for example:
  - a timeline dolly to the next era;
  - a tilt down to the place;
  - a machine that draws itself, lights up and releases particles;
  - a push into a calendar of trial days;
  - the days flying into a balance.

  The animation explains a mechanism or a comparison; it is not decoration.
- **Purposeful host appearances.** The host appears where a person helps: the hook, a reaction such as "Not proof", a turn in the story, or the question. There is no fixed quota. He reacts, with a different framing each time, rather than standing through long stretches.

## Craft notes from the Delhi Rain tests
- **Rhythm:**
  - Something meaningful develops roughly every couple of seconds: a new step of the explanation, a label landing on the spoken word, a scene change.
  - Blinks, background drift and decorative transitions don't count.
  - Don't cut just to hit a number; a held moment is fine when the viewer is reading or feeling.
- **Use the whole 1080×1920 frame.** There is no fixed working rectangle. Make the key objects big enough to read on a phone. Captions may overlay pictures when they have a contrasting outline and don't hide an important detail. Check Telugu frames separately for empty dark areas.
- **Text (from Golden Sparrow 5/6):**
  - A big key term first (about 90 px), then the picture or document, then a small source line (≥ 24 px).
  - Labels with leader lines point at the thing they name.
  - Telugu labels run about 1.2× the English pixel size.
  - Telugu fonts lack → and ≈: spell them out.
- **One spine per series:** a recurring device that orients the viewer, such as Golden Sparrow's time line or Delhi Rain's 1957 → 1971–72 → 2025 rail.
- **Honest metaphors:**
  - A visual metaphor (for example a balance for "a tendency") is labelled as an illustration ("not measured rainfall").
  - It keeps the uncertainty visible: a band that includes "no difference", and a beam that never settles.
  - No invented numbers.
- **Accuracy in animation:**
  - Show what an experiment aimed for, not a result it didn't get (the 2025 smog never clears).
  - Chemistry is shown as it is (silver iodide as particles that ice can form on).
- **Season and place:** Delhi winter is cool grey haze, not snow.
- **Each language keyed to its own words.** Telugu word order can reverse beats: there the finding comes before the report, and "to compare" comes before the second eleven days. Build the same beats in each language's order and pace; never stretch or speed the voice to match English.
- **Freeze checks:** thin line drawings and small moving sprites can trigger `freezedetect` while genuinely moving. Look at the frames before calling something a hold, and record such cases as detector false positives.

## Building blocks used (reusable)
- `/home/claude/dr1/v2.py`: the Delhi Rain 1/6 v2 renderer. It is local because it reads private host assets; the patterns are listed here.
  - Timeline dolly with card flips.
  - Self-drawing schematic (blueprint stroke with a partial path).
  - Particle plume.
  - Calendar tiles that pop on the spoken count.
  - Balance metaphor with an uncertainty wedge.
  - Magnifier with a looping micro-mechanism.
  - SOURCE card and headline card (our layout).
  - Year counter over the series rail.
  - Painterly plates with leader-line labels and flowing arrows.
