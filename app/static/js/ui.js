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
  const calm = () => reduce || root.classList.contains('a11y-calm');
  function fillBars(scope) {
    (scope || document).querySelectorAll('.bar > i[data-w]').forEach((el) => {
      requestAnimationFrame(() => { el.style.width = el.dataset.w + '%'; });
    });
  }
  function countUp(scope) {
    (scope || document).querySelectorAll('[data-count]').forEach((el) => {
      const to = parseInt(el.dataset.count, 10) || 0, suffix = el.dataset.suffix || '';
      if (calm() || to === 0) { el.textContent = to + suffix; return; }
      const t0 = performance.now(), dur = 900;
      (function step(t) {
        const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        el.textContent = Math.round(to * e) + suffix;
        if (k < 1) requestAnimationFrame(step);
      })(t0);
    });
  }
  window.QZ = {
    fillBars, countUp, flushPending, calm, PKEY: 'qz_pending',
    confetti(n) {
      if (calm()) return;              // "Calm screen" (a grown-up's, the child's Aa, or the device's reduced motion)
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
  /* An answer whose Check had no connection (drill.js keeps it in localStorage until the server has it) is sent on
     the next page load (the offline page reloads itself once back online): "your answer is safe" holds after a
     refresh or leaving the page. Only for the child it belongs to (the server refuses another child anyway), within
     12 hours. A page that is still trying (drill.js) sends it itself. */
  const PKEY = 'qz_pending';
  let flushing = null;
  function flushPending() {
    if (flushing) return flushing;
    let p = null;
    try { p = JSON.parse(localStorage.getItem(PKEY) || 'null'); } catch (e) {}
    const pupil = document.body && document.body.dataset.pupil;
    if (!p || !p.url || !p.body || !pupil || p.body.pupil !== pupil) return Promise.resolve(false);
    const drop = () => { try { const q = JSON.parse(localStorage.getItem(PKEY) || 'null');
      if (q && q.body && q.body.token === p.body.token) localStorage.removeItem(PKEY); } catch (e) {} };
    if (Date.now() - (p.at || 0) > 12 * 3600 * 1000) { drop(); return Promise.resolve(false); }
    flushing = fetch(p.url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p.body),
      credentials: 'same-origin' })
      .then(r => { if (r.status === 401 || r.status >= 502) return false; drop(); return r.ok; })    // 409: marked already
      .catch(() => false).finally(() => { flushing = null; });
    return flushing;
  }
  if (document.body && document.body.dataset.pupil) {
    flushPending();
    flushCheck();
  }
  /* The same for a Year 4 check finished without a connection (tables_check.html keeps it under MKEY until the
     server has marked it; that page sends it itself). On My day the page then reloads, to show it counted. */
  function flushCheck() {
    const MKEY = 'qz_mtc_done';
    if (location.pathname === '/me/tables/year4-check') return;
    let p = null;
    try { p = JSON.parse(localStorage.getItem(MKEY) || 'null'); } catch (e) {}
    if (!p || !p.url || !p.body || p.body.pupil !== document.body.dataset.pupil) return;
    if (Date.now() - (p.at || 0) > 12 * 3600 * 1000) { try { localStorage.removeItem(MKEY); } catch (e) {} return; }
    fetch(p.url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(p.body), credentials: 'same-origin' })
      .then(r => { if (r.status === 401 || r.status >= 502) return;
        try { const q = JSON.parse(localStorage.getItem(MKEY) || 'null'); if (q && q.body && q.body.token === p.body.token) localStorage.removeItem(MKEY); } catch (e) {}
        if (r.ok && location.pathname === '/me') location.reload(); })
      .catch(() => {});
  }
  // A child left signed in goes back to "Who's learning?" after 10 minutes without a tap or a key (deps.CHILD_IDLE),
  // so a brother or sister picking up the tablet needs their own PIN. Nothing is lost: an unanswered question comes back.
  if (document.body && document.body.dataset.pupil) {
    let idleT = 0;
    const idle = () => { clearTimeout(idleT); idleT = setTimeout(() => { location.href = '/learn?away=1'; }, 10 * 60 * 1000); };   // the picker says why
    ['pointerdown', 'keydown', 'touchstart'].forEach(ev => document.addEventListener(ev, idle, { passive: true, capture: true }));
    idle();
  }
  document.addEventListener('DOMContentLoaded', () => { fillBars(); countUp(); });
  if (document.readyState !== 'loading') { fillBars(); countUp(); }
})();
