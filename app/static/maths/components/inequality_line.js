/* inequality_line — number line showing a single linear inequality.
 * spec: { op: "<"|"<="|">"|">=", value, min, max }
 * OPEN circle at value for strict </> ; CLOSED (filled) for <=/>= .
 * Bold accent ray + arrowhead: LEFT for </<= , RIGHT for >/>= .
 * Pupil types their answer in the input; __getValue() returns the trimmed string.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["inequality_line"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const op = spec.op || '<';
      const value = spec.value ?? 0;
      const min = spec.min ?? 0, max = spec.max ?? 10;
      const strict = (op === '<' || op === '>');
      const pointsRight = (op === '>' || op === '>=');

      const W = 640, H = 90, padL = 34, padR = 34, y = 46;
      const x0 = padL, x1 = W - padR;
      const round6 = (v) => parseFloat(Number(v).toFixed(6));
      const span = (max - min) || 1;
      const toX = (v) => x0 + (v - min) / span * (x1 - x0);

      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', style: 'max-width:460px;background:#0b0f14;border:1px solid #30363d;border-radius:10px' });

      // base line
      svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: '#8b949e', 'stroke-width': 2 }));

      // integer ticks + labels
      const lo = Math.ceil(min), hi = Math.floor(max);
      for (let v = lo; v <= hi; v++) {
        svg.appendChild(mk('line', { x1: toX(v), y1: y - 8, x2: toX(v), y2: y + 8, stroke: '#c9d1d9', 'stroke-width': 2 }));
        const lab = mk('text', { x: toX(v), y: y + 26, fill: '#8b949e', 'font-size': 12, 'text-anchor': 'middle' });
        lab.textContent = round6(v);
        svg.appendChild(lab);
      }

      // ray from the circle to the correct end
      const cx = toX(value);
      const endX = pointsRight ? x1 : x0;
      const dir = pointsRight ? 1 : -1;
      const tipX = endX;                       // arrowhead tip at the end of the line
      const shaftEnd = tipX - dir * 12;        // stop shaft short so head sits on top
      svg.appendChild(mk('line', { x1: cx, y1: y, x2: shaftEnd, y2: y, stroke: '#4f8df7', 'stroke-width': 5, 'stroke-linecap': 'round' }));

      // arrowhead (triangle) pointing outward
      const hw = 8;  // half-height
      svg.appendChild(mk('polygon', {
        points: `${tipX},${y} ${tipX - dir * 14},${y - hw} ${tipX - dir * 14},${y + hw}`,
        fill: '#4f8df7'
      }));

      // circle at value: OPEN (unfilled) for strict, CLOSED (filled) otherwise
      svg.appendChild(mk('circle', {
        cx: cx, cy: y, r: 7,
        fill: strict ? '#0b0f14' : '#4f8df7',
        stroke: '#4f8df7', 'stroke-width': 3
      }));

      host.appendChild(svg);

      // typed input
      const inp = document.createElement('input');
      inp.type = 'text';
      inp.className = 'm-input';
      if (spec.placeholder) inp.placeholder = spec.placeholder;
      inp.style.cssText = 'display:block;margin-top:10px;width:100%;max-width:460px;box-sizing:border-box;padding:8px 10px;background:#0b0f14;border:1px solid #30363d;border-radius:8px;color:#e6edf3;font-size:15px';
      inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); api.submit && api.submit(); } });
      host.appendChild(inp);

      host.__getValue = () => inp.value.trim();
      host.__feedback = (res) => {
        inp.style.borderColor = res.correct ? '#22c55e' : '#f85149';
      };
    }
  };
})();
