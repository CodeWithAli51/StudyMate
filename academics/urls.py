from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    path('', views.index, name='index'),
    path('subjects/<int:pk>/', views.subject_detail, name='subject_detail'),
    path('chapters/<int:pk>/', views.chapter_detail, name='chapter_detail'),
    path('topics/<int:pk>/', views.topic_detail, name='topic_detail'),
]
