from django.core.management.base import BaseCommand
from estates.models import Amenity


class Command(BaseCommand):
    help = 'Insert amenities into the database'

    AMENITIES = [
        ('parking', 'Parking'),
        ('gym', 'Gym'),
        ('swimming_pool', 'Swimming pool'),
        ('cafeteria', 'Cafeteria'),
        ('spa', 'Spa'),
        ('playground', 'Playground'),
        ('terraces', 'Terraces'),
        ('helipads', 'Helipads'),
        ('package_locker', 'Package locker'),
        ('pet_friendly_amenities', 'Pet-Friendly Amenities'),
        ('laundry_facilities', 'Laundry facilities'),
    ]

    def handle(self, *args, **kwargs):
        for code, name in self.AMENITIES:
            Amenity.objects.get_or_create(code=code, defaults={'name': name})
        self.stdout.write(self.style.SUCCESS('Successfully inserted amenities'))
