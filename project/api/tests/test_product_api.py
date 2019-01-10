import copy
import json

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.gis.geos import Point
from faker import Faker

from ..models import Product
from ..views import ProductsView


class ProductsGetTestCase(TestCase):
    '''Unit test for GET /products'''
    def setUp(self):
        # Get URL for /products
        self.url = reverse('products')
        self.factory = RequestFactory()
        self.view = ProductsView.as_view()

        fake = Faker('el_GR')
        products = []
        # Create 50 fake products
        for _ in range(50):
            products.append(Product(
                name=fake.first_name(),
                address=fake.address(),
                description=fake.description(),
                category=fake.category()
            ))

        Product.objects.bulk_create(products)

    def test_default_parameters(self):
        '''Check if when given no parameters, the view uses the default values'''
        req = self.factory.get(self.url)
        res = self.view(req)

        data = json.loads(res.content)
        self.assertEqual(data['start'], 0)
        self.assertEqual(data['count'], 20)
        self.assertEqual(data['total'], 50)
