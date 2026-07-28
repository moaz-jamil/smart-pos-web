from django.urls import path
from purchases import views

urlpatterns = [
    path('', views.purchases_list, name='purchases_list'),
    path('create/', views.purchase_create, name='purchase_create'),
]
