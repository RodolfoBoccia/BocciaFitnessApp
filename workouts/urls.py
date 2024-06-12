from django.urls import path
from . import views

urlpatterns = [
    path("add_workout/", views.CreateWorkoutsView.as_view(), name='workouts'),
    path('', views.workout_list, name='workout_list'),
    path('workouts/<int:pk>/delete/', views.WorkoutsDeleteView.as_view(), name='delete'),
    path('workouts/<int:pk>/update/', views.WorkoutsUpdateView.as_view(), name='update'),
]




