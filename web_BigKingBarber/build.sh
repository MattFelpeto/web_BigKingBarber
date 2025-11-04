#!/usr/bin/env bash
set -o errexit

# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Recopilar archivos estáticos (¡Necesario durante el build!)
python manage.py collectstatic --no-input

# 3. NOTA: El comando 'migrate' se ha movido al startCommand en render.yaml