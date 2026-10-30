/* shape — read a 2-D polygon or a 3-D solid diagram and type an answer.
 * value = trimmed string from the typed input.
 * spec: { kind:"2d"|"3d", name, ask:"sides"|"vertices"|"faces"|"edges"|"name"|"lines_of_symmetry", marks }
 *   2d names: triangle, square, rectangle, pentagon, hexagon, heptagon, octagon
 *   3d names: cube, cuboid, square-based pyramid, triangular prism
 * The shape's name is never written on screen.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  const INK = '#e6edf3', LINE = '#c9d1d9', ACC = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }
  function pts(list) { return list.map(p => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join(' '); }

  const SIDES = { triangle: 3, square: 4, rectangle: 4, pentagon: 5, hexagon: 6, heptagon: 7, octagon: 8 };

  window.MComp["shape"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const kind = (spec.kind || '2d').toLowerCase();
      const name = String(spec.name || '').toLowerCase().trim();
      const ask = String(spec.ask || 'sides').toLowerCase();
      const marks = String(spec.marks || '');

      const W = 360, H = 270;
      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: 'max-width:360px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;display:block;margin:0 auto'
      });

      // group drawn after the shape, used only for post-feedback symmetry hints
      const symGroup = mk('g', { opacity: 0 });

      if (kind === '3d') draw3d(svg, name);
      else draw2d(svg, name, marks, symGroup);

      svg.appendChild(symGroup);
      host.appendChild(svg);

      // ---- typed input ----
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px;text-align:center';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.spellcheck = false;
      input.setAttribute('aria-label', 'Your answer');
      if (ask === 'name') { input.placeholder = 'shape name'; }
      else { input.inputMode = 'numeric'; input.placeholder = 'how many?'; }
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:' + (ask === 'name' ? '220px' : '160px') +
        ';max-width:90%;background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;text-align:center;outline:none';
      input.addEventListener('focus', () => { input.style.borderColor = ACC; });
      input.addEventListener('blur', () => { input.style.borderColor = '#30363d'; });
      input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); } });
      wrap.appendChild(input);
      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => {
        input.style.borderColor = res && res.correct ? GOOD : BAD;
        if (ask === 'lines_of_symmetry' && kind !== '3d') symGroup.setAttribute('opacity', 1);
      };

      // =================== 2-D ===================
      function draw2d(svg, name, marks, sym) {
        const cx = W / 2, cy = H / 2;
        let verts;

        if (name === 'rectangle') {
          const w = 230, h = 140;
          verts = [[cx - w / 2, cy - h / 2], [cx + w / 2, cy - h / 2], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]];
        } else {
          const n = SIDES[name] || 5;
          const R = 100;
          // vertex at top for odd n; flat top/bottom for even n
          const off = -Math.PI / 2 + (n % 2 === 0 ? Math.PI / n : 0);
          verts = [];
          for (let i = 0; i < n; i++) {
            const a = off + i * 2 * Math.PI / n;
            verts.push([cx + R * Math.cos(a), cy + R * Math.sin(a)]);
          }
        }

        svg.appendChild(mk('polygon', {
          points: pts(verts), fill: 'rgba(79,141,247,0.14)', stroke: ACC,
          'stroke-width': 3, 'stroke-linejoin': 'round'
        }));
        verts.forEach(p => svg.appendChild(mk('circle', { cx: p[0], cy: p[1], r: 4.5, fill: INK, stroke: '#0b0f14', 'stroke-width': 1.5 })));

        // right-angle marker in one corner (square / rectangle)
        if (marks === 'right_angle' && (name === 'square' || name === 'rectangle')) {
          const c = verts[0], a = verts[1], b = verts[3];
          const s = 18;
          const u = unit(c, a), v = unit(c, b);
          const p1 = [c[0] + u[0] * s, c[1] + u[1] * s];
          const p3 = [c[0] + v[0] * s, c[1] + v[1] * s];
          const p2 = [c[0] + (u[0] + v[0]) * s, c[1] + (u[1] + v[1]) * s];
          svg.appendChild(mk('polyline', { points: pts([p1, p2, p3]), fill: 'none', stroke: INK, 'stroke-width': 2 }));
        }

        // candidate mirror lines — hidden until feedback
        if (ask === 'lines_of_symmetry') {
          let angles;
          if (name === 'rectangle') angles = [0, Math.PI / 2];
          else {
            const n = SIDES[name] || 5;
            const off = -Math.PI / 2 + (n % 2 === 0 ? Math.PI / n : 0);
            angles = [];
            for (let k = 0; k < n; k++) angles.push(off + k * Math.PI / n);
          }
          const L = 118;
          angles.forEach(a => {
            sym.appendChild(mk('line', {
              x1: cx - L * Math.cos(a), y1: cy - L * Math.sin(a),
              x2: cx + L * Math.cos(a), y2: cy + L * Math.sin(a),
              stroke: GOOD, 'stroke-width': 1.5, 'stroke-dasharray': '5 4', opacity: 0.75
            }));
          });
        }

        function unit(from, to) {
          const dx = to[0] - from[0], dy = to[1] - from[1], m = Math.hypot(dx, dy) || 1;
          return [dx / m, dy / m];
        }
      }

      // =================== 3-D ===================
      function draw3d(svg, name) {
        const solid = [], dashed = [], vis = [], hid = [];
        const E = (a, b, hidden) => (hidden ? dashed : solid).push([a, b]);

        if (name === 'cube' || name === 'cuboid') {
          const w = name === 'cuboid' ? 190 : 150, h = name === 'cuboid' ? 105 : 150;
          const dx = 55, dy = -42;
          const x0 = (W - w - dx) / 2, y1 = (H + h - dy) / 2 - 6;
          const A = [x0, y1], B = [x0 + w, y1], C = [x0 + w, y1 - h], D = [x0, y1 - h];
          const A2 = [A[0] + dx, A[1] + dy], B2 = [B[0] + dx, B[1] + dy], C2 = [C[0] + dx, C[1] + dy], D2 = [D[0] + dx, D[1] + dy];
          // front face
          E(A, B); E(B, C); E(C, D); E(D, A);
          // back face — A2 is hidden
          E(B2, C2); E(C2, D2); E(A2, B2, true); E(A2, D2, true);
          // connectors
          E(B, B2); E(C, C2); E(D, D2); E(A, A2, true);
          vis.push(A, B, C, D, B2, C2, D2); hid.push(A2);
          face(svg, [D, C, C2, D2]);   // top
          face(svg, [B, C, C2, B2]);   // right
        } else if (name === 'square-based pyramid' || name === 'square based pyramid' || name === 'pyramid') {
          const cx = W / 2, by = 205, rx = 115, ry = 42;
          const F = [cx, by + ry], R = [cx + rx, by], K = [cx, by - ry], Lf = [cx - rx, by];
          const P = [cx, 40];
          E(F, R); E(F, Lf); E(K, R, true); E(K, Lf, true);
          E(P, F); E(P, R); E(P, Lf); E(P, K, true);
          vis.push(F, R, Lf, P); hid.push(K);
          face(svg, [P, Lf, F]); face(svg, [P, F, R]);
        } else { // triangular prism
          const dx = 62, dy = -46;
          const a = [55, 215], b = [195, 215], c = [125, 88];
          const a2 = [a[0] + dx, a[1] + dy], b2 = [b[0] + dx, b[1] + dy], c2 = [c[0] + dx, c[1] + dy];
          E(a, b); E(b, c); E(c, a);              // front triangle
          E(b2, c2); E(a2, b2, true); E(a2, c2, true); // back triangle (a2 hidden)
          E(b, b2); E(c, c2); E(a, a2, true);     // connectors
          vis.push(a, b, c, b2, c2); hid.push(a2);
          face(svg, [c, b, b2, c2]);              // slanted top-right face
        }

        solid.forEach(([p, q]) => svg.appendChild(mk('line', {
          x1: p[0], y1: p[1], x2: q[0], y2: q[1], stroke: ACC, 'stroke-width': 3, 'stroke-linecap': 'round'
        })));
        dashed.forEach(([p, q]) => svg.appendChild(mk('line', {
          x1: p[0], y1: p[1], x2: q[0], y2: q[1], stroke: '#8b949e', 'stroke-width': 2,
          'stroke-dasharray': '7 6', 'stroke-linecap': 'round'
        })));
        vis.forEach(p => svg.appendChild(mk('circle', { cx: p[0], cy: p[1], r: 4.5, fill: INK, stroke: '#0b0f14', 'stroke-width': 1.5 })));
        hid.forEach(p => svg.appendChild(mk('circle', { cx: p[0], cy: p[1], r: 4.5, fill: '#0b0f14', stroke: '#8b949e', 'stroke-width': 2 })));

        function face(svg, poly) {
          svg.appendChild(mk('polygon', { points: pts(poly), fill: 'rgba(79,141,247,0.12)', stroke: 'none' }));
        }
      }
    }
  };
})();
