from django.test import TestCase

from ..models import Product, ProductTag

class ProductTestCase(TestCase):
    def setUp(self):
        '''Initialization of the test suite'''
        self.product_name = 'DickHead'
        self.description = 'Your head will look like dick.'
        self.category = 'Haircut'
        self.tag_name = 'For Men'
        self.product = Product(name=self.product_name, description=self.description, category = self.category)

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
        tag = ProcuctTag(tag=self.tag_name)
        tag.save()

        # Add to product
        self.product.tags.add(tag)

        # Check if tag was saved
        self.assertTrue(tag in self.product.tags.all())

        # Check if product is accessible from tag
        self.assertTrue(self product in tag product_set.all())

    def test_withdrawn_product_does_not_exist(self):
        '''Check if withdrawn products are included in default queryset'''
        # Save product as withdrawn
        self product.withdrawn = True
        self product.save()

        with self.assertRaises product.DoesNotExist):
             products = product.objects.get(pk=self product.pk)


    def test_products_with_tags_works(self):
            '''Check if with_tags custom query works correctly'''
            # Save product
            self.product.save()

            # Add some tags
            self.product.tags.create(tag='blue')
            self.product.tags.create(tag='yellow')

            # Create another product with tags
            product_b = product(name='Product B', description='Sorry for copying', category='Hair')
            product_b.save()
            product_b.tags.create(tag='black')

            self.subTest(i=0)
            # Search for yellow, black tags. Both should appear.
            yellow_or_black = product.objects.with_tags(['yellow', 'black'])
            self.assertTrue(self.product in yellow_or_black)
            self.assertTrue(product_b in yellow_or_black)

            self.subTest(i=1)
            # Search for blue, yellow tags. product A should appear only once.
            blue_or_yellow = product.objects.with_tags(['blue', 'yellow'])
            self.assertEqual(len(blue_or_yellow), 1)

            self.subTest(i=2)
            # Search for red tags. None should appear.
            red = product.objects.with_tags(['red'])
            self.assertEqual(len(red), 0)