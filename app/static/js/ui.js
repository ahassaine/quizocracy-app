/* Theme toggle, animated bars and counters, confetti. */
(function () {
  const root = document.documentElement;
  const btn = document.getElementById('themeBtn');
  function current() { return root.dataset.theme || 'light'; }
  const SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  const MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  function paint() { if (btn) btn.innerHTML = current() === 'dark' ? SUN : MOON; }
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
      const colors = ['#4F46E5', '#F43F5E', '#F59E0B', '#14B8A6', '#0EA5E9'];
      for (let i = 0; i < Math.min(n || 60, 70); i++) {
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
