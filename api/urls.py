from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'sales', views.SaleViewSet)
router.register(r'expenses', views.ExpenseViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
