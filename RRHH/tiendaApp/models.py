from django.db import models
from django import forms
from django.utils import timezone # Esto para rescatar la fecha y hora del sistema
from tiendaApp.choices import sexos # Esto para rescatar la opciones de sexos
import os

class Cargo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Cargo')
    creado = models.DateTimeField(default=timezone.now) # obtenemos la fecha y hora del server
    
    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'cargo' # nombre con el que se creara la tabla
        verbose_name = 'Cargo' # como se mostrara la tabla en Admin
        verbose_name_plural = 'Cargos' # como se mostrara en plural

class Departamento(models.Model):
    codigo = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Departamento')
    creado = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        db_table = 'departamento' # nombre con el que se creara la tabla
        verbose_name = 'Departamento' # como se mostrara la tabla en Admin
        verbose_name_plural = 'departamentos' # como se mostrara en plural
class Empleado(models.Model):
    run = models.CharField(max_length=10, verbose_name='RUN')
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    paterno = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    materno = models.CharField(max_length=50, verbose_name='Apellido Materno', blank=True, null=True)
    sexo = models.CharField(max_length=1,choices=sexos, default='m')
    codigoEmpleado = models.CharField(max_length=20, verbose_name='Código de Empleado')
    sueldo = models.PositiveIntegerField(default=450000, verbose_name='Sueldo Base')
    fechaNac = models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')
    cargo = models.ForeignKey(Cargo, null=False,on_delete=models.RESTRICT)
    departamento = models.ForeignKey(Departamento, null=True,on_delete=models.CASCADE)
    creado = models.DateTimeField(default=timezone.now)
    hora_entrada = models.DateTimeField(null=True, blank=True)
    hora_salida = models.DateTimeField(null=True, blank=True)

    def generarNombre(instance, filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = 'empleados'
        fecha = timezone.now().strftime("%d%m%Y_%H%M%S")
        nombre = "{}.{}".format(fecha, extension)

        return os.path.join(ruta, nombre)
    
    foto = models.ImageField(upload_to=generarNombre, null=True, default='empleados/empleado.png')

    def __str__(self): 
        return "{} {} {}".format(self.nombre, self.paterno, self.materno)

    class Meta:
        db_table = 'empleado'
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['nombre', 'paterno', 'materno']

class Candidato(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    posicion_solicitada = models.CharField(max_length=100)
    estado = models.CharField(max_length=50, blank=True, default='En Proceso')
    # Otros campos que consideres necesarios

    def __str__(self):
        return self.nombre
