/* The question banks: grammar, science, phonics and reading. One page for every question type (mcq, tap, text,
   write, num, and seg (sound buttons) and order (put events in order)).
   Phonics (SPEC_PHONICS.md): q.w is the word to read, shown big and never spoken; q.say is a word the speaker says,
   never shown. Reading (SPEC_READING.md): q.passage is shown beside the question while its questions are asked. */
function BankDrill(activity) {
  const $ = (id) => document.getElementById(id);
  let cur = null, pick = null, taps = new Set(), choices = null, gaps = null, seq = [], cuts = new Set(), shownPassage = null;
  const area = $('area');
  const head = $('drillHead'), YEAR = parseInt(head && head.dataset.year, 10) || 0;
  const PHONICS = activity === 'phonics';
  // Years 1-2 hear what they tap; never in phonics, where hearing a word option would read it for them
  const say = (t) => { if (window.Speak && !PHONICS) Speak.word(t); };
  const PIC = /^\s*(?:\p{Extended_Pictographic}\uFE0F?\u200D?)+\s*$/u;       // an option that is one picture
  /* Reading: the passage, beside the question (wide screens) or above it. Shown again only when another passage's
     question comes (a mistake put right, a question missed on another day). */
  function passage(q) {
    const box = $('passage');
    if (!box) return;
    if (!q.passage) { box.hidden = true; shownPassage = null; return; }
    box.hidden = false;
    const P = q.passage;
    $('passageAt').textContent = P.n && P.of ? 'Question ' + P.n + ' of ' + P.of : '';
    if (!box.dataset.wired && $('toPassage')) { box.dataset.wired = '1';
      $('toPassage').addEventListener('click', () => box.scrollIntoView({ behavior: 'smooth', block: 'start' })); }
    // the same passage's next question: straight to the question (on a phone the passage is above it)
    if (shownPassage === P.key) { if (innerWidth < 900) $('stage').scrollIntoView({ block: 'start' }); return; }
    shownPassage = P.key;
    const paras = String(P.text).split(/\n\s*\n/).map(p => '<p>' + esc(p.trim()).replace(/\n/g, '<br>') + '</p>').join('');
    $('passageBody').innerHTML = '<div class="mut small" data-testid="passage-kind">' + esc(P.kind || '') + '</div>'
      + '<h2 class="passage-title" data-testid="passage-title">' + esc(P.title) + '</h2>' + paras;
    $('passageBody').scrollTop = 0;
    if (P.again) $('passageBody').insertAdjacentHTML('afterbegin', '<div class="small" data-testid="passage-again" style="font-weight:700;margin-bottom:6px">'
      + 'You have read every passage for your year, well done! This one comes round again.</div>');
  }
  /* Phonics sound buttons: tap between two letters to split the word into its sounds (sh|i|p). */
  function segmenter(w) {
    const box = document.createElement('div'); box.className = 'gaps seg'; box.setAttribute('data-testid', 'seg');
    [...w].forEach((c, i) => {
      if (i) {
        const g = document.createElement('button'); g.type = 'button'; g.className = 'gap';
        g.setAttribute('aria-label', 'Split before ' + c); g.setAttribute('data-testid', 'cut-' + i);
        g.addEventListener('click', () => { if (g.disabled) return;
          cuts.has(i) ? cuts.delete(i) : cuts.add(i); g.classList.toggle('on', cuts.has(i)); });
        box.appendChild(g);
      }
      const l = document.createElement('span'); l.className = 'letter'; l.textContent = c; box.appendChild(l);
    });
    const tip = document.createElement('div'); tip.className = 'mut small';
    tip.textContent = 'Tap between the letters to split the word into its sounds. Tap again to join them.';
    area.appendChild(box); area.appendChild(tip);
    // the whole word on one line, whatever the text size: letters shrink to fit the space beside the gaps
    const fit = () => { const room = area.clientWidth - 34 * (w.length - 1) - 24;
      box.style.fontSize = Math.max(22, Math.min(56, room / (w.length * 0.72))) + 'px'; };
    fit(); addEventListener('resize', fit);
    return box;
  }
  /* Put in order: tap the events in the order they happen; each gets its number. Tap one again to take it out. */
  function orderer(items) {
    const box = document.createElement('div'); box.className = 'opts order'; box.setAttribute('data-testid', 'order');
    const paint = () => box.querySelectorAll('.opt').forEach((b, i) => {
      const at = seq.indexOf(i); b.classList.toggle('sel', at >= 0);
      b.querySelector('.num').textContent = at >= 0 ? String(at + 1) : ''; });
    items.forEach((t, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'opt';
      b.setAttribute('data-testid', 'item-' + i);
      b.innerHTML = '<span class="num" aria-hidden="true"></span><span>' + esc(t) + '</span>';
      b.addEventListener('click', () => { if (b.disabled) return;
        const at = seq.indexOf(i); if (at >= 0) seq.splice(at, 1); else seq.push(i); paint(); });
      box.appendChild(b);
    });
    const tip = document.createElement('div'); tip.className = 'mut small';
    tip.textContent = 'Tap them in order: first, then second… Tap one again to take it out.';
    area.appendChild(tip); area.appendChild(box);
    return box;
  }
  const SPACES = /^put spaces between the words\b/i;
  /* "Put spaces between the words": tap between two letters to put a space there (a finger can't place a
     cursor inside a word on a tablet). The sentence keeps its own capitals and full stop. */
  function spacer(s) {
    const ch = [], sp = new Set();
    [...s].forEach(c => { if (c === ' ') sp.add(ch.length); else ch.push(c); });
    const hid = document.createElement('input'); hid.type = 'hidden'; hid.id = 'answer';
    const box = document.createElement('div'); box.className = 'gaps'; box.setAttribute('data-testid', 'gaps');
    const build = () => { hid.value = ch.map((c, i) => (i && sp.has(i) ? ' ' : '') + c).join(''); };
    ch.forEach((c, i) => {
      if (i && /[A-Za-z0-9]/.test(c)) {
        const g = document.createElement('button'); g.type = 'button'; g.className = 'gap' + (sp.has(i) ? ' on' : '');
        g.setAttribute('aria-label', 'Space before ' + c); g.setAttribute('data-testid', 'gap-' + i);
        g.addEventListener('click', () => { if (g.disabled) return;
          sp.has(i) ? sp.delete(i) : sp.add(i); g.classList.toggle('on', sp.has(i)); build(); });
        box.appendChild(g);
      }
      const l = document.createElement('span'); l.className = 'letter'; l.textContent = c; box.appendChild(l);
    });
    build();
    const tip = document.createElement('div'); tip.className = 'mut small'; tip.textContent = 'Tap between two letters to put a space there. Tap again to take it away.';
    area.appendChild(box); area.appendChild(tip); area.appendChild(hid);
    return box;
  }
  /* Key words (app/bank/glossary.py): a term the server found in the question or its explanation gets a dotted
     underline; a tap shows its one-line meaning in a small box. The meaning is not read aloud. */
  function glossHtml(text, terms) {
    const keys = Object.keys(terms || {}).sort((a, b) => b.length - a.length);
    if (!keys.length) return esc(text);
    const alt = keys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).map(k => /y$/.test(k) ? k.slice(0, -1) + '(?:y|ies)' : k + '(?:s|es)?');
    const rx = new RegExp('(^|[^\\w-])(' + alt.join('|') + ')(?![\\w-])', 'gi');
    const termOf = (w) => { const l = w.toLowerCase(); return [l, l.slice(0, -1), l.slice(0, -2), l.slice(0, -3) + 'y'].find(t => terms[t]); };
    let out = '', at = 0, m;
    const s = String(text);
    while ((m = rx.exec(s))) {
      const start = m.index + m[1].length, t = termOf(m[2]);
      out += esc(s.slice(at, start)) + (t ? '<button type="button" class="kw" data-testid="kw" data-kw="' + esc(t) + '" aria-expanded="false">' + esc(m[2]) + '</button>' : esc(m[2]));
      at = start + m[2].length;
    }
    return out + esc(s.slice(at));
  }
  let kwTerms = {};
  function gloss(el, text, terms) { kwTerms = Object.assign({}, kwTerms, terms || {}); el.innerHTML = glossHtml(text, terms); }
  if (!document.getElementById('kwStyle')) {
    const st = document.createElement('style'); st.id = 'kwStyle';
    st.textContent = '.kw{background:none;border:0;padding:0;margin:0;font:inherit;color:inherit;cursor:help;text-decoration:underline dotted;text-decoration-thickness:2px;text-underline-offset:4px}'
      + '.kw[aria-expanded=true]{color:var(--brand,#4f46e5)}'
      + '.kw-pop{position:absolute;z-index:50;max-width:min(300px,calc(100vw - 32px));padding:9px 12px;border-radius:10px;background:var(--card);color:var(--ink);border:1px solid var(--line);box-shadow:0 6px 24px rgba(0,0,0,.18);font-size:.95rem;font-weight:400;line-height:1.4}';
    document.head.appendChild(st);
    let pop = null, from = null;
    const close = () => { if (pop) pop.remove(); if (from) from.setAttribute('aria-expanded', 'false'); pop = from = null; };
    document.addEventListener('click', (e) => {
      const b = e.target.closest && e.target.closest('.kw');
      if (!b) { if (pop && !(e.target.closest && e.target.closest('.kw-pop'))) close(); return; }
      e.preventDefault();
      const again = b === from; close(); if (again) return;
      pop = document.createElement('div'); pop.className = 'kw-pop'; pop.setAttribute('role', 'tooltip'); pop.setAttribute('data-testid', 'kw-pop');
      pop.innerHTML = '<b>' + esc(b.dataset.kw) + '</b>: ' + esc(kwTerms[b.dataset.kw] || '');
      document.body.appendChild(pop); from = b; b.setAttribute('aria-expanded', 'true');
      const r = b.getBoundingClientRect(), w = pop.offsetWidth;
      pop.style.top = (window.scrollY + r.bottom + 6) + 'px';
      pop.style.left = Math.max(16, Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - w - 16)) + 'px';
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') close(); });
  }
  function input(attrs) {
    const i = document.createElement('input');
    Object.assign(i, { type: 'text', autocomplete: 'off', id: 'answer' });
    i.setAttribute('autocapitalize', 'off'); i.setAttribute('spellcheck', 'false');
    Object.assign(i, attrs || {});
    return i;
  }
  Drill({ activity, idk: true,           // the "I don't know" button next to Check
    render(q) {
      cur = q; pick = null; taps = new Set(); choices = null; gaps = null; seq = []; cuts = new Set();
      // the skill's own title when it already names its strand ("Phase 3: ch sh th ng"), not "Phase 3 · Phase 3: …"
      $('skill').textContent = q.passage ? q.strand : String(q.skill).indexOf(q.strand) === 0 ? q.skill : q.strand + ' · ' + q.skill;
      kwTerms = {}; gloss($('q'), q.prompt, q.terms);
      area.innerHTML = '';
      passage(q);
      if (q.w && q.kind !== 'seg') {       // phonics: the word to read, big; never read aloud
        const w = document.createElement('div'); w.className = 'read-word'; w.setAttribute('data-testid', 'read-word');
        w.textContent = q.w; area.appendChild(w);
      }
      if (q.say) {                          // phonics: the word to listen to; it is never shown
        const b = document.createElement('button'); b.type = 'button'; b.className = 'btn hear'; b.setAttribute('data-testid', 'hear');
        b.innerHTML = '<span aria-hidden="true">🔊</span> Hear the word';
        b.addEventListener('click', () => { if (window.Speak && Speak.say) Speak.say(q.say); });
        area.appendChild(b);
        // a silent phone, a quiet room: no listening questions today (the server leaves them out until tomorrow)
        const ns = document.createElement('button'); ns.type = 'button'; ns.className = 'linkish small'; ns.setAttribute('data-testid', 'nosound');
        ns.textContent = 'No sound here? Skip the listening questions today';
        ns.style.display = 'block'; ns.style.margin = '-6px 0 12px';
        ns.addEventListener('click', async () => { ns.disabled = true;
          try { await fetch('/api/phonics/nosound', { method: 'POST', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin',
            body: JSON.stringify({ pupil: document.body.dataset.pupil, token: q.token }) }); } catch (e) {}
          location.reload(); });
        area.appendChild(ns);
        if (!(window.Speak && Speak.ok)) {   // no voice on this device at all: say so, the skip is just above
          const n = document.createElement('div'); n.className = 'mut small'; n.setAttribute('data-testid', 'no-voice');
          n.textContent = 'This device cannot read words aloud. Press the link above to skip listening questions.';
          area.appendChild(n);
        }
      }
      if (q.kind === 'seg') {
        gaps = segmenter(q.w);
      } else if (q.kind === 'order') {
        orderer(q.items);
      } else if (q.kind === 'mcq') {
        const box = document.createElement('div'); box.className = 'opts';
        if (q.opts.every(o => PIC.test(o))) box.classList.add('pics');
        q.opts.forEach((o, i) => {
          const b = document.createElement('button'); b.type = 'button'; b.className = 'opt'; b.textContent = o;
          b.dataset.i = i; b.setAttribute('data-testid', 'opt-' + i);
          b.addEventListener('click', () => { if (b.disabled) return; pick = i; say(o);
            box.querySelectorAll('.opt').forEach(x => x.classList.toggle('sel', x === b)); });
          box.appendChild(b);
        });
        area.appendChild(box);
      } else if (q.kind === 'tap') {
        const box = document.createElement('div'); box.className = 'words';
        q.words.forEach((w, i) => {
          const b = document.createElement('button'); b.type = 'button'; b.className = 'word'; b.textContent = w;
          b.setAttribute('data-testid', 'word-' + i);
          b.addEventListener('click', () => { if (b.disabled) return;
            taps.has(i) ? taps.delete(i) : taps.add(i); b.classList.toggle('sel', taps.has(i)); say(w); });
          box.appendChild(b);
        });
        area.appendChild(box);
      } else if (q.kind === 'write' && SPACES.test(q.prompt)) {
        gaps = spacer(q.s);
      } else if (q.kind === 'write') {
        // the sentence to change is already in the box: say so, or a child types the answer after it
        const lab = document.createElement('label'); lab.htmlFor = 'answer'; lab.className = 'mut small';
        lab.setAttribute('data-testid', 'write-tip'); lab.style.display = 'block'; lab.style.marginBottom = '6px';
        lab.textContent = 'The words are in the box. Change them there, then press Check.';
        const t = document.createElement('textarea'); t.id = 'answer'; t.className = 'write'; t.rows = 2;
        t.value = q.s; t.setAttribute('spellcheck', 'false'); t.setAttribute('autocapitalize', 'off');
        area.appendChild(lab); area.appendChild(t); t.focus(); t.setSelectionRange(t.value.length, t.value.length);
        const rs = document.createElement('button'); rs.type = 'button'; rs.className = 'linkish small'; rs.setAttribute('data-testid', 'write-reset');
        rs.textContent = '↺ Start again with the sentence as it was'; rs.addEventListener('click', () => { if (!t.readOnly) { t.value = q.s; t.focus(); } });
        area.appendChild(rs);
      } else {
        const row = document.createElement('div'); row.className = 'row';
        const i = input(q.kind === 'num' ? { inputMode: 'decimal', className: 'answer' } : { className: 'answer wide' });
        if (q.gap) i.placeholder = 'Type the missing word(s)';
        row.appendChild(i);
        if (q.kind === 'num' && q.unit) { const u = document.createElement('span'); u.className = 'unit'; u.textContent = q.unit; row.appendChild(u); }
        area.appendChild(row);
        const words = q.kind === 'text' && Drill.choices(q.prompt);
        // a few fixed words ("living, dead or never alive"): buttons; Years 1-4 get only the buttons
        if (words) choices = Drill.choiceButtons(i, words, YEAR >= 1 && YEAR <= 4, row);
        if (!(choices && YEAR >= 1 && YEAR <= 4)) i.focus();
      }
    },
    speech(q) {          // what the 🔊 button reads: the question, then what there is to choose from
      if (PHONICS) return [q.prompt].concat(q.say ? [q.say] : []);     // never the word to read, nor word options
      const p = [q.prompt];
      if (q.kind === 'mcq') p.push(q.opts.map(o => /[.?!]$/.test(o) ? o : o + '.').join(' '));
      if (q.kind === 'tap') p.push(q.words.join(' '));
      if (q.kind === 'order') p.push(q.items.map(o => /[.?!]$/.test(o) ? o : o + '.').join(' '));
      if (q.kind === 'write' && !SPACES.test(q.prompt)) p.push(q.s);
      return p;
    },
    read() {
      if (!cur) return null;
      if (cur.kind === 'mcq') return pick === null ? null : { value: pick };
      if (cur.kind === 'tap') return taps.size ? { value: [...taps] } : null;
      if (cur.kind === 'seg') return cuts.size ? { value: [...cuts] } : null;
      if (cur.kind === 'order') return seq.length === cur.items.length ? { value: seq.slice() } : null;
      const v = $('answer').value.trim();
      return v ? { value: v } : null;
    },
    explain(r) {
      const end = /[.?!'"’”)]$/.test(String(r.expected).trim()) ? '' : '.';   // no "draw.." or "?."
      // a sentence answer: the words that differ are marked, in what was typed and in the answer
      const marked = (parts, fix) => parts.map(([t, d]) => !d ? esc(t) : fix
        ? '<span class="mk-fix" data-testid="mark-fixed" style="background:rgba(15,159,118,.45);color:#fff;border-radius:4px;padding:0 3px">' + esc(t) + '</span>'
        : '<span class="mk-bad" data-testid="mark-wrong" style="text-decoration:underline wavy var(--bad);text-underline-offset:4px;text-decoration-thickness:2px">' + esc(t) + '</span>').join(' ');
      const lead = cur.kind === 'seg' ? 'The sounds are <b data-testid="seg-answer">' + esc(r.expected) + '</b>.'
        : cur.kind === 'order' ? 'The right order is: <b>' + esc(r.expected) + '</b>.'
        : cur.kind === 'tap'                                     // not "The answer is a."
        ? ((r.hits || []).length > 1 ? 'The words to tap are <b>' : 'The word to tap is <b>') + '“' + esc(r.expected) + '”</b>.'
        : r.marks ? 'The answer is <b>' + marked(r.marks.word, true) + '</b>' + end
          + '<div class="small" data-testid="you-wrote" style="margin-top:4px">You wrote: ' + marked(r.marks.typed, false) + '</div>'
        : 'The answer is <b>' + esc(r.expected) + '</b>' + end;
      kwTerms = Object.assign({}, kwTerms, r.terms || {});
      return lead + (r.whynot ? '<div class="why" data-testid="why-not">' + glossHtml(r.whynot, r.terms) + '</div>' : '')
        + (r.why ? '<div class="why">' + glossHtml(r.why, r.terms) + '</div>' : '');
    },
    whyRight(r) { kwTerms = Object.assign({}, kwTerms, r.terms || {}); return r.why ? '<div class="why">' + glossHtml(r.why, r.terms) + '</div>' : ''; },
    after(r) {
      if (r.terms && Object.keys(r.terms).length) gloss($('q'), cur.prompt, r.terms);    // answered: every key word
      area.querySelectorAll('button').forEach(b => { b.disabled = true; });
      if (cur.kind === 'mcq') area.querySelectorAll('.opt').forEach((b, i) => {
        if (i === r.right) b.classList.add('right'); else if (i === pick) b.classList.add('wrong'); });
      if (cur.kind === 'tap') area.querySelectorAll('.word').forEach((b, i) => {
        if (r.hits.includes(i)) b.classList.add('right'); else if (taps.has(i)) b.classList.add('wrong'); });
      const a = $('answer'); if (a) { a.readOnly = true; a.style.borderColor = r.correct ? '#22c55e' : '#f85149'; }
      if (choices) choices.__mark(r);
      if (gaps) gaps.classList.add(r.correct ? 'right' : 'wrong');
      if (cur.kind === 'order') area.querySelectorAll('.order .opt').forEach((b, i) => {
        b.classList.add(seq.indexOf(i) === r.order_pos[i] ? 'right' : 'wrong'); });
      if (r.mastered) $('feedback').innerHTML += ' · skill mastered!';
      if (r.passage_done) $('feedback').insertAdjacentHTML('beforeend', '<div class="passage-done" data-testid="passage-done">📖 You finished “'
        + esc(r.passage_done.title) + '”: ' + r.passage_done.right + ' of ' + r.passage_done.of + ' right.</div>');
    } });
}
