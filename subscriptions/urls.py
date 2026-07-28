from django.urls import path
from subscriptions import views

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
]
