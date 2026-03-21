# MCP Server

import logging
from fastmcp import FastMCP
from models import (CreateUserRequest, SearchUserRequest)
from services.user_service import user_service

logging.basicConfig(level=logging.INFO)

server = FastMCP()

# Tool 1 - criar usuario
@server.tool()
def create_user(data):
    try:
        user_id = user_service.create_user(data)
        logging.info(f"[MCP] Usuário criado com ID: {user_id}")

        return {'message': "Usuário criado com sucesso", 'user_id': user_id}
    except Exception as e:
        logging.error(f"[MCP] Erro ao criar usuário: {e}")
        return {'error': str(e)}

# Tool 2 - buscar usuario
@server.tool()
def get_user(user_id: int):
    try:
        user = user_service.get_user(user_id)

        if user is None:
            logging.warning(f"[MCP] Usuário com ID {user_id} não encontrado.")
            return {'error': f"Usuario com ID {user_id} não encontrado"}

        return user
        
    except Exception as e:
        logging.error(f"[MCP] Erro ao buscar usuário: {e}")
        return {'error': str(e)}

# Tool 3 - busca semantica
@server.tool()
def search_users(data):
    try:
        results = user_service.search_users(data)

        return results
    
    except Exception as e:
        logging.error(f"[MCP] Erro na busca semântica: {e}")
        return {'error': str(e)}


# Iniciar o servidor MCP
if __name__ == "__main__":
    logging.info("Iniciando o MCP Server...")
    server.run()