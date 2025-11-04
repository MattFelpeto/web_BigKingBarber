#!/usr/bin/env bash

# Salida inmediata si un comando falla
set -o errexit

# 1. Instalar dependencias
# Render detectó que usas requirements.txt
pip install -r requirements.txt

# 2. Recolectar archivos estáticos
# El flag --noinput evita que el proceso se detenga esperando confirmación.
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# 3. CRUCIAL: Ejecutar las migraciones
# Este paso crea o actualiza las tablas de la base de datos (incluyendo la tabla de turnos)
# y debe ocurrir antes de que el servidor Gunicorn inicie.
echo "Ejecutando migraciones de base de datos..."
python manage.py migrate
