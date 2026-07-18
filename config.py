"""Backward-compatible configuration exports."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from lor_rag.config import Settings, get_settings

__all__ = ["Settings", "get_settings"]
