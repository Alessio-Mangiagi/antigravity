# =============================================================================
# frames/readme_view.py — Visualizzatore README in-app (ReadmeFrame)
# Legge README.md dalla root del progetto e lo mostra in un widget
# tk.Text scrollabile con colori adattati al tema scuro.
# Raggiungibile tramite il pulsante "?" in Home e nel menu Practice.
# =============================================================================

import tkinter as tk
from pathlib import Path
import customtkinter as ctk

# README.md si trova due livelli sopra questo file (root del progetto)
README_PATH = Path(__file__).parent.parent / "README.md"


class ReadmeFrame(ctk.CTkFrame):
    """Schermata che mostra il contenuto di README.md con scrollbar."""

    def __init__(self, master, origin: str = "home"):
        """
        origin: schermata da cui si è arrivati ('home' o 'practice').
                Usato per scegliere dove tornare con il pulsante Indietro.
        """
        super().__init__(master, fg_color="transparent")
        self.app    = master
        self.origin = origin
        self._build()

    # ─── Costruzione interfaccia ──────────────────────────────────────────────

    def _build(self):
        self._build_header()
        self._build_text_area()

    def _build_header(self):
        """Barra superiore con pulsante Indietro e titolo."""
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=28, pady=(18, 0))

        ctk.CTkButton(
            hdr, text="<- Indietro", width=100,
            fg_color="transparent", border_width=1,
            command=self._go_back,
        ).pack(side="left")

        ctk.CTkLabel(
            hdr, text="README — Guida all'applicazione",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(side="left", padx=20)

    def _build_text_area(self):
        """Widget tk.Text scrollabile che mostra il contenuto del README."""
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=28, pady=14)

        # Scrollbar verticale
        scrollbar = ctk.CTkScrollbar(container)
        scrollbar.pack(side="right", fill="y")

        self.text_widget = tk.Text(
            container,
            font=("Courier New", 13),
            bg="#1e1e2e", fg="#cdd6f4",
            relief="flat", bd=0,
            wrap="word",
            state="disabled",
            cursor="arrow",
            padx=22, pady=18,
            yscrollcommand=scrollbar.set,
        )
        self.text_widget.pack(fill="both", expand=True, padx=1, pady=1)
        scrollbar.configure(command=self.text_widget.yview)

        # Tag di stile per titoli, tabelle e codice
        self.text_widget.tag_configure("h1",   font=("Courier New", 20, "bold"),  foreground="#89b4fa")
        self.text_widget.tag_configure("h2",   font=("Courier New", 15, "bold"),  foreground="#cba6f7")
        self.text_widget.tag_configure("h3",   font=("Courier New", 13, "bold"),  foreground="#89dceb")
        self.text_widget.tag_configure("code", font=("Courier New", 12),          foreground="#a6e3a1", background="#313244")
        self.text_widget.tag_configure("sep",  foreground="#45475a")

        self._load_readme()

    def _load_readme(self):
        """Legge README.md e lo inserisce nel widget con formattazione basilare."""
        if not README_PATH.exists():
            content = "README.md non trovato.\nAssicurati che il file esista nella cartella del progetto."
            self._insert_plain(content)
            return

        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")

        with open(README_PATH, encoding="utf-8") as f:
            for line in f:
                self._insert_line(line)

        self.text_widget.config(state="disabled")
        self.text_widget.yview_moveto(0)  # torna all'inizio

    def _insert_line(self, line: str):
        """Inserisce una riga applicando il tag di stile corretto."""
        stripped = line.rstrip("\n")

        if stripped.startswith("# "):
            self.text_widget.insert("end", stripped[2:] + "\n", "h1")
        elif stripped.startswith("## "):
            self.text_widget.insert("end", "\n" + stripped[3:] + "\n", "h2")
        elif stripped.startswith("### "):
            self.text_widget.insert("end", stripped[4:] + "\n", "h3")
        elif stripped.startswith("---"):
            self.text_widget.insert("end", "─" * 70 + "\n", "sep")
        elif stripped.startswith("```"):
            pass  # salta delimitatori di blocco codice
        else:
            # Sostituisce il testo inline `code` con il tag code
            self._insert_with_inline_code(stripped + "\n")

    def _insert_with_inline_code(self, text: str):
        """Gestisce il backtick inline: `testo` → tag 'code'."""
        parts = text.split("`")
        for i, part in enumerate(parts):
            tag = "code" if i % 2 == 1 else ""
            self.text_widget.insert("end", part, tag)

    def _insert_plain(self, text: str):
        self.text_widget.config(state="normal")
        self.text_widget.insert("end", text)
        self.text_widget.config(state="disabled")

    # ─── Navigazione ──────────────────────────────────────────────────────────

    def _go_back(self):
        """Torna alla schermata di provenienza."""
        self.app.show_home()

# "><(((º> sabusabu <º)))><"
