# MenmoRun

App per imparare la tecnica delle **10 dita** sulla tastiera QWERTY italiana.  
Costruita con Python + CustomTkinter.

---

## Avvio rapido

```bash
pip install -r requirements.txt
python main.py
```

---

## Come si usa

1. Scegli la **difficoltà** dalla schermata iniziale (Facile / Medio / Difficile / Personalizzato)
2. Digita il testo mostrato nel riquadro superiore
3. Il **timer parte automaticamente** al primo tasto premuto
4. Completa il testo per vedere WPM, precisione e confronto con il record

---

## Livelli di difficoltà

| Livello       | Testi                                | Caratteristiche              |
|---------------|--------------------------------------|------------------------------|
| Facile        | Frasi brevi (5–8 parole)             | Vocabolario semplice         |
| Medio         | Frasi complete (8–14 parole)         | Linguaggio più articolato    |
| Difficile     | Testi lunghi (20+ parole)            | Frasi complesse e tecniche   |
| Personalizzato | Il tuo testo (lunghezza libera)     | Incolla qualsiasi contenuto  |

### Modalità Parola per Parola

Nella modalità **Personalizzato** puoi scegliere tra:
- **Testo completo** — vedi l'intero testo e scrivi tutto di fila
- **Parola per parola** — compare una parola alla volta, premi Spazio per passare alla successiva

---

## Modalità Stenografica a 10 tasti

Accessibile dal pulsante **Stenografia** nella home, nella sezione *Modalità avanzata*.

Invece di premere un tasto alla volta, devi premere più tasti **contemporaneamente** (chord) per produrre una parola intera. La risoluzione avviene al rilascio dell'ultimo tasto.

**I 10 tasti usati:** la home row `A S D F G H J K L` + `SPAZIO`

### Campione di chord

| Chord (tasti simultanei) | Parola prodotta |
|--------------------------|-----------------|
| `A + D`                  | il              |
| `J + K`                  | la              |
| `D + F`                  | di              |
| `G + H`                  | che             |
| `S + K`                  | non             |
| `D + H`                  | per             |
| `F + K`                  | con             |
| `A + S + D`              | alla            |
| `G + H + J`              | nella           |
| `J + K + L`              | sono            |
| `D + G + K`              | questo          |
| `F + H + L`              | tutto           |
| `G + H + J`              | nella           |
| `A + K + L`              | quando          |

Il dizionario completo contiene **42 chord** per le parole italiane più frequenti.

### Statistiche stenografiche

Le statistiche mostrano **Chord / min** (chord corretti al minuto) e **Precisione %**.  
Il feedback è immediato: verde per chord corretto, rosso con lampeggio per chord errato (mostra quale parola avresti prodotto).

---

## Feedback visivo durante la digitazione

| Stato carattere | Colore normale | Colore daltonismo |
|----------------|---------------|-------------------|
| Corretto        | Verde          | Celeste (#56B4E9) |
| Errato          | Rosso          | Arancione (#FE6100) |
| Posizione attuale (cursore) | Blu | Giallo (#F0E442) |
| Non ancora raggiunto | Colore del dito | Colore del dito |

---

## Tecnica delle 10 dita

Ogni dito è responsabile di **colonne fisse** della tastiera.  
Il tasto successivo da premere viene **evidenziato** sulla tastiera visiva.

| Dito              | Tasti assegnati                  |
|-------------------|----------------------------------|
| Mignolo sinistro  | Q · A · Z                       |
| Anulare sinistro  | W · S · X                       |
| Medio sinistro    | E · D · C                       |
| Indice sinistro   | R · F · V  e  T · G · B         |
| Indice destro     | Y · H · N  e  U · J · M         |
| Medio destro      | I · K                           |
| Anulare destro    | O · L                           |
| Mignolo destro    | P · à · è · ì · ò · ù           |
| Pollici           | Barra spazio                    |

### Regole fondamentali

- **Posizione di riposo:** dita su `A S D F` (mano sinistra) e `J K L` (mano destra)
- Tieni i **polsi sollevati** dalla scrivania
- **Non guardare la tastiera** — usa la tastiera visiva nell'app come guida
- Priorità alla **precisione**: la velocità arriva con la pratica

---

## Statistiche

Salvate automaticamente in `~/.memorun_stats.json` dopo ogni esercizio completato.

| Campo          | Descrizione                                      |
|----------------|--------------------------------------------------|
| `sessions`     | Numero totale di esercizi completati             |
| `best_wpm`     | Record personale di velocità                     |
| `total_wpm`    | Somma dei WPM (usata per calcolare la media)     |
| `total_chars`  | Totale caratteri digitati in tutti gli esercizi  |

Puoi **azzerare le statistiche** dalla home: clicca il pulsante "Azzera statistiche" e digita `RESET` nella finestra di conferma.

---

## Modalità Daltonismo

Attivabile con l'interruttore **"Modalità Daltonismo"** nella schermata iniziale.

Usa la palette **Okabe-Ito**, progettata per essere distinguibile da persone con:
- **Deuteranopia** (difficoltà a distinguere rosso-verde, la più comune)
- **Protanopia** (assenza dei fotorecettori per il rosso)

La palette sostituisce verde→celeste e rosso→arancione sia nella tastiera visiva che nel feedback di digitazione.  
L'impostazione viene **salvata automaticamente** e ricordata alle sessioni successive.

---

## Tema

Selezionabile dalla home con il pulsante segmentato **Chiaro / Scuro / Sistema**.  
La scelta viene salvata e applicata all'avvio successivo.

---

## Scorciatoie da tastiera

| Tasto    | Azione                              |
|----------|-------------------------------------|
| `Escape` | Torna alla schermata iniziale       |

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
├── src/
│   ├── app.py         # Finestra principale + navigazione
│   ├── config.py      # Testi (~290), layout tastiera, colori dita
│   ├── settings.py    # Preferenze utente (daltonismo, tema)
│   ├── stats.py       # Caricamento/salvataggio statistiche
│   └── frames/
│       ├── home.py        # Schermata iniziale
│       ├── practice.py    # Esercizio di digitazione
│       ├── result.py      # Risultati post-esercizio
│       ├── custom_text.py # Inserimento testo personalizzato
│       ├── steno.py       # Modalità stenografica a 10 tasti (chord-based)
│       └── readme_view.py # Visualizzatore README in-app
├── sito/
│   ├── index.html     # Landing page
│   ├── style.css      # Stili
│   └── main.js        # Animazioni e interazioni
├── requirements.txt
└── README.md
```
