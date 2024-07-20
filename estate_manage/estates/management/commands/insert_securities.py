from django.core.management.base import BaseCommand
from estates.models import SecurityFeatures


class Command(BaseCommand):
    help = 'Insert amenities into the database'

    SECURITY = [
        ('perimeter_security', 'Perimeter Security'),
        ('access_control_systems', 'Access Control Systems'),
        ('surveillance_technology', 'Surveillance Technology'),
        ('interior_security_measures', 'Interior Security Measures',),
        ('balancing_visibility_and_discretion', 'Balancing Visibility and Discretion'),
        ('regular_audits_and_assessments', 'Regular Audits and Assessments'),
    ]

    def handle(self, *args, **kwargs):
        for code, name in self.SECURITY:
            SecurityFeatures.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write(self.style.SUCCESS('Successfully inserted securities'))
