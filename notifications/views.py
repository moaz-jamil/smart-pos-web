from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from notifications.models import Notification

@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})


@login_required
def mark_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk, user=request.user)
    notif.is_read = True
    notif.save()
    return redirect('notifications_list')
