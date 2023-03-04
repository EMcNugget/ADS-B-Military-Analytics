FROM python:3.10.0a6-alpine3.13-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

ENV API_KEY=...

ENV API_HOST=...

ENV MDB_URL=...

# Referece README.md for more information on the environment variables\

CMD ["python", "app.py"]
