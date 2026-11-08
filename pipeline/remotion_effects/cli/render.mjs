#!/usr/bin/env node
// Silent MP4 or stills from one effect. Free and local: Remotion + the Chromium already on the machine.
//   node cli/render.mjs headline --aspect 9x16 --lang te --out clip.mp4
//   node cli/render.mjs stat-chart --aspect 16x9 --props spec.json --out clip.mp4
//   node cli/render.mjs map-route --sheet sheet.jpg            (contact sheet: 4 time points)
//   node cli/render.mjs all --sheet-dir renders/sheets --aspect 9x16 --lang en
//   node cli/render.mjs videos --video-dir renders/videos --aspect 16x9 --lang te
import {existsSync, globSync, mkdirSync, readFileSync, rmSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {dirname, join, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';
import {renderMedia, renderStill, selectComposition} from '@remotion/renderer';

const here = dirname(fileURLToPath(import.meta.url)), root = join(here, '..');
const argv = process.argv.slice(2), slug = argv[0];
const opt = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const aspect = opt('aspect', '9x16'), lang = opt('lang', 'en');
spawnSync('node', [join(here, 'sync-fonts.mjs')], {stdio: 'inherit'});

function browser() {
  if (process.env.REMOTION_BROWSER) return process.env.REMOTION_BROWSER;
  const pw = globSync('/opt/pw-browsers/chromium-*/chrome-linux64/chrome')[0];
  return pw ?? ['/usr/bin/google-chrome', '/usr/bin/chromium'].find(existsSync) ?? null;
}
const chrome = {browserExecutable: browser(), chromeMode: 'chrome-for-testing', chromiumOptions: {gl: 'swangle', enableMultiProcessOnLinux: true}, logLevel: 'error', timeoutInMilliseconds: 180000};
const bundled = await bundle({entryPoint: join(root, 'src', 'index.ts'), publicDir: join(root, 'public')});
const sample = (s, l) => JSON.parse(readFileSync(join(root, 'samples', `${s}.${l}.json`), 'utf8'));
const props = (s) => opt('props') ? JSON.parse(readFileSync(resolve(opt('props')), 'utf8')) : sample(s, lang);

async function sheet(s, out) {
  const inputProps = props(s), comp = await selectComposition({serveUrl: bundled, id: `${s}-${aspect}`, inputProps, ...chrome});
  const n = comp.durationInFrames, pts = [0, .33, .66, 1].map((k) => Math.min(n - 1, Math.round(k * (n - 1))));
  const tmp = out + '.tmp'; mkdirSync(tmp, {recursive: true}); const files = [];
  for (const [i, f] of pts.entries()) { const o = join(tmp, `${i}.jpg`); await renderStill({composition: comp, serveUrl: bundled, frame: f, inputProps, output: o, imageFormat: 'jpeg', jpegQuality: 92, ...chrome}); files.push(o); }
  const scale = aspect === '9x16' ? 'scale=360:-1' : 'scale=640:-1';
  const r = spawnSync('ffmpeg', ['-v', 'error', '-y', ...files.flatMap((f) => ['-i', f]), '-filter_complex', files.map((_, i) => `[${i}]${scale}[v${i}]`).join(';') + ';' + files.map((_, i) => `[v${i}]`).join('') + `hstack=inputs=${files.length}`, '-q:v', '3', out], {encoding: 'utf8'});
  if (r.status) throw new Error(r.stderr); rmSync(tmp, {recursive: true});
}
async function video(s, out) {
  const inputProps = props(s), comp = await selectComposition({serveUrl: bundled, id: `${s}-${aspect}`, inputProps, ...chrome});
  await renderMedia({composition: comp, serveUrl: bundled, codec: 'h264', crf: 18, pixelFormat: 'yuv420p', muted: true, outputLocation: out, inputProps, concurrency: 2, ...chrome});
}
const t0 = Date.now();
if (slug === 'all') {
  const dir = opt('sheet-dir', 'renders/sheets'); mkdirSync(dir, {recursive: true}); 
  const only = opt('only')?.split(',') ?? [...new Set(globSync('samples/*.en.json', {cwd: root}).map((f) => f.split('/').pop().replace('.en.json', '')))].sort();
  for (const s of only) { try { await sheet(s, join(dir, `${s}_${aspect}_${lang}.jpg`)); console.log('ok  ', s); } catch (e) { console.log('FAIL', s, String(e.message).slice(0, 300)); process.exitCode = 1; } }
} else if (slug === 'videos') {
  const dir = opt('video-dir', 'renders/videos'); mkdirSync(dir, {recursive: true});
  const only = opt('only')?.split(',') ?? [...new Set(globSync('samples/*.en.json', {cwd: root}).map((f) => f.split('/').pop().replace('.en.json', '')))].sort();
  for (const s of only) { const t = Date.now(); try { await video(s, join(dir, `${s}_${aspect}_${lang}.mp4`)); console.log('ok  ', s, `${((Date.now() - t) / 1000).toFixed(1)}s`); } catch (e) { console.log('FAIL', s, String(e.message).slice(0, 300)); process.exitCode = 1; } }
} else if (opt('sheet')) await sheet(slug, opt('sheet'));
else await video(slug, opt('out', `renders/${slug}_${aspect}_${lang}.mp4`));
console.log(`done in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
