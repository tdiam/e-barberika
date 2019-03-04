import random

from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from project.api.models import (
    Product, ProductTag,
    Shop, ShopTag,
    Price,
)

NUM_CATEGORIES = 10
NUM_TAGS = 25

def pick_max_count(collection, count):
    picks = random.choices(collection, k=count)
    return set(picks)

class Command(BaseCommand):
    help = 'Populate database with N random products, shops and prices'
    requires_migrations_checks = True
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument('count', default=50, type=int)

    def handle(self, *args, **options):
        fake = Faker('el_GR')
        lorem = fake.provider('faker.providers.lorem')
        name_provider = fake.provider('faker.providers.person')
        uncommon_words = lorem.word_list[2 * len(lorem.common_words):]
        company_names = uncommon_words + name_provider.last_names

        # categories
        categories = fake.words(NUM_CATEGORIES, ext_word_list=uncommon_words)

        # shop and product tags
        product_tags = fake.words(NUM_TAGS, ext_word_list=uncommon_words, unique=True)
        product_tags = [ProductTag(tag=x) for x in product_tags]
        ProductTag.objects.bulk_create(product_tags)
        product_tags = ProductTag.objects.all()

        shop_tags = fake.words(NUM_TAGS, ext_word_list=uncommon_words, unique=True)
        shop_tags = [ShopTag(tag=x) for x in shop_tags]
        ShopTag.objects.bulk_create(shop_tags)
        shop_tags = ShopTag.objects.all()

        # shops
        shops = []
        shop_names = fake.words(options['count'], ext_word_list=company_names)
        for name in shop_names:
            s = Shop(
                name=name.capitalize(),
                address=fake.address(),
                coordinates=Point(float(fake.local_longitude()), float(fake.local_latitude()))
            )
            s.save()
            shops.append(s)

            for t in pick_max_count(shop_tags, 2):
                s.tags.add(t)


        # products
        products = []
        product_names = fake.words(options['count'], ext_word_list=uncommon_words)
        for name in product_names:
            p = Product(
                name=name.capitalize(),
                description=fake.text(max_nb_chars=200, ext_word_list=None),
                category=random.choice(categories)
            )
            p.save()
            products.append(p)

            for t in pick_max_count(product_tags, 2):
                p.tags.add(t)


        # user is asoures
        User = get_user_model()
        asoures_user = User.objects.get(username='asoures')

        # for each shop, add prices for at most `products/3` products

        prices = []
        for s in shops:
            prods = pick_max_count(products, options['count'] // 3)
            for prod in prods:
                date_from = fake.date_between('-30d', 'today')
                date_to = fake.date_between('today', '+30d')
                p = Price(
                    shop=s,
                    product=prod,
                    user=asoures_user,
                    price=random.randint(5, 60),
                    date_from=date_from,
                    date_to=date_to,
                )
                prices.append(p)

        Price.objects.bulk_create(prices)
