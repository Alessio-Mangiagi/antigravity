# =============================================================================
# config.py — Costanti globali dell'applicazione
# Contiene: testi di esercitazione, layout tastiera QWERTY,
#           mappatura dita, colori e nomi dei diti.
# Modificare qui per aggiungere testi o cambiare i colori.
# =============================================================================

# ─── Testi di esercitazione suddivisi per difficoltà ─────────────────────────
TEXTS = {
    "Facile": [
        "il gatto dorme sul tappeto rosso",
        "la casa e grande e molto bella",
        "oggi il sole splende nel cielo",
        "il cane corre veloce nel parco",
        "mangio una mela fresca ogni giorno",
        "il libro e posato sul tavolo",
        "la luna brilla nella notte scura",
        "bevo un caffe caldo ogni mattina",
        "il treno parte dalla stazione presto",
        "la bambina sorride e gioca felice",
        "il mare e blu e molto profondo",
        "vado a scuola ogni giorno di settimana",
    ],
    "Medio": [
        "la programmazione richiede pratica costante e molta dedizione per migliorare",
        "il computer moderno e diventato uno strumento potente e indispensabile",
        "studiare dattilografia migliora la velocita di scrittura in modo significativo",
        "scrivere con tutte e dieci le dita aumenta notevolmente la produttivita",
        "ogni giorno di pratica porta grandi miglioramenti nella velocita di battitura",
        "la tastiera qwerty e lo standard piu diffuso in tutto il mondo occidentale",
        "imparare a digitare velocemente e una competenza fondamentale nel mondo moderno",
        "la postura corretta durante la digitazione previene dolori alle mani e alla schiena",
        "i polsi devono rimanere sollevati mentre si digita per evitare infortuni",
        "ogni dito e responsabile di specifici tasti sulla tastiera italiana standard",
    ],
    "Difficile": [
        "La velocita di battitura si misura in parole per minuto e un dattilografo esperto raggiunge facilmente le ottanta parole al minuto con grande precisione e costanza nel tempo",
        "Imparare a digitare senza guardare la tastiera e fondamentale per diventare un professionista e aumentare notevolmente la produttivita lavorativa in qualsiasi ambiente di lavoro moderno",
        "La tecnica delle dieci dita prevede che ogni dito sia responsabile di specifici tasti riducendo i movimenti inutili e aumentando la velocita complessiva di digitazione professionale",
        "Un buon dattilografo mantiene sempre i polsi sollevati dalla scrivania e le dita curve sopra i tasti garantendo una postura ergonomica e prevenendo infortuni nel lungo periodo",
        "La pratica costante e metodica della dattilografia porta risultati straordinari nel corso delle settimane trasformando una scrittura lenta e incerta in una digitazione fluida e sicura",
    ],
}

# ─── Layout fisico tastiera QWERTY (righe dall'alto verso il basso) ───────────
KEYBOARD_ROWS = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],   # riga superiore
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],         # home row
    ["z", "x", "c", "v", "b", "n", "m"],                   # riga inferiore
]

# ─── Colore assegnato a ogni dito — palette normale ───────────────────────────
FINGER_COLORS = {
    "mignolo_sx": "#e74c3c",   # rosso
    "anulare_sx": "#e67e22",   # arancione
    "medio_sx":   "#f1c40f",   # giallo
    "indice_sx":  "#2ecc71",   # verde
    "indice_dx":  "#3498db",   # blu
    "medio_dx":   "#9b59b6",   # viola
    "anulare_dx": "#1abc9c",   # verde acqua
    "mignolo_dx": "#e91e63",   # rosa
    "pollice":    "#95a5a6",   # grigio (barra spazio)
}

# ─── Palette Okabe-Ito per daltonismo (deuteranopia / protanopia) ─────────────
# Evita coppie rosso/verde che risultano indistinguibili per i daltonici.
# Fonte: https://jfly.uni-koeln.de/color/
FINGER_COLORS_COLORBLIND = {
    "mignolo_sx": "#E69F00",   # arancione caldo
    "anulare_sx": "#56B4E9",   # celeste
    "medio_sx":   "#F0E442",   # giallo
    "indice_sx":  "#009E73",   # verde-blu
    "indice_dx":  "#0072B2",   # blu scuro
    "medio_dx":   "#D55E00",   # arancione bruciato
    "anulare_dx": "#CC79A7",   # viola-rosa
    "mignolo_dx": "#648FFF",   # blu lavanda
    "pollice":    "#BBBBBB",   # grigio chiaro
}

# ─── Colori feedback testo nell'area di digitazione ───────────────────────────
# 'normal'     → verde/rosso/blu  (palette classica)
# 'colorblind' → celeste/arancione/giallo  (Okabe-Ito)
TEXT_COLORS = {
    "normal": {
        "correct_fg": "#a6e3a1",   # verde → carattere corretto
        "wrong_fg":   "#1e1e2e",
        "wrong_bg":   "#f38ba8",   # rosso → errore
        "cursor_fg":  "#1e1e2e",
        "cursor_bg":  "#89b4fa",   # blu → posizione attuale
        "pending_fg": "#45475a",   # grigio → non ancora digitato
    },
    "colorblind": {
        "correct_fg": "#56B4E9",   # celeste → carattere corretto
        "wrong_fg":   "#1e1e2e",
        "wrong_bg":   "#FE6100",   # arancione → errore
        "cursor_fg":  "#1e1e2e",
        "cursor_bg":  "#F0E442",   # giallo → posizione attuale
        "pending_fg": "#45475a",
    },
}


def get_finger_colors(colorblind: bool = False) -> dict:
    """Restituisce la palette colori dita in base alla modalità attiva."""
    return FINGER_COLORS_COLORBLIND if colorblind else FINGER_COLORS


def get_text_colors(colorblind: bool = False) -> dict:
    """Restituisce i colori del feedback testo in base alla modalità attiva."""
    return TEXT_COLORS["colorblind" if colorblind else "normal"]

# ─── Nome leggibile di ogni dito (mostrato nel suggerimento durante l'esercizio) ──
FINGER_NAMES = {
    "mignolo_sx": "Mignolo sinistro",
    "anulare_sx": "Anulare sinistro",
    "medio_sx":   "Medio sinistro",
    "indice_sx":  "Indice sinistro",
    "indice_dx":  "Indice destro",
    "medio_dx":   "Medio destro",
    "anulare_dx": "Anulare destro",
    "mignolo_dx": "Mignolo destro",
    "pollice":    "Pollice (spazio)",
}

# ─── Mappatura tasto → dito responsabile (tecnica 10 dita) ───────────────────
# Ogni lettera è assegnata al dito che la tecnica a 10 dita prescrive.
KEY_FINGER = {
    # Mignolo sinistro: colonna sinistra
    "q": "mignolo_sx", "a": "mignolo_sx", "z": "mignolo_sx",
    # Anulare sinistro
    "w": "anulare_sx", "s": "anulare_sx", "x": "anulare_sx",
    # Medio sinistro
    "e": "medio_sx",   "d": "medio_sx",   "c": "medio_sx",
    # Indice sinistro: copre due colonne (r-f-v e t-g-b)
    "r": "indice_sx",  "f": "indice_sx",  "v": "indice_sx",
    "t": "indice_sx",  "g": "indice_sx",  "b": "indice_sx",
    # Indice destro: copre due colonne (y-h-n e u-j-m)
    "y": "indice_dx",  "h": "indice_dx",  "n": "indice_dx",
    "u": "indice_dx",  "j": "indice_dx",  "m": "indice_dx",
    # Medio destro
    "i": "medio_dx",   "k": "medio_dx",
    # Anulare destro
    "o": "anulare_dx", "l": "anulare_dx",
    # Mignolo destro: colonna destra
    "p": "mignolo_dx",
    # Pollici → barra spazio
    " ": "pollice",
}
