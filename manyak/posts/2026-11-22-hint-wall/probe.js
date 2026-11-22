// node probe.js scene.html "<js expr returning value>" t... — renderAt(t) 후 식 평가(장면 배치 확인용)
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 } }); await p.goto('file://' + path.resolve(process.argv[2]));
  const ex = process.argv[3];
  for (const t of process.argv.slice(4)) console.log(t, JSON.stringify(await p.evaluate(([t, ex]) => { renderAt(t); return eval(ex); }, [parseFloat(t), ex])));
  await b.close(); })();
