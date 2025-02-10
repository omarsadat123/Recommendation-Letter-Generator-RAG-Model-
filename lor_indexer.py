import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class LORIndexer:
    def __init__(self, file_path="sample_lor.json", index_path="lor_index.faiss"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.file_path = file_path
        self.index_path = index_path
        self.templates = self.load_templates()
        self.index = None
        self.embeddings = []
        
    def load_templates(self):
        with open(self.file_path, encoding="utf-8") as f:
            return json.load(f)

    def create_index(self):
        self.embeddings = [self.model.encode(t["template"]) for t in self.templates]
        dimension = len(self.embeddings[0])
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype("float32"))
        faiss.write_index(self.index, self.index_path)

    def load_index(self):         # check index is exists or not.
        
        try:
            self.index = faiss.read_index(self.index_path)          
        except:
            self.create_index()

    def search_match(self, input_text):    #Searches and matching LOR and calculate rating.
        
        if self.index is None:
            self.load_index()

        query_embedding = self.model.encode(input_text).reshape(1, -1).astype("float32")
        Dis, Ind = self.index.search(query_embedding, 1)

        match_index = Ind[0][0]
        similarity_score = Dis[0][0]

       
        normalized_score = max(1, 10 - int(similarity_score))         # distance  1-10 rating

        return match_index, normalized_score

    def get_template(self, index):
        return self.templates[index]

if __name__ == "__main__":
    indexer = LORIndexer()
    indexer.create_index()
    print("FAISS Index created successfully.")
