from django.db import models
from apartments.models import Apartment


class Analytics(models.Model):
    """This model represents the data collected for analytics purposes. 
    It stores information related to various aspects of the estate management 
    system, such as occupancy, finances, and maintenance."""

    ANALYTICS_TYPE_CHOICES = [
        ('occupancy', 'Occupancy'),
        ('finance', 'Finance'),
        ('maintenance', 'Maintenance'),
    ]
    
    analytics_type = models.CharField(max_length=50, choices=ANALYTICS_TYPE_CHOICES)
    related_apartments = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='analytics')
    recorded_value = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.analytics_type} - {self.recorded_date}"


class CustomReport(models.Model):
    """This model handles the generation and storage of custom reports based on specific criteria or timeframes."""

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='custom_reports')
    created_date = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='reports/')
    filters_applied = models.JSONField(default=dict)  # Stores filters used to generate the report
    
    def __str__(self):
        return f"Custom Report: {self.title} by {self.created_by.username}"


class Forecasting(models.Model):
    """This model represents the forecasting tools used to predict future 
    trends in various areas such as occupancy, rental income, and expenses."""

    FORECAST_TYPE_CHOICES = [
        ('occupancy', 'Occupancy'),
        ('rental_income', 'Rental Income'),
        ('expenses', 'Expenses'),
    ]
    
    forecast_type = models.CharField(max_length=50, choices=FORECAST_TYPE_CHOICES)
    related_apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='forecasts')
    forecasted_value = models.DecimalField(max_digits=10, decimal_places=2)
    forecast_date = models.DateTimeField(auto_now_add=True)
    forecast_period = models.CharField(max_length=50)  # Example: '2025 Q1'
    
    def __str__(self):
        return f"Forecast: {self.forecast_type} for {self.forecast_period}"
