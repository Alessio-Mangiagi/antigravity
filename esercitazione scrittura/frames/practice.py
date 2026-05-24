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

from config import TEXTS, KEYBOARD_ROWS, FINGER_NAMES, KEY_FINGER, get_finger_colors, get_text_colors
from stats  import update_stats, save_stats


class PracticeFrame(ctk.CTkFrame):
    """Schermata principale dell'esercizio di dattilografia."""

    def __init__(self, master, difficulty: str):
        super().__init__(master, fg_color="transparent")
        self.app        = master
        self.difficulty = difficulty
        self.text       = random.choice(TEXTS[difficulty])  # testo dell'esercizio corrente
        self.typed      = ""           # stringa digitata finora dall'utente
        self.start_time = None         # timestamp del primo tasto premuto
        self.timer_running = False     # controlla il loop del timer
        self.finished   = False        # blocca input dopo completamento

        # Palette colori attiva (normale o daltonismo) — letta una volta sola al costruttore
        self.finger_colors = get_finger_colors(self.app.colorblind)
        self.text_colors   = get_text_colors(self.app.colorblind)

        self._build()
        self._refresh_text()           # mostra il testo da digitare all'avvio
        self._highlight_next_key()     # evidenzia subito il primo tasto

    # ─── Costruzione interfaccia ──────────────────────────────────────────────

    def _build(self):
        self._build_header()
        self._build_stats_bar()
        self._build_text_display()
        self._build_entry()
        self._build_progress_bar()
        kb_area = ctk.CTkFrame(self, fg_color="transparent")
        kb_area.pack()
        self._build_keyboard(kb_area)
        self._build_finger_legend(kb_area)
        self._build_hint_label()
        self._build_restart_button()

    def _build_header(self):
        """Riga in cima: pulsante Home + etichetta difficoltà."""
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(18, 0))
        ctk.CTkButton(
            hdr, text="<- Home", width=80,
            fg_color="transparent", border_width=1,
            command=self.app.show_home,
        ).pack(side="left")
        ctk.CTkLabel(hdr, text=f"Difficolta: {self.difficulty}", font=ctk.CTkFont(size=13)).pack(side="left", padx=18)
        # Pulsante README accessibile anche durante l'esercizio
        ctk.CTkButton(
            hdr, text="? README", width=90, height=28,
            fg_color="transparent", border_width=1,
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
        self.entry.focus()

    def _build_progress_bar(self):
        """Barra orizzontale che mostra la percentuale di testo completata."""
        self.progress = ctk.CTkProgressBar(self, height=8)
        self.progress.pack(fill="x", padx=28, pady=4)
        self.progress.set(0)

    def _build_keyboard(self, parent):
        """Tastiera QWERTY visiva 3 righe + barra spazio.
        Ogni tasto mostra il colore del dito assegnato come colore del testo.
        Il tasto successivo da premere viene evidenziato con lo sfondo colorato."""
        kb = ctk.CTkFrame(parent, fg_color="transparent")
        kb.pack(side="left", pady=4, padx=(0, 20))
        self.key_btns: dict[str, ctk.CTkButton] = {}

        # Offset orizzontale delle righe per simulare il layout reale della tastiera
        offsets = [0, 14, 28]
        for r, row in enumerate(KEYBOARD_ROWS):
            row_frame = ctk.CTkFrame(kb, fg_color="transparent")
            row_frame.pack()
            if offsets[r]:
                ctk.CTkFrame(row_frame, width=offsets[r], fg_color="transparent").pack(side="left")
            for key in row:
                color = self.finger_colors[KEY_FINGER.get(key, "indice_dx")]
                btn = ctk.CTkButton(
                    row_frame, text=key.upper(),
                    width=40, height=40,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color=("gray72", "gray28"),   # sfondo neutro di default
                    hover=False, corner_radius=5,
                    text_color=color,                # lettera colorata per dito
                )
                btn.pack(side="left", padx=2, pady=2)
                self.key_btns[key] = btn

        # Barra spazio (più larga, assegnata ai pollici)
        sf = ctk.CTkFrame(kb, fg_color="transparent")
        sf.pack()
        ctk.CTkFrame(sf, width=60, fg_color="transparent").pack(side="left")
        sp = ctk.CTkButton(
            sf, text="SPAZIO",
            width=270, height=40,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=("gray72", "gray28"),
            hover=False, corner_radius=5,
            text_color=self.finger_colors["pollice"],
        )
        sp.pack(side="left", padx=2, pady=2)
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
            ("mignolo_dx", "P"),
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
        ctk.CTkButton(
            self, text="Nuovo testo",
            command=lambda: self.app.show_practice(self.difficulty),
            width=130, fg_color="transparent", border_width=1,
        ).pack(pady=6)

    # ─── Logica di gioco ──────────────────────────────────────────────────────

    def _on_key(self, event):
        """Chiamata ad ogni rilascio di tasto. Aggiorna tutto il display e controlla il completamento."""
        if self.finished:
            return

        typed = self.entry_var.get()

        # Avvia il timer al primo carattere digitato
        if not self.start_time and typed:
            self.start_time = time.time()
            self.timer_running = True
            self._tick()

        self.typed = typed
        self._refresh_text()
        self._update_stats()
        self._highlight_next_key()

        # L'esercizio è completato quando si raggiunge la lunghezza del testo
        if len(typed) >= len(self.text):
            self._finish()

    def _refresh_text(self):
        """Ridisegna il widget tk.Text applicando i tag colore a ogni carattere."""
        typed = self.typed
        text  = self.text
        self.txt.config(state="normal")
        self.txt.delete("1.0", "end")
        for i, ch in enumerate(text):
            if i < len(typed):
                tag = "correct" if typed[i] == ch else "wrong"
            elif i == len(typed):
                tag = "cursor"    # posizione corrente del cursore
            else:
                finger = KEY_FINGER.get(ch.lower(), "indice_dx")
                tag = f"finger_{finger}"
            self.txt.insert("end", ch, tag)
        self.txt.config(state="disabled")
        self.progress.set(min(len(typed) / len(text), 1.0) if text else 0)

    def _update_stats(self):
        """Aggiorna WPM e precisione nella barra statistiche in tempo reale.
        WPM usa la formula standard: (caratteri / 5) / minuti."""
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
        # Reset sfondo di tutti i tasti
        for key, btn in self.key_btns.items():
            color = self.finger_colors[KEY_FINGER.get(key, "indice_dx")]
            btn.configure(fg_color=("gray72", "gray28"), text_color=color)

        # Evidenzia il tasto successivo con sfondo pieno del colore del dito
        pos = len(self.typed)
        if pos < len(self.text):
            next_key = self.text[pos].lower()
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
        correct = sum(a == b for a, b in zip(self.typed, self.text))
        acc     = int(correct / len(self.text) * 100)

        # Salva le statistiche aggiornate su disco
        update_stats(self.app.stats, wpm, len(self.text))
        save_stats(self.app.stats)

        # Piccolo ritardo prima di navigare per dare feedback visivo
        self.after(300, lambda: self.app.show_result(wpm, acc, self.difficulty))
