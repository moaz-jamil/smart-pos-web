from django.urls import path
from branches import views

urlpatterns = [
    path('', views.branches_list, name='branches_list'),
]
