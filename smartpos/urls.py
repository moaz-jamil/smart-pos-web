from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('products/', include('products.urls')),
    path('inventory/', include('inventory.urls')),
    path('customers/', include('customers.urls')),
    path('suppliers/', include('suppliers.urls')),
    path('purchases/', include('purchases.urls')),
    path('sales/', include('sales.urls')),
    path('pos/', include('pos.urls')),
    path('employees/', include('employees.urls')),
    path('attendance/', include('attendance.urls')),
    path('payroll/', include('payroll.urls')),
    path('reports/', include('reports.urls')),
    path('expenses/', include('expenses.urls')),
    path('settings/', include('settings_app.urls')),
    path('notifications/', include('notifications.urls')),
    path('branches/', include('branches.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('ai/', include('ai.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
