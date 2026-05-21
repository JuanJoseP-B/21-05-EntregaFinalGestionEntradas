from django.contrib import admin
from .models import Evento, PrecioCategoria, Ubicacion


class PrecioCategoriaInline(admin.TabularInline):
    model = PrecioCategoria
    extra = 1


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'organizador', 'estado', 'fecha_inicio', 'ubicacion')
    list_filter = ('estado',)
    search_fields = ('titulo',)
    inlines = [PrecioCategoriaInline]


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'capacidad_maxima')


@admin.register(PrecioCategoria)
class PrecioCategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'evento', 'precio', 'cantidad_disponible')
