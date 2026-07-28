from settings_app.models import BusinessSetting
from branches.models import Branch
from notifications.models import Notification

def business_context(request):
    if not request.user.is_authenticated:
        return {
            'currency_symbol': '$',
            'business_name': 'SmartPOS',
            'unread_notifications_count': 0,
        }

    user = request.user
    business = getattr(user, 'business', None)
    
    setting = None
    if business:
        setting = getattr(business, 'settings', None)
        if not setting:
            setting, _ = BusinessSetting.objects.get_or_create(business=business)

    branches = Branch.objects.filter(business=business) if business else []
    notifications = Notification.objects.filter(user=user, is_read=False).order_by('-created_at')[:5] if user.is_authenticated else []
    
    return {
        'current_business': business,
        'business_setting': setting,
        'currency_symbol': setting.currency_symbol if setting else '$',
        'business_branches': branches,
        'header_notifications': notifications,
        'unread_notifications_count': Notification.objects.filter(user=user, is_read=False).count() if user.is_authenticated else 0,
    }
