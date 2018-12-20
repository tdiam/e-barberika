from django.contrib.gis.db import models


class ShopTags(models.Model):
    tag = models.CharField(primary_key=True, max_length=255)


class ShopManager(models.Manager):
    def get_queryset(self):
        '''Omit withdrawn shops from results by default'''
        return super().get_queryset().filter(withdrawn=False)


class Shop(models.Model):
    '''Physical places where the products of our application are sold'''
    
    # Long integers are required from the specification
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    # We will use GeoDjango for storing and querying spatial data
    # https://docs.djangoproject.com/en/2.1/ref/contrib/gis/
    coordinates = models.PointField()

    withdrawn = models.BooleanField(default=False)

    tags = models.ManyToManyField(ShopTags)

    objects = ShopManager()
