from django.urls import path
from inventory import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('movement/create/', views.stock_movement_create, name='stock_movement_create'),
    path('warehouses/', views.warehouses_list, name='warehouses_list'),
]
