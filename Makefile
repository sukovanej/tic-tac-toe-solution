.PHONY: mypy run

mypy:
	poetry run mypy tic.py

run:
	poetry run cli

test:
	poetry run pytest tests

format:
	poetry run black src tests
	poetry run isort src tests
