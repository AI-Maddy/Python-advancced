"""Root conftest — ensure all pattern/idiom directories are on sys.path."""
from __future__ import annotations

import sys
from pathlib import Path

# Add each pattern/idiom directory to sys.path so tests can import main modules
root = Path(__file__).parent

for pattern_dir in root.rglob("tests"):
    parent = pattern_dir.parent
    if str(parent) not in sys.path:
        sys.path.insert(0, str(parent))
