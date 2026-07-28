from django.urls import path
from pos import views

urlpatterns = [
    path('', views.pos_terminal_view, name='pos_terminal'),
    path('api/search/', views.pos_product_search_api, name='pos_search_api'),
    path('api/checkout/', views.pos_checkout_api, name='pos_checkout_api'),
]
