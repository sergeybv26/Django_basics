import json
import os
from authapp.models import ShopUser
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product

JSON_PATH = 'json'


def load_from_json(file_name):

    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):

    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for category in categories:
            ProductCategory.objects.create(**category)

        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            Product.objects.create(**product)

        ShopUser.objects.create_superuser('django', password='geekbrains', age=18)
