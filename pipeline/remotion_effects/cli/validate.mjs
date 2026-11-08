#!/usr/bin/env node
// Bundles once and resolves every sample in both languages and ratios. Bad props or missing sources fail here.
import {existsSync, globSync, readFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {selectComposition} from '@remotion/renderer';
const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const browserExecutable = process.env.REMOTION_BROWSER ?? globSync('/opt/pw-browsers/chromium-*/chrome-linux64/chrome')[0] ?? ['/usr/bin/google-chrome', '/usr/bin/chromium'].find(existsSync);
const serveUrl = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});
let bad = 0;
// Purely typographic or decorative effects carry no factual claim, so demo:false is allowed there.
const NEVER_FACTUAL = new Set(JSON.parse(readFileSync(join(root, 'cli', 'no-facts.json'), 'utf8')));
const check = async (id, inputProps, expectFail) => {
  try { await selectComposition({serveUrl, id, inputProps, browserExecutable, chromeMode: 'chrome-for-testing', logLevel: 'error'}); if (expectFail) { bad++; console.log('FAIL (should have been rejected)', id); } }
  catch (e) { if (!expectFail) { bad++; console.log('FAIL', id, String(e.message).slice(0, 240)); } else console.log('rejected as expected:', String(e.message).split('\n')[0].slice(0, 160)); }
};
const files = globSync('samples/*.json', {cwd: root}).sort();
for (const f of files) { const [s] = f.split('/').pop().split('.'); const p = JSON.parse(readFileSync(join(root, f), 'utf8')); for (const a of ['9x16', '16x9']) await check(`${s}-${a}`, p); }
for (const f of files.filter((x) => x.endsWith('.en.json'))) { const [s] = f.split('/').pop().split('.'); const p = JSON.parse(readFileSync(join(root, f), 'utf8')); if (p.demo) await check(`${s}-9x16`, {...p, demo: false}, !NEVER_FACTUAL.has(s)); }
console.log(bad ? `${bad} problem(s)` : `${files.length} samples ok`); process.exit(bad ? 1 : 0);
