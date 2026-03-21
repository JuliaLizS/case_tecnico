# MCP Server

import logging
from fastmcp import FastMCP
from models import (CreateUserRequest, SearchUserRequest, ListUsersRequest)
from services.user_service import user_service
from logging_config import configure_logging

configure_logging()
logger = logging.getLogger(__name__)

server = FastMCP()

# Tool 1 - criar usuario
@server.tool()
def create_user(data: CreateUserRequest):
    try:
        user_id = user_service.create_user(data)
        logger.info(
            "Usuário criado com sucesso via tool create_user",
            extra={"event": "create_user_success", "tool": "create_user", "user_id": user_id}
        )

        return {'message': "Usuário criado com sucesso", 'user_id': user_id}
    except Exception as e:
        logger.error(
            "Erro ao criar usuário via tool create_user",
            extra={"event": "create_user_error", "tool": "create_user", "error": str(e)}
        )
        return {'error': str(e)}

# Tool 2 - buscar usuario
@server.tool()
def get_user(user_id: int):
    try:
        user = user_service.get_user(user_id)

        if user is None:
            logger.warning(
                "Usuário não encontrado via tool get_user",
                extra={"event": "get_user_not_found", "tool": "get_user", "user_id": user_id}
            )
            return {'error': f"Usuario com ID {user_id} não encontrado"}

        return user
        
    except Exception as e:
        logger.error(
            "Erro ao buscar usuário via tool get_user",
            extra={"event": "get_user_error", "tool": "get_user", "user_id": user_id, "error": str(e)}
        )
        return {'error': str(e)}

# Tool 3 - busca semantica
@server.tool()
def search_users(data: SearchUserRequest):
    try:
        results = user_service.search_users(data)

        return results
    
    except Exception as e:
        logger.error(
            "Erro na busca semântica via tool search_users",
            extra={"event": "search_users_error", "tool": "search_users", "top_k": data.top_k, "error": str(e)}
        )
        return {'error': str(e)}


# Tool 4 - listar usuarios
@server.tool()
def list_users(data: ListUsersRequest):
    try:
        users = user_service.list_users(data)
        return users
    except Exception as e:
        logger.error(
            "Erro ao listar usuários via tool list_users",
            extra={
                "event": "list_users_error",
                "tool": "list_users",
                "limit": data.limit,
                "offset": data.offset,
                "error": str(e)
            }
        )
        return {'error': str(e)}


# Iniciar o servidor MCP
if __name__ == "__main__":
    logger.info("Iniciando o MCP Server", extra={"event": "server_start"})
    server.run()