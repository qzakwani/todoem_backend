from pathlib import Path
from datetime import timedelta

import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

VERIFICATION_KEY = os.getenv("VERIFICATION_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Application definition
ASGI_APPLICATION = "todoem.asgi.application"

INSTALLED_APPS = [
    "daphne",
    
    # My apps
    "account",
    "task",
    "lister",
    "tasklist",
    "taskgroup",
    "docs",
    
    "core",
    
    # Third party
    "rest_framework",
    "phonenumber_field",
    "django_celery_results",
    "anymail",
    "corsheaders",
    
    #
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "todoem.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            f'{BASE_DIR}/emails/',
            ],
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

WSGI_APPLICATION = "todoem.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Asia/Muscat'

USE_I18N = False

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


#* My settings *#

AUTH_USER_MODEL = 'account.User'

# email settings
MAIN_EMAIL_DOMAIN = "@todoem.xyz"
EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"

ANYMAIL = {
    "SENDGRID_API_KEY": os.getenv("SENDGRID_API_KEY"),
}


##################
###   RDREST   ###
##################
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    )
}



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(weeks=1),
    # 'ACCESS_TOKEN_LIFETIME': timedelta(seconds=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(weeks=4),
    "ROTATE_REFRESH_TOKENS": True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'id',
    
    'TOKEN_USER_CLASS': 'account.temp.TempUser',
}

##################
###   CELERY   ###
##################

CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_SERIALIZER = 'json'




####################
###   CHANNELS   ###
####################

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}



################
###   DOCS   ###
################
DOCS = {
    "USE_GENERATED": True,
    "PUBLIC": False,
    
    "META": {
        "openapi": "3.0.3",
        "info": {
            "title": "todoem API",
            "version": "1.0.0"
        },
    },
    "MODELS_SCHEMA": True,
    
    "SERVERS": {
        "ADD_CURRENT": True,
        "ADD_ALLOWED": False,
        "ADD": None
        },
    "JWT_SECURITY": {
        "ADD": True,
        "ALL": False,
    },

    "LOGIN_URL": "admin:login",
    
    "IGNORE_MODELS": [
        "DocsSettings",
        "TaskResult",
        "ChordCounter",
        "GroupResult",
        "DocsSchema",
        "LogEntry",
        "Permission",
        "Group",
        "ContentType",
        "Session",
    ]
}


STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


##  CORS  ##

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "POST",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Access-Control-Allow-Headers"
]