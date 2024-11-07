from django.shortcuts import render
from .models import Notification

def notifications(request, type, pk):
    notification = Notification.objects.filter(user=request.user)
    unread = notification.filter(status="UN")
    read = notification.filter(status="RD")
    context = {
        'menu': 'notification',
        'unread': unread,
        'read': read,
    }
    return render(request, 'notify/notifications.html', context)
