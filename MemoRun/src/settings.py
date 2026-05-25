# =============================================================================
# settings.py — Preferenze utente (distinte dalle statistiche)
# File salvato in: ~/.typing_tutor_settings.json
# Preferenze attuali:
#   colorblind_mode  (bool) → attiva la palette Okabe-Ito per daltonismo
# =============================================================================

import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".typing_tutor_settings.json"

_DEFAULTS = {
    "colorblind_mode": False,
    "theme": "System",
}


def load_settings() -> dict:
    """Carica le preferenze dal file JSON. Merge con i default per gestire chiavi mancanti."""
    base = dict(_DEFAULTS)
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, encoding="utf-8") as f:
            base.update(json.load(f))
    return base


def save_settings(settings: dict) -> None:
    """Salva il dizionario delle preferenze nel file JSON."""
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)
