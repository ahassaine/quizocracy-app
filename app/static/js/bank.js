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
  function input(attrs) {
    const i = document.createElement('input');
    Object.assign(i, { type: 'text', autocomplete: 'off', id: 'answer' });
    i.setAttribute('autocapitalize', 'off'); i.setAttribute('spellcheck', 'false');
    Object.assign(i, attrs || {});
    return i;
  }
  Drill({ activity,
    render(q) {
      cur = q; pick = null; taps = new Set(); choices = null; gaps = null;
      $('skill').textContent = q.strand + ' · ' + q.skill;
      $('q').textContent = q.prompt;
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
        const t = document.createElement('textarea'); t.id = 'answer'; t.className = 'write'; t.rows = 2;
        t.value = q.s; t.setAttribute('spellcheck', 'false'); t.setAttribute('autocapitalize', 'off');
        area.appendChild(t); t.focus(); t.setSelectionRange(t.value.length, t.value.length);
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
      const lead = cur.kind === 'tap'                                     // not "The answer is a."
        ? ((r.hits || []).length > 1 ? 'The words to tap are <b>' : 'The word to tap is <b>') + '“' + esc(r.expected) + '”</b>.'
        : 'The answer is <b>' + esc(r.expected) + '</b>' + end;
      return lead + (r.why ? '<div class="why">' + esc(r.why) + '</div>' : '');
    },
    after(r) {
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
