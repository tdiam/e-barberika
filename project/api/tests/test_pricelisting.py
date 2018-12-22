from django.test import TestCase
from django.contrib.auth.models import User

from ..models import  shopplaceholder, productplaceholder, prices

class PriceListingTestCase(TestCase):
    ''' This is the test suite for the Price Listing Model '''

    def setUp(self):
        store = shopplaceholder()
        prod = productplaceholder()
        usr = User()
        store.save()
        prod.save()
        usr.save()
        self.prices = prices(
            shop=store,
            product=prod,
            user=usr,
            price=10.0
            )

    def test_can_create_listing(self):
        '''Test that we can create a listing'''

        num_of_prices_before = prices.objects.count()

        self.prices.save()

        num_of_prices_after = prices.objects.count()

        self.assertEqual(num_of_prices_before + 1, num_of_prices_after)
