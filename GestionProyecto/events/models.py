from django.conf import settings
from django.db import models
from django.db.models import Sum


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    ciudad = models.CharField(max_length=100)
    capacidad_maxima = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return f'{self.nombre} — {self.ciudad}'


class Evento(models.Model):
    BORRADOR = 'BORRADOR'
    PUBLICADO = 'PUBLICADO'
    CANCELADO = 'CANCELADO'
    ESTADO_CHOICES = [
        (BORRADOR, 'Borrador'),
        (PUBLICADO, 'Publicado'),
        (CANCELADO, 'Cancelado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    imagen_banner = models.ImageField(upload_to='events/banners/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default=BORRADOR)
    ubicacion = models.ForeignKey(
        Ubicacion, on_delete=models.PROTECT, related_name='eventos'
    )
    organizador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='eventos_organizados',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return self.titulo

    @property
    def entradas_vendidas(self):
        return self.entradas.filter(pagado=True).count()

    @property
    def ingresos_totales(self):
        total = self.entradas.filter(pagado=True).aggregate(
            total=Sum('categoria__precio')
        )['total']
        return total or 0


class PrecioCategoria(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='categorias')
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Categoría de precio'
        verbose_name_plural = 'Categorías de precio'

    def __str__(self):
        return f'{self.nombre} — {self.evento.titulo}'

    @property
    def vendidas(self):
        return self.entradas.filter(pagado=True).count()

    @property
    def disponibles(self):
        return max(0, self.cantidad_disponible - self.vendidas)

    @property
    def agotado(self):
        return self.disponibles <= 0
