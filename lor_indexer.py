"""Backward-compatible import for the LOR indexer."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from lor_rag.indexer import LORIndexer

__all__ = ["LORIndexer"]
