from django.urls import path
from products import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.categories_list, name='categories_list'),
    path('brands/', views.brands_list, name='brands_list'),
]
