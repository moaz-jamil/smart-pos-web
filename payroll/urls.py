from django.urls import path
from payroll import views

urlpatterns = [
    path('', views.payroll_list, name='payroll_list'),
    path('generate/', views.payroll_generate, name='payroll_generate'),
    path('<int:pk>/payslip/', views.payslip_detail, name='payslip_detail'),
]
