test:
	pytest -v

lint:
	ruff format && ruff check --fix

run-beat:
	celery -A scr.celery.app beat -l INFO

run-worker:
	celery -A scr.celery.app worker -l INFO
