from pathlib import Path
import sys

# Ensure root directory is accessible for imports
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from ice_cream_rev import MainWindow, main

__all__ = ["MainWindow", "main"]
