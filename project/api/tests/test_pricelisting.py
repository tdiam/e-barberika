from django.test import TestCase
from ..models import PriceListing

import datetime

class PriceListingTestCase(TestCase):
    ''' This is the test suite for the Price Listing Model '''

    def setUp(self):
        self.listing = PriceListing(
            store_name='ΕΡΓΑΤΙΑ',
            product_name='Κανονικο',
            user_name='Παναγιωτης',

            price=10.0,
            date_inserted=datetime.datetime.now(),
            date_invalidated=None
        )

    def test_can_create_listing(self):
        '''Test that we can create a listing'''

        num_of_listings_before = PriceListing.objects.count()

        self.listing.save()

        num_of_listings_after = PriceListing.objects.count()

        self.assertEqual(num_of_listings_before + 1, num_of_listings_after)