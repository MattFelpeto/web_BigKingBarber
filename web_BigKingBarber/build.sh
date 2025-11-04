#!/usr/bin/env bash
set -o errexit

# 1. Instalar dependencias
echo "Instalando dependencias de Python..."
pip install -r requirements.txt

# 2. Recopilar archivos estáticos
# Esto se hace aquí para que WhiteNoise pueda procesarlos durante el build.
echo "Recolectando archivos estáticos durante el build..."
python manage.py collectstatic --no-input

# Nota: El comando 'migrate' se ha movido al start.sh para asegurar que se ejecute 
# cuando la base de datos esté lista antes de iniciar el servidor.