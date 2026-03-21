# FAISS

import faiss
import numpy as np
import os
import json

# Utilizei um arquivo id_map.json para mapear posições do 
# índice FAISS para IDs reais, porque o FAISS não possui 
# suporte interno para metadata. Toda metadata permanece 
# corretamente armazenada no SQLite, mantendo a separação 
# de responsabilidades.”

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FAISS_DIR = os.path.join(BASE_DIR, 'faiss_index')
INDEX_FILE = os.path.join(FAISS_DIR, 'index.faiss')
IDMAP_FILE = os.path.join(FAISS_DIR, 'id_map.json')

EMBED_DIM = 384 

class VectorStore:
    # Carregar FAISS existente ou se não existir cria um novo
    def __init__(self):
        os.makedirs(FAISS_DIR, exist_ok=True)

        if os.path.exists(INDEX_FILE) and os.path.exists(IDMAP_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            with open(IDMAP_FILE, 'r') as f:
                self.id_map = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(EMBED_DIM)
            self.id_map = []
    
    # Persistencia - salvar o indice e o id_map
    def save_index(self):
        faiss.write_index(self.index, INDEX_FILE)
        with open(IDMAP_FILE, 'w') as f:
            json.dump(self.id_map, f)

    # Adiciona um vetor ao índice e mapea o ID do usuário
    def add_vector(self, user_id: int, embedding: np.ndarray):
        embedding = embedding.astype(np.float32)
        self.index.add(np.array([embedding]))
        self.id_map.append(user_id)
        self.save_index()

    # Busca vetorial usando o embedding de consulta e retorna os IDs e scores dos usuários mais próximos
    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        if len(self.id_map) == 0:
            return []
        
        query_embedding = query_embedding.astype(np.float32)
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        results = []

        for dist, idx in zip(distances[0], indices[0]):
            if idx < 0 or idx >= len(self.id_map):
                continue

            user_id = self.id_map[idx]
            results.append((user_id, float(dist)))
        
        return results

vector_store = VectorStore()