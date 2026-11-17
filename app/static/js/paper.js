/* A SATs practice paper (drills/sats.py): one question at a time against the paper's clock, nothing marked until
   the end. "Skip for now" leaves a question for later; once every question has been seen, the skipped ones come
   round again. Finishing (or the clock running out) sends every answer at once; the result lists each question
   with its answer and why. A finished paper waiting for the server is kept in localStorage and sent again. */
function Paper(PAPER) {
  const $ = (id) => document.getElementById(id);
  const PUPIL = document.body.dataset.pupil, YEAR = parseInt(($('drillHead') || {}).dataset ? $('drillHead').dataset.year : 0, 10) || 0;
  const DKEY = 'qz_sats_done';
  let token = null, qs = [], answers = [], seen = [], at = 0, deadline = 0, secs = 0, tick = 0, finishing = false, picks = {}, warned = false;
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  async function post(url, body) {
    const ac = window.AbortController ? new AbortController() : null;
    const t = ac ? setTimeout(() => ac.abort(), 20000) : 0;
    try {
      const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin',
        body: JSON.stringify(Object.assign({ pupil: PUPIL }, body)), signal: ac ? ac.signal : undefined });
      let data = null; try { data = await r.json(); } catch (e) {}
      return { status: r.status, data };
    } finally { if (t) clearTimeout(t); }
  }
  function store(v) { try { if (v) localStorage.setItem(DKEY, JSON.stringify(v)); else localStorage.removeItem(DKEY); } catch (e) {} }
  function stored() { try { return JSON.parse(localStorage.getItem(DKEY) || 'null'); } catch (e) { return null; } }

  /* ---- one question ---- */
  function render() {
    const q = qs[at], area = $('pArea');
    picks = {};
    area.innerHTML = '';
    nav();
    $('pCount').textContent = 'Question ' + (at + 1) + ' of ' + qs.length;
    $('pPrompt').textContent = q.prompt || '';
    $('pPrompt').hidden = q.kind === 'maths';
    seen[at] = true;
    if (q.kind === 'maths') {
      const pr = document.createElement('div'); pr.className = 'm-prompt'; pr.textContent = q.prompt; area.appendChild(pr);
      const host = document.createElement('div'); host.className = 'm-host'; host.id = 'mHost'; area.appendChild(host);
      const comp = (window.MComp || {})[q.component];
      if (comp) comp.render(host, q.spec || {}, { submit: () => next(false), year: YEAR, prompt: q.prompt });
      else host.textContent = 'This question cannot be shown here. Skip it.';
    } else if (q.kind === 'spelling') {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'btn hear'; b.setAttribute('data-testid', 'paper-play');
      b.innerHTML = '<span aria-hidden="true">🔊</span> Hear the word';
      const audio = new Audio('/api/sats/audio/' + encodeURIComponent(token) + '/' + at);
      b.addEventListener('click', () => { try { audio.currentTime = 0; audio.play(); } catch (e) {} });
      area.appendChild(b);
      if (q.sentence) { const s = document.createElement('div'); s.className = 'bq'; s.setAttribute('data-testid', 'paper-sentence');
        s.textContent = q.sentence; area.appendChild(s); }
      area.appendChild(input('text'));
      // the word did not play (sound off, a silent phone): say so, and give its number of letters as the daily
      // spelling does, so the sentence alone is not a guessing game
      const noSound = () => { if ($('pNoSound')) return; const n = document.createElement('div'); n.id = 'pNoSound'; n.className = 'small';
        n.setAttribute('data-testid', 'paper-nosound'); n.style.fontWeight = '700';
        n.textContent = 'The word did not play. Turn the sound up and press Hear the word. It has ' + q.letters + ' letters.';
        area.insertBefore(n, area.querySelector('.row')); };
      audio.addEventListener('error', noSound);
      try { const pr = audio.play(); if (pr && pr.catch) pr.catch(noSound); } catch (e) { noSound(); }
      b.addEventListener('click', () => { setTimeout(() => { if (audio.paused && audio.currentTime === 0) noSound(); }, 1500); });
    } else bank(q, area);
    restore(q, area);
    const a = area.querySelector('input,textarea'); if (a && q.kind !== 'maths') a.focus();
    $('pSkip').hidden = false;
  }
  /* an answer given before, shown again when the child comes back to a question (a maths picture cannot be
     filled in again: its answer is named, and kept unless they give a new one) */
  function restore(q, area) {
    const v = answers[at];
    if (v === null || v === undefined) return;
    if (q.kind === 'maths') {
      const n = document.createElement('div'); n.className = 'small'; n.setAttribute('data-testid', 'paper-kept');
      n.style.fontWeight = '700'; n.textContent = 'Your answer: ' + (Array.isArray(v) ? v.join(', ') : typeof v === 'object' ? JSON.stringify(v) : v)
        + '. Answer again to change it, or press Next to keep it.';
      area.insertBefore(n, area.firstChild.nextSibling); return;
    }
    if (q.kind === 'mcq') { picks.v = v; const b = area.querySelectorAll('.opt')[v]; if (b) b.classList.add('sel'); return; }
    if (q.kind === 'tap') { picks.v = v.slice(); v.forEach(i => { const b = area.querySelectorAll('.word')[i]; if (b) b.classList.add('sel'); }); return; }
    if (q.kind === 'order') { picks.v = v.slice(); area.querySelectorAll('.order .opt').forEach((b, i) => { const k = picks.v.indexOf(i);
      b.classList.toggle('sel', k >= 0); b.querySelector('.num').textContent = k >= 0 ? String(k + 1) : ''; }); return; }
    const a = $('pAnswer'); if (a) a.value = v;
  }
  /* the question numbers: go to any question, answered ones filled in */
  function nav() {
    const box = $('pNav'); if (!box) return;
    box.innerHTML = '';
    qs.forEach((q, k) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = String(k + 1);
      b.className = 'pn' + (answers[k] !== null ? ' done' : '') + (k === at ? ' cur' : '');
      b.setAttribute('aria-label', 'Question ' + (k + 1) + (answers[k] !== null ? ', answered' : ', not answered'));
      b.setAttribute('data-testid', 'paper-nav-' + (k + 1));
      b.addEventListener('click', () => { keep(); at = k; $('pReview').hidden = true; $('pRun').hidden = false;
        $('pRunNav').appendChild($('pNav')); render(); });
      box.appendChild(b); });
  }
  function keep() { if ($('pRun').hidden) return; const v = value(); if (v !== null) answers[at] = v; }
  function input(kind, unit) {
    const row = document.createElement('div'); row.className = 'row';
    const i = document.createElement('input'); i.type = 'text'; i.id = 'pAnswer'; i.autocomplete = 'off';
    i.className = kind === 'num' ? 'answer' : 'answer wide'; i.setAttribute('spellcheck', 'false'); i.setAttribute('autocapitalize', 'off');
    i.setAttribute('data-testid', 'paper-answer');
    if (kind === 'num') i.inputMode = 'decimal';
    i.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); next(false); } });
    row.appendChild(i);
    if (unit) { const u = document.createElement('span'); u.className = 'unit'; u.textContent = unit; row.appendChild(u); }
    return row;
  }
  function bank(q, area) {
    if (q.kind === 'mcq') {
      const box = document.createElement('div'); box.className = 'opts';
      q.opts.forEach((o, i) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'opt'; b.textContent = o;
        b.setAttribute('data-testid', 'paper-opt-' + i);
        b.addEventListener('click', () => { picks.v = i; box.querySelectorAll('.opt').forEach(x => x.classList.toggle('sel', x === b)); });
        box.appendChild(b); });
      area.appendChild(box);
    } else if (q.kind === 'tap') {
      const box = document.createElement('div'); box.className = 'words'; picks.v = [];
      q.words.forEach((w, i) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'word'; b.textContent = w;
        b.setAttribute('data-testid', 'paper-word-' + i);
        b.addEventListener('click', () => { const k = picks.v.indexOf(i); if (k >= 0) picks.v.splice(k, 1); else picks.v.push(i);
          b.classList.toggle('sel', k < 0); });
        box.appendChild(b); });
      area.appendChild(box);
    } else if (q.kind === 'order') {
      const tip = document.createElement('div'); tip.className = 'mut small'; tip.textContent = 'Tap them in order: first, then second… Tap one again to take it out.';
      const box = document.createElement('div'); box.className = 'opts order'; picks.v = [];
      const paint = () => box.querySelectorAll('.opt').forEach((b, i) => { const k = picks.v.indexOf(i);
        b.classList.toggle('sel', k >= 0); b.querySelector('.num').textContent = k >= 0 ? String(k + 1) : ''; });
      q.items.forEach((t, i) => { const b = document.createElement('button'); b.type = 'button'; b.className = 'opt';
        b.setAttribute('data-testid', 'paper-item-' + i);
        b.innerHTML = '<span class="num" aria-hidden="true"></span><span>' + esc(t) + '</span>';
        b.addEventListener('click', () => { const k = picks.v.indexOf(i); if (k >= 0) picks.v.splice(k, 1); else picks.v.push(i); paint(); });
        box.appendChild(b); });
      area.appendChild(tip); area.appendChild(box);
    } else if (q.kind === 'write') {
      const lab = document.createElement('div'); lab.className = 'mut small'; lab.textContent = 'The words are in the box. Change them there.';
      const t = document.createElement('textarea'); t.id = 'pAnswer'; t.className = 'write'; t.rows = 2; t.value = q.s;
      t.setAttribute('spellcheck', 'false'); t.setAttribute('data-testid', 'paper-write');
      area.appendChild(lab); area.appendChild(t);
      const rs = document.createElement('button'); rs.type = 'button'; rs.className = 'linkish small'; rs.setAttribute('data-testid', 'paper-write-reset');
      rs.textContent = '↺ Start again with the sentence as it was'; rs.addEventListener('click', () => { t.value = q.s; t.focus(); });
      area.appendChild(rs);
    } else {
      area.appendChild(input(q.kind === 'num' ? 'num' : 'text', q.unit));
      if (q.gap) $('pAnswer').placeholder = 'Type the missing word(s)';
    }
  }
  function value() {
    const q = qs[at];
    if (q.kind === 'maths') { const h = $('mHost'); const v = h && h.__getValue ? h.__getValue() : null;
      return (v === null || v === '' || (typeof v === 'number' && isNaN(v))) ? null : v; }
    if (q.kind === 'mcq') return picks.v === undefined ? null : picks.v;
    if (q.kind === 'tap') return picks.v && picks.v.length ? picks.v.slice() : null;
    if (q.kind === 'order') return picks.v && picks.v.length === q.items.length ? picks.v.slice() : null;
    const a = $('pAnswer'); const v = a ? a.value.trim() : '';
    return v ? v : null;
  }
  /* the next question: one not seen yet, then the skipped ones (left blank) in turn */
  function nextIndex() {
    for (let k = at + 1; k < qs.length; k++) if (!seen[k]) return k;
    if (seen.every(Boolean)) { for (let k = at + 1; k < qs.length; k++) if (answers[k] === null) return k; }
    for (let k = 1; k <= qs.length; k++) { const j = (at + k) % qs.length; if (answers[j] === null && j !== at) return j; }
    return -1;
  }
  function next(skip) {
    if (finishing) return;
    const v = skip ? null : value();
    if (!skip && v === null && answers[at] === null) { $('pMsg').textContent = qs[at].kind === 'order' ? 'Number every one, or press Skip for now.' : 'Answer it, or press Skip for now.'; return; }
    $('pMsg').textContent = '';
    if (!skip && v !== null) answers[at] = v;
    const left = answers.filter(a => a === null).length;
    $('pLeft').textContent = left ? left + ' not answered yet' : 'All answered';
    const k = nextIndex();
    if (k < 0 || (skip && k === at)) { review(); return; }
    at = k; render();
  }
  function review() {            // every question answered or skipped: finish, or go back to the skipped ones
    const left = answers.filter(a => a === null).length;
    $('pRun').hidden = true; $('pReview').hidden = false;
    $('pReviewText').textContent = left ? 'You have ' + left + ' question' + (left > 1 ? 's' : '') + ' not answered. Go back to them, or finish now.'
      : 'You have answered every question. Tap a number to check one again, or finish now.';
    $('pBack').hidden = !left;
    const r = $('pReviewNav'); if (r && $('pNav')) r.appendChild($('pNav'));
  }
  function clock() {
    const leftMs = deadline - Date.now(), s = Math.max(0, Math.ceil(leftMs / 1000));
    $('pClock').textContent = Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0');
    $('pFill').style.width = Math.max(0, 100 * leftMs / (secs * 1000)) + '%';
    $('pClock').classList.toggle('low', s <= 60);
    if (s === 60 && !warned) { warned = true; $('pMsg').textContent = 'One minute left.'; setTimeout(() => { if ($('pMsg').textContent === 'One minute left.') $('pMsg').textContent = ''; }, 6000); }
    if (leftMs <= 0) { clearInterval(tick); $('pMsg').textContent = 'Time is up.'; finish(true); }
  }
  async function start() {
    $('pIntro').hidden = true; $('pMsg').textContent = 'Getting your paper ready…';
    let r;
    try { r = await post('/api/sats/start', { paper: PAPER }); } catch (e) { r = null; }
    if (!r || r.status !== 200 || !r.data || !r.data.ok) {
      $('pIntro').hidden = false; $('pMsg').textContent = r && r.status === 409 ? 'Someone else signed in on this device. Go back to My day.'
        : 'The paper could not start. Check the connection and try again.'; return; }
    const d = r.data; token = d.token; qs = d.questions; secs = d.seconds;
    answers = qs.map(() => null); seen = qs.map(() => false); at = 0;
    if (d.passage) {
      const P = d.passage, box = $('passage'); box.hidden = false;
      $('passageBody').innerHTML = '<div class="mut small">' + esc(P.kind) + '</div><h2 class="passage-title" data-testid="passage-title">' + esc(P.title) + '</h2>'
        + String(P.text).split(/\n\s*\n/).map(p => '<p>' + esc(p.trim()).replace(/\n/g, '<br>') + '</p>').join('');
    }
    $('pMsg').textContent = ''; $('pRun').hidden = false; warned = false;
    deadline = Date.now() + secs * 1000; clock(); tick = setInterval(clock, 500);
    $('pLeft').textContent = qs.length + ' not answered yet';
    render();
  }
  async function finish(timeUp) {
    if (finishing) return;
    keep();                     // what is in the box when the time runs out counts, like pencil on the paper
    finishing = true; clearInterval(tick);
    const used = Math.round(secs - Math.max(0, (deadline - Date.now()) / 1000));
    const body = { token, answers, used };
    store(body);
    await send(body);
  }
  async function send(body) {
    finishing = true;
    $('pRun').hidden = true; $('pReview').hidden = true; $('pMsg').textContent = 'Marking your paper…';
    for (let tries = 0; tries < 30; tries++) {
      let r = null;
      try { r = await post('/api/sats/finish', body); } catch (e) {}
      if (r && r.status === 200 && r.data && r.data.ok) { store(null); result(r.data); return; }
      if (r && r.status === 409) { store(null); $('pMsg').textContent = 'This paper was already marked, or it is too old. Start a new one from the papers page.'; return; }
      $('pMsg').textContent = 'No connection: your answers are kept on this device. Trying again…';
      await new Promise(res => setTimeout(res, 5000));
    }
  }
  function result(d) {
    $('pMsg').textContent = '';
    $('pDone').hidden = false;
    $('pScore').textContent = d.score; $('pOf').textContent = d.of;
    $('pBest').hidden = !d.best;
    const mins = d.used != null ? Math.floor(d.used / 60) + ' min ' + (d.used % 60) + ' s' : '';
    $('pTime').textContent = (mins ? 'Time used: ' + mins + ' of ' + Math.round(d.secs / 60) + ' minutes.' : '')
      + (d.blank ? ' ' + d.blank + ' left blank.' : '');
    $('pCounted').textContent = d.counted ? 'Your answers count towards today. Any you missed are now in Practise my mistakes.' : '';
    $('pRows').innerHTML = d.rows.map((r, i) => '<div class="paper-row ' + (r.correct ? 'ok' : 'bad') + '" data-testid="paper-row">'
      + '<div class="kid"><b>' + (i + 1) + '.</b><span class="chip ' + (r.correct ? 'done' : '') + '">' + (r.correct ? '✓ right' : r.blank ? 'not answered' : '✗ not quite') + '</span></div>'
      + '<div style="margin:4px 0">' + esc(r.prompt) + '</div>'
      + (r.blank ? '' : '<div class="small"><span class="mut">You wrote:</span> ' + esc(r.given) + '</div>')
      + (r.correct ? '' : '<div class="small"><span class="mut">The answer:</span> <b>' + esc(r.expected) + '</b></div>')
      + (!r.correct && r.why ? '<div class="why small">' + esc(r.why) + '</div>' : '')
      + (!r.correct && r.layout && r.layout.grid ? '<pre class="m-col small" style="font:600 .9rem/1.3 ui-monospace,Menlo,Consolas,monospace;white-space:pre;overflow-x:auto;padding:6px 8px;border-radius:8px;background:rgba(127,127,127,.12)">' + esc(r.layout.grid) + '</pre>' : '')
      + '</div>').join('');
    if (window.QZ && QZ.confetti && d.best) QZ.confetti(100);
  }

  $('pStart').addEventListener('click', start);
  $('pNext').addEventListener('click', () => next(false));
  $('pSkip').addEventListener('click', () => next(true));
  $('pFinish').addEventListener('click', () => { const left = answers.filter(a => a === null).length - (value() !== null ? 1 : 0);
    if (left > 0 && !confirm(left + ' question' + (left > 1 ? 's are' : ' is') + ' not answered. Finish anyway?')) return; finish(false); });
  $('pFinish2').addEventListener('click', () => finish(false));
  $('pBack').addEventListener('click', () => { $('pReview').hidden = true; $('pRun').hidden = false;
    const k = answers.findIndex(a => a === null); at = k < 0 ? 0 : k; $('pRunNav').appendChild($('pNav')); render(); });
  // a paper finished with no connection: send it now
  const old = stored();
  if (old && old.token) { $('pIntro').hidden = true; send(old).catch(() => {}); }
}
