from django.urls import path
from sales import views

urlpatterns = [
    path('', views.sales_list, name='sales_list'),
    path('<int:pk>/', views.sale_detail, name='sale_detail'),
    path('<int:pk>/refund/', views.sale_refund, name='sale_refund'),
    path('coupons/', views.coupons_list, name='coupons_list'),
]
