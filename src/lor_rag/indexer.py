"""Template indexing and similarity search utilities."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

LOGGER = logging.getLogger(__name__)


class LORIndexer:
    """Create and query a FAISS index for letter templates."""

    def __init__(self, file_path: str | Path | None = None, index_path: str | Path | None = None) -> None:
        root_dir = Path(__file__).resolve().parents[2]
        self.file_path = Path(file_path) if file_path else root_dir / "sample_lor.json"
        self.index_path = Path(index_path) if index_path else root_dir / "lor_index.faiss"
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.templates = self.load_templates()
        self.index: faiss.Index | None = None

    def load_templates(self) -> List[Dict[str, Any]]:
        """Load template records from JSON."""

        try:
            with self.file_path.open(encoding="utf-8") as file:
                return json.load(file)
        except (OSError, json.JSONDecodeError) as exc:
            LOGGER.exception("Failed to load templates from %s", self.file_path)
            raise RuntimeError(f"Could not read templates from {self.file_path}") from exc

    def create_index(self) -> None:
        """Build and persist the FAISS index from templates."""

        embeddings = [self.model.encode(template["template"]) for template in self.templates]
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))
        faiss.write_index(self.index, str(self.index_path))

    def load_index(self) -> None:
        """Load existing index or create a new one when unavailable."""

        try:
            self.index = faiss.read_index(str(self.index_path))
        except RuntimeError:
            LOGGER.warning("Index not found at %s. Creating a new index.", self.index_path)
            self.create_index()

    def search_match(self, input_text: str) -> Tuple[int, int]:
        """Return best matching template index and a normalized 1-10 similarity score."""

        if self.index is None:
            self.load_index()

        if self.index is None:
            raise RuntimeError("FAISS index is not initialized.")

        query_embedding = self.model.encode(input_text).reshape(1, -1).astype("float32")
        distances, indices = self.index.search(query_embedding, 1)

        match_index = int(indices[0][0])
        similarity_score = float(distances[0][0])

        # Convert L2 distance to a simple 1-10 scale for user-friendly rating.
        normalized_score = max(1, 10 - int(similarity_score))
        return match_index, normalized_score

    def get_template(self, index: int) -> Dict[str, Any]:
        """Return template metadata by index."""

        return self.templates[index]
