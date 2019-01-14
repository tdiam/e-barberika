from datetime import datetime
import json

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from project.api.models import Product, Shop, Price
from project.api.views import PricesView

class PricePostTestCase(TestCase):
    ''' Test suite for price model '''

    def setUp(self):
        # _
        User = get_user_model()

        self.factory = RequestFactory()
        self.view = PricesView.as_view()

        shop = Shop(id=10, name='hexαδακτυλος', address='Αριστοφανους 32', coordinates=Point(22.18339, 39.89279))
        shop_away = Shop(id=11, name='χεξadaktylos', address='Devils horn', coordinates=Point(10, 10))
        shop.save()
        shop_away.save()

        product = Product(id=20, name='Αντρικιο', description='Γυναικειο', category='κουρεμα')
        product.save()

        userinfo = dict(username='johndoe', password='johndoe')
        self.user = User(**userinfo)
        self.user.save()

        # proto request
        self.request = dict(
            shopId=10,
            productId=20,
            dateFrom='2018-10-30',
            dateTo='2018-11-30',
            price=10.7
        )

        self.request_away = dict(
            shopId=11,
            productId=20,
            dateFrom='2018-10-30',
            dateTo='2018-12-15',
            price=31
        )


    def _get_response(self, request_data):
        request = self.factory.post('/', request_data)
        request.user = self.user

        resp = self.view(request)
        # print(resp.content.decode())
        return resp

    def test_post_prices(self):
        ''' check if POST /observatory/api/prices/ works '''
        prev_count = Price.objects.count()

        response = self._get_response(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(prev_count + 1, Price.objects.count())

    def test_post_prices_without_user(self):
        ''' bad user --> 403 forbidden '''
        request = self.factory.post('/', self.request)
        response = self.view(request)

        self.assertEqual(response.status_code, 403)

    def test_post_prices_invalid_parameters(self):
        ''' invalid params --> 400 bad request '''
        for which in self.request:
            req = dict(self.request)
            req[which] = 'invalid parameter'

            response = self._get_response(req)
            self.assertEqual(response.status_code, 400)

        # dateFrom <= dateTo or fail
        req = dict(self.request)
        req['dateFrom'] = '2018-12-20'
        req['dateTo'] = '2018-12-10'

        response = self._get_response(req)
        self.assertEqual(response.status_code, 400)

    def test_post_prices_updates_old_date_for_same_shop_product(self):
        response = self._get_response(self.request)
        old_price = Price.objects.all().filter(shop__id=self.request['shopId'], date_from=Price.parse_date('2018-10-30')).get()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Price.objects.all().count(), 1)
        self.assertEqual(old_price.date_to, datetime.date(Price.parse_date('2018-11-30')))

        response = self._get_response(self.request_away)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Price.objects.all().count(), 2)

        req = dict(self.request)
        req['dateFrom'] = '2018-11-15'
        req['dateTo'] = '2019-02-02'

        response = self._get_response(req)

        # check if request was ok
        self.assertEqual(response.status_code, 201)

        # check if new price was added ok
        old_price = Price.objects.all().filter(shop__id=self.request['shopId'], date_from=Price.parse_date('2018-10-30')).get()
        new_price = Price.objects.all().filter(shop__id=self.request['shopId'], date_from=Price.parse_date('2018-11-15')).get()
        unaffected_price = Price.objects.all().filter(shop__id=self.request_away['shopId'], date_from=Price.parse_date('2018-10-30')).get()

        # check to see if previous `price.dateTo` was updated
        self.assertEqual(old_price.date_to, new_price.date_from)

        # check if new `dateTo` is ok
        self.assertEqual(new_price.date_to, datetime.date(Price.parse_date(req['dateTo'])))

        # check if price at other shop remained unaffected
        self.assertEqual(unaffected_price.date_to, datetime.date(Price.parse_date(self.request_away['dateTo'])))





class PriceGetTestCase(TestCase):
    def setUp(self):
        User = get_user_model()
        self.factory = RequestFactory()
        self.view = PricesView.as_view()

        self.shop = Shop(id=10, name='hexαδακτυλος', address='Αριστοφανους 32', coordinates=Point(22.18339, 39.89279))
        self.shop_away = Shop(id=11, name='χεξadaktylos', address='Devils horn', coordinates=Point(10, 10))
        self.shop.save()
        self.shop_away.save()

        self.product = Product(id=20, name='Αντρικιο', description='Γυναικειο', category='κουρεμα')
        self.product.save()


        self.product_2 = Product(id=21, name='λαδι μαλλιων', description='αντρικο', category='αναλωσιμο')
        self.product_2.save()

        userinfo = dict(username='johndoe', password='johndoe')
        self.user = User(**userinfo)
        self.user.save()

        price_1 = Price(shop=self.shop, product=self.product, user=self.user,
                        date_from=Price.parse_date('2018-10-15'),
                        date_to=Price.parse_date('2018-10-20'),
                        price=10)
        price_1.save()

        price_2 = Price(shop=self.shop_away, product=self.product, user=self.user,
                        date_from=Price.parse_date('2018-10-16'),
                        date_to=Price.parse_date('2018-10-21'),
                        price=20)
        price_2.save()

        price_3 = Price(shop=self.shop, product=self.product_2, user=self.user,
                        date_from=Price.parse_date('2018-10-10'),
                        date_to=Price.parse_date('2018-10-23'),
                        price=20)
        price_3.save()

    def _request(self, params=None):
        if isinstance(params, dict):
            req = self.factory.get('/', params)
        elif isinstance(params, str):
            req = self.factory.get('/' + params)
        else:
            req = self.factory.get('/')
        r = self.view(req)

        # print(r.content)

        return r

    def test_can_send_no_parameters(self):
        res = self._request()
        self.assertEqual(res.status_code, 200)

    def test_can_send_start(self):
        res = self._request({'start' : 10})
        self.assertEqual(res.status_code, 200)

        self.assertEqual(json.loads(res.content)['start'], 10)

    def test_can_detect_false_start(self):
        res = self._request({'start' : 'asd'})
        self.assertEqual(res.status_code, 400)

    def test_can_send_count(self):
        res = self._request({'count' : 56})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content)['count'], 56)

    def test_can_detect_false_count(self):
        res = self._request({'count' : 'asf'})
        self.assertEqual(res.status_code, 400)

    def test_can_send_start_n_count(self):
        res = self._request({'start' : 10, 'count' : 20})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content)['start'], 10)
        self.assertEqual(json.loads(res.content)['count'], 20)


    def test_cannot_send_one_geo(self):
        res = self._request({'geoDist' : 3})
        self.assertEqual(res.status_code, 400)

    def test_cannot_send_two_geos(self):
        res = self._request({'geoLat' : 4.564, 'geoLng' : 78.23546})
        self.assertEqual(res.status_code, 400)

    def test_can_send_all_geos(self):
        res = self._request({'geoDist' : 3, 'geoLat' : 34.46354634, 'geoLng' : 46.346})
        self.assertEqual(res.status_code, 200)

    def test_can_detect_wrong_dist(self):
        res = self._request({'geoDist' : 3.45, 'geoLat' : 34.46354634, 'geoLng' : 46.346})
        self.assertEqual(res.status_code, 400)

    def test_can_detect_wrong_lat(self):
        res = self._request({'geoDist' : 3, 'geoLat' : 90.000001, 'geoLng' : 46.346})
        self.assertEqual(res.status_code, 400)

    def test_can_detect_wrong_lng(self):
        res = self._request({'geoDist' : 3, 'geoLat' : 34.46354634, 'geoLng' : 180.000001})
        self.assertEqual(res.status_code, 400)

    def test_cannot_send_one_date(self):
        res = self._request({'dateFrom' : '2018-12-23'})
        self.assertEqual(res.status_code, 400)

    def test_can_send_correct_dates(self):
        res = self._request({'dateFrom' : '2018-12-21', 'dateTo' : '2018-12-25'})
        self.assertEqual(res.status_code, 200)

    def test_can_send_same_dates(self):
        res = self._request({'dateFrom' : '2018-12-21', 'dateTo' : '2018-12-21'})
        self.assertEqual(res.status_code, 200)

    def test_cannot_send_not_correctly_formatted_dates(self):
        res = self._request({'dateFrom' : '2018-2-21', 'dateTo' : '2018-12-21'})
        self.assertEqual(res.status_code, 400)

    def test_cannot_send_out_of_order_dates(self):
        res = self._request({'dateFrom' : '2018-12-27', 'dateTo' : '2018-12-21'})
        self.assertEqual(res.status_code, 400)

    def test_can_send_lists(self):
        res = self._request('?shops=12&shops=123')
        self.assertEqual(res.status_code, 200)

    def test_can_send_sort(self):
        res = self._request('?sort=price|ASC&sort=date|ASC')
        self.assertEqual(res.status_code, 200)

    def test_cannot_send_bollocks_sort(self):
        res = self._request('?sort=price|ASC&sort=size|ASC')
        self.assertEqual(res.status_code, 400)

    def test_cannot_send_duplicate_sort(self):
        res = self._request('?sort=price|ASC&sort=date|DESC&sort=price|ASC')
        self.assertEqual(res.status_code, 400)

    def test_cannot_send_conflicting_sort(self):
        res = self._request('?sort=price|ASC&sort=price|DESC')
        self.assertEqual(res.status_code, 400)

    def test_can_send_complex_query(self):
        res = self._request('?start=0&count=50&geoDist=3&geoLng=37.977328&geoLat=23.727811'
                            '&dateFrom=2018-12-21&dateTo=2018-12-25&shops=123&shops=11&shops=89'
                            '&products=1&products=23&products=233&tags=laptop&sort=price|ASC')
        self.assertEqual(res.status_code, 200)

    # Below this, some things are hardcoded, but who cares

    def test_sort_by_price_works(self):
        res = self._request('?sort=price|ASC&dateFrom=2015-01-01&dateTo=2030-01-01')

        j = json.loads(res.content.decode())
        self.assertEqual(j['prices'][0]['price'], 10)
        self.assertEqual(j['prices'][2]['price'], 20)

        res = self._request('?sort=price|ASC&dateFrom=2015-01-01&dateTo=2030-01-01')
        j = json.loads(res.content.decode())
        self.assertEqual(j['prices'][2]['price'], 20)
        self.assertEqual(j['prices'][0]['price'], 10)

    def test_sort_by_dist_works(self):
        res = self._request('?sort=geoDist|DESC&geoLng=38&geoLat=27&geoDist=10000&dateFrom=2015-01-01&dateTo=2030-01-01')
        j = json.loads(res.content.decode())
        self.assertGreaterEqual(j['prices'][0]['shopDist'], j['prices'][2]['shopDist'])

        res = self._request('?sort=geoDist|ASC&geoLng=38&geoLat=27&geoDist=10000&dateFrom=2015-01-01&dateTo=2030-01-01')
        j = json.loads(res.content.decode())
        self.assertGreaterEqual(j['prices'][2]['shopDist'], j['prices'][0]['shopDist'])

        #  print(json.dumps(j, indent=4, ensure_ascii=False))

    def test_sort_by_date_works(self):
        res = self._request('?sort=date|DESC&dateFrom=2015-01-01&dateTo=2030-01-01')
        j = json.loads(res.content.decode())
        self.assertGreaterEqual(j['prices'][0]['date'], j['prices'][2]['date'])

        res = self._request('?sort=date|ASC&dateFrom=2015-01-01&dateTo=2030-01-01')
        j = json.loads(res.content.decode())
        self.assertGreaterEqual(j['prices'][2]['date'], j['prices'][0]['date'])

    def test_sort_with_secondary_works(self):
        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&geoLng=38&geoLat=27&geoDist=10000&sort=geoDist|DESC&sort=price|ASC')
        j = json.loads(res.content.decode())

        # check (price, shop_id) pairs
        self.assertEqual((j['prices'][0]['price'], j['prices'][0]['shopId']), (20, 11))
        self.assertEqual((j['prices'][1]['price'], j['prices'][1]['shopId']), (10, 10))
        self.assertEqual((j['prices'][2]['price'], j['prices'][2]['shopId']), (20, 10))

        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&geoLng=38&geoLat=27&geoDist=10000&sort=geoDist|DESC&sort=price|DESC')
        j = json.loads(res.content.decode())

        # check (price, shop_id) pairs
        self.assertEqual((j['prices'][0]['price'], j['prices'][0]['shopId']), (20, 11))
        self.assertEqual((j['prices'][1]['price'], j['prices'][1]['shopId']), (20, 10))
        self.assertEqual((j['prices'][2]['price'], j['prices'][2]['shopId']), (10, 10))

    def test_checking_for_product_and_shop_ids_works(self):
        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&shops=10')
        j = json.loads(res.content.decode())
        for p in j['prices']:
            self.assertEqual(p['shopId'], 10)

        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&shops=10&shops=11')
        j = json.loads(res.content.decode())
        for p in j['prices']:
            self.assertIn(p['shopId'], [10, 11])

        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&products=20')
        j = json.loads(res.content.decode())
        for p in j['prices']:
            self.assertEqual(p['productId'], 20)

        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&products=20&products=21')
        j = json.loads(res.content.decode())
        for p in j['prices']:
            self.assertIn(p['productId'], [20, 21])

        res = self._request('?dateFrom=2015-01-01&dateTo=2030-01-01&products=20&shops=11')
        j = json.loads(res.content.decode())
        for p in j['prices']:
            self.assertEqual(p['productId'], 20)
            self.assertEqual(p['shopId'], 11)


    def test_checking_date_works(self):
        # check that only `price_3` is returned
        res = self._request('?dateFrom=2015-01-01&dateTo=2018-10-10')
        j = json.loads(res.content.decode())

        p = j['prices'][0]
        self.assertEqual(j['total'], 1)
        self.assertEqual((p['price'], p['shopId'], p['productId']), (20, 10, 21))

        # check that `price_3` and `price_2` are returned, in that order
        # (because we sort by date ascending, and 2018-10-10 < 2018-10-16)
        res = self._request('?dateFrom=2018-10-21&dateTo=2030-10-01&sort=date|ASC')
        j = json.loads(res.content.decode())

        # print(j)
        p3 = j['prices'][0]
        p2 = j['prices'][1]
        self.assertEqual(j['total'], 2)
        self.assertEqual((p3['price'], p3['shopId'], p3['productId']), (20, 10, 21))
        self.assertEqual((p2['price'], p2['shopId'], p2['productId']), (20, 11, 20))


    def test_checking_distance_works(self):
        for x in range(10):
            distance = x * 1000
            self.subTest(x)

            res = self._request(f'?dateFrom=2015-01-01&dateTo=2028-10-10&geoLng=38&geoLat=27&geoDist={distance}')
            j = json.loads(res.content.decode())
            for p in j['prices']:
                self.assertLessEqual(p['shopDist'], distance)


