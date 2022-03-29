import csv

from food.models import Ingredient

CSV_PATH = (
    # путь указать для своего репозитория
    '/Users/NikitaChalykh/Dev/foodgram-project-react/data/ingredients.csv'
)

with open(CSV_PATH, newline='', encoding='utf8') as csv_file:
    fieldnames = ['name', 'measurement_unit']
    reader = csv.DictReader(csv_file, fieldnames=fieldnames)
    Ingredient.objects.bulk_create(Ingredient(**data) for data in reader)
print('Im here')
