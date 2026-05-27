# =============================================================================
# frames/result.py — Schermata risultati (ResultFrame)
# Mostra al termine di ogni esercizio:
#   • WPM e precisione con colori (rosso/arancione/verde) in base alla soglia
#   • Badge "Nuovo record" se il WPM supera il record precedente
#   • Messaggio motivazionale personalizzato
#   • Pulsanti Riprova / Cambia difficoltà
#   • Reminder visivo sulla home row (tasti A S D F  J K L colorati per dito)
# =============================================================================

import random
import customtkinter as ctk
from ..config import get_finger_colors, TEXTS


class ResultFrame(ctk.CTkFrame):
    """Schermata mostrata al completamento di un esercizio."""

    _WPM_POOR   = 20
    _WPM_MEDIUM = 40
    _ACC_POOR   = 80
    _ACC_MEDIUM = 95

    def __init__(self, master, wpm: int, accuracy: int, difficulty: str, current_text: str = ""):
        super().__init__(master, fg_color="transparent")
        self.app          = master
        self.wpm          = wpm
        self.accuracy     = accuracy
        self.difficulty   = difficulty
        self.current_text = current_text
        self.finger_colors = get_finger_colors(self.app.colorblind)
        self._build()

    # ─── Costruzione interfaccia ──────────────────────────────────────────────

    def _build(self):
        self._build_title()
        self._build_result_cards()
        self._build_record_badge()
        self._build_message()
        self._build_action_buttons()
        self._build_home_row_reminder()
        self._build_readme_button()

    def _build_title(self):
        """Titolo celebrativo in cima alla schermata."""
        ctk.CTkLabel(
            self, text="Esercizio completato!",
            font=ctk.CTkFont(size=30, weight="bold"),
        ).pack(pady=(55, 26))

    def _build_result_cards(self):
        """Due card grandi con WPM e Precisione, colorate in base alla soglia."""
        wpm_color = self._wpm_color(self.wpm)
        acc_color = self._acc_color(self.accuracy)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=10)

        cards = [
            ("Velocità",   str(self.wpm),      "WPM", wpm_color),
            ("Precisione", str(self.accuracy),  "%",   acc_color),
        ]
        for col, (lbl, val, unit, color) in enumerate(cards):
            card = ctk.CTkFrame(container, fg_color=("gray85", "gray20"), width=210)
            card.grid(row=0, column=col, padx=22, sticky="nsew")
            ctk.CTkLabel(card, text=val,  font=ctk.CTkFont(size=54, weight="bold"), text_color=color).pack(pady=(22, 0))
            ctk.CTkLabel(card, text=unit, font=ctk.CTkFont(size=16), text_color=color).pack()
            ctk.CTkLabel(card, text=lbl,  font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 22))

    def _build_record_badge(self):
        """Badge giallo visibile solo se il WPM attuale è il nuovo record personale."""
        if self.app.stats["sessions"] > 1 and self.wpm >= self.app.stats["best_wpm"]:
            ctk.CTkLabel(
                self, text="Nuovo record personale!",
                font=ctk.CTkFont(size=17, weight="bold"),
                text_color="#f1c40f",
            ).pack(pady=8)

    def _build_message(self):
        """Messaggio motivazionale scelto in base a WPM e precisione."""
        ctk.CTkLabel(
            self, text=self._message(),
            font=ctk.CTkFont(size=14),
            wraplength=520, justify="center",
        ).pack(pady=16)

    def _build_action_buttons(self):
        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.pack(pady=26)
        ctk.CTkButton(
            bf, text="Riprova",
            command=lambda: self.app.show_practice(self.difficulty, self.current_text),
            width=160, height=44, font=ctk.CTkFont(size=14),
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            bf, text="Cambia frase",
            command=self._new_random_text,
            width=160, height=44, font=ctk.CTkFont(size=14),
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            bf, text="Cambia difficoltà",
            command=self.app.show_home,
            width=160, height=44, font=ctk.CTkFont(size=14),
            fg_color=("gray70", "gray30"),
        ).pack(side="left", padx=10)

    def _new_random_text(self):
        if self.difficulty == "Personalizzato":
            self.app.show_custom_text()
            return
        pool = TEXTS.get(self.difficulty, [])
        candidates = [t for t in pool if t != self.current_text]
        new_text = random.choice(candidates) if candidates else random.choice(pool)
        self.app.show_practice(self.difficulty, new_text)

    def _build_home_row_reminder(self):
        """Reminder visivo dei 7 tasti della home row colorati per dito,
        per ricordare all'utente la posizione di riposo delle dita."""
        ctk.CTkLabel(
            self,
            text="Ricorda: tieni le dita sulle home row  (A S D F  J K L)",
            font=ctk.CTkFont(size=12), text_color="gray",
        ).pack(pady=(20, 0))

        row_frame = ctk.CTkFrame(self, fg_color="transparent")
        row_frame.pack(pady=6)

        home_row_keys = [
            ("A", "mignolo_sx"), ("S", "anulare_sx"), ("D", "medio_sx"), ("F", "indice_sx"),
            ("J", "indice_dx"),  ("K", "medio_dx"),   ("L", "anulare_dx"),
        ]
        for key, finger in home_row_keys:
            color = self.finger_colors[finger]
            ctk.CTkButton(
                row_frame, text=key, width=38, height=38,
                fg_color=color, hover=False, corner_radius=5,
                font=ctk.CTkFont(size=13, weight="bold"), text_color="white",
            ).pack(side="left", padx=3)

    def _build_readme_button(self):
        """Pulsante README accessibile anche dalla schermata risultati."""
        ctk.CTkButton(
            self, text="? README",
            width=110, height=28,
            font=ctk.CTkFont(size=11),
            command=self.app.show_readme,
        ).pack(pady=(4, 0))

    # ─── Helper privati ───────────────────────────────────────────────────────

    def _wpm_color(self, wpm: int) -> str:
        """Restituisce il colore (rosso/arancione/verde) in base al WPM."""
        if wpm < self._WPM_POOR:
            return "#e74c3c"
        if wpm < self._WPM_MEDIUM:
            return "#f39c12"
        return "#2ecc71"

    def _acc_color(self, acc: int) -> str:
        """Restituisce il colore (rosso/arancione/verde) in base alla precisione."""
        if acc < self._ACC_POOR:
            return "#e74c3c"
        if acc < self._ACC_MEDIUM:
            return "#f39c12"
        return "#2ecc71"

    def _message(self) -> str:
        """Messaggio motivazionale scelto in base a WPM e precisione raggiunti."""
        if self.accuracy < self._ACC_POOR:
            return "Concentrati sulla precisione prima della velocita. Rallenta e digita ogni carattere con cura."
        if self.wpm < self._WPM_POOR:
            return "Buon inizio! Pratica ogni giorno e la velocita aumentera naturalmente. Non guardare la tastiera!"
        if self.wpm < self._WPM_MEDIUM:
            return "Stai migliorando! Usa le dita giuste per ogni tasto e non guardare la tastiera."
        if self.wpm < 60:
            return "Ottimo risultato! Sei ad un buon livello. Continua e raggiungerai presto i 60 WPM."
        return "Eccellente! Sei un dattilografo esperto. Sfidati con testi piu difficili!"

# "><(((º> sabusabu <º)))><"
