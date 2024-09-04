from django.db import models
from django.contrib.auth.models import User
from apartments.models import Apartment
from leaseAgreements.models import LeaseAgreement

class Document(models.Model):
    """
    Represents a document stored in the system, including metadata such as the 
    document type, the user who uploaded it, and any related properties or leases.

    Attributes
    ----------
    title : str
        The title of the document.
    file : FileField
        The file associated with the document.
    document_type : str
        The type of the document, chosen from predefined options.
    uploaded_by : User
        The user who uploaded the document.
    related_apartment : Apartment, optional
        The apartment related to the document, nullable.
    related_lease : LeaseAgreement, optional
        The lease agreement related to the document, nullable.
    upload_date : datetime
        The date and time when the document was uploaded (auto-generated).
    shared_with : ManyToManyField
        Users with whom the document is shared.
    """
    
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
    is_archived = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Document: {self.title} - {self.document_type}"


class DocumentSharing(models.Model):
    """
    Manages the sharing of documents with specific users, such as tenants, service providers, 
    and company stakeholders.

    Attributes
    ----------
    document : Document
        The document that is being shared.
    shared_with : User
        The user with whom the document is shared.
    shared_date : datetime
        The date and time when the document was shared (auto-generated).
    access_granted : bool
        Indicates whether access to the document is granted, default is True.
    """
    
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='sharings')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_documents')
    shared_date = models.DateTimeField(auto_now_add=True)
    access_granted = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Document: {self.document.title} shared with {self.shared_with.username}"
