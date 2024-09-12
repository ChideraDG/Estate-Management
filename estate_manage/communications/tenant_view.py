import datetime
from django.shortcuts import render, redirect
from django.db.models import Q
from users.models import Profile
from .models import Message


def tenant_communications(request, pk):
    menu = 'comms'
    profile = request.user.profile.tenant

    messages = None
    if profile.building_owner:
        building_owner = profile.building_owner
        messages_queryset = Message.objects.filter(
            Q(sender=request.user, recipient=building_owner.user.user) |
            Q(sender=building_owner.user.user, recipient=request.user)
        )
        
        if messages_queryset.exists():
            # Get the latest message
            latest_message = messages_queryset.last()
            
            # Prepare the message data
            message_data = {
                'id': building_owner.id,
                'profile_picture': building_owner.profile_pics,
                'name': f"{building_owner.building_owner_name}",
                'latest_message': latest_message.message,
                'unread': messages_queryset.filter(recipient=request.user, is_read=False).count(),
                'read': latest_message.is_read,
                'timestamp': latest_message.timestamp,
            }
        messages = message_data
    else:
        building_owner = None
    
    Profile.objects.filter(username=request.user).update(unread_messages=tenant_get_unread(request))
    context = {
        'menu': menu,
        "message": messages,
        "building_owner": building_owner
    }
    return render(request, "communications/tenant_comms.html", context)

def tenant_chat(request, pk, bo_id):
    menu = 'comms'
    profile = request.user.profile.tenant

    if profile.building_owner:
        building_owner = profile.building_owner
        messages = Message.objects.filter(
            Q(sender=request.user, recipient=building_owner.user.user) |
            Q(sender=building_owner.user.user, recipient=request.user)
        )
    else:
        building_owner = None
    
    # Group messages by date
    messages_by_date = {}
    for message in messages:
        message_date = message.timestamp.date()
        if message_date not in messages_by_date:
            messages_by_date[message_date] = []
        messages_by_date[message_date].append(message)
        
    if messages:
        if messages.last().recipient == request.user:
            read = messages.filter(is_read=False)
            read.update(is_read=True)
            
    Profile.objects.filter(username=request.user).update(unread_messages=tenant_get_unread(request))
    if request.method == "POST":
        message_content = request.POST.get("message", "").strip()

        if message_content:  # Ensure message isn't empty
            Message.objects.create(
                sender=request.user,
                recipient=building_owner.user.user,
                message=message_content
            )

            return redirect("tenant-chat", pk=request.user.profile, bo_id=bo_id)
    
    context = {
        'menu': menu,
        "building_owner": building_owner,
        'messages_by_date': messages_by_date,
        'today_date': datetime.date.today(),
    }
    return render(request, "communications/tenant_chat.html", context)

def tenant_get_unread(request):
    profile = request.user.profile.tenant
    if profile.building_owner:
        building_owner = profile.building_owner

    # Prepare a list to hold the unread counts
    unread_total = []

    # Query for unread messages sent to the current user from each tenant
    unread_count = Message.objects.filter(
        sender=building_owner.user.user, 
        recipient=request.user, 
        is_read=False
    ).count()

    if unread_count > 0:
        unread_total.append(unread_count)

    return len(unread_total)