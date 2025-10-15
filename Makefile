# Detect OS for cross-platform compatibility
ifeq ($(OS),Windows_NT)
    POETRY := $(shell where poetry 2>nul)
    PYTHON := python
    RM := rmdir /s /q
    RM_FILE := del /q
    MKDIR := mkdir
    COPY := copy
    ECHO := @echo
    SEP := &&
    NULL := nul
else
    POETRY := $(shell which poetry 2>/dev/null)
    PYTHON := python3
    RM := rm -rf
    RM_FILE := rm -f
    MKDIR := mkdir -p
    COPY := cp
    ECHO := @echo
    SEP := ;
    NULL := /dev/null
endif

.PHONY: help venv install setup migrate superuser run test clean lint lint-ci format shell collectstatic startapp dev-deps db-shell db-reset makemigrations tailwind-install tailwind-start tailwind-build test-accounts test-core test-explore test-theme coverage django-upgrade pre-commit-install

help: ## Show help message
	$(ECHO) "=========================================="
	$(ECHO) "Django Project - Available Commands"
	$(ECHO) "=========================================="
	$(ECHO) ""
	$(ECHO) "Setup Commands:"
	$(ECHO) "  make venv                - Create virtual environment"
	$(ECHO) "  make install             - Install Poetry if not present"
	$(ECHO) "  make env                 - Create .env file from .env.example"
	$(ECHO) "  make deps                - Install project dependencies"
	$(ECHO) "  make pre-commit-install  - Install pre-commit hooks"
	$(ECHO) "  make setup               - Complete setup: venv, install dependencies, migrate, and pre-commit"
	$(ECHO) ""
	$(ECHO) "Development Commands:"
	$(ECHO) "  make run              - Run development server"
	$(ECHO) "  make shell            - Open Django shell"
	$(ECHO) "  make migrate          - Run database migrations"
	$(ECHO) "  make makemigrations   - Create new migrations"
	$(ECHO) "  make superuser        - Create Django superuser"
	$(ECHO) "  make startapp         - Create new Django app (usage: make startapp name=myapp)"
	$(ECHO) ""
	$(ECHO) "Testing Commands:"
	$(ECHO) "  make test             - Run all tests"
	$(ECHO) "  make test-accounts    - Run tests for accounts app"
	$(ECHO) "  make test-core        - Run tests for core app"
	$(ECHO) "  make test-explore     - Run tests for explore app"
	$(ECHO) "  make test-theme       - Run tests for theme app"
	$(ECHO) "  make coverage         - Run tests with coverage report"
	$(ECHO) ""
	$(ECHO) "Code Quality Commands:"
	$(ECHO) "  make format           - Format code with black and isort"
	$(ECHO) "  make lint             - Run basic linting (flake8)"
	$(ECHO) "  make lint-ci          - Run all CI linters (black, isort, autoflake, flake8, django-upgrade, pyupgrade)"
	$(ECHO) "  make django-upgrade   - Check for Django 5.0 deprecations"
	$(ECHO) "  make clean            - Clean cache and temporary files"
	$(ECHO) "  make dev-deps         - Install development dependencies"
	$(ECHO) ""
	$(ECHO) "Database Commands:"
	$(ECHO) "  make db-shell         - Open database shell"
	$(ECHO) "  make db-reset         - Reset database (WARNING: deletes all data)"
	$(ECHO) ""
	$(ECHO) "Static Files & Tailwind:"
	$(ECHO) "  make collectstatic    - Collect static files"
	$(ECHO) "  make tailwind-install - Install Tailwind CSS"
	$(ECHO) "  make tailwind-start   - Start Tailwind CSS dev server"
	$(ECHO) "  make tailwind-build   - Build Tailwind CSS for production"
	$(ECHO) ""
	$(ECHO) "=========================================="
	$(ECHO) ""

venv: ## Create virtual environment
	$(ECHO) "Creating virtual environment..."
ifeq ($(OS),Windows_NT)
	@if not exist env $(PYTHON) -m venv env
	$(ECHO) "Virtual environment created! Activate it with: env\Scripts\activate"
else
	@test -d env || $(PYTHON) -m venv env
	$(ECHO) "Virtual environment created! Activate it with: source env/bin/activate"
endif

check-poetry: ## Check if Poetry is installed
ifndef POETRY
	$(ECHO) "Poetry is not installed. Please run 'make install' first."
	@exit 1
endif

install: ## Install Poetry using pip
	$(ECHO) "Checking Poetry installation..."
ifeq ($(OS),Windows_NT)
	@where poetry >$(NULL) 2>&1 || ( \
		echo Poetry not found. Installing Poetry... $(SEP) \
		pip install poetry \
	)
else
	@which poetry >$(NULL) 2>&1 || ( \
		echo "Poetry not found. Installing Poetry..." $(SEP) \
		pip3 install poetry \
	)
endif
	$(ECHO) "Poetry is ready!"

env: ## Create .env file from .env.example
ifeq ($(OS),Windows_NT)
	@if not exist .env ( \
		echo Creating .env file from .env.example... $(SEP) \
		$(COPY) .env.example .env $(SEP) \
		echo .env created. Update database credentials if needed. \
	) else ( \
		echo .env already exists. Skipping... \
	)
else
	@test -f .env || ( \
		echo "Creating .env file from .env.example..." $(SEP) \
		$(COPY) .env.example .env $(SEP) \
		echo ".env created. Update database credentials if needed." \
	)
endif

deps: check-poetry ## Install project dependencies
	$(ECHO) "Installing dependencies..."
	poetry install

pre-commit-install: check-poetry ## Install pre-commit hooks
	$(ECHO) "Installing pre-commit hooks..."
	poetry run pre-commit install
	$(ECHO) "Pre-commit hooks installed successfully!"

setup: venv install env deps migrate pre-commit-install ## Complete project setup
	$(ECHO) ""
	$(ECHO) "========================================"
	$(ECHO) "Setup complete!"
	$(ECHO) "========================================"
	$(ECHO) ""
	$(ECHO) "Next steps:"
	$(ECHO) "  1. Create a superuser: make superuser"
	$(ECHO) "  2. Run the server: make run"
	$(ECHO) ""

migrate: check-poetry ## Run database migrations
	$(ECHO) "Running migrations..."
	poetry run python manage.py migrate

makemigrations: check-poetry ## Create new migrations
	$(ECHO) "Creating migrations..."
	poetry run python manage.py makemigrations

superuser: check-poetry ## Create Django superuser
	poetry run python manage.py createsuperuser

run: check-poetry ## Run development server
	poetry run python manage.py runserver

shell: check-poetry ## Open Django shell
	poetry run python manage.py shell

clean: ## Clean cache and temporary files
	$(ECHO) "Cleaning cache and temporary files..."
ifeq ($(OS),Windows_NT)
	@if exist __pycache__ $(RM) __pycache__
	@if exist .pytest_cache $(RM) .pytest_cache
	@for /d /r %%i in (__pycache__) do @if exist "%%i" $(RM) "%%i"
	@for /r %%i in (*.pyc) do @if exist "%%i" $(RM_FILE) "%%i"
	@for /r %%i in (*.pyo) do @if exist "%%i" $(RM_FILE) "%%i"
else
	@find . -type d -name "__pycache__" -exec $(RM) {} + 2>$(NULL) || true
	@find . -type f -name "*.pyc" -exec $(RM_FILE) {} + 2>$(NULL) || true
	@find . -type f -name "*.pyo" -exec $(RM_FILE) {} + 2>$(NULL) || true
	@$(RM) .pytest_cache 2>$(NULL) || true
endif
	$(ECHO) "Cleanup complete!"

collectstatic: check-poetry ## Collect static files
	poetry run python manage.py collectstatic --noinput

startapp: check-poetry ## Create new Django app (usage: make startapp name=myapp)
ifndef name
	$(ECHO) "Error: Please provide an app name. Usage: make startapp name=myapp"
	@exit 1
endif
	poetry run python manage.py startapp $(name)
	$(ECHO) "App '$(name)' created in apps/ directory"

format: check-poetry ## Format code with black and isort
	$(ECHO) "Formatting code with black..."
	@poetry run black . 2>$(NULL) || $(ECHO) "Black is not installed. Run: poetry add --group dev black"
	$(ECHO) "Sorting imports with isort..."
	@poetry run isort . 2>$(NULL) || $(ECHO) "isort is not installed. Run: poetry add --group dev isort"

lint: check-poetry ## Lint code with flake8
	@poetry run flake8 . 2>$(NULL) || $(ECHO) "Flake8 is not installed. Run: poetry add --group dev flake8"

django-upgrade: check-poetry ## Check for Django 5.0 deprecations
	$(ECHO) "Checking for Django 5.0 deprecations..."
ifeq ($(OS),Windows_NT)
	@poetry run django-upgrade --target-version 5.0 $(shell for /r apps %%i in (*.py) do @echo %%i) $(shell for /r config %%i in (*.py) do @echo %%i) manage.py 2>$(NULL) || $(ECHO) "django-upgrade is not installed"
else
	@poetry run django-upgrade --target-version 5.0 $$(find apps/ config/ -name "*.py") manage.py 2>$(NULL) || $(ECHO) "django-upgrade is not installed"
endif

lint-ci: check-poetry ## Run all CI linters (matches GitHub Actions workflow)
	$(ECHO) "Running all CI linters..."
	$(ECHO) ""
	$(ECHO) "1. Checking code formatting with Black..."
	@poetry run black --check --diff . || ($(ECHO) "ERROR: Black formatting check failed. Run 'make format' to fix." && exit 1)
	$(ECHO) ""
	$(ECHO) "2. Checking import sorting with isort..."
	@poetry run isort --check-only --diff . || ($(ECHO) "ERROR: isort check failed. Run 'make format' to fix." && exit 1)
	$(ECHO) ""
	$(ECHO) "3. Checking for unused imports with autoflake..."
ifeq ($(OS),Windows_NT)
	@poetry run autoflake --check --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --ignore-init-module-imports --recursive apps/ config/ manage.py
else
	@poetry run autoflake --check --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --ignore-init-module-imports --recursive apps/ config/ manage.py
endif
	$(ECHO) ""
	$(ECHO) "4. Running flake8..."
ifeq ($(OS),Windows_NT)
	@poetry run flake8 --select=TMS010,TMS011,TMS012,TMS013,TMS020,TMS021,TMS022 apps/ config/ manage.py
else
	@poetry run flake8 --select=TMS010,TMS011,TMS012,TMS013,TMS020,TMS021,TMS022 apps/ config/ manage.py
endif
	$(ECHO) ""
	$(ECHO) "5. Checking for Django 5.0 deprecations..."
ifeq ($(OS),Windows_NT)
	@poetry run django-upgrade --target-version 5.0 $(shell for /r apps %%i in (*.py) do @echo %%i) $(shell for /r config %%i in (*.py) do @echo %%i) manage.py
else
	@poetry run django-upgrade --target-version 5.0 $$(find apps/ config/ -name "*.py") manage.py
endif
	$(ECHO) ""
	$(ECHO) "6. Checking for Python 3.10+ syntax with pyupgrade..."
ifeq ($(OS),Windows_NT)
	@poetry run pyupgrade --py310-plus $(shell for /r apps %%i in (*.py) do @echo %%i) $(shell for /r config %%i in (*.py) do @echo %%i) manage.py
else
	@poetry run pyupgrade --py310-plus $$(find apps/ config/ -name "*.py") manage.py
endif
	$(ECHO) ""
	$(ECHO) "All linters passed!"

dev-deps: check-poetry ## Install development dependencies
	$(ECHO) "Installing development dependencies..."
	poetry add --group dev black flake8 pytest pytest-django

# Database commands
db-shell: check-poetry ## Open database shell
	poetry run python manage.py dbshell

db-reset: check-poetry ## Reset database (WARNING: deletes all data)
ifeq ($(OS),Windows_NT)
	$(ECHO) "WARNING: This will delete all data!"
	@set /p confirm="Are you sure? (yes/no): "
	@if "%confirm%"=="yes" ( \
		if exist db.sqlite3 $(RM_FILE) db.sqlite3 $(SEP) \
		poetry run python manage.py migrate \
	) else ( \
		echo Database reset cancelled. \
	)
else
	$(ECHO) "WARNING: This will delete all data!"
	@read -p "Are you sure? (yes/no): " confirm $(SEP) \
	if [ "$$confirm" = "yes" ]; then \
		$(RM_FILE) db.sqlite3 2>$(NULL) || true $(SEP) \
		poetry run python manage.py migrate $(SEP) \
	else \
		echo "Database reset cancelled." $(SEP) \
	fi
endif

# Tailwind CSS commands
tailwind-install: check-poetry ## Install and setup Tailwind CSS
	$(ECHO) "Installing Tailwind CSS..."
	poetry run python manage.py tailwind install

tailwind-start: check-poetry ## Start Tailwind CSS development server
	$(ECHO) "Starting Tailwind CSS dev server..."
	poetry run python manage.py tailwind start

tailwind-build: check-poetry ## Build Tailwind CSS for production
	$(ECHO) "Building Tailwind CSS for production..."
	poetry run python manage.py tailwind build

# App-specific commands
test: check-poetry ## Run all tests (matches CI workflow)
	$(ECHO) "Running tests..."
	poetry run python manage.py test apps --verbosity=2

test-accounts: check-poetry ## Run tests for accounts app
	poetry run python manage.py test apps.accounts

test-core: check-poetry ## Run tests for core app
	poetry run python manage.py test apps.core

test-explore: check-poetry ## Run tests for explore app
	poetry run python manage.py test apps.explore

test-theme: check-poetry ## Run tests for theme app
	poetry run python manage.py test apps.theme

coverage: check-poetry ## Run tests with coverage report
	$(ECHO) "Running tests with coverage..."
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage html
