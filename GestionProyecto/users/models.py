from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Usuario personalizado con roles ORGANIZADOR / ASISTENTE / OPERADOR."""

    class Role(models.TextChoices):
        ORGANIZADOR = 'ORGANIZADOR', 'Organizador'
        ASISTENTE = 'ASISTENTE', 'Asistente'
        OPERADOR = 'OPERADOR', 'Operador'

    rol = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ASISTENTE,
    )
    telefono = models.CharField(max_length=20, blank=True)

    @property
    def is_organizador(self):
        return self.rol == self.Role.ORGANIZADOR

    @property
    def is_asistente(self):
        return self.rol == self.Role.ASISTENTE

    @property
    def is_operador(self):
        return self.rol == self.Role.OPERADOR

    def __str__(self):
        return self.username
