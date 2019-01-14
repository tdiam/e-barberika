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

    def test_single_product_is_in_response(self):
        '''Check if the default response contains the first product's name'''
        # Default order
        product = Product.objects.order_by('-id')[0]

        req = self.factory.get(self.url)
        res = self.view(req)

        self.assertContains(res, product.name)

    def test_pagination_works(self):
        '''Check if setting the count returns the correct number of products'''
        req = self.factory.get(self.url, {'count': 30})
        res = self.view(req)

        data = json.loads(res.content)
        self.assertEqual(len(data['products']), 30)

    def test_count_greater_than_total(self):
        '''Count greater than total number of products should not affect response'''
        req = self.factory.get(self.url, {'count': 999999999999})
        res = self.view(req)

        data = json.loads(res.content)
        self.assertEqual(len(data['products']), 50)

    def test_bad_parameters(self):
        '''Wrong format of parameters should return 400 Bad Request'''
        bad_param_sets = [
            {'start': -10},
            {'start': 'hello'},
            {'start': 0, 'count': -1},
            {'status': 'YOLO'},
            {'status': 51},
            {'sort': 'id|DESK'},
            {'sort': 'name'},
            {'sort': 'id|DESC|ASC|DESC'},
        ]

        for i, bad_params in enumerate(bad_param_sets):
            with self.subTest(i=i):
                req = self.factory.get(self.url, bad_params)
                res = self.view(req)
                self.assertEqual(res.status_code, 400)

    def test_status_parameter(self):
        '''Check total number of products returned for each possible value of `status`'''
        # Get 10 products
        ten_products = Product.objects.values_list('id')[:10]
        # Withdraw them
        Product.objects.filter(id__in=ten_products).update(withdrawn=True)

        # When status is ACTIVE (default)
        with self.subTest(msg='ACTIVE status'):
            req = self.factory.get(self.url)
            res = self.view(req)
            data = json.loads(res.content)
            self.assertEqual(data['total'], 40)

        # When status is ALL
        with self.subTest(msg='ALL status'):
            req = self.factory.get(self.url, {'status': 'ALL'})
            res = self.view(req)
            data = json.loads(res.content)
            self.assertEqual(data['total'], 50)

        # When status is WITHDRAWN
        with self.subTest(msg='WITHDRAWN status'):
            req = self.factory.get(self.url, {'status': 'WITHDRAWN'})
            res = self.view(req)
            data = json.loads(res.content)
            self.assertEqual(data['total'], 10)


class ProductsPostTestCase(TestCase):
    '''Unit test for POST /products'''
    def setUp(self):
        # Get URL for /products
        self.url = reverse('products')
        self.factory = RequestFactory()
        self.view = ProductsView.as_view()

        fake = Faker('el_GR')
        self.data = dict(
            name=fake.first_name(),
        )

    def test_create_with_good_data(self):
        '''Check with normal data to see if 201 is returned and the entry is created'''
        req = self.factory.post(self.url, self.data)
        res = self.view(req)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(Product.objects.filter(name=self.data['name']).exists())

    def test_create_with_bad_data(self):
        '''Try omitting or setting bad values for each field to see if 400 Bad Request is returned'''
        # Helper functions
        def _set(key, val):
            '''Copies self.data and sets d[key] to val'''
            res = copy.deepcopy(self.data)
            res[key] = val
            return res

        def _del(key):
            '''Copies self.data and removes d[key]'''
            res = copy.deepcopy(self.data)
            res.pop(key, None)
            return res

        datasets = [
            _del('name'),
            _set('name', ''),
            _del('description'),
            _set('description', ''),
            _del('category'),
            _set('category', ''),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.post(self.url, data)
                res = self.view(req)
                self.assertEqual(res.status_code, 400)
