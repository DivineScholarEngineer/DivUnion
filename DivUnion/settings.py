"""Django settings for the DivUnion project.

The configuration is intentionally compact but production ready enough for
local development and the Netlify static export build used by this
repository.  Values that should be customised in production can be
provided via environment variables.
"""

from __future__ import annotations

from pathlib import Path
import os
from typing import Any, Dict, List

BASE_DIR = Path(__file__).resolve().parent.parent


def env_str(name: str, default: str) -> str:
    """Return a cleaned environment variable value."""

    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


def env_int(name: str, default: int) -> int:
    """Return an integer environment variable value."""

    value = os.environ.get(name)
    if value is None:
        return default
    value = value.strip()
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default

# Security -----------------------------------------------------------------
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-9@x6$0y4r@7vqumr8vmt=*#)w=b^=f8@9a2t-#=3w)y=z!m6m!",
)
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

raw_allowed_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
if raw_allowed_hosts:
    ALLOWED_HOSTS: List[str] = [host.strip() for host in raw_allowed_hosts.split(",") if host.strip()]
else:
    ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# Applications --------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_filters",
    "django_distill",
    "accounts",
    "store",
]

CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5"]
CRISPY_TEMPLATE_PACK = "bootstrap5"

AUTH_USER_MODEL = "accounts.CustomUser"

# Middleware ----------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "DivUnion.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "DivUnion.wsgi.application"
ASGI_APPLICATION = "DivUnion.asgi.application"

# Database ------------------------------------------------------------------
DATABASES: Dict[str, Dict[str, Any]] = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

mysql_requested = env_str("DJANGO_DB_ENGINE", "").lower() == "mysql"
mysql_requested = mysql_requested or bool(env_str("MYSQL_DATABASE", ""))
mysql_requested = mysql_requested or bool(env_str("DJANGO_DB_NAME", ""))

if mysql_requested:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env_str("MYSQL_DATABASE", env_str("DJANGO_DB_NAME", "divunion")),
        "USER": env_str("MYSQL_USER", env_str("DJANGO_DB_USER", "")),
        "PASSWORD": env_str("MYSQL_PASSWORD", env_str("DJANGO_DB_PASSWORD", "")),
        "HOST": env_str("MYSQL_HOST", env_str("DJANGO_DB_HOST", "localhost")),
        "PORT": env_str("MYSQL_PORT", env_str("DJANGO_DB_PORT", "3306")),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
        "CONN_MAX_AGE": env_int("DJANGO_DB_CONN_MAX_AGE", 60),
    }

# Password validation -------------------------------------------------------
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

# Internationalisation ------------------------------------------------------
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & media ------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DISTILL_DIR = BASE_DIR / "distill_build"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "index"
LOGOUT_REDIRECT_URL = "index"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # 30 days
SESSION_COOKIE_HTTPONLY = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)

COOKIE_CONSENT_NAME = "cookie_consent"
