from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class LORIndexer:
    def __init__(self, file_path: str = "sample_lor.json", index_path: str = "lor_index.faiss"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.file_path = file_path
        self.index_path = index_path
        self.templates = self.load_templates()
        self.index = None
        self.embeddings: list[np.ndarray] = []

    def load_templates(self) -> list[dict[str, Any]]:
        with open(self.file_path, encoding="utf-8") as f:
            return json.load(f)

    def create_index(self) -> None:
        self.embeddings = [self.model.encode(t["template"]) for t in self.templates]
        if not self.embeddings:
            raise ValueError("No templates available to index.")

        vectors = np.array(self.embeddings).astype("float32")
        faiss.normalize_L2(vectors)
        dimension = vectors.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(vectors)
        faiss.write_index(self.index, self.index_path)

    def load_index(self) -> None:
        index_file = Path(self.index_path)
        if index_file.exists():
            self.index = faiss.read_index(str(index_file))
        else:
            self.create_index()

    def search_match(self, input_text: str) -> tuple[int, int]:
        if self.index is None:
            self.load_index()

        query_embedding = self.model.encode(input_text).reshape(1, -1).astype("float32")
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, 1)

        match_index = int(indices[0][0])
        similarity_score = float(scores[0][0])
        normalized_score = int(max(1, min(10, round(similarity_score * 10))))

        return match_index, normalized_score

    def get_template(self, index: int) -> dict[str, Any]:
        return self.templates[index]


if __name__ == "__main__":
    indexer = LORIndexer()
    indexer.create_index()
    print("FAISS Index created successfully.")
