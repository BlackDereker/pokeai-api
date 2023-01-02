# Run uvicorn
phony: install run-dev

install:
	pip install poetry
	poetry install

run:
	uvicorn entrypoint:app

run-dev:
	uvicorn entrypoint:app --reload
