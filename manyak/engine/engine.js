// 만약에 3D mini engine (WebGL1, no dependencies)
// Usage: const E = MiniEngine(canvas); E.begin(cam); E.draw(mesh, matrix, opts); E.end();
(function (global) {
  'use strict';
  // ---------- math (column-major 4x4) ----------
  const M4 = {
    I() { const m = new Float32Array(16); m[0] = m[5] = m[10] = m[15] = 1; return m; },
    mul(a, b) {
      const o = new Float32Array(16);
      for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) {
        let s = 0; for (let k = 0; k < 4; k++) s += a[k * 4 + r] * b[c * 4 + k];
        o[c * 4 + r] = s;
      }
      return o;
    },
    T(x, y, z) { const m = M4.I(); m[12] = x; m[13] = y; m[14] = z; return m; },
    S(x, y, z) { const m = M4.I(); m[0] = x; m[5] = (y === undefined ? x : y); m[10] = (z === undefined ? x : z); return m; },
    RX(a) { const m = M4.I(), c = Math.cos(a), s = Math.sin(a); m[5] = c; m[6] = s; m[9] = -s; m[10] = c; return m; },
    RY(a) { const m = M4.I(), c = Math.cos(a), s = Math.sin(a); m[0] = c; m[2] = -s; m[8] = s; m[10] = c; return m; },
    RZ(a) { const m = M4.I(), c = Math.cos(a), s = Math.sin(a); m[0] = c; m[1] = s; m[4] = -s; m[5] = c; return m; },
    persp(fovy, asp, n, f) {
      const t = 1 / Math.tan(fovy / 2), m = new Float32Array(16);
      m[0] = t / asp; m[5] = t; m[10] = (f + n) / (n - f); m[11] = -1; m[14] = 2 * f * n / (n - f); return m;
    },
    lookAt(e, c, u) {
      let zx = e[0] - c[0], zy = e[1] - c[1], zz = e[2] - c[2];
      let l = Math.hypot(zx, zy, zz); zx /= l; zy /= l; zz /= l;
      let xx = u[1] * zz - u[2] * zy, xy = u[2] * zx - u[0] * zz, xz = u[0] * zy - u[1] * zx;
      l = Math.hypot(xx, xy, xz); xx /= l; xy /= l; xz /= l;
      const yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
      const m = M4.I();
      m[0] = xx; m[4] = xy; m[8] = xz; m[1] = yx; m[5] = yy; m[9] = yz; m[2] = zx; m[6] = zy; m[10] = zz;
      m[12] = -(xx * e[0] + xy * e[1] + xz * e[2]);
      m[13] = -(yx * e[0] + yy * e[1] + yz * e[2]);
      m[14] = -(zx * e[0] + zy * e[1] + zz * e[2]);
      return m;
    },
    // chain helper: M4.chain(T(...), RY(...), S(...))
    chain(...ms) { let o = ms[0]; for (let i = 1; i < ms.length; i++) o = M4.mul(o, ms[i]); return o; },
    normal3(m) {
      const a = m[0], b = m[4], c = m[8], d = m[1], e = m[5], f = m[9], g = m[2], h = m[6], i = m[10];
      const A = e * i - f * h, B = -(d * i - f * g), C = d * h - e * g;
      const D = -(b * i - c * h), E = a * i - c * g, F = -(a * h - b * g);
      const G = b * f - c * e, H = -(a * f - c * d), I = a * e - b * d;
      let det = a * A + b * B + c * C; if (Math.abs(det) < 1e-12) det = 1e-12;
      // inverse transpose = cofactor / det, column-major
      return new Float32Array([A / det, B / det, C / det, D / det, E / det, F / det, G / det, H / det, I / det]);
    },
    apply(m, p) {
      return [m[0] * p[0] + m[4] * p[1] + m[8] * p[2] + m[12], m[1] * p[0] + m[5] * p[1] + m[9] * p[2] + m[13], m[2] * p[0] + m[6] * p[1] + m[10] * p[2] + m[14]];
    }
  };

  // ---------- helpers ----------
  function hex(h) { const n = parseInt(h.replace('#', ''), 16); return [(n >> 16 & 255) / 255, (n >> 8 & 255) / 255, (n & 255) / 255]; }
  function rng(seed) { let s = seed >>> 0 || 1; return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; }; }
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, t) => a + (b - a) * t;
  const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
  const easeOutBack = (t) => { t = clamp(t, 0, 1); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };

  // ---------- mesh generators (non-indexed) ----------
  function sphereGeo(lat, lon, thetaMax) {
    thetaMax = thetaMax || Math.PI;
    const P = [], N = [], U = [];
    const pt = (i, j) => {
      const th = i / lat * thetaMax, ph = j / lon * Math.PI * 2;
      const x = Math.sin(th) * Math.sin(ph), y = Math.cos(th), z = Math.sin(th) * Math.cos(ph);
      return [x * 0.5, y * 0.5, z * 0.5, x, y, z, j / lon, 1 - i / lat];
    };
    for (let i = 0; i < lat; i++) for (let j = 0; j < lon; j++) {
      const a = pt(i, j), b = pt(i + 1, j), c = pt(i + 1, j + 1), d = pt(i, j + 1);
      for (const v of [a, b, c, a, c, d]) { P.push(v[0], v[1], v[2]); N.push(v[3], v[4], v[5]); U.push(v[6], v[7]); }
    }
    return { P, N, U };
  }
  function pushFlatTri(G, a, b, c, ua, ub, uc) {
    const ux = b[0] - a[0], uy = b[1] - a[1], uz = b[2] - a[2], vx = c[0] - a[0], vy = c[1] - a[1], vz = c[2] - a[2];
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx; const l = Math.hypot(nx, ny, nz) || 1; nx /= l; ny /= l; nz /= l;
    for (const p of [a, b, c]) { G.P.push(p[0], p[1], p[2]); G.N.push(nx, ny, nz); }
    G.U.push(...(ua || [0, 0]), ...(ub || [1, 0]), ...(uc || [1, 1]));
  }
  function boxGeo() {
    const G = { P: [], N: [], U: [] };
    const f = (a, b, c, d) => { pushFlatTri(G, a, b, c, [0, 0], [1, 0], [1, 1]); pushFlatTri(G, a, c, d, [0, 0], [1, 1], [0, 1]); };
    const h = 0.5, v = (x, y, z) => [x * h, y * h, z * h];
    f(v(-1, -1, 1), v(1, -1, 1), v(1, 1, 1), v(-1, 1, 1));
    f(v(1, -1, -1), v(-1, -1, -1), v(-1, 1, -1), v(1, 1, -1));
    f(v(1, -1, 1), v(1, -1, -1), v(1, 1, -1), v(1, 1, 1));
    f(v(-1, -1, -1), v(-1, -1, 1), v(-1, 1, 1), v(-1, 1, -1));
    f(v(-1, 1, 1), v(1, 1, 1), v(1, 1, -1), v(-1, 1, -1));
    f(v(-1, -1, -1), v(1, -1, -1), v(1, -1, 1), v(-1, -1, 1));
    return G;
  }
  // cylinder along y, height 1 (-0.5..0.5); rTop/rBot radius; smooth sides
  function cylGeo(seg, rTop, rBot, caps, flat, noise) {
    const G = { P: [], N: [], U: [] };
    const R = rng(77);
    const jit = [];
    for (let j = 0; j <= seg; j++) jit.push(j === seg ? jit[0] : 1 + (noise ? (R() - 0.5) * noise : 0));
    const slope = (rBot - rTop);
    for (let j = 0; j < seg; j++) {
      const a0 = j / seg * Math.PI * 2, a1 = (j + 1) / seg * Math.PI * 2;
      const p = (a, r, y, k) => [Math.sin(a) * r * jit[k], y, Math.cos(a) * r * jit[k]];
      const b0 = p(a0, rBot, -0.5, j), b1 = p(a1, rBot, -0.5, j + 1), t0 = p(a0, rTop, 0.5, j), t1 = p(a1, rTop, 0.5, j + 1);
      if (flat) {
        pushFlatTri(G, b0, b1, t1, [j / seg, 0], [(j + 1) / seg, 0], [(j + 1) / seg, 1]);
        if (rTop > 0.0001) pushFlatTri(G, b0, t1, t0, [j / seg, 0], [(j + 1) / seg, 1], [j / seg, 1]);
      } else {
        const n = (a) => { const nx = Math.sin(a), nz = Math.cos(a), ny = slope; const l = Math.hypot(nx, ny, nz); return [nx / l, ny / l, nz / l]; };
        const n0 = n(a0), n1 = n(a1);
        const tri = [[b0, n0, [j / seg, 0]], [b1, n1, [(j + 1) / seg, 0]], [t1, n1, [(j + 1) / seg, 1]], [b0, n0, [j / seg, 0]], [t1, n1, [(j + 1) / seg, 1]], [t0, n0, [j / seg, 1]]];
        for (const [pp, nn, uu] of tri) { G.P.push(...pp); G.N.push(...nn); G.U.push(...uu); }
      }
      if (caps) {
        if (rTop > 0.0001) { const c = [0, 0.5, 0]; for (const [pp, uu] of [[c, [0.5, 0.5]], [t0, [0, 0]], [t1, [1, 0]]]) { G.P.push(...pp); G.N.push(0, 1, 0); G.U.push(...uu); } }
        const c = [0, -0.5, 0]; for (const [pp, uu] of [[c, [0.5, 0.5]], [b1, [1, 0]], [b0, [0, 0]]]) { G.P.push(...pp); G.N.push(0, -1, 0); G.U.push(...uu); }
      }
    }
    return G;
  }
  // disc in XY plane facing +z, radius 0.5
  function discGeo(seg) {
    const G = { P: [], N: [], U: [] };
    for (let j = 0; j < seg; j++) {
      const a0 = j / seg * Math.PI * 2, a1 = (j + 1) / seg * Math.PI * 2;
      const pts = [[0, 0], [Math.cos(a0) * 0.5, Math.sin(a0) * 0.5], [Math.cos(a1) * 0.5, Math.sin(a1) * 0.5]];
      for (const p of pts) { G.P.push(p[0], p[1], 0); G.N.push(0, 0, 1); G.U.push(p[0] + 0.5, p[1] + 0.5); }
    }
    return G;
  }
  function quadGeo() {
    const G = { P: [], N: [], U: [] };
    const v = [[-0.5, -0.5, 0, 0], [0.5, -0.5, 1, 0], [0.5, 0.5, 1, 1], [-0.5, -0.5, 0, 0], [0.5, 0.5, 1, 1], [-0.5, 0.5, 0, 1]];
    for (const p of v) { G.P.push(p[0], p[1], 0); G.N.push(0, 0, 1); G.U.push(p[2], p[3]); }
    return G;
  }
  // triangular prism (triangle kimbap shape) axis z, slightly rounded by bevel
  function prismGeo() {
    const G = { P: [], N: [], U: [] };
    const tri = [[0, 0.5], [-0.5, -0.36], [0.5, -0.36]];
    const d = 0.19;
    const F = tri.map(p => [p[0], p[1], d]), B = tri.map(p => [p[0], p[1], -d]);
    pushFlatTri(G, F[0], F[1], F[2], [0.5, 1], [0, 0], [1, 0]);
    pushFlatTri(G, B[0], B[2], B[1], [0.5, 1], [1, 0], [0, 0]);
    for (let i = 0; i < 3; i++) {
      const j = (i + 1) % 3;
      pushFlatTri(G, F[i], B[i], B[j]); pushFlatTri(G, F[i], B[j], F[j]);
    }
    return G;
  }

  function MiniEngine(canvas) {
    const gl = canvas.getContext('webgl', { antialias: true, preserveDrawingBuffer: true, alpha: false });
    if (!gl) throw new Error('no webgl');
    gl.getExtension('OES_standard_derivatives');
    const VS = `attribute vec3 aP;attribute vec3 aN;attribute vec2 aU;uniform mat4 uM;uniform mat4 uVP;uniform mat3 uNM;
      varying vec3 vN;varying vec3 vW;varying vec2 vU;
      void main(){vec4 w=uM*vec4(aP,1.0);vW=w.xyz;vN=uNM*aN;vU=aU;gl_Position=uVP*w;}`;
    const FS = `precision highp float;varying vec3 vN;varying vec3 vW;varying vec2 vU;
      uniform vec3 uC;uniform vec3 uCam;uniform vec3 uL;uniform vec3 uFog;uniform vec3 uSky;uniform vec3 uGnd;
      uniform float uFN;uniform float uFF;uniform float uA;uniform float uEm;uniform float uSp;uniform float uTx;uniform sampler2D uT;uniform vec2 uTR;
      void main(){vec3 N=normalize(vN);if(!gl_FrontFacing)N=-N;vec3 base=uC;float a=uA;
        if(uTx>0.5){vec4 t=texture2D(uT,vU*uTR);base*=t.rgb;a*=t.a;}
        if(a<0.01)discard;
        vec3 V=normalize(uCam-vW);vec3 L=normalize(uL);float ndl=max(dot(N,L),0.0);
        vec3 amb=mix(uGnd,uSky,N.y*0.5+0.5);vec3 H=normalize(L+V);
        float sp=pow(max(dot(N,H),0.0),48.0)*uSp;float rim=pow(1.0-max(dot(N,V),0.0),3.0)*0.32;
        vec3 c=base*(amb*0.62+ndl*vec3(1.0,0.97,0.92)*0.72)+vec3(sp)+rim*vec3(1.0,0.96,0.92);
        c=mix(c,base,uEm);
        float d=length(uCam-vW);float f=clamp((d-uFN)/(uFF-uFN),0.0,1.0);f=f*f;
        c=mix(c,uFog,f);gl_FragColor=vec4(c,a);}`;
    const BVS = `attribute vec2 aP;varying float vY;void main(){vY=aP.y*0.5+0.5;gl_Position=vec4(aP,0.999,1.0);}`;
    const BFS = `precision mediump float;varying float vY;uniform vec3 uTop;uniform vec3 uBot;void main(){gl_FragColor=vec4(mix(uBot,uTop,smoothstep(0.0,1.0,vY)),1.0);}`;
    function prog(vs, fs) {
      const p = gl.createProgram();
      for (const [t, s] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) {
        const sh = gl.createShader(t); gl.shaderSource(sh, s); gl.compileShader(sh);
        if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(sh));
        gl.attachShader(p, sh);
      }
      gl.linkProgram(p); if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
      const u = {}, n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS);
      for (let i = 0; i < n; i++) { const info = gl.getActiveUniform(p, i); u[info.name] = gl.getUniformLocation(p, info.name); }
      return { p, u, aP: gl.getAttribLocation(p, 'aP'), aN: gl.getAttribLocation(p, 'aN'), aU: gl.getAttribLocation(p, 'aU') };
    }
    const MP = prog(VS, FS), BP = prog(BVS, BFS);
    const bgBuf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, bgBuf); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);

    function mesh(G) {
      const mk = (a) => { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(a), gl.STATIC_DRAW); return b; };
      return { p: mk(G.P), n: mk(G.N), u: mk(G.U), count: G.P.length / 3 };
    }
    const meshes = {
      sphere: mesh(sphereGeo(16, 24)),
      hemi: mesh(sphereGeo(8, 24, Math.PI / 2)),
      box: mesh(boxGeo()),
      cyl: mesh(cylGeo(18, 0.5, 0.5, true)),
      cone: mesh(cylGeo(18, 0.0, 0.5, true)),
      disc: mesh(discGeo(28)),
      quad: mesh(quadGeo()),
      prism: mesh(prismGeo()),
      mountain: mesh(cylGeo(28, 0.0, 0.5, false, true, 0.18)),
    };
    function texture(drawFn, w, h, repeat) {
      const c = document.createElement('canvas'); c.width = w; c.height = h; const ctx = c.getContext('2d'); drawFn(ctx, w, h);
      const t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, c);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      const wrap = repeat ? gl.REPEAT : gl.CLAMP_TO_EDGE;
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, wrap); gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, wrap);
      return t;
    }
    let list = [], cam = null, env = null;
    function begin(c, e) { list = []; cam = c; env = e; }
    function draw(m, mat, color, o) {
      o = o || {};
      list.push({ m, mat, color: typeof color === 'string' ? hex(color) : color, a: o.alpha === undefined ? 1 : o.alpha, em: o.em || 0, sp: o.spec === undefined ? 0.35 : o.spec, tex: o.tex || null, tr: o.tr || [1, 1], tp: (o.alpha !== undefined && o.alpha < 1) || o.transparent });
    }
    function end() {
      const W = canvas.width, H = canvas.height;
      gl.viewport(0, 0, W, H);
      gl.clearColor(0, 0, 0, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      // background gradient
      gl.disable(gl.DEPTH_TEST); gl.useProgram(BP.p);
      gl.bindBuffer(gl.ARRAY_BUFFER, bgBuf); gl.enableVertexAttribArray(BP.aP); gl.vertexAttribPointer(BP.aP, 2, gl.FLOAT, false, 0, 0);
      gl.uniform3fv(BP.u.uTop, env.skyTop); gl.uniform3fv(BP.u.uBot, env.skyBot); gl.drawArrays(gl.TRIANGLES, 0, 3);
      gl.disableVertexAttribArray(BP.aP);
      gl.enable(gl.DEPTH_TEST); gl.depthFunc(gl.LEQUAL);
      gl.useProgram(MP.p);
      const proj = M4.persp(cam.fov * Math.PI / 180, W / H, cam.near || 0.05, cam.far || 3000);
      const view = M4.lookAt(cam.pos, cam.look, cam.up || [0, 1, 0]);
      const vp = M4.mul(proj, view);
      const U = MP.u;
      gl.uniformMatrix4fv(U.uVP, false, vp); gl.uniform3fv(U.uCam, cam.pos); gl.uniform3fv(U.uL, env.light);
      gl.uniform3fv(U.uFog, env.fog); gl.uniform3fv(U.uSky, env.amb); gl.uniform3fv(U.uGnd, env.gnd);
      gl.uniform1f(U.uFN, env.fogNear); gl.uniform1f(U.uFF, env.fogFar); gl.uniform1i(U.uT, 0);
      for (const a of [MP.aP, MP.aN, MP.aU]) gl.enableVertexAttribArray(a);
      const op = list.filter(d => !d.tp), tr = list.filter(d => d.tp);
      const dist = (d) => { const p = [d.mat[12], d.mat[13], d.mat[14]]; return Math.hypot(p[0] - cam.pos[0], p[1] - cam.pos[1], p[2] - cam.pos[2]); };
      tr.sort((a, b) => dist(b) - dist(a));
      let lastMesh = null;
      const run = (d) => {
        if (d.m !== lastMesh) {
          gl.bindBuffer(gl.ARRAY_BUFFER, d.m.p); gl.vertexAttribPointer(MP.aP, 3, gl.FLOAT, false, 0, 0);
          gl.bindBuffer(gl.ARRAY_BUFFER, d.m.n); gl.vertexAttribPointer(MP.aN, 3, gl.FLOAT, false, 0, 0);
          gl.bindBuffer(gl.ARRAY_BUFFER, d.m.u); gl.vertexAttribPointer(MP.aU, 2, gl.FLOAT, false, 0, 0);
          lastMesh = d.m;
        }
        gl.uniformMatrix4fv(U.uM, false, d.mat); gl.uniformMatrix3fv(U.uNM, false, M4.normal3(d.mat));
        gl.uniform3fv(U.uC, d.color); gl.uniform1f(U.uA, d.a); gl.uniform1f(U.uEm, d.em); gl.uniform1f(U.uSp, d.sp);
        if (d.tex) { gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, d.tex); gl.uniform1f(U.uTx, 1); gl.uniform2fv(U.uTR, d.tr); } else gl.uniform1f(U.uTx, 0);
        gl.drawArrays(gl.TRIANGLES, 0, d.m.count);
      };
      gl.disable(gl.BLEND); gl.depthMask(true);
      op.forEach(run);
      gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA); gl.depthMask(false);
      tr.forEach(run);
      gl.depthMask(true); gl.disable(gl.BLEND);
      return vp;
    }
    return { gl, meshes, texture, begin, draw, end, M4, hex };
  }

  // ---------- spring camera (deterministic) ----------
  // shots: [{t0, target(t) -> {pos,look,fov}, w (omega)}]; returns camera at time t
  function springCamera(shots, t, extraShake) {
    let si = 0; for (let i = 0; i < shots.length; i++) if (t >= shots[i].t0) si = i;
    const S = shots[si], w = S.w || 6, dt = 1 / 120;
    const tgt0 = S.target(S.t0);
    let pos = tgt0.pos.slice(), look = tgt0.look.slice(), fov = tgt0.fov || 40, vp = [0, 0, 0], vl = [0, 0, 0], vf = 0;
    if (S.snap) { const c = S.target(t); return Object.assign({}, c, { fov: c.fov || 40 }); }
    for (let tt = S.t0; tt < t; tt += dt) {
      const g = S.target(Math.min(tt + dt, t));
      for (let k = 0; k < 3; k++) {
        vp[k] += (w * w * (g.pos[k] - pos[k]) - 2 * w * vp[k]) * dt; pos[k] += vp[k] * dt;
        vl[k] += (w * w * (g.look[k] - look[k]) - 2 * w * vl[k]) * dt; look[k] += vl[k] * dt;
      }
      const gf = g.fov || 40; vf += (w * w * (gf - fov) - 2 * w * vf) * dt; fov += vf * dt;
    }
    if (extraShake) { pos = pos.map((v, k) => v + extraShake[k]); look = look.map((v, k) => v + extraShake[k] * 0.6); }
    return { pos, look, fov };
  }

  // ---------- character (series standard) ----------
  // o: {sit 0..1 (legs forward, put base at seat height - 0.46),
  //     shirt, hair:'bob'|'short', hairColor, pants, surprise 0..1, mouth 0..1, eyeDots 0..1, headYaw, headPitch, bodyYaw, blink 0..1, hood, vest, armL, armR (angles), talk}
  function drawCharacter(E, base, o) {
    const { M4 } = E; const m = E.meshes; const D = (mesh, mat, c, op) => E.draw(mesh, mat, c, op);
    const skin = '#f3cdb8', pants = o.pants || '#26262e';
    const B = M4.mul(base, M4.RY(o.bodyYaw || 0));
    const sp = { spec: 0.45 };
    // legs + shoes
    for (const s of [-1, 1]) {
      const lk = (o.legSwing || 0) * s - (o.sit || 0) * Math.PI / 2;
      const L = M4.chain(B, M4.T(0.12 * s, 0.46, 0), M4.RX(lk));
      D(m.cyl, M4.chain(L, M4.T(0, -0.22, 0), M4.S(0.17, 0.46, 0.17)), pants, sp);
      D(m.sphere, M4.chain(L, M4.T(0, -0.44, 0.05), M4.S(0.2, 0.12, 0.28)), '#3a3a44', sp);
    }
    // body
    const shirt = o.shirt || '#ff6b81';
    D(m.sphere, M4.chain(B, M4.T(0, 0.8, 0), M4.S(0.64, 0.74, 0.54)), shirt, sp);
    if (o.vest) {
      D(m.sphere, M4.chain(B, M4.T(0, 0.8, 0.012), M4.S(0.665, 0.72, 0.56)), o.vest, sp);
      D(m.sphere, M4.chain(B, M4.T(0, 0.86, 0.2), M4.S(0.2, 0.5, 0.18)), '#ffffff', sp);
      D(m.box, M4.chain(B, M4.T(0.16, 0.95, 0.265), M4.RX(-0.3), M4.S(0.12, 0.06, 0.02)), '#ffffff', { spec: 0.1 });
    }
    if (o.hood) {
      D(m.sphere, M4.chain(B, M4.T(0, 1.1, -0.16), M4.S(0.5, 0.22, 0.3)), shirt, sp);
      // pocket
      D(m.sphere, M4.chain(B, M4.T(0, 0.66, 0.235), M4.S(0.34, 0.16, 0.08)), '#ef5a72', sp);
    }
    // arms
    for (const s of [-1, 1]) {
      const ang = s < 0 ? (o.armL || [0.25, 0]) : (o.armR || [0.25, 0]);
      const A = M4.chain(B, M4.T(0.3 * s, 1.0, 0), M4.RZ(ang[0] * s), M4.RX(-ang[1]));
      D(m.cyl, M4.chain(A, M4.T(0, -0.2, 0), M4.S(0.14, 0.42, 0.14)), shirt, sp);
      D(m.sphere, M4.chain(A, M4.T(0, -0.44, 0), M4.S(0.17)), skin, sp);
    }
    // head
    const Hd = M4.chain(B, M4.T(0, 1.12, 0), M4.RY(o.headYaw || 0), M4.RX(o.headPitch || 0), M4.RZ(o.headRoll || 0), M4.T(0, 0.36, 0));
    const hr = 0.88; // diameter
    D(m.sphere, M4.mul(Hd, M4.S(hr)), skin, { spec: 0.25 });
    const hairC = o.hairColor || '#1d1d22';
    if (o.hair === 'short') {
      D(m.hemi, M4.chain(Hd, M4.T(0, 0.02, -0.02), M4.RX(-0.25), M4.S(0.93, 0.95, 0.93)), hairC, { spec: 0.5 });
    } else {
      D(m.hemi, M4.chain(Hd, M4.T(0, 0.0, 0), M4.RX(-0.12), M4.S(0.95)), hairC, { spec: 0.55 });
      D(m.sphere, M4.chain(Hd, M4.T(0, -0.08, -0.09), M4.S(0.93, 0.82, 0.84)), hairC, { spec: 0.55 });
    }
    const sur = o.surprise || 0, dots = o.eyeDots || 0, blink = o.blink || 0;
    const eyeS = (1 + sur * 0.3) * (1 - dots * 0.62);
    for (const s of [-1, 1]) {
      const ey = M4.chain(Hd, M4.T(0.15 * s, -0.09, 0.392));
      D(m.sphere, M4.mul(ey, M4.S(0.12 * eyeS, 0.17 * eyeS * (1 - blink * 0.9), 0.07)), '#16161b', { spec: 0.9 });
      if (dots < 0.5 && blink < 0.5) D(m.sphere, M4.chain(ey, M4.T(0.025 * eyeS, 0.04 * eyeS, 0.03), M4.S(0.045 * eyeS)), '#ffffff', { em: 0.8 });
      D(m.sphere, M4.chain(Hd, M4.T(0.25 * s, -0.2, 0.3), M4.S(0.13, 0.07, 0.04)), '#ff98a8', { em: 0.3, spec: 0.1 });
      const br = M4.chain(Hd, M4.T(0.15 * s, 0.035 + sur * 0.05, 0.405), M4.RZ((o.browTilt || 0) * s - sur * 0.18 * s), M4.S(0.12, 0.026, 0.03));
      D(m.box, br, hairC, { spec: 0.1 });
    }
    D(m.sphere, M4.chain(Hd, M4.T(0, -0.17, 0.41), M4.S(0.065, 0.055, 0.05)), '#e9b39c', { spec: 0.3 });
    const mo = clamp(o.mouth || 0, 0, 1.2);
    D(m.sphere, M4.chain(Hd, M4.T(0, -0.285 - mo * 0.02, 0.33), M4.S(0.11 + mo * 0.05, 0.035 + mo * 0.12, 0.05)), '#7a2230', { spec: 0.2 });
    return Hd;
  }


  // ---------- basis matrix: up = local +y, fwd = local +z (character faces +z) ----------
  function basis(pos, up, fwd, s) {
    const n = (v) => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l]; };
    const Y = n(up); const d = fwd[0] * Y[0] + fwd[1] * Y[1] + fwd[2] * Y[2];
    let Z = n([fwd[0] - Y[0] * d, fwd[1] - Y[1] * d, fwd[2] - Y[2] * d]);
    const X = [Y[1] * Z[2] - Y[2] * Z[1], Y[2] * Z[0] - Y[0] * Z[2], Y[0] * Z[1] - Y[1] * Z[0]];
    s = s || 1; const m = M4.I();
    m[0] = X[0] * s; m[1] = X[1] * s; m[2] = X[2] * s; m[4] = Y[0] * s; m[5] = Y[1] * s; m[6] = Y[2] * s;
    m[8] = Z[0] * s; m[9] = Z[1] * s; m[10] = Z[2] * s; m[12] = pos[0]; m[13] = pos[1]; m[14] = pos[2];
    return m;
  }
  // ---------- crowd mini person (5 draws; height ~1, faces +z; o.pitch looks up) ----------
  function drawMini(E, base, o) {
    const { M4 } = E; const m = E.meshes; o = o || {};
    E.draw(m.sphere, M4.chain(base, M4.T(0, 0.33, 0), M4.S(0.42, 0.52, 0.36)), o.shirt || '#4f8cff', { spec: 0.4 });
    const Hd = M4.chain(base, M4.T(0, 0.72, 0), M4.RY(o.yaw || 0), M4.RX(-(o.pitch || 0)), M4.T(0, 0.12, 0));
    E.draw(m.sphere, M4.mul(Hd, M4.S(0.5)), o.skin || '#f3cdb8', { spec: 0.25 });
    E.draw(m.hemi, M4.chain(Hd, M4.RX(-0.25), M4.S(0.53)), o.hair || '#1d1d22', { spec: 0.5 });
    for (const s of [-1, 1]) E.draw(m.sphere, M4.chain(Hd, M4.T(0.09 * s, -0.03, 0.225), M4.S(0.075, 0.11, 0.05)), '#111116', { spec: 0.9 });
  }
  global.MiniEngine = MiniEngine;
  global.ME = { M4, hex, rng, clamp, lerp, smooth, easeOutBack, springCamera, drawCharacter, drawMini, basis };
})(window);
