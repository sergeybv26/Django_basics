from django.test import TestCase

from mainapp.models import Product, ProductCategory


class ProductsTestCase(TestCase):
    def setUp(self) -> None:
        category = ProductCategory.objects.create(name='диваны',
                                                  description='лучшие диваны')

        self.product_1 = Product.objects.create(name='диван 1',
                                                category=category,
                                                short_desc='диван_1',
                                                description='описание дивана 1',
                                                price=1500,
                                                quantity=200)

        self.product_2 = Product.objects.create(name='диван 2',
                                                category=category,
                                                short_desc='диван_2',
                                                description='описание дивана 2',
                                                price=3200,
                                                quantity=200,
                                                is_active = False)

        self.product_3 = Product.objects.create(name='диван 3',
                                                category=category,
                                                short_desc='диван_3',
                                                description='описание дивана 3',
                                                price=5600,
                                                quantity=200)

    def test_product_get(self):
        product_1 = Product.objects.get(name='диван 1')
        product_2 = Product.objects.get(name='диван 2')

        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_get_items(self):
        product_1 = Product.objects.get(name='диван 1')
        product_3 = Product.objects.get(name='диван 3')

        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])
