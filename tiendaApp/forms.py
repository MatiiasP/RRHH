from django import forms
from tiendaApp.choices import sexos
from tiendaApp.models import Cargo, Departamento, Empleado, Solicitud
import datetime



class EmpleadoForm(forms.ModelForm):
    run = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. 17111222-K'}))
    codigoEmpleado = forms.CharField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese código empleado'}))
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese nombre'}))
    paterno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellido paterno'}))
    materno = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese apellido materno'}), required=False)
    sexo = forms.CharField(widget=forms.Select(choices=sexos, attrs={'class': 'form-control'}))
    sueldo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese sueldo'}))
    fechaNac = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'día/mes/año', 'type': 'date'}))

    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        empty_label="Selecciona un cargo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        empty_label="Selecciona un departamento",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Empleado
        fields = "__all__"
        exclude = ['creado']

        
    def clean_sueldo(self):
        sueldo = self.cleaned_data['sueldo']
        try:
            sueldo = int(sueldo)
        except ValueError:
            raise forms.ValidationError("El sueldo debe ser un número entero")
        
        if sueldo <= 0:
            raise forms.ValidationError("El sueldo debe ser mayor que cero.")
        return sueldo
    
    def clean_fechaNac(self):
        fecha_nacimiento = self.cleaned_data.get('fechaNac')

        fecha_minima = datetime.date(1900, 1, 1)
        fecha_maxima = datetime.date(2005, 12, 31)

        if fecha_nacimiento:
            if fecha_nacimiento < fecha_minima or fecha_nacimiento > fecha_maxima:
                raise forms.ValidationError('La fecha de nacimiento debe estar entre 1900 y 2005')
            
        return fecha_nacimiento
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if nombre and not nombre.isalpha() and ' ' not in nombre:
            raise forms.ValidationError("El nombre debe contener solo letras y espacios")
        return nombre


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['codigoEmpleado', 'nombre', 'tipo', 'fecha_inicio', 'fecha_fin'] 