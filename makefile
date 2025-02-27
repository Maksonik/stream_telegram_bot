test:
	pytest -v

lint:
	ruff format --config=ruff-format.toml && ruff check --fix

beat:
	celery -A scr.celery.app beat -l INFO

worker:
	celery -A scr.celery.app worker -l INFO
