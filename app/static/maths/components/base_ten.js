/* base_ten — build a number with hundreds/tens/ones blocks. value = the number.
 * spec: { mode:"build", max:9 }
 * Until a block is added, the value is null: an empty board is no answer, not 0.
 */
(function () {
  window.MComp = window.MComp || {};
  window.MComp["base_ten"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      // only the columns the number needs: Years 1-2 build numbers below 100, and "with tens and ones" says so;
      // a Hundreds column there is just the first "+" a five-year-old taps (api: year, prompt from the page)
      const year = (api && api.year) || 0;
      const noHundreds = (year >= 1 && year <= 2) || /\btens and ones\b/i.test((api && api.prompt) || '');
      const cols = [
        { key: 'h', label: 'Hundreds', mult: 100, colour: '#4f8df7' },
        { key: 't', label: 'Tens', mult: 10, colour: '#22c55e' },
        { key: 'o', label: 'Ones', mult: 1, colour: '#e3b341' },
      ].filter(c => !(noHundreds && c.key === 'h'));
      const count = { h: 0, t: 0, o: 0 };
      let touched = false;
      const tip = document.createElement('div');       // why "+" stopped: 10 ones make a ten
      tip.setAttribute('role', 'status'); tip.setAttribute('data-testid', 'blocks-tip');
      tip.style.cssText = 'min-height:1.3em;margin-top:8px;font-weight:700;color:#e3b341';
      const TIP = { o: '10 ones make a ten — use the tens.', t: '10 tens make a hundred — use the hundreds.' };
      const wrap = document.createElement('div');
      wrap.style.cssText = 'display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap';
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
      }
      // the number the blocks make so far, as they are added (a fast tap that missed shows at once)
      function showTotal() {
        const v = count.h * 100 + count.t * 10 + count.o;
        total.innerHTML = 'Your number: <span style="color:inherit" data-testid="blocks-total">' + v + '</span>';
      }

      cols.forEach(c => {
        const col = document.createElement('div');
        // fixed sizes: the column never widens or grows as blocks go in, so "+" stays under the finger
        col.style.cssText = 'text-align:center;width:96px';
        const lab = document.createElement('div'); lab.textContent = c.label; lab.style.cssText = 'color:#8b949e;font-size:.75rem;margin-bottom:4px';
        const stack = document.createElement('div'); stack.id = 'bt-' + c.key;
        stack.style.cssText = 'box-sizing:border-box;height:124px;width:96px;overflow:hidden;background:#0b0f14;border:1px dashed #30363d;border-radius:8px;padding:4px;display:flex;flex-wrap:wrap;align-content:flex-end;justify-content:center';
        const ctrl = document.createElement('div'); ctrl.style.cssText = 'margin-top:6px';
        const minus = document.createElement('button'); minus.textContent = '−'; minus.className = 'btn ghost'; minus.style.padding = '4px 10px';
        const plus = document.createElement('button'); plus.textContent = '+'; plus.className = 'btn primary'; plus.style.padding = '4px 10px'; plus.style.marginLeft = '6px';
        minus.type = 'button'; plus.type = 'button';
        minus.setAttribute('aria-label', 'Take away a ' + c.label.toLowerCase().replace(/s$/, '') + ' block');
        plus.setAttribute('aria-label', 'Add a ' + c.label.toLowerCase().replace(/s$/, '') + ' block');
        minus.onclick = () => { touched = true; count[c.key] = Math.max(0, count[c.key] - 1); tip.textContent = ''; paint(); showTotal(); };
        plus.onclick = () => {
          touched = true;
          const max = spec.max ?? 9, full = count[c.key] >= max;
          count[c.key] = Math.min(max, count[c.key] + 1);
          const up = cols.findIndex(x => x.key === c.key) > 0;          // a bigger column to swap ten of these for
          tip.textContent = full ? (up && TIP[c.key] ? TIP[c.key] : 'That is as many as this column holds.') : '';
          paint(); showTotal();
        };
        ctrl.appendChild(minus); ctrl.appendChild(plus);
        col.appendChild(lab); col.appendChild(stack); col.appendChild(ctrl);
        wrap.appendChild(col);
      });
      host.appendChild(wrap); host.appendChild(tip); host.appendChild(total); paint(); showTotal();

      host.__empty = 'Add some blocks first.';
      host.__getValue = () => touched ? count.h * 100 + count.t * 10 + count.o : null;
      host.__feedback = (res) => { showTotal(); total.style.color = res.correct ? '#22c55e' : '#f85149'; };
    }
  };
})();
