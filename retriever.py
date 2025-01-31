import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from llm_helper import llm

class LORRetriever:
    def __init__(self, file_path="data/lor_templates.json", index_path="lor_index.faiss"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index(index_path)
        self.templates = self.load_templates()

    def load_templates(self):
        with open("data/lor_templates.json", encoding="utf-8") as f:
            return json.load(f)

    def search(self, query, top_k=2):
        query_embedding = self.model.encode(query).astype("float32").reshape(1, -1)
        distances, indices = self.index.search(query_embedding, top_k)
        results = [self.templates[idx] for idx in indices[0] if idx < len(self.templates)]
        return results

    def generate_lor(self, user_inputs):
        query = " ".join(user_inputs.values())  # Create query 
        examples = self.search(query)

        prompt = self.build_prompt(user_inputs, examples)
        response = llm.invoke(prompt)
        return response.content

    def build_prompt(self, inputs, examples):
        base = "Generate a recommendation letter using the following details:\n"
        for key, value in inputs.items():
            base += f"- {key.replace('_', ' ').title()}: {value}\n"

        if examples:
            base += "\nFollow this template structure:\n"
            for example in examples:
                base += f"\nExample:\n{example['template']}\n"

        return base

retriever = LORRetriever()
