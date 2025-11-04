#!/usr/bin/env bash

# Script de inicio para el servicio Web de Render.

# 1. Aplicar migraciones de la base de datos
# ESTO DEBE EJECUTARSE ANTES DE INICIAR EL SERVIDOR.
echo "Aplicando migraciones a la base de datos..."
python manage.py migrate

# 2. Iniciar Gunicorn
echo "Iniciando servidor Gunicorn..."
# Asegúrate de que 'web_BigKingBarber' sea el nombre correcto de tu carpeta principal del proyecto
gunicorn web_BigKingBarber.wsgi:application