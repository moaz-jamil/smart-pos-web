from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from sales.models import Sale, SaleItem, Coupon
from inventory.models import StockMovement

@login_required
def sales_list(request):
    business = request.user.business
    sales = Sale.objects.filter(business=business).order_by('-created_at') if business else Sale.objects.all().order_by('-created_at')
    return render(request, 'sales/sales_list.html', {'sales': sales})


@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})


@login_required
@transaction.atomic
def sale_refund(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if sale.payment_status == Sale.STATUS_REFUNDED:
        messages.warning(request, "This sale has already been refunded.")
        return redirect('sale_detail', pk=sale.pk)

    if request.method == 'POST':
        sale.payment_status = Sale.STATUS_REFUNDED
        sale.save()

        # Restore product stock
        for item in sale.items.all():
            product = item.product
            product.stock_quantity += item.quantity
            product.save()

            StockMovement.objects.create(
                business=sale.business,
                branch=sale.branch,
                product=product,
                movement_type=StockMovement.TYPE_IN,
                quantity=item.quantity,
                reference_number=f"REFUND-{sale.invoice_number}",
                created_by=request.user,
                notes=f"Stock restored from refunded Sale #{sale.invoice_number}"
            )

        messages.success(request, f"Sale #{sale.invoice_number} successfully refunded and stock restored.")
        return redirect('sales_list')

    return render(request, 'sales/sale_refund_confirm.html', {'sale': sale})


@login_required
def coupons_list(request):
    business = request.user.business
    coupons = Coupon.objects.filter(business=business) if business else Coupon.objects.all()

    if request.method == 'POST':
        code = request.POST.get('code', '').upper()
        discount = request.POST.get('discount_percentage')
        min_purchase = request.POST.get('min_purchase')
        valid_until = request.POST.get('valid_until')

        if code and discount and valid_until:
            Coupon.objects.create(
                business=business,
                code=code,
                discount_percentage=discount,
                min_purchase=min_purchase or 0,
                valid_until=valid_until
            )
            messages.success(request, f"Coupon '{code}' created.")
            return redirect('coupons_list')

    return render(request, 'sales/coupons.html', {'coupons': coupons})
