import uuid
from django.conf import settings
from django.db import models


class Entrada(models.Model):
    codigo_unico = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    pagado = models.BooleanField(default=False)
    usado = models.BooleanField(default=False)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    codigo_qr = models.ImageField(upload_to='qr/', blank=True, null=True)
    asistente = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entradas',
    )
    categoria = models.ForeignKey(
        'events.PrecioCategoria',
        on_delete=models.CASCADE,
        related_name='entradas',
    )
    evento = models.ForeignKey(
        'events.Evento',
        on_delete=models.CASCADE,
        related_name='entradas',
    )

    def __str__(self):
        return f"{self.codigo_unico[:8]}… – {self.evento}"

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
        ordering = ['-fecha_compra']
