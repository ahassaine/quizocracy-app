/* array — build a rows×cols rectangular array of dots. value = rows * cols.
 * spec: { mode:"build", maxRows, maxCols, targetRows, targetCols }
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["array"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const maxRows = spec.maxRows ?? 10, maxCols = spec.maxCols ?? 10;
      let rows = 0, cols = 0;

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
        [minus, plus].forEach(b => b.style.cssText = 'width:34px;height:34px;font-size:1.2rem;font-weight:700;background:#161b22;color:#e6edf3;border:1px solid #30363d;border-radius:8px;cursor:pointer');
        function refresh() { val.textContent = get(); }
        minus.onclick = () => { set(get() - 1); refresh(); paint(); readout(); };
        plus.onclick = () => { set(get() + 1); refresh(); paint(); readout(); };
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

      function readout() {
        read.innerHTML = `${rows} rows × ${cols} = <span style="color:#4f8df7">${rows * cols}</span>`;
      }

      // --- drag on grid to set rows/cols ---
      function fromPointer(ev) {
        const rect = svg.getBoundingClientRect();
        const px = ((ev.touches ? ev.touches[0].clientX : ev.clientX) - rect.left) / rect.width * W;
        const py = ((ev.touches ? ev.touches[0].clientY : ev.clientY) - rect.top) / rect.height * H;
        const gw = W - pad * 2, gh = H - pad * 2;
        const c = Math.ceil((px - pad) / (gw / maxCols));
        const r = Math.ceil((py - pad) / (gh / maxRows));
        clampC(c); clampR(r);
        rowCtrl._refresh(); colCtrl._refresh(); paint(); readout();
      }
      let dragging = false;
      const down = e => { dragging = true; fromPointer(e); e.preventDefault(); };
      const move = e => { if (dragging) { fromPointer(e); e.preventDefault(); } };
      const up = () => { dragging = false; };
      svg.addEventListener('mousedown', down); svg.addEventListener('mousemove', move); window.addEventListener('mouseup', up);
      svg.addEventListener('touchstart', down, { passive: false }); svg.addEventListener('touchmove', move, { passive: false }); window.addEventListener('touchend', up);

      host.appendChild(wrap);
      paint(); readout();

      host.__getValue = () => rows * cols;
      host.__feedback = (res) => { read.style.color = res.correct ? '#22c55e' : '#f85149'; };
    }
  };
})();
