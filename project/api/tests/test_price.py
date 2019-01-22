from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.gis.geos import Point

from project.api.models import Shop, Product, Price


class PriceTestCase(TestCase):
    ''' Test suite for price model '''

    def setUp(self):
        User = get_user_model()

        self.shop = Shop(name='hexαδακτυλος', address='Αριστοφανους 32', coordinates=Point(22.18339, 39.89279))
        self.shop.save()

        self.product = Product(name='Αντρικιο', description='Γυναικειο', category='κουρεμα')
        self.product.save()

        userinfo = dict(username='johndoe', password='johndoe')
        self.user = User(**userinfo)
        self.user.save()
        grp, _ = Group.objects.get_or_create(name='Volunteer')
        self.user.groups.add(grp)

        self.entry = Price(shop=self.shop, product=self.product, user=self.user, price=10.0)

    def test_can_add_price(self):
        ''' check if adding price works '''
        prev_count = Price.objects.count()
        self.entry.save()

        self.assertEqual(Price.objects.count(), prev_count + 1)

    def test_can_use_add_price(self):
        res = Price.add_price(shop=self.shop, product=self.product, user=self.user, date_to=Price.parse_date('2018-10-10'), date_from=Price.parse_date('2018-09-09'), price=10.0)

        self.assertTrue(res)
        self.assertEqual(Price.objects.count(), 1)
