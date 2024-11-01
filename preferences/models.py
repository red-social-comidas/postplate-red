from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

CustomUser = get_user_model()


class Preferences(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='preferences'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Preference'
        verbose_name_plural = 'Preferences'
