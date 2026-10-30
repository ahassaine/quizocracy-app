/* Shared flow for the drills: fetch a question, read the answer, check it, show the day's progress. */
(function () {
  const $ = (id) => document.getElementById(id);
  async function post(url, body) {
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {}), credentials: 'same-origin' });
    if (r.status === 401) { location.href = '/learn'; return { ok: false }; }
    return r.json();
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

  function setDay(d) {
    if (!d) return;
    const pct = d.target ? Math.min(100, Math.round(100 * d.done / d.target)) : 0;
    $('dayDone').textContent = d.done; $('dayTarget').textContent = d.target;
    $('dayFill').style.width = pct + '%';
    $('dayBar').classList.toggle('done', d.done >= d.target);
    if (d.done >= d.target) $('dayMsg').textContent = 'Target reached for today! You can keep going.';
  }

  window.Drill = function (opts) {
    const act = opts.activity;
    let token = null, answered = false, shownAt = 0, busy = false, seq = 0;
    async function next() {
      const my = ++seq;
      answered = false; busy = true;
      $('feedback').className = 'feedback'; $('feedback').textContent = '';
      $('check').style.display = ''; $('check').disabled = false; $('next').style.display = 'none';
      const q = await post('/api/' + act + '/next');
      if (my !== seq) return;              // a newer request superseded this one
      busy = false;
      if (!q.ok) { $('feedback').textContent = 'Could not load a question.'; return; }
      token = q.token; setDay(q.day);
      opts.render(q);
      shownAt = Date.now();
    }
    async function check() {
      if (answered || busy || !token) return;
      const val = opts.read();
      if (val === null) { $('feedback').className = 'feedback warn'; $('feedback').textContent = 'Type your answer first.'; return; }
      busy = true;
      const res = await post('/api/' + act + '/check', Object.assign({ token, ms: Date.now() - shownAt }, val));
      busy = false;
      if (!res.ok) { $('feedback').textContent = 'That question expired — here is another.'; return next(); }
      answered = true; setDay(res.day);
      $('check').disabled = true; $('next').style.display = '';
      const fb = $('feedback');
      fb.className = 'feedback ' + (res.correct ? 'yes' : 'no');
      fb.innerHTML = res.correct ? '✅ Correct!' : '❌ Not quite. ' + opts.explain(res);
      if (opts.after) opts.after(res);
      if (res.correct && opts.autoNext) { const at = seq; setTimeout(() => { if (answered && at === seq) next(); }, opts.autoNext); }
      else $('next').focus();
    }
    $('check').addEventListener('click', check);
    $('next').addEventListener('click', next);
    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter') return;
      e.preventDefault();
      answered ? next() : check();
    });
    next();
    return { next, check, esc };
  };
  window.esc = esc;
})();
