FROM python:3.10-slim

WORKDIR /app

COPY ./pokeai_api .

COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "entrypoint:app", "--host", "0.0.0.0"]