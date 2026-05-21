from django.conf import settings
from django.db import models
from django.db.models import Sum


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    capacidad_maxima = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} – {self.ciudad}"

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'


class Evento(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = 'BORRADOR', 'Borrador'
        PUBLICADO = 'PUBLICADO', 'Publicado'
        CANCELADO = 'CANCELADO', 'Cancelado'
        FINALIZADO = 'FINALIZADO', 'Finalizado'

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    imagen_banner = models.ImageField(upload_to='events/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.BORRADOR)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos',
    )
    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.titulo

    @property
    def entradas_vendidas(self):
        return self.entradas.filter(pagado=True).count()

    @property
    def ingresos_totales(self):
        result = self.entradas.filter(pagado=True).aggregate(total=Sum('categoria__precio'))
        return result['total'] or 0

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-created_at']


class PrecioCategoria(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='categorias')

    def __str__(self):
        return f"{self.nombre} – ${self.precio}"

    @property
    def disponibles(self):
        vendidas = self.entradas.filter(pagado=True).count()
        return max(0, self.cantidad_disponible - vendidas)

    class Meta:
        verbose_name = 'Categoría de precio'
        verbose_name_plural = 'Categorías de precio'
