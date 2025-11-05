import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Requerido: Asegúrate de configurar la variable de entorno SECRET_KEY en Render.
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-django-secret-key-for-local-dev')


# Modifica estas lineas para el despliegue en Render:

# 1. DEBUG: Correctamente en False para producción.
DEBUG = False

# 2. ALLOWED_HOSTS: ¡LA CORRECCIÓN CRÍTICA ESTÁ AQUÍ!
#    Añadimos '127.0.0.1' para que el Health Check de Render (que viene de localhost)
#    no falle y provoque un error 500.
ALLOWED_HOSTS = [
    'web-bigkingbarber.onrender.com', # Tu dominio principal
    '127.0.0.1',                      # Para el Health Check de Render
]

# Mantenemos la lógica de la variable de entorno por si Render la inyecta a tiempo
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    'appWebBKB.apps.AppwebbkbConfig', # Referencia corregida a tu AppConfig
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    # Otras apps deben ir aquí
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise debe ir justo después de SecurityMiddleware para servir archivos estáticos eficientemente
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web_BigKingBarber.urls' # Ajusta si el nombre de tu proyecto es diferente

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Agrega si tienes una carpeta templates a nivel de proyecto
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

WSGI_APPLICATION = 'web_BigKingBarber.wsgi.application' # Ajusta si el nombre de tu proyecto es diferente


# --- CONFIGURACIÓN DE BASE DE DATOS PARA RENDER ---
# Usamos dj-database-url para configurar la base de datos usando la variable de entorno
# La configuración prioriza la variable de entorno DATABASE_URL de Render si existe.
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600, 
            # Corregido el error de sintaxis: 'conn_health_check' -> 'conn_health_checks'
            conn_health_checks=True,
        )
    }
else:
    # Configuración de desarrollo local (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# --- FIN CONFIGURACIÓN DE BASE DE DATOS ---


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-ar' # Configurado a español de Argentina

TIME_ZONE = 'America/Argentina/Buenos_Aires' # Configurado a zona horaria de Argentina

USE_I18N = True

USE_TZ = True


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (MANDATORIA PARA RENDER) ---
# Este es el directorio donde 'collectstatic' reunirá todos los archivos estáticos.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# La URL para referenciar archivos estáticos
STATIC_URL = '/static/'

# Directorios adicionales donde Django buscará archivos estáticos (opcional, si no están dentro de las apps)
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'), # Descomenta si tienes una carpeta 'static' en la raíz
]

# --- ¡LA CORRECCIÓN DEL ERROR 500 ESTÁ AQUÍ! ---
# Configuración de WhiteNoise para servir archivos estáticos comprimidos y cacheados
STORAGES = {
    "staticfiles": {
        # Cambiamos de 'CompressedManifestStaticFilesStorage' (que da error 500 si falta un archivo)
        # a 'CompressedStaticFilesStorage' (que solo dará 404, pero no rompe el sitio).
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# --- CONFIGURACIÓN DE SEGURIDAD PARA PRODUCCIÓN (HTTPS/PROXY) ---

# Comentamos la redirección SSL de Django porque Render ya la maneja.
# SECURE_SSL_REDIRECT = True

# Estas líneas son seguras y recomendadas.
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
