from django.urls import path
from suppliers import views

urlpatterns = [
    path('', views.suppliers_list, name='suppliers_list'),
    path('<int:pk>/edit/', views.supplier_edit, name='supplier_edit'),
    path('<int:pk>/history/', views.supplier_history, name='supplier_history'),
]
