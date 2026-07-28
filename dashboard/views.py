import datetime
from decimal import Decimal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.utils import timezone

from sales.models import Sale, SaleItem
from purchases.models import Purchase
from expenses.models import Expense
from products.models import Product
from customers.models import Customer
from suppliers.models import Supplier
from employees.models import EmployeeProfile

@login_required
def dashboard_view(request):
    user = request.user
    business = getattr(user, 'business', None)

    today = timezone.now().date()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Base Querysets
    sales_qs = Sale.objects.filter(business=business) if business else Sale.objects.all()
    purchases_qs = Purchase.objects.filter(business=business) if business else Purchase.objects.all()
    expenses_qs = Expense.objects.filter(business=business) if business else Expense.objects.all()
    products_qs = Product.objects.filter(business=business) if business else Product.objects.all()
    customers_qs = Customer.objects.filter(business=business) if business else Customer.objects.all()
    suppliers_qs = Supplier.objects.filter(business=business) if business else Supplier.objects.all()

    # Cards Calculations
    todays_sales_val = sales_qs.filter(created_at__date=today).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    todays_orders_cnt = sales_qs.filter(created_at__date=today).count()
    todays_expenses_val = expenses_qs.filter(expense_date=today).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    # Profit Calculation Today: (Today's Sales Items Total Revenue) - (Today's Sales Items Total Purchase Cost)
    today_items = SaleItem.objects.filter(sale__in=sales_qs.filter(created_at__date=today))
    today_cogs = sum(item.quantity * item.product.purchase_price for item in today_items)
    todays_profit_val = todays_sales_val - Decimal(str(today_cogs)) - todays_expenses_val

    total_products_cnt = products_qs.count()
    low_stock_cnt = products_qs.filter(stock_quantity__lte=F('min_stock_level')).count()
    total_customers_cnt = customers_qs.count()
    total_suppliers_cnt = suppliers_qs.count()
    total_employees_cnt = EmployeeProfile.objects.filter(business=business).count() if business else 0

    # Recent Data
    recent_orders = sales_qs.order_by('-created_at')[:8]
    recent_purchases = purchases_qs.order_by('-created_at')[:5]
    low_stock_products = products_qs.filter(stock_quantity__lte=F('min_stock_level'))[:6]

    # Chart 1: Last 7 Days Sales Trend
    chart_dates = []
    chart_sales_data = []
    for i in range(6, -1, -1):
        day_date = today - datetime.timedelta(days=i)
        chart_dates.append(day_date.strftime('%b %d'))
        day_total = sales_qs.filter(created_at__date=day_date).aggregate(total=Sum('total_amount'))['total'] or 0
        chart_sales_data.append(float(day_total))

    # Chart 2: Top 5 Best Selling Products
    top_products_qs = SaleItem.objects.filter(sale__in=sales_qs)\
        .values('product__name')\
        .annotate(total_sold=Sum('quantity'))\
        .order_by('-total_sold')[:5]

    top_prod_labels = [p['product__name'] for p in top_products_qs]
    top_prod_data = [p['total_sold'] for p in top_products_qs]

    context = {
        'todays_sales': todays_sales_val,
        'todays_orders': todays_orders_cnt,
        'todays_profit': todays_profit_val,
        'todays_expenses': todays_expenses_val,
        'total_products': total_products_cnt,
        'low_stock_count': low_stock_cnt,
        'total_customers': total_customers_cnt,
        'total_suppliers': total_suppliers_cnt,
        'total_employees': total_employees_cnt,
        'recent_orders': recent_orders,
        'recent_purchases': recent_purchases,
        'low_stock_products': low_stock_products,
        'chart_dates': chart_dates,
        'chart_sales_data': chart_sales_data,
        'top_prod_labels': top_prod_labels,
        'top_prod_data': top_prod_data,
    }

    return render(request, 'dashboard/index.html', context)
