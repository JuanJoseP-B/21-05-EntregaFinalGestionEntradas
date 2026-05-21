from django.contrib import admin
from .models import Entrada


@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    list_display = ('codigo_unico', 'evento', 'asistente', 'categoria', 'pagado', 'usado', 'fecha_compra')
    list_filter = ('pagado', 'usado', 'evento')
    search_fields = ('codigo_unico', 'asistente__username')
    readonly_fields = ('codigo_unico', 'fecha_compra')
