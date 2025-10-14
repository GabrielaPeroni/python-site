POETRY := $(shell where poetry 2>nul)

.PHONY: help install setup migrate superuser run test clean lint format shell

help: ## Mostra log de ajuda
	@echo Comandos disponíveis:
	@echo.
	@echo   make install      - Instalar Poetry se não estiver presente
	@echo   make env          - Criar arquivo .env a partir de .env.example
	@echo   make setup        - Configuração completa: instalar dependências e migrar
	@echo   make migrate      - Executar migrações de banco de dados
	@echo   make superuser    - Criar superusuário Django
	@echo   make run          - Executar servidor de desenvolvimento
	@echo   make shell        - Abrir shell Django
	@echo   make clean        - Limpar cache e arquivos temporários
	@echo   make format       - Formatar código com black (se instalado)
	@echo   make lint         - Lint código com flake8 (se instalado)
	@echo   make db-shell     - Abrir shell do banco de dados
	@echo   make db-reset     - Redefinir banco de dados (deleta todos os dados)
	@echo.

check-poetry: ## Verifica se o Poetry está instalado
ifndef POETRY
	@echo Poetry não está instalado. Por favor, execute 'make install' primeiro.
	@exit 1
endif

install: ## Instalar Poetry usando pip
	@echo Verificando instalação do Poetry...
	@where poetry >nul 2>&1 || ( \
		echo Poetry não encontrado. Instalando Poetry... && \
		pip install poetry \
	)
	@echo Poetry está pronto!

env: ## Criar arquivo .env a partir de .env.example
	@if not exist .env ( \
		echo Criando arquivo .env a partir de .env.example... && \
		copy .env.example .env && \
		echo .env criado. Atualize as credenciais do banco de dados, se necessário. \
	) else ( \
		echo .env já existe. Ignorando... \
	)

deps: check-poetry ## Instalar dependências do projeto
	@echo Instalando dependências...
	poetry install

setup: install deps migrate ## Configuração completa do projeto
	@echo.
	@echo ========================================
	@echo Configuração completa!
	@echo ========================================
	@echo.
	@echo Próximos passos:
	@echo   1. Criar um superusuário: make superuser
	@echo   2. Executar o servidor: make run
	@echo.

migrate: check-poetry ## Executar migrações de banco de dados
	@echo Executando migrações...
	poetry run python manage.py migrate

makemigrations: check-poetry ## Criar novas migrações
	@echo Criando migrações...
	poetry run python manage.py makemigrations

superuser: check-poetry ## Criar superusuário Django
	poetry run python manage.py createsuperuser

run: check-poetry ## Executar servidor
	poetry run python manage.py runserver

shell: check-poetry ## Abrir shell Django
	poetry run python manage.py shell

clean: ## Limpar cache e arquivos temporários
	@echo Limpando cache e arquivos temporários...
	@if exist __pycache__ rmdir /s /q __pycache__
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@for /d /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
	@for /r %%i in (*.pyc) do @if exist "%%i" del /q "%%i"
	@for /r %%i in (*.pyo) do @if exist "%%i" del /q "%%i"
	@echo Limpeza completa!

collectstatic: check-poetry ## Coletar arquivos estáticos
	poetry run python manage.py collectstatic --noinput

startapp: check-poetry ## Criar um novo aplicativo Django (uso: make startapp name=myapp)
ifndef name
	@echo Erro: Por favor, forneça um nome de aplicativo. Uso: make startapp name=myapp
	@exit 1
endif
	poetry run python manage.py startapp $(name)

format: check-poetry ## Formatar código com black
	poetry run black . 2>nul || echo Black não está instalado. Execute: poetry add --group dev black

lint: check-poetry ## Lint código com flake8
	poetry run flake8 . 2>nul || echo Flake8 não está instalado. Execute: poetry add --group dev flake8

dev-deps: check-poetry ## Instalar dependências de desenvolvimento
	poetry add --group dev black flake8 pytest pytest-django

# Database commands
db-shell: check-poetry ## Abrir shell do banco de dados
	poetry run python manage.py dbshell

db-reset: check-poetry ## Resetar banco de dados (ATENÇÃO: deleta todos os dados)
	@echo ATENÇÃO: Isso irá deletar todos os dados!
	@set /p confirm="Você tem certeza? (sim/não): "
	@if "%confirm%"=="sim" ( \
		if exist db.sqlite3 del db.sqlite3 && \
		poetry run python manage.py migrate \
	) else ( \
		echo Reset do banco de dados cancelado. \
	)
