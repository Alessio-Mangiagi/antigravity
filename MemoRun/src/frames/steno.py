# =============================================================================
# frames/steno.py — Modalità stenografica a 10 tasti (StenoFrame)
# Chord-based input: l'utente preme più tasti contemporaneamente.
# I 10 tasti usati sono la home row: A S D F G H J K L + SPAZIO.
# Ogni chord (insieme di tasti) corrisponde a una parola italiana.
# =============================================================================

import time
import random
import customtkinter as ctk
from ..config import get_finger_colors

# ─── 10 tasti stenografici (home row + spazio) ────────────────────────────────
STENO_KEYS = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' ']

# ─── Dizionario chord → parola italiana ──────────────────────────────────────
# frozenset di tasti → parola da produrre
STENO_CHORDS: dict[frozenset, str] = {
    # 1 tasto
    frozenset(['a']):               'a',
    frozenset(['j']):               'e',
    frozenset([' ']):               ' ',
    # 2 tasti
    frozenset(['a', 'd']):          'il',
    frozenset(['j', 'k']):          'la',
    frozenset(['a', 's']):          'al',
    frozenset(['d', 'f']):          'di',
    frozenset(['g', 'h']):          'che',
    frozenset(['h', 'j']):          'ha',
    frozenset(['k', 'l']):          'lo',
    frozenset(['a', 'j']):          'un',
    frozenset(['s', 'k']):          'non',
    frozenset(['d', 'h']):          'per',
    frozenset(['f', 'k']):          'con',
    frozenset(['f', 'l']):          'del',
    frozenset(['g', 'k']):          'tra',
    frozenset(['s', 'd']):          'si',
    frozenset(['h', 'l']):          'le',
    frozenset(['f', 'h']):          'in',
    frozenset(['g', 'l']):          'su',
    frozenset(['s', 'l']):          'ma',
    frozenset(['d', 'l']):          'gli',
    frozenset(['f', 'j']):          'ci',
    frozenset(['g', 'j']):          'né',
    # 3 tasti
    frozenset(['a', 's', 'd']):     'alla',
    frozenset(['g', 'h', 'j']):     'nella',
    frozenset(['j', 'k', 'l']):     'sono',
    frozenset(['a', 'd', 'f']):     'una',
    frozenset(['d', 'g', 'k']):     'questo',
    frozenset(['f', 'h', 'l']):     'tutto',
    frozenset(['g', 'j', 'k']):     'anche',
    frozenset(['a', 'f', 'j']):     'più',
    frozenset(['d', 'f', 'h']):     'come',
    frozenset(['s', 'g', 'l']):     'così',
    frozenset(['a', 'h', 'l']):     'dopo',
    frozenset(['d', 'j', 'k']):     'loro',
    frozenset(['f', 'g', 'j']):     'ogni',
    frozenset(['h', 'k', 'l']):     'prima',
    frozenset(['a', 's', 'j']):     'fare',
    frozenset(['d', 'f', 'k']):     'dove',
    frozenset(['g', 'h', 'l']):     'mentre',
    frozenset(['a', 'k', 'l']):     'quando',
}

# mappa inversa: parola → chord keys
CHORD_FOR_WORD: dict[str, frozenset] = {v: k for k, v in STENO_CHORDS.items()}

# ─── Esercizi preconfezionati ─────────────────────────────────────────────────
STENO_EXERCISES = [
    ['il', 'la', 'un', 'una', 'di', 'in', 'che', 'non', 'per', 'con'],
    ['al', 'si', 'lo', 'le', 'ma', 'su', 'tra', 'del', 'ha', 'più'],
    ['alla', 'nella', 'sono', 'questo', 'tutto', 'anche', 'come', 'così', 'il', 'la'],
    ['un', 'la', 'e', 'a', 'di', 'che', 'non', 'per', 'anche', 'tutto'],
    ['dopo', 'loro', 'ogni', 'prima', 'fare', 'dove', 'mentre', 'quando', 'il', 'la'],
    ['gli', 'ci', 'con', 'del', 'tra', 'su', 'ma', 'in', 'per', 'non'],
]

_KEY_LABEL = {
    'a': 'A', 's': 'S', 'd': 'D', 'f': 'F', 'g': 'G',
    'h': 'H', 'j': 'J', 'k': 'K', 'l': 'L', ' ': '▁SPC',
}


def _chord_str(keys: frozenset) -> str:
    order = {k: i for i, k in enumerate(STENO_KEYS)}
    sorted_keys = sorted(keys, key=lambda k: order.get(k, 99))
    return " + ".join(_KEY_LABEL.get(k, k.upper()) for k in sorted_keys)


class StenoFrame(ctk.CTkFrame):
    """Schermata della modalità stenografica a 10 tasti."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.app = master
        self.finger_colors = get_finger_colors(self.app.colorblind)

        self.exercise   = random.choice(STENO_EXERCISES)
        self.word_index = 0
        self.correct    = 0
        self.wrong      = 0
        self.start_time: float | None = None
        self.finished   = False

        # chord tracking: tasti attualmente premuti / tasti del chord in corso
        self._pressed: set[str] = set()
        self._chord:   set[str] = set()

        self._build()
        self._show_target()

        # Bind globale sulla finestra root per catturare i tasti senza entry
        self.app.bind('<KeyPress>',   self._on_press)
        self.app.bind('<KeyRelease>', self._on_release)

    def destroy(self):
        """Rimuove i binding globali prima di distruggersi."""
        try:
            self.app.unbind('<KeyPress>')
            self.app.unbind('<KeyRelease>')
        except Exception:
            pass
        super().destroy()

    # ─── Costruzione interfaccia ──────────────────────────────────────────────

    def _build(self):
        self._build_header()
        self._build_progress()
        self._build_target_area()
        self._build_steno_keyboard()
        self._build_stats_bar()
        self._build_chord_reference()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(18, 0))
        ctk.CTkButton(hdr, text="<- Home", width=80, command=self.app.show_home).pack(side="left")
        ctk.CTkLabel(
            hdr, text="Modalità Stenografica  ·  10 tasti",
            font=ctk.CTkFont(size=13),
        ).pack(side="left", padx=18)
        ctk.CTkButton(
            hdr, text="Nuovo esercizio", width=120, height=28,
            font=ctk.CTkFont(size=11),
            command=self.app.show_steno,
        ).pack(side="right")

    def _build_progress(self):
        self.progress_var = ctk.StringVar(value="0 / 10")
        ctk.CTkLabel(
            self, textvariable=self.progress_var,
            font=ctk.CTkFont(size=12), text_color="gray",
        ).pack(pady=(8, 0))

    def _build_target_area(self):
        ctk.CTkLabel(
            self, text="Premi il chord per:",
            font=ctk.CTkFont(size=13), text_color="gray",
        ).pack(pady=(16, 2))

        self.target_label = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=58, weight="bold"),
        )
        self.target_label.pack(pady=(0, 4))

        self.chord_hint = ctk.CTkLabel(
            self, text="",
            font=ctk.CTkFont(size=14), text_color="gray",
        )
        self.chord_hint.pack(pady=(0, 6))

        self.feedback_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16))
        self.feedback_label.pack(pady=(0, 6))

    def _build_steno_keyboard(self):
        ctk.CTkLabel(
            self, text="Tastiera stenografica (10 tasti — home row + spazio)",
            font=ctk.CTkFont(size=11), text_color="gray",
        ).pack(pady=(0, 3))

        card = ctk.CTkFrame(self, fg_color=("#c8c8c8", "#1e1e2e"), corner_radius=14)
        card.pack()
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=16, pady=14)

        self.steno_btns: dict[str, ctk.CTkButton] = {}
        for key in STENO_KEYS:
            btn = ctk.CTkButton(
                inner,
                text=_KEY_LABEL[key],
                width=54 if key != ' ' else 80,
                height=54,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=("#b0b0b0", "#2a2a3e"),
                hover=False,
                corner_radius=8,
                text_color=("gray20", "gray80"),
            )
            btn.pack(side="left", padx=3)
            self.steno_btns[key] = btn

    def _build_stats_bar(self):
        sb = ctk.CTkFrame(self)
        sb.pack(fill="x", padx=80, pady=8)
        self.cpm_var = ctk.StringVar(value="0")
        self.acc_var = ctk.StringVar(value="100")
        for col, (lbl, var) in enumerate([("Chord / min", self.cpm_var), ("Precisione %", self.acc_var)]):
            card = ctk.CTkFrame(sb, fg_color=("gray85", "gray20"))
            card.grid(row=0, column=col, padx=8, pady=6, sticky="nsew")
            sb.columnconfigure(col, weight=1)
            ctk.CTkLabel(card, textvariable=var, font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(8, 0))
            ctk.CTkLabel(card, text=lbl, font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 8))

    def _build_chord_reference(self):
        """Griglia compatta chord → parola per tutte le voci del dizionario."""
        ctk.CTkLabel(
            self, text="Dizionario chord",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(pady=(8, 4))

        ref = ctk.CTkFrame(self, fg_color="transparent")
        ref.pack(padx=20, pady=(0, 16))

        entries = sorted(CHORD_FOR_WORD.items(), key=lambda x: (len(x[1]), x[0]))
        cols = 6
        for i, (word, keys) in enumerate(entries):
            cell = ctk.CTkFrame(ref, fg_color=("gray88", "gray18"), corner_radius=5)
            cell.grid(row=i // cols, column=i % cols, padx=3, pady=2, sticky="nsew")
            ref.columnconfigure(i % cols, weight=1)
            ctk.CTkLabel(cell, text=word, font=ctk.CTkFont(size=11, weight="bold")).pack(padx=6, pady=(3, 0))
            ctk.CTkLabel(
                cell, text=_chord_str(keys),
                font=ctk.CTkFont(size=8), text_color="gray",
            ).pack(padx=6, pady=(0, 3))

    # ─── Logica chord ─────────────────────────────────────────────────────────

    def _show_target(self):
        if self.word_index >= len(self.exercise):
            self._finish()
            return
        word = self.exercise[self.word_index]
        self.target_label.configure(text=word, text_color=("gray10", "gray95"))
        chord = CHORD_FOR_WORD.get(word, frozenset())
        self.chord_hint.configure(text=f"Chord: {_chord_str(chord)}")
        self.progress_var.set(f"{self.word_index} / {len(self.exercise)}")
        self.feedback_label.configure(text="")
        self._reset_keyboard()
        self._highlight_keys(chord, "#3498db")

    def _reset_keyboard(self):
        for btn in self.steno_btns.values():
            btn.configure(fg_color=("#b0b0b0", "#2a2a3e"), text_color=("gray20", "gray80"))

    def _highlight_keys(self, keys: frozenset, color: str):
        for k in keys:
            if k in self.steno_btns:
                self.steno_btns[k].configure(fg_color=color, text_color="white")

    def _on_press(self, event):
        if self.finished:
            return
        key = event.char.lower() if event.char else ''
        if event.keysym == 'Escape':
            self.app.show_home()
            return
        if key not in STENO_KEYS:
            return
        if not self.start_time:
            self.start_time = time.time()
        self._pressed.add(key)
        self._chord.add(key)
        self.steno_btns[key].configure(fg_color="#27ae60", text_color="white")

    def _on_release(self, event):
        if self.finished:
            return
        key = event.char.lower() if event.char else ''
        if key in STENO_KEYS:
            self._pressed.discard(key)
        if not self._pressed and self._chord:
            self._resolve_chord()

    def _resolve_chord(self):
        chord = frozenset(self._chord)
        self._chord.clear()

        target_word  = self.exercise[self.word_index]
        target_chord = CHORD_FOR_WORD.get(target_word, frozenset())

        if chord == target_chord:
            self.correct += 1
            self.feedback_label.configure(text="✓ Corretto!", text_color="#27ae60")
            self.word_index += 1
            self._update_stats()
            self.after(280, self._show_target)
        else:
            self.wrong += 1
            matched = STENO_CHORDS.get(chord)
            if matched:
                msg = f"✗  Chord digitato → '{matched}'"
            else:
                msg = "✗  Chord non riconosciuto"
            self.feedback_label.configure(text=msg, text_color="#e74c3c")
            self._update_stats()
            # lampeggia in rosso i tasti premuti erroneamente, poi ripristina
            self._highlight_keys(chord, "#e74c3c")
            self.after(400, lambda: (self._reset_keyboard(), self._highlight_keys(target_chord, "#3498db")))

    def _update_stats(self):
        total = self.correct + self.wrong
        if self.start_time and total:
            elapsed = max(time.time() - self.start_time, 0.1)
            self.cpm_var.set(str(int(self.correct / elapsed * 60)))
        if total:
            self.acc_var.set(str(int(self.correct / total * 100)))

    def _finish(self):
        self.finished = True
        elapsed = max(time.time() - (self.start_time or time.time()), 0.1)
        total = self.correct + self.wrong
        cpm   = int(self.correct / elapsed * 60)
        acc   = int(self.correct / max(total, 1) * 100)

        self.target_label.configure(text="Completato!", text_color="#27ae60")
        self.chord_hint.configure(text=f"Chord/min: {cpm}  ·  Precisione: {acc}%")
        self.feedback_label.configure(
            text=f"✓ {self.correct} / {total} chord corretti",
            text_color="#27ae60",
        )
        self.progress_var.set(f"{len(self.exercise)} / {len(self.exercise)}")
        self._reset_keyboard()

# "><(((º> sabusabu <º)))><"
