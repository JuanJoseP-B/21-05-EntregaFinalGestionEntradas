from django import forms
from .models import Evento, Ubicacion, PrecioCategoria


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ('nombre', 'direccion', 'ciudad', 'capacidad_maxima')


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ('titulo', 'descripcion', 'fecha_inicio', 'fecha_fin', 'imagen_banner', 'estado', 'ubicacion')
        widgets = {
            'fecha_inicio': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'fecha_fin': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M',
            ),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_inicio'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['fecha_fin'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['ubicacion'].required = False
        self.fields['imagen_banner'].required = False


class PrecioCategoriaForm(forms.ModelForm):
    class Meta:
        model = PrecioCategoria
        fields = ('nombre', 'precio', 'cantidad_disponible')
