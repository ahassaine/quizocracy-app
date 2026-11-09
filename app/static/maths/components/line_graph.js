/* line_graph — read a time graph (points joined by straight lines), type an answer.
 * spec: { points: [[label, value], ...], yLabel: "°C", xLabel: "Time", missing: i, keypad? }
 * value = trimmed typed string.
 * Drawn at the host's real width (1 viewBox unit = 1 CSS px) so the scale stays readable on a phone.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a, txt) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; return e; }

  // ---- number helpers (kill float artefacts; thousands commas as the questions write them) ----
  function fmt(v) {
    let r = Math.round(v * 1e6) / 1e6;
    if (Object.is(r, -0)) r = 0;
    return Math.abs(r) >= 1000 ? r.toLocaleString('en-GB', { maximumFractionDigits: 6 }) : String(r);
  }
  // Round scale steps only: 1, 2, 2.5, 5 x 10^k (2.5 itself only when the data has decimals).
  function niceSteps(span, ints) {
    const out = [];
    for (let k = Math.floor(Math.log10(span / 400)); k <= Math.ceil(Math.log10(span)) + 1; k++)
      [1, 2, 2.5, 5].forEach(m => { const s = Number((m * Math.pow(10, k)).toPrecision(6)); if (!ints || (s >= 1 && !(m === 2.5 && k < 1))) out.push(s); });
    return out;
  }
  function hostWidth(host, max) { const w = Math.floor(host.getBoundingClientRect().width) - 2; return w > 0 ? Math.max(260, Math.min(max, w)) : max; }
  function textW(s, size) { return String(s).length * size * 0.58; }
  // x labels: one line if they fit the slot, else two lines, else slanted.
  function labelLayout(labels, slot, size) {
    if (labels.every(l => textW(l, size) <= slot - 6)) return { mode: 'flat', lines: labels.map(l => [String(l)]), depth: size + 10 };
    const two = labels.map(l => {
      const w = String(l).split(/\s+/);
      if (w.length < 2) return [String(l)];
      let best = null;
      for (let i = 1; i < w.length; i++) { const a = w.slice(0, i).join(' '), b = w.slice(i).join(' '); const m = Math.max(a.length, b.length); if (!best || m < best.m) best = { m, l: [a, b] }; }
      return best.l;
    });
    if (two.every(ls => ls.every(l => textW(l, size) <= slot - 6))) return { mode: 'flat', lines: two, depth: 2 * size + 14 };
    const long = Math.max(...labels.map(l => textW(l, size)));
    return { mode: 'slant', lines: labels.map(l => [String(l)]), depth: Math.min(150, long * 0.72 + size + 10) };
  }

  const LINE_GAP = 17, MAX_LINES = 25;     // px between labelled gridlines; most lines before values are printed instead

  window.MComp["line_graph"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const pts = Array.isArray(spec.points) ? spec.points.filter(p => Array.isArray(p) && p.length >= 2) : [];
      const n = pts.length;
      const labels = pts.map(p => String(p[0]));
      const vals = pts.map(p => Number(p[1]));
      const missing = (typeof spec.missing === 'number' && spec.missing >= 0 && spec.missing < n) ? spec.missing : -1;

      // ---- y scale in round steps covering 0..max (extend below 0 if needed) ----
      // Every value a child must read should sit on a LABELLED gridline: the default scale (at most 8 lines) if it
      // holds them all, else the largest finer round step that does, with at most MAX_LINES lines (the graph grows
      // taller). Failing that, the "?" point must still sit on a line, and every other point that is between lines
      // has its value printed beside it.
      const dataMax = n ? Math.max(...vals) : 1;
      const dataMin = n ? Math.min(...vals) : 0;
      const lo = Math.min(0, dataMin);
      const hi = Math.max(dataMax, lo + 1e-9);
      const steps = niceSteps(hi - lo, vals.every(Number.isInteger));
      const lines = (s) => Math.ceil(hi / s - 1e-9) - Math.floor(lo / s + 1e-9);
      const onGrid = (v, s) => Math.abs(v / s - Math.round(v / s)) < 1e-6;
      let step = steps.find(s => lines(s) <= 8) || steps[steps.length - 1];
      const finer = steps.filter(s => s < step).reverse().filter(s => lines(s) <= MAX_LINES);
      if (!vals.every(v => onGrid(v, step))) {
        const f = finer.find(s => vals.every(v => onGrid(v, s))) ||
                  (missing >= 0 && !onGrid(vals[missing], step) ? finer.find(s => onGrid(vals[missing], s)) : null);
        if (f) step = f;
      }
      const yMin = Math.floor(lo / step + 1e-9) * step;
      let yMax = Math.ceil(hi / step - 1e-9) * step;
      if (yMax <= yMin) yMax = yMin + step;
      const nTicks = Math.round((yMax - yMin) / step);
      // Last resort for the "?" point: unlabelled divisions (at most 5 per labelled step, at least 10 px apart) that
      // it sits on — reading a scale with unlabelled divisions, as children are taught.
      let minor = 0;
      if (missing >= 0 && !onGrid(vals[missing], step))
        minor = steps.filter(s => s < step).reverse().find(s => onGrid(vals[missing], s) && onGrid(step, s) && step / s <= 5) || 0;
      const nMinor = minor ? Math.round((yMax - yMin) / minor) : 0;

      const draw = () => {
        const W = hostWidth(host, 640);
        const ticks = [];
        for (let k = 0; k <= nTicks; k++) ticks.push(fmt(yMin + k * step));
        const padL = (spec.yLabel ? 34 : 12) + Math.max(...ticks.map(t => t.length)) * 7.4, padR = 18, padT = 30;
        const plotW = W - padL - padR, slot = plotW / Math.max(1, n);
        const lay = labelLayout(labels, slot, 12);
        const plotH = Math.max(W < 480 ? 220 : 272, nTicks * LINE_GAP, nMinor * 10);
        const H = padT + plotH + lay.depth + (spec.xLabel ? 26 : 8);
        const x0 = padL, x1 = W - padR, yTop = padT, yBot = padT + plotH;
        const toY = (v) => yBot - ((v - yMin) / (yMax - yMin)) * plotH;
        const toX = (i) => (n === 1) ? (x0 + plotW / 2) : (x0 + slot / 2 + slot * i);

        const svg = mk('svg', {
          viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'Line graph',
          style: `max-width:${W}px;box-sizing:content-box;background:#0b0f14;border:1px solid #30363d;border-radius:10px;display:block`
        });

        // ---- horizontal gridlines, every one labelled (plus the unlabelled divisions, if any) ----
        for (let k = 1; k < nMinor; k++) {
          const v = yMin + k * minor;
          if (onGrid(v - yMin, step)) continue;
          const y = toY(v);
          svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: '#232a34', 'stroke-width': 1 }));
          svg.appendChild(mk('line', { x1: x0 - 5, y1: y, x2: x0, y2: y, stroke: '#8b949e', 'stroke-width': 1 }));
        }
        for (let k = 0; k <= nTicks; k++) {
          const v = yMin + k * step, y = toY(v);
          const zero = Math.abs(v) < step * 1e-6;
          svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: zero ? '#8b949e' : '#2d3440', 'stroke-width': zero ? 2 : 1 }));
          svg.appendChild(mk('text', { x: x0 - 8, y: y + 4, fill: '#9aa4b2', 'font-size': 12, 'text-anchor': 'end' }, ticks[k]));
        }

        // ---- vertical gridlines at each point + x tick labels ----
        for (let i = 0; i < n; i++) {
          const cx = toX(i);
          svg.appendChild(mk('line', { x1: cx, y1: yTop, x2: cx, y2: yBot, stroke: '#1b2129', 'stroke-width': 1 }));
          svg.appendChild(mk('line', { x1: cx, y1: yBot, x2: cx, y2: yBot + 5, stroke: '#8b949e', 'stroke-width': 1 }));
          if (lay.mode === 'slant') {
            const ly = yBot + 16;
            svg.appendChild(mk('text', { x: cx, y: ly, fill: '#c9d1d9', 'font-size': 12, 'text-anchor': 'end', transform: `rotate(-40 ${cx} ${ly})` }, labels[i]));
          } else {
            lay.lines[i].forEach((l, k) => svg.appendChild(mk('text', { x: cx, y: yBot + 19 + k * 14, fill: '#c9d1d9', 'font-size': 12, 'text-anchor': 'middle' }, l)));
          }
        }

        // ---- axes ----
        svg.appendChild(mk('line', { x1: x0, y1: yTop, x2: x0, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));
        svg.appendChild(mk('line', { x1: x0, y1: yBot, x2: x1, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));

        // ---- axis titles ----
        if (spec.xLabel) {
          svg.appendChild(mk('text', { x: (x0 + x1) / 2, y: H - 9, fill: '#e6edf3', 'font-size': 13, 'font-weight': 600, 'text-anchor': 'middle' }, String(spec.xLabel)));
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

        // ---- points; a value between gridlines is printed above its point ----
        for (let i = 0; i < n; i++) {
          const cx = toX(i), cy = toY(vals[i]);
          if (i === missing) {
            svg.appendChild(mk('circle', { cx, cy, r: 5.5, fill: '#0b0f14', stroke: '#e6edf3', 'stroke-width': 2.5 }));
            svg.appendChild(mk('text', { x: cx, y: cy - 12, fill: '#e6edf3', 'font-size': 14, 'font-weight': 700, 'text-anchor': 'middle' }, '?'));
          } else {
            svg.appendChild(mk('circle', { cx, cy, r: 4.5, fill: '#4f8df7' }));
            if (!onGrid(vals[i], step)) {
              // above the point unless both neighbours are higher (a dip): then below it
              const dip = (i === 0 || vals[i - 1] > vals[i]) && (i === n - 1 || vals[i + 1] > vals[i]) && n > 1;
              svg.appendChild(mk('text', { x: cx, y: dip ? cy + 20 : cy - 10, fill: '#e6edf3', 'font-size': 13, 'font-weight': 700,
                'text-anchor': 'middle', stroke: '#0b0f14', 'stroke-width': 4, 'paint-order': 'stroke', 'stroke-linejoin': 'round' }, fmt(vals[i])));
            }
          }
        }
        return svg;
      };
      let svg = draw();
      host.appendChild(svg);
      if (window.ResizeObserver) {                     // phone turned, window resized: redraw at the new width
        let lastW = host.getBoundingClientRect().width;
        new ResizeObserver(() => { const w = host.getBoundingClientRect().width; if (w > 0 && Math.abs(w - lastW) > 8 && svg.parentNode === host) { lastW = w; const s = draw(); host.replaceChild(s, svg); svg = s; } }).observe(host);
      }

      // ---- typed answer: a digit pad only for whole-number answers; words, decimals and negatives need a full keyboard ----
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = spec.keypad || 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('autocapitalize', 'off');
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:160px;max-width:100%;background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;text-align:center;outline:none';
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
