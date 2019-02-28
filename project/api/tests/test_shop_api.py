import copy
import json

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from faker import Faker

from .helpers import ApiRequestFactory
from ..middleware import ParseUrlEncodedParametersMiddleware as ApiMiddleware
from ..models import Shop, ShopTag
from ..views import ShopsView, ShopView


User = get_user_model()

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


class ShopsGetTestCase(TestCase):
    '''Unit test for GET /shops'''
    def setUp(self):
        # Get URL for /shops
        self.url = reverse('shops')
        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(ShopsView.as_view())

        fake = Faker('el_GR')
        shops = []
        # Create 50 fake shops
        for _ in range(50):
            lng = float(fake.longitude())
            lat = float(fake.latitude())
            shops.append(Shop(
                name=fake.first_name(),
                address=fake.address(),
                coordinates=Point(lng, lat),
            ))

        Shop.objects.bulk_create(shops)

    def test_default_parameters(self):
        '''Check if when given no parameters, the view uses the default values'''
        req = self.factory.get(self.url)
        res = self.view(req)

        data = json.loads(res.content)
        self.assertEqual(data['start'], 0)
        self.assertEqual(data['count'], 20)
        self.assertEqual(data['total'], 50)

    def test_single_shop_is_in_response(self):
        '''Check if the default response contains the first shop's name'''
        # Default order
        shop = Shop.objects.order_by('-id')[0]

        req = self.factory.get(self.url)
        res = self.view(req)

        self.assertContains(res, shop.name)

    def test_pagination_works(self):
        '''Check if setting the count returns the correct number of shops'''
        req = self.factory.get(self.url, {'count': 30})
        res = self.view(req)

        data = json.loads(res.content)
        self.assertEqual(len(data['shops']), 30)

    def test_count_greater_than_total(self):
        '''Count greater than total number of shops should not affect response'''
        req = self.factory.get(self.url, {'count': 999999999999})
        res = self.view(req)

        data = json.loads(res.content)
        self.assertEqual(len(data['shops']), 50)

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
            {'sort': 'address|ASC'},
            {'sort': 'id|DESC|ASC|DESC'},
        ]

        for i, bad_params in enumerate(bad_param_sets):
            with self.subTest(i=i):
                req = self.factory.get(self.url, bad_params)
                res = self.view(req)
                self.assertEqual(res.status_code, 400)

    def test_status_parameter(self):
        '''Check total number of shops returned for each possible value of `status`'''
        # Get 10 shops
        ten_shops = Shop.objects.values_list('id')[:10]
        # Withdraw them
        Shop.objects.filter(id__in=ten_shops).update(withdrawn=True)

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


class ShopsPostTestCase(TestCase):
    '''Unit test for POST /shops'''
    def setUp(self):
        # Get URL for /shops
        self.url = reverse('shops')
        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(ShopsView.as_view())

        # Create volunteer
        self.volunteer = User.objects.create_user(username='volunteer', password='volunteer')
        self.volunteer.groups.create(name='Volunteer')

        fake = Faker('el_GR')
        self.data = dict(
            name=fake.first_name(),
            address=fake.address(),
            lng=float(fake.longitude()),
            lat=float(fake.latitude()),
            tags=fake.bs().split(),
        )

    def test_access_level(self):
        '''Check if POST is only accessible to volunteer users'''
        req = self.factory.post(self.url, self.data)
        req.user = AnonymousUser()
        res = self.view(req)

        self.assertEqual(res.status_code, 401)

    def test_create_with_good_data(self):
        '''Check with normal data to see if 200 is returned and the entry is created'''
        req = self.factory.post(self.url, self.data)
        req.user = self.volunteer
        res = self.view(req)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(Shop.objects.filter(name=self.data['name']).exists())
        for tag in self.data['tags']:
            self.assertTrue(ShopTag.objects.filter(shop__name=self.data['name'], tag=tag).exists())

    def test_create_with_bad_data(self):
        '''Try omitting or setting bad values for each field to see if 400 Bad Request is returned'''
        datasets = [
            _del(self.data, 'name'),
            _set(self.data, 'name', ''),
            _del(self.data, 'address'),
            _set(self.data, 'address', ''),
            _del(self.data, 'lng'),
            _set(self.data, 'lng', '181.0'),
            _set(self.data, 'lng', 'abcdef'),
            _set(self.data, 'lng', ''),
            _set(self.data, 'lat', '-92.48'),
            _set(self.data, 'lat', 'xyz'),
            _set(self.data, 'lat', ''),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.post(self.url, data)
                req.user = self.volunteer
                res = self.view(req)
                self.assertEqual(res.status_code, 400)


class ShopItemTestCase(TestCase):
    def setUp(self):
        # Only so that middleware is applied
        # Not necessary to reflect exact resource path
        self.url = settings.API_ROOT
        self.factory = ApiRequestFactory()
        self.view = ApiMiddleware(ShopView.as_view())

        # Create volunteer
        self.volunteer = User.objects.create_user(username='volunteer', password='volunteer')
        self.volunteer.groups.create(name='Volunteer')

        # Create admin
        self.admin = User.objects.create_user(username='admin', password='admin', is_staff=True)

        fake = Faker('el_GR')
        lng = float(fake.longitude())
        lat = float(fake.latitude())
        self.shop = Shop(
            name=fake.first_name(),
            address=fake.address(),
            coordinates=Point(lng, lat),
        )
        self.shop.save()
        tag_objs = [ShopTag(tag=t) for t in fake.bs().split()]
        for t in tag_objs:
            t.save()

        self.shop.tags.set(tag_objs)

        self.new_data = dict(
            name=fake.first_name(),
            address=fake.address(),
            lng=float(fake.longitude()),
            lat=float(fake.latitude()),
            tags=fake.bs().split(),
        )

    def test_access_level(self):
        '''Check if view protects volunteer-only methods'''
        methods = ['put', 'patch', 'delete']

        for method in methods:
            forge = getattr(self.factory, method)
            req = forge(self.url)
            req.user = AnonymousUser()
            res = self.view(req, pk=self.shop.id)
            self.assertEqual(res.status_code, 401)

    def test_get_finds_existing_shop(self):
        '''Check if GET /shops/<id> returns the created shop'''
        req = self.factory.get(self.url)
        res = self.view(req, pk=self.shop.id)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.shop.name)

    def test_get_returns_404_for_nonexisting(self):
        '''Check if GET returns 404 when given nonexisting ids'''
        ids = [-1, self.shop.id + 1, 'nonexisting-id', '']

        for id_ in ids:
            with self.subTest(msg=f'id={id_}'):
                req = self.factory.get(self.url)
                res = self.view(req, pk=id_)

                self.assertEqual(res.status_code, 404)

    def test_put_replaces_existing_shop(self):
        '''Check if PUT /shops/<id> replaces existing shop'''
        req = self.factory.put(self.url, self.new_data)
        req.user = self.volunteer
        res = self.view(req, pk=self.shop.id)

        self.shop.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.shop.name, self.new_data['name'])
        for t in self.new_data['tags']:
            self.assertTrue(ShopTag.objects.filter(shop__id=self.shop.id, tag=t).exists())

    def test_put_without_tags_clears_them(self):
        '''Check if passing no tags to PUT clears them for this shop'''
        data = _del(self.new_data, 'tags')
        req = self.factory.put(self.url, data)
        req.user = self.volunteer
        res = self.view(req, pk=self.shop.id)

        self.shop.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.shop.tags.count(), 0)

    def test_put_fails_on_invalid_data(self):
        '''Check if PUT returns 400 when given incomplete or invalid data'''
        datasets = [
            _del(self.new_data, 'name'),
            _set(self.new_data, 'name', ''),
            _del(self.new_data, 'address'),
            _set(self.new_data, 'address', ''),
            _del(self.new_data, 'lng'),
            _set(self.new_data, 'lng', '451'),
            _set(self.new_data, 'lng', 'invalid'),
            _set(self.new_data, 'lng', ''),
            _set(self.new_data, 'lat', '-110.4'),
            _set(self.new_data, 'lat', 'zzzzz'),
            _set(self.new_data, 'lat', ''),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.put(self.url, data)
                req.user = self.volunteer
                res = self.view(req, pk=self.shop.id)
                self.assertEqual(res.status_code, 400)

    def test_patch_edits_existing_shop(self):
        '''Check if PATCH updates information of existing shop'''
        datasets = [
            {'name': self.new_data['name']},
            {'address': self.new_data['address']},
            {'lng': self.new_data['lng']},
            _del(self.new_data, 'name'),
            _del(self.new_data, 'address'),
            _del(self.new_data, 'lng'),
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.patch(self.url, data)
                req.user = self.volunteer
                res = self.view(req, pk=self.shop.id)

                self.assertEqual(res.status_code, 200)
                # Get updated information from database
                self.shop.refresh_from_db()

                # Check if all fields have been updated successfully
                for field, val in data.items():
                    if field == 'tags':
                        stored_tags = list(self.shop.tags.values_list('tag', flat=True))
                        self.assertCountEqual(stored_tags, val)
                    else:
                        if field == 'lng':
                            stored_val = self.shop.coordinates.x
                        elif field == 'lat':
                            stored_val = self.shop.coordinates.y
                        else:
                            stored_val = getattr(self.shop, field)
                        self.assertEqual(stored_val, val)

    def test_patch_fails_with_bad_data(self):
        '''Check if PATCH returns 400 when given invalid data'''
        datasets = [
            {'name': ''},
            {'address': ''},
            {'lng': '451'},
            {'lng': 'invalid'},
            {'lng': ''},
            {'lat': '-110.4'},
            {'lat': ''},
        ]

        for i, data in enumerate(datasets):
            with self.subTest(i=i):
                req = self.factory.patch(self.url, data)
                req.user = self.volunteer
                res = self.view(req, pk=self.shop.id)
                self.assertEqual(res.status_code, 400)

    def test_delete_returns_404_for_wrong_id(self):
        '''Check if DELETE returns 404 when given a wrong shop ID'''
        req = self.factory.delete(self.url)
        req.user = self.volunteer

        for shop_id in [-1, self.shop.id + 1, 'invalid-id']:
            res = self.view(req, pk=shop_id)
            self.assertEqual(res.status_code, 404)

    def test_delete_withdraws_when_user_is_volunteer(self):
        '''Check if DELETE withdraws the shop when user is a volunteer'''
        req = self.factory.delete(self.url)
        req.user = self.volunteer
        res = self.view(req, pk=self.shop.id)

        # Get updated information from database
        self.shop.refresh_from_db()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.shop.withdrawn)

    def test_delete_removes_shop_when_user_is_admin(self):
        '''Check if DELETE removes the shop from db when user is an admin'''
        req = self.factory.delete(self.url)
        req.user = self.admin
        res = self.view(req, pk=self.shop.id)

        self.assertEqual(res.status_code, 200)
        with self.assertRaises(Shop.DoesNotExist):
            self.shop.refresh_from_db()
