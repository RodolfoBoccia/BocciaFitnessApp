from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, DeleteView, UpdateView
from .forms import WorkoutForm
from .models import Workout
from obiettivi.models import GoalModel


class CreateWorkoutsView(LoginRequiredMixin, FormView):
    template_name = 'add_workout.html'
    form_class = WorkoutForm
    success_url = reverse_lazy('workout_list')

    def form_valid(self, form):
        form.instance.utente = self.request.user

        try:
            obiettivo_principale = GoalModel.objects.get(utente=self.request.user, is_selected=True)
        except ObjectDoesNotExist:
            obiettivo_principale = None

        if obiettivo_principale is not None:
            if not obiettivo_principale.is_deadline_expired():
                if not obiettivo_principale.is_completed:
                    obiettivo_principale.cal += form.instance.calories_burned
                    form.instance.goal = obiettivo_principale
                    if obiettivo_principale.cal >= obiettivo_principale.CaloriesGoal:
                        obiettivo_principale.is_completed = True
                    obiettivo_principale.save()

        #Ho aggiunto questo if all'inizio per evitare che l'utente possa aggiungere un workout ad un obiettivo scaduto!
        form.save()
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        try:
            obiettivo_principale = GoalModel.objects.get(utente=self.request.user, is_selected=True)
        except ObjectDoesNotExist:
            obiettivo_principale = None

        return super().get(request, *args, **kwargs)


@login_required
def workout_list(request):
    workouts = Workout.objects.filter(utente=request.user)
    return render(request, 'workout_list.html', {'workouts': workouts})


class WorkoutsView(FormView):
    template_name = 'workouts_detail.html'
    form_class = WorkoutForm


class WorkoutsDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = 'workouts_delete.html'
    success_url = reverse_lazy('workout_list')

    """def form_valid(self, form):
        elem = self.get_object()
        calories = elem.calories_burned

        try:
            obiettivo_principale = elem.goal
        except ObjectDoesNotExist:
               obiettivo_principale = None

        if obiettivo_principale is not None:
            if obiettivo_principale.cal <= calories:
                obiettivo_principale.cal = 0
            else:
                obiettivo_principale.cal = obiettivo_principale.cal - calories

            if obiettivo_principale.is_completed and obiettivo_principale.cal < obiettivo_principale.CaloriesGoal:
                obiettivo_principale.is_completed = False

        obiettivo_principale.save()
        elem.delete()
        return super().form_valid(form)"""


class WorkoutsUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    form_class = WorkoutForm
    template_name = 'update_workout.html'
    success_url = reverse_lazy('workout_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def form_valid(self, form):
        old_workout = self.get_object()
        new_workout = form.save(commit=False)  # Salva il nuovo Workout ma non lo aggiungo al database ancora
        old_calories = old_workout.calories_burned  # Ottengo le calorie del vecchio Workout

        try:
            obiettivo_principale = old_workout.goal
        except ObjectDoesNotExist:
            obiettivo_principale = None

        # Sottraggo le calorie del vecchio Workout e aggiungo le calorie del nuovo Workout
        if obiettivo_principale:
            if obiettivo_principale.cal <= old_calories:
                obiettivo_principale.cal = 0
            else:
                obiettivo_principale.cal -= old_calories
            obiettivo_principale.cal += new_workout.calories_burned
            if obiettivo_principale.is_completed and obiettivo_principale.cal < obiettivo_principale.CaloriesGoal:
                obiettivo_principale.is_completed = False
            obiettivo_principale.save()

        new_workout.save()

        return super().form_valid(form)
