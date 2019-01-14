import copy
import json

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from .helpers import ApiRequestFactory
from ..middleware import ParseUrlEncodedParametersMiddleware as ApiMiddleware
from ..models import Product, ProductTag
from ..views import ProductsView, ProductView

# Helper functions
def _set(d, key, val):
    '''Copies d and sets d[key] to val'''
    res = copy.deepcopy(d)
    res[key] = val
    return res

def _del(d, key):
    '''Copies d and removes d[key]'''
    res = copy.deepcopy(d)
    res.pop(key, None)
    return res

class ProductsGetTestCase(TestCase):
    '''Unit test for GET /products'''
    def setUp(self):
        # Get URL for /products
        self.url = reverse('products')
        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(ProductsView.as_view())

        fake = Faker('el_GR')
        products = []
        # Create 50 fake products
        for _ in range(50):
            products.append(Product(
                name=fake.first_name(),
                description=fake.text(max_nb_chars=200, ext_word_list=None),
                category=fake.word(ext_word_list=None),
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
        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(ProductsView.as_view())

        fake = Faker('el_GR')
        self.data = dict(
            name=fake.first_name(),
            description=fake.text(max_nb_chars=200, ext_word_list=None),
            category=fake.word(ext_word_list=None),
        )

    def test_create_with_good_data(self):
        '''Check with normal data to see if 201 is returned and the entry is created'''
        req = self.factory.post(self.url, self.data)
        res = self.view(req)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(Product.objects.filter(name=self.data['name']).exists())

    def test_create_with_bad_data(self):
        '''Try omitting or setting bad values for each field to see if 400 Bad Request is returned'''

        datasets = [
            _del(self.data, 'name'),
            _set(self.data, 'name', ''),
            _del(self.data, 'description'),
            _set(self.data, 'description', ''),
            _del(self.data, 'category'),
            _set(self.data, 'category', ''),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.post(self.url, data)
                res = self.view(req)
                self.assertEqual(res.status_code, 400)

class ProductItemTestCase(TestCase):
    def setUp(self):
        # Only so that middleware is applied
        # Not necessary to reflect exact resource path
        self.url = settings.API_ROOT
        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(ProductView.as_view())

        fake = Faker('el_GR')
        self.product = Product(
            name=fake.first_name(),
            description=fake.text(max_nb_chars=200, ext_word_list=None),
            category=fake.word(ext_word_list=None),
        )
        self.product.save()
        tag_objs = [ProductTag(tag=t) for t in fake.bs().split()]
        for t in tag_objs:
            t.save()

        self.product.tags.set(tag_objs)

        self.new_data = dict(
            name=fake.first_name(),
            description=fake.text(max_nb_chars=200, ext_word_list=None),
            category=fake.word(ext_word_list=None),
            tags=fake.bs().split(),
        )

    def test_get_finds_existing_product(self):
        '''Check if GET /products/<id> returns the created product'''
        req = self.factory.get(self.url)
        res = self.view(req, pk=self.product.id)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.product.name)

    def test_get_returns_404_for_nonexisting(self):
        '''Check if GET returns 404 when given nonexisting ids'''
        ids = [-1, self.product.id + 1, 'nonexisting-id', '']

        for id_ in ids:
            with self.subTest(msg=f'id={id_}'):
                req = self.factory.get(self.url)
                res = self.view(req, pk=id_)

                self.assertEqual(res.status_code, 404)

    def test_put_replaces_existing_product(self):
        '''Check if PUT /products/<id> replaces existing product'''
        req = self.factory.put(self.url, self.new_data)
        res = self.view(req, pk=self.product.id)

        self.product.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.product.name, self.new_data['name'])
        for t in self.new_data['tags']:
            self.assertTrue(ProductTag.objects.filter(product__id=self.product.id, tag=t).exists())

    def test_put_without_tags_clears_them(self):
        '''Check if passing no tags to PUT clears them for this product'''
        data = _del(self.new_data, 'tags')
        req = self.factory.put(self.url, data)
        res = self.view(req, pk=self.product.id)

        self.product.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.product.tags.count(), 0)

    def test_put_fails_on_invalid_data(self):
        '''Check if PUT returns 400 when given incomplete or invalid data'''
        datasets = [
            _del(self.new_data, 'name'),
            _set(self.new_data, 'name', ''),
            _del(self.new_data, 'description'),
            _set(self.new_data, 'description', ''),
            _del(self.new_data, 'category'),
            _set(self.new_data, 'category', ''),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.put(self.url, data)
                res = self.view(req, pk=self.product.id)
                self.assertEqual(res.status_code, 400)

    def test_patch_edits_existing_product(self):
        '''Check if PATCH updates information of existing product'''
        datasets = [
            {'name': self.new_data['name']},
            {'description': self.new_data['description']},
            {'category': self.new_data['category']},
            _del(self.new_data, 'name'),
            _del(self.new_data, 'description'),
            _del(self.new_data, 'category'),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.patch(self.url, data)
                res = self.view(req, pk=self.product.id)

                self.assertEqual(res.status_code, 200)
                # Get updated information from database
                self.product.refresh_from_db()

                # Check if all fields have been updated successfully
                for field, val in data.items():
                    if field == 'tags':
                        stored_tags = list(self.product.tags.values_list('tag', flat=True))
                        self.assertCountEqual(stored_tags, val)
                    else:
                        stored_val = getattr(self.product, field)
                        self.assertEqual(stored_val, val)

    def test_patch_fails_with_bad_data(self):
        '''Check if PATCH returns 400 when given invalid data'''
        datasets = [
            {'name': ''},
            {'description': ''},
            {'category': ''},
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.patch(self.url, data)
                res = self.view(req, pk=self.product.id)
                self.assertEqual(res.status_code, 400)
