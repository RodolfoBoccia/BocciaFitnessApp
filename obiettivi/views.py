from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import GoalForm
from .models import GoalModel
from django.shortcuts import redirect


@login_required
def delete_goal(request, pk):
    goal = GoalModel.objects.get(pk=pk)

    if goal.is_selected:
        goal.is_selected = False
        goal.save()

    goal.delete()

    return redirect('listaobiettivi')


@login_required
def update_goal_selection(request):
    if request.method == 'POST':
        selected_goal_id = request.POST.get('selected_goal')
        if selected_goal_id:
            GoalModel.objects.all().update(is_selected=False)
            goal = GoalModel.objects.get(pk=selected_goal_id)
            if goal.is_selected:
                goal.is_selected = False
            else:
                goal.is_selected = True

            goal.save()

    return redirect('homeview')


class CreateGoalView(LoginRequiredMixin, CreateView):
    template_name = 'create_goal.html'
    form_class = GoalForm
    success_url = reverse_lazy('listaobiettivi')

    def form_valid(self, form):
        form.instance.utente = self.request.user
        form.instance.data_creazione = datetime.now()
        form.instance.deadline = form.instance.data_creazione + timedelta(days=form.instance.tempistica)
        form.save()
        return super().form_valid(form)


@login_required
def listaobiettivi(request):
    goals = GoalModel.objects.filter(utente=request.user)
    if request.method == 'POST':
        selected_goal_pk = request.POST.get('selected_goal')
        if selected_goal_pk:
            selected_goal = GoalModel.objects.get(pk=selected_goal_pk)
            GoalModel.objects.filter(utente=request.user).exclude(pk=selected_goal_pk).update(is_selected=False)
            selected_goal.is_selected = True
            selected_goal.save()

            return redirect('listaobiettivi')
    return render(request, 'goals.html', {'goals': goals})


class UpdateGoalView(LoginRequiredMixin, UpdateView):
    model = GoalModel
    fields = ('goal_type', 'descrizione', 'tempistica', 'CaloriesGoal')
    template_name = 'update_goal.html'
    success_url = reverse_lazy('listaobiettivi')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        return obj

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        goal = self.object
        return context
