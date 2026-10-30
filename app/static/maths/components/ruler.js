/* ruler — read a measuring instrument, type the reading. value = typed string.
 * spec: { mode: "length" | "mass" | "capacity", value, max, unit }
 *   length   — horizontal ruler 0..max (cm), majors+numbers every 1 unit,
 *              minors at halves, coloured pencil/bar from 0 to `value`.
 *   mass     — circular dial 0..max (g/kg), numbered gradations, needle at `value`.
 *   capacity — measuring jug 0..max (ml), gradation lines, liquid up to `value`.
 * The pupil reads the instrument and types the reading into a .m-input box.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  const INK = '#e6edf3', DIM = '#8b949e', FAINT = '#495260', LINE = '#30363d';
  const ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149', BG = '#0b0f14';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }
  function fmt(v) {
    const r = Math.round(v * 1000) / 1000;
    return String(r);
  }
  const CANDS = [0.01, 0.02, 0.025, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000];
  function divides(v, s) { const q = v / s; return Math.abs(q - Math.round(q)) < 1e-6; }

  /* Choose a minor gradation that (a) `value` lands exactly on, (b) divides `max`,
   * and (c) yields a readable number of ticks; then a major that is a multiple of it. */
  function chooseSteps(max, value, maxTicks) {
    maxTicks = maxTicks || 50;
    let minor = null;
    for (let i = CANDS.length - 1; i >= 0; i--) {
      const s = CANDS[i];
      if (max / s > maxTicks) continue;
      if (!divides(max, s)) continue;
      if (!divides(value, s)) continue;
      minor = s; break;
    }
    if (minor == null) {
      // fall back: something safe that at least divides max
      for (let i = CANDS.length - 1; i >= 0; i--) {
        const s = CANDS[i];
        if (max / s <= maxTicks && divides(max, s)) { minor = s; break; }
      }
    }
    if (minor == null) minor = max / 10;
    let major = minor;
    for (const k of [10, 5, 4, 2, 1]) {
      const m = minor * k;
      if (divides(max, m) && max / m <= 12 && max / m >= 2) { major = m; break; }
    }
    if (major === minor && max / major > 12) major = minor * Math.ceil(max / minor / 10);
    return { minor, major };
  }

  function svgEl(W, H, maxW) {
    return mk('svg', {
      viewBox: `0 0 ${W} ${H}`, width: '100%',
      style: `max-width:${maxW || 520}px;background:${BG};border:1px solid ${LINE};border-radius:10px;display:block;margin:0 auto;touch-action:manipulation`
    });
  }

  /* ---------------------------------------------------------------- length */
  function drawLength(spec) {
    const max = spec.max ?? 10, value = spec.value ?? 0;
    const W = 640, H = 210;
    const padL = 34, padR = 34;
    const x0 = padL, x1 = W - padR;
    const yTop = 96, yBot = 186;               // ruler body
    const toX = (v) => x0 + (v / max) * (x1 - x0);

    const svg = svgEl(W, H);
    // pencil / bar being measured, sitting above the ruler
    const barY = 46, barH = 30;
    const bx = toX(value);
    const bodyEnd = Math.max(x0 + 2, bx - 18);
    svg.appendChild(mk('rect', { x: x0, y: barY, width: Math.max(0, bodyEnd - x0), height: barH, fill: ACCENT, rx: 3 }));
    // pencil tip
    svg.appendChild(mk('polygon', { points: `${bodyEnd},${barY} ${bx},${barY + barH / 2} ${bodyEnd},${barY + barH}`, fill: '#e3b341' }));
    // guide lines down to the ruler
    svg.appendChild(mk('line', { x1: x0, y1: barY - 6, x2: x0, y2: yTop, stroke: FAINT, 'stroke-width': 1, 'stroke-dasharray': '4 4' }));
    svg.appendChild(mk('line', { x1: bx, y1: barY - 6, x2: bx, y2: yTop, stroke: FAINT, 'stroke-width': 1, 'stroke-dasharray': '4 4' }));

    // ruler body
    svg.appendChild(mk('rect', { x: x0 - 14, y: yTop, width: (x1 - x0) + 28, height: yBot - yTop, fill: '#161b22', stroke: DIM, 'stroke-width': 2, rx: 4 }));

    for (let i = 0; i <= max * 2 + 1e-9; i++) {
      const v = i / 2;
      const isMaj = i % 2 === 0;
      const x = toX(v);
      svg.appendChild(mk('line', {
        x1: x, y1: yTop, x2: x, y2: yTop + (isMaj ? 26 : 14),
        stroke: isMaj ? '#c9d1d9' : FAINT, 'stroke-width': isMaj ? 2 : 1
      }));
      if (isMaj) svg.appendChild(mk('text', { x: x, y: yTop + 46, fill: INK, 'font-size': 15, 'text-anchor': 'middle' }, fmt(v)));
    }
    svg.appendChild(mk('text', { x: x1 + 6, y: yBot - 8, fill: DIM, 'font-size': 13, 'text-anchor': 'end' }, spec.unit || 'cm'));
    return svg;
  }

  /* ------------------------------------------------------------------ mass */
  function drawMass(spec) {
    const max = spec.max ?? 1000, value = spec.value ?? 0;
    const { minor, major } = chooseSteps(max, value, 60);
    const W = 520, H = 470;
    const cx = W / 2, cy = 232, R = 190;
    const START = 135, SWEEP = 270;            // degrees, clockwise, SVG coords
    const ang = (v) => (START + (v / max) * SWEEP) * Math.PI / 180;
    const pt = (v, r) => [cx + r * Math.cos(ang(v)), cy + r * Math.sin(ang(v))];

    const svg = svgEl(W, H);
    svg.appendChild(mk('circle', { cx, cy, r: R + 22, fill: '#161b22', stroke: LINE, 'stroke-width': 2 }));
    svg.appendChild(mk('circle', { cx, cy, r: R + 4, fill: BG, stroke: DIM, 'stroke-width': 2 }));

    // arc of the scale
    const [ax, ay] = pt(0, R), [bx, by] = pt(max, R);
    svg.appendChild(mk('path', { d: `M ${ax} ${ay} A ${R} ${R} 0 1 1 ${bx} ${by}`, fill: 'none', stroke: DIM, 'stroke-width': 2 }));

    const nMinor = Math.round(max / minor);
    for (let i = 0; i <= nMinor; i++) {
      const v = i * minor;
      const isMaj = divides(v, major);
      const [x1, y1] = pt(v, R);
      const [x2, y2] = pt(v, R - (isMaj ? 24 : 12));
      svg.appendChild(mk('line', { x1, y1, x2, y2, stroke: isMaj ? '#c9d1d9' : FAINT, 'stroke-width': isMaj ? 3 : 1 }));
      if (isMaj) {
        const [lx, ly] = pt(v, R - 44);
        svg.appendChild(mk('text', { x: lx, y: ly + 5, fill: INK, 'font-size': 16, 'font-weight': 600, 'text-anchor': 'middle' }, fmt(v)));
      }
    }

    // needle
    const [nx, ny] = pt(value, R - 30);
    const [tx, ty] = pt(value, -26);           // short counterweight tail
    svg.appendChild(mk('line', { x1: tx, y1: ty, x2: nx, y2: ny, stroke: BAD, 'stroke-width': 4, 'stroke-linecap': 'round' }));
    svg.appendChild(mk('circle', { cx, cy, r: 12, fill: '#161b22', stroke: '#c9d1d9', 'stroke-width': 2 }));
    svg.appendChild(mk('circle', { cx, cy, r: 4, fill: BAD }));
    svg.appendChild(mk('text', { x: cx, y: cy + 74, fill: DIM, 'font-size': 18, 'text-anchor': 'middle', 'font-weight': 600 }, spec.unit || 'g'));
    return svg;
  }

  /* -------------------------------------------------------------- capacity */
  function drawCapacity(spec) {
    const max = spec.max ?? 1000, value = spec.value ?? 0;
    const { minor, major } = chooseSteps(max, value, 40);
    const W = 420, H = 470;
    const jx = 118, jw = 200;                  // jug body
    const yTop = 66, yBot = 410;
    const toY = (v) => yBot - (v / max) * (yBot - yTop);

    const svg = svgEl(W, H, 400);

    // liquid
    const ly = toY(value);
    svg.appendChild(mk('rect', { x: jx + 3, y: ly, width: jw - 6, height: Math.max(0, yBot - ly - 3), fill: ACCENT, opacity: 0.55 }));
    svg.appendChild(mk('line', { x1: jx + 3, y1: ly, x2: jx + jw - 3, y2: ly, stroke: ACCENT, 'stroke-width': 3 }));

    // jug walls + base + spout + handle
    svg.appendChild(mk('path', {
      d: `M ${jx} ${yTop - 22} L ${jx} ${yBot} L ${jx + jw} ${yBot} L ${jx + jw} ${yTop - 22}`,
      fill: 'none', stroke: '#c9d1d9', 'stroke-width': 3, 'stroke-linejoin': 'round'
    }));
    svg.appendChild(mk('path', { d: `M ${jx} ${yTop - 22} L ${jx - 26} ${yTop - 40}`, fill: 'none', stroke: '#c9d1d9', 'stroke-width': 3 }));
    svg.appendChild(mk('path', {
      d: `M ${jx + jw} ${yTop + 20} q 52 40 0 130`, fill: 'none', stroke: '#c9d1d9', 'stroke-width': 6, 'stroke-linecap': 'round'
    }));

    // gradations (drawn from the right wall inwards, labels to the right of the jug)
    const nMinor = Math.round(max / minor);
    for (let i = 0; i <= nMinor; i++) {
      const v = i * minor;
      const isMaj = divides(v, major);
      const y = toY(v);
      const len = isMaj ? 62 : 30;
      svg.appendChild(mk('line', {
        x1: jx + jw - len, y1: y, x2: jx + jw - 3, y2: y,
        stroke: isMaj ? '#c9d1d9' : FAINT, 'stroke-width': isMaj ? 2 : 1
      }));
      if (isMaj) svg.appendChild(mk('text', { x: jx + jw - len - 8, y: y + 5, fill: INK, 'font-size': 15, 'text-anchor': 'end' }, fmt(v)));
    }
    svg.appendChild(mk('text', { x: W / 2, y: yBot + 40, fill: DIM, 'font-size': 16, 'text-anchor': 'middle', 'font-weight': 600 }, spec.unit || 'ml'));
    return svg;
  }

  window.MComp["ruler"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      spec = spec || {};
      const mode = spec.mode || 'length';
      const unit = spec.unit || (mode === 'length' ? 'cm' : mode === 'mass' ? 'g' : 'ml');

      let svg;
      if (mode === 'mass') svg = drawMass(spec);
      else if (mode === 'capacity') svg = drawCapacity(spec);
      else svg = drawLength(spec);
      host.appendChild(svg);

      // typed answer + unit suffix
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:14px;display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap';

      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'decimal';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your reading in ' + unit);
      input.style.cssText = `font-size:1.3rem;padding:8px 12px;width:140px;background:${BG};color:${INK};border:2px solid ${LINE};border-radius:8px;text-align:center;outline:none`;
      input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
      input.addEventListener('blur', () => { input.style.borderColor = LINE; });
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); }
      });

      const suffix = document.createElement('span');
      suffix.textContent = unit;
      suffix.style.cssText = `color:${DIM};font-size:1.15rem;font-weight:600`;

      wrap.appendChild(input); wrap.appendChild(suffix);
      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => {
        input.style.borderColor = res && res.correct ? GOOD : BAD;
      };
    }
  };
})();
