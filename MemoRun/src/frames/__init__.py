# =============================================================================
# frames/__init__.py — Esporta tutte le schermate dell'applicazione
# Permette di importare con: from frames import HomeFrame, PracticeFrame, ResultFrame
# =============================================================================

from frames.home        import HomeFrame
from frames.practice    import PracticeFrame
from frames.result      import ResultFrame
from frames.readme_view import ReadmeFrame
from frames.custom_text import CustomTextFrame

__all__ = ["HomeFrame", "PracticeFrame", "ResultFrame", "ReadmeFrame", "CustomTextFrame"]
