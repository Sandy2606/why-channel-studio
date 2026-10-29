const { chromium } = require('playwright');
const mark = (tx, ty, s) => `<g transform="translate(${tx},${ty}) scale(${s}) translate(-100,-164)">
<circle cx="100" cy="290" r="64" fill="#FFB224" opacity="0.5" filter="url(#g)"/>
<path d="M100 200 L100 175 C100 155 126.7 151.6 146 128.6 A60 60 0 1 0 40.23 95.23" fill="none" stroke="#F4F1EA" stroke-width="60" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="100" cy="290" r="38" fill="#FFB224"/></g>`;
const page = (te) => `<html><head><style>@font-face{font-family:T;src:url(file:///home/claude/fonts/NotoSansTelugu.ttf);font-weight:100 900}body{margin:0;background:#0A0A0A}</style></head><body>
<svg width="2160" height="2160" viewBox="0 0 2160 2160"><defs><filter id="g" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="22"/></filter></defs>
<rect width="2160" height="2160" fill="#0A0A0A"/>
${te ? mark(1080, 860, 1000/328) : mark(1080, 1080, 1180/328)}
${te ? '<text x="1080" y="1660" text-anchor="middle" font-family="T" font-weight="900" font-size="300" fill="#FFB224">తెలుగు</text>' : ''}
</svg></body></html>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 2160, height: 2160 } });
  for (const [te, name] of [[false, 'why_profile_2160.png'], [true, 'why_telugu_profile_2160.png']]) {
    await p.setContent(page(te)); await p.waitForTimeout(500);
    await p.screenshot({ path: name, clip: { x: 0, y: 0, width: 2160, height: 2160 } });
  }
  await b.close();
})();
