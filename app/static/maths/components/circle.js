/* circle — a circle with one of its parts marked and labelled.
 *
 * spec:
 *   { radius:5, show:"radius" }        centre dot + marked line centre→edge
 *   { radius:5, show:"diameter" }      marked line right across through the centre
 *   { radius:5, show:"circumference" } thick accent outline + leader-line label
 *   { radius:5, show:"none" }          plain circle with a centre dot
 *   label: overrides the printed measurement text (e.g. "r = 5 cm")
 *
 * The drawn circle is a fixed comfortable pixel size — `radius` is a LABEL,
 * not a scale (it only nudges the drawn size very slightly, for sense).
 *
 * host.__getValue() === trimmed typed string.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';

  const BG = '#0b0f14', BORDER = '#30363d', INK = '#e6edf3', MUTE = '#8b949e';
  const ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }
  const r2 = (n) => Math.round(n * 100) / 100;
  const FONT = 'system-ui,sans-serif';

  function text(x, y, s, colour, size, anchor, weight) {
    return mk('text', {
      x: r2(x), y: r2(y), fill: colour, 'font-size': size || 13,
      'font-weight': weight || 700, 'text-anchor': anchor || 'middle',
      'font-family': FONT
    }, s);
  }

  window.MComp["circle"] = {
    render(host, spec, api) {
      host.innerHTML = '';

      let rv = Number(spec.radius);
      if (!isFinite(rv) || rv <= 0) rv = 5;
      const show = ['radius', 'diameter', 'circumference', 'none']
        .indexOf(spec.show) >= 0 ? spec.show : 'radius';

      // ---- geometry --------------------------------------------------------
      const W = 360, H = 300;
      const CX = 180, CY = 148;
      // fixed comfortable size; only a gentle nudge so bigger numbers look bigger
      const R = Math.round(Math.max(88, Math.min(108, 88 + Math.log10(rv + 1) * 18)));

      const svg = mk('svg', {
        viewBox: '0 0 ' + W + ' ' + H, width: '100%',
        style: 'max-width:380px;background:' + BG + ';border:1px solid ' + BORDER +
          ';border-radius:10px;display:block;-webkit-user-select:none;user-select:none'
      });

      const uid = 'cir' + Math.random().toString(36).slice(2, 8);
      const defs = mk('defs', {});
      function marker(id, colour) {
        const m = mk('marker', {
          id: id, viewBox: '0 0 10 10', refX: 8.5, refY: 5,
          markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse'
        });
        m.appendChild(mk('path', { d: 'M0,0 L10,5 L0,10 z', fill: colour }));
        return m;
      }
      defs.appendChild(marker(uid + 'a', ACCENT));
      svg.appendChild(defs);

      // faint fill so the disc reads as a shape
      svg.appendChild(mk('circle', {
        cx: CX, cy: CY, r: R, fill: 'rgba(79,141,247,0.07)', stroke: 'none'
      }));

      // ---- the outline (redrawn on feedback) --------------------------------
      const outline = mk('circle', {
        cx: CX, cy: CY, r: R, fill: 'none', stroke: INK, 'stroke-width': 2
      });
      svg.appendChild(outline);

      // ---- the marked part --------------------------------------------------
      const markG = mk('g', {});
      svg.appendChild(markG);

      const defLabel = {
        radius: 'r = ' + rv + ' cm',
        diameter: 'd = ' + (rv * 2) + ' cm',
        circumference: 'circumference',
        none: ''
      }[show];
      const labelTxt = (spec.label != null && String(spec.label).length)
        ? String(spec.label) : defLabel;

      // little end-ticks perpendicular to a horizontal measured line
      function tick(x, colour) {
        return mk('line', {
          x1: r2(x), y1: CY - 6, x2: r2(x), y2: CY + 6,
          stroke: colour, 'stroke-width': 2, 'stroke-linecap': 'round'
        });
      }

      function draw(colour) {
        markG.innerHTML = '';
        outline.setAttribute('stroke', show === 'circumference' ? colour : INK);
        outline.setAttribute('stroke-width', show === 'circumference' ? 5 : 2);

        if (show === 'circumference') {
          // leader line from the outline out to the label (upper right)
          const a = -50 * Math.PI / 180;                 // screen angle
          const px = CX + R * Math.cos(a), py = CY + R * Math.sin(a);
          const qx = CX + (R + 34) * Math.cos(a), qy = CY + (R + 34) * Math.sin(a);
          markG.appendChild(mk('line', {
            x1: r2(qx), y1: r2(qy), x2: r2(px), y2: r2(py),
            stroke: colour, 'stroke-width': 2, 'stroke-linecap': 'round',
            'marker-end': 'url(#' + uid + 'a)'
          }));
          markG.appendChild(mk('line', {
            x1: r2(qx), y1: r2(qy), x2: r2(qx + 26), y2: r2(qy),
            stroke: colour, 'stroke-width': 2, 'stroke-linecap': 'round'
          }));
          if (labelTxt) {
            markG.appendChild(text(qx + 30, qy + 4, labelTxt, colour, 13, 'start'));
          }
          markG.appendChild(mk('circle', { cx: CX, cy: CY, r: 4, fill: INK }));
          return;
        }

        if (show === 'none') {
          markG.appendChild(mk('circle', { cx: CX, cy: CY, r: 4.5, fill: colour }));
          markG.appendChild(text(CX, CY + 22, 'centre', MUTE, 11, 'middle', 600));
          return;
        }

        const isDia = (show === 'diameter');
        const x1 = isDia ? CX - R : CX;
        const x2 = CX + R;

        markG.appendChild(mk('line', {
          x1: r2(x1), y1: CY, x2: r2(x2), y2: CY,
          stroke: colour, 'stroke-width': 3, 'stroke-linecap': 'round'
        }));
        markG.appendChild(tick(x2, colour));
        if (isDia) markG.appendChild(tick(x1, colour));

        // centre dot (always) — for the diameter it sits ON the line
        markG.appendChild(mk('circle', { cx: CX, cy: CY, r: 4.5, fill: INK }));
        markG.appendChild(mk('circle', { cx: CX, cy: CY, r: 4.5, fill: 'none', stroke: colour, 'stroke-width': 1.5 }));

        if (labelTxt) {
          markG.appendChild(text((x1 + x2) / 2, CY - 14, labelTxt, colour, 14));
        }
        markG.appendChild(text(CX, CY + 26, 'centre', MUTE, 11, 'middle', 600));
      }
      draw(ACCENT);

      host.appendChild(svg);

      // ---- typed input -------------------------------------------------------
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      input.placeholder = 'your answer';
      input.inputMode = spec.keypad || 'text';
      input.style.cssText += 'width:200px;font-size:1.2rem;padding:8px 12px;background:' + BG +
        ';color:' + INK + ';border:2px solid ' + BORDER +
        ';border-radius:8px;text-align:center;outline:none;max-width:100%';
      input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
      input.addEventListener('blur', () => { input.style.borderColor = BORDER; });
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') { ev.preventDefault(); api && api.submit && api.submit(); }
      });
      wrap.appendChild(input);
      host.appendChild(wrap);

      // ---- contract ----------------------------------------------------------
      host.__getValue = () => input.value.trim();

      host.__feedback = (res) => {
        const col = (res && res.correct) ? GOOD : BAD;
        input.style.borderColor = col;
        draw(col);
      };
    }
  };
})();
