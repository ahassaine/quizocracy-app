/* pie_chart — read a pie chart, type an answer. value = typed string.
 * spec: { slices: [["Blue",25],["Red",50],...],
 *         showAngles: false, showPercents: false, highlight: i, mode:"read",
 *         valueUnit?: "%" | "°" | "" }
 * Sectors are true SVG arcs: each central angle = (value / total) * 360°.
 * Values that add up to 100 are percentages and values that add up to 360 are degrees (either way the
 * label is exactly true); they get "%" / "°" and no "Total =" line, which would contradict the story.
 * Drawn at the host's real width (1 viewBox unit = 1 CSS px) so the legend stays readable on a phone.
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
  // trim trailing zeros: 90 -> "90", 22.5 -> "22.5"; thousands commas
  function num(v, dp) {
    const r = Number(v.toFixed(dp == null ? 1 : dp));
    return Math.abs(r) >= 1000 ? r.toLocaleString('en-GB', { maximumFractionDigits: 6 }) : String(r);
  }

  // A slice named after a colour is drawn in that colour; the rest take palette colours not already used.
  const NAMED = { red: '#ef4444', blue: '#3b82f6', green: '#22c55e', yellow: '#facc15', orange: '#f97316',
                  purple: '#a855f7', pink: '#f472b6', brown: '#a0522d', black: '#000000', white: '#ffffff',
                  grey: '#9ca3af', gray: '#9ca3af', gold: '#d4a017', silver: '#c0c0c0' };
  const PALETTE = [['blue', '#4f8df7'], ['green', '#22c55e'], ['yellow', '#e3b341'], ['red', '#f85149'], ['purple', '#a371f7'],
                   ['teal', '#39c5cf'], ['pink', '#db61a2'], ['orange', '#f0883e'], ['lime', '#7ee787'], ['sky', '#79c0ff'],
                   ['peach', '#ffa657'], ['lilac', '#d2a8ff']];
  // "Red", "Light blue", "Red team" — but not "Oranges" or "Redhill"
  function colourName(label) { return (String(label).toLowerCase().match(/[a-z]+/g) || []).find(w => NAMED[w]) || null; }
  function fills(labels) {
    const named = labels.map(colourName), used = new Set(named.filter(Boolean).map(c => c === 'gray' ? 'grey' : c));
    const free = PALETTE.filter(p => !used.has(p[0]));
    let j = 0;
    return named.map(c => c ? NAMED[c] : (free.length ? free : PALETTE)[j++ % (free.length || PALETTE.length)][1]);
  }
  function dark(hex) {      // text on this fill should be light
    const v = parseInt(hex.slice(1), 16), r = v >> 16, g = (v >> 8) & 255, b = v & 255;
    return 0.299 * r + 0.587 * g + 0.114 * b < 110;
  }
  function hostWidth(host, max) { const w = Math.floor(host.getBoundingClientRect().width) - 2; return w > 0 ? Math.max(260, Math.min(max, w)) : max; }
  function textW(s, size) { return String(s).length * size * 0.58; }

  const INK = '#e6edf3', DIM = '#8b949e', ACCENT = '#4f8df7';
  const BG = '#0b0f14', BORDER = '#30363d';

  window.MComp["pie_chart"] = {
    render(host, spec, api) {
      host.innerHTML = '';

      // ---- data -------------------------------------------------------
      const raw = Array.isArray(spec.slices) ? spec.slices : [];
      const slices = [];
      for (const s of raw) {
        if (!s) continue;
        const label = String(Array.isArray(s) ? s[0] : (s.label != null ? s.label : ''));
        const value = Number(Array.isArray(s) ? s[1] : s.value);
        if (!isFinite(value) || value <= 0) continue;
        slices.push({ label: label, value: value });
      }
      const total = slices.reduce((a, s) => a + s.value, 0);
      const unit = typeof spec.valueUnit === 'string' ? spec.valueUnit
        : (Math.abs(total - 100) < 1e-6 ? '%' : (Math.abs(total - 360) < 1e-6 ? '°' : ''));
      const showAngles = !!spec.showAngles && unit !== '°';
      const showPercents = !!spec.showPercents && unit !== '%';
      const hi = (typeof spec.highlight === 'number' && spec.highlight >= 0 &&
                  spec.highlight < slices.length) ? spec.highlight : -1;
      const colours = fills(slices.map(s => s.label));

      if (!slices.length || total <= 0) {
        const svg = mk('svg', { viewBox: '0 0 640 120', width: '100%', role: 'img', style: 'max-width:640px;background:' + BG + ';border:1px solid ' + BORDER + ';border-radius:10px;display:block' });
        svg.appendChild(mk('text', { x: 320, y: 64, fill: DIM, 'font-size': 14, 'text-anchor': 'middle' }, 'No data'));
        host.appendChild(svg);
        addInput(host, api, spec);
        return;
      }

      // compute exact angles, start at 12 o'clock, go clockwise
      let acc = 0;
      for (const s of slices) {
        s.frac = s.value / total;
        s.angle = s.frac * 360;
        s.a0 = -90 + acc * 360;
        acc += s.frac;
        s.a1 = -90 + acc * 360;
        s.mid = (s.a0 + s.a1) / 2;
      }
      // guard float drift on the final sector
      slices[slices.length - 1].a1 = 270;
      const single = slices.length === 1 || slices[0].angle >= 359.999;
      const SMALL = 34; // degrees: a sector needs this much angle to hold its label inside; otherwise lead it out

      const draw = () => {
        // ---- geometry ---------------------------------------------------
        const W = hostWidth(host, 640);
        const leadW = Math.max(0, ...slices.filter(s => !single && s.angle < SMALL).map(s => textW(s.label, 13)));
        // small sectors are named on leader lines when there is room beside the pie; on a narrow screen the
        // legend (same colours) names them instead and the pie keeps its size
        const leaders = leadW > 0 && W / 2 - (leadW + 50) >= 80;
        const R = Math.min(118, leaders ? W / 2 - (leadW + 50) : W / 2 - 16);
        const PIE_H = 2 * R + 94;
        const legendTxt = slices.map((s, i) => {
          const bits = [];
          if (showAngles) bits.push(num(s.angle) + '°');
          if (showPercents && !(i === hi && spec.hideValue)) bits.push(num(s.frac * 100) + '%');
          const main = s.label + '  —  ' + (i === hi && spec.hideValue ? '?' : num(s.value, 2) + unit);   // the outlined value is the answer
          return { main: main, bits: bits.length ? '(' + bits.join(', ') + ')' : '' };
        });
        // legend extras sit at the right edge when there is room, else on a second line
        const twoLine = legendTxt.some(t => t.bits && textW(t.main, 14) + textW(t.bits, 14) + 90 > W);
        const rowH = twoLine ? 42 : 24;
        const legendH = 22 + slices.length * rowH;
        const H = PIE_H + legendH;
        const cx = W / 2, cy = PIE_H / 2 + 4;

        const svg = mk('svg', {
          viewBox: `0 0 ${W} ${H}`,
          width: '100%',
          role: 'img',
          style: `max-width:${W}px;box-sizing:content-box;background:` + BG + ';border:1px solid ' + BORDER +
                 ';border-radius:10px;display:block'
        });
        svg.appendChild(mk('title', {}, 'Pie chart'));

        const pt = (ang, rad) => {
          const t = ang * Math.PI / 180;
          return [cx + rad * Math.cos(t), cy + rad * Math.sin(t)];
        };

        // ---- sectors ----------------------------------------------------
        const gSect = mk('g', {});
        svg.appendChild(gSect);
        slices.forEach((s, i) => {
          const fill = colours[i];
          let node;
          if (single) {
            node = mk('circle', { cx: cx, cy: cy, r: R, fill: fill });
          } else {
            const [x0, y0] = pt(s.a0, R);
            const [x1, y1] = pt(s.a1, R);
            const large = s.angle > 180 ? 1 : 0;
            const d = `M ${cx} ${cy} L ${x0.toFixed(3)} ${y0.toFixed(3)} ` +
                      `A ${R} ${R} 0 ${large} 1 ${x1.toFixed(3)} ${y1.toFixed(3)} Z`;
            node = mk('path', { d: d, fill: fill });
          }
          // a black sector would vanish into the background: give the dark ones a light edge
          node.setAttribute('stroke', dark(fill) ? '#8b949e' : BG);
          node.setAttribute('stroke-width', 2);
          gSect.appendChild(node);
        });

        // highlight outline drawn last so it sits above neighbouring edges
        if (hi >= 0) {
          const s = slices[hi];
          let out;
          if (single) {
            out = mk('circle', { cx: cx, cy: cy, r: R });
          } else {
            const [x0, y0] = pt(s.a0, R);
            const [x1, y1] = pt(s.a1, R);
            const large = s.angle > 180 ? 1 : 0;
            out = mk('path', {
              d: `M ${cx} ${cy} L ${x0.toFixed(3)} ${y0.toFixed(3)} ` +
                 `A ${R} ${R} 0 ${large} 1 ${x1.toFixed(3)} ${y1.toFixed(3)} Z`
            });
          }
          out.setAttribute('fill', 'none');
          out.setAttribute('stroke', ACCENT);
          out.setAttribute('stroke-width', 5);
          out.setAttribute('stroke-linejoin', 'round');
          svg.appendChild(out);
        }

        // outer rim so a 100% pie still reads as a circle
        if (single) {
          svg.appendChild(mk('circle', { cx: cx, cy: cy, r: R, fill: 'none', stroke: BORDER, 'stroke-width': 1 }));
        }

        // ---- in-sector / leader labels ----------------------------------
        const leadersL = [], leadersR = [];
        slices.forEach((s, i) => {
          const txt = s.label;
          if (!txt) return;
          if (single || s.angle >= SMALL) {
            const [lx, ly] = pt(s.mid, single ? 0 : R * 0.62);
            const lightTxt = dark(colours[i]);
            svg.appendChild(mk('text', {
              x: lx, y: ly + 5, fill: lightTxt ? '#ffffff' : '#0b0f14', 'font-size': 14, 'font-weight': 700,
              'text-anchor': 'middle', 'paint-order': 'stroke',
              stroke: lightTxt ? 'rgba(0,0,0,0.6)' : 'rgba(255,255,255,0.55)', 'stroke-width': 3, 'stroke-linejoin': 'round'
            }, txt));
          } else if (leaders) {
            (Math.cos(s.mid * Math.PI / 180) >= 0 ? leadersR : leadersL).push(s);
          }
        });

        // stack leader labels vertically on their side so they never collide
        function placeLeaders(list, right) {
          if (!list.length) return;
          list.sort((a, b) => a.mid - b.mid);
          const step = 22;
          let ys = list.map(s => pt(s.mid, R + 26)[1]);
          // de-overlap downward, then clamp back into the pie band
          for (let i = 1; i < ys.length; i++) if (ys[i] - ys[i - 1] < step) ys[i] = ys[i - 1] + step;
          const over = ys[ys.length - 1] - (PIE_H - 12);
          if (over > 0) for (let i = 0; i < ys.length; i++) ys[i] -= over;
          if (ys[0] < 16) { const d = 16 - ys[0]; for (let i = 0; i < ys.length; i++) ys[i] += d; }

          list.forEach((s, i) => {
            const [ax, ay] = pt(s.mid, R + 2);
            const [bx, by] = pt(s.mid, R + 22);
            const ty = ys[i];
            const tx = right ? cx + R + 34 : cx - R - 34;
            const elbowX = right ? tx - 10 : tx + 10;
            const poly = `${ax.toFixed(2)},${ay.toFixed(2)} ${bx.toFixed(2)},${by.toFixed(2)} ` +
                         `${elbowX},${ty} ${tx},${ty}`;
            svg.appendChild(mk('polyline', {
              points: poly, fill: 'none', stroke: DIM, 'stroke-width': 1.5
            }));
            svg.appendChild(mk('text', {
              x: right ? tx + 6 : tx - 6, y: ty + 4, fill: INK, 'font-size': 13,
              'text-anchor': right ? 'start' : 'end'
            }, s.label));
          });
        }
        placeLeaders(leadersR, true);
        placeLeaders(leadersL, false);

        // ---- legend -----------------------------------------------------
        const legY = PIE_H + 4;
        svg.appendChild(mk('line', { x1: 16, y1: legY, x2: W - 16, y2: legY, stroke: '#21262d', 'stroke-width': 1 }));
        slices.forEach((s, i) => {
          const y = legY + 22 + i * rowH;
          const g = mk('g', {});
          g.appendChild(mk('rect', {
            x: 18, y: y - 11, width: 14, height: 14, rx: 3,
            fill: colours[i],
            stroke: i === hi ? ACCENT : (dark(colours[i]) ? '#8b949e' : 'none'), 'stroke-width': i === hi ? 2.5 : 1
          }));
          g.appendChild(mk('text', {
            x: 42, y: y + 1, fill: i === hi ? ACCENT : INK, 'font-size': 14,
            'font-weight': i === hi ? 700 : 400
          }, legendTxt[i].main));
          if (legendTxt[i].bits) {
            g.appendChild(mk('text', twoLine ? { x: 42, y: y + 19, fill: DIM, 'font-size': 14 }
              : { x: W - 18, y: y + 1, fill: DIM, 'font-size': 14, 'text-anchor': 'end' }, legendTxt[i].bits));
          }
          svg.appendChild(g);
        });
        return svg;
      };
      let svg = draw();
      host.appendChild(svg);
      if (window.ResizeObserver) {                     // phone turned, window resized: redraw at the new width
        let lastW = host.getBoundingClientRect().width;
        new ResizeObserver(() => { const w = host.getBoundingClientRect().width; if (w > 0 && Math.abs(w - lastW) > 8 && svg.parentNode === host) { lastW = w; const s = draw(); host.replaceChild(s, svg); svg = s; } }).observe(host);
      }

      // total line (helps when values don't sum to 100); not for percentages or degrees, where it reads as a count
      if (!unit) {
        const meta = document.createElement('div');
        meta.style.cssText = 'margin-top:8px;color:#8b949e;font-size:0.9rem';
        meta.textContent = 'Total = ' + num(total, 2);
        host.appendChild(meta);
      }

      addInput(host, api, spec);
    }
  };

  // typed answer: a digit pad only for whole-number answers; words, fractions and decimals need a full keyboard
  function addInput(host, api, spec) {
    const wrap = document.createElement('div');
    wrap.style.cssText = 'margin-top:12px';
    const input = document.createElement('input');
    input.type = 'text';
    input.inputMode = spec && spec.keypad || 'text';
    input.className = 'm-input';
    input.autocomplete = 'off';
    input.setAttribute('autocapitalize', 'off');
    input.setAttribute('aria-label', 'Your answer');
    input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:160px;max-width:100%;' +
      'background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;' +
      'text-align:center;outline:none';
    input.addEventListener('focus', () => { input.style.borderColor = '#4f8df7'; });
    input.addEventListener('blur', () => { input.style.borderColor = '#30363d'; });
    input.addEventListener('keydown', (ev) => {
      if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); }
    });
    wrap.appendChild(input);
    host.appendChild(wrap);

    host.__getValue = () => input.value.trim();
    host.__feedback = (res) => { input.style.borderColor = res && res.correct ? '#22c55e' : '#f85149'; };
  }
})();
