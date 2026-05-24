# =============================================================================
# frames/home.py — Schermata iniziale (HomeFrame)
# Mostra:
#   • Titolo, sottotitolo
#   • Barra controlli: toggle Modalità Daltonismo + pulsante README (?)
#   • 4 card con le statistiche dell'utente
#   • 3 box difficoltà per avviare un esercizio
#   • Griglia legenda colori dita (si aggiorna con la modalità daltonismo)
# =============================================================================

import customtkinter as ctk
from config   import FINGER_NAMES, get_finger_colors
from settings import save_settings
from stats    import average_wpm


class HomeFrame(ctk.CTkFrame):
    """Schermata principale visualizzata all'avvio e dopo ogni esercizio."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.app = master
        # Legge la palette attiva in base alla preferenza corrente
        self.finger_colors = get_finger_colors(self.app.colorblind)
        self._build()

    # ─── Costruzione dell'interfaccia ─────────────────────────────────────────

    def _build(self):
        self._build_title()
        self._build_controls_bar()
        self._build_stats_cards()
        self._build_difficulty_buttons()
        self._build_finger_guide()

    def _build_title(self):
        """Titolo e sottotitolo centrati in cima."""
        ctk.CTkLabel(
            self, text="Dattilografia 10 Dita",
            font=ctk.CTkFont(size=34, weight="bold"),
        ).pack(pady=(30, 4))
        ctk.CTkLabel(
            self, text="Impara a scrivere velocemente con tutte e 10 le dita",
            font=ctk.CTkFont(size=13), text_color="gray",
        ).pack(pady=(0, 10))

    def _build_controls_bar(self):
        """Riga con toggle Daltonismo (sinistra) e pulsante README (destra)."""
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=40, pady=(0, 10))

        # ── Toggle modalità daltonismo ────────────────────────────────────────
        switch = ctk.CTkSwitch(
            bar,
            text="Modalita Daltonismo",
            font=ctk.CTkFont(size=12),
            command=self._toggle_colorblind,
        )
        switch.pack(side="left")
        # Imposta lo stato iniziale dello switch in base alla preferenza salvata
        if self.app.colorblind:
            switch.select()
        else:
            switch.deselect()

        # ── Badge che indica la palette attiva ───────────────────────────────
        palette_label = "Palette: Okabe-Ito" if self.app.colorblind else "Palette: standard"
        self.palette_badge = ctk.CTkLabel(
            bar, text=palette_label,
            font=ctk.CTkFont(size=11), text_color="gray",
        )
        self.palette_badge.pack(side="left", padx=14)

        # ── Pulsante README ───────────────────────────────────────────────────
        ctk.CTkButton(
            bar, text="? README",
            width=100, height=30,
            fg_color="transparent", border_width=1,
            font=ctk.CTkFont(size=12),
            command=self.app.show_readme,
        ).pack(side="right")

    def _build_stats_cards(self):
        """4 card affiancate con le statistiche cumulative dell'utente."""
        s   = self.app.stats
        avg = average_wpm(s)

        frame = ctk.CTkFrame(self)
        frame.pack(padx=50, pady=4, fill="x")

        cards = [
            (str(s["sessions"]),     "Sessioni"),
            (str(s["best_wpm"]),      "Record WPM"),
            (str(avg),                "Media WPM"),
            (f"{s['total_chars']:,}", "Caratteri totali"),
        ]
        for col, (val, lbl) in enumerate(cards):
            card = ctk.CTkFrame(frame, fg_color=("gray85", "gray20"))
            card.grid(row=0, column=col, padx=8, pady=12, sticky="nsew")
            frame.columnconfigure(col, weight=1)
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(14, 2))
            ctk.CTkLabel(card, text=lbl, font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 14))

    def _build_difficulty_buttons(self):
        """Tre box cliccabili per selezionare Facile / Medio / Difficile."""
        ctk.CTkLabel(
            self, text="Seleziona difficolta:",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(pady=(14, 8))

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack()

        difficulties = [
            ("Facile",    "#27ae60", "Parole semplici  ·  5-8 parole"),
            ("Medio",     "#f39c12", "Frasi complete  ·  8-14 parole"),
            ("Difficile", "#e74c3c", "Testi lunghi  ·  20+ parole"),
        ]
        for diff, color, desc in difficulties:
            box = ctk.CTkFrame(container, fg_color=("gray90", "gray15"))
            box.pack(side="left", padx=12, pady=6)
            ctk.CTkLabel(box, text=diff, font=ctk.CTkFont(size=17, weight="bold"), text_color=color).pack(pady=(18, 3), padx=28)
            ctk.CTkLabel(box, text=desc, font=ctk.CTkFont(size=11), text_color="gray").pack(pady=(0, 12), padx=28)
            ctk.CTkButton(
                box, text="Inizia", fg_color=color, hover_color=color,
                command=lambda d=diff: self.app.show_practice(d),
            ).pack(pady=(0, 18), padx=28)

    def _build_finger_guide(self):
        """Griglia 2×4 con palette colori aggiornata (normale o daltonismo)."""
        ctk.CTkLabel(
            self, text="Posizione delle dita",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(pady=(16, 6))

        grid = ctk.CTkFrame(self, fg_color="transparent")
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
            color = self.finger_colors[finger]   # usa la palette attiva
            name  = FINGER_NAMES[finger]
            box = ctk.CTkFrame(grid, fg_color=color, corner_radius=7)
            box.grid(row=i // 4, column=i % 4, padx=4, pady=4, sticky="nsew")
            grid.columnconfigure(i % 4, weight=1)
            ctk.CTkLabel(box, text=name, font=ctk.CTkFont(size=10, weight="bold"), text_color="white").pack(padx=10, pady=(7, 1))
            ctk.CTkLabel(box, text=keys, font=ctk.CTkFont(size=10), text_color="white").pack(padx=10, pady=(0, 7))

    # ─── Azioni ───────────────────────────────────────────────────────────────

    def _toggle_colorblind(self):
        """Inverte la modalità daltonismo, salva la preferenza e ricarica la Home."""
        self.app.settings["colorblind_mode"] = not self.app.colorblind
        save_settings(self.app.settings)
        # Ricrea la Home per aggiornare tutti i colori della guida dita
        self.app.show_home()
