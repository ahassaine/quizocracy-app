/* fraction_bar — shade segments of a bar to build a fraction. value = "shaded/parts".
 * spec: { parts:<int denominator>, mode:"shade" }
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["fraction_bar"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const parts = Math.max(1, spec.parts | 0 || 1);
      const W = 500, H = 90, padX = 10, barY = 34, barH = 44;
      const bx0 = padX, bx1 = W - padX, segW = (bx1 - bx0) / parts;
      const shaded = new Array(parts).fill(false);
      let touched = false;                        // an untouched bar is no answer yet, not "0/parts"

      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'max-width:520px;background:#0b0f14;border:1px solid #30363d;border-radius:10px;touch-action:none;-webkit-user-select:none;user-select:none' });

      const readout = mk('text', { x: W / 2, y: 20, fill: '#e6edf3', 'font-size': 15, 'text-anchor': 'middle', 'font-weight': 700 });
      svg.appendChild(readout);

      const segs = [];
      for (let i = 0; i < parts; i++) {
        const r = mk('rect', {
          x: bx0 + i * segW, y: barY, width: segW, height: barH,
          fill: '#161b22', stroke: '#30363d', 'stroke-width': 1.5,
          style: 'cursor:pointer'
        });
        r.__i = i;
        svg.appendChild(r);
        segs.push(r);
      }
      host.appendChild(svg);

      function count() { return shaded.reduce((a, b) => a + (b ? 1 : 0), 0); }
      function paint(colorOverride) {
        for (let i = 0; i < parts; i++) {
          segs[i].setAttribute('fill', shaded[i] ? (colorOverride || '#4f8df7') : '#161b22');
        }
        const n = count();
        readout.textContent = n + '/' + parts;
      }

      // toggle by drag-paint: first touched segment sets the paint direction
      let dragging = false, paintTo = true;
      function segAt(ev) {
        const r = svg.getBoundingClientRect();
        const cx = (ev.touches && ev.touches[0] ? ev.touches[0].clientX : ev.clientX) - r.left;
        const vx = cx / r.width * W;
        const i = Math.floor((vx - bx0) / segW);
        return (i >= 0 && i < parts) ? i : -1;
      }
      function down(ev) {
        const i = segAt(ev); if (i < 0) return;
        dragging = true; touched = true;
        paintTo = !shaded[i];
        shaded[i] = paintTo;
        paint();
        ev.preventDefault();
      }
      function move(ev) {
        if (!dragging) return;
        const i = segAt(ev); if (i < 0) return;
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

      paint();

      host.__empty = 'Shade some of the bar first.';
      host.__getValue = () => touched ? count() + '/' + parts : null;
      host.__feedback = (res) => {
        paint(res.correct ? '#22c55e' : '#f85149');
        if (!res.correct && res.expected != null) {
          const m = String(res.expected).match(/(\d+)/);
          readout.textContent = count() + '/' + parts + (m ? '  (want ' + m[1] + '/' + parts + ')' : '');
        }
      };
    }
  };
})();
