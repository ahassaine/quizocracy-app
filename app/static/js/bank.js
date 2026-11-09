/* Grammar and science questions: one page for every question type (mcq, tap, text, write, num). */
function BankDrill(activity) {
  const $ = (id) => document.getElementById(id);
  let cur = null, pick = null, taps = new Set();
  const area = $('area');
  function input(attrs) {
    const i = document.createElement('input');
    Object.assign(i, { type: 'text', autocomplete: 'off', id: 'answer' });
    i.setAttribute('autocapitalize', 'off'); i.setAttribute('spellcheck', 'false');
    Object.assign(i, attrs || {});
    return i;
  }
  Drill({ activity,
    render(q) {
      cur = q; pick = null; taps = new Set();
      $('skill').textContent = q.strand + ' · ' + q.skill;
      $('q').textContent = q.prompt;
      area.innerHTML = '';
      if (q.kind === 'mcq') {
        const box = document.createElement('div'); box.className = 'opts';
        q.opts.forEach((o, i) => {
          const b = document.createElement('button'); b.type = 'button'; b.className = 'opt'; b.textContent = o;
          b.dataset.i = i; b.setAttribute('data-testid', 'opt-' + i);
          b.addEventListener('click', () => { if (b.disabled) return; pick = i;
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
            taps.has(i) ? taps.delete(i) : taps.add(i); b.classList.toggle('sel', taps.has(i)); });
          box.appendChild(b);
        });
        area.appendChild(box);
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
        area.appendChild(row); i.focus();
      }
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
      return 'The answer is <b>' + esc(r.expected) + '</b>' + end + (r.why ? '<div class="why">' + esc(r.why) + '</div>' : '');
    },
    after(r) {
      area.querySelectorAll('button').forEach(b => { b.disabled = true; });
      if (cur.kind === 'mcq') area.querySelectorAll('.opt').forEach((b, i) => {
        if (i === r.right) b.classList.add('right'); else if (i === pick) b.classList.add('wrong'); });
      if (cur.kind === 'tap') area.querySelectorAll('.word').forEach((b, i) => {
        if (r.hits.includes(i)) b.classList.add('right'); else if (taps.has(i)) b.classList.add('wrong'); });
      const a = $('answer'); if (a) { a.readOnly = true; a.style.borderColor = r.correct ? '#22c55e' : '#f85149'; }
      if (r.mastered) $('feedback').innerHTML += ' · skill mastered!';
    } });
}
