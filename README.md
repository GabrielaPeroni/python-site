# MaricaCity - Sistema de turismo local

Este projeto é um **remake** de um aplicativo feito para o projeto Qualifica Maricá
O repositório original pode ser encontrado aqui: [Marica-City](https://github.com/GabrielaPeroni/Marica-City).

- Projeto criado para fins acadêmicos para a matéria 'Desenvolvimento Rápido em Python'
- A estrutura permite adicionar múltiplos apps e páginas facilmente.
- Todas as dependências gerenciadas com Poetry e Makefile.

Para mais detalhes sobre a implementação do CRUD, consulte [CRUD.md](./CRUD.md)

# 🚀 Como rodar o projeto

### Pre-requisitos

- Python 3.10+
- Make (para Windows, instale usando chocolatey: `choco install make` ou use Git Bash)

### 1. Instale as dependências e ative o ambiente virtual

```bash
make setup
```

### 2. Crie um superuser (opcional) e rode o servidor:

```bash
make superuser
make run
```

## 📖 Setup manual (sem o MakeFile)

### 1. Instale Poetry e dependencias:

```bash
pip install poetry
poetry install
```

### 2. Rode migrations:

```bash
poetry run python manage.py migrate
```

### 3. Crie um superuser (opcional):

```bash
poetry run python manage.py createsuperuser
```

### 4. Rode o servidor:

```bash
poetry run python manage.py runserver
```

## 📜 Licença

- **Código Django**: [MIT](./LICENSE.txt).
