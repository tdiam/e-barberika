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
        shop.save()

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


    def _get_response(self, request_data):
        request = self.factory.post('/', request_data)
        request.user = self.user
        return self.view(request)

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
            req[which] = 'invalid date'

            response = self._get_response(req)
            self.assertEqual(response.status_code, 400)

        # dateFrom <= dateTo or fail
        req = dict(self.request)
        req['dateFrom'] = '2018-12-20'
        req['dateTo'] = '2018-12-10'

        response = self._get_response(req)
        self.assertEqual(response.status_code, 400)

class PriceGetTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.view = PricesView.as_view()

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

    def test_can_detect_false_start(self):
        res = self._request({'start' : 'asd'})
        self.assertEqual(res.status_code, 400)

    def test_can_send_count(self):
        res = self._request({'count' : 56})
        self.assertEqual(res.status_code, 200)

    def test_can_detect_false_count(self):
        res = self._request({'count' : 'asf'})
        self.assertEqual(res.status_code, 400)

    def test_can_send_start_n_count(self):
        res = self._request({'start' : 10, 'count' : 20})
        self.assertEqual(res.status_code, 200)

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
