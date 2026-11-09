/* equal_groups — objects arranged in equal groups (rings of counters).
 * The visual model for "3 groups of 4".
 *
 * spec: { mode:"read"|"build", groups, per, maxGroups, maxPer, loose, rings, typed, targetGroups, targetPer }
 *   mode:"read"  — draws `groups` rings of `per` counters; typed answer.
 *                  With `loose` (a "how many groups / in each group" question) it draws the starting
 *                  picture instead: `loose` counters not yet grouped, and `rings` empty rings when the
 *                  question shares into a given number of groups.
 *                  __getValue() -> trimmed typed string.
 *   mode:"build" — +/- steppers for groups and counters-per-group, live drawing.
 *                  __getValue() -> groups * per (number), or with `typed` the pupil also types the
 *                  total and the value is "G groups of P = N" (the server marks both).
 *                  Nothing built yet -> null (no answer, not 0).
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  const INK = '#e6edf3', MUTED = '#8b949e', BORDER = '#30363d', BG = '#0b0f14';
  const ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

  window.MComp["equal_groups"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const build = spec.mode === 'build';
      const maxGroups = clamp(spec.maxGroups ?? 8, 1, 12);
      const maxPer = clamp(spec.maxPer ?? 10, 1, 12);

      let groups = build ? clamp(spec.groups ?? 1, 0, maxGroups) : Math.max(0, spec.groups ?? 0);
      let per = build ? clamp(spec.per ?? 1, 0, maxPer) : Math.max(0, spec.per ?? 0);
      let touched = false;

      const wrap = document.createElement('div');
      wrap.style.cssText = 'display:flex;flex-direction:column;gap:12px;color:' + INK +
        ';font-family:system-ui,-apple-system,Segoe UI,sans-serif;max-width:520px';

      // ---------- drawing surface ----------
      const W = 520, H = 340;
      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: 'max-width:520px;display:block;background:' + BG + ';border:1px solid ' + BORDER +
          ';border-radius:10px;touch-action:manipulation'
      });
      wrap.appendChild(svg);

      // counters laid out on a small grid inside the ring
      function counterLayout(n) {
        if (n <= 0) return { cols: 0, rows: 0 };
        const cols = Math.ceil(Math.sqrt(n));
        return { cols, rows: Math.ceil(n / cols) };
      }

      // the starting picture: loose counters in rows (above), and the empty rings to share them into
      function paintLoose(n, rings) {
        const top = 14, bandH = rings ? H * 0.55 : H - 28;
        const cols = Math.min(n, Math.max(5, Math.ceil(Math.sqrt(n * (W - 40) / bandH))));
        const rowsN = Math.ceil(n / cols);
        const sx = (W - 40) / cols, sy = bandH / Math.max(1, rowsN);
        const dot = Math.max(4, Math.min(11, Math.min(sx, sy) * 0.34));
        for (let k = 0; k < n; k++) {
          const r = Math.floor(k / cols), c = k % cols;
          const inRow = Math.min(cols, n - r * cols), off = (cols - inRow) * sx / 2;
          svg.appendChild(mk('circle', { cx: 20 + off + sx * (c + 0.5), cy: top + sy * (r + 0.5), r: dot, fill: ACCENT, stroke: '#79b0ff', 'stroke-width': 1 }));
        }
        if (!rings) return;
        const y0 = top + bandH + 10, h = H - y0 - 10;
        const cw = (W - 20) / rings, R = Math.max(12, Math.min(cw / 2 - 6, h / 2));
        for (let i = 0; i < rings; i++) {
          svg.appendChild(mk('circle', { cx: 10 + cw * (i + 0.5), cy: y0 + h / 2, r: R, fill: 'rgba(79,141,247,0.06)', stroke: BORDER, 'stroke-width': 2, 'stroke-dasharray': '5 4' }));
        }
      }

      function paint() {
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        if (!build && spec.loose) { paintLoose(spec.loose | 0, spec.rings | 0); return; }
        const g = build ? groups : groups;
        if (g <= 0) {
          svg.appendChild(mk('text', {
            x: W / 2, y: H / 2, fill: MUTED, 'font-size': 18, 'text-anchor': 'middle'
          }, build ? 'Add some groups' : 'No groups'));
          return;
        }

        // arrange rings in a grid: prefer wide rows
        let cols = Math.min(g, g <= 4 ? g : Math.ceil(g / 2));
        if (g > 8) cols = Math.ceil(g / 2);
        cols = Math.max(1, Math.min(4, cols));
        const rows = Math.ceil(g / cols);

        const padX = 18, padY = 18;
        const cellW = (W - padX * 2) / cols;
        const cellH = (H - padY * 2) / rows;
        const R = Math.max(20, Math.min(cellW, cellH) / 2 - 8);

        const lay = counterLayout(per);
        // grid inscribed in the ring: side = R * sqrt(2) (a touch tighter for the stroke)
        const inner = R * 1.36;
        const stepX = lay.cols ? inner / lay.cols : 0;
        const stepY = lay.rows ? inner / lay.rows : 0;
        const dot = Math.max(3, Math.min(stepX, stepY) * 0.34);

        for (let i = 0; i < g; i++) {
          const r = Math.floor(i / cols), c = i % cols;
          const inRow = Math.min(cols, g - r * cols);           // centre a short last row
          const rowOffset = (cols - inRow) * cellW / 2;
          const cx = padX + rowOffset + cellW * (c + 0.5);
          const cy = padY + cellH * (r + 0.5);

          // the ring
          svg.appendChild(mk('circle', {
            cx, cy, r: R, fill: 'rgba(79,141,247,0.06)',
            stroke: BORDER, 'stroke-width': 2
          }));

          // counters inside
          for (let k = 0; k < per; k++) {
            const kr = Math.floor(k / lay.cols), kc = k % lay.cols;
            const inK = Math.min(lay.cols, per - kr * lay.cols);
            const kOffX = (lay.cols - inK) * stepX / 2;
            const x = cx - inner / 2 + kOffX + stepX * (kc + 0.5);
            const y = cy - inner / 2 + stepY * (kr + 0.5);
            svg.appendChild(mk('circle', {
              cx: x, cy: y, r: dot, fill: ACCENT, stroke: '#79b0ff', 'stroke-width': 1
            }));
          }
        }
      }

      // ---------- mode: read ----------
      if (!build) {
        host.appendChild(wrap);
        paint();

        const inputWrap = document.createElement('div');
        const input = document.createElement('input');
        input.type = 'text';
        input.inputMode = spec.keypad || 'text';
        input.className = 'm-input';
        input.autocomplete = 'off';
        input.setAttribute('aria-label', 'Your answer');
        input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:200px;max-width:100%;background:' +
          BG + ';color:' + INK + ';border:2px solid ' + BORDER +
          ';border-radius:8px;text-align:center;outline:none';
        input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
        input.addEventListener('blur', () => { input.style.borderColor = BORDER; });
        input.addEventListener('keydown', (ev) => {
          if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); }
        });
        inputWrap.appendChild(input);
        wrap.appendChild(inputWrap);

        host.__getValue = () => input.value.trim();
        host.__feedback = (res) => { input.style.borderColor = res && res.correct ? GOOD : BAD; };
        return;
      }

      // ---------- mode: build ----------
      function stepper(label, get, set) {
        const box = document.createElement('div');
        box.style.cssText = 'display:flex;align-items:center;gap:8px';
        const lab = document.createElement('span');
        lab.textContent = label;
        lab.style.cssText = 'min-width:96px;color:' + MUTED + ';font-size:.85rem';
        const minus = document.createElement('button');
        const plus = document.createElement('button');
        minus.type = 'button'; plus.type = 'button';
        minus.textContent = '−'; plus.textContent = '+';
        minus.setAttribute('aria-label', 'Fewer ' + label);
        plus.setAttribute('aria-label', 'More ' + label);
        const val = document.createElement('span');
        val.style.cssText = 'min-width:30px;text-align:center;font-weight:700;font-size:1.15rem';
        [minus, plus].forEach(b => {
          b.style.cssText = 'width:38px;height:38px;font-size:1.2rem;font-weight:700;background:#161b22;color:' +
            INK + ';border:1px solid ' + BORDER + ';border-radius:8px;cursor:pointer;touch-action:manipulation';
        });
        const bump = (d) => { touched = true; set(get() + d); val.textContent = get(); paint(); readout(); };
        minus.addEventListener('click', () => bump(-1));
        plus.addEventListener('click', () => bump(1));
        box.append(lab, minus, val, plus);
        box._refresh = () => { val.textContent = get(); };
        return box;
      }

      const ctrls = document.createElement('div');
      ctrls.style.cssText = 'display:flex;gap:20px;flex-wrap:wrap';
      const gCtrl = stepper('Groups', () => groups, v => { groups = clamp(v, 0, maxGroups); });
      const pCtrl = stepper('In each group', () => per, v => { per = clamp(v, 0, maxPer); });
      ctrls.append(gCtrl, pCtrl);
      wrap.appendChild(ctrls);

      const read = document.createElement('div');
      read.style.cssText = 'font-size:1.25rem;font-weight:800;padding:2px 0;line-height:1.4';
      wrap.appendChild(read);

      // when the total is typed, the readout names the groups but does not work out the total
      function readout() {
        read.innerHTML = groups + ' group' + (groups === 1 ? '' : 's') + ' of ' + per +
          (spec.typed ? '' : ' = <span style="color:' + ACCENT + '">' + (groups * per) + '</span>');
      }

      let input = null;
      if (spec.typed) {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex;align-items:center;gap:10px;flex-wrap:wrap';
        const lab = document.createElement('label');
        lab.textContent = 'How many altogether?'; lab.style.cssText = 'color:' + MUTED + ';font-size:.95rem';
        input = document.createElement('input');
        input.type = 'text'; input.className = 'm-input'; input.autocomplete = 'off';
        input.inputMode = spec.keypad || 'numeric';
        input.id = 'eg-total-' + Math.random().toString(36).slice(2, 7); lab.htmlFor = input.id;
        input.style.cssText = 'font-size:1.2rem;padding:8px 12px;width:120px;text-align:center';
        input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); } });
        row.append(lab, input);
        wrap.appendChild(row);
      }

      host.appendChild(wrap);
      gCtrl._refresh(); pCtrl._refresh();
      paint(); readout();

      host.__empty = spec.typed ? 'Make the groups and type how many there are.' : 'Make the groups first.';
      host.__getValue = () => {
        if (!touched || !groups || !per) return null;
        if (!input) return groups * per;
        const t = input.value.trim();
        if (!t) return null;
        const n = t.replace(/[\s,]/g, '');
        return groups + ' groups of ' + per + ' = ' + (/^\d+$/.test(n) ? +n : t);
      };
      host.__feedback = (res) => {
        read.style.color = res && res.correct ? GOOD : BAD;
        if (input) input.style.borderColor = res && res.correct ? GOOD : BAD;
      };
    }
  };
})();
