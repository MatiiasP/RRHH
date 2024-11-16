from django.shortcuts import render, redirect, get_object_or_404
from tiendaApp.forms import EmpleadoForm
from tiendaApp.models import Empleado, Cargo, Departamento
from django.utils import timezone
from .models import Candidato

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
    return render(request, 'tiendaTemplates/empleados.html', data)

def cargar_editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)
    form = EmpleadoForm(instance=empleado)

    return render(request, 'tiendaTemplates/empleadoEdit.html', {'form':form, 'empleado':empleado})


def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            if 'foto' in request.FILES:
                empleado.foto = request.FILES['foto']
            form.save()
            return redirect('empleados')
        
    else:
        form = EmpleadoForm(instance=empleado)
    
    return render(request, 'tiendaTemplates/empleados.html', {'form':form})

def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        empleado.delete()
        return redirect('empleados')
    
    return render( request, 'tiendaTemplates/empleadoDel.html', {'empleado': empleado})

from django.shortcuts import render
from django.utils import timezone
from .models import Empleado

from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Empleado

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

def solicitudes_view(request):
    return render(request, 'tiendaTemplates/solicitudes.html')

def reclutamiento(request):
    if request.method == 'POST':
        # Manejo de archivo subido
        file = request.FILES.get('candidato_file')
        if file:
            # Procesa el archivo (por ejemplo, guardarlo, leerlo, etc.)
            pass  # Aquí va tu lógica para manejar el archivo

    # Tu lógica para obtener candidatos
    candidatos = Candidato.objects.all()  # Cambia esto según tu lógica

    return render(request, 'tiendaTemplates/reclutamiento.html', {'candidatos': candidatos})