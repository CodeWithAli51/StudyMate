from django.urls import path

from . import views

app_name = 'planner'

urlpatterns = [
    path('', views.PlannerIndexView.as_view(), name='index'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/new/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/<int:pk>/complete/', views.task_complete, name='task_complete'),
    path('tasks/<int:pk>/start/', views.task_start, name='task_start'),
    path('today/', views.today_plan, name='today'),
    path('sessions/', views.session_history, name='session_history'),
    path('sessions/<int:pk>/', views.session_detail, name='session_detail'),
    path('sessions/<int:pk>/finish/', views.session_finish, name='session_finish'),
    path('tasks/<int:task_pk>/start-session/', views.session_start, name='session_start'),
]
