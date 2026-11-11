# Proposed sfx/catalog.json additions (NOT committed: for the user's approval)

Measured on 2026-11-10 from the files as they are (no file changed): duration; loudest 50 ms window (proposed `hit_at` for spot sounds); median level. Beds have no hit point. Sources come from `sfx/golden_sparrow_sfx_sources.txt` and `sfx/pixabay_gs/SOURCE_LIST.txt`.

| File | Proposed key | Proposed role | Type | Duration (s) | Proposed hit_at (s) | Median level (dBFS) | Source | Licence | Note |
|---|---|---|---|---|---|---|---|---|---|
| `amb/village.mp3` | `amb_village` | Indian village bed: distant voices, birds, rural life (GS film) | bed | 293.4 | — (bed) | -39.8 | Pixabay, ranjit_foley "Indian Village Ambience" 219221 | Pixabay Content License |  |
| `amb/birds_cattle.mp3` | `amb_birds_cattle` | Morning countryside: birds and distant cowbells | bed | 111.31 | — (bed) | -49.7 | Pixabay, "amb-birds-cowbells_saranda" 23682 | Pixabay Content License |  |
| `amb/court.mp3` | `amb_court` | Palace hall or court murmur, reverberant | bed | 222.14 | — (bed) | -51.0 | Pixabay, "hall_ambience" 17513 (high-passed 250 Hz) | Pixabay Content License | edited copy of pixabay_gs original |
| `amb/bazaar.mp3` | `amb_bazaar` | Market or bazaar crowd | bed | 33.0 | — (bed) | -28.4 | Pixabay, "market bazaar" 22400 (first 33 s only) | Pixabay Content License | later part had intelligible modern speech, cut |
| `amb/battle.mp3` | `amb_battle` | Distant battle rumble, no rapid automatic fire | bed | 18.0 | — (bed) | -43.8 | Pixabay, "Distant War" 377958 (70–80 s and 180–190 s, low-passed) | Pixabay Content License | restrained use only (GS-01) |
| `amb/march.mp3` | `amb_march` | Army marching steps | bed | 38.57 | — (bed) | -28.6 | Pixabay, "Army Marching Steps" 442715 | Pixabay Content License |  |
| `amb/horses.mp3` | `sfx_horses` | Galloping hooves (cavalry pass) | spot | 14.63 | 3.8 | -23.6 | Pixabay, "Horse running HQ" 247600 | Pixabay Content License |  |
| `amb/drums.mp3` | `sfx_war_drums` | Ceremonial war drums, short phrase | spot | 7.58 | 5.85 | -21.5 | Pixabay, "Ancient War Drums" 463214 | Pixabay Content License |  |
| `amb/elephant.mp3` | `sfx_elephant` | Elephant trumpet (only where an elephant is on screen; SD-02) | spot | 1.94 | 0.5 | -27.7 | Pixabay, "Trumpet sound of an Elephant" 154720 | Pixabay Content License |  |
| `amb/footsteps_stone.mp3` | `sfx_footsteps_stone` | Footsteps on stone (court, fort) | spot | 19.06 | 0.5 | -73.3 | Pixabay, "Footsteps_Stone" 68257 | Pixabay Content License | long silent stretches between steps |
| `amb/ship_bell.mp3` | `sfx_ship_bell` | Ship bell, two chimes (ports) | spot | 2.95 | 0.4 | -52.5 | Pixabay, "Ship Bell Two Chimes" 102730 | Pixabay Content License |  |
| `amb/dock.wav` | `amb_harbour` | Harbour water lapping on rocks (dock beds) | bed | 77.86 | — (bed) | -35.2 | Mixkit "small waves harbor rocks" | Mixkit License | byte-identical in level and length to harbour_waves.wav; propose ONE entry (amb_harbour) pointing to harbour_waves.wav |
| `harbour_waves.wav` | `amb_harbour` | (same as amb/dock.wav) | bed | 77.86 | — (bed) | -35.2 | Mixkit "small waves harbor rocks" | Mixkit License | used by GS 4/6 mix |
| `loom_shuttle.mp3` | `sfx_loom_shuttle` | Weaving-loom shuttle passing back and forth | bed/spot | 58.1 | — (bed) | -53.8 | Pixabay mirror of Freesound 510266 (Naïma, CC0) | Pixabay Content License |  |
| `quill_writing.mp3` | `sfx_quill` | Quill pen writing on hard paper | bed/spot | 98.23 | — (bed) | -42.3 | Pixabay mirror of Freesound 194905 (marcoman89) | Pixabay Content License |  |
| `ship_creak.mp3` | `amb_ship_creak` | Wooden ship creaking at sea | bed | 20.02 | — (bed) | -44.8 | Pixabay, "ship creaking 24b" 30119 | Pixabay Content License |  |
| `cannon_distant.wav` | `sfx_cannon_distant` | Distant cannon fire (several shots) | spot | 35.71 | 3.6 | -34.8 | Freesound 675613, craigsmith "S20-12 Distant cannon fire" (35.7 s, matches) | CC0 | golden_sparrow_sfx_sources.txt still lists it as MISSING; the file present matches the verified original. Please confirm its provenance |
| `amb_fire.mp3` | `amb_fire` | Fire crackle bed (burnings, lamps) | bed | 8.5 | — (bed) | -34.3 | not recorded in the repo | UNKNOWN: needs your confirmation | used since Oct (Ravana, Diwali); converted by setup.sh |
| `amb_crowd.mp3` | `amb_crowd` | Crowd bed (processions) | bed | 9.4 | — (bed) | -24.8 | not recorded in the repo | UNKNOWN: needs your confirmation | converted by setup.sh |
| `amb_drums.mp3` | `amb_drums` | Festival drums bed (processions) | bed | 9.1 | — (bed) | -18.5 | not recorded in the repo | UNKNOWN: needs your confirmation | converted by setup.sh |

**Not proposed:** the 13 originals in `sfx/pixabay_gs/` are the untouched source downloads of the `amb/` files (kept for provenance and credits), so the catalog should point at the edited `amb/` copies. `alex_jauk-wooden-water-wheel-196741.mp3` (a water wheel, not a charkha) has no `amb/` copy and wasn't used: catalog it or leave it?

**Correction to earlier reports:** I said seven sounds were uncatalogued. The exact count is 20 working files (12 in `amb/`, 8 at the top level), one of them a duplicate, plus the 13 untouched source originals.

Once approved, the entries go into `sfx/catalog.json` in the existing format (`file`, `source`, `dur`, `use`, `note`, `hit_at`), with no change to any audio file.
