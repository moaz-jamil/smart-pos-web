from django.urls import path
from ai import views

urlpatterns = [
    path('', views.ai_forecast_view, name='ai_forecast'),
]
