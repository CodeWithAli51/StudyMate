from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/setup/', views.profile_setup, name='profile_setup'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('profile/subjects/', views.subject_select, name='subject_select'),
]
