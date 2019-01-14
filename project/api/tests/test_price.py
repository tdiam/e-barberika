from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from project.api.models import Shop, Product, Price


class PriceTestCase(TestCase):
    ''' Test suite for price model '''

    def setUp(self):
        User = get_user_model()

        shop = Shop(name='hexαδακτυλος', address='Αριστοφανους 32', coordinates=Point(22.18339, 39.89279))
        shop.save()

        product = Product(name='Αντρικιο', description='Γυναικειο', category='κουρεμα')
        product.save()

        userinfo = dict(username='johndoe', password='johndoe')
        user = User(**userinfo)
        user.save()

        self.entry = Price(shop=shop, product=product, user=user, price=10.0)

    def test_can_add_price(self):
        ''' check if adding price works '''
        prev_count = Price.objects.count()
        self.entry.save()

        self.assertEqual(Price.objects.count(), prev_count + 1)
