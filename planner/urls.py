from django.urls import path

from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.PlannerIndexView.as_view(), name='index'),
]
