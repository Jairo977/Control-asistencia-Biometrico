from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('user', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='user')
    groups = models.ManyToManyField(
        Group,
        related_name='usuario_set',
        blank=True,
        verbose_name='grupos'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuario_set',
        blank=True,
        verbose_name='permisos de usuario'
    )

    def es_admin(self):
        return self.rol == 'admin' or self.is_superuser

    def __str__(self):
        return self.username
