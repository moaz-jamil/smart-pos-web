from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction

from inventory.models import StockMovement, Warehouse
from products.models import Product

@login_required
def inventory_list(request):
    business = request.user.business
    movements = StockMovement.objects.filter(business=business).order_by('-created_at') if business else StockMovement.objects.all().order_by('-created_at')
    return render(request, 'inventory/inventory_list.html', {'movements': movements})


@login_required
@transaction.atomic
def stock_movement_create(request):
    business = request.user.business
    products = Product.objects.filter(business=business) if business else Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product')
        movement_type = request.POST.get('movement_type')
        quantity = int(request.POST.get('quantity', 0))
        ref_no = request.POST.get('reference_number', '')
        notes = request.POST.get('notes', '')

        product = get_object_or_404(Product, pk=product_id)

        if movement_type in [StockMovement.TYPE_IN, StockMovement.TYPE_ADJUSTMENT]:
            product.stock_quantity += quantity
        elif movement_type == StockMovement.TYPE_OUT:
            if product.stock_quantity < quantity:
                messages.error(request, f"Cannot stock out {quantity} units. Current stock is {product.stock_quantity}.")
                return redirect('stock_movement_create')
            product.stock_quantity -= quantity

        product.save()

        StockMovement.objects.create(
            business=business,
            branch=request.user.branch,
            product=product,
            movement_type=movement_type,
            quantity=quantity,
            reference_number=ref_no,
            notes=notes,
            created_by=request.user
        )

        messages.success(request, f"Stock movement recorded for '{product.name}'. New Stock: {product.stock_quantity}")
        return redirect('inventory_list')

    return render(request, 'inventory/stock_movement_form.html', {'products': products})


@login_required
def warehouses_list(request):
    business = request.user.business
    warehouses = Warehouse.objects.filter(business=business) if business else Warehouse.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        if name:
            Warehouse.objects.create(business=business, branch=request.user.branch, name=name, location=location)
            messages.success(request, f"Warehouse '{name}' created.")
            return redirect('warehouses_list')

    return render(request, 'inventory/warehouses.html', {'warehouses': warehouses})
