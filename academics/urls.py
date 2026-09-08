from django.urls import path

from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.AcademicsIndexView.as_view(), name='index'),
]
