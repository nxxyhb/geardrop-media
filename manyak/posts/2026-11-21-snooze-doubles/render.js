// node render.js <scene.html> <out.mp4> [duration] | node render.js <scene.html> --shots <dir> t1 t2 ...
const { chromium } = require('/opt/npm-tools/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
(async () => {
  const [scenePath, out, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
  const page = await browser.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  page.on('console', m => console.log('[page]', m.text()));
  page.on('pageerror', e => { console.error('[pageerror]', e.message); process.exitCode = 1; });
  await page.goto('file://' + path.resolve(scenePath));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForFunction(() => typeof window.renderAt === 'function');
  const stage = await page.$('#stage');
  if (out === '--shots') {
    const dir = rest[0]; fs.mkdirSync(dir, { recursive: true });
    for (const t of rest.slice(1)) {
      await page.evaluate((t) => window.renderAt(t), parseFloat(t));
      await stage.screenshot({ path: path.join(dir, `f_${parseFloat(t).toFixed(2)}.jpg`), type: 'jpeg', quality: 85 });
    }
  } else {
    const dur = parseFloat(rest[0] || (await page.evaluate(() => window.DURATION)));
    const fps = 30, n = Math.round(dur * fps);
    const tmp = out.replace(/\.mp4$/, '.tmp.mp4');
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-crf', '18', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', '-r', String(fps), tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      await page.evaluate((t) => window.renderAt(t), i / fps);
      const buf = await stage.screenshot({ type: 'jpeg', quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) console.log(`frame ${i}/${n} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
    fs.renameSync(tmp, out);
    console.log('done', out, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  await browser.close();
})();
