// node hudcheck.js scene.html  -> 0.25초 간격 전 구간 window.hudCheck()
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.resolve(process.argv[2])); await p.evaluate(() => document.fonts.ready);
  const dur = await p.evaluate(() => window.DURATION); let bad = 0, n = 0, worst = 0, minL = 999, maxR = 0, topMin = 999, botMax = 0;
  for (let t = 0; t <= dur + 1e-6; t += 0.25) {
    const r = await p.evaluate((t) => { window.renderAt(t); return window.hudCheck(); }, t); n++;
    for (const e of r) { worst = Math.max(worst, Math.abs(e.cx - 270)); minL = Math.min(minL, e.left); maxR = Math.max(maxR, e.right); topMin = Math.min(topMin, e.top); botMax = Math.max(botMax, e.bottom);
      if (!e.ok || e.top < 115 || e.bottom > 720) { bad++; console.log('FAIL', t.toFixed(2), JSON.stringify(e)); } }
  }
  console.log(JSON.stringify({ frames: n, fails: bad, maxCxDev: +worst.toFixed(1), minLeft: minL, maxRight: maxR, minTop: topMin, maxBottom: botMax }));
  await b.close();
})();
