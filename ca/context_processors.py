from ca.models import Notifications

def message_processor(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(notification_receiver = request.user)[:4]
    else:
        notifications = None
    return {
        'notifications' : notifications
    }