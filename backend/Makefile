# Backend Makefile

.PHONY: help help-full \
run-dev-backend clean-backend test-backend test-watch-backend \
lint-backend lint-branch-backend \
format-backend format-branch-backend \
poetry-lock-backend build-backend \
logs-dev-backend attach-dev-backend status-dev-backend# Docker compose command with project name
DOCKER_COMPOSE := docker compose -p boneca

help:
	@printf "\n    🩰 Boneca - Backend Service\n"
	@printf "    ═════════════════════════\n\n"
	@printf "    ⚡ Quick Actions\n"
	@printf "    ────────────\n"
	@printf "    ➜ make run-dev       │ Build and run development environment with hot reload\n"
	@printf "    ➜ make logs          │ Follow development server logs\n"
	@printf "    ➜ make attach        │ Attach to development server container\n"
	@printf "    ➜ make status        │ Check development server status\n"
	@printf "    ➜ make test          │ Run full test suite\n"
	@printf "    ➜ make clean         │ Stop and clean everything in boneca project\n"
	@printf "    ➜ make lint-branch   │ Run linting on files changed in current branch\n"
	@printf "    ➜ make format-branch │ Format files changed in current branch\n"
	@printf "    ➜ make \033[95mgo-go-boneca-rangers\033[0m │ 🦸 Complete code quality pipeline: format + lint + test\n\n"
	@printf "    📝 Use 'make help-full' for complete documentation\n\n"

help-full:
	@printf "\n    🩰 Boneca - Backend Service\n"
	@printf "    ═════════════════════════\n\n"
	@printf "    🚀 Development Commands\n"
	@printf "    ──────────────────────\n"
	@printf "    ➜ make run-dev-backend       │ Build and run development environment\n"
	@printf "    ➜ make logs-dev-backend      │ Follow development server logs\n"
	@printf "    ➜ make attach-dev-backend    │ Attach to development server container\n"
	@printf "    ➜ make status-dev-backend    │ Check development server status\n"
	@printf "    ➜ make build-backend         │ Build all Docker images\n"
	@printf "    ➜ make poetry-lock-backend   │ Update poetry.lock file in Docker\n\n"
	@printf "    🔍 Code Quality\n"
	@printf "    ─────────────\n"
	@printf "    ➜ make test-backend          │ Run test suite in Docker\n"
	@printf "    ➜ make lint-backend          │ Run all linting in Docker\n"
	@printf "    ➜ make lint-branch-backend   │ Lint changed files in Docker\n"
	@printf "    ➜ make format-backend        │ Format all code in Docker\n"
	@printf "    ➜ make format-branch-backend │ Format changed files in Docker\n\n"
	@printf "    🧹 Maintenance\n"
	@printf "    ────────────\n"
	@printf "    ➜ make clean-backend         │ Clean Docker resources and caches\n\n"
	@printf "    📚 Quick Examples\n"
	@printf "    ──────────────\n"
	@printf "    Development workflow:\n"
	@printf "    1. $$ make run-dev-backend     # Start development server\n"
	@printf "    2. $$ make format-branch       # Format your changes\n"
	@printf "    3. $$ make lint-branch         # Check your changes\n"
	@printf "    4. $$ make test-backend        # Run tests\n\n"
	@printf "    Docker workflow:\n"
	@printf "    $$ make build-backend && make run-dev-backend\n\n"
	@printf "    API Endpoints:\n"
	@printf "    • http://localhost:8000/         - Welcome message\n"
	@printf "    • http://localhost:8000/api/v1/ping   - Health check\n"
	@printf "    • http://localhost:8000/api/v1/docs   - API documentation\n\n"

# Quick action aliases
run-dev: run-dev-backend
test: test-backend
clean: clean-backend
lint-branch: lint-branch-backend
format-branch: format-branch-backend
logs: logs-dev-backend
attach: attach-dev-backend
status: status-dev-backend
go-go-boneca-rangers: go-go-boneca-rangers-backend

# Development commands
run-dev-backend:
	$(DOCKER_COMPOSE) build boneca-dev
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev

logs-dev-backend:
	$(DOCKER_COMPOSE) logs -f boneca-dev

attach-dev-backend:
	$(DOCKER_COMPOSE) attach boneca-dev

status-dev-backend:
	$(DOCKER_COMPOSE) ps boneca-dev

build-backend:
	$(DOCKER_COMPOSE) build

poetry-lock-backend:
	$(DOCKER_COMPOSE) run --rm boneca poetry lock

# Testing and quality commands
test-backend:
	@echo "Starting development container if not running..."
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev
	@echo "Running tests in the container..."
	$(DOCKER_COMPOSE) exec boneca-dev poetry run pytest \
		tests \
		-v \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html \
		--asyncio-mode=auto \
		$(PYTEST_ARGS)

test-watch-backend:
	@echo "Starting development container if not running..."
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev
	@echo "Running tests in watch mode in the container..."
	$(DOCKER_COMPOSE) exec boneca-dev poetry run pytest \
		tests \
		-v \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html \
		--asyncio-mode=auto \
		-f \
		$(PYTEST_ARGS)

lint-backend:
	@echo "Starting development container if not running..."
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev
	@echo "Running linting checks in the container..."
	$(DOCKER_COMPOSE) exec boneca-dev sh -c "\
		cd /app && \
		poetry run flake8 src tests && \
		poetry run mypy --explicit-package-bases src tests && \
		poetry run black --check src tests && \
		poetry run isort --check-only src tests"

lint-strict-backend: lint-backend
	$(DOCKER_COMPOSE) --profile dev run --rm boneca-dev poetry run flake8 src tests --select=D,B,C,S  # docstring, bugbear, comprehensions, simplify

lint-branch-backend:
	$(DOCKER_COMPOSE) --profile dev run --rm boneca-dev sh -c "\
		git diff --name-only origin/main | grep '\.py$$' | \
		xargs -r poetry run flake8 && \
		git diff --name-only origin/main | grep '\.py$$' | \
		xargs -r poetry run black --check && \
		git diff --name-only origin/main | grep '\.py$$' | \
		xargs -r poetry run isort --check-only"

format-backend:
	@echo "Starting development container if not running..."
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev
	@echo "Running code formatting in the container..."
	$(DOCKER_COMPOSE) exec boneca-dev sh -c "\
		poetry run black src tests && \
		poetry run isort src tests"

format-branch-backend:
	@echo "Starting development container if not running..."
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev
	@echo "Running code formatting on changed files in the container..."
	$(DOCKER_COMPOSE) exec boneca-dev sh -c "\
		git diff --name-only origin/main | grep '\.py$$' | \
		xargs -r poetry run black && \
		git diff --name-only origin/main | grep '\.py$$' | \
		xargs -r poetry run isort"

# Complete code quality pipeline
go-go-boneca-rangers-backend:
	@echo "🦸 GO GO BONECA RANGERS! 🦸"
	@echo "Starting complete code quality pipeline..."
	@echo ""
	@echo "⚡ Step 1: Starting development container..."
	$(DOCKER_COMPOSE) --profile dev up -d boneca-dev
	@echo ""
	@echo "🎨 Step 2: Auto-formatting code with Black..."
	$(DOCKER_COMPOSE) exec boneca-dev poetry run black src tests
	@echo ""
	@echo "📦 Step 3: Fixing imports with isort..."
	$(DOCKER_COMPOSE) exec boneca-dev poetry run isort src tests
	@echo ""
	@echo "🔍 Step 4: Running linters (flake8, mypy, black check, isort check)..."
	$(DOCKER_COMPOSE) exec boneca-dev sh -c "\
		cd /app && \
		poetry run flake8 src tests && \
		poetry run mypy --explicit-package-bases src tests && \
		poetry run black --check src tests && \
		poetry run isort --check-only src tests"
	@echo ""
	@echo "🧪 Step 5: Running tests with coverage..."
	$(DOCKER_COMPOSE) exec boneca-dev poetry run pytest \
		tests \
		-v \
		--cov=src \
		--cov-report=term-missing \
		--cov-report=html \
		--asyncio-mode=auto
	@echo ""
	@echo "🦸 BONECA RANGERS ASSEMBLE! All checks passed! 🦸"
	@echo "✅ Code formatted ✅ Imports sorted ✅ Linting passed ✅ Tests passed"

# Cleanup commands
clean-backend:
	$(DOCKER_COMPOSE) stop || true
	# Run cleanup inside Docker first
	$(DOCKER_COMPOSE) --profile dev run --rm boneca-dev sh -c "\
		find /app -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true && \
		find /app -type f -name '*.pyc' -delete 2>/dev/null || true && \
		find /app -type f -name '*.pyo' -delete 2>/dev/null || true && \
		find /app -type f -name '*.pyd' -delete 2>/dev/null || true && \
		find /app -type f -name '.coverage' -delete 2>/dev/null || true && \
		find /app -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true && \
		find /app -type d -name '*.egg' -exec rm -rf {} + 2>/dev/null || true && \
		find /app -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true && \
		find /app -type d -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true"
	# Then clean up Docker resources
	$(DOCKER_COMPOSE) down -v --remove-orphans
	$(DOCKER_COMPOSE) rm -f
	docker system prune -f

backend-lint:
	poetry run flake8 src tests
	poetry run mypy src tests
	poetry run black src tests --check
	poetry run isort src tests --check-only

backend-format:
	poetry run black src tests
	poetry run isort src tests

backend-lint-branch:
	git diff --name-only origin/main | grep '\.py$$' | xargs -r poetry run flake8
	git diff --name-only origin/main | grep '\.py$$' | xargs -r poetry run black --check
	git diff --name-only origin/main | grep '\.py$$' | xargs -r poetry run isort --check-only

backend-format-branch:
	git diff --name-only origin/main | grep '\.py$$' | xargs -r poetry run black
	git diff --name-only origin/main | grep '\.py$$' | xargs -r poetry run isort

backend-clean-local:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
