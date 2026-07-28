from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from settings_app.models import BusinessSetting

@login_required
def settings_detail(request):
    business = request.user.business
    setting, _ = BusinessSetting.objects.get_or_create(business=business)

    if request.method == 'POST':
        setting.currency_symbol = request.POST.get('currency_symbol', '$')
        setting.tax_number = request.POST.get('tax_number', '')
        setting.tax_rate = request.POST.get('tax_rate', 5.00)
        setting.receipt_header = request.POST.get('receipt_header', '')
        setting.receipt_footer = request.POST.get('receipt_footer', '')
        setting.low_stock_threshold = request.POST.get('low_stock_threshold', 5)
        setting.save()

        messages.success(request, "Business settings updated successfully.")
        return redirect('settings_detail')

    return render(request, 'settings_app/settings_detail.html', {'setting': setting})
