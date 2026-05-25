# =============================================================================
# app.py — Finestra principale dell'applicazione (TypingApp)
# Responsabilità:
#   • Inizializza la finestra CustomTkinter
#   • Carica le statistiche utente all'avvio
#   • Gestisce la navigazione tra le schermate (Home → Practice → Result)
# Per aggiungere una nuova schermata: aggiungi un metodo show_* e importa il Frame.
# =============================================================================

import customtkinter as ctk
from .stats    import load_stats
from .settings import load_settings, save_settings
from .frames   import HomeFrame, PracticeFrame, ResultFrame, ReadmeFrame, CustomTextFrame

ctk.set_default_color_theme("blue")


class TypingApp(ctk.CTk):
    """Finestra root che funge da controller di navigazione tra le schermate."""

    def __init__(self):
        super().__init__()
        self.title("Memorun")
        self.geometry("1050x780")
        self.minsize(900, 700)
        self.resizable(True, True)

        self.stats    = load_stats()
        self.settings = load_settings()

        ctk.set_appearance_mode(self.settings.get("theme", "System"))
        self._update_bg()

        # Riferimento alla schermata attualmente visualizzata
        self.current_frame: ctk.CTkFrame | None = None

        self.show_home()

    # ─── Navigazione ──────────────────────────────────────────────────────────

    def show_home(self):
        """Mostra la schermata iniziale con statistiche e selezione difficoltà."""
        self._switch(HomeFrame(self))

    def show_practice(self, difficulty: str):
        """Avvia un esercizio con la difficoltà specificata ('Facile'/'Medio'/'Difficile')."""
        self._switch(PracticeFrame(self, difficulty))

    def show_result(self, wpm: int, accuracy: int, difficulty: str):
        """Mostra i risultati dopo il completamento di un esercizio."""
        self._switch(ResultFrame(self, wpm, accuracy, difficulty))

    def show_custom_text(self):
        """Mostra la schermata per inserire un testo personalizzato."""
        self._switch(CustomTextFrame(self))

    def show_practice_custom(self, text: str, word_by_word: bool = False):
        """Avvia un esercizio con testo personalizzato."""
        self._switch(PracticeFrame(self, "Personalizzato", custom_text=text, word_by_word=word_by_word))

    def show_readme(self):
        """Apre il visualizzatore README in-app."""
        self._switch(ReadmeFrame(self))

    def _switch(self, frame: ctk.CTkFrame):
        """Rimuove la schermata corrente e sostituisce con quella nuova."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    _BG = {"Light": "#cce8f4", "Dark": "#000000"}

    def apply_theme(self, mode: str):
        self.settings["theme"] = mode
        save_settings(self.settings)
        ctk.set_appearance_mode(mode)
        self._update_bg()
        self.show_home()

    def _update_bg(self):
        resolved = ctk.get_appearance_mode()   # "Light" o "Dark" (risolve System)
        color = self._BG.get(resolved)
        if color:
            self.configure(fg_color=color)

    @property
    def colorblind(self) -> bool:
        return self.settings.get("colorblind_mode", False)

    @property
    def theme(self) -> str:
        return self.settings.get("theme", "System")
