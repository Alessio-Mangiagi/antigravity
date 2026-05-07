"""
Caveman Translator — Desktop App
Requires: pip install customtkinter anthropic
"""

import os
import json
import base64
import hashlib
import platform
import getpass
import threading
import customtkinter as ctk
import anthropic
from cryptography.fernet import Fernet, InvalidToken

# ── Config path ───────────────────────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "caveman_config.json")


# ── API Key encryption ────────────────────────────────────────────────────────

def _get_cipher() -> Fernet:
    machine_id = f"{platform.node()}:{getpass.getuser()}".encode()
    key_bytes = hashlib.pbkdf2_hmac("sha256", machine_id, b"caveman_v1", 200_000)
    return Fernet(base64.urlsafe_b64encode(key_bytes))

def save_api_key(api_key: str) -> None:
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

# ── Theme ────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# ── Prompts ──────────────────────────────────────────────────────────────────
LEVEL_PROMPTS = {
    "Lite": (
        "You are a caveman translator (lite mode). Rewrite the user's text removing all "
        "filler words, hedging, and pleasantries. Keep articles and full sentences. "
        "Professional but tight. No preamble—output only the rewritten text."
    ),
    "Full": (
        "You are a caveman translator (full mode). Rewrite the user's text in classic "
        "caveman style: drop articles (a/an/the), use fragments, short synonyms "
        "(big not extensive, fix not 'implement a solution for'), drop all filler and "
        "pleasantries. Technical terms stay exact. Pattern: [thing] [action] [reason]. "
        "No preamble—output only the rewritten text."
    ),
    "Ultra": (
        "You are a caveman translator (ultra mode). Maximum compression. Abbreviate "
        "aggressively (DB/auth/config/req/res/fn), strip conjunctions, use arrows for "
        "causality (X → Y), one word when one word enough. "
        "No preamble—output only the ultra-compressed text."
    ),
    "文言文": (
        "You are a caveman translator (文言文 mode). Rewrite the user's text in classical "
        "Chinese (文言文) style. Maximum terseness. Classical sentence patterns, verbs "
        "precede objects, subjects often omitted, use classical particles (之/乃/為/其/也/矣). "
        "Aim for 80-90% character reduction. No preamble—output only the classical Chinese text."
    ),
}

EXAMPLES = [
    (
        "Corporate email",
        "I wanted to reach out to touch base and circle back regarding the synergistic "
        "opportunities we discussed in our previous meeting. Going forward, I think it would "
        "be beneficial for all stakeholders if we could leverage our core competencies to "
        "drive sustainable growth.",
    ),
    (
        "Tech explanation",
        "Basically, what I'm trying to explain is that when you send an HTTP request to a "
        "server, the server processes that request and then sends back a response. The response "
        "contains a status code that indicates whether the request was successful or not.",
    ),
    (
        "Meeting request",
        "I was wondering if you might possibly be available sometime next week, perhaps on "
        "Tuesday or Wednesday, for a brief 30-minute meeting to discuss the project timeline "
        "and align on our mutual goals and deliverables?",
    ),
    (
        "Bug report",
        "I've been experiencing an issue with the application where it intermittently crashes "
        "and throws an error message. I'm not entirely sure what's causing it, but it seems to "
        "happen most often when I try to save a large file.",
    ),
]

# ── App ───────────────────────────────────────────────────────────────────────
class CavemanApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🪨 Caveman Translator")
        self.geometry("860x620")
        self.minsize(700, 500)
        self.resizable(True, True)

        self._level = ctk.StringVar(value="Full")
        self._api_key = ctk.StringVar(value=load_api_key() or "")
        self._busy = False

        self._build_ui()

    # ── UI Construction ───────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_main()
        self._build_footer()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=20, pady=(16, 0))
        hdr.grid_columnconfigure(1, weight=1)

        # Title
        title_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            title_frame, text="🪨  Caveman Translator",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left")

        ctk.CTkLabel(
            hdr,
            text="Verbose text go in. Caveman wisdom come out.",
            font=ctk.CTkFont(size=13),
            text_color=("gray50", "gray60"),
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

        # API key entry (top-right)
        key_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        key_frame.grid(row=0, column=1, rowspan=2, sticky="e")

        ctk.CTkLabel(key_frame, text="API Key:", font=ctk.CTkFont(size=12)).pack(side="left", padx=(0, 6))
        self._key_entry = ctk.CTkEntry(
            key_frame, textvariable=self._api_key,
            width=220, show="•", placeholder_text="sk-ant-…",
            font=ctk.CTkFont(size=12),
        )
        self._key_entry.pack(side="left")

        self._key_status = ctk.CTkLabel(
            key_frame,
            text="✔" if load_api_key() else "",
            font=ctk.CTkFont(size=13),
            text_color="#10B981",
        )
        self._key_status.pack(side="left", padx=(4, 0))

        ctk.CTkButton(
            key_frame, text="💾", width=30, height=28,
            fg_color="transparent", hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=14),
            command=self._save_api_key,
        ).pack(side="left", padx=(4, 0))

        ctk.CTkButton(
            key_frame, text="🗑", width=30, height=28,
            fg_color="transparent", hover_color=("gray85", "gray25"),
            font=ctk.CTkFont(size=14),
            command=self._delete_api_key,
        ).pack(side="left", padx=(2, 0))

        # Level buttons
        level_frame = ctk.CTkFrame(hdr, fg_color="transparent")
        level_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))

        ctk.CTkLabel(
            level_frame, text="Level:",
            font=ctk.CTkFont(size=13), text_color=("gray50", "gray60"),
        ).pack(side="left", padx=(0, 8))

        for level in LEVEL_PROMPTS:
            ctk.CTkRadioButton(
                level_frame, text=level,
                variable=self._level, value=level,
                font=ctk.CTkFont(size=13),
            ).pack(side="left", padx=6)

    def _build_main(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=1, column=0, sticky="nsew", padx=20, pady=12)
        main.grid_columnconfigure((0, 1), weight=1)
        main.grid_rowconfigure(1, weight=1)

        # Labels
        ctk.CTkLabel(
            main, text="YOUR VERBOSE WORDS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray45", "gray55"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        ctk.CTkLabel(
            main, text="CAVEMAN VERSION",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray45", "gray55"),
        ).grid(row=0, column=1, sticky="w", padx=(12, 0), pady=(0, 4))

        # Input textbox
        self._input = ctk.CTkTextbox(
            main, font=ctk.CTkFont(size=14), wrap="word",
            corner_radius=10,
        )
        self._input.grid(row=1, column=0, sticky="nsew", pady=(0, 0))
        self._input.insert("end", "")
        self._input.bind("<Control-Return>", lambda e: self._translate())
        self._input.bind("<Command-Return>", lambda e: self._translate())

        # Output textbox (read-only via state trick)
        self._output = ctk.CTkTextbox(
            main, font=ctk.CTkFont(size=14), wrap="word",
            corner_radius=10,
        )
        self._output.grid(row=1, column=1, sticky="nsew", padx=(12, 0))
        self._set_output("Output appear here. UGH.", color="gray")

    def _build_footer(self):
        foot = ctk.CTkFrame(self, fg_color="transparent")
        foot.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 16))
        foot.grid_columnconfigure(4, weight=1)

        # Action buttons
        self._translate_btn = ctk.CTkButton(
            foot, text="⚡  Translate",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=140, height=36,
            command=self._translate,
        )
        self._translate_btn.grid(row=0, column=0, padx=(0, 8))

        ctk.CTkButton(
            foot, text="Copy", width=80, height=36,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray90"),
            hover_color=("gray85", "gray25"),
            command=self._copy_output,
        ).grid(row=0, column=1, padx=(0, 8))

        ctk.CTkButton(
            foot, text="Clear", width=80, height=36,
            fg_color="transparent",
            border_width=1,
            text_color=("gray20", "gray90"),
            hover_color=("gray85", "gray25"),
            command=self._clear,
        ).grid(row=0, column=2, padx=(0, 16))

        # Examples menu
        ctk.CTkLabel(
            foot, text="Examples:",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        ).grid(row=0, column=3, padx=(0, 6))

        example_names = [e[0] for e in EXAMPLES]
        self._example_menu = ctk.CTkOptionMenu(
            foot, values=example_names,
            width=160, height=36,
            font=ctk.CTkFont(size=13),
            command=self._load_example,
        )
        self._example_menu.set("Pick example…")
        self._example_menu.grid(row=0, column=4, sticky="w")

        # Token badge
        self._token_label = ctk.CTkLabel(
            foot, text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        )
        self._token_label.grid(row=0, column=5, sticky="e", padx=(12, 0))

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _set_output(self, text, color=None):
        self._output.configure(state="normal")
        self._output.delete("1.0", "end")
        self._output.insert("end", text)
        if color:
            self._output.configure(text_color=color)
        else:
            self._output.configure(text_color=("gray10", "gray90"))
        self._output.configure(state="disabled")

    def _get_input(self):
        return self._input.get("1.0", "end").strip()

    def _load_example(self, name):
        for label, text in EXAMPLES:
            if label == name:
                self._input.delete("1.0", "end")
                self._input.insert("end", text)
                break

    def _copy_output(self):
        text = self._output.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(text)

    def _clear(self):
        self._input.delete("1.0", "end")
        self._set_output("Output appear here. UGH.", color="gray")
        self._token_label.configure(text="")
        self._example_menu.set("Pick example…")

    # ── API Key management ────────────────────────────────────────────────────
    def _save_api_key(self):
        key = self._api_key.get().strip()
        if not key:
            self._key_status.configure(text="✘", text_color="red")
            return
        save_api_key(key)
        self._key_status.configure(text="✔", text_color="#10B981")

    def _delete_api_key(self):
        delete_api_key()
        self._api_key.set("")
        self._key_status.configure(text="", text_color="#10B981")

    # ── Translation ───────────────────────────────────────────────────────────
    def _translate(self):
        if self._busy:
            return
        text = self._get_input()
        if not text:
            return
        api_key = self._api_key.get().strip()
        if not api_key:
            self._set_output("⚠  Enter your Anthropic API key (top right).", color="orange")
            return

        self._busy = True
        self._translate_btn.configure(state="disabled", text="Thinking…")
        self._set_output("Me thinking... 🪨", color="gray")
        self._token_label.configure(text="")

        threading.Thread(target=self._call_api, args=(text, api_key), daemon=True).start()

    def _call_api(self, text, api_key):
        level = self._level.get()
        system_prompt = LEVEL_PROMPTS[level]
        try:
            client = anthropic.Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": text}],
            )
            result = response.content[0].text
            usage = response.usage
            in_tok = usage.input_tokens
            out_tok = usage.output_tokens
            saved = round((1 - out_tok / max(1, in_tok)) * 100)
            badge = f"{in_tok} → {out_tok} tokens" + (f"  ({saved}% saved)" if saved > 0 else "")
            self.after(0, lambda: self._on_success(result, badge))
        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))

    def _on_success(self, result, badge):
        self._set_output(result)
        self._token_label.configure(text=badge)
        self._busy = False
        self._translate_btn.configure(state="normal", text="⚡  Translate")

    def _on_error(self, msg):
        self._set_output(f"⚠  Error: {msg}", color="red")
        self._busy = False
        self._translate_btn.configure(state="normal", text="⚡  Translate")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = CavemanApp()
    app.mainloop()
