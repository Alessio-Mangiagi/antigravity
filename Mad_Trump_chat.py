"""
Trump Chat — Parody AI  |  supports Anthropic API + Ollama (local)

Requirements:
    pip install customtkinter anthropic openai requests cryptography

Ollama setup (local AI):
    1. Install Ollama → https://ollama.com
    2. Pull a model:  ollama pull llama3
    3. Start server:  ollama serve          (auto-starts on install)
    4. Select "Ollama (Local)" in the app and pick your model
"""

import os
import json
import base64
import hashlib
import platform
import getpass
import threading
import requests
import customtkinter as ctk
import anthropic
from openai import OpenAI  # Ollama uses an OpenAI-compatible API
from cryptography.fernet import Fernet, InvalidToken

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

RED    = "#B22234"
GOLD   = "#FFD700"
DARK   = "#1A1A1A"
DARKER = "#111111"
WHITE  = "#F5F5F5"
GRAY   = "#2B2B2B"
LGRAY  = "#3A3A3A"
GREEN  = "#1DB954"

# ── Language Support ───────────────────────────────────────────────────────────
LANGUAGES = {
    "en": {
        "title": "🇺🇸 Trump Chat — Parody AI",
        "header_title": "TRUMP CHAT",
        "header_subtitle": "The most tremendous chatbot. Believe me.",
        "warning": "⚠ PARODY",
        "backend_label": "Backend:",
        "anthropic_option": "Anthropic (Cloud)",
        "ollama_option": "Ollama (Local)",
        "model_label": "Model:",
        "status_cloud": "● Cloud",
        "status_local": "● Local",
        "status_offline": "● Offline",
        "refresh_button": "↺",
        "placeholder": "Ask Trump anything…",
        "send_button": "Send ➤",
        "clear_button": "🗑",
        "suggestion_1": "Who is the best president?",
        "suggestion_2": "Tell me about your wall",
        "suggestion_3": "What do you think of AI?",
        "suggestion_4": "Is the media fake news?",
        "welcome_message": (
            "Folks, I am SO glad you're here. Nobody builds better chatbots than me, "
            "believe me. What do you want to talk about? It's going to be TREMENDOUS!"
        ),
        "typing_indicator": "● ● ●",
        "author_tag": "Donald T.",
        "author_tag_with_model": "Donald T. via {}",
        "you_label": "You",
        "error_message": "Something broke — very bad, terrible. ({})",
        "ollama_not_running": "(Ollama not running)",
        "no_models_found": "(no models found)"
    },
    "it": {
        "title": "🇺🇸 Trump Chat — Parodia IA",
        "header_title": "TRUMP CHAT",
        "header_subtitle": "La chatbot più incredibile. Credimi.",
        "warning": "⚠ PARODIA",
        "backend_label": "Backend:",
        "anthropic_option": "Anthropic (Cloud)",
        "ollama_option": "Ollama (Locale)",
        "model_label": "Modello:",
        "status_cloud": "● Cloud",
        "status_local": "● Locale",
        "status_offline": "● Offline",
        "refresh_button": "↺",
        "placeholder": "Chiedi qualcosa a Trump…",
        "send_button": "Invia ➤",
        "clear_button": "🗑",
        "suggestion_1": "Chi è il miglior presidente?",
        "suggestion_2": "Dimmi del tuo muro",
        "suggestion_3": "Cosa pensi dell'IA?",
        "suggestion_4": "I media sono fake news?",
        "welcome_message": (
            "Ragazzi, sono FELICE che siate qui. Nessuno crea chatbot migliori di me, "
            "credetemi. Di cosa volete parlare? Sarà INCREDBILE!"
        ),
        "typing_indicator": "● ● ●",
        "author_tag": "Donald T.",
        "author_tag_with_model": "Donald T. via {}",
        "you_label": "Tu",
        "error_message": "Qualcosa è andato storto — molto brutto, terribile. ({})",
        "ollama_not_running": "(Ollama non in esecuzione)",
        "no_models_found": "(nessun modello trovato)"
    }
}

# Current language (default to English)
CURRENT_LANGUAGE = "en"

SYSTEM_PROMPT = """You are a satirical parody AI that responds exactly like Donald Trump — for entertainment purposes only (PARODY).
Rules:
- Use his trademark phrases: "believe me", "tremendous", "the best", "nobody knows more about X than me", "many people are saying", "it's a disaster", "fake news"
- Speak in short, repetitive, punchy sentences
- Boast constantly — everything is "the greatest", "beautiful", "perfect"
- Use superlatives obsessively
- Keep replies to 3-5 sentences max
- This is clearly satire — do NOT present as real statements"""

OLLAMA_BASE = "http://localhost:1234"

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trump_config.json")


# ── API Key encryption ─────────────────────────────────────────────────────────

def _get_cipher() -> Fernet:
    """Derive a Fernet cipher from machine-specific data (hostname + username)."""
    machine_id = f"{platform.node()}:{getpass.getuser()}".encode()
    key_bytes = hashlib.pbkdf2_hmac("sha256", machine_id, b"trump_chat_v1", 200_000)
    return Fernet(base64.urlsafe_b64encode(key_bytes))

def save_api_key(api_key: str) -> None:
    """Encrypt and save the API key to the local config file."""
    cipher = _get_cipher()
    encrypted = cipher.encrypt(api_key.strip().encode()).decode()
    config: dict = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass
    config["api_key"] = encrypted
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f)

def load_api_key() -> str | None:
    """Load and decrypt the API key from the local config file."""
    if not os.path.exists(CONFIG_PATH):
        return None
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        encrypted = config.get("api_key")
        if not encrypted:
            return None
        return _get_cipher().decrypt(encrypted.encode()).decode()
    except (InvalidToken, Exception):
        return None

def delete_api_key() -> None:
    """Remove the saved API key from the config file."""
    if not os.path.exists(CONFIG_PATH):
        return
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        config.pop("api_key", None)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(config, f)
    except Exception:
        pass


# ── Helpers ────────────────────────────────────────────────────────────────────

def get_ollama_models() -> list:
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []

def tr(key: str) -> str:
    """Translate a key to the current language"""
    return LANGUAGES[CURRENT_LANGUAGE].get(key, LANGUAGES["en"][key])

def set_language(lang_code: str):
    """Change the current language and update the UI"""
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = lang_code
    # Update window title
    app.title(tr("title"))
    

# ── Main App ───────────────────────────────────────────────────────────────────

class TrumpChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(tr("title"))
        self.geometry("720x680")
        self.minsize(580, 540)
        self.configure(fg_color=DARKER)

        self.history       = []
        saved_key = load_api_key()
        self.anthropic_cl  = anthropic.Anthropic(api_key=saved_key) if saved_key else anthropic.Anthropic()
        self.ollama_client = OpenAI(base_url=f"{OLLAMA_BASE}/v1", api_key="ollama")

        self._build_ui()
        self._add_bot_message(tr("welcome_message"))

    # ── UI Construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build_header()
        self._build_model_bar()
        self._build_chat_area()
        self._build_suggestions()
        self._build_input_bar()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=RED, corner_radius=0, height=64)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(hdr, text="🇺🇸", font=ctk.CTkFont(size=28)).grid(
            row=0, column=0, rowspan=2, padx=(16, 10), pady=12)
        ctk.CTkLabel(hdr, text=tr("header_title"),
            font=ctk.CTkFont(size=17, weight="bold"), text_color=GOLD
        ).grid(row=0, column=1, sticky="sw", pady=(12, 0))
        ctk.CTkLabel(hdr, text=tr("header_subtitle"),
            font=ctk.CTkFont(size=11), text_color="#FFAAAA"
        ).grid(row=1, column=1, sticky="nw", pady=(0, 10))
        ctk.CTkLabel(hdr, text=tr("warning"),
            font=ctk.CTkFont(size=10, weight="bold"), text_color=GOLD
        ).grid(row=0, column=2, rowspan=2, padx=16)

    def _build_model_bar(self):
        bar = ctk.CTkFrame(self, fg_color="#222222", corner_radius=0, height=48)
        bar.grid(row=1, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(bar, text=tr("backend_label"), font=ctk.CTkFont(size=12),
                     text_color="#AAAAAA").grid(row=0, column=0, padx=(12, 6), pady=12)

        self.backend_var = ctk.StringVar(value=tr("anthropic_option"))
        ctk.CTkOptionMenu(
            bar,
            values=[tr("anthropic_option"), tr("ollama_option")],
            variable=self.backend_var,
            font=ctk.CTkFont(size=12),
            fg_color=LGRAY, button_color=GRAY,
            button_hover_color=RED, text_color=WHITE,
            width=170, height=28,
            command=self._on_backend_change,
        ).grid(row=0, column=1, padx=4, pady=10)

        # Ollama model picker (shown only when Ollama selected)
        self.model_label = ctk.CTkLabel(bar, text=tr("model_label"), font=ctk.CTkFont(size=12),
                                        text_color="#AAAAAA")
        ollama_models = get_ollama_models()
        self.ollama_models = [tr("no_models_found")] if not ollama_models else ollama_models
        self.model_var = ctk.StringVar(value=self.ollama_models[0] if self.ollama_models else "")
        self.model_menu = ctk.CTkOptionMenu(
            bar, values=self.ollama_models, variable=self.model_var,
            font=ctk.CTkFont(size=12),
            fg_color=LGRAY, button_color=GRAY,
            button_hover_color=GREEN, text_color=WHITE,
            width=180, height=28,
        )
        self.refresh_btn = ctk.CTkButton(
            bar, text=tr("refresh_button"), width=28, height=28,
            fg_color=GRAY, hover_color=GREEN, text_color=WHITE,
            font=ctk.CTkFont(size=14), corner_radius=14,
            command=self._refresh_ollama_models,
        )

        # Language selector
        ctk.CTkLabel(bar, text="Language:", font=ctk.CTkFont(size=12),
                     text_color="#AAAAAA").grid(row=0, column=5, padx=(20, 6), pady=12)
        self.lang_var = ctk.StringVar(value="English" if CURRENT_LANGUAGE == "en" else "Italiano")
        self.lang_menu = ctk.CTkOptionMenu(
            bar,
            values=["English", "Italiano"],
            variable=self.lang_var,
            font=ctk.CTkFont(size=12),
            fg_color=LGRAY, button_color=GRAY,
            button_hover_color=GREEN, text_color=WHITE,
            width=100, height=28,
            command=self._on_language_change,
        )
        self.lang_menu.grid(row=0, column=6, padx=4, pady=10)

        # Status dot
        self.status_dot = ctk.CTkLabel(bar, text=tr("status_cloud"), font=ctk.CTkFont(size=11),
                                       text_color="#4FC3F7")
        self.status_dot.grid(row=0, column=7, padx=12)

        # Settings button
        ctk.CTkButton(
            bar, text="⚙", width=28, height=28,
            fg_color=GRAY, hover_color=RED, text_color=WHITE,
            font=ctk.CTkFont(size=14), corner_radius=14,
            command=self._show_api_key_settings,
        ).grid(row=0, column=8, padx=(0, 10))

    def _on_language_change(self, value: str):
        """Handle language change"""
        new_lang = "it" if value == "Italiano" else "en"
        if new_lang != CURRENT_LANGUAGE:
            set_language(new_lang)
            # Refresh UI elements with new language
            self._refresh_ui_language()

    def _refresh_ui_language(self):
        """Refresh UI elements with current language"""
        # Update window title
        self.title(tr("title"))
        
        # Update backend option menu
        self.backend_var.set(tr("anthropic_option"))
        self.model_menu.configure(values=[tr("no_models_found")] if not get_ollama_models() else get_ollama_models())
        
        # Update status dot text
        if self.backend_var.get() == tr("ollama_option"):
            self.status_dot.configure(text=tr("status_local"))
        else:
            self.status_dot.configure(text=tr("status_cloud"))
        
        # Update suggestion buttons
        for i, child in enumerate(self.winfo_children()):
            if isinstance(child, ctk.CTkFrame) and child._current_row == 3:
                for j, btn in enumerate(child.winfo_children()[0].winfo_children()):
                    if j == 0:
                        btn.configure(text=tr("suggestion_1"))
                    elif j == 1:
                        btn.configure(text=tr("suggestion_2"))
                    elif j == 2:
                        btn.configure(text=tr("suggestion_3"))
                    elif j == 3:
                        btn.configure(text=tr("suggestion_4"))
        
        # Update input box placeholder (we can't directly change placeholder text, so we reset it)
        current_text = self.input_box.get()
        self.input_box.delete(0, "end")
        self.input_box.configure(placeholder_text=tr("placeholder"))
        self.input_box.insert(0, current_text)
        
        # Update other static text elements
        for child in self.winfo_children():
            if hasattr(child, 'winfo_children'):
                for widget in child.winfo_children():
                    if isinstance(widget, ctk.CTkLabel):
                        # Check for specific labels to update
                        if widget.cget("text") == tr("backend_label").replace(":", ""):
                            widget.configure(text=tr("backend_label"))
                        elif widget.cget("text") == tr("model_label").replace(":", ""):
                            widget.configure(text=tr("model_label"))
    
    def _build_chat_area(self):
        self.chat_frame = ctk.CTkScrollableFrame(
            self, fg_color=DARK, corner_radius=0,
            scrollbar_button_color=GRAY,
            scrollbar_button_hover_color=LGRAY,
        )
        self.chat_frame.grid(row=2, column=0, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

    def _build_suggestions(self):
        sug = ctk.CTkFrame(self, fg_color=GRAY, corner_radius=0, height=40)
        sug.grid(row=3, column=0, sticky="ew")
        sug.grid_propagate(False)
        inner = ctk.CTkFrame(sug, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        suggestions = [
            tr("suggestion_1"),
            tr("suggestion_2"),
            tr("suggestion_3"),
            tr("suggestion_4")
        ]
        for s in suggestions:
            ctk.CTkButton(
                inner, text=s, font=ctk.CTkFont(size=11), height=26,
                fg_color=LGRAY, hover_color=RED, text_color=WHITE,
                border_width=0, corner_radius=13,
                command=lambda t=s: self._send(t),
            ).pack(side="left", padx=4)

    def _build_input_bar(self):
        bar = ctk.CTkFrame(self, fg_color=GRAY, corner_radius=0, height=60)
        bar.grid(row=4, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkEntry(
            bar, placeholder_text=tr("placeholder"),
            font=ctk.CTkFont(size=14),
            fg_color=LGRAY, border_color="#555",
            text_color=WHITE, placeholder_text_color="#888",
            height=38, corner_radius=19,
        )
        self.input_box.grid(row=0, column=0, padx=(12, 8), pady=11, sticky="ew")
        self.input_box.bind("<Return>", lambda e: self._send())

        self.send_btn = ctk.CTkButton(
            bar, text=tr("send_button"),
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=RED, hover_color="#8B0000", text_color=WHITE,
            height=38, width=90, corner_radius=19,
            command=self._send,
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 8), pady=11)

        ctk.CTkButton(
            bar, text=tr("clear_button"), width=38, height=38,
            fg_color=LGRAY, hover_color="#555", text_color="#AAA",
            corner_radius=19, font=ctk.CTkFont(size=16),
            command=self._clear_chat,
        ).grid(row=0, column=2, padx=(0, 12), pady=11)

    # ── Backend Switching ──────────────────────────────────────────────────────

    def _on_backend_change(self, value: str):
        if value == tr("ollama_option"):
            self._refresh_ollama_models()
            self.model_label.grid(row=0, column=2, padx=(8, 4), pady=12)
            self.model_menu.grid(row=0, column=3, padx=4, pady=10)
            self.refresh_btn.grid(row=0, column=5, padx=(4, 8), pady=10)
            self.status_dot.configure(text=tr("status_local"), text_color="#66BB6A")
        else:
            self.model_label.grid_remove()
            self.model_menu.grid_remove()
            self.refresh_btn.grid_remove()
            self.status_dot.configure(text=tr("status_cloud"), text_color="#4FC3F7")

    def _refresh_ollama_models(self):
        models = get_ollama_models()
        if models:
            self.ollama_models = models
            self.model_menu.configure(values=models)
            self.model_var.set(models[0])
            self.status_dot.configure(
                text=f"{tr('status_local')} ({len(models)} models)", text_color="#66BB6A")
        else:
            self.model_menu.configure(values=[tr("ollama_not_running")])
            self.model_var.set(tr("ollama_not_running"))
            self.status_dot.configure(text=tr("status_offline"), text_color="#EF5350")

    # ── Message Bubbles ────────────────────────────────────────────────────────

    def _add_user_message(self, text: str):
        row = self.chat_frame.grid_size()[1]
        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=12, pady=(6, 0))
        w.grid_columnconfigure(0, weight=1)

        bubble = ctk.CTkFrame(w, fg_color=RED, corner_radius=16)
        bubble.grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(bubble, text=text, font=ctk.CTkFont(size=13),
                     text_color=WHITE, wraplength=500, justify="left",
                     ).pack(padx=14, pady=8)
        ctk.CTkLabel(w, text=tr("you_label"), font=ctk.CTkFont(size=10),
                     text_color="#888").grid(row=1, column=1, sticky="e", pady=(2, 0))
        self._scroll_bottom()

    def _add_bot_message(self, text: str, typing: bool = False):
        row = self.chat_frame.grid_size()[1]
        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=12, pady=(6, 0))
        w.grid_columnconfigure(1, weight=1)

        av = ctk.CTkFrame(w, fg_color=GOLD, width=34, height=34, corner_radius=17)
        av.grid(row=0, column=0, sticky="n", padx=(0, 8))
        av.grid_propagate(False)
        ctk.CTkLabel(av, text="DT", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#8B0000").place(relx=0.5, rely=0.5, anchor="center")

        bubble = ctk.CTkFrame(w, fg_color=LGRAY, corner_radius=16)
        bubble.grid(row=0, column=1, sticky="w")
        # Calculate wraplength dynamically based on window width
        wrap = min(500, max(300, self.winfo_width() - 220)) if self.winfo_width() > 10 else 500
        label = ctk.CTkLabel(
            bubble,
            text=tr("typing_indicator") if typing else text,
            font=ctk.CTkFont(size=13),
            text_color="#AAAAAA" if typing else WHITE,
            wraplength=wrap, justify="left",
        )
        label.pack(padx=14, pady=9)

        tag = tr("author_tag")
        if not typing and self.backend_var.get() == tr("ollama_option"):
            tag = tr("author_tag_with_model").format(self.model_var.get())
        ctk.CTkLabel(w, text=tag, font=ctk.CTkFont(size=10),
                     text_color="#888").grid(row=1, column=1, sticky="w", pady=(2, 4))

        self._scroll_bottom()
        return w

    def _scroll_bottom(self):
        self.after(60, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    # ── Sending Logic ──────────────────────────────────────────────────────────

    def _send(self, text: str = None):
        msg = text or self.input_box.get().strip()
        if not msg:
            return
        self.input_box.delete(0, "end")
        self.send_btn.configure(state="disabled")
        self._add_user_message(msg)
        self.history.append({"role": "user", "content": msg})
        typing_w = self._add_bot_message("", typing=True)
        threading.Thread(
            target=self._fetch_reply, args=(typing_w,), daemon=True
        ).start()

    def _fetch_reply(self, typing_w):
        try:
            if self.backend_var.get() == tr("anthropic_option"):
                reply = self._call_anthropic()
            else:
                reply = self._call_ollama()
        except Exception as e:
            reply = tr("error_message").format(e)

        self.history.append({"role": "assistant", "content": reply})
        self.after(0, lambda: self._replace_typing(typing_w, reply))

    def _call_anthropic(self) -> str:
        resp = self.anthropic_cl.messages.create(
            model="claude-opus-4-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )
        return resp.content[0].text

    def _call_ollama(self) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history
        resp = self.ollama_client.chat.completions.create(
            model=self.model_var.get(),
            messages=messages,
            max_tokens=1000,
        )
        return resp.choices[0].message.content

    def _replace_typing(self, typing_w, reply: str):
        """Destroy the typing-indicator widget and rebuild it with the real reply."""
        # Remember grid position before destroying
        grid_info = typing_w.grid_info()
        row = grid_info.get("row", 0)
        typing_w.destroy()

        # Re-create the bubble in the same grid slot
        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=12, pady=(6, 0))
        w.grid_columnconfigure(1, weight=1)

        av = ctk.CTkFrame(w, fg_color=GOLD, width=34, height=34, corner_radius=17)
        av.grid(row=0, column=0, sticky="n", padx=(0, 8))
        av.grid_propagate(False)
        ctk.CTkLabel(av, text="DT", font=ctk.CTkFont(size=11, weight="bold"),
                     text_color="#8B0000").place(relx=0.5, rely=0.5, anchor="center")

        wrap = min(500, max(300, self.winfo_width() - 220)) if self.winfo_width() > 10 else 500
        bubble = ctk.CTkFrame(w, fg_color=LGRAY, corner_radius=16)
        bubble.grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(
            bubble, text=reply,
            font=ctk.CTkFont(size=13), text_color=WHITE,
            wraplength=wrap, justify="left",
        ).pack(padx=14, pady=9)

        tag = tr("author_tag")
        if self.backend_var.get() == tr("ollama_option"):
            tag = tr("author_tag_with_model").format(self.model_var.get())
        ctk.CTkLabel(w, text=tag, font=ctk.CTkFont(size=10),
                     text_color="#888").grid(row=1, column=1, sticky="w", pady=(2, 4))

        self.send_btn.configure(state="normal")
        self._scroll_bottom()

    def _show_api_key_settings(self):
        win = ctk.CTkToplevel(self)
        win.title("API Key Settings")
        win.geometry("420x260")
        win.resizable(False, False)
        win.configure(fg_color=DARK)
        win.grab_set()

        ctk.CTkLabel(win, text="Anthropic API Key",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color=GOLD
                     ).pack(pady=(20, 4))

        has_key = load_api_key() is not None
        status_text = "✔ Chiave salvata" if has_key else "✘ Nessuna chiave salvata"
        status_color = GREEN if has_key else "#EF5350"
        status_lbl = ctk.CTkLabel(win, text=status_text,
                                   font=ctk.CTkFont(size=11), text_color=status_color)
        status_lbl.pack(pady=(0, 10))

        entry_frame = ctk.CTkFrame(win, fg_color="transparent")
        entry_frame.pack(padx=24, fill="x")

        key_var = ctk.StringVar()
        key_entry = ctk.CTkEntry(
            entry_frame, textvariable=key_var, show="*",
            placeholder_text="sk-ant-...",
            font=ctk.CTkFont(size=13), height=38, corner_radius=10,
            fg_color=LGRAY, border_color="#555", text_color=WHITE,
        )
        key_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        visible = ctk.BooleanVar(value=False)
        def _toggle_visibility():
            key_entry.configure(show="" if visible.get() else "*")
        ctk.CTkCheckBox(
            entry_frame, text="Mostra", variable=visible,
            font=ctk.CTkFont(size=11), text_color="#AAA",
            fg_color=RED, hover_color="#8B0000",
            command=_toggle_visibility,
        ).pack(side="left")

        msg_lbl = ctk.CTkLabel(win, text="", font=ctk.CTkFont(size=11))
        msg_lbl.pack(pady=(8, 0))

        def _save():
            key = key_var.get().strip()
            if not key:
                msg_lbl.configure(text="Inserisci una chiave valida.", text_color="#EF5350")
                return
            save_api_key(key)
            self.anthropic_cl = anthropic.Anthropic(api_key=key)
            status_lbl.configure(text="✔ Chiave salvata", text_color=GREEN)
            msg_lbl.configure(text="Chiave cifrata e salvata!", text_color=GREEN)
            key_entry.delete(0, "end")

        def _delete():
            delete_api_key()
            self.anthropic_cl = anthropic.Anthropic()
            status_lbl.configure(text="✘ Nessuna chiave salvata", text_color="#EF5350")
            msg_lbl.configure(text="Chiave rimossa.", text_color="#AAA")

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=16)
        ctk.CTkButton(btn_frame, text="Salva", width=110, height=34,
                      fg_color=RED, hover_color="#8B0000", font=ctk.CTkFont(size=13),
                      command=_save).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Elimina", width=110, height=34,
                      fg_color=LGRAY, hover_color="#555", font=ctk.CTkFont(size=13),
                      command=_delete).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Chiudi", width=80, height=34,
                      fg_color=GRAY, hover_color="#444", font=ctk.CTkFont(size=13),
                      command=win.destroy).pack(side="left", padx=6)

    def _clear_chat(self):
        self.history.clear()
        for w in self.chat_frame.winfo_children():
            w.destroy()
        self._add_bot_message(tr("welcome_message"))


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = TrumpChatApp()
    app.mainloop()