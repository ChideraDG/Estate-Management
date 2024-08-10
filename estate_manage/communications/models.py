from django.db import models
from django.contrib.auth.models import User
from apartments.models import Apartment
from tenants.models import Tenant

class Message(models.Model):
    """This model represents individual messages sent between tenants and property management."""

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} - {self.subject}"


class Announcement(models.Model):
    """This model represents announcements sent to tenants or specific groups."""

    title = models.CharField(max_length=200)
    body = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Announcement: {self.title} - {self.send_date}"


class Feedback(models.Model):
    """This model collects feedback from tenants regarding services and property conditions."""

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 10)])
    comments = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback by {self.tenant} - Rating: {self.rating}"


class Survey(models.Model):
    """This model represents surveys sent to tenants to gather more structured feedback."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Survey: {self.title} - {self.created_date}"


class SurveyResponse(models.Model):
    """This model stores the responses to surveys from tenants."""

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='survey_responses')
    response_data = models.JSONField()
    submitted_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Survey Response by {self.tenant} to {self.survey}"
