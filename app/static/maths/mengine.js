/* Interactive maths — client shell (server-authoritative).
 *
 * A component registers as:
 *   window.MComp["<name>"] = { render(host, spec, api) { ... } };
 * and MUST set:  host.__getValue = () => <current value>;
 * and MAY set:   host.__feedback = (result) => <highlight on the manipulative>;
 *
 * The shell fetches a question (/api/maths/next), renders the component, reads
 * host.__getValue() when the pupil clicks Check, posts it to /api/maths/check,
 * and shows correctness + the worked solution. The answer is never in the client
 * until after the pupil commits.
 */
(function () {
  window.MComp = window.MComp || {};
  const $ = (id) => document.getElementById(id);
  async function post(url, body) {
    const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
    return r.json();
  }
  function el(tag, cls, html) { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; }

  let state = { skill: null, token: null, answered: false };

  async function loadSkill(skill, title) {
    state.skill = skill; state.answered = false;
    $('mTitle').textContent = title || '';
    const stage = $('mStage'); stage.innerHTML = '';
    $('mFeedback').innerHTML = ''; $('mFeedback').className = 'm-feedback';
    const q = await post('/api/maths/next', { skill });
    if (!q.ok) { stage.innerHTML = '<p>Could not load this skill.</p>'; return; }
    state.token = q.token;
    stage.appendChild(el('div', 'm-prompt', q.prompt));
    const host = el('div', 'm-host'); host.id = 'mHost'; stage.appendChild(host);
    const comp = window.MComp[q.component];
    if (!comp) { host.innerHTML = '<em>[missing component: ' + q.component + ']</em>'; }
    else { comp.render(host, q.spec || {}, { submit: onCheck }); }
    $('mCheck').style.display = ''; $('mCheck').disabled = false; $('mNext').style.display = 'none';
  }

  async function onCheck() {
    if (state.answered) return;
    const host = $('mHost');
    const value = host && host.__getValue ? host.__getValue() : null;
    if (value === null || value === '' || (typeof value === 'number' && isNaN(value))) {
      flash('Enter or set your answer first.'); return;
    }
    const res = await post('/api/maths/check', { token: state.token, value });
    if (!res.ok) { flash('This question expired — loading a new one.'); return; }
    state.answered = true;
    $('mCheck').disabled = true; $('mNext').style.display = '';
    const fb = $('mFeedback');
    fb.className = 'm-feedback ' + (res.correct ? 'ok' : 'no');
    let html = res.correct ? '✅ Correct!' : '❌ Not quite. Answer: <b>' + escapeHtml(res.expected) + '</b>';
    if (res.solution && res.solution.length) html += '<div class="m-sol">' + res.solution.map(escapeHtml).join('<br>') + '</div>';
    fb.innerHTML = html;
    if (host && host.__feedback) host.__feedback(res);
  }

  function flash(msg) { const fb = $('mFeedback'); fb.className = 'm-feedback warn'; fb.textContent = msg; }
  function escapeHtml(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }

  window.MLab = {
    pick(skill, title) { loadSkill(skill, title); },
    check: onCheck,
    next() { loadSkill(state.skill, $('mTitle').textContent); },
  };
})();
