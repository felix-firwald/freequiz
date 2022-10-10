from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

STATUSES = [
    ('dark', 'полезная информация'),
    ('warning', 'предупреждение'),
    ('danger', 'срочное объявление')
]


class Notification(models.Model):
    name = models.CharField(max_length=60, verbose_name='название')
    showbar = models.CharField(
        max_length=255,
        verbose_name='короткое описание'
    )
    slug = models.SlugField(unique=True, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=STATUSES
    )

    class Meta:
        verbose_name = 'Оповещение'
        verbose_name_plural = 'Оповещения'
        ordering = ['pk']


class Delivered(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
