const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto('https://science.nasa.gov/earth/earth-observatory/south-asian-night-lights-79682/', { waitUntil: 'networkidle', timeout: 60000 });
  const el = await p.$('xpath=//p[contains(., "imperceptible")]'); await el.scrollIntoViewIfNeeded();
  const r = await el.evaluate((n) => {
    const t = n.firstChild; const s = t.textContent; const a = s.indexOf('so subtle'); const z = s.length;
    const rg = document.createRange(); rg.setStart(t, a); rg.setEnd(t, z);
    const pb = n.getBoundingClientRect();
    return Array.from(rg.getClientRects()).map(q => [q.left - pb.left, q.top - pb.top, q.right - pb.left, q.bottom - pb.top]);
  });
  console.log(JSON.stringify(r)); await el.screenshot({ path: 'cap/nasa_para.png' }); await b.close();
})();
