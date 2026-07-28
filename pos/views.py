import json
from decimal import Decimal
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone

from products.models import Product, Category
from customers.models import Customer
from sales.models import Sale, SaleItem, Coupon
from inventory.models import StockMovement
from settings_app.models import BusinessSetting

@login_required
def pos_terminal_view(request):
    business = request.user.business
    products = Product.objects.filter(business=business, status=True) if business else Product.objects.filter(status=True)
    categories = Category.objects.filter(business=business, status=True) if business else Category.objects.filter(status=True)
    customers = Customer.objects.filter(business=business, status=True) if business else Customer.objects.filter(status=True)
    setting = getattr(business, 'settings', None) if business else None

    context = {
        'products': products,
        'categories': categories,
        'customers': customers,
        'tax_rate': setting.tax_rate if setting else Decimal('5.00'),
    }
    return render(request, 'pos/terminal.html', context)


@login_required
def pos_product_search_api(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category_id')

    business = request.user.business
    products = Product.objects.filter(business=business, status=True) if business else Product.objects.filter(status=True)

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(barcode__icontains=query) | products.filter(name__icontains=query) | products.filter(sku__icontains=query)

    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'barcode': p.barcode,
            'sku': p.sku,
            'price': float(p.selling_price),
            'stock': p.stock_quantity,
            'tax_rate': float(p.tax_rate),
            'discount_rate': float(p.discount_rate),
            'image_url': p.image.url if p.image else '',
        })
    return JsonResponse({'status': 'success', 'products': data})


@login_required
@csrf_exempt
@transaction.atomic
def pos_checkout_api(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        customer_id = data.get('customer_id')
        payment_method = data.get('payment_method', 'CASH')
        paid_amount = Decimal(str(data.get('paid_amount', 0)))
        discount_amount = Decimal(str(data.get('discount_amount', 0)))
        coupon_code = data.get('coupon_code', '').strip()

        if not items:
            return JsonResponse({'status': 'error', 'message': 'Cart is empty'}, status=400)

        business = request.user.business
        customer = Customer.objects.filter(pk=customer_id).first() if customer_id else None
        coupon = Coupon.objects.filter(business=business, code=coupon_code, status=True).first() if coupon_code else None

        # Calculate totals & validate stock
        subtotal = Decimal('0.00')
        tax_total = Decimal('0.00')
        sale_items_data = []

        for item in items:
            product = Product.objects.select_for_update().get(pk=item['id'])
            qty = int(item['quantity'])

            if product.stock_quantity < qty:
                return JsonResponse({'status': 'error', 'message': f'Insufficient stock for {product.name}. Available: {product.stock_quantity}'}, status=400)

            item_price = product.selling_price
            item_subtotal = item_price * qty
            item_tax = (item_subtotal * product.tax_rate) / Decimal('100')

            subtotal += item_subtotal
            tax_total += item_tax

            # Deduct Product Stock
            product.stock_quantity -= qty
            product.save()

            # Record Stock Out Movement
            StockMovement.objects.create(
                business=business,
                branch=request.user.branch,
                product=product,
                movement_type=StockMovement.TYPE_OUT,
                quantity=qty,
                reference_number=f"POS-SALE-{timezone.now().strftime('%Y%m%d%H%M%S')}",
                created_by=request.user,
                notes="POS Checkout Sale"
            )

            sale_items_data.append({
                'product': product,
                'quantity': qty,
                'unit_price': item_price,
                'subtotal': item_subtotal,
                'tax_rate': product.tax_rate,
            })

        total_amount = subtotal + tax_total - discount_amount
        change_amount = paid_amount - total_amount if paid_amount > total_amount else Decimal('0.00')

        # Create Invoice Number
        inv_count = Sale.objects.filter(business=business).count() + 1
        invoice_number = f"INV-{timezone.now().strftime('%Y%m')}-{inv_count:04d}"

        # Create Sale
        sale = Sale.objects.create(
            business=business,
            branch=request.user.branch,
            customer=customer,
            cashier=request.user,
            coupon=coupon,
            invoice_number=invoice_number,
            total_amount=total_amount,
            tax_amount=tax_total,
            discount_amount=discount_amount,
            paid_amount=paid_amount,
            change_amount=change_amount,
            payment_method=payment_method,
            payment_status=Sale.STATUS_PAID if paid_amount >= total_amount else Sale.STATUS_PARTIAL,
        )

        # Create Sale Items
        items_payload = []
        for item_info in sale_items_data:
            si = SaleItem.objects.create(
                sale=sale,
                product=item_info['product'],
                quantity=item_info['quantity'],
                unit_price=item_info['unit_price'],
                tax_rate=item_info['tax_rate'],
                subtotal=item_info['subtotal']
            )
            items_payload.append({
                'name': item_info['product'].name,
                'qty': item_info['quantity'],
                'price': float(item_info['unit_price']),
                'subtotal': float(item_info['subtotal']),
            })

        # Add reward points if customer exists
        if customer:
            points_earned = int(total_amount / 10)
            customer.reward_points += points_earned
            customer.save()

        return JsonResponse({
            'status': 'success',
            'invoice_number': invoice_number,
            'date': sale.created_at.strftime('%Y-%m-%d %H:%M'),
            'cashier': request.user.username,
            'customer_name': customer.name if customer else 'Walk-in Customer',
            'subtotal': float(subtotal),
            'tax': float(tax_total),
            'discount': float(discount_amount),
            'total': float(total_amount),
            'paid': float(paid_amount),
            'change': float(change_amount),
            'items': items_payload
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
