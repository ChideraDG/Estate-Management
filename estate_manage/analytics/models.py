from django.db import models
from apartments.models import Apartment

class Analytics(models.Model):
    """
    Represents the data collected for analytics purposes, storing information related 
    to various aspects of the estate management system, such as occupancy, finances, and maintenance.

    Attributes
    ----------
    analytics_type : str
        The type of analytics data (occupancy, finance, maintenance).
    related_apartments : Apartment
        The apartment associated with the analytics data (nullable).
    recorded_value : Decimal
        The recorded value for the specific type of analytics.
    recorded_date : datetime
        The date and time when the analytics data was recorded (auto-generated).
    """
    
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
    """
    Handles the generation and storage of custom reports based on specific criteria or timeframes.

    Attributes
    ----------
    title : str
        The title of the custom report.
    description : str, optional
        A brief description of the custom report.
    created_by : User
        The user who created the report (nullable).
    created_date : datetime
        The date and time when the report was created (auto-generated).
    report_file : File
        The file containing the generated report.
    filters_applied : dict
        The filters applied during the report generation, stored as JSON.
    """
    
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='custom_reports')
    created_date = models.DateTimeField(auto_now_add=True)
    report_file = models.FileField(upload_to='reports/')
    filters_applied = models.JSONField(default=dict)  # Stores filters used to generate the report
    
    def __str__(self):
        return f"Custom Report: {self.title} by {self.created_by.username}"


class Forecasting(models.Model):
    """
    Represents the forecasting tools used to predict future trends in various 
    areas such as occupancy, rental income, and expenses.

    Attributes
    ----------
    forecast_type : str
        The type of forecast (occupancy, rental income, expenses).
    related_apartment : Apartment
        The apartment associated with the forecast (nullable).
    forecasted_value : Decimal
        The predicted value for the specific forecast type.
    forecast_date : datetime
        The date and time when the forecast was generated (auto-generated).
    forecast_period : str
        The period the forecast applies to (e.g., '2025 Q1').
    """
    
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
