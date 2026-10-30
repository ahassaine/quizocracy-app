/* pictogram — read a pictogram (with a key) and type a numeric answer.
 * value = trimmed typed string.
 * spec: { categories:["Ali","Sara",...], values:[n,n,...], key:<int>, symbol:"circle"|"star"|"apple", unit?:"children" }
 * Supports half symbols when value is not an exact multiple of key.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }

  const INK = '#e6edf3', MUTED = '#8b949e', LINE = '#21262d', BORDER = '#30363d',
        BG = '#0b0f14', ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';

  // ---- symbol geometry (all drawn inside a box of side `s` centred on 0,0) ----
  function starPoints(s) {
    const R = s / 2, r = R * 0.42, pts = [];
    for (let i = 0; i < 10; i++) {
      const rad = (i % 2 === 0) ? R : r;
      const a = -Math.PI / 2 + i * Math.PI / 5;
      pts.push((Math.cos(a) * rad).toFixed(2) + ',' + (Math.sin(a) * rad).toFixed(2));
    }
    return pts.join(' ');
  }
  function applePath(s) {
    const R = s / 2;
    // two lobes + a point at the bottom; simple, symmetrical apple body
    return [
      'M 0 ' + (-0.28 * R),
      'C ' + (-0.30 * R) + ' ' + (-0.80 * R) + ' ' + (-1.00 * R) + ' ' + (-0.72 * R) + ' ' + (-1.00 * R) + ' ' + (-0.05 * R),
      'C ' + (-1.00 * R) + ' ' + (0.55 * R) + ' ' + (-0.45 * R) + ' ' + (1.00 * R) + ' 0 ' + (1.00 * R),
      'C ' + (0.45 * R) + ' ' + (1.00 * R) + ' ' + (1.00 * R) + ' ' + (0.55 * R) + ' ' + (1.00 * R) + ' ' + (-0.05 * R),
      'C ' + (1.00 * R) + ' ' + (-0.72 * R) + ' ' + (0.30 * R) + ' ' + (-0.80 * R) + ' 0 ' + (-0.28 * R),
      'Z'
    ].join(' ');
  }

  window.MComp["pictogram"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const cats = Array.isArray(spec.categories) ? spec.categories : [];
      const vals = Array.isArray(spec.values) ? spec.values : [];
      const n = Math.min(cats.length, vals.length);
      const key = Number(spec.key) > 0 ? Number(spec.key) : 1;
      const shape = ['circle', 'star', 'apple'].indexOf(spec.symbol) >= 0 ? spec.symbol : 'circle';
      const unit = spec.unit ? String(spec.unit) : '';
      const fillCol = shape === 'apple' ? '#f85149' : (shape === 'star' ? '#e3b341' : ACCENT);

      // ---- layout ----
      const S = 26;                 // symbol box side
      const GAP = 10;               // gap between symbols
      const PITCH = S + GAP;
      const padL = 14, padR = 16, padT = 14, padB = 14;
      const rowH = 40;
      const labelW = Math.max(70, Math.min(140, 10 + 8.2 * Math.max(4, ...cats.slice(0, n).map(c => String(c).length))));
      const colX = padL + labelW + 8;               // first symbol's left edge
      let maxCells = 1;
      for (let i = 0; i < n; i++) maxCells = Math.max(maxCells, Math.ceil((Number(vals[i]) || 0) / key));
      const keyH = 34;
      const W = colX + maxCells * PITCH + padR;
      const H = padT + keyH + n * rowH + padB;

      const svg = mk('svg', {
        viewBox: '0 0 ' + W + ' ' + H,
        width: '100%',
        role: 'img',
        'aria-label': 'Pictogram',
        style: 'max-width:520px;background:' + BG + ';border:1px solid ' + BORDER + ';border-radius:10px;display:block'
      });

      // one reusable clip for half symbols (left half of the symbol box)
      const uid = 'pg' + Math.random().toString(36).slice(2, 8);
      const defs = mk('defs', {});
      const clip = mk('clipPath', { id: uid + '-half', clipPathUnits: 'userSpaceOnUse' });
      clip.appendChild(mk('rect', { x: -S, y: -S, width: S, height: 2 * S }));
      defs.appendChild(clip);
      svg.appendChild(defs);

      // symbol factory: draws at (cx, cy); frac = 1 (full) or 0.5 (half)
      function symbol(cx, cy, frac) {
        const g = mk('g', { transform: 'translate(' + cx + ',' + cy + ')' });
        function body(attrs) {
          if (shape === 'circle') return mk('circle', Object.assign({ cx: 0, cy: 0, r: S / 2 }, attrs));
          if (shape === 'star') return mk('polygon', Object.assign({ points: starPoints(S) }, attrs));
          return mk('path', Object.assign({ d: applePath(S) }, attrs));
        }
        if (shape === 'apple') {
          // stalk + leaf, always outlined so a half apple still reads as an apple
          g.appendChild(mk('path', {
            d: 'M 0 ' + (-S * 0.30) + ' C ' + (S * 0.04) + ' ' + (-S * 0.46) + ' ' + (S * 0.10) + ' ' + (-S * 0.52) + ' ' + (S * 0.16) + ' ' + (-S * 0.56),
            stroke: '#7d5a3c', 'stroke-width': 2, fill: 'none', 'stroke-linecap': 'round'
          }));
        }
        // faint full outline (shows what a whole symbol looks like)
        g.appendChild(body({ fill: 'none', stroke: frac < 1 ? '#495260' : 'none', 'stroke-width': 1.5 }));
        // filled part
        const filled = body({ fill: fillCol, stroke: '#0b0f14', 'stroke-width': 1 });
        if (frac < 1) filled.setAttribute('clip-path', 'url(#' + uid + '-half)');
        g.appendChild(filled);
        if (frac < 1) {
          g.appendChild(mk('line', { x1: 0, y1: -S / 2 - 1, x2: 0, y2: S / 2 + 1, stroke: '#0b0f14', 'stroke-width': 1.5 }));
        }
        return g;
      }

      // ---- key line ----
      const keyY = padT + keyH / 2 - 2;
      svg.appendChild(symbol(padL + S / 2, keyY, 1));
      svg.appendChild(mk('text', {
        x: padL + S + 10, y: keyY + 5, fill: INK, 'font-size': 14, 'font-weight': 700
      }, '= ' + key + (unit ? ' ' + unit : '')));
      svg.appendChild(mk('line', {
        x1: padL, y1: padT + keyH - 2, x2: W - padR, y2: padT + keyH - 2, stroke: LINE, 'stroke-width': 1
      }));

      // ---- rows ----
      for (let i = 0; i < n; i++) {
        const cy = padT + keyH + rowH * i + rowH / 2;
        if (i % 2 === 1) {
          svg.appendChild(mk('rect', {
            x: padL - 4, y: cy - rowH / 2 + 2, width: W - padL - padR + 8, height: rowH - 4,
            fill: '#ffffff', opacity: 0.03, rx: 6
          }));
        }
        svg.appendChild(mk('text', {
          x: padL + labelW, y: cy + 5, fill: '#c9d1d9', 'font-size': 14, 'text-anchor': 'end'
        }, String(cats[i])));

        const v = Number(vals[i]) || 0;
        const full = Math.floor(v / key);
        const rem = v - full * key;
        for (let j = 0; j < full; j++) svg.appendChild(symbol(colX + j * PITCH + S / 2, cy, 1));
        if (rem > 0) svg.appendChild(symbol(colX + full * PITCH + S / 2, cy, 0.5));
      }

      host.appendChild(svg);

      // ---- typed answer ----
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'numeric';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:140px;background:' + BG + ';color:' + INK +
        ';border:2px solid ' + BORDER + ';border-radius:8px;text-align:center;outline:none';
      input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
      input.addEventListener('blur', () => { input.style.borderColor = BORDER; });
      input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); } });
      wrap.appendChild(input);
      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => { input.style.borderColor = res.correct ? GOOD : BAD; };
    }
  };
})();
