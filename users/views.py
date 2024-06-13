from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.shortcuts import render, redirect
from goals.models import GoalModel


@login_required
def profile_view(request):
    goals_completed = GoalModel.objects.filter(utente=request.user, is_completed=True)
    return render(request, 'profile.html', {'goals_completed': goals_completed, 'user': request.user})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('users:login')


@login_required
def profile_update_view(request):
    form = ProfileUpdateForm(instance=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect('users:profile')

    return render(request, 'profile_update.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = 'templates/home.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'


class HomePageView(TemplateView):
    template_name = 'home.html'
