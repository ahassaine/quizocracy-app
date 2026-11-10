/* array — build a rows×cols rectangular array of dots. value = rows * cols.
 * spec: { mode:"build", maxRows, maxCols, targetRows, targetCols, typed, eitherWay }
 *   typed — the pupil also types the total; value = "R rows of C = N", so the server marks both the
 *           array asked for and the total (eitherWay: "show 3 × 4" may be built 4 rows of 3).
 * Until the pupil builds something, the value is null ("nothing built" is no answer, not 0).
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["array"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      // room for the array asked for either way round ("3 rows of 10" built as 10 rows of 3 must fit too)
      const need = Math.max(spec.targetRows || 0, spec.targetCols || 0);
      const maxRows = Math.min(12, Math.max(spec.maxRows ?? 10, need)), maxCols = Math.min(12, Math.max(spec.maxCols ?? 10, need));
      let rows = 0, cols = 0, touched = false;

      const wrap = document.createElement('div');
      wrap.style.cssText = 'display:flex;flex-direction:column;gap:12px;color:#e6edf3;font-family:system-ui,sans-serif';

      // --- SVG grid of dots ---
      const W = 460, H = 320, pad = 24;
      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'max-width:480px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;touch-action:none;cursor:crosshair' });
      wrap.appendChild(svg);

      function cell(c, r) {
        const gw = W - pad * 2, gh = H - pad * 2;
        const nx = maxCols, ny = maxRows;
        const sx = gw / nx, sy = gh / ny;
        return { x: pad + sx * (c + 0.5), y: pad + sy * (r + 0.5), rad: Math.max(3, Math.min(sx, sy) * 0.32) };
      }

      function paint() {
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        // guide dots (faint) for the whole grid
        for (let r = 0; r < maxRows; r++) {
          for (let c = 0; c < maxCols; c++) {
            const p = cell(c, r);
            const filled = r < rows && c < cols;
            svg.appendChild(mk('circle', {
              cx: p.x, cy: p.y, r: filled ? p.rad : Math.max(1.5, p.rad * 0.35),
              fill: filled ? '#4f8df7' : '#1b2029',
              stroke: filled ? '#79b0ff' : 'none', 'stroke-width': filled ? 1 : 0
            }));
          }
        }
      }

      // --- controls ---
      function stepper(label, get, set) {
        const box = document.createElement('div');
        box.style.cssText = 'display:flex;align-items:center;gap:8px';
        const lab = document.createElement('span');
        lab.textContent = label; lab.style.cssText = 'min-width:64px;color:#8b949e;font-size:.85rem';
        const minus = document.createElement('button'); minus.textContent = '−';
        const val = document.createElement('span'); val.style.cssText = 'min-width:28px;text-align:center;font-weight:700;font-size:1.1rem';
        const plus = document.createElement('button'); plus.textContent = '+';
        [minus, plus].forEach(b => b.style.cssText = 'width:48px;height:48px;font-size:1.5rem;touch-action:manipulation;font-weight:700;background:#161b22;color:#e6edf3;border:1px solid #30363d;border-radius:8px;cursor:pointer');
        minus.type = 'button'; plus.type = 'button';
        minus.setAttribute('aria-label', 'Fewer ' + label.toLowerCase()); plus.setAttribute('aria-label', 'More ' + label.toLowerCase());
        function refresh() { val.textContent = get(); }
        minus.onclick = () => { touched = true; set(get() - 1); refresh(); paint(); readout(); };
        plus.onclick = () => { touched = true; set(get() + 1); refresh(); paint(); readout(); };
        box.append(lab, minus, val, plus);
        box._refresh = refresh;
        return box;
      }

      const clampR = v => rows = Math.max(0, Math.min(maxRows, v));
      const clampC = v => cols = Math.max(0, Math.min(maxCols, v));
      const rowCtrl = stepper('Rows', () => rows, clampR);
      const colCtrl = stepper('Columns', () => cols, clampC);
      const ctrls = document.createElement('div');
      ctrls.style.cssText = 'display:flex;gap:20px;flex-wrap:wrap';
      ctrls.append(rowCtrl, colCtrl);
      wrap.appendChild(ctrls);

      const read = document.createElement('div');
      read.style.cssText = 'font-size:1.3rem;font-weight:800;padding:4px 0';
      wrap.appendChild(read);

      // when the total is typed, the readout names the array but does not work out the total
      function readout() {
        read.innerHTML = spec.typed
          ? `${rows} row${rows === 1 ? '' : 's'} of ${cols}`
          : `${rows} rows × ${cols} = <span style="color:#4f8df7">${rows * cols}</span>`;
      }

      let input = null;
      if (spec.typed) {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex;align-items:center;gap:10px;flex-wrap:wrap';
        const lab = document.createElement('label');
        lab.textContent = 'How many altogether?'; lab.style.cssText = 'color:#8b949e;font-size:.95rem';
        input = document.createElement('input');
        input.type = 'text'; input.className = 'm-input'; input.autocomplete = 'off';
        input.inputMode = spec.keypad || 'numeric';
        input.id = 'arr-total-' + Math.random().toString(36).slice(2, 7); lab.htmlFor = input.id;
        input.style.cssText = 'font-size:1.2rem;padding:8px 12px;width:120px;text-align:center';
        input.addEventListener('keydown', (ev) => { if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); } });
        row.append(lab, input);
        wrap.appendChild(row);
      }

      // --- drag on grid to set rows/cols ---
      function fromPointer(ev) {
        const rect = svg.getBoundingClientRect();
        const px = ((ev.touches ? ev.touches[0].clientX : ev.clientX) - rect.left) / rect.width * W;
        const py = ((ev.touches ? ev.touches[0].clientY : ev.clientY) - rect.top) / rect.height * H;
        const gw = W - pad * 2, gh = H - pad * 2;
        const c = Math.ceil((px - pad) / (gw / maxCols));
        const r = Math.ceil((py - pad) / (gh / maxRows));
        clampC(c); clampR(r); touched = true;
        rowCtrl._refresh(); colCtrl._refresh(); paint(); readout();
      }
      let dragging = false;
      const down = e => { dragging = true; fromPointer(e); e.preventDefault(); };
      const move = e => { if (dragging) { fromPointer(e); e.preventDefault(); } };
      const up = () => { dragging = false; };
      svg.addEventListener('mousedown', down); svg.addEventListener('mousemove', move); window.addEventListener('mouseup', up);
      svg.addEventListener('touchstart', down, { passive: false }); svg.addEventListener('touchmove', move, { passive: false }); window.addEventListener('touchend', up);

      host.appendChild(wrap);
      rowCtrl._refresh(); colCtrl._refresh(); paint(); readout();

      host.__empty = spec.typed ? 'Build the array and type how many there are.' : 'Build the array first.';
      host.__getValue = () => {
        if (!touched || !rows || !cols) return null;
        if (!input) return rows * cols;
        const t = input.value.trim();
        if (!t) return null;
        let r = rows, c = cols;
        if (spec.eitherWay && r === spec.targetCols && c === spec.targetRows) { r = spec.targetRows; c = spec.targetCols; }
        const n = t.replace(/[\s,]/g, '');
        return `${r} rows of ${c} = ${/^\d+$/.test(n) ? +n : t}`;
      };
      host.__feedback = (res) => {
        read.style.color = res.correct ? '#22c55e' : '#f85149';
        if (input) input.style.borderColor = res.correct ? '#22c55e' : '#f85149';
      };
    }
  };
})();
