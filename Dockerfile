FROM python:3.11.6

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential wget curl git && \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock* ./

RUN pip install pipenv && pipenv install --deploy --system

COPY . .

EXPOSE 8000

CMD ["python", "server.py"]