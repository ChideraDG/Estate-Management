from django.db import models
from apartments.models import Apartment


class WorkOrder(models.Model):
    """
    Represents individual maintenance requests or work orders.

    Attributes
    ----------
    apartment : ForeignKey
        The apartment associated with the work order.
    description : str
        A detailed description of the maintenance issue.
    reported_date : date
        The date when the work order was reported, automatically set to the current date.
    status : str
        The current status of the work order, chosen from predefined options ('Open', 'In Progress', 'Completed', 'Closed').
    assigned_to : ForeignKey, optional
        The service provider assigned to the work order, nullable.
    completion_date : date, optional
        The date when the work order was completed, nullable.
    notes : str, optional
        Additional notes or comments about the work order, nullable.
    """

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
    """
    Tracks preventive maintenance schedules and logs.

    Attributes
    ----------
    apartment : ForeignKey
        The apartment associated with the maintenance schedule.
    maintenance_type : str
        The type of maintenance to be performed.
    scheduled_date : date
        The date on which the maintenance is scheduled.
    completed : bool
        Indicates whether the maintenance has been completed.
    notes : str, optional
        Additional notes or comments about the maintenance, nullable.
    """

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='maintenance_schedules')
    maintenance_type = models.CharField(max_length=100)
    scheduled_date = models.DateField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Maintenance Schedule: {self.maintenance_type} on {self.scheduled_date}"


class ServiceProvider(models.Model):
    """
    Maintains a list of contractors and service providers with their contact details and service history.

    Attributes
    ----------
    name : str
        The name of the service provider.
    contact_person : str
        The contact person's name at the service provider.
    phone_number : str, optional
        The contact phone number for the service provider, nullable.
    email : EmailField, optional
        The contact email for the service provider, nullable.
    address : str, optional
        The physical address of the service provider, nullable.
    service_type : str
        The type of services provided by the service provider.
    service_history : str, optional
        A record of the service history for the provider, nullable.
    """

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
    """
    Logs updates and status changes for work orders.

    Attributes
    ----------
    work_order : ForeignKey
        The work order associated with the log entry.
    update_date : datetime
        The date and time when the update was made, automatically set to the current date and time.
    status : str
        The status of the work order at the time of the update, chosen from predefined options ('Open', 'In Progress', 'Completed', 'Closed').
    notes : str, optional
        Additional notes or comments about the update, nullable.
    """

    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='logs')
    update_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=WorkOrder.STATUS_CHOICES)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Work Order Log: {self.work_order} - {self.get_status_display()} on {self.update_date}"
