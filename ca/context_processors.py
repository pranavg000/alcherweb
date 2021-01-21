from ca.models import Notifications
from django.contrib.auth.models import User

def message_processor(request):
    if request.user.is_authenticated:
        notifications = Notifications.objects.filter(notification_receiver = request.user)
        sendToAll = User.objects.get(username="sendToAll")
        notifications |= Notifications.objects.filter(notification_receiver = sendToAll)
        notifications = notifications.order_by('-notification_timestamp')[:4]
    else:
        notifications = None
    return {
        'notifications' : notifications
    }