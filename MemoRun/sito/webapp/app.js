/* ═══════════════════════════════════════════════════════════════════════════
   MenmoRun — Web App
   ═══════════════════════════════════════════════════════════════════════════ */

/* ── TEXTS ──────────────────────────────────────────────────────────────── */

const TEXTS = {
  Facile: [
    "il gatto dorme sul tappeto rosso",
    "la casa è grande e molto bella",
    "oggi il sole splende nel cielo",
    "il cane corre veloce nel parco",
    "mangio una mela fresca ogni giorno",
    "il libro è posato sul tavolo",
    "la luna brilla nella notte scura",
    "bevo un caffè caldo ogni mattina",
    "il treno parte dalla stazione presto",
    "la bambina sorride e gioca felice",
    "il mare è blu e molto profondo",
    "vado a scuola ogni giorno di settimana",
    "il fiore sboccia in primavera",
    "la neve cade lenta dal cielo",
    "il bambino ride e corre forte",
    "mangio la pasta con il sugo",
    "il nonno legge il giornale mattina",
    "la gatta dorme vicino al fuoco",
    "bevo acqua fresca ogni pomeriggio",
    "il pane è caldo e profumato",
    "la finestra è aperta sul giardino",
    "il cielo è pieno di stelle",
    "porto lo zaino rosso a scuola",
    "la nonna cucina la torta buona",
    "il sole tramonta sul mare calmo",
    "il gatto gioca con la palla",
    "la strada è lunga e dritta",
    "mangio la frutta ogni mattina presto",
    "il fiume scorre lento tra i prati",
    "la porta è chiusa a chiave",
    "il vento soffia forte oggi pomeriggio",
    "la bici è parcheggiata fuori casa",
    "il latte è fresco e molto buono",
    "la lampada illumina la stanza piccola",
    "il topo corre sotto il tavolo",
    "la foglia cade gialla dal ramo",
    "bevo un tè caldo la sera",
    "il cavallo corre nel campo verde",
    "la bambina legge un libro colorato",
    "il pesce nuota nel lago blu",
    "la scuola inizia alle otto di mattina",
    "il cane dorme vicino alla porta",
    "la mamma prepara la colazione presto",
    "il papà guida la macchina blu",
    "la torta è dolce e molto buona",
    "il treno arriva in orario oggi",
    "la pioggia cade sul tetto rosso",
    "il bosco è verde e molto grande",
    "la montagna è alta e nevosa",
    "bevo il succo di arancia fresco",
  ],
  Medio: [
    "la programmazione richiede pratica costante e molta dedizione per migliorare",
    "il computer moderno è diventato uno strumento potente e indispensabile",
    "studiare dattilografia migliora la velocità di scrittura in modo significativo",
    "scrivere con tutte e dieci le dita aumenta notevolmente la produttività",
    "ogni giorno di pratica porta grandi miglioramenti nella velocità di battitura",
    "la tastiera qwerty è lo standard più diffuso in tutto il mondo occidentale",
    "imparare a digitare velocemente è una competenza fondamentale nel mondo moderno",
    "la postura corretta durante la digitazione previene dolori alle mani e alla schiena",
    "i polsi devono rimanere sollevati mentre si digita per evitare infortuni",
    "ogni dito è responsabile di specifici tasti sulla tastiera italiana standard",
    "la memoria muscolare si sviluppa con la ripetizione costante degli esercizi",
    "digitare senza guardare la tastiera richiede concentrazione e allenamento continuo",
    "la velocità di scrittura aumenta progressivamente con la pratica quotidiana regolare",
    "mantenere una postura eretta durante la digitazione riduce la fatica muscolare",
    "le dita indice riposano sempre sui tasti guida della tastiera standard",
    "la tecnica corretta di battitura evita tensioni inutili nei tendini delle mani",
    "praticare la dattilografia ogni giorno è il modo migliore per migliorare rapidamente",
    "il ritmo costante nella digitazione è più importante della velocità assoluta",
    "la precisione nella battitura deve sempre precedere la ricerca della velocità massima",
    "esercitarsi con testi diversi aiuta a familiarizzare con tutte le combinazioni di lettere",
    "la dattilografia professionale richiede anni di pratica e grande disciplina personale",
    "un dattilografo esperto non ha bisogno di guardare la tastiera mentre scrive",
    "la mano sinistra controlla i tasti del lato sinistro della tastiera italiana",
    "correggere subito gli errori durante la scrittura rallenta la velocità complessiva",
    "la resistenza alla fatica migliora con sessioni di allenamento regolari e brevi",
    "digitare con le dita curve sui tasti garantisce maggiore controllo e precisione",
    "ogni sessione di pratica dovrebbe includere esercizi di riscaldamento per le dita",
    "la concentrazione mentale è fondamentale per mantenere alta la precisione di battitura",
    "imparare la posizione dei tasti speciali accelera la scrittura di testi tecnici",
    "la riga centrale della tastiera contiene i tasti di riferimento per le dita",
    "la battitura cieca aumenta la velocità perché elimina il movimento degli occhi",
    "la velocità di battitura si misura tradizionalmente in parole al minuto digitate",
    "la tastiera meccanica offre un feedback tattile che molti dattilografi preferiscono",
    "la frequenza delle lettere in italiano influenza il design ergonomico delle tastiere",
    "la ripetizione metodica degli esercizi porta alla formazione di abitudini motorie solide",
    "la dattilografia è una disciplina che combina abilità motoria e concentrazione mentale",
    "la produttività di un professionista dipende anche dalla velocità di battitura",
    "le pause regolari durante la digitazione prolungata prevengono il sovraccarico muscolare",
    "la battitura ritmica assomiglia alla pratica musicale per la sua natura ripetitiva",
    "registrare i propri progressi motiva a continuare l'allenamento con costanza e impegno",
  ],
  Difficile: [
    "La velocità di battitura si misura in parole per minuto e un dattilografo esperto raggiunge facilmente le ottanta parole al minuto con grande precisione e costanza nel tempo",
    "Imparare a digitare senza guardare la tastiera è fondamentale per diventare un professionista e aumentare notevolmente la produttività lavorativa in qualsiasi ambiente di lavoro moderno",
    "La tecnica delle dieci dita prevede che ogni dito sia responsabile di specifici tasti riducendo i movimenti inutili e aumentando la velocità complessiva di digitazione professionale",
    "Un buon dattilografo mantiene sempre i polsi sollevati dalla scrivania e le dita curve sopra i tasti garantendo una postura ergonomica e prevenendo infortuni nel lungo periodo",
    "La pratica costante e metodica della dattilografia porta risultati straordinari nel corso delle settimane trasformando una scrittura lenta e incerta in una digitazione fluida e sicura",
    "La memoria muscolare che si sviluppa attraverso la pratica ripetuta della dattilografia permette alle dita di raggiungere i tasti corretti in modo automatico e quasi istintivo",
    "Coloro che imparano la tecnica corretta fin dalle prime sessioni evitano di dover correggere successivamente le cattive abitudini che rallentano la crescita della velocità di battitura",
    "La postura ergonomica durante la digitazione prolungata non solo previene dolori alla schiena e alle mani ma aumenta anche la produttività complessiva nel corso della giornata lavorativa",
    "Il ritmo regolare e la precisione sono le due qualità che un dattilografo professionista deve coltivare con pari attenzione poiché la velocità senza precisione produce testi pieni di errori",
    "La tastiera italiana presenta alcune differenze rispetto alla tastiera anglosassone che il dattilografo deve conoscere a fondo per poter sfruttare appieno la propria velocità di digitazione",
    "La dattilografia è una disciplina che richiede dedizione e costanza nel tempo giacché i progressi sono graduali ma diventano evidenti dopo alcune settimane di allenamento quotidiano regolare",
    "Acquisire la capacità di digitare senza alzare lo sguardo dalla schermata rappresenta un salto qualitativo enorme che libera la mente per concentrarsi interamente sul contenuto che si sta producendo",
    "La tecnica a dieci dita distribuisce equamente il carico di lavoro tra tutte le dita riducendo la fatica e permettendo sessioni di digitazione molto più lunghe senza dolori o crampi muscolari",
    "La pratica della dattilografia in giovane età porta benefici che durano tutta la vita professionale rendendo più agevole qualsiasi attività lavorativa che preveda l'uso intensivo del computer",
    "La velocità di battitura di un professionista qualificato supera spesso le cento parole al minuto il che equivale a produrre un testo di media lunghezza nel tempo di una sola pausa caffè",
    "Una sessione di allenamento ben strutturata alterna fasi di esercizio intenso con momenti di riposo attivo che includono stretching delle mani e dei polsi per mantenere i muscoli in salute",
    "La scelta della tastiera giusta è una decisione importante per chi lavora molte ore al giorno davanti al computer poiché il tipo di meccanismo influenza il comfort e la velocità di battitura",
    "La coordinazione bimanuale sviluppata attraverso la dattilografia ha effetti positivi su altre attività motorie complesse come suonare uno strumento musicale o eseguire lavori di precisione artigianale",
    "La corretta inclinazione del polso durante la digitazione è un aspetto spesso trascurato dai principianti ma fondamentale per evitare la sindrome del tunnel carpale nel corso degli anni",
    "La costanza nell'allenamento è la qualità più importante per chi vuole diventare un dattilografo veloce poiché nessun talento naturale può compensare la mancanza di pratica regolare e sistematica nel tempo",
  ],
};

/* ── KEYBOARD CONFIG ────────────────────────────────────────────────────── */

const KB_ROWS = [
  ['q','w','e','r','t','y','u','i','o','p'],
  ['a','s','d','f','g','h','j','k','l'],
  ['z','x','c','v','b','n','m'],
];
const KB_ROW_OFFSETS = [0, 20, 40]; // px stagger

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
  'à':'mignolo_dx','è':'mignolo_dx','ì':'mignolo_dx','ò':'mignolo_dx','ù':'mignolo_dx',
  ' ':'pollice',
};

const FINGER_COLORS = {
  mignolo_sx: '#e74c3c',
  anulare_sx: '#e67e22',
  medio_sx:   '#f1c40f',
  indice_sx:  '#2ecc71',
  indice_dx:  '#3498db',
  medio_dx:   '#9b59b6',
  anulare_dx: '#1abc9c',
  mignolo_dx: '#e91e63',
  pollice:    '#95a5a6',
};

const FINGER_NAMES = {
  mignolo_sx: 'Mignolo sx',
  anulare_sx: 'Anulare sx',
  medio_sx:   'Medio sx',
  indice_sx:  'Indice sx',
  indice_dx:  'Indice dx',
  medio_dx:   'Medio dx',
  anulare_dx: 'Anulare dx',
  mignolo_dx: 'Mignolo dx',
  pollice:    'Pollice',
};

const FINGER_KEY_LABELS = {
  mignolo_sx: 'Q  A  Z',
  anulare_sx: 'W  S  X',
  medio_sx:   'E  D  C',
  indice_sx:  'R F V  T G B',
  indice_dx:  'Y H N  U J M',
  medio_dx:   'I  K',
  anulare_dx: 'O  L',
  mignolo_dx: 'P  à è ì ò ù',
};

/* ── STENO CONFIG ───────────────────────────────────────────────────────── */

const STENO_KEYS = ['a','s','d','f','g','h','j','k','l',' '];
const STENO_KEY_LABEL = { a:'A',s:'S',d:'D',f:'F',g:'G',h:'H',j:'J',k:'K',l:'L',' ':'SPC' };

// Key: sorted keys joined by space → word
const STENO_CHORDS = {
  'a': 'a',
  'j': 'e',
  ' ': ' ',
  'a d': 'il',
  'j k': 'la',
  'a s': 'al',
  'd f': 'di',
  'g h': 'che',
  'h j': 'ha',
  'k l': 'lo',
  'a j': 'un',
  'k s': 'non',
  'd h': 'per',
  'f k': 'con',
  'f l': 'del',
  'g k': 'tra',
  'd s': 'si',
  'h l': 'le',
  'f h': 'in',
  'g l': 'su',
  'l s': 'ma',
  'd l': 'gli',
  'f j': 'ci',
  'g j': 'né',
  'a d s': 'alla',
  'g h j': 'nella',
  'j k l': 'sono',
  'a d f': 'una',
  'd g k': 'questo',
  'f h l': 'tutto',
  'g j k': 'anche',
  'a f j': 'più',
  'd f h': 'come',
  'g l s': 'così',
  'a h l': 'dopo',
  'd j k': 'loro',
  'f g j': 'ogni',
  'h k l': 'prima',
  'a j s': 'fare',
  'd f k': 'dove',
  'g h l': 'mentre',
  'a k l': 'quando',
};

// Reverse map: word → chord key string
const CHORD_FOR_WORD = Object.fromEntries(
  Object.entries(STENO_CHORDS).map(([k, v]) => [v, k])
);

const STENO_EXERCISES = [
  ['il','la','un','una','di','in','che','non','per','con'],
  ['al','si','lo','le','ma','su','tra','del','ha','più'],
  ['alla','nella','sono','questo','tutto','anche','come','così','il','la'],
  ['un','la','e','a','di','che','non','per','anche','tutto'],
  ['dopo','loro','ogni','prima','fare','dove','mentre','quando','il','la'],
  ['gli','ci','con','del','tra','su','ma','in','per','non'],
];

function chordKey(keysIterable) {
  return [...keysIterable].sort().join(' ');
}

function chordStr(keyStr) {
  return keyStr.split(' ').map(k => STENO_KEY_LABEL[k] || k.toUpperCase()).join(' + ');
}

/* ── STATS ──────────────────────────────────────────────────────────────── */

const STATS_KEY = 'memorun_stats';
const DEFAULT_STATS = { sessions: 0, best_wpm: 0, total_wpm: 0, total_chars: 0 };

function loadStats() {
  try { return { ...DEFAULT_STATS, ...JSON.parse(localStorage.getItem(STATS_KEY) || '{}') }; }
  catch { return { ...DEFAULT_STATS }; }
}
function saveStats(s) { localStorage.setItem(STATS_KEY, JSON.stringify(s)); }
function avgWPM(s) { return s.sessions > 0 ? Math.round(s.total_wpm / s.sessions) : 0; }
function updateStats(s, wpm, chars) {
  s.sessions++;
  s.total_wpm += wpm;
  s.total_chars += chars;
  if (wpm > s.best_wpm) s.best_wpm = wpm;
  saveStats(s);
}

/* ── UTILS ──────────────────────────────────────────────────────────────── */

const $ = id => document.getElementById(id);
const app = () => $('app');

function h(tag, cls, attrs, ...children) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (attrs) Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'style' && typeof v === 'object') Object.assign(el.style, v);
    else if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v);
  });
  children.forEach(c => {
    if (c == null) return;
    el.append(typeof c === 'string' ? c : c);
  });
  return el;
}

function rand(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

/* ── APP STATE ──────────────────────────────────────────────────────────── */

let stats = loadStats();
let stenoCleanup = null;

/* ── SCREEN MANAGER ─────────────────────────────────────────────────────── */

function render(screenEl) {
  if (stenoCleanup) { stenoCleanup(); stenoCleanup = null; }
  const a = app();
  a.innerHTML = '';
  a.appendChild(screenEl);
}

/* ══════════════════════════════════════════════════════════════════════════
   HOME SCREEN
   ══════════════════════════════════════════════════════════════════════════ */

function goHome() {
  stats = loadStats();
  const screen = h('div', 'screen active');
  screen.appendChild(buildAppNav(null, [
    h('button', 'btn btn-sm btn-pink', { onclick: () => resetStatsDialog() }, 'Azzera stats'),
  ]));

  const body = h('div', 'screen-body');
  const wrap = h('div', 'home-wrap');

  // Title
  wrap.appendChild(h('h1', 'home-title', null, 'MenmoRun'));
  wrap.appendChild(h('p', 'home-subtitle', null,
    'Impara a scrivere velocemente con tutte e 10 le dita'));

  // Stats row
  const statsRow = h('div', 'stats-row');
  [
    [stats.sessions,       'Sessioni'],
    [stats.best_wpm,       'Record WPM'],
    [avgWPM(stats),        'Media WPM'],
    [stats.total_chars.toLocaleString('it'), 'Caratteri totali'],
  ].forEach(([val, lbl]) => {
    const card = h('div', 'stat-card');
    card.appendChild(h('div', 'stat-card-val', null, String(val)));
    card.appendChild(h('div', 'stat-card-lbl', null, lbl));
    statsRow.appendChild(card);
  });
  wrap.appendChild(statsRow);

  // Difficulty
  wrap.appendChild(h('div', 'section-lbl', null, 'Seleziona difficoltà'));
  const diffGrid = h('div', 'diff-grid');
  [
    { name: 'Facile',        color: '#27ae60', desc: 'Parole semplici · 5–8 parole',   diff: 'Facile' },
    { name: 'Medio',         color: '#f39c12', desc: 'Frasi complete · 8–14 parole',   diff: 'Medio' },
    { name: 'Difficile',     color: '#e74c3c', desc: 'Testi lunghi · 20+ parole',      diff: 'Difficile' },
    { name: 'Personalizzato',color: '#8e44ad', desc: 'Il tuo testo · lunghezza libera', diff: null },
  ].forEach(({ name, color, desc, diff }) => {
    const card = h('div', 'diff-card', {
      onclick: () => diff ? goPractice(diff) : goCustom(),
    });
    card.style.borderColor = color + '44';
    const nameEl = h('div', 'diff-card-name', null, name);
    nameEl.style.color = color;
    const descEl = h('div', 'diff-card-desc', null, desc);
    const btn = h('button', 'btn btn-sm', null, 'Inizia');
    btn.style.borderColor = color;
    btn.style.color = color;
    btn.style.boxShadow = `0 0 10px ${color}44`;
    btn.addEventListener('click', e => { e.stopPropagation(); diff ? goPractice(diff) : goCustom(); });
    card.append(nameEl, descEl, btn);
    diffGrid.appendChild(card);
  });
  wrap.appendChild(diffGrid);

  // Steno
  wrap.appendChild(h('div', 'sep'));
  wrap.appendChild(h('div', 'section-lbl', null, 'Modalità avanzata'));
  const stenoCard = h('div', 'steno-card', { onclick: goSteno });
  stenoCard.appendChild(h('div', 'steno-card-name', null, 'Stenografia · 10 tasti'));
  stenoCard.appendChild(h('div', 'steno-card-desc', null, 'Chord-based input · A S D F G H J K L ▁'));
  wrap.appendChild(stenoCard);

  // Finger guide
  wrap.appendChild(h('div', 'section-lbl', null, 'Posizione delle dita'));
  const fingerGrid = h('div', 'finger-guide-grid');
  Object.entries(FINGER_KEY_LABELS).forEach(([finger, keys]) => {
    const cell = h('div', 'finger-cell');
    cell.style.background = FINGER_COLORS[finger];
    cell.appendChild(h('div', 'finger-cell-name', null, FINGER_NAMES[finger]));
    cell.appendChild(h('div', 'finger-cell-keys', null, keys));
    fingerGrid.appendChild(cell);
  });
  wrap.appendChild(fingerGrid);

  body.appendChild(wrap);
  screen.appendChild(body);
  render(screen);
}

function resetStatsDialog() {
  if (confirm('Azzerare tutte le statistiche?')) {
    stats = { ...DEFAULT_STATS };
    saveStats(stats);
    goHome();
  }
}

/* ══════════════════════════════════════════════════════════════════════════
   PRACTICE SCREEN
   ══════════════════════════════════════════════════════════════════════════ */

function goPractice(difficulty, text = null, wordByWord = false) {
  if (!text) text = rand(TEXTS[difficulty] || TEXTS.Facile);
  buildPractice(difficulty, text, wordByWord);
}

function buildPractice(difficulty, text, wordByWord) {
  const screen = h('div', 'screen active');
  screen.appendChild(buildAppNav(goHome, [
    h('span', 'practice-diff', null, `Difficoltà: ${difficulty}`),
    h('button', 'btn btn-sm btn-ghost', { onclick: () => goPractice(difficulty) }, 'Nuovo testo'),
  ]));

  const body = h('div', 'screen-body');
  const wrap = h('div', 'practice-wrap');

  // Live stats bar
  const liveStats = h('div', 'live-stats');
  const wpmEl  = h('div', 'live-val wpm-val',  null, '0');
  const accEl  = h('div', 'live-val acc-val',  null, '100');
  const timeEl = h('div', 'live-val time-val', null, '0:00');
  [
    [wpmEl,  'WPM'],
    [accEl,  'Precisione %'],
    [timeEl, 'Tempo'],
  ].forEach(([valEl, lbl]) => {
    const card = h('div', 'live-card');
    card.append(valEl, h('div', 'live-lbl', null, lbl));
    liveStats.appendChild(card);
  });
  wrap.appendChild(liveStats);

  // Word-by-word counter
  const wbwCounter = h('div', 'wbw-counter');
  wbwCounter.style.display = wordByWord ? '' : 'none';
  wrap.appendChild(wbwCounter);

  // Text display
  const textDisplay = h('div', 'text-display');
  wrap.appendChild(textDisplay);

  // Input
  const input = h('input', 'practice-input', {
    type: 'text',
    placeholder: 'Inizia a digitare qui…',
    autocomplete: 'off',
    autocorrect: 'off',
    autocapitalize: 'off',
    spellcheck: 'false',
  });
  wrap.appendChild(input);

  // Progress bar
  const progressFill = h('div', 'progress-fill');
  progressFill.style.width = '0%';
  wrap.appendChild(h('div', 'progress-track', null, progressFill));

  // Bottom: keyboard + legend
  const bottom = h('div', 'practice-bottom');
  const kbWrap = h('div', 'kb-wrap');
  const keyMap = buildKeyboard(kbWrap);
  const hintLabel = h('div', 'hint-label');

  const legendWrap = h('div', 'legend-wrap');
  legendWrap.appendChild(h('div', 'legend-title', null, 'Legenda dita'));
  const legendGrid = h('div', 'legend-grid');
  Object.entries(FINGER_KEY_LABELS).forEach(([finger, keys]) => {
    const cell = h('div', 'legend-cell');
    cell.style.background = FINGER_COLORS[finger];
    cell.appendChild(h('span', 'legend-cell-name', null, FINGER_NAMES[finger]));
    cell.appendChild(h('span', 'legend-cell-keys', null, keys));
    legendGrid.appendChild(cell);
  });
  legendWrap.appendChild(legendGrid);

  bottom.append(h('div', '', null, kbWrap, hintLabel), legendWrap);
  wrap.appendChild(bottom);

  body.appendChild(wrap);
  screen.appendChild(body);
  render(screen);
  input.focus();

  // ── Practice state ──────────────────────────────────────────────────────
  const words = wordByWord ? text.split(' ') : [];
  let wordIndex = 0;
  let allTyped = '';
  let typed = '';
  let startTime = null;
  let finished = false;
  let timerID = null;

  function refreshDisplay() {
    let html = '';
    const src = wordByWord ? words[wordIndex] || '' : text;
    const cur = wordByWord ? input.value.replace(/ $/, '') : typed;

    for (let i = 0; i < src.length; i++) {
      const ch = src[i];
      const display = ch === ' ' ? ' ' : ch;
      if (i < cur.length) {
        const ok = cur[i] === ch;
        html += ok
          ? `<span class="char correct">${display}</span>`
          : `<span class="char wrong">${display}</span>`;
      } else if (i === cur.length) {
        html += `<span class="char cursor">${display}</span>`;
      } else {
        const finger = KEY_FINGER[ch.toLowerCase()] || 'indice_dx';
        const color = FINGER_COLORS[finger];
        html += `<span class="char pending" style="color:${color}">${display}</span>`;
      }
    }
    textDisplay.innerHTML = html;

    const total = wordByWord ? words.length : text.length;
    const done  = wordByWord ? wordIndex : typed.length;
    progressFill.style.width = total > 0 ? (Math.min(done / total, 1) * 100) + '%' : '0%';

    if (wordByWord) {
      wbwCounter.textContent = `Parola ${Math.min(wordIndex + 1, words.length)} / ${words.length}`;
    }
  }

  function highlightNextKey() {
    // Reset all keys
    Object.values(keyMap).forEach(({ el, color }) => {
      el.classList.remove('highlighted');
      el.style.background = '';
      el.style.color = color;
    });

    const src = wordByWord ? words[wordIndex] || '' : text;
    const pos = wordByWord ? input.value.replace(/ $/, '').length : typed.length;

    if (pos < src.length) {
      const nextCh = src[pos].toLowerCase();
      if (keyMap[nextCh]) {
        const { el, color } = keyMap[nextCh];
        el.classList.add('highlighted');
        el.style.background = color;
        el.style.color = '#fff';
        const finger = KEY_FINGER[nextCh] || 'indice_dx';
        hintLabel.textContent = `Dito: ${FINGER_NAMES[finger] || finger}`;
        hintLabel.style.color = color;
      }
    } else {
      hintLabel.textContent = '';
    }
  }

  function calcStats() {
    if (!startTime) return;
    const elapsed = Math.max((Date.now() - startTime) / 60000, 0.001);
    const cur = wordByWord ? allTyped + input.value : typed;
    const wpm = Math.round((cur.length / 5) / elapsed);
    wpmEl.textContent = wpm;
    if (cur.length > 0) {
      const src = wordByWord ? text : text;
      const correct = [...cur].filter((c, i) => c === (src[i] || '')).length;
      accEl.textContent = Math.round((correct / cur.length) * 100);
    }
  }

  function tickTimer() {
    if (!startTime || finished) return;
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const m = Math.floor(elapsed / 60), s = elapsed % 60;
    timeEl.textContent = `${m}:${s.toString().padStart(2, '0')}`;
    timerID = setTimeout(tickTimer, 500);
  }

  function finish() {
    finished = true;
    clearTimeout(timerID);

    const elapsed = Math.max((Date.now() - startTime) / 60000, 0.001);
    const wpm = Math.round((text.length / 5) / elapsed);

    const src = text;
    const final = wordByWord ? allTyped : typed;
    const correct = [...final].filter((c, i) => c === (src[i] || '')).length;
    const acc = Math.round((correct / Math.max(final.length, 1)) * 100);

    updateStats(stats, wpm, text.length);

    setTimeout(() => goResult(wpm, acc, difficulty, text), 300);
  }

  input.addEventListener('keydown', e => {
    if (e.key === 'Backspace' || e.key === 'Delete') e.preventDefault();
    if (e.key === 'Escape') goHome();
  });

  input.addEventListener('input', () => {
    if (finished) return;
    const val = input.value;

    if (!startTime && val.length > 0) {
      startTime = Date.now();
      tickTimer();
    }

    if (wordByWord) {
      const word = words[wordIndex];
      const isLast = wordIndex === words.length - 1;

      if (val.endsWith(' ')) {
        allTyped += val.slice(0, -1) + ' ';
        if (isLast) { allTyped = allTyped.trimEnd(); finish(); return; }
        wordIndex++;
        input.value = '';
      } else if (isLast && val.length >= word.length) {
        allTyped += val;
        finish(); return;
      }
    } else {
      typed = val;
      if (typed.length >= text.length) {
        refreshDisplay(); calcStats();
        finish(); return;
      }
    }

    refreshDisplay();
    calcStats();
    highlightNextKey();
  });

  refreshDisplay();
  highlightNextKey();
}

/* ══════════════════════════════════════════════════════════════════════════
   RESULT SCREEN
   ══════════════════════════════════════════════════════════════════════════ */

function goResult(wpm, acc, difficulty, text) {
  const screen = h('div', 'screen active');
  screen.appendChild(buildAppNav(goHome));

  const body = h('div', 'screen-body');
  const wrap = h('div', 'result-wrap');

  wrap.appendChild(h('h2', 'result-title', null, 'Esercizio completato!'));

  // Result cards
  const cards = h('div', 'result-cards');
  [
    { val: wpm,  unit: 'WPM',  lbl: 'Velocità',  color: wpmColor(wpm) },
    { val: acc,  unit: '%',    lbl: 'Precisione', color: accColor(acc) },
  ].forEach(({ val, unit, lbl, color }) => {
    const card = h('div', 'result-card');
    card.style.borderColor = color + '44';
    const big = h('div', 'result-big', null, String(val));
    big.style.color = color;
    big.style.textShadow = `0 0 28px ${color}66`;
    const unitEl = h('div', 'result-unit', null, unit);
    unitEl.style.color = color;
    card.append(big, unitEl, h('div', 'result-lbl', null, lbl));
    cards.appendChild(card);
  });
  wrap.appendChild(cards);

  // Record badge
  if (stats.sessions >= 1 && wpm >= stats.best_wpm) {
    wrap.appendChild(h('div', 'record-badge', null, '★ Nuovo record personale!'));
  }

  // Message
  wrap.appendChild(h('p', 'result-msg', null, resultMessage(wpm, acc)));

  // Action buttons
  const actions = h('div', 'result-actions');
  const riprova = h('button', 'btn', { onclick: () => goPractice(difficulty, text) }, 'Riprova');
  const cambia  = h('button', 'btn btn-pink', { onclick: () => {
    const pool = (TEXTS[difficulty] || []).filter(t => t !== text);
    goPractice(difficulty, pool.length ? rand(pool) : rand(TEXTS[difficulty]));
  }}, 'Cambia frase');
  const home   = h('button', 'btn btn-ghost', { onclick: goHome }, 'Cambia difficoltà');
  actions.append(riprova, cambia, home);
  wrap.appendChild(actions);

  // Homerow reminder
  wrap.appendChild(h('p', 'homerow-reminder', null, 'Ricorda: tieni le dita sulla home row (A S D F  J K L)'));
  const homerow = h('div', 'homerow-keys');
  [
    ['A','mignolo_sx'],['S','anulare_sx'],['D','medio_sx'],['F','indice_sx'],
    ['J','indice_dx'], ['K','medio_dx'],  ['L','anulare_dx'],
  ].forEach(([key, finger]) => {
    const el = h('div', 'homerow-key', null, key);
    el.style.background = FINGER_COLORS[finger];
    homerow.appendChild(el);
  });
  wrap.appendChild(homerow);

  body.appendChild(wrap);
  screen.appendChild(body);
  render(screen);
}

function wpmColor(wpm)  { return wpm < 20 ? '#e74c3c' : wpm < 40 ? '#f39c12' : '#2ecc71'; }
function accColor(acc)  { return acc < 80 ? '#e74c3c' : acc < 95 ? '#f39c12' : '#2ecc71'; }

function resultMessage(wpm, acc) {
  if (acc < 80)  return 'Concentrati sulla precisione prima della velocità. Rallenta e digita ogni carattere con cura.';
  if (wpm < 20)  return 'Buon inizio! Pratica ogni giorno e la velocità aumenterà naturalmente. Non guardare la tastiera!';
  if (wpm < 40)  return 'Stai migliorando! Usa le dita giuste per ogni tasto e non guardare la tastiera.';
  if (wpm < 60)  return 'Ottimo risultato! Sei a un buon livello. Continua e raggiungerai presto i 60 WPM.';
  return 'Eccellente! Sei un dattilografo esperto. Sfidati con testi più difficili!';
}

/* ══════════════════════════════════════════════════════════════════════════
   STENO SCREEN
   ══════════════════════════════════════════════════════════════════════════ */

function goSteno() {
  const screen = h('div', 'screen active');
  screen.appendChild(buildAppNav(goHome, [
    h('button', 'btn btn-sm btn-purple', { onclick: goSteno }, 'Nuovo esercizio'),
  ]));

  const body = h('div', 'screen-body');
  const wrap = h('div', 'steno-wrap');

  const exercise = rand(STENO_EXERCISES);
  let wordIndex = 0;
  let correct = 0, wrong = 0;
  let startTime = null;
  let finished = false;
  const pressed = new Set();
  const chord   = new Set();

  // Progress
  const progressEl = h('div', 'steno-progress', null, `0 / ${exercise.length}`);
  wrap.appendChild(progressEl);

  // Target area
  const targetArea = h('div', 'steno-target-area');
  const wordEl    = h('span', 'steno-word', null, '');
  const hintEl    = h('div', 'steno-chord-hint', null, '');
  const feedbackEl = h('div', 'steno-feedback', null, '');
  targetArea.append(
    h('div', 'steno-prompt', null, 'Premi il chord per:'),
    wordEl, hintEl, feedbackEl
  );
  wrap.appendChild(targetArea);

  // Steno keyboard
  const kbSection = h('div', 'steno-kb-section');
  kbSection.appendChild(h('div', 'steno-kb-lbl', null, 'Tastiera stenografica — home row + spazio'));
  const kbRow = h('div', 'steno-kb-row');
  const stenoBtns = {};
  STENO_KEYS.forEach(k => {
    const btn = h('div', k === ' ' ? 'steno-btn steno-space-btn' : 'steno-btn', null, STENO_KEY_LABEL[k]);
    kbRow.appendChild(btn);
    stenoBtns[k] = btn;
  });
  kbSection.appendChild(kbRow);
  wrap.appendChild(kbSection);

  // Live stats
  const cpmEl = h('div', 'steno-stat-val', null, '0');
  const sAccEl = h('div', 'steno-stat-val', null, '100');
  const statsSection = h('div', 'steno-stats');
  [[cpmEl,'Chord / min'],[sAccEl,'Precisione %']].forEach(([valEl, lbl]) => {
    const s = h('div', 'steno-stat');
    s.append(valEl, h('div', 'steno-stat-lbl', null, lbl));
    statsSection.appendChild(s);
  });
  wrap.appendChild(statsSection);

  // Chord reference
  wrap.appendChild(h('div', 'steno-ref-title', null, 'Dizionario chord'));
  const refGrid = h('div', 'steno-ref-grid');
  Object.entries(CHORD_FOR_WORD)
    .sort((a, b) => a[0].length - b[0].length || a[0].localeCompare(b[0]))
    .forEach(([word, keyStr]) => {
      const cell = h('div', 'steno-ref-cell');
      cell.appendChild(h('div', 'steno-ref-word', null, word));
      cell.appendChild(h('div', 'steno-ref-chord', null, chordStr(keyStr)));
      refGrid.appendChild(cell);
    });
  wrap.appendChild(refGrid);

  body.appendChild(wrap);
  screen.appendChild(body);
  render(screen);

  // ── Show first target ───────────────────────────────────────────────────
  function showTarget() {
    if (wordIndex >= exercise.length) { doFinish(); return; }
    const word = exercise[wordIndex];
    wordEl.textContent = word;
    wordEl.style.opacity = '1';
    const keyStr = CHORD_FOR_WORD[word] || '';
    hintEl.textContent = `Chord: ${chordStr(keyStr)}`;
    feedbackEl.textContent = '';
    progressEl.textContent = `${wordIndex} / ${exercise.length}`;
    resetKb();
    if (keyStr) keyStr.split(' ').forEach(k => { if (stenoBtns[k]) stenoBtns[k].classList.add('hint'); });
  }

  function resetKb() {
    Object.values(stenoBtns).forEach(btn => btn.className = btn.className.replace(/\bhint\b|\bpressed\b|\berror\b/g, '').trim());
  }

  function updateStenoStats() {
    const total = correct + wrong;
    if (startTime && total > 0) {
      const elapsed = Math.max((Date.now() - startTime) / 60000, 0.001);
      cpmEl.textContent = Math.round(correct / elapsed);
    }
    if (total > 0) sAccEl.textContent = Math.round((correct / total) * 100);
  }

  function resolveChord() {
    const key = chordKey(chord);
    chord.clear();

    if (finished) return;
    const targetWord = exercise[wordIndex];
    const targetKey  = CHORD_FOR_WORD[targetWord] || '';

    if (key === targetKey) {
      correct++;
      feedbackEl.textContent = '✓ Corretto!';
      feedbackEl.style.color = '#27ae60';
      wordIndex++;
      updateStenoStats();
      setTimeout(showTarget, 280);
    } else {
      wrong++;
      const matched = STENO_CHORDS[key];
      feedbackEl.textContent = matched ? `✗  Hai premuto: "${matched}"` : '✗  Chord non riconosciuto';
      feedbackEl.style.color = '#e74c3c';
      updateStenoStats();
      Object.values(stenoBtns).forEach(btn => {
        if (btn.classList.contains('pressed')) {
          btn.classList.remove('pressed');
          btn.classList.add('error');
        }
      });
      setTimeout(() => {
        resetKb();
        if (targetKey) targetKey.split(' ').forEach(k => { if (stenoBtns[k]) stenoBtns[k].classList.add('hint'); });
      }, 400);
    }
  }

  function doFinish() {
    finished = true;
    const elapsed = Math.max((Date.now() - (startTime || Date.now())) / 60000, 0.001);
    const total = correct + wrong;
    const cpm = Math.round(correct / elapsed);
    const finalAcc = Math.round((correct / Math.max(total, 1)) * 100);

    wordEl.textContent = 'Completato!';
    wordEl.style.color = '#27ae60';
    hintEl.textContent = `Chord/min: ${cpm}  ·  Precisione: ${finalAcc}%`;
    feedbackEl.textContent = `✓ ${correct} / ${total} chord corretti`;
    feedbackEl.style.color = '#27ae60';
    progressEl.textContent = `${exercise.length} / ${exercise.length}`;
    resetKb();
  }

  function onKeyDown(e) {
    if (finished) return;
    const key = e.key === ' ' ? ' ' : e.key.toLowerCase();
    if (e.key === 'Escape') { goHome(); return; }
    if (!STENO_KEYS.includes(key)) return;
    e.preventDefault();
    if (!startTime) startTime = Date.now();
    pressed.add(key);
    chord.add(key);
    if (stenoBtns[key]) {
      stenoBtns[key].classList.remove('hint');
      stenoBtns[key].classList.add('pressed');
    }
  }

  function onKeyUp(e) {
    const key = e.key === ' ' ? ' ' : e.key.toLowerCase();
    pressed.delete(key);
    if (pressed.size === 0 && chord.size > 0) resolveChord();
  }

  document.addEventListener('keydown', onKeyDown);
  document.addEventListener('keyup', onKeyUp);
  stenoCleanup = () => {
    document.removeEventListener('keydown', onKeyDown);
    document.removeEventListener('keyup', onKeyUp);
  };

  showTarget();
}

/* ══════════════════════════════════════════════════════════════════════════
   CUSTOM TEXT SCREEN
   ══════════════════════════════════════════════════════════════════════════ */

function goCustom() {
  const screen = h('div', 'screen active');
  screen.appendChild(buildAppNav(goHome));

  const body = h('div', 'screen-body');
  const wrap = h('div', 'custom-wrap');

  wrap.appendChild(h('h2', 'custom-title', null, 'Testo personalizzato'));
  wrap.appendChild(h('p', 'custom-desc', null,
    'Incolla qualsiasi testo: un articolo, un codice sorgente, una poesia.'));

  const textarea = h('textarea', 'custom-textarea', {
    placeholder: 'Incolla qui il tuo testo…',
  });
  wrap.appendChild(textarea);

  const wbwLabel = h('label', 'toggle-label');
  const wbwCheck = h('input', null, { type: 'checkbox' });
  wbwLabel.append(wbwCheck, 'Modalità parola per parola');

  wrap.appendChild(h('div', 'custom-opts', null, wbwLabel));

  const actions = h('div', 'custom-actions');
  actions.appendChild(h('button', 'btn btn-ghost', { onclick: goHome }, '← Indietro'));
  const startBtn = h('button', 'btn', { onclick: () => {
    const val = textarea.value.trim();
    if (!val) return;
    goPractice('Personalizzato', val, wbwCheck.checked);
  }}, 'Inizia esercizio');
  actions.appendChild(startBtn);

  wrap.appendChild(actions);
  body.appendChild(wrap);
  screen.appendChild(body);
  render(screen);
  textarea.focus();
}

/* ══════════════════════════════════════════════════════════════════════════
   SHARED COMPONENTS
   ══════════════════════════════════════════════════════════════════════════ */

function buildAppNav(backFn, rightEls = []) {
  const nav = h('div', 'app-nav');
  const left = h('div', 'nav-right');
  if (backFn) {
    left.appendChild(h('button', 'btn btn-sm btn-ghost', { onclick: backFn }, '← Home'));
  } else {
    const logo = h('a', 'nav-logo', { href: '../' });
    logo.innerHTML = 'Menmo<span>Run</span>';
    left.appendChild(logo);
  }
  nav.appendChild(left);
  if (rightEls.length) {
    const right = h('div', 'nav-right');
    rightEls.forEach(el => right.appendChild(el));
    nav.appendChild(right);
  }
  return nav;
}

function buildKeyboard(container) {
  const map = {};

  KB_ROWS.forEach((row, ri) => {
    const rowEl = h('div', 'kb-row');
    rowEl.style.paddingLeft = KB_ROW_OFFSETS[ri] + 'px';
    row.forEach(key => {
      const finger = KEY_FINGER[key] || 'indice_dx';
      const color  = FINGER_COLORS[finger];
      const el = h('div', 'kb-key', null, key.toUpperCase());
      el.style.color = color;
      rowEl.appendChild(el);
      map[key] = { el, color };
    });
    container.appendChild(rowEl);
  });

  // Space
  const spRow = h('div', 'kb-space-row');
  spRow.style.paddingLeft = '20px';
  const sp = h('div', 'kb-space', null, 'SPAZIO');
  sp.style.color = FINGER_COLORS.pollice;
  spRow.appendChild(sp);
  container.appendChild(spRow);
  map[' '] = { el: sp, color: FINGER_COLORS.pollice };

  return map;
}

/* ── INIT ───────────────────────────────────────────────────────────────── */

window.addEventListener('DOMContentLoaded', goHome);

// "><(((º> sabusabu <º)))><"
