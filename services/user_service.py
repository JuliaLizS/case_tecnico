import sqlite3
import logging
from database.connect import create_connection
from database.database import create_table
from embeddings import generate_embedding
from vector_store import vector_store
from models import (CreateUserRequest, UserResponse, SearchUserRequest, ListUsersRequest)
from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

class UserService:

    def __init__(self):
        create_table()

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
            logger.info(
                "Usuário criado e embedding adicionado ao vector store",
                extra={"event": "user_create_success", "user_id": user_id}
            )
            return user_id
        
        except sqlite3.Error as e:
            conn.rollback()
            logger.error(
                "Erro ao criar usuário no banco",
                extra={"event": "user_create_db_error", "error": str(e)}
            )
            raise
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
                logger.warning(
                    "Usuário não encontrado na busca por ID",
                    extra={"event": "user_get_not_found", "user_id": user_id}
                )
                return None
            
            return UserResponse(
                id=row[0], 
                name=row[1], 
                email=row[2], 
                description=row[3]
            )

        except sqlite3.Error as e:
            logger.error(
                "Erro ao buscar usuário por ID no banco",
                extra={"event": "user_get_db_error", "user_id": user_id, "error": str(e)}
            )
            raise
        finally:
            conn.close()

    # busca semantica
    def search_users(self, data: SearchUserRequest):
        query_emb = generate_embedding(data.query)

        results = vector_store.search(query_emb, data.top_k)

        if not results:
            logger.info(
                "Busca semântica sem resultados",
                extra={"event": "search_users_empty", "top_k": data.top_k, "result_count": 0}
            )
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
                    logger.warning(
                        "Usuário referenciado no índice não encontrado no banco",
                        extra={"event": "search_users_user_missing", "user_id": user_id}
                    )
                    continue

                final_output.append({

                    "id": row[0], 
                    "name": row[1], 
                    "email": row[2], 
                    "description": row[3],
                    "score": score
                })

            final_output.sort(key=lambda x: x["score"])
            logger.info(
                "Busca semântica executada com sucesso",
                extra={"event": "search_users_success", "top_k": data.top_k, "result_count": len(final_output)}
            )
            return final_output     
    
        except sqlite3.Error as e:
            logger.error(
                "Erro ao consultar usuários durante busca semântica",
                extra={"event": "search_users_db_error", "error": str(e)}
            )
            raise
        
        finally:
            conn.close()


    # listar usuarios com paginacao
    def list_users(self, data: ListUsersRequest):
        conn = create_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                'SELECT id, name, email, description FROM users LIMIT ? OFFSET ?',
                (data.limit, data.offset)
            )
            rows = cur.fetchall()

            return [
                {"id": r[0], "name": r[1], "email": r[2], "description": r[3]}
                for r in rows
            ]

        except sqlite3.Error as e:
            logger.error(
                "Erro ao listar usuários no banco",
                extra={
                    "event": "list_users_db_error",
                    "limit": data.limit,
                    "offset": data.offset,
                    "error": str(e)
                }
            )
            raise
        finally:
            conn.close()


user_service = UserService()