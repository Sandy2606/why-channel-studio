// Copies shared brand assets into Remotion's public folder, so the repo keeps one copy of each.
import {cpSync, mkdirSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
const here = dirname(fileURLToPath(import.meta.url)), repo = join(here, '..', '..', '..'), pub = join(here, '..', 'public');
mkdirSync(join(pub, 'fonts'), {recursive: true}); mkdirSync(join(pub, 'geo'), {recursive: true});
for (const f of ['ArchivoBlack-Regular.ttf', 'SpaceMono-Regular.ttf', 'SpaceMono-Bold.ttf', 'NotoSansTelugu.ttf']) cpSync(join(repo, 'brand', 'fonts', f), join(pub, 'fonts', f));
cpSync(join(repo, 'pipeline', 'lib', 'countries.geojson'), join(pub, 'geo', 'land.geojson'));
