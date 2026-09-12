from django.urls import path
from . import views

# app_name = 'task'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('history/', views.task_list, name='history'),
    path('<slug:slug>/', views.task_detail, name='task_detail'),
    # path('<slug:slug>/', views.task_list, name='task_detail'),
    
]
