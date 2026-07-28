from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from subscriptions.models import SubscriptionPlan, BusinessSubscription

@login_required
def subscriptions_list(request):
    plans = SubscriptionPlan.objects.all()
    active_sub = BusinessSubscription.objects.filter(business=request.user.business, status=True).first() if request.user.business else None
    return render(request, 'subscriptions/subscriptions_list.html', {'plans': plans, 'active_sub': active_sub})
