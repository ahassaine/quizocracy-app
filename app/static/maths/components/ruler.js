/* ruler — read a measuring instrument, type the reading. value = typed string.
 * spec: { mode: "length" | "mass" | "capacity", value, max, unit, answer_unit }
 *   length   — horizontal ruler 0..max (cm or mm), drawn at the card's real width; numbered every
 *              1 cm / 10 mm (fewer when they would not fit), with mm or half-cm minor ticks;
 *              coloured pencil/bar from 0 to `value`.
 *   mass     — circular dial 0..max (g/kg), numbered gradations, needle at `value`.
 *   capacity — measuring jug 0..max (ml), gradation lines, liquid up to `value`.
 * The pupil reads the instrument and types the reading into a .m-input box. The box is labelled with
 * `answer_unit` when the question asks in another unit than the instrument's ("in millimetres" on a cm
 * ruler, kg on a gram dial); "" or "tenths" for a count.
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

  const NICE = CANDS.filter(s => Math.abs(s / Math.pow(10, Math.floor(Math.log10(s) + 1e-9)) - 2.5) > 1e-6);   // 1-2-5 steps first; 2.5/25/250 only if needed

  /* Choose a minor gradation that (a) `value` lands exactly on, (b) divides `max`,
   * (c) gives at least 5 intervals (so the reading is never the only mark between 0 and max)
   * and (d) not more than maxTicks; then the most labels (2..10) that fit as a multiple of it.
   * When nothing fits the value, the scale still gets 10..maxTicks gradations and the value
   * sits between two of them (fine for "read, then round"). */
  function chooseSteps(max, value, maxTicks) {
    maxTicks = maxTicks || 50;
    const fits = (s, needValue) => max / s <= maxTicks && max / s >= 5 && divides(max, s) && (!needValue || divides(value, s));
    let minor = null;
    for (const list of [NICE, CANDS]) {
      for (let i = list.length - 1; i >= 0 && minor == null; i--) if (fits(list[i], true)) minor = list[i];
      if (minor != null) break;
    }
    if (minor == null) {                       // about 20 gradations, the value between two of them
      const ok = NICE.filter(s => fits(s, false));
      if (ok.length) minor = ok.reduce((a, b) => Math.abs(max / b - 20) < Math.abs(max / a - 20) ? b : a);
    }
    if (minor == null) minor = max / 10;
    let major = minor;
    const majors = [1, 2, 4, 5, 10].map(k => minor * k).filter(m => divides(max, m) && max / m <= 10 && max / m >= 2);
    if (majors.length) major = majors.find(m => NICE.some(c => Math.abs(c - m) < 1e-9)) || majors[0];
    if (major === minor && max / major > 10) major = minor * Math.ceil(max / minor / 10);
    return { minor, major };
  }
  // a number drawn over a needle, liquid or surface line keeps a dark outline so it stays readable
  const HALO = { stroke: BG, 'stroke-width': 4, 'paint-order': 'stroke', 'stroke-linejoin': 'round' };

  function svgEl(W, H, maxW) {
    return mk('svg', {
      viewBox: `0 0 ${W} ${H}`, width: '100%',
      style: `max-width:${maxW || 520}px;background:${BG};border:1px solid ${LINE};border-radius:10px;display:block;margin:0 auto;touch-action:manipulation`
    });
  }

  /* ---------------------------------------------------------------- length */
  function drawLength(spec, width) {
    const max = spec.max ?? 10, value = spec.value ?? 0;
    const mm = (spec.unit || 'cm') === 'mm';
    const W = Math.max(280, Math.min(640, Math.floor(width || 640))), H = 170;
    const padL = 22, padR = 22;
    const x0 = padL, x1 = W - padR;
    const yTop = 86, yBot = 160;               // ruler body
    const toX = (v) => x0 + (v / max) * (x1 - x0);
    const px = (x1 - x0) / max;                // CSS px per unit (the svg is drawn 1:1)

    const svg = svgEl(W, H, W);
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

    // a real ruler: numbered every cm (every 10 mm), a long tick at each cm, a middle tick at each half,
    // and mm ticks when they are at least 3 px apart; numbering thins out (2, 5 … cm) when numbers would touch
    const cm = mm ? 10 : 1;                    // units per centimetre
    const pxCm = px * cm;
    const sub = pxCm >= 30 ? 10 : (pxCm >= 8 ? 2 : 1);        // ticks per cm
    const FS = 13, labW = String(max).length * FS * 0.62 + 6;
    let every = 1;
    for (const k of [1, 2, 5, 10, 20]) { every = k; if (pxCm * k >= labW) break; }
    const nT = Math.round(max / cm * sub);
    for (let i = 0; i <= nT; i++) {
      const v = i * cm / sub;
      const whole = i % sub === 0, half = sub % 2 === 0 && i % (sub / 2) === 0;
      const x = toX(v);
      svg.appendChild(mk('line', {
        x1: x, y1: yTop, x2: x, y2: yTop + (whole ? 24 : half ? 16 : 9),
        stroke: whole ? '#c9d1d9' : FAINT, 'stroke-width': whole ? 2 : 1
      }));
      const c = Math.round(i / sub);
      if (whole && c % every === 0) svg.appendChild(mk('text', { x: x, y: yTop + 42, fill: INK, 'font-size': FS, 'text-anchor': 'middle' }, fmt(v)));
    }
    svg.appendChild(mk('text', { x: x1 + 6, y: yBot - 6, fill: DIM, 'font-size': 12, 'text-anchor': 'end' }, spec.unit || 'cm'));
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
    const labels = [];
    for (let i = 0; i <= nMinor; i++) {
      const v = i * minor;
      const isMaj = divides(v, major);
      const [x1, y1] = pt(v, R);
      const [x2, y2] = pt(v, R - (isMaj ? 24 : 12));
      svg.appendChild(mk('line', { x1, y1, x2, y2, stroke: isMaj ? '#c9d1d9' : '#6e7681', 'stroke-width': isMaj ? 3 : 1.2 }));
      if (isMaj) {
        const [lx, ly] = pt(v, R - 44);
        labels.push(mk('text', Object.assign({ x: lx, y: ly + 5, fill: INK, 'font-size': 16, 'font-weight': 600, 'text-anchor': 'middle' }, HALO), fmt(v)));
      }
    }

    // needle (under the numbers, which keep a dark outline, so the one it points at stays readable)
    const [nx, ny] = pt(value, R - 30);
    const [tx, ty] = pt(value, -26);           // short counterweight tail
    svg.appendChild(mk('line', { x1: tx, y1: ty, x2: nx, y2: ny, stroke: BAD, 'stroke-width': 4, 'stroke-linecap': 'round' }));
    labels.forEach(t => svg.appendChild(t));
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
        stroke: isMaj ? '#e6edf3' : '#c9d1d9', 'stroke-width': isMaj ? 2 : 1.2
      }));
      if (isMaj) svg.appendChild(mk('text', Object.assign({ x: jx + jw - len - 8, y: y + 5, fill: INK, 'font-size': 15, 'text-anchor': 'end' }, HALO), fmt(v)));
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
      const boxUnit = spec.answer_unit != null ? spec.answer_unit : unit;   // the unit the question asks for

      let svg;
      if (mode === 'mass') svg = drawMass(spec);
      else if (mode === 'capacity') svg = drawCapacity(spec);
      else svg = drawLength(spec, host.getBoundingClientRect().width);
      host.appendChild(svg);

      // typed answer + unit suffix
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:14px;display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap';

      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = spec.keypad || 'decimal';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', boxUnit ? 'Your answer in ' + boxUnit : 'Your answer');
      input.style.cssText = `font-size:1.3rem;padding:8px 12px;width:140px;background:${BG};color:${INK};border:2px solid ${LINE};border-radius:8px;text-align:center;outline:none`;
      input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
      input.addEventListener('blur', () => { input.style.borderColor = LINE; });
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); }
      });

      const suffix = document.createElement('span');
      suffix.textContent = boxUnit;
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
