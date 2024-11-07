from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notification(models.Model):
    """
    A model to represent notifications within the estate management app.
    Notifications can be of different types (e.g., lease renewals, payment reminders) and can have different statuses
    (e.g., unread, read, archived). Each notification is linked to a specific user and can optionally include a link
    for additional details.
    """
    
    # Notification Types
    LEASE_RENEWAL = 'LR'
    PAYMENT_REMINDER = 'PR'
    MAINTENANCE_UPDATE = 'MU'
    CUSTOM_MESSAGE = 'CM'
    
    NOTIFICATION_TYPES = [
        (LEASE_RENEWAL, 'Lease Renewal'),
        (PAYMENT_REMINDER, 'Payment Reminder'),
        (MAINTENANCE_UPDATE, 'Maintenance Update'),
        (CUSTOM_MESSAGE, 'Custom Message'),
    ]

    # Notification Status
    UNREAD = 'UN'
    READ = 'RD'
    ARCHIVED = 'AR'

    NOTIFICATION_STATUS = [
        (UNREAD, 'Unread'),
        (READ, 'Read'),
        (ARCHIVED, 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=2, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=2, choices=NOTIFICATION_STATUS, default=UNREAD)
    link = models.URLField(blank=True, null=True, help_text="Optional link to more details.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.title}"

    def mark_as_read(self):
        self.status = self.READ
        self.save(update_fields=['status', 'updated_at'])

    def mark_as_archived(self):
        self.status = self.ARCHIVED
        self.save(update_fields=['status', 'updated_at'])

    def send_notification(self):
        self.sent_at = timezone.now()
        self.save(update_fields=['sent_at', 'updated_at'])
        # Add code here to send email, push, or SMS notifications if needed.

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
