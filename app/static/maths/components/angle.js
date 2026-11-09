/* angle — draws an angle from two rays, optionally with a protractor overlay.
 *
 * spec:
 *   { mode:"classify", degrees:D }
 *       two rays + a small arc; pupil types a word (acute/right/obtuse/straight/reflex).
 *   { mode:"measure", degrees:D, protractor:true }
 *       same drawing with a semicircular protractor (ticks every 10°, labelled every
 *       30° on BOTH the inner and the outer scale); pupil reads the size in degrees.
 *   { mode:"turn", degrees:D }
 *       one ray in the start direction, a dashed ray in the finish direction and a
 *       curved arrow showing an anticlockwise turn of D (typically 90/180/270/360).
 *
 * The first ray is always horizontal, pointing right; the second is rotated
 * ANTICLOCKWISE by `degrees`, so the arc always lies on the correct side and
 * reflex angles (180 < D < 360) draw the long way round.
 *
 * spec.given: the question states the drawn angle, so it is labelled with its value (not "?"), and
 * spec.unknown draws the angle asked for, marked "?":
 *   "straight"  — the first ray carries on into a straight line; "?" on the other angle on it
 *   "straight2" — the same, split into two equal angles, both "?"
 *   "full"      — "?" on the reflex angle that completes the full turn
 *   "right"     — a dashed ray at 90° (right-angle mark); "?" on the angle between
 * A right angle is marked with the square symbol only when its size is given; when the pupil must
 * classify or measure it, an arc is drawn as for any other angle (the square would be the answer).
 *
 * All modes: host.__getValue() === trimmed typed string.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';

  const BG = '#0b0f14', BORDER = '#30363d', INK = '#e6edf3', MUTE = '#8b949e';
  const ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';
  const FAINT = '#1c2430';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }
  const rad = (d) => d * Math.PI / 180;
  const r2 = (n) => Math.round(n * 100) / 100;

  window.MComp["angle"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const mode = spec.mode || 'classify';
      let deg = Number(spec.degrees);
      if (!isFinite(deg)) deg = 90;
      // keep strictly inside (0, 360]; turn mode allows a full 360
      if (mode === 'turn') deg = Math.max(1, Math.min(360, deg));
      else deg = Math.max(1, Math.min(359, deg));

      const showProt = (mode === 'measure') && spec.protractor !== false;
      const unknown = (mode === 'classify' && spec.given) ? spec.unknown : null;

      // ---- geometry -------------------------------------------------------
      const W = 360, H = 300;
      const VX = 180, VY = 165;              // vertex
      const R_PROT = 112;                    // protractor radius
      const R_RAY = showProt ? 140 : 130;    // ray length
      const R_ARC = deg > 180 ? 34 : 42;     // angle arc radius

      // screen point at maths-angle a (anticlockwise from east), radius r
      const P = (a, r) => [VX + r * Math.cos(rad(a)), VY - r * Math.sin(rad(a))];

      const svg = mk('svg', {
        viewBox: '0 0 ' + W + ' ' + H, width: '100%',
        style: 'max-width:420px;background:' + BG + ';border:1px solid ' + BORDER +
          ';border-radius:10px;display:block;-webkit-user-select:none;user-select:none'
      });

      // arrowhead marker
      const defs = mk('defs', {});
      function marker(id, colour) {
        const m = mk('marker', {
          id: id, viewBox: '0 0 10 10', refX: 8.5, refY: 5,
          markerWidth: 6, markerHeight: 6, orient: 'auto-start-reverse'
        });
        m.appendChild(mk('path', { d: 'M0,0 L10,5 L0,10 z', fill: colour }));
        return m;
      }
      const uid = 'ang' + Math.random().toString(36).slice(2, 8);
      defs.appendChild(marker(uid + 'i', INK));
      defs.appendChild(marker(uid + 'a', ACCENT));
      defs.appendChild(marker(uid + 'm', MUTE));
      svg.appendChild(defs);

      // ---- protractor ------------------------------------------------------
      if (showProt) {
        const g = mk('g', {});
        const a0 = P(0, R_PROT), a180 = P(180, R_PROT);
        g.appendChild(mk('path', {
          d: 'M' + r2(a0[0]) + ',' + r2(a0[1]) +
             ' A' + R_PROT + ',' + R_PROT + ' 0 0 1 ' + r2(a180[0]) + ',' + r2(a180[1]) + ' Z',
          fill: 'rgba(79,141,247,0.06)', stroke: '#3d4b5c', 'stroke-width': 1.4
        }));
        // inner rim (the "hole" edge of a real protractor)
        const b0 = P(0, 26), b180 = P(180, 26);
        g.appendChild(mk('path', {
          d: 'M' + r2(b0[0]) + ',' + r2(b0[1]) +
             ' A26,26 0 0 1 ' + r2(b180[0]) + ',' + r2(b180[1]),
          fill: 'none', stroke: '#3d4b5c', 'stroke-width': 1
        }));

        for (let a = 0; a <= 180; a += 5) {
          const major = (a % 30 === 0), mid = (a % 10 === 0);
          const len = major ? 15 : (mid ? 10 : 6);
          const p1 = P(a, R_PROT), p2 = P(a, R_PROT - len);
          g.appendChild(mk('line', {
            x1: r2(p1[0]), y1: r2(p1[1]), x2: r2(p2[0]), y2: r2(p2[1]),
            stroke: major ? '#7d8b9c' : '#4a5666', 'stroke-width': major ? 1.6 : 1
          }));
          if (!major) continue;
          // outer scale: reads 0 at the LEFT (i.e. 180 - a); nearer the rim
          const o = P(a, R_PROT - 25);
          g.appendChild(mk('text', {
            x: r2(o[0]), y: r2(o[1] + 3.5), fill: MUTE, 'font-size': 10,
            'text-anchor': 'middle', 'font-family': 'system-ui,sans-serif'
          }, String(180 - a)));
          // inner scale: reads 0 at the RIGHT (a); further in
          const i = P(a, R_PROT - 44);
          g.appendChild(mk('text', {
            x: r2(i[0]), y: r2(i[1] + 3.5), fill: '#6f7d8d', 'font-size': 9,
            'text-anchor': 'middle', 'font-family': 'system-ui,sans-serif'
          }, String(a)));
        }
        // baseline + centre cross
        g.appendChild(mk('line', {
          x1: r2(a180[0]), y1: r2(a180[1]), x2: r2(a0[0]), y2: r2(a0[1]),
          stroke: '#4a5666', 'stroke-width': 1.2
        }));
        g.appendChild(mk('line', { x1: VX - 7, y1: VY, x2: VX + 7, y2: VY, stroke: '#7d8b9c', 'stroke-width': 1 }));
        g.appendChild(mk('line', { x1: VX, y1: VY - 7, x2: VX, y2: VY + 7, stroke: '#7d8b9c', 'stroke-width': 1 }));
        svg.appendChild(g);
      }

      // ---- rays -------------------------------------------------------------
      function ray(a, colour, dashed, mrk) {
        const p = P(a, R_RAY);
        const at = { x1: VX, y1: VY, x2: r2(p[0]), y2: r2(p[1]), stroke: colour, 'stroke-width': 3, 'stroke-linecap': 'round' };
        if (dashed) { at['stroke-dasharray'] = '7 6'; at['stroke-width'] = 2.5; }
        if (mrk) at['marker-end'] = 'url(#' + mrk + ')';
        return mk('line', at);
      }

      if (mode === 'turn') {
        svg.appendChild(ray(0, INK, false, uid + 'i'));                 // start direction
        svg.appendChild(ray(deg % 360, MUTE, true, uid + 'm'));         // finish direction
      } else {
        svg.appendChild(ray(0, INK, false, uid + 'i'));
        svg.appendChild(ray(deg, INK, false, uid + 'i'));
        if (unknown === 'straight' || unknown === 'straight2') svg.appendChild(ray(180, INK, false, uid + 'i'));
        if (unknown === 'straight2') svg.appendChild(ray(deg + (180 - deg) / 2, MUTE, true, null));
        if (unknown === 'right') svg.appendChild(ray(90, MUTE, true, null));
      }

      // ---- the marked angle (arc from ray 1 anticlockwise to ray 2) ----------
      // In screen coordinates y is flipped, so anticlockwise = sweep-flag 0.
      function arcPath(r, from, sweepDeg) {
        const s = P(from, r), e = P(from + sweepDeg, r);
        const large = (Math.abs(sweepDeg) > 180) ? 1 : 0;
        return 'M' + r2(s[0]) + ',' + r2(s[1]) +
               ' A' + r + ',' + r + ' 0 ' + large + ' 0 ' + r2(e[0]) + ',' + r2(e[1]);
      }

      const arcG = mk('g', {});
      svg.appendChild(arcG);
      let arcEl = null, sqEl = null;

      function drawMark(colour) {
        arcG.innerHTML = '';
        arcEl = null; sqEl = null;
        if (mode === 'turn') {
          const sweep = (deg >= 360) ? 358 : deg;              // 360 needs a visible gap
          const rr = 62;
          arcEl = mk('path', {
            d: arcPath(rr, 8, sweep - 12), fill: 'none', stroke: colour,
            'stroke-width': 3, 'stroke-linecap': 'round', 'marker-end': 'url(#' + uid + 'a)'
          });
          arcG.appendChild(arcEl);
          return;
        }
        if (deg === 90 && spec.given) {
          // right-angle square in the corner between the two rays
          const s = 20;
          const u = P(0, s), v = P(90, s), c = [u[0] + (v[0] - VX), u[1] + (v[1] - VY)];
          sqEl = mk('path', {
            d: 'M' + r2(u[0]) + ',' + r2(u[1]) + ' L' + r2(c[0]) + ',' + r2(c[1]) + ' L' + r2(v[0]) + ',' + r2(v[1]),
            fill: 'none', stroke: colour, 'stroke-width': 2.5
          });
          arcG.appendChild(mk('rect', { x: VX, y: VY - s, width: s, height: s, fill: 'rgba(79,141,247,0.10)' }));
          arcG.appendChild(sqEl);
          return;
        }
        // fill wedge (faint) then the arc itself
        const w0 = P(0, R_ARC), w1 = P(deg, R_ARC);
        arcG.appendChild(mk('path', {
          d: 'M' + VX + ',' + VY + ' L' + r2(w0[0]) + ',' + r2(w0[1]) +
             ' A' + R_ARC + ',' + R_ARC + ' 0 ' + (deg > 180 ? 1 : 0) + ' 0 ' + r2(w1[0]) + ',' + r2(w1[1]) + ' Z',
          fill: 'rgba(79,141,247,0.12)', stroke: 'none'
        }));
        arcEl = mk('path', {
          d: arcPath(R_ARC, 0, deg), fill: 'none', stroke: colour,
          'stroke-width': 2.5, 'stroke-linecap': 'round'
        });
        arcG.appendChild(arcEl);
        if (deg === 180) {
          // straight angle: mark the vertex so it is not mistaken for a plain line
          arcG.appendChild(mk('circle', { cx: VX, cy: VY, r: 4, fill: colour }));
        }
      }

      // the angle the question asks for (drawn beside the given one), each part marked "?"
      const unkParts = unknown === 'straight' ? [[deg, 180 - deg]]
        : unknown === 'straight2' ? [[deg, (180 - deg) / 2], [deg + (180 - deg) / 2, (180 - deg) / 2]]
        : unknown === 'full' ? [[deg, 360 - deg]]
        : unknown === 'right' ? [[deg, 90 - deg]] : [];
      const unkG = mk('g', {});
      svg.appendChild(unkG);
      function drawUnknown(colour) {
        unkG.innerHTML = '';
        unkParts.forEach(([from, sweep], k) => {
          const r = unknown === 'full' ? 28 : 34 + k * 6;
          const at = { d: arcPath(r, from, sweep), fill: 'none', stroke: colour, 'stroke-width': 2.5, 'stroke-linecap': 'round' };
          if (unknown === 'full') at['stroke-dasharray'] = '5 4';
          unkG.appendChild(mk('path', at));
          const lp = P(from + sweep / 2, r + 22 + (sweep < 30 ? 40 + k * 18 : 0));   // a thin angle: write its "?" further out
          unkG.appendChild(mk('text', {
            x: r2(lp[0]), y: r2(lp[1] + 5), fill: colour, 'font-size': 15, 'font-weight': 700,
            'text-anchor': 'middle', 'font-family': 'system-ui,sans-serif'
          }, '?'));
        });
        if (unknown === 'right') {                       // the right angle the two parts make
          const s = 14, u = P(0, s), v = P(90, s), c = [u[0] + (v[0] - VX), u[1] + (v[1] - VY)];
          unkG.appendChild(mk('path', { d: 'M' + r2(u[0]) + ',' + r2(u[1]) + ' L' + r2(c[0]) + ',' + r2(c[1]) + ' L' + r2(v[0]) + ',' + r2(v[1]), fill: 'none', stroke: MUTE, 'stroke-width': 1.5 }));
        }
      }
      drawUnknown(ACCENT);
      drawMark(ACCENT);

      // ---- vertex + labels ---------------------------------------------------
      svg.appendChild(mk('circle', { cx: VX, cy: VY, r: 3.5, fill: INK }));

      function label(a, r, txt, colour) {
        const p = P(a, r);
        // nudge outwards so the text clears the ray
        const dx = 12 * Math.cos(rad(a)), dy = -12 * Math.sin(rad(a));
        svg.appendChild(mk('text', {
          x: r2(p[0] + dx), y: r2(p[1] + dy + 4), fill: colour || INK, 'font-size': 13,
          'font-weight': 700, 'text-anchor': 'middle', 'font-family': 'system-ui,sans-serif'
        }, txt));
      }
      if (mode === 'turn') {
        // beside each ray, not past its arrowhead: "start" above the start ray, "finish" on the clockwise
        // side of the finish ray, so a full turn (both rays the same) does not print one word over the other
        function side(a, off, txt, colour) {
          const p = P(a, R_RAY * 0.68), o = rad(a + off), cx = Math.cos(o);
          svg.appendChild(mk('text', {
            x: r2(p[0] + 12 * cx), y: r2(p[1] - 16 * Math.sin(o) + 4), fill: colour, 'font-size': 13,
            'font-weight': 700, 'text-anchor': cx < -0.3 ? 'end' : (cx > 0.3 ? 'start' : 'middle'),
            'font-family': 'system-ui,sans-serif'
          }, txt));
        }
        side(0, 90, 'start', INK);
        side(deg % 360, -90, 'finish', MUTE);
      } else {
        label(0, R_RAY - 4, 'A', INK);
        label(deg, R_RAY - 4, 'B', INK);
        const mid = deg / 2;
        const lp = P(mid, deg === 90 ? 46 : R_ARC + 22);
        svg.appendChild(mk('text', {
          x: r2(lp[0]), y: r2(lp[1] + 4), fill: spec.given ? INK : ACCENT, 'font-size': 14, 'font-weight': 700,
          'text-anchor': 'middle', 'font-family': 'system-ui,sans-serif'
        }, spec.given ? r2(deg) + '°' : '?'));
      }

      host.appendChild(svg);

      // ---- typed input -------------------------------------------------------
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      if (mode !== 'measure' && !spec.numeric) {    // a word: acute / obtuse …, quarter / half …
        input.inputMode = 'text';
        input.placeholder = 'type the word';
        input.style.width = '210px';
      } else {
        input.inputMode = spec.keypad || 'numeric';
        input.placeholder = mode === 'measure' ? 'degrees' : 'type a number';
        input.style.width = '170px';
      }
      input.style.cssText += ';font-size:1.2rem;padding:8px 12px;background:' + BG + ';color:' + INK +
        ';border:2px solid ' + BORDER + ';border-radius:8px;text-align:center;outline:none;max-width:100%';
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
        drawMark(col);
        drawUnknown(col);
      };
    }
  };
})();
