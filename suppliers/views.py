from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from suppliers.models import Supplier
from suppliers.forms import SupplierForm

@login_required
def suppliers_list(request):
    business = request.user.business
    suppliers = Supplier.objects.filter(business=business) if business else Supplier.objects.all()

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            if business:
                s.business = business
            s.save()
            messages.success(request, f"Supplier '{s.company_name}' added.")
            return redirect('suppliers_list')
    else:
        form = SupplierForm()

    return render(request, 'suppliers/suppliers_list.html', {'suppliers': suppliers, 'form': form})


@login_required
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, f"Supplier '{supplier.company_name}' updated.")
            return redirect('suppliers_list')
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'suppliers/supplier_form.html', {'form': form, 'supplier': supplier})


@login_required
def supplier_history(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    purchases = supplier.purchases.all().order_by('-created_at')
    return render(request, 'suppliers/supplier_history.html', {'supplier': supplier, 'purchases': purchases})
