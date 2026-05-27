import customtkinter as ctk


class CustomTextFrame(ctk.CTkFrame):
    """Schermata per inserire un testo personalizzato su cui esercitarsi."""

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.app = master
        self._build()

    def _build(self):
        ctk.CTkButton(
            self, text="<- Home", width=80,
            command=self.app.show_home,
        ).pack(anchor="w", padx=28, pady=(18, 0))

        ctk.CTkLabel(
            self, text="Testo Personalizzato",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(pady=(20, 4))
        ctk.CTkLabel(
            self, text="Incolla o scrivi il testo su cui vuoi esercitarti",
            font=ctk.CTkFont(size=13), text_color="gray",
        ).pack(pady=(0, 16))

        self.textbox = ctk.CTkTextbox(
            self, font=ctk.CTkFont(size=15),
            height=220, wrap="word",
        )
        self.textbox.pack(fill="x", padx=60, pady=4)
        self.textbox.insert("1.0", "")

        ctk.CTkLabel(
            self, text="Modalità visualizzazione:",
            font=ctk.CTkFont(size=13),
        ).pack(pady=(14, 4))
        self.mode_seg = ctk.CTkSegmentedButton(
            self,
            values=["Testo completo", "Parola per parola"],
            font=ctk.CTkFont(size=13),
            height=36,
        )
        self.mode_seg.set("Testo completo")
        self.mode_seg.pack(pady=(0, 8))

        self.error_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=12), text_color="#e74c3c",
        )
        self.error_label.pack(pady=(4, 0))

        ctk.CTkButton(
            self, text="Inizia esercizio",
            height=44, font=ctk.CTkFont(size=15, weight="bold"),
            command=self._start,
        ).pack(pady=16)

    def _start(self):
        text = self.textbox.get("1.0", "end").strip()
        if len(text) < 10:
            self.error_label.configure(text="Inserisci almeno 10 caratteri.")
            return
        word_by_word = self.mode_seg.get() == "Parola per parola"
        self.app.show_practice_custom(text, word_by_word)

# "><(((º> sabusabu <º)))><"
