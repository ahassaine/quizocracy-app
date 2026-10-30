/* pie_chart — read a pie chart, type an answer. value = typed string.
 * spec: { slices: [["Blue",25],["Red",50],...],
 *         showAngles: false, showPercents: false, highlight: i, mode:"read" }
 * Sectors are true SVG arcs: each central angle = (value / total) * 360°.
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
  // trim trailing zeros: 90 -> "90", 22.5 -> "22.5"
  function num(v, dp) {
    const r = Number(v.toFixed(dp == null ? 1 : dp));
    return String(r);
  }

  const PALETTE = ['#4f8df7', '#22c55e', '#e3b341', '#f85149', '#a371f7',
                   '#39c5cf', '#db61a2', '#f0883e', '#7ee787', '#79c0ff',
                   '#ffa657', '#d2a8ff'];
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
      const showAngles = !!spec.showAngles;
      const showPercents = !!spec.showPercents;
      const hi = (typeof spec.highlight === 'number' && spec.highlight >= 0 &&
                  spec.highlight < slices.length) ? spec.highlight : -1;

      // ---- geometry ---------------------------------------------------
      const legendRows = slices.length;
      const legendH = 22 + legendRows * 24;
      const PIE_H = 330;
      const W = 640;
      const H = PIE_H + legendH;
      const cx = W / 2, cy = PIE_H / 2 + 4, R = 118;

      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`,
        width: '100%',
        role: 'img',
        style: 'max-width:660px;background:' + BG + ';border:1px solid ' + BORDER +
               ';border-radius:10px;display:block'
      });
      svg.appendChild(mk('title', {}, 'Pie chart'));

      if (!slices.length || total <= 0) {
        svg.appendChild(mk('text', { x: cx, y: cy, fill: DIM, 'font-size': 14, 'text-anchor': 'middle' }, 'No data'));
        host.appendChild(svg);
        addInput(host, api);
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

      const pt = (ang, rad) => {
        const t = ang * Math.PI / 180;
        return [cx + rad * Math.cos(t), cy + rad * Math.sin(t)];
      };

      // ---- sectors ----------------------------------------------------
      const gSect = mk('g', {});
      svg.appendChild(gSect);
      const single = slices.length === 1 || slices[0].angle >= 359.999;

      slices.forEach((s, i) => {
        const fill = PALETTE[i % PALETTE.length];
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
        node.setAttribute('stroke', BG);
        node.setAttribute('stroke-width', 2);
        s.node = node;
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
      // A sector needs enough angle to hold text inside; otherwise lead it out.
      const SMALL = 34; // degrees
      const leadersL = [], leadersR = [];
      slices.forEach((s, i) => {
        const txt = s.label;
        if (!txt) return;
        if (single || s.angle >= SMALL) {
          const [lx, ly] = pt(s.mid, single ? 0 : R * 0.62);
          const t = mk('text', {
            x: lx, y: ly + 4, fill: '#0b0f14', 'font-size': 14, 'font-weight': 700,
            'text-anchor': 'middle', 'paint-order': 'stroke',
            stroke: 'rgba(255,255,255,0.55)', 'stroke-width': 3, 'stroke-linejoin': 'round'
          }, txt);
          svg.appendChild(t);
        } else {
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
          const tx = right ? cx + R + 52 : cx - R - 52;
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
      svg.appendChild(mk('line', { x1: 24, y1: legY, x2: W - 24, y2: legY, stroke: '#21262d', 'stroke-width': 1 }));
      slices.forEach((s, i) => {
        const y = legY + 22 + i * 24;
        const g = mk('g', {});
        g.appendChild(mk('rect', {
          x: 30, y: y - 11, width: 14, height: 14, rx: 3,
          fill: PALETTE[i % PALETTE.length],
          stroke: i === hi ? ACCENT : 'none', 'stroke-width': i === hi ? 2.5 : 0
        }));
        const bits = [];
        if (showAngles) bits.push(num(s.angle) + '°');
        if (showPercents) bits.push(num(s.frac * 100) + '%');
        const main = s.label + '  —  ' + num(s.value, 2);
        g.appendChild(mk('text', {
          x: 54, y: y + 1, fill: i === hi ? ACCENT : INK, 'font-size': 14,
          'font-weight': i === hi ? 700 : 400
        }, main));
        if (bits.length) {
          g.appendChild(mk('text', {
            x: W - 30, y: y + 1, fill: DIM, 'font-size': 14, 'text-anchor': 'end'
          }, '(' + bits.join(', ') + ')'));
        }
        svg.appendChild(g);
      });

      host.appendChild(svg);

      // total line (helps when values don't sum to 100)
      const meta = document.createElement('div');
      meta.style.cssText = 'margin-top:8px;color:#8b949e;font-size:0.9rem';
      meta.textContent = 'Total = ' + num(total, 2);
      host.appendChild(meta);

      addInput(host, api);
    }
  };

  function addInput(host, api) {
    const wrap = document.createElement('div');
    wrap.style.cssText = 'margin-top:12px';
    const input = document.createElement('input');
    input.type = 'text';
    input.inputMode = 'text';
    input.className = 'm-input';
    input.autocomplete = 'off';
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
