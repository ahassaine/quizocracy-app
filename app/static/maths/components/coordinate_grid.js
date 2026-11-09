/* coordinate_grid — plot a lattice point on a coordinate plane.
 * value = string "(x,y)" with integer coords.
 *
 * spec (first quadrant, LEGACY — unchanged):
 *   { mode:"plot", size:8 }                      → x,y ∈ 0..8, origin bottom-left
 *
 * spec (four quadrants, NEW — opt-in):
 *   { xmin:-6, xmax:6, ymin:-6, ymax:6 }         → axes drawn through the origin
 *
 * optional extras (work in either mode):
 *   { points:  [[x,y,"A"], [x,y,"B"], ...] }     → fixed labelled reference dots
 *   { polygon: [[x,y], [x,y], ...] }             → closed outline through lattice points
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["coordinate_grid"] = {
    render(host, spec, api) {
      host.innerHTML = '';

      // ---- range -------------------------------------------------------
      // Four-quadrant mode is opt-in: it engages only when at least one of
      // xmin/xmax/ymin/ymax is supplied. Otherwise the legacy first-quadrant
      // geometry (size, gap 42, pad 34) is reproduced exactly.
      const hasRange = ['xmin', 'xmax', 'ymin', 'ymax'].some(k => spec[k] != null);
      const size = Math.max(1, spec.size ?? 8);

      let xmin, xmax, ymin, ymax, gap;
      if (!hasRange) {
        xmin = 0; xmax = size; ymin = 0; ymax = size;
        gap = 42;                                  // legacy px between lattice lines
      } else {
        xmin = Math.round(spec.xmin ?? 0);
        xmax = Math.round(spec.xmax ?? size);
        ymin = Math.round(spec.ymin ?? 0);
        ymax = Math.round(spec.ymax ?? size);
        if (xmax <= xmin) xmax = xmin + 1;
        if (ymax <= ymin) ymax = ymin + 1;
        // keep the plane legible and ≲460px wide: a 12×12 plane → gap 38
        const span = Math.max(xmax - xmin, ymax - ymin);
        gap = Math.max(16, Math.min(42, Math.floor(460 / span)));
      }

      const spanX = xmax - xmin, spanY = ymax - ymin;
      const pad = 34;
      // drawn at the card's real width: a wider grid scaled down to a phone shrinks its 12 px numbers to 7 px,
      // so on a narrow card the squares get smaller instead (the numbers thin out below when they would touch)
      const avail = Math.floor(host.getBoundingClientRect().width || 0);
      if (avail > 0) gap = Math.max(12, Math.min(gap, Math.floor((avail - pad * 2 - 2) / spanX)));
      const every = gap >= 18 ? 1 : (gap >= 10 ? 2 : 5);   // label every n-th grid line
      const plotW = spanX * gap, plotH = spanY * gap;
      const W = plotW + pad * 2, H = plotH + pad * 2;
      const ox = pad - xmin * gap;                 // pixel x of grid x=0
      const oy = H - pad + ymin * gap;             // pixel y of grid y=0
      const toPx = (gx, gy) => [ox + gx * gap, oy - gy * gap];
      const toGrid = (px, py) => {
        let gx = Math.round((px - ox) / gap);
        let gy = Math.round((oy - py) / gap);
        gx = Math.max(xmin, Math.min(xmax, gx));
        gy = Math.max(ymin, Math.min(ymax, gy));
        return [gx, gy];
      };

      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: `max-width:${W}px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;touch-action:none;cursor:crosshair` });

      // ---- gridlines (across the whole plane) --------------------------
      const [, gTop] = toPx(0, ymax); const [, gBot] = toPx(0, ymin);
      const [gLeft] = toPx(xmin, 0); const [gRight] = toPx(xmax, 0);
      for (let i = xmin; i <= xmax; i++) {
        const [vx] = toPx(i, 0);
        svg.appendChild(mk('line', { x1: vx, y1: gBot, x2: vx, y2: gTop, stroke: '#1c2531', 'stroke-width': 1 }));
      }
      for (let i = ymin; i <= ymax; i++) {
        const [, hy] = toPx(0, i);
        svg.appendChild(mk('line', { x1: gLeft, y1: hy, x2: gRight, y2: hy, stroke: '#1c2531', 'stroke-width': 1 }));
      }

      // ---- axes (through the origin) -----------------------------------
      const [axx, axy] = toPx(0, 0);
      svg.appendChild(mk('line', { x1: gLeft, y1: axy, x2: gRight, y2: axy, stroke: '#8b949e', 'stroke-width': 2 }));
      svg.appendChild(mk('line', { x1: axx, y1: gBot, x2: axx, y2: gTop, stroke: '#8b949e', 'stroke-width': 2 }));

      // ---- axis numbers -------------------------------------------------
      // Legacy first-quadrant labelling is preserved exactly: x skips 0,
      // y prints 0..size (the "0" sits at the origin).
      for (let i = xmin; i <= xmax; i++) {
        if (i === 0 || i % every) continue;
        const [px, py] = toPx(i, 0);
        const t = mk('text', { x: px, y: py + 16, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'middle' });
        t.textContent = i; svg.appendChild(t);
      }
      for (let i = ymin; i <= ymax; i++) {
        if (i === 0 && hasRange) continue;         // one "0" only, drawn below
        if (i % every) continue;
        const [px2, py2] = toPx(0, i);
        const t2 = mk('text', { x: px2 - 8, y: py2 + 4, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'end' });
        t2.textContent = i; svg.appendChild(t2);
      }
      if (hasRange) {                              // origin marker for the four-quadrant plane
        const t0 = mk('text', { x: axx - 6, y: axy + 15, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'end' });
        t0.textContent = '0'; svg.appendChild(t0);
      }

      // ---- axis labels ---------------------------------------------------
      const xl = mk('text', { x: (gLeft + gRight) / 2, y: H - 4, fill: '#e6edf3', 'font-size': 13, 'text-anchor': 'middle', 'font-weight': 700 }); xl.textContent = 'x'; svg.appendChild(xl);
      const yl = mk('text', { x: 10, y: (gBot + gTop) / 2, fill: '#e6edf3', 'font-size': 13, 'text-anchor': 'middle', 'font-weight': 700, transform: `rotate(-90 10 ${(gBot + gTop) / 2})` }); yl.textContent = 'y'; svg.appendChild(yl);

      // ---- optional polygon outline --------------------------------------
      const poly = Array.isArray(spec.polygon) ? spec.polygon.filter(p => Array.isArray(p) && p.length >= 2) : [];
      if (poly.length >= 2) {
        const pts = poly.map(p => toPx(Number(p[0]), Number(p[1])).join(',')).join(' ');
        svg.appendChild(mk('polygon', {
          points: pts, fill: '#4f8df7', 'fill-opacity': 0.10,
          stroke: '#4f8df7', 'stroke-opacity': 0.75, 'stroke-width': 1.5,
          'stroke-linejoin': 'round'
        }));
      }

      // ---- optional straight lines (stimulus only) -----------------------
      // Each line is defined by two grid points; it is drawn as an infinite
      // straight line clipped to the plotting-area bounding box. Rendered here,
      // BEFORE the fixed points and the pupil's dot, so nothing is obscured.
      const clipLine = (x1, y1, x2, y2) => {
        // box edges in pixels (gTop < gBot because pixel-y grows downward)
        const dx = x2 - x1, dy = y2 - y1;
        const cand = [];
        const add = (x, y) => {
          const EPS = 1e-6;
          if (x >= gLeft - EPS && x <= gRight + EPS && y >= gTop - EPS && y <= gBot + EPS) {
            if (!cand.some(c => Math.abs(c[0] - x) < 1e-3 && Math.abs(c[1] - y) < 1e-3)) cand.push([x, y]);
          }
        };
        if (Math.abs(dx) > 1e-9) {                       // intersect x = gLeft / gRight
          for (const ex of [gLeft, gRight]) { const t = (ex - x1) / dx; add(ex, y1 + t * dy); }
        }
        if (Math.abs(dy) > 1e-9) {                       // intersect y = gTop / gBot
          for (const ey of [gTop, gBot]) { const t = (ey - y1) / dy; add(x1 + t * dx, ey); }
        }
        return cand.length >= 2 ? [cand[0], cand[1]] : null;
      };
      const lines = Array.isArray(spec.lines) ? spec.lines : [];
      for (const ln of lines) {
        if (!ln || !Array.isArray(ln.p1) || !Array.isArray(ln.p2)) continue;
        const [ax, ay] = toPx(Number(ln.p1[0]), Number(ln.p1[1]));
        const [bx, by] = toPx(Number(ln.p2[0]), Number(ln.p2[1]));
        if (ax === bx && ay === by) continue;            // degenerate: p1 === p2
        const seg = clipLine(ax, ay, bx, by);
        if (!seg) continue;                              // line misses the plane
        const [[sx, sy], [ex, ey]] = seg;
        const attr = { x1: sx, y1: sy, x2: ex, y2: ey, stroke: '#4f8df7', 'stroke-width': 1.25, 'stroke-linecap': 'round' };
        if (ln.dashed) attr['stroke-dasharray'] = '6 4';
        svg.appendChild(mk('line', attr));
        if (ln.label != null && ln.label !== '') {
          // anchor near the upper (smaller pixel-y) clipped end, nudged off the line
          const [ux, uy] = sy <= ey ? [sx, sy] : [ex, ey];
          const nx = ux < (gLeft + gRight) / 2 ? ux + 8 : ux - 8;   // push toward interior
          const anchor = ux < (gLeft + gRight) / 2 ? 'start' : 'end';
          const lab = mk('text', { x: nx, y: uy + 14, fill: '#4f8df7', 'font-size': 12, 'font-weight': 700, 'text-anchor': anchor });
          lab.textContent = String(ln.label); svg.appendChild(lab);
        }
      }

      // ---- optional fixed labelled points --------------------------------
      const fixed = Array.isArray(spec.points) ? spec.points.filter(p => Array.isArray(p) && p.length >= 2) : [];
      for (const p of fixed) {
        const [px, py] = toPx(Number(p[0]), Number(p[1]));
        svg.appendChild(mk('circle', { cx: px, cy: py, r: 5, fill: '#7ea88c', stroke: '#0b0f14', 'stroke-width': 1.5 }));
        if (p[2] != null && p[2] !== '') {
          const lab = mk('text', { x: px + 9, y: py - 8, fill: '#9fc7ad', 'font-size': 13, 'font-weight': 700, 'text-anchor': 'start' });
          lab.textContent = String(p[2]); svg.appendChild(lab);
        }
      }

      // ---- target (expected) + plotted dot --------------------------------
      const target = mk('circle', { r: 8, fill: 'none', stroke: '#22c55e', 'stroke-width': 2.5, opacity: 0 });
      svg.appendChild(target);
      const dot = mk('circle', { r: 7, fill: '#4f8df7', stroke: '#0b0f14', 'stroke-width': 2, opacity: 0 });
      svg.appendChild(dot);

      const readout = mk('text', { x: W - 8, y: 20, fill: '#e6edf3', 'font-size': 15, 'text-anchor': 'end', 'font-weight': 700 });
      if (!spec.typed) { readout.textContent = '(–, –)'; svg.appendChild(readout); }
      host.appendChild(svg);

      // ---- typed-answer mode: the grid is STIMULUS only (a drawn line / points),
      //      the pupil TYPES the answer (a y-value, gradient, intercept, …).
      //      No drag-to-plot; __getValue returns the typed string.
      if (spec.typed) {
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'm-input';
        input.setAttribute('inputmode', spec.keypad || 'text');
        if (spec.placeholder) input.placeholder = spec.placeholder;
        input.style.cssText = 'margin-top:10px;display:block;font-size:1.1rem;padding:8px 12px;' +
          'width:160px;background:#0b0f14;color:#e6edf3;border:1px solid #30363d;border-radius:8px';
        input.addEventListener('keydown', (ev) => {
          if (ev.key === 'Enter') { ev.preventDefault(); if (api && api.submit) api.submit(); }
        });
        host.appendChild(input);
        host.__getValue = () => input.value.trim();
        host.__feedback = (res) => {
          input.style.borderColor = res.correct ? '#22c55e' : '#f85149';
        };
        return;   // skip the plotting wiring below
      }

      let value = null;
      function place(gx, gy) {
        const [px, py] = toPx(gx, gy);
        dot.setAttribute('cx', px); dot.setAttribute('cy', py); dot.setAttribute('opacity', 1);
        value = `(${gx},${gy})`;
        readout.textContent = `(${gx}, ${gy})`;
      }

      function pointer(ev) {
        const r = svg.getBoundingClientRect();
        const cx = (ev.touches ? ev.touches[0].clientX : ev.clientX) - r.left;
        const cy = (ev.touches ? ev.touches[0].clientY : ev.clientY) - r.top;
        const px = cx / r.width * W, py = cy / r.height * H;
        return toGrid(px, py);
      }
      let down = false;
      function set(ev) { const [gx, gy] = pointer(ev); place(gx, gy); ev.preventDefault(); }
      svg.addEventListener('mousedown', (e) => { down = true; set(e); });
      svg.addEventListener('mousemove', (e) => { if (down) set(e); });
      window.addEventListener('mouseup', () => { down = false; });
      svg.addEventListener('touchstart', (e) => { down = true; set(e); });
      svg.addEventListener('touchmove', (e) => { if (down) set(e); });
      window.addEventListener('touchend', () => { down = false; });

      host.__empty = 'Tap the grid to plot your point.';
      host.__getValue = () => value;
      host.__feedback = (res) => {
        dot.setAttribute('fill', res.correct ? '#22c55e' : '#f85149');
        if (!res.correct && res.expected) {
          const m = String(res.expected).match(/-?\d+/g);
          if (m && m.length >= 2) {
            const [px, py] = toPx(Number(m[0]), Number(m[1]));
            target.setAttribute('cx', px); target.setAttribute('cy', py); target.setAttribute('opacity', 1);
          }
        }
      };
    }
  };
})();
