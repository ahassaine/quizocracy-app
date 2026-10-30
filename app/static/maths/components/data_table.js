/* data_table — general bordered data table (tally charts, frequency tables,
 * timetables, Carroll diagrams, price lists).
 * spec: { headers: [..], rows: [[..],..], missing: [rowIndex, colIndex], caption, placeholder }
 * value = trimmed typed string.
 */
(function () {
  window.MComp = window.MComp || {};

  window.MComp["data_table"] = {
    render(host, spec, api) {
      host.innerHTML = '';

      const headers = Array.isArray(spec.headers) ? spec.headers : [];
      const rows = Array.isArray(spec.rows) ? spec.rows : [];
      const miss = Array.isArray(spec.missing) ? spec.missing : null;
      const mR = miss && typeof miss[0] === 'number' ? miss[0] : -1;
      const mC = miss && typeof miss[1] === 'number' ? miss[1] : -1;

      let nCols = headers.length;
      rows.forEach((r) => { if (Array.isArray(r) && r.length > nCols) nCols = r.length; });
      if (nCols < 1) nCols = 1;

      const txt = (v) => (v == null ? '' : String(v));

      const wrap = document.createElement('div');
      wrap.style.cssText = 'width:100%;max-width:520px;box-sizing:border-box';

      // Caption
      if (spec.caption != null && String(spec.caption).trim() !== '') {
        const cap = document.createElement('div');
        cap.textContent = String(spec.caption);
        cap.style.cssText = 'font-size:.98rem;font-weight:700;letter-spacing:.02em;' +
          'color:#e6edf3;margin-bottom:10px;line-height:1.35';
        wrap.appendChild(cap);
      }

      // Scroll container — keeps wide tables inside the component
      const scroller = document.createElement('div');
      scroller.style.cssText = 'width:100%;overflow-x:auto;overflow-y:hidden;' +
        '-webkit-overflow-scrolling:touch;border:1px solid #30363d;border-radius:10px;' +
        'background:#0b0f14;box-sizing:border-box';

      const table = document.createElement('table');
      table.style.cssText = 'border-collapse:collapse;background:#0b0f14;' +
        'color:#e6edf3;font-size:1.02rem;min-width:100%;';

      const cellPad = 'padding:8px 12px;';
      const bodyCss = cellPad + 'text-align:center;white-space:nowrap;' +
        'border-top:1px solid #21262d;border-right:1px solid #30363d;' +
        'font-variant-numeric:tabular-nums';

      // Header
      if (headers.length) {
        const thead = document.createElement('thead');
        const htr = document.createElement('tr');
        for (let c = 0; c < nCols; c++) {
          const th = document.createElement('th');
          th.textContent = txt(headers[c]);
          th.scope = 'col';
          th.style.cssText = cellPad + 'text-align:center;white-space:nowrap;' +
            'font-size:.85rem;text-transform:uppercase;letter-spacing:.07em;' +
            'color:#8b949e;background:#161b22;border-bottom:2px solid #30363d;' +
            'border-right:1px solid #30363d';
          htr.appendChild(th);
        }
        if (htr.lastChild) htr.lastChild.style.borderRight = 'none';
        thead.appendChild(htr);
        table.appendChild(thead);
      }

      // Body
      const tbody = document.createElement('tbody');
      let blankCell = null;
      rows.forEach((r, i) => {
        const tr = document.createElement('tr');
        tr.style.background = (i % 2) ? '#11161d' : 'transparent';
        for (let c = 0; c < nCols; c++) {
          const td = document.createElement('td');
          td.style.cssText = bodyCss + (c === nCols - 1 ? ';border-right:none' : '');
          if (c === 0 && !headers.length) td.style.fontWeight = '700';
          if (i === mR && c === mC) {
            const box = document.createElement('div');
            box.style.cssText = 'min-height:1.5em;min-width:60px;margin:0 auto;' +
              'border:2px dashed #4f8df7;border-radius:6px;background:rgba(79,141,247,.10);' +
              'color:#4f8df7;font-weight:700;line-height:1.5em;padding:0 6px;box-sizing:border-box';
            box.textContent = '';
            td.appendChild(box);
            blankCell = box;
          } else {
            td.textContent = txt(Array.isArray(r) ? r[c] : '');
          }
          tr.appendChild(td);
        }
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      scroller.appendChild(table);
      wrap.appendChild(scroller);

      // Typed input
      const inputWrap = document.createElement('div');
      inputWrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      if (spec.placeholder != null) input.placeholder = String(spec.placeholder);
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.25rem;padding:8px 12px;width:100%;max-width:200px;' +
        'background:#0b0f14;color:#e6edf3;border:2px solid #30363d;border-radius:8px;' +
        'text-align:center;outline:none;box-sizing:border-box';
      input.addEventListener('focus', () => { input.style.borderColor = '#4f8df7'; });
      input.addEventListener('blur', () => { input.style.borderColor = '#30363d'; });
      input.addEventListener('input', () => {
        if (blankCell) blankCell.textContent = input.value.trim();
      });
      input.addEventListener('keydown', (ev) => {
        if (ev.key === 'Enter') { ev.preventDefault(); api.submit(); }
      });
      inputWrap.appendChild(input);
      wrap.appendChild(inputWrap);

      host.appendChild(wrap);

      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => {
        const col = res && res.correct ? '#22c55e' : '#f85149';
        input.style.borderColor = col;
        if (blankCell) {
          blankCell.style.borderColor = col;
          blankCell.style.color = col;
          blankCell.style.borderStyle = 'solid';
          blankCell.style.background = res && res.correct
            ? 'rgba(34,197,94,.12)' : 'rgba(248,81,73,.12)';
        }
      };
    }
  };
})();
