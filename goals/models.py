from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date


class GoalModel(models.Model):
    GOAL_CHOICES = (
        ('Perdita peso', 'Perdita peso'),
        ('Aumento massa muscolare', 'Aumento massa muscolare'),
        ('Miglioramento atletico', 'Miglioramento atletico'),
    )

    STATUS_CHOICES = (
        ('V', 'In Corso'),
        ('S', 'Scaduto'),
    )
    TEMP_CHOICES = (
        (1, '1 giorno'),
        (7, '1 settimana'),
        (30, '1 mese'),
        (90, '3 mesi'),
    )

    def get_status_color(self):
        if self.status == 'V':
            return 'green'
        elif self.status == 'S':
            return 'red'
        else:
            return ''

    def is_deadline_expired(self):
        today = date.today()
        if self.deadline < today:
            self.is_expired = True
            self.save()
            return True
        else:
            self.is_expired = False
            self.save()
            return False

    deadline = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='V')
    tempistica = models.IntegerField(choices=TEMP_CHOICES, default=30)
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=30, choices=GOAL_CHOICES)
    data_creazione = models.DateField(default=timezone.now)
    descrizione = models.TextField(max_length=255, blank=True, null=True)
    CaloriesGoal = models.IntegerField(default=0, blank=False, null=False)
    is_selected = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    cal = models.IntegerField(default=0)
