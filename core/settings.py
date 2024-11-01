from pathlib import Path
import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()  # cargar el .env para poder usar las variables de entorno
# IMPORTANTE: EL .env DEBE ESTAR EN LA RAIZ DEL PROYECTO RUTA "backend/core/.env"

from datetime import timedelta

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k(d=ov2cc%x*453*98e8inj3u0j3mfdcmellkx2(1v*540_9$&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

PROJECT_APPS = [
    'core',
    'users',
    'publication',
    'roles',
    'friendship',
    'preferences',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'drf_yasg',  # Documentation
    'corsheaders',
    # Garantiza que el refresh token anterior quede invalidado una vez que se rota, lo que evita que se usen tokens antiguos.
    'rest_framework_simplejwt.token_blacklist',
    'cloudinary',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# -------DB SQL-LITE------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ------DB SQL SERVER-------

# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'DB-NOCOUNTRY',  # El nombre de tu base de datos
#         'USER': '***',  # Deja en blanco si usas autenticación de Windows
#         'PASSWORD': '***',  # Deja en blanco si usas autenticación de Windows
#         'HOST': '***',  # El nombre de tu servidor
#         'PORT': '',  # El puerto por defecto de SQL Server
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',  # Cambia el driver a la versión
#             'trusted_connection': 'yes',  # Autenticación de Windows
#             'TrustServerCertificate': 'yes',  # Confía en el certificado del servidor
#             'Encrypt': 'False',  # Desactiva la encriptación SSL
#         },
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Archivo settings.py
AUTH_USER_MODEL = 'users.CustomUser'


# -------------------------------------------------------------
# Configuración de Django Rest Framework para usar JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # Solo usuarios autenticados por defecto
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Para la documentación automática
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Tiempo de vida del token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,  # Rotación automática de tokens
    'BLACKLIST_AFTER_ROTATION': True,
    # Prefijo para el token en las cabeceras HTTP
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Configuracion de 'drf_spectacular_sidecar' para la DOC
SPECTACULAR_SETTINGS = {
    'TITLE': 'Documentación de mi API',
    'DESCRIPTION': 'Descripción breve de la API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # Para usar los archivos locales
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Configuracion de cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
