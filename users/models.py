from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class CustomUser(AbstractUser):
    nome = models.CharField(max_length=100, null=True, blank=True)
    cognome = models.CharField(max_length=100, null=True, blank=True)
    età = models.PositiveIntegerField(null=True, blank=True)
    peso = models.PositiveIntegerField(null=True, blank=True)
    altezza = models.PositiveIntegerField(null=True, blank=True)
