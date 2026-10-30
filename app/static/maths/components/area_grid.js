/* area_grid — squared grid for AREA, PERIMETER and FRACTION AREA MODELS.
 *
 * spec: { mode, rows, cols, cells, parts, shaded }
 *   mode:"read_area"      — shape drawn from `cells` ([[r,c],..]) or rows×cols rectangle;
 *                           pupil counts squares. Typed input. value = typed string.
 *   mode:"read_perimeter" — same drawing with the outline emphasised; pupil counts the
 *                           boundary length. Typed input. value = typed string.
 *   mode:"build_area"     — empty rows×cols grid; pupil clicks cells. value = <number shaded>.
 *   mode:"fraction"       — rectangle of `parts` equal squares; pupil clicks to shade.
 *                           value = "<shaded>/<parts>" STRING.
 *   mode:"fraction_read"  — `shaded` of `parts` already shaded; pupil types the fraction.
 *                           value = typed string.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';

  const BG = '#0b0f14', BORDER = '#30363d', INK = '#e6edf3', MUTE = '#8b949e';
  const ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';
  const EMPTY = '#161b22', FAINT = '#1c2430';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }

  // near-square factorisation of n (rows <= cols), keeping cols <= 10 where possible
  function factor(n) {
    n = Math.max(1, n | 0);
    let best = [1, n];
    for (let r = 1; r * r <= n; r++) {
      if (n % r === 0) best = [r, n / r];
    }
    // a single row reads better for small denominators
    if (n <= 6) return [1, n];
    if (best[1] > 12 && n % 2 === 0) return [2, n / 2];
    return best;
  }

  window.MComp["area_grid"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const mode = spec.mode || 'read_area';
      const interactive = (mode === 'build_area' || mode === 'fraction');
      const isFraction = (mode === 'fraction' || mode === 'fraction_read');

      // ---- geometry -------------------------------------------------------
      let rows, cols, parts = null;
      let filled = null; // Set of "r,c" for pre-drawn shapes

      if (isFraction) {
        parts = Math.max(1, (spec.parts | 0) || 1);
        if (spec.rows && spec.cols && spec.rows * spec.cols === parts) {
          rows = spec.rows | 0; cols = spec.cols | 0;
        } else {
          const f = factor(parts); rows = f[0]; cols = f[1];
        }
      } else if (Array.isArray(spec.cells) && spec.cells.length) {
        const cs = spec.cells.map(p => [p[0] | 0, p[1] | 0]);
        const minR = Math.min(...cs.map(p => p[0])), minC = Math.min(...cs.map(p => p[1]));
        filled = new Set(cs.map(p => (p[0] - minR) + ',' + (p[1] - minC)));
        rows = Math.max(...cs.map(p => p[0])) - minR + 1;
        cols = Math.max(...cs.map(p => p[1])) - minC + 1;
      } else {
        rows = Math.max(1, (spec.rows | 0) || 1);
        cols = Math.max(1, (spec.cols | 0) || 1);
        if (!interactive) {
          filled = new Set();
          for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) filled.add(r + ',' + c);
        }
      }

      const isOn = (r, c) => !filled || filled.has(r + ',' + c);

      // cell size: keep legible up to 10x10 inside ~460px
      const CELL = Math.max(22, Math.min(44, Math.floor(400 / Math.max(rows, cols, 1))));
      const PAD = 16, TOP = interactive || isFraction ? 30 : 14;
      const W = cols * CELL + PAD * 2;
      const H = rows * CELL + PAD + TOP;
      const gx = PAD, gy = TOP;
      const maxW = Math.min(460, W + 20);

      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: 'max-width:' + maxW + 'px;background:' + BG + ';border:1px solid ' + BORDER +
          ';border-radius:10px;display:block;touch-action:none;-webkit-user-select:none;user-select:none'
      });

      // ---- state ----------------------------------------------------------
      // shaded[] indexed r*cols+c; only meaningful for interactive / fraction_read
      const shaded = new Array(rows * cols).fill(false);
      if (mode === 'fraction_read') {
        const k = Math.max(0, Math.min(parts, (spec.shaded | 0) || 0));
        for (let i = 0; i < k; i++) shaded[i] = true;
      }

      // ---- background: faint full grid ------------------------------------
      const bg = mk('g', {});
      svg.appendChild(bg);
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          bg.appendChild(mk('rect', {
            x: gx + c * CELL, y: gy + r * CELL, width: CELL, height: CELL,
            fill: EMPTY, stroke: FAINT, 'stroke-width': 1, 'shape-rendering': 'crispEdges'
          }));
        }
      }

      // ---- cells (the drawn/clickable layer) ------------------------------
      const cellG = mk('g', {});
      svg.appendChild(cellG);
      const rects = new Array(rows * cols).fill(null);
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const idx = r * cols + c;
          const draw = interactive || isFraction || isOn(r, c);
          if (!draw) continue;
          const rc = mk('rect', {
            x: gx + c * CELL, y: gy + r * CELL, width: CELL, height: CELL,
            fill: EMPTY, stroke: BORDER, 'stroke-width': 1.5, 'shape-rendering': 'crispEdges',
            style: interactive ? 'cursor:pointer' : ''
          });
          rects[idx] = rc;
          cellG.appendChild(rc);
        }
      }

      // ---- perimeter outline ----------------------------------------------
      const outlineG = mk('g', {});
      svg.appendChild(outlineG);
      function drawOutline(color, width) {
        outlineG.innerHTML = '';
        for (let r = 0; r < rows; r++) {
          for (let c = 0; c < cols; c++) {
            if (!isOn(r, c)) continue;
            const x = gx + c * CELL, y = gy + r * CELL;
            const edges = [];
            if (r === 0 || !isOn(r - 1, c)) edges.push([x, y, x + CELL, y]);
            if (r === rows - 1 || !isOn(r + 1, c)) edges.push([x, y + CELL, x + CELL, y + CELL]);
            if (c === 0 || !isOn(r, c - 1)) edges.push([x, y, x, y + CELL]);
            if (c === cols - 1 || !isOn(r, c + 1)) edges.push([x + CELL, y, x + CELL, y + CELL]);
            for (const e of edges) {
              outlineG.appendChild(mk('line', {
                x1: e[0], y1: e[1], x2: e[2], y2: e[3],
                stroke: color, 'stroke-width': width, 'stroke-linecap': 'square'
              }));
            }
          }
        }
      }

      // ---- readout ---------------------------------------------------------
      let readout = null;
      if (interactive || isFraction) {
        readout = mk('text', { x: W / 2, y: 20, fill: INK, 'font-size': 15, 'text-anchor': 'middle', 'font-weight': 700 });
        svg.appendChild(readout);
      }

      function count() { return shaded.reduce((a, b) => a + (b ? 1 : 0), 0); }

      function paint(override) {
        const on = override || ACCENT;
        for (let i = 0; i < rects.length; i++) {
          if (!rects[i]) continue;
          if (interactive || isFraction) {
            rects[i].setAttribute('fill', shaded[i] ? on : EMPTY);
          } else {
            rects[i].setAttribute('fill', on);
          }
        }
        if (readout) {
          readout.textContent = isFraction ? (count() + '/' + parts) : (count() + (count() === 1 ? ' square' : ' squares'));
        }
      }

      // ---- interaction (mouse + touch, drag-paint) -------------------------
      if (interactive) {
        let dragging = false, paintTo = true;
        function cellAt(ev) {
          const b = svg.getBoundingClientRect();
          const t = (ev.touches && ev.touches[0]) ? ev.touches[0] : ev;
          const vx = (t.clientX - b.left) / b.width * W;
          const vy = (t.clientY - b.top) / b.height * H;
          const c = Math.floor((vx - gx) / CELL), r = Math.floor((vy - gy) / CELL);
          if (r < 0 || r >= rows || c < 0 || c >= cols) return -1;
          return r * cols + c;
        }
        function down(ev) {
          const i = cellAt(ev); if (i < 0) return;
          dragging = true; paintTo = !shaded[i];
          shaded[i] = paintTo; paint(); ev.preventDefault();
        }
        function move(ev) {
          if (!dragging) return;
          const i = cellAt(ev); if (i < 0) return;
          if (shaded[i] !== paintTo) { shaded[i] = paintTo; paint(); }
          ev.preventDefault();
        }
        function up() { dragging = false; }
        svg.addEventListener('mousedown', down);
        svg.addEventListener('mousemove', move);
        window.addEventListener('mouseup', up);
        svg.addEventListener('touchstart', down, { passive: false });
        svg.addEventListener('touchmove', move, { passive: false });
        window.addEventListener('touchend', up);
      }

      host.appendChild(svg);

      // ---- initial paint ---------------------------------------------------
      if (mode === 'read_perimeter') {
        for (const rc of rects) if (rc) rc.setAttribute('fill', '#1d2b45');
        drawOutline(ACCENT, 4);
      } else if (mode === 'read_area') {
        paint(ACCENT);
      } else {
        paint();
      }

      // ---- typed input (read modes) ---------------------------------------
      const typed = (mode === 'read_area' || mode === 'read_perimeter' || mode === 'fraction_read');
      let input = null;
      if (typed) {
        const wrap = document.createElement('div');
        wrap.style.cssText = 'margin-top:12px';
        input = document.createElement('input');
        input.type = 'text';
        input.inputMode = (mode === 'fraction_read') ? 'text' : 'numeric';
        input.className = 'm-input';
        input.autocomplete = 'off';
        input.placeholder = (mode === 'fraction_read') ? 'e.g. 3/8' : '';
        input.setAttribute('aria-label', 'Your answer');
        input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:140px;background:' + BG + ';color:' + INK +
          ';border:2px solid ' + BORDER + ';border-radius:8px;text-align:center;outline:none';
        input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
        input.addEventListener('blur', () => { input.style.borderColor = BORDER; });
        input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); } });
        wrap.appendChild(input);
        host.appendChild(wrap);
      }

      // ---- contract --------------------------------------------------------
      if (typed) {
        host.__getValue = () => input.value.trim();
      } else if (mode === 'fraction') {
        host.__getValue = () => count() + '/' + parts;
      } else {
        host.__getValue = () => count();
      }

      host.__feedback = (res) => {
        const col = res && res.correct ? GOOD : BAD;
        if (typed) {
          if (input) input.style.borderColor = col;
          if (mode === 'read_perimeter') drawOutline(col, 4);
          else if (mode === 'read_area') paint(col);
          else paint(col);
        } else {
          paint(col);
          if (readout && res && !res.correct && res.expected != null) {
            readout.textContent += '  (want ' + String(res.expected) + ')';
          }
        }
      };
    }
  };
})();
