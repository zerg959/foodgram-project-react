import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        data_path = settings.BASE_DIR
        with open(
            f'{data_path}/data/ingredients.csv', 'r', encoding='utf-8'
        ) as file:
            file_reader = csv.reader(file)
            data = []
            for row in file_reader:
                name, measurement_unit = row
                ingredient = Ingredient(
                    name=name,
                    measurement_unit=measurement_unit
                )
                data.append(ingredient)
            Ingredient.objects.bulk_create(data)
