/* Read-aloud for the drills: the browser's own voice (speechSynthesis, en-GB where there is one), no server.
 * Every question gets a big speaker button. Years 1-2 also hear each question as it appears, and hear the
 * feedback, once speech is allowed: browsers (iPad/iPhone Safari above all) only speak after a first tap on
 * the page, so until then the button says "Tap to hear" and the first tap anywhere reads the question.
 * Where speech is missing, the button is not shown and nothing else changes. */
(function () {
  const synth = window.speechSynthesis;
  // the grown-up's read-aloud setting (child_form.html, on <body>): "on" (questions and feedback), "questions"
  // (no spoken feedback) or "off" (nothing is said, and there is no 🔊 button); speed "slower" or "normal"
  const MODE = (document.body && document.body.dataset.voice) || 'on';
  const SLOW = !!(document.body && document.body.dataset.voiceRate === 'slower');
  const ok = !!(synth && window.SpeechSynthesisUtterance) && MODE !== 'off';
  const talk = MODE === 'on';                                      // feedback is spoken too
  const head = document.getElementById('drillHead');
  const year = parseInt(head && head.dataset.year, 10) || 0;     // the child's school year (0: not known)
  const young = year >= 1 && year <= 2;                            // read each question out without being asked

  // ---- natural text: what a person would say, not the symbols ----
  const FRAC = { 2: 'half', 3: 'third', 4: 'quarter', 5: 'fifth', 6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'ninth',
    10: 'tenth', 12: 'twelfth', 100: 'hundredth' };
  function frac(n, d) {
    const name = FRAC[d];
    if (!name) return n + ' over ' + d;
    if (d === 2) return n + ' ' + (n === 1 ? 'half' : 'halves');
    return n + ' ' + name + (n === 1 ? '' : 's');
  }
  function natural(s) {
    s = String(s == null ? '' : s);
    s = s.replace(/[\u{1F000}-\u{1FAFF}☀-➿️]/gu, ' ');            // pictures
    s = s.replace(/([A-Za-z]+)_{2,}/g, '$1, blank');                               // "i__" (a word to finish)
    s = s.replace(/_{2,}(\s+_{2,})*/g, ' blank ');                                 // "___"
    s = s.replace(/(\d)\s*\/\s*(\d+)(?!\d)/g, (m, n, d) => frac(+n, +d));          // 3/4 -> 3 quarters
    s = s.replace(/(\d)\s*[x×]\s*(?=\d|blank\b)/g, '$1 times ').replace(/×/g, ' times ').replace(/÷/g, ' divided by ');
    s = s.replace(/(\d|\bblank)\s+[−–-]\s+(?=\d|blank\b)/g, '$1 minus ');          // 9 − 4, 10 − ___, ___ − 4
    s = s.replace(/(^|[\s(=,:])[−-](?=\d)/g, '$1minus ');                          // −62
    s = s.replace(/\s*−\s*/g, ' minus ');                                          // the minus sign is never a dash
    s = s.replace(/\s*≤\s*/g, ' is less than or equal to ').replace(/\s*≥\s*/g, ' is greater than or equal to ');
    s = s.replace(/\s*<\s*/g, ' is less than ').replace(/\s*>\s*/g, ' is greater than ');
    s = s.replace(/\s*\+\s*/g, ' plus ').replace(/\s*=\s*/g, ' equals ');
    s = s.replace(/(\d)\s*%/g, '$1 percent').replace(/°C\b/g, ' degrees Celsius').replace(/°/g, ' degrees');
    s = s.replace(/(\d)\s+:\s+(?=\d)/g, '$1 to ');                                 // a ratio 3 : 4
    s = s.replace(/[·•|]/g, ', ').replace(/[→⟶]/g, ' to ').replace(/&/g, ' and ').replace(/…/g, '...');
    s = s.replace(/[“”"*#\[\]{}]/g, ' ').replace(/(^|[^A-Za-z])['‘’]/g, '$1 ').replace(/['‘’](?![A-Za-z])/g, ' ');   // quotes, not apostrophes
    s = s.replace(/[()]/g, ', ');
    s = s.replace(/\b[A-Z]{4,}\b/g, (w) => w.toLowerCase());                       // "MORE" is a word, "HCF" is spelt
    return s.replace(/\s+([,.?!])/g, '$1').replace(/([,.?!])(\s*,)+/g, '$1').replace(/^[\s,]+|[\s,]+$/g, '')
      .replace(/\s{2,}/g, ' ');
  }

  // ---- the voice ----
  let voice = null;
  function pickVoice() {
    const vs = synth.getVoices() || [];
    const gb = vs.filter(v => /^en[-_]GB/i.test(v.lang));
    voice = gb.find(v => /female|serena|kate|martha|stephanie|libby|sonia/i.test(v.name)) || gb[0]
      || vs.find(v => /^en\b|^en[-_]/i.test(v.lang)) || null;
  }
  if (ok) { pickVoice(); if (synth.addEventListener) synth.addEventListener('voiceschanged', pickVoice); }

  let unlocked = false, cur = null, btn = null, run = 0;
  function chunks(parts) {               // short pieces: long utterances stop half way in some browsers
    const out = [];
    parts.map(natural).filter(Boolean).forEach(p => {
      (p.match(/[^.?!]+[.?!]*\s*/g) || [p]).forEach(x => { x = x.trim(); if (x) out.push(x); });
    });
    return out;
  }
  function speak(parts, onstart) {
    if (!ok) return;
    const my = ++run, list = chunks(parts);
    synth.cancel();
    if (!list.length) { setOn(false); return; }
    list.forEach((t, i) => {
      const u = new SpeechSynthesisUtterance(t);
      u.lang = (voice && voice.lang) || 'en-GB';
      if (voice) u.voice = voice;
      u.rate = (year && year <= 3 ? 0.88 : 0.95) * (SLOW ? 0.8 : 1);
      if (i === 0) u.onstart = started;
      if (i === list.length - 1) u.onend = u.onerror = () => { if (my === run) setOn(false); };
      synth.speak(u);
    });
    // some browsers never fire onstart (Chrome on Linux): speech that is under way counts as started all the same,
    // so the question is not read a second time at the first tap, and "Tap to hear" goes
    let once = false;
    function started() { if (once || my !== run) return; once = true; setOn(true); if (onstart) onstart(); }
    setTimeout(() => { if (synth.speaking) started(); }, 300);
  }
  function setOn(on) { if (btn) btn.classList.toggle('on', on); }
  function unlock() {                    // inside a tap: from now on the page may speak by itself
    if (!ok || unlocked) return;
    unlocked = true;
    try { const u = new SpeechSynthesisUtterance(' '); u.volume = 0; synth.speak(u); } catch (e) {}
    settle();
  }
  // "Tap to hear" goes once speech works; a moment later, so the text does not move under a finger mid-tap.
  // The button keeps its width, so the question beside it does not re-wrap and nothing below moves.
  function settle() { setTimeout(() => {
    if (!btn || !unlocked || !btn.classList.contains('first')) return;
    btn.style.minWidth = btn.offsetWidth + 'px';
    btn.classList.remove('first');
  }, 600); }
  function play(c, rest) {               // the question, after its own sound (a spelling word) if it has one
    if (!c) return;
    c.heard = true;
    if (rest && c.leadHeard) { speak(c.parts); return; }      // the word already played by itself: only the hint
    if (c.lead) Promise.resolve(c.lead()).then(() => { if (cur === c) speak(c.parts); });
    else speak(c.parts);
  }

  function mount() {
    const stage = document.getElementById('stage');
    if (!ok || !stage || btn) return;
    btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'speak-btn'; btn.id = 'speak';
    btn.setAttribute('data-testid', 'speak'); btn.setAttribute('data-speaks', '');
    btn.setAttribute('aria-label', 'Read it to me');
    btn.innerHTML = '<span aria-hidden="true">🔊</span><b>Tap to hear</b>';
    btn.addEventListener('click', () => {
      unlock();
      if (btn.classList.contains('on')) { ++run; synth.cancel(); setOn(false); return; }
      play(cur);
    });
    stage.insertBefore(btn, stage.firstChild);
  }
  // the first tap or key anywhere allows speech; a young child who has not heard this question yet hears it now
  function firstGesture(e) {
    if (unlocked) return;
    unlock();
    const t = e.target && e.target.closest ? e.target : null;
    if (synth.speaking || synth.pending) return;                 // it is being read now: never twice
    if (young && cur && !cur.heard && !(t && t.closest('[data-speaks]'))) play(cur, true);
  }
  if (ok) ['click', 'touchend', 'keydown'].forEach(ev => document.addEventListener(ev, firstGesture, true));

  window.Speak = {
    ok, year, young, natural,
    talks: ok && talk && young,          // feedback is spoken by itself (Years 1-2, read-aloud "on")
    /* the question now on screen. what: [text, ...] or { parts, lead, after }: lead() makes the question's own
       sound (returns a promise) and runs when the child asks; after is that sound already playing by itself */
    set(what) {
      mount();
      if (!ok) return;
      const w = Array.isArray(what) ? { parts: what } : (what || { parts: [] });
      ++run; synth.cancel(); setOn(false);
      cur = { parts: (w.parts || []).filter(Boolean), lead: w.lead || null, heard: false, leadHeard: false };
      const c = cur;
      // the question's own sound playing by itself (a spelling word's clip): true once it has played
      if (w.after) Promise.resolve(w.after).then(played => { if (played === true) {
        c.leadHeard = true; if (!c.parts.length) { c.heard = true; unlocked = true; settle(); } } });
      if (!young || !cur.parts.length) return;
      if (!unlocked && btn) btn.classList.add('first');
      Promise.resolve(w.after).then(() => {
        if (cur !== c) return;
        // try anyway: where the browser allows it, speech starts and counts as allowed
        speak(c.parts, () => { c.heard = true; unlocked = true; settle(); });
      });
    },
    feedback(text) { if (ok && talk && young && unlocked) speak([text]); },  // "Not quite. Good try! ..." (not with "questions only")
    word(text) { if (ok && young && unlocked) speak([text]); },            // an option the child tapped
    stop() { if (ok) { ++run; synth.cancel(); setOn(false); } },
  };
})();
