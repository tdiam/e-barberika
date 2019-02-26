import random

from faker import Faker
from django.core.management.base import BaseCommand

from project.api import models
from django.contrib.gis.geos import Point

NUM_CATEGORIES = 5
NUM_TAGS = 10

def pick_max_two(collection):
    one = random.randint(0, len(collection)-1)
    two = random.randint(0, len(collection)-1)

    return list(set([one, two]))

class Command(BaseCommand):
    help = 'Populate database with N random products and shops'
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
        for _ in range(options['count']):
            s = models.Shop(
                name=fake.first_name(),
                address=fake.address(),
                coordinates=Point(float(fake.longitude()), float(fake.latitude()))
            )
            s.save()
            for t in pick_max_two(tags):
                s.tags.add(models.ShopTag.objects.get(tag=tags[t]))


        # products
        for _ in range(options['count']):
            p = models.Product(
                name=fake.first_name(),
                description=fake.text(max_nb_chars=200, ext_word_list=None),
                category=categories[random.randint(0, NUM_CATEGORIES-1)]
            )
            p.save()

            for t in pick_max_two(tags):
                p.tags.add(models.ProductTag.objects.get(tag=tags[t]))
