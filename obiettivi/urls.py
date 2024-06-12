
from django.urls import path
from . import views


urlpatterns = [
    path('lista/', views.listaobiettivi, name='listaobiettivi'),
    path('create_goal/', views.CreateGoalView.as_view(), name='create_goal'),
    path('<int:pk>/delete/', views.delete_goal, name='delete_goal'),
    path('<int:pk>/edit/', views.UpdateGoalView.as_view(), name='edit'),
    path('update_goal_selection/', views.update_goal_selection, name='update_goal_selection'),
]
