/* Shared flow for the drills: fetch a question, read the answer, check it, show the day's progress. */
(function () {
  const $ = (id) => document.getElementById(id);
  const PUPIL = document.body.dataset.pupil;       // the child this page was opened for (see base.html)
  async function post(url, body) {
    body = Object.assign({}, body || {});
    if (PUPIL) body.pupil = PUPIL;                  // the server refuses if another child signed in since
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body), credentials: 'same-origin' });
    if (r.status === 401) { location.href = '/learn'; return { ok: false }; }
    return r.json();
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

  let reached = null, rewarded = null;
  const FIX = new URLSearchParams(location.search).has('fix');      // ?fix=1: wrong answers come back first
  function setDay(d) {
    if (!d) return;
    const now = d.done >= d.target;
    if (reached === false && now && window.QZ) QZ.confetti(140);     // the moment the target is reached
    reached = now;
    const pct = d.target ? Math.min(100, Math.floor(100 * d.done / d.target)) : 0;
    $('dayDone').textContent = d.done; $('dayTarget').textContent = d.target;
    $('dayFill').style.width = pct + '%';
    $('dayBar').classList.toggle('done', d.done >= d.target);
    if (d.done >= d.target) $('dayMsg').textContent = 'Target reached for today! You can keep going.';
    const rw = $('dayReward');
    if (rw && d.reward) {
      if (rw.hidden && rewarded === false && window.QZ) QZ.confetti(220);   // the moment the reward is earned
      rw.querySelector('span').textContent = 'You earned: ' + d.reward;
      rw.hidden = false;
    }
    rewarded = !!d.reward;
  }

  window.Drill = function (opts) {
    const act = opts.activity, api = opts.api || ('/api/' + act + '/');   // opts.api: another endpoint (team testing page)
    let token = null, answered = false, shownAt = 0, busy = false, seq = 0, gone = false;
    function switched(res) {        // another child signed in on this device (e.g. in another tab): stop here
      if (!res || res.error !== 'switched') return false;
      gone = true; token = null; ++seq;
      const fb = $('feedback'); fb.className = 'feedback warn';
      fb.innerHTML = esc(res.name) + ' is signed in on this device now, so this page has stopped. '
        + '<a href="/learn">Go back to “Who’s learning?”</a>';
      $('check').disabled = true; $('next').style.display = 'none';
      return true;
    }
    async function next(note) {          // note: a message shown with the new question, until it is answered
      if (gone) return;
      const my = ++seq;
      answered = false; busy = true;
      $('feedback').className = 'feedback'; $('feedback').textContent = '';
      $('check').style.display = ''; $('check').disabled = false; $('next').style.display = 'none';
      const q = await post(api + 'next', opts.nextBody ? opts.nextBody() : (FIX ? { fix: 1 } : {}));
      if (my !== seq) return;              // a newer request superseded this one
      busy = false;
      if (switched(q)) return;
      if (!q.ok) { $('feedback').textContent = 'Could not load a question.'; return; }
      token = q.token; setDay(q.day);
      if (FIX && $('fixMsg')) $('fixMsg').textContent = q.fixing
        ? 'Putting a mistake right · ' + q.fix_left + ' left' : 'No mistakes left to fix here. Well done!';
      opts.render(q);
      document.body.dataset.qtoken = q.token;      // which question is on screen (used by the tests)
      if (typeof note === 'string') { $('feedback').className = 'feedback warn'; $('feedback').textContent = note; }
      shownAt = Date.now();
    }
    async function check() {
      if (answered || busy || !token || gone) return;
      const val = opts.read();
      if (val === null) {                  // nothing given yet: the page may say what to do (opts.empty), e.g. "Add some blocks first."
        $('feedback').className = 'feedback warn';
        $('feedback').textContent = (opts.empty && opts.empty()) || 'Type your answer first.'; return;
      }
      busy = true;
      const res = await post(api + 'check',Object.assign({ token, ms: Date.now() - shownAt }, val));
      busy = false;
      if (switched(res)) return;
      if (!res.ok) return next('That question expired, so here is another one.');
      answered = true; setDay(res.day);
      $('check').disabled = true; $('next').style.display = '';
      const fb = $('feedback');
      fb.className = 'feedback ' + (res.correct ? 'yes' : 'no');
      const st = $('stage');
      if (st) { st.classList.remove('shake', 'flash'); void st.offsetWidth; st.classList.add(res.correct ? 'flash' : 'shake'); }
      fb.innerHTML = res.correct ? 'Correct' : 'Not quite. ' + opts.explain(res);
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
