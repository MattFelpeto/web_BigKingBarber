# turnos/admin.py

from django.contrib import admin
from .models import Sucursal, Barbero, Horario, Turno

# --- Personalización de Modelos en el Admin ---

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de sucursales
    list_display = ('nombre', 'direccion')
    search_fields = ('nombre', 'direccion')

@admin.register(Barbero)
class BarberoAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de barberos
    list_display = ('nombre', 'apellido', 'sucursal')
    # Filtro lateral para buscar por sucursal
    list_filter = ('sucursal',)
    search_fields = ('nombre', 'apellido')

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de horarios
    list_display = ('barbero', 'dia_semana', 'hora_inicio', 'hora_fin')
    # Filtro y búsqueda para encontrar horarios fácilmente
    list_filter = ('barbero', 'dia_semana')
    search_fields = ('barbero__nombre',) # Permite buscar por el nombre del barbero

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de turnos
    list_display = ('cliente_nombre', 'barbero', 'fecha_hora', 'cliente_telefono', 'duracion_minutos')
    # Filtros avanzados
    list_filter = ('barbero', 'fecha_hora', 'duracion_minutos')
    # Campos para búsqueda rápida
    search_fields = ('cliente_nombre', 'cliente_email', 'barbero__nombre')
    # Ordenar por defecto por la fecha y hora más reciente
    ordering = ('-fecha_hora',)


# Nota importante para probar la lógica de 10:00 a 20:00:
# ¡Asegúrate de ir al administrador (http://127.0.0.1:8000/admin/)
# y crear los registros necesarios en las tablas Sucursal, Barbero y Horario!
# En Horario, debes usar 10:00:00 como hora_inicio y 20:00:00 como hora_fin.