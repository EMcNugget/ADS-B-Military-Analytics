FROM python:3.8.5-slim-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENV MDB_URL=mongodb+srv://mcnugget:Train2007@mildata.oyy7jmp.mongodb.net/?retryWrites=true&w=majority
ENV API_HOST=adsbexchange-com1.p.rapidapi.com
ENV API_KEY=ebf3ccc26cmshc2649b8713bb71bp19ac2ajsn38f04ae99987

EXPOSE 8080

CMD ["python", "main.py"]