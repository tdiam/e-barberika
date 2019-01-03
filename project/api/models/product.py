from django.db import models


class ProductTag(models.Model):
    tag = models.CharField(primary_key=True, max_length=255)

    def __str__(self):
        return self.tag


class BaseProductManager(models.Manager):
    def get_queryset(self):
        '''Omit withdrawn products from results by default'''
        return super().get_queryset().filter(withdrawn=False)


class ProductQuerySet(models.QuerySet):
    def with_tags(self, tags):

        return self.filter(
            tags__tag__in=tags
        ).distinct()

# Adapted from:
# https://docs.djangoproject.com/en/2.1/topics/db/managers/#from-queryset
ProductManager = BaseProductManager.from_queryset(ProductQuerySet)


class Product(models.Model):

    # Long integers are required from the specification
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)

    description = models.TextField()

    category = models.CharField(max_length=255)

    withdrawn = models.BooleanField(default=False)

    tags = models.ManyToManyField(ProductTag)

    objects = ProductManager()

    def __str__(self):
        return self.name
