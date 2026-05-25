# =============================================================================
# stats.py — Gestione delle statistiche utente
# Le statistiche sono salvate in un file JSON nella home dell'utente:
#   ~/.typing_tutor_stats.json
# Struttura del dizionario:
#   sessions    → numero totale di esercizi completati
#   best_wpm    → record personale di velocità (parole per minuto)
#   total_wpm   → somma dei WPM di tutte le sessioni (usata per calcolare la media)
#   total_chars → totale di caratteri digitati in tutti gli esercizi
# =============================================================================

import json
from pathlib import Path

# Percorso del file JSON nella cartella home dell'utente
STATS_FILE = Path.home() / ".memorun_stats.json"

# Struttura vuota usata al primo avvio (nessun dato salvato)
_DEFAULT_STATS = {
    "sessions":    0,
    "best_wpm":    0,
    "total_wpm":   0,
    "total_chars": 0,
}


def load_stats() -> dict:
    """Carica le statistiche dal file JSON. Restituisce i valori di default se il file non esiste."""
    if STATS_FILE.exists():
        with open(STATS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return dict(_DEFAULT_STATS)


def save_stats(stats: dict) -> None:
    """Salva il dizionario delle statistiche nel file JSON."""
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)


def update_stats(stats: dict, wpm: int, char_count: int) -> None:
    """Aggiorna le statistiche in-memory dopo un esercizio completato.
    Chiama save_stats() separatamente per persistere le modifiche."""
    stats["sessions"]    += 1
    stats["total_chars"] += char_count
    stats["total_wpm"]   += wpm
    if wpm > stats["best_wpm"]:
        stats["best_wpm"] = wpm


def average_wpm(stats: dict) -> int:
    """Calcola la media WPM. Restituisce 0 se non ci sono sessioni."""
    if stats["sessions"] == 0:
        return 0
    return int(stats["total_wpm"] / stats["sessions"])
