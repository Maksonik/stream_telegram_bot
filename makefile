run:
	docker compose up

test:
	pytest -v

test-cov:
	pytest --cov=scr tests/ --cov-report=xml  --vcr-record=none

lint:
	ruff format --config=ruff-format.toml && ruff check --fix

beat:
	celery -A scr.celery.app beat -l INFO

worker:
	celery -A scr.celery.app worker -l INFO
