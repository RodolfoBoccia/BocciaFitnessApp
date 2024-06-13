from django.db import models
from django.conf import settings


class Workout(models.Model):
    WORKOUT_TYPES = (
        ('Corsa', 'Corsa'),
        ('Pesi', 'Pesi'),
        ('Cyclette', 'Cyclette'),
        ('Altro', 'Altro'),
    )
    date = models.DateField(auto_now_add=True)
    repetitions = models.IntegerField(null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    calories_burned = models.IntegerField(null=False, blank=False)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    descrizione = models.CharField(max_length=50, null=True, blank=True)
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, default=None)
    goal = models.ForeignKey('goals.GoalModel', on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.get_workout_type_display()
