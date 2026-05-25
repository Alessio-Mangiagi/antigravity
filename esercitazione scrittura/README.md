# Memorun

App per imparare la tecnica delle **10 dita** sulla tastiera QWERTY italiana.  
Costruita con Python + CustomTkinter.

---

## Avvio rapido

```bash
python main.py
```

---

## Come si usa

1. Scegli la **difficoltà** dalla schermata iniziale (Facile / Medio / Difficile)
2. Digita il testo mostrato nel riquadro superiore
3. Il **timer parte automaticamente** al primo tasto premuto
4. Completa il testo per vedere WPM, precisione e confronto con il record

---

## Feedback visivo durante la digitazione

| Stato carattere | Colore normale | Colore daltonismo |
|----------------|---------------|-------------------|
| Corretto        | Verde          | Celeste (#56B4E9) |
| Errato          | Rosso          | Arancione (#FE6100) |
| Posizione attuale (cursore) | Blu | Giallo (#F0E442) |
| Non ancora raggiunto | Grigio | Grigio |

---

## Tecnica delle 10 dita

Ogni dito è responsabile di **colonne fisse** della tastiera.  
Il tasto successivo da premere viene **evidenziato** sulla tastiera visiva.

| Dito              | Tasti assegnati          |
|-------------------|--------------------------|
| Mignolo sinistro  | Q · A · Z                |
| Anulare sinistro  | W · S · X                |
| Medio sinistro    | E · D · C                |
| Indice sinistro   | R · F · V  e  T · G · B |
| Indice destro     | Y · H · N  e  U · J · M |
| Medio destro      | I · K                    |
| Anulare destro    | O · L                    |
| Mignolo destro    | P                        |
| Pollici           | Barra spazio             |

### Regole fondamentali

- **Posizione di riposo:** dita su `A S D F` (mano sinistra) e `J K L` (mano destra)
- Tieni i **polsi sollevati** dalla scrivania
- **Non guardare la tastiera** — usa la tastiera visiva nell'app come guida
- Priorità alla **precisione**: la velocità arriva con la pratica

---

## Statistiche

Salvate automaticamente in `~/.typing_tutor_stats.json` dopo ogni esercizio completato.

| Campo          | Descrizione                                      |
|----------------|--------------------------------------------------|
| `sessions`     | Numero totale di esercizi completati             |
| `best_wpm`     | Record personale di velocità                     |
| `total_wpm`    | Somma dei WPM (usata per calcolare la media)     |
| `total_chars`  | Totale caratteri digitati in tutti gli esercizi  |

---

## Modalità Daltonismo

Attivabile con l'interruttore **"Modalita Daltonismo"** nella schermata iniziale.

Usa la palette **Okabe-Ito**, progettata per essere distinguibile da persone con:
- **Deuteranopia** (difficoltà a distinguere rosso-verde, la più comune)
- **Protanopia** (assenza dei fotorecettori per il rosso)

La palette sostituisce verde→celeste e rosso→arancione sia nella tastiera visiva che nel feedback di digitazione.  
L'impostazione viene **salvata automaticamente** e ricordata alle sessioni successive.

---

## Livelli WPM indicativi

| Livello        | WPM      |
|----------------|----------|
| Principiante   | < 20     |
| In miglioramento | 20–40  |
| Buono          | 40–60    |
| Avanzato       | 60–80    |
| Esperto        | 80+      |

> **Formula WPM:** ogni 5 caratteri (spazi inclusi) contano come 1 parola standard.

---

## Struttura del progetto

```
├── main.py            # Entry point
├── app.py             # Finestra principale + navigazione
├── config.py          # Testi, layout tastiera, colori dita
├── settings.py        # Preferenze utente (daltonismo, ecc.)
├── stats.py           # Caricamento/salvataggio statistiche
├── README.md          # Questo file
├── frames/
│   ├── home.py        # Schermata iniziale
│   ├── practice.py    # Esercizio di digitazione
│   ├── result.py      # Risultati post-esercizio
│   ├── custom_text.py # Inserimento testo personalizzato
│   └── readme_view.py # Visualizzatore README in-app
└── sito/
    ├── landing.html   # Landing page
    ├── style.css      # Stili
    └── main.js        # Animazioni e interazioni
```
