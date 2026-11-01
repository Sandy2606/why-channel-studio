const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1100, height: 1400 }, deviceScaleFactor: 2 });
  await p.goto('https://science.nasa.gov/earth/earth-observatory/south-asian-night-lights-79682/', { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(2000);
  const el = await p.$('xpath=//p[contains(., "imperceptible")]');
  if (el) { await el.scrollIntoViewIfNeeded(); await el.screenshot({ path: 'nasa_para.png' }); console.log('para ok'); }
  const h = await p.$('h1'); if (h) { await h.screenshot({ path: 'nasa_h1.png' }); console.log('h1 ok'); }
  const box = el ? await el.boundingBox() : null; console.log(JSON.stringify(box));
  console.log(el ? await el.innerText() : 'no para');
  await b.close();
})();
