.PHONY: help install run test lint format makemigrations migrate docker-build docker-up docker-down docker-logs docker-shell startapp

# ====================================================================================
# HELP
# ====================================================================================

help:
	@echo "Makefile for FastAPI Production-Ready Backend"
	@echo ""
	@echo "Usage:"
	@echo "  make install      Install all dependencies"
	@echo "  make run          Run the application locally"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linters"
	@echo "  make format       Format code"
	@echo ""
	@echo "App Management:"
	@echo "  make startapp <name>      Create a new app (or use app=<name>)"
	@echo ""
	@echo "Database Migrations:"
	@echo "  make makemigrations  Create a new database migration"
	@echo "  make migrate      Apply database migrations"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  Build docker images"
	@echo "  make docker-up     Run docker compose up"
	@echo "  make docker-down   Run docker compose down"
	@echo "  make docker-logs   Follow docker compose logs"
	@echo "  make docker-shell  Get a shell into the api container"
	@echo ""

# ====================================================================================
# LOCAL DEVELOPMENT
# ====================================================================================

install:
	@echo "Installing dependencies..."
	uv pip install -e .[dev]

run:
	@echo "Starting application..."
	uvicorn src.main:app --reload

test:
	@echo "Running tests..."
	pytest

lint:
	@echo "Running linters..."
	ruff check .
	mypy .

format:
	@echo "Formatting code..."
	ruff format .

# ====================================================================================
# DATABASE MIGRATIONS
# ====================================================================================

makemigrations:
	@echo "Creating new database migration..."
	alembic revision --autogenerate -m "$(m)"

migrate:
	@echo "Applying database migrations..."
	alembic upgrade head

# ====================================================================================
# APP MANAGEMENT
# ====================================================================================

# Handle "make startapp <name>" syntax
ifeq (startapp,$(firstword $(MAKECMDGOALS)))
  # Valid arguments for startapp (anything after 'startapp')
  STARTAPP_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  # Turn them into do-nothing targets
  $(eval $(STARTAPP_ARGS):;@:)
endif

startapp:
	@echo "Creating new app..."
	@if [ -n "$(STARTAPP_ARGS)" ]; then \
		uv run python scripts/startapp.py $(STARTAPP_ARGS); \
	elif [ -n "$(app)" ]; then \
		uv run python scripts/startapp.py $(app); \
	else \
		printf "Enter App Name: "; \
		read app_name; \
		uv run python scripts/startapp.py $$app_name; \
	fi

# ====================================================================================
# DOCKER
# ====================================================================================

docker-build:
	@echo "Building docker images..."
	docker compose build

docker-up:
	@echo "Starting docker compose..."
	docker compose up

docker-down:
	@echo "Stopping docker compose..."
	docker compose down

docker-logs:
	@echo "Following docker compose logs..."
	docker compose logs -f

docker-shell:
	@echo "Getting a shell into the api container..."
	docker compose exec api /bin/sh
