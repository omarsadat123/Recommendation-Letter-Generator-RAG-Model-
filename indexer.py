import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class LORIndexer:
    def __init__(self, file_path="data/lor_templates.json", index_path="lor_index.faiss"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  # embedding model
        self.file_path = file_path
        self.index_path = index_path
        self.templates = self.load_templates()
        self.index = None

    def load_templates(self):
        with open(self.file_path, encoding="utf-8") as f:
            return json.load(f)

    def create_index(self):
        embeddings = [self.model.encode(t["template"]) for t in self.templates]
        dimension = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))
        faiss.write_index(self.index, self.index_path)

    def run(self):
        print("Creating FAISS Index...")
        self.create_index()
        print("Index created and saved.")

if __name__ == "__main__":
    indexer = LORIndexer()
    indexer.run()
