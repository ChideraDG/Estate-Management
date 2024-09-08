from django.db import models
from django.contrib.auth.models import User
from apartments.models import Apartment
from tenants.models import Tenant

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    latest_message = models.TextField(blank=True, null=True)
    latest_message_timestamp = models.DateTimeField(null=True, blank=True)
    unread_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Conversation with {self.client.username}"
    
class Message(models.Model):
    """
    Represents individual messages sent between tenants and property management.

    Attributes
    ----------
    sender : User
        The user who sent the message.
    recipient : User
        The user who received the message.
    subject : str, optional
        The subject of the message (nullable).
    body : str
        The content of the message.
    timestamp : datetime
        The date and time when the message was sent (auto-generated).
    is_read : bool
        Indicates whether the message has been read, default is False.
    """
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', null=True, blank=True)
    
    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} - {self.subject}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the conversation with the latest message details
        self.conversation.user = self.sender
        self.conversation.latest_message = self.message
        self.conversation.latest_message_timestamp = self.timestamp
        self.conversation.unread_count += 1
        self.conversation.save()

class Announcement(models.Model):
    """
    Represents announcements sent to tenants or specific groups.

    Attributes
    ----------
    title : str
        The title of the announcement.
    body : str
        The content of the announcement.
    send_date : datetime
        The date and time when the announcement was sent (auto-generated).
    is_active : bool
        Indicates whether the announcement is currently active, default is True.
    """
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Announcement: {self.title} - {self.send_date}"


class Feedback(models.Model):
    """
    Collects feedback from tenants regarding services and property conditions.

    Attributes
    ----------
    tenant : User
        The tenant providing the feedback.
    apartment : Apartment
        The apartment associated with the feedback.
    rating : int
        The rating provided by the tenant (1-9).
    comments : str, optional
        Additional comments provided by the tenant (nullable).
    timestamp : datetime
        The date and time when the feedback was submitted (auto-generated).
    """
    
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 10)])
    comments = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback by {self.tenant} - Rating: {self.rating}"


class Survey(models.Model):
    """
    Represents surveys sent to tenants to gather more structured feedback.

    Attributes
    ----------
    title : str
        The title of the survey.
    description : str
        A detailed description of the survey.
    created_date : datetime
        The date and time when the survey was created (auto-generated).
    is_active : bool
        Indicates whether the survey is currently active, default is True.
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Survey: {self.title} - {self.created_date}"


class SurveyResponse(models.Model):
    """
    Stores the responses to surveys from tenants.

    Attributes
    ----------
    survey : Survey
        The survey to which the response belongs.
    tenant : Tenant
        The tenant who submitted the response.
    response_data : dict
        The responses provided by the tenant, stored as JSON.
    submitted_date : datetime
        The date and time when the response was submitted (auto-generated).
    """
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='survey_responses')
    response_data = models.JSONField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Survey Response by {self.tenant} to {self.survey}"
