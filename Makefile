.PHONY: mypy run

mypy:
	poetry run mypy tic.py

run:
	poetry run python tic.py

test:
	poetry run pytest tests -s

format:
	poetry run black src tests
	poetry run isort src tests
