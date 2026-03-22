import streamlit as st
from services.user_service import user_service
from models import CreateUserRequest, SearchUserRequest, ListUsersRequest

st.set_page_config(page_title="MCP Users", page_icon="👤", layout="centered")
st.title("👤 MCP Server — Painel de Usuários")

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Criar usuário",
    "🔍 Buscar por ID",
    "🧠 Busca semântica",
    "📋 Listar usuários",
])

# ── Tab 1: Criar usuário ──────────────────────────────────────────────────────
with tab1:
    st.subheader("Criar usuário")
    with st.form("form_create"):
        name  = st.text_input("Nome")
        email = st.text_input("E-mail")
        desc  = st.text_area("Descrição")
        submitted = st.form_submit_button("Criar")

    if submitted:
        if not name or not email or not desc:
            st.warning("Preencha todos os campos.")
        else:
            try:
                req = CreateUserRequest(name=name, email=email, description=desc)
                user_id = user_service.create_user(req)
                st.success(f"Usuário criado com sucesso! ID: **{user_id}**")
            except Exception as e:
                st.error(f"Erro: {e}")

# ── Tab 2: Buscar por ID ──────────────────────────────────────────────────────
with tab2:
    st.subheader("Buscar usuário por ID")
    user_id_input = st.number_input("ID do usuário", min_value=1, step=1)
    if st.button("Buscar"):
        user = user_service.get_user(int(user_id_input))
        if user is None:
            st.warning(f"Usuário com ID {user_id_input} não encontrado.")
        else:
            st.success("Usuário encontrado!")
            st.json(user.model_dump())

# ── Tab 3: Busca semântica ────────────────────────────────────────────────────
with tab3:
    st.subheader("Busca semântica")
    query  = st.text_input("Texto de busca")
    top_k  = st.slider("Top K resultados", min_value=1, max_value=20, value=5)
    if st.button("Buscar por similaridade"):
        if not query:
            st.warning("Digite um texto para buscar.")
        else:
            results = user_service.search_users(SearchUserRequest(query=query, top_k=top_k))
            if not results:
                st.info("Nenhum resultado encontrado.")
            else:
                st.success(f"{len(results)} resultado(s) encontrado(s):")
                for r in results:
                    with st.expander(f"[score: {r['score']:.4f}] {r['name']} — {r['email']}"):
                        st.write(r["description"])

# ── Tab 4: Listar usuários ────────────────────────────────────────────────────
with tab4:
    st.subheader("Listar usuários")
    col1, col2 = st.columns(2)
    with col1:
        limit  = st.number_input("Limit",  min_value=1, max_value=100, value=10)
    with col2:
        offset = st.number_input("Offset", min_value=0, value=0)
    if st.button("Listar"):
        users = user_service.list_users(ListUsersRequest(limit=int(limit), offset=int(offset)))
        if not users:
            st.info("Nenhum usuário encontrado para essa página.")
        else:
            st.success(f"{len(users)} usuário(s) listado(s):")
            st.dataframe(users, use_container_width=True)
