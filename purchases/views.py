from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone

from purchases.models import Purchase, PurchaseItem
from suppliers.models import Supplier
from products.models import Product
from inventory.models import StockMovement

@login_required
def purchases_list(request):
    business = request.user.business
    purchases = Purchase.objects.filter(business=business).order_by('-created_at') if business else Purchase.objects.all().order_by('-created_at')
    return render(request, 'purchases/purchases_list.html', {'purchases': purchases})


@login_required
@transaction.atomic
def purchase_create(request):
    business = request.user.business
    suppliers = Supplier.objects.filter(business=business) if business else Supplier.objects.all()
    products = Product.objects.filter(business=business) if business else Product.objects.all()

    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))
        unit_cost = Decimal(request.POST.get('unit_cost', '0.00'))
        payment_status = request.POST.get('payment_status', 'PAID')

        supplier = get_object_or_404(Supplier, pk=supplier_id)
        product = get_object_or_404(Product, pk=product_id)

        total_cost = unit_cost * quantity
        inv_no = f"PO-{timezone.now().strftime('%Y%m%d%H%M%S')}"

        po = Purchase.objects.create(
            business=business,
            branch=request.user.branch,
            supplier=supplier,
            invoice_number=inv_no,
            total_amount=total_cost,
            paid_amount=total_cost if payment_status == 'PAID' else Decimal('0.00'),
            payment_status=payment_status,
            received_status=Purchase.RECEIVED_STATUS_RECEIVED,
            created_by=request.user
        )

        PurchaseItem.objects.create(
            purchase=po,
            product=product,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost
        )

        # Ingestion into product inventory
        product.stock_quantity += quantity
        product.purchase_price = unit_cost
        product.save()

        StockMovement.objects.create(
            business=business,
            branch=request.user.branch,
            product=product,
            movement_type=StockMovement.TYPE_IN,
            quantity=quantity,
            reference_number=inv_no,
            created_by=request.user,
            notes=f"Received PO #{inv_no} from {supplier.company_name}"
        )

        if payment_status != 'PAID':
            supplier.outstanding_balance += total_cost
            supplier.save()

        messages.success(request, f"Purchase Order #{inv_no} created and {quantity} units added to '{product.name}'.")
        return redirect('purchases_list')

    return render(request, 'purchases/purchase_form.html', {'suppliers': suppliers, 'products': products})
