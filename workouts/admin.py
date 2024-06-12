from django.contrib import admin
from .models import Workout
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['date', 'calories_burned', 'workout_type','weight','repetitions' ,'descrizione','distance','utente','goal']

admin.site.register(Workout, WorkoutAdmin)
