from django.urls import path

from . import views

app_name = 'revision'

urlpatterns = [
    path('', views.RevisionIndexView.as_view(), name='index'),
]
