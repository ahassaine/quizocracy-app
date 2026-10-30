/* scatter_plot — read a scatter graph (dots on scaled x/y axes), type a numeric/text answer.
 * spec: { points: [[x,y], ...], xLabel, yLabel, line:{p1:[x1,y1],p2:[x2,y2]}, highlight: i }
 * value = trimmed typed string.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a, txt) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; return e; }

  // ---- number helpers (kill float artefacts) ----
  function decimalsOf(x) {
    const s = String(x);
    if (s.indexOf('e') >= 0 || s.indexOf('E') >= 0) return 10;
    const i = s.indexOf('.');
    return i < 0 ? 0 : s.length - i - 1;
  }
  function fmt(v, dp) {
    let s = Number(v).toFixed(Math.min(10, Math.max(0, dp)));
    if (s.indexOf('.') >= 0) s = s.replace(/0+$/, '').replace(/\.$/, '');
    if (s === '-0') s = '0';
    return s;
  }
  // nice step covering `span` in roughly `target` gridlines
  function niceStep(span, target) {
    if (!(span > 0)) return 1;
    const raw = span / Math.max(2, target);
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const n = raw / mag;
    let m;
    if (n <= 1) m = 1; else if (n <= 2) m = 2; else if (n <= 2.5) m = 2.5; else if (n <= 5) m = 5; else m = 10;
    return m * mag;
  }
  // scale one axis from data range → {min,max,step,dp}, with a little padding, NOT forcing origin
  function axisScale(lo, hi) {
    if (!(hi > lo)) { hi = lo + 1; }              // degenerate: give it width
    const pad = (hi - lo) * 0.08;
    let plo = lo - pad, phi = hi + pad;
    const step = niceStep(phi - plo, 6);
    const min = Math.floor((plo / step) + 1e-9) * step;
    let max = Math.ceil((phi / step) - 1e-9) * step;
    if (max <= min) max = min + step;
    return { min, max, step, dp: decimalsOf(step) };
  }

  window.MComp["scatter_plot"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const pts = Array.isArray(spec.points) ? spec.points.filter(p => Array.isArray(p) && p.length >= 2) : [];
      const xs = pts.map(p => Number(p[0]));
      const ys = pts.map(p => Number(p[1]));
      const highlight = (typeof spec.highlight === 'number' && spec.highlight >= 0 && spec.highlight < pts.length) ? spec.highlight : -1;

      const W = 640, H = 380;
      const padL = 62, padR = 22, padT = 22, padB = 62;
      const x0 = padL, x1 = W - padR, yTop = padT, yBot = H - padB;
      const plotW = x1 - x0, plotH = yBot - yTop;

      // ---- scales from data (both axes), no forced origin ----
      const line = spec.line && spec.line.p1 && spec.line.p2 ? spec.line : null;
      const allX = xs.slice(), allY = ys.slice();
      const xSc = axisScale(allX.length ? Math.min(...allX) : 0, allX.length ? Math.max(...allX) : 1);
      const ySc = axisScale(allY.length ? Math.min(...allY) : 0, allY.length ? Math.max(...allY) : 1);

      const toX = (v) => x0 + ((v - xSc.min) / (xSc.max - xSc.min)) * plotW;
      const toY = (v) => yBot - ((v - ySc.min) / (ySc.max - ySc.min)) * plotH;

      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: 'max-width:520px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;display:block'
      });

      // ---- horizontal gridlines + y tick labels ----
      const yTicks = Math.round((ySc.max - ySc.min) / ySc.step);
      for (let k = 0; k <= yTicks; k++) {
        const v = ySc.min + k * ySc.step;
        const y = toY(v);
        svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: '#21262d', 'stroke-width': 1 }));
        svg.appendChild(mk('line', { x1: x0 - 5, y1: y, x2: x0, y2: y, stroke: '#8b949e', 'stroke-width': 1 }));
        svg.appendChild(mk('text', { x: x0 - 9, y: y + 4, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'end' }, fmt(v, ySc.dp)));
      }

      // ---- vertical gridlines + x tick labels ----
      const xTicks = Math.round((xSc.max - xSc.min) / xSc.step);
      for (let k = 0; k <= xTicks; k++) {
        const v = xSc.min + k * xSc.step;
        const x = toX(v);
        svg.appendChild(mk('line', { x1: x, y1: yTop, x2: x, y2: yBot, stroke: '#1b2129', 'stroke-width': 1 }));
        svg.appendChild(mk('line', { x1: x, y1: yBot, x2: x, y2: yBot + 5, stroke: '#8b949e', 'stroke-width': 1 }));
        svg.appendChild(mk('text', { x: x, y: yBot + 21, fill: '#c9d1d9', 'font-size': 12, 'text-anchor': 'middle' }, fmt(v, xSc.dp)));
      }

      // ---- axes ----
      svg.appendChild(mk('line', { x1: x0, y1: yTop, x2: x0, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));
      svg.appendChild(mk('line', { x1: x0, y1: yBot, x2: x1, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));

      // ---- axis titles ----
      if (spec.xLabel) {
        svg.appendChild(mk('text', { x: (x0 + x1) / 2, y: H - 12, fill: '#e6edf3', 'font-size': 13, 'font-weight': 600, 'text-anchor': 'middle' }, String(spec.xLabel)));
      }
      if (spec.yLabel) {
        svg.appendChild(mk('text', {
          x: 16, y: (yTop + yBot) / 2, fill: '#e6edf3', 'font-size': 13, 'font-weight': 600,
          'text-anchor': 'middle', transform: `rotate(-90 16 ${(yTop + yBot) / 2})`
        }, String(spec.yLabel)));
      }

      // ---- line of best fit, clipped to the plotted x-range ----
      if (line) {
        const [ax, ay] = line.p1.map(Number);
        const [bx, by] = line.p2.map(Number);
        const dx = bx - ax;
        // evaluate y at the two axis edges (or use vertical if dx ~ 0)
        let X1 = xSc.min, X2 = xSc.max, Y1, Y2;
        if (Math.abs(dx) < 1e-12) { X1 = X2 = ax; Y1 = ySc.min; Y2 = ySc.max; }
        else {
          const m = (by - ay) / dx;
          Y1 = ay + m * (X1 - ax);
          Y2 = ay + m * (X2 - ax);
        }
        svg.appendChild(mk('line', {
          x1: toX(X1), y1: toY(Y1), x2: toX(X2), y2: toY(Y2),
          stroke: '#4f8df7', 'stroke-width': 1.6, 'stroke-linecap': 'round', opacity: 0.9
        }));
      }

      // ---- data points ----
      for (let i = 0; i < pts.length; i++) {
        const cx = toX(xs[i]), cy = toY(ys[i]);
        if (i === highlight) {
          svg.appendChild(mk('circle', { cx, cy, r: 4, fill: '#e6edf3' }));
          svg.appendChild(mk('circle', { cx, cy, r: 8.5, fill: 'none', stroke: '#f85149', 'stroke-width': 2 }));
        } else {
          svg.appendChild(mk('circle', { cx, cy, r: 4, fill: '#4f8df7' }));
        }
      }

      host.appendChild(svg);

      // ---- typed answer ----
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:200px;background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;text-align:center;outline:none';
      input.addEventListener('focus', () => { input.style.borderColor = '#4f8df7'; });
      input.addEventListener('blur', () => { input.style.borderColor = '#30363d'; });
      input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); } });
      wrap.appendChild(input);
      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => { input.style.borderColor = res.correct ? '#22c55e' : '#f85149'; };
    }
  };
})();
