from django.urls import path
from settings_app import views

urlpatterns = [
    path('', views.settings_detail, name='settings_detail'),
]
