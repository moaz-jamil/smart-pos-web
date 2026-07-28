from django.urls import path
from customers import views

urlpatterns = [
    path('', views.customers_list, name='customers_list'),
    path('<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('<int:pk>/history/', views.customer_history, name='customer_history'),
]
