import os
from pathlib import Path
import dj_database_url # Importar dj_database_url para parsear la URL de PostgreSQL

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Asegúrate de que BASE_DIR esté definido correctamente en tu archivo original.
BASE_DIR = Path(__file__).resolve().parent.parent


# Modifica estas lineas para el despliegue en Render:

# 1. DEBUG: Volvemos a False para el entorno de producción.
DEBUG = False

# 2. ALLOWED_HOSTS: Se recomienda usar '*' para permitir el acceso desde Render.
ALLOWED_HOSTS = ['*']

# ... (El resto de tus configuraciones, como INSTALLED_APPS, MIDDLEWARE, etc., deben seguir aquí) ...

# --- CONFIGURACIÓN DE BASE DE DATOS PARA RENDER ---
# Usamos dj-database-url para configurar la base de datos usando la variable de entorno
DATABASES = {
    'default': dj_database_url.config(
        # La URL de la base de datos de Render se inyecta aquí automáticamente
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600, 
        conn_health_check=True,
    )
}

# Si la variable de entorno no está definida (ej: desarrollo local sin variable), 
# usa una configuración de SQLite local por defecto
if not os.environ.get('DATABASE_URL'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
# --- FIN CONFIGURACIÓN DE BASE DE DATOS ---


# --- CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS (MANDATORIA PARA RENDER) ---
# Este es el directorio donde 'collectstatic' reunirá todos los archivos estáticos.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# La URL para referenciar archivos estáticos
STATIC_URL = '/static/'

# Directorios adicionales donde Django buscará archivos estáticos (opcional, si no están dentro de las apps)
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'), # Descomenta si tienes una carpeta 'static' en la raíz
]

# Configuración de WhiteNoise para servir archivos estáticos comprimidos y cacheados
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Opcional, pero recomendado para producción:
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# (Asegúrate de que 'whitenoise.middleware.WhiteNoiseMiddleware' esté en tu MIDDLEWARE)
