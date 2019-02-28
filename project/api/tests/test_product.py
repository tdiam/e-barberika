from django.test import TestCase

from ..models import Product, ProductTag


class ProductTestCase(TestCase):
    def setUp(self):
        '''Initialization of the test suite'''
        self.product_name = 'DickHead'
        self.description = 'Your head will look like dick.'
        self.category = 'Haircut'
        self.tag_name = 'For Men'
        self.product = Product(name=self.product_name, description=self.description, category=self.category)

    def test_can_create_product(self):
        '''Check if product works with the database and can be saved'''
        num_of_products_before = Product.objects.count()
        self.product.save()
        num_of_products_after = Product.objects.count()
        # If saving was successful, then the two numbers should
        # differ by one
        self.assertEqual(num_of_products_before + 1, num_of_products_after)

    def test_product_tags_work(self):
        # Save product to use in relationship
        self.product.save()

        # Create a tag
        tag = ProductTag(tag=self.tag_name)
        tag.save()

        # Add to product
        self.product.tags.add(tag)

        # Check if tag was saved
        self.assertTrue(tag in self.product.tags.all())

        # Check if product is accessible from tag
        self.assertTrue(self.product in tag.product_set.all())

    def test_withdrawn_product_exists(self):
        '''Check if withdrawn products are included in default queryset'''
        # Save product as withdrawn
        self.product.withdrawn = True
        self.product.save()

        try:
            _products = Product.objects.get(pk=self.product.pk)
        except Product.DoesNotExist:
            self.fail('withdrawn product should be accessible')

    def test_products_with_tags_works(self):
        '''Check if with_tags custom query works correctly'''
        # Save product
        self.product.save()

        # Add some tags
        self.product.tags.create(tag='blue')
        self.product.tags.create(tag='yellow')

        # Create another product with tags
        product_b = Product(name='Product B', description='Sorry for copying', category='Hair')
        product_b.save()
        product_b.tags.create(tag='black')

        self.subTest(i=0)
        # Search for yellow, black tags. Both should appear.
        yellow_or_black = Product.objects.with_tags(['yellow', 'black'])
        self.assertTrue(self.product in yellow_or_black)
        self.assertTrue(product_b in yellow_or_black)

        self.subTest(i=1)
        # Search for blue, yellow tags. product A should appear only once.
        blue_or_yellow = Product.objects.with_tags(['blue', 'yellow'])
        self.assertEqual(blue_or_yellow.count(), 1)

        self.subTest(i=2)
        # Search for red tags. None should appear.
        red = Product.objects.with_tags(['red'])
        self.assertEqual(red.count(), 0)

    def test_producttag_bulk_get_or_create(self):
        '''Tests the bulk_get_or_create table-level method'''
        # List of initial tags
        tags = 'one two three'.split()

        _ = ProductTag.objects.bulk_get_or_create(tags)

        # Now repeat for all plus one new 'four' tag
        tags.append('four')
        _ = ProductTag.objects.bulk_get_or_create(tags + ['four'])

        # First 3 must not be reinserted while the 4th must
        self.assertEqual(ProductTag.objects.count(), 4)
