from django.test import TestCase
from ..models import Shop


class ShopTestCase(TestCase):
    '''This is the test suite for the Shop model'''

    def setUp(self):
        '''Initialization of the test suite'''
        self.shop = Shop(name='Εξαδάκτυλος')

    def test_can_create_shop(self):
        '''Test suites can then define multiple tests for the
        same instance, to test various behaviors of Shop.
        This can be done by creating methods in this class whose
        names start with "test_"
        '''
        num_of_shops_before = Shop.objects.count()
        self.shop.save()
        num_of_shops_after = Shop.objects.count()
        # If saving was successful, then the two numbers should
        # differ by one
        self.assertEqual(num_of_shops_before + 1, num_of_shops_after)
