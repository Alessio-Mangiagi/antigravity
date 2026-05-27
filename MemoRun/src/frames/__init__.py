# =============================================================================
# frames/__init__.py — Esporta tutte le schermate dell'applicazione
# Permette di importare con: from frames import HomeFrame, PracticeFrame, ResultFrame
# =============================================================================

from .home        import HomeFrame
from .practice    import PracticeFrame
from .result      import ResultFrame
from .readme_view import ReadmeFrame
from .custom_text import CustomTextFrame
from .steno       import StenoFrame

__all__ = ["HomeFrame", "PracticeFrame", "ResultFrame", "ReadmeFrame", "CustomTextFrame", "StenoFrame"]

# "><(((º> sabusabu <º)))><"
