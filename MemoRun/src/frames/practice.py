# =============================================================================
# frames/practice.py — Schermata di esercitazione (PracticeFrame)
# Mostra:
#   • Header con pulsante home e difficoltà corrente
#   • Barra statistiche real-time: WPM, Precisione, Tempo
#   • Widget tk.Text con feedback carattere per carattere (verde/rosso/blu)
#   • Campo di input dove l'utente digita
#   • Barra di avanzamento
#   • Tastiera visiva QWERTY con evidenziazione del tasto successivo
#   • Label con il nome del dito da usare
# =============================================================================

import time
import random
import customtkinter as ctk
import tkinter as tk

from ..config import TEXTS, KEYBOARD_ROWS, FINGER_NAMES, KEY_FINGER, get_finger_colors, get_text_colors
from ..stats  import update_stats, save_stats


class PracticeFrame(ctk.CTkFrame):
    """Schermata principale dell'esercizio di dattilografia."""

    def __init__(self, master, difficulty: str, custom_text: str = "", word_by_word: bool = False):
        super().__init__(master, fg_color="transparent")
        self.app          = master
        self.difficulty   = difficulty
        self.text         = custom_text if custom_text else random.choice(TEXTS[difficulty])
        self.typed        = ""
        self.start_time   = None
        self.timer_running = False
        self.finished     = False

        self.word_by_word = word_by_word
        if word_by_word:
            self.words      = self.text.split()
            self.word_index = 0
            self.all_typed  = ""   # accumula tutto il testo digitato (parole completate)

        self.finger_colors = get_finger_colors(self.app.colorblind)
        self.text_colors   = get_text_colors(self.app.colorblind)

        self._build()
        self._refresh_text()
        self._highlight_next_key()

    # ─── Costruzione interfaccia ──────────────────────────────────────────────

    def _build(self):
        self._build_header()
        self._build_stats_bar()
        if self.word_by_word:
            self._build_word_counter()
        self._build_text_display()
        self._build_entry()
        self._build_progress_bar()
        kb_area = ctk.CTkFrame(self, fg_color="transparent")
        kb_area.pack()
        self._build_keyboard(kb_area)
        self._build_finger_legend(kb_area)
        self._build_hint_label()
        self._build_restart_button()

    def _build_word_counter(self):
        self.word_counter_var = ctk.StringVar(value=f"Parola 1 / {len(self.words)}")
        ctk.CTkLabel(
            self, textvariable=self.word_counter_var,
            font=ctk.CTkFont(size=13), text_color="gray",
        ).pack(pady=(2, 0))

    def _update_word_counter(self):
        idx = min(self.word_index + 1, len(self.words))
        self.word_counter_var.set(f"Parola {idx} / {len(self.words)}")

    def _build_header(self):
        """Riga in cima: pulsante Home + etichetta difficoltà."""
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(18, 0))
        ctk.CTkButton(
            hdr, text="<- Home", width=80,
            command=self.app.show_home,
        ).pack(side="left")
        ctk.CTkLabel(hdr, text=f"Difficoltà: {self.difficulty}", font=ctk.CTkFont(size=13)).pack(side="left", padx=18)
        ctk.CTkButton(
            hdr, text="? README", width=90, height=28,
            font=ctk.CTkFont(size=11),
            command=self.app.show_readme,
        ).pack(side="right")

    def _build_stats_bar(self):
        """Tre card affiancate: WPM, Precisione %, Tempo trascorso."""
        sb = ctk.CTkFrame(self)
        sb.pack(fill="x", padx=28, pady=10)

        # StringVar aggiornate in real-time durante la digitazione
        self.wpm_var  = ctk.StringVar(value="0")
        self.acc_var  = ctk.StringVar(value="100")
        self.time_var = ctk.StringVar(value="0:00")

        for col, (lbl, var) in enumerate([
            ("WPM",         self.wpm_var),
            ("Precisione %", self.acc_var),
            ("Tempo",        self.time_var),
        ]):
            card = ctk.CTkFrame(sb, fg_color=("gray85", "gray20"))
            card.grid(row=0, column=col, padx=8, pady=8, sticky="nsew")
            sb.columnconfigure(col, weight=1)
            ctk.CTkLabel(card, textvariable=var, font=ctk.CTkFont(size=30, weight="bold")).pack(pady=(10, 0))
            ctk.CTkLabel(card, text=lbl, font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 10))

    def _build_text_display(self):
        """Widget tk.Text in sola lettura per colorare ogni carattere.
        Tag usati: 'correct' (verde), 'wrong' (rosso), 'cursor' (blu), 'pending' (grigio)."""
        container = ctk.CTkFrame(self)
        container.pack(fill="x", padx=28, pady=6)

        self.txt = tk.Text(
            container,
            font=("Courier New", 20),
            bg="#1e1e2e", fg="#cdd6f4",   # colori base tema scuro
            relief="flat", bd=0,
            height=3, wrap="word",
            state="disabled", cursor="arrow",
            padx=18, pady=16,
        )
        self.txt.pack(fill="x", padx=1, pady=1)

        # Tag colore per il feedback visivo — usa la palette attiva (normale o daltonismo)
        tc = self.text_colors
        self.txt.tag_configure("correct", foreground=tc["correct_fg"])
        self.txt.tag_configure("wrong",   foreground=tc["wrong_fg"],  background=tc["wrong_bg"])
        self.txt.tag_configure("cursor",  foreground=tc["cursor_fg"], background=tc["cursor_bg"])
        self.txt.tag_configure("pending", foreground=tc["pending_fg"])
        for finger, color in self.finger_colors.items():
            self.txt.tag_configure(f"finger_{finger}", foreground=color)

    def _build_entry(self):
        """Campo di testo dove l'utente digita. Ogni rilascio tasto aggiorna il display."""
        self.entry_var = ctk.StringVar()
        self.entry = ctk.CTkEntry(
            self, textvariable=self.entry_var,
            font=ctk.CTkFont(size=17), height=48,
            placeholder_text="Inizia a digitare qui...",
        )
        self.entry.pack(fill="x", padx=28, pady=4)
        self.entry.bind("<KeyRelease>", self._on_key)
        self.entry.bind("<BackSpace>", lambda e: "break")
        self.entry.bind("<Delete>",    lambda e: "break")
        self.entry.bind("<Escape>",    lambda e: self.app.show_home())
        self.entry.focus()

    def _build_progress_bar(self):
        """Barra orizzontale che mostra la percentuale di testo completata."""
        self.progress = ctk.CTkProgressBar(self, height=8)
        self.progress.pack(fill="x", padx=28, pady=4)
        self.progress.set(0)

    def _build_keyboard(self, parent):
        """Tastiera QWERTY visiva 3 righe + barra spazio dentro card arrotondata."""
        # Card contenitore con sfondo scuro e bordi arrotondati
        card = ctk.CTkFrame(
            parent,
            fg_color=("#c8c8c8", "#1e1e2e"),
            corner_radius=16,
        )
        card.pack(side="left", pady=4, padx=(0, 20))

        kb = ctk.CTkFrame(card, fg_color="transparent")
        kb.pack(padx=14, pady=14)
        self.key_btns: dict[str, ctk.CTkButton] = {}

        offsets = [0, 14, 28, 120]  # 120 = centra 5 tasti accentati sotto 10 tasti
        for r, row in enumerate(KEYBOARD_ROWS):
            if r == 3:
                ctk.CTkFrame(kb, height=4, fg_color="transparent").pack()
            row_frame = ctk.CTkFrame(kb, fg_color="transparent")
            row_frame.pack()
            if offsets[r]:
                ctk.CTkFrame(row_frame, width=offsets[r], fg_color="transparent").pack(side="left")
            for key in row:
                color = self.finger_colors[KEY_FINGER.get(key, "indice_dx")]
                btn = ctk.CTkButton(
                    row_frame, text=key.upper(),
                    width=42, height=42,
                    font=ctk.CTkFont(size=13, weight="bold"),
                    fg_color=("#b0b0b0", "#2a2a3e"),
                    hover=False, corner_radius=8,
                    text_color=color,
                )
                btn.pack(side="left", padx=3, pady=3)
                self.key_btns[key] = btn

        # Barra spazio
        sf = ctk.CTkFrame(kb, fg_color="transparent")
        sf.pack()
        ctk.CTkFrame(sf, width=60, fg_color="transparent").pack(side="left")
        sp = ctk.CTkButton(
            sf, text="SPAZIO",
            width=290, height=42,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#b0b0b0", "#2a2a3e"),
            hover=False, corner_radius=8,
            text_color=self.finger_colors["pollice"],
        )
        sp.pack(side="left", padx=3, pady=3)
        self.key_btns[" "] = sp

    def _build_hint_label(self):
        """Label che mostra il nome del dito da usare per il prossimo tasto."""
        self.hint_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13))
        self.hint_label.pack(pady=3)

    def _build_finger_legend(self, parent):
        """Griglia 2×4 con colori e nomi dita — spiega la codifica colore del testo."""
        wrapper = ctk.CTkFrame(parent, fg_color="transparent")
        wrapper.pack(side="left", anchor="n", pady=4)

        ctk.CTkLabel(
            wrapper, text="Legenda dita",
            font=ctk.CTkFont(size=11), text_color="gray",
        ).pack(pady=(0, 4))

        grid = ctk.CTkFrame(wrapper, fg_color="transparent")
        grid.pack()

        finger_keys = [
            ("mignolo_sx", "Q  A  Z"),
            ("anulare_sx", "W  S  X"),
            ("medio_sx",   "E  D  C"),
            ("indice_sx",  "R F V  T G B"),
            ("indice_dx",  "Y H N  U J M"),
            ("medio_dx",   "I  K"),
            ("anulare_dx", "O  L"),
            ("mignolo_dx", "P  à è ì ò ù"),
        ]
        for i, (finger, keys) in enumerate(finger_keys):
            color = self.finger_colors[finger]
            name  = FINGER_NAMES[finger]
            box = ctk.CTkFrame(grid, fg_color=color, corner_radius=5)
            box.grid(row=i // 4, column=i % 4, padx=3, pady=2, sticky="nsew")
            grid.columnconfigure(i % 4, weight=1)
            ctk.CTkLabel(box, text=name, font=ctk.CTkFont(size=9, weight="bold"), text_color="white").pack(padx=6, pady=(4, 0))
            ctk.CTkLabel(box, text=keys, font=ctk.CTkFont(size=9), text_color="white").pack(padx=6, pady=(0, 4))

    def _build_restart_button(self):
        """Pulsante per caricare un nuovo testo della stessa difficoltà."""
        if self.difficulty == "Personalizzato":
            cmd = self.app.show_custom_text
        else:
            cmd = lambda: self.app.show_practice(self.difficulty)
        ctk.CTkButton(
            self, text="Nuovo testo",
            command=cmd, width=130,
        ).pack(pady=6)

    # ─── Logica di gioco ──────────────────────────────────────────────────────

    def _on_key(self, event):
        """Chiamata ad ogni rilascio di tasto. Aggiorna tutto il display e controlla il completamento."""
        if self.finished:
            return

        typed = self.entry_var.get()

        if not self.start_time and typed:
            self.start_time = time.time()
            self.timer_running = True
            self._tick()

        if self.word_by_word:
            current_word = self.words[self.word_index]
            is_last = self.word_index == len(self.words) - 1

            if typed.endswith(" "):
                # Avanza alla parola successiva quando si preme spazio
                self.all_typed += typed[:-1] + " "
                if is_last:
                    self._finish()
                    return
                self.word_index += 1
                self.entry_var.set("")
                self._update_word_counter()
            elif is_last and len(typed) >= len(current_word):
                # Ultima parola completata senza spazio
                self.all_typed += typed
                self._finish()
                return

            self._refresh_text()
            self._update_stats()
            self._highlight_next_key()
            return

        self.typed = typed
        self._refresh_text()
        self._update_stats()
        self._highlight_next_key()

        if len(typed) >= len(self.text):
            self._finish()

    def _refresh_text(self):
        """Ridisegna il widget tk.Text applicando i tag colore a ogni carattere."""
        if self.word_by_word:
            word  = self.words[self.word_index] if self.word_index < len(self.words) else ""
            typed = self.entry_var.get().rstrip(" ")
            self.txt.config(state="normal")
            self.txt.delete("1.0", "end")
            for i, ch in enumerate(word):
                if i < len(typed):
                    tag = "correct" if typed[i] == ch else "wrong"
                elif i == len(typed):
                    tag = "cursor"
                else:
                    finger = KEY_FINGER.get(ch.lower(), "indice_dx")
                    tag = f"finger_{finger}"
                self.txt.insert("end", ch, tag)
            self.txt.config(state="disabled")
            self.progress.set(self.word_index / len(self.words) if self.words else 0)
            return

        typed = self.typed
        text  = self.text
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        for i, ch in enumerate(text):
            if i < len(typed):
                tag = "correct" if typed[i] == ch else "wrong"
            elif i == len(typed):
                tag = "cursor"
            else:
                finger = KEY_FINGER.get(ch.lower(), "indice_dx")
                tag = f"finger_{finger}"
            self.txt.insert("end", ch, tag)
        self.txt.config(state="disabled")
        self.progress.set(min(len(typed) / len(text), 1.0) if text else 0)

    def _update_stats(self):
        """Aggiorna WPM e precisione nella barra statistiche in tempo reale.
        WPM usa la formula standard: (caratteri / 5) / minuti."""
        if self.word_by_word:
            total = self.all_typed + self.entry_var.get()
            if self.start_time and total:
                elapsed = max(time.time() - self.start_time, 0.1)
                self.wpm_var.set(str(int((len(total) / 5) / elapsed * 60)))
            if total:
                correct = sum(a == b for a, b in zip(total, self.text))
                self.acc_var.set(str(int(correct / len(total) * 100)))
            return

        typed = self.typed
        text  = self.text
        if self.start_time and typed:
            elapsed = max(time.time() - self.start_time, 0.1)
            wpm = int((len(typed) / 5) / elapsed * 60)
            self.wpm_var.set(str(wpm))
        if typed:
            correct = sum(a == b for a, b in zip(typed, text))
            self.acc_var.set(str(int(correct / len(typed) * 100)))

    def _highlight_next_key(self):
        """Evidenzia sulla tastiera visiva il prossimo tasto da premere.
        Tutti gli altri tasti tornano allo sfondo neutro."""
        for key, btn in self.key_btns.items():
            color = self.finger_colors[KEY_FINGER.get(key, "indice_dx")]
            btn.configure(fg_color=("gray72", "gray28"), text_color=color)

        if self.word_by_word:
            word = self.words[self.word_index] if self.word_index < len(self.words) else ""
            pos  = len(self.entry_var.get().rstrip(" "))
        else:
            word = self.text
            pos  = len(self.typed)

        if pos < len(word):
            next_key = word[pos].lower()
            if next_key in self.key_btns:
                finger = KEY_FINGER.get(next_key, "indice_dx")
                color  = self.finger_colors[finger]
                self.key_btns[next_key].configure(fg_color=color, text_color="white")
                self.hint_label.configure(
                    text=f"Dito: {FINGER_NAMES.get(finger, finger)}",
                    text_color=color,
                )

    def _tick(self):
        """Loop ricorsivo che aggiorna il timer ogni 500 ms."""
        if not self.timer_running:
            return
        elapsed = int(time.time() - self.start_time)
        m, s = divmod(elapsed, 60)
        self.time_var.set(f"{m}:{s:02d}")
        self.after(500, self._tick)

    def _finish(self):
        """Calcola i risultati finali, aggiorna le statistiche e naviga alla schermata risultati."""
        self.finished      = True
        self.timer_running = False

        elapsed = max(time.time() - self.start_time, 0.1)
        wpm     = int((len(self.text) / 5) / elapsed * 60)

        if self.word_by_word:
            full_typed = self.all_typed
            correct = sum(a == b for a, b in zip(full_typed, self.text))
            acc = int(correct / max(len(full_typed), 1) * 100)
        else:
            correct = sum(a == b for a, b in zip(self.typed, self.text))
            acc = int(correct / len(self.text) * 100)

        update_stats(self.app.stats, wpm, len(self.text))
        save_stats(self.app.stats)

        self.after(300, lambda: self.app.show_result(wpm, acc, self.difficulty, self.text))
