// node search.js scene.html NAME t1,t2 — CAM_OVERRIDE 격자 탐색: 머리(반경0.55)·힌트 간판이 크롭 안전 x 50~475, 머리 위 ≥ 칩+30 를 만족하는 카메라
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 } }); await p.goto('file://' + path.resolve(process.argv[2]));
  const res = await p.evaluate(([name, ts]) => {
    const B = eval(name); window.GCHK = name==='GUARDC'; window.TOPMIN = name==='GUARDC'||name==='LOWUP'||name==='COLD' ? 0 : 335; const out = [];
    for (const qx of [-0.8,-0.4,0,0.4,0.8]) for (const df of [0, 4, 8, 12, 16]) for (const px of [-0.6,-0.4,-0.2, 0, 0.2, 0.4, 0.6, 0.8]) for (const py of [-0.3,-0.15, 0, 0.15]) {
      const f0 = v3.norm(v3.sub(B.look, B.pos)); const r = v3.norm([-f0[2], 0, f0[0]]);
      const cam = { pos: v3.add(B.pos, v3.mul(r, qx)), look: v3.add(B.look, v3.add(v3.mul(r, px), [0, py, 0])), fov: B.fov + df };
      let worst = 1e9, info = [];
      for (const t of ts) { window.CAM_OVERRIDE = null; renderAt(t); const H = window.__head; window.CAM_OVERRIDE = cam; renderAt(t);
        const xs = [proj(v3.add(H, v3.mul(r, -0.55)))[0], proj(v3.add(H, v3.mul(r, 0.55)))[0]];
        const top = proj(v3.add(H, [0, 0.55, 0]))[1];
        const bx = []; for (const a of [-1, 1]) for (const c of [-1, 1]) bx.push(proj(v3.add(BTN, v3.add(v3.mul(TW, 0.34 * a), [0, 0.34 * c, 0])))[0]);
        const hl = Math.min(...xs), hr = Math.max(...xs), br = Math.max(...bx), bl = Math.min(...bx);
        let m = Math.min(hl - 55, 470 - hr, 470 - br, top - (window.TOPMIN||335), bl - 55);
        for (const [G,R] of [[window.__gh,0.55],[window.__gcap,0.5]]) if (G && window.GCHK) { const gx=[proj(v3.add(G, v3.mul(r,-R)))[0],proj(v3.add(G, v3.mul(r,R)))[0]]; m=Math.min(m, Math.min(...gx)-55, 470-Math.max(...gx)); } worst = Math.min(worst, m); info.push([t, Math.round(hl), Math.round(hr), Math.round(top), Math.round(bl), Math.round(br)]); }
      out.push({ qx, df, px, py, worst: Math.round(worst), size: Math.round(info[0][2] - info[0][1]), info });
    }
    window.CAM_OVERRIDE = null; out.sort((a, b) => (b.worst >= 0) - (a.worst >= 0) || (b.worst >= 0 ? b.size - a.size : b.worst - a.worst)); return out.slice(0, 4);
  }, [process.argv[3], process.argv[4].split(',').map(Number)]);
  for (const r of res) console.log(JSON.stringify(r)); await b.close(); })();
