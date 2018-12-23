from django.test import TestCase
from django.contrib.gis.geos import Point

from ..models import Shop, ShopTag


class ShopTestCase(TestCase):
    '''This is the test suite for the Shop model'''

    def setUp(self):
        '''Initialization of the test suite'''
        self.shop_name = 'Εξαδάκτυλος'
        self.address = 'Αριστοφάνους 51'
        self.tag_name = 'Ανδρικά'
        # Longitude, latitude
        self.coords = 22.18339, 39.89279
        self.shop = Shop(name=self.shop_name, address=self.address, coordinates=Point(*self.coords))

    def test_can_create_shop(self):
        '''Check if Shop works with the database and can be saved'''
        num_of_shops_before = Shop.objects.count()
        self.shop.save()
        num_of_shops_after = Shop.objects.count()
        # If saving was successful, then the two numbers should
        # differ by one
        self.assertEqual(num_of_shops_before + 1, num_of_shops_after)

    def test_shop_tags_work(self):
        '''Some checks on the many-to-many relationship between Shop and ShopTag'''
        # Save shop to use in relationship
        self.shop.save()

        # Create a tag
        tag = ShopTag(tag=self.tag_name)
        tag.save()

        # Add to shop
        self.shop.tags.add(tag)

        # Check if tag was saved
        self.assertTrue(tag in self.shop.tags.all())

        # Check if shop is accessible from tag
        self.assertTrue(self.shop in tag.shop_set.all())

    def test_withdrawn_shop_does_not_exist(self):
        '''Check if withdrawn shops are included in default queryset'''
        # Save shop as withdrawn
        self.shop.withdrawn = True
        self.shop.save()

        with self.assertRaises(Shop.DoesNotExist):
            _shops = Shop.objects.get(pk=self.shop.pk)

    def test_shops_within_distance_works(self):
        '''Define a close and a far point and check if within_distance_from queries work correctly'''
        # Save shop
        self.shop.save()

        # Close point
        # Must be <= 2km from the shop
        lng, lat = self.coords
        # 0.01 degrees in longitude is at most 1.1132km
        # https://en.wikipedia.org/wiki/Decimal_degrees
        lng -= 0.01

        shops_near_a = Shop.objects.within_distance_from(lat, lng, km=2)
        self.assertTrue(self.shop in shops_near_a)

        # Far point
        # Must be > 2km from the shop
        lng, lat = self.coords
        # 0.05 degrees >= 2.1748km between the 67th parallel north and south
        # https://en.wikipedia.org/wiki/67th_parallel_north
        lng -= 0.05

        shops_near_b = Shop.objects.within_distance_from(lat, lng, km=2)
        self.assertFalse(self.shop in shops_near_b)

    def test_shops_with_tags_works(self):
        '''Check if with_tags custom query works correctly'''
        # Save shop
        self.shop.save()

        # Add some tags
        self.shop.tags.create(tag='blue')
        self.shop.tags.create(tag='yellow')

        # Create another shop with tags
        shop_b = Shop(name='Κατάστημα Β', address='Ιάσονος 40', coordinates=Point(0, 0))
        shop_b.save()
        shop_b.tags.create(tag='black')

        self.subTest(i=0)
        # Search for yellow, black tags. Both should appear.
        yellow_or_black = Shop.objects.with_tags(['yellow', 'black'])
        self.assertTrue(self.shop in yellow_or_black)
        self.assertTrue(shop_b in yellow_or_black)

        self.subTest(i=1)
        # Search for blue, yellow tags. Shop A should appear only once.
        blue_or_yellow = Shop.objects.with_tags(['blue', 'yellow'])
        self.assertEqual(len(blue_or_yellow), 1)

        self.subTest(i=2)
        # Search for red tags. None should appear.
        red = Shop.objects.with_tags(['red'])
        self.assertEqual(len(red), 0)
