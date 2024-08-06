from django.core.management.base import BaseCommand
from houses.models import Feature


class Command(BaseCommand):
    help = 'Insert features into the database'

    FEATURES = [
        ('fireplace', 'Fireplace'),
        ('hardwood_floors', 'Hardwood Floors'),
        ('central_air_conditioning', 'Central Air Conditioning'),
        ('swimming_pool', 'Swimming Pool'),
        ('built_in_kitchen_appliances', 'Built-in Kitchen Appliances'),
        ('walk_in_closet', 'Walk-in Closet'),
        ('home_office', 'Home Office'),
        ('finished_basement', 'Finished Basement'),
        ('garage_door_opener', 'Garage Door Opener'),
        ('solar_panels', 'Solar Panels'),
        ('garden', 'Garden'),
        ('patio', 'Patio'),
        ('security_system', 'Security System'),
        ('smart_home_technology', 'Smart Home Technology'),
        ('jacuzzi_hot_tub', 'Jacuzzi/Hot Tub'),
        ('high_ceilings', 'High Ceilings'),
        ('balcony', 'Balcony'),
        ('fitness_room', 'Fitness Room'),
        ('wine_cellar', 'Wine Cellar'),
        ('skylights', 'Skylights'),
    ]

    def handle(self, *args, **kwargs):
        for code, name in self.FEATURES:
            Feature.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS('Successfully inserted features'))
