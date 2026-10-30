/* io_table — input/output ("function machine") table; type the missing output or the rule.
 * spec: { rows: [[in,out],...], ruleLabel: "+ 10" | undefined, missing: rowIndex, placeholder: "?" }
 * value = trimmed typed string.
 */
(function () {
  window.MComp = window.MComp || {};

  window.MComp["io_table"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const rows = Array.isArray(spec.rows) ? spec.rows : [];
      const missing = (typeof spec.missing === 'number') ? spec.missing : -1;

      const wrap = document.createElement('div');
      wrap.style.cssText = 'max-width:340px;width:100%';

      // Rule caption
      const rule = document.createElement('div');
      const hasRule = spec.ruleLabel != null && String(spec.ruleLabel).trim() !== '';
      rule.textContent = 'Rule: ' + (hasRule ? String(spec.ruleLabel) : '?');
      rule.style.cssText = 'font-size:.95rem;font-weight:700;letter-spacing:.02em;color:' +
        (hasRule ? '#e6edf3' : '#4f8df7') +
        ';background:#0b0f14;border:1px solid #30363d;border-radius:8px;' +
        'padding:6px 12px;display:inline-block;margin-bottom:10px';
      wrap.appendChild(rule);

      // Table
      const table = document.createElement('table');
      table.style.cssText = 'width:100%;border-collapse:collapse;background:#0b0f14;' +
        'border:1px solid #30363d;border-radius:10px;overflow:hidden;' +
        'font-size:1.15rem;color:#e6edf3;table-layout:fixed';

      const thead = document.createElement('thead');
      const htr = document.createElement('tr');
      ['In', 'Out'].forEach((label) => {
        const th = document.createElement('th');
        th.textContent = label;
        th.style.cssText = 'padding:8px 10px;text-align:center;font-size:.9rem;' +
          'text-transform:uppercase;letter-spacing:.08em;color:#8b949e;' +
          'background:#161b22;border-bottom:2px solid #30363d;' +
          'border-right:1px solid #30363d';
        htr.appendChild(th);
      });
      htr.lastChild.style.borderRight = 'none';
      thead.appendChild(htr);
      table.appendChild(thead);

      const tbody = document.createElement('tbody');
      let blankCell = null;
      rows.forEach((r, i) => {
        const tr = document.createElement('tr');
        tr.style.background = (i % 2) ? '#11161d' : 'transparent';
        const inTd = document.createElement('td');
        const outTd = document.createElement('td');
        const cellCss = 'padding:9px 10px;text-align:center;border-top:1px solid #21262d;' +
          'border-right:1px solid #30363d;font-variant-numeric:tabular-nums';
        inTd.style.cssText = cellCss;
        outTd.style.cssText = cellCss + ';border-right:none';
        inTd.textContent = (r && r[0] != null) ? String(r[0]) : '';

        if (i === missing) {
          const box = document.createElement('div');
          box.style.cssText = 'min-height:1.5em;min-width:64px;margin:0 auto;' +
            'border:2px dashed #4f8df7;border-radius:6px;background:rgba(79,141,247,.10);' +
            'color:#4f8df7;font-weight:700;line-height:1.5em';
          box.textContent = '';
          outTd.appendChild(box);
          blankCell = box;
        } else {
          outTd.textContent = (r && r[1] != null) ? String(r[1]) : '';
        }
        tr.appendChild(inTd);
        tr.appendChild(outTd);
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      wrap.appendChild(table);

      // Typed input
      const inputWrap = document.createElement('div');
      inputWrap.style.cssText = 'margin-top:12px';
      const input = document.createElement('input');
      input.type = 'text';
      input.className = 'm-input';
      input.autocomplete = 'off';
      if (missing >= 0 && hasRule) input.inputMode = 'numeric';
      if (spec.placeholder != null) input.placeholder = String(spec.placeholder);
      input.setAttribute('aria-label', 'Your answer');
      input.style.cssText = 'font-size:1.3rem;padding:8px 12px;width:100%;max-width:180px;' +
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
