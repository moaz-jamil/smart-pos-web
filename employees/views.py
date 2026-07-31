from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employees.models import EmployeeProfile
from authentication.models import User

@login_required
def employees_list(request):
    business = request.user.get_business()
    employees = EmployeeProfile.objects.filter(business=business)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        designation = request.POST.get('designation', 'Cashier')
        salary = request.POST.get('salary', 3000)

        if username and password:
            usr = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=User.ROLE_EMPLOYEE,
                business=business,
                branch=request.user.branch
            )
            EmployeeProfile.objects.create(
                business=business,
                user=usr,
                designation=designation,
                salary=salary
            )
            messages.success(request, f"Employee user '{username}' created.")
            return redirect('employees_list')

    return render(request, 'employees/employees_list.html', {'employees': employees})
