from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance


class ShopTags(models.Model):
    tag = models.CharField(primary_key=True, max_length=255)


class ShopManager(models.Manager):
    def get_queryset(self):
        '''Omit withdrawn shops from results by default'''
        return super().get_queryset().filter(withdrawn=False)

    def within_distance_from(self, lat, lng, **distance):
        '''Find shops within given distance from given point.

        Arguments:
            - lat: Latitude of reference point.
            - lng: Longitude of reference point.
            - **distance: `Distance` arguments. For supported units see:
                https://docs.djangoproject.com/en/2.1/ref/contrib/gis/measure/#supported-units

        Example:
            ```
            shops = Shop.objects.within_distance_from(39.89, 22.18, km=10)
            ```
        '''
        return self.get_queryset().filter(
            coordinates__dwithin=(Point(lng, lat), Distance(**distance))
        )


class Shop(models.Model):
    '''Physical places where the products of our application are sold'''

    # Long integers are required from the specification
    id = models.BigAutoField(primary_key=True)

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    # We will use GeoDjango for storing and querying spatial data
    # https://docs.djangoproject.com/en/2.1/ref/contrib/gis/
    # geography=True will enable distance lookups that use metric
    # https://docs.djangoproject.com/en/2.1/ref/contrib/gis/model-api/#geography
    #
    # NOTE: If the field is set via Python and the Point model is used,
    # the syntax is Point(longitude, latitude).
    coordinates = models.PointField(geography=True)

    withdrawn = models.BooleanField(default=False)

    tags = models.ManyToManyField(ShopTags)

    objects = ShopManager()

    def __str__(self):
        return self.name
