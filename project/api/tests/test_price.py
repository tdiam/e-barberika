from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Shop_tmp, Product_tmp, Price


class PriceTestCase(TestCase):
    ''' Test suite for price model '''

    def setUp(self):
        User = get_user_model()

        shop = Shop_tmp()
        shop.save()

        product = Product_tmp()
        product.save()

        user = User()
        user.save()

        self.entry = Price(shop=shop, product=product, user=user, price=10.0)

    def test_can_add_price(self):
        ''' check if adding price works '''
        prev_count = Price.objects.count()
        self.entry.save()

        self.assertEqual(Price.objects.count(), prev_count + 1)
