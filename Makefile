.PHONY: infra-up infra-down run migrate test clean build-prod

# --- Infrastructure ---
infra-up:
	docker compose up -d --build val-db-dev mqtt-dev

infra-down:
	docker compose down

# --- Développement ---
run:
	uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload --reload-dir app --log-level debug

migrate:
	alembic upgrade head

test:
	python3 -m pytest app/tests/

# --- Production & Build ---
build-prod:
	docker compose -f docker-compose.prd.yml up -d --build

# --- Utilitaires ---
clean:
	docker compose down -v
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
