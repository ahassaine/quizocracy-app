/* clock — set an analogue clock by dragging the hands. value = "H:MM" string.
 * spec: { mode:"set" }
 */
(function () {
  window.MComp = window.MComp || {};
  const NS = 'http://www.w3.org/2000/svg';
  function mk(t, a) { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; }

  window.MComp["clock"] = {
    render(host, spec, api) {
      host.innerHTML = '';
      const SZ = 240, C = SZ / 2, R = 100;
      const svg = mk('svg', {
        viewBox: `0 0 ${SZ} ${SZ}`, width: 240, height: 240,
        style: 'max-width:100%;background:#0b0f14;border:1px solid #30363d;border-radius:14px;touch-action:none;display:block'
      });

      // outer face
      svg.appendChild(mk('circle', { cx: C, cy: C, r: R + 12, fill: '#0b0f14', stroke: '#30363d', 'stroke-width': 2 }));
      svg.appendChild(mk('circle', { cx: C, cy: C, r: R + 12, fill: 'none', stroke: '#4f8df7', 'stroke-width': 1, opacity: 0.35 }));

      // tick marks + hour numbers
      for (let m = 0; m < 60; m++) {
        const a = (m / 60) * 2 * Math.PI - Math.PI / 2;
        const big = m % 5 === 0;
        const r1 = R + (big ? 2 : 6), r2 = R + 10;
        svg.appendChild(mk('line', {
          x1: C + Math.cos(a) * r1, y1: C + Math.sin(a) * r1,
          x2: C + Math.cos(a) * r2, y2: C + Math.sin(a) * r2,
          stroke: big ? '#c9d1d9' : '#495260', 'stroke-width': big ? 2 : 1
        }));
      }
      for (let h = 1; h <= 12; h++) {
        const a = (h / 12) * 2 * Math.PI - Math.PI / 2;
        const t = mk('text', {
          x: C + Math.cos(a) * (R - 18), y: C + Math.sin(a) * (R - 18) + 6,
          fill: '#e6edf3', 'font-size': 17, 'font-weight': 700, 'text-anchor': 'middle',
          'font-family': 'system-ui,sans-serif'
        });
        t.textContent = h;
        svg.appendChild(t);
      }

      // hands (drawn from centre)
      const hourHand = mk('line', { x1: C, y1: C, x2: C, y2: C - 55, stroke: '#4f8df7', 'stroke-width': 7, 'stroke-linecap': 'round', style: 'cursor:grab' });
      const minHand = mk('line', { x1: C, y1: C, x2: C, y2: C - 85, stroke: '#9db8e8', 'stroke-width': 4, 'stroke-linecap': 'round', style: 'cursor:grab' });
      svg.appendChild(hourHand);
      svg.appendChild(minHand);
      svg.appendChild(mk('circle', { cx: C, cy: C, r: 6, fill: '#e6edf3' }));
      host.appendChild(svg);

      // digital readout
      const read = document.createElement('div');
      read.style.cssText = 'font-size:2rem;font-weight:800;text-align:center;margin-top:10px;color:#e6edf3;font-family:system-ui,monospace';
      host.appendChild(read);

      // state: continuous angles in "minutes-of-full-circle" units (0..720 for hour, 0..60 for minute)
      // Y3 objective is 'to the nearest minute', so snap to 1 by default;
      // a generator may pass spec.snap (e.g. 5) to make an easier tier.
      const MIN_SNAP = Math.max(1, parseInt((spec && spec.snap) || 1, 10));
      let minTick = 0;        // 0..59, snapped to MIN_SNAP
      let hourFloat = 0;      // 0..12 continuous

      function draw() {
        // minute hand angle
        const ma = (minTick / 60) * 2 * Math.PI - Math.PI / 2;
        minHand.setAttribute('x2', C + Math.cos(ma) * 85);
        minHand.setAttribute('y2', C + Math.sin(ma) * 85);
        // hour hand angle (continuous)
        const ha = (hourFloat / 12) * 2 * Math.PI - Math.PI / 2;
        hourHand.setAttribute('x2', C + Math.cos(ha) * 55);
        hourHand.setAttribute('y2', C + Math.sin(ha) * 55);
        // readout
        const mm = String(minTick).padStart(2, '0');
        read.textContent = hourOf() + ':' + mm;
      }

      // The hour a correctly-set clock shows. A valid clock satisfies
      // hourFloat ~= hour + minutes/60, so back out the minute contribution and
      // round to the nearest hour. Tolerant of small drag imprecision, and fixes
      // o'clock times previously reading as the PREVIOUS hour (floor bug).
      function hourOf() {
        let hr = Math.round(hourFloat - minTick / 60);
        hr = ((hr % 12) + 12) % 12;
        return hr === 0 ? 12 : hr;
      }

      function value() {
        return hourOf() + ':' + String(minTick).padStart(2, '0');
      }

      // angle of a pointer relative to centre, in fraction of circle [0,1) where 0 = 12 o'clock
      function frac(ev) {
        const r = svg.getBoundingClientRect();
        const cx = ev.clientX - r.left, cy = ev.clientY - r.top;
        // map to viewBox coords
        const vx = cx / r.width * SZ, vy = cy / r.height * SZ;
        let ang = Math.atan2(vy - C, vx - C) + Math.PI / 2; // 0 at top, clockwise
        let f = ang / (2 * Math.PI);
        f = f - Math.floor(f); // normalise [0,1)
        return f;
      }
      function dist(ev, hand) {
        const r = svg.getBoundingClientRect();
        const vx = (ev.clientX - r.left) / r.width * SZ, vy = (ev.clientY - r.top) / r.height * SZ;
        const dx = vx - C, dy = vy - C;
        return Math.hypot(dx, dy);
      }

      let active = null; // 'hour' | 'minute'

      function pick(ev) {
        // choose the hand: if beyond hour-hand reach, grab minute; else nearer angle wins
        const f = frac(ev);
        const d = dist(ev, null);
        const minAngFrac = minTick / 60;
        const hourAngFrac = hourFloat / 12;
        // angular distance to each hand
        const ad = (a, b) => { let x = Math.abs(a - b); return Math.min(x, 1 - x); };
        const dMin = ad(f, minAngFrac);
        const dHour = ad(f, hourAngFrac);
        // far out -> minute (longer hand); otherwise pick nearer hand angle
        if (d > 62) return 'minute';
        return dMin <= dHour ? 'minute' : 'hour';
      }

      function apply(ev) {
        const f = frac(ev);
        if (active === 'minute') {
          let m = f * 60;
          m = Math.round(m / MIN_SNAP) * MIN_SNAP;
          if (m >= 60) m -= 60;
          minTick = m;
        } else if (active === 'hour') {
          // continuous hour position from angle; keep fractional part so it sits between numbers
          hourFloat = f * 12;
          if (hourFloat >= 12) hourFloat -= 12;
        }
        draw();
      }

      function down(ev) {
        active = pick(ev);
        apply(ev);
        ev.preventDefault();
      }
      function move(ev) { if (active) { apply(ev); ev.preventDefault(); } }
      function up() { active = null; }

      // Pointer events cover mouse + touch uniformly
      svg.addEventListener('pointerdown', (ev) => { down(ev); try { svg.setPointerCapture(ev.pointerId); } catch (e) {} });
      svg.addEventListener('pointermove', move);
      svg.addEventListener('pointerup', up);
      svg.addEventListener('pointercancel', up);
      window.addEventListener('pointerup', up);

      draw();

      host.__getValue = () => value();
      host.__feedback = (res) => {
        read.style.color = res.correct ? '#22c55e' : '#f85149';
      };
    }
  };
})();
