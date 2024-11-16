from django.shortcuts import render, redirect, get_object_or_404
from tiendaApp.forms import EmpleadoForm, SolicitudForm
from tiendaApp.models import Empleado, Cargo, Departamento
from django.utils import timezone
from .models import Candidato, Empleado, Solicitud
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .forms import SolicitudForm


# Create your views here.
def inicio(request):
    return render(request, 'tiendaTemplates/inicio.html')

def crear_empleado(request):
    if request.method == "POST":
        form  = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = EmpleadoForm()

    return render(request, 'tiendaTemplates/empleadoAdd.html', {'form': form})

def todos_empleados(request):
    empleados = Empleado.objects.all()
    cargo = Cargo.objects.all()
    departamento = Departamento.objects.all()

    data = {
        'empleados': empleados,
        'cargos': cargo,
        'departamentos': departamento,
    }
    return render(request, 'tiendaTemplates/empleados.html', {'empleados': empleados})

def cargar_editar_empleado(request, id):  # Cambia empleado_id a id
    empleado = get_object_or_404(Empleado, id=id)  # Usa id aquí
    form = EmpleadoForm(instance=empleado)

    return render(request, 'tiendaTemplates/empleadoEdit.html', {'form': form, 'empleado': empleado})


def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)  # Asegúrate de que el modelo y la ID sean correctos
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)  # Agrega `request.FILES` para manejar archivos
        if form.is_valid():
            form.save()
            # Redirige a una vista de éxito (puede ser la lista de empleados o la página de detalle)
            return redirect('inicio')  # Cambia 'inicio' si quieres redirigir a otro lugar, como un detalle de empleado
    else:
        form = EmpleadoForm(instance=empleado)
    
    return render(request, 'tiendaTemplates/empleadoEdit.html', {
        'form': form,
        'empleado': empleado  # Pasamos `empleado` en lugar de `empleado_id` para mayor flexibilidad
    })

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados')
    
    return render( request, 'tiendaTemplates/empleadoDel.html', {'empleado': empleado})





def controla(request):
    # Captura el ID del empleado desde la solicitud GET, si existe
    employee_id = request.GET.get('employeeId')

    # Si se proporciona un ID, filtra los empleados por ese ID, de lo contrario, muestra todos
    if employee_id:
        empleados = Empleado.objects.filter(codigoEmpleado=employee_id)
    else:
        empleados = Empleado.objects.all()

    # Procesamiento de la entrada/salida/limpieza cuando se envía una solicitud POST
    if request.method == 'POST':
        action = request.POST.get('action')
        codigoEmpleado = action.split('_')[1]  # Obtener el ID del empleado desde el nombre del botón
        empleado = Empleado.objects.get(codigoEmpleado=codigoEmpleado)

        if 'entrada' in action:
            empleado.hora_entrada = timezone.now()
            empleado.save()
        elif 'salida' in action:
            empleado.hora_salida = timezone.now()
            empleado.save()
        elif 'limpiar' in action:
            empleado.hora_entrada = None  # Limpiar hora de entrada
            empleado.hora_salida = None   # Limpiar hora de salida
            empleado.save()  # Guardar cambios

    return render(request, 'tiendaTemplates/controla.html', {'empleados': empleados})


def reclutamiento(request):
    if request.method == "POST":
        action = request.POST.get("action", "")
        
        # Guardar nuevo candidato
        if "nombre" in request.POST:
            nombre = request.POST["nombre"]
            email = request.POST["email"]
            telefono = request.POST["telefono"]
            posicion_solicitada = request.POST["posicion_solicitada"]
            curriculum = request.FILES.get("curriculum")
            
            nuevo_candidato = Candidato(
                nombre=nombre,
                email=email,
                telefono=telefono,
                posicion_solicitada=posicion_solicitada,
                curriculum=curriculum,
            )
            nuevo_candidato.save()
            return redirect('reclutamiento')

        # Aprobar o rechazar candidato
        elif action.startswith("aprobar_"):
            candidato_id = action.split("_")[1]
            Candidato.objects.filter(id=candidato_id).update(estado="Aprobado")
        elif action.startswith("rechazar_"):
            candidato_id = action.split("_")[1]
            Candidato.objects.filter(id=candidato_id).update(estado="Rechazado")

    # Obtener todos los candidatos
    candidatos = Candidato.objects.all()
    return render(request, 'tiendaTemplates/reclutamiento.html', {'candidatos': candidatos})

def candidatos_view(request, estado):
    candidatos = Candidato.objects.filter(estado=estado)
    return render(request, 'tiendaTemplates/candidatos_list.html', {'candidatos': candidatos})
    


def registrar_solicitud(request):
    if request.method == 'POST':
        # Capturamos los datos del formulario
        codigoEmpleado = request.POST.get('codigoEmpleado')
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        archivo = request.FILES.get('archivo')  # Para manejar el archivo adjunto

        # Creamos una nueva instancia de Solicitud
        nueva_solicitud = Solicitud(
            codigoEmpleado_id=codigoEmpleado,
            nombre=nombre,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        try:
            nueva_solicitud.save()  # Guardar la nueva solicitud en la base de datos
            messages.success(request, 'Solicitud registrada con éxito.')
            return redirect('mostrar_solicitudes', estado='Pendiente')
        except Exception as e:
            messages.error(request, f'Error al guardar la solicitud: {str(e)}')

    return render(request, 'solicitudes.html') 

def solicitudes_view(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        codigoEmpleado = request.POST.get('codigoEmpleado')
        nombre = request.POST.get('nombre')
        tipo = request.POST.get('tipo')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        
        # Crea una nueva solicitud
        nueva_solicitud = Solicitud(
            codigoEmpleado=codigoEmpleado,
            nombre=nombre,
            tipo=tipo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        nueva_solicitud.save()

        messages.success(request, "Solicitud registrada exitosamente.")
        return redirect('solicitudes_view')  # Redirige a la vista de solicitudes

    # Si no es un POST, obtenemos todas las solicitudes
    solicitudes = Solicitud.objects.all()
    empleados = Empleado.objects.all()

    data = {
        'solicitudes': solicitudes,
        'empleados': empleados
    }
    return render(request, 'tiendaTemplates/solicitudes.html', data)

def aprobar_solicitud(request, id):
    if request.method == 'POST':
        solicitud = get_object_or_404(Solicitud, id=id)  # Obtener la solicitud o 404 si no existe
        solicitud.estado = 'Aprobado'  # Cambiar el estado a Aprobado
        solicitud.save()  # Guardar los cambios
        return redirect('solicitudes')
    
def rechazar_solicitud(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    solicitud.estado = 'Rechazado'  # Cambia el estado
    solicitud.save()
    return redirect('solicitudes')

def mostrar_solicitudes(request, estado):
    if estado == 'Aprobado' or estado == 'Rechazado':
        solicitudes = Solicitud.objects.filter(estado=estado)
    else:
        solicitudes = Solicitud.objects.all()  # Puedes modificar esto según lo que necesites para otros casos.
    
    # Pasar el contexto a la plantilla
    context = {
        'solicitudes': solicitudes,
        'estado': estado,
    }
    return render(request, 'tiendaTemplates/solicitudes_filtradas.html', context)

def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitud creada con éxito.')
            return redirect('inicio')
    else:
        form = SolicitudForm()
    return render(request, 'tiendaTemplates/solicitud.html', {'form': form})





def registrar_solicitud_(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            # Obtén el código del empleado de los datos del formulario
            codigoEmpleado = form.cleaned_data['codigoEmpleado']  # Asegúrate de que esto esté en tu formulario
            # Busca la instancia de Empleado correspondiente
            empleado = Empleado.objects.get(codigoEmpleado=codigoEmpleado)
            # Crea la solicitud
            solicitud = form.save(commit=False)  # No guarda aún en la base de datos
            solicitud.codigoEmpleado = empleado  # Asigna la instancia de Empleado
            
            solicitud.save()  # Guarda la solicitud en la base de datos
            return redirect('tiendaTemplates/mostrar_solicitudes.html')
    else:
        form = SolicitudForm()
    
    return render(request, 'tiendaTemplates/solicitudes.html', {'form': form})

