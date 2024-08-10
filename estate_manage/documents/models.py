from django.db import models
from django.contrib.auth.models import User
from apartments.models import Apartment
from leaseAgreements.models import LeaseAgreement


class Document(models.Model):
    """This model represents a document stored in the system. It includes metadata such 
    as the document type, the user who uploaded it, and related properties or leases."""

    DOCUMENT_TYPE_CHOICES = [
        ('lease_agreement', 'Lease Agreement'),
        ('property_document', 'Property Document'),
        ('maintenance_record', 'Maintenance Record'),
        ('financial_report', 'Financial Report'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_documents')
    related_apartment = models.ForeignKey(Apartment, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    related_lease = models.ForeignKey(LeaseAgreement, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    upload_date = models.DateTimeField(auto_now_add=True)
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_documents')
    
    def __str__(self):
        return f"Document: {self.title} - {self.document_type}"


class DocumentSharing(models.Model):
    """This model manages the sharing of documents with specific users, such as 
    tenants, service providers, and company stakeholders."""

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='sharings')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_documents')
    shared_date = models.DateTimeField(auto_now_add=True)
    access_granted = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Document: {self.document.title} shared with {self.shared_with.username}"
