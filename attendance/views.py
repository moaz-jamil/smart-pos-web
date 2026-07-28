import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from attendance.models import Attendance

@login_required
def attendance_list(request):
    business = request.user.business
    attendances = Attendance.objects.filter(business=business).order_by('-date') if business else Attendance.objects.all().order_by('-date')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})


@login_required
def clock_in_out(request):
    user = request.user
    today = timezone.now().date()
    now_time = timezone.now().time()

    att, created = Attendance.objects.get_or_create(
        business=user.business,
        employee=user,
        date=today,
        defaults={'clock_in': now_time, 'branch': user.branch}
    )

    if not created and not att.clock_out:
        att.clock_out = now_time
        # Compute working hours
        c_in = datetime.datetime.combine(today, att.clock_in)
        c_out = datetime.datetime.combine(today, now_time)
        hrs = (c_out - c_in).total_seconds() / 3600.0
        att.working_hours = Decimal(f"{hrs:.2f}")
        att.save()
        messages.success(request, f"Clocked Out at {now_time.strftime('%H:%M:%S')}. Working Hours: {att.working_hours} hrs")
    elif created:
        messages.success(request, f"Clocked In at {now_time.strftime('%H:%M:%S')}.")
    else:
        messages.info(request, "You have already completed attendance for today.")

    return redirect('attendance_list')
