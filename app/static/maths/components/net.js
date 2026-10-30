/* net — draws the 2-D net of a 3-D solid; pupil types an answer.
 * value = trimmed string from the typed input.
 * spec: { solid: "cube"|"cuboid"|"square_pyramid"|"triangular_prism"|"cylinder"|"cone" }
 * The solid's name is never written on screen (that is usually the question).
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  const BG = '#0b0f14', BORD = '#30363d', INK = '#e6edf3';
  const ACC = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';
  const FILL = 'rgba(79,141,247,0.11)';

  function mk(t, a) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    return e;
  }
  function pts(list) { return list.map(p => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join(' '); }

  function poly(list) {
    return mk('polygon', {
      points: pts(list), fill: FILL, stroke: ACC,
      'stroke-width': 2.5, 'stroke-linejoin': 'round', 'stroke-linecap': 'round'
    });
  }
  function rect(x, y, w, h) { return poly([[x, y], [x + w, y], [x + w, y + h], [x, y + h]]); }
  function circ(cx, cy, r) {
    return mk('circle', { cx: cx, cy: cy, r: r, fill: FILL, stroke: ACC, 'stroke-width': 2.5 });
  }

  // ---------------- net builders: each returns { els, bbox:[x0,y0,x1,y1] } ----------------

  function netCube() {
    const u = 62, els = [];
    // 4 squares in a row (y = u), plus one above and one below the 2nd square
    for (let i = 0; i < 4; i++) els.push(rect(i * u, u, u, u));
    els.push(rect(u, 0, u, u));
    els.push(rect(u, 2 * u, u, u));
    return { els, bbox: [0, 0, 4 * u, 3 * u] };
  }

  function netCuboid() {
    // row of 4 side faces (height h): widths w, d, w, d ; top+bottom (w x d) on the 2nd…
    // attach the w x d faces above/below a face of width w so opposite faces match.
    const w = 84, d = 52, h = 74, els = [];
    const xs = [0, w, w + d, 2 * w + d];        // widths w, d, w, d
    const ws = [w, d, w, d];
    for (let i = 0; i < 4; i++) els.push(rect(xs[i], d, ws[i], h));
    els.push(rect(0, 0, w, d));                 // top   (w x d), above the 1st (width w) face
    els.push(rect(0, d + h, w, d));             // bottom(w x d), below the same face
    return { els, bbox: [0, 0, 2 * w + 2 * d, h + 2 * d] };
  }

  function netSquarePyramid() {
    const s = 96, t = 66, els = [];
    const x0 = t, y0 = t;                       // central square top-left
    els.push(rect(x0, y0, s, s));
    const cx = x0 + s / 2, cy = y0 + s / 2;
    els.push(poly([[x0, y0], [x0 + s, y0], [cx, y0 - t]]));               // up
    els.push(poly([[x0 + s, y0], [x0 + s, y0 + s], [x0 + s + t, cy]]));   // right
    els.push(poly([[x0, y0 + s], [x0 + s, y0 + s], [cx, y0 + s + t]]));   // down
    els.push(poly([[x0, y0], [x0, y0 + s], [x0 - t, cy]]));               // left
    return { els, bbox: [0, 0, s + 2 * t, s + 2 * t] };
  }

  function netTriangularPrism() {
    const b = 68, h = 108, els = [];
    const th = Math.sqrt(3) / 2 * b;            // equilateral triangle height
    for (let i = 0; i < 3; i++) els.push(rect(i * b, th, b, h));
    // triangles above and below the MIDDLE rectangle
    els.push(poly([[b, th], [2 * b, th], [1.5 * b, 0]]));
    els.push(poly([[b, th + h], [2 * b, th + h], [1.5 * b, th + h + th]]));
    return { els, bbox: [0, 0, 3 * b, 2 * th + h] };
  }

  function netCylinder() {
    const r = 36, h = 100, els = [];
    const w = 2 * Math.PI * r;                  // circumference = rectangle width
    const y0 = 2 * r;
    els.push(rect(0, y0, w, h));
    els.push(circ(w / 2, y0 - r, r));           // top circle, tangent to top edge
    els.push(circ(w / 2, y0 + h + r, r));       // bottom circle, tangent to bottom edge
    return { els, bbox: [0, 0, w, h + 4 * r] };
  }

  function netCone() {
    const R = 112, r = 38, els = [];
    const th = 2 * Math.PI * r / R;             // sector angle so arc length = circumference
    const ax = 0, ay = 0;                       // apex at origin, sector opening downward
    const a1 = Math.PI / 2 - th / 2, a2 = Math.PI / 2 + th / 2;
    const p1 = [ax + R * Math.cos(a1), ay + R * Math.sin(a1)];
    const p2 = [ax + R * Math.cos(a2), ay + R * Math.sin(a2)];
    const large = th > Math.PI ? 1 : 0;
    els.push(mk('path', {
      d: `M ${ax} ${ay} L ${p1[0].toFixed(2)} ${p1[1].toFixed(2)} ` +
         `A ${R} ${R} 0 ${large} 1 ${p2[0].toFixed(2)} ${p2[1].toFixed(2)} Z`,
      fill: FILL, stroke: ACC, 'stroke-width': 2.5, 'stroke-linejoin': 'round'
    }));
    // small circle attached at the middle of the arc (tangent there)
    els.push(circ(ax, ay + R + r, r));
    const half = R * Math.sin(th / 2);
    const x0 = Math.min(-half, -r), x1 = Math.max(half, r);
    return { els, bbox: [x0, 0, x1, R + 2 * r] };
  }

  const NETS = {
    cube: netCube,
    cuboid: netCuboid,
    square_pyramid: netSquarePyramid,
    triangular_prism: netTriangularPrism,
    cylinder: netCylinder,
    cone: netCone
  };

  window.MComp["net"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      let key = String(spec.solid || 'cube').toLowerCase().trim().replace(/[\s-]+/g, '_');
      if (!NETS[key]) key = 'cube';
      const net = NETS[key]();

      const PAD = 18;
      const [x0, y0, x1, y1] = net.bbox;
      const vw = (x1 - x0) + 2 * PAD, vh = (y1 - y0) + 2 * PAD;
      const svg = mk('svg', {
        viewBox: `${(x0 - PAD).toFixed(2)} ${(y0 - PAD).toFixed(2)} ${vw.toFixed(2)} ${vh.toFixed(2)}`,
        width: '100%', preserveAspectRatio: 'xMidYMid meet',
        style: 'max-width:360px;background:' + BG + ';border:1px solid ' + BORD +
               ';border-radius:10px;display:block;margin:0 auto'
      });
      svg.setAttribute('role', 'img');
      svg.setAttribute('aria-label', 'A net made of flat faces joined along their edges');
      const g = mk('g', {});
      net.els.forEach(e => g.appendChild(e));
      svg.appendChild(g);
      host.appendChild(svg);

      // ---- typed input ----
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px;text-align:center';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.spellcheck = false;
      input.placeholder = 'your answer';
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:220px;max-width:90%;background:' + BG +
        ';color:' + INK + ';border:2px solid ' + BORD + ';border-radius:8px;text-align:center;outline:none';
      input.addEventListener('focus', () => { input.style.borderColor = ACC; });
      input.addEventListener('blur', () => { input.style.borderColor = BORD; });
      input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); } });
      wrap.appendChild(input);
      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => {
        const ok = !!(res && res.correct);
        input.style.borderColor = ok ? GOOD : BAD;
        g.querySelectorAll('polygon,path,circle').forEach(e => e.setAttribute('stroke', ok ? GOOD : BAD));
      };
    }
  };
})();
