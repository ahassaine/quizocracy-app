/* Grammar and science questions: one page for every question type (mcq, tap, text, write, num). */
function BankDrill(activity) {
  const $ = (id) => document.getElementById(id);
  let cur = null, pick = null, taps = new Set(), choices = null, gaps = null;
  const area = $('area');
  const head = $('drillHead'), YEAR = parseInt(head && head.dataset.year, 10) || 0;
  const say = (t) => { if (window.Speak) Speak.word(t); };          // Years 1-2 hear what they tap
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
      cur = q; pick = null; taps = new Set(); choices = null; gaps = null;
      $('skill').textContent = q.strand + ' · ' + q.skill;
      kwTerms = {}; gloss($('q'), q.prompt, q.terms);
      area.innerHTML = '';
      if (q.kind === 'mcq') {
        const box = document.createElement('div'); box.className = 'opts';
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
        lab.textContent = 'The sentence is in the box. Change it there, then press Check.';
        const t = document.createElement('textarea'); t.id = 'answer'; t.className = 'write'; t.rows = 2;
        t.value = q.s; t.setAttribute('spellcheck', 'false'); t.setAttribute('autocapitalize', 'off');
        area.appendChild(lab); area.appendChild(t); t.focus(); t.setSelectionRange(t.value.length, t.value.length);
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
      const p = [q.prompt];
      if (q.kind === 'mcq') p.push(q.opts.map(o => /[.?!]$/.test(o) ? o : o + '.').join(' '));
      if (q.kind === 'tap') p.push(q.words.join(' '));
      if (q.kind === 'write' && !SPACES.test(q.prompt)) p.push(q.s);
      return p;
    },
    read() {
      if (!cur) return null;
      if (cur.kind === 'mcq') return pick === null ? null : { value: pick };
      if (cur.kind === 'tap') return taps.size ? { value: [...taps] } : null;
      const v = $('answer').value.trim();
      return v ? { value: v } : null;
    },
    explain(r) {
      const end = /[.?!'"’”)]$/.test(String(r.expected).trim()) ? '' : '.';   // no "draw.." or "?."
      // a sentence answer: the words that differ are marked, in what was typed and in the answer
      const marked = (parts, fix) => parts.map(([t, d]) => !d ? esc(t) : fix
        ? '<span class="mk-fix" data-testid="mark-fixed" style="background:rgba(15,159,118,.45);color:#fff;border-radius:4px;padding:0 3px">' + esc(t) + '</span>'
        : '<span class="mk-bad" data-testid="mark-wrong" style="text-decoration:underline wavy var(--bad);text-underline-offset:4px;text-decoration-thickness:2px">' + esc(t) + '</span>').join(' ');
      const lead = cur.kind === 'tap'                                     // not "The answer is a."
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
      if (r.mastered) $('feedback').innerHTML += ' · skill mastered!';
    } });
}
