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
    path('empleados/editar/<int:id>/', vistas.cargar_editar_empleado, name='editarEmpleado'),  
    path('empleados/editado/<int:empleado_id>/', vistas.editar_empleado, name='empleadoEditado'),
    path('empleados/eliminar/<int:empleado_id>/', vistas.eliminar_empleado, name='eliminarEmpleado'),
    path('solicitudes/', vistas.solicitudes_view, name='solicitudes'),
    path('controla/', vistas.controla, name='controla'),
    path('reclutamiento/', vistas.reclutamiento, name='reclutamiento'),
    path('candidatos/<str:estado>/', vistas.candidatos_view, name='mostrar_candidatos'),
    path('mostrar-solicitudes/<str:estado>/', vistas.mostrar_solicitudes, name='mostrar_solicitudes'),
    path('solicitudes/aprobar/<int:id>/', vistas.aprobar_solicitud, name='aprobar_solicitud'),
    path('solicitudes/rechazar/<int:id>/', vistas.rechazar_solicitud, name='rechazar_solicitud'),
    path('solicitudes/estado/<str:estado>/', vistas.mostrar_solicitudes, name='mostrar_solicitudes_estado'),
    path('registrar_solicitud/', vistas.registrar_solicitud, name='registrar_solicitud'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


