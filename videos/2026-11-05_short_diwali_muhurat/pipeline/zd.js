const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 520, height: 1600 }, deviceScaleFactor: 2, userAgent:'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'});
 await p.goto('https://zerodha.com/marketintel/bulletin/461711/muhurat-trading-session-on-account-of-diwali-november-2026', { waitUntil: 'domcontentloaded', timeout: 60000 }); await p.waitForTimeout(4000);
 const t = await p.$('xpath=//table[contains(., "Pre Open")]'); await t.scrollIntoViewIfNeeded();
 const r = await t.evaluate(n => { const pb = n.getBoundingClientRect(); return Array.from(n.querySelectorAll('tr')).map(tr => { const q = tr.getBoundingClientRect(); return [tr.innerText.replace(/\s+/g,' '), [q.left-pb.left, q.top-pb.top, q.right-pb.left, q.bottom-pb.top].map(v=>Math.round(v*2))]; }); });
 await t.screenshot({ path: 'clip_zd.png' }); console.log(JSON.stringify(r)); await b.close(); })();
