from django.test import TestCase
from django.test.client import Client

from mainapp.models import ProductCategory, Product


def fill_db():
    category = ProductCategory.objects.create(name='диваны',
                                              description='лучшие диваны')

    for i in range(10):
        Product.objects.create(name=f'диван {i}',
                               category=category,
                               short_desc=f'диван_{i}',
                               description=f'описание дивана {i}',
                               price=100 * (i + 1),
                               quantity=200)


class TestMainappSmoke(TestCase):

    def setUp(self):
        fill_db()
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)

    def test_products_url(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)

        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)

        for product in Product.objects.all():
            response = self.client.get(f'/products/product/{product.pk}/')
            self.assertEqual(response.status_code, 200)
