#!/usr/bin/env python3
"""
ocr_pdf.py — Estrai testo da PDF scansionati usando pytesseract

Utilizzo:
    python ocr_pdf.py documento.pdf
    python ocr_pdf.py documento.pdf --lingua ita
    python ocr_pdf.py documento.pdf --lingua ita --dpi 400
    python ocr_pdf.py documento.pdf --pagine 1-3
    python ocr_pdf.py documento.pdf --output risultato.txt

Dipendenze:
    pip install pytesseract pdf2image Pillow
    sudo apt install tesseract-ocr tesseract-ocr-ita poppler-utils   # Linux
    brew install tesseract poppler                                     # macOS
"""

import argparse
import sys
import os
from pathlib import Path


def controlla_dipendenze():
    """Verifica che tutte le librerie e i tool siano installati."""
    errori = []

    try:
        import pytesseract
        pytesseract.get_tesseract_version()
    except ImportError:
        errori.append("pytesseract non installato → pip install pytesseract")
    except pytesseract.TesseractNotFoundError:
        errori.append("Tesseract non trovato → installa tesseract-ocr (vedi intestazione file)")

    try:
        from pdf2image import convert_from_path
    except ImportError:
        errori.append("pdf2image non installato → pip install pdf2image")

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        errori.append("Pillow non installato → pip install Pillow")

    if errori:
        print("❌ Dipendenze mancanti:\n")
        for e in errori:
            print(f"   • {e}")
        sys.exit(1)


def analizza_pagine(stringa_pagine, totale):
    """
    Converte una stringa come '1-3,5,7' in una lista di indici (0-based).
    Restituisce None se la stringa è vuota (tutte le pagine).
    """
    if not stringa_pagine:
        return None

    indici = set()
    for parte in stringa_pagine.split(","):
        parte = parte.strip()
        if "-" in parte:
            inizio, fine = parte.split("-", 1)
            inizio = max(1, int(inizio.strip()))
            fine = min(totale, int(fine.strip()))
            indici.update(range(inizio, fine + 1))
        else:
            n = int(parte)
            if 1 <= n <= totale:
                indici.add(n)

    return sorted(indici)


def ocr_pdf(
    percorso_pdf: str,
    lingua: str = "ita",
    dpi: int = 300,
    pagine: str = None,
    percorso_output: str = None,
    modalita_psm: int = 3,
):
    """
    Esegue OCR su un PDF scansionato e restituisce il testo estratto.

    Args:
        percorso_pdf:    Percorso del file PDF.
        lingua:          Codice lingua Tesseract (es. 'ita', 'eng', 'ita+eng').
        dpi:             Risoluzione di rasterizzazione (300 consigliato).
        pagine:          Stringa pagine da elaborare, es. '1-3,5'. None = tutte.
        percorso_output: Se specificato, salva il testo in questo file .txt.
        modalita_psm:    Page Segmentation Mode di Tesseract (3 = automatico).

    Returns:
        str: Testo estratto da tutte le pagine elaborate.
    """
    import pytesseract
    from pdf2image import convert_from_path
    from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError

    pdf = Path(percorso_pdf)
    if not pdf.exists():
        print(f"❌ File non trovato: {percorso_pdf}")
        sys.exit(1)
    if pdf.suffix.lower() != ".pdf":
        print(f"⚠️  Il file non sembra un PDF: {percorso_pdf}")

    print(f"\n📄 File     : {pdf.name}")
    print(f"🌐 Lingua   : {lingua}")
    print(f"🖨️  DPI      : {dpi}")

    # --- Converti PDF in immagini ---
    print("\n⏳ Conversione pagine in corso...")
    try:
        immagini = convert_from_path(str(pdf), dpi=dpi)
    except PDFInfoNotInstalledError:
        print("❌ poppler non trovato. Installa poppler-utils (Linux) o poppler (macOS).")
        sys.exit(1)
    except PDFPageCountError as e:
        print(f"❌ Impossibile leggere il PDF: {e}")
        sys.exit(1)

    totale_pagine = len(immagini)
    print(f"✅ Pagine trovate: {totale_pagine}")

    # --- Seleziona pagine ---
    selezione = analizza_pagine(pagine, totale_pagine)
    if selezione:
        print(f"📑 Pagine selezionate: {selezione}")
        immagini_da_elaborare = [(selezione[i], immagini[selezione[i] - 1]) for i in range(len(selezione))]
    else:
        immagini_da_elaborare = [(i + 1, img) for i, img in enumerate(immagini)]

    # --- Configurazione Tesseract ---
    config_tesseract = f"--psm {modalita_psm}"

    # --- OCR pagina per pagina ---
    print("\n🔍 OCR in corso...\n")
    testi = []

    for numero_pag, immagine in immagini_da_elaborare:
        print(f"   Pagina {numero_pag}/{totale_pagine}...", end=" ", flush=True)

        testo = pytesseract.image_to_string(
            immagine,
            lang=lingua,
            config=config_tesseract,
        )

        testo = testo.strip()
        parole = len(testo.split()) if testo else 0
        print(f"({parole} parole)")

        intestazione = f"\n{'='*60}\n PAGINA {numero_pag}\n{'='*60}\n"
        testi.append(intestazione + testo)

    testo_finale = "\n".join(testi)

    # --- Output ---
    if percorso_output:
        output = Path(percorso_output)
        output.write_text(testo_finale, encoding="utf-8")
        print(f"\n💾 Testo salvato in: {output.resolve()}")
    else:
        # Default: salva accanto al PDF con stesso nome
        output_default = pdf.with_suffix(".txt")
        output_default.write_text(testo_finale, encoding="utf-8")
        print(f"\n💾 Testo salvato in: {output_default.resolve()}")

    parole_totali = len(testo_finale.split())
    caratteri_totali = len(testo_finale)
    print(f"📊 Totale: {parole_totali} parole, {caratteri_totali} caratteri")

    return testo_finale


def main():
    parser = argparse.ArgumentParser(
        description="Estrai testo da PDF scansionati con pytesseract",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python ocr_pdf.py documento.pdf
  python ocr_pdf.py documento.pdf --lingua eng
  python ocr_pdf.py documento.pdf --lingua ita+eng --dpi 400
  python ocr_pdf.py documento.pdf --pagine 1-5
  python ocr_pdf.py documento.pdf --pagine 1,3,5-8
  python ocr_pdf.py documento.pdf --output /tmp/testo.txt

Lingue disponibili (se installate):
  ita  → Italiano
  eng  → Inglese
  fra  → Francese
  deu  → Tedesco
  spa  → Spagnolo
  Combina più lingue: --lingua ita+eng
        """,
    )
    parser.add_argument("pdf", help="Percorso del file PDF")
    parser.add_argument("--lingua", default="ita", help="Lingua OCR (default: ita)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI rasterizzazione (default: 300)")
    parser.add_argument("--pagine", default=None, help="Pagine da elaborare, es. '1-3,5'")
    parser.add_argument("--output", default=None, help="File di output .txt")
    parser.add_argument(
        "--psm",
        type=int,
        default=3,
        help="Page Segmentation Mode Tesseract (default: 3 = auto)",
    )

    args = parser.parse_args()

    controlla_dipendenze()
    ocr_pdf(
        percorso_pdf=args.pdf,
        lingua=args.lingua,
        dpi=args.dpi,
        pagine=args.pagine,
        percorso_output=args.output,
        modalita_psm=args.psm,
    )


if __name__ == "__main__":
    main()
