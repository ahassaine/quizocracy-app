/* bar_chart — read a bar chart, type a numeric answer. value = typed string.
 * spec: { categories: ["Red","Blue",...], values: [n, n, ...], mode:"read" }
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a, txt) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; return e; }

  window.MComp["bar_chart"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const cats = Array.isArray(spec.categories) ? spec.categories : [];
      const vals = Array.isArray(spec.values) ? spec.values : [];
      const n = Math.min(cats.length, vals.length);

      const W = 640, H = 340, padL = 46, padR = 20, padT = 28, padB = 46;
      const x0 = padL, x1 = W - padR, yTop = padT, yBot = H - padB;
      const plotW = x1 - x0, plotH = yBot - yTop;

      // y-axis scale: nice integer max with integer gridlines.
      const rawMax = Math.max(1, ...vals.slice(0, n));
      const step = niceStep(rawMax);
      const yMax = Math.ceil(rawMax / step) * step;
      const toY = (v) => yBot - (v / yMax) * plotH;

      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'max-width:660px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;display:block' });

      // gridlines + y labels
      for (let v = 0; v <= yMax + 1e-9; v += step) {
        const y = toY(v);
        svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: v === 0 ? '#8b949e' : '#21262d', 'stroke-width': v === 0 ? 2 : 1 }));
        svg.appendChild(mk('text', { x: x0 - 8, y: y + 4, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'end' }, String(v)));
      }
      // y-axis line
      svg.appendChild(mk('line', { x1: x0, y1: yTop, x2: x0, y2: yBot, stroke: '#8b949e', 'stroke-width': 2 }));

      // bars
      const slot = plotW / Math.max(1, n);
      const bw = Math.min(64, slot * 0.6);
      const palette = ['#4f8df7', '#22c55e', '#e3b341', '#f85149', '#a371f7', '#39c5cf', '#db61a2', '#f0883e'];
      for (let i = 0; i < n; i++) {
        const cx = x0 + slot * i + slot / 2;
        const v = vals[i];
        const y = toY(v);
        svg.appendChild(mk('rect', { x: cx - bw / 2, y: y, width: bw, height: Math.max(0, yBot - y), fill: palette[i % palette.length], rx: 3 }));
        // value atop bar
        svg.appendChild(mk('text', { x: cx, y: y - 6, fill: '#e6edf3', 'font-size': 13, 'font-weight': 700, 'text-anchor': 'middle' }, String(v)));
        // category label
        svg.appendChild(mk('text', { x: cx, y: yBot + 20, fill: '#c9d1d9', 'font-size': 13, 'text-anchor': 'middle' }, String(cats[i])));
      }

      host.appendChild(svg);

      // typed numeric input
      const inputWrap = document.createElement('div');
      inputWrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'decimal';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:140px;background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;text-align:center;outline:none';
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

      function niceStep(m) {
        // choose a step that yields a small number of integer gridlines (<= ~10)
        const targets = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000];
        for (const s of targets) { if (m / s <= 10) return s; }
        return Math.ceil(m / 10);
      }
    }
  };
})();
