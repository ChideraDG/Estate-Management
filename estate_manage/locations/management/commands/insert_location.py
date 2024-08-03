from django.core.management.base import BaseCommand
from locations.models import Country, State
import pycountry


class Command(BaseCommand):
    help = 'Insert locations into the database'

    def handle(self, *args, **kwargs):
        for country in pycountry.countries:
            try:
                Country.objects.create(name=country.name, code=country.alpha_2)
            except Exception as e:
                print(f"Error creating country {country.name}: {e}")

        # Populate states for each country (if available)
        for country in Country.objects.all():
            subdivisions = pycountry.subdivisions.get(country_code=country.code)
            for subdivision in subdivisions:
                try:
                    State.objects.create(name=subdivision.name, code=subdivision.code, country=country)
                except Exception as e:
                    print(f"Error creating state {subdivision.name} for country {country.name}: {e}")

        self.stdout.write(self.style.SUCCESS('Successfully inserted locations'))
