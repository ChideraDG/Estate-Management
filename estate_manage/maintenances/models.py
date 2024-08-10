from django.db import models
from apartments.models import Apartment


class WorkOrder(models.Model):
    """This model represents individual maintenance requests or work orders."""

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
    ]
    
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='work_orders')
    description = models.TextField()
    reported_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    assigned_to = models.ForeignKey('ServiceProvider', on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    completion_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Work Order: {self.description[:20]} - {self.get_status_display()}"


class MaintenanceSchedule(models.Model):
    """This model tracks preventive maintenance schedules and logs."""

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='maintenance_schedules')
    maintenance_type = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Maintenance Schedule: {self.maintenance_type} on {self.scheduled_date}"


class ServiceProvider(models.Model):
    """This model maintains a list of contractors and service providers with their contact details and service history."""

    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    service_type = models.CharField(max_length=100)
    service_history = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Service Provider: {self.name} - {self.service_type}"


class WorkOrderLog(models.Model):
    """This model logs the updates and status changes for work orders."""
    
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='logs')
    update_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=WorkOrder.STATUS_CHOICES)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Work Order Log: {self.work_order} - {self.get_status_display()} on {self.update_date}"

