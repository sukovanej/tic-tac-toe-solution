.PHONY: mypy run

mypy:
	poetry run mypy tic.py

run:
	poetry run cli

test:
	poetry run pytest tests/test_tic.py::test_get_game_result

format:
	poetry run black src tests
	poetry run isort src tests
