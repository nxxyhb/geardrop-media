// node search2.js scene.html NAME t1,t2 — video #5: 머리(0.55)·몸통(0.5)과 힌트 간판이 겹치지 않고(간판 왼쪽 ≥ 인물 오른쪽+8) 모두 크롭 안전 x 55~470
const { chromium } = require('/opt/npm-tools/node_modules/playwright'); const path = require('path');
(async () => { const b = await chromium.launch({ executablePath: '/usr/bin/google-chrome', args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 540, height: 960 } }); await p.goto('file://' + path.resolve(process.argv[2]));
  const res = await p.evaluate(([name, ts]) => {
    const B = eval(name); const out = [];
    for (const qx of [-1.2,-0.8,-0.4,0,0.4,0.8,1.2]) for (const df of [-4, 0, 4, 8, 12]) for (const px of [-0.6,-0.4,-0.2, 0, 0.2, 0.4, 0.6]) for (const py of [-0.2, 0, 0.2]) {
      const f0 = v3.norm(v3.sub(B.look, B.pos)); const r = v3.norm([-f0[2], 0, f0[0]]);
      const cam = { pos: v3.add(B.pos, v3.mul(r, qx)), look: v3.add(B.look, v3.add(v3.mul(r, px), [0, py, 0])), fov: B.fov + df };
      let worst = 1e9, info = [];
      for (const t of ts) { window.CAM_OVERRIDE = null; renderAt(t); const H = window.__head; window.CAM_OVERRIDE = cam; renderAt(t);
        const body = [H[0], H[1] - 0.75, H[2]];
        const pts = []; for (const [C, R] of [[H, 0.55], [body, 0.5]]) for (let a = 0; a < 16; a++) { const an = a / 16 * 2 * Math.PI; for (const v of [[Math.cos(an) * R, Math.sin(an) * R, 0], [Math.cos(an) * R, 0, Math.sin(an) * R]]) pts.push(proj(v3.add(C, v))); }
        const hx = pts.filter(q => q[1] < 960).map(q => q[0]);
        const hl = Math.min(...hx), hr = Math.max(...hx);
        const bx = []; for (const a of [-1, 1]) for (const c of [-1, 1]) bx.push(proj(v3.add(BTN, v3.add(v3.mul(TW, 0.34 * a), [0, 0.34 * c, 0]))));
        const br = Math.max(...bx.map(q => q[0])), bl = Math.min(...bx.map(q => q[0])), bt = Math.min(...bx.map(q=>q[1])), bb = Math.max(...bx.map(q=>q[1]));
        const ht = proj(v3.add(H, [0, 0.55, 0]))[1];
        let m = Math.min(hl - 55, 470 - br, bl - hr - 8, bt - 340, 900 - bb, ht - 300);
        worst = Math.min(worst, m); info.push([t, Math.round(hl), Math.round(hr), Math.round(bl), Math.round(br), Math.round(bt), Math.round(bb), Math.round(ht)]); }
      out.push({ qx, df, px, py, worst: Math.round(worst), size: Math.round(info[0][2] - info[0][1]), info });
    }
    window.CAM_OVERRIDE = null; out.sort((a, b) => (b.worst >= 0) - (a.worst >= 0) || (b.worst >= 0 ? b.size - a.size : b.worst - a.worst)); return out.slice(0, 4);
  }, [process.argv[3], process.argv[4].split(',').map(Number)]);
  for (const r of res) console.log(JSON.stringify(r)); await b.close(); })();
