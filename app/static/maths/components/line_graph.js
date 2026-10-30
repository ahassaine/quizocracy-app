/* line_graph — read a time graph (points joined by straight lines), type a numeric answer.
 * spec: { points: [[label, value], ...], yLabel: "°C", xLabel: "Time", missing: i }
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

  window.MComp["line_graph"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const pts = Array.isArray(spec.points) ? spec.points.filter(p => Array.isArray(p) && p.length >= 2) : [];
      const n = pts.length;
      const labels = pts.map(p => String(p[0]));
      const vals = pts.map(p => Number(p[1]));
      const missing = (typeof spec.missing === 'number' && spec.missing >= 0 && spec.missing < n) ? spec.missing : -1;

      const W = 640, H = 360;
      const padL = 62, padR = 22, padT = 26, padB = 62;
      const x0 = padL, x1 = W - padR, yTop = padT, yBot = H - padB;
      const plotW = x1 - x0, plotH = yBot - yTop;

      // ---- y scale: nice round steps covering 0..max (extend below 0 if needed) ----
      const dataMax = n ? Math.max(...vals) : 1;
      const dataMin = n ? Math.min(...vals) : 0;
      const lo = Math.min(0, dataMin);
      const hi = Math.max(dataMax, lo + 1e-9);
      const step = niceStep(Math.max(hi - lo, Math.abs(hi) || 1), 6);
      const yMin = Math.floor((lo / step) + 1e-9) * step;
      let yMax = Math.ceil((hi / step) - 1e-9) * step;
      if (yMax <= yMin) yMax = yMin + step;
      const tickDp = decimalsOf(step);
      const toY = (v) => yBot - ((v - yMin) / (yMax - yMin)) * plotH;

      const slot = plotW / Math.max(1, n);
      const toX = (i) => (n === 1) ? (x0 + plotW / 2) : (x0 + slot / 2 + slot * i);

      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: 'max-width:520px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;display:block'
      });

      // ---- horizontal gridlines + y tick labels ----
      const nTicks = Math.round((yMax - yMin) / step);
      for (let k = 0; k <= nTicks; k++) {
        const v = yMin + k * step;
        const y = toY(v);
        const zero = Math.abs(v) < step * 1e-6;
        svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: zero ? '#8b949e' : '#21262d', 'stroke-width': zero ? 2 : 1 }));
        svg.appendChild(mk('text', { x: x0 - 9, y: y + 4, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'end' }, fmt(v, tickDp)));
      }

      // ---- vertical gridlines at each point + x tick labels ----
      for (let i = 0; i < n; i++) {
        const cx = toX(i);
        svg.appendChild(mk('line', { x1: cx, y1: yTop, x2: cx, y2: yBot, stroke: '#1b2129', 'stroke-width': 1 }));
        svg.appendChild(mk('line', { x1: cx, y1: yBot, x2: cx, y2: yBot + 5, stroke: '#8b949e', 'stroke-width': 1 }));
        svg.appendChild(mk('text', { x: cx, y: yBot + 21, fill: '#c9d1d9', 'font-size': 12, 'text-anchor': 'middle' }, labels[i]));
      }

      // ---- axes ----
      svg.appendChild(mk('line', { x1: x0, y1: yTop, x2: x0, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));
      svg.appendChild(mk('line', { x1: x0, y1: yBot, x2: x1, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));

      // ---- axis titles ----
      if (spec.xLabel) {
        svg.appendChild(mk('text', { x: (x0 + x1) / 2, y: H - 14, fill: '#e6edf3', 'font-size': 13, 'font-weight': 600, 'text-anchor': 'middle' }, String(spec.xLabel)));
      }
      if (spec.yLabel) {
        svg.appendChild(mk('text', {
          x: 16, y: (yTop + yBot) / 2, fill: '#e6edf3', 'font-size': 13, 'font-weight': 600,
          'text-anchor': 'middle', transform: `rotate(-90 16 ${(yTop + yBot) / 2})`
        }, String(spec.yLabel)));
      }

      // ---- segments: solid, except those touching the missing point (dashed) ----
      for (let i = 0; i < n - 1; i++) {
        const dashed = (i === missing || i + 1 === missing);
        svg.appendChild(mk('line', {
          x1: toX(i), y1: toY(vals[i]), x2: toX(i + 1), y2: toY(vals[i + 1]),
          stroke: dashed ? '#8b949e' : '#4f8df7', 'stroke-width': dashed ? 2 : 2.5,
          'stroke-linecap': 'round',
          ...(dashed ? { 'stroke-dasharray': '6 5' } : {})
        }));
      }

      // ---- points ----
      for (let i = 0; i < n; i++) {
        const cx = toX(i), cy = toY(vals[i]);
        if (i === missing) {
          svg.appendChild(mk('circle', { cx, cy, r: 5.5, fill: '#0b0f14', stroke: '#e6edf3', 'stroke-width': 2.5 }));
          svg.appendChild(mk('text', { x: cx, y: cy - 12, fill: '#e6edf3', 'font-size': 13, 'font-weight': 700, 'text-anchor': 'middle' }, '?'));
        } else {
          svg.appendChild(mk('circle', { cx, cy, r: 4.5, fill: '#4f8df7' }));
        }
      }

      host.appendChild(svg);

      // ---- typed answer ----
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'decimal';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:140px;background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;text-align:center;outline:none';
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
