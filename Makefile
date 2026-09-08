up:
	docker compose up -d db
	sleep 3
	alembic upgrade head
	python scripts/seed.py

down:
	docker compose down

reset:
	docker compose down -v

test:
	pytest

css:
	bash scripts/build_css.sh