FROM python:3.10-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./pokeai_api ./pokeai_api

COPY ./entrypoint.py .

ENTRYPOINT ["uvicorn", "entrypoint:app", "--host", "0.0.0.0"]