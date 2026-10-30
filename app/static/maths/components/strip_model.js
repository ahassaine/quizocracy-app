/* strip_model — Singapore bar (strip) model for word problems. value = typed string.
 * spec: { mode:"equal_parts"|"part_whole", parts:<int>, partLabel:<str>,
 *         total:<num|str>, totalLabel:<str>, unknown:"total"|"part" }
 *
 *  equal_parts : one long bar split into `parts` equal segments each labelled
 *                `partLabel`; a brace above spans the bar showing `totalLabel`.
 *  part_whole  : whole bar on top labelled `totalLabel`; beneath it two segments,
 *                the known part and "?" for the unknown one.
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';

  const INK = '#e6edf3', SUB = '#8b949e', LINE = '#30363d';
  const ACCENT = '#4f8df7', GOOD = '#22c55e', BAD = '#f85149';
  const FILL = '#161b22', FILL_A = '#17304f';

  function mk(t, a, txt) {
    const e = document.createElementNS(NS, t);
    for (const k in a) e.setAttribute(k, a[k]);
    if (txt != null) e.textContent = txt;
    return e;
  }
  function isQ(s) { return String(s == null ? '' : s).trim() === '?'; }

  window.MComp["strip_model"] = {
    render(host, spec, api) {
      host.innerHTML = '';

      const mode = spec.mode === 'part_whole' ? 'part_whole' : 'equal_parts';
      const unknown = spec.unknown === 'part' ? 'part' : 'total';
      const parts = Math.max(1, Math.min(12, spec.parts | 0 || 1));
      const partLabel = spec.partLabel == null ? '' : String(spec.partLabel);
      const totalLabel = spec.totalLabel != null ? String(spec.totalLabel)
        : (spec.total != null ? String(spec.total) : '?');

      const W = 520, padX = 22;
      const bx0 = padX, bx1 = W - padX, barW = bx1 - bx0;
      const H = mode === 'equal_parts' ? 150 : 178;

      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: 'max-width:520px;background:#0b0f14;border:1px solid ' + LINE +
               ';border-radius:10px;display:block;-webkit-user-select:none;user-select:none'
      });

      const boxes = [];   // rects we may recolour on feedback

      // ---- helpers -------------------------------------------------------
      // Label centred in a segment; a lone "?" renders bold + accent.
      function segLabel(cx, cy, text, opts) {
        opts = opts || {};
        const q = isQ(text);
        const t = mk('text', {
          x: cx, y: cy + (opts.size || 17) * 0.35,
          fill: q ? ACCENT : (opts.fill || INK),
          'font-size': q ? (opts.size || 17) + 3 : (opts.size || 17),
          'font-weight': q ? 800 : 600,
          'text-anchor': 'middle',
          'font-family': 'system-ui,-apple-system,Segoe UI,sans-serif'
        }, String(text));
        svg.appendChild(t);
        return t;
      }

      // Curly-ish brace spanning [x0,x1] at baseline y, opening downward.
      function brace(x0, x1, y, depth) {
        const d = depth || 9, mid = (x0 + x1) / 2;
        const p = `M ${x0} ${y + d}
                   q 0 ${-d} ${d} ${-d}
                   L ${mid - d} ${y}
                   q ${d} 0 ${d} ${-d * 0.7}
                   q 0 ${d * 0.7} ${d} ${d * 0.7}
                   L ${x1 - d} ${y}
                   q ${d} 0 ${d} ${d}`;
        svg.appendChild(mk('path', {
          d: p.replace(/\s+/g, ' '), fill: 'none',
          stroke: SUB, 'stroke-width': 1.6, 'stroke-linecap': 'round',
          'stroke-linejoin': 'round'
        }));
        return mid;
      }

      function bar(x, y, w, h, accent) {
        const r = mk('rect', {
          x: x, y: y, width: w, height: h, rx: 4,
          fill: accent ? FILL_A : FILL,
          stroke: accent ? ACCENT : LINE, 'stroke-width': 1.6
        });
        svg.appendChild(r);
        boxes.push(r);
        return r;
      }

      // ---- layouts -------------------------------------------------------
      if (mode === 'equal_parts') {
        const braceY = 44, barY = 60, barH = 50;

        // total brace + its label above the whole bar
        const mid = brace(bx0, bx1, braceY, 9);
        segLabel(mid, 22, totalLabel, { size: 19 });

        // one bar divided into equal segments
        const segW = barW / parts;
        bar(bx0, barY, barW, barH, unknown === 'part');
        for (let i = 1; i < parts; i++) {
          const x = bx0 + i * segW;
          svg.appendChild(mk('line', {
            x1: x, y1: barY, x2: x, y2: barY + barH,
            stroke: LINE, 'stroke-width': 1.4
          }));
        }
        const lsize = segW < 40 ? 13 : segW < 58 ? 15 : 17;
        for (let i = 0; i < parts; i++) {
          segLabel(bx0 + segW * (i + 0.5), barY + barH / 2, partLabel, { size: lsize });
        }

        svg.appendChild(mk('text', {
          x: W / 2, y: barY + barH + 28, fill: SUB, 'font-size': 13,
          'text-anchor': 'middle',
          'font-family': 'system-ui,-apple-system,Segoe UI,sans-serif'
        }, parts + (parts === 1 ? ' equal part' : ' equal parts')));
      } else {
        // part_whole: whole bar on top, two parts beneath
        const wholeY = 34, barH = 46, gap = 26;
        const partY = wholeY + barH + gap;

        svg.appendChild(mk('text', {
          x: bx0, y: 20, fill: SUB, 'font-size': 12,
          'font-family': 'system-ui,-apple-system,Segoe UI,sans-serif'
        }, 'whole'));

        bar(bx0, wholeY, barW, barH, unknown === 'total');
        segLabel(W / 2, wholeY + barH / 2, totalLabel, { size: 19 });

        // known part width proportional where numbers allow, else half/half
        const totNum = Number(String(spec.total == null ? totalLabel : spec.total).replace(/[^0-9.\-]/g, ''));
        const partNum = Number(String(partLabel).replace(/[^0-9.\-]/g, ''));
        let frac = 0.5;
        if (unknown === 'part' && isFinite(totNum) && isFinite(partNum) && totNum > 0 && partNum > 0 && partNum < totNum) {
          frac = Math.min(0.85, Math.max(0.15, partNum / totNum));
        }
        const wA = Math.round(barW * frac), wB = barW - wA;

        // known part first, "?" second when the part is the unknown
        bar(bx0, partY, wA, barH, false);
        segLabel(bx0 + wA / 2, partY + barH / 2, partLabel, { size: wA < 60 ? 14 : 17 });

        bar(bx0 + wA, partY, wB, barH, unknown === 'part');
        segLabel(bx0 + wA + wB / 2, partY + barH / 2,
                 unknown === 'part' ? '?' : partLabel, { size: wB < 60 ? 14 : 17 });

        // vertical tie lines showing the two parts make the whole
        [bx0, bx0 + wA, bx1].forEach((x) => {
          svg.appendChild(mk('line', {
            x1: x, y1: wholeY + barH, x2: x, y2: partY,
            stroke: LINE, 'stroke-width': 1, 'stroke-dasharray': '3 3'
          }));
        });

        svg.appendChild(mk('text', {
          x: bx0, y: partY + barH + 20, fill: SUB, 'font-size': 12,
          'font-family': 'system-ui,-apple-system,Segoe UI,sans-serif'
        }, 'parts'));
      }

      host.appendChild(svg);

      // ---- typed input ---------------------------------------------------
      const wrap = document.createElement('div');
      wrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.inputMode = 'numeric';
      input.className = 'm-input';
      input.autocomplete = 'off';
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:140px;background:#0b0f14;color:' +
        INK + ';border:2px solid ' + LINE + ';border-radius:8px;text-align:center;outline:none';
      input.addEventListener('focus', () => { input.style.borderColor = ACCENT; });
      input.addEventListener('blur', () => { input.style.borderColor = LINE; });
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); }
      });
      wrap.appendChild(input);
      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => {
        const c = res.correct ? GOOD : BAD;
        input.style.borderColor = c;
        boxes.forEach((r) => {
          if (r.getAttribute('stroke') === ACCENT) {
            r.setAttribute('stroke', c);
            r.setAttribute('fill', res.correct ? '#0f2a1a' : '#2a1114');
          }
        });
      };
    }
  };
})();
