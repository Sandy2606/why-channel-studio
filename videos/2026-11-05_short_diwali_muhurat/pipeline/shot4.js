const { chromium } = require('playwright');
// usage: node shot4.js url xpathContains phrase out.png [width]
(async () => {
  const [url, contains, phrase, out, width] = process.argv.slice(2);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: +(width || 440), height: 1600 }, deviceScaleFactor: 2,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36' });
  await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(4000);
  const els = await p.$$(`xpath=//*[self::p or self::td or self::tr or self::li or self::div][contains(normalize-space(.), "${contains}")]`);
  let el = null, best = 1e9;
  for (const e of els) { const n = await e.evaluate(x => x.innerText.length); if (n < best && n > 0) { best = n; el = e; } }
  if (!el) { console.log('NOTFOUND'); await b.close(); return; }
  await el.scrollIntoViewIfNeeded();
  const r = await el.evaluate((n, ph) => {
    const pb = n.getBoundingClientRect(); const w = document.createTreeWalker(n, NodeFilter.SHOW_TEXT); let txt = '', nodes = [];
    while (w.nextNode()) { nodes.push([w.currentNode, txt.length]); txt += w.currentNode.textContent; }
    const a = txt.indexOf(ph); if (a < 0) return null; const z = a + ph.length;
    const loc = (i) => { for (let k = nodes.length - 1; k >= 0; k--) if (nodes[k][1] <= i) return [nodes[k][0], i - nodes[k][1]]; };
    const rg = document.createRange(); const [s0, o0] = loc(a); const [s1, o1] = loc(z); rg.setStart(s0, o0); rg.setEnd(s1, o1);
    return Array.from(rg.getClientRects()).filter(q => q.width > 2).map(q => [q.left - pb.left, q.top - pb.top, q.right - pb.left, q.bottom - pb.top].map(v => Math.round(v * 2)));
  }, phrase);
  await el.screenshot({ path: out }); console.log(JSON.stringify(r)); await b.close();
})();
