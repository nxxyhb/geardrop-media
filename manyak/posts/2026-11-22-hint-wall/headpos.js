// node headpos.js scene.html t... -> 주인공 머리 화면 좌표(CSS)
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 } }); await p.goto('file://' + path.resolve(process.argv[2]));
  for (const t of process.argv.slice(3)) console.log(t, JSON.stringify(await p.evaluate((t) => { renderAt(t); return proj(window.__head); }, parseFloat(t))));
  await b.close(); })();
