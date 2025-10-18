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

.PHONY: help venv install setup migrate superuser run test clean lint lint-ci format shell collectstatic startapp dev-deps db-shell db-reset makemigrations test-accounts test-core test-explore test-theme coverage django-upgrade pre-commit-install

## Mostrar mensagem de ajuda
help:
	@echo ==========================================
	@echo Projeto Django - Comandos Disponiveis
	@echo ==========================================
	@echo Comandos de Configuracao:
	@echo   make venv                - Criar ambiente virtual
	@echo   make install             - Instalar Poetry se nao estiver presente
	@echo   make env                 - Criar arquivo .env com variaveis default
	@echo   make deps                - Instalar dependencias do projeto
	@echo   make pre-commit-install  - Instalar hooks do pre-commit
	@echo   make setup               - Configuracao completa: venv, dependencias, migrate e pre-commit
	@echo .
	@echo Comandos de Desenvolvimento:
	@echo   make run              - Executar servidor de desenvolvimento
	@echo   make shell            - Abrir shell do Django
	@echo   make migrate          - Executar migracoes do banco de dados
	@echo   make makemigrations   - Criar novas migracoes
	@echo   make superuser        - Criar superusuario do Django
	@echo   make startapp         - Criar novo app Django (uso: make startapp name=myapp)
	@echo .
	@echo Comandos de Teste:
	@echo   make test             - Executar todos os testes
	@echo   make test-accounts    - Executar testes para o app de contas
	@echo   make test-core        - Executar testes para o app principal
	@echo   make test-explore     - Executar testes para o app de exploração
	@echo   make test-theme       - Executar testes para o app de tema
	@echo   make coverage         - Executar testes com relatorio de cobertura
	@echo .
	@echo Comandos de Qualidade de Codigo:
	@echo   make format           - Formatar codigo com black e isort
	@echo   make lint             - Executar linting basico (flake8)
	@echo   make lint-ci          - Executar todos os linters do CI (black, isort, autoflake, flake8, django-upgrade, pyupgrade)
	@echo   make django-upgrade   - Verificar deprecacoes do Django 5.0
	@echo   make clean            - Limpar cache e arquivos temporarios
	@echo   make dev-deps         - Instalar dependencias de desenvolvimento
	@echo .
	@echo Comandos de Banco de Dados:
	@echo   make db-shell         - Abrir shell do banco de dados
	@echo   make db-reset         - Resetar banco de dados (AVISO: apaga todos os dados)
	@echo
	@echo Arquivos Estaticos:
	@echo   make collectstatic    - Coletar arquivos estaticos
	@echo ==========================================



venv: ## Criar ambiente virtual
	@echo Criando ambiente virtual...
ifeq ($(OS),Windows_NT)
	@if not exist env $(PYTHON) -m venv env
	@echo   Ambiente virtual criado! Ative com: env\Scripts\activate
else
	@test -d env || $(PYTHON) -m venv env
	@echo   Ambiente virtual criado! Ative com: source env/bin/activate
endif


env: ## Criar arquivo .env
ifeq ($(OS),Windows_NT)
	@if not exist .env ( \
		echo Criando arquivo .env... && \
		(echo # Django Settings)> .env && \
		(echo SECRET_KEY=django-insecure-example-key-for-development-only-change-in-production)>> .env && \
		(echo DEBUG=True)>> .env && \
		(echo ALLOWED_HOSTS=localhost,127.0.0.1)>> .env && \
		(echo.>> .env) && \
		(echo # Database Settings - SQLite ^(for development^))>> .env && \
		(echo DB_ENGINE=django.db.backends.sqlite3)>> .env && \
		(echo DB_NAME=db.sqlite3)>> .env \
	)
else
	@test -f .env || ( \
		echo "Criando arquivo .env..." && \
		echo "# Django Settings" > .env && \
		echo "SECRET_KEY=django-insecure-example-key-for-development-only-change-in-production" >> .env && \
		echo "DEBUG=True" >> .env && \
		echo "ALLOWED_HOSTS=localhost,127.0.0.1" >> .env && \
		echo "" >> .env && \
		echo "# Database Settings - SQLite (for development)" >> .env && \
		echo "DB_ENGINE=django.db.backends.sqlite3" >> .env && \
		echo "DB_NAME=db.sqlite3" >> .env \
	)
endif



check-poetry: ## Verificar se Poetry esta instalado
ifndef POETRY
	@echo    Poetry nao esta instalado. Por favor, execute 'make install' primeiro.
	@exit 1
endif


install: ## Instalar Poetry usando pip
	@echo Verificando instalacao do Poetry...
ifeq ($(OS),Windows_NT)
	@where poetry >$(NULL) 2>&1 || ( \
		echo    Poetry nao encontrado. Instalando Poetry... $(SEP) \
		pip install poetry \
	)
else
	@which poetry >$(NULL) 2>&1 || ( \
		echo    Poetry nao encontrado. Instalando Poetry... $(SEP) \
		pip3 install poetry \
	)
endif


deps: check-poetry ## Instalar dependencias do projeto
	@echo Instalando dependencias...
	poetry install


pre-commit-install: check-poetry ## Instalar hooks do pre-commit
	@echo Instalando hooks do pre-commit...
	poetry run pre-commit install


setup: venv install env deps migrate pre-commit-install ## Configuracao completa do projeto
	@echo ========================================
	@echo Configuracao completa!
	@echo ========================================
	@echo Proximos passos:
	@echo   1. Criar um superusuario: make superuser
	@echo   2. Executar o servidor: make run

migrate: check-poetry
	@echo Executando migracoes...
	poetry run python manage.py migrate

makemigrations: check-poetry
	@echo Criando migracoes...
	poetry run python manage.py makemigrations

superuser: check-poetry
	poetry run python manage.py createsuperuser

run: check-poetry
	poetry run python manage.py runserver

shell: check-poetry
	poetry run python manage.py shell

clean:
	@echo Limpando cache e arquivos temporarios...
ifeq ($(OS),Windows_NT)
	@if exist __pycache__ $(RM) __pycache__
	@if exist .pytest_cache $(RM) .pytest_cache
	@for /d /r %%i in (__pycache__) do @if exist %%i $(RM) %%i
	@for /r %%i in (*.pyc) do @if exist %%i $(RM_FILE) %%i
	@for /r %%i in (*.pyo) do @if exist %%i $(RM_FILE) %%i
else
	@find . -type d -name __pycache__ -exec $(RM) {} + 2>$(NULL) || true
	@find . -type f -name *.pyc -exec $(RM_FILE) {} + 2>$(NULL) || true
	@find . -type f -name *.pyo -exec $(RM_FILE) {} + 2>$(NULL) || true
	@$(RM) .pytest_cache 2>$(NULL) || true
endif
	@echo   Limpeza completa!


collectstatic: check-poetry ## Coletar arquivos estaticos
	poetry run python manage.py collectstatic --noinput


startapp: check-poetry ## Criar novo app Django
ifndef name
	@echo Erro: Por favor forneça um nome de app
	@exit 1
endif
	poetry run python manage.py startapp $(name)
	@echo App '$(name)' criado no diretorio apps/


format: check-poetry ## Formatar codigo com black e isort
	@echo Formatando codigo com black...
	@poetry run black . 2>$(NULL) || @echo Black nao esta instalado. Execute: poetry add --group dev black
	@echo Ordenando imports com isort...
	@poetry run isort . 2>$(NULL) || @echo isort nao esta instalado. Execute: poetry add --group dev isort


lint: check-poetry ## Executar linting basico com flake8
	@poetry run flake8 . 2>$(NULL) || @echo Flake8 nao esta instalado. Execute: poetry add --group dev flake8


django-upgrade: check-poetry ## Verificar deprecacoes do Django 5.0
	@echo Verificando deprecacoes do Django 5.0...
ifeq ($(OS),Windows_NT)
	@poetry run django-upgrade --target-version 5.0 $(shell for /r apps %%i in (*.py) do @echo %%i) $(shell for /r config %%i in (*.py) do @echo %%i) manage.py 2>$(NULL) || @echo django-upgrade nao esta instalado
else
	@poetry run django-upgrade --target-version 5.0 $$(find apps/ config/ -name *.py) manage.py 2>$(NULL) || @echo django-upgrade nao esta instalado
endif


lint-ci: check-poetry ## Executar todos os linters do CI (corresponde ao workflow do GitHub Actions)
	@echo Executando todos os linters do CI...
	@echo
	@echo 1. Verificando formatacao de codigo com Black...
	@poetry run black --check --diff . || (@echo ERRO: Verificacao de formatacao do Black falhou. Execute 'make format' para corrigir. && exit 1)
	@echo
	@echo 2. Verificando ordenacao de imports com isort...
	@poetry run isort --check-only --diff . || (@echo ERRO: Verificacao do isort falhou. Execute 'make format' para corrigir. && exit 1)
	@echo
	@echo 3. Verificando imports nao utilizados com autoflake...
ifeq ($(OS),Windows_NT)
	@poetry run autoflake --check --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --ignore-init-module-imports --recursive apps/ config/ manage.py
else
	@poetry run autoflake --check --remove-all-unused-imports --remove-unused-variables --remove-duplicate-keys --ignore-init-module-imports --recursive apps/ config/ manage.py
endif
	@echo
	@echo 4. Executando flake8...
ifeq ($(OS),Windows_NT)
	@poetry run flake8 --select=TMS010,TMS011,TMS012,TMS013,TMS020,TMS021,TMS022 apps/ config/ manage.py
else
	@poetry run flake8 --select=TMS010,TMS011,TMS012,TMS013,TMS020,TMS021,TMS022 apps/ config/ manage.py
endif
	@echo
	@echo 5. Verificando deprecacoes do Django 5.0...
ifeq ($(OS),Windows_NT)
	@poetry run django-upgrade --target-version 5.0 $(shell for /r apps %%i in (*.py) do @echo %%i) $(shell for /r config %%i in (*.py) do @echo %%i) manage.py
else
	@poetry run django-upgrade --target-version 5.0 $$(find apps/ config/ -name *.py) manage.py
endif
	@echo
	@echo 6. Verificando sintaxe Python 3.10+ com pyupgrade...
ifeq ($(OS),Windows_NT)
	@poetry run pyupgrade --py310-plus $(shell for /r apps %%i in (*.py) do @echo %%i) $(shell for /r config %%i in (*.py) do @echo %%i) manage.py
else
	@poetry run pyupgrade --py310-plus $$(find apps/ config/ -name *.py) manage.py
endif
	@echo
	@echo Todos os linters passaram!


dev-deps: check-poetry ## Instalar dependencias de desenvolvimento
	@echo Instalando dependencias de desenvolvimento...
	poetry add --group dev black flake8 pytest pytest-django


db-shell: check-poetry ## Abrir shell do banco de dados
	poetry run python manage.py dbshell


db-reset: check-poetry ## Resetar banco de dados (AVISO: apaga todos os dados)
ifeq ($(OS),Windows_NT)
	@echo AVISO: Isso apagara todos os dados!
	@set /p confirm=Tem certeza? (sim/nao):
	@if %confirm%==sim ( \
		if exist db.sqlite3 $(RM_FILE) db.sqlite3 $(SEP) \
		poetry run python manage.py migrate \
	) else ( \
		echo Reset do banco de dados cancelado. \
	)
else
	@echo AVISO: Isso apagara todos os dados!
	@read -p Tem certeza? (sim/nao):  confirm $(SEP) \
	if [ $$confirm = sim ]; then \
		$(RM_FILE) db.sqlite3 2>$(NULL) || true $(SEP) \
		poetry run python manage.py migrate $(SEP) \
	else \
		echo Reset do banco de dados cancelado. $(SEP) \
	fi
endif


test: check-poetry ## Executar todos os testes (corresponde ao workflow do CI)
	@echo Executando testes...
	poetry run python manage.py test apps --verbosity=2


coverage: check-poetry
	@echo Executando testes com cobertura...

test-accounts: check-poetry ##  Rodar testes accounts app
	poetry run python manage.py test apps.accounts

test-core: check-poetry ##  Rodar testes core app
	poetry run python manage.py test apps.core

test-explore: check-poetry ##  Rodar testes explore app
	poetry run python manage.py test apps.explore

test-theme: check-poetry ##  Rodar testes theme app
	poetry run python manage.py test apps.theme

coverage: check-poetry ## Rodar testes com relatório de cobertura
	@echo "Rodando testes com relatorio de cobertura..."
	poetry run coverage run --source='.' manage.py test
	poetry run coverage report
	poetry run coverage html
