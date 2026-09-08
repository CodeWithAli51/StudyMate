from django.urls import path

from . import views

app_name = 'practice'

urlpatterns = [
    path('', views.PracticeIndexView.as_view(), name='index'),
]
