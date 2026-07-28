from django.urls import path
from authentication import views

urlpatterns = [
    path('', views.root_redirect, name='root_redirect'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_business_view, name='register_business'),
    path('profile/', views.user_profile_view, name='user_profile'),
]
