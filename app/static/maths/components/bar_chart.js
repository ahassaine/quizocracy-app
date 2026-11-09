/* bar_chart — read a bar chart, type an answer. value = typed string.
 * spec: { categories: ["Red","Blue",...], values: [n, n, ...], mode:"read", showValues?, keypad? }
 * Drawn at the host's real width (1 viewBox unit = 1 CSS px) so the scale stays readable on a phone.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a, txt) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; return e; }

  // A category named after a colour is drawn in that colour; the rest take palette colours not already used.
  const NAMED = { red: '#ef4444', blue: '#3b82f6', green: '#22c55e', yellow: '#facc15', orange: '#f97316',
                  purple: '#a855f7', pink: '#f472b6', brown: '#a0522d', black: '#000000', white: '#ffffff',
                  grey: '#9ca3af', gray: '#9ca3af', gold: '#d4a017', silver: '#c0c0c0' };
  const PALETTE = [['blue', '#4f8df7'], ['green', '#22c55e'], ['yellow', '#e3b341'], ['red', '#f85149'], ['purple', '#a371f7'],
                   ['teal', '#39c5cf'], ['pink', '#db61a2'], ['orange', '#f0883e']];
  // "Red", "Light blue", "Red team" — but not "Oranges" or "Redhill"
  function colourName(label) { return (String(label).toLowerCase().match(/[a-z]+/g) || []).find(w => NAMED[w]) || null; }
  function fills(labels) {
    const named = labels.map(colourName), used = new Set(named.filter(Boolean).map(c => c === 'gray' ? 'grey' : c));
    const free = PALETTE.filter(p => !used.has(p[0]));
    let j = 0;
    return named.map(c => {
      if (c) return { fill: NAMED[c], stroke: c === 'black' || c === 'brown' ? '#c9d1d9' : (c === 'white' ? '#8b949e' : 'none') };
      const p = (free.length ? free : PALETTE)[j++ % (free.length || PALETTE.length)];
      return { fill: p[1], stroke: 'none' };
    });
  }
  // 12 345 -> "12,345" (the questions write large numbers with commas)
  function fmt(v) {
    const r = Math.round(v * 1e6) / 1e6;
    return Math.abs(r) >= 1000 ? r.toLocaleString('en-GB', { maximumFractionDigits: 6 }) : String(r);
  }
  // Round scale steps only: 1, 2, 2.5, 5 x 10^k (2.5 itself only when the data has decimals).
  function niceSteps(top, ints) {
    const out = [];
    for (let k = Math.floor(Math.log10(top / 400)); k <= Math.ceil(Math.log10(top)) + 1; k++)
      [1, 2, 2.5, 5].forEach(m => { const s = Number((m * Math.pow(10, k)).toPrecision(6)); if (!ints || (s >= 1 && !(m === 2.5 && k < 1))) out.push(s); });
    return out;
  }
  function hostWidth(host, max) { const w = Math.floor(host.getBoundingClientRect().width) - 2; return w > 0 ? Math.max(260, Math.min(max, w)) : max; }
  function textW(s, size) { return String(s).length * size * 0.58; }
  // Category labels: one line if they fit the slot, else two lines, else slanted.
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

  window.MComp["bar_chart"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const cats = Array.isArray(spec.categories) ? spec.categories : [];
      const vals = (Array.isArray(spec.values) ? spec.values : []).map(Number);
      const n = Math.min(cats.length, vals.length);
      const data = vals.slice(0, n);

      // y-axis scale in round steps. Every bar a child must read should end on a LABELLED line: the default scale
      // (at most 10 lines) if it holds every bar, else the largest finer round step that does, with at most
      // MAX_LINES lines (the chart grows taller for them). Failing that, the default scale is kept and each bar
      // that ends between lines carries its value.
      const rawMax = Math.max(1e-9, ...data);
      const steps = niceSteps(rawMax, data.every(Number.isInteger));
      const lines = (s) => Math.ceil(rawMax / s - 1e-9);
      const onGrid = (v, s) => Math.abs(v / s - Math.round(v / s)) < 1e-6;
      let step = steps.find(s => lines(s) <= 10) || steps[steps.length - 1];
      if (!data.every(v => onGrid(v, step))) {
        const f = steps.filter(s => s < step).reverse().find(s => lines(s) <= MAX_LINES && data.every(v => onGrid(v, s)));
        if (f) step = f;
      }
      const nLines = Math.max(1, lines(step));
      const yMax = nLines * step;
      const fills_ = fills(cats.slice(0, n));

      const draw = () => {
        const W = hostWidth(host, 640);
        const tickLabels = [];
        for (let i = 0; i <= nLines; i++) tickLabels.push(fmt(i * step));
        const padL = 14 + Math.max(...tickLabels.map(t => t.length)) * 7.4, padR = 14;
        const plotW = W - padL - padR, slot = plotW / Math.max(1, n);
        // printed values: when two neighbours would touch, every second one sits a line higher
        const shown = data.map(v => spec.showValues || !onGrid(v, step));
        const crowded = data.some((v, i) => i > 0 && shown[i] && shown[i - 1] && (textW(fmt(v), 13) + textW(fmt(data[i - 1]), 13)) / 2 > slot - 4);
        const padT = crowded ? 42 : 26;
        const lay = labelLayout(cats.slice(0, n), slot, 13);
        const plotH = Math.max(W < 480 ? 220 : 266, nLines * LINE_GAP);
        const H = padT + plotH + lay.depth + 8;
        const x0 = padL, x1 = W - padR, yTop = padT, yBot = padT + plotH;
        const toY = (v) => yBot - (v / yMax) * plotH;

        const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'Bar chart',
          style: `max-width:${W}px;box-sizing:content-box;background:#0b0f14;border:1px solid #30363d;border-radius:10px;display:block` });

        // gridlines, every one labelled
        for (let i = 0; i <= nLines; i++) {
          const y = toY(i * step);
          svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: i === 0 ? '#8b949e' : '#2d3440', 'stroke-width': i === 0 ? 2 : 1 }));
          svg.appendChild(mk('text', { x: x0 - 7, y: y + 4, fill: '#9aa4b2', 'font-size': 12, 'text-anchor': 'end' }, tickLabels[i]));
        }
        svg.appendChild(mk('line', { x1: x0, y1: yTop, x2: x0, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));

        // bars
        const bw = Math.min(64, slot * 0.62);
        for (let i = 0; i < n; i++) {
          const cx = x0 + slot * i + slot / 2;
          const v = data[i], y = toY(v), f = fills_[i];
          svg.appendChild(mk('rect', { x: cx - bw / 2, y: y, width: bw, height: Math.max(0, yBot - y), fill: f.fill, rx: 3,
            stroke: f.stroke, 'stroke-width': f.stroke === 'none' ? 0 : 1.5 }));
          // the value is printed only when the scale cannot show it (or the question asks for it): otherwise it gives the answer away
          if (shown[i]) svg.appendChild(mk('text', { x: cx, y: y - 6 - (crowded && i % 2 ? 16 : 0), fill: '#e6edf3', 'font-size': 13, 'font-weight': 700, 'text-anchor': 'middle' }, fmt(v)));
          // category label
          if (lay.mode === 'slant') {
            const ly = yBot + 16;
            svg.appendChild(mk('text', { x: cx, y: ly, fill: '#c9d1d9', 'font-size': 13, 'text-anchor': 'end', transform: `rotate(-40 ${cx} ${ly})` }, lay.lines[i][0]));
          } else {
            lay.lines[i].forEach((l, k) => svg.appendChild(mk('text', { x: cx, y: yBot + 19 + k * 15, fill: '#c9d1d9', 'font-size': 13, 'text-anchor': 'middle' }, l)));
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

      // typed answer: a digit pad only for whole-number answers; words, decimals and negatives need a full keyboard
      const inputWrap = document.createElement('div');
      inputWrap.style.cssText = 'margin-top:12px';
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
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); }
      });
      inputWrap.appendChild(input);
      host.appendChild(inputWrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => {
        input.style.borderColor = res.correct ? '#22c55e' : '#f85149';
      };
    }
  };
})();
