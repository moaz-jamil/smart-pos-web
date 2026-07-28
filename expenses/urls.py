from django.urls import path
from expenses import views

urlpatterns = [
    path('', views.expenses_list, name='expenses_list'),
    path('categories/', views.expense_categories, name='expense_categories'),
]
