/* Shared flow for the drills: fetch a question, read the answer, check it, show the day's progress. */
(function () {
  const $ = (id) => document.getElementById(id);
  const PUPIL = document.body.dataset.pupil;       // the child this page was opened for (see base.html)
  /* One request. It throws when there is no answer from the server (no connection, a timeout, a server that
     is restarting): the callers then wait and send the same thing again (send). */
  async function post(url, body) {
    body = Object.assign({}, body || {});
    if (PUPIL) body.pupil = PUPIL;                  // the server refuses if another child signed in since
    const ac = window.AbortController ? new AbortController() : null;
    const t = ac ? setTimeout(() => ac.abort(), 15000) : 0;      // Wi-Fi that hangs instead of failing
    try {
      const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body), credentials: 'same-origin', signal: ac ? ac.signal : undefined });
      if (r.status === 401) { location.href = '/learn'; return { ok: false }; }
      if (r.status > 500) throw new Error('server ' + r.status);      // 502/503/504: on its way back
      try { return await r.json(); }
      catch (e) { if (r.status === 500) return { ok: false, error: 'server' }; throw e; }   // not our server's answer (a Wi-Fi login page)
    } finally { clearTimeout(t); }
  }
  /* send(): post until it gets through. Between tries a note says the answer is safe; a try is made again after
     1, 2, 4 … 30 seconds, at once when the device is back online, or when the child taps Check or Next again
     (wake). still(): false once the page has moved on, and then nothing more is sent. The server takes each
     question's token once only, so sending an answer twice never counts it twice. */
  let wake = null, netNote = null;
  function offline(on, text) {
    if (!netNote) {
      const fb = $('feedback'); if (!fb) return;
      netNote = document.createElement('div'); netNote.className = 'feedback warn netmsg'; netNote.id = 'netMsg';
      netNote.setAttribute('role', 'status'); netNote.setAttribute('aria-live', 'polite'); netNote.setAttribute('data-testid', 'net-msg');
      fb.parentNode.insertBefore(netNote, fb);
    }
    netNote.hidden = !on; netNote.textContent = on ? (text || 'No connection — your answer is safe. Trying again…') : '';
  }
  function nap(ms) {
    return new Promise(res => {
      const done = () => { clearTimeout(t); removeEventListener('online', done); if (wake === done) wake = null; res(); };
      const t = setTimeout(done, ms);
      addEventListener('online', done); wake = done;
    });
  }
  async function send(url, body, still, text) {
    for (let i = 0; ; i++) {
      try { const r = await post(url, typeof body === 'function' ? body() : body); if (still()) offline(false); return r; }
      catch (e) {
        if (!still()) return null;
        offline(true, text);
        await nap(Math.min(30000, 1000 * Math.pow(2, i)));
        if (!still()) return null;
      }
    }
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

  let reached = null, rewarded = null, allDone = null;
  const FIX = new URLSearchParams(location.search).has('fix');      // ?fix=1: wrong answers come back first
  const FIX_CHECK = FIX && new URLSearchParams(location.search).has('check');   // &check=1: only the Year 4 check's misses
  const FIX_MOVED = FIX && new URLSearchParams(location.search).has('moved');   // &moved=1: on from another subject
  // the child's school year (from _drill_head.html; 0 on pages without a child): Years 1-3 get a big, happy
  // "Correct" and kind words sooner; Year 7 up a quiet one (13-year-olds don't want "for little kids")
  const YEAR = parseInt(($('drillHead') || { dataset: {} }).dataset.year, 10) || 0;
  const YOUNG = YEAR >= 1 && YEAR <= 3, TEEN = YEAR >= 7;
  const PRAISE = ['Well done!', 'Brilliant!', 'Super!', 'Great job!', 'Fantastic!'];
  function cheer() {
    if (YOUNG) return '<span class="joy-star" aria-hidden="true">★</span><span class="joy-word">Correct!</span> '
      + '<span class="joy-praise">' + PRAISE[Math.floor(Math.random() * PRAISE.length)] + '</span>';
    return '<span class="tick' + (TEEN ? ' quiet' : '') + '" aria-hidden="true">✓</span> Correct';
  }
  // after a run of misses (2 for Years 1-3, 3 after that) a kind word comes with the answer
  const KIND = TEEN ? 'Keep going: the next one is a fresh start.' : 'Good try! Let’s try another one.';
  let misses = 0;
  /* The day's line and bar. Returns what this answer changed: now (this activity's target is reached), hit (just
     reached), all (the whole day just reached 100%), won (the reward was just earned), reward (its text). */
  function setDay(d) {
    if (!d) return {};
    const now = d.done >= d.target;
    const out = { now, hit: reached === false && now, all: allDone === false && d.day_pct >= 100,
      won: rewarded === false && !!d.reward, reward: d.reward || '' };
    if (reached === false && now && window.QZ) QZ.confetti(140);     // the moment the target is reached
    reached = now;
    const pct = d.target ? Math.min(100, Math.floor(100 * d.done / d.target)) : 0;
    $('dayDone').textContent = d.done; $('dayTarget').textContent = d.target;
    $('dayFill').style.width = pct + '%';
    $('dayBar').classList.toggle('done', d.done >= d.target);
    if (d.day_pct >= 100) $('dayMsg').innerHTML = '<b>All done for today, well done!</b> <a href="/me">See my day</a>';
    else if (d.done >= d.target) $('dayMsg').textContent = 'Target reached for today! You can keep going.';
    const rw = $('dayReward');
    if (rw && d.reward) {
      if (rw.hidden && rewarded === false && window.QZ) QZ.confetti(220);   // the moment the reward is earned
      // earned before this page opened: one slim line, so the question and Check stay in view on a phone
      if (rw.hidden && rewarded === null) rw.classList.add('slim');
      rw.querySelector('span').textContent = 'You earned: ' + d.reward;
      rw.hidden = false;
    }
    rewarded = !!d.reward; allDone = d.day_pct >= 100;
    return out;
  }
  /* Once this activity's target is reached, the main button after an answer is "Back to My day", with a smaller
     "Keep going" (#next) beside it: a child who can't read the day line still sees that this part is finished. */
  function finishButtons(on) {
    let back = $('backDay');
    const nx = $('next');
    if (on && !back) {
      back = document.createElement('a'); back.id = 'backDay'; back.className = 'btn primary big'; back.href = '/me';
      back.setAttribute('data-testid', 'back-day'); back.textContent = 'Back to My day';
      nx.parentNode.insertBefore(back, nx);
    }
    if (back) back.style.display = on ? '' : 'none';
    nx.classList.toggle('big', !on); nx.textContent = on ? 'Keep going' : 'Next →';
  }

  window.Drill = function (opts) {
    const act = opts.activity, api = opts.api || ('/api/' + act + '/');   // opts.api: another endpoint (team testing page)
    let token = null, answered = false, shownAt = 0, busy = false, seq = 0, gone = false;
    let lastVal = null;                  // what was last sent to Check for this question (for a report)
    let skillName = '';                  // the skill of the question on screen (maths: title; grammar, science: skill)
    function switched(res) {        // another child signed in on this device (e.g. in another tab): stop here
      if (!res || res.error !== 'switched') return false;
      gone = true; token = null; ++seq;
      if (window.Speak) Speak.stop();
      const fb = $('feedback'); fb.className = 'feedback warn';
      fb.innerHTML = esc(res.name) + ' is signed in on this device now, so this page has stopped. '
        + '<a href="/learn">Go back to “Who’s learning?”</a>';
      $('check').disabled = true; $('next').style.display = 'none';
      return true;
    }
    let fixing = false, fixLeft = 0, fixDone = '', moved = FIX_MOVED;
    function fixNote(text) {             // text null: every mistake is done
      const m = $('fixMsg');
      if (text) { m.textContent = text; return; }
      m.innerHTML = esc(fixDone || 'All your mistakes are done. Well done!') + ' <a href="/me">Back to my day</a>'
        + (FIX_CHECK ? ' · <a href="/me/tables/year4-check">Try the check again</a>' : '');
    }
    /* "Something wrong with this question?" (_drill_buttons.html): a reason, a note if they like, sent with the
       question's token; the server keeps the question as it was served. */
    let reason = null, reporting = false;
    function reportReset() {
      if (!$('report')) return;
      reason = null; $('reportBox').hidden = true; $('reportOpen').hidden = false;
      $('reportOpen').setAttribute('aria-expanded', 'false'); $('reportMsg').textContent = ''; $('reportNote').value = '';
      $('reportBox').querySelectorAll('[data-reason]').forEach(b => { b.classList.remove('sel'); b.setAttribute('aria-checked', 'false'); });
    }
    if ($('report')) {
      $('reportOpen').addEventListener('click', () => {
        const open = $('reportBox').hidden;
        $('reportBox').hidden = !open; $('reportOpen').setAttribute('aria-expanded', String(open)); $('reportMsg').textContent = '';
      });
      $('reportBox').querySelectorAll('[data-reason]').forEach(b => b.addEventListener('click', () => {
        reason = b.dataset.reason;
        $('reportBox').querySelectorAll('[data-reason]').forEach(x => { x.classList.toggle('sel', x === b); x.setAttribute('aria-checked', String(x === b)); });
      }));
      $('reportCancel').addEventListener('click', () => { const m = $('reportMsg').textContent; reportReset(); $('reportMsg').textContent = m; });
      $('reportSend').addEventListener('click', async () => {
        if (!reason) { $('reportMsg').textContent = 'Tap what is wrong first.'; return; }
        if (reporting) { if (wake) wake(); return; }      // a tap while waiting for the connection: try now
        reporting = true;
        const body = { activity: act, token, reason, note: $('reportNote').value, answer: lastVal,
          device: { w: innerWidth, h: innerHeight, touch: 'ontouchstart' in window || navigator.maxTouchPoints > 0 } };
        const res = await send('/api/report', body, () => !gone, 'No connection — your report is safe. Trying again…');
        reporting = false;
        if (!res || switched(res)) return;
        reportReset(); $('reportOpen').hidden = true;
        $('reportMsg').textContent = res.ok ? "Thanks! We'll check it, and your grown-up can see it too."
          : (res.error === 'limit' ? 'Thanks! You have sent a lot of reports today, so we will look at those first.'
            : 'Sorry, that did not send. Try again in a moment.');
        if (!res.ok && res.error !== 'limit') $('reportOpen').hidden = false;
      });
    }
    let loading = false, checking = false;
    async function next(note) {          // note: a message shown with the new question, until it is answered
      if (gone) return;
      if (loading) { if (wake) wake(); return; }      // still waiting for the connection: a tap on Next tries now
      // the answered question, its "Correct" and Next stay on screen until the new question has arrived
      const my = ++seq; loading = busy = true;
      const body = opts.nextBody ? opts.nextBody() : (FIX ? (FIX_CHECK ? { fix: 1, check: 1 } : { fix: 1 }) : {});
      const q = await send(api + 'next', body, () => my === seq && !gone, 'No connection. The next question comes when you are back online…');
      if (my === seq) loading = false;
      if (my !== seq || !q) return;        // a newer request superseded this one
      busy = false;
      if (switched(q)) return;
      answered = false; lastVal = null; reportReset();
      $('feedback').className = 'feedback'; $('feedback').textContent = '';
      $('check').style.display = ''; $('check').disabled = false; $('next').style.display = 'none';
      if ($('backDay')) $('backDay').style.display = 'none';
      if (!q.ok) { $('feedback').textContent = 'Could not load a question.'; return; }
      token = q.token; setDay(q.day); skillName = q.title || q.skill || '';
      // "Practise my mistakes" runs through every subject: none ready here, so on to the next subject that has some
      if (FIX && !q.fixing && q.fix_next) { location.href = '/me/' + q.fix_next + '?fix=1&moved=1'; return; }
      fixing = FIX && q.fixing; fixLeft = q.fix_total != null ? q.fix_total : q.fix_left; fixDone = q.fix_done || '';
      // the server's line (fix_msg) says what comes and when; the first one after moving on names the subject
      if (FIX && $('fixMsg')) fixNote(q.fix_msg != null ? (q.fix_msg ? (moved ? 'Now ' + q.fix_title + ' · ' : '') + q.fix_msg : null)
        : q.fixing ? 'Putting a mistake right · ' + fixLeft + ' left'
        : (q.fix_later ? 'Your mistakes come back after a few other questions · ' + q.fix_later + ' waiting'
          : (fixLeft ? 'Your other mistakes come back a little later · ' + fixLeft + ' waiting' : null)));
      moved = false;
      opts.render(q);
      if (window.Speak) Speak.set(opts.speech ? opts.speech(q) : [q.prompt]);   // the 🔊 button (speak.js)
      document.body.dataset.qtoken = q.token;      // which question is on screen (used by the tests)
      if (typeof note === 'string') { $('feedback').className = 'feedback warn'; $('feedback').textContent = note; }
      shownAt = Date.now();
    }
    async function check() {
      if (busy && checking) { if (wake) wake(); return; }   // still waiting for the connection: a tap on Check tries now
      if (answered || busy || !token || gone) return;
      const val = opts.read();
      if (val === null) {                  // nothing given yet: the page may say what to do (opts.empty), e.g. "Add some blocks first."
        $('feedback').className = 'feedback warn';
        $('feedback').textContent = (opts.empty && opts.empty())
          || (document.querySelector('[data-testid=choices]') ? 'Tap your answer first.' : 'Type your answer first.');
        if (window.Speak) Speak.feedback($('feedback').textContent);       // Years 1-2 hear it: they may not read it
        return;
      }
      busy = checking = true; lastVal = val;
      const my = seq, ms = Date.now() - shownAt, sentFor = token;
      let tries = 0;
      // each try sends what is on screen then, so an answer changed while offline is the one marked
      const res = await send(api + 'check', () => {
        if (tries++) { const v = opts.read(); if (v !== null) lastVal = v; }
        const b = Object.assign({ token, ms }, lastVal);
        if (!opts.api) hold(api + 'check', b);        // kept until answered: if the connection drops, a refresh or another page sends it (ui.js)
        return b;
      }, () => my === seq && !gone);
      if (res && !opts.api) hold(null, { token: sentFor });
      busy = checking = false;
      if (!res || my !== seq) return;
      if (switched(res)) return;
      if (!res.ok && res.error === 'expired' && tries > 1)  // the answer reached the server before the connection dropped
        return next('Your answer was marked while the connection was down. Here is the next question.');
      if (!res.ok) return next('That question expired, so here is another one.');
      if (res.retry) {                     // a near miss ("eigth"): nothing marked, the same question stays open
        const fb = $('feedback'); fb.className = 'feedback warn'; fb.textContent = res.hint || 'Nearly. Check it and try again.';
        const a = $('answer') || $('past'); if (a && a.offsetParent && !a.readOnly) a.focus();
        if (window.Speak) Speak.feedback(fb.textContent);
        return;
      }
      answered = true; const day = setDay(res.day);
      if (fixing && res.correct && $('fixMsg')) {     // the count drops the moment a mistake is put right
        fixing = false; fixLeft = Math.max(0, fixLeft - 1);
        // right again in the same sitting: practised, and it comes back in a later one to count as put right
        if (fixLeft) fixNote((res.again_later ? 'Practised, it comes back later' : 'Mistake put right') + ' · ' + fixLeft + ' left');
      }
      $('check').disabled = true; $('next').style.display = '';
      finishButtons(!!day.now);
      const fb = $('feedback');
      // res.other: another real word, spelt right (spelling): not a mistake, so no "Not quite" and no shake
      fb.className = 'feedback ' + (res.correct ? 'yes' : res.other ? 'warn' : 'no') + (res.correct && YOUNG ? ' joy' : '');
      const st = $('stage');
      if (st) { st.classList.remove('shake', 'flash'); void st.offsetWidth; if (!res.other) st.classList.add(res.correct ? 'flash' : 'shake'); }
      misses = res.correct ? 0 : res.other ? misses : misses + 1;
      fb.innerHTML = res.correct ? cheer() + (res.again_later ? (YOUNG ? ' ' : '. ') + 'It comes back later, to check you remember it.' : '')
          + (res.hint ? '<div class="why" data-testid="hint">' + esc(res.hint) + '</div>' : '')
        : (res.other ? '' : 'Not quite. ') + opts.explain(res) + (res.hint ? '<div class="why" data-testid="hint">' + esc(res.hint) + '</div>' : '') + (misses >= (YOUNG ? 2 : 3) ? '<div class="kind" data-testid="kind">' + KIND + '</div>' : '');
      if (opts.after) opts.after(res);
      // moments that grow: a skill secure for the first time, an old mistake put right (the server says which)
      const wins = (res.mastered ? ['★ New skill secure' + (skillName ? ': ' + skillName : '') + '!'] : [])
        .concat(res.put_right ? ['★ You put right a mistake from before. Well done!'] : []);
      if (wins.length) {
        fb.insertAdjacentHTML('beforeend', wins.map(w => '<div class="win-moment" data-testid="win-moment">' + esc(w) + '</div>').join(''));
        if (window.QZ && !day.hit) QZ.confetti(res.mastered ? 120 : 60);
      }
      // Years 1-2 hear it too, and hear when they have finished: they may not read the day line or the reward
      const done = day.all ? ' All done for today!' + (day.reward ? ' You earned: ' + day.reward + '.' : '')
        : day.won ? ' You earned: ' + day.reward + '.' : day.hit ? ' That is all for today here. Tap Back to My day.' : '';
      // opts.spoken(res): what to say instead of the screen's words (spelling says the letters one by one)
      if (window.Speak) Speak.feedback(((opts.spoken && opts.spoken(res)) || (fb.innerText || fb.textContent).replace(/★/g, '').replace(/\s*\n+\s*/g, '. ')) + done);
      if (res.correct && opts.autoNext && !day.hit) { const at = seq; setTimeout(() => { if (answered && at === seq) next(); }, opts.autoNext); }
      else $('next').focus();
    }
    $('check').addEventListener('click', check);
    $('next').addEventListener('click', next);
    document.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter') return;
      if (e.target && e.target.closest && e.target.closest('#report, #a11y, #a11yPanel')) return;   // a report or the Aa settings, not an answer
      e.preventDefault();
      answered ? next() : check();
    });
    // an answer kept from a page that lost its connection goes first, so this page does not ask that question again
    const kept = window.QZ && QZ.flushPending && !opts.api ? QZ.flushPending() : Promise.resolve(false);
    kept.then(sent => next(sent ? 'Your answer from before has been sent.' : undefined));
    return { next, check, esc };
  };
  /* The answer of a Check that had no connection, in localStorage until the server has it (url null: it has).
     Only one at a time: a newer answer replaces it. Not for the team's testing pages (opts.api). */
  function hold(url, body) {
    try {
      const key = (window.QZ && QZ.PKEY) || 'qz_pending';
      if (url) { localStorage.setItem(key, JSON.stringify({ url, body: Object.assign({ pupil: PUPIL }, body), at: Date.now() })); return; }
      const p = JSON.parse(localStorage.getItem(key) || 'null');
      if (p && p.body && p.body.token === body.token) localStorage.removeItem(key);
    } catch (e) {}
  }
  window.esc = esc;

  /* A typed answer that can only be one of a few words the question itself names ("(type yes or no)",
     "Type yes or no.", "(A or B)", "Is it living, dead or never alive?", "odd or even?"): those words, else null.
     Read from how the question is written, the same text the child reads; the answer is never sent here. */
  const PAIR = /\b(yes or no|true or false|odd or even|even or odd|more or less|bigger or smaller|living, dead or never alive)(\s+[a-z]+)?\s*\?/i;
  function words(list) {
    const w = list.split(/\s*,\s*|\s+or\s+/i).map(x => x.trim().replace(/^['"‘“]+|['"’”.]+$/g, '').trim()).filter(Boolean);
    return w.length >= 2 && w.length <= 4 && w.every(x => x.length <= 20 && x.split(/\s+/).length <= 3 && !/[\d%=:]/.test(x)
      && !FORM.test(x)) ? w : null;
  }
  const FORM = /\b(numbers?|fractions?|form|words?|decimals?|units?)\b/i;      // "(a fraction or a whole number)" is how to write it
  window.Drill.choices = function (prompt, placeholder) {
    const s = String(prompt || '');
    const br = s.match(/\(\s*(?:type\s+)?([^()]+?\s+or\s+[^()]+?)\s*\)/gi);          // the last "( … or … )"
    if (br) { const w = words(br[br.length - 1].replace(/^\(\s*(?:type\s*:?\s+)?|\s*\)$/gi, '')); if (w) return w; }
    const ty = s.match(/\b(?:type|answer)\s+((?:'[^']+'|\w+)\s+or\s+(?:'[^']+'|\w+))(?=\s*(?:[.?!]|for\b|$))/i);
    if (ty) { const w = words(ty[1]); if (w) return w; }
    const p = s.match(PAIR) || s.match(/^(true or false)\b/i);
    if (p) return words(p[1].toLowerCase());
    return placeholder && /^yes or no$/i.test(String(placeholder).trim()) ? ['yes', 'no'] : null;
  };
  /* Tap buttons for those words, put after `input`'s row; a tap writes the word into the input, which stays the
     answer. hide: the box goes (Years 1-4 can't spell "never alive"); otherwise buttons and box side by side. */
  window.Drill.choiceButtons = function (input, list, hide, anchor) {
    const box = document.createElement('div'); box.className = 'opts choices'; box.setAttribute('data-testid', 'choices');
    list.forEach((w, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'opt';
      b.textContent = w === w.toLowerCase() && w.length > 2 ? w.charAt(0).toUpperCase() + w.slice(1) : w;   // not "Ml", "X"
      b.dataset.value = w; b.setAttribute('data-testid', 'choice-' + i);
      b.addEventListener('click', () => { if (b.disabled) return;
        input.value = w; input.dispatchEvent(new Event('input', { bubbles: true }));
        box.querySelectorAll('.opt').forEach(x => x.classList.toggle('sel', x === b));
        if (window.Speak) Speak.word(w); });
      box.appendChild(b);
    });
    const at = anchor || input;
    at.parentNode.insertBefore(box, at.nextSibling);
    if (hide) { input.style.display = 'none'; input.tabIndex = -1; }
    box.__mark = (res) => box.querySelectorAll('.opt').forEach(b => {     // after Check: green for right, pink for a miss
      b.disabled = true;
      const right = String(res.expected || '').trim().toLowerCase() === b.dataset.value.toLowerCase();
      if (b.classList.contains('sel')) b.classList.add(res.correct ? 'right' : 'wrong');
      else if (!res.correct && right) b.classList.add('right');
    });
    return box;
  };
})();
