from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, profile_view, profile_update_view

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('updateprofile/', profile_update_view, name='updateprofile'),
]
