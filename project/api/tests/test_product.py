from django.test import TestCase
from ..models import Product


class ProductTestCase(TestCase):
    ''' This is the test suite for the Product Model '''

    def setUp(self):
        self.product = Product(
            product_name ='Playmobil Haircut',
            store_name = 'Sixfinger Guy',
            price = 3.0
        )

    def test_can_create_product(self):
        num_of_products_before = Product.objects.count()

        self.product.save()

        num_of_products_after = Product.objects.count()

        self.assertEqual(num_of_products_before + 1, num_of_products_after)