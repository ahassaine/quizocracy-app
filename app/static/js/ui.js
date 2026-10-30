/* Theme toggle, animated bars and counters, confetti. */
(function () {
  const root = document.documentElement;
  const btn = document.getElementById('themeBtn');
  function current() { return root.dataset.theme || 'light'; }
  function paint() { if (btn) btn.textContent = current() === 'dark' ? '☀️' : '🌙'; }
  if (btn) btn.addEventListener('click', () => {
    const t = current() === 'dark' ? 'light' : 'dark';
    root.dataset.theme = t;
    try { localStorage.setItem('qz_theme', t); } catch (e) {}
    paint();
  });
  paint();

  const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function fillBars(scope) {
    (scope || document).querySelectorAll('.bar > i[data-w]').forEach((el) => {
      requestAnimationFrame(() => { el.style.width = el.dataset.w + '%'; });
    });
  }
  function countUp(scope) {
    (scope || document).querySelectorAll('[data-count]').forEach((el) => {
      const to = parseInt(el.dataset.count, 10) || 0, suffix = el.dataset.suffix || '';
      if (reduce || to === 0) { el.textContent = to + suffix; return; }
      const t0 = performance.now(), dur = 900;
      (function step(t) {
        const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(to * e) + suffix;
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    });
  }
  window.QZ = {
    fillBars, countUp,
    confetti(n) {
      if (reduce) return;
      const box = document.createElement('div'); box.className = 'confetti';
      const colors = ['#7C5CFF', '#FF7A59', '#FFC542', '#2ED3A0', '#3DB4FF'];
      for (let i = 0; i < (n || 90); i++) {
        const p = document.createElement('i');
        p.style.left = Math.random() * 100 + 'vw';
        p.style.background = colors[i % colors.length];
        p.style.animationDuration = (1.6 + Math.random() * 1.6) + 's';
        p.style.animationDelay = (Math.random() * .4) + 's';
        p.style.transform = 'rotate(' + (Math.random() * 360) + 'deg)';
        box.appendChild(p);
      }
      document.body.appendChild(box);
      setTimeout(() => box.remove(), 3800);
    },
  };
  document.addEventListener('DOMContentLoaded', () => { fillBars(); countUp(); });
  if (document.readyState !== 'loading') { fillBars(); countUp(); }
})();
