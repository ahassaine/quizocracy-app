/* number_line — place a marker on a number line. value = the number chosen.
 * spec: { min, max, step, major, fractions }  (major = spacing of labelled ticks)
 *   fractions: n — a line in steps of 1/n for a fraction question. Only whole numbers are labelled
 *              (decimal labels would give 0.375 for 3/8) and the value is sent as "k/n".
 * The line is drawn at the card's real width so its numbers stay readable on a phone. There is no live
 * readout (it would do the reading for the child); the marker snaps to the nearest tick, and when the
 * ticks are too close for a finger a "closer look" strip below shows the part of the line around the
 * marker with wide ticks. After Check, the chosen and the right values are written by the marks.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a, txt) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (txt != null) e.textContent = txt; return e; }
  const INK = '#e6edf3', DIM = '#8b949e', FAINT = '#495260', ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';

  window.MComp["number_line"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const min = spec.min ?? 0, max = spec.max ?? 100, step = spec.step ?? 1, major = spec.major ?? (max - min) / 10;
      const den = spec.fractions | 0;                  // > 0: a fraction line in steps of 1/den
      // round away binary-float noise so labels/values read cleanly (0.6, not 0.6000000000000001)
      const round6 = (v) => parseFloat(Number(v).toFixed(6));
      const nSteps = Math.round((max - min) / step);
      const valAt = (i) => round6(min + i * step);     // index-based: no accumulated drift
      const idxOf = (v) => Math.max(0, Math.min(nSteps, Math.round((v - min) / step)));

      // a label as a child writes it: thousands commas, a real minus sign, fractions on a fraction line
      function fmt(v) {
        if (den) {
          const k = Math.round(v * den), w = Math.trunc(k / den), r = Math.abs(k % den);
          const sign = k < 0 ? '−' : '';
          if (!r) return sign + Math.abs(w);
          return sign + (w ? Math.abs(w) + ' ' : '') + r + '/' + den;
        }
        const s = Math.abs(v) >= 1000 ? Math.abs(v).toLocaleString('en-GB', { maximumFractionDigits: 6 }) : String(Math.abs(round6(v)));
        return (v < 0 ? '−' : '') + s;
      }

      // ---- size: real CSS pixels (a viewBox scaled down to a phone shrinks 12 px labels to 6 px) ----
      const W = Math.max(280, Math.min(660, Math.floor(host.getBoundingClientRect().width || 640)));
      const H = 84, padX = 18, y = 46, FS = 13;
      const x0 = padX, x1 = W - padX;
      const pxStep = (x1 - x0) / Math.max(1, nSteps);
      const toX = (v) => x0 + (v - min) / (max - min) * (x1 - x0);

      const wrap = document.createElement('div');
      wrap.style.cssText = 'max-width:' + W + 'px';
      const svg = mk('svg', { viewBox: `0 0 ${W} ${H}`, width: '100%', role: 'img', 'aria-label': 'Number line from ' + fmt(min) + ' to ' + fmt(max),
        style: 'display:block;background:#0b0f14;border:1px solid #30363d;border-radius:10px;touch-action:none;cursor:pointer;-webkit-user-select:none;user-select:none' });
      wrap.appendChild(svg);

      // ---- which ticks are labelled: majors (whole numbers on a fraction line), thinned until labels fit ----
      const isMajor = (i) => {
        const v = valAt(i);
        if (den) return Math.abs(v * 1 - Math.round(v)) < 1e-6;
        const k = (v - min) / major; return Math.abs(k - Math.round(k)) < 1e-6;
      };
      const majors = [];
      for (let i = 0; i <= nSteps; i++) if (isMajor(i)) majors.push(i);
      const widest = Math.max(...majors.map(i => fmt(valAt(i)).length), 1) * FS * 0.6 + 4;
      let every = 1;
      if (majors.length > 1) {
        const gap = (majors[1] - majors[0]) * pxStep;
        for (const m of [1, 2, 5, 10, 20, 50, 100]) { every = m; if (gap * m >= widest) break; }
      }

      // a tick number, kept inside the box at the two ends (10,000,000 is wider than the margin)
      function numLabel(x, yy, txt) {
        const half = txt.length * FS * 0.3;
        const a = x - half < 2 ? 'start' : (x + half > W - 2 ? 'end' : 'middle');
        return mk('text', { x: a === 'start' ? 2 : a === 'end' ? W - 2 : x, y: yy, fill: DIM, 'font-size': FS, 'text-anchor': a, 'font-family': 'system-ui,sans-serif' }, txt);
      }

      function drawTicks(g, from, to, X, yy, labelAll) {
        for (let i = from; i <= to; i++) {
          const v = valAt(i), maj = isMajor(i);
          const half = den ? den % 2 === 0 && Math.round(v * den) % (den / 2) === 0      // a half (a fraction line)
            : Math.round(major / step) % 2 === 0 && Math.round((v - min) / step) % Math.round(major / step / 2) === 0;   // halfway between labels
          const h = maj ? 10 : (half ? 7 : 5);
          g.appendChild(mk('line', { x1: X(v), y1: yy - h, x2: X(v), y2: yy + h, stroke: maj ? '#c9d1d9' : (half ? '#8b949e' : FAINT), 'stroke-width': maj ? 2 : 1 }));
          const mi = majors.indexOf(i);
          if (maj && (labelAll || mi % every === 0)) g.appendChild(numLabel(X(v), yy + 26, fmt(v)));
        }
      }

      svg.appendChild(mk('line', { x1: x0, y1: y, x2: x1, y2: y, stroke: DIM, 'stroke-width': 2 }));
      const zoomBand = mk('rect', { x: 0, y: y - 14, width: 0, height: 28, fill: ACCENT, opacity: 0, rx: 3 });
      svg.appendChild(zoomBand);
      drawTicks(svg, 0, nSteps, toX, y, false);
      const target = mk('polygon', { points: '', fill: GOOD, opacity: 0 });
      const marker = mk('polygon', { points: '', fill: ACCENT, stroke: '#fff', 'stroke-width': 1, style: 'cursor:grab' });
      svg.appendChild(target); svg.appendChild(marker);
      const markLab = mk('text', { x: 0, y: 14, fill: INK, 'font-size': FS, 'text-anchor': 'middle', 'font-weight': 700 });
      const targLab = mk('text', { x: 0, y: 14, fill: GOOD, 'font-size': FS, 'text-anchor': 'middle', 'font-weight': 700 });
      svg.appendChild(markLab); svg.appendChild(targLab);
      const tri = (x, yy) => `${x},${yy - 14} ${x - 8},${yy - 27} ${x + 8},${yy - 27}`;

      // ---- the closer look: a block of ticks around the marker, aligned to the line (never centred on
      //      the marker, so its end labels are ordinary tick labels, not a readout) ----
      const MIN_PX = 12;
      let zoom = null;
      if (pxStep < MIN_PX) {
        const ZW = W, ZH = 74, zy = 40;
        let B = den || 10;                               // a fraction line zooms one whole at a time
        if (!den) for (const b of [10, 5, 2]) { B = b; if ((ZW - 2 * padX) / b >= 22) break; }
        const zsvg = mk('svg', { viewBox: `0 0 ${ZW} ${ZH}`, width: '100%', 'aria-hidden': 'true',
          style: 'display:none;margin-top:8px;background:#0b0f14;border:1px dashed #30363d;border-radius:10px;touch-action:none;cursor:pointer;-webkit-user-select:none;user-select:none' });
        zsvg.appendChild(mk('text', { x: 8, y: 14, fill: DIM, 'font-size': 11 }, 'Closer look'));
        const zg = mk('g', {}); zsvg.appendChild(zg);
        const zmarker = mk('polygon', { points: '', fill: ACCENT, stroke: '#fff', 'stroke-width': 1 });
        const ztarget = mk('polygon', { points: '', fill: GOOD, opacity: 0 });
        zsvg.appendChild(ztarget); zsvg.appendChild(zmarker);
        wrap.appendChild(zsvg);
        zoom = { svg: zsvg, from: -1, to: -1, B, X: null,
          show(i) {
            const from = Math.min(Math.max(0, nSteps - B), Math.floor(i / B) * B), to = Math.min(nSteps, from + B);
            if (from !== this.from) {
              this.from = from; this.to = to;
              const a = valAt(from), b = valAt(to);
              this.X = (v) => padX + (v - a) / ((b - a) || 1) * (ZW - 2 * padX);
              zg.innerHTML = '';
              zg.appendChild(mk('line', { x1: padX, y1: zy, x2: ZW - padX, y2: zy, stroke: DIM, 'stroke-width': 2 }));
              drawTicks(zg, from, to, this.X, zy, true);
              for (const end of [from, to]) {             // the block's ends always carry their numbers
                if (isMajor(end)) continue;
                zg.appendChild(numLabel(this.X(valAt(end)), zy + 26, fmt(valAt(end))));
              }
              zoomBand.setAttribute('x', toX(a)); zoomBand.setAttribute('width', Math.max(2, toX(b) - toX(a)));
              zoomBand.setAttribute('opacity', 0.18);
            }
            zsvg.style.display = 'block';
            zmarker.setAttribute('points', tri(this.X(valAt(i)), zy));
          },
          has(v) { const i = idxOf(v); return this.from >= 0 && i >= this.from && i <= this.to && Math.abs(valAt(i) - v) < step / 2 + 1e-9; },
        };
        zoom.marker = zmarker; zoom.target = ztarget; zoom.zy = zy;
      }

      const hint = document.createElement('div');
      hint.className = 'mut small';
      hint.style.cssText = 'margin-top:6px';
      hint.textContent = zoom ? 'Tap the line to put the arrow on it, then move it in the closer look.' : 'Tap the line to put the arrow on it.';
      wrap.appendChild(hint);
      host.appendChild(wrap);

      let idx = null;
      function setI(i, fromZoom) {
        idx = Math.max(0, Math.min(nSteps, i));
        marker.setAttribute('points', tri(toX(valAt(idx)), y));
        if (zoom) {
          if (fromZoom) zoom.marker.setAttribute('points', tri(zoom.X(valAt(idx)), zoom.zy));
          else zoom.show(idx);
        }
      }

      function pointerI(ev, el, X0, X1, from, to) {
        const r = el.getBoundingClientRect();
        const px = (ev.clientX - r.left) / r.width * W;
        const f = (px - X0) / (X1 - X0);
        return from + Math.round(f * (to - from));
      }
      function wire(el, isZoom) {
        let dragging = false;
        const at = (ev) => isZoom
          ? Math.max(zoom.from, Math.min(zoom.to, pointerI(ev, el, padX, W - padX, zoom.from, zoom.to)))
          : pointerI(ev, el, x0, x1, 0, nSteps);
        el.addEventListener('pointerdown', (ev) => {
          dragging = true; setI(at(ev), isZoom); ev.preventDefault();
          try { el.setPointerCapture(ev.pointerId); } catch (e) {}
        });
        el.addEventListener('pointermove', (ev) => { if (dragging) { setI(at(ev), isZoom); ev.preventDefault(); } });
        const up = () => { dragging = false; };
        el.addEventListener('pointerup', up); el.addEventListener('pointercancel', up);
      }
      wire(svg, false);
      if (zoom) wire(zoom.svg, true);
      // keyboard: arrows move the marker one tick
      svg.setAttribute('tabindex', '0');
      svg.addEventListener('keydown', (ev) => {
        if (ev.key === 'ArrowLeft' || ev.key === 'ArrowRight') {
          setI(idx == null ? Math.round(nSteps / 2) : idx + (ev.key === 'ArrowRight' ? 1 : -1), false); ev.preventDefault();
        }
      });

      host.__empty = 'Tap the number line first.';
      host.__getValue = () => {
        if (idx == null) return null;
        const v = valAt(idx);
        return den ? Math.round(v * den) + '/' + den : v;
      };
      host.__feedback = (res) => {
        const ok = !!(res && res.correct);
        marker.setAttribute('fill', ok ? GOOD : BAD);
        if (zoom) zoom.marker.setAttribute('fill', ok ? GOOD : BAD);
        if (idx != null) { markLab.setAttribute('x', Math.max(20, Math.min(W - 20, toX(valAt(idx))))); markLab.textContent = fmt(valAt(idx)); markLab.setAttribute('fill', ok ? GOOD : BAD); }
        if (ok) return;
        let ev = Number(res.expected);
        const m = String(res.expected).match(/^\s*(-?)(?:(\d+)\s+)?(\d+)\/(\d+)\s*$/);
        if (m) ev = (m[1] ? -1 : 1) * ((+m[2] || 0) + (+m[3]) / (+m[4]));
        if (isNaN(ev)) return;
        target.setAttribute('points', tri(toX(ev), y)); target.setAttribute('opacity', 0.85);
        targLab.setAttribute('x', Math.max(20, Math.min(W - 20, toX(ev)))); targLab.textContent = fmt(ev);
        if (idx != null && Math.abs(toX(ev) - toX(valAt(idx))) < 40) targLab.setAttribute('y', H - 2);   // keep the two numbers apart
        if (zoom && zoom.has(ev)) { zoom.target.setAttribute('points', tri(zoom.X(ev), zoom.zy)); zoom.target.setAttribute('opacity', 0.85); }
      };
    }
  };
})();
