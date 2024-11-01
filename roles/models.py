from django.db import models
from django.conf import settings
from django.db import models

class Role(models.Model):
    """
    Modelo que representa un rol dentro de la plataforma (por ejemplo, admin, colaborador).
    """
    name = models.CharField(max_length=50, unique=True)  
    description = models.TextField(blank=True, null=True)  

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


