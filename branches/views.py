from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from branches.models import Branch

@login_required
def branches_list(request):
    business = request.user.business
    branches = Branch.objects.filter(business=business) if business else Branch.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        code = request.POST.get('code')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if name:
            Branch.objects.create(business=business, name=name, code=code, phone=phone, address=address)
            messages.success(request, f"Branch '{name}' created.")
            return redirect('branches_list')

    return render(request, 'branches/branches_list.html', {'branches': branches})
