from django.core.management.base import BaseCommand

from project.api import models

class Command(BaseCommand):
    help = 'Clear database'
    requires_migrations_checks = True
    requires_system_checks = True

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        models.Shop.objects.all().delete()
        models.ShopTag.objects.all().delete()
        models.Product.objects.all().delete()
        models.ProductTag.objects.all().delete()
        models.Price.objects.all().delete()
