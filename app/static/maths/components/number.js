/* number — typed numeric / text answer (constructed response). */
(function () {
  window.MComp = window.MComp || {};
  window.MComp["number"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const wrap = document.createElement('div'); wrap.className = 'row';
      const input = document.createElement('input');
      input.className = 'm-input'; input.type = 'text';
      // the server picks the keyboard the answer needs: iOS 'numeric' has no "." or "−", 'decimal' has no "−"
      input.inputMode = spec.text ? 'text' : (spec.keypad || 'text');
      input.placeholder = spec.placeholder || (spec.text ? 'type your answer' : 'type a number');
      input.autocomplete = 'off';
      wrap.appendChild(input);
      if (spec.unit) {
        const u = document.createElement('span'); u.textContent = spec.unit;
        u.style.color = '#8b949e'; wrap.appendChild(u);
      }
      host.appendChild(wrap);
      input.addEventListener('keydown', e => { if (e.key === 'Enter') api.submit(); });
      setTimeout(() => input.focus(), 30);
      host.__getValue = () => input.value.trim();
      host.__feedback = (res) => { input.style.borderColor = res.correct ? '#22c55e' : '#f85149'; };
    }
  };
})();
