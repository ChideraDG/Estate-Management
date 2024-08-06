from django.core.management.base import BaseCommand
from estates.models import Utility


class Command(BaseCommand):
    help = 'Insert amenities into the database'

    UTILITIES = [
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
        ('sewage', 'Sewage'),
        ('security', 'Security'),
        ('elevator', 'Elevator'),
        ('trash_collection', 'Trash Collection'),
        ('garbage_collection', 'Garbage Collection'),
    ]

    def handle(self, *args, **kwargs):
        for code, name in self.UTILITIES:
            Utility.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write(self.style.SUCCESS('Successfully inserted utilities'))
