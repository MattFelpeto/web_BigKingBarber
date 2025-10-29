# turnos/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Sucursal, Barbero, Horario, Turno
from datetime import datetime, timedelta, date, time
from django.db.models import Q


def index(request):
    """Renderiza la página principal."""
    # Asume que index.html está en: turnos/templates/turnos/index.html
    return render(request, 'turnos/index.html')

# --- Vista del Formulario Principal ---
def solicitar_turno(request):
    sucursales = Sucursal.objects.all()

    if request.method == 'POST':
        # Lógica de guardado del turno final
        try:
            barbero_id = request.POST.get('barbero')
            fecha = request.POST.get('fecha-turno')
            hora = request.POST.get('hora-turno')
            
            # Combina fecha y hora
            fecha_hora_str = f"{fecha} {hora}"
            # Asegura la conversión correcta al objeto datetime
            fecha_hora_dt = datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
            
            Turno.objects.create(
                barbero_id=barbero_id,
                fecha_hora=fecha_hora_dt,
                cliente_nombre=request.POST.get('nombre-cliente'),
                cliente_email=request.POST.get('mail'),
                cliente_telefono=request.POST.get('telefono'),
                duracion_minutos=30 # Aseguramos que el turno se guarda con 30 minutos
            )
            return redirect('turno_exitoso')
        except Exception as e:
            print(f"Error al guardar turno: {e}")
            return render(request, 'turnos/solicitar_turno.html', {'sucursales': sucursales, 'error_message': 'Hubo un error al reservar.'})


    return render(request, 'turnos/solicitar_turno.html', {'sucursales': sucursales})

def turno_exitoso(request):
    return render(request, 'turnos/turno_exitoso.html')

# --- Vistas API para AJAX ---

@csrf_exempt
def barberos_por_sucursal(request, sucursal_id):
    """Retorna los barberos de una sucursal dada."""
    barberos = Barbero.objects.filter(sucursal_id=sucursal_id).values('id', 'nombre')
    return JsonResponse(list(barberos), safe=False)


@csrf_exempt
def horas_disponibles(request, barbero_id, fecha_str):
    """Retorna los slots de 30 min libres para un barbero en una fecha específica,
    respetando su horario laboral (ej: 10:00 a 20:00).
    """
    try:
        fecha_dt = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        dia_semana = fecha_dt.weekday() # 0=Lunes, 6=Domingo
        
        DURACION_TURNO = 30 # Minutos, ¡Asegura 30 minutos por turno!
        
        # 1. Obtener horario base del barbero para ese día
        # Este objeto Horario es el que definirá si trabaja de 10:00 a 20:00
        horario = Horario.objects.get(barbero_id=barbero_id, dia_semana=dia_semana)
        
        # Combinar fecha con las horas de inicio y fin del horario
        hora_inicio = datetime.combine(fecha_dt, horario.hora_inicio)
        hora_fin = datetime.combine(fecha_dt, horario.hora_fin)
        
    except Horario.DoesNotExist:
        # Si no hay horario cargado para ese día, se asume no disponible
        return JsonResponse([], safe=False)
    except Exception:
        return JsonResponse([], safe=False)

    # 2. Obtener turnos ya reservados (filtrado estricto por barbero y fecha)
    turnos_reservados = Turno.objects.filter(
        barbero_id=barbero_id, 
        fecha_hora__date=fecha_dt
    ).order_by('fecha_hora')

    slots = []
    current_time = hora_inicio
    
    # 3. Iterar en franjas de 30 minutos
    while current_time + timedelta(minutes=DURACION_TURNO) <= hora_fin:
        slot_start = current_time
        slot_end = slot_start + timedelta(minutes=DURACION_TURNO)
        
        is_free = True
        
        # Verificar superposición con turnos ya reservados
        for turno in turnos_reservados:
            turno_start = turno.fecha_hora.replace(tzinfo=None)
            turno_end = turno_start + timedelta(minutes=turno.duracion_minutos)
            
            # Condición de superposición: [slot_start, slot_end) se solapa con [turno_start, turno_end)
            if slot_start < turno_end and turno_start < slot_end:
                is_free = False
                break
        
        # Solo agregar el slot si está libre Y el slot de inicio es en el futuro
        if is_free and slot_start > datetime.now(): 
            slots.append({
                'value': slot_start.strftime('%H:%M'), 
                'display': slot_start.strftime('%I:%M %p'),
            })
            
        current_time = slot_end # Avanzar 30 minutos

    return JsonResponse(slots, safe=False)