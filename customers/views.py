from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customers.models import Customer
from customers.forms import CustomerForm

@login_required
def customers_list(request):
    business = request.user.get_business()
    customers = Customer.objects.filter(business=business)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.business = business
            c.save()
            messages.success(request, f"Customer '{c.name}' added successfully.")
            return redirect('customers_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = CustomerForm()

    return render(request, 'customers/customers_list.html', {'customers': customers, 'form': form})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Customer '{customer.name}' updated.")
            return redirect('customers_list')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customers/customer_form.html', {'form': form, 'customer': customer})


@login_required
def customer_history(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    sales = customer.sales.all().order_by('-created_at')
    return render(request, 'customers/customer_history.html', {'customer': customer, 'sales': sales})
