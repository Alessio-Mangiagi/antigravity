"""
Enterprise Chatbot MVP  |  Fase 2
Intenti: FAQ · Supporto · Ordini · Prodotti · Escalation

Requirements:
    pip install customtkinter anthropic openai requests cryptography
"""

import threading
import time
import json
import os
import base64
import hashlib
import platform
import getpass
import requests
import customtkinter as ctk
import anthropic
from cryptography.fernet import Fernet, InvalidToken
from openai import OpenAI
from datetime import datetime

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PRIMARY   = "#4F6EF7"
SECONDARY = "#7C3AED"
SUCCESS   = "#10B981"
WARNING   = "#F59E0B"
DANGER    = "#EF4444"
DARK      = "#0F172A"
DARKER    = "#080E1A"
CARD      = "#1E293B"
CARD2     = "#263045"
BORDER    = "#334155"
WHITE     = "#F1F5F9"
MUTED     = "#64748B"

# ── Knowledge Base ─────────────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "orari": "Siamo operativi dal lunedì al venerdì, dalle 09:00 alle 18:00. Il sabato dalle 10:00 alle 13:00.",
    "contatti": "Puoi contattarci a supporto@azienda.it oppure al numero 800-123-456 (gratuito).",
    "reso": "Il reso è gratuito entro 30 giorni dall'acquisto. Puoi avviarlo dal tuo profilo → 'I miei ordini'.",
    "spedizione": "Spediamo in tutta Italia in 2-3 giorni lavorativi. La spedizione è gratuita sopra i 50€.",
    "pagamento": "Accettiamo carta di credito, PayPal, bonifico bancario e contrassegno.",
    "garanzia": "I nostri prodotti hanno 2 anni di garanzia legale. Alcuni prodotti hanno garanzia estesa fino a 5 anni.",
    "fattura": "La fattura viene emessa automaticamente. Puoi scaricarla dalla tua area personale.",
    "account": "Per problemi di accesso usa 'Password dimenticata' nella pagina di login, o contattaci.",
}

SYSTEM_PROMPT = f"""Sei un assistente virtuale professionale di un'azienda italiana.
Il tuo ruolo è aiutare i clienti in modo chiaro, cordiale e conciso.

Intenti principali che gestisci:
1. FAQ – rispondi a domande frequenti usando la knowledge base
2. Supporto Tecnico – guida l'utente nella risoluzione di problemi
3. Stato Ordini – chiedi numero ordine e fornisci assistenza
4. Prodotti e Prezzi – descrivi prodotti e promozioni
5. Escalation – se non riesci a risolvere, offri di passare a un operatore umano

Knowledge Base:
{json.dumps(KNOWLEDGE_BASE, ensure_ascii=False, indent=2)}

Regole:
- Rispondi sempre in italiano
- Sii conciso (max 3-4 frasi)
- Se la domanda esula dalle tue competenze, proponi escalation all'operatore
- Non inventare informazioni non presenti nella knowledge base
- Includi [ESCALATION] nel testo se l'utente chiede esplicitamente un operatore umano"""

WELCOME = "Ciao! 👋 Sono l'assistente virtuale. Posso aiutarti con ordini, prodotti, supporto tecnico e molto altro. Come posso aiutarti oggi?"

SUGGESTIONS = ["📦 Stato ordine", "↩️ Come fare un reso", "🚚 Tempi di spedizione", "📞 Parlare con operatore"]

OLLAMA_BASE = "http://localhost:11434"
LOG_FILE    = os.path.join(os.path.dirname(__file__), "chatbot_kpi.json")
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbot_config.json")


# ── API Key encryption ─────────────────────────────────────────────────────────

def _get_cipher() -> Fernet:
    machine_id = f"{platform.node()}:{getpass.getuser()}".encode()
    key_bytes = hashlib.pbkdf2_hmac("sha256", machine_id, b"chatbot_v1", 200_000)
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

# ── KPI Logger ─────────────────────────────────────────────────────────────────
class KPILogger:
    def __init__(self):
        self.session_start = time.time()
        self.messages = 0
        self.escalations = 0
        self.response_times = []

    def log_response(self, ms: float, escalated: bool = False):
        self.messages += 1
        self.response_times.append(ms)
        if escalated:
            self.escalations += 1

    def summary(self) -> dict:
        rt = self.response_times
        return {
            "session_start": datetime.fromtimestamp(self.session_start).isoformat(),
            "total_messages": self.messages,
            "escalations": self.escalations,
            "avg_response_ms": round(sum(rt) / len(rt), 1) if rt else 0,
            "max_response_ms": round(max(rt), 1) if rt else 0,
        }

    def save(self):
        data = []
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = []
        data.append(self.summary())
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ── Helpers ────────────────────────────────────────────────────────────────────
def get_ollama_models() -> list:
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=3)
        r.raise_for_status()
        return [m["name"] for m in r.json().get("models", [])]
    except Exception:
        return []


# ── Main App ───────────────────────────────────────────────────────────────────
class EnterpriseChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("💼 Assistente Virtuale – MVP")
        self.geometry("780x720")
        self.minsize(600, 560)
        self.configure(fg_color=DARKER)

        self.history        = []
        self.kpi            = KPILogger()
        self.escalated      = False
        saved_key = load_api_key()
        self.anthropic_cl   = anthropic.Anthropic(api_key=saved_key) if saved_key else anthropic.Anthropic()
        self.ollama_client  = OpenAI(base_url=f"{OLLAMA_BASE}/v1", api_key="ollama")

        self._build_ui()
        self._add_bot_message(WELCOME)

    # ── UI ─────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._build_header()
        self._build_toolbar()
        self._build_chat()
        self._build_suggestions()
        self._build_input()

    def _build_header(self):
        hdr = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=68)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(1, weight=1)

        # Gradient-style logo block
        logo = ctk.CTkFrame(hdr, fg_color=PRIMARY, width=46, height=46, corner_radius=12)
        logo.grid(row=0, column=0, rowspan=2, padx=(16, 12), pady=11)
        logo.grid_propagate(False)
        ctk.CTkLabel(logo, text="🤖", font=ctk.CTkFont(size=22)).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(hdr, text="Assistente Virtuale",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=WHITE
                     ).grid(row=0, column=1, sticky="sw", pady=(14, 0))
        ctk.CTkLabel(hdr, text="MVP · Fase 2  |  5 Intenti attivi",
                     font=ctk.CTkFont(size=11), text_color=MUTED
                     ).grid(row=1, column=1, sticky="nw", pady=(0, 12))

        self.status_pill = ctk.CTkLabel(
            hdr, text="● Online", font=ctk.CTkFont(size=11, weight="bold"),
            text_color=SUCCESS)
        self.status_pill.grid(row=0, column=2, rowspan=2, padx=16)

    def _build_toolbar(self):
        bar = ctk.CTkFrame(self, fg_color="#16213E", corner_radius=0, height=46)
        bar.grid(row=1, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(3, weight=1)

        ctk.CTkLabel(bar, text="Backend:", font=ctk.CTkFont(size=12),
                     text_color=MUTED).grid(row=0, column=0, padx=(12, 6), pady=10)

        self.backend_var = ctk.StringVar(value="Anthropic (Cloud)")
        ctk.CTkOptionMenu(
            bar, values=["Anthropic (Cloud)", "Ollama (Local)"],
            variable=self.backend_var,
            font=ctk.CTkFont(size=12),
            fg_color=CARD2, button_color=BORDER,
            button_hover_color=PRIMARY, text_color=WHITE,
            width=170, height=28,
            command=self._on_backend_change,
        ).grid(row=0, column=1, padx=4, pady=9)

        self.model_label = ctk.CTkLabel(bar, text="Modello:", font=ctk.CTkFont(size=12), text_color=MUTED)
        self.model_var   = ctk.StringVar(value="(no models)")
        self.model_menu  = ctk.CTkOptionMenu(
            bar, values=["(no models)"], variable=self.model_var,
            font=ctk.CTkFont(size=12),
            fg_color=CARD2, button_color=BORDER,
            button_hover_color=SUCCESS, text_color=WHITE,
            width=180, height=28,
        )
        self.refresh_btn = ctk.CTkButton(
            bar, text="↺", width=28, height=28,
            fg_color=CARD2, hover_color=SUCCESS, text_color=WHITE,
            font=ctk.CTkFont(size=14), corner_radius=14,
            command=self._refresh_ollama,
        )

        # KPI button
        ctk.CTkButton(
            bar, text="📊 KPI", width=70, height=28,
            fg_color=CARD2, hover_color=SECONDARY, text_color=WHITE,
            font=ctk.CTkFont(size=12), corner_radius=6,
            command=self._show_kpi,
        ).grid(row=0, column=4, padx=(0, 4), pady=9)

        # Settings button
        ctk.CTkButton(
            bar, text="⚙", width=28, height=28,
            fg_color=CARD2, hover_color=DANGER, text_color=WHITE,
            font=ctk.CTkFont(size=14), corner_radius=14,
            command=self._show_api_key_settings,
        ).grid(row=0, column=5, padx=(0, 12), pady=9)

    def _build_chat(self):
        self.chat_frame = ctk.CTkScrollableFrame(
            self, fg_color=DARK, corner_radius=0,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=CARD2,
        )
        self.chat_frame.grid(row=2, column=0, sticky="nsew")
        self.chat_frame.grid_columnconfigure(0, weight=1)

    def _build_suggestions(self):
        sug = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=42)
        sug.grid(row=3, column=0, sticky="ew")
        sug.grid_propagate(False)
        inner = ctk.CTkFrame(sug, fg_color="transparent")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        for s in SUGGESTIONS:
            ctk.CTkButton(
                inner, text=s, font=ctk.CTkFont(size=11), height=26,
                fg_color=CARD2, hover_color=PRIMARY, text_color=WHITE,
                border_width=0, corner_radius=13,
                command=lambda t=s: self._send(t),
            ).pack(side="left", padx=4)

    def _build_input(self):
        bar = ctk.CTkFrame(self, fg_color=CARD, corner_radius=0, height=62)
        bar.grid(row=4, column=0, sticky="ew")
        bar.grid_propagate(False)
        bar.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkEntry(
            bar, placeholder_text="Scrivi un messaggio…",
            font=ctk.CTkFont(size=14),
            fg_color=CARD2, border_color=BORDER,
            text_color=WHITE, placeholder_text_color=MUTED,
            height=38, corner_radius=19,
        )
        self.input_box.grid(row=0, column=0, padx=(14, 8), pady=12, sticky="ew")
        self.input_box.bind("<Return>", lambda e: self._send())

        self.send_btn = ctk.CTkButton(
            bar, text="Invia ➤",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=PRIMARY, hover_color=SECONDARY, text_color=WHITE,
            height=38, width=96, corner_radius=19,
            command=self._send,
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 8), pady=12)

        ctk.CTkButton(
            bar, text="🗑", width=38, height=38,
            fg_color=CARD2, hover_color=DANGER, text_color=MUTED,
            corner_radius=19, font=ctk.CTkFont(size=16),
            command=self._clear_chat,
        ).grid(row=0, column=2, padx=(0, 14), pady=12)

    # ── Backend ────────────────────────────────────────────────────────────────

    def _on_backend_change(self, value: str):
        if value == "Ollama (Local)":
            self._refresh_ollama()
            self.model_label.grid(row=0, column=2, padx=(8, 4), pady=10)
            self.model_menu.grid(row=0, column=3, padx=4, pady=9)
            self.refresh_btn.grid(row=0, column=5, padx=(4, 4), pady=9)
            self.status_pill.configure(text="● Locale", text_color=SUCCESS)
        else:
            self.model_label.grid_remove()
            self.model_menu.grid_remove()
            self.refresh_btn.grid_remove()
            self.status_pill.configure(text="● Online", text_color=SUCCESS)

    def _refresh_ollama(self):
        models = get_ollama_models()
        if models:
            self.model_menu.configure(values=models)
            self.model_var.set(models[0])
            self.status_pill.configure(text=f"● Locale ({len(models)})", text_color=SUCCESS)
        else:
            self.model_menu.configure(values=["(Ollama offline)"])
            self.model_var.set("(Ollama offline)")
            self.status_pill.configure(text="● Offline", text_color=DANGER)

    # ── Messages ───────────────────────────────────────────────────────────────

    def _add_user_message(self, text: str):
        row = self.chat_frame.grid_size()[1]
        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=14, pady=(8, 0))
        w.grid_columnconfigure(0, weight=1)

        bubble = ctk.CTkFrame(w, fg_color=PRIMARY, corner_radius=16)
        bubble.grid(row=0, column=1, sticky="e")
        ctk.CTkLabel(bubble, text=text, font=ctk.CTkFont(size=13),
                     text_color=WHITE, wraplength=430, justify="left",
                     ).pack(padx=14, pady=9)
        ctk.CTkLabel(w, text="Tu  " + datetime.now().strftime("%H:%M"),
                     font=ctk.CTkFont(size=10), text_color=MUTED
                     ).grid(row=1, column=1, sticky="e", pady=(2, 0))
        self._scroll_bottom()

    def _add_bot_message(self, text: str, typing: bool = False, escalation: bool = False):
        row = self.chat_frame.grid_size()[1]
        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=14, pady=(8, 0))
        w.grid_columnconfigure(1, weight=1)

        color = WARNING if escalation else CARD2
        av = ctk.CTkFrame(w, fg_color=PRIMARY, width=34, height=34, corner_radius=10)
        av.grid(row=0, column=0, sticky="n", padx=(0, 10))
        av.grid_propagate(False)
        ctk.CTkLabel(av, text="🤖", font=ctk.CTkFont(size=16)
                     ).place(relx=0.5, rely=0.5, anchor="center")

        bubble = ctk.CTkFrame(w, fg_color=color, corner_radius=16)
        bubble.grid(row=0, column=1, sticky="w")
        wrap = max(300, self.winfo_width() - 270) if self.winfo_width() > 10 else 460
        label = ctk.CTkLabel(
            bubble,
            text="● ● ●" if typing else text,
            font=ctk.CTkFont(size=13),
            text_color=MUTED if typing else WHITE,
            wraplength=wrap, justify="left",
        )
        label.pack(padx=14, pady=9)

        tag = "Assistente  " + datetime.now().strftime("%H:%M")
        ctk.CTkLabel(w, text=tag, font=ctk.CTkFont(size=10),
                     text_color=MUTED).grid(row=1, column=1, sticky="w", pady=(2, 4))

        if escalation:
            self._add_escalation_button(w)

        self._scroll_bottom()
        return w

    def _add_escalation_button(self, parent):
        btn = ctk.CTkButton(
            parent, text="📞 Connetti a operatore umano",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=WARNING, hover_color="#D97706", text_color=DARK,
            height=32, corner_radius=16,
            command=self._connect_operator,
        )
        btn.grid(row=2, column=1, sticky="w", pady=(6, 4))

    def _connect_operator(self):
        self.escalated = True
        self.kpi.log_response(0, escalated=True)
        self._add_system_message(
            "🔴 Stai per essere connesso a un operatore umano. "
            "Tempo medio di attesa: 2-5 minuti. "
            "Un agente ti contatterà a breve via chat o email."
        )

    def _add_system_message(self, text: str):
        row = self.chat_frame.grid_size()[1]
        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=14, pady=(8, 0))
        w.grid_columnconfigure(0, weight=1)
        bubble = ctk.CTkFrame(w, fg_color="#1a2a1a", corner_radius=8,
                               border_width=1, border_color=SUCCESS)
        bubble.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(bubble, text=text, font=ctk.CTkFont(size=12),
                     text_color=SUCCESS, wraplength=500, justify="center",
                     ).pack(padx=14, pady=8)
        self._scroll_bottom()

    def _scroll_bottom(self):
        self.after(60, lambda: self.chat_frame._parent_canvas.yview_moveto(1.0))

    # ── Send Logic ─────────────────────────────────────────────────────────────

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
        t0 = time.time()
        escalation = False
        try:
            if self.backend_var.get() == "Anthropic (Cloud)":
                reply = self._call_anthropic()
            else:
                reply = self._call_ollama()
            if "[ESCALATION]" in reply:
                escalation = True
                reply = reply.replace("[ESCALATION]", "").strip()
        except Exception as e:
            reply = f"⚠️ Errore di comunicazione: {e}\nSi prega di riprovare o contattare il supporto."

        elapsed = (time.time() - t0) * 1000
        self.kpi.log_response(elapsed, escalated=escalation)
        self.history.append({"role": "assistant", "content": reply})
        self.after(0, lambda: self._replace_typing(typing_w, reply, escalation))

    def _call_anthropic(self) -> str:
        resp = self.anthropic_cl.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=self.history,
        )
        return resp.content[0].text

    def _call_ollama(self) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history
        resp = self.ollama_client.chat.completions.create(
            model=self.model_var.get(),
            messages=messages,
            max_tokens=512,
        )
        return resp.choices[0].message.content

    def _replace_typing(self, typing_w, reply: str, escalation: bool = False):
        grid_info = typing_w.grid_info()
        row = grid_info.get("row", 0)
        typing_w.destroy()

        w = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        w.grid(row=row, column=0, sticky="ew", padx=14, pady=(8, 0))
        w.grid_columnconfigure(1, weight=1)

        color = WARNING if escalation else CARD2
        av = ctk.CTkFrame(w, fg_color=PRIMARY, width=34, height=34, corner_radius=10)
        av.grid(row=0, column=0, sticky="n", padx=(0, 10))
        av.grid_propagate(False)
        ctk.CTkLabel(av, text="🤖", font=ctk.CTkFont(size=16)
                     ).place(relx=0.5, rely=0.5, anchor="center")

        wrap = max(300, self.winfo_width() - 270) if self.winfo_width() > 10 else 460
        bubble = ctk.CTkFrame(w, fg_color=color, corner_radius=16)
        bubble.grid(row=0, column=1, sticky="ew")
        ctk.CTkLabel(
            bubble, text=reply,
            font=ctk.CTkFont(size=13), text_color=WHITE,
            wraplength=wrap, justify="left",
        ).pack(padx=14, pady=9)

        tag = "Assistente  " + datetime.now().strftime("%H:%M")
        ctk.CTkLabel(w, text=tag, font=ctk.CTkFont(size=10),
                     text_color=MUTED).grid(row=1, column=1, sticky="w", pady=(2, 4))

        if escalation:
            self._add_escalation_button(w)

        self.send_btn.configure(state="normal")
        self._scroll_bottom()

    def _clear_chat(self):
        self.history.clear()
        for child in self.chat_frame.winfo_children():
            child.destroy()
        self._add_bot_message(WELCOME)

    # ── KPI Panel ──────────────────────────────────────────────────────────────

    def _show_kpi(self):
        kpi = self.kpi.summary()
        win = ctk.CTkToplevel(self)
        win.title("📊 KPI – Sessione corrente")
        win.geometry("400x340")
        win.configure(fg_color=DARK)
        win.grab_set()

        ctk.CTkLabel(win, text="📊 KPI Dashboard",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color=WHITE
                     ).pack(pady=(20, 4))
        ctk.CTkLabel(win, text="Sessione corrente",
                     font=ctk.CTkFont(size=12), text_color=MUTED
                     ).pack(pady=(0, 16))

        rows = [
            ("💬 Messaggi totali",   str(kpi["total_messages"])),
            ("📞 Escalation",        str(kpi["escalations"])),
            ("⚡ Risposta media",    f"{kpi['avg_response_ms']} ms"),
            ("🔴 Risposta max",      f"{kpi['max_response_ms']} ms"),
            ("🎯 Target (<3000 ms)", "✅ OK" if kpi["avg_response_ms"] < 3000 else "❌ Superato"),
        ]
        for label, value in rows:
            row = ctk.CTkFrame(win, fg_color=CARD, corner_radius=8)
            row.pack(fill="x", padx=20, pady=4)
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=13),
                         text_color=WHITE).pack(side="left", padx=14, pady=10)
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=13, weight="bold"),
                         text_color=PRIMARY).pack(side="right", padx=14, pady=10)

        ctk.CTkButton(
            win, text="💾 Salva Log", fg_color=SUCCESS, hover_color="#059669",
            font=ctk.CTkFont(size=13), command=lambda: (self.kpi.save(), win.destroy()),
        ).pack(pady=16)

    def _show_api_key_settings(self):
        win = ctk.CTkToplevel(self)
        win.title("API Key Settings")
        win.geometry("420x260")
        win.resizable(False, False)
        win.configure(fg_color=DARK)
        win.grab_set()

        ctk.CTkLabel(win, text="Anthropic API Key",
                     font=ctk.CTkFont(size=15, weight="bold"), text_color=WHITE
                     ).pack(pady=(20, 4))

        has_key = load_api_key() is not None
        status_text  = "✔ Chiave salvata" if has_key else "✘ Nessuna chiave salvata"
        status_color = SUCCESS if has_key else DANGER
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
            fg_color=CARD2, border_color=BORDER, text_color=WHITE,
        )
        key_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))

        visible = ctk.BooleanVar(value=False)
        def _toggle():
            key_entry.configure(show="" if visible.get() else "*")
        ctk.CTkCheckBox(
            entry_frame, text="Mostra", variable=visible,
            font=ctk.CTkFont(size=11), text_color="#AAA",
            fg_color=PRIMARY, hover_color=SECONDARY,
            command=_toggle,
        ).pack(side="left")

        msg_lbl = ctk.CTkLabel(win, text="", font=ctk.CTkFont(size=11))
        msg_lbl.pack(pady=(8, 0))

        def _save():
            key = key_var.get().strip()
            if not key:
                msg_lbl.configure(text="Inserisci una chiave valida.", text_color=DANGER)
                return
            save_api_key(key)
            self.anthropic_cl = anthropic.Anthropic(api_key=key)
            status_lbl.configure(text="✔ Chiave salvata", text_color=SUCCESS)
            msg_lbl.configure(text="Chiave cifrata e salvata!", text_color=SUCCESS)
            key_entry.delete(0, "end")

        def _delete():
            delete_api_key()
            self.anthropic_cl = anthropic.Anthropic()
            status_lbl.configure(text="✘ Nessuna chiave salvata", text_color=DANGER)
            msg_lbl.configure(text="Chiave rimossa.", text_color=MUTED)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=16)
        ctk.CTkButton(btn_frame, text="Salva", width=110, height=34,
                      fg_color=PRIMARY, hover_color=SECONDARY, font=ctk.CTkFont(size=13),
                      command=_save).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Elimina", width=110, height=34,
                      fg_color=CARD2, hover_color="#555", font=ctk.CTkFont(size=13),
                      command=_delete).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Chiudi", width=80, height=34,
                      fg_color=BORDER, hover_color="#444", font=ctk.CTkFont(size=13),
                      command=win.destroy).pack(side="left", padx=6)

    def on_close(self):
        self.kpi.save()
        self.destroy()


# ── Entry Point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = EnterpriseChatApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
