from django.contrib import admin

# Register your models here.

from tiendaApp.models import Cargo, Departamento, Empleado

class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre']

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['run', 'nombre', 'paterno', 'materno', 'sexo', 'codigoEmpleado', 'sueldo', 'fechaNac', 'cargo', 'departamento']


admin.site.register(Cargo, CargoAdmin)
admin.site.register(Departamento, DepartamentoAdmin)
admin.site.register(Empleado, EmpleadoAdmin)