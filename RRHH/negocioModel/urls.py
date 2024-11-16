from django.contrib import admin
from django.urls import path
from tiendaApp import views as vistas
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', vistas.inicio, name='inicio'),
    path('empleadoAdd/', vistas.crear_empleado, name='crearEmpleados'),
    path('empleados/', vistas.todos_empleados, name='empleados'),
    path('empleadoEdit/<int:empleado_id>', vistas.cargar_editar_empleado, name='editarEmpleado'),
    path('empleadoUpdate/<int:empleado_id>', vistas.editar_empleado, name='empleadoEditado'),
    path('empleadoDel/<int:empleado_id>', vistas.eliminar_empleado, name='eliminarEmpleado'),
    path('controla/', vistas.controla, name='controla'),
    path('solicitudes/', vistas.solicitudes_view, name='solicitudes'),
    path('reclutamiento/', vistas.reclutamiento, name='reclutamiento'),
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
