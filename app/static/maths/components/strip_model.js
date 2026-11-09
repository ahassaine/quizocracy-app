/* strip_model — Singapore bar (strip) model for word problems. value = typed string.
 * spec: { mode:"equal_parts"|"part_whole", parts:<int>, partLabel:<str>,
 *         total:<num|str>, totalLabel:<str>, unknown:"total"|"part" }
 *
 *  equal_parts : one long bar split into `parts` equal segments each labelled
 *                `partLabel`; a brace above spans the bar showing `totalLabel`.
 *  part_whole  : whole bar on top labelled `totalLabel`; beneath it two segments,
 *                the known part and "?" for the unknown one; when the whole is the
 *                unknown, partLabels: [a, b] names both parts.
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
      // every part is drawn (a bar for 14x must show 14 boxes); 60 is only a guard against a runaway spec
      const parts = Math.max(1, Math.min(60, spec.parts | 0 || 1));
      const partLabel = spec.partLabel == null ? '' : String(spec.partLabel);
      // part_whole with the whole unknown names BOTH parts: partLabels: ["439,629", "43,188"]
      const partLabels = Array.isArray(spec.partLabels) && spec.partLabels.length === 2 ? spec.partLabels.map(String) : null;
      const totalLabel = spec.totalLabel != null ? String(spec.totalLabel)
        : (spec.total != null ? String(spec.total) : '?');

      // real CSS px (1 viewBox unit = 1 px) so labels keep their size on a phone
      const W = (() => { const w = Math.floor(host.getBoundingClientRect().width) - 2; return w > 0 ? Math.max(260, Math.min(520, w)) : 520; })();
      const padX = W < 400 ? 12 : 22;
      const bx0 = padX, bx1 = W - padX, barW = bx1 - bx0;
      const H = mode === 'equal_parts' ? 150 : 178;

      const svg = mk('svg', {
        viewBox: `0 0 ${W} ${H}`, width: '100%',
        style: `max-width:${W}px;box-sizing:content-box;background:#0b0f14;border:1px solid ` + LINE +
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
        // every box carries its label when it fits at 12 px or more; otherwise the caption names one part
        const lsize = segW < 40 ? 13 : segW < 58 ? 15 : 17;
        const fits = (sz) => partLabel.length * sz * 0.6 <= segW - 4;
        const size = [lsize, 14, 13, 12].find(fits);
        if (size) {
          for (let i = 0; i < parts; i++) segLabel(bx0 + segW * (i + 0.5), barY + barH / 2, partLabel, { size: size });
        }

        svg.appendChild(mk('text', {
          x: W / 2, y: barY + barH + 28, fill: SUB, 'font-size': 13,
          'text-anchor': 'middle',
          'font-family': 'system-ui,-apple-system,Segoe UI,sans-serif'
        }, parts + (parts === 1 ? ' equal part' : ' equal parts') + (!size && partLabel ? ', each ' + partLabel : '')));
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
        // a label is a size only when it is ONE number: "£1,250", "36 cm", "1 1/2", "3/4"; else NaN
        const num = (t) => {
          const s = String(t).replace(/,/g, '').replace(/^\s*[£$€]/, '').replace(/\s*[a-z%]+\s*$/i, '').trim();
          let m = s.match(/^(-?\d+(?:\.\d+)?)$/);
          if (m) return Number(m[1]);
          m = s.match(/^(\d+)\s+(\d+)\/(\d+)$/);
          if (m && +m[3]) return +m[1] + m[2] / m[3];
          m = s.match(/^(\d+)\/(\d+)$/);
          return m && +m[2] ? m[1] / m[2] : NaN;
        };
        const totNum = num(spec.total == null ? totalLabel : spec.total);
        const partNum = num(partLabel);
        // second part: "?" when it is the unknown, else its own label (never a copy of the first)
        const labelA = partLabels ? partLabels[0] : partLabel;
        const labelB = unknown === 'part' ? '?' : (partLabels ? partLabels[1] : '?');
        let frac = 0.5;
        if (unknown === 'part' && isFinite(totNum) && isFinite(partNum) && totNum > 0 && partNum > 0 && partNum < totNum) {
          frac = Math.min(0.85, Math.max(0.15, partNum / totNum));
        } else if (partLabels && num(labelA) > 0 && num(labelB) > 0) {
          frac = Math.min(0.85, Math.max(0.15, num(labelA) / (num(labelA) + num(labelB))));
        }
        let wA = Math.round(barW * frac);
        // a narrow box still needs room for its number at 12 px
        const need = (t) => String(t).length * 12 * 0.6 + 10;
        wA = Math.max(wA, Math.min(barW / 2, need(labelA)));
        wA = Math.min(wA, Math.max(barW / 2, barW - need(labelB)));
        const wB = barW - wA;
        const sz = (t, w) => [17, 14, 13, 12].find(s => String(t).length * s * 0.6 <= w - 6) || 12;

        bar(bx0, partY, wA, barH, false);
        segLabel(bx0 + wA / 2, partY + barH / 2, labelA, { size: sz(labelA, wA) });

        bar(bx0 + wA, partY, wB, barH, unknown === 'part');
        segLabel(bx0 + wA + wB / 2, partY + barH / 2, labelB, { size: sz(labelB, wB) });

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
      input.inputMode = spec.keypad || 'text';       // digits only for whole numbers; decimals and words need more
      input.setAttribute('autocapitalize', 'off');
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
