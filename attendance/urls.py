from django.urls import path
from attendance import views

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('clock/', views.clock_in_out, name='clock_in_out'),
]
