import json, base64, html, sys
sys.path.insert(0, '/home/claude/gs/pack2')
from pack2_data import P, STYLE, LAYERS
REFNOTE = {'R1': 'Attach R1 (your cloth reference image).', 'CHAR': 'Attach the character sheet.', 'T3': 'Attach T3 (the trunk-room image).'}
for x in P:
    lead = ' '.join(REFNOTE[r] for r in x['refs'])
    x['full'] = ((lead + ' ') if lead else '') + x['prompt'].strip() + ' ' + STYLE + ('' if x['id'] == 'R1' else ' ' + LAYERS)
# ---------- markdown for review
V = '/home/claude/why-channel-studio/videos/2026-11-08_long_golden_sparrow_s1'
o = ['# The Golden Sparrow S1: image prompt pack v2 (G01–G30 + R1)', '',
     '**How to make the images:**',
     '- **Where:** continue in the same ChatGPT chat that made T1–T8, so it keeps the approved style.',
     '- **One image per prompt:** paste one prompt at a time and download the result at full size.',
     '- **Sending them back:** send the images here and type their IDs in the same order you attach them.',
     '- **Test batch first:** make only the 7 images marked TEST (R1 first, because G05 and G10 use it). We approve them, and only then make the rest.', '',
     '## Reference requirements (reconciled)',
     '| Reference | What it fixes | Needed by |', '|---|---|---|',
     '| **Character sheet** (approved v1) | Anna, Chelli, the trunk, Ammamma\'s kalamkari cloth | G15 only (the only new image with the children) |',
     '| **T3** (approved image) | Ammamma\'s room: tiled roof, barred window, red-oxide floor, trunk | G15 |',
     '| **R1 cloth reference** (make first) | "Our cloth": the fictional 1680 chintz and its bale mark | ' + ', '.join(x['id'] for x in P if 'R1' in x['refs']) + ' |',
     '| None | Everything else, with style kept by the shared style block and the same chat | the remaining ' + str(sum(1 for x in P if not x['refs'] and x['id'] != 'R1')) + ' images |', '',
     'My earlier "seven need the character sheet" was wrong. Only **G15** needs it (with T3). The cloth reference R1 is needed by the eight images that show our cloth.', '',
     '**Our cloth vs Ammamma\'s cloth:** these are two different cloths.',
     '- **Ammamma\'s kalamkari** (Rama, Sita, Lakshmana) belongs to the present-day frame story, and the character sheet fixes its look.',
     '- **Our cloth** is the 1680 chintz that travels from the village to London, and R1 fixes its look.', '',
     '## Prompts', '']
for x in P:
    o += [f"### {x['id']} · {x['title']}{'  ·  TEST BATCH' if x['batch'] == 1 else ''}",
          f"- **Scene:** {x['scene']}. {x['purpose']}",
          f"- **References to attach:** {', '.join(x['refs']) if x['refs'] else 'none'}"]
    if x['history']: o.append(f"- **Historical details:** {x['history']}")
    o += [f"- **Art direction:** {x['art']}", f"- **16:9 / 9:16 / parallax:** {x['comp']}", '', '```', x['full'], '```', '']
open(f'{V}/image_prompt_pack_v2.md', 'w').write('\n'.join(o) + '\n')
json.dump(P, open(f'{V}/visuals/prompts/pack2_prompts.json', 'w'), ensure_ascii=False, indent=1)
# ---------- phone page
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
tpl = open('/home/claude/gs/pack2/template2.html').read()
page = tpl.replace('__DATA__', json.dumps(P, ensure_ascii=False)).replace('__SHEET__', b64('/home/claude/gs/pack2/sheet.jpg')).replace('__T3__', b64('/home/claude/gs/pack2/t3.jpg'))
open('/home/claude/gs/pack2/golden_sparrow_image_pack_v2.html', 'w').write(page)
print('ok', len(P), sum(1 for x in P if x['batch'] == 1))
