from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Aplicativos
    "django_ratelimit",
    "apps.core",
    "apps.accounts",
    "apps.explore",
    "apps.news",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.google_oauth",
                "apps.core.context_processors.admin_stats",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=str(BASE_DIR / "db.sqlite3")),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default=""),
        "PORT": config("DB_PORT", default=""),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "ratelimit-cache",
    }
}

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Arquivos de mídia (Conteúdo enviado pelo usuário)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Modelo de Usuário Personalizado
AUTH_USER_MODEL = "accounts.User"

# Configurações de autenticação
# Redirecionar para a página inicial onde o modal de login está disponível
LOGIN_URL = "core:landing"
LOGIN_REDIRECT_URL = "core:landing"
LOGOUT_REDIRECT_URL = "core:landing"

# Configurações do Google
# Deve ser definido no arquivo .env
GOOGLE_OAUTH_CLIENT_ID = config("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_MAPS_API_KEY = config("GOOGLE_MAPS_API_KEY", default="")

# Limitação de Taxa (para prevenir abuso de API)
RATELIMIT_ENABLE = config("RATELIMIT_ENABLE", default=True, cast=bool)
RATELIMIT_USE_CACHE = "default"  # Usar cache padrão para limitação de taxa
RATELIMIT_VIEW = "apps.explore.ratelimit_handlers.ratelimited_error"

# Silenciar avisos do django-ratelimit para LocMemCache em desenvolvimento
# Para produção com múltiplos processos, mude para Redis ou Memcached
SILENCED_SYSTEM_CHECKS = ["django_ratelimit.E003", "django_ratelimit.W001"]

# Configuração de testes
# Usar executor de testes personalizado para excluir .github da descoberta de testes
TEST_RUNNER = "config.test_runner.CustomTestRunner"
