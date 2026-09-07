from django.db import models

# Modelo que representa a un paciente de la clínica.
# Cada paciente almacena datos básicos de contacto y personales.
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField()

    def __str__(self):
        # Mostrar el nombre del paciente en los listados y administración.
        return self.nombre


# Modelo que representa una cita o expediente clínico de un paciente.
# Un expediente contiene fecha, hora, tratamiento y detalles médicos.
class Expediente(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    tratamiento = models.TextField()
    notas = models.TextField()
    codigo_cie = models.CharField(max_length=20, blank=True)
    diagnostico = models.CharField(max_length=255, blank=True)
    nota_adicional = models.TextField(blank=True)

    def __str__(self):
        # Mostrar el paciente y la fecha/hora de la cita para identificar el expediente.
        return f"{self.paciente} - {self.fecha} {self.hora}"
    
# Modelo para almacenar diagnósticos CIE.
# Incluye el código y descripciones en español e inglés.
class DiagnosticoCIE(models.Model):

    codigo = models.CharField(
        max_length=20
    )

    nombre_es = models.TextField()

    nombre_en = models.TextField()

    def __str__(self):

        # Mostrar código y nombre en español en los listados.
        return f"{self.codigo} - {self.nombre_es}"