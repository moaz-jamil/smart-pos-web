from django.urls import path
from reports import views

urlpatterns = [
    path('', views.reports_overview, name='reports_overview'),
    path('export/sales/excel/', views.export_excel_sales, name='export_excel_sales'),
    path('export/sales/pdf/', views.export_pdf_sales, name='export_pdf_sales'),
    path('export/inventory/excel/', views.export_excel_inventory, name='export_excel_inventory'),
]
