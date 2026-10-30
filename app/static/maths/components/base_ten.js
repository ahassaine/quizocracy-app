/* base_ten — build a number with hundreds/tens/ones blocks. value = the number.
 * spec: { mode:"build", max:9 }
 */
(function () {
  window.MComp = window.MComp || {};
  window.MComp["base_ten"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const cols = [
        { key: 'h', label: 'Hundreds', mult: 100, colour: '#4f8df7' },
        { key: 't', label: 'Tens', mult: 10, colour: '#22c55e' },
        { key: 'o', label: 'Ones', mult: 1, colour: '#e3b341' },
      ];
      const count = { h: 0, t: 0, o: 0 };
      const wrap = document.createElement('div');
      wrap.style.cssText = 'display:flex;gap:14px;align-items:flex-end;flex-wrap:wrap';
      const total = document.createElement('div');
      total.style.cssText = 'font-size:1.6rem;font-weight:800;margin:10px 0';

      function paint() {
        cols.forEach(c => {
          const stack = document.getElementById('bt-' + c.key); stack.innerHTML = '';
          for (let i = 0; i < count[c.key]; i++) {
            const b = document.createElement('div');
            const sz = c.key === 'h' ? 26 : c.key === 't' ? 26 : 12;
            b.style.cssText = `width:${c.key==='t'?12:sz}px;height:${sz}px;background:${c.colour};border:1px solid #0b0f14;border-radius:2px;margin:1px;display:inline-block`;
            stack.appendChild(b);
          }
        });
        const v = count.h * 100 + count.t * 10 + count.o;
        total.innerHTML = 'Your number: <span style="color:#4f8df7">' + v + '</span>';
      }

      cols.forEach(c => {
        const col = document.createElement('div');
        col.style.cssText = 'text-align:center;min-width:96px';
        const lab = document.createElement('div'); lab.textContent = c.label; lab.style.cssText = 'color:#8b949e;font-size:.75rem;margin-bottom:4px';
        const stack = document.createElement('div'); stack.id = 'bt-' + c.key;
        stack.style.cssText = 'min-height:120px;max-width:110px;background:#0b0f14;border:1px dashed #30363d;border-radius:8px;padding:4px;display:flex;flex-wrap:wrap;align-content:flex-end;justify-content:center';
        const ctrl = document.createElement('div'); ctrl.style.cssText = 'margin-top:6px';
        const minus = document.createElement('button'); minus.textContent = '−'; minus.className = 'btn ghost'; minus.style.padding = '4px 10px';
        const plus = document.createElement('button'); plus.textContent = '+'; plus.className = 'btn primary'; plus.style.padding = '4px 10px'; plus.style.marginLeft = '6px';
        minus.onclick = () => { count[c.key] = Math.max(0, count[c.key] - 1); paint(); };
        plus.onclick = () => { count[c.key] = Math.min(spec.max ?? 9, count[c.key] + 1); paint(); };
        ctrl.appendChild(minus); ctrl.appendChild(plus);
        col.appendChild(lab); col.appendChild(stack); col.appendChild(ctrl);
        wrap.appendChild(col);
      });
      host.appendChild(wrap); host.appendChild(total); paint();

      host.__getValue = () => count.h * 100 + count.t * 10 + count.o;
      host.__feedback = (res) => { total.style.color = res.correct ? '#22c55e' : '#f85149'; };
    }
  };
})();
