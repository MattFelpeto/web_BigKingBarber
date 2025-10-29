# turnos/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # URL principal del formulario
    path('', views.index, name='home'),
    path('turnos/', views.solicitar_turno, name='solicitar_turno'),
    path('turno-exitoso/', views.turno_exitoso, name='turno_exitoso'), 

    # URLs API para AJAX
    path('api/barberos_por_sucursal/<int:sucursal_id>/', views.barberos_por_sucursal, name='api_barberos'),
    path('api/horas_disponibles/<int:barbero_id>/<str:fecha_str>/', views.horas_disponibles, name='api_horas'),
]