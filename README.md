# MaricaCity - Sistema de turismo local

Este projeto é um **remake** de um aplicativo feito para o projeto Qualifica Maricá
O repositório original pode ser encontrado aqui: [Marica-City](https://github.com/GabrielaPeroni/Marica-City).

- Projeto criado para fins acadêmicos para a matéria 'Desenvolvimento Rápido em Python'
- A estrutura permite adicionar múltiplos apps e páginas facilmente.
- Todas as dependências gerenciadas com Poetry e Makefile.

Para mais detalhes sobre a implementação do CRUD, consulte [CRUD.md](./documentacao/CRUD.md)
Para uma visão completa da estrutura do projeto e arquitetura, consulte [STRUCTURE.md](./documentacao/STRUCTURE.md)

# 🚀 Como rodar o projeto

### Pre-requisitos

- Python 3.10+
- Make (para Windows, instale usando chocolatey: `choco install make` ou use Git Bash)
- **Importante para Windows**: Este projeto inclui `poetry.toml` configurado para evitar problemas com caminhos de arquivo longos (MAX_PATH). O ambiente virtual será criado na pasta `.venv/` do projeto.

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

## 🛠️ Troubleshooting

### Windows: Erro de caminho de arquivo muito longo

Se você encontrar erros como `[WinError 206] O nome do arquivo ou extensão é muito longo` ou problemas ao instalar dependências (especialmente joblib ou outras libs), siga estes passos:

**Solução 1: Usar a configuração do projeto (Recomendado)**
Este projeto já inclui `poetry.toml` que cria o ambiente virtual em `.venv/` no diretório do projeto, evitando caminhos longos.

```bash
# Remova qualquer ambiente virtual existente
poetry env remove --all

# Reinstale as dependências (o poetry.toml será aplicado automaticamente)
poetry install
```

**Solução 2: Habilitar caminhos longos no Windows 10/11**
Execute como Administrador no PowerShell:

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

Reinicie o computador após executar este comando.

**Solução 3: Usar caminho mais curto para o projeto**
Mova o projeto para um diretório com caminho mais curto, como:

```
C:\dev\marica-city\
```

ao invés de:

```
C:\Users\Noell\Documents\Personal\GitHub\marica-city-remake\
```

## 📜 Licença

- **Código Django**: [MIT](./documentacao/LICENSE.txt).
