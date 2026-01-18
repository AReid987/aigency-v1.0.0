# Makefile for Multi-Source Dashboard Backend

.PHONY: help install setup dev test clean docker-build docker-up docker-down migrate lint format

help: ## Show this help message
	@echo "Multi-Source Dashboard Backend"
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

setup: ## Initialize database and create admin user
	python scripts/startup.py

dev: ## Start development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

celery-worker: ## Start Celery worker
	celery -A app.tasks.celery_app worker --loglevel=info

celery-beat: ## Start Celery beat scheduler
	celery -A app.tasks.celery_app beat --loglevel=info

celery-flower: ## Start Celery Flower monitoring
	celery -A app.tasks.celery_app flower --port=5555

test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 app/ tests/
	mypy app/

format: ## Format code
	black app/ tests/
	isort app/ tests/

clean: ## Clean up temporary files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Docker commands
docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start all services with Docker
	docker-compose up -d

docker-down: ## Stop all Docker services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-setup: ## Setup database in Docker
	docker-compose exec backend python scripts/startup.py

# Database commands
migrate-create: ## Create a new migration
	alembic revision --autogenerate -m "$(msg)"

migrate-up: ## Apply migrations
	alembic upgrade head

migrate-down: ## Downgrade one migration
	alembic downgrade -1

migrate-history: ## Show migration history
	alembic history

# Development workflow
start-dev: docker-up docker-setup ## Start full development environment
	@echo "Development environment started!"
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Flower: http://localhost:5555"
	@echo "Login: admin@dashboard.local / admin123"

stop-dev: docker-down ## Stop development environment

restart-dev: docker-down docker-up ## Restart development environment

# Production commands
prod-build: ## Build for production
	docker-compose -f docker-compose.prod.yml build

prod-up: ## Start production environment
	docker-compose -f docker-compose.prod.yml up -d

prod-down: ## Stop production environment
	docker-compose -f docker-compose.prod.yml down