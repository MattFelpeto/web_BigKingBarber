# turnos/models.py

from django.db import models

# Modelos auxiliares 
DIAS_SEMANA = (
    (0, 'Lunes'),
    (1, 'Martes'),
    (2, 'Miércoles'),
    (3, 'Jueves'),
    (4, 'Viernes'),
    (5, 'Sábado'),
    (6, 'Domingo'),
)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Barbero(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='barberos')

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.sucursal.nombre})"

class Horario(models.Model):
    """Define el horario regular de trabajo de un barbero por día de la semana.
    
    Para cumplir con el requerimiento de 10:00 a 20:00, deberás cargar estos valores
    en la base de datos para cada día que el barbero trabaje.
    """
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE, related_name='horarios')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA) # 0=Lunes, 6=Domingo
    hora_inicio = models.TimeField() # Debe ser cargado como 10:00:00
    hora_fin = models.TimeField()     # Debe ser cargado como 20:00:00
    
    class Meta:
        unique_together = ('barbero', 'dia_semana')

    def __str__(self):
        return f"Horario de {self.barbero.nombre} - {self.get_dia_semana_display()}"


# Modelo principal
class Turno(models.Model):
    barbero = models.ForeignKey(Barbero, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    
    # Datos del Cliente
    cliente_nombre = models.CharField(max_length=150)
    cliente_email = models.EmailField()
    cliente_telefono = models.CharField(max_length=20)
    
    duracion_minutos = models.IntegerField(default=30) # ¡Aquí se define la duración base!

    def __str__(self):
        return f"Turno de {self.cliente_nombre} con {self.barbero.nombre} el {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"