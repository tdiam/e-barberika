from django.test import TestCase
from django.contrib.auth.models import User

from ..models import  ShopPlaceholder, ProductPlaceholder, PriceListing

class PriceListingTestCase(TestCase):
    ''' This is the test suite for the Price Listing Model '''

    def setUp(self):
        store = ShopPlaceholder()
        prod = ProductPlaceholder()
        usr = User()
        store.save()
        prod.save()
        usr.save()
        self.listing = PriceListing(
            shop=store,
            product=prod,
            user=usr,
            price=10.0
            )

    def test_can_create_listing(self):
        '''Test that we can create a listing'''

        num_of_listings_before = PriceListing.objects.count()

        self.listing.save()

        num_of_listings_after = PriceListing.objects.count()

        self.assertEqual(num_of_listings_before + 1, num_of_listings_after)
