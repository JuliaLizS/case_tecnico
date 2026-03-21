import sqlite3
from database.connect import create_connection
from embeddings import generate_embedding
from vector_store import vector_store
from models import (CreateUserRequest, UserResponse, SearchUserRequest)
import logging

class UserService:

    # criar usuario
    def create_user(self, data: CreateUserRequest) -> int:
        conn = create_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                '''
                INSERT INTO users (name, email, description)
                VALUES (?, ?, ?)
                ''', 
                (data.name, data.email, data.description)
            )
            user_id = cur.lastrowid
            conn.commit()

            # Gerar embedding
            embedding = generate_embedding(data.description)

            # Salvar vetor
            vector_store.add_vector(user_id, embedding)
            logging.info(f"Usuário criado com ID {user_id} e embedding adicionado ao vetor store.")
            return user_id
        
        except sqlite3.Error as e:
            logging.error(f"Erro ao criar o usuário: {e}")
        finally:
            conn.close()

    # buscar usuario por id
    def get_user(self, user_id: int) -> UserResponse | None:
        conn = create_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                'SELECT id, name, email, description FROM users WHERE id = ?', 
                (user_id,)
            )

            row = cur.fetchone()

            if not row:
                logging.warning(f"Usuário com ID {user_id} não encontrado.")
                return None
            
            return UserResponse(
                id=row[0], 
                name=row[1], 
                email=row[2], 
                description=row[3]
            )

        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar o usuário: {e}")
        finally:
            conn.close()

    # busca semantica
    def search_users(self, data: SearchUserRequest):
        query_emb = generate_embedding(data.query)

        results = vector_store.search(query_emb, data.top_k)

        if not results:
            logging.info("Nenhum usuário encontrado para a consulta.")
            return []
        
        conn = create_connection()
        cur = conn.cursor()

        final_output = []

        try:
            for user_id, score in results:
                cur.execute(
                    'SELECT id, name, email, description FROM users WHERE id = ?', 
                    (user_id,)
                )
                row = cur.fetchone()
                
                if not row:
                    logging.warning(f"Usuário com ID {user_id} não encontrado durante a busca semântica.")
                    continue

                final_output.append({

                    "id": row[0], 
                    "name": row[1], 
                    "email": row[2], 
                    "description": row[3],
                    "score": score
                })

            final_output.sort(key=lambda x: x["score"])
            return final_output     
    
        except sqlite3.Error as e:
            logging.error(f"Erro ao buscar o usuário com ID {user_id}: {e}")
        
        finally:
            conn.close()


user_service = UserService()