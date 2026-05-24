# =============================================================================
# app.py — Finestra principale dell'applicazione (TypingApp)
# Responsabilità:
#   • Inizializza la finestra CustomTkinter
#   • Carica le statistiche utente all'avvio
#   • Gestisce la navigazione tra le schermate (Home → Practice → Result)
# Per aggiungere una nuova schermata: aggiungi un metodo show_* e importa il Frame.
# =============================================================================

import customtkinter as ctk
from stats    import load_stats
from settings import load_settings
from frames   import HomeFrame, PracticeFrame, ResultFrame, ReadmeFrame

# Tema globale dell'applicazione (dark + accent blue)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class TypingApp(ctk.CTk):
    """Finestra root che funge da controller di navigazione tra le schermate."""

    def __init__(self):
        super().__init__()
        self.title("Dattilografia 10 Dita")
        self.geometry("1050x780")
        self.resizable(False, False)

        # Statistiche caricate dal file JSON e condivise con tutte le schermate
        self.stats    = load_stats()
        # Preferenze utente (daltonismo, ecc.) separate dalle statistiche
        self.settings = load_settings()

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

    def show_readme(self):
        """Apre il visualizzatore README in-app."""
        self._switch(ReadmeFrame(self))

    def _switch(self, frame: ctk.CTkFrame):
        """Rimuove la schermata corrente e sostituisce con quella nuova."""
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        self.current_frame.pack(fill="both", expand=True)

    @property
    def colorblind(self) -> bool:
        """Scorciatoia per leggere la modalità daltonismo dalle impostazioni."""
        return self.settings.get("colorblind_mode", False)
