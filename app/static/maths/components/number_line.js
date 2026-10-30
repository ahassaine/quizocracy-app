/* number_line — place a marker on a number line. value = the number chosen.
 * spec: { min, max, step, major }  (major = spacing of labelled ticks)
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["number_line"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const min = spec.min ?? 0, max = spec.max ?? 100, step = spec.step ?? 1, major = spec.major ?? (max - min) / 10;
      const W = 640, H = 90, padL = 30, padR = 30, y = 46;
      const x0 = padL, x1 = W - padR;
      // round away binary-float noise so labels/values read cleanly (0.6, not 0.6000000000000001)
      const round6 = (v) => parseFloat(Number(v).toFixed(6));
      const toX = (v) => x0 + (v - min) / (max - min) * (x1 - x0);
      const toV = (x) => {
        let v = min + (x - x0) / (x1 - x0) * (max - min);
        v = round6(min + Math.round((v - min) / step) * step);   // snap RELATIVE to min
        return Math.max(min, Math.min(max, v));
      };

      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'max-width:660px;background:#0b0f14;border:1px solid #30363d;border-radius:10px' });
      svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: '#8b949e', 'stroke-width': 2 }));
      // ticks
      const nSteps = Math.round((max - min) / step);
      for (let i = 0; i <= nSteps; i++) {
        const v = round6(min + i * step);              // index-based: no accumulated drift
        const k = (v - min) / major;
        const isMaj = Math.abs(k - Math.round(k)) < 1e-6;
        const t = mk('line', { x1: toX(v), y1: y - (isMaj ? 10 : 5), x2: toX(v), y2: y + (isMaj ? 10 : 5), stroke: isMaj ? '#c9d1d9' : '#495260', 'stroke-width': isMaj ? 2 : 1 });
        svg.appendChild(t);
        if (isMaj) { const lab = mk('text', { x: toX(v), y: y + 26, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'middle' }); lab.textContent = round6(v); svg.appendChild(lab); }
      }
      const marker = mk('polygon', { points: '', fill: '#4f8df7', stroke: '#fff', 'stroke-width': 1, style: 'cursor:grab' });
      const target = mk('polygon', { points: '', fill: '#22c55e', opacity: 0 });
      svg.appendChild(target); svg.appendChild(marker);
      const readout = mk('text', { x: W / 2, y: 16, fill: '#e6edf3', 'font-size': 14, 'text-anchor': 'middle', 'font-weight': 700 });
      svg.appendChild(readout);
      host.appendChild(svg);

      let value = null;
      function tri(x) { return `${x},${y - 14} ${x - 7},${y - 26} ${x + 7},${y - 26}`; }
      function setV(v) { value = v; marker.setAttribute('points', tri(toX(v))); readout.textContent = v; }

      function pointerV(ev) {
        const r = svg.getBoundingClientRect();
        const px = (ev.touches ? ev.touches[0].clientX : ev.clientX) - r.left;
        return toV(px / r.width * W);
      }
      let dragging = false;
      function down(ev) { dragging = true; setV(pointerV(ev)); ev.preventDefault(); }
      function move(ev) { if (dragging) setV(pointerV(ev)); }
      function up() { dragging = false; }
      svg.addEventListener('mousedown', down); svg.addEventListener('mousemove', move);
      window.addEventListener('mouseup', up);
      svg.addEventListener('touchstart', down); svg.addEventListener('touchmove', move); window.addEventListener('touchend', up);

      host.__getValue = () => value;
      host.__feedback = (res) => {
        const ev = Number(res.expected);
        if (!isNaN(ev)) { target.setAttribute('points', tri(toX(ev))); target.setAttribute('opacity', 0.85); }
        marker.setAttribute('fill', res.correct ? '#22c55e' : '#f85149');
      };
    }
  };
})();
