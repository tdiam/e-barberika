import random

import datetime
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from project.api import models

NUM_CATEGORIES = 5
NUM_TAGS = 10

def pick_max_count(collection, count):
    picks = [random.randint(0, len(collection)-1) for _ in range(count)]

    return set(picks)

class Command(BaseCommand):
    help = 'Populate database with N random products, shops and prices'
    requires_migrations_checks = True
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument('count', default=50, type=int)

    def handle(self, *args, **options):
        fake = Faker('el_GR')

        # categories
        categories = [fake.word(ext_word_list=None) for _ in range(NUM_CATEGORIES)]

        # shop and product tags
        tags = list(set([fake.word(ext_word_list=None) for _ in range(NUM_TAGS)]))

        product_tags = [models.ProductTag(tag=x) for x in tags]
        models.ProductTag.objects.bulk_create(product_tags)

        shop_tags = [models.ShopTag(tag=x) for x in tags]
        models.ShopTag.objects.bulk_create(shop_tags)

        # shops
        shops = []
        for _ in range(options['count']):
            s = models.Shop(
                name=fake.first_name(),
                address=fake.address(),
                coordinates=Point(float(fake.longitude()), float(fake.latitude()))
            )
            s.save()
            for t in pick_max_count(tags, 2):
                s.tags.add(models.ShopTag.objects.get(tag=tags[t]))

            shops.append(s)


        # products
        products = []
        for _ in range(options['count']):
            p = models.Product(
                name=fake.first_name(),
                description=fake.text(max_nb_chars=200, ext_word_list=None),
                category=categories[random.randint(0, NUM_CATEGORIES-1)]
            )
            p.save()

            for t in pick_max_count(tags, 2):
                p.tags.add(models.ProductTag.objects.get(tag=tags[t]))

            products.append(p)

        # user is asoures
        User = get_user_model()
        asoures_user = User.objects.get(username='asoures')

        # for each shop, add prices for at most `products/3` products
        date_to = models.Price.parse_date('2022-10-10') # well into the future 
        for s in shops:
            prod_ids = pick_max_count(products, options['count'] // 3)

            for pid in prod_ids:
                date = fake.date_this_month()
                models.Price(
                    shop=s,
                    product=products[pid],
                    user=asoures_user,
                    price=random.randint(10, 60),
                    date_from=date - datetime.timedelta(weeks=5),
                    date_to=date_to
                ).save()
