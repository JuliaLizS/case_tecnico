FROM python:3.11.6

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential wget curl git && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock* ./

RUN pip install pipenv && pipenv install --deploy --system

COPY . .

EXPOSE 8000
EXPOSE 8501

ENV MCP_TRANSPORT=http
ENV APP_MODE=mcp

CMD ["sh", "-c", "if [ \"$APP_MODE\" = \"streamlit\" ]; then streamlit run app.py --server.address=0.0.0.0 --server.port=8501; else python server.py; fi"]git status