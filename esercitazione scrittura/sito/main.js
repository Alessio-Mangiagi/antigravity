/* ── Keyboard data ──────────────────────────────────────────────────────── */

const FINGER_COLORS = {
  mignolo_sx: '#e74c3c', anulare_sx: '#e67e22', medio_sx: '#f1c40f',
  indice_sx: '#2ecc71', indice_dx: '#3498db', medio_dx: '#9b59b6',
  anulare_dx: '#1abc9c', mignolo_dx: '#e91e63', pollice: '#95a5a6',
};

const KEY_FINGER = {
  q:'mignolo_sx', a:'mignolo_sx', z:'mignolo_sx',
  w:'anulare_sx', s:'anulare_sx', x:'anulare_sx',
  e:'medio_sx',   d:'medio_sx',   c:'medio_sx',
  r:'indice_sx',  f:'indice_sx',  v:'indice_sx',
  t:'indice_sx',  g:'indice_sx',  b:'indice_sx',
  y:'indice_dx',  h:'indice_dx',  n:'indice_dx',
  u:'indice_dx',  j:'indice_dx',  m:'indice_dx',
  i:'medio_dx',   k:'medio_dx',
  o:'anulare_dx', l:'anulare_dx',
  p:'mignolo_dx',
  ' ':'pollice',
};

const KB_ROWS = [
  ['q','w','e','r','t','y','u','i','o','p'],
  ['a','s','d','f','g','h','j','k','l'],
  ['z','x','c','v','b','n','m'],
];

const ROW_OFFSETS = [0, 20, 40]; // px

/* ── Build keyboard ─────────────────────────────────────────────────────── */

function buildKb(id) {
  const container = document.getElementById(id);
  if (!container) return {};

  const map = {};

  KB_ROWS.forEach((row, ri) => {
    const rowEl = document.createElement('div');
    rowEl.className = 'kb-row';
    rowEl.style.paddingLeft = ROW_OFFSETS[ri] + 'px';

    row.forEach(key => {
      const finger = KEY_FINGER[key] || 'indice_dx';
      const color  = FINGER_COLORS[finger];
      const el     = document.createElement('div');
      el.className = 'kb-key';
      el.style.color = color;
      el.textContent = key.toUpperCase();
      rowEl.appendChild(el);
      map[key] = { el, color };
    });

    container.appendChild(rowEl);
  });

  // Space bar row
  const spRow = document.createElement('div');
  spRow.className = 'kb-space-row';
  spRow.style.paddingLeft = '20px';
  const sp = document.createElement('div');
  sp.className = 'kb-space';
  sp.style.color = FINGER_COLORS.pollice;
  sp.textContent = 'SPAZIO';
  spRow.appendChild(sp);
  container.appendChild(spRow);
  map[' '] = { el: sp, color: FINGER_COLORS.pollice };

  return map;
}

const heroMap = buildKb('kb-hero');
buildKb('kb-feat');  // static, no animation

/* ── Animate hero keyboard ──────────────────────────────────────────────── */

const SEQ = 'pratica ogni giorno ';
let seqIdx = 0;
let prevKey = null;

function tickKeyboard() {
  // Reset previous
  if (prevKey !== null && heroMap[prevKey]) {
    const { el, color } = heroMap[prevKey];
    el.classList.remove('lit');
    el.style.background = 'var(--bg-3)';
    el.style.color = color;
    el.style.boxShadow = '';
  }

  const ch = SEQ[seqIdx % SEQ.length];
  seqIdx++;
  const key = ch.toLowerCase();
  prevKey = key;

  if (heroMap[key]) {
    const { el, color } = heroMap[key];
    el.classList.add('lit');
    el.style.background = color;
    el.style.color = '#fff';
    el.style.boxShadow = `0 0 18px ${color}55`;
  }
}

setInterval(tickKeyboard, 320);

/* ── Text preview ───────────────────────────────────────────────────────── */

const PREVIEW = 'la tastiera qwerty e lo standard';
const TYPED   = 'la tastiera qwerty ';

const previewEl = document.getElementById('text-preview');
PREVIEW.split('').forEach((ch, i) => {
  const span = document.createElement('span');
  span.textContent = ch;

  if (i < TYPED.length) {
    span.style.color = TYPED[i] === ch ? '#a6e3a1' : '#f38ba8';
  } else if (i === TYPED.length) {
    span.style.color = '#1e1e2e';
    span.style.backgroundColor = '#89b4fa';
    span.style.borderRadius = '2px';
  } else {
    const finger = KEY_FINGER[ch.toLowerCase()];
    span.style.color = finger ? FINGER_COLORS[finger] : '#45475a';
  }

  previewEl.appendChild(span);
});

/* ── Okabe-Ito swatches ─────────────────────────────────────────────────── */

['#E69F00','#56B4E9','#F0E442','#009E73','#0072B2','#D55E00','#CC79A7','#648FFF']
  .forEach(c => {
    const el = document.createElement('div');
    el.className = 'swatch';
    el.style.backgroundColor = c;
    document.getElementById('palette-swatches').appendChild(el);
  });

/* ── Scroll reveal ──────────────────────────────────────────────────────── */

const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      revealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.08, rootMargin: '-40px 0px' });

document.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));

/* ── Stat counters ──────────────────────────────────────────────────────── */

document.querySelectorAll('[data-target]').forEach(el => {
  const target = parseInt(el.dataset.target);
  const suffix = el.dataset.suffix || '';
  let fired = false;

  const obs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting && !fired) {
      fired = true;
      let n = 0;
      const step = target / 32;
      const t = setInterval(() => {
        n += step;
        if (n >= target) { el.textContent = target + suffix; clearInterval(t); }
        else { el.textContent = Math.floor(n) + suffix; }
      }, 36);
    }
  }, { threshold: 0.6 });

  obs.observe(el);
});
