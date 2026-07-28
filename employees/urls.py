from django.urls import path
from employees import views

urlpatterns = [
    path('', views.employees_list, name='employees_list'),
]
