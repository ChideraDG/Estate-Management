from django.shortcuts import render
from django.db.models import Q
from .models import Message, Conversation


def bo_tenant_communications(request, pk):
    all_messages = Message.objects.filter(Q(sender=request.user) |
                                  Q(recipient=request.user))
    unread_messages = all_messages.filter(is_read=False)
    read_messages = all_messages.filter(is_read=True)
    conversations = Conversation.objects.filter(user=request.user).order_by('-latest_message_timestamp')

    context = {
        "menu": 'tm',
        "s_menu": 'ct',
        "all_messages": all_messages,
        "unread_messages": unread_messages,
        "read_messages": read_messages,
        "conversations": conversations,
    }
    return render(request, 'communications/bo_comms.html', context)