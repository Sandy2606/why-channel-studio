# Proposed sfx/catalog.json change (NOT committed: for the user's approval)

Proposed file: `playbook/reports/2026-11-10_sfx_catalog_proposed.json`. On approval it replaces `sfx/catalog.json`; no audio file is added, changed or deleted.

## 1. New entries (19)

| Key | File | Use | Licence | Provenance status | Cleared for new work |
|---|---|---|---|---|---|
| `amb_village` | `amb/village.mp3` | village bed: distant voices, birds, rural life | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `amb_birds_cattle` | `amb/birds_cattle.mp3` | morning countryside: birds, distant cowbells | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `amb_court` | `amb/court.mp3` | court or palace hall murmur | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `amb_bazaar` | `amb/bazaar.mp3` | market crowd | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `amb_battle` | `amb/battle.mp3` | distant battle rumble; restrained use (GS-01) | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `amb_march` | `amb/march.mp3` | army marching steps | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `sfx_horses` | `amb/horses.mp3` | cavalry pass | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `sfx_war_drums` | `amb/drums.mp3` | ceremonial war drums | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `sfx_elephant` | `amb/elephant.mp3` | elephant trumpet, only when an elephant is on screen (SD-02) | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `sfx_footsteps_stone` | `amb/footsteps_stone.mp3` | footsteps on stone | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `sfx_ship_bell` | `amb/ship_bell.mp3` | ship bell, two chimes (ports) | Pixabay Content License | VERIFIED against the kept original (audio match) | yes |
| `amb_harbour` | `harbour_waves.wav` | harbour water lapping (dock beds) | Mixkit License | SOURCE RECORDED: duration matches; original download not kept, so audio not compared | yes |
| `sfx_loom_shuttle` | `loom_shuttle.mp3` | weaving-loom shuttle | Pixabay Content License | SOURCE RECORDED: duration matches; original download not kept, so audio not compared | yes |
| `sfx_quill` | `quill_writing.mp3` | quill pen on hard paper | Pixabay Content License | SOURCE RECORDED: duration matches; original download not kept, so audio not compared | yes |
| `amb_ship_creak` | `ship_creak.mp3` | wooden ship creaking at sea | Pixabay Content License | SOURCE RECORDED: duration matches; original download not kept, so audio not compared | yes |
| `sfx_cannon_distant` | `cannon_distant.wav` | distant cannon fire (several shots) | CC0 (as listed by Freesound) | PENDING | no |
| `amb_fire` | `amb_fire.mp3` | fire crackle bed | UNKNOWN | UNKNOWN | no |
| `amb_crowd` | `amb_crowd.mp3` | procession crowd bed | UNKNOWN | UNKNOWN | no |
| `amb_drums` | `amb_drums.mp3` | festival drums bed | UNKNOWN | UNKNOWN | no |

## 2. Path corrections to existing entries (28)

These entries record `lib/<name>` from the folder the library was first built in; the files actually live flat in `sfx/`. Only the `file` field changes.

`impact_big`: `lib/impact_big.wav` → `impact_big.wav`, `impact_trailer`: `lib/impact_trailer.wav` → `impact_trailer.wav`, `sub_knock`: `lib/sub_knock.wav` → `sub_knock.wav`, `heartbeat`: `lib/heartbeat.wav` → `heartbeat.wav`, `riser`: `lib/riser.wav` → `riser.wav`, `woosh_deep`: `lib/woosh_deep.wav` → `woosh_deep.wav`, `swoosh_slow`: `lib/swoosh_slow.wav` → `swoosh_slow.wav`, `page_turn`: `lib/page_turn.wav` → `page_turn.wav`, `paper_slide`: `lib/paper_slide.wav` → `paper_slide.wav`, `tick`: `lib/tick.wav` → `tick.wav`, `ticker_run`: `lib/ticker_run.wav` → `ticker_run.wav`, `typing_run`: `lib/typing_run.wav` → `typing_run.wav`, `key_press`: `lib/key_press.wav` → `key_press.wav`, `mouse_click`: `lib/mouse_click.wav` → `mouse_click.wav`, `paper_drop`: `lib/paper_drop.wav` → `paper_drop.wav`, `marker`: `lib/marker.wav` → `marker.wav`, `scribble`: `lib/scribble.wav` → `scribble.wav`, `shutter`: `lib/shutter.wav` → `shutter.wav`, `boom_impact`: `lib/boom_impact.wav` → `boom_impact.wav`, `boom_distant`: `lib/boom_distant.wav` → `boom_distant.wav`, `riser_synth`: `lib/riser_synth.wav` → `riser_synth.wav`, `woosh_tunnel`: `lib/woosh_tunnel.wav` → `woosh_tunnel.wav`, `woosh_air`: `lib/woosh_air.wav` → `woosh_air.wav`, `heartbeat_slow`: `lib/heartbeat_slow.wav` → `heartbeat_slow.wav`, `stamp`: `lib/stamp.wav` → `stamp.wav`, `pin_push`: `lib/pin_push.wav` → `pin_push.wav`, `map_unfold`: `lib/map_unfold.wav` → `map_unfold.wav`, `polaroid`: `lib/polaroid.wav` → `polaroid.wav`

## 3. Not added
- The 13 untouched originals in `sfx/pixabay_gs/` (kept for credits and provenance).
- `alex_jauk-wooden-water-wheel-196741.mp3` (unused; not a charkha), per the user's decision.
- `amb/dock.wav`, a byte-identical duplicate of `harbour_waves.wav`; kept on disk, not catalogued separately.

## 4. Full diff (sorted keys)

```diff
--- sfx/catalog.json (current)
+++ sfx/catalog.json (proposed)
@@ -5,2 +5,107 @@
  ],
+ "amb_battle": {
+  "dur": 18.0,
+  "file": "amb/battle.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: halves match the original at 70.0 s (r=0.986) and 181.0 s (r=0.897); source in golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 377958 \"Distant War\" (70–80 s + 180–190 s, low-passed)",
+  "use": "distant battle rumble; restrained use (GS-01)"
+ },
+ "amb_bazaar": {
+  "dur": 33.0,
+  "file": "amb/bazaar.mp3",
+  "license": "Pixabay Content License",
+  "note": "later part had intelligible modern speech, cut",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/freesound_community-market-bazaar-22400.mp3 (r=0.976, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 22400 \"market bazaar\" (first 33 s)",
+  "use": "market crowd"
+ },
+ "amb_birds_cattle": {
+  "dur": 111.31,
+  "file": "amb/birds_cattle.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/freesound_community-amb-birds-cowbells_saranda-23682.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 23682 \"amb-birds-cowbells_saranda\"",
+  "use": "morning countryside: birds, distant cowbells"
+ },
+ "amb_court": {
+  "dur": 222.14,
+  "file": "amb/court.mp3",
+  "license": "Pixabay Content License",
+  "note": "high-passed copy (lower correlation expected)",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/freesound_community-hall_ambience-17513.mp3 (r=0.895, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 17513 \"hall_ambience\" (high-passed 250 Hz)",
+  "use": "court or palace hall murmur"
+ },
+ "amb_crowd": {
+  "approved_for_new_work": false,
+  "dur": 9.4,
+  "file": "amb_crowd.mp3",
+  "licence_status": "UNKNOWN",
+  "license": "UNKNOWN",
+  "note": "existing productions unchanged; not cleared for new work",
+  "provenance": "UNKNOWN: from the sound pack the user sent on 2026-10-26 (Dussehra long video), cut into tracks; the source site and licence were never recorded",
+  "source": "unknown (user-supplied pack, 2026-10-26)",
+  "use": "procession crowd bed"
+ },
+ "amb_drums": {
+  "approved_for_new_work": false,
+  "dur": 9.1,
+  "file": "amb_drums.mp3",
+  "licence_status": "UNKNOWN",
+  "license": "UNKNOWN",
+  "note": "existing productions unchanged; not cleared for new work",
+  "provenance": "UNKNOWN: from the sound pack the user sent on 2026-10-26 (Dussehra long video), cut into tracks; the source site and licence were never recorded",
+  "source": "unknown (user-supplied pack, 2026-10-26)",
+  "use": "festival drums bed"
+ },
+ "amb_fire": {
+  "approved_for_new_work": false,
+  "dur": 8.5,
+  "file": "amb_fire.mp3",
+  "licence_status": "UNKNOWN",
+  "license": "UNKNOWN",
+  "note": "existing productions unchanged; not cleared for new work",
+  "provenance": "UNKNOWN: from the sound pack the user sent on 2026-10-26 (Dussehra long video), cut into tracks; the source site and licence were never recorded",
+  "source": "unknown (user-supplied pack, 2026-10-26)",
+  "use": "fire crackle bed"
+ },
+ "amb_harbour": {
+  "dur": 77.86,
+  "file": "harbour_waves.wav",
+  "license": "Mixkit License",
+  "note": "sfx/amb/dock.wav is a byte-identical copy, kept (not deleted) because existing projects may refer to it",
+  "provenance": "duration 77.86 s matches the recorded 77.9 s source (golden_sparrow_sfx_sources.txt, item 2); original download not kept separately",
+  "source": "Mixkit \"small waves harbor rocks\"",
+  "use": "harbour water lapping (dock beds)"
+ },
+ "amb_march": {
+  "dur": 38.57,
+  "file": "amb/march.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/alex_jauk-army-marching-steps-ambience-noise-442715.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 442715 \"Army Marching Steps\"",
+  "use": "army marching steps"
+ },
+ "amb_ship_creak": {
+  "dur": 20.02,
+  "file": "ship_creak.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "duration 20.02 s matches the recorded 0:20 source (item 3); original download not kept separately",
+  "source": "Pixabay 30119 \"ship creaking 24b\"",
+  "use": "wooden ship creaking at sea"
+ },
+ "amb_village": {
+  "dur": 293.4,
+  "file": "amb/village.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/ranjit_foley-indian-village-ambience-219221.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 219221 \"Indian Village Ambience\" (ranjit_foley)",
+  "use": "village bed: distant voices, birds, rural life"
+ },
  "bell_ring": {
@@ -15,3 +120,3 @@
   "dur": 5.51,
-  "file": "lib/boom_distant.wav",
+  "file": "boom_distant.wav",
   "hit_at": 0.44,
@@ -24,3 +129,3 @@
   "dur": 5.99,
-  "file": "lib/boom_impact.wav",
+  "file": "boom_impact.wav",
   "hit_at": 1.3,
@@ -97,3 +202,3 @@
   "dur": 1.1,
-  "file": "lib/heartbeat.wav",
+  "file": "heartbeat.wav",
   "note": "",
@@ -104,3 +209,3 @@
   "dur": 4.0,
-  "file": "lib/heartbeat_slow.wav",
+  "file": "heartbeat_slow.wav",
   "hit_at": 0.45,
@@ -113,3 +218,3 @@
   "dur": 7.93,
-  "file": "lib/impact_big.wav",
+  "file": "impact_big.wav",
   "hit_at": 2.17,
@@ -121,3 +226,3 @@
   "dur": 4.87,
-  "file": "lib/impact_trailer.wav",
+  "file": "impact_trailer.wav",
   "hit_at": 0.93,
@@ -137,3 +242,3 @@
   "dur": 0.35,
-  "file": "lib/key_press.wav",
+  "file": "key_press.wav",
   "hit_at": 0.0,
@@ -170,3 +275,3 @@
   "dur": 1.42,
-  "file": "lib/map_unfold.wav",
+  "file": "map_unfold.wav",
   "hit_at": 0.6,
@@ -179,3 +284,3 @@
   "dur": 1.24,
-  "file": "lib/marker.wav",
+  "file": "marker.wav",
   "hit_at": 0.04,
@@ -212,3 +317,3 @@
   "dur": 0.35,
-  "file": "lib/mouse_click.wav",
+  "file": "mouse_click.wav",
   "hit_at": 0.01,
@@ -221,3 +326,3 @@
   "dur": 0.45,
-  "file": "lib/page_turn.wav",
+  "file": "page_turn.wav",
   "note": "",
@@ -228,3 +333,3 @@
   "dur": 0.61,
-  "file": "lib/paper_drop.wav",
+  "file": "paper_drop.wav",
   "hit_at": 0.21,
@@ -237,3 +342,3 @@
   "dur": 1.09,
-  "file": "lib/paper_slide.wav",
+  "file": "paper_slide.wav",
   "note": "",
@@ -252,3 +357,3 @@
   "dur": 0.5,
-  "file": "lib/pin_push.wav",
+  "file": "pin_push.wav",
   "hit_at": 0.27,
@@ -261,3 +366,3 @@
   "dur": 3.41,
-  "file": "lib/polaroid.wav",
+  "file": "polaroid.wav",
   "hit_at": 0.8,
@@ -278,3 +383,3 @@
   "dur": 2.58,
-  "file": "lib/riser.wav",
+  "file": "riser.wav",
   "hit_at": 2.53,
@@ -286,3 +391,3 @@
   "dur": 9.34,
-  "file": "lib/riser_synth.wav",
+  "file": "riser_synth.wav",
   "hit_at": 3.87,
@@ -295,3 +400,3 @@
   "dur": 1.19,
-  "file": "lib/scribble.wav",
+  "file": "scribble.wav",
   "hit_at": 0.17,
@@ -302,5 +407,85 @@
  },
+ "sfx_cannon_distant": {
+  "approved_for_new_work": false,
+  "dur": 35.71,
+  "file": "cannon_distant.wav",
+  "hit_at": 3.6,
+  "licence_status": "PENDING VERIFICATION",
+  "license": "CC0 (as listed by Freesound)",
+  "note": "",
+  "provenance": "PENDING: metadata matches the documented original (WAV, 48 kHz, 24-bit, mono, 35.705 s, 4.9 MB); audio not compared because the original needs a Freesound login; golden_sparrow_sfx_sources.txt still says MISSING",
+  "source": "Freesound 675613 \"S20-12 Distant cannon fire\" (craigsmith)",
+  "use": "distant cannon fire (several shots)"
+ },
+ "sfx_elephant": {
+  "dur": 1.94,
+  "file": "amb/elephant.mp3",
+  "hit_at": 0.5,
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/u_7bikmggkv2-trumpet-sound-of-an-elephant-154720.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 154720 \"Trumpet sound of an Elephant\"",
+  "use": "elephant trumpet, only when an elephant is on screen (SD-02)"
+ },
+ "sfx_footsteps_stone": {
+  "dur": 19.06,
+  "file": "amb/footsteps_stone.mp3",
+  "hit_at": 0.5,
+  "license": "Pixabay Content License",
+  "note": "long silent gaps between steps",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/freesound_community-footsteps_stone-68257.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 68257 \"Footsteps_Stone\"",
+  "use": "footsteps on stone"
+ },
+ "sfx_horses": {
+  "dur": 14.63,
+  "file": "amb/horses.mp3",
+  "hit_at": 3.8,
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/tanweraman-horse-running-hq-247600.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 247600 \"Horse running HQ\"",
+  "use": "cavalry pass"
+ },
+ "sfx_loom_shuttle": {
+  "dur": 58.1,
+  "file": "loom_shuttle.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "duration 58.1 s matches the recorded 0:58 source (item 1); original download not kept separately",
+  "source": "Pixabay mirror of Freesound 510266 \"navette de métier à tisser\" (Naïma, CC0)",
+  "use": "weaving-loom shuttle"
+ },
+ "sfx_quill": {
+  "dur": 98.23,
+  "file": "quill_writing.mp3",
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "duration 98.23 s matches the recorded 98.2 s source (item 4); original download not kept separately",
+  "source": "Pixabay mirror of Freesound 194905 (marcoman89)",
+  "use": "quill pen on hard paper"
+ },
+ "sfx_ship_bell": {
+  "dur": 2.95,
+  "file": "amb/ship_bell.mp3",
+  "hit_at": 0.4,
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/freesound_community-ship-bell-two-chimes-102730.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 102730 \"Ship Bell Two Chimes\"",
+  "use": "ship bell, two chimes (ports)"
+ },
+ "sfx_war_drums": {
+  "dur": 7.58,
+  "file": "amb/drums.mp3",
+  "hit_at": 5.85,
+  "license": "Pixabay Content License",
+  "note": "",
+  "provenance": "verified 2026-11-10: audio envelope matches sfx/pixabay_gs/dragon-studio-ancient-war-drums-463214.mp3 (r=1.0, offset 0.0 s); source and licence recorded in sfx/golden_sparrow_sfx_sources.txt",
+  "source": "Pixabay 463214 \"Ancient War Drums\"",
+  "use": "ceremonial war drums"
+ },
  "shutter": {
   "dur": 0.4,
-  "file": "lib/shutter.wav",
+  "file": "shutter.wav",
   "hit_at": 0.04,
@@ -329,3 +514,3 @@
   "dur": 1.03,
-  "file": "lib/stamp.wav",
+  "file": "stamp.wav",
   "hit_at": 0.02,
@@ -338,3 +523,3 @@
   "dur": 0.62,
-  "file": "lib/sub_knock.wav",
+  "file": "sub_knock.wav",
   "note": "",
@@ -345,3 +530,3 @@
   "dur": 5.5,
-  "file": "lib/swoosh_slow.wav",
+  "file": "swoosh_slow.wav",
   "note": "",
@@ -352,3 +537,3 @@
   "dur": 0.07,
-  "file": "lib/tick.wav",
+  "file": "tick.wav",
   "note": "",
@@ -359,3 +544,3 @@
   "dur": 0.85,
-  "file": "lib/ticker_run.wav",
+  "file": "ticker_run.wav",
   "note": "",
@@ -366,3 +551,3 @@
   "dur": 26.31,
-  "file": "lib/typing_run.wav",
+  "file": "typing_run.wav",
   "hit_at": 14.87,
@@ -434,3 +619,3 @@
   "dur": 2.32,
-  "file": "lib/woosh_air.wav",
+  "file": "woosh_air.wav",
   "hit_at": 0.71,
@@ -443,3 +628,3 @@
   "dur": 2.98,
-  "file": "lib/woosh_deep.wav",
+  "file": "woosh_deep.wav",
   "note": "",
@@ -450,3 +635,3 @@
   "dur": 6.75,
-  "file": "lib/woosh_tunnel.wav",
+  "file": "woosh_tunnel.wav",
   "hit_at": 0.62,
```
