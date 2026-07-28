import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from products.models import Product
from sales.models import SaleItem

@login_required
def ai_forecast_view(request):
    business = request.user.business
    products = Product.objects.filter(business=business) if business else Product.objects.all()

    forecast_data = []

    for p in products:
        # Calculate sales over past 14 days
        two_weeks_ago = datetime.date.today() - datetime.timedelta(days=14)
        sold_qty = SaleItem.objects.filter(product=p, sale__created_at__date__gte=two_weeks_ago).aggregate(total=Sum('quantity'))['total'] or 0

        avg_daily_sales = sold_qty / 14.0 if sold_qty > 0 else 0.1

        # Days remaining calculation
        days_remaining = int(p.stock_quantity / avg_daily_sales) if avg_daily_sales > 0 else 999
        suggested_reorder = max(0, (p.min_stock_level * 3) - p.stock_quantity)

        forecast_data.append({
            'product': p,
            'sold_14_days': sold_qty,
            'avg_daily_sales': round(avg_daily_sales, 2),
            'days_remaining': days_remaining,
            'suggested_reorder': suggested_reorder,
            'risk_level': 'HIGH' if days_remaining <= 5 or p.is_low_stock else ('MEDIUM' if days_remaining <= 14 else 'LOW'),
        })

    forecast_data = sorted(forecast_data, key=lambda x: x['days_remaining'])

    return render(request, 'ai/forecast.html', {'forecasts': forecast_data})
