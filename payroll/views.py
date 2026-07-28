from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from payroll.models import Payroll
from employees.models import EmployeeProfile

@login_required
def payroll_list(request):
    business = request.user.business
    payrolls = Payroll.objects.filter(business=business).order_by('-year', '-month') if business else Payroll.objects.all().order_by('-year', '-month')
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})


@login_required
def payroll_generate(request):
    business = request.user.business
    today = timezone.now().date()

    if request.method == 'POST':
        month = int(request.POST.get('month', today.month))
        year = int(request.POST.get('year', today.year))

        employees = EmployeeProfile.objects.filter(business=business) if business else EmployeeProfile.objects.all()
        created_count = 0

        for emp in employees:
            if not Payroll.objects.filter(business=business, employee=emp.user, month=month, year=year).exists():
                net = emp.salary
                Payroll.objects.create(
                    business=business,
                    employee=emp.user,
                    month=month,
                    year=year,
                    base_salary=emp.salary,
                    bonus=Decimal('0.00'),
                    deductions=Decimal('0.00'),
                    net_salary=net,
                    payment_status=Payroll.STATUS_PAID
                )
                created_count += 1

        messages.success(request, f"Generated {created_count} payroll slips for month {month}/{year}.")
        return redirect('payroll_list')

    return redirect('payroll_list')


@login_required
def payslip_detail(request, pk):
    payroll = get_object_or_404(Payroll, pk=pk)
    return render(request, 'payroll/payslip.html', {'payroll': payroll})
